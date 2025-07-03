#!/usr/bin/env python3
"""
Database Models Package
SQLAlchemy models for MarketingFunnelMaster Unified Backend

Executor: Claude Code
Erstellt: 2025-07-03
"""

# Import all models to ensure they're registered with SQLAlchemy Base
from .users import User, UserProfile, UserSettings
from .leads import Lead, LeadQuizAnswer, LeadFunnel
from .websites import Website, WebsiteContent, WebsiteDomain
from .analytics import AnalyticsEvent, PerformanceMetrics, ConversionData
from .agents import AIAgent, AgentTask, AgentMessage, AgentPerformance
from .products import Product, ProductCategory, ProductReview
from .affiliates import AffiliateProgram, AffiliateLink, AffiliateCommission
from .campaigns import Campaign, CampaignMetrics, EmailSequence

# Export all models
__all__ = [
    # User models
    "User",
    "UserProfile", 
    "UserSettings",
    
    # Lead models
    "Lead",
    "LeadQuizAnswer",
    "LeadFunnel",
    
    # Website models
    "Website",
    "WebsiteContent", 
    "WebsiteDomain",
    
    # Analytics models
    "AnalyticsEvent",
    "PerformanceMetrics",
    "ConversionData",
    
    # Agent models
    "AIAgent",
    "AgentTask",
    "AgentMessage",
    "AgentPerformance",
    
    # Product models
    "Product",
    "ProductCategory",
    "ProductReview",
    
    # Affiliate models
    "AffiliateProgram",
    "AffiliateLink", 
    "AffiliateCommission",
    
    # Campaign models
    "Campaign",
    "CampaignMetrics",
    "EmailSequence"
]