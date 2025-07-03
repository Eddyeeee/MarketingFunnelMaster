#!/usr/bin/env python3
"""
Authentication API Routes
Basic API endpoints for authentication testing

Executor: Claude Code
Erstellt: 2025-07-03
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from core.auth import get_current_user, JWTService, UserRole
from models.users import User
from config.database import get_db
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

# Response models
class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    role: UserRole
    is_active: bool
    is_verified: bool
    subscription_tier: str
    websites_count: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class AuthStatusResponse(BaseModel):
    authenticated: bool
    user: Optional[UserResponse] = None
    permissions: list[str] = []
    token_valid: bool = True
    expires_at: Optional[datetime] = None

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information
    Protected endpoint to test authentication
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return UserResponse.from_orm(current_user)

@router.get("/status", response_model=AuthStatusResponse)
async def get_auth_status(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get authentication status without requiring valid token
    Useful for frontend auth state management
    """
    if not credentials:
        return AuthStatusResponse(
            authenticated=False,
            token_valid=False
        )
    
    try:
        # Try to get current user
        jwt_service = JWTService()
        token_data = jwt_service.verify_token(credentials.credentials)
        
        if not token_data:
            return AuthStatusResponse(
                authenticated=False,
                token_valid=False
            )
        
        # Get user from database
        user = db.query(User).filter(User.id == token_data.user_id).first()
        
        if not user or not user.is_active:
            return AuthStatusResponse(
                authenticated=False,
                token_valid=False
            )
        
        return AuthStatusResponse(
            authenticated=True,
            user=UserResponse.from_orm(user),
            permissions=user.permissions or [],
            token_valid=True,
            expires_at=token_data.expires_at
        )
        
    except Exception:
        return AuthStatusResponse(
            authenticated=False,
            token_valid=False
        )

@router.post("/refresh")
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh authentication token
    """
    jwt_service = JWTService()
    new_token = jwt_service.create_access_token(user_id=current_user.id)
    
    return {
        "access_token": new_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(current_user)
    }

@router.get("/permissions")
async def get_user_permissions(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's permissions
    """
    return {
        "user_id": current_user.id,
        "role": current_user.role,
        "permissions": current_user.permissions or [],
        "is_admin": current_user.is_admin,
        "subscription_tier": current_user.subscription_tier
    }