#!/usr/bin/env python3
"""
FastAPI Authentication Dependencies
Provides dependency injection for authentication and authorization

Executor: Claude Code
Erstellt: 2025-07-03
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Callable
import logging

from .jwt_service import jwt_service, TokenData
from .api_key_service import api_key_service, APIKeyData
from .permissions import PermissionManager, UserRole
from models.users import User

logger = logging.getLogger(__name__)

# Security schemes
bearer_scheme = HTTPBearer(auto_error=False)
api_key_scheme = HTTPBearer(scheme_name="ApiKey", auto_error=False)

class AuthenticationError(HTTPException):
    """Custom authentication error"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationError(HTTPException):
    """Custom authorization error"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> TokenData:
    """
    Get current authenticated user from JWT token
    Raises HTTPException if authentication fails
    """
    if not credentials:
        raise AuthenticationError("Missing authentication credentials")
    
    try:
        # Verify JWT token
        payload = await jwt_service.verify_token(credentials.credentials)
        
        # Extract user data from token
        user_info = payload.get("user", {})
        session_info = payload.get("session", {})
        
        token_data = TokenData(
            user_id=user_info.get("id"),
            email=user_info.get("email"),
            role=user_info.get("role"),
            permissions=user_info.get("permissions", []),
            subscription_tier=user_info.get("subscription_tier"),
            session_id=session_info.get("session_id"),
            is_active=True
        )
        
        logger.debug(f"✅ User authenticated: {token_data.user_id}")
        
        return token_data
        
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        raise AuthenticationError("Authentication failed")

async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Optional[TokenData]:
    """
    Get current user if authenticated, otherwise return None
    Does not raise exceptions for missing/invalid credentials
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
    except Exception as e:
        logger.warning(f"⚠️ Optional authentication failed: {e}")
        return None

async def get_api_key_auth(
    credentials: HTTPAuthorizationCredentials = Depends(api_key_scheme)
) -> APIKeyData:
    """
    Authenticate using API key (for agent-to-agent communication)
    """
    if not credentials:
        raise AuthenticationError("Missing API key")
    
    try:
        # Verify API key
        api_key_data = await api_key_service.verify_api_key(credentials.credentials)
        
        if not api_key_data:
            raise AuthenticationError("Invalid API key")
        
        # Check rate limits
        if not await api_key_service.check_rate_limits(
            api_key_data.key_id, 
            api_key_data.metadata
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="API key rate limit exceeded"
            )
        
        logger.debug(f"✅ Agent authenticated: {api_key_data.agent_type}")
        
        return api_key_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API key authentication error: {e}")
        raise AuthenticationError("API key authentication failed")

def require_permissions(*required_permissions: str) -> Callable:
    """
    Dependency factory for requiring specific permissions
    Usage: @app.get("/", dependencies=[Depends(require_permissions("websites.read"))])
    """
    def permission_dependency(
        current_user: TokenData = Depends(get_current_user)
    ) -> TokenData:
        
        # Admin users have all permissions
        if current_user.role == UserRole.ADMIN.value:
            return current_user
        
        # Check if user has required permissions
        user_permissions = set(current_user.permissions)
        required_perms = set(required_permissions)
        
        if not required_perms.issubset(user_permissions):
            missing_perms = required_perms - user_permissions
            raise AuthorizationError(
                f"Missing required permissions: {', '.join(missing_perms)}"
            )
        
        return current_user
    
    return permission_dependency

def require_role(*required_roles: UserRole) -> Callable:
    """
    Dependency factory for requiring specific roles
    Usage: @app.get("/", dependencies=[Depends(require_role(UserRole.ADMIN))])
    """
    def role_dependency(
        current_user: TokenData = Depends(get_current_user)
    ) -> TokenData:
        
        allowed_roles = [role.value for role in required_roles]
        
        if current_user.role not in allowed_roles:
            raise AuthorizationError(
                f"Required role: {' or '.join(allowed_roles)}, got: {current_user.role}"
            )
        
        return current_user
    
    return role_dependency

def require_admin(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """
    Dependency for requiring admin role
    """
    if current_user.role != UserRole.ADMIN.value:
        raise AuthorizationError("Admin access required")
    
    return current_user

def require_subscription_tier(*required_tiers: str) -> Callable:
    """
    Dependency factory for requiring specific subscription tiers
    Usage: @app.get("/", dependencies=[Depends(require_subscription_tier("pro", "enterprise"))])
    """
    def subscription_dependency(
        current_user: TokenData = Depends(get_current_user)
    ) -> TokenData:
        
        if current_user.subscription_tier not in required_tiers:
            raise AuthorizationError(
                f"Required subscription tier: {' or '.join(required_tiers)}, "
                f"got: {current_user.subscription_tier}"
            )
        
        return current_user
    
    return subscription_dependency

def require_agent_scope(*required_scopes: str) -> Callable:
    """
    Dependency factory for requiring specific agent scopes
    Usage: @app.post("/", dependencies=[Depends(require_agent_scope("research.conduct"))])
    """
    def scope_dependency(
        api_key_data: APIKeyData = Depends(get_api_key_auth)
    ) -> APIKeyData:
        
        agent_scopes = set(api_key_data.scopes)
        required_scope_set = set(required_scopes)
        
        if not required_scope_set.issubset(agent_scopes):
            missing_scopes = required_scope_set - agent_scopes
            raise AuthorizationError(
                f"Missing required scopes: {', '.join(missing_scopes)}"
            )
        
        return api_key_data
    
    return scope_dependency

async def get_user_or_agent(
    user_credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    api_credentials: HTTPAuthorizationCredentials = Depends(api_key_scheme)
) -> dict:
    """
    Accept either user JWT token or agent API key
    Returns dict with 'type' and 'data' fields
    """
    
    # Try user authentication first
    if user_credentials:
        try:
            user_data = await get_current_user(user_credentials)
            return {
                "type": "user",
                "data": user_data
            }
        except HTTPException:
            pass
    
    # Try agent authentication
    if api_credentials:
        try:
            agent_data = await get_api_key_auth(api_credentials)
            return {
                "type": "agent", 
                "data": agent_data
            }
        except HTTPException:
            pass
    
    # Neither authentication method worked
    raise AuthenticationError("Valid user token or API key required")

class PermissionChecker:
    """Helper class for complex permission checking"""
    
    def __init__(self, current_user: TokenData):
        self.current_user = current_user
        self.permission_manager = PermissionManager()
    
    def has_permission(self, permission: str, resource_id: Optional[str] = None) -> bool:
        """Check if user has specific permission"""
        
        # Admin users have all permissions
        if self.current_user.role == UserRole.ADMIN.value:
            return True
        
        # Check basic permission
        if permission not in self.current_user.permissions:
            return False
        
        # Check resource-specific permissions (e.g., "websites.read:own")
        if resource_id and ":own" in permission:
            # This would typically check if the resource belongs to the user
            # Implementation would depend on the specific resource type
            return self._check_resource_ownership(permission, resource_id)
        
        return True
    
    def can_access_resource(self, resource_type: str, resource_id: str, action: str) -> bool:
        """Check if user can perform action on specific resource"""
        
        permission = f"{resource_type}.{action}"
        
        # Check if user has the permission
        if not self.has_permission(permission):
            # Check if user has permission for own resources
            own_permission = f"{permission}:own"
            if self.has_permission(own_permission):
                return self._check_resource_ownership(own_permission, resource_id)
            return False
        
        return True
    
    def _check_resource_ownership(self, permission: str, resource_id: str) -> bool:
        """Check if user owns the resource (placeholder implementation)"""
        # This would typically query the database to check ownership
        # For now, return True as placeholder
        return True

def get_permission_checker(
    current_user: TokenData = Depends(get_current_user)
) -> PermissionChecker:
    """Get permission checker instance for current user"""
    return PermissionChecker(current_user)

# Rate limiting dependencies
from .rate_limiter import RateLimiter

rate_limiter = RateLimiter()

def rate_limit(requests_per_minute: int = 60):
    """
    Rate limiting dependency
    Usage: @app.get("/", dependencies=[Depends(rate_limit(100))])
    """
    async def rate_limit_dependency(
        current_user: Optional[TokenData] = Depends(get_current_user_optional)
    ):
        user_id = current_user.user_id if current_user else "anonymous"
        
        if not await rate_limiter.check_rate_limit(user_id, requests_per_minute):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {requests_per_minute} requests per minute"
            )
    
    return rate_limit_dependency