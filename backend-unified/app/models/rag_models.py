"""
RAG Models - Week 2 Implementation
Milestone 1C: Pydantic models for Adaptive RAG System

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from datetime import datetime

class SearchStrategy(str, Enum):
    """Available search strategies for adaptive RAG"""
    ADAPTIVE = "adaptive"
    VECTOR = "vector"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"
    PERFORMANCE_WEIGHTED = "performance_weighted"

class DeviceType(str, Enum):
    """Device types for UX optimization"""
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

class UserPersona(str, Enum):
    """User personas for personalized search"""
    TECH_EARLY_ADOPTER = "TechEarlyAdopter"
    REMOTE_DAD = "RemoteDad"
    STUDENT_HUSTLER = "StudentHustler"
    BUSINESS_OWNER = "BusinessOwner"

class QueryContext(BaseModel):
    """Context information for search optimization"""
    domain: Optional[str] = Field(None, description="Website domain context")
    user_persona: Optional[UserPersona] = Field(None, description="User persona classification")
    device_type: Optional[DeviceType] = Field(None, description="Device type for UX optimization")
    session_id: Optional[str] = Field(None, description="Session tracking")
    previous_queries: Optional[List[str]] = Field(default_factory=list, description="Query history")
    
class QueryRequest(BaseModel):
    """Search query request model"""
    query: str = Field(..., min_length=1, max_length=2000, description="Search query text")
    search_strategy: Optional[SearchStrategy] = Field(
        SearchStrategy.ADAPTIVE, 
        description="Search strategy selection"
    )
    context: Optional[QueryContext] = Field(None, description="Query context for optimization")
    max_results: Optional[int] = Field(10, ge=1, le=50, description="Maximum results to return")
    include_debug: Optional[bool] = Field(False, description="Include debug information")
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()

class SearchResult(BaseModel):
    """Individual search result"""
    content: str = Field(..., description="Result content")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_id: Optional[str] = Field(None, description="Source document ID")
    chunk_id: Optional[str] = Field(None, description="Chunk ID for traceability")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

class SearchResponse(BaseModel):
    """Search response with results and metadata"""
    results: List[SearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results found")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")
    strategy_used: str = Field(..., description="Search strategy that was used")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    query_id: Optional[str] = Field(None, description="Query ID for tracking")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    debug_info: Optional[Dict[str, Any]] = Field(None, description="Debug information")

class BulkQueryRequest(BaseModel):
    """Bulk search request for multiple queries"""
    queries: List[QueryRequest] = Field(..., min_items=1, max_items=100, description="List of queries")
    batch_optimization: bool = Field(True, description="Enable batch optimization")
    parallel_execution: bool = Field(True, description="Execute queries in parallel")

class FeedbackType(str, Enum):
    """Types of feedback for learning system"""
    EXPLICIT = "explicit"
    IMPLICIT = "implicit"
    AGENT = "agent"

class FeedbackData(BaseModel):
    """User feedback data for learning"""
    relevance_score: Optional[int] = Field(None, ge=1, le=5, description="Relevance rating 1-5")
    user_action: Optional[str] = Field(None, description="User action taken")
    time_spent: Optional[int] = Field(None, ge=0, description="Time spent with result")
    clicked_results: Optional[List[str]] = Field(default_factory=list, description="Clicked result IDs")
    conversion_event: Optional[bool] = Field(None, description="Conversion occurred")
    additional_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional feedback")

class FeedbackRequest(BaseModel):
    """Feedback submission request"""
    query_id: str = Field(..., description="Query ID for feedback")
    response_id: Optional[str] = Field(None, description="Response ID for feedback")
    feedback_type: FeedbackType = Field(..., description="Type of feedback")
    feedback_data: FeedbackData = Field(..., description="Feedback data")
    user_id: Optional[str] = Field(None, description="User ID for personalization")

class AgentQueryRequest(BaseModel):
    """Agent-to-agent query request following CLAUDE.md protocol"""
    agent_id: str = Field(..., description="Requesting agent ID")
    task_type: str = Field(..., description="Task type: research|content|technical|monetization")
    priority: str = Field(..., description="Priority: low|medium|high|critical")
    query: str = Field(..., description="Query or task description")
    expected_output: str = Field(..., description="Expected output format")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Agent context")
    deadline: Optional[datetime] = Field(None, description="Task deadline")

class AgentQueryResponse(BaseModel):
    """Agent query response"""
    agent_response: Dict[str, Any] = Field(..., description="Agent response data")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    processing_chain: List[str] = Field(..., description="Processing steps taken")
    execution_time_ms: int = Field(..., description="Execution time")
    status: str = Field(..., description="Response status")

class AgentFeedbackRequest(BaseModel):
    """Agent feedback for learning system"""
    agent_id: str = Field(..., description="Agent providing feedback")
    query_id: str = Field(..., description="Original query ID")
    outcome_success: bool = Field(..., description="Whether outcome was successful")
    performance_metrics: Dict[str, float] = Field(..., description="Performance metrics")
    improvement_suggestions: Optional[List[str]] = Field(default_factory=list, description="Improvement suggestions")

class PerformanceMetrics(BaseModel):
    """Performance analytics response"""
    avg_response_time: float = Field(..., description="Average response time in seconds")
    success_rate: float = Field(..., ge=0.0, le=1.0, description="Success rate")
    user_satisfaction: float = Field(..., ge=0.0, le=1.0, description="User satisfaction score")
    query_volume: int = Field(..., description="Number of queries processed")
    strategy_performance: Dict[str, Dict[str, float]] = Field(..., description="Per-strategy performance")
    improvement_trends: Dict[str, float] = Field(..., description="Performance improvement trends")
    time_period: str = Field(..., description="Time period for metrics")

class SystemHealth(BaseModel):
    """System health status"""
    status: str = Field(..., description="Overall system status")
    database_health: Dict[str, str] = Field(..., description="Database connection status")
    service_health: Dict[str, str] = Field(..., description="Service health status")
    resource_usage: Dict[str, float] = Field(..., description="Resource utilization")
    last_optimization: Optional[datetime] = Field(None, description="Last optimization timestamp")