# Performance Monitoring and Analytics for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from statistics import mean, median, stdev
from collections import defaultdict
import numpy as np

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import *
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# PERFORMANCE ANALYTICS ENGINE
# =============================================================================

class PerformanceAnalyticsEngine:
    """Advanced performance monitoring and analytics for journey systems"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        
        # Analytics configuration
        self.analytics_config = {
            "real_time_window": 300,      # 5 minutes for real-time metrics
            "short_term_window": 3600,    # 1 hour for short-term trends
            "medium_term_window": 86400,  # 24 hours for daily analytics
            "long_term_window": 604800,   # 7 days for weekly analytics
            "performance_thresholds": {
                "session_duration_target": 420,    # 7 minutes
                "conversion_rate_target": 0.15,    # 15%
                "engagement_score_target": 0.75,   # 75%
                "optimization_success_target": 0.85 # 85%
            }
        }
    
    async def get_real_time_performance_metrics(self, time_window_minutes: int = 5) -> Dict[str, Any]:
        """Get real-time performance metrics for the last N minutes"""
        try:
            logger.debug(f"Getting real-time performance metrics for last {time_window_minutes} minutes")
            
            since = datetime.utcnow() - timedelta(minutes=time_window_minutes)
            
            # Get real-time session metrics
            session_metrics = await self._get_real_time_session_metrics(since)
            
            # Get real-time conversion metrics
            conversion_metrics = await self._get_real_time_conversion_metrics(since)
            
            # Get real-time optimization metrics
            optimization_metrics = await self._get_real_time_optimization_metrics(since)
            
            # Get real-time personalization metrics
            personalization_metrics = await self._get_real_time_personalization_metrics(since)
            
            # Calculate system health scores
            system_health = await self._calculate_system_health_scores(
                session_metrics, conversion_metrics, optimization_metrics, personalization_metrics
            )
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "time_window_minutes": time_window_minutes,
                "session_metrics": session_metrics,
                "conversion_metrics": conversion_metrics,
                "optimization_metrics": optimization_metrics,
                "personalization_metrics": personalization_metrics,
                "system_health": system_health,
                "alerts": await self._generate_real_time_alerts(system_health)
            }
            
        except Exception as e:
            logger.error(f"Error getting real-time performance metrics: {str(e)}")
            return {"error": str(e)}
    
    async def get_journey_funnel_analytics(self, time_range: str = "24h", persona_filter: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive journey funnel analytics"""
        try:
            logger.debug(f"Getting journey funnel analytics for {time_range}")
            
            since = self._parse_time_range(time_range)
            
            # Get funnel conversion rates
            funnel_data = await self._calculate_funnel_conversion_rates(since, persona_filter)
            
            # Get stage performance metrics
            stage_performance = await self._calculate_stage_performance_metrics(since, persona_filter)
            
            # Get journey path analytics
            journey_path_analytics = await self._analyze_journey_paths(since, persona_filter)
            
            # Get drop-off analysis
            dropoff_analysis = await self._analyze_journey_dropoffs(since, persona_filter)
            
            # Get persona performance comparison
            persona_performance = await self._compare_persona_performance(since)
            
            return {
                "time_range": time_range,
                "persona_filter": persona_filter,
                "funnel_data": funnel_data,
                "stage_performance": stage_performance,
                "journey_path_analytics": journey_path_analytics,
                "dropoff_analysis": dropoff_analysis,
                "persona_performance": persona_performance,
                "recommendations": await self._generate_funnel_recommendations(funnel_data, stage_performance)
            }
            
        except Exception as e:
            logger.error(f"Error getting journey funnel analytics: {str(e)}")
            return {"error": str(e)}
    
    async def get_optimization_effectiveness_analytics(self, time_range: str = "7d") -> Dict[str, Any]:
        """Get comprehensive optimization effectiveness analytics"""
        try:
            logger.debug(f"Getting optimization effectiveness analytics for {time_range}")
            
            since = self._parse_time_range(time_range)
            
            # Get optimization performance by type
            optimization_performance = await self._analyze_optimization_performance(since)
            
            # Get A/B test results
            ab_test_results = await self._analyze_ab_test_performance(since)
            
            # Get personalization effectiveness
            personalization_effectiveness = await self._analyze_personalization_effectiveness(since)
            
            # Get scarcity trigger effectiveness
            scarcity_effectiveness = await self._analyze_scarcity_effectiveness(since)
            
            # Get ROI analysis
            roi_analysis = await self._calculate_optimization_roi(since)
            
            # Get trend analysis
            trend_analysis = await self._analyze_optimization_trends(since)
            
            return {
                "time_range": time_range,
                "optimization_performance": optimization_performance,
                "ab_test_results": ab_test_results,
                "personalization_effectiveness": personalization_effectiveness,
                "scarcity_effectiveness": scarcity_effectiveness,
                "roi_analysis": roi_analysis,
                "trend_analysis": trend_analysis,
                "optimization_recommendations": await self._generate_optimization_recommendations(optimization_performance)
            }
            
        except Exception as e:
            logger.error(f"Error getting optimization effectiveness analytics: {str(e)}")
            return {"error": str(e)}
    
    async def get_cross_device_analytics(self, time_range: str = "7d") -> Dict[str, Any]:
        """Get cross-device journey analytics"""
        try:
            logger.debug(f"Getting cross-device analytics for {time_range}")
            
            since = self._parse_time_range(time_range)
            
            # Get cross-device session statistics
            cross_device_stats = await self._analyze_cross_device_sessions(since)
            
            # Get device switching patterns
            device_switching = await self._analyze_device_switching_patterns(since)
            
            # Get cross-device conversion analysis
            cross_device_conversions = await self._analyze_cross_device_conversions(since)
            
            # Get continuity effectiveness
            continuity_effectiveness = await self._analyze_journey_continuity(since)
            
            return {
                "time_range": time_range,
                "cross_device_stats": cross_device_stats,
                "device_switching": device_switching,
                "cross_device_conversions": cross_device_conversions,
                "continuity_effectiveness": continuity_effectiveness,
                "cross_device_recommendations": await self._generate_cross_device_recommendations(cross_device_stats)
            }
            
        except Exception as e:
            logger.error(f"Error getting cross-device analytics: {str(e)}")
            return {"error": str(e)}
    
    async def generate_performance_report(self, report_type: str = "comprehensive", time_range: str = "7d") -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            logger.info(f"Generating {report_type} performance report for {time_range}")
            
            # Get all analytics components
            tasks = [
                self.get_real_time_performance_metrics(5),
                self.get_journey_funnel_analytics(time_range),
                self.get_optimization_effectiveness_analytics(time_range),
                self.get_cross_device_analytics(time_range)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            real_time_metrics = results[0] if not isinstance(results[0], Exception) else {}
            funnel_analytics = results[1] if not isinstance(results[1], Exception) else {}
            optimization_analytics = results[2] if not isinstance(results[2], Exception) else {}
            cross_device_analytics = results[3] if not isinstance(results[3], Exception) else {}
            
            # Generate executive summary
            executive_summary = await self._generate_executive_summary(
                real_time_metrics, funnel_analytics, optimization_analytics, cross_device_analytics
            )
            
            # Generate strategic recommendations
            strategic_recommendations = await self._generate_strategic_recommendations(
                funnel_analytics, optimization_analytics, cross_device_analytics
            )
            
            return {
                "report_type": report_type,
                "time_range": time_range,
                "generated_at": datetime.utcnow().isoformat(),
                "executive_summary": executive_summary,
                "real_time_metrics": real_time_metrics,
                "funnel_analytics": funnel_analytics,
                "optimization_analytics": optimization_analytics,
                "cross_device_analytics": cross_device_analytics,
                "strategic_recommendations": strategic_recommendations,
                "next_review_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating performance report: {str(e)}")
            return {"error": str(e)}
    
    # =============================================================================
    # REAL-TIME METRICS METHODS
    # =============================================================================
    
    async def _get_real_time_session_metrics(self, since: datetime) -> Dict[str, Any]:
        """Get real-time session metrics"""
        # Active sessions
        active_sessions_result = await self.db.execute(
            select(func.count(JourneySession.id))
            .where(
                and_(
                    JourneySession.start_timestamp >= since,
                    JourneySession.end_timestamp.is_(None)
                )
            )
        )
        active_sessions = active_sessions_result.scalar() or 0
        
        # New sessions
        new_sessions_result = await self.db.execute(
            select(func.count(JourneySession.id))
            .where(JourneySession.start_timestamp >= since)
        )
        new_sessions = new_sessions_result.scalar() or 0
        
        # Average session duration
        duration_result = await self.db.execute(
            select(func.avg(JourneySession.total_session_time))
            .where(
                and_(
                    JourneySession.start_timestamp >= since,
                    JourneySession.end_timestamp.is_not(None)
                )
            )
        )
        avg_duration = duration_result.scalar() or 0
        
        # Conversion probability distribution
        conversion_dist_result = await self.db.execute(
            select(func.avg(JourneySession.conversion_probability))
            .where(JourneySession.start_timestamp >= since)
        )
        avg_conversion_probability = conversion_dist_result.scalar() or 0
        
        return {
            "active_sessions": active_sessions,
            "new_sessions": new_sessions,
            "average_session_duration": round(avg_duration, 2),
            "average_conversion_probability": round(avg_conversion_probability, 4),
            "sessions_per_minute": round(new_sessions / 5, 2) if new_sessions > 0 else 0
        }
    
    async def _get_real_time_conversion_metrics(self, since: datetime) -> Dict[str, Any]:
        """Get real-time conversion metrics"""
        # Total conversions
        conversions_result = await self.db.execute(
            select(func.count(ConversionEvent.id))
            .where(ConversionEvent.conversion_timestamp >= since)
        )
        total_conversions = conversions_result.scalar() or 0
        
        # Conversion rate
        total_sessions_result = await self.db.execute(
            select(func.count(JourneySession.id))
            .where(JourneySession.start_timestamp >= since)
        )
        total_sessions = total_sessions_result.scalar() or 1
        
        conversion_rate = total_conversions / total_sessions if total_sessions > 0 else 0
        
        # Revenue
        revenue_result = await self.db.execute(
            select(func.sum(ConversionEvent.conversion_value))
            .where(ConversionEvent.conversion_timestamp >= since)
        )
        total_revenue = revenue_result.scalar() or 0
        
        return {
            "total_conversions": total_conversions,
            "conversion_rate": round(conversion_rate, 4),
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(total_revenue / total_conversions, 2) if total_conversions > 0 else 0,
            "conversions_per_minute": round(total_conversions / 5, 2)
        }
    
    async def _get_real_time_optimization_metrics(self, since: datetime) -> Dict[str, Any]:
        """Get real-time optimization metrics"""
        # Total optimizations
        optimizations_result = await self.db.execute(
            select(func.count(OptimizationEvent.id))
            .where(OptimizationEvent.optimization_timestamp >= since)
        )
        total_optimizations = optimizations_result.scalar() or 0
        
        # Successful optimizations
        successful_result = await self.db.execute(
            select(func.count(OptimizationEvent.id))
            .where(
                and_(
                    OptimizationEvent.optimization_timestamp >= since,
                    OptimizationEvent.optimization_success == True
                )
            )
        )
        successful_optimizations = successful_result.scalar() or 0
        
        success_rate = successful_optimizations / total_optimizations if total_optimizations > 0 else 0
        
        # Average impact
        impact_result = await self.db.execute(
            select(func.avg(OptimizationEvent.expected_impact))
            .where(OptimizationEvent.optimization_timestamp >= since)
        )
        avg_impact = impact_result.scalar() or 0
        
        return {
            "total_optimizations": total_optimizations,
            "successful_optimizations": successful_optimizations,
            "success_rate": round(success_rate, 4),
            "average_expected_impact": round(avg_impact, 4),
            "optimizations_per_minute": round(total_optimizations / 5, 2)
        }
    
    async def _get_real_time_personalization_metrics(self, since: datetime) -> Dict[str, Any]:
        """Get real-time personalization metrics"""
        # Total personalizations
        personalizations_result = await self.db.execute(
            select(func.count(PersonalizationData.id))
            .where(PersonalizationData.applied_timestamp >= since)
        )
        total_personalizations = personalizations_result.scalar() or 0
        
        # Conversion attributed
        conversions_result = await self.db.execute(
            select(func.count(PersonalizationData.id))
            .where(
                and_(
                    PersonalizationData.applied_timestamp >= since,
                    PersonalizationData.conversion_attributed == True
                )
            )
        )
        conversions_attributed = conversions_result.scalar() or 0
        
        attribution_rate = conversions_attributed / total_personalizations if total_personalizations > 0 else 0
        
        # Average confidence
        confidence_result = await self.db.execute(
            select(func.avg(PersonalizationData.confidence_score))
            .where(PersonalizationData.applied_timestamp >= since)
        )
        avg_confidence = confidence_result.scalar() or 0
        
        return {
            "total_personalizations": total_personalizations,
            "conversions_attributed": conversions_attributed,
            "attribution_rate": round(attribution_rate, 4),
            "average_confidence": round(avg_confidence, 4),
            "personalizations_per_minute": round(total_personalizations / 5, 2)
        }
    
    # =============================================================================
    # ANALYTICS CALCULATION METHODS
    # =============================================================================
    
    async def _calculate_funnel_conversion_rates(self, since: datetime, persona_filter: Optional[str]) -> Dict[str, Any]:
        """Calculate journey funnel conversion rates"""
        # Build base query
        base_query = select(
            JourneySession.current_stage,
            func.count(JourneySession.id).label("session_count")
        ).where(JourneySession.start_timestamp >= since)
        
        if persona_filter:
            base_query = base_query.where(JourneySession.persona_type == persona_filter)
        
        base_query = base_query.group_by(JourneySession.current_stage)
        
        stage_counts_result = await self.db.execute(base_query)
        stage_counts = dict(stage_counts_result.fetchall())
        
        # Calculate conversion rates between stages
        stages = ["awareness", "consideration", "decision", "conversion"]
        funnel_data = {}
        
        for i in range(len(stages) - 1):
            current_stage = stages[i]
            next_stage = stages[i + 1]
            
            current_count = stage_counts.get(current_stage, 0)
            next_count = stage_counts.get(next_stage, 0)
            
            conversion_rate = next_count / current_count if current_count > 0 else 0
            
            funnel_data[f"{current_stage}_to_{next_stage}"] = {
                "current_stage_count": current_count,
                "next_stage_count": next_count,
                "conversion_rate": round(conversion_rate, 4)
            }
        
        # Overall funnel efficiency
        total_awareness = stage_counts.get("awareness", 0)
        total_conversions = stage_counts.get("conversion", 0)
        overall_conversion_rate = total_conversions / total_awareness if total_awareness > 0 else 0
        
        funnel_data["overall"] = {
            "total_entries": total_awareness,
            "total_conversions": total_conversions,
            "overall_conversion_rate": round(overall_conversion_rate, 4)
        }
        
        return funnel_data
    
    async def _calculate_stage_performance_metrics(self, since: datetime, persona_filter: Optional[str]) -> Dict[str, Any]:
        """Calculate performance metrics for each journey stage"""
        stages = ["awareness", "consideration", "decision", "conversion"]
        stage_performance = {}
        
        for stage in stages:
            # Build query for stage
            query = select(
                func.count(JourneySession.id).label("session_count"),
                func.avg(JourneySession.total_session_time).label("avg_duration"),
                func.avg(JourneySession.conversion_probability).label("avg_conversion_prob"),
                func.avg(JourneySession.total_touchpoints).label("avg_touchpoints")
            ).where(
                and_(
                    JourneySession.current_stage == stage,
                    JourneySession.start_timestamp >= since
                )
            )
            
            if persona_filter:
                query = query.where(JourneySession.persona_type == persona_filter)
            
            result = await self.db.execute(query)
            metrics = result.fetchone()
            
            stage_performance[stage] = {
                "session_count": metrics.session_count or 0,
                "average_duration": round(metrics.avg_duration or 0, 2),
                "average_conversion_probability": round(metrics.avg_conversion_prob or 0, 4),
                "average_touchpoints": round(metrics.avg_touchpoints or 0, 2)
            }
        
        return stage_performance
    
    async def _analyze_journey_paths(self, since: datetime, persona_filter: Optional[str]) -> Dict[str, Any]:
        """Analyze journey path performance"""
        query = select(
            JourneySession.journey_path,
            func.count(JourneySession.id).label("session_count"),
            func.avg(JourneySession.conversion_probability).label("avg_conversion_prob"),
            func.avg(JourneySession.total_session_time).label("avg_duration")
        ).where(JourneySession.start_timestamp >= since)
        
        if persona_filter:
            query = query.where(JourneySession.persona_type == persona_filter)
        
        query = query.group_by(JourneySession.journey_path).order_by(func.count(JourneySession.id).desc())
        
        result = await self.db.execute(query)
        paths = result.fetchall()
        
        journey_paths = []
        for path in paths:
            journey_paths.append({
                "path": path.journey_path,
                "session_count": path.session_count,
                "average_conversion_probability": round(path.avg_conversion_prob or 0, 4),
                "average_duration": round(path.avg_duration or 0, 2)
            })
        
        return {
            "top_paths": journey_paths[:10],
            "total_unique_paths": len(journey_paths)
        }
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _parse_time_range(self, time_range: str) -> datetime:
        """Parse time range string to datetime"""
        time_mapping = {
            "1h": timedelta(hours=1),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
            "90d": timedelta(days=90)
        }
        
        delta = time_mapping.get(time_range, timedelta(hours=24))
        return datetime.utcnow() - delta
    
    async def _calculate_system_health_scores(self, session_metrics: Dict, conversion_metrics: Dict,
                                            optimization_metrics: Dict, personalization_metrics: Dict) -> Dict[str, Any]:
        """Calculate overall system health scores"""
        targets = self.analytics_config["performance_thresholds"]
        
        # Session health score
        session_score = min(1.0, session_metrics.get("average_session_duration", 0) / targets["session_duration_target"])
        
        # Conversion health score
        conversion_score = min(1.0, conversion_metrics.get("conversion_rate", 0) / targets["conversion_rate_target"])
        
        # Optimization health score
        optimization_score = min(1.0, optimization_metrics.get("success_rate", 0) / targets["optimization_success_target"])
        
        # Overall system health
        overall_health = mean([session_score, conversion_score, optimization_score])
        
        return {
            "session_health_score": round(session_score, 3),
            "conversion_health_score": round(conversion_score, 3),
            "optimization_health_score": round(optimization_score, 3),
            "overall_system_health": round(overall_health, 3),
            "health_status": self._get_health_status(overall_health)
        }
    
    def _get_health_status(self, health_score: float) -> str:
        """Get health status based on score"""
        if health_score >= 0.9:
            return "excellent"
        elif health_score >= 0.8:
            return "good"
        elif health_score >= 0.7:
            return "fair"
        elif health_score >= 0.6:
            return "poor"
        else:
            return "critical"
    
    async def _generate_real_time_alerts(self, system_health: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate real-time alerts based on system health"""
        alerts = []
        
        if system_health["overall_system_health"] < 0.7:
            alerts.append({
                "type": "system_health",
                "severity": "high",
                "message": "Overall system health below acceptable threshold",
                "threshold": 0.7,
                "current_value": system_health["overall_system_health"]
            })
        
        if system_health["conversion_health_score"] < 0.6:
            alerts.append({
                "type": "conversion_performance",
                "severity": "medium",
                "message": "Conversion performance significantly below target",
                "threshold": 0.6,
                "current_value": system_health["conversion_health_score"]
            })
        
        return alerts
    
    # Placeholder methods for comprehensive analytics
    async def _analyze_journey_dropoffs(self, since: datetime, persona_filter: Optional[str]) -> Dict[str, Any]:
        """Analyze journey drop-off points"""
        return {"dropoff_analysis": "placeholder"}
    
    async def _compare_persona_performance(self, since: datetime) -> Dict[str, Any]:
        """Compare performance across personas"""
        return {"persona_comparison": "placeholder"}
    
    async def _analyze_optimization_performance(self, since: datetime) -> Dict[str, Any]:
        """Analyze optimization performance by type"""
        return {"optimization_performance": "placeholder"}
    
    async def _analyze_ab_test_performance(self, since: datetime) -> Dict[str, Any]:
        """Analyze A/B test results"""
        return {"ab_test_results": "placeholder"}
    
    async def _analyze_personalization_effectiveness(self, since: datetime) -> Dict[str, Any]:
        """Analyze personalization effectiveness"""
        return {"personalization_effectiveness": "placeholder"}
    
    async def _analyze_scarcity_effectiveness(self, since: datetime) -> Dict[str, Any]:
        """Analyze scarcity trigger effectiveness"""
        return {"scarcity_effectiveness": "placeholder"}
    
    async def _calculate_optimization_roi(self, since: datetime) -> Dict[str, Any]:
        """Calculate ROI for optimizations"""
        return {"roi_analysis": "placeholder"}
    
    async def _analyze_optimization_trends(self, since: datetime) -> Dict[str, Any]:
        """Analyze optimization trends over time"""
        return {"trend_analysis": "placeholder"}
    
    async def _analyze_cross_device_sessions(self, since: datetime) -> Dict[str, Any]:
        """Analyze cross-device session patterns"""
        return {"cross_device_stats": "placeholder"}
    
    async def _analyze_device_switching_patterns(self, since: datetime) -> Dict[str, Any]:
        """Analyze device switching patterns"""
        return {"device_switching": "placeholder"}
    
    async def _analyze_cross_device_conversions(self, since: datetime) -> Dict[str, Any]:
        """Analyze cross-device conversions"""
        return {"cross_device_conversions": "placeholder"}
    
    async def _analyze_journey_continuity(self, since: datetime) -> Dict[str, Any]:
        """Analyze journey continuity effectiveness"""
        return {"continuity_effectiveness": "placeholder"}
    
    async def _generate_funnel_recommendations(self, funnel_data: Dict, stage_performance: Dict) -> List[Dict[str, Any]]:
        """Generate funnel optimization recommendations"""
        return [{"recommendation": "placeholder"}]
    
    async def _generate_optimization_recommendations(self, optimization_performance: Dict) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        return [{"recommendation": "placeholder"}]
    
    async def _generate_cross_device_recommendations(self, cross_device_stats: Dict) -> List[Dict[str, Any]]:
        """Generate cross-device recommendations"""
        return [{"recommendation": "placeholder"}]
    
    async def _generate_executive_summary(self, real_time_metrics: Dict, funnel_analytics: Dict,
                                        optimization_analytics: Dict, cross_device_analytics: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        return {
            "key_metrics": {
                "active_sessions": real_time_metrics.get("session_metrics", {}).get("active_sessions", 0),
                "conversion_rate": real_time_metrics.get("conversion_metrics", {}).get("conversion_rate", 0),
                "system_health": real_time_metrics.get("system_health", {}).get("overall_system_health", 0)
            },
            "summary": "System performing within acceptable parameters"
        }
    
    async def _generate_strategic_recommendations(self, funnel_analytics: Dict, optimization_analytics: Dict,
                                                cross_device_analytics: Dict) -> List[Dict[str, Any]]:
        """Generate strategic recommendations"""
        return [
            {
                "category": "optimization",
                "recommendation": "Increase real-time optimization frequency for high-value sessions",
                "priority": "high",
                "expected_impact": 0.15
            },
            {
                "category": "personalization",
                "recommendation": "Enhance personalization strategies for mobile users",
                "priority": "medium",
                "expected_impact": 0.12
            }
        ]