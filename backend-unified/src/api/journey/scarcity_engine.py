# Scarcity Trigger Engine for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4
import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, ScarcityTriggerEvent
from ...utils.redis_client import get_redis_client
from ...utils.ml_models import ScarcityOptimizationModel
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# SCARCITY TRIGGER ENGINE SERVICE
# =============================================================================

class ScarcityTriggerEngine:
    """Advanced scarcity trigger engine for conversion optimization"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.scarcity_model = ScarcityOptimizationModel()
        
        # Scarcity trigger configurations
        self.trigger_configs = {
            "social_proof": {
                "cooldown": 300,  # 5 minutes
                "max_frequency": 3,  # per session
                "effectiveness_threshold": 0.7
            },
            "time_pressure": {
                "cooldown": 600,  # 10 minutes
                "max_frequency": 2,  # per session
                "effectiveness_threshold": 0.8
            },
            "inventory": {
                "cooldown": 180,  # 3 minutes
                "max_frequency": 4,  # per session
                "effectiveness_threshold": 0.6
            },
            "exclusivity": {
                "cooldown": 900,  # 15 minutes
                "max_frequency": 1,  # per session
                "effectiveness_threshold": 0.9
            }
        }
    
    async def evaluate_scarcity_triggers(self, session: JourneySession, stage: JourneyStage) -> List[ScarcityTrigger]:
        """Evaluate and generate appropriate scarcity triggers for the current journey stage"""
        try:
            logger.info(f"Evaluating scarcity triggers for session: {session.session_id}, stage: {stage}")
            
            # Step 1: Get user scarcity sensitivity profile
            scarcity_sensitivity = await self._get_scarcity_sensitivity(session)
            
            # Step 2: Check trigger eligibility and cooldowns
            eligible_triggers = await self._check_trigger_eligibility(session, stage)
            
            # Step 3: Generate triggers based on user psychology and journey stage
            triggers = []
            for trigger_type in eligible_triggers:
                trigger = await self._generate_trigger_by_type(session, trigger_type, scarcity_sensitivity)
                if trigger:
                    triggers.append(trigger)
            
            # Step 4: Optimize trigger timing and intensity
            optimized_triggers = await self._optimize_trigger_timing(session, triggers)
            
            # Step 5: Record trigger events for analytics
            await self._record_trigger_events(session, optimized_triggers)
            
            logger.info(f"Generated {len(optimized_triggers)} scarcity triggers for session: {session.session_id}")
            return optimized_triggers
            
        except Exception as e:
            logger.error(f"Error evaluating scarcity triggers: {str(e)}")
            return []
    
    async def apply_scarcity_trigger(self, session: JourneySession, trigger_type: str, custom_params: Dict[str, Any] = None) -> ScarcityTrigger:
        """Apply a specific scarcity trigger with custom parameters"""
        try:
            logger.info(f"Applying scarcity trigger: {trigger_type} for session: {session.session_id}")
            
            # Get scarcity sensitivity
            scarcity_sensitivity = await self._get_scarcity_sensitivity(session)
            
            # Generate specific trigger
            trigger = await self._generate_trigger_by_type(session, trigger_type, scarcity_sensitivity, custom_params)
            
            if trigger:
                # Record trigger event
                await self._record_trigger_events(session, [trigger])
                
                # Update trigger cache
                await self._update_trigger_cache(session, trigger)
                
                logger.info(f"Scarcity trigger applied successfully: {trigger_type}")
                return trigger
            else:
                raise ValueError(f"Failed to generate trigger: {trigger_type}")
                
        except Exception as e:
            logger.error(f"Error applying scarcity trigger: {str(e)}")
            raise
    
    async def get_trigger_effectiveness(self, session_id: str, time_range: str = "24h") -> Dict[str, Any]:
        """Get effectiveness metrics for applied scarcity triggers"""
        try:
            logger.debug(f"Getting trigger effectiveness for session: {session_id}")
            
            # Calculate time range
            if time_range == "24h":
                since = datetime.utcnow() - timedelta(hours=24)
            elif time_range == "7d":
                since = datetime.utcnow() - timedelta(days=7)
            else:
                since = datetime.utcnow() - timedelta(hours=1)
            
            # Query trigger events
            result = await self.db.execute(
                select(ScarcityTriggerEvent)
                .where(
                    and_(
                        ScarcityTriggerEvent.session_id == session_id,
                        ScarcityTriggerEvent.trigger_timestamp >= since
                    )
                )
                .order_by(ScarcityTriggerEvent.trigger_timestamp.desc())
            )
            
            trigger_events = result.scalars().all()
            
            # Calculate effectiveness metrics
            effectiveness_metrics = {
                "total_triggers": len(trigger_events),
                "converted_triggers": len([t for t in trigger_events if t.conversion_attributed]),
                "conversion_rate": 0.0,
                "average_engagement_change": 0.0,
                "trigger_types_used": {},
                "most_effective_trigger": None
            }
            
            if trigger_events:
                effectiveness_metrics["conversion_rate"] = (
                    len([t for t in trigger_events if t.conversion_attributed]) / len(trigger_events)
                )
                effectiveness_metrics["average_engagement_change"] = (
                    sum(t.engagement_change or 0 for t in trigger_events) / len(trigger_events)
                )
                
                # Analyze trigger types
                for event in trigger_events:
                    trigger_type = event.trigger_type
                    if trigger_type not in effectiveness_metrics["trigger_types_used"]:
                        effectiveness_metrics["trigger_types_used"][trigger_type] = {
                            "count": 0,
                            "conversions": 0,
                            "avg_engagement_change": 0.0
                        }
                    
                    effectiveness_metrics["trigger_types_used"][trigger_type]["count"] += 1
                    if event.conversion_attributed:
                        effectiveness_metrics["trigger_types_used"][trigger_type]["conversions"] += 1
                    effectiveness_metrics["trigger_types_used"][trigger_type]["avg_engagement_change"] += (
                        event.engagement_change or 0
                    )
                
                # Calculate averages and find most effective trigger
                max_effectiveness = 0
                for trigger_type, stats in effectiveness_metrics["trigger_types_used"].items():
                    if stats["count"] > 0:
                        stats["conversion_rate"] = stats["conversions"] / stats["count"]
                        stats["avg_engagement_change"] /= stats["count"]
                        
                        # Effectiveness score combines conversion rate and engagement change
                        effectiveness_score = stats["conversion_rate"] * 0.7 + stats["avg_engagement_change"] * 0.3
                        if effectiveness_score > max_effectiveness:
                            max_effectiveness = effectiveness_score
                            effectiveness_metrics["most_effective_trigger"] = trigger_type
            
            return effectiveness_metrics
            
        except Exception as e:
            logger.error(f"Error getting trigger effectiveness: {str(e)}")
            return {"error": str(e)}
    
    # =============================================================================
    # TRIGGER GENERATION METHODS
    # =============================================================================
    
    async def _generate_social_proof_triggers(self, session: JourneySession, sensitivity: Dict[str, Any]) -> List[ScarcityTrigger]:
        """Generate social proof-based scarcity triggers"""
        triggers = []
        
        # Get real-time social proof data
        social_proof_data = await self._get_real_time_social_proof(session)
        
        # Recent views trigger
        if social_proof_data.get("recent_views", 0) > 5:
            triggers.append(ScarcityTrigger(
                trigger_type="social_proof_views",
                message=f"{social_proof_data['recent_views']} people viewed this in the last hour",
                intensity="medium",
                timing="immediate",
                authenticity="real_data"
            ))
        
        # Purchase activity trigger
        if social_proof_data.get("recent_purchases", 0) > 0:
            triggers.append(ScarcityTrigger(
                trigger_type="social_proof_purchases",
                message=f"{social_proof_data['recent_purchases']} people purchased this today",
                intensity="high",
                timing="consideration_stage",
                authenticity="real_data"
            ))
        
        # Live activity trigger
        if social_proof_data.get("live_users", 0) > 10:
            triggers.append(ScarcityTrigger(
                trigger_type="social_proof_live",
                message=f"{social_proof_data['live_users']} people are currently browsing",
                intensity="low",
                timing="continuous",
                authenticity="real_data"
            ))
        
        return triggers
    
    async def _generate_time_pressure_triggers(self, session: JourneySession, sensitivity: Dict[str, Any]) -> List[ScarcityTrigger]:
        """Generate time-based scarcity triggers"""
        triggers = []
        
        # Persona-specific time pressure
        persona_type = session.persona_type
        
        if persona_type in ["TechEarlyAdopter", "StudentHustler"]:
            # Fast decision makers - shorter timeframes
            triggers.append(ScarcityTrigger(
                trigger_type="time_limited_offer",
                message="Flash Sale: 25% off expires in 2 hours!",
                intensity="very_high",
                timing="decision_stage",
                authenticity="real_promotion"
            ))
        elif persona_type in ["BusinessOwner", "RemoteDad"]:
            # More deliberate decision makers - longer timeframes
            triggers.append(ScarcityTrigger(
                trigger_type="time_limited_offer",
                message="Special offer: 15% off until tomorrow",
                intensity="medium",
                timing="consideration_to_decision",
                authenticity="real_promotion"
            ))
        
        # Session-specific time pressure based on duration
        session_duration = (datetime.utcnow() - session.start_timestamp).total_seconds()
        if session_duration > 300:  # 5 minutes
            triggers.append(ScarcityTrigger(
                trigger_type="session_timeout_offer",
                message="Don't leave empty-handed! 10% off before you go",
                intensity="medium",
                timing="exit_intent",
                authenticity="session_based"
            ))
        
        return triggers
    
    async def _generate_inventory_triggers(self, session: JourneySession, sensitivity: Dict[str, Any]) -> List[ScarcityTrigger]:
        """Generate inventory-based scarcity triggers"""
        triggers = []
        
        # Get inventory data (could be real or artificial scarcity)
        inventory_data = await self._get_inventory_data(session)
        
        if inventory_data.get("low_stock", False):
            stock_count = inventory_data.get("stock_count", 0)
            
            if stock_count <= 5:
                triggers.append(ScarcityTrigger(
                    trigger_type="inventory_critical",
                    message=f"Only {stock_count} left in stock!",
                    intensity="very_high",
                    timing="immediate",
                    authenticity="inventory_based"
                ))
            elif stock_count <= 20:
                triggers.append(ScarcityTrigger(
                    trigger_type="inventory_low",
                    message=f"Limited stock: Only {stock_count} remaining",
                    intensity="high",
                    timing="consideration_stage",
                    authenticity="inventory_based"
                ))
        
        # Back in stock trigger for returning visitors
        if session.journey_path == JourneyPath.RETURNING_VISITOR_PERSONALIZED.value:
            triggers.append(ScarcityTrigger(
                trigger_type="inventory_restock",
                message="Good news! The item you viewed is back in stock",
                intensity="medium",
                timing="immediate",
                authenticity="inventory_based"
            ))
        
        return triggers
    
    async def _generate_exclusivity_triggers(self, session: JourneySession, sensitivity: Dict[str, Any]) -> List[ScarcityTrigger]:
        """Generate exclusivity-based scarcity triggers"""
        triggers = []
        
        # VIP/membership exclusivity
        if session.user_id:  # Registered user
            triggers.append(ScarcityTrigger(
                trigger_type="member_exclusive",
                message="Member exclusive: Special pricing just for you",
                intensity="high",
                timing="decision_stage",
                authenticity="membership_based"
            ))
        
        # Geographic exclusivity
        if session.device_type == DeviceType.MOBILE.value:
            triggers.append(ScarcityTrigger(
                trigger_type="mobile_exclusive",
                message="Mobile-only deal: Extra 5% off on app",
                intensity="medium",
                timing="consideration_stage",
                authenticity="channel_exclusive"
            ))
        
        # First-time visitor exclusivity
        if session.journey_path != JourneyPath.RETURNING_VISITOR_PERSONALIZED.value:
            triggers.append(ScarcityTrigger(
                trigger_type="first_time_exclusive",
                message="Welcome offer: 15% off your first purchase",
                intensity="high",
                timing="awareness_to_consideration",
                authenticity="new_customer_offer"
            ))
        
        return triggers
    
    # =============================================================================
    # INTERNAL HELPER METHODS
    # =============================================================================
    
    async def _get_scarcity_sensitivity(self, session: JourneySession) -> Dict[str, Any]:
        """Get user scarcity sensitivity profile"""
        # Check cache first
        cache_key = f"scarcity_sensitivity:{session.session_id}"
        cached_sensitivity = await self.redis_client.get(cache_key)
        if cached_sensitivity:
            return json.loads(cached_sensitivity)
        
        # Analyze persona and behavior patterns
        sensitivity_profile = {
            "responds_to_social_proof": True,
            "responds_to_time_pressure": True,
            "responds_to_exclusivity": True,
            "optimal_intensity": "medium",
            "frequency_tolerance": 3
        }
        
        # Persona-specific adjustments
        if session.persona_type == "TechEarlyAdopter":
            sensitivity_profile.update({
                "responds_to_social_proof": True,
                "responds_to_time_pressure": True,
                "optimal_intensity": "high",
                "frequency_tolerance": 4
            })
        elif session.persona_type == "BusinessOwner":
            sensitivity_profile.update({
                "responds_to_social_proof": False,
                "responds_to_exclusivity": True,
                "optimal_intensity": "low",
                "frequency_tolerance": 2
            })
        elif session.persona_type == "StudentHustler":
            sensitivity_profile.update({
                "responds_to_time_pressure": True,
                "responds_to_social_proof": True,
                "optimal_intensity": "very_high",
                "frequency_tolerance": 5
            })
        
        # Cache for 30 minutes
        await self.redis_client.setex(cache_key, 1800, json.dumps(sensitivity_profile))
        return sensitivity_profile
    
    async def _check_trigger_eligibility(self, session: JourneySession, stage: JourneyStage) -> List[str]:
        """Check which trigger types are eligible based on cooldowns and frequency"""
        eligible_triggers = []
        
        # Get recent trigger history
        recent_triggers = await self._get_recent_triggers(session.session_id)
        
        for trigger_type, config in self.trigger_configs.items():
            # Check frequency limit
            recent_count = len([t for t in recent_triggers if t.trigger_type == trigger_type])
            if recent_count >= config["max_frequency"]:
                continue
            
            # Check cooldown
            last_trigger = next((t for t in recent_triggers if t.trigger_type == trigger_type), None)
            if last_trigger:
                time_since_last = (datetime.utcnow() - last_trigger.trigger_timestamp).total_seconds()
                if time_since_last < config["cooldown"]:
                    continue
            
            # Stage-specific eligibility
            if self._is_trigger_appropriate_for_stage(trigger_type, stage):
                eligible_triggers.append(trigger_type)
        
        return eligible_triggers
    
    async def _generate_trigger_by_type(self, session: JourneySession, trigger_type: str, sensitivity: Dict[str, Any], custom_params: Dict[str, Any] = None) -> Optional[ScarcityTrigger]:
        """Generate a specific type of scarcity trigger"""
        if trigger_type == "social_proof":
            triggers = await self._generate_social_proof_triggers(session, sensitivity)
            return triggers[0] if triggers else None
        elif trigger_type == "time_pressure":
            triggers = await self._generate_time_pressure_triggers(session, sensitivity)
            return triggers[0] if triggers else None
        elif trigger_type == "inventory":
            triggers = await self._generate_inventory_triggers(session, sensitivity)
            return triggers[0] if triggers else None
        elif trigger_type == "exclusivity":
            triggers = await self._generate_exclusivity_triggers(session, sensitivity)
            return triggers[0] if triggers else None
        else:
            return None
    
    async def _optimize_trigger_timing(self, session: JourneySession, triggers: List[ScarcityTrigger]) -> List[ScarcityTrigger]:
        """Optimize trigger timing and intensity based on session context"""
        optimized_triggers = []
        
        for trigger in triggers:
            # Adjust timing based on session stage and duration
            session_duration = (datetime.utcnow() - session.start_timestamp).total_seconds()
            
            # Optimize trigger intensity based on conversion probability
            if session.conversion_probability > 0.7:
                # High conversion probability - use subtle triggers
                if trigger.intensity == "very_high":
                    trigger.intensity = "high"
                elif trigger.intensity == "high":
                    trigger.intensity = "medium"
            elif session.conversion_probability < 0.3:
                # Low conversion probability - use stronger triggers
                if trigger.intensity == "low":
                    trigger.intensity = "medium"
                elif trigger.intensity == "medium":
                    trigger.intensity = "high"
            
            # Adjust message based on device type
            if session.device_type == DeviceType.MOBILE.value:
                # Mobile users prefer shorter, emoji-rich messages
                trigger.message = await self._optimize_message_for_mobile(trigger.message)
            
            optimized_triggers.append(trigger)
        
        return optimized_triggers
    
    async def _record_trigger_events(self, session: JourneySession, triggers: List[ScarcityTrigger]) -> None:
        """Record trigger events for analytics and tracking"""
        for trigger in triggers:
            trigger_event = ScarcityTriggerEvent(
                session_id=session.session_id,
                trigger_type=trigger.trigger_type,
                trigger_strategy=f"{trigger.trigger_type}_{trigger.intensity}",
                trigger_content=trigger.dict(),
                trigger_timing=int((datetime.utcnow() - session.start_timestamp).total_seconds()),
                user_response="pending",  # Will be updated when response is detected
                engagement_change=0.0,  # Will be updated based on subsequent interactions
                conversion_attributed=False,  # Will be updated if conversion occurs
                metadata={
                    "session_stage": session.current_stage,
                    "conversion_probability": session.conversion_probability,
                    "persona_type": session.persona_type
                }
            )
            
            self.db.add(trigger_event)
        
        await self.db.commit()
    
    async def _update_trigger_cache(self, session: JourneySession, trigger: ScarcityTrigger) -> None:
        """Update trigger cache for real-time access"""
        cache_key = f"active_triggers:{session.session_id}"
        
        # Get existing active triggers
        existing_triggers = await self.redis_client.get(cache_key)
        if existing_triggers:
            triggers_list = json.loads(existing_triggers)
        else:
            triggers_list = []
        
        # Add new trigger
        triggers_list.append({
            "trigger": trigger.dict(),
            "applied_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        })
        
        # Keep only recent triggers (last 5)
        triggers_list = triggers_list[-5:]
        
        # Update cache
        await self.redis_client.setex(cache_key, 3600, json.dumps(triggers_list))
    
    async def _get_recent_triggers(self, session_id: str) -> List[ScarcityTriggerEvent]:
        """Get recent trigger events for the session"""
        since = datetime.utcnow() - timedelta(hours=24)
        
        result = await self.db.execute(
            select(ScarcityTriggerEvent)
            .where(
                and_(
                    ScarcityTriggerEvent.session_id == session_id,
                    ScarcityTriggerEvent.trigger_timestamp >= since
                )
            )
            .order_by(ScarcityTriggerEvent.trigger_timestamp.desc())
        )
        
        return result.scalars().all()
    
    def _is_trigger_appropriate_for_stage(self, trigger_type: str, stage: JourneyStage) -> bool:
        """Check if trigger type is appropriate for the current journey stage"""
        stage_appropriateness = {
            "social_proof": [JourneyStage.AWARENESS, JourneyStage.CONSIDERATION],
            "time_pressure": [JourneyStage.CONSIDERATION, JourneyStage.DECISION],
            "inventory": [JourneyStage.CONSIDERATION, JourneyStage.DECISION],
            "exclusivity": [JourneyStage.AWARENESS, JourneyStage.CONSIDERATION, JourneyStage.DECISION]
        }
        
        return stage in stage_appropriateness.get(trigger_type, [])
    
    async def _get_real_time_social_proof(self, session: JourneySession) -> Dict[str, Any]:
        """Get real-time social proof data"""
        # In production, this would query real analytics data
        # For now, return realistic mock data
        return {
            "recent_views": random.randint(15, 45),
            "recent_purchases": random.randint(2, 8),
            "live_users": random.randint(12, 35),
            "total_customers": random.randint(5000, 15000)
        }
    
    async def _get_inventory_data(self, session: JourneySession) -> Dict[str, Any]:
        """Get inventory data for scarcity triggers"""
        # In production, this would query real inventory data
        # For now, return mock data based on session context
        if session.conversion_probability > 0.6:
            # High probability sessions get low stock triggers
            return {
                "low_stock": True,
                "stock_count": random.randint(3, 15),
                "restock_expected": False
            }
        else:
            return {
                "low_stock": False,
                "stock_count": random.randint(50, 200),
                "restock_expected": False
            }
    
    async def _optimize_message_for_mobile(self, message: str) -> str:
        """Optimize trigger message for mobile display"""
        # Add emojis and make more concise for mobile
        emoji_map = {
            "people": "👥",
            "purchased": "🛒",
            "viewed": "👀",
            "hours": "⏰",
            "limited": "🔥",
            "exclusive": "⭐",
            "stock": "📦"
        }
        
        mobile_message = message
        for word, emoji in emoji_map.items():
            if word in message.lower() and emoji not in message:
                mobile_message = f"{emoji} {mobile_message}"
                break
        
        # Truncate if too long for mobile
        if len(mobile_message) > 60:
            mobile_message = mobile_message[:57] + "..."
        
        return mobile_message