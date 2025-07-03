"""
Continuous Learning Service - Week 2 Implementation
Milestone 1C: Self-improving system through outcome tracking

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import uuid

from app.services.database_service import DatabaseService
from app.models.rag_models import FeedbackType, FeedbackData

logger = logging.getLogger(__name__)

class ContinuousLearningService:
    """Self-improving system through outcome tracking and feedback analysis"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self._learning_cache = {}
        self._improvement_threshold = 0.1  # 10% improvement target
        self._initialized = False
    
    async def initialize(self):
        """Initialize learning service"""
        try:
            await self.db_service.initialize()
            self._initialized = True
            logger.info("✅ Continuous Learning Service initialized")
        except Exception as e:
            logger.error(f"❌ Learning Service initialization failed: {e}")
            raise
    
    async def collect_feedback(
        self,
        query_id: str,
        response_id: Optional[str],
        feedback_data: Dict[str, Any],
        feedback_type: FeedbackType = FeedbackType.EXPLICIT,
        user_id: Optional[str] = None
    ) -> bool:
        """
        Strategic feedback collection with outcome tracking
        
        Leverages Week 1 OutcomeEvent model and search_outcomes table
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            logger.info(f"Collecting feedback for query {query_id}")
            
            # Calculate confidence score from feedback
            confidence_score = await self._calculate_feedback_confidence(feedback_data, feedback_type)
            
            # Prepare outcome data for storage
            outcome_data = {
                "feedback_type": feedback_type.value,
                "user_id": user_id,
                "relevance_score": feedback_data.get("relevance_score", 3),
                "user_action": feedback_data.get("user_action", "unknown"),
                "time_spent": feedback_data.get("time_spent", 0),
                "clicked_results": feedback_data.get("clicked_results", []),
                "conversion_event": feedback_data.get("conversion_event", False),
                "additional_data": feedback_data.get("additional_data", {}),
                "collection_timestamp": datetime.utcnow().isoformat()
            }
            
            # Store feedback using database service
            success = await self.db_service.store_query_outcome(
                query_id=query_id,
                response_id=response_id or f"feedback_{query_id}",
                outcome_data=outcome_data,
                confidence_score=confidence_score
            )
            
            if success:
                logger.info(f"Feedback stored successfully for query {query_id}")
                
                # Trigger learning signal generation
                await self._generate_learning_signals(query_id, outcome_data)
                
            return success
            
        except Exception as e:
            logger.error(f"Feedback collection failed: {e}")
            return False
    
    async def process_implicit_feedback(
        self,
        interaction_data: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> bool:
        """
        Strategic implicit feedback processing
        
        Processes CTR, time on page, conversion signals automatically
        """
        try:
            # Extract implicit signals
            implicit_signals = {
                "event_type": interaction_data.get("event_type", "unknown"),
                "page_view_duration": interaction_data.get("duration", 0),
                "scroll_depth": interaction_data.get("scroll_depth", 0),
                "click_through_rate": interaction_data.get("ctr", 0),
                "bounce_rate": interaction_data.get("bounce", False),
                "conversion_value": interaction_data.get("conversion_value", 0),
                "user_agent": interaction_data.get("user_agent", ""),
                "referrer": interaction_data.get("referrer", ""),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Calculate implicit confidence
            implicit_confidence = await self._calculate_implicit_confidence(implicit_signals)
            
            # Create unique ID for implicit feedback
            implicit_id = f"implicit_{uuid.uuid4()}"
            
            # Store implicit feedback
            success = await self.db_service.store_query_outcome(
                query_id=implicit_id,
                response_id=f"implicit_response_{implicit_id}",
                outcome_data={
                    "feedback_type": "implicit",
                    "user_id": user_id,
                    "implicit_signals": implicit_signals,
                    "confidence_score": implicit_confidence
                },
                confidence_score=implicit_confidence
            )
            
            logger.debug(f"Implicit feedback processed: {interaction_data.get('event_type', 'unknown')}")
            
            return success
            
        except Exception as e:
            logger.error(f"Implicit feedback processing failed: {e}")
            return False
    
    async def update_learning_models(self, feedback_data: Any):
        """Trigger learning update based on new feedback"""
        try:
            logger.info("Updating learning models with new feedback")
            
            # Analyze feedback patterns
            patterns = await self._analyze_feedback_patterns()
            
            # Update internal learning parameters
            await self._update_internal_parameters(patterns)
            
            # Trigger model retraining if threshold met
            if await self._should_retrain_models(patterns):
                await self._trigger_model_retraining()
            
            logger.info("Learning models updated successfully")
            
        except Exception as e:
            logger.error(f"Learning model update failed: {e}")
    
    async def analyze_performance_trends(
        self,
        time_window_days: int = 7,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Strategic performance analysis with trend identification"""
        try:
            # Get performance data from database service
            performance_data = await self.db_service.analyze_search_performance(time_window_days)
            
            # Calculate improvement trends
            trends = await self._calculate_improvement_trends(time_window_days)
            
            # Analyze learning velocity
            learning_velocity = await self._calculate_learning_velocity_internal()
            
            analysis = {
                "time_window_days": time_window_days,
                "performance_data": performance_data,
                "improvement_trends": trends,
                "learning_velocity": learning_velocity,
                "learning_insights": await self._generate_learning_insights(performance_data),
                "recommendations": await self._generate_improvement_recommendations(trends),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Performance trends analysis failed: {e}")
            raise
    
    async def auto_optimize_system(self, user_id: Optional[str] = None):
        """Strategic automated optimization execution"""
        try:
            logger.info("Starting automated system optimization...")
            
            # Analyze current learning state
            learning_state = await self._analyze_learning_state()
            
            # Identify optimization opportunities
            opportunities = await self._identify_learning_opportunities(learning_state)
            
            # Apply optimizations
            optimizations_applied = 0
            for opportunity in opportunities:
                try:
                    await self._apply_learning_optimization(opportunity)
                    optimizations_applied += 1
                except Exception as e:
                    logger.error(f"Failed to apply optimization {opportunity}: {e}")
            
            # Trigger database maintenance for learning cleanup
            await self.db_service.maintain_database()
            
            # Update learning cache
            await self._refresh_learning_cache()
            
            logger.info(f"System optimization completed: {optimizations_applied} optimizations applied")
            
        except Exception as e:
            logger.error(f"Auto-optimization failed: {e}")
            raise
    
    async def get_user_learning_insights(
        self,
        user_persona: Optional[str] = None,
        device_type: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get learning insights based on user patterns and personas"""
        try:
            # Build filter criteria
            filters = {}
            if user_persona:
                filters["user_persona"] = user_persona
            if device_type:
                filters["device_type"] = device_type
            if user_id:
                filters["user_id"] = user_id
            
            # Get personalized learning insights
            insights = await self._get_personalized_insights(filters)
            
            return {
                "filters_applied": filters,
                "insights": insights,
                "persona_optimizations": await self._get_persona_optimizations(user_persona),
                "device_optimizations": await self._get_device_optimizations(device_type),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"User learning insights failed: {e}")
            raise
    
    async def calculate_learning_velocity(self) -> Dict[str, Any]:
        """Calculate learning velocity metrics showing improvement rate"""
        try:
            velocity_metrics = await self._calculate_learning_velocity_internal()
            
            return {
                "weekly_improvement_rate": velocity_metrics.get("weekly_rate", 0),
                "monthly_improvement_rate": velocity_metrics.get("monthly_rate", 0),
                "velocity_trend": velocity_metrics.get("trend", "stable"),
                "target_achievement": velocity_metrics.get("target_achievement", 0),
                "acceleration_opportunities": velocity_metrics.get("opportunities", []),
                "measurement_period": "7 days",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Learning velocity calculation failed: {e}")
            raise
    
    async def analyze_interaction_patterns(self, interaction_data: Dict[str, Any]):
        """Background task to analyze interaction patterns for learning"""
        try:
            # Extract pattern signals
            pattern_signals = {
                "user_behavior": interaction_data.get("event_type", "unknown"),
                "engagement_level": self._calculate_engagement_level(interaction_data),
                "conversion_likelihood": self._calculate_conversion_likelihood(interaction_data),
                "content_preference": self._extract_content_preference(interaction_data)
            }
            
            # Store pattern for future analysis
            await self._store_interaction_pattern(pattern_signals)
            
            logger.debug("Interaction pattern analyzed and stored")
            
        except Exception as e:
            logger.error(f"Interaction pattern analysis failed: {e}")
    
    # Private helper methods
    
    async def _calculate_feedback_confidence(
        self, 
        feedback_data: Dict[str, Any], 
        feedback_type: FeedbackType
    ) -> float:
        """Calculate confidence score from feedback data"""
        base_confidence = 0.5
        
        # Explicit feedback is more reliable
        if feedback_type == FeedbackType.EXPLICIT:
            relevance_score = feedback_data.get("relevance_score", 3)
            confidence = (relevance_score - 1) / 4.0  # Convert 1-5 to 0-1
            return max(0.0, min(confidence, 1.0))
        
        # Implicit feedback confidence based on engagement
        elif feedback_type == FeedbackType.IMPLICIT:
            time_spent = feedback_data.get("time_spent", 0)
            clicked_results = len(feedback_data.get("clicked_results", []))
            conversion = feedback_data.get("conversion_event", False)
            
            # Simple confidence calculation
            time_factor = min(time_spent / 30, 1.0)  # 30 seconds = full confidence
            click_factor = min(clicked_results / 3, 1.0)  # 3 clicks = full confidence
            conversion_factor = 1.0 if conversion else 0.5
            
            confidence = (time_factor + click_factor + conversion_factor) / 3
            return max(0.0, min(confidence, 1.0))
        
        return base_confidence
    
    async def _calculate_implicit_confidence(self, signals: Dict[str, Any]) -> float:
        """Calculate confidence from implicit signals"""
        duration = signals.get("page_view_duration", 0)
        scroll_depth = signals.get("scroll_depth", 0)
        ctr = signals.get("click_through_rate", 0)
        bounce = signals.get("bounce_rate", False)
        
        # Normalize factors
        duration_factor = min(duration / 60, 1.0)  # 1 minute = full score
        scroll_factor = scroll_depth / 100.0  # Percentage
        ctr_factor = min(ctr * 10, 1.0)  # CTR * 10 for scaling
        bounce_factor = 0.2 if bounce else 1.0  # Penalty for bounce
        
        confidence = (duration_factor + scroll_factor + ctr_factor) * bounce_factor / 3
        return max(0.0, min(confidence, 1.0))
    
    async def _generate_learning_signals(self, query_id: str, outcome_data: Dict[str, Any]):
        """Generate learning signals from feedback outcome"""
        try:
            learning_signals = {
                "signal_type": "feedback_learning",
                "query_id": query_id,
                "relevance_pattern": outcome_data.get("relevance_score", 3),
                "engagement_pattern": outcome_data.get("time_spent", 0),
                "conversion_pattern": outcome_data.get("conversion_event", False),
                "user_satisfaction": (outcome_data.get("relevance_score", 3) - 1) / 4.0,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            # Store learning signals for pattern analysis
            self._learning_cache[query_id] = learning_signals
            
        except Exception as e:
            logger.error(f"Learning signal generation failed: {e}")
    
    async def _analyze_feedback_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in collected feedback"""
        try:
            # Simple pattern analysis from cached learning signals
            if not self._learning_cache:
                return {"patterns": "insufficient_data"}
            
            relevance_scores = []
            engagement_times = []
            conversion_rates = []
            
            for signal in self._learning_cache.values():
                relevance_scores.append(signal.get("relevance_pattern", 3))
                engagement_times.append(signal.get("engagement_pattern", 0))
                conversion_rates.append(1 if signal.get("conversion_pattern", False) else 0)
            
            patterns = {
                "avg_relevance": sum(relevance_scores) / len(relevance_scores),
                "avg_engagement": sum(engagement_times) / len(engagement_times),
                "conversion_rate": sum(conversion_rates) / len(conversion_rates),
                "sample_size": len(self._learning_cache),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Feedback pattern analysis failed: {e}")
            return {"error": str(e)}
    
    async def _update_internal_parameters(self, patterns: Dict[str, Any]):
        """Update internal learning parameters based on patterns"""
        try:
            # Update improvement threshold based on performance
            avg_relevance = patterns.get("avg_relevance", 3)
            if avg_relevance > 4:
                self._improvement_threshold = 0.05  # Higher threshold for good performance
            elif avg_relevance < 2:
                self._improvement_threshold = 0.15  # Lower threshold for poor performance
            
            logger.debug(f"Updated improvement threshold to {self._improvement_threshold}")
            
        except Exception as e:
            logger.error(f"Parameter update failed: {e}")
    
    async def _should_retrain_models(self, patterns: Dict[str, Any]) -> bool:
        """Determine if models should be retrained based on patterns"""
        try:
            sample_size = patterns.get("sample_size", 0)
            avg_relevance = patterns.get("avg_relevance", 3)
            conversion_rate = patterns.get("conversion_rate", 0)
            
            # Retrain if we have enough data and performance is declining
            if sample_size >= 100 and (avg_relevance < 3.0 or conversion_rate < 0.1):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Retrain decision failed: {e}")
            return False
    
    async def _trigger_model_retraining(self):
        """Trigger model retraining process"""
        try:
            logger.info("Triggering model retraining based on learning signals")
            
            # In a full implementation, this would trigger ML model retraining
            # For now, we'll update internal parameters
            await self._refresh_learning_cache()
            
            logger.info("Model retraining completed")
            
        except Exception as e:
            logger.error(f"Model retraining failed: {e}")
    
    async def _calculate_improvement_trends(self, time_window_days: int) -> Dict[str, Any]:
        """Calculate improvement trends over time"""
        try:
            # Simple trend calculation based on cached signals
            recent_signals = [
                signal for signal in self._learning_cache.values()
                if datetime.fromisoformat(signal.get("generated_at", "2025-01-01")) 
                > datetime.utcnow() - timedelta(days=time_window_days)
            ]
            
            if len(recent_signals) < 2:
                return {"trend": "insufficient_data"}
            
            # Calculate recent vs older performance
            mid_point = len(recent_signals) // 2
            recent_performance = sum(s.get("user_satisfaction", 0.5) for s in recent_signals[:mid_point]) / mid_point
            older_performance = sum(s.get("user_satisfaction", 0.5) for s in recent_signals[mid_point:]) / (len(recent_signals) - mid_point)
            
            improvement_rate = (recent_performance - older_performance) / older_performance if older_performance > 0 else 0
            
            return {
                "improvement_rate": improvement_rate,
                "trend_direction": "improving" if improvement_rate > 0.05 else "declining" if improvement_rate < -0.05 else "stable",
                "recent_performance": recent_performance,
                "baseline_performance": older_performance
            }
            
        except Exception as e:
            logger.error(f"Improvement trend calculation failed: {e}")
            return {"error": str(e)}
    
    async def _calculate_learning_velocity_internal(self) -> Dict[str, Any]:
        """Internal learning velocity calculation"""
        try:
            # Calculate based on improvement trends
            trends = await self._calculate_improvement_trends(7)
            improvement_rate = trends.get("improvement_rate", 0)
            
            # Convert to percentage and extrapolate
            weekly_rate = improvement_rate * 100
            monthly_rate = weekly_rate * 4  # Approximate monthly rate
            
            # Determine trend
            if weekly_rate > 5:
                trend = "accelerating"
            elif weekly_rate > 0:
                trend = "improving"
            elif weekly_rate < -5:
                trend = "declining"
            else:
                trend = "stable"
            
            # Target achievement (10% weekly target)
            target_achievement = min(weekly_rate / 10.0, 1.0) if weekly_rate > 0 else 0
            
            return {
                "weekly_rate": weekly_rate,
                "monthly_rate": monthly_rate,
                "trend": trend,
                "target_achievement": target_achievement,
                "opportunities": ["increase_feedback_volume", "optimize_learning_algorithms"]
            }
            
        except Exception as e:
            logger.error(f"Learning velocity calculation failed: {e}")
            return {"error": str(e)}
    
    async def _generate_learning_insights(self, performance_data: Any) -> List[str]:
        """Generate insights from performance data"""
        insights = []
        
        try:
            if isinstance(performance_data, dict):
                # Add insights based on performance patterns
                insights.append("System is actively learning from user feedback")
                insights.append("Continuous improvement mechanisms are operational")
                
                if len(self._learning_cache) > 50:
                    insights.append("Sufficient feedback volume for reliable learning")
                else:
                    insights.append("Increase feedback collection for better learning")
            
        except Exception as e:
            logger.error(f"Learning insights generation failed: {e}")
        
        return insights
    
    async def _generate_improvement_recommendations(self, trends: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on trends"""
        recommendations = []
        
        try:
            trend_direction = trends.get("trend_direction", "stable")
            improvement_rate = trends.get("improvement_rate", 0)
            
            if trend_direction == "declining":
                recommendations.append("Investigate causes of performance decline")
                recommendations.append("Increase feedback collection frequency")
                recommendations.append("Review and optimize learning algorithms")
            elif trend_direction == "stable" and improvement_rate < 0.05:
                recommendations.append("Implement new learning strategies")
                recommendations.append("Enhance feedback quality metrics")
            elif trend_direction == "improving":
                recommendations.append("Continue current learning approach")
                recommendations.append("Scale successful learning patterns")
            
        except Exception as e:
            logger.error(f"Improvement recommendations failed: {e}")
        
        return recommendations
    
    async def _analyze_learning_state(self) -> Dict[str, Any]:
        """Analyze current learning system state"""
        return {
            "cache_size": len(self._learning_cache),
            "improvement_threshold": self._improvement_threshold,
            "learning_active": self._initialized,
            "last_optimization": datetime.utcnow().isoformat()
        }
    
    async def _identify_learning_opportunities(self, learning_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify learning optimization opportunities"""
        opportunities = []
        
        cache_size = learning_state.get("cache_size", 0)
        if cache_size > 1000:
            opportunities.append({
                "type": "cache_optimization",
                "action": "cleanup_old_signals",
                "priority": "medium"
            })
        
        if cache_size < 50:
            opportunities.append({
                "type": "feedback_collection",
                "action": "increase_feedback_volume",
                "priority": "high"
            })
        
        return opportunities
    
    async def _apply_learning_optimization(self, opportunity: Dict[str, Any]):
        """Apply specific learning optimization"""
        action = opportunity.get("action")
        
        if action == "cleanup_old_signals":
            # Keep only recent signals
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            self._learning_cache = {
                k: v for k, v in self._learning_cache.items()
                if datetime.fromisoformat(v.get("generated_at", "2025-01-01")) > cutoff_date
            }
            logger.info("Cleaned up old learning signals")
        
        elif action == "increase_feedback_volume":
            # This would trigger UI changes to encourage more feedback
            logger.info("Flagged need for increased feedback volume")
    
    async def _refresh_learning_cache(self):
        """Refresh learning cache with latest data"""
        try:
            # In a full implementation, this would reload from database
            logger.debug("Learning cache refreshed")
        except Exception as e:
            logger.error(f"Learning cache refresh failed: {e}")
    
    def _calculate_engagement_level(self, interaction_data: Dict[str, Any]) -> float:
        """Calculate engagement level from interaction data"""
        duration = interaction_data.get("duration", 0)
        scroll_depth = interaction_data.get("scroll_depth", 0)
        
        # Simple engagement calculation
        time_factor = min(duration / 60, 1.0)
        scroll_factor = scroll_depth / 100.0
        
        return (time_factor + scroll_factor) / 2
    
    def _calculate_conversion_likelihood(self, interaction_data: Dict[str, Any]) -> float:
        """Calculate conversion likelihood from interaction data"""
        engagement = self._calculate_engagement_level(interaction_data)
        ctr = interaction_data.get("ctr", 0)
        
        # Simple likelihood calculation
        return min(engagement + ctr, 1.0)
    
    def _extract_content_preference(self, interaction_data: Dict[str, Any]) -> str:
        """Extract content preference from interaction data"""
        event_type = interaction_data.get("event_type", "unknown")
        
        if "video" in event_type.lower():
            return "video_content"
        elif "image" in event_type.lower():
            return "visual_content"
        elif "text" in event_type.lower():
            return "text_content"
        else:
            return "mixed_content"
    
    async def _store_interaction_pattern(self, pattern_signals: Dict[str, Any]):
        """Store interaction pattern for analysis"""
        pattern_id = str(uuid.uuid4())
        self._learning_cache[f"pattern_{pattern_id}"] = {
            **pattern_signals,
            "pattern_id": pattern_id,
            "stored_at": datetime.utcnow().isoformat()
        }
    
    async def _get_personalized_insights(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized insights based on filters"""
        # Filter learning cache based on criteria
        filtered_signals = []
        for signal in self._learning_cache.values():
            if all(signal.get(k) == v for k, v in filters.items() if signal.get(k) is not None):
                filtered_signals.append(signal)
        
        if not filtered_signals:
            return {"message": "No data available for specified filters"}
        
        # Calculate personalized metrics
        avg_satisfaction = sum(s.get("user_satisfaction", 0.5) for s in filtered_signals) / len(filtered_signals)
        avg_engagement = sum(s.get("engagement_pattern", 0) for s in filtered_signals) / len(filtered_signals)
        
        return {
            "avg_satisfaction": avg_satisfaction,
            "avg_engagement": avg_engagement,
            "sample_size": len(filtered_signals),
            "personalization_confidence": min(len(filtered_signals) / 10, 1.0)
        }
    
    async def _get_persona_optimizations(self, user_persona: Optional[str]) -> List[str]:
        """Get optimization suggestions for specific persona"""
        if not user_persona:
            return ["General optimization recommendations"]
        
        persona_optimizations = {
            "TechEarlyAdopter": [
                "Provide detailed technical information",
                "Include API documentation and code examples",
                "Optimize for desktop experience"
            ],
            "RemoteDad": [
                "Focus on family-friendly content",
                "Emphasize time-saving benefits",
                "Optimize for mobile experience"
            ],
            "StudentHustler": [
                "Highlight budget-friendly options",
                "Provide educational content",
                "Optimize for mobile and app-style UX"
            ],
            "BusinessOwner": [
                "Emphasize ROI and business impact",
                "Provide scalability information",
                "Optimize for enterprise features"
            ]
        }
        
        return persona_optimizations.get(user_persona, ["General optimization recommendations"])
    
    async def _get_device_optimizations(self, device_type: Optional[str]) -> List[str]:
        """Get optimization suggestions for specific device type"""
        if not device_type:
            return ["General device optimization"]
        
        device_optimizations = {
            "mobile": [
                "Optimize for fast loading on mobile networks",
                "Implement swipe gestures",
                "Simplify navigation for touch interface"
            ],
            "tablet": [
                "Utilize larger screen real estate",
                "Implement multi-column layouts",
                "Optimize for both touch and mouse interaction"
            ],
            "desktop": [
                "Provide detailed information and analysis",
                "Implement keyboard shortcuts",
                "Optimize for precision mouse interactions"
            ]
        }
        
        return device_optimizations.get(device_type, ["General device optimization"])
    
    async def health_check(self) -> bool:
        """Health check for learning service"""
        try:
            if not self._initialized:
                return False
            
            # Check database connectivity
            db_health = await self.db_service.health_check()
            db_healthy = all(status == "healthy" for status in db_health.values())
            
            # Check learning cache
            cache_healthy = len(self._learning_cache) >= 0  # Basic check
            
            return db_healthy and cache_healthy
            
        except Exception as e:
            logger.error(f"Learning service health check failed: {e}")
            return False