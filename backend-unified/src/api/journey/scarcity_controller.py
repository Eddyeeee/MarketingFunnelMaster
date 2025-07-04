# Scarcity Trigger API Controller for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .scarcity_engine import ScarcityTriggerEngine
from .services import JourneySessionService
from ...database import get_db
from ...utils.auth import get_current_user
from ...utils.rate_limiting import rate_limit
from ...utils.monitoring import track_api_call, track_performance

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/journey/scarcity", tags=["scarcity"])

# =============================================================================
# SCARCITY MODELS
# =============================================================================

class ScarcityEvaluationRequest(BaseModel):
    """Request model for scarcity trigger evaluation"""
    session_id: str = Field(..., description="Journey session ID")
    current_stage: JourneyStage = Field(..., description="Current journey stage")
    force_evaluation: bool = Field(default=False, description="Force evaluation ignoring cooldowns")
    trigger_preferences: Dict[str, Any] = Field(default_factory=dict, description="Trigger preferences")

class ScarcityApplicationRequest(BaseModel):
    """Request model for applying specific scarcity trigger"""
    session_id: str = Field(..., description="Journey session ID")
    trigger_type: str = Field(..., description="Type of scarcity trigger to apply")
    intensity_level: Optional[str] = Field(None, description="Intensity level: low, medium, high, very_high")
    custom_message: Optional[str] = Field(None, description="Custom trigger message")
    timing_preference: Optional[str] = Field(None, description="Timing preference: immediate, delayed, exit_intent")
    custom_params: Dict[str, Any] = Field(default_factory=dict, description="Custom trigger parameters")

class ScarcityTriggerResponse(BaseModel):
    """Response model for scarcity trigger operations"""
    success: bool = Field(..., description="Operation success status")
    session_id: str = Field(..., description="Journey session ID")
    triggers_applied: List[ScarcityTrigger] = Field(default_factory=list, description="Applied scarcity triggers")
    trigger_metadata: Dict[str, Any] = Field(default_factory=dict, description="Trigger metadata and analytics")
    next_trigger_opportunity: Optional[Dict[str, Any]] = Field(None, description="Next trigger opportunity")

class ScarcityEffectivenessResponse(BaseModel):
    """Response model for scarcity effectiveness analytics"""
    session_id: str = Field(..., description="Journey session ID")
    effectiveness_metrics: Dict[str, Any] = Field(..., description="Effectiveness metrics")
    trigger_performance: List[Dict[str, Any]] = Field(default_factory=list, description="Individual trigger performance")
    optimization_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Optimization recommendations")

class ScarcityConfigurationRequest(BaseModel):
    """Request model for scarcity configuration"""
    trigger_type: str = Field(..., description="Trigger type to configure")
    configuration: Dict[str, Any] = Field(..., description="Configuration parameters")
    apply_to_session: Optional[str] = Field(None, description="Apply to specific session")
    global_setting: bool = Field(default=False, description="Apply as global setting")

# =============================================================================
# SCARCITY TRIGGER ENDPOINTS
# =============================================================================

@router.post("/evaluate", response_model=ScarcityTriggerResponse)
@track_api_call("scarcity_evaluate")
@rate_limit(requests_per_minute=100)
async def evaluate_scarcity_triggers(
    evaluation_request: ScarcityEvaluationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> ScarcityTriggerResponse:
    """
    Evaluate and generate appropriate scarcity triggers
    
    Analyzes current journey state and user psychology to determine
    optimal scarcity triggers for conversion optimization.
    """
    try:
        session_id = evaluation_request.session_id
        logger.info(f"Evaluating scarcity triggers for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize services
        journey_service = JourneySessionService(db)
        scarcity_engine = ScarcityTriggerEngine(db)
        
        # Get journey session
        session = await journey_service._get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Journey session not found")
        
        # Evaluate scarcity triggers
        with track_performance("scarcity_trigger_evaluation"):
            triggers = await scarcity_engine.evaluate_scarcity_triggers(
                session, evaluation_request.current_stage
            )
        
        # Generate trigger metadata
        trigger_metadata = {
            "evaluation_timestamp": datetime.utcnow().isoformat(),
            "session_stage": evaluation_request.current_stage.value,
            "persona_type": session.persona_type,
            "conversion_probability": session.conversion_probability,
            "total_triggers_generated": len(triggers),
            "trigger_types": [t.trigger_type for t in triggers],
            "average_intensity": _calculate_average_intensity(triggers)
        }
        
        # Identify next trigger opportunity
        next_opportunity = await _identify_next_trigger_opportunity(session, triggers)
        
        # Background tasks for analytics and optimization
        background_tasks.add_task(
            track_scarcity_trigger_evaluation,
            session_id,
            evaluation_request.current_stage.value,
            len(triggers),
            trigger_metadata
        )
        
        background_tasks.add_task(
            update_scarcity_analytics,
            session_id,
            triggers,
            trigger_metadata
        )
        
        logger.info(f"Scarcity evaluation completed: {session_id}, {len(triggers)} triggers generated")
        
        return ScarcityTriggerResponse(
            success=True,
            session_id=session_id,
            triggers_applied=triggers,
            trigger_metadata=trigger_metadata,
            next_trigger_opportunity=next_opportunity
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error evaluating scarcity triggers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scarcity evaluation failed: {str(e)}")

@router.post("/apply", response_model=ScarcityTriggerResponse)
@track_api_call("scarcity_apply")
@rate_limit(requests_per_minute=50)
async def apply_scarcity_trigger(
    application_request: ScarcityApplicationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> ScarcityTriggerResponse:
    """
    Apply a specific scarcity trigger
    
    Applies a targeted scarcity trigger with custom parameters
    for immediate conversion optimization.
    """
    try:
        session_id = application_request.session_id
        trigger_type = application_request.trigger_type
        logger.info(f"Applying scarcity trigger: {trigger_type} for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Validate trigger type
        valid_trigger_types = ["social_proof", "time_pressure", "inventory", "exclusivity"]
        if trigger_type not in valid_trigger_types:
            raise HTTPException(status_code=400, detail=f"Invalid trigger type. Must be one of: {valid_trigger_types}")
        
        # Initialize services
        journey_service = JourneySessionService(db)
        scarcity_engine = ScarcityTriggerEngine(db)
        
        # Get journey session
        session = await journey_service._get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Journey session not found")
        
        # Prepare custom parameters
        custom_params = application_request.custom_params.copy()
        if application_request.intensity_level:
            custom_params["intensity"] = application_request.intensity_level
        if application_request.custom_message:
            custom_params["message"] = application_request.custom_message
        if application_request.timing_preference:
            custom_params["timing"] = application_request.timing_preference
        
        # Apply scarcity trigger
        with track_performance("scarcity_trigger_application"):
            trigger = await scarcity_engine.apply_scarcity_trigger(
                session, trigger_type, custom_params
            )
        
        # Generate trigger metadata
        trigger_metadata = {
            "application_timestamp": datetime.utcnow().isoformat(),
            "trigger_type": trigger_type,
            "custom_parameters": custom_params,
            "session_stage": session.current_stage,
            "conversion_probability": session.conversion_probability,
            "application_method": "manual",
            "expected_impact": _calculate_expected_impact(trigger, session)
        }
        
        # Background tasks for tracking and optimization
        background_tasks.add_task(
            track_manual_trigger_application,
            session_id,
            trigger_type,
            trigger.dict(),
            trigger_metadata
        )
        
        background_tasks.add_task(
            monitor_trigger_effectiveness,
            session_id,
            trigger.trigger_type,
            trigger_metadata["expected_impact"]
        )
        
        logger.info(f"Scarcity trigger applied successfully: {trigger_type} for session: {session_id}")
        
        return ScarcityTriggerResponse(
            success=True,
            session_id=session_id,
            triggers_applied=[trigger],
            trigger_metadata=trigger_metadata,
            next_trigger_opportunity=await _identify_next_trigger_opportunity(session, [trigger])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error applying scarcity trigger: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scarcity trigger application failed: {str(e)}")

@router.get("/effectiveness/{session_id}", response_model=ScarcityEffectivenessResponse)
@track_api_call("scarcity_effectiveness")
@rate_limit(requests_per_minute=100)
async def get_scarcity_effectiveness(
    session_id: str = Path(..., description="Journey session ID"),
    time_range: str = Query("24h", description="Time range: 1h, 24h, 7d"),
    include_recommendations: bool = Query(True, description="Include optimization recommendations"),
    db: AsyncSession = Depends(get_db)
) -> ScarcityEffectivenessResponse:
    """
    Get scarcity trigger effectiveness metrics
    
    Returns comprehensive analytics on scarcity trigger performance
    and provides optimization recommendations.
    """
    try:
        logger.debug(f"Getting scarcity effectiveness for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize services
        scarcity_engine = ScarcityTriggerEngine(db)
        
        # Get effectiveness metrics
        with track_performance("scarcity_effectiveness_analysis"):
            effectiveness_metrics = await scarcity_engine.get_trigger_effectiveness(session_id, time_range)
        
        # Generate trigger performance breakdown
        trigger_performance = []
        if "trigger_types_used" in effectiveness_metrics:
            for trigger_type, stats in effectiveness_metrics["trigger_types_used"].items():
                trigger_performance.append({
                    "trigger_type": trigger_type,
                    "applications": stats["count"],
                    "conversions": stats["conversions"],
                    "conversion_rate": stats.get("conversion_rate", 0.0),
                    "avg_engagement_change": stats.get("avg_engagement_change", 0.0),
                    "effectiveness_score": _calculate_effectiveness_score(stats)
                })
        
        # Generate optimization recommendations
        optimization_recommendations = []
        if include_recommendations:
            optimization_recommendations = await _generate_scarcity_optimization_recommendations(
                effectiveness_metrics, trigger_performance
            )
        
        return ScarcityEffectivenessResponse(
            session_id=session_id,
            effectiveness_metrics=effectiveness_metrics,
            trigger_performance=trigger_performance,
            optimization_recommendations=optimization_recommendations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting scarcity effectiveness: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Effectiveness analysis failed: {str(e)}")

@router.get("/analytics/performance")
@track_api_call("scarcity_analytics")
@rate_limit(requests_per_minute=50)
async def get_scarcity_analytics(
    time_range: str = Query("7d", description="Time range: 7d, 30d, 90d"),
    trigger_type: Optional[str] = Query(None, description="Filter by trigger type"),
    persona_type: Optional[str] = Query(None, description="Filter by persona type"),
    journey_stage: Optional[str] = Query(None, description="Filter by journey stage"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive scarcity trigger analytics
    
    Returns aggregate analytics across all sessions and trigger types
    with performance insights and trend analysis.
    """
    try:
        logger.debug(f"Getting scarcity analytics for time range: {time_range}")
        
        # Initialize services (would implement AnalyticsService)
        # For now, return mock analytics data
        
        scarcity_analytics = {
            "overview": {
                "total_triggers_applied": 15000,
                "total_conversions_attributed": 3200,
                "overall_conversion_rate": 0.213,
                "average_engagement_lift": 0.18,
                "total_revenue_attributed": 487500.00
            },
            "trigger_type_performance": {
                "social_proof": {
                    "applications": 6000,
                    "conversions": 1440,
                    "conversion_rate": 0.24,
                    "avg_engagement_lift": 0.15,
                    "revenue_attributed": 198000.00
                },
                "time_pressure": {
                    "applications": 4500,
                    "conversions": 1080,
                    "conversion_rate": 0.24,
                    "avg_engagement_lift": 0.22,
                    "revenue_attributed": 162000.00
                },
                "inventory": {
                    "applications": 3500,
                    "conversions": 560,
                    "conversion_rate": 0.16,
                    "avg_engagement_lift": 0.12,
                    "revenue_attributed": 84000.00
                },
                "exclusivity": {
                    "applications": 1000,
                    "conversions": 120,
                    "conversion_rate": 0.12,
                    "avg_engagement_lift": 0.25,
                    "revenue_attributed": 43500.00
                }
            },
            "persona_performance": {
                "TechEarlyAdopter": {
                    "best_trigger_type": "social_proof",
                    "conversion_rate": 0.28,
                    "preferred_intensity": "high"
                },
                "StudentHustler": {
                    "best_trigger_type": "time_pressure",
                    "conversion_rate": 0.31,
                    "preferred_intensity": "very_high"
                },
                "RemoteDad": {
                    "best_trigger_type": "social_proof",
                    "conversion_rate": 0.19,
                    "preferred_intensity": "medium"
                },
                "BusinessOwner": {
                    "best_trigger_type": "exclusivity",
                    "conversion_rate": 0.15,
                    "preferred_intensity": "low"
                }
            },
            "stage_performance": {
                "awareness": {
                    "effective_triggers": ["social_proof", "exclusivity"],
                    "avg_conversion_rate": 0.12
                },
                "consideration": {
                    "effective_triggers": ["social_proof", "inventory"],
                    "avg_conversion_rate": 0.18
                },
                "decision": {
                    "effective_triggers": ["time_pressure", "inventory"],
                    "avg_conversion_rate": 0.35
                }
            },
            "optimization_insights": [
                {
                    "insight": "Time pressure triggers show 22% higher engagement on mobile devices",
                    "recommendation": "Prioritize time pressure for mobile users",
                    "expected_impact": 0.15
                },
                {
                    "insight": "Social proof triggers are most effective during peak traffic hours",
                    "recommendation": "Schedule social proof triggers for 2-4 PM and 8-10 PM",
                    "expected_impact": 0.12
                },
                {
                    "insight": "Inventory scarcity works better with visual stock indicators",
                    "recommendation": "Add visual stock level bars to inventory triggers",
                    "expected_impact": 0.18
                }
            ]
        }
        
        # Apply filters if specified
        if trigger_type:
            scarcity_analytics["filtered_by_trigger_type"] = trigger_type
        if persona_type:
            scarcity_analytics["filtered_by_persona"] = persona_type
        if journey_stage:
            scarcity_analytics["filtered_by_stage"] = journey_stage
        
        return scarcity_analytics
        
    except Exception as e:
        logger.error(f"Error getting scarcity analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scarcity analytics failed: {str(e)}")

@router.post("/configure")
@track_api_call("scarcity_configure")
@rate_limit(requests_per_minute=20)
async def configure_scarcity_triggers(
    configuration_request: ScarcityConfigurationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Configure scarcity trigger parameters
    
    Allows customization of scarcity trigger behavior, timing,
    and effectiveness parameters for optimization.
    """
    try:
        trigger_type = configuration_request.trigger_type
        logger.info(f"Configuring scarcity trigger: {trigger_type}")
        
        # Validate trigger type
        valid_trigger_types = ["social_proof", "time_pressure", "inventory", "exclusivity"]
        if trigger_type not in valid_trigger_types:
            raise HTTPException(status_code=400, detail=f"Invalid trigger type. Must be one of: {valid_trigger_types}")
        
        # Initialize services
        scarcity_engine = ScarcityTriggerEngine(db)
        
        # Apply configuration
        configuration_result = {
            "trigger_type": trigger_type,
            "configuration": configuration_request.configuration,
            "applied_at": datetime.utcnow().isoformat(),
            "scope": "global" if configuration_request.global_setting else "session",
            "status": "applied"
        }
        
        # Apply to specific session if requested
        if configuration_request.apply_to_session:
            session_id = configuration_request.apply_to_session
            # Apply session-specific configuration
            cache_key = f"scarcity_config:{session_id}:{trigger_type}"
            await scarcity_engine.redis_client.setex(
                cache_key, 
                3600,  # 1 hour
                json.dumps(configuration_request.configuration)
            )
            configuration_result["applied_to_session"] = session_id
        
        # Background task for configuration tracking
        background_tasks.add_task(
            track_scarcity_configuration,
            trigger_type,
            configuration_request.configuration,
            configuration_request.global_setting
        )
        
        return {
            "success": True,
            "configuration_result": configuration_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error configuring scarcity triggers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scarcity configuration failed: {str(e)}")

@router.get("/health")
async def scarcity_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Health check endpoint for scarcity service"""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "service": "scarcity_trigger_engine",
            "module": "2b_dynamic_customer_journey",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Scarcity health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Scarcity service unhealthy")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _calculate_average_intensity(triggers: List[ScarcityTrigger]) -> str:
    """Calculate average intensity of triggers"""
    if not triggers:
        return "none"
    
    intensity_values = {"low": 1, "medium": 2, "high": 3, "very_high": 4}
    intensity_names = {1: "low", 2: "medium", 3: "high", 4: "very_high"}
    
    total_intensity = sum(intensity_values.get(t.intensity, 2) for t in triggers)
    average_intensity = total_intensity / len(triggers)
    
    return intensity_names.get(round(average_intensity), "medium")

async def _identify_next_trigger_opportunity(session, applied_triggers: List[ScarcityTrigger]) -> Optional[Dict[str, Any]]:
    """Identify next optimal trigger opportunity"""
    applied_types = [t.trigger_type for t in applied_triggers]
    
    # Suggest next trigger based on what hasn't been used
    all_trigger_types = ["social_proof", "time_pressure", "inventory", "exclusivity"]
    unused_types = [t for t in all_trigger_types if t not in applied_types]
    
    if unused_types:
        next_type = unused_types[0]  # Could be more sophisticated
        return {
            "trigger_type": next_type,
            "recommended_timing": "15_minutes",
            "expected_impact": 0.15,
            "reasoning": f"Complement existing triggers with {next_type}"
        }
    
    return None

def _calculate_expected_impact(trigger: ScarcityTrigger, session) -> float:
    """Calculate expected impact of trigger based on session context"""
    base_impact = {
        "social_proof": 0.12,
        "time_pressure": 0.18,
        "inventory": 0.15,
        "exclusivity": 0.10
    }.get(trigger.trigger_type, 0.10)
    
    # Adjust based on intensity
    intensity_multiplier = {
        "low": 0.7,
        "medium": 1.0,
        "high": 1.3,
        "very_high": 1.6
    }.get(trigger.intensity, 1.0)
    
    # Adjust based on conversion probability
    if session.conversion_probability > 0.7:
        probability_multiplier = 1.2
    elif session.conversion_probability < 0.3:
        probability_multiplier = 0.8
    else:
        probability_multiplier = 1.0
    
    return base_impact * intensity_multiplier * probability_multiplier

def _calculate_effectiveness_score(stats: Dict[str, Any]) -> float:
    """Calculate overall effectiveness score for a trigger type"""
    conversion_rate = stats.get("conversion_rate", 0.0)
    engagement_change = stats.get("avg_engagement_change", 0.0)
    
    # Weighted combination of conversion rate and engagement change
    effectiveness_score = (conversion_rate * 0.7) + (engagement_change * 0.3)
    return min(1.0, max(0.0, effectiveness_score))

async def _generate_scarcity_optimization_recommendations(effectiveness_metrics: Dict[str, Any], trigger_performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate optimization recommendations based on effectiveness data"""
    recommendations = []
    
    # Low performing trigger types
    for perf in trigger_performance:
        if perf["effectiveness_score"] < 0.5:
            recommendations.append({
                "type": "trigger_optimization",
                "trigger_type": perf["trigger_type"],
                "issue": "low_effectiveness",
                "recommendation": f"Consider reducing frequency or adjusting intensity for {perf['trigger_type']} triggers",
                "expected_improvement": 0.08
            })
    
    # High performing trigger types
    best_trigger = effectiveness_metrics.get("most_effective_trigger")
    if best_trigger:
        recommendations.append({
            "type": "trigger_amplification",
            "trigger_type": best_trigger,
            "recommendation": f"Increase usage of {best_trigger} triggers as they show highest effectiveness",
            "expected_improvement": 0.15
        })
    
    # Overall conversion rate recommendations
    overall_rate = effectiveness_metrics.get("conversion_rate", 0.0)
    if overall_rate < 0.15:
        recommendations.append({
            "type": "strategy_adjustment",
            "recommendation": "Consider A/B testing different trigger messages and timing",
            "expected_improvement": 0.12
        })
    
    return recommendations

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def track_scarcity_trigger_evaluation(session_id: str, stage: str, trigger_count: int, metadata: Dict[str, Any]):
    """Background task to track trigger evaluation"""
    logger.info(f"Tracking scarcity evaluation: {session_id}, {stage}, {trigger_count} triggers")
    # Implementation for evaluation tracking

async def update_scarcity_analytics(session_id: str, triggers: List[ScarcityTrigger], metadata: Dict[str, Any]):
    """Background task to update scarcity analytics"""
    logger.debug(f"Updating scarcity analytics: {session_id}, {len(triggers)} triggers")
    # Implementation for analytics updates

async def track_manual_trigger_application(session_id: str, trigger_type: str, trigger_data: Dict[str, Any], metadata: Dict[str, Any]):
    """Background task to track manual trigger application"""
    logger.info(f"Tracking manual trigger: {session_id}, {trigger_type}")
    # Implementation for manual trigger tracking

async def monitor_trigger_effectiveness(session_id: str, trigger_type: str, expected_impact: float):
    """Background task to monitor trigger effectiveness"""
    logger.debug(f"Monitoring trigger effectiveness: {session_id}, {trigger_type}, {expected_impact}")
    # Implementation for effectiveness monitoring

async def track_scarcity_configuration(trigger_type: str, configuration: Dict[str, Any], global_setting: bool):
    """Background task to track scarcity configuration changes"""
    logger.info(f"Tracking scarcity configuration: {trigger_type}, global: {global_setting}")
    # Implementation for configuration tracking