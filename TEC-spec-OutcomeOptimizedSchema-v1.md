# TEC-spec-OutcomeOptimizedSchema-v1.md
# Outcome-Optimized Data Schema for Self-Learning Agentic RAG System

## Overview
This specification defines the comprehensive data schema optimized for outcome tracking, self-learning capabilities, and continuous performance improvement across the hybrid vector-graph RAG architecture.

## Core Design Principles

### 1. Outcome-First Architecture
- Every data point includes performance metrics
- Self-learning feedback loops are built into the schema
- Continuous optimization based on real-world outcomes

### 2. Temporal Intelligence
- All entities track their evolution over time
- Historical performance patterns inform future decisions
- Temporal snapshots enable rollback and analysis

### 3. Multi-Modal Integration
- Seamless integration between vector and graph databases
- Cross-referencing capabilities between different data types
- Unified performance metrics across modalities

## Unified Data Models

### 1. Core Entity Models
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class PerformanceMetrics(BaseModel):
    """Universal performance tracking for all entities"""
    engagement_score: float = Field(default=0.0, ge=0.0, le=1.0)
    conversion_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # User interaction metrics
    click_through_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    dwell_time_seconds: float = Field(default=0.0, ge=0.0)
    user_satisfaction: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    
    # Learning signals
    prediction_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    adaptation_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Temporal tracking
    last_updated: datetime = Field(default_factory=datetime.now)
    measurement_window_days: int = Field(default=7, ge=1, le=365)

class LearningSignals(BaseModel):
    """Signals used for self-learning optimization"""
    positive_feedback_count: int = Field(default=0, ge=0)
    negative_feedback_count: int = Field(default=0, ge=0)
    correction_count: int = Field(default=0, ge=0)
    
    # Behavioral signals
    repeat_access_count: int = Field(default=0, ge=0)
    sharing_count: int = Field(default=0, ge=0)
    bookmark_count: int = Field(default=0, ge=0)
    
    # Performance evolution
    performance_trend: float = Field(default=0.0, ge=-1.0, le=1.0)  # -1 declining, +1 improving
    volatility_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Context signals
    context_relevance: Dict[str, float] = Field(default_factory=dict)
    seasonal_patterns: Dict[str, float] = Field(default_factory=dict)

class EntityType(str, Enum):
    DOCUMENT = "document"
    CHUNK = "chunk"
    CONCEPT = "concept"
    STRATEGY = "strategy"
    OUTCOME = "outcome"
    METRIC = "metric"
    AGENT = "agent"
    QUERY = "query"
    RESPONSE = "response"

class UniversalEntity(BaseModel):
    """Universal entity model for all data types"""
    id: UUID = Field(default_factory=uuid4)
    type: EntityType
    name: str
    description: Optional[str] = None
    
    # Content
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    
    # Performance tracking
    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    learning_signals: LearningSignals = Field(default_factory=LearningSignals)
    
    # Relationships
    parent_id: Optional[UUID] = None
    child_ids: List[UUID] = Field(default_factory=list)
    related_entities: List[UUID] = Field(default_factory=list)
    
    # Vector embeddings
    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    
    # Temporal data
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    accessed_at: Optional[datetime] = None
    
    # Source tracking
    source_type: Optional[str] = None
    source_id: Optional[str] = None
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Lifecycle
    is_active: bool = True
    retirement_date: Optional[datetime] = None
    replacement_id: Optional[UUID] = None
```

### 2. Specialized Entity Models
```python
class DocumentEntity(UniversalEntity):
    """Document-specific entity model"""
    type: EntityType = EntityType.DOCUMENT
    
    # Document-specific fields
    title: str
    source_url: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[datetime] = None
    
    # Content metrics
    word_count: int = Field(default=0, ge=0)
    reading_time_minutes: float = Field(default=0.0, ge=0.0)
    complexity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Processing status
    chunks_generated: bool = False
    graph_entities_extracted: bool = False
    
    # Performance specific to documents
    citation_count: int = Field(default=0, ge=0)
    reference_count: int = Field(default=0, ge=0)

class ChunkEntity(UniversalEntity):
    """Chunk-specific entity model"""
    type: EntityType = EntityType.CHUNK
    
    # Chunk-specific fields
    document_id: UUID
    chunk_index: int = Field(ge=0)
    token_count: int = Field(ge=0)
    overlap_tokens: int = Field(default=0, ge=0)
    
    # Context
    preceding_chunk_id: Optional[UUID] = None
    following_chunk_id: Optional[UUID] = None
    
    # Retrieval optimization
    retrieval_count: int = Field(default=0, ge=0)
    average_query_similarity: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Quality metrics
    coherence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    information_density: float = Field(default=0.0, ge=0.0, le=1.0)

class QueryEntity(UniversalEntity):
    """Query-specific entity model"""
    type: EntityType = EntityType.QUERY
    
    # Query-specific fields
    original_query: str
    processed_query: str
    intent_classification: Optional[str] = None
    complexity_level: int = Field(default=1, ge=1, le=5)
    
    # Query processing
    preprocessing_steps: List[str] = Field(default_factory=list)
    entity_extraction: List[str] = Field(default_factory=list)
    keyword_extraction: List[str] = Field(default_factory=list)
    
    # Performance
    response_time_ms: float = Field(default=0.0, ge=0.0)
    search_strategy_used: str = "unknown"
    
    # Results
    results_count: int = Field(default=0, ge=0)
    top_result_scores: List[float] = Field(default_factory=list)
    
    # User interaction
    session_id: Optional[str] = None
    user_feedback: Optional[int] = Field(default=None, ge=1, le=5)
    follow_up_queries: List[UUID] = Field(default_factory=list)

class ResponseEntity(UniversalEntity):
    """Response-specific entity model"""
    type: EntityType = EntityType.RESPONSE
    
    # Response-specific fields
    query_id: UUID
    response_text: str
    response_type: str = "text"  # text, json, structured
    
    # Generation metadata
    model_used: str
    generation_time_ms: float = Field(default=0.0, ge=0.0)
    token_count: int = Field(default=0, ge=0)
    
    # Quality metrics
    coherence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    factual_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Citations and sources
    source_chunk_ids: List[UUID] = Field(default_factory=list)
    source_confidence_scores: List[float] = Field(default_factory=list)
    
    # User interaction
    user_rating: Optional[int] = Field(default=None, ge=1, le=5)
    was_helpful: Optional[bool] = None
    correction_feedback: Optional[str] = None

class AgentEntity(UniversalEntity):
    """Agent-specific entity model"""
    type: EntityType = EntityType.AGENT
    
    # Agent-specific fields
    agent_type: str
    version: str = "1.0.0"
    capabilities: List[str] = Field(default_factory=list)
    
    # Performance tracking
    task_success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    average_response_time_ms: float = Field(default=0.0, ge=0.0)
    error_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Learning metrics
    improvement_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    knowledge_freshness: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Resource usage
    compute_cost_per_task: float = Field(default=0.0, ge=0.0)
    memory_usage_mb: float = Field(default=0.0, ge=0.0)
    
    # Interaction history
    total_tasks_completed: int = Field(default=0, ge=0)
    total_errors: int = Field(default=0, ge=0)
    last_error_timestamp: Optional[datetime] = None
```

### 3. Relationship Models
```python
class RelationshipType(str, Enum):
    CONTAINS = "contains"
    REFERENCES = "references"
    INFLUENCES = "influences"
    SIMILAR_TO = "similar_to"
    FOLLOWS = "follows"
    CONTRADICTS = "contradicts"
    ENHANCES = "enhances"
    DEPENDS_ON = "depends_on"
    GENERATES = "generates"
    OPTIMIZES = "optimizes"

class EntityRelationship(BaseModel):
    """Universal relationship model"""
    id: UUID = Field(default_factory=uuid4)
    source_entity_id: UUID
    target_entity_id: UUID
    relationship_type: RelationshipType
    
    # Relationship strength and confidence
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Performance tracking
    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    
    # Temporal validity
    valid_from: datetime = Field(default_factory=datetime.now)
    valid_to: Optional[datetime] = None
    
    # Usage tracking
    usage_count: int = Field(default=0, ge=0)
    last_used: Optional[datetime] = None
    
    # Learning signals
    reinforcement_count: int = Field(default=0, ge=0)
    contradiction_count: int = Field(default=0, ge=0)
    
    # Context
    context_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Source tracking
    discovered_by: Optional[str] = None  # agent, user, system
    validation_status: str = "pending"  # pending, validated, rejected
```

### 4. Outcome Tracking Models
```python
class OutcomeType(str, Enum):
    SEARCH_SATISFACTION = "search_satisfaction"
    TASK_COMPLETION = "task_completion"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    LEARNING = "learning"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"

class OutcomeEvent(BaseModel):
    """Universal outcome tracking"""
    id: UUID = Field(default_factory=uuid4)
    outcome_type: OutcomeType
    
    # Associated entities
    primary_entity_id: UUID
    related_entity_ids: List[UUID] = Field(default_factory=list)
    
    # Outcome metrics
    success: bool
    value: float = Field(default=0.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Context
    user_session_id: Optional[str] = None
    agent_id: Optional[UUID] = None
    query_id: Optional[UUID] = None
    
    # Temporal data
    timestamp: datetime = Field(default_factory=datetime.now)
    duration_seconds: Optional[float] = None
    
    # Detailed outcome data
    outcome_details: Dict[str, Any] = Field(default_factory=dict)
    
    # Learning signals
    was_expected: bool = True
    surprise_factor: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Attribution
    contributing_factors: List[str] = Field(default_factory=list)
    hindering_factors: List[str] = Field(default_factory=list)

class LearningIteration(BaseModel):
    """Track learning iterations and improvements"""
    id: UUID = Field(default_factory=uuid4)
    entity_id: UUID
    iteration_number: int = Field(ge=1)
    
    # Performance before/after
    performance_before: PerformanceMetrics
    performance_after: PerformanceMetrics
    
    # Changes made
    changes_applied: List[str] = Field(default_factory=list)
    parameters_adjusted: Dict[str, Any] = Field(default_factory=dict)
    
    # Learning method
    learning_method: str = "reinforcement"  # reinforcement, supervised, unsupervised
    confidence_in_change: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Validation
    validation_outcomes: List[UUID] = Field(default_factory=list)
    validation_success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Temporal
    applied_at: datetime = Field(default_factory=datetime.now)
    evaluation_period_days: int = Field(default=7, ge=1, le=30)
```

### 5. System Performance Models
```python
class SystemMetrics(BaseModel):
    """System-wide performance tracking"""
    id: UUID = Field(default_factory=uuid4)
    
    # Performance metrics
    total_queries_processed: int = Field(default=0, ge=0)
    average_response_time_ms: float = Field(default=0.0, ge=0.0)
    search_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    user_satisfaction_score: float = Field(default=0.0, ge=0.0, le=5.0)
    
    # Resource utilization
    cpu_usage_percent: float = Field(default=0.0, ge=0.0, le=100.0)
    memory_usage_mb: float = Field(default=0.0, ge=0.0)
    storage_usage_gb: float = Field(default=0.0, ge=0.0)
    
    # Database performance
    vector_db_response_time_ms: float = Field(default=0.0, ge=0.0)
    graph_db_response_time_ms: float = Field(default=0.0, ge=0.0)
    
    # Learning system performance
    learning_iterations_completed: int = Field(default=0, ge=0)
    performance_improvements_applied: int = Field(default=0, ge=0)
    
    # Error tracking
    error_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    critical_errors: int = Field(default=0, ge=0)
    
    # Temporal
    measurement_start: datetime
    measurement_end: datetime
    
    # Trends
    performance_trend: float = Field(default=0.0, ge=-1.0, le=1.0)
    improvement_velocity: float = Field(default=0.0, ge=0.0)

class A_B_TestResult(BaseModel):
    """A/B testing for continuous optimization"""
    id: UUID = Field(default_factory=uuid4)
    test_name: str
    
    # Test configuration
    control_variant: str = "A"
    treatment_variant: str = "B"
    
    # Metrics
    control_performance: PerformanceMetrics
    treatment_performance: PerformanceMetrics
    
    # Statistical significance
    sample_size_control: int = Field(ge=1)
    sample_size_treatment: int = Field(ge=1)
    confidence_level: float = Field(default=0.95, ge=0.0, le=1.0)
    p_value: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Results
    winning_variant: Optional[str] = None
    improvement_percentage: float = Field(default=0.0)
    
    # Implementation
    test_start_date: datetime
    test_end_date: Optional[datetime] = None
    status: str = "running"  # running, completed, stopped
    
    # Context
    test_context: Dict[str, Any] = Field(default_factory=dict)
    implementation_notes: Optional[str] = None
```

## Schema Integration Patterns

### 1. Cross-Database Synchronization
```python
class SyncConfiguration(BaseModel):
    """Configuration for cross-database synchronization"""
    vector_db_primary: bool = True
    graph_db_primary: bool = False
    
    # Sync rules
    sync_frequency_seconds: int = Field(default=300, ge=60)  # 5 minutes
    batch_size: int = Field(default=100, ge=1, le=1000)
    
    # Conflict resolution
    conflict_resolution_strategy: str = "latest_wins"
    
    # Performance tracking
    sync_performance_metrics: bool = True
    sync_learning_signals: bool = True
    sync_relationships: bool = True

class EntitySyncManager:
    """Manage synchronization between databases"""
    
    async def sync_entity_performance(self, entity_id: UUID):
        """Sync performance metrics across databases"""
        # Implementation for bi-directional sync
        pass
    
    async def propagate_learning_signals(self, entity_id: UUID):
        """Propagate learning signals to improve related entities"""
        # Implementation for learning propagation
        pass
```

### 2. Performance Analytics Schema
```python
class PerformanceAnalytics(BaseModel):
    """Advanced analytics for performance optimization"""
    
    # Entity performance patterns
    top_performing_entities: List[UUID] = Field(default_factory=list)
    underperforming_entities: List[UUID] = Field(default_factory=list)
    
    # Trend analysis
    performance_trends: Dict[str, float] = Field(default_factory=dict)
    seasonal_patterns: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    
    # Predictive insights
    predicted_performance: Dict[UUID, float] = Field(default_factory=dict)
    confidence_intervals: Dict[UUID, tuple] = Field(default_factory=dict)
    
    # Optimization recommendations
    optimization_suggestions: List[Dict[str, Any]] = Field(default_factory=list)
    potential_improvements: Dict[UUID, float] = Field(default_factory=dict)
    
    # Meta-learning
    learning_efficiency: float = Field(default=0.0, ge=0.0, le=1.0)
    adaptation_speed: float = Field(default=0.0, ge=0.0, le=1.0)
```

This comprehensive schema provides the foundation for a self-learning, outcome-optimized RAG system that continuously improves based on real-world performance data and user interactions.