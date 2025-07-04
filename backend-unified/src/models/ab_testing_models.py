"""
A/B Testing Data Models
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Pydantic models for A/B testing framework including test configuration,
variants, results, and statistical analysis.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid

# =============================================================================
# ENUMS
# =============================================================================

class TestType(str, Enum):
    AB_TEST = "ab_test"
    MULTIVARIATE = "multivariate"
    BANDIT = "bandit"
    SPLIT_URL = "split_url"

class TestStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INCONCLUSIVE = "inconclusive"

class MetricType(str, Enum):
    CONVERSION_RATE = "conversion_rate"
    REVENUE = "revenue"
    ENGAGEMENT = "engagement"
    RETENTION = "retention"
    CLICK_THROUGH_RATE = "click_through_rate"
    TIME_ON_PAGE = "time_on_page"
    BOUNCE_RATE = "bounce_rate"

class VariantType(str, Enum):
    CONTROL = "control"
    VARIANT = "variant"

class AllocationStrategy(str, Enum):
    EQUAL = "equal"
    WEIGHTED = "weighted"
    BANDIT = "bandit"
    ADAPTIVE = "adaptive"

class ConfidenceLevel(float, Enum):
    NINETY = 0.90
    NINETY_FIVE = 0.95
    NINETY_NINE = 0.99

class ImplementationType(str, Enum):
    FULL_ROLLOUT = "full_rollout"
    GRADUAL_ROLLOUT = "gradual_rollout"
    SEGMENT_ROLLOUT = "segment_rollout"
    CANARY_ROLLOUT = "canary_rollout"

class ImplementationStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"

# =============================================================================
# CORE MODELS
# =============================================================================

class ABTest(BaseModel):
    """A/B test configuration model"""
    
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    test_name: str = Field(..., min_length=1, max_length=255)
    test_type: TestType
    hypothesis: str = Field(..., min_length=1, max_length=1000)
    
    # Metrics
    primary_metric: MetricType
    secondary_metrics: List[MetricType] = []
    
    # Statistical parameters
    confidence_level: ConfidenceLevel = ConfidenceLevel.NINETY_FIVE
    minimum_detectable_effect: float = Field(default=0.05, ge=0.01, le=1.0)
    statistical_power: float = Field(default=0.80, ge=0.70, le=0.95)
    
    # Test parameters
    max_duration_days: int = Field(default=30, ge=1, le=180)
    minimum_sample_size: int = Field(default=1000, ge=100)
    required_sample_size: Optional[int] = None
    
    # Targeting
    target_url_pattern: str = Field(..., min_length=1)
    audience_filters: Optional[Dict[str, Any]] = None
    device_targeting: Optional[List[str]] = None
    
    # Advanced settings
    auto_winner_threshold: float = Field(default=0.95, ge=0.90, le=0.99)
    early_stopping_enabled: bool = True
    sequential_testing: bool = False
    allocation_strategy: AllocationStrategy = AllocationStrategy.EQUAL
    
    # Status and timing
    status: TestStatus = TestStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TestVariant(BaseModel):
    """A/B test variant model"""
    
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    test_id: str
    
    # Variant details
    variant_type: VariantType
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    
    # Variant configuration
    changes: Dict[str, Any] = Field(..., description="JSON describing the changes to apply")
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Performance expectations
    baseline_conversion_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    expected_lift: Optional[float] = Field(None, ge=-1.0, le=10.0)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class TrafficAllocation(BaseModel):
    """Traffic allocation for variant"""
    
    test_id: str
    variant_id: str
    allocation_percentage: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class TestAssignment(BaseModel):
    """User assignment to test variant"""
    
    test_id: str
    variant_id: str
    user_id: Optional[str] = None
    session_id: str
    
    # Assignment context
    page_url: str
    user_agent: Optional[str] = None
    device_type: Optional[str] = None
    assignment_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Assignment metadata
    assignment_method: str = "hash_based"
    custom_attributes: Optional[Dict[str, Any]] = None

class TestEvent(BaseModel):
    """A/B test event model"""
    
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    test_id: str
    variant_id: str
    
    # User identification
    user_id: Optional[str] = None
    session_id: str
    
    # Event details
    event_type: str
    event_value: Optional[float] = None
    event_properties: Optional[Dict[str, Any]] = None
    
    # Timing
    event_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Event metadata
    page_url: Optional[str] = None
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None
    
    # Performance tracking
    server_processing_time_ms: Optional[int] = None
    client_timestamp: Optional[datetime] = None

# =============================================================================
# STATISTICAL MODELS
# =============================================================================

class StatisticalSignificance(BaseModel):
    """Statistical significance calculation results"""
    
    test_type: str = "frequentist"  # frequentist, bayesian, sequential
    p_value: Optional[float] = None
    confidence_interval: Optional[tuple[float, float]] = None
    effect_size: Optional[float] = None
    lift: float = 0.0
    is_significant: bool = False
    
    # Test-specific metrics
    z_statistic: Optional[float] = None
    degrees_of_freedom: Optional[int] = None
    bayesian_probability: Optional[float] = None
    
    # Rates
    control_rate: float = 0.0
    variant_rate: float = 0.0
    relative_improvement: float = 0.0
    absolute_improvement: float = 0.0
    
    # Configuration
    confidence_level: float = 0.95

class TestStatistics(BaseModel):
    """Real-time test statistics"""
    
    test_id: str
    variant_id: str
    
    # Basic metrics
    participants: int = 0
    conversions: int = 0
    conversion_rate: float = 0.0
    
    # Revenue metrics
    total_revenue: float = 0.0
    revenue_per_visitor: float = 0.0
    
    # Engagement metrics
    total_events: int = 0
    avg_time_on_page: float = 0.0
    bounce_rate: float = 0.0
    
    # Statistical metrics
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    p_value: Optional[float] = None
    statistical_significance: bool = False
    
    # Metadata
    updated_at: datetime = Field(default_factory=datetime.now)
    calculation_timestamp: datetime = Field(default_factory=datetime.now)

class TestResult(BaseModel):
    """Final A/B test results"""
    
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    test_id: str
    
    # Test outcome
    winning_variant_id: Optional[str] = None
    recommendation: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    
    # Statistical summary
    statistical_significance: Dict[str, Any]
    effect_size: Optional[float] = None
    practical_significance: bool = False
    
    # Business impact
    estimated_revenue_impact: Optional[float] = None
    estimated_conversion_lift: Optional[float] = None
    implementation_priority: Optional[str] = Field(None, regex="^(low|medium|high|critical)$")
    
    # Test quality metrics
    sample_size_adequacy: bool
    test_duration_days: int
    data_quality_score: float = Field(..., ge=0.0, le=1.0)
    
    # Metadata
    analysis_completed_at: datetime = Field(default_factory=datetime.now)
    analyzed_by: Optional[str] = None

# =============================================================================
# IMPLEMENTATION MODELS
# =============================================================================

class TestImplementation(BaseModel):
    """A/B test implementation tracking"""
    
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    test_id: str
    variant_id: str
    
    # Implementation details
    implementation_type: ImplementationType
    rollout_percentage: float = Field(default=1.0, ge=0.0, le=1.0)
    target_segments: Optional[List[str]] = None
    
    # Status tracking
    status: ImplementationStatus = ImplementationStatus.PLANNED
    
    # Performance monitoring
    performance_metrics: Optional[Dict[str, Any]] = None
    rollback_reason: Optional[str] = None
    
    # Timing
    planned_start_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    implemented_by: Optional[str] = None
    
    class Config:
        use_enum_values = True

# =============================================================================
# ANALYSIS MODELS
# =============================================================================

class VariantPerformance(BaseModel):
    """Performance metrics for a single variant"""
    
    variant_id: str
    variant_name: str
    variant_type: VariantType
    
    # Core metrics
    participants: int
    conversions: int
    conversion_rate: float
    
    # Statistical analysis
    confidence_interval: Optional[tuple[float, float]] = None
    statistical_significance: Optional[StatisticalSignificance] = None
    
    # Relative performance
    lift_percentage: float = 0.0
    lift_absolute: float = 0.0
    
    # Revenue metrics
    total_revenue: float = 0.0
    revenue_per_visitor: float = 0.0
    average_order_value: float = 0.0
    
    # Engagement metrics
    avg_time_on_page: float = 0.0
    bounce_rate: float = 0.0
    pages_per_session: float = 0.0

class TestAnalysis(BaseModel):
    """Comprehensive test analysis"""
    
    test_id: str
    test_name: str
    test_status: TestStatus
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Test overview
    duration_days: int
    total_participants: int
    total_conversions: int
    overall_conversion_rate: float
    
    # Variant performance
    variant_performances: List[VariantPerformance]
    
    # Statistical results
    has_significant_result: bool
    winning_variant_id: Optional[str] = None
    confidence_level: float
    minimum_detectable_effect: float
    
    # Recommendations
    recommendation: str
    next_steps: List[str]
    implementation_urgency: str = Field(regex="^(low|medium|high|critical)$")
    
    # Quality metrics
    sample_size_adequate: bool
    test_duration_appropriate: bool
    data_quality_issues: List[str] = []
    
    # Business impact
    estimated_annual_impact: Optional[float] = None
    implementation_effort: Optional[str] = None
    roi_estimate: Optional[float] = None

# =============================================================================
# HELPER MODELS
# =============================================================================

class TestHealthCheck(BaseModel):
    """Test health monitoring"""
    
    test_id: str
    health_score: float = Field(..., ge=0.0, le=1.0)
    
    # Health indicators
    sample_size_progress: float
    conversion_rate_stability: float
    statistical_power_current: float
    data_quality_score: float
    
    # Issues and warnings
    issues: List[str] = []
    warnings: List[str] = []
    recommendations: List[str] = []
    
    # Projections
    estimated_completion_date: Optional[datetime] = None
    estimated_final_sample_size: Optional[int] = None
    projected_significance: Optional[float] = None
    
    # Metadata
    last_checked: datetime = Field(default_factory=datetime.now)

class VariantOptimization(BaseModel):
    """Variant optimization suggestions"""
    
    variant_id: str
    current_performance: VariantPerformance
    
    # Optimization opportunities
    optimization_suggestions: List[Dict[str, Any]]
    estimated_improvement: float
    confidence_in_suggestion: float = Field(..., ge=0.0, le=1.0)
    
    # Implementation details
    suggested_changes: Dict[str, Any]
    implementation_complexity: str = Field(regex="^(low|medium|high)$")
    estimated_development_time: Optional[str] = None
    
    # Risk assessment
    risk_level: str = Field(regex="^(low|medium|high)$")
    potential_downsides: List[str] = []
    mitigation_strategies: List[str] = []

class TestComparison(BaseModel):
    """Comparison between multiple tests"""
    
    comparison_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    test_ids: List[str]
    comparison_type: str = Field(regex="^(cross_test|historical|meta_analysis)$")
    
    # Comparison results
    common_patterns: List[str]
    differing_factors: List[str]
    meta_analysis_results: Optional[Dict[str, Any]] = None
    
    # Insights
    key_learnings: List[str]
    recommended_best_practices: List[str]
    future_test_suggestions: List[str]
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.now)
    analyzed_by: Optional[str] = None