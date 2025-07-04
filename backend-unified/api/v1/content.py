#!/usr/bin/env python3
"""
Content Generation API Routes
Module 3A: AI Content Generation Pipeline API Implementation

Executor: Claude Code
Erstellt: 2025-07-04 (Module 3A Phase 1)
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from uuid import UUID, uuid4
from datetime import datetime
import logging

from backend_unified.core.agents.orchestrator import AgentOrchestrator
from models.unified_models import (
    ContentOutlineEntity, ContentPieceEntity, VisualAssetEntity, 
    SocialAdaptationEntity, ContentTemplateEntity, ContentPipelineEntity,
    create_content_outline_entity, create_content_piece_entity, create_content_pipeline_entity,
    EntityType, RelationshipType, OutcomeType
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize agent orchestrator (will be dependency injected in production)
orchestrator = AgentOrchestrator()

# Request/Response Models
class ContentGenerationRequest(BaseModel):
    """Content generation request model"""
    niche: str = Field(description="Target niche")
    persona: str = Field(description="Target persona (tech_early_adopter, remote_dad, student_hustler, business_owner)")
    device: str = Field(description="Target device (mobile, tablet, desktop)")
    content_type: str = Field(default="blog_post", description="Type of content to generate")
    template_id: Optional[UUID] = Field(default=None, description="Optional template to use")
    custom_requirements: Dict[str, Any] = Field(default_factory=dict, description="Custom requirements")

class ContentGenerationResponse(BaseModel):
    """Content generation response model"""
    pipeline_id: UUID = Field(description="Pipeline execution ID")
    status: str = Field(description="Generation status")
    content: Optional[Dict[str, Any]] = Field(default=None, description="Generated content")
    visual_assets: Optional[Dict[str, Any]] = Field(default=None, description="Generated visual assets")
    social_adaptations: Optional[Dict[str, Any]] = Field(default=None, description="Social media adaptations")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    error: Optional[str] = Field(default=None, description="Error message if failed")

class ContentOptimizationRequest(BaseModel):
    """Content optimization request model"""
    content_id: UUID = Field(description="Content piece ID to optimize")
    optimization_goals: List[str] = Field(description="Optimization objectives")
    current_performance: Dict[str, float] = Field(description="Current performance metrics")

class TemplateCreationRequest(BaseModel):
    """Template creation request model"""
    template_name: str = Field(description="Template name")
    template_category: str = Field(description="Template category")
    target_niche: str = Field(description="Target niche")
    template_structure: Dict[str, Any] = Field(description="Template structure")
    persona_adaptations: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    device_optimizations: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

# Dependency injection for orchestrator
async def get_orchestrator() -> AgentOrchestrator:
    """Get agent orchestrator instance"""
    if not orchestrator.initialized:
        await orchestrator.initialize()
    return orchestrator

# Main Content Generation Endpoints

@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_content_pipeline(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    agent_orchestrator: AgentOrchestrator = Depends(get_orchestrator)
) -> ContentGenerationResponse:
    """
    Generate complete content package including text, visuals, and social adaptations
    
    This is the main content generation endpoint that orchestrates the full pipeline:
    1. Content outline generation
    2. Content writing with persona optimization
    3. Visual asset generation (parallel)
    4. Social media adaptation (parallel)
    """
    try:
        logger.info(f"Starting content generation pipeline: {request.niche}-{request.persona}-{request.device}")
        
        # Execute content generation pipeline
        pipeline_result = await agent_orchestrator.generate_content_pipeline(
            niche=request.niche,
            persona=request.persona,
            device=request.device,
            content_type=request.content_type
        )
        
        # Create pipeline entity for tracking
        pipeline_entity = create_content_pipeline_entity(
            niche=request.niche,
            persona=request.persona,
            device=request.device
        )
        
        # Add background task for performance tracking
        background_tasks.add_task(
            track_pipeline_performance,
            pipeline_entity.id,
            pipeline_result
        )
        
        return ContentGenerationResponse(
            pipeline_id=pipeline_entity.pipeline_id,
            status=pipeline_result.get("status", "completed"),
            content=pipeline_result.get("content"),
            visual_assets=pipeline_result.get("visual_assets"),
            social_adaptations=pipeline_result.get("social_adaptations"),
            performance_metrics=pipeline_result.get("performance_metrics", {}),
            error=pipeline_result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@router.get("/pipeline/{pipeline_id}")
async def get_pipeline_status(pipeline_id: UUID) -> Dict[str, Any]:
    """Get content generation pipeline status"""
    try:
        # In production, this would query the database for pipeline status
        # For now, return mock status
        return {
            "pipeline_id": str(pipeline_id),
            "status": "completed",
            "stages_completed": 4,
            "total_stages": 4,
            "execution_time_seconds": 5.2,
            "quality_score": 0.87
        }
    except Exception as e:
        logger.error(f"Failed to get pipeline status: {e}")
        raise HTTPException(status_code=404, detail="Pipeline not found")

@router.post("/optimize/{content_id}")
async def optimize_content(
    content_id: UUID,
    request: ContentOptimizationRequest,
    agent_orchestrator: AgentOrchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Optimize existing content based on performance data"""
    try:
        logger.info(f"Optimizing content {content_id} with goals: {request.optimization_goals}")
        
        # In production, this would:
        # 1. Retrieve original content from database
        # 2. Analyze performance gaps
        # 3. Generate optimization suggestions
        # 4. Apply optimizations
        
        return {
            "content_id": str(content_id),
            "optimization_status": "completed",
            "improvements_applied": [
                "Enhanced call-to-action placement",
                "Improved persona-specific language",
                "Optimized for mobile readability"
            ],
            "predicted_performance_improvement": 0.15,
            "optimization_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Content optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

# Template Management Endpoints

@router.post("/templates", response_model=Dict[str, Any])
async def create_content_template(request: TemplateCreationRequest) -> Dict[str, Any]:
    """Create a new content template"""
    try:
        template_entity = ContentTemplateEntity(
            name=request.template_name,
            template_name=request.template_name,
            template_category=request.template_category,
            target_niche=request.target_niche,
            template_structure=request.template_structure,
            persona_adaptations=request.persona_adaptations,
            device_optimizations=request.device_optimizations
        )
        
        # In production, save to database
        
        return {
            "template_id": str(template_entity.id),
            "template_name": template_entity.template_name,
            "status": "created",
            "created_at": template_entity.created_at.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Template creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Template creation failed: {str(e)}")

@router.get("/templates")
async def list_content_templates(
    niche: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """List available content templates"""
    try:
        # Mock template data - in production, query database
        templates = [
            {
                "template_id": str(uuid4()),
                "template_name": "Tech Product Review",
                "template_category": "product_review",
                "target_niche": "technology",
                "usage_count": 42,
                "average_performance": 0.78
            },
            {
                "template_id": str(uuid4()),
                "template_name": "Family Solution Guide",
                "template_category": "how_to_guide",
                "target_niche": "family_lifestyle",
                "usage_count": 28,
                "average_performance": 0.82
            }
        ]
        
        # Apply filters
        if niche:
            templates = [t for t in templates if t["target_niche"] == niche]
        if category:
            templates = [t for t in templates if t["template_category"] == category]
        
        return {
            "templates": templates[:limit],
            "total_count": len(templates),
            "filters_applied": {"niche": niche, "category": category}
        }
        
    except Exception as e:
        logger.error(f"Template listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Template listing failed: {str(e)}")

@router.get("/templates/{template_id}")
async def get_content_template(template_id: UUID) -> Dict[str, Any]:
    """Get specific content template details"""
    try:
        # Mock template data - in production, query database
        return {
            "template_id": str(template_id),
            "template_name": "Tech Product Review",
            "template_category": "product_review",
            "target_niche": "technology",
            "template_structure": {
                "sections": [
                    "Product Introduction",
                    "Key Features Analysis",
                    "Pros and Cons",
                    "Price Comparison",
                    "Final Verdict"
                ],
                "word_count_target": 1500,
                "seo_keywords": ["best", "review", "features", "price"]
            },
            "persona_adaptations": {
                "tech_early_adopter": {
                    "focus": "cutting_edge_features",
                    "tone": "technical_enthusiast"
                },
                "business_owner": {
                    "focus": "roi_and_efficiency",
                    "tone": "professional_analytical"
                }
            },
            "device_optimizations": {
                "mobile": {
                    "paragraph_length": "short",
                    "cta_placement": "frequent"
                },
                "desktop": {
                    "paragraph_length": "medium",
                    "cta_placement": "strategic"
                }
            },
            "usage_count": 42,
            "average_performance": 0.78
        }
        
    except Exception as e:
        logger.error(f"Template retrieval failed: {e}")
        raise HTTPException(status_code=404, detail="Template not found")

# Analytics and Performance Endpoints

@router.get("/analytics")
async def get_content_analytics(
    time_period: str = "7d",
    niche: Optional[str] = None,
    persona: Optional[str] = None
) -> Dict[str, Any]:
    """Get content generation analytics"""
    try:
        # Mock analytics data - in production, query from analytics system
        return {
            "time_period": time_period,
            "total_content_generated": 127,
            "average_generation_time_seconds": 4.8,
            "quality_score_average": 0.84,
            "persona_performance": {
                "tech_early_adopter": {"conversion_rate": 0.15, "engagement_score": 0.78},
                "remote_dad": {"conversion_rate": 0.22, "engagement_score": 0.71},
                "student_hustler": {"conversion_rate": 0.18, "engagement_score": 0.82},
                "business_owner": {"conversion_rate": 0.25, "engagement_score": 0.69}
            },
            "device_performance": {
                "mobile": {"conversion_rate": 0.19, "avg_time_on_page": 45},
                "tablet": {"conversion_rate": 0.21, "avg_time_on_page": 67},
                "desktop": {"conversion_rate": 0.23, "avg_time_on_page": 89}
            },
            "top_performing_niches": [
                {"niche": "smart_home", "conversion_rate": 0.28},
                {"niche": "fitness_tracking", "conversion_rate": 0.24},
                {"niche": "productivity_tools", "conversion_rate": 0.21}
            ]
        }
        
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

@router.get("/performance/{content_id}")
async def get_content_performance(content_id: UUID) -> Dict[str, Any]:
    """Get performance metrics for specific content piece"""
    try:
        # Mock performance data - in production, query from analytics system
        return {
            "content_id": str(content_id),
            "performance_metrics": {
                "views": 2847,
                "unique_visitors": 1923,
                "conversion_rate": 0.18,
                "average_time_on_page": 67,
                "bounce_rate": 0.34,
                "social_shares": 89,
                "comments": 23
            },
            "persona_breakdown": {
                "tech_early_adopter": {"percentage": 45, "conversion_rate": 0.21},
                "business_owner": {"percentage": 32, "conversion_rate": 0.19},
                "student_hustler": {"percentage": 23, "conversion_rate": 0.14}
            },
            "device_breakdown": {
                "mobile": {"percentage": 58, "conversion_rate": 0.16},
                "desktop": {"percentage": 32, "conversion_rate": 0.22},
                "tablet": {"percentage": 10, "conversion_rate": 0.19}
            },
            "optimization_suggestions": [
                "Enhance mobile call-to-action visibility",
                "Add more technical details for early adopters",
                "Include pricing comparison section"
            ]
        }
        
    except Exception as e:
        logger.error(f"Performance retrieval failed: {e}")
        raise HTTPException(status_code=404, detail="Content performance not found")

# Health and Status Endpoints

@router.get("/health")
async def content_generation_health(
    agent_orchestrator: AgentOrchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Check content generation system health"""
    try:
        orchestrator_health = await agent_orchestrator.health_check()
        debug_info = await agent_orchestrator.get_debug_info()
        
        return {
            "status": "healthy" if orchestrator_health else "unhealthy",
            "orchestrator_initialized": orchestrator_health,
            "registered_agents": debug_info.get("agents_count", 0),
            "active_tasks": debug_info.get("active_tasks", 0),
            "agent_details": debug_info.get("agents", {}),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/agents")
async def list_content_agents(
    agent_orchestrator: AgentOrchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """List all registered content generation agents"""
    try:
        debug_info = await agent_orchestrator.get_debug_info()
        
        return {
            "agents": debug_info.get("agents", {}),
            "total_agents": debug_info.get("agents_count", 0),
            "active_tasks": debug_info.get("active_tasks", 0),
            "system_initialized": debug_info.get("initialized", False)
        }
        
    except Exception as e:
        logger.error(f"Agent listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent listing failed: {str(e)}")

# Background task functions

async def track_pipeline_performance(pipeline_id: UUID, pipeline_result: Dict[str, Any]):
    """Background task to track pipeline performance"""
    try:
        logger.info(f"Tracking performance for pipeline {pipeline_id}")
        
        # In production, this would:
        # 1. Store pipeline execution data
        # 2. Update performance metrics
        # 3. Trigger learning updates
        # 4. Generate performance reports
        
        # Mock implementation
        performance_data = {
            "pipeline_id": str(pipeline_id),
            "execution_time": pipeline_result.get("performance_metrics", {}).get("generation_time_seconds", 0),
            "quality_score": pipeline_result.get("performance_metrics", {}).get("quality_score", 0),
            "status": pipeline_result.get("status", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Performance tracked: {performance_data}")
        
    except Exception as e:
        logger.error(f"Performance tracking failed: {e}")

# Router configuration
router.tags = ["Content Generation"]