# Real-Time Optimization API Controller for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .real_time_optimizer import RealTimeOptimizer
from .services import JourneySessionService
from ...database import get_db
from ...utils.auth import get_current_user
from ...utils.rate_limiting import rate_limit
from ...utils.monitoring import track_api_call, track_performance

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/journey/optimization", tags=["optimization"])

# =============================================================================
# OPTIMIZATION MODELS
# =============================================================================

class OptimizationRequest(BaseModel):
    """Request model for real-time optimization"""
    session_id: str = Field(..., description="Journey session ID")
    engagement_data: Dict[str, Any] = Field(..., description="Current engagement metrics")
    optimization_type: str = Field(default="comprehensive", description="Type of optimization: comprehensive, targeted, minimal")
    force_optimization: bool = Field(default=False, description="Force optimization ignoring cooldowns")

class FlowOptimizationRequest(BaseModel):
    """Request model for journey flow optimization"""
    session_id: str = Field(..., description="Journey session ID")
    current_metrics: Dict[str, Any] = Field(..., description="Current flow metrics")
    optimization_focus: Optional[str] = Field(None, description="Focus area: engagement, conversion, retention")

class AbandonmentPredictionRequest(BaseModel):
    """Request model for abandonment prediction and intervention"""
    session_id: str = Field(..., description="Journey session ID")
    behavioral_signals: Dict[str, Any] = Field(..., description="Current behavioral signals")
    intervention_level: str = Field(default="auto", description="Intervention level: minimal, moderate, aggressive, auto")

class ConversionOptimizationRequest(BaseModel):
    """Request model for conversion probability optimization"""
    session_id: str = Field(..., description="Journey session ID")
    conversion_signals: Dict[str, Any] = Field(..., description="Current conversion signals")
    optimization_strategy: Optional[str] = Field(None, description="Optimization strategy override")

class CrossDeviceOptimizationRequest(BaseModel):
    """Request model for cross-device optimization"""
    session_id: str = Field(..., description="Journey session ID")
    device_switch_data: Dict[str, Any] = Field(..., description="Device switch context data")
    continuity_requirements: Dict[str, Any] = Field(default_factory=dict, description="Continuity requirements")

class OptimizationResponse(BaseModel):
    """Response model for optimization operations"""
    success: bool = Field(..., description="Operation success status")
    session_id: str = Field(..., description="Journey session ID")
    optimization_applied: bool = Field(..., description="Whether optimization was applied")
    optimization_details: Dict[str, Any] = Field(default_factory=dict, description="Optimization details")
    performance_improvement: Dict[str, Any] = Field(default_factory=dict, description="Expected performance improvement")
    next_monitoring_interval: Optional[int] = Field(None, description="Next monitoring interval in seconds")

class OptimizationAnalyticsResponse(BaseModel):
    """Response model for optimization analytics"""
    optimization_performance: Dict[str, Any] = Field(..., description="Optimization performance metrics")
    success_rates: Dict[str, Any] = Field(..., description="Success rates by optimization type")
    impact_analysis: List[Dict[str, Any]] = Field(default_factory=list, description="Impact analysis")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Optimization recommendations")

# =============================================================================
# OPTIMIZATION ENDPOINTS
# =============================================================================

@router.post("/monitor", response_model=OptimizationResponse)
@track_api_call("optimization_monitor")
@rate_limit(requests_per_minute=300)
async def monitor_and_optimize_session(
    optimization_request: OptimizationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> OptimizationResponse:
    """
    Monitor session and apply real-time optimizations
    
    Continuously monitors journey session performance and applies
    real-time optimizations when performance thresholds are met.
    """
    try:
        session_id = optimization_request.session_id
        logger.info(f"Starting real-time optimization monitoring for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize optimizer
        optimizer = RealTimeOptimizer(db)
        
        # Monitor and optimize session
        with track_performance("real_time_optimization_monitoring"):
            optimization_result = await optimizer.monitor_and_optimize_session(
                session_id, optimization_request.engagement_data
            )
        
        # Handle errors from optimizer
        if "error" in optimization_result:
            raise HTTPException(status_code=500, detail=optimization_result["error"])
        
        # Background tasks for analytics and monitoring
        background_tasks.add_task(
            track_optimization_monitoring,
            session_id,
            optimization_request.optimization_type,
            optimization_result.get("optimization_applied", False)
        )
        
        background_tasks.add_task(
            update_optimization_analytics,
            session_id,
            optimization_result,
            optimization_request.engagement_data
        )
        
        logger.info(f"Optimization monitoring completed: {session_id}, optimization_applied: {optimization_result.get('optimization_applied', False)}")
        
        return OptimizationResponse(
            success=True,
            session_id=session_id,
            optimization_applied=optimization_result.get("optimization_applied", False),
            optimization_details=optimization_result.get("optimization_details", {}),
            performance_improvement=optimization_result.get("performance_improvement", {}),
            next_monitoring_interval=optimization_result.get("next_monitoring_interval")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimization monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization monitoring failed: {str(e)}")

@router.post("/flow", response_model=OptimizationResponse)
@track_api_call("optimization_flow")
@rate_limit(requests_per_minute=150)
async def optimize_journey_flow(
    flow_request: FlowOptimizationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> OptimizationResponse:
    """
    Optimize journey flow in real-time
    
    Analyzes journey flow bottlenecks and applies optimizations
    to improve progression and reduce friction.
    """
    try:
        session_id = flow_request.session_id
        logger.info(f"Optimizing journey flow for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize optimizer
        optimizer = RealTimeOptimizer(db)
        
        # Optimize journey flow
        with track_performance("journey_flow_optimization"):
            flow_optimization_result = await optimizer.optimize_journey_flow_real_time(
                session_id, flow_request.current_metrics
            )
        
        # Handle errors from optimizer
        if "error" in flow_optimization_result:
            raise HTTPException(status_code=500, detail=flow_optimization_result["error"])
        
        # Background tasks for tracking
        background_tasks.add_task(
            track_flow_optimization,
            session_id,
            flow_request.optimization_focus,
            flow_optimization_result.get("flow_optimizations_applied", 0)
        )
        
        logger.info(f"Journey flow optimization completed: {session_id}")
        
        return OptimizationResponse(
            success=True,
            session_id=session_id,
            optimization_applied=flow_optimization_result.get("flow_optimizations_applied", 0) > 0,
            optimization_details=flow_optimization_result,
            performance_improvement={
                "flow_improvement": flow_optimization_result.get("expected_flow_improvement", 0),
                "optimization_count": flow_optimization_result.get("flow_optimizations_applied", 0)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing journey flow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Flow optimization failed: {str(e)}")

@router.post("/abandonment-prevention", response_model=OptimizationResponse)
@track_api_call("optimization_abandonment_prevention")
@rate_limit(requests_per_minute=200)
async def predict_and_prevent_abandonment(
    abandonment_request: AbandonmentPredictionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> OptimizationResponse:
    """
    Predict and prevent session abandonment
    
    Analyzes behavioral signals to predict abandonment risk
    and applies preemptive interventions to retain users.
    """
    try:
        session_id = abandonment_request.session_id
        logger.info(f"Analyzing abandonment risk for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize optimizer
        optimizer = RealTimeOptimizer(db)
        
        # Predict and prevent abandonment
        with track_performance("abandonment_prediction_and_prevention"):
            abandonment_result = await optimizer.predict_and_preempt_abandonment(
                session_id, abandonment_request.behavioral_signals
            )
        
        # Handle errors from optimizer
        if "error" in abandonment_result:
            raise HTTPException(status_code=500, detail=abandonment_result["error"])
        
        # Determine if interventions were applied
        interventions_applied = "interventions_applied" in abandonment_result or "gentle_interventions" in abandonment_result
        
        # Background tasks for tracking
        background_tasks.add_task(
            track_abandonment_prediction,
            session_id,
            abandonment_result.get("abandonment_probability", 0),
            abandonment_result.get("abandonment_risk", "unknown"),
            interventions_applied
        )
        
        logger.info(f"Abandonment analysis completed: {session_id}, risk: {abandonment_result.get('abandonment_risk', 'unknown')}")
        
        return OptimizationResponse(
            success=True,
            session_id=session_id,
            optimization_applied=interventions_applied,
            optimization_details=abandonment_result,
            performance_improvement={
                "retention_improvement": abandonment_result.get("expected_retention_improvement", 0),
                "abandonment_risk_reduction": max(0, 0.8 - abandonment_result.get("abandonment_probability", 0.5))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in abandonment prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Abandonment prediction failed: {str(e)}")

@router.post("/conversion", response_model=OptimizationResponse)
@track_api_call("optimization_conversion")
@rate_limit(requests_per_minute=100)
async def optimize_conversion_probability(
    conversion_request: ConversionOptimizationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> OptimizationResponse:
    """
    Optimize conversion probability in real-time
    
    Analyzes conversion signals and applies targeted optimizations
    to increase conversion probability and revenue impact.
    """
    try:
        session_id = conversion_request.session_id
        logger.info(f"Optimizing conversion probability for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize optimizer
        optimizer = RealTimeOptimizer(db)
        
        # Optimize conversion probability
        with track_performance("conversion_probability_optimization"):
            conversion_result = await optimizer.optimize_conversion_probability_real_time(
                session_id, conversion_request.conversion_signals
            )
        
        # Handle errors from optimizer
        if "error" in conversion_result:
            raise HTTPException(status_code=500, detail=conversion_result["error"])
        
        # Background tasks for tracking
        background_tasks.add_task(
            track_conversion_optimization,
            session_id,
            conversion_result.get("previous_probability", 0),
            conversion_result.get("new_probability", 0),
            conversion_result.get("optimization_approach", "unknown")
        )
        
        logger.info(f"Conversion optimization completed: {session_id}, improvement: {conversion_result.get('probability_improvement', 0)}")
        
        return OptimizationResponse(
            success=True,
            session_id=session_id,
            optimization_applied=True,
            optimization_details=conversion_result,
            performance_improvement={
                "conversion_probability_improvement": conversion_result.get("probability_improvement", 0),
                "expected_revenue_impact": conversion_result.get("expected_revenue_impact", 0)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing conversion probability: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion optimization failed: {str(e)}")

@router.post("/cross-device", response_model=OptimizationResponse)
@track_api_call("optimization_cross_device")
@rate_limit(requests_per_minute=100)
async def optimize_cross_device_experience(
    cross_device_request: CrossDeviceOptimizationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> OptimizationResponse:
    """
    Optimize cross-device journey experience
    
    Optimizes experience during device switches to maintain
    journey continuity and engagement.
    """
    try:
        session_id = cross_device_request.session_id
        logger.info(f"Optimizing cross-device experience for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize optimizer
        optimizer = RealTimeOptimizer(db)
        
        # Optimize cross-device experience
        with track_performance("cross_device_optimization"):
            cross_device_result = await optimizer.cross_device_optimization(
                session_id, cross_device_request.device_switch_data
            )
        
        # Handle errors from optimizer
        if "error" in cross_device_result:
            raise HTTPException(status_code=500, detail=cross_device_result["error"])
        
        # Background tasks for tracking
        background_tasks.add_task(
            track_cross_device_optimization,
            session_id,
            cross_device_request.device_switch_data.get("previous_device"),
            cross_device_request.device_switch_data.get("new_device"),
            cross_device_result.get("seamless_handoff_achieved", False)
        )
        
        logger.info(f"Cross-device optimization completed: {session_id}")
        
        return OptimizationResponse(
            success=True,
            session_id=session_id,
            optimization_applied=cross_device_result.get("device_switch_optimized", False),
            optimization_details=cross_device_result,
            performance_improvement={
                "cross_device_experience_improvement": cross_device_result.get("cross_device_experience_score", 0.8),
                "continuity_score": cross_device_result.get("seamless_handoff_achieved", False)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing cross-device experience: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cross-device optimization failed: {str(e)}")

@router.get("/analytics/performance")
@track_api_call("optimization_analytics")
@rate_limit(requests_per_minute=50)
async def get_optimization_analytics(
    time_range: str = Query("7d", description="Time range: 7d, 30d, 90d"),
    optimization_type: Optional[str] = Query(None, description="Filter by optimization type"),
    persona_type: Optional[str] = Query(None, description="Filter by persona type"),
    journey_stage: Optional[str] = Query(None, description="Filter by journey stage"),
    db: AsyncSession = Depends(get_db)
) -> OptimizationAnalyticsResponse:
    """
    Get real-time optimization performance analytics
    
    Returns comprehensive analytics on optimization effectiveness,
    success rates, and performance improvements across sessions.
    """
    try:
        logger.debug(f"Getting optimization analytics for time range: {time_range}")
        
        # Initialize services (would implement AnalyticsService)
        # For now, return mock analytics data
        
        optimization_performance = {
            "total_optimizations": 18500,
            "successful_optimizations": 15725,
            "success_rate": 0.85,
            "average_performance_improvement": 0.18,
            "total_revenue_impact": 387500.00,
            "optimization_types": {
                "real_time_monitoring": {"count": 8000, "success_rate": 0.87},
                "flow_optimization": {"count": 4200, "success_rate": 0.82},
                "abandonment_prevention": {"count": 3800, "success_rate": 0.89},
                "conversion_optimization": {"count": 2100, "success_rate": 0.78},
                "cross_device_optimization": {"count": 400, "success_rate": 0.92}
            }
        }
        
        success_rates = {
            "by_persona": {
                "TechEarlyAdopter": 0.88,
                "StudentHustler": 0.91,
                "RemoteDad": 0.82,
                "BusinessOwner": 0.79
            },
            "by_stage": {
                "awareness": 0.83,
                "consideration": 0.87,
                "decision": 0.89,
                "conversion": 0.85
            },
            "by_device": {
                "mobile": 0.86,
                "tablet": 0.84,
                "desktop": 0.85
            }
        }
        
        impact_analysis = [
            {
                "optimization_type": "abandonment_prevention",
                "average_impact": 0.25,
                "revenue_attribution": 125000.00,
                "sessions_improved": 3400,
                "confidence": 0.94
            },
            {
                "optimization_type": "conversion_optimization",
                "average_impact": 0.22,
                "revenue_attribution": 98000.00,
                "sessions_improved": 1850,
                "confidence": 0.89
            },
            {
                "optimization_type": "flow_optimization",
                "average_impact": 0.15,
                "revenue_attribution": 87500.00,
                "sessions_improved": 3800,
                "confidence": 0.87
            }
        ]
        
        recommendations = [
            {
                "type": "optimization_frequency",
                "recommendation": "Increase monitoring frequency for high-value sessions (conversion probability > 0.7)",
                "expected_impact": 0.12,
                "implementation_priority": "high"
            },
            {
                "type": "abandonment_intervention",
                "recommendation": "Deploy preemptive abandonment interventions 30 seconds earlier",
                "expected_impact": 0.08,
                "implementation_priority": "medium"
            },
            {
                "type": "cross_device_optimization",
                "recommendation": "Implement predictive device switching to prepare optimizations in advance",
                "expected_impact": 0.15,
                "implementation_priority": "high"
            }
        ]
        
        return OptimizationAnalyticsResponse(
            optimization_performance=optimization_performance,
            success_rates=success_rates,
            impact_analysis=impact_analysis,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error getting optimization analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

@router.get("/health")
async def optimization_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Health check endpoint for optimization service"""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "service": "real_time_optimization_engine",
            "module": "2b_dynamic_customer_journey",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Optimization health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Optimization service unhealthy")

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def track_optimization_monitoring(session_id: str, optimization_type: str, optimization_applied: bool):
    """Background task to track optimization monitoring"""
    logger.info(f"Tracking optimization monitoring: {session_id}, {optimization_type}, applied: {optimization_applied}")
    # Implementation for monitoring tracking

async def update_optimization_analytics(session_id: str, optimization_result: Dict[str, Any], engagement_data: Dict[str, Any]):
    """Background task to update optimization analytics"""
    logger.debug(f"Updating optimization analytics: {session_id}")
    # Implementation for analytics updates

async def track_flow_optimization(session_id: str, optimization_focus: Optional[str], optimizations_applied: int):
    """Background task to track flow optimization"""
    logger.info(f"Tracking flow optimization: {session_id}, focus: {optimization_focus}, applied: {optimizations_applied}")
    # Implementation for flow optimization tracking

async def track_abandonment_prediction(session_id: str, abandonment_probability: float, risk_level: str, interventions_applied: bool):
    """Background task to track abandonment prediction"""
    logger.info(f"Tracking abandonment prediction: {session_id}, probability: {abandonment_probability}, risk: {risk_level}")
    # Implementation for abandonment tracking

async def track_conversion_optimization(session_id: str, previous_probability: float, new_probability: float, approach: str):
    """Background task to track conversion optimization"""
    logger.info(f"Tracking conversion optimization: {session_id}, improvement: {new_probability - previous_probability}")
    # Implementation for conversion tracking

async def track_cross_device_optimization(session_id: str, previous_device: str, new_device: str, seamless_handoff: bool):
    """Background task to track cross-device optimization"""
    logger.info(f"Tracking cross-device optimization: {session_id}, {previous_device} -> {new_device}, seamless: {seamless_handoff}")
    # Implementation for cross-device tracking