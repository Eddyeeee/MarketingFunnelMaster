#!/usr/bin/env python3
"""
Database Models Package
SQLAlchemy models for MarketingFunnelMaster Unified Backend

Executor: Claude Code
Erstellt: 2025-07-03
"""

# Import only existing models for now
from .users import User, UserProfile, UserSettings
from .leads import Lead, LeadQuizAnswer, LeadFunnel

# TODO: Import additional models as they are created
# from .websites import Website, WebsiteContent, WebsiteDomain
# from .analytics import AnalyticsEvent, PerformanceMetrics, ConversionData
# from .agents import AIAgent, AgentTask, AgentMessage, AgentPerformance
# from .products import Product, ProductCategory, ProductReview
# from .affiliates import AffiliateProgram, AffiliateLink, AffiliateCommission
# from .campaigns import Campaign, CampaignMetrics, EmailSequence

# Export existing models only
__all__ = [
    # User models
    "User",
    "UserProfile", 
    "UserSettings",
    
    # Lead models
    "Lead",
    "LeadQuizAnswer",
    "LeadFunnel"
]