"""
Learning Router - Week 2 Implementation
Milestone 1C: Feedback collection and continuous learning endpoints

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging
from datetime import datetime

from app.services.learning_service import ContinuousLearningService
from app.models.rag_models import (
    FeedbackRequest, FeedbackType, PerformanceMetrics
)
from core.auth.auth_dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize learning service
learning_service = ContinuousLearningService()

@router.post("/feedback")
async def submit_feedback(
    feedback: FeedbackRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Strategic feedback collection with outcome tracking
    
    Implements continuous learning through user feedback collection
    """
    try:
        logger.info(f"Processing feedback for query {feedback.query_id}")
        
        # Process feedback through learning service
        feedback_processed = await learning_service.collect_feedback(
            query_id=feedback.query_id,
            response_id=feedback.response_id,
            feedback_data=feedback.feedback_data.dict(),
            feedback_type=feedback.feedback_type,
            user_id=current_user.id if current_user else feedback.user_id
        )
        
        # Background learning update
        background_tasks.add_task(
            learning_service.update_learning_models,
            feedback
        )
        
        response = {
            "feedback_processed": feedback_processed,
            "learning_update_triggered": True,
            "message": "Feedback received and learning update scheduled",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Feedback processed successfully for query {feedback.query_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Feedback processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Feedback processing failed: {str(e)}"
        )

@router.post("/implicit-feedback")
async def process_implicit_feedback(
    interaction_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Strategic implicit feedback processing for automatic learning
    
    Processes CTR, time on page, conversion signals automatically
    """
    try:
        logger.debug(f"Processing implicit feedback: {interaction_data.get('event_type', 'unknown')}")
        
        # Process implicit feedback
        processed = await learning_service.process_implicit_feedback(
            interaction_data=interaction_data,
            user_id=current_user.id if current_user else None
        )
        
        # Background pattern analysis
        background_tasks.add_task(
            learning_service.analyze_interaction_patterns,
            interaction_data
        )
        
        return {
            "implicit_feedback_processed": processed,
            "pattern_analysis_triggered": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Implicit feedback processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Implicit feedback processing failed: {str(e)}"
        )

@router.get("/performance/trends")
async def get_learning_trends(
    time_window_days: int = 7,
    current_user = Depends(get_current_user)
):
    """
    Get learning performance trends and improvement metrics
    """
    try:
        trends = await learning_service.analyze_performance_trends(
            time_window_days=time_window_days,
            user_id=current_user.id if current_user else None
        )
        
        return trends
        
    except Exception as e:
        logger.error(f"Learning trends analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Learning trends analysis failed: {str(e)}"
        )

@router.post("/optimization/trigger")
async def trigger_auto_optimization(
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Strategic automated optimization execution
    
    Triggers system-wide learning optimization based on collected feedback
    """
    try:
        # Background auto-optimization
        background_tasks.add_task(
            learning_service.auto_optimize_system,
            user_id=current_user.id if current_user else None
        )
        
        return {
            "auto_optimization_triggered": True,
            "message": "System optimization started in background",
            "estimated_completion": "5-10 minutes",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Auto-optimization trigger failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Auto-optimization trigger failed: {str(e)}"
        )

@router.get("/insights/user-patterns")
async def get_user_learning_insights(
    user_persona: Optional[str] = None,
    device_type: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Get learning insights based on user patterns and personas
    
    Provides personalized learning insights for UX optimization
    """
    try:
        insights = await learning_service.get_user_learning_insights(
            user_persona=user_persona,
            device_type=device_type,
            user_id=current_user.id if current_user else None
        )
        
        return insights
        
    except Exception as e:
        logger.error(f"User learning insights failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"User learning insights failed: {str(e)}"
        )

@router.get("/metrics/learning-velocity")
async def get_learning_velocity_metrics():
    """
    Get learning velocity metrics showing improvement rate
    
    Strategic metric for tracking continuous improvement effectiveness
    """
    try:
        velocity_metrics = await learning_service.calculate_learning_velocity()
        
        return {
            "learning_velocity": velocity_metrics,
            "target_improvement": "10% weekly",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Learning velocity calculation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Learning velocity calculation failed: {str(e)}"
        )

# Health check for learning system
@router.get("/health")
async def learning_health_check():
    """Health check for learning system"""
    try:
        learning_health = await learning_service.health_check()
        
        return {
            "status": "healthy" if learning_health else "unhealthy",
            "learning_system": "operational" if learning_health else "degraded",
            "feedback_processing": "active" if learning_health else "inactive",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Learning health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }