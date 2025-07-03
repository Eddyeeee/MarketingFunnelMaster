#!/usr/bin/env python3
"""
User Models - Migration from Drizzle ORM to SQLAlchemy
Preserves existing data structure while adding new capabilities

Executor: Claude Code
Erstellt: 2025-07-03
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum
from datetime import datetime
from typing import Optional, Dict, Any

class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    AGENT = "agent"
    VIEWER = "viewer"

class UserStatus(str, enum.Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class User(Base):
    """
    User model - migrated from existing Drizzle schema
    Preserves all existing fields and adds new functionality
    """
    __tablename__ = "users"
    
    # Core fields (preserve existing structure)
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String)
    
    # Authentication fields
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Role and permissions
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    permissions = Column(JSON, default=list)  # List of permission strings
    
    # Timestamps (preserve existing)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime)
    
    # New fields for enhanced functionality
    subscription_tier = Column(String, default="free")  # free, pro, enterprise
    api_key = Column(String, unique=True, index=True)
    api_key_created_at = Column(DateTime)
    
    # Usage tracking
    websites_count = Column(Integer, default=0)
    ai_requests_count = Column(Integer, default=0)
    monthly_ai_requests = Column(Integer, default=0)
    last_ai_request = Column(DateTime)
    
    # Billing information
    stripe_customer_id = Column(String)
    subscription_status = Column(String)  # active, canceled, past_due, etc.
    subscription_ends_at = Column(DateTime)
    
    # Preferences and settings
    timezone = Column(String, default="UTC")
    language = Column(String, default="en")
    notification_preferences = Column(JSON, default=dict)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="user", cascade="all, delete-orphan")
    websites = relationship("Website", back_populates="owner", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', role='{self.role}')>"
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == UserRole.ADMIN
    
    @property
    def is_premium(self) -> bool:
        """Check if user has premium subscription"""
        return self.subscription_tier in ["pro", "enterprise"]
    
    @property
    def can_create_websites(self) -> bool:
        """Check if user can create more websites"""
        max_websites = {
            "free": 5,
            "pro": 100, 
            "enterprise": 1500
        }
        return self.websites_count < max_websites.get(self.subscription_tier, 5)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        if self.is_admin:
            return True
        return permission in (self.permissions or [])

class UserProfile(Base):
    """
    User profile with additional information
    """
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile information
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    job_title = Column(String)
    phone = Column(String)
    avatar_url = Column(String)
    
    # Address information
    country = Column(String)
    city = Column(String)
    address = Column(Text)
    postal_code = Column(String)
    
    # Business information
    business_type = Column(String)  # affiliate, ecommerce, saas, etc.
    business_size = Column(String)  # solo, small, medium, large
    primary_niche = Column(String)
    target_audience = Column(JSON)  # Array of audience segments
    
    # Marketing preferences
    marketing_goals = Column(JSON)  # Array of goals
    preferred_content_types = Column(JSON)  # Array of content types
    budget_range = Column(String)
    
    # Social media profiles
    social_profiles = Column(JSON, default=dict)  # {platform: url}
    
    # Bio and description
    bio = Column(Text)
    website_url = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id='{self.user_id}', company='{self.company}')>"
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        parts = [self.first_name, self.last_name]
        return " ".join(filter(None, parts)) or None

class UserSettings(Base):
    """
    User settings and preferences
    """
    __tablename__ = "user_settings"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Dashboard preferences
    dashboard_layout = Column(JSON, default=dict)
    default_view = Column(String, default="overview")
    theme = Column(String, default="light")  # light, dark, auto
    
    # Notification settings
    email_notifications = Column(Boolean, default=True)
    browser_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    
    # AI and automation settings
    ai_assistance_level = Column(String, default="balanced")  # minimal, balanced, aggressive
    auto_content_generation = Column(Boolean, default=True)
    auto_seo_optimization = Column(Boolean, default=True)
    auto_affiliate_suggestions = Column(Boolean, default=True)
    
    # Website generation preferences
    default_template = Column(String, default="nextjs-tailwind")
    preferred_color_scheme = Column(String)
    brand_colors = Column(JSON)  # Array of hex colors
    
    # Content preferences
    content_tone = Column(String, default="professional")  # casual, professional, authoritative
    content_length = Column(String, default="medium")  # short, medium, long
    target_reading_level = Column(String, default="general")  # beginner, general, expert
    
    # Analytics and reporting
    analytics_frequency = Column(String, default="weekly")  # daily, weekly, monthly
    report_recipients = Column(JSON, default=list)  # Array of email addresses
    
    # API and integration settings
    webhook_url = Column(String)
    api_rate_limit = Column(Integer, default=100)  # Requests per minute
    
    # Privacy settings
    data_sharing_consent = Column(Boolean, default=False)
    analytics_tracking = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=True)
    
    # Advanced settings
    experimental_features = Column(Boolean, default=False)
    beta_access = Column(Boolean, default=False)
    developer_mode = Column(Boolean, default=False)
    
    # Custom settings (for future extensibility)
    custom_settings = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="settings")
    
    def __repr__(self):
        return f"<UserSettings(user_id='{self.user_id}', theme='{self.theme}')>"
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get custom setting value"""
        return self.custom_settings.get(key, default) if self.custom_settings else default
    
    def set_setting(self, key: str, value: Any):
        """Set custom setting value"""
        if not self.custom_settings:
            self.custom_settings = {}
        self.custom_settings[key] = value

# Database model metadata for migration
USER_MIGRATION_MAPPING = {
    # Maps old Drizzle field names to new SQLAlchemy field names
    "users": {
        "id": "id",
        "email": "email", 
        "name": "name",
        "createdAt": "created_at",
        "updatedAt": "updated_at"
    }
}