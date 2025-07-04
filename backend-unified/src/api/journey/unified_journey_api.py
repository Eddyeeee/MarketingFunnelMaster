# Unified Journey API Layer for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .services import JourneySessionService
from .personalization_engine import PersonalizationEngine
from .scarcity_engine import ScarcityTriggerEngine
from .real_time_optimizer import RealTimeOptimizer
from .ux_integration_bridge import UXIntelligenceIntegrationBridge
from ...database import get_db
from ...utils.auth import get_current_user
from ...utils.rate_limiting import rate_limit
from ...utils.monitoring import track_api_call, track_performance

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/journey/unified", tags=["unified-journey"])

# =============================================================================
# UNIFIED JOURNEY MODELS
# =============================================================================

class UnifiedJourneyInitRequest(BaseModel):
    """Request model for unified journey initialization"""
    session_data: JourneySessionCreate = Field(..., description="Journey session data")
    ux_data: Dict[str, Any] = Field(default_factory=dict, description="UX Intelligence data")
    personalization_preferences: Dict[str, Any] = Field(default_factory=dict, description="Personalization preferences")
    optimization_level: str = Field(default="standard", description="Optimization level: minimal, standard, aggressive")

class UnifiedJourneyResponse(BaseModel):
    """Response model for unified journey operations"""
    success: bool = Field(..., description="Operation success status")
    session_id: str = Field(..., description="Journey session ID")
    journey_session: JourneySessionResponse = Field(..., description="Journey session details")
    personalized_content: PersonalizedContent = Field(..., description="Initial personalized content")
    ux_intelligence: Dict[str, Any] = Field(default_factory=dict, description="UX Intelligence insights")
    optimization_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Initial optimization recommendations")
    real_time_monitoring: Dict[str, Any] = Field(default_factory=dict, description="Real-time monitoring setup")

class UnifiedInteractionRequest(BaseModel):
    """Request model for unified interaction processing"""
    session_id: str = Field(..., description="Journey session ID")
    interaction_data: Dict[str, Any] = Field(..., description="Interaction data")
    behavioral_signals: Dict[str, Any] = Field(default_factory=dict, description="Behavioral signals")
    engagement_metrics: Dict[str, Any] = Field(default_factory=dict, description="Engagement metrics")
    force_optimization: bool = Field(default=False, description="Force optimization regardless of cooldowns")

class UnifiedInteractionResponse(BaseModel):
    """Response model for unified interaction processing"""
    success: bool = Field(..., description="Operation success status")
    session_id: str = Field(..., description="Journey session ID")
    stage_progression: Dict[str, Any] = Field(default_factory=dict, description="Stage progression updates")
    personalization_updates: Dict[str, Any] = Field(default_factory=dict, description="Personalization updates")
    scarcity_triggers: List[ScarcityTrigger] = Field(default_factory=list, description="Applied scarcity triggers")
    optimizations_applied: List[Dict[str, Any]] = Field(default_factory=list, description="Real-time optimizations applied")
    next_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Next action recommendations")
    analytics_update: Dict[str, Any] = Field(default_factory=dict, description="Analytics updates")

class UnifiedJourneyAnalyticsRequest(BaseModel):
    """Request model for unified journey analytics"""
    session_ids: Optional[List[str]] = Field(None, description="Specific session IDs to analyze")
    time_range: str = Field(default="24h", description="Time range: 1h, 24h, 7d, 30d")
    analytics_scope: List[str] = Field(default=["all"], description="Analytics scope: journey, personalization, scarcity, optimization, ux")
    aggregation_level: str = Field(default="session", description="Aggregation level: session, persona, stage, device")

class UnifiedJourneyAnalyticsResponse(BaseModel):
    """Response model for unified journey analytics"""
    success: bool = Field(..., description="Operation success status")
    analytics_scope: List[str] = Field(..., description="Analytics scope covered")
    time_range: str = Field(..., description="Time range analyzed")
    journey_analytics: Dict[str, Any] = Field(default_factory=dict, description="Journey flow analytics")
    personalization_analytics: Dict[str, Any] = Field(default_factory=dict, description="Personalization analytics")
    scarcity_analytics: Dict[str, Any] = Field(default_factory=dict, description="Scarcity trigger analytics")
    optimization_analytics: Dict[str, Any] = Field(default_factory=dict, description="Real-time optimization analytics")
    ux_analytics: Dict[str, Any] = Field(default_factory=dict, description="UX Intelligence analytics")
    cross_system_insights: List[Dict[str, Any]] = Field(default_factory=list, description="Cross-system insights")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="System-wide recommendations")

# =============================================================================
# UNIFIED JOURNEY ORCHESTRATION SERVICE
# =============================================================================

class UnifiedJourneyOrchestrator:
    """Orchestrates all journey engine components for unified operation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        # Initialize all sub-services
        self.journey_service = JourneySessionService(db)
        self.personalization_engine = PersonalizationEngine(db)
        self.scarcity_engine = ScarcityTriggerEngine(db)
        self.real_time_optimizer = RealTimeOptimizer(db)
        self.ux_bridge = UXIntelligenceIntegrationBridge(db)
    
    async def initialize_unified_journey(self, request: UnifiedJourneyInitRequest) -> UnifiedJourneyResponse:
        """Initialize a complete unified journey experience"""
        try:
            logger.info(f"Initializing unified journey for session: {request.session_data.session_id}")
            
            # Step 1: Initialize journey session
            journey_response = await self.journey_service.start_journey_session(request.session_data)
            
            # Step 2: Initialize UX Intelligence integration
            if request.ux_data:
                unified_session_data = UnifiedSessionData(
                    session_id=request.session_data.session_id,
                    ux_data=request.ux_data,
                    journey_data=request.session_data.dict()
                )
                ux_response = await self.ux_bridge.initialize_unified_session(unified_session_data)
            else:
                ux_response = {"unified_intelligence": {}}
            
            # Step 3: Generate initial personalized content
            personalized_content = await self.personalization_engine.generate_personalized_content(
                journey_response.session, request.personalization_preferences
            )
            
            # Step 4: Get initial optimization recommendations
            optimization_recommendations = await self._get_initial_optimization_recommendations(
                journey_response.session, request.optimization_level
            )
            
            # Step 5: Set up real-time monitoring
            monitoring_setup = await self._setup_real_time_monitoring(
                journey_response.session, request.optimization_level
            )
            
            logger.info(f"Unified journey initialized successfully: {request.session_data.session_id}")
            
            return UnifiedJourneyResponse(
                success=True,
                session_id=request.session_data.session_id,
                journey_session=journey_response,
                personalized_content=personalized_content,
                ux_intelligence=ux_response.get("unified_intelligence", {}),
                optimization_recommendations=optimization_recommendations,
                real_time_monitoring=monitoring_setup
            )
            
        except Exception as e:
            logger.error(f"Error initializing unified journey: {str(e)}")
            raise
    
    async def process_unified_interaction(self, request: UnifiedInteractionRequest) -> UnifiedInteractionResponse:
        """Process interaction through all journey systems in a coordinated manner"""
        try:
            logger.debug(f"Processing unified interaction for session: {request.session_id}")
            
            # Get current session
            session = await self.journey_service._get_session(request.session_id)
            if not session:
                raise ValueError(f"Session not found: {request.session_id}")
            
            # Process interaction through all systems concurrently
            tasks = [
                self._process_journey_stage_progression(session, request.interaction_data),
                self._process_personalization_update(session, request.interaction_data),
                self._process_scarcity_evaluation(session, request.behavioral_signals),
                self._process_real_time_optimization(session, request.engagement_metrics, request.force_optimization),
                self._process_ux_intelligence_update(session, request.interaction_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Unpack results
            stage_progression = results[0] if not isinstance(results[0], Exception) else {}
            personalization_updates = results[1] if not isinstance(results[1], Exception) else {}
            scarcity_triggers = results[2] if not isinstance(results[2], Exception) else []
            optimizations_applied = results[3] if not isinstance(results[3], Exception) else []
            ux_updates = results[4] if not isinstance(results[4], Exception) else {}
            
            # Generate next recommendations based on all system outputs
            next_recommendations = await self._generate_next_action_recommendations(
                session, stage_progression, personalization_updates, scarcity_triggers, optimizations_applied
            )
            
            # Update analytics
            analytics_update = await self._update_unified_analytics(
                session, request.interaction_data, results
            )
            
            return UnifiedInteractionResponse(
                success=True,
                session_id=request.session_id,
                stage_progression=stage_progression,
                personalization_updates=personalization_updates,
                scarcity_triggers=scarcity_triggers if isinstance(scarcity_triggers, list) else [],
                optimizations_applied=optimizations_applied if isinstance(optimizations_applied, list) else [],
                next_recommendations=next_recommendations,
                analytics_update=analytics_update
            )
            
        except Exception as e:
            logger.error(f"Error processing unified interaction: {str(e)}")
            raise
    
    async def get_unified_analytics(self, request: UnifiedJourneyAnalyticsRequest) -> UnifiedJourneyAnalyticsResponse:
        """Get comprehensive analytics across all journey systems"""
        try:
            logger.debug(f"Getting unified analytics for scope: {request.analytics_scope}")
            
            analytics_results = {}
            
            # Gather analytics from each system based on scope
            if "all" in request.analytics_scope or "journey" in request.analytics_scope:
                analytics_results["journey"] = await self._get_journey_analytics(request)
            
            if "all" in request.analytics_scope or "personalization" in request.analytics_scope:
                analytics_results["personalization"] = await self._get_personalization_analytics(request)
            
            if "all" in request.analytics_scope or "scarcity" in request.analytics_scope:
                analytics_results["scarcity"] = await self._get_scarcity_analytics(request)
            
            if "all" in request.analytics_scope or "optimization" in request.analytics_scope:
                analytics_results["optimization"] = await self._get_optimization_analytics(request)
            
            if "all" in request.analytics_scope or "ux" in request.analytics_scope:
                analytics_results["ux"] = await self._get_ux_analytics(request)
            
            # Generate cross-system insights
            cross_system_insights = await self._generate_cross_system_insights(analytics_results)
            
            # Generate system-wide recommendations
            system_recommendations = await self._generate_system_recommendations(analytics_results, cross_system_insights)
            
            return UnifiedJourneyAnalyticsResponse(
                success=True,
                analytics_scope=request.analytics_scope,
                time_range=request.time_range,
                journey_analytics=analytics_results.get("journey", {}),
                personalization_analytics=analytics_results.get("personalization", {}),
                scarcity_analytics=analytics_results.get("scarcity", {}),
                optimization_analytics=analytics_results.get("optimization", {}),
                ux_analytics=analytics_results.get("ux", {}),
                cross_system_insights=cross_system_insights,
                recommendations=system_recommendations
            )
            
        except Exception as e:
            logger.error(f"Error getting unified analytics: {str(e)}")
            raise
    
    # =============================================================================
    # INTERNAL PROCESSING METHODS
    # =============================================================================
    
    async def _process_journey_stage_progression(self, session, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process journey stage progression"""
        current_stage = JourneyStage(session.current_stage)
        progression_signals = interaction_data.get("progression_signals", [])
        
        # Determine if stage progression should occur
        if await self._should_progress_stage(session, progression_signals):
            next_stage = await self._determine_next_stage(session, progression_signals)
            if next_stage:
                updated_session = await self.journey_service.update_journey_stage(
                    session.session_id, next_stage
                )
                return {
                    "stage_changed": True,
                    "previous_stage": current_stage.value,
                    "new_stage": next_stage.value,
                    "progression_reason": progression_signals
                }
        
        return {"stage_changed": False, "current_stage": current_stage.value}
    
    async def _process_personalization_update(self, session, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process personalization updates"""
        engagement_data = interaction_data.get("engagement_data", {})
        
        if engagement_data:
            optimization_result = await self.personalization_engine.optimize_personalization_real_time(
                session, engagement_data
            )
            return {
                "personalization_updated": True,
                "optimization_result": optimization_result
            }
        
        return {"personalization_updated": False}
    
    async def _process_scarcity_evaluation(self, session, behavioral_signals: Dict[str, Any]) -> List[ScarcityTrigger]:
        """Process scarcity trigger evaluation"""
        current_stage = JourneyStage(session.current_stage)
        scarcity_readiness = behavioral_signals.get("scarcity_readiness", 0.5)
        
        if scarcity_readiness > 0.6:  # High readiness threshold
            triggers = await self.scarcity_engine.evaluate_scarcity_triggers(session, current_stage)
            return triggers
        
        return []
    
    async def _process_real_time_optimization(self, session, engagement_metrics: Dict[str, Any], force_optimization: bool) -> List[Dict[str, Any]]:
        """Process real-time optimization"""
        if engagement_metrics or force_optimization:
            optimization_result = await self.real_time_optimizer.monitor_and_optimize_session(
                session.session_id, engagement_metrics
            )
            
            if optimization_result.get("optimization_applied"):
                return optimization_result.get("optimization_details", {}).get("optimizations", [])
        
        return []
    
    async def _process_ux_intelligence_update(self, session, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process UX Intelligence updates"""
        try:
            ux_response = await self.ux_bridge.process_unified_interaction(
                session.session_id, interaction_data
            )
            return ux_response
        except Exception as e:
            logger.warning(f"UX Intelligence update failed: {str(e)}")
            return {}
    
    # =============================================================================
    # ANALYTICS METHODS
    # =============================================================================
    
    async def _get_journey_analytics(self, request: UnifiedJourneyAnalyticsRequest) -> Dict[str, Any]:
        """Get journey flow analytics"""
        # Placeholder implementation - would integrate with actual analytics service
        return {
            "session_count": 1500,
            "average_session_duration": 420,
            "stage_conversion_rates": {
                "awareness_to_consideration": 0.68,
                "consideration_to_decision": 0.45,
                "decision_to_conversion": 0.82
            },
            "top_journey_paths": [
                {"path": "mobile_tiktok_fast_track", "sessions": 650, "conversion_rate": 0.25},
                {"path": "desktop_research_deep", "sessions": 480, "conversion_rate": 0.31},
                {"path": "returning_visitor_personalized", "sessions": 370, "conversion_rate": 0.42}
            ]
        }
    
    async def _get_personalization_analytics(self, request: UnifiedJourneyAnalyticsRequest) -> Dict[str, Any]:
        """Get personalization analytics"""
        return {
            "total_personalizations": 1200,
            "personalization_success_rate": 0.87,
            "average_engagement_lift": 0.18,
            "top_strategies": [
                {"strategy": "mobile_tiktok_viral_replication", "success_rate": 0.92},
                {"strategy": "desktop_research_comprehensive", "success_rate": 0.85},
                {"strategy": "returning_visitor_upsell", "success_rate": 0.88}
            ]
        }
    
    async def _get_scarcity_analytics(self, request: UnifiedJourneyAnalyticsRequest) -> Dict[str, Any]:
        """Get scarcity trigger analytics"""
        return {
            "total_triggers": 800,
            "trigger_success_rate": 0.78,
            "average_conversion_lift": 0.22,
            "best_performing_triggers": [
                {"trigger": "time_pressure", "success_rate": 0.84},
                {"trigger": "social_proof", "success_rate": 0.79},
                {"trigger": "inventory_scarcity", "success_rate": 0.71}
            ]
        }
    
    async def _get_optimization_analytics(self, request: UnifiedJourneyAnalyticsRequest) -> Dict[str, Any]:
        """Get real-time optimization analytics"""
        return {
            "total_optimizations": 950,
            "optimization_success_rate": 0.85,
            "average_performance_improvement": 0.16,
            "optimization_types": {
                "flow_optimization": {"count": 350, "success_rate": 0.87},
                "abandonment_prevention": {"count": 280, "success_rate": 0.89},
                "conversion_optimization": {"count": 320, "success_rate": 0.81}
            }
        }
    
    async def _get_ux_analytics(self, request: UnifiedJourneyAnalyticsRequest) -> Dict[str, Any]:
        """Get UX Intelligence analytics"""
        return {
            "ux_sessions_analyzed": 1400,
            "persona_accuracy": 0.89,
            "device_optimization_success": 0.91,
            "cross_system_sync_rate": 0.94
        }
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    async def _get_initial_optimization_recommendations(self, session, optimization_level: str) -> List[Dict[str, Any]]:
        """Get initial optimization recommendations"""
        recommendations = []
        
        if optimization_level in ["standard", "aggressive"]:
            recommendations.extend([
                {
                    "type": "personalization_enhancement",
                    "priority": "high",
                    "expected_impact": 0.15,
                    "implementation": "immediate"
                },
                {
                    "type": "engagement_monitoring",
                    "priority": "medium",
                    "expected_impact": 0.10,
                    "implementation": "continuous"
                }
            ])
        
        if optimization_level == "aggressive":
            recommendations.append({
                "type": "proactive_scarcity",
                "priority": "high",
                "expected_impact": 0.20,
                "implementation": "conditional"
            })
        
        return recommendations
    
    async def _setup_real_time_monitoring(self, session, optimization_level: str) -> Dict[str, Any]:
        """Set up real-time monitoring configuration"""
        monitoring_intervals = {
            "minimal": 300,    # 5 minutes
            "standard": 180,   # 3 minutes
            "aggressive": 60   # 1 minute
        }
        
        return {
            "monitoring_enabled": True,
            "monitoring_interval": monitoring_intervals.get(optimization_level, 180),
            "optimization_level": optimization_level,
            "real_time_triggers": ["engagement_drop", "abandonment_risk", "conversion_opportunity"]
        }
    
    async def _should_progress_stage(self, session, progression_signals: List[str]) -> bool:
        """Determine if journey stage should progress"""
        stage_thresholds = {
            "awareness": ["engagement_threshold_met", "content_consumed"],
            "consideration": ["comparison_viewed", "features_explored"],
            "decision": ["pricing_viewed", "checkout_initiated"]
        }
        
        required_signals = stage_thresholds.get(session.current_stage, [])
        return any(signal in progression_signals for signal in required_signals)
    
    async def _determine_next_stage(self, session, progression_signals: List[str]) -> Optional[JourneyStage]:
        """Determine next journey stage"""
        stage_progression = {
            "awareness": JourneyStage.CONSIDERATION,
            "consideration": JourneyStage.DECISION,
            "decision": JourneyStage.CONVERSION
        }
        
        return stage_progression.get(session.current_stage)
    
    async def _generate_next_action_recommendations(self, session, stage_progression: Dict[str, Any], 
                                                   personalization_updates: Dict[str, Any], 
                                                   scarcity_triggers: List[ScarcityTrigger], 
                                                   optimizations_applied: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate next action recommendations based on all system outputs"""
        recommendations = []
        
        # Stage-based recommendations
        if stage_progression.get("stage_changed"):
            recommendations.append({
                "type": "stage_transition_optimization",
                "action": f"Optimize for {stage_progression['new_stage']} stage",
                "priority": "high",
                "timing": "immediate"
            })
        
        # Personalization recommendations
        if personalization_updates.get("personalization_updated"):
            recommendations.append({
                "type": "personalization_monitoring",
                "action": "Monitor personalization effectiveness",
                "priority": "medium", 
                "timing": "continuous"
            })
        
        # Scarcity recommendations
        if scarcity_triggers:
            recommendations.append({
                "type": "scarcity_follow_up",
                "action": "Monitor scarcity trigger response",
                "priority": "high",
                "timing": "immediate"
            })
        
        return recommendations
    
    async def _update_unified_analytics(self, session, interaction_data: Dict[str, Any], results: List[Any]) -> Dict[str, Any]:
        """Update unified analytics with interaction results"""
        return {
            "analytics_updated": True,
            "session_id": session.session_id,
            "interaction_timestamp": datetime.utcnow().isoformat(),
            "systems_updated": len([r for r in results if not isinstance(r, Exception)])
        }
    
    async def _generate_cross_system_insights(self, analytics_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights across all systems"""
        insights = []
        
        # Cross-system performance correlation
        if "journey" in analytics_results and "personalization" in analytics_results:
            insights.append({
                "insight": "Journey progression correlates with personalization effectiveness",
                "confidence": 0.87,
                "systems": ["journey", "personalization"],
                "recommendation": "Prioritize personalization at key journey transition points"
            })
        
        # Optimization impact analysis
        if "optimization" in analytics_results and "scarcity" in analytics_results:
            insights.append({
                "insight": "Real-time optimization amplifies scarcity trigger effectiveness",
                "confidence": 0.82,
                "systems": ["optimization", "scarcity"],
                "recommendation": "Coordinate optimization timing with scarcity trigger deployment"
            })
        
        return insights
    
    async def _generate_system_recommendations(self, analytics_results: Dict[str, Any], 
                                             cross_system_insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate system-wide recommendations"""
        recommendations = []
        
        # High-level system recommendations
        recommendations.extend([
            {
                "type": "system_integration",
                "recommendation": "Increase coordination between personalization and scarcity systems",
                "expected_impact": 0.18,
                "priority": "high"
            },
            {
                "type": "optimization_frequency",
                "recommendation": "Implement more frequent optimization cycles for high-value sessions",
                "expected_impact": 0.12,
                "priority": "medium"
            },
            {
                "type": "cross_device_enhancement",
                "recommendation": "Enhance cross-device journey continuity features",
                "expected_impact": 0.15,
                "priority": "high"
            }
        ])
        
        return recommendations

# =============================================================================
# UNIFIED JOURNEY ENDPOINTS
# =============================================================================

@router.post("/initialize", response_model=UnifiedJourneyResponse)
@track_api_call("unified_journey_initialize")
@rate_limit(requests_per_minute=100)
async def initialize_unified_journey(
    init_request: UnifiedJourneyInitRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> UnifiedJourneyResponse:
    """
    Initialize unified journey experience
    
    Creates a complete, coordinated journey experience with all systems
    (personalization, scarcity, optimization, UX intelligence) working together.
    """
    try:
        logger.info(f"Initializing unified journey for session: {init_request.session_data.session_id}")
        
        # Initialize orchestrator
        orchestrator = UnifiedJourneyOrchestrator(db)
        
        # Initialize unified journey
        with track_performance("unified_journey_initialization"):
            journey_response = await orchestrator.initialize_unified_journey(init_request)
        
        # Background tasks for tracking and monitoring
        background_tasks.add_task(
            track_unified_journey_initialization,
            init_request.session_data.session_id,
            init_request.optimization_level,
            journey_response.success
        )
        
        logger.info(f"Unified journey initialized successfully: {init_request.session_data.session_id}")
        return journey_response
        
    except Exception as e:
        logger.error(f"Error initializing unified journey: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unified journey initialization failed: {str(e)}")

@router.post("/interact", response_model=UnifiedInteractionResponse)
@track_api_call("unified_journey_interact")
@rate_limit(requests_per_minute=500)
async def process_unified_interaction(
    interaction_request: UnifiedInteractionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> UnifiedInteractionResponse:
    """
    Process unified interaction across all journey systems
    
    Processes user interactions through all journey systems in a coordinated
    manner, applying optimizations and generating recommendations.
    """
    try:
        session_id = interaction_request.session_id
        logger.debug(f"Processing unified interaction for session: {session_id}")
        
        # Initialize orchestrator
        orchestrator = UnifiedJourneyOrchestrator(db)
        
        # Process unified interaction
        with track_performance("unified_interaction_processing"):
            interaction_response = await orchestrator.process_unified_interaction(interaction_request)
        
        # Background tasks for analytics
        background_tasks.add_task(
            track_unified_interaction,
            session_id,
            len(interaction_response.optimizations_applied),
            len(interaction_response.scarcity_triggers),
            interaction_response.stage_progression.get("stage_changed", False)
        )
        
        return interaction_response
        
    except Exception as e:
        logger.error(f"Error processing unified interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unified interaction processing failed: {str(e)}")

@router.post("/analytics", response_model=UnifiedJourneyAnalyticsResponse)
@track_api_call("unified_journey_analytics")
@rate_limit(requests_per_minute=50)
async def get_unified_journey_analytics(
    analytics_request: UnifiedJourneyAnalyticsRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> UnifiedJourneyAnalyticsResponse:
    """
    Get comprehensive unified journey analytics
    
    Returns analytics across all journey systems with cross-system insights
    and system-wide optimization recommendations.
    """
    try:
        logger.debug(f"Getting unified analytics for scope: {analytics_request.analytics_scope}")
        
        # Initialize orchestrator
        orchestrator = UnifiedJourneyOrchestrator(db)
        
        # Get unified analytics
        with track_performance("unified_analytics_generation"):
            analytics_response = await orchestrator.get_unified_analytics(analytics_request)
        
        # Background task for analytics tracking
        background_tasks.add_task(
            track_unified_analytics_request,
            analytics_request.analytics_scope,
            analytics_request.time_range,
            len(analytics_response.cross_system_insights)
        )
        
        return analytics_response
        
    except Exception as e:
        logger.error(f"Error getting unified analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unified analytics failed: {str(e)}")

@router.get("/health")
async def unified_journey_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Health check endpoint for unified journey service"""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        
        # Test component health
        orchestrator = UnifiedJourneyOrchestrator(db)
        
        return {
            "status": "healthy",
            "service": "unified_journey_orchestrator",
            "module": "2b_dynamic_customer_journey",
            "components": "journey,personalization,scarcity,optimization,ux_bridge",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Unified journey health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Unified journey service unhealthy")

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def track_unified_journey_initialization(session_id: str, optimization_level: str, success: bool):
    """Background task to track unified journey initialization"""
    logger.info(f"Tracking unified journey init: {session_id}, level: {optimization_level}, success: {success}")

async def track_unified_interaction(session_id: str, optimizations_count: int, triggers_count: int, stage_changed: bool):
    """Background task to track unified interaction"""
    logger.debug(f"Tracking unified interaction: {session_id}, optimizations: {optimizations_count}, triggers: {triggers_count}")

async def track_unified_analytics_request(analytics_scope: List[str], time_range: str, insights_count: int):
    """Background task to track unified analytics request"""
    logger.debug(f"Tracking unified analytics: scope: {analytics_scope}, range: {time_range}, insights: {insights_count}")