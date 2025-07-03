#!/usr/bin/env python3
"""
Authentication & Authorization Core Package
Multi-Tier Authentication Framework for MarketingFunnelMaster

Executor: Claude Code
Erstellt: 2025-07-03
"""

from .jwt_service import JWTService, TokenData
from .api_key_service import APIKeyService, APIKeyData
from .auth_dependencies import (
    get_current_user,
    get_current_user_optional,
    get_api_key_auth,
    require_permissions,
    require_admin
)
from .security_service import SecurityService, SecurityHardening
from .rate_limiter import RateLimiter
from .permissions import PermissionManager, UserRole

# Export all authentication components
__all__ = [
    # JWT Service
    "JWTService",
    "TokenData",
    
    # API Key Service  
    "APIKeyService",
    "APIKeyData",
    
    # FastAPI Dependencies
    "get_current_user",
    "get_current_user_optional", 
    "get_api_key_auth",
    "require_permissions",
    "require_admin",
    
    # Security Services
    "SecurityService",
    "SecurityHardening",
    
    # Rate Limiting
    "RateLimiter",
    
    # Permissions
    "PermissionManager",
    "UserRole"
]