"""
Device-Specific Conversion Optimization Controller
Module: 2C - Conversion & Marketing Automation
Created: 2024-07-04

Core controller for device-specific conversion optimization logic targeting
Mobile TikTok Users vs Desktop Research Users with real-time adaptive UX flows.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import uuid
import asyncio
import logging
from enum import Enum

from ..database.connection import get_database_connection
from ..services.analytics_service import AnalyticsService
from ..services.ux_intelligence_service import UXIntelligenceService
from ..models.device_optimization_models import (
    DeviceConversionInput,
    DeviceConversionOutput,
    ConversionFlow,
    UIAdjustments,
    ConversionTrigger,
    PerformanceMetrics
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/conversion/device", tags=["device-conversion"])

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class DeviceType(str, Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

class TrafficSource(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    GOOGLE = "google"
    DIRECT = "direct"
    OTHER = "other"

class PersonaType(str, Enum):
    TECH_EARLY_ADOPTER = "TechEarlyAdopter"
    REMOTE_DAD = "RemoteDad"
    STUDENT_HUSTLER = "StudentHustler"
    BUSINESS_OWNER = "BusinessOwner"

class JourneyStage(str, Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    DECISION = "decision"
    PURCHASE = "purchase"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class OptimizationFlow(str, Enum):
    MOBILE_TIKTOK_FLOW = "mobile_tiktok_flow"
    DESKTOP_RESEARCH_FLOW = "desktop_research_flow"
    TABLET_DISCOVERY_FLOW = "tablet_discovery_flow"
    ADAPTIVE_FLOW = "adaptive_flow"

class UILayout(str, Enum):
    HOOK = "hook"
    GALLERY = "gallery"
    COMPARISON = "comparison"
    ANALYSIS = "analysis"

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class SessionData(BaseModel):
    engagement_score: float = Field(..., ge=0.0, le=1.0)
    time_on_page: int = Field(..., ge=0)
    scroll_depth: float = Field(..., ge=0.0, le=1.0)
    interactions: List[str] = Field(default_factory=list)

class DeviceOptimizationRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    device_type: DeviceType
    traffic_source: TrafficSource
    persona: PersonaType
    session_data: SessionData
    current_step: JourneyStage
    urgency_level: UrgencyLevel
    device_fingerprint: Optional[str] = None
    custom_parameters: Optional[Dict[str, Any]] = None

class CTAConfiguration(BaseModel):
    text: str
    style: str
    position: str
    urgency_level: str
    personalization: Dict[str, Any]

class ContentConfiguration(BaseModel):
    headline: str
    subheadline: Optional[str] = None
    body_text: str
    media_elements: List[Dict[str, Any]]
    social_proof_elements: List[Dict[str, Any]]

class TimingConfiguration(BaseModel):
    display_delay: int = Field(..., ge=0)
    interaction_timeout: int = Field(..., ge=0)
    optimization_interval: int = Field(..., ge=0)

class DeviceOptimizationResponse(BaseModel):
    optimization_id: str
    optimized_flow: OptimizationFlow
    ui_adjustments: Dict[str, Any]
    conversion_triggers: List[Dict[str, Any]]
    expected_conversion_rate: float
    performance_metrics: Dict[str, Any]
    processing_time_ms: int
    confidence_score: float

class OptimizationPerformanceRequest(BaseModel):
    device_type: Optional[DeviceType] = None
    persona_type: Optional[PersonaType] = None
    time_range_hours: int = Field(default=24, ge=1, le=168)  # Max 1 week

class OptimizationPerformanceResponse(BaseModel):
    device_type: str
    persona_type: str
    optimization_flow: str
    total_optimizations: int
    avg_expected_conversion: float
    avg_actual_conversion: float
    conversion_improvement: float
    performance_score: float

# =============================================================================
# DEVICE-SPECIFIC OPTIMIZATION STRATEGIES
# =============================================================================

class MobileTikTokStrategy:
    """3-Second Hook Strategy for Mobile TikTok Users"""
    
    @staticmethod
    def generate_hook_configuration(persona: PersonaType) -> Dict[str, Any]:
        """Generate mobile TikTok hook configuration based on persona"""
        
        persona_hooks = {
            PersonaType.TECH_EARLY_ADOPTER: {
                "type": "animation",
                "duration": 2500,  # 2.5 seconds
                "content": "🚀 Revolutionary tech that changes everything",
                "trigger": "instant",
                "visual_style": "tech_modern"
            },
            PersonaType.REMOTE_DAD: {
                "type": "video",
                "duration": 3000,  # 3 seconds
                "content": "⚡ More time with family, less time working",
                "trigger": "instant",
                "visual_style": "family_friendly"
            },
            PersonaType.STUDENT_HUSTLER: {
                "type": "bold_text",
                "duration": 2000,  # 2 seconds
                "content": "💰 Student discount: 50% OFF limited time!",
                "trigger": "instant",
                "visual_style": "energetic_youth"
            },
            PersonaType.BUSINESS_OWNER: {
                "type": "animation",
                "duration": 2500,  # 2.5 seconds
                "content": "📈 ROI guaranteed or money back",
                "trigger": "instant",
                "visual_style": "professional"
            }
        }
        
        return persona_hooks.get(persona, persona_hooks[PersonaType.TECH_EARLY_ADOPTER])
    
    @staticmethod
    def generate_swipe_gallery(persona: PersonaType) -> Dict[str, Any]:
        """Generate swipe gallery configuration"""
        
        return {
            "swipe_direction": "horizontal",
            "auto_advance": False,
            "transition_speed": "fast",
            "image_count": 5,
            "social_proof_overlay": True,
            "purchase_cta_position": "bottom_fixed"
        }
    
    @staticmethod
    def generate_one_click_purchase(persona: PersonaType) -> Dict[str, Any]:
        """Generate one-click purchase configuration"""
        
        return {
            "payment_methods": ["apple_pay", "google_pay", "paypal"],
            "prefilled_forms": True,
            "trust_signals": ["security_badge", "money_back_guarantee"],
            "urgency_triggers": ["stock_counter", "time_limited_offer"]
        }

class DesktopResearchStrategy:
    """Analysis-Driven Strategy for Desktop Research Users"""
    
    @staticmethod
    def generate_comparison_tables(persona: PersonaType) -> Dict[str, Any]:
        """Generate comparison table configuration"""
        
        persona_comparisons = {
            PersonaType.TECH_EARLY_ADOPTER: {
                "focus": "technical_specifications",
                "columns": ["features", "tech_specs", "innovation_score", "future_roadmap"],
                "highlight_technical": True
            },
            PersonaType.BUSINESS_OWNER: {
                "focus": "business_value",
                "columns": ["features", "roi_calculator", "scalability", "support"],
                "highlight_roi": True
            },
            PersonaType.REMOTE_DAD: {
                "focus": "productivity_family_balance",
                "columns": ["features", "time_savings", "ease_of_use", "family_benefits"],
                "highlight_efficiency": True
            },
            PersonaType.STUDENT_HUSTLER: {
                "focus": "value_and_affordability",
                "columns": ["features", "student_pricing", "learning_resources", "career_impact"],
                "highlight_value": True
            }
        }
        
        return persona_comparisons.get(persona, persona_comparisons[PersonaType.BUSINESS_OWNER])
    
    @staticmethod
    def generate_detailed_analysis(persona: PersonaType) -> Dict[str, Any]:
        """Generate detailed analysis content"""
        
        return {
            "whitepapers": True,
            "case_studies": True,
            "technical_documentation": persona == PersonaType.TECH_EARLY_ADOPTER,
            "roi_calculator": persona in [PersonaType.BUSINESS_OWNER, PersonaType.REMOTE_DAD],
            "video_demos": True,
            "expert_testimonials": True
        }
    
    @staticmethod
    def generate_trust_building(persona: PersonaType) -> Dict[str, Any]:
        """Generate trust building elements"""
        
        return {
            "company_credentials": True,
            "security_certifications": True,
            "money_back_guarantee": True,
            "customer_support_info": True,
            "industry_awards": True,
            "client_testimonials": True
        }

class TabletDiscoveryStrategy:
    """Hybrid Strategy for Tablet Discovery Users"""
    
    @staticmethod
    def generate_visual_gallery(persona: PersonaType) -> Dict[str, Any]:
        """Generate visual gallery configuration"""
        
        return {
            "layout": "masonry",
            "touch_gestures": ["swipe", "pinch", "tap"],
            "zoom_capability": True,
            "image_optimization": "tablet_optimized",
            "lazy_loading": True,
            "transition_effects": "smooth"
        }
    
    @staticmethod
    def generate_comparison_features(persona: PersonaType) -> Dict[str, Any]:
        """Generate comparison features for tablet"""
        
        return {
            "side_to_side_comparison": True,
            "filter_options": ["price", "features", "ratings"],
            "sorting_options": ["relevance", "price", "popularity"],
            "quick_actions": ["add_to_cart", "save_for_later", "share"]
        }

# =============================================================================
# DEVICE OPTIMIZATION SERVICE
# =============================================================================

class DeviceOptimizationService:
    """Core service for device-specific conversion optimization"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.analytics_service = AnalyticsService(db_connection)
        self.ux_intelligence_service = UXIntelligenceService(db_connection)
    
    async def optimize_for_device(self, request: DeviceOptimizationRequest) -> DeviceOptimizationResponse:
        """Main optimization function for device-specific conversion"""
        
        start_time = datetime.now()
        optimization_id = str(uuid.uuid4())
        
        try:
            # 1. Determine optimization flow based on device and persona
            optimization_flow = self._determine_optimization_flow(
                request.device_type, 
                request.traffic_source, 
                request.persona
            )
            
            # 2. Generate device-specific UI adjustments
            ui_adjustments = await self._generate_ui_adjustments(
                optimization_flow, 
                request.persona, 
                request.session_data
            )
            
            # 3. Create conversion triggers
            conversion_triggers = await self._generate_conversion_triggers(
                request.device_type,
                request.persona,
                request.urgency_level,
                request.session_data
            )
            
            # 4. Calculate expected conversion rate
            expected_conversion_rate = await self._calculate_expected_conversion_rate(
                request.device_type,
                request.persona,
                optimization_flow,
                request.session_data
            )
            
            # 5. Generate performance metrics
            performance_metrics = await self._generate_performance_metrics(
                request, 
                optimization_flow
            )
            
            # 6. Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                request.session_data.engagement_score,
                expected_conversion_rate,
                performance_metrics
            )
            
            # 7. Store optimization in database
            await self._store_optimization(
                optimization_id,
                request,
                optimization_flow,
                ui_adjustments,
                conversion_triggers,
                expected_conversion_rate,
                performance_metrics,
                confidence_score
            )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return DeviceOptimizationResponse(
                optimization_id=optimization_id,
                optimized_flow=optimization_flow,
                ui_adjustments=ui_adjustments,
                conversion_triggers=conversion_triggers,
                expected_conversion_rate=expected_conversion_rate,
                performance_metrics=performance_metrics,
                processing_time_ms=int(processing_time),
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Device optimization failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
    
    def _determine_optimization_flow(self, device_type: DeviceType, traffic_source: TrafficSource, persona: PersonaType) -> OptimizationFlow:
        """Determine the optimal conversion flow based on device and context"""
        
        if device_type == DeviceType.MOBILE and traffic_source == TrafficSource.TIKTOK:
            return OptimizationFlow.MOBILE_TIKTOK_FLOW
        elif device_type == DeviceType.DESKTOP:
            return OptimizationFlow.DESKTOP_RESEARCH_FLOW
        elif device_type == DeviceType.TABLET:
            return OptimizationFlow.TABLET_DISCOVERY_FLOW
        else:
            return OptimizationFlow.ADAPTIVE_FLOW
    
    async def _generate_ui_adjustments(self, flow: OptimizationFlow, persona: PersonaType, session_data: SessionData) -> Dict[str, Any]:
        """Generate UI adjustments based on optimization flow"""
        
        adjustments = {
            "layout": UILayout.HOOK.value,
            "cta": {},
            "content": {},
            "timing": {}
        }
        
        if flow == OptimizationFlow.MOBILE_TIKTOK_FLOW:
            adjustments.update({
                "layout": UILayout.HOOK.value,
                "cta": MobileTikTokStrategy.generate_one_click_purchase(persona),
                "content": {
                    "hook": MobileTikTokStrategy.generate_hook_configuration(persona),
                    "gallery": MobileTikTokStrategy.generate_swipe_gallery(persona)
                },
                "timing": {
                    "hook_display": 0,
                    "gallery_transition": 3000,
                    "purchase_prompt": 8000
                }
            })
        
        elif flow == OptimizationFlow.DESKTOP_RESEARCH_FLOW:
            adjustments.update({
                "layout": UILayout.COMPARISON.value,
                "cta": {
                    "text": "Start Free Trial",
                    "style": "primary_large",
                    "position": "header_and_footer"
                },
                "content": {
                    "comparison": DesktopResearchStrategy.generate_comparison_tables(persona),
                    "analysis": DesktopResearchStrategy.generate_detailed_analysis(persona),
                    "trust": DesktopResearchStrategy.generate_trust_building(persona)
                },
                "timing": {
                    "progressive_disclosure": True,
                    "reading_time_tracking": True
                }
            })
        
        elif flow == OptimizationFlow.TABLET_DISCOVERY_FLOW:
            adjustments.update({
                "layout": UILayout.GALLERY.value,
                "cta": {
                    "text": "Explore Features",
                    "style": "interactive_tablet",
                    "position": "floating_bottom"
                },
                "content": {
                    "gallery": TabletDiscoveryStrategy.generate_visual_gallery(persona),
                    "comparison": TabletDiscoveryStrategy.generate_comparison_features(persona)
                },
                "timing": {
                    "gesture_based_navigation": True,
                    "adaptive_content_loading": True
                }
            })
        
        return adjustments
    
    async def _generate_conversion_triggers(self, device_type: DeviceType, persona: PersonaType, urgency_level: UrgencyLevel, session_data: SessionData) -> List[Dict[str, Any]]:
        """Generate conversion triggers based on device and context"""
        
        triggers = []
        
        # Base triggers for all devices
        if session_data.engagement_score > 0.7:
            triggers.append({
                "type": "high_engagement_prompt",
                "timing": "immediate",
                "message": "You seem interested! Would you like to learn more?",
                "action": "show_detailed_info"
            })
        
        if urgency_level in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
            triggers.append({
                "type": "urgency_prompt",
                "timing": "after_30_seconds",
                "message": "Limited time offer ends soon!",
                "action": "highlight_offer"
            })
        
        # Device-specific triggers
        if device_type == DeviceType.MOBILE:
            triggers.append({
                "type": "exit_intent_mobile",
                "timing": "on_scroll_up",
                "message": "Wait! Get 20% off before you go",
                "action": "show_mobile_discount"
            })
        
        elif device_type == DeviceType.DESKTOP:
            triggers.append({
                "type": "reading_time_trigger",
                "timing": "after_2_minutes",
                "message": "Ready to see it in action?",
                "action": "offer_demo"
            })
        
        # Persona-specific triggers
        if persona == PersonaType.TECH_EARLY_ADOPTER:
            triggers.append({
                "type": "innovation_highlight",
                "timing": "after_feature_view",
                "message": "Be among the first to experience this technology",
                "action": "beta_access_offer"
            })
        
        elif persona == PersonaType.STUDENT_HUSTLER:
            triggers.append({
                "type": "student_discount",
                "timing": "immediate",
                "message": "Student? Get 50% off with verification",
                "action": "student_verification_flow"
            })
        
        return triggers
    
    async def _calculate_expected_conversion_rate(self, device_type: DeviceType, persona: PersonaType, flow: OptimizationFlow, session_data: SessionData) -> float:
        """Calculate expected conversion rate based on historical data and device optimization"""
        
        # Base conversion rates by device type (from specifications)
        base_rates = {
            DeviceType.MOBILE: 0.10,    # 10% target (8-15% range)
            DeviceType.DESKTOP: 0.18,   # 18% target (12-25% range)
            DeviceType.TABLET: 0.14     # 14% target (10-18% range)
        }
        
        # Persona multipliers based on expected behavior
        persona_multipliers = {
            PersonaType.TECH_EARLY_ADOPTER: 1.2,
            PersonaType.BUSINESS_OWNER: 1.1,
            PersonaType.REMOTE_DAD: 1.0,
            PersonaType.STUDENT_HUSTLER: 0.9
        }
        
        # Engagement score impact
        engagement_multiplier = 0.5 + (session_data.engagement_score * 1.5)
        
        # Calculate expected rate
        base_rate = base_rates.get(device_type, 0.12)
        persona_impact = persona_multipliers.get(persona, 1.0)
        
        expected_rate = base_rate * persona_impact * engagement_multiplier
        
        # Cap at realistic maximum
        return min(expected_rate, 0.35)
    
    async def _generate_performance_metrics(self, request: DeviceOptimizationRequest, flow: OptimizationFlow) -> Dict[str, Any]:
        """Generate performance metrics for the optimization"""
        
        return {
            "response_time_target_ms": 500,
            "device_detection_time_ms": 50,
            "flow_optimization_time_ms": 100,
            "ui_adaptation_time_ms": 200,
            "expected_load_time_ms": 1500 if request.device_type == DeviceType.MOBILE else 1000,
            "target_engagement_score": 0.85,
            "optimization_confidence": 0.9
        }
    
    def _calculate_confidence_score(self, engagement_score: float, expected_conversion_rate: float, performance_metrics: Dict[str, Any]) -> float:
        """Calculate confidence score for the optimization"""
        
        # Factors contributing to confidence
        engagement_factor = engagement_score
        conversion_factor = min(expected_conversion_rate / 0.2, 1.0)  # Normalize to 20% max
        performance_factor = performance_metrics.get("optimization_confidence", 0.8)
        
        # Weighted confidence calculation
        confidence = (
            engagement_factor * 0.4 +
            conversion_factor * 0.3 +
            performance_factor * 0.3
        )
        
        return round(confidence, 3)
    
    async def _store_optimization(self, optimization_id: str, request: DeviceOptimizationRequest, flow: OptimizationFlow, ui_adjustments: Dict[str, Any], conversion_triggers: List[Dict[str, Any]], expected_conversion_rate: float, performance_metrics: Dict[str, Any], confidence_score: float):
        """Store optimization data in database"""
        
        query = """
        INSERT INTO device_conversion_optimizations (
            id, session_id, device_type, device_fingerprint, traffic_source, persona_type,
            optimization_flow, ui_layout, cta_configuration, content_configuration, timing_configuration,
            expected_conversion_rate, performance_metrics, conversion_triggers
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        """
        
        await self.db.execute(
            query,
            optimization_id,
            request.session_id,
            request.device_type.value,
            request.device_fingerprint,
            request.traffic_source.value,
            request.persona.value,
            flow.value,
            ui_adjustments.get("layout"),
            ui_adjustments.get("cta", {}),
            ui_adjustments.get("content", {}),
            ui_adjustments.get("timing", {}),
            expected_conversion_rate,
            performance_metrics,
            conversion_triggers
        )

# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post("/optimize", response_model=DeviceOptimizationResponse)
async def optimize_device_conversion(
    request: DeviceOptimizationRequest,
    db=Depends(get_database_connection)
):
    """
    Optimize conversion flow for specific device type and user persona
    
    - **Mobile TikTok**: 3-second hook → swipe gallery → one-click purchase
    - **Desktop Research**: comparison tables → detailed analysis → trust building  
    - **Tablet Discovery**: visual gallery → feature comparison → social proof
    """
    
    service = DeviceOptimizationService(db)
    return await service.optimize_for_device(request)

@router.get("/performance", response_model=List[OptimizationPerformanceResponse])
async def get_optimization_performance(
    request: OptimizationPerformanceRequest = Depends(),
    db=Depends(get_database_connection)
):
    """
    Get device optimization performance analytics
    
    Returns conversion performance metrics by device type and persona
    """
    
    query = """
    SELECT * FROM calculate_device_conversion_performance($1, $2, $3)
    """
    
    rows = await db.fetch(
        query,
        request.device_type.value if request.device_type else None,
        request.persona_type.value if request.persona_type else None,
        request.time_range_hours
    )
    
    return [
        OptimizationPerformanceResponse(
            device_type=row['device_type'],
            persona_type=row['persona_type'],
            optimization_flow=row['optimization_flow'],
            total_optimizations=row['total_optimizations'],
            avg_expected_conversion=float(row['avg_expected_conversion'] or 0),
            avg_actual_conversion=float(row['avg_actual_conversion'] or 0),
            conversion_improvement=float(row['conversion_improvement'] or 0),
            performance_score=float(row['performance_score'] or 0)
        )
        for row in rows
    ]

@router.get("/flows/{device_type}")
async def get_optimization_flows(device_type: DeviceType):
    """
    Get available optimization flows for a specific device type
    """
    
    flows = {
        DeviceType.MOBILE: {
            "primary_flow": "mobile_tiktok_flow",
            "description": "3-second hook strategy optimized for TikTok traffic",
            "features": ["instant_hook", "swipe_gallery", "one_click_purchase"],
            "target_conversion": "8-15%"
        },
        DeviceType.DESKTOP: {
            "primary_flow": "desktop_research_flow", 
            "description": "Analysis-driven strategy for research-focused users",
            "features": ["comparison_tables", "detailed_analysis", "trust_building"],
            "target_conversion": "12-25%"
        },
        DeviceType.TABLET: {
            "primary_flow": "tablet_discovery_flow",
            "description": "Hybrid discovery strategy with visual emphasis", 
            "features": ["visual_gallery", "feature_comparison", "social_proof"],
            "target_conversion": "10-18%"
        }
    }
    
    return flows.get(device_type, {"error": "Device type not supported"})

@router.post("/update-conversion-rate/{optimization_id}")
async def update_actual_conversion_rate(
    optimization_id: str,
    actual_conversion_rate: float = Field(..., ge=0.0, le=1.0),
    db=Depends(get_database_connection)
):
    """
    Update the actual conversion rate for a specific optimization
    """
    
    query = """
    UPDATE device_conversion_optimizations 
    SET actual_conversion_rate = $1, updated_at = CURRENT_TIMESTAMP
    WHERE id = $2
    RETURNING id, expected_conversion_rate, actual_conversion_rate
    """
    
    result = await db.fetchrow(query, actual_conversion_rate, optimization_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Optimization not found")
    
    improvement = 0
    if result['expected_conversion_rate']:
        improvement = ((actual_conversion_rate - result['expected_conversion_rate']) / 
                      result['expected_conversion_rate']) * 100
    
    return {
        "optimization_id": optimization_id,
        "expected_conversion_rate": result['expected_conversion_rate'],
        "actual_conversion_rate": actual_conversion_rate,
        "improvement_percentage": round(improvement, 2)
    }

@router.get("/analytics/summary")
async def get_conversion_analytics_summary(
    time_range_hours: int = Field(default=24, ge=1, le=168),
    db=Depends(get_database_connection)
):
    """
    Get conversion optimization analytics summary
    """
    
    query = """
    SELECT 
        device_type,
        COUNT(*) as total_optimizations,
        ROUND(AVG(expected_conversion_rate), 4) as avg_expected_conversion,
        ROUND(AVG(actual_conversion_rate), 4) as avg_actual_conversion,
        COUNT(*) FILTER (WHERE actual_conversion_rate > expected_conversion_rate) as improvements,
        ROUND(
            (COUNT(*) FILTER (WHERE actual_conversion_rate > expected_conversion_rate)::NUMERIC / 
             COUNT(*)::NUMERIC) * 100, 2
        ) as improvement_rate
    FROM device_conversion_optimizations
    WHERE created_at >= CURRENT_TIMESTAMP - ($1 || ' hours')::INTERVAL
        AND actual_conversion_rate IS NOT NULL
    GROUP BY device_type
    ORDER BY total_optimizations DESC
    """
    
    rows = await db.fetch(query, time_range_hours)
    
    return {
        "time_range_hours": time_range_hours,
        "summary": [
            {
                "device_type": row['device_type'],
                "total_optimizations": row['total_optimizations'],
                "avg_expected_conversion": float(row['avg_expected_conversion'] or 0),
                "avg_actual_conversion": float(row['avg_actual_conversion'] or 0),
                "improvements": row['improvements'],
                "improvement_rate": float(row['improvement_rate'] or 0)
            }
            for row in rows
        ]
    }