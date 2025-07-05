# Enhanced Personalization API Controller - Phase 3, Week 1
# Module: Personalization Intelligence API
# Created: 2025-07-05

import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .personalization_engine_enhanced import EnhancedPersonalizationEngine, ContentEngineIntegration
from .services import JourneySessionService
from ...database import get_db
from ...utils.auth import get_current_user
from ...utils.rate_limiting import rate_limit
from ...utils.monitoring import track_api_call, track_performance

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/journey/personalization/v2", tags=["personalization-v2"])

# =============================================================================
# ENHANCED PERSONALIZATION MODELS
# =============================================================================

class EnhancedPersonalizationRequest(BaseModel):
    """Enhanced request model for personalization with device and persona context"""
    session_id: str = Field(..., description="Journey session ID")
    context_data: Dict[str, Any] = Field(default_factory=dict, description="Enhanced context including search terms, keywords, interactions")
    optimization_level: str = Field(default="advanced", description="Optimization level: basic, standard, advanced, ml-enhanced")
    enable_persona_detection: bool = Field(default=True, description="Enable automatic persona detection")
    enable_device_optimization: bool = Field(default=True, description="Enable device-specific optimization")

class PersonaDetectionRequest(BaseModel):
    """Request model for explicit persona detection"""
    session_id: str = Field(..., description="Journey session ID")
    user_data: Dict[str, Any] = Field(..., description="User data for persona detection")
    update_session: bool = Field(default=True, description="Update session with detected persona")

class PersonaDetectionResponse(BaseModel):
    """Response model for persona detection"""
    success: bool = Field(..., description="Operation success status")
    detected_persona: PersonaData = Field(..., description="Detected persona information")
    confidence_score: float = Field(..., description="Detection confidence score")
    persona_attributes: Dict[str, Any] = Field(..., description="Additional persona attributes")

class DeviceOptimizationRequest(BaseModel):
    """Request model for device-specific optimization"""
    session_id: str = Field(..., description="Journey session ID")
    content: PersonalizedContent = Field(..., description="Content to optimize")
    device_context: DeviceContext = Field(..., description="Device context information")

class EnhancedPersonalizationResponse(BaseModel):
    """Enhanced response model with persona and device insights"""
    success: bool = Field(..., description="Operation success status")
    session_id: str = Field(..., description="Journey session ID")
    personalized_content: PersonalizedContent = Field(..., description="Personalized content")
    persona_detection: Optional[PersonaData] = Field(None, description="Detected persona information")
    device_optimization: Dict[str, Any] = Field(default_factory=dict, description="Applied device optimizations")
    personalization_metadata: Dict[str, Any] = Field(default_factory=dict, description="Enhanced personalization metadata")
    ml_insights: Optional[Dict[str, Any]] = Field(None, description="ML model insights")
    a_b_test_info: Optional[Dict[str, Any]] = Field(None, description="A/B test information")

class PersonalizationInsightsResponse(BaseModel):
    """Response model for personalization insights"""
    success: bool = Field(..., description="Operation success status")
    session_insights: Dict[str, Any] = Field(..., description="Session-specific insights")
    ml_model_health: Dict[str, Any] = Field(..., description="ML model health status")
    optimization_opportunities: List[Dict[str, Any]] = Field(..., description="Identified optimization opportunities")

# =============================================================================
# ENHANCED PERSONALIZATION ENDPOINTS
# =============================================================================

@router.post("/generate", response_model=EnhancedPersonalizationResponse)
@track_api_call("enhanced_personalization_generate")
@rate_limit(requests_per_minute=200)
async def generate_enhanced_personalized_content(
    personalization_request: EnhancedPersonalizationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> EnhancedPersonalizationResponse:
    """
    Generate enhanced personalized content with persona detection and device optimization
    
    Creates highly personalized content using advanced ML models, automatic persona
    detection, and device-specific optimizations for maximum conversion impact.
    """
    try:
        session_id = personalization_request.session_id
        logger.info(f"Generating enhanced personalized content for session: {session_id}")
        
        # Validate session ID
        if not validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Initialize services
        journey_service = JourneySessionService(db)
        personalization_engine = EnhancedPersonalizationEngine(db)
        
        # Get journey session
        session = await journey_service._get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Journey session not found")
        
        # Prepare enhanced context
        enhanced_context = {
            **personalization_request.context_data,
            'enable_persona_detection': personalization_request.enable_persona_detection,
            'enable_device_optimization': personalization_request.enable_device_optimization,
            'optimization_level': personalization_request.optimization_level
        }
        
        # Generate enhanced personalized content
        with track_performance("enhanced_personalization_content_generation"):
            personalized_content = await personalization_engine.generate_personalized_content(
                session, enhanced_context
            )
        
        # Get persona detection results
        persona_detection = None
        if personalization_request.enable_persona_detection:
            persona_detection = PersonaData(
                type=session.persona_type,
                confidence=0.85,  # Would come from actual detection
                attributes={'detection_method': 'enhanced_behavioral'}
            )
        
        # Get device optimization details
        device_optimization = {}
        if personalization_request.enable_device_optimization:
            device_optimization = {
                'device_type': session.device_type,
                'optimizations_applied': ['message_length', 'cta_simplification', 'trust_signal_prioritization'],
                'optimization_impact': 0.15
            }
        
        # Get ML insights
        ml_insights = await personalization_engine.get_personalization_insights(session_id)
        
        # Generate A/B test information
        a_b_test_info = await _generate_enhanced_ab_test_info(session, personalized_content)
        
        # Enhanced personalization metadata
        personalization_metadata = {
            "strategy_used": personalized_content.personalization_strategy,
            "confidence_score": 0.85,
            "optimization_level": personalization_request.optimization_level,
            "ml_model_version": "v2.0",
            "persona_device_combination": f"{session.persona_type}_{session.device_type}",
            "generation_timestamp": datetime.utcnow().isoformat()
        }
        
        # Background tasks for enhanced analytics
        background_tasks.add_task(
            track_enhanced_personalization_performance,
            session_id,
            personalized_content.personalization_strategy,
            persona_detection,
            device_optimization
        )
        
        background_tasks.add_task(
            update_ml_learning_data,
            session_id,
            personalized_content,
            personalization_metadata
        )
        
        logger.info(f"Enhanced personalized content generated successfully: {session_id}")
        
        return EnhancedPersonalizationResponse(
            success=True,
            session_id=session_id,
            personalized_content=personalized_content,
            persona_detection=persona_detection,
            device_optimization=device_optimization,
            personalization_metadata=personalization_metadata,
            ml_insights=ml_insights.get('ml_insights') if ml_insights else None,
            a_b_test_info=a_b_test_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating enhanced personalized content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced personalization generation failed: {str(e)}")

@router.post("/detect-persona", response_model=PersonaDetectionResponse)
@track_api_call("persona_detection")
@rate_limit(requests_per_minute=100)
async def detect_user_persona(
    detection_request: PersonaDetectionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> PersonaDetectionResponse:
    """
    Explicitly detect user persona based on behavioral data
    
    Uses advanced behavioral analysis and ML models to accurately
    identify user personas for targeted personalization.
    """
    try:
        session_id = detection_request.session_id
        logger.info(f"Detecting persona for session: {session_id}")
        
        # Initialize services
        personalization_engine = EnhancedPersonalizationEngine(db)
        
        # Detect persona
        with track_performance("persona_detection"):
            persona_data = await personalization_engine.persona_detector.detect_persona(
                detection_request.user_data
            )
        
        # Update session if requested
        if detection_request.update_session and persona_data.confidence > 0.7:
            journey_service = JourneySessionService(db)
            session = await journey_service._get_session(session_id)
            if session:
                await personalization_engine._update_session_persona(session, persona_data)
        
        # Extract detailed attributes
        persona_attributes = {
            **persona_data.attributes,
            'behavioral_patterns': personalization_engine.persona_detector.behavioral_patterns.get(
                persona_data.type, {}
            )
        }
        
        # Background task for tracking
        background_tasks.add_task(
            track_persona_detection,
            session_id,
            persona_data.type,
            persona_data.confidence
        )
        
        return PersonaDetectionResponse(
            success=True,
            detected_persona=persona_data,
            confidence_score=persona_data.confidence,
            persona_attributes=persona_attributes
        )
        
    except Exception as e:
        logger.error(f"Error detecting persona: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Persona detection failed: {str(e)}")

@router.post("/optimize-for-device", response_model=Dict[str, Any])
@track_api_call("device_optimization")
@rate_limit(requests_per_minute=150)
async def optimize_content_for_device(
    optimization_request: DeviceOptimizationRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Optimize content for specific device characteristics
    
    Applies device-specific rendering strategies to ensure optimal
    content presentation across different screen sizes and capabilities.
    """
    try:
        logger.info(f"Optimizing content for device: {optimization_request.device_context.type}")
        
        # Initialize services
        personalization_engine = EnhancedPersonalizationEngine(db)
        
        # Optimize content
        with track_performance("device_content_optimization"):
            optimized_content = await personalization_engine.device_optimizer.optimize_for_device(
                optimization_request.content,
                optimization_request.device_context
            )
        
        # Calculate optimization metrics
        optimization_metrics = {
            'message_length_reduction': len(optimization_request.content.hero_message) - len(optimized_content.hero_message),
            'trust_signal_optimization': len(optimization_request.content.trust_signals) - len(optimized_content.trust_signals),
            'mobile_friendly_score': 0.9 if optimization_request.device_context.type == DeviceType.MOBILE else 0.7
        }
        
        return {
            "success": True,
            "original_content": optimization_request.content.dict(),
            "optimized_content": optimized_content.dict(),
            "device_type": optimization_request.device_context.type,
            "optimization_metrics": optimization_metrics
        }
        
    except Exception as e:
        logger.error(f"Error optimizing content for device: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Device optimization failed: {str(e)}")

@router.get("/insights/{session_id}", response_model=PersonalizationInsightsResponse)
@track_api_call("personalization_insights")
@rate_limit(requests_per_minute=100)
async def get_personalization_insights(
    session_id: str = Path(..., description="Journey session ID"),
    db: AsyncSession = Depends(get_db)
) -> PersonalizationInsightsResponse:
    """
    Get comprehensive personalization insights for a session
    
    Returns detailed insights including ML model performance, optimization
    opportunities, and personalization effectiveness metrics.
    """
    try:
        logger.info(f"Getting personalization insights for session: {session_id}")
        
        # Initialize services
        personalization_engine = EnhancedPersonalizationEngine(db)
        
        # Get comprehensive insights
        with track_performance("personalization_insights_generation"):
            insights = await personalization_engine.get_personalization_insights(session_id)
        
        # Get ML model health
        from ...utils.ml_models import ml_model_manager
        ml_health = await ml_model_manager.get_model_health()
        
        # Identify optimization opportunities
        optimization_opportunities = [
            {
                'type': 'content_variant_testing',
                'description': 'Test emoji-heavy vs professional messaging',
                'expected_impact': 0.15,
                'confidence': 0.85
            },
            {
                'type': 'timing_optimization',
                'description': 'Adjust intervention timing based on engagement',
                'expected_impact': 0.12,
                'confidence': 0.78
            }
        ]
        
        return PersonalizationInsightsResponse(
            success=True,
            session_insights=insights,
            ml_model_health=ml_health,
            optimization_opportunities=optimization_opportunities
        )
        
    except Exception as e:
        logger.error(f"Error getting personalization insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")

@router.get("/page-content/{session_id}/{page_type}")
@track_api_call("personalized_page_content")
@rate_limit(requests_per_minute=200)
async def get_personalized_page_content(
    session_id: str = Path(..., description="Journey session ID"),
    page_type: str = Path(..., description="Page type: landing, product, checkout"),
    include_meta: bool = Query(True, description="Include SEO meta tags"),
    include_structured_data: bool = Query(True, description="Include structured data"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get fully personalized content for a specific page type
    
    Returns complete page content including layout, sections, meta tags,
    and structured data optimized for the user's persona and device.
    """
    try:
        logger.info(f"Getting personalized page content: {session_id}, {page_type}")
        
        # Validate page type
        valid_page_types = ['landing', 'product', 'checkout', 'comparison', 'support']
        if page_type not in valid_page_types:
            raise HTTPException(status_code=400, detail=f"Invalid page type. Must be one of: {valid_page_types}")
        
        # Initialize services
        journey_service = JourneySessionService(db)
        personalization_engine = EnhancedPersonalizationEngine(db)
        content_integration = ContentEngineIntegration(personalization_engine)
        
        # Get journey session
        session = await journey_service._get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Journey session not found")
        
        # Prepare context
        context = {
            'page_type': page_type,
            'include_meta': include_meta,
            'include_structured_data': include_structured_data
        }
        
        # Get personalized page content
        with track_performance("personalized_page_content_generation"):
            page_content = await content_integration.get_personalized_content_for_page(
                session, page_type, context
            )
        
        # Remove optional fields if not requested
        if not include_meta:
            page_content.pop('meta', None)
        if not include_structured_data:
            page_content.pop('structured_data', None)
        
        return {
            "success": True,
            "session_id": session_id,
            "page_type": page_type,
            "persona": session.persona_type,
            "device": session.device_type,
            "content": page_content
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting personalized page content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Page content generation failed: {str(e)}")

@router.get("/analytics/persona-performance")
@track_api_call("persona_performance_analytics")
@rate_limit(requests_per_minute=50)
async def get_persona_performance_analytics(
    time_range: str = Query("7d", description="Time range: 7d, 30d, 90d"),
    include_device_breakdown: bool = Query(True, description="Include device-specific breakdown"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed analytics on persona-specific personalization performance
    
    Returns comprehensive metrics showing how different personas respond
    to various personalization strategies across devices.
    """
    try:
        logger.info(f"Getting persona performance analytics for time range: {time_range}")
        
        # Mock analytics data (would be retrieved from analytics service)
        persona_performance = {
            "TechEarlyAdopter": {
                "total_sessions": 5200,
                "avg_engagement_lift": 0.22,
                "avg_conversion_rate": 0.18,
                "top_strategies": ["tech_adopter_awareness", "tech_adopter_decision"],
                "device_breakdown": {
                    "mobile": {"sessions": 3100, "conversion_rate": 0.16},
                    "tablet": {"sessions": 800, "conversion_rate": 0.19},
                    "desktop": {"sessions": 1300, "conversion_rate": 0.21}
                } if include_device_breakdown else None
            },
            "RemoteDad": {
                "total_sessions": 3800,
                "avg_engagement_lift": 0.18,
                "avg_conversion_rate": 0.15,
                "top_strategies": ["remote_dad_consideration", "remote_dad_decision"],
                "device_breakdown": {
                    "mobile": {"sessions": 900, "conversion_rate": 0.12},
                    "tablet": {"sessions": 1100, "conversion_rate": 0.14},
                    "desktop": {"sessions": 1800, "conversion_rate": 0.17}
                } if include_device_breakdown else None
            },
            "StudentHustler": {
                "total_sessions": 7500,
                "avg_engagement_lift": 0.25,
                "avg_conversion_rate": 0.14,
                "top_strategies": ["student_hustler_awareness", "student_hustler_decision"],
                "device_breakdown": {
                    "mobile": {"sessions": 6200, "conversion_rate": 0.13},
                    "tablet": {"sessions": 800, "conversion_rate": 0.15},
                    "desktop": {"sessions": 500, "conversion_rate": 0.18}
                } if include_device_breakdown else None
            },
            "BusinessOwner": {
                "total_sessions": 2100,
                "avg_engagement_lift": 0.20,
                "avg_conversion_rate": 0.22,
                "top_strategies": ["business_owner_consideration", "business_owner_decision"],
                "device_breakdown": {
                    "mobile": {"sessions": 400, "conversion_rate": 0.18},
                    "tablet": {"sessions": 500, "conversion_rate": 0.20},
                    "desktop": {"sessions": 1200, "conversion_rate": 0.24}
                } if include_device_breakdown else None
            }
        }
        
        # Calculate aggregate metrics
        total_sessions = sum(p["total_sessions"] for p in persona_performance.values())
        avg_engagement_lift = sum(p["avg_engagement_lift"] * p["total_sessions"] for p in persona_performance.values()) / total_sessions
        avg_conversion_rate = sum(p["avg_conversion_rate"] * p["total_sessions"] for p in persona_performance.values()) / total_sessions
        
        return {
            "success": True,
            "time_range": time_range,
            "persona_performance": persona_performance,
            "aggregate_metrics": {
                "total_sessions": total_sessions,
                "avg_engagement_lift": round(avg_engagement_lift, 3),
                "avg_conversion_rate": round(avg_conversion_rate, 3)
            },
            "insights": [
                {
                    "insight": "StudentHustler persona shows highest engagement lift on mobile",
                    "recommendation": "Prioritize mobile-first design for student-targeted campaigns",
                    "expected_impact": 0.08
                },
                {
                    "insight": "BusinessOwner persona converts best on desktop",
                    "recommendation": "Enhance desktop experience with detailed analytics and comparisons",
                    "expected_impact": 0.12
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting persona performance analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

@router.get("/health/v2")
async def enhanced_personalization_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Enhanced health check endpoint with ML model status"""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        
        # Get ML model health
        from ...utils.ml_models import ml_model_manager
        ml_health = await ml_model_manager.get_model_health()
        
        return {
            "status": "healthy",
            "service": "enhanced_personalization_engine",
            "version": "v2.0",
            "module": "phase_3_personalization",
            "ml_models": {
                "personalization_model": ml_health.get('personalization_model', {}).get('is_trained', False),
                "recommendation_engine": ml_health.get('recommendation_engine', {}).get('is_trained', False)
            },
            "features": {
                "persona_detection": True,
                "device_optimization": True,
                "ml_enhancement": True,
                "content_integration": True
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Enhanced personalization health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Enhanced personalization service unhealthy")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def _generate_enhanced_ab_test_info(session, personalized_content: PersonalizedContent) -> Optional[Dict[str, Any]]:
    """Generate enhanced A/B test information with ML insights"""
    if session.conversion_probability > 0.3:
        return {
            "test_id": f"enhanced_ab_{session.session_id}_{datetime.utcnow().strftime('%Y%m%d')}",
            "variant": "enhanced_ml",
            "test_type": "ml_personalization_optimization",
            "control_group": False,
            "test_duration": "7_days",
            "success_metrics": ["conversion_rate", "engagement_score", "revenue_per_session"],
            "ml_confidence": 0.85,
            "expected_lift": 0.15
        }
    return None

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def track_enhanced_personalization_performance(
    session_id: str, 
    strategy: str, 
    persona_data: Optional[PersonaData],
    device_optimization: Dict[str, Any]
):
    """Background task to track enhanced personalization performance"""
    logger.info(f"Tracking enhanced personalization: {session_id}, {strategy}")
    # Implementation for enhanced performance tracking

async def update_ml_learning_data(
    session_id: str,
    content: PersonalizedContent,
    metadata: Dict[str, Any]
):
    """Background task to update ML model learning data"""
    logger.debug(f"Updating ML learning data: {session_id}")
    # Implementation for ML model learning updates

async def track_persona_detection(
    session_id: str,
    persona_type: str,
    confidence: float
):
    """Background task to track persona detection accuracy"""
    logger.info(f"Tracking persona detection: {session_id}, {persona_type}, confidence={confidence}")
    # Implementation for persona detection tracking