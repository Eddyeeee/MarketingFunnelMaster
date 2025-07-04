"""
Unified Data Models for Agentic RAG System
Integrates Neon PostgreSQL and Neo4j with outcome-optimized schema
Version: 1.0.0
Created: 2025-07-03
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
import json
import asyncio
from dataclasses import dataclass

# Core Enums
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
    # Module 3A: Content Generation Types
    CONTENT_OUTLINE = "content_outline"
    CONTENT_PIECE = "content_piece"
    VISUAL_ASSET = "visual_asset"
    SOCIAL_ADAPTATION = "social_adaptation"
    CONTENT_TEMPLATE = "content_template"
    CONTENT_PIPELINE = "content_pipeline"

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
    # Module 3A: Content Generation Relationships
    PERSONALIZES_FOR = "personalizes_for"
    ADAPTS_TO_DEVICE = "adapts_to_device"
    OPTIMIZES_FOR_PERSONA = "optimizes_for_persona"
    DERIVED_FROM_TEMPLATE = "derived_from_template"
    SOCIAL_ADAPTATION_OF = "social_adaptation_of"

class OutcomeType(str, Enum):
    SEARCH_SATISFACTION = "search_satisfaction"
    TASK_COMPLETION = "task_completion"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    LEARNING = "learning"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    # Module 3A: Content Generation Outcomes
    CONTENT_GENERATION_SUCCESS = "content_generation_success"
    PERSONA_OPTIMIZATION_SUCCESS = "persona_optimization_success"
    DEVICE_ADAPTATION_SUCCESS = "device_adaptation_success"
    CONTENT_QUALITY_VALIDATION = "content_quality_validation"
    SOCIAL_MEDIA_ENGAGEMENT = "social_media_engagement"

# Core Performance Tracking Models
class PerformanceMetrics(BaseModel):
    """Universal performance tracking for all entities"""
    engagement_score: float = Field(default=0.0, ge=0.0, le=1.0, description="User engagement level")
    conversion_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Conversion success rate")
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Content relevance score")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="System confidence in data")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall success rate")
    
    # User interaction metrics
    click_through_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="CTR for search results")
    dwell_time_seconds: float = Field(default=0.0, ge=0.0, description="Time spent on content")
    user_satisfaction: Optional[float] = Field(default=None, ge=1.0, le=5.0, description="User satisfaction rating")
    
    # Learning signals
    prediction_accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Prediction accuracy")
    adaptation_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Learning adaptation rate")
    
    # Temporal tracking
    last_updated: datetime = Field(default_factory=datetime.now)
    measurement_window_days: int = Field(default=7, ge=1, le=365)

    class Config:
        schema_extra = {
            "example": {
                "engagement_score": 0.75,
                "conversion_rate": 0.12,
                "relevance_score": 0.88,
                "confidence_score": 0.92,
                "success_rate": 0.68,
                "click_through_rate": 0.15,
                "dwell_time_seconds": 45.5,
                "user_satisfaction": 4.2,
                "prediction_accuracy": 0.85,
                "adaptation_rate": 0.22
            }
        }

class LearningSignals(BaseModel):
    """Signals used for self-learning optimization"""
    positive_feedback_count: int = Field(default=0, ge=0, description="Count of positive feedback")
    negative_feedback_count: int = Field(default=0, ge=0, description="Count of negative feedback")
    correction_count: int = Field(default=0, ge=0, description="Count of corrections applied")
    
    # Behavioral signals
    repeat_access_count: int = Field(default=0, ge=0, description="Times content was re-accessed")
    sharing_count: int = Field(default=0, ge=0, description="Times content was shared")
    bookmark_count: int = Field(default=0, ge=0, description="Times content was bookmarked")
    
    # Performance evolution
    performance_trend: float = Field(default=0.0, ge=-1.0, le=1.0, description="Performance trend: -1 declining, +1 improving")
    volatility_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Performance volatility")
    
    # Context signals
    context_relevance: Dict[str, float] = Field(default_factory=dict, description="Context-specific relevance scores")
    seasonal_patterns: Dict[str, float] = Field(default_factory=dict, description="Seasonal performance patterns")

    def calculate_overall_signal_strength(self) -> float:
        """Calculate overall signal strength for learning"""
        total_feedback = self.positive_feedback_count + self.negative_feedback_count
        if total_feedback == 0:
            return 0.0
        
        positive_ratio = self.positive_feedback_count / total_feedback
        engagement_factor = min(self.repeat_access_count / 10.0, 1.0)
        trend_factor = (self.performance_trend + 1.0) / 2.0  # Normalize to 0-1
        
        return (positive_ratio * 0.5 + engagement_factor * 0.3 + trend_factor * 0.2)

# Universal Entity Model
class UniversalEntity(BaseModel):
    """Universal entity model for all data types"""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    type: EntityType = Field(description="Entity type")
    name: str = Field(min_length=1, max_length=500, description="Entity name")
    description: Optional[str] = Field(default=None, max_length=2000, description="Entity description")
    
    # Content
    content: Optional[str] = Field(default=None, description="Main content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    tags: List[str] = Field(default_factory=list, max_items=20, description="Tags for categorization")
    
    # Performance tracking
    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    learning_signals: LearningSignals = Field(default_factory=LearningSignals)
    
    # Relationships
    parent_id: Optional[UUID] = Field(default=None, description="Parent entity ID")
    child_ids: List[UUID] = Field(default_factory=list, description="Child entity IDs")
    related_entities: List[UUID] = Field(default_factory=list, description="Related entity IDs")
    
    # Vector embeddings
    embedding: Optional[List[float]] = Field(default=None, description="Vector embedding")
    embedding_model: Optional[str] = Field(default=None, description="Model used for embedding")
    
    # Temporal data
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    accessed_at: Optional[datetime] = Field(default=None, description="Last access time")
    
    # Source tracking
    source_type: Optional[str] = Field(default=None, description="Source type")
    source_id: Optional[str] = Field(default=None, description="Source identifier")
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction confidence")
    
    # Lifecycle
    is_active: bool = Field(default=True, description="Whether entity is active")
    retirement_date: Optional[datetime] = Field(default=None, description="Retirement date")
    replacement_id: Optional[UUID] = Field(default=None, description="Replacement entity ID")

    @validator('embedding')
    def validate_embedding_dimension(cls, v):
        if v is not None and len(v) != 1536:  # OpenAI embedding dimension
            raise ValueError('Embedding must be 1536 dimensions for OpenAI compatibility')
        return v

    def to_postgres_dict(self) -> Dict[str, Any]:
        """Convert to PostgreSQL format"""
        return {
            "id": str(self.id),
            "title": self.name,
            "source": self.source_type or "unknown",
            "content": self.content or "",
            "content_type": self.type.value,
            "metadata": json.dumps(self.metadata),
            "engagement_score": self.performance.engagement_score,
            "conversion_rate": self.performance.conversion_rate,
            "last_accessed": self.accessed_at,
            "access_count": self.learning_signals.repeat_access_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "content_vector": self.embedding,
            "is_active": self.is_active,
            "retirement_date": self.retirement_date,
            "replacement_id": str(self.replacement_id) if self.replacement_id else None
        }

    def to_neo4j_dict(self) -> Dict[str, Any]:
        """Convert to Neo4j format"""
        return {
            "uuid": str(self.id),
            "name": self.name,
            "type": self.type.value,
            "description": self.description,
            "performance_score": self.performance.relevance_score,
            "confidence_score": self.performance.confidence_score,
            "relevance_score": self.performance.relevance_score,
            "valid_from": self.created_at,
            "valid_to": self.retirement_date,
            "source_document_id": self.source_id,
            "extraction_confidence": self.extraction_confidence,
            "user_interaction_count": self.learning_signals.repeat_access_count,
            "success_rate": self.performance.success_rate,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags,
            "properties": {
                **self.metadata,
                "content_preview": self.content[:200] if self.content else None,
                "performance_metrics": self.performance.dict(),
                "learning_signals": self.learning_signals.dict()
            }
        }

# Specialized Entity Models
class DocumentEntity(UniversalEntity):
    """Document-specific entity model"""
    type: EntityType = Field(default=EntityType.DOCUMENT, const=True)
    
    # Document-specific fields
    title: str = Field(min_length=1, max_length=1000, description="Document title")
    source_url: Optional[str] = Field(default=None, description="Source URL")
    author: Optional[str] = Field(default=None, max_length=200, description="Document author")
    publication_date: Optional[datetime] = Field(default=None, description="Publication date")
    
    # Content metrics
    word_count: int = Field(default=0, ge=0, description="Word count")
    reading_time_minutes: float = Field(default=0.0, ge=0.0, description="Estimated reading time")
    complexity_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Content complexity")
    
    # Processing status
    chunks_generated: bool = Field(default=False, description="Whether chunks have been generated")
    graph_entities_extracted: bool = Field(default=False, description="Whether graph entities extracted")
    
    # Performance specific to documents
    citation_count: int = Field(default=0, ge=0, description="Number of citations")
    reference_count: int = Field(default=0, ge=0, description="Number of references")

    def estimate_reading_time(self) -> float:
        """Estimate reading time based on word count"""
        words_per_minute = 200  # Average reading speed
        return self.word_count / words_per_minute if self.word_count > 0 else 0.0

class ChunkEntity(UniversalEntity):
    """Chunk-specific entity model"""
    type: EntityType = Field(default=EntityType.CHUNK, const=True)
    
    # Chunk-specific fields
    document_id: UUID = Field(description="Parent document ID")
    chunk_index: int = Field(ge=0, description="Index within document")
    token_count: int = Field(ge=0, description="Number of tokens")
    overlap_tokens: int = Field(default=0, ge=0, description="Overlapping tokens with adjacent chunks")
    
    # Context
    preceding_chunk_id: Optional[UUID] = Field(default=None, description="Previous chunk ID")
    following_chunk_id: Optional[UUID] = Field(default=None, description="Next chunk ID")
    
    # Retrieval optimization
    retrieval_count: int = Field(default=0, ge=0, description="Number of times retrieved")
    average_query_similarity: float = Field(default=0.0, ge=0.0, le=1.0, description="Average similarity to queries")
    
    # Quality metrics
    coherence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Content coherence")
    information_density: float = Field(default=0.0, ge=0.0, le=1.0, description="Information density")

    def calculate_relevance_boost(self) -> float:
        """Calculate relevance boost based on retrieval patterns"""
        retrieval_factor = min(self.retrieval_count / 100.0, 1.0)
        quality_factor = (self.coherence_score + self.information_density) / 2.0
        return retrieval_factor * 0.3 + quality_factor * 0.7

class QueryEntity(UniversalEntity):
    """Query-specific entity model"""
    type: EntityType = Field(default=EntityType.QUERY, const=True)
    
    # Query-specific fields
    original_query: str = Field(min_length=1, description="Original user query")
    processed_query: str = Field(description="Processed/cleaned query")
    intent_classification: Optional[str] = Field(default=None, description="Classified intent")
    complexity_level: int = Field(default=1, ge=1, le=5, description="Query complexity level")
    
    # Query processing
    preprocessing_steps: List[str] = Field(default_factory=list, description="Applied preprocessing steps")
    entity_extraction: List[str] = Field(default_factory=list, description="Extracted entities")
    keyword_extraction: List[str] = Field(default_factory=list, description="Extracted keywords")
    
    # Performance
    response_time_ms: float = Field(default=0.0, ge=0.0, description="Response time in milliseconds")
    search_strategy_used: str = Field(default="unknown", description="Search strategy used")
    
    # Results
    results_count: int = Field(default=0, ge=0, description="Number of results returned")
    top_result_scores: List[float] = Field(default_factory=list, description="Top result relevance scores")
    
    # User interaction
    session_id: Optional[str] = Field(default=None, description="User session ID")
    user_feedback: Optional[int] = Field(default=None, ge=1, le=5, description="User feedback rating")
    follow_up_queries: List[UUID] = Field(default_factory=list, description="Follow-up query IDs")

class ResponseEntity(UniversalEntity):
    """Response-specific entity model"""
    type: EntityType = Field(default=EntityType.RESPONSE, const=True)
    
    # Response-specific fields
    query_id: UUID = Field(description="Associated query ID")
    response_text: str = Field(description="Generated response text")
    response_type: str = Field(default="text", description="Response type (text, json, structured)")
    
    # Generation metadata
    model_used: str = Field(description="Model used for generation")
    generation_time_ms: float = Field(default=0.0, ge=0.0, description="Generation time in milliseconds")
    token_count: int = Field(default=0, ge=0, description="Response token count")
    
    # Quality metrics
    coherence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Response coherence")
    factual_accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Factual accuracy")
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Response completeness")
    
    # Citations and sources
    source_chunk_ids: List[UUID] = Field(default_factory=list, description="Source chunk IDs")
    source_confidence_scores: List[float] = Field(default_factory=list, description="Source confidence scores")
    
    # User interaction
    user_rating: Optional[int] = Field(default=None, ge=1, le=5, description="User rating")
    was_helpful: Optional[bool] = Field(default=None, description="Whether response was helpful")
    correction_feedback: Optional[str] = Field(default=None, description="User correction feedback")

# Relationship Models
class EntityRelationship(BaseModel):
    """Universal relationship model"""
    id: UUID = Field(default_factory=uuid4, description="Relationship ID")
    source_entity_id: UUID = Field(description="Source entity ID")
    target_entity_id: UUID = Field(description="Target entity ID")
    relationship_type: RelationshipType = Field(description="Type of relationship")
    
    # Relationship strength and confidence
    strength: float = Field(default=0.5, ge=0.0, le=1.0, description="Relationship strength")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence in relationship")
    
    # Performance tracking
    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    
    # Temporal validity
    valid_from: datetime = Field(default_factory=datetime.now)
    valid_to: Optional[datetime] = Field(default=None, description="Relationship expiry")
    
    # Usage tracking
    usage_count: int = Field(default=0, ge=0, description="Times relationship was used")
    last_used: Optional[datetime] = Field(default=None, description="Last usage time")
    
    # Learning signals
    reinforcement_count: int = Field(default=0, ge=0, description="Times relationship was reinforced")
    contradiction_count: int = Field(default=0, ge=0, description="Times relationship was contradicted")
    
    # Context
    context_metadata: Dict[str, Any] = Field(default_factory=dict, description="Context metadata")
    
    # Source tracking
    discovered_by: Optional[str] = Field(default=None, description="Discovery source (agent, user, system)")
    validation_status: str = Field(default="pending", description="Validation status")

    def calculate_relationship_quality(self) -> float:
        """Calculate overall relationship quality score"""
        usage_factor = min(self.usage_count / 10.0, 1.0)
        reinforcement_ratio = (
            self.reinforcement_count / max(self.reinforcement_count + self.contradiction_count, 1)
        )
        
        return (
            self.strength * 0.3 +
            self.confidence * 0.3 +
            usage_factor * 0.2 +
            reinforcement_ratio * 0.2
        )

# Outcome Tracking Models
class OutcomeEvent(BaseModel):
    """Universal outcome tracking"""
    id: UUID = Field(default_factory=uuid4, description="Outcome ID")
    outcome_type: OutcomeType = Field(description="Type of outcome")
    
    # Associated entities
    primary_entity_id: UUID = Field(description="Primary entity involved")
    related_entity_ids: List[UUID] = Field(default_factory=list, description="Related entities")
    
    # Outcome metrics
    success: bool = Field(description="Whether outcome was successful")
    value: float = Field(default=0.0, description="Outcome value/impact")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in outcome measurement")
    
    # Context
    user_session_id: Optional[str] = Field(default=None, description="User session ID")
    agent_id: Optional[UUID] = Field(default=None, description="Agent involved")
    query_id: Optional[UUID] = Field(default=None, description="Associated query")
    
    # Temporal data
    timestamp: datetime = Field(default_factory=datetime.now)
    duration_seconds: Optional[float] = Field(default=None, description="Outcome duration")
    
    # Detailed outcome data
    outcome_details: Dict[str, Any] = Field(default_factory=dict, description="Detailed outcome data")
    
    # Learning signals
    was_expected: bool = Field(default=True, description="Whether outcome was expected")
    surprise_factor: float = Field(default=0.0, ge=0.0, le=1.0, description="How surprising the outcome was")
    
    # Attribution
    contributing_factors: List[str] = Field(default_factory=list, description="Factors that contributed")
    hindering_factors: List[str] = Field(default_factory=list, description="Factors that hindered")

# System Performance Models
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

# Factory Functions
def create_document_entity(title: str, content: str, source_url: Optional[str] = None) -> DocumentEntity:
    """Create a new document entity"""
    return DocumentEntity(
        name=title,
        title=title,
        content=content,
        source_url=source_url,
        word_count=len(content.split()) if content else 0,
        reading_time_minutes=len(content.split()) / 200 if content else 0
    )

def create_chunk_entity(document_id: UUID, content: str, chunk_index: int) -> ChunkEntity:
    """Create a new chunk entity"""
    return ChunkEntity(
        name=f"Chunk {chunk_index}",
        content=content,
        document_id=document_id,
        chunk_index=chunk_index,
        token_count=len(content.split()),  # Simplified token count
        parent_id=document_id
    )

def create_query_entity(query_text: str, session_id: Optional[str] = None) -> QueryEntity:
    """Create a new query entity"""
    return QueryEntity(
        name=f"Query: {query_text[:50]}...",
        original_query=query_text,
        processed_query=query_text.lower().strip(),
        session_id=session_id,
        complexity_level=min(len(query_text.split()) // 5 + 1, 5)
    )

def create_relationship(source_id: UUID, target_id: UUID, 
                       relationship_type: RelationshipType,
                       strength: float = 0.5) -> EntityRelationship:
    """Create a new entity relationship"""
    return EntityRelationship(
        source_entity_id=source_id,
        target_entity_id=target_id,
        relationship_type=relationship_type,
        strength=strength,
        confidence=strength  # Initially, confidence equals strength
    )

# Validation utilities
def validate_entity_consistency(entity: UniversalEntity) -> List[str]:
    """Validate entity consistency and return any issues"""
    issues = []
    
    if entity.type == EntityType.CHUNK and not entity.parent_id:
        issues.append("Chunk entity must have a parent_id")
    
    if entity.embedding and len(entity.embedding) != 1536:
        issues.append("Embedding must be 1536 dimensions")
    
    if entity.performance.confidence_score > entity.extraction_confidence:
        issues.append("Performance confidence cannot exceed extraction confidence")
    
    return issues

# Module 3A: Content Generation Specialized Entities
class ContentOutlineEntity(UniversalEntity):
    """Content outline specific entity model"""
    type: EntityType = Field(default=EntityType.CONTENT_OUTLINE, const=True)
    
    # Outline specific fields
    niche: str = Field(description="Target niche")
    persona: str = Field(description="Target persona")
    device: str = Field(description="Target device type")
    outline_structure: Dict[str, Any] = Field(default_factory=dict, description="Structured outline data")
    seo_keywords: List[str] = Field(default_factory=list, description="SEO keywords")
    target_length: int = Field(default=1000, description="Target content length")
    conversion_goals: List[str] = Field(default_factory=list, description="Conversion objectives")

class ContentPieceEntity(UniversalEntity):
    """Generated content piece entity model"""
    type: EntityType = Field(default=EntityType.CONTENT_PIECE, const=True)
    
    # Content specific fields
    outline_id: Optional[UUID] = Field(default=None, description="Source outline ID")
    niche: str = Field(description="Content niche")
    persona: str = Field(description="Target persona")
    device: str = Field(description="Optimized device type")
    content_type: str = Field(description="Type of content (blog, product_page, etc.)")
    
    # Content structure
    title: str = Field(description="Content title")
    meta_description: str = Field(default="", description="SEO meta description")
    body_content: str = Field(description="Main content body")
    call_to_action: str = Field(default="", description="Call to action text")
    
    # Quality metrics
    word_count: int = Field(default=0, description="Word count")
    readability_score: float = Field(default=0.0, description="Readability score")
    seo_score: float = Field(default=0.0, description="SEO optimization score")
    persona_alignment_score: float = Field(default=0.0, description="Persona alignment score")
    
    # Performance tracking
    conversion_rate: float = Field(default=0.0, description="Content conversion rate")
    engagement_metrics: Dict[str, float] = Field(default_factory=dict, description="Engagement metrics")

class VisualAssetEntity(UniversalEntity):
    """Visual content asset entity model"""
    type: EntityType = Field(default=EntityType.VISUAL_ASSET, const=True)
    
    # Visual specific fields
    content_piece_id: Optional[UUID] = Field(default=None, description="Associated content piece")
    asset_type: str = Field(description="Type of visual asset")
    file_path: str = Field(description="Asset file path")
    dimensions: Dict[str, int] = Field(default_factory=dict, description="Asset dimensions")
    file_size_kb: int = Field(default=0, description="File size in KB")
    
    # Generation metadata
    prompt_used: str = Field(default="", description="Generation prompt")
    style_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Style guidelines")
    brand_compliance: bool = Field(default=True, description="Brand compliance status")

class SocialAdaptationEntity(UniversalEntity):
    """Social media adaptation entity model"""
    type: EntityType = Field(default=EntityType.SOCIAL_ADAPTATION, const=True)
    
    # Social adaptation fields
    source_content_id: UUID = Field(description="Source content piece ID")
    platform: str = Field(description="Target social media platform")
    adaptation_type: str = Field(description="Type of adaptation")
    
    # Platform-specific content
    caption: str = Field(default="", description="Social media caption")
    hashtags: List[str] = Field(default_factory=list, description="Hashtags")
    platform_specific_data: Dict[str, Any] = Field(default_factory=dict, description="Platform specific data")
    
    # Engagement optimization
    hook_strategy: str = Field(default="", description="Engagement hook strategy")
    call_to_action: str = Field(default="", description="Social CTA")
    engagement_prediction: float = Field(default=0.0, description="Predicted engagement rate")

class ContentTemplateEntity(UniversalEntity):
    """Content template entity model"""
    type: EntityType = Field(default=EntityType.CONTENT_TEMPLATE, const=True)
    
    # Template fields
    template_name: str = Field(description="Template name")
    template_category: str = Field(description="Template category")
    target_niche: str = Field(description="Target niche")
    template_structure: Dict[str, Any] = Field(default_factory=dict, description="Template structure")
    
    # Personalization rules
    persona_adaptations: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Persona-specific adaptations")
    device_optimizations: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Device-specific optimizations")
    
    # Performance data
    usage_count: int = Field(default=0, description="Times template was used")
    average_performance: float = Field(default=0.0, description="Average template performance")
    success_patterns: List[Dict[str, Any]] = Field(default_factory=list, description="Successful usage patterns")

class ContentPipelineEntity(UniversalEntity):
    """Content generation pipeline execution entity model"""
    type: EntityType = Field(default=EntityType.CONTENT_PIPELINE, const=True)
    
    # Pipeline execution data
    pipeline_id: UUID = Field(description="Pipeline execution ID")
    niche: str = Field(description="Target niche")
    persona: str = Field(description="Target persona")
    device: str = Field(description="Target device")
    
    # Execution tracking
    stages_completed: int = Field(default=0, description="Number of stages completed")
    total_stages: int = Field(default=4, description="Total pipeline stages")
    execution_start: datetime = Field(default_factory=datetime.now, description="Pipeline start time")
    execution_end: Optional[datetime] = Field(default=None, description="Pipeline end time")
    
    # Generated content references
    outline_id: Optional[UUID] = Field(default=None, description="Generated outline ID")
    content_id: Optional[UUID] = Field(default=None, description="Generated content ID")
    visual_asset_ids: List[UUID] = Field(default_factory=list, description="Generated visual asset IDs")
    social_adaptation_ids: List[UUID] = Field(default_factory=list, description="Generated social adaptation IDs")
    
    # Pipeline performance
    generation_time_seconds: float = Field(default=0.0, description="Total generation time")
    quality_score: float = Field(default=0.0, description="Overall quality score")
    pipeline_efficiency: float = Field(default=0.0, description="Pipeline efficiency score")
    
    # Error tracking
    errors_encountered: List[Dict[str, Any]] = Field(default_factory=list, description="Errors during execution")
    retry_count: int = Field(default=0, description="Number of retries")

# Factory functions for content entities
def create_content_outline_entity(niche: str, persona: str, device: str, 
                                 outline_data: Dict[str, Any]) -> ContentOutlineEntity:
    """Create a new content outline entity"""
    return ContentOutlineEntity(
        name=f"Content Outline: {outline_data.get('title', 'Untitled')}",
        niche=niche,
        persona=persona,
        device=device,
        outline_structure=outline_data,
        seo_keywords=outline_data.get('seo_keywords', []),
        target_length=outline_data.get('target_length', 1000),
        conversion_goals=outline_data.get('conversion_goals', [])
    )

def create_content_piece_entity(title: str, content: str, niche: str, 
                               persona: str, device: str, 
                               outline_id: Optional[UUID] = None) -> ContentPieceEntity:
    """Create a new content piece entity"""
    return ContentPieceEntity(
        name=title,
        title=title,
        body_content=content,
        niche=niche,
        persona=persona,
        device=device,
        outline_id=outline_id,
        word_count=len(content.split()) if content else 0,
        content_type="generated_content"
    )

def create_content_pipeline_entity(niche: str, persona: str, device: str) -> ContentPipelineEntity:
    """Create a new content pipeline entity"""
    pipeline_id = uuid4()
    return ContentPipelineEntity(
        name=f"Content Pipeline: {niche}-{persona}-{device}",
        pipeline_id=pipeline_id,
        niche=niche,
        persona=persona,
        device=device
    )

# Export all models
__all__ = [
    "EntityType", "RelationshipType", "OutcomeType",
    "PerformanceMetrics", "LearningSignals",
    "UniversalEntity", "DocumentEntity", "ChunkEntity", "QueryEntity", "ResponseEntity",
    "ContentOutlineEntity", "ContentPieceEntity", "VisualAssetEntity", "SocialAdaptationEntity",
    "ContentTemplateEntity", "ContentPipelineEntity",
    "EntityRelationship", "OutcomeEvent", "SystemMetrics",
    "create_document_entity", "create_chunk_entity", "create_query_entity", "create_relationship",
    "create_content_outline_entity", "create_content_piece_entity", "create_content_pipeline_entity",
    "validate_entity_consistency"
]