#!/usr/bin/env python3
"""
API Key Service for AI Agent Authentication
Secure agent-to-agent communication with scoped permissions

Executor: Claude Code
Erstellt: 2025-07-03
"""

import secrets
import hashlib
import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import logging

from config.settings import settings
from .permissions import AgentPermissions

logger = logging.getLogger(__name__)

class APIKeyData(BaseModel):
    """API Key data structure"""
    key_id: str
    agent_type: str
    agent_instance_id: str
    user_id: str
    scopes: List[str]
    metadata: Dict[str, Any]
    is_active: bool = True

class RateLimitConfig(BaseModel):
    """Rate limit configuration"""
    requests_per_minute: int
    requests_per_hour: int
    concurrent_requests: int

class APIKeyService:
    """API Key management service for AI agents"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.key_prefix = "mfm_agent_"
        self.metadata_prefix = "api_key_meta:"
        self.rate_limit_prefix = "rate_limit:"
        
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
            logger.info("✅ API Key Service Redis connection established")
        except Exception as e:
            logger.error(f"❌ API Key Service Redis connection failed: {e}")
            raise
    
    async def create_agent_api_key(
        self,
        user_id: str,
        agent_type: str,
        agent_instance_id: str,
        custom_scopes: Optional[List[str]] = None,
        expires_in_days: int = 365,
        custom_rate_limits: Optional[RateLimitConfig] = None
    ) -> Dict[str, Any]:
        """Create API key for AI agent with scoped permissions"""
        
        if not self.redis_client:
            await self.initialize_redis()
        
        # Generate secure API key
        random_part = secrets.token_urlsafe(32)
        api_key = f"{self.key_prefix}{agent_type}_{random_part}"
        
        # Generate unique key ID
        key_id = f"ak_{secrets.token_urlsafe(8)}"
        
        # Get agent permissions (default + custom)
        default_scopes = AgentPermissions.get_agent_permissions(agent_type)
        scopes = list(set(default_scopes + (custom_scopes or [])))
        
        # Get rate limits
        rate_limits = custom_rate_limits or self._get_default_rate_limits(agent_type)
        
        # Create API key hash for secure storage
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Create comprehensive metadata
        metadata = {
            "key_id": key_id,
            "api_key_hash": api_key_hash,
            "agent_type": agent_type,
            "agent_instance_id": agent_instance_id,
            "user_id": user_id,
            "scopes": scopes,
            "rate_limits": {
                "requests_per_minute": rate_limits.requests_per_minute,
                "requests_per_hour": rate_limits.requests_per_hour,
                "concurrent_requests": rate_limits.concurrent_requests
            },
            "restrictions": self._get_agent_restrictions(agent_type),
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat(),
            "last_used": None,
            "usage_count": 0,
            "is_active": True,
            "performance_metrics": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0,
                "last_performance_update": datetime.utcnow().isoformat()
            }
        }
        
        # Calculate TTL in seconds
        ttl_seconds = expires_in_days * 24 * 60 * 60
        
        # Store metadata in Redis
        await self.redis_client.setex(
            f"{self.metadata_prefix}{key_id}",
            ttl_seconds,
            json.dumps(metadata)
        )
        
        # Store key hash mapping for fast lookup
        await self.redis_client.setex(
            f"api_key_hash:{api_key_hash}",
            ttl_seconds,
            key_id
        )
        
        # Add to user's API keys set
        await self.redis_client.sadd(f"user_api_keys:{user_id}", key_id)
        await self.redis_client.expire(f"user_api_keys:{user_id}", ttl_seconds)
        
        # Add to agent type index
        await self.redis_client.sadd(f"agent_keys:{agent_type}", key_id)
        await self.redis_client.expire(f"agent_keys:{agent_type}", ttl_seconds)
        
        logger.info(f"✅ API key created for {agent_type} agent (user: {user_id})")
        
        return {
            "api_key": api_key,
            "key_id": key_id,
            "agent_type": agent_type,
            "scopes": scopes,
            "rate_limits": rate_limits.dict(),
            "expires_at": metadata["expires_at"],
            "metadata": metadata
        }
    
    async def verify_api_key(self, api_key: str) -> Optional[APIKeyData]:
        """Verify API key and return metadata"""
        
        if not self.redis_client:
            await self.initialize_redis()
        
        try:
            # Hash the provided key for lookup
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Get key ID from hash
            key_id = await self.redis_client.get(f"api_key_hash:{key_hash}")
            if not key_id:
                logger.warning("❌ API key not found")
                return None
            
            # Get metadata
            metadata_json = await self.redis_client.get(f"{self.metadata_prefix}{key_id}")
            if not metadata_json:
                logger.warning(f"❌ API key metadata not found for key_id: {key_id}")
                return None
            
            metadata = json.loads(metadata_json)
            
            # Check if key is active
            if not metadata.get("is_active", False):
                logger.warning(f"❌ API key is inactive: {key_id}")
                return None
            
            # Check expiration
            expires_at = datetime.fromisoformat(metadata["expires_at"])
            if datetime.utcnow() > expires_at:
                logger.warning(f"❌ API key expired: {key_id}")
                await self._deactivate_api_key(key_id, "expired")
                return None
            
            # Update usage statistics
            await self._update_api_key_usage(key_id, metadata)
            
            # Return structured API key data
            api_key_data = APIKeyData(
                key_id=metadata["key_id"],
                agent_type=metadata["agent_type"],
                agent_instance_id=metadata["agent_instance_id"],
                user_id=metadata["user_id"],
                scopes=metadata["scopes"],
                metadata=metadata,
                is_active=metadata["is_active"]
            )
            
            logger.debug(f"✅ API key verified: {agent_type} agent")
            
            return api_key_data
            
        except Exception as e:
            logger.error(f"❌ API key verification error: {e}")
            return None
    
    async def check_rate_limits(self, key_id: str, metadata: Dict[str, Any]) -> bool:
        """Check if API key is within rate limits"""
        
        rate_limits = metadata["rate_limits"]
        current_time = datetime.utcnow()
        
        # Check requests per minute
        minute_key = f"{self.rate_limit_prefix}minute:{key_id}:{int(current_time.timestamp() // 60)}"
        minute_count = await self.redis_client.get(minute_key)
        minute_count = int(minute_count) if minute_count else 0
        
        if minute_count >= rate_limits["requests_per_minute"]:
            logger.warning(f"❌ Minute rate limit exceeded for key: {key_id}")
            return False
        
        # Check requests per hour
        hour_key = f"{self.rate_limit_prefix}hour:{key_id}:{int(current_time.timestamp() // 3600)}"
        hour_count = await self.redis_client.get(hour_key)
        hour_count = int(hour_count) if hour_count else 0
        
        if hour_count >= rate_limits["requests_per_hour"]:
            logger.warning(f"❌ Hour rate limit exceeded for key: {key_id}")
            return False
        
        # Check concurrent requests
        concurrent_key = f"{self.rate_limit_prefix}concurrent:{key_id}"
        concurrent_count = await self.redis_client.get(concurrent_key)
        concurrent_count = int(concurrent_count) if concurrent_count else 0
        
        if concurrent_count >= rate_limits["concurrent_requests"]:
            logger.warning(f"❌ Concurrent request limit exceeded for key: {key_id}")
            return False
        
        # Increment counters
        pipe = self.redis_client.pipeline()
        
        # Increment minute counter
        pipe.incr(minute_key)
        pipe.expire(minute_key, 60)
        
        # Increment hour counter
        pipe.incr(hour_key)
        pipe.expire(hour_key, 3600)
        
        # Increment concurrent counter (will be decremented when request completes)
        pipe.incr(concurrent_key)
        pipe.expire(concurrent_key, 300)  # 5 minute safety timeout
        
        await pipe.execute()
        
        return True
    
    async def decrement_concurrent_requests(self, key_id: str):
        """Decrement concurrent request counter when request completes"""
        concurrent_key = f"{self.rate_limit_prefix}concurrent:{key_id}"
        await self.redis_client.decr(concurrent_key)
    
    async def check_agent_permissions(
        self, 
        api_key_data: APIKeyData, 
        required_scope: str,
        target_agent: Optional[str] = None
    ) -> bool:
        """Check if agent has required permissions for operation"""
        
        # Check if agent has required scope
        if required_scope not in api_key_data.scopes:
            logger.warning(
                f"❌ Agent {api_key_data.agent_type} missing scope: {required_scope}"
            )
            return False
        
        # Check agent-to-agent communication restrictions
        if target_agent:
            restrictions = api_key_data.metadata.get("restrictions", {})
            allowed_agents = restrictions.get("allowed_agents", [])
            
            # Empty list means can communicate with all agents
            if allowed_agents and target_agent not in allowed_agents:
                logger.warning(
                    f"❌ Agent {api_key_data.agent_type} not allowed to communicate with {target_agent}"
                )
                return False
        
        # Check forbidden operations
        restrictions = api_key_data.metadata.get("restrictions", {})
        forbidden_operations = restrictions.get("forbidden_operations", [])
        
        if required_scope in forbidden_operations:
            logger.warning(
                f"❌ Operation {required_scope} is forbidden for agent {api_key_data.agent_type}"
            )
            return False
        
        return True
    
    async def list_user_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """List all API keys for a user"""
        
        try:
            # Get user's API key IDs
            key_ids = await self.redis_client.smembers(f"user_api_keys:{user_id}")
            
            api_keys = []
            for key_id in key_ids:
                metadata_json = await self.redis_client.get(f"{self.metadata_prefix}{key_id}")
                if metadata_json:
                    metadata = json.loads(metadata_json)
                    
                    # Don't include the actual API key hash in response
                    safe_metadata = {
                        "key_id": metadata["key_id"],
                        "agent_type": metadata["agent_type"],
                        "agent_instance_id": metadata["agent_instance_id"],
                        "scopes": metadata["scopes"],
                        "created_at": metadata["created_at"],
                        "expires_at": metadata["expires_at"],
                        "last_used": metadata["last_used"],
                        "usage_count": metadata["usage_count"],
                        "is_active": metadata["is_active"],
                        "performance_metrics": metadata.get("performance_metrics", {})
                    }
                    api_keys.append(safe_metadata)
            
            return api_keys
            
        except Exception as e:
            logger.error(f"❌ Error listing API keys for user {user_id}: {e}")
            return []
    
    async def revoke_api_key(self, key_id: str, reason: str = "manual_revocation") -> bool:
        """Revoke API key"""
        
        try:
            # Get metadata
            metadata_json = await self.redis_client.get(f"{self.metadata_prefix}{key_id}")
            if not metadata_json:
                return False
            
            metadata = json.loads(metadata_json)
            
            # Deactivate the key
            await self._deactivate_api_key(key_id, reason)
            
            logger.info(f"✅ API key revoked: {key_id} (reason: {reason})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error revoking API key {key_id}: {e}")
            return False
    
    async def rotate_api_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Rotate API key (create new key with same settings)"""
        
        try:
            # Get current metadata
            metadata_json = await self.redis_client.get(f"{self.metadata_prefix}{key_id}")
            if not metadata_json:
                return None
            
            current_metadata = json.loads(metadata_json)
            
            # Create new API key with same settings
            new_key_result = await self.create_agent_api_key(
                user_id=current_metadata["user_id"],
                agent_type=current_metadata["agent_type"],
                agent_instance_id=current_metadata["agent_instance_id"],
                custom_scopes=current_metadata["scopes"],
                expires_in_days=365  # Default 1 year
            )
            
            # Deactivate old key
            await self._deactivate_api_key(key_id, "rotated")
            
            logger.info(f"✅ API key rotated: {key_id} -> {new_key_result['key_id']}")
            
            return new_key_result
            
        except Exception as e:
            logger.error(f"❌ Error rotating API key {key_id}: {e}")
            return None
    
    def _get_default_rate_limits(self, agent_type: str) -> RateLimitConfig:
        """Get default rate limits based on agent type"""
        
        limits_mapping = {
            "opportunity_scanner": RateLimitConfig(
                requests_per_minute=500,
                requests_per_hour=10000,
                concurrent_requests=50
            ),
            "content_generator": RateLimitConfig(
                requests_per_minute=200,
                requests_per_hour=5000,
                concurrent_requests=20
            ),
            "website_builder": RateLimitConfig(
                requests_per_minute=100,
                requests_per_hour=2000,
                concurrent_requests=10
            ),
            "seo_optimizer": RateLimitConfig(
                requests_per_minute=300,
                requests_per_hour=7500,
                concurrent_requests=30
            ),
            "monetization_agent": RateLimitConfig(
                requests_per_minute=150,
                requests_per_hour=3000,
                concurrent_requests=15
            ),
            "default": RateLimitConfig(
                requests_per_minute=100,
                requests_per_hour=1000,
                concurrent_requests=5
            )
        }
        
        return limits_mapping.get(agent_type, limits_mapping["default"])
    
    def _get_agent_restrictions(self, agent_type: str) -> Dict[str, Any]:
        """Get security restrictions based on agent type"""
        
        base_restrictions = {
            "allowed_ips": ["0.0.0.0/0"],  # Allow all IPs by default
            "allowed_agents": [],  # Empty means can communicate with all agents
            "forbidden_operations": [
                "users.delete",
                "billing.modify",
                "admin.access",
                "system.all"
            ],
            "max_data_retention_days": 30,
            "require_encryption": True
        }
        
        # Agent-specific restrictions
        agent_specific_restrictions = {
            "opportunity_scanner": {
                "max_data_retention_days": 7,  # Shorter retention for market data
                "allowed_agents": ["content_generator", "website_builder"]
            },
            "content_generator": {
                "max_data_retention_days": 14,
                "allowed_agents": ["seo_optimizer", "website_builder"]
            },
            "website_builder": {
                "forbidden_operations": base_restrictions["forbidden_operations"] + [
                    "leads.delete",
                    "campaigns.delete"
                ]
            }
        }
        
        # Merge base restrictions with agent-specific ones
        restrictions = base_restrictions.copy()
        if agent_type in agent_specific_restrictions:
            restrictions.update(agent_specific_restrictions[agent_type])
        
        return restrictions
    
    async def _update_api_key_usage(self, key_id: str, metadata: Dict[str, Any]):
        """Update API key usage statistics"""
        
        try:
            # Update usage count and last used timestamp
            metadata["usage_count"] = metadata.get("usage_count", 0) + 1
            metadata["last_used"] = datetime.utcnow().isoformat()
            
            # Update performance metrics (placeholder)
            performance = metadata.get("performance_metrics", {})
            performance["total_requests"] = performance.get("total_requests", 0) + 1
            performance["last_performance_update"] = datetime.utcnow().isoformat()
            metadata["performance_metrics"] = performance
            
            # Get remaining TTL
            ttl = await self.redis_client.ttl(f"{self.metadata_prefix}{key_id}")
            if ttl > 0:
                await self.redis_client.setex(
                    f"{self.metadata_prefix}{key_id}",
                    ttl,
                    json.dumps(metadata)
                )
                
        except Exception as e:
            logger.error(f"❌ Error updating API key usage for {key_id}: {e}")
    
    async def _deactivate_api_key(self, key_id: str, reason: str):
        """Deactivate API key"""
        
        try:
            # Get current metadata
            metadata_json = await self.redis_client.get(f"{self.metadata_prefix}{key_id}")
            if metadata_json:
                metadata = json.loads(metadata_json)
                
                # Mark as inactive
                metadata["is_active"] = False
                metadata["deactivated_at"] = datetime.utcnow().isoformat()
                metadata["deactivation_reason"] = reason
                
                # Update metadata
                ttl = await self.redis_client.ttl(f"{self.metadata_prefix}{key_id}")
                if ttl > 0:
                    await self.redis_client.setex(
                        f"{self.metadata_prefix}{key_id}",
                        ttl,
                        json.dumps(metadata)
                    )
                
                # Remove from hash lookup (prevents future authentication)
                api_key_hash = metadata["api_key_hash"]
                await self.redis_client.delete(f"api_key_hash:{api_key_hash}")
                
        except Exception as e:
            logger.error(f"❌ Error deactivating API key {key_id}: {e}")
    
    async def get_agent_statistics(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for agents"""
        
        try:
            stats = {
                "total_keys": 0,
                "active_keys": 0,
                "by_agent_type": {},
                "usage_stats": {
                    "total_requests_today": 0,
                    "active_agents_now": 0
                }
            }
            
            # Get all agent keys for specific type or all types
            if agent_type:
                key_ids = await self.redis_client.smembers(f"agent_keys:{agent_type}")
                agent_types = [agent_type]
            else:
                # Get all agent types
                agent_types = [
                    "opportunity_scanner", "content_generator", "website_builder",
                    "seo_optimizer", "monetization_agent"
                ]
                key_ids = set()
                for atype in agent_types:
                    type_keys = await self.redis_client.smembers(f"agent_keys:{atype}")
                    key_ids.update(type_keys)
            
            # Analyze each key
            for key_id in key_ids:
                metadata_json = await self.redis_client.get(f"{self.metadata_prefix}{key_id}")
                if metadata_json:
                    metadata = json.loads(metadata_json)
                    
                    stats["total_keys"] += 1
                    
                    if metadata.get("is_active"):
                        stats["active_keys"] += 1
                    
                    # Count by agent type
                    atype = metadata["agent_type"]
                    if atype not in stats["by_agent_type"]:
                        stats["by_agent_type"][atype] = {
                            "total": 0,
                            "active": 0,
                            "total_requests": 0
                        }
                    
                    stats["by_agent_type"][atype]["total"] += 1
                    if metadata.get("is_active"):
                        stats["by_agent_type"][atype]["active"] += 1
                    
                    # Add request counts
                    performance = metadata.get("performance_metrics", {})
                    total_requests = performance.get("total_requests", 0)
                    stats["by_agent_type"][atype]["total_requests"] += total_requests
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting agent statistics: {e}")
            return {}

# Global API key service instance
api_key_service = APIKeyService()