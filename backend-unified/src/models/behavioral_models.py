"""
Behavioral Tracking Data Models
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Pydantic models for behavioral tracking, engagement analysis,
and real-time trigger responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid

# =============================================================================
# ENUMS
# =============================================================================

class EventType(str, Enum):
    PAGE_VIEW = "page_view"
    SCROLL = "scroll"
    CLICK = "click"
    HOVER = "hover"
    FORM_INTERACTION = "form_interaction"
    PURCHASE = "purchase"
    EXIT_INTENT = "exit_intent"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    CONVERSION = "conversion"
    ENGAGEMENT_THRESHOLD = "engagement_threshold"
    TIME_MILESTONE = "time_milestone"
    CUSTOM = "custom"

class EventCategory(str, Enum):
    NAVIGATION = "navigation"
    INTERACTION = "interaction"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    ERROR = "error"

class InteractionType(str, Enum):
    CLICK = "click"
    TOUCH = "touch"
    SWIPE = "swipe"
    SCROLL = "scroll"
    HOVER = "hover"
    FOCUS = "focus"
    BLUR = "blur"
    DRAG = "drag"
    PINCH = "pinch"
    ZOOM = "zoom"

class EngagementLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class BehaviorPattern(str, Enum):
    NEW_SESSION = "new_session"
    CONTENT_SCANNER = "content_scanner"
    RESEARCH_FOCUSED = "research_focused"
    HIGH_ENGAGEMENT = "high_engagement"
    DEEP_READER = "deep_reader"
    MOBILE_BROWSER = "mobile_browser"
    STANDARD_VISITOR = "standard_visitor"

# =============================================================================
# CORE MODELS
# =============================================================================

class ElementPosition(BaseModel):
    """Position and dimensions of an element"""
    x: int
    y: int
    width: Optional[int] = None
    height: Optional[int] = None

class ViewportInfo(BaseModel):
    """Viewport information"""
    width: int
    height: int
    device_pixel_ratio: Optional[float] = 1.0

class PerformanceMetrics(BaseModel):
    """Page performance metrics"""
    page_load_time: Optional[int] = None
    time_to_first_byte: Optional[int] = None
    dom_content_loaded: Optional[int] = None
    first_contentful_paint: Optional[int] = None
    largest_contentful_paint: Optional[int] = None
    cumulative_layout_shift: Optional[float] = None

class BehavioralEvent(BaseModel):
    """Core behavioral event model"""
    
    # Event identification
    event_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(..., min_length=1, max_length=100)
    user_id: Optional[str] = Field(None, max_length=100)
    
    # Event data
    event_type: EventType
    event_category: EventCategory
    event_action: str = Field(..., max_length=100)
    event_label: Optional[str] = Field(None, max_length=255)
    event_value: Optional[float] = None
    
    # Context data
    page_url: str = Field(..., max_length=2000)
    page_title: Optional[str] = Field(None, max_length=255)
    referrer: Optional[str] = Field(None, max_length=2000)
    user_agent: Optional[str] = Field(None, max_length=1000)
    viewport: Optional[ViewportInfo] = None
    
    # Interaction details
    element_id: Optional[str] = Field(None, max_length=100)
    element_class: Optional[str] = Field(None, max_length=255)
    element_text: Optional[str] = Field(None, max_length=1000)
    element_position: Optional[ElementPosition] = None
    interaction_type: Optional[InteractionType] = None
    interaction_duration: Optional[int] = None
    
    # Performance and engagement
    performance_metrics: Optional[PerformanceMetrics] = None
    time_on_page: Optional[int] = None
    scroll_depth: Optional[float] = Field(None, ge=0.0, le=1.0)
    engagement_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    # Custom properties
    custom_properties: Optional[Dict[str, Any]] = None
    
    # Timestamps
    client_timestamp: Optional[datetime] = None
    server_timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SessionMetrics(BaseModel):
    """Session-level behavioral metrics"""
    
    session_id: str
    user_id: Optional[str] = None
    
    # Session overview
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    page_count: int = 0
    event_count: int = 0
    
    # Engagement metrics
    total_scroll_depth: float = 0.0
    max_scroll_depth: float = 0.0
    avg_time_per_page: float = 0.0
    interaction_count: int = 0
    engagement_score: float = 0.0
    
    # Behavior classification
    dominant_pattern: BehaviorPattern = BehaviorPattern.STANDARD_VISITOR
    engagement_level: EngagementLevel = EngagementLevel.MEDIUM
    
    # Conversion indicators
    conversion_probability: float = 0.0
    intent_signals: List[str] = []
    
    # Device and context
    device_type: Optional[str] = None
    browser_type: Optional[str] = None
    traffic_source: Optional[str] = None
    
    # Performance
    avg_page_load_time: Optional[float] = None
    total_events_processed: int = 0
    
    # Metadata
    last_updated: datetime = Field(default_factory=datetime.now)

class BehavioralInsights(BaseModel):
    """Behavioral insights and predictions"""
    
    # Identification
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Behavioral patterns
    dominant_behavior_pattern: BehaviorPattern
    engagement_level: EngagementLevel
    behavior_confidence: float = Field(..., ge=0.0, le=1.0)
    
    # Predictions
    conversion_probability: float = Field(..., ge=0.0, le=1.0)
    next_action_prediction: Dict[str, Any]
    optimal_intervention_timing: Dict[str, Any]
    
    # Intent analysis
    intent_signals: List[str]
    purchase_intent_score: float = Field(default=0.0, ge=0.0, le=1.0)
    research_intent_score: float = Field(default=0.0, ge=0.0, le=1.0)
    comparison_intent_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Engagement analysis
    attention_spans: List[int] = []
    interaction_patterns: Dict[str, Any] = {}
    content_preferences: Dict[str, Any] = {}
    
    # Risk factors
    bounce_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    abandonment_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Recommendations
    recommended_actions: List[str] = []
    personalization_suggestions: Dict[str, Any] = {}
    content_recommendations: List[str] = []

class TriggerResponse(BaseModel):
    """Response to a behavioral trigger"""
    
    # Trigger identification
    trigger_id: str
    trigger_name: str
    session_id: str
    
    # Trigger details
    trigger_type: str
    conditions_met: List[str]
    actions_executed: List[Dict[str, Any]]
    
    # Execution results
    success: bool
    execution_time_ms: int
    error_message: Optional[str] = None
    
    # Impact tracking
    expected_impact: str
    tracking_data: Dict[str, Any] = {}
    
    # Metadata
    triggered_at: datetime = Field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None

class EngagementMetrics(BaseModel):
    """Real-time engagement metrics"""
    
    session_id: str
    user_id: Optional[str] = None
    
    # Current metrics
    current_page_time: int = 0
    current_scroll_depth: float = 0.0
    current_engagement_score: float = 0.0
    
    # Session totals
    total_page_views: int = 0
    total_interactions: int = 0
    total_time_active: int = 0
    
    # Behavioral indicators
    is_engaged: bool = False
    is_converting: bool = False
    attention_level: str = "normal"  # low, normal, high, very_high
    
    # Real-time predictions
    bounce_probability: float = 0.0
    conversion_probability: float = 0.0
    time_to_next_action: Optional[int] = None
    
    # Performance indicators
    page_performance_score: float = 1.0
    interaction_responsiveness: float = 1.0
    
    # Metadata
    last_activity: datetime = Field(default_factory=datetime.now)
    metrics_version: str = "1.0"

# =============================================================================
# ANALYSIS MODELS
# =============================================================================

class BehaviorAnalysis(BaseModel):
    """Comprehensive behavior analysis"""
    
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    user_id: Optional[str] = None
    
    # Analysis period
    start_time: datetime
    end_time: datetime
    events_analyzed: int
    
    # Behavioral classification
    primary_pattern: BehaviorPattern
    secondary_patterns: List[BehaviorPattern] = []
    pattern_confidence: float = Field(..., ge=0.0, le=1.0)
    
    # Engagement analysis
    engagement_progression: List[float] = []
    engagement_peaks: List[Dict[str, Any]] = []
    engagement_drops: List[Dict[str, Any]] = []
    
    # Interaction analysis
    interaction_density: float = 0.0
    interaction_quality_score: float = 0.0
    most_interacted_elements: List[str] = []
    
    # Content analysis
    content_consumption_rate: float = 0.0
    content_completion_rate: float = 0.0
    preferred_content_types: List[str] = []
    
    # Journey analysis
    page_flow: List[str] = []
    typical_session_length: int = 0
    conversion_funnel_position: str = "awareness"
    
    # Predictive insights
    likelihood_to_convert: float = Field(default=0.0, ge=0.0, le=1.0)
    estimated_lifetime_value: Optional[float] = None
    churn_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Recommendations
    optimization_opportunities: List[str] = []
    personalization_recommendations: List[str] = []
    content_suggestions: List[str] = []
    
    # Quality metrics
    data_quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    analysis_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.now)
    analysis_version: str = "1.0"

class RealTimeAlert(BaseModel):
    """Real-time behavioral alert"""
    
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    user_id: Optional[str] = None
    
    # Alert details
    alert_type: str  # engagement_drop, high_bounce_risk, conversion_opportunity
    severity: str = "medium"  # low, medium, high, critical
    message: str
    
    # Context
    triggering_event: Optional[BehavioralEvent] = None
    related_metrics: Dict[str, Any] = {}
    
    # Recommendations
    suggested_actions: List[str] = []
    urgency_level: str = "normal"  # low, normal, high, immediate
    
    # Metadata
    triggered_at: datetime = Field(default_factory=datetime.now)
    acknowledged: bool = False
    resolved: bool = False

# =============================================================================
# AGGREGATION MODELS
# =============================================================================

class HourlyBehaviorSummary(BaseModel):
    """Hourly aggregated behavior metrics"""
    
    hour: datetime
    
    # Volume metrics
    total_sessions: int = 0
    total_events: int = 0
    unique_users: int = 0
    total_page_views: int = 0
    
    # Engagement metrics
    avg_session_duration: float = 0.0
    avg_engagement_score: float = 0.0
    avg_scroll_depth: float = 0.0
    interaction_rate: float = 0.0
    
    # Conversion metrics
    conversion_rate: float = 0.0
    total_conversions: int = 0
    avg_conversion_value: float = 0.0
    
    # Behavioral patterns
    top_behavior_patterns: List[str] = []
    engagement_distribution: Dict[str, int] = {}
    
    # Performance metrics
    avg_page_load_time: float = 0.0
    bounce_rate: float = 0.0
    exit_rate: float = 0.0
    
    # Device breakdown
    device_breakdown: Dict[str, int] = {}
    browser_breakdown: Dict[str, int] = {}
    
    # Quality metrics
    data_completeness: float = 1.0
    processing_delay_avg: float = 0.0

class CohortBehaviorAnalysis(BaseModel):
    """Cohort-based behavior analysis"""
    
    cohort_id: str
    cohort_name: str
    cohort_definition: Dict[str, Any]
    
    # Cohort metrics
    cohort_size: int
    analysis_period_days: int
    retention_rates: List[float] = []
    
    # Behavioral characteristics
    common_patterns: List[BehaviorPattern] = []
    engagement_trends: List[float] = []
    conversion_funnel: Dict[str, float] = {}
    
    # Comparative analysis
    vs_global_average: Dict[str, float] = {}
    performance_percentile: float = 0.5
    
    # Insights
    key_insights: List[str] = []
    optimization_opportunities: List[str] = []
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)