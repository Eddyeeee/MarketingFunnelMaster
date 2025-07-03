#!/usr/bin/env python3
"""
Lead Models - Migration from existing Express.js schema
Preserves quiz answers, persona data, and funnel stages

Executor: Claude Code
Erstellt: 2025-07-03
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Integer, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum
from datetime import datetime
from typing import Optional, Dict, Any, List

class LeadStatus(str, enum.Enum):
    """Lead status enumeration"""
    NEW = "new"
    QUALIFIED = "qualified"
    NURTURING = "nurturing"
    CONVERTED = "converted"
    LOST = "lost"
    UNSUBSCRIBED = "unsubscribed"

class LeadSource(str, enum.Enum):
    """Lead source enumeration"""
    ORGANIC = "organic"
    PAID_ADS = "paid_ads"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    REFERRAL = "referral"
    DIRECT = "direct"
    AFFILIATE = "affiliate"
    QUIZ = "quiz"

class FunnelStage(str, enum.Enum):
    """Funnel stage enumeration"""
    AWARENESS = "awareness"
    INTEREST = "interest"
    CONSIDERATION = "consideration"
    INTENT = "intent"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    RETENTION = "retention"
    ADVOCACY = "advocacy"

class Lead(Base):
    """
    Lead model - migrated from existing Express.js schema
    Preserves all existing fields including quiz answers and persona data
    """
    __tablename__ = "leads"
    
    # Core fields (preserve existing structure)
    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    
    # Basic information
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    
    # Quiz data (preserve existing JSON structure)
    quiz_answers = Column(JSON)  # Preserve existing quiz answers structure
    quiz_score = Column(Integer)
    quiz_completed_at = Column(DateTime)
    
    # Persona and segmentation (preserve existing)
    persona = Column(String, index=True)  # Preserve existing persona classification
    persona_confidence = Column(Float)  # AI-generated confidence score
    persona_attributes = Column(JSON)  # Additional persona data
    
    # Funnel tracking (preserve existing)
    funnel_stage = Column(Enum(FunnelStage), default=FunnelStage.AWARENESS, index=True)
    funnel_stage_history = Column(JSON, default=list)  # Track stage progression
    
    # Lead qualification
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    lead_score = Column(Integer, default=0)  # 0-100 lead scoring
    source = Column(Enum(LeadSource), index=True)
    source_details = Column(JSON)  # Additional source information
    
    # Attribution and tracking
    utm_source = Column(String)
    utm_medium = Column(String)
    utm_campaign = Column(String)
    utm_term = Column(String)
    utm_content = Column(String)
    
    # Referral information
    referrer_url = Column(String)
    landing_page = Column(String)
    user_agent = Column(Text)
    ip_address = Column(String)
    
    # Geographic information
    country = Column(String)
    region = Column(String)
    city = Column(String)
    timezone = Column(String)
    
    # Engagement tracking
    first_touch = Column(DateTime)
    last_touch = Column(DateTime)
    total_sessions = Column(Integer, default=0)
    total_pageviews = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)  # in seconds
    
    # Communication preferences
    email_subscribed = Column(Boolean, default=True)
    sms_subscribed = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    
    # Lead nurturing
    last_email_sent = Column(DateTime)
    email_opens = Column(Integer, default=0)
    email_clicks = Column(Integer, default=0)
    unsubscribed_at = Column(DateTime)
    
    # Conversion tracking
    converted_at = Column(DateTime)
    conversion_value = Column(Float)
    conversion_product = Column(String)
    
    # Tags and categories
    tags = Column(JSON, default=list)  # Array of tag strings
    categories = Column(JSON, default=list)  # Array of category strings
    
    # Custom fields for flexibility
    custom_fields = Column(JSON, default=dict)
    
    # AI-generated insights
    ai_insights = Column(JSON)  # AI-generated lead insights
    predicted_ltv = Column(Float)  # Predicted lifetime value
    churn_probability = Column(Float)  # 0-1 probability of churn
    
    # Timestamps (preserve existing)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Foreign keys
    user_id = Column(String, ForeignKey("users.id"), index=True)
    assigned_to = Column(String, ForeignKey("users.id"))  # Sales rep assignment
    
    # Relationships
    user = relationship("User", back_populates="leads", foreign_keys=[user_id])
    quiz_answers_rel = relationship("LeadQuizAnswer", back_populates="lead", cascade="all, delete-orphan")
    funnel_activities = relationship("LeadFunnel", back_populates="lead", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lead(id='{self.id}', email='{self.email}', persona='{self.persona}')>"
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.name or self.email
    
    @property
    def is_qualified(self) -> bool:
        """Check if lead is qualified"""
        return self.status in [LeadStatus.QUALIFIED, LeadStatus.CONVERTED]
    
    @property
    def is_active(self) -> bool:
        """Check if lead is active (not lost or unsubscribed)"""
        return self.status not in [LeadStatus.LOST, LeadStatus.UNSUBSCRIBED]
    
    def add_tag(self, tag: str):
        """Add tag to lead"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove tag from lead"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def update_funnel_stage(self, new_stage: FunnelStage):
        """Update funnel stage and track history"""
        if not self.funnel_stage_history:
            self.funnel_stage_history = []
        
        if self.funnel_stage != new_stage:
            self.funnel_stage_history.append({
                "from_stage": self.funnel_stage.value if self.funnel_stage else None,
                "to_stage": new_stage.value,
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": None  # Could calculate time in previous stage
            })
            self.funnel_stage = new_stage

class LeadQuizAnswer(Base):
    """
    Detailed quiz answers - normalized from JSON for better querying
    """
    __tablename__ = "lead_quiz_answers"
    
    id = Column(String, primary_key=True, index=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False, index=True)
    
    # Quiz information
    quiz_id = Column(String, index=True)
    quiz_version = Column(String)
    question_id = Column(String, index=True)
    question_text = Column(Text)
    question_type = Column(String)  # multiple_choice, text, rating, etc.
    
    # Answer data
    answer_text = Column(Text)
    answer_value = Column(String)
    answer_score = Column(Integer)
    is_correct = Column(Boolean)
    
    # Additional metadata
    time_to_answer = Column(Integer)  # seconds
    answer_order = Column(Integer)  # order within quiz
    
    # Timestamps
    answered_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    
    # Relationship
    lead = relationship("Lead", back_populates="quiz_answers_rel")
    
    def __repr__(self):
        return f"<LeadQuizAnswer(lead_id='{self.lead_id}', question_id='{self.question_id}')>"

class LeadFunnel(Base):
    """
    Lead funnel activity tracking
    """
    __tablename__ = "lead_funnels"
    
    id = Column(String, primary_key=True, index=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False, index=True)
    
    # Funnel activity
    activity_type = Column(String, index=True)  # email_open, page_view, download, etc.
    activity_details = Column(JSON)
    funnel_stage = Column(Enum(FunnelStage), index=True)
    
    # Attribution
    source_campaign = Column(String)
    source_medium = Column(String)
    source_content = Column(String)
    
    # Event data
    event_value = Column(Float)  # monetary value if applicable
    event_properties = Column(JSON)  # additional event data
    
    # Timestamps
    occurred_at = Column(DateTime, default=func.now(), index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship
    lead = relationship("Lead", back_populates="funnel_activities")
    
    def __repr__(self):
        return f"<LeadFunnel(lead_id='{self.lead_id}', activity='{self.activity_type}')>"

# Database model metadata for migration
LEAD_MIGRATION_MAPPING = {
    # Maps old Express.js field names to new SQLAlchemy field names
    "leads": {
        "id": "id",
        "email": "email",
        "quizAnswers": "quiz_answers",  # Preserve JSON structure
        "persona": "persona",
        "funnelStage": "funnel_stage",
        "createdAt": "created_at",
        "updatedAt": "updated_at"
    }
}

# Persona classification helper
class PersonaClassifier:
    """Helper class for persona classification and insights"""
    
    PERSONA_DEFINITIONS = {
        "tech_early_adopter": {
            "name": "Tech Early Adopter",
            "description": "Loves trying new technology and gadgets",
            "characteristics": ["tech_savvy", "innovation_focused", "high_disposable_income"],
            "typical_products": ["smart_devices", "software", "tech_accessories"]
        },
        "remote_dad": {
            "name": "Remote Dad", 
            "description": "Working father balancing family and career",
            "characteristics": ["family_focused", "time_conscious", "value_oriented"],
            "typical_products": ["productivity_tools", "family_products", "time_savers"]
        },
        "student_hustler": {
            "name": "Student Hustler",
            "description": "Student looking for side income opportunities",
            "characteristics": ["budget_conscious", "learning_oriented", "opportunity_seeker"],
            "typical_products": ["courses", "tools", "side_hustles"]
        },
        "business_owner": {
            "name": "Business Owner",
            "description": "Entrepreneur focused on growing their business",
            "characteristics": ["roi_focused", "scaling_mindset", "efficiency_driven"],
            "typical_products": ["business_tools", "automation", "growth_solutions"]
        }
    }
    
    @classmethod
    def classify_from_quiz(cls, quiz_answers: Dict[str, Any]) -> Dict[str, Any]:
        """Classify persona based on quiz answers"""
        # This would contain the logic to analyze quiz answers
        # and determine the most likely persona
        
        # Placeholder implementation
        return {
            "persona": "tech_early_adopter",
            "confidence": 0.85,
            "attributes": cls.PERSONA_DEFINITIONS["tech_early_adopter"],
            "reasoning": ["High tech interest score", "Premium budget range"]
        }