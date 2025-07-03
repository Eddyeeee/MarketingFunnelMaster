#!/usr/bin/env python3
"""
JWT Service Implementation
Multi-Tier JWT Authentication with Redis Session Management

Executor: Claude Code
Erstellt: 2025-07-03
"""

import jwt
import json
import secrets
import hashlib
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

class TokenData(BaseModel):
    """Token data structure"""
    user_id: str
    email: str
    role: str
    permissions: List[str]
    subscription_tier: str
    session_id: str
    is_active: bool = True

class SessionData(BaseModel):
    """Session data structure"""
    session_id: str
    ip_address: str
    user_agent: str
    mfa_verified: bool = False
    risk_level: str = "medium"
    device_trusted: bool = False
    geo_location: str = "unknown"

class JWTService:
    """JWT token management service with Redis session storage"""
    
    def __init__(self):
        self.secret_key = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM
        self.issuer = "marketingfunnelmaster.com"
        self.audience = ["api.marketingfunnelmaster.com"]
        self.redis_client: Optional[redis.Redis] = None
        
    async def initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("✅ JWT Service Redis connection established")
        except Exception as e:
            logger.error(f"❌ JWT Service Redis connection failed: {e}")
            raise
    
    async def create_access_token(
        self, 
        user_id: str, 
        email: str,
        role: str,
        permissions: List[str],
        subscription_tier: str,
        session_data: SessionData,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token with comprehensive metadata"""
        
        if not self.redis_client:
            await self.initialize_redis()
        
        # Set expiration
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        # Generate unique token ID
        jti = f"jwt_{secrets.token_urlsafe(16)}"
        
        # Get user limits based on subscription tier
        user_limits = self._get_user_limits(subscription_tier)
        
        # Create JWT payload
        payload = {
            # Standard JWT claims
            "iss": self.issuer,
            "sub": user_id,
            "aud": self.audience,
            "exp": int(expire.timestamp()),
            "iat": int(datetime.utcnow().timestamp()),
            "nbf": int(datetime.utcnow().timestamp()),
            "jti": jti,
            
            # User information
            "user": {
                "id": user_id,
                "email": email,
                "role": role,
                "subscription_tier": subscription_tier,
                "permissions": permissions,
                "limits": user_limits
            },
            
            # Session information
            "session": {
                "session_id": session_data.session_id,
                "ip_address": session_data.ip_address,
                "user_agent_hash": self._hash_user_agent(session_data.user_agent),
                "created_at": int(datetime.utcnow().timestamp()),
                "last_activity": int(datetime.utcnow().timestamp())
            },
            
            # Security metadata
            "security": {
                "mfa_verified": session_data.mfa_verified,
                "risk_level": session_data.risk_level,
                "device_trusted": session_data.device_trusted,
                "geo_location": session_data.geo_location
            }
        }
        
        # Encode JWT token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store token metadata in Redis for tracking and blacklisting
        await self._store_token_metadata(jti, user_id, expire, session_data.session_id)
        
        # Store session data
        await self._store_session_data(session_data.session_id, user_id, session_data, expire)
        
        logger.info(f"✅ Access token created for user {user_id} (session: {session_data.session_id})")
        
        return token
    
    async def create_refresh_token(
        self, 
        user_id: str, 
        session_id: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create refresh token for token renewal"""
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=30)  # 30-day refresh token
        
        jti = f"refresh_{secrets.token_urlsafe(16)}"
        
        payload = {
            "iss": self.issuer,
            "sub": user_id,
            "aud": self.audience,
            "exp": int(expire.timestamp()),
            "iat": int(datetime.utcnow().timestamp()),
            "type": "refresh",
            "session_id": session_id,
            "jti": jti
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store refresh token metadata
        await self._store_refresh_token_metadata(jti, user_id, session_id, expire)
        
        logger.info(f"✅ Refresh token created for user {user_id}")
        
        return token
    
    async def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token with security checks"""
        
        if not self.redis_client:
            await self.initialize_redis()
        
        try:
            # Decode and verify JWT
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer
            )
            
            jti = payload.get("jti")
            if not jti:
                raise jwt.InvalidTokenError("Token missing JTI")
            
            # Check if token is blacklisted
            if await self._is_token_blacklisted(jti):
                raise jwt.InvalidTokenError("Token is blacklisted")
            
            # Verify token metadata exists
            token_metadata = await self._get_token_metadata(jti)
            if not token_metadata:
                raise jwt.InvalidTokenError("Token metadata not found")
            
            # Update last activity
            await self._update_token_activity(jti)
            
            logger.debug(f"✅ Token verified for user {payload.get('sub')}")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Token expired")
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ Invalid token: {str(e)}")
            raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Token verification error: {e}")
            raise jwt.InvalidTokenError(f"Token verification failed: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Create new access token using refresh token"""
        
        try:
            # Verify refresh token
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer
            )
            
            # Verify it's a refresh token
            if payload.get("type") != "refresh":
                raise jwt.InvalidTokenError("Not a refresh token")
            
            user_id = payload.get("sub")
            session_id = payload.get("session_id")
            jti = payload.get("jti")
            
            # Check if refresh token is blacklisted
            if await self._is_token_blacklisted(jti):
                raise jwt.InvalidTokenError("Refresh token is blacklisted")
            
            # Get current session data
            session_data = await self._get_session_data(session_id)
            if not session_data:
                raise jwt.InvalidTokenError("Session not found")
            
            # Get user data (would typically come from database)
            # For now, we'll use cached session data
            user_data = await self._get_user_data(user_id)
            if not user_data:
                raise jwt.InvalidTokenError("User not found")
            
            # Create new access token
            new_token = await self.create_access_token(
                user_id=user_id,
                email=user_data["email"],
                role=user_data["role"],
                permissions=user_data["permissions"],
                subscription_tier=user_data["subscription_tier"],
                session_data=SessionData.parse_obj(session_data)
            )
            
            logger.info(f"✅ Access token refreshed for user {user_id}")
            
            return new_token
            
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ Refresh token validation failed: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Token refresh error: {e}")
            return None
    
    async def blacklist_token(self, token: str, reason: str = "manual_logout"):
        """Add token to blacklist"""
        
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": False}  # Allow expired tokens for blacklisting
            )
            
            jti = payload.get("jti")
            if jti:
                # Add to blacklist with expiration time
                exp = payload.get("exp", 0)
                ttl = max(0, exp - int(datetime.utcnow().timestamp()))
                
                await self.redis_client.setex(
                    f"blacklist:{jti}",
                    ttl,
                    json.dumps({
                        "reason": reason,
                        "blacklisted_at": datetime.utcnow().isoformat()
                    })
                )
                
                logger.info(f"✅ Token blacklisted: {jti} (reason: {reason})")
                
        except Exception as e:
            logger.error(f"❌ Error blacklisting token: {e}")
    
    async def logout_session(self, session_id: str):
        """Logout session and blacklist all associated tokens"""
        
        try:
            # Get all tokens for session
            session_tokens = await self.redis_client.smembers(f"session_tokens:{session_id}")
            
            # Blacklist all tokens
            for jti in session_tokens:
                await self.redis_client.setex(
                    f"blacklist:{jti}",
                    86400,  # 24 hours
                    json.dumps({
                        "reason": "session_logout",
                        "blacklisted_at": datetime.utcnow().isoformat()
                    })
                )
            
            # Remove session data
            await self.redis_client.delete(f"session:{session_id}")
            await self.redis_client.delete(f"session_tokens:{session_id}")
            
            logger.info(f"✅ Session logged out: {session_id}")
            
        except Exception as e:
            logger.error(f"❌ Error logging out session: {e}")
    
    def _get_user_limits(self, subscription_tier: str) -> Dict:
        """Get user limits based on subscription tier"""
        limits_mapping = {
            "free": {
                "max_websites": 5,
                "max_ai_requests_per_month": 1000,
                "max_concurrent_agents": 2,
                "max_api_calls_per_minute": 10,
                "max_storage_mb": 100
            },
            "pro": {
                "max_websites": 100,
                "max_ai_requests_per_month": 10000,
                "max_concurrent_agents": 10,
                "max_api_calls_per_minute": 100,
                "max_storage_mb": 10000
            },
            "enterprise": {
                "max_websites": 1500,
                "max_ai_requests_per_month": 100000,
                "max_concurrent_agents": 50,
                "max_api_calls_per_minute": 1000,
                "max_storage_mb": 100000
            }
        }
        return limits_mapping.get(subscription_tier, limits_mapping["free"])
    
    def _hash_user_agent(self, user_agent: str) -> str:
        """Hash user agent for privacy and fingerprinting"""
        return hashlib.sha256(user_agent.encode()).hexdigest()[:16]
    
    async def _store_token_metadata(self, jti: str, user_id: str, expire: datetime, session_id: str):
        """Store token metadata in Redis"""
        
        metadata = {
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expire.isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "active": True
        }
        
        ttl = int((expire - datetime.utcnow()).total_seconds())
        
        # Store token metadata
        await self.redis_client.setex(
            f"token:{jti}",
            ttl,
            json.dumps(metadata)
        )
        
        # Add token to session token set
        await self.redis_client.sadd(f"session_tokens:{session_id}", jti)
        await self.redis_client.expire(f"session_tokens:{session_id}", ttl)
    
    async def _store_session_data(self, session_id: str, user_id: str, session_data: SessionData, expire: datetime):
        """Store session data in Redis"""
        
        session_info = {
            "user_id": user_id,
            "session_id": session_id,
            "ip_address": session_data.ip_address,
            "user_agent": session_data.user_agent,
            "mfa_verified": session_data.mfa_verified,
            "risk_level": session_data.risk_level,
            "device_trusted": session_data.device_trusted,
            "geo_location": session_data.geo_location,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat()
        }
        
        ttl = int((expire - datetime.utcnow()).total_seconds())
        
        await self.redis_client.setex(
            f"session:{session_id}",
            ttl,
            json.dumps(session_info)
        )
    
    async def _store_refresh_token_metadata(self, jti: str, user_id: str, session_id: str, expire: datetime):
        """Store refresh token metadata"""
        
        metadata = {
            "type": "refresh",
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expire.isoformat()
        }
        
        ttl = int((expire - datetime.utcnow()).total_seconds())
        
        await self.redis_client.setex(
            f"refresh_token:{jti}",
            ttl,
            json.dumps(metadata)
        )
    
    async def _is_token_blacklisted(self, jti: str) -> bool:
        """Check if token is blacklisted"""
        return await self.redis_client.exists(f"blacklist:{jti}")
    
    async def _get_token_metadata(self, jti: str) -> Optional[Dict]:
        """Get token metadata from Redis"""
        metadata_json = await self.redis_client.get(f"token:{jti}")
        if metadata_json:
            return json.loads(metadata_json)
        return None
    
    async def _get_session_data(self, session_id: str) -> Optional[Dict]:
        """Get session data from Redis"""
        session_json = await self.redis_client.get(f"session:{session_id}")
        if session_json:
            return json.loads(session_json)
        return None
    
    async def _get_user_data(self, user_id: str) -> Optional[Dict]:
        """Get user data (placeholder - would fetch from database)"""
        # This would typically fetch from database
        # For now, return mock data
        return {
            "email": "user@example.com",
            "role": "user", 
            "permissions": ["websites.read", "websites.create"],
            "subscription_tier": "pro"
        }
    
    async def _update_token_activity(self, jti: str):
        """Update token last activity timestamp"""
        metadata = await self._get_token_metadata(jti)
        if metadata:
            metadata["last_activity"] = datetime.utcnow().isoformat()
            
            # Get remaining TTL
            ttl = await self.redis_client.ttl(f"token:{jti}")
            if ttl > 0:
                await self.redis_client.setex(
                    f"token:{jti}",
                    ttl,
                    json.dumps(metadata)
                )
    
    async def cleanup_expired_tokens(self):
        """Cleanup expired tokens and sessions (background task)"""
        try:
            # This would be run as a background task
            # Redis automatically expires keys, but we can do additional cleanup
            
            # Get all session keys
            session_keys = await self.redis_client.keys("session:*")
            
            for session_key in session_keys:
                session_data = await self.redis_client.get(session_key)
                if session_data:
                    session_info = json.loads(session_data)
                    expires_at = datetime.fromisoformat(session_info.get("expires_at", ""))
                    
                    if datetime.utcnow() > expires_at:
                        # Remove expired session
                        await self.redis_client.delete(session_key)
                        
                        # Remove associated token references
                        session_id = session_key.replace("session:", "")
                        await self.redis_client.delete(f"session_tokens:{session_id}")
            
            logger.info("✅ Token cleanup completed")
            
        except Exception as e:
            logger.error(f"❌ Token cleanup error: {e}")

# Global JWT service instance
jwt_service = JWTService()