# Database Models for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, DECIMAL, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import uuid

Base = declarative_base()

# =============================================================================
# JOURNEY SESSIONS TABLE
# =============================================================================

class JourneySession(Base):
    """Journey session model"""
    __tablename__ = "journey_sessions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # User identification
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Persona and device information
    persona_type = Column(String(50), nullable=True, index=True)
    persona_confidence = Column(Float, nullable=True)
    device_type = Column(String(20), nullable=True, index=True)
    device_fingerprint = Column(Text, nullable=True)
    
    # Journey state
    start_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    end_timestamp = Column(DateTime(timezone=True), nullable=True)
    current_stage = Column(String(50), nullable=True, index=True)
    journey_path = Column(String(100), nullable=True, index=True)
    
    # Metrics
    conversion_probability = Column(Float, nullable=True, index=True)
    total_touchpoints = Column(Integer, default=0)
    total_session_time = Column(Integer, default=0)  # in seconds
    
    # JSON data
    entry_point = Column(JSON, nullable=True)
    utm_data = Column(JSON, nullable=True)
    referrer_data = Column(JSON, nullable=True)
    exit_point = Column(JSON, nullable=True)
    conversion_events = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    touchpoints = relationship("JourneyTouchpoint", back_populates="session", cascade="all, delete-orphan")
    conversions = relationship("ConversionEvent", back_populates="session", cascade="all, delete-orphan")
    personalizations = relationship("PersonalizationData", back_populates="session", cascade="all, delete-orphan")
    scarcity_triggers = relationship("ScarcityTriggerEvent", back_populates="session", cascade="all, delete-orphan")
    optimizations = relationship("OptimizationEvent", back_populates="session", cascade="all, delete-orphan")

# =============================================================================
# JOURNEY TOUCHPOINTS TABLE
# =============================================================================

class JourneyTouchpoint(Base):
    """Journey touchpoint model"""
    __tablename__ = "journey_touchpoints"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), ForeignKey("journey_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Touchpoint data
    touchpoint_sequence = Column(Integer, nullable=False)
    touchpoint_type = Column(String(50), nullable=False, index=True)
    page_url = Column(Text, nullable=True)
    page_title = Column(String(255), nullable=True)
    
    # Interaction data
    interaction_type = Column(String(50), nullable=True, index=True)
    interaction_data = Column(JSON, nullable=True)
    
    # Metrics
    engagement_score = Column(Float, nullable=True, index=True)
    duration_seconds = Column(Integer, nullable=True)
    scroll_depth = Column(Float, nullable=True)
    click_count = Column(Integer, default=0)
    conversion_value = Column(DECIMAL(10, 2), default=0.00)
    
    # Context
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    device_context = Column(JSON, nullable=True)
    performance_metrics = Column(JSON, nullable=True)
    personalization_applied = Column(JSON, nullable=True)
    ab_test_variant = Column(String(50), nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("JourneySession", back_populates="touchpoints")

# =============================================================================
# CONVERSION EVENTS TABLE
# =============================================================================

class ConversionEvent(Base):
    """Conversion event model"""
    __tablename__ = "conversion_events"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), ForeignKey("journey_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Event data
    event_type = Column(String(50), nullable=False, index=True)
    event_value = Column(DECIMAL(10, 2), default=0.00, index=True)
    event_currency = Column(String(3), default="EUR")
    funnel_step = Column(String(50), nullable=True, index=True)
    
    # Attribution and revenue
    conversion_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    attribution_data = Column(JSON, nullable=True)
    product_data = Column(JSON, nullable=True)
    user_data = Column(JSON, nullable=True)
    campaign_data = Column(JSON, nullable=True)
    device_data = Column(JSON, nullable=True)
    revenue_attributed = Column(DECIMAL(10, 2), default=0.00)
    commission_earned = Column(DECIMAL(10, 2), default=0.00)
    lifetime_value_prediction = Column(DECIMAL(10, 2), nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("JourneySession", back_populates="conversions")

# =============================================================================
# PERSONALIZATION DATA TABLE
# =============================================================================

class PersonalizationData(Base):
    """Personalization data model"""
    __tablename__ = "personalization_data"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), ForeignKey("journey_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Personalization details
    personalization_type = Column(String(50), nullable=True, index=True)
    personalization_strategy = Column(String(100), nullable=True, index=True)
    variant_id = Column(String(100), nullable=True, index=True)
    content_delivered = Column(JSON, nullable=True)
    
    # Performance metrics
    performance_metrics = Column(JSON, nullable=True)
    user_response = Column(String(50), nullable=True)
    engagement_time = Column(Integer, nullable=True)
    conversion_attributed = Column(Boolean, default=False, index=True)
    
    # ML model data
    ml_model_version = Column(String(50), nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Timestamps
    applied_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("JourneySession", back_populates="personalizations")

# =============================================================================
# CROSS-DEVICE SESSIONS TABLE
# =============================================================================

class CrossDeviceSession(Base):
    """Cross-device session model"""
    __tablename__ = "cross_device_sessions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unified_session_id = Column(String(100), unique=True, nullable=False, index=True)
    primary_session_id = Column(String(100), ForeignKey("journey_sessions.session_id"), nullable=True, index=True)
    
    # Cross-device data
    linked_session_ids = Column(ARRAY(Text), nullable=True)
    user_identifier = Column(String(255), nullable=True, index=True)
    linking_method = Column(String(50), nullable=True, index=True)
    
    # Analytics
    device_sequence = Column(JSON, nullable=True)
    cross_device_insights = Column(JSON, nullable=True)
    total_cross_device_time = Column(Integer, nullable=True)
    unified_conversion_probability = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# =============================================================================
# UX INTELLIGENCE INTEGRATION BRIDGE TABLES
# =============================================================================

class UXJourneySessionBridge(Base):
    """Bridge table connecting UX Intelligence sessions with Journey sessions"""
    __tablename__ = "ux_journey_session_bridge"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Bridge data
    ux_session_id = Column(String(100), nullable=True, index=True)
    journey_session_id = Column(String(100), ForeignKey("journey_sessions.session_id"), nullable=False, index=True)
    integration_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data_flow_direction = Column(String(20), nullable=True)
    integration_status = Column(String(20), default="active", index=True)
    metadata = Column(JSON, nullable=True)

class PersonaJourneyEvolution(Base):
    """Persona evolution tracking through journey interactions"""
    __tablename__ = "persona_journey_evolution"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Evolution data
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    original_persona_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    evolved_persona_data = Column(JSON, nullable=True)
    evolution_triggers = Column(JSON, nullable=True)
    evolution_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    confidence_improvement = Column(Float, nullable=True)
    journey_context = Column(JSON, nullable=True)

# =============================================================================
# SCARCITY TRIGGER TRACKING TABLE
# =============================================================================

class ScarcityTriggerEvent(Base):
    """Scarcity trigger event model"""
    __tablename__ = "scarcity_trigger_events"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), ForeignKey("journey_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Trigger data
    trigger_type = Column(String(50), nullable=False, index=True)
    trigger_strategy = Column(String(100), nullable=True)
    trigger_content = Column(JSON, nullable=True)
    trigger_timing = Column(Integer, nullable=True)  # seconds into session
    
    # Response data
    user_response = Column(String(50), nullable=True)
    engagement_change = Column(Float, nullable=True)
    conversion_attributed = Column(Boolean, default=False, index=True)
    trigger_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("JourneySession", back_populates="scarcity_triggers")

# =============================================================================
# OPTIMIZATION TRACKING TABLE
# =============================================================================

class OptimizationEvent(Base):
    """Optimization event model for tracking real-time optimizations"""
    __tablename__ = "optimization_events"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), ForeignKey("journey_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Optimization data
    optimization_type = Column(String(50), nullable=False, index=True)
    optimization_strategy = Column(String(100), nullable=True, index=True)
    optimization_details = Column(JSON, nullable=True)
    optimization_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Impact measurement
    expected_impact = Column(Float, nullable=True)
    actual_impact = Column(Float, nullable=True)
    impact_measurement_timestamp = Column(DateTime(timezone=True), nullable=True)
    
    # Success metrics
    success_metrics = Column(JSON, nullable=True)
    optimization_success = Column(Boolean, nullable=True, index=True)
    
    # Additional metadata
    ml_model_version = Column(String(50), nullable=True)
    confidence_score = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("JourneySession", back_populates="optimizations")

# =============================================================================
# ANALYTICS MATERIALIZED VIEWS (represented as models for ORM)
# =============================================================================

class JourneyFunnelAnalytics(Base):
    """Journey funnel analytics materialized view"""
    __tablename__ = "journey_funnel_analytics"
    
    # Composite key fields
    journey_path = Column(String(100), primary_key=True)
    current_stage = Column(String(50), primary_key=True)
    device_type = Column(String(20), primary_key=True)
    persona_type = Column(String(50), primary_key=True)
    date = Column(DateTime(timezone=True), primary_key=True, index=True)
    
    # Metrics
    session_count = Column(Integer)
    avg_conversion_probability = Column(Float)
    avg_session_time = Column(Float)
    avg_touchpoints = Column(Float)
    conversions = Column(Integer)
    conversion_rate = Column(Float)

class PersonalizationPerformanceAnalytics(Base):
    """Personalization performance analytics materialized view"""
    __tablename__ = "personalization_performance_analytics"
    
    # Composite key fields
    personalization_type = Column(String(50), primary_key=True)
    personalization_strategy = Column(String(100), primary_key=True)
    variant_id = Column(String(100), primary_key=True)
    date = Column(DateTime(timezone=True), primary_key=True, index=True)
    
    # Metrics
    applications = Column(Integer)
    avg_engagement_time = Column(Float)
    conversions = Column(Integer)
    conversion_rate = Column(Float)
    avg_confidence = Column(Float)

# =============================================================================
# MIGRATION LOG TABLE
# =============================================================================

class MigrationLog(Base):
    """Migration log model"""
    __tablename__ = "migration_log"
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    migration_name = Column(String(255), unique=True, nullable=False)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(Text, nullable=True)
    rollback_script = Column(Text, nullable=True)

# =============================================================================
# EXTENDED EXISTING MODELS (placeholders for integration)
# =============================================================================

# Note: These would extend existing 2A models if they exist
# For now, we'll define them as new models for the journey engine

class ExtendedUserProfile(Base):
    """Extended user profile with journey data"""
    __tablename__ = "extended_user_profiles"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    
    # Journey-specific fields
    journey_history = Column(JSON, nullable=True)
    journey_preferences = Column(JSON, nullable=True)
    scarcity_sensitivity = Column(Float, nullable=True)
    personalization_consent = Column(Boolean, default=True)
    cross_device_consent = Column(Boolean, default=True)
    journey_history_summary = Column(JSON, nullable=True)
    last_journey_session_id = Column(String(100), nullable=True, index=True)
    preferred_journey_path = Column(String(100), nullable=True, index=True)
    conversion_patterns = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ExtendedPersonaProfile(Base):
    """Extended persona profile with journey insights"""
    __tablename__ = "extended_persona_profiles"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    persona_type = Column(String(50), nullable=False, index=True)
    
    # Journey-specific fields
    journey_behavior_patterns = Column(JSON, nullable=True)
    decision_speed = Column(String(20), nullable=True, index=True)
    personalization_receptivity = Column(String(20), nullable=True, index=True)
    journey_continuity_preference = Column(String(20), nullable=True, index=True)
    scarcity_trigger_preferences = Column(JSON, nullable=True)
    optimal_journey_timing = Column(JSON, nullable=True)
    cross_device_behavior = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# =============================================================================
# INDEX HINTS FOR PERFORMANCE
# =============================================================================

# Additional indexes will be created in migration scripts
# Key performance indexes:
# - journey_sessions: (session_id, current_stage, conversion_probability)
# - journey_touchpoints: (session_id, touchpoint_sequence)
# - conversion_events: (session_id, event_type, conversion_timestamp)
# - personalization_data: (session_id, personalization_type, conversion_attributed)
# - scarcity_trigger_events: (session_id, trigger_type, conversion_attributed)