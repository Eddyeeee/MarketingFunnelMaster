# Journey API Models for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
from enum import Enum
from uuid import UUID

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class JourneyStage(str, Enum):
    """Journey stages enum"""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    DECISION = "decision"
    CONVERSION = "conversion"
    RETENTION = "retention"

class DeviceType(str, Enum):
    """Device types enum"""
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

class JourneyPath(str, Enum):
    """Predefined journey paths"""
    MOBILE_TIKTOK_FAST_TRACK = "mobile_tiktok_fast_track"
    DESKTOP_RESEARCH_DEEP = "desktop_research_deep"
    RETURNING_VISITOR_PERSONALIZED = "returning_visitor_personalized"
    STANDARD_CONVERSION_FUNNEL = "standard_conversion_funnel"

class TouchpointType(str, Enum):
    """Touchpoint types enum"""
    PAGE_VIEW = "page_view"
    INTERACTION = "interaction"
    CONVERSION_EVENT = "conversion_event"
    EXIT_INTENT = "exit_intent"
    STAGE_TRANSITION = "stage_transition"

class InteractionType(str, Enum):
    """Interaction types enum"""
    CLICK = "click"
    SCROLL = "scroll"
    SWIPE = "swipe"
    HOVER = "hover"
    FORM_FILL = "form_fill"
    ZOOM = "zoom"
    PLAY_VIDEO = "play_video"

# =============================================================================
# BASE MODELS
# =============================================================================

class PersonaData(BaseModel):
    """Persona information"""
    type: str = Field(..., description="Persona type (e.g., 'TechEarlyAdopter')")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Persona attributes")

class DeviceContext(BaseModel):
    """Device context information"""
    type: DeviceType = Field(..., description="Device type")
    screen_size: Optional[str] = Field(None, description="Screen resolution (e.g., '375x812')")
    user_agent: Optional[str] = Field(None, description="Browser user agent string")
    fingerprint: Optional[str] = Field(None, description="Device fingerprint")
    connection_speed: Optional[str] = Field(None, description="Connection speed (3g, 4g, wifi)")
    performance_budget: Optional[str] = Field(None, description="Performance budget level")

class EntryPoint(BaseModel):
    """Journey entry point information"""
    source: str = Field(..., description="Traffic source (tiktok, google, direct, etc.)")
    campaign: Optional[str] = Field(None, description="Campaign identifier")
    landing_page: str = Field(..., description="Landing page URL")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    referrer_video: Optional[str] = Field(None, description="Referrer video ID (for social media)")

class IntentSignals(BaseModel):
    """User intent signals"""
    purchase_intent: float = Field(..., ge=0.0, le=1.0, description="Purchase intent score")
    urgency_level: str = Field(..., description="Urgency level (low, medium, high)")
    price_sensitivity: str = Field(..., description="Price sensitivity level")
    research_depth: Optional[str] = Field(None, description="Research depth preference")

# =============================================================================
# REQUEST MODELS
# =============================================================================

class JourneySessionCreate(BaseModel):
    """Request model for creating a journey session"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[UUID] = Field(None, description="User ID if authenticated")
    persona: PersonaData = Field(..., description="Detected persona data")
    device_context: DeviceContext = Field(..., description="Device context information")
    entry_point: EntryPoint = Field(..., description="Journey entry point")
    intent_signals: IntentSignals = Field(..., description="Initial intent signals")
    utm_data: Optional[Dict[str, str]] = Field(default_factory=dict, description="UTM parameters")
    referrer_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Referrer data")
    returning_visitor_indicators: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Returning visitor data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Session start timestamp")

    @validator('session_id')
    def validate_session_id(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Session ID must be at least 10 characters long')
        return v

class EngagementMetrics(BaseModel):
    """Engagement metrics for touchpoint tracking"""
    time_on_page: int = Field(..., ge=0, description="Time spent on page in seconds")
    scroll_depth: float = Field(..., ge=0.0, le=1.0, description="Maximum scroll depth")
    interaction_count: int = Field(..., ge=0, description="Number of interactions")
    exit_intent: bool = Field(default=False, description="Exit intent detected")
    engagement_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Calculated engagement score")

class JourneyStageUpdate(BaseModel):
    """Request model for updating journey stage"""
    new_stage: JourneyStage = Field(..., description="New journey stage")
    trigger_event: str = Field(..., description="Event that triggered stage change")
    engagement_metrics: EngagementMetrics = Field(..., description="Current engagement metrics")
    contextual_data: Dict[str, Any] = Field(default_factory=dict, description="Additional context data")

class TouchpointData(BaseModel):
    """Touchpoint interaction data"""
    type: TouchpointType = Field(..., description="Type of touchpoint")
    page_url: str = Field(..., description="Page URL")
    interaction_data: Dict[str, Any] = Field(default_factory=dict, description="Specific interaction data")
    performance_metrics: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Performance metrics")

class TouchpointCreate(BaseModel):
    """Request model for creating a touchpoint"""
    session_id: str = Field(..., description="Journey session ID")
    touchpoint: TouchpointData = Field(..., description="Touchpoint data")
    contextual_signals: Dict[str, Any] = Field(default_factory=dict, description="Contextual signals")

class ConversionEventData(BaseModel):
    """Conversion event data"""
    type: str = Field(..., description="Conversion event type")
    value: float = Field(default=0.0, ge=0.0, description="Conversion value")
    funnel_step: str = Field(..., description="Funnel step where conversion occurred")
    conversion_data: Dict[str, Any] = Field(default_factory=dict, description="Additional conversion data")

class ConversionEventCreate(BaseModel):
    """Request model for creating a conversion event"""
    session_id: str = Field(..., description="Journey session ID")
    conversion_event: ConversionEventData = Field(..., description="Conversion event data")
    journey_context: Dict[str, Any] = Field(default_factory=dict, description="Journey context at conversion")

class OptimizationRequest(BaseModel):
    """Request model for journey optimization"""
    session_id: str = Field(..., description="Journey session ID")
    optimization_type: str = Field(..., description="Type of optimization to apply")
    optimization_parameters: Dict[str, Any] = Field(default_factory=dict, description="Optimization parameters")
    contextual_constraints: Dict[str, Any] = Field(default_factory=dict, description="Contextual constraints")

# =============================================================================
# RESPONSE MODELS
# =============================================================================

class JourneyState(BaseModel):
    """Current journey state"""
    current_stage: JourneyStage = Field(..., description="Current journey stage")
    personalized_path: JourneyPath = Field(..., description="Assigned journey path")
    conversion_probability: float = Field(..., ge=0.0, le=1.0, description="Conversion probability")
    next_optimal_touchpoint: str = Field(..., description="Next recommended touchpoint")
    estimated_time_to_decision: Optional[str] = Field(None, description="Estimated time to decision")
    journey_progress: Optional[float] = Field(None, ge=0.0, le=1.0, description="Journey completion progress")

class PersonalizedContent(BaseModel):
    """Personalized content recommendations"""
    hero_message: str = Field(..., description="Main hero message")
    call_to_action: str = Field(..., description="Primary call to action")
    trust_signals: List[str] = Field(default_factory=list, description="Trust signals to display")
    scarcity_trigger: Optional[str] = Field(None, description="Scarcity trigger message")
    social_proof: Optional[str] = Field(None, description="Social proof content")
    personalization_strategy: Optional[str] = Field(None, description="Applied personalization strategy")

class JourneySessionResponse(BaseModel):
    """Response model for journey session creation"""
    success: bool = Field(..., description="Operation success status")
    session_id: str = Field(..., description="Journey session ID")
    journey_state: JourneyState = Field(..., description="Current journey state")
    personalized_content: PersonalizedContent = Field(..., description="Personalized content")
    next_actions: Optional[List[str]] = Field(default_factory=list, description="Recommended next actions")

class PersonalizedRecommendation(BaseModel):
    """Personalized recommendation"""
    type: str = Field(..., description="Recommendation type")
    content: str = Field(..., description="Recommendation content")
    priority: str = Field(..., description="Priority level (high, medium, low)")
    expected_impact: Optional[float] = Field(None, description="Expected impact score")

class ScarcityTrigger(BaseModel):
    """Scarcity trigger data"""
    trigger_type: str = Field(..., description="Type of scarcity trigger")
    message: str = Field(..., description="Scarcity message")
    intensity: str = Field(..., description="Intensity level")
    timing: str = Field(..., description="Optimal timing")
    authenticity: str = Field(..., description="Authenticity level")

class JourneyStateResponse(BaseModel):
    """Response model for journey state updates"""
    success: bool = Field(..., description="Operation success status")
    updated_journey_state: JourneyState = Field(..., description="Updated journey state")
    personalized_recommendations: List[PersonalizedRecommendation] = Field(default_factory=list, description="Personalized recommendations")
    scarcity_triggers: List[ScarcityTrigger] = Field(default_factory=list, description="Applied scarcity triggers")
    real_time_adaptations: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Real-time adaptations applied")

class TouchpointImpact(BaseModel):
    """Touchpoint impact metrics"""
    engagement_delta: float = Field(..., description="Change in engagement score")
    conversion_probability_change: float = Field(..., description="Change in conversion probability")
    next_recommended_action: str = Field(..., description="Next recommended action")

class TouchpointResponse(BaseModel):
    """Response model for touchpoint tracking"""
    success: bool = Field(..., description="Operation success status")
    touchpoint_id: str = Field(..., description="Created touchpoint ID")
    journey_impact: TouchpointImpact = Field(..., description="Impact on journey metrics")
    real_time_adaptation: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Applied real-time adaptations")

class ConversionResponse(BaseModel):
    """Response model for conversion event tracking"""
    success: bool = Field(..., description="Operation success status")
    conversion_id: str = Field(..., description="Created conversion event ID")
    journey_complete: bool = Field(..., description="Whether journey is complete")
    next_journey_goal: Optional[str] = Field(None, description="Next journey goal")
    personalized_nurturing: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Personalized nurturing strategy")

class OptimizationResult(BaseModel):
    """Optimization result"""
    type: str = Field(..., description="Optimization type")
    change: str = Field(..., description="Applied change")
    expected_impact: float = Field(..., description="Expected impact score")

class OptimizationResponse(BaseModel):
    """Response model for journey optimization"""
    success: bool = Field(..., description="Operation success status")
    optimizations_applied: List[OptimizationResult] = Field(default_factory=list, description="Applied optimizations")
    total_expected_lift: float = Field(..., description="Total expected performance lift")
    implementation_time: str = Field(..., description="Implementation timing")

# =============================================================================
# ANALYTICS MODELS
# =============================================================================

class FunnelStageMetrics(BaseModel):
    """Funnel stage performance metrics"""
    visitors: int = Field(..., description="Number of visitors")
    conversion_rate: float = Field(..., description="Conversion rate to next stage")
    average_time: int = Field(..., description="Average time in stage (seconds)")
    drop_off_reasons: List[str] = Field(default_factory=list, description="Main drop-off reasons")

class FunnelAnalytics(BaseModel):
    """Funnel performance analytics"""
    awareness: FunnelStageMetrics = Field(..., description="Awareness stage metrics")
    consideration: FunnelStageMetrics = Field(..., description="Consideration stage metrics")
    decision: FunnelStageMetrics = Field(..., description="Decision stage metrics")
    purchase: FunnelStageMetrics = Field(..., description="Purchase stage metrics")
    optimization_opportunities: List[Dict[str, Any]] = Field(default_factory=list, description="Optimization opportunities")

class CohortCharacteristics(BaseModel):
    """Cohort characteristics"""
    cohort_size: int = Field(..., description="Size of the cohort")
    conversion_rate: float = Field(..., description="Cohort conversion rate")
    average_time_to_conversion: int = Field(..., description="Average time to conversion (seconds)")
    lifetime_value: float = Field(..., description="Average lifetime value")
    characteristics: List[str] = Field(default_factory=list, description="Key characteristics")

class CohortAnalytics(BaseModel):
    """Cohort analysis data"""
    mobile_video_traffic: CohortCharacteristics = Field(..., description="Mobile video traffic cohort")
    desktop_researchers: CohortCharacteristics = Field(..., description="Desktop researchers cohort")
    returning_customers: CohortCharacteristics = Field(..., description="Returning customers cohort")

# =============================================================================
# ERROR MODELS
# =============================================================================

class JourneyError(BaseModel):
    """Journey API error response"""
    error: bool = Field(default=True, description="Error flag")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

# =============================================================================
# CONFIGURATION MODELS
# =============================================================================

class JourneyConfig(BaseModel):
    """Journey configuration settings"""
    max_session_duration: int = Field(default=3600, description="Maximum session duration in seconds")
    touchpoint_timeout: int = Field(default=30, description="Touchpoint timeout in seconds")
    optimization_interval: int = Field(default=60, description="Optimization check interval in seconds")
    personalization_threshold: float = Field(default=0.7, description="Minimum confidence for personalization")
    scarcity_trigger_cooldown: int = Field(default=300, description="Scarcity trigger cooldown in seconds")

# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_session_id(session_id: str) -> bool:
    """Validate session ID format"""
    return len(session_id) >= 10 and session_id.isalnum()

def validate_probability_score(score: float) -> bool:
    """Validate probability score range"""
    return 0.0 <= score <= 1.0

def validate_journey_stage_transition(current: JourneyStage, new: JourneyStage) -> bool:
    """Validate journey stage transition logic"""
    valid_transitions = {
        JourneyStage.AWARENESS: [JourneyStage.CONSIDERATION, JourneyStage.DECISION],
        JourneyStage.CONSIDERATION: [JourneyStage.DECISION, JourneyStage.CONVERSION],
        JourneyStage.DECISION: [JourneyStage.CONVERSION, JourneyStage.RETENTION],
        JourneyStage.CONVERSION: [JourneyStage.RETENTION],
        JourneyStage.RETENTION: []  # Terminal stage
    }
    return new in valid_transitions.get(current, [])