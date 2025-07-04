# Real-Time Optimization Engine for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4
import math

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, OptimizationEvent
from .personalization_engine import PersonalizationEngine
from .scarcity_engine import ScarcityTriggerEngine
from .ux_integration_bridge import UXIntelligenceIntegrationBridge
from ...utils.redis_client import get_redis_client
from ...utils.ml_models import OptimizationModel, PredictiveAnalyticsModel
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# REAL-TIME OPTIMIZATION ENGINE
# =============================================================================

class RealTimeOptimizer:
    """Advanced real-time optimization engine for dynamic journey enhancement"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.optimization_model = OptimizationModel()
        self.analytics_model = PredictiveAnalyticsModel()
        
        # Initialize sub-engines
        self.personalization_engine = PersonalizationEngine(db)
        self.scarcity_engine = ScarcityTriggerEngine(db)
        self.ux_bridge = UXIntelligenceIntegrationBridge(db)
        
        # Optimization thresholds and parameters
        self.optimization_config = {
            "min_engagement_drop": 0.15,  # Trigger optimization if engagement drops by 15%
            "conversion_probability_threshold": 0.7,  # High probability sessions get priority
            "real_time_window": 300,  # 5 minutes for real-time analysis
            "optimization_cooldown": 180,  # 3 minutes between optimizations
            "max_optimizations_per_session": 5
        }
    
    async def monitor_and_optimize_session(self, session_id: str, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor session in real-time and apply optimizations as needed"""
        try:
            logger.info(f"Starting real-time optimization monitoring for session: {session_id}")
            
            # Get current session state
            session = await self._get_session(session_id)
            if not session:
                return {"error": "Session not found"}
            
            # Analyze current performance vs baseline
            performance_analysis = await self._analyze_session_performance(session, engagement_data)
            
            # Determine if optimization is needed
            optimization_needed = await self._should_optimize(session, performance_analysis)
            
            if optimization_needed:
                # Apply multi-layer optimization
                optimization_result = await self._apply_real_time_optimization(session, performance_analysis)
                
                # Record optimization event
                await self._record_optimization_event(session, optimization_result)
                
                return {
                    "optimization_applied": True,
                    "session_id": session_id,
                    "optimization_details": optimization_result,
                    "performance_improvement": optimization_result.get("expected_improvement", {}),
                    "next_monitoring_interval": self._calculate_next_monitoring_interval(optimization_result)
                }
            else:
                return {
                    "optimization_applied": False,
                    "session_id": session_id,
                    "performance_status": "satisfactory",
                    "monitoring_continues": True,
                    "next_check_in": 60  # Check again in 60 seconds
                }
                
        except Exception as e:
            logger.error(f"Error in real-time optimization monitoring: {str(e)}")
            return {"error": str(e)}
    
    async def optimize_journey_flow_real_time(self, session_id: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Apply real-time journey flow optimization"""
        try:
            logger.debug(f"Optimizing journey flow for session: {session_id}")
            
            session = await self._get_session(session_id)
            if not session:
                return {"error": "Session not found"}
            
            # Analyze journey flow bottlenecks
            flow_analysis = await self._analyze_journey_flow(session, current_metrics)
            
            # Generate flow optimization strategies
            optimization_strategies = await self._generate_flow_optimizations(session, flow_analysis)
            
            # Apply highest impact optimizations
            applied_optimizations = []
            for strategy in optimization_strategies[:3]:  # Apply top 3 strategies
                if strategy["confidence"] > 0.75:
                    result = await self._apply_flow_optimization(session, strategy)
                    applied_optimizations.append(result)
            
            # Update journey flow cache
            await self._update_flow_optimization_cache(session, applied_optimizations)
            
            return {
                "session_id": session_id,
                "flow_optimizations_applied": len(applied_optimizations),
                "optimizations": applied_optimizations,
                "expected_flow_improvement": sum(opt.get("expected_impact", 0) for opt in applied_optimizations),
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing journey flow: {str(e)}")
            return {"error": str(e)}
    
    async def predict_and_preempt_abandonment(self, session_id: str, behavioral_signals: Dict[str, Any]) -> Dict[str, Any]:
        """Predict session abandonment and apply preemptive interventions"""
        try:
            logger.debug(f"Analyzing abandonment risk for session: {session_id}")
            
            session = await self._get_session(session_id)
            if not session:
                return {"error": "Session not found"}
            
            # Calculate abandonment probability
            abandonment_probability = await self._calculate_abandonment_probability(session, behavioral_signals)
            
            if abandonment_probability > 0.6:  # High risk threshold
                # Apply preemptive interventions
                interventions = await self._apply_abandonment_interventions(session, abandonment_probability)
                
                return {
                    "abandonment_risk": "high",
                    "abandonment_probability": abandonment_probability,
                    "interventions_applied": interventions,
                    "expected_retention_improvement": sum(i.get("retention_impact", 0) for i in interventions)
                }
            elif abandonment_probability > 0.3:  # Medium risk
                # Gentle engagement boost
                gentle_interventions = await self._apply_gentle_engagement_boost(session)
                
                return {
                    "abandonment_risk": "medium",
                    "abandonment_probability": abandonment_probability,
                    "gentle_interventions": gentle_interventions,
                    "monitoring_increased": True
                }
            else:
                return {
                    "abandonment_risk": "low",
                    "abandonment_probability": abandonment_probability,
                    "status": "session_healthy",
                    "continue_monitoring": True
                }
                
        except Exception as e:
            logger.error(f"Error in abandonment prediction: {str(e)}")
            return {"error": str(e)}
    
    async def optimize_conversion_probability_real_time(self, session_id: str, conversion_signals: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize conversion probability through real-time adjustments"""
        try:
            logger.debug(f"Optimizing conversion probability for session: {session_id}")
            
            session = await self._get_session(session_id)
            if not session:
                return {"error": "Session not found"}
            
            # Analyze conversion signals and current probability
            current_probability = session.conversion_probability
            signal_analysis = await self._analyze_conversion_signals(session, conversion_signals)
            
            # Determine optimization approach
            if current_probability < 0.3:
                # Low probability - aggressive optimization
                optimization_approach = "aggressive_conversion_boost"
            elif current_probability < 0.6:
                # Medium probability - targeted optimization
                optimization_approach = "targeted_conversion_enhancement"
            else:
                # High probability - fine-tuning
                optimization_approach = "conversion_fine_tuning"
            
            # Apply conversion optimization
            optimization_result = await self._apply_conversion_optimization(
                session, signal_analysis, optimization_approach
            )
            
            # Update conversion probability
            new_probability = await self._calculate_updated_conversion_probability(
                session, optimization_result
            )
            
            # Update session
            await self._update_session_conversion_probability(session.session_id, new_probability)
            
            return {
                "session_id": session_id,
                "optimization_approach": optimization_approach,
                "previous_probability": current_probability,
                "new_probability": new_probability,
                "probability_improvement": new_probability - current_probability,
                "optimizations_applied": optimization_result.get("optimizations", []),
                "expected_revenue_impact": optimization_result.get("revenue_impact", 0)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing conversion probability: {str(e)}")
            return {"error": str(e)}
    
    async def cross_device_optimization(self, session_id: str, device_switch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize experience during cross-device journey continuation"""
        try:
            logger.info(f"Optimizing cross-device journey for session: {session_id}")
            
            session = await self._get_session(session_id)
            if not session:
                return {"error": "Session not found"}
            
            # Analyze device switch context
            switch_analysis = await self._analyze_device_switch(session, device_switch_data)
            
            # Generate device-specific optimizations
            device_optimizations = await self._generate_cross_device_optimizations(session, switch_analysis)
            
            # Apply continuity optimizations
            continuity_result = await self._apply_journey_continuity_optimization(session, device_optimizations)
            
            # Update UX Intelligence with cross-device context
            await self.ux_bridge.process_unified_interaction(
                session_id, {
                    "interaction_type": "device_switch",
                    "device_switch_data": device_switch_data,
                    "optimizations_applied": continuity_result
                }
            )
            
            return {
                "session_id": session_id,
                "device_switch_optimized": True,
                "continuity_optimizations": continuity_result,
                "cross_device_experience_score": switch_analysis.get("experience_score", 0.8),
                "seamless_handoff_achieved": True
            }
            
        except Exception as e:
            logger.error(f"Error in cross-device optimization: {str(e)}")
            return {"error": str(e)}
    
    # =============================================================================
    # CORE ANALYSIS METHODS
    # =============================================================================
    
    async def _analyze_session_performance(self, session: JourneySession, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current session performance against baselines"""
        # Get baseline metrics for comparison
        baseline_metrics = await self._get_baseline_metrics(session.persona_type, session.current_stage)
        
        current_metrics = {
            "engagement_score": engagement_data.get("engagement_score", 0.5),
            "time_on_page": engagement_data.get("time_on_page", 0),
            "interaction_rate": engagement_data.get("interactions", 0) / max(engagement_data.get("time_on_page", 1), 1),
            "scroll_depth": engagement_data.get("scroll_depth", 0.5),
            "conversion_signals": len(engagement_data.get("conversion_signals", []))
        }
        
        # Calculate performance deltas
        performance_analysis = {
            "engagement_delta": current_metrics["engagement_score"] - baseline_metrics.get("engagement_score", 0.6),
            "interaction_delta": current_metrics["interaction_rate"] - baseline_metrics.get("interaction_rate", 0.3),
            "scroll_delta": current_metrics["scroll_depth"] - baseline_metrics.get("scroll_depth", 0.6),
            "performance_trend": "improving" if current_metrics["engagement_score"] > 0.7 else "declining",
            "optimization_priority": self._calculate_optimization_priority(current_metrics, baseline_metrics)
        }
        
        return performance_analysis
    
    async def _should_optimize(self, session: JourneySession, performance_analysis: Dict[str, Any]) -> bool:
        """Determine if optimization should be applied"""
        # Check cooldown
        last_optimization = await self._get_last_optimization_time(session.session_id)
        if last_optimization and (datetime.utcnow() - last_optimization).total_seconds() < self.optimization_config["optimization_cooldown"]:
            return False
        
        # Check optimization frequency
        optimization_count = await self._get_optimization_count(session.session_id)
        if optimization_count >= self.optimization_config["max_optimizations_per_session"]:
            return False
        
        # Check performance thresholds
        engagement_drop = abs(performance_analysis.get("engagement_delta", 0))
        if engagement_drop > self.optimization_config["min_engagement_drop"]:
            return True
        
        # High value sessions get priority optimization
        if session.conversion_probability > self.optimization_config["conversion_probability_threshold"]:
            return True
        
        # Optimization based on priority score
        return performance_analysis.get("optimization_priority", 0) > 0.7
    
    async def _apply_real_time_optimization(self, session: JourneySession, performance_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply comprehensive real-time optimization"""
        optimization_results = {
            "optimizations": [],
            "expected_improvement": {},
            "optimization_strategy": "multi_layer_enhancement"
        }
        
        # Layer 1: Personalization optimization
        if performance_analysis.get("engagement_delta", 0) < -0.1:
            personalization_result = await self.personalization_engine.optimize_personalization_real_time(
                session, {"performance_analysis": performance_analysis}
            )
            optimization_results["optimizations"].append({
                "layer": "personalization",
                "result": personalization_result
            })
        
        # Layer 2: Scarcity trigger optimization
        if session.conversion_probability > 0.4:
            scarcity_triggers = await self.scarcity_engine.evaluate_scarcity_triggers(
                session, JourneyStage(session.current_stage)
            )
            if scarcity_triggers:
                optimization_results["optimizations"].append({
                    "layer": "scarcity",
                    "triggers_applied": len(scarcity_triggers)
                })
        
        # Layer 3: UX Intelligence integration
        ux_optimization = await self.ux_bridge.process_unified_interaction(
            session.session_id, {
                "interaction_type": "real_time_optimization",
                "performance_analysis": performance_analysis,
                "optimization_request": True
            }
        )
        optimization_results["optimizations"].append({
            "layer": "ux_intelligence",
            "result": ux_optimization
        })
        
        # Calculate expected improvement
        optimization_results["expected_improvement"] = {
            "engagement_improvement": 0.15,
            "conversion_probability_increase": 0.08,
            "user_experience_enhancement": 0.12
        }
        
        return optimization_results
    
    async def _analyze_journey_flow(self, session: JourneySession, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze journey flow for bottlenecks and optimization opportunities"""
        # Get journey path efficiency
        expected_stage_duration = await self._get_expected_stage_duration(session.current_stage, session.persona_type)
        actual_stage_duration = (datetime.utcnow() - session.start_timestamp).total_seconds()
        
        flow_analysis = {
            "stage_efficiency": expected_stage_duration / max(actual_stage_duration, 1),
            "progression_rate": current_metrics.get("stage_progression_rate", 0.5),
            "bottleneck_detected": actual_stage_duration > (expected_stage_duration * 1.5),
            "flow_quality_score": min(1.0, current_metrics.get("flow_smoothness", 0.7)),
            "optimization_opportunities": []
        }
        
        # Identify specific bottlenecks
        if flow_analysis["bottleneck_detected"]:
            if session.current_stage == JourneyStage.AWARENESS.value:
                flow_analysis["optimization_opportunities"].append("awareness_engagement_enhancement")
            elif session.current_stage == JourneyStage.CONSIDERATION.value:
                flow_analysis["optimization_opportunities"].append("consideration_acceleration")
            elif session.current_stage == JourneyStage.DECISION.value:
                flow_analysis["optimization_opportunities"].append("decision_friction_reduction")
        
        return flow_analysis
    
    async def _calculate_abandonment_probability(self, session: JourneySession, behavioral_signals: Dict[str, Any]) -> float:
        """Calculate probability of session abandonment"""
        # Extract behavioral indicators
        session_duration = (datetime.utcnow() - session.start_timestamp).total_seconds()
        scroll_patterns = behavioral_signals.get("scroll_patterns", {})
        interaction_frequency = behavioral_signals.get("interaction_frequency", 0)
        exit_intent_signals = behavioral_signals.get("exit_intent_signals", [])
        
        # Base probability calculation
        base_probability = 0.3  # Default baseline
        
        # Adjust based on session duration
        if session_duration > 600:  # 10 minutes
            base_probability += 0.2
        elif session_duration < 60:  # Less than 1 minute
            base_probability += 0.3
        
        # Adjust based on engagement
        if interaction_frequency < 0.1:  # Very low interaction
            base_probability += 0.25
        
        # Exit intent signals
        if "cursor_towards_close" in exit_intent_signals:
            base_probability += 0.3
        if "back_button_hover" in exit_intent_signals:
            base_probability += 0.2
        
        # Scroll behavior
        if scroll_patterns.get("erratic_scrolling", False):
            base_probability += 0.15
        
        # Persona-specific adjustments
        if session.persona_type == "TechEarlyAdopter":
            base_probability -= 0.1  # Lower abandonment tendency
        elif session.persona_type == "BusinessOwner":
            base_probability -= 0.05  # Slightly lower
        
        return min(1.0, max(0.0, base_probability))
    
    # =============================================================================
    # OPTIMIZATION APPLICATION METHODS
    # =============================================================================
    
    async def _generate_flow_optimizations(self, session: JourneySession, flow_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate flow optimization strategies"""
        optimizations = []
        
        for opportunity in flow_analysis.get("optimization_opportunities", []):
            if opportunity == "awareness_engagement_enhancement":
                optimizations.append({
                    "type": "engagement_boost",
                    "action": "increase_visual_appeal",
                    "confidence": 0.85,
                    "expected_impact": 0.18
                })
            elif opportunity == "consideration_acceleration":
                optimizations.append({
                    "type": "comparison_enhancement",
                    "action": "add_comparison_tools",
                    "confidence": 0.80,
                    "expected_impact": 0.15
                })
            elif opportunity == "decision_friction_reduction":
                optimizations.append({
                    "type": "friction_reduction",
                    "action": "simplify_checkout_flow",
                    "confidence": 0.90,
                    "expected_impact": 0.25
                })
        
        # Add general optimizations
        if flow_analysis["flow_quality_score"] < 0.7:
            optimizations.append({
                "type": "flow_enhancement",
                "action": "optimize_navigation_flow",
                "confidence": 0.75,
                "expected_impact": 0.12
            })
        
        return sorted(optimizations, key=lambda x: x["expected_impact"], reverse=True)
    
    async def _apply_flow_optimization(self, session: JourneySession, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a specific flow optimization strategy"""
        optimization_type = strategy["type"]
        action = strategy["action"]
        
        result = {
            "type": optimization_type,
            "action": action,
            "implementation_details": {},
            "expected_impact": strategy["expected_impact"],
            "applied_at": datetime.utcnow().isoformat()
        }
        
        if optimization_type == "engagement_boost":
            result["implementation_details"] = {
                "visual_enhancements": ["hero_animation", "color_optimization"],
                "interaction_improvements": ["hover_effects", "micro_animations"]
            }
        elif optimization_type == "comparison_enhancement":
            result["implementation_details"] = {
                "comparison_tools": ["feature_table", "side_by_side_view"],
                "decision_aids": ["recommendation_engine", "best_match_highlighting"]
            }
        elif optimization_type == "friction_reduction":
            result["implementation_details"] = {
                "checkout_optimizations": ["one_click_purchase", "guest_checkout"],
                "form_improvements": ["auto_fill", "progress_indicators"]
            }
        
        return result
    
    async def _apply_abandonment_interventions(self, session: JourneySession, abandonment_probability: float) -> List[Dict[str, Any]]:
        """Apply preemptive interventions to prevent abandonment"""
        interventions = []
        
        # High-impact interventions for high abandonment risk
        if abandonment_probability > 0.8:
            # Immediate scarcity trigger
            interventions.append({
                "type": "immediate_scarcity",
                "intervention": "flash_discount_popup",
                "retention_impact": 0.3,
                "urgency": "critical"
            })
            
            # Exit-intent capture
            interventions.append({
                "type": "exit_intent_capture",
                "intervention": "exit_intent_offer",
                "retention_impact": 0.25,
                "urgency": "critical"
            })
        
        # Medium-impact interventions
        if abandonment_probability > 0.6:
            # Engagement re-activation
            interventions.append({
                "type": "engagement_reactivation",
                "intervention": "interactive_element_highlight",
                "retention_impact": 0.15,
                "urgency": "high"
            })
            
            # Social proof injection
            interventions.append({
                "type": "social_proof",
                "intervention": "live_activity_notification",
                "retention_impact": 0.12,
                "urgency": "medium"
            })
        
        return interventions
    
    async def _apply_gentle_engagement_boost(self, session: JourneySession) -> List[Dict[str, Any]]:
        """Apply gentle interventions to boost engagement"""
        return [
            {
                "type": "subtle_animation",
                "intervention": "gentle_call_to_action_pulse",
                "engagement_impact": 0.08
            },
            {
                "type": "content_refresh",
                "intervention": "dynamic_content_update",
                "engagement_impact": 0.06
            }
        ]
    
    async def _analyze_conversion_signals(self, session: JourneySession, conversion_signals: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current conversion signals and patterns"""
        signals = conversion_signals.get("signals", [])
        signal_strength = conversion_signals.get("signal_strength", 0.5)
        
        analysis = {
            "signal_count": len(signals),
            "signal_strength": signal_strength,
            "positive_signals": [s for s in signals if s.get("type") == "positive"],
            "negative_signals": [s for s in signals if s.get("type") == "negative"],
            "conversion_readiness": signal_strength > 0.7,
            "optimization_recommendations": []
        }
        
        # Generate recommendations based on signals
        if len(analysis["negative_signals"]) > len(analysis["positive_signals"]):
            analysis["optimization_recommendations"].append("address_conversion_barriers")
        
        if signal_strength < 0.4:
            analysis["optimization_recommendations"].append("boost_conversion_confidence")
        
        return analysis
    
    async def _apply_conversion_optimization(self, session: JourneySession, signal_analysis: Dict[str, Any], approach: str) -> Dict[str, Any]:
        """Apply conversion optimization based on approach"""
        optimization_result = {
            "approach": approach,
            "optimizations": [],
            "revenue_impact": 0.0
        }
        
        if approach == "aggressive_conversion_boost":
            optimization_result["optimizations"] = [
                {"type": "strong_scarcity", "impact": 0.2},
                {"type": "social_proof_injection", "impact": 0.15},
                {"type": "urgency_creation", "impact": 0.18}
            ]
            optimization_result["revenue_impact"] = 0.25
            
        elif approach == "targeted_conversion_enhancement":
            optimization_result["optimizations"] = [
                {"type": "trust_signal_enhancement", "impact": 0.12},
                {"type": "benefit_highlighting", "impact": 0.10},
                {"type": "risk_reversal", "impact": 0.08}
            ]
            optimization_result["revenue_impact"] = 0.15
            
        elif approach == "conversion_fine_tuning":
            optimization_result["optimizations"] = [
                {"type": "micro_copy_optimization", "impact": 0.05},
                {"type": "button_optimization", "impact": 0.04},
                {"type": "layout_refinement", "impact": 0.03}
            ]
            optimization_result["revenue_impact"] = 0.08
        
        return optimization_result
    
    # =============================================================================
    # UTILITY AND HELPER METHODS
    # =============================================================================
    
    async def _get_session(self, session_id: str) -> Optional[JourneySession]:
        """Get journey session by ID"""
        result = await self.db.execute(
            select(JourneySession).where(JourneySession.session_id == session_id)
        )
        return result.scalar_one_or_none()
    
    async def _get_baseline_metrics(self, persona_type: str, current_stage: str) -> Dict[str, Any]:
        """Get baseline metrics for persona and stage"""
        # Placeholder - would be calculated from historical data
        baseline_mapping = {
            "TechEarlyAdopter": {
                "engagement_score": 0.75,
                "interaction_rate": 0.4,
                "scroll_depth": 0.8
            },
            "BusinessOwner": {
                "engagement_score": 0.65,
                "interaction_rate": 0.3,
                "scroll_depth": 0.7
            },
            "StudentHustler": {
                "engagement_score": 0.8,
                "interaction_rate": 0.5,
                "scroll_depth": 0.9
            },
            "RemoteDad": {
                "engagement_score": 0.7,
                "interaction_rate": 0.35,
                "scroll_depth": 0.75
            }
        }
        
        return baseline_mapping.get(persona_type, {
            "engagement_score": 0.6,
            "interaction_rate": 0.3,
            "scroll_depth": 0.6
        })
    
    def _calculate_optimization_priority(self, current_metrics: Dict[str, Any], baseline_metrics: Dict[str, Any]) -> float:
        """Calculate optimization priority score"""
        engagement_gap = baseline_metrics.get("engagement_score", 0.6) - current_metrics.get("engagement_score", 0.5)
        interaction_gap = baseline_metrics.get("interaction_rate", 0.3) - current_metrics.get("interaction_rate", 0.2)
        
        priority_score = (engagement_gap * 0.6) + (interaction_gap * 0.4)
        return max(0.0, min(1.0, priority_score))
    
    async def _get_last_optimization_time(self, session_id: str) -> Optional[datetime]:
        """Get timestamp of last optimization for session"""
        result = await self.db.execute(
            select(OptimizationEvent.optimization_timestamp)
            .where(OptimizationEvent.session_id == session_id)
            .order_by(OptimizationEvent.optimization_timestamp.desc())
            .limit(1)
        )
        last_time = result.scalar_one_or_none()
        return last_time
    
    async def _get_optimization_count(self, session_id: str) -> int:
        """Get number of optimizations applied to session"""
        result = await self.db.execute(
            select(func.count(OptimizationEvent.id))
            .where(OptimizationEvent.session_id == session_id)
        )
        count = result.scalar_one()
        return count or 0
    
    async def _record_optimization_event(self, session: JourneySession, optimization_result: Dict[str, Any]) -> None:
        """Record optimization event for tracking"""
        optimization_event = OptimizationEvent(
            session_id=session.session_id,
            optimization_type="real_time_multi_layer",
            optimization_strategy=optimization_result.get("optimization_strategy", "unknown"),
            optimization_details=optimization_result,
            expected_impact=sum(opt.get("expected_impact", 0) for opt in optimization_result.get("optimizations", [])),
            actual_impact=0.0,  # Will be measured later
            success_metrics=optimization_result.get("expected_improvement", {}),
            metadata={
                "session_stage": session.current_stage,
                "persona_type": session.persona_type,
                "conversion_probability": session.conversion_probability
            }
        )
        
        self.db.add(optimization_event)
        await self.db.commit()
    
    def _calculate_next_monitoring_interval(self, optimization_result: Dict[str, Any]) -> int:
        """Calculate optimal next monitoring interval in seconds"""
        optimization_count = len(optimization_result.get("optimizations", []))
        
        # More optimizations = more frequent monitoring
        if optimization_count >= 3:
            return 120  # 2 minutes
        elif optimization_count >= 2:
            return 180  # 3 minutes
        else:
            return 300  # 5 minutes
    
    async def _get_expected_stage_duration(self, stage: str, persona_type: str) -> float:
        """Get expected duration for stage based on persona"""
        stage_durations = {
            "awareness": {
                "TechEarlyAdopter": 120,
                "StudentHustler": 90,
                "BusinessOwner": 300,
                "RemoteDad": 240
            },
            "consideration": {
                "TechEarlyAdopter": 300,
                "StudentHustler": 180,
                "BusinessOwner": 600,
                "RemoteDad": 450
            },
            "decision": {
                "TechEarlyAdopter": 180,
                "StudentHustler": 120,
                "BusinessOwner": 400,
                "RemoteDad": 300
            }
        }
        
        return stage_durations.get(stage, {}).get(persona_type, 300)  # Default 5 minutes
    
    async def _calculate_updated_conversion_probability(self, session: JourneySession, optimization_result: Dict[str, Any]) -> float:
        """Calculate updated conversion probability after optimization"""
        current_probability = session.conversion_probability
        optimization_impact = sum(opt.get("expected_impact", 0) for opt in optimization_result.get("optimizations", []))
        
        # Apply diminishing returns
        improvement_factor = 1 - current_probability  # Space for improvement
        actual_improvement = optimization_impact * improvement_factor * 0.7  # 70% effectiveness
        
        new_probability = min(0.95, current_probability + actual_improvement)
        return new_probability
    
    async def _update_session_conversion_probability(self, session_id: str, new_probability: float) -> None:
        """Update session conversion probability"""
        await self.db.execute(
            update(JourneySession)
            .where(JourneySession.session_id == session_id)
            .values(conversion_probability=new_probability)
        )
        await self.db.commit()
    
    async def _analyze_device_switch(self, session: JourneySession, device_switch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze device switch context"""
        return {
            "previous_device": device_switch_data.get("previous_device"),
            "new_device": device_switch_data.get("new_device"),
            "switch_context": device_switch_data.get("switch_context", "unknown"),
            "experience_score": 0.8,  # Would be calculated based on seamlessness
            "optimization_needed": device_switch_data.get("previous_device") != device_switch_data.get("new_device")
        }
    
    async def _generate_cross_device_optimizations(self, session: JourneySession, switch_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate optimizations for cross-device experience"""
        optimizations = []
        
        if switch_analysis["optimization_needed"]:
            optimizations.append({
                "type": "device_adaptation",
                "optimization": "adapt_layout_for_new_device",
                "impact": 0.15
            })
            
            optimizations.append({
                "type": "context_preservation",
                "optimization": "maintain_journey_context",
                "impact": 0.12
            })
            
            optimizations.append({
                "type": "experience_continuity",
                "optimization": "seamless_state_transfer",
                "impact": 0.10
            })
        
        return optimizations
    
    async def _apply_journey_continuity_optimization(self, session: JourneySession, device_optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply journey continuity optimizations"""
        return {
            "continuity_optimizations_applied": len(device_optimizations),
            "optimizations": device_optimizations,
            "expected_continuity_improvement": sum(opt.get("impact", 0) for opt in device_optimizations),
            "seamless_handoff_score": 0.9
        }
    
    async def _update_flow_optimization_cache(self, session: JourneySession, optimizations: List[Dict[str, Any]]) -> None:
        """Update flow optimization cache"""
        cache_key = f"flow_optimizations:{session.session_id}"
        optimization_data = {
            "session_id": session.session_id,
            "optimizations": optimizations,
            "timestamp": datetime.utcnow().isoformat(),
            "total_impact": sum(opt.get("expected_impact", 0) for opt in optimizations)
        }
        
        await self.redis_client.setex(cache_key, 1800, json.dumps(optimization_data))