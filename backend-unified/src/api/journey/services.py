# Journey Services for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, JourneyTouchpoint, ConversionEvent, PersonalizationData, CrossDeviceSession
from ..ux_intelligence.services import UXIntelligenceService
from ...utils.redis_client import get_redis_client
from ...utils.ml_models import ConversionPredictionModel, PersonalizationModel
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# CORE JOURNEY SESSION SERVICE
# =============================================================================

class JourneySessionService:
    """Core service for managing customer journey sessions"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.ux_intelligence = UXIntelligenceService(db)
        self.conversion_model = ConversionPredictionModel()
        self.personalization_model = PersonalizationModel()
    
    async def start_journey_session(self, session_data: JourneySessionCreate) -> JourneySessionResponse:
        """Initialize a new customer journey session"""
        try:
            logger.info(f"Starting journey session: {session_data.session_id}")
            
            # Step 1: Validate session data
            await self._validate_session_data(session_data)
            
            # Step 2: Determine optimal journey path
            journey_path = await self._determine_journey_path(session_data)
            
            # Step 3: Calculate initial conversion probability
            initial_probability = await self._calculate_initial_conversion_probability(session_data)
            
            # Step 4: Create journey session record
            journey_session = JourneySession(
                session_id=session_data.session_id,
                user_id=session_data.user_id,
                persona_type=session_data.persona.type,
                persona_confidence=session_data.persona.confidence,
                device_type=session_data.device_context.type.value,
                device_fingerprint=session_data.device_context.fingerprint,
                current_stage=JourneyStage.AWARENESS.value,
                journey_path=journey_path,
                conversion_probability=initial_probability,
                entry_point=session_data.entry_point.dict(),
                utm_data=session_data.utm_data,
                referrer_data=session_data.referrer_data,
                metadata={
                    "persona_attributes": session_data.persona.attributes,
                    "device_context": session_data.device_context.dict(),
                    "intent_signals": session_data.intent_signals.dict()
                }
            )
            
            self.db.add(journey_session)
            await self.db.commit()
            
            # Step 5: Initialize real-time tracking
            await self._initialize_real_time_tracking(journey_session)
            
            # Step 6: Generate personalized content
            personalized_content = await self._generate_initial_personalized_content(
                journey_session, session_data
            )
            
            # Step 7: Create UX Intelligence bridge if needed
            if session_data.user_id:
                await self._create_ux_intelligence_bridge(journey_session)
            
            logger.info(f"Journey session started successfully: {session_data.session_id}")
            
            return JourneySessionResponse(
                success=True,
                session_id=journey_session.session_id,
                journey_state=JourneyState(
                    current_stage=JourneyStage(journey_session.current_stage),
                    personalized_path=JourneyPath(journey_session.journey_path),
                    conversion_probability=journey_session.conversion_probability,
                    next_optimal_touchpoint=await self._get_next_optimal_touchpoint(journey_session),
                    estimated_time_to_decision=await self._estimate_time_to_decision(journey_session)
                ),
                personalized_content=personalized_content,
                next_actions=await self._get_recommended_next_actions(journey_session)
            )
            
        except Exception as e:
            logger.error(f"Error starting journey session: {str(e)}")
            await self.db.rollback()
            raise
    
    async def update_journey_stage(self, session_id: str, stage_update: JourneyStageUpdate) -> JourneyStateResponse:
        """Update journey stage and recalculate personalization"""
        try:
            logger.info(f"Updating journey stage for session: {session_id}")
            
            # Step 1: Get current session
            session = await self._get_session(session_id)
            if not session:
                raise ValueError(f"Journey session not found: {session_id}")
            
            # Step 2: Validate stage transition
            current_stage = JourneyStage(session.current_stage)
            if not validate_journey_stage_transition(current_stage, stage_update.new_stage):
                raise ValueError(f"Invalid stage transition: {current_stage} -> {stage_update.new_stage}")
            
            # Step 3: Update session stage
            previous_stage = session.current_stage
            session.current_stage = stage_update.new_stage.value
            session.updated_at = datetime.utcnow()
            
            # Step 4: Record touchpoint for stage transition
            touchpoint = await self._create_stage_transition_touchpoint(
                session, previous_stage, stage_update
            )
            
            # Step 5: Update session metrics
            session.total_touchpoints += 1
            session.total_session_time = int((datetime.utcnow() - session.start_timestamp).total_seconds())
            
            # Step 6: Recalculate conversion probability
            new_probability = await self._recalculate_conversion_probability(
                session, stage_update.engagement_metrics
            )
            session.conversion_probability = new_probability
            
            # Step 7: Generate personalized recommendations
            recommendations = await self._generate_stage_recommendations(
                session, stage_update.contextual_data
            )
            
            # Step 8: Evaluate scarcity triggers
            scarcity_triggers = await self._evaluate_scarcity_triggers(
                session, stage_update.new_stage
            )
            
            # Step 9: Apply real-time adaptations
            adaptations = await self._apply_real_time_adaptations(session, stage_update)
            
            await self.db.commit()
            
            # Step 10: Update real-time analytics
            await self._update_real_time_analytics(session_id, stage_update.new_stage, new_probability)
            
            logger.info(f"Journey stage updated successfully: {session_id} -> {stage_update.new_stage}")
            
            return JourneyStateResponse(
                success=True,
                updated_journey_state=JourneyState(
                    current_stage=stage_update.new_stage,
                    personalized_path=JourneyPath(session.journey_path),
                    conversion_probability=session.conversion_probability,
                    next_optimal_touchpoint=await self._get_next_optimal_touchpoint(session),
                    journey_progress=await self._calculate_journey_progress(session)
                ),
                personalized_recommendations=recommendations,
                scarcity_triggers=scarcity_triggers,
                real_time_adaptations=adaptations
            )
            
        except Exception as e:
            logger.error(f"Error updating journey stage: {str(e)}")
            await self.db.rollback()
            raise
    
    async def get_journey_state(self, session_id: str) -> Dict[str, Any]:
        """Get current journey state"""
        try:
            session = await self._get_session(session_id)
            if not session:
                raise ValueError(f"Journey session not found: {session_id}")
            
            # Get touchpoint history
            touchpoint_history = await self._get_touchpoint_history(session_id)
            
            # Calculate progress metrics
            progress_metrics = await self._calculate_progress_metrics(session)
            
            return {
                "session_id": session.session_id,
                "journey_state": {
                    "current_stage": session.current_stage,
                    "start_time": session.start_timestamp.isoformat(),
                    "total_touchpoints": session.total_touchpoints,
                    "conversion_probability": session.conversion_probability,
                    "progress_metrics": progress_metrics
                },
                "touchpoint_history": touchpoint_history
            }
            
        except Exception as e:
            logger.error(f"Error getting journey state: {str(e)}")
            raise
    
    # =============================================================================
    # INTERNAL HELPER METHODS
    # =============================================================================
    
    async def _validate_session_data(self, session_data: JourneySessionCreate) -> None:
        """Validate session data"""
        if not validate_session_id(session_data.session_id):
            raise ValueError("Invalid session ID format")
        
        if not validate_probability_score(session_data.persona.confidence):
            raise ValueError("Invalid persona confidence score")
        
        # Check for duplicate session
        existing = await self._get_session(session_data.session_id)
        if existing:
            raise ValueError(f"Session already exists: {session_data.session_id}")
    
    async def _determine_journey_path(self, session_data: JourneySessionCreate) -> str:
        """Determine optimal journey path based on user context"""
        device_type = session_data.device_context.type
        traffic_source = session_data.entry_point.source
        
        # Mobile TikTok Users
        if (device_type == DeviceType.MOBILE and 
            traffic_source.lower() in ["tiktok", "instagram", "youtube_shorts"]):
            return JourneyPath.MOBILE_TIKTOK_FAST_TRACK.value
        
        # Desktop Researchers
        elif (device_type == DeviceType.DESKTOP and 
              traffic_source.lower() in ["google", "direct", "referral"]):
            return JourneyPath.DESKTOP_RESEARCH_DEEP.value
        
        # Returning Visitors
        elif session_data.returning_visitor_indicators:
            return JourneyPath.RETURNING_VISITOR_PERSONALIZED.value
        
        # Default path
        else:
            return JourneyPath.STANDARD_CONVERSION_FUNNEL.value
    
    async def _calculate_initial_conversion_probability(self, session_data: JourneySessionCreate) -> float:
        """Calculate initial conversion probability using ML model"""
        features = {
            "persona_confidence": session_data.persona.confidence,
            "device_type": session_data.device_context.type.value,
            "traffic_source": session_data.entry_point.source,
            "purchase_intent": session_data.intent_signals.purchase_intent,
            "urgency_level": session_data.intent_signals.urgency_level,
            "time_of_day": session_data.timestamp.hour,
            "day_of_week": session_data.timestamp.weekday()
        }
        
        # Use ML model to predict conversion probability
        probability = await self.conversion_model.predict(features)
        
        # Clamp between reasonable bounds
        return max(0.1, min(0.9, probability))
    
    async def _initialize_real_time_tracking(self, session: JourneySession) -> None:
        """Initialize real-time tracking for the session"""
        cache_key = f"journey_session:{session.session_id}"
        session_data = {
            "session_id": session.session_id,
            "current_stage": session.current_stage,
            "conversion_probability": session.conversion_probability,
            "journey_path": session.journey_path,
            "start_time": session.start_timestamp.isoformat(),
            "touchpoint_count": 0
        }
        
        # Cache session data for 1 hour
        await self.redis_client.setex(cache_key, 3600, json.dumps(session_data))
    
    async def _generate_initial_personalized_content(self, session: JourneySession, session_data: JourneySessionCreate) -> PersonalizedContent:
        """Generate initial personalized content"""
        # Determine personalization strategy based on journey path
        if session.journey_path == JourneyPath.MOBILE_TIKTOK_FAST_TRACK.value:
            return await self._generate_mobile_tiktok_content(session, session_data)
        elif session.journey_path == JourneyPath.DESKTOP_RESEARCH_DEEP.value:
            return await self._generate_desktop_research_content(session, session_data)
        elif session.journey_path == JourneyPath.RETURNING_VISITOR_PERSONALIZED.value:
            return await self._generate_returning_visitor_content(session, session_data)
        else:
            return await self._generate_standard_content(session, session_data)
    
    async def _generate_mobile_tiktok_content(self, session: JourneySession, session_data: JourneySessionCreate) -> PersonalizedContent:
        """Generate content for mobile TikTok users"""
        referrer_video = session_data.entry_point.referrer_video
        
        if referrer_video:
            # Replicate TikTok video elements
            hero_message = f"🚀 {session_data.persona.type} Special - As Seen on TikTok!"
            cta = "Swipe to see all features →"
            social_proof = "67K+ people love this!"
        else:
            # Default mobile content
            hero_message = "🔥 Trending Now - Limited Time Offer!"
            cta = "Tap to explore →"
            social_proof = "Join thousands of happy customers"
        
        return PersonalizedContent(
            hero_message=hero_message,
            call_to_action=cta,
            trust_signals=["30-day guarantee", "Free shipping", "5-star reviews"],
            scarcity_trigger="Only 23 left in stock",
            social_proof=social_proof,
            personalization_strategy="mobile_tiktok_viral_replication"
        )
    
    async def _generate_desktop_research_content(self, session: JourneySession, session_data: JourneySessionCreate) -> PersonalizedContent:
        """Generate content for desktop researchers"""
        return PersonalizedContent(
            hero_message="Complete Solution for Business Professionals",
            call_to_action="Compare Features →",
            trust_signals=["Industry certified", "Expert endorsed", "Enterprise grade"],
            social_proof="Trusted by 10,000+ businesses",
            personalization_strategy="desktop_research_comprehensive"
        )
    
    async def _generate_returning_visitor_content(self, session: JourneySession, session_data: JourneySessionCreate) -> PersonalizedContent:
        """Generate content for returning visitors"""
        return PersonalizedContent(
            hero_message="Welcome back! Your exclusive offer awaits",
            call_to_action="Continue where you left off →",
            trust_signals=["Returning customer discount", "VIP support", "Extended warranty"],
            scarcity_trigger="Your 15% discount expires in 6 hours",
            social_proof="You're one of our valued returning customers",
            personalization_strategy="returning_visitor_exclusive"
        )
    
    async def _generate_standard_content(self, session: JourneySession, session_data: JourneySessionCreate) -> PersonalizedContent:
        """Generate standard content"""
        return PersonalizedContent(
            hero_message="Discover the Perfect Solution for You",
            call_to_action="Get started →",
            trust_signals=["Money-back guarantee", "Secure checkout", "Customer support"],
            social_proof="Trusted by thousands",
            personalization_strategy="standard_conversion_funnel"
        )
    
    async def _create_ux_intelligence_bridge(self, session: JourneySession) -> None:
        """Create bridge connection with UX Intelligence Engine"""
        # This would integrate with the existing UX Intelligence system
        # For now, we'll create a placeholder bridge record
        bridge_data = {
            "journey_session_id": session.session_id,
            "ux_session_id": f"ux_{session.session_id}",
            "integration_timestamp": datetime.utcnow(),
            "data_flow_direction": "bidirectional"
        }
        
        # Store bridge data in cache for now
        cache_key = f"ux_journey_bridge:{session.session_id}"
        await self.redis_client.setex(cache_key, 3600, json.dumps(bridge_data, default=str))
    
    async def _get_session(self, session_id: str) -> Optional[JourneySession]:
        """Get journey session by ID"""
        result = await self.db.execute(
            select(JourneySession).where(JourneySession.session_id == session_id)
        )
        return result.scalar_one_or_none()
    
    async def _create_stage_transition_touchpoint(self, session: JourneySession, previous_stage: str, stage_update: JourneyStageUpdate) -> JourneyTouchpoint:
        """Create touchpoint record for stage transition"""
        touchpoint = JourneyTouchpoint(
            session_id=session.session_id,
            touchpoint_sequence=session.total_touchpoints + 1,
            touchpoint_type=TouchpointType.STAGE_TRANSITION.value,
            interaction_data={
                "previous_stage": previous_stage,
                "new_stage": stage_update.new_stage.value,
                "trigger_event": stage_update.trigger_event,
                "engagement_metrics": stage_update.engagement_metrics.dict()
            },
            engagement_score=stage_update.engagement_metrics.engagement_score or 0.5,
            duration_seconds=stage_update.engagement_metrics.time_on_page,
            scroll_depth=stage_update.engagement_metrics.scroll_depth,
            click_count=stage_update.engagement_metrics.interaction_count
        )
        
        self.db.add(touchpoint)
        return touchpoint
    
    async def _recalculate_conversion_probability(self, session: JourneySession, engagement_metrics: EngagementMetrics) -> float:
        """Recalculate conversion probability based on new data"""
        current_probability = session.conversion_probability
        
        # Factor in engagement metrics
        engagement_boost = 0.0
        if engagement_metrics.engagement_score and engagement_metrics.engagement_score > 0.7:
            engagement_boost += 0.1
        if engagement_metrics.scroll_depth > 0.8:
            engagement_boost += 0.05
        if engagement_metrics.interaction_count > 3:
            engagement_boost += 0.05
        
        # Factor in journey stage progression
        stage_boost = {
            JourneyStage.AWARENESS.value: 0.0,
            JourneyStage.CONSIDERATION.value: 0.1,
            JourneyStage.DECISION.value: 0.2,
            JourneyStage.CONVERSION.value: 0.3
        }.get(session.current_stage, 0.0)
        
        # Calculate new probability
        new_probability = min(0.95, current_probability + engagement_boost + stage_boost)
        return max(0.05, new_probability)
    
    async def _generate_stage_recommendations(self, session: JourneySession, contextual_data: Dict[str, Any]) -> List[PersonalizedRecommendation]:
        """Generate personalized recommendations for current stage"""
        recommendations = []
        
        if session.current_stage == JourneyStage.CONSIDERATION.value:
            recommendations.extend([
                PersonalizedRecommendation(
                    type="content_adaptation",
                    content="Show detailed feature comparison",
                    priority="high",
                    expected_impact=0.15
                ),
                PersonalizedRecommendation(
                    type="social_proof",
                    content="Display customer testimonials",
                    priority="medium",
                    expected_impact=0.08
                )
            ])
        elif session.current_stage == JourneyStage.DECISION.value:
            recommendations.extend([
                PersonalizedRecommendation(
                    type="scarcity_trigger",
                    content="Activate limited-time offer",
                    priority="high",
                    expected_impact=0.22
                ),
                PersonalizedRecommendation(
                    type="trust_building",
                    content="Emphasize money-back guarantee",
                    priority="medium",
                    expected_impact=0.12
                )
            ])
        
        return recommendations
    
    async def _evaluate_scarcity_triggers(self, session: JourneySession, stage: JourneyStage) -> List[ScarcityTrigger]:
        """Evaluate and generate appropriate scarcity triggers"""
        triggers = []
        
        if stage == JourneyStage.DECISION:
            # Time-based scarcity for decision stage
            triggers.append(ScarcityTrigger(
                trigger_type="time_pressure",
                message="Limited time: 25% off expires in 4 hours",
                intensity="high",
                timing="immediate",
                authenticity="real_promotion"
            ))
            
            # Social proof scarcity
            triggers.append(ScarcityTrigger(
                trigger_type="social_proof",
                message="7 people purchased this in the last hour",
                intensity="medium",
                timing="consideration_to_decision",
                authenticity="real_data"
            ))
        
        return triggers
    
    async def _apply_real_time_adaptations(self, session: JourneySession, stage_update: JourneyStageUpdate) -> Dict[str, Any]:
        """Apply real-time adaptations based on session data"""
        adaptations = {
            "content_adaptations": [],
            "layout_adaptations": [],
            "interaction_adaptations": []
        }
        
        # Adapt based on engagement metrics
        if stage_update.engagement_metrics.engagement_score and stage_update.engagement_metrics.engagement_score < 0.5:
            adaptations["content_adaptations"].append({
                "type": "engagement_boost",
                "action": "increase_visual_elements",
                "expected_impact": 0.1
            })
        
        # Adapt based on device type
        if session.device_type == DeviceType.MOBILE.value:
            adaptations["layout_adaptations"].append({
                "type": "mobile_optimization",
                "action": "single_column_layout",
                "expected_impact": 0.05
            })
        
        return adaptations
    
    async def _get_next_optimal_touchpoint(self, session: JourneySession) -> str:
        """Determine next optimal touchpoint"""
        stage_touchpoints = {
            JourneyStage.AWARENESS.value: "product_gallery_view",
            JourneyStage.CONSIDERATION.value: "feature_comparison",
            JourneyStage.DECISION.value: "checkout_initiation",
            JourneyStage.CONVERSION.value: "purchase_completion"
        }
        
        return stage_touchpoints.get(session.current_stage, "engagement_activity")
    
    async def _estimate_time_to_decision(self, session: JourneySession) -> str:
        """Estimate time to decision based on journey path"""
        time_estimates = {
            JourneyPath.MOBILE_TIKTOK_FAST_TRACK.value: "90_seconds",
            JourneyPath.DESKTOP_RESEARCH_DEEP.value: "45_minutes",
            JourneyPath.RETURNING_VISITOR_PERSONALIZED.value: "5_minutes",
            JourneyPath.STANDARD_CONVERSION_FUNNEL.value: "15_minutes"
        }
        
        return time_estimates.get(session.journey_path, "unknown")
    
    async def _get_recommended_next_actions(self, session: JourneySession) -> List[str]:
        """Get recommended next actions"""
        if session.journey_path == JourneyPath.MOBILE_TIKTOK_FAST_TRACK.value:
            return ["Enable swipe gestures", "Show viral social proof", "Prepare one-click checkout"]
        elif session.journey_path == JourneyPath.DESKTOP_RESEARCH_DEEP.value:
            return ["Load comparison tables", "Prepare detailed specs", "Show expert testimonials"]
        else:
            return ["Track engagement", "Prepare personalization", "Monitor conversion signals"]
    
    async def _get_touchpoint_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get touchpoint history for session"""
        result = await self.db.execute(
            select(JourneyTouchpoint)
            .where(JourneyTouchpoint.session_id == session_id)
            .order_by(JourneyTouchpoint.touchpoint_sequence)
        )
        
        touchpoints = result.scalars().all()
        return [
            {
                "touchpoint_type": tp.touchpoint_type,
                "timestamp": tp.timestamp.isoformat(),
                "duration": tp.duration_seconds,
                "engagement_score": tp.engagement_score
            }
            for tp in touchpoints
        ]
    
    async def _calculate_progress_metrics(self, session: JourneySession) -> Dict[str, float]:
        """Calculate journey progress metrics"""
        stage_weights = {
            JourneyStage.AWARENESS.value: 0.2,
            JourneyStage.CONSIDERATION.value: 0.4,
            JourneyStage.DECISION.value: 0.6,
            JourneyStage.CONVERSION.value: 0.8,
            JourneyStage.RETENTION.value: 1.0
        }
        
        progress = stage_weights.get(session.current_stage, 0.0)
        
        return {
            "engagement_score": min(1.0, session.total_touchpoints * 0.1),
            "intent_strength": session.conversion_probability,
            "decision_readiness": progress,
            "journey_completion": progress
        }
    
    async def _calculate_journey_progress(self, session: JourneySession) -> float:
        """Calculate overall journey progress"""
        stage_progress = {
            JourneyStage.AWARENESS.value: 0.25,
            JourneyStage.CONSIDERATION.value: 0.5,
            JourneyStage.DECISION.value: 0.75,
            JourneyStage.CONVERSION.value: 1.0
        }
        
        return stage_progress.get(session.current_stage, 0.0)
    
    async def _update_real_time_analytics(self, session_id: str, new_stage: JourneyStage, conversion_probability: float) -> None:
        """Update real-time analytics"""
        analytics_data = {
            "session_id": session_id,
            "stage_transition": new_stage.value,
            "conversion_probability": conversion_probability,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Publish to analytics stream
        await self.redis_client.lpush("journey_analytics_stream", json.dumps(analytics_data))
        
        # Update session cache
        cache_key = f"journey_session:{session_id}"
        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            session_data = json.loads(cached_data)
            session_data["current_stage"] = new_stage.value
            session_data["conversion_probability"] = conversion_probability
            session_data["last_update"] = datetime.utcnow().isoformat()
            
            await self.redis_client.setex(cache_key, 3600, json.dumps(session_data))