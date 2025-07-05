# A/B Testing Dashboard and Analytics - Week 3 Implementation
# Module: 3A - Week 3 - Comprehensive A/B Testing Dashboard and Analytics
# Created: 2025-07-05

import asyncio
import json
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_

from .models import *
from .database_models import JourneySession, PersonalizationData
from .ab_testing_framework import (
    ABTestingFramework, ABTest, ABTestVariant, TestStatus, TestType, OptimizationGoal
)
from .ab_testing_integration import ABTestingPersonalizationEngine
from .real_time_optimization_engine import RealTimeOptimizationEngine
from .cross_test_learning_engine import CrossTestLearningEngine
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# DASHBOARD MODELS AND ENUMS
# =============================================================================

class DashboardView(Enum):
    OVERVIEW = "overview"
    TEST_DETAILS = "test_details"
    PERFORMANCE_ANALYTICS = "performance_analytics"
    OPTIMIZATION_INSIGHTS = "optimization_insights"
    LEARNING_INTELLIGENCE = "learning_intelligence"

class MetricType(Enum):
    CONVERSION_RATE = "conversion_rate"
    CLICK_THROUGH_RATE = "click_through_rate"
    ENGAGEMENT_TIME = "engagement_time"
    BOUNCE_RATE = "bounce_rate"
    REVENUE_PER_VISITOR = "revenue_per_visitor"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class DashboardAlert:
    """Dashboard alert for important events"""
    alert_id: str
    test_id: str
    test_name: str
    severity: AlertSeverity
    message: str
    details: Dict[str, Any]
    action_required: bool
    suggested_actions: List[str]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

@dataclass
class PerformanceSnapshot:
    """Performance snapshot for dashboard"""
    timestamp: datetime
    test_id: str
    variant_id: str
    metrics: Dict[str, float]
    traffic_volume: int
    optimization_score: float

@dataclass
class DashboardSummary:
    """High-level dashboard summary"""
    total_active_tests: int
    total_completed_tests: int
    avg_conversion_rate: float
    total_sessions_today: int
    active_optimizations: int
    alerts_count: int
    top_performer: Dict[str, Any]
    bottom_performer: Dict[str, Any]
    system_health_score: float

# =============================================================================
# A/B TESTING DASHBOARD ENGINE
# =============================================================================

class ABTestingDashboard:
    """Comprehensive A/B testing dashboard and analytics system"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        
        # Initialize component engines
        self.ab_testing_framework = ABTestingFramework(db)
        self.personalization_engine = ABTestingPersonalizationEngine(db)
        self.optimization_engine = RealTimeOptimizationEngine(db)
        self.learning_engine = CrossTestLearningEngine(db)
        
        # Dashboard configuration
        self.refresh_interval = 60  # seconds
        self.alert_retention_days = 30
        self.performance_history_days = 90
        
        # Analytics configuration
        self.analytics_batch_size = 1000
        self.real_time_window_minutes = 15
        
    async def get_dashboard_overview(self, time_range: str = "24h") -> Dict[str, Any]:
        """Get comprehensive dashboard overview"""
        try:
            logger.info(f"Getting dashboard overview for time range: {time_range}")
            
            # Get dashboard summary
            summary = await self._get_dashboard_summary(time_range)
            
            # Get active tests overview
            active_tests = await self._get_active_tests_overview()
            
            # Get performance trends
            performance_trends = await self._get_performance_trends(time_range)
            
            # Get recent optimizations
            recent_optimizations = await self._get_recent_optimizations(time_range)
            
            # Get active alerts
            active_alerts = await self._get_active_alerts()
            
            # Get learning insights summary
            learning_insights = await self._get_learning_insights_summary()
            
            # Calculate real-time metrics
            real_time_metrics = await self._get_real_time_metrics()
            
            return {
                'overview': {
                    'summary': asdict(summary),
                    'real_time_metrics': real_time_metrics,
                    'system_status': await self._get_system_status()
                },
                'active_tests': active_tests,
                'performance_trends': performance_trends,
                'recent_optimizations': recent_optimizations,
                'alerts': [asdict(alert) for alert in active_alerts],
                'learning_insights': learning_insights,
                'last_updated': datetime.utcnow().isoformat(),
                'refresh_interval': self.refresh_interval
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard overview: {str(e)}")
            return {'error': str(e)}
    
    async def get_test_detailed_analytics(self, test_id: str) -> Dict[str, Any]:
        """Get detailed analytics for a specific test"""
        try:
            logger.info(f"Getting detailed analytics for test: {test_id}")
            
            # Get test configuration and current status
            test_config = await self._get_test_configuration(test_id)
            if not test_config:
                return {'error': 'Test not found'}
            
            # Get variant performance details
            variant_analytics = await self._get_variant_detailed_analytics(test_id)
            
            # Get statistical analysis
            statistical_analysis = await self._get_statistical_analysis(test_id)
            
            # Get performance timeline
            performance_timeline = await self._get_performance_timeline(test_id)
            
            # Get device and persona breakdowns
            device_breakdown = await self._get_device_breakdown(test_id)
            persona_breakdown = await self._get_persona_breakdown(test_id)
            
            # Get optimization history
            optimization_history = await self._get_optimization_history(test_id)
            
            # Get predictions and recommendations
            predictions = await self._get_test_predictions(test_id)
            
            # Get interaction heatmaps
            interaction_data = await self._get_interaction_heatmaps(test_id)
            
            return {
                'test_configuration': test_config,
                'variant_analytics': variant_analytics,
                'statistical_analysis': statistical_analysis,
                'performance_timeline': performance_timeline,
                'breakdowns': {
                    'device_breakdown': device_breakdown,
                    'persona_breakdown': persona_breakdown
                },
                'optimization_history': optimization_history,
                'predictions': predictions,
                'interaction_data': interaction_data,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting test detailed analytics: {str(e)}")
            return {'error': str(e)}
    
    async def get_performance_analytics(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get comprehensive performance analytics across all tests"""
        try:
            logger.info("Getting comprehensive performance analytics")
            
            # Apply filters
            time_range = filters.get('time_range', '30d') if filters else '30d'
            test_types = filters.get('test_types', []) if filters else []
            device_types = filters.get('device_types', []) if filters else []
            persona_types = filters.get('persona_types', []) if filters else []
            
            # Get aggregated performance metrics
            aggregated_metrics = await self._get_aggregated_performance_metrics(
                time_range, test_types, device_types, persona_types
            )
            
            # Get conversion funnel analysis
            funnel_analysis = await self._get_conversion_funnel_analysis(filters)
            
            # Get comparative analysis
            comparative_analysis = await self._get_comparative_analysis(filters)
            
            # Get performance distribution
            performance_distribution = await self._get_performance_distribution(filters)
            
            # Get optimization impact analysis
            optimization_impact = await self._get_optimization_impact_analysis(filters)
            
            # Get trending insights
            trending_insights = await self._get_trending_insights(filters)
            
            return {
                'aggregated_metrics': aggregated_metrics,
                'funnel_analysis': funnel_analysis,
                'comparative_analysis': comparative_analysis,
                'performance_distribution': performance_distribution,
                'optimization_impact': optimization_impact,
                'trending_insights': trending_insights,
                'filters_applied': filters or {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance analytics: {str(e)}")
            return {'error': str(e)}
    
    async def create_custom_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom analytics report"""
        try:
            logger.info(f"Creating custom report: {report_config.get('report_name', 'unnamed')}")
            
            report_id = f"report_{datetime.utcnow().timestamp()}"
            
            # Get data based on report configuration
            report_data = {}
            
            for section in report_config.get('sections', []):
                section_type = section.get('type')
                section_filters = section.get('filters', {})
                
                if section_type == 'test_performance':
                    report_data[section['name']] = await self._get_test_performance_data(section_filters)
                elif section_type == 'optimization_analysis':
                    report_data[section['name']] = await self._get_optimization_analysis_data(section_filters)
                elif section_type == 'learning_insights':
                    report_data[section['name']] = await self._get_learning_insights_data(section_filters)
                elif section_type == 'comparative_metrics':
                    report_data[section['name']] = await self._get_comparative_metrics_data(section_filters)
            
            # Generate insights and recommendations
            insights = await self._generate_report_insights(report_data, report_config)
            
            # Create report summary
            report_summary = await self._create_report_summary(report_data, insights)
            
            # Store report for future access
            await self._store_custom_report(report_id, report_config, report_data, insights)
            
            return {
                'report_id': report_id,
                'report_name': report_config.get('report_name', 'Custom Report'),
                'summary': report_summary,
                'data': report_data,
                'insights': insights,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating custom report: {str(e)}")
            return {'error': str(e)}

    # =============================================================================
    # REAL-TIME MONITORING AND ALERTS
    # =============================================================================

    async def start_real_time_monitoring(self) -> Dict[str, Any]:
        """Start real-time monitoring for dashboard"""
        try:
            logger.info("Starting real-time dashboard monitoring")
            
            # Initialize monitoring configuration
            monitoring_config = {
                'started_at': datetime.utcnow().isoformat(),
                'refresh_interval': self.refresh_interval,
                'alert_thresholds': await self._get_alert_thresholds(),
                'monitored_metrics': [metric.value for metric in MetricType],
                'status': 'active'
            }
            
            # Store monitoring configuration
            await self.redis_client.setex(
                'dashboard_monitoring_config',
                86400,
                json.dumps(monitoring_config)
            )
            
            # Schedule monitoring tasks
            await self._schedule_performance_monitoring()
            await self._schedule_alert_monitoring()
            await self._schedule_optimization_monitoring()
            
            return {
                'status': 'monitoring_started',
                'refresh_interval': self.refresh_interval,
                'monitored_metrics': monitoring_config['monitored_metrics'],
                'alert_system': 'active'
            }
            
        except Exception as e:
            logger.error(f"Error starting real-time monitoring: {str(e)}")
            return {'error': str(e)}
    
    async def check_and_generate_alerts(self) -> List[DashboardAlert]:
        """Check system status and generate alerts if needed"""
        try:
            alerts = []
            
            # Check for statistical significance alerts
            significance_alerts = await self._check_statistical_significance_alerts()
            alerts.extend(significance_alerts)
            
            # Check for performance degradation alerts
            performance_alerts = await self._check_performance_degradation_alerts()
            alerts.extend(performance_alerts)
            
            # Check for optimization opportunity alerts
            optimization_alerts = await self._check_optimization_opportunity_alerts()
            alerts.extend(optimization_alerts)
            
            # Check for system health alerts
            system_alerts = await self._check_system_health_alerts()
            alerts.extend(system_alerts)
            
            # Store alerts
            for alert in alerts:
                await self._store_alert(alert)
            
            # Send notifications for critical alerts
            critical_alerts = [alert for alert in alerts if alert.severity == AlertSeverity.CRITICAL]
            if critical_alerts:
                await self._send_alert_notifications(critical_alerts)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking and generating alerts: {str(e)}")
            return []

    # =============================================================================
    # ANALYTICS DATA METHODS
    # =============================================================================

    async def _get_dashboard_summary(self, time_range: str) -> DashboardSummary:
        """Get high-level dashboard summary"""
        try:
            # Get active and completed test counts
            active_tests = await self._count_active_tests()
            completed_tests = await self._count_completed_tests(time_range)
            
            # Calculate average conversion rate
            avg_conversion_rate = await self._calculate_average_conversion_rate(time_range)
            
            # Get session count for today
            sessions_today = await self._count_sessions_today()
            
            # Count active optimizations
            active_optimizations = await self._count_active_optimizations()
            
            # Count alerts
            alerts_count = await self._count_active_alerts()
            
            # Get top and bottom performers
            top_performer = await self._get_top_performer(time_range)
            bottom_performer = await self._get_bottom_performer(time_range)
            
            # Calculate system health score
            system_health_score = await self._calculate_system_health_score()
            
            return DashboardSummary(
                total_active_tests=active_tests,
                total_completed_tests=completed_tests,
                avg_conversion_rate=avg_conversion_rate,
                total_sessions_today=sessions_today,
                active_optimizations=active_optimizations,
                alerts_count=alerts_count,
                top_performer=top_performer,
                bottom_performer=bottom_performer,
                system_health_score=system_health_score
            )
            
        except Exception as e:
            logger.error(f"Error getting dashboard summary: {str(e)}")
            return DashboardSummary(0, 0, 0.0, 0, 0, 0, {}, {}, 0.0)

    async def _get_variant_detailed_analytics(self, test_id: str) -> Dict[str, Any]:
        """Get detailed analytics for all variants in a test"""
        try:
            test_config = await self._get_test_configuration(test_id)
            if not test_config:
                return {}
            
            variant_analytics = {}
            
            for variant in test_config.get('variants', []):
                variant_id = variant['variant_id']
                
                # Get basic metrics
                basic_metrics = await self._get_variant_basic_metrics(test_id, variant_id)
                
                # Get conversion funnel
                conversion_funnel = await self._get_variant_conversion_funnel(test_id, variant_id)
                
                # Get time-series data
                time_series = await self._get_variant_time_series(test_id, variant_id)
                
                # Get interaction patterns
                interaction_patterns = await self._get_variant_interaction_patterns(test_id, variant_id)
                
                # Get user segments performance
                segment_performance = await self._get_variant_segment_performance(test_id, variant_id)
                
                variant_analytics[variant_id] = {
                    'variant_name': variant.get('variant_name', variant_id),
                    'is_control': variant.get('is_control', False),
                    'traffic_allocation': variant.get('traffic_allocation', 0),
                    'basic_metrics': basic_metrics,
                    'conversion_funnel': conversion_funnel,
                    'time_series': time_series,
                    'interaction_patterns': interaction_patterns,
                    'segment_performance': segment_performance
                }
            
            return variant_analytics
            
        except Exception as e:
            logger.error(f"Error getting variant detailed analytics: {str(e)}")
            return {}

    async def _get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics for dashboard"""
        try:
            current_time = datetime.utcnow()
            window_start = current_time - timedelta(minutes=self.real_time_window_minutes)
            
            # Get real-time conversion rates
            conversion_rates = await self._get_real_time_conversion_rates(window_start, current_time)
            
            # Get traffic volumes
            traffic_volumes = await self._get_real_time_traffic_volumes(window_start, current_time)
            
            # Get active optimizations
            active_optimizations = await self._get_real_time_active_optimizations()
            
            # Get performance changes
            performance_changes = await self._get_real_time_performance_changes(window_start, current_time)
            
            return {
                'conversion_rates': conversion_rates,
                'traffic_volumes': traffic_volumes,
                'active_optimizations': active_optimizations,
                'performance_changes': performance_changes,
                'window_minutes': self.real_time_window_minutes,
                'last_update': current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting real-time metrics: {str(e)}")
            return {}

    # =============================================================================
    # ALERT SYSTEM METHODS
    # =============================================================================

    async def _check_statistical_significance_alerts(self) -> List[DashboardAlert]:
        """Check for statistical significance alerts"""
        alerts = []
        
        try:
            active_tests = await self._get_active_test_ids()
            
            for test_id in active_tests:
                test_results = await self.ab_testing_framework.get_test_results(test_id)
                
                if 'error' not in test_results:
                    significance_analysis = test_results.get('statistical_analysis', {})
                    
                    if significance_analysis.get('overall_significance') == 'significant':
                        # Check if test has been running long enough
                        test_config = test_results.get('test_config', {})
                        start_date = datetime.fromisoformat(test_config.get('start_date', ''))
                        days_running = (datetime.utcnow() - start_date).days
                        
                        if days_running >= 7:  # Minimum 7 days
                            alerts.append(DashboardAlert(
                                alert_id=f"significance_{test_id}_{datetime.utcnow().timestamp()}",
                                test_id=test_id,
                                test_name=test_config.get('test_name', 'Unknown Test'),
                                severity=AlertSeverity.WARNING,
                                message="Test has reached statistical significance",
                                details={
                                    'days_running': days_running,
                                    'significance_level': significance_analysis.get('overall_significance'),
                                    'variant_results': test_results.get('variant_results', [])
                                },
                                action_required=True,
                                suggested_actions=[
                                    "Review test results for early stopping",
                                    "Consider declaring a winner",
                                    "Evaluate business impact before stopping"
                                ]
                            ))
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking statistical significance alerts: {str(e)}")
            return []

    async def _check_performance_degradation_alerts(self) -> List[DashboardAlert]:
        """Check for performance degradation alerts"""
        alerts = []
        
        try:
            active_tests = await self._get_active_test_ids()
            
            for test_id in active_tests:
                # Get recent performance trends
                recent_performance = await self._get_recent_performance_trend(test_id, hours=4)
                
                if recent_performance and len(recent_performance) >= 3:
                    # Check for declining trend
                    recent_rates = [point['conversion_rate'] for point in recent_performance]
                    
                    if len(recent_rates) >= 3:
                        # Simple trend analysis
                        trend_slope = (recent_rates[-1] - recent_rates[0]) / len(recent_rates)
                        
                        if trend_slope < -0.01:  # 1% decline threshold
                            test_config = await self._get_test_configuration(test_id)
                            
                            alerts.append(DashboardAlert(
                                alert_id=f"degradation_{test_id}_{datetime.utcnow().timestamp()}",
                                test_id=test_id,
                                test_name=test_config.get('test_name', 'Unknown Test'),
                                severity=AlertSeverity.WARNING,
                                message=f"Performance declining by {abs(trend_slope)*100:.1f}%",
                                details={
                                    'trend_slope': trend_slope,
                                    'recent_performance': recent_performance,
                                    'decline_percentage': abs(trend_slope) * 100
                                },
                                action_required=True,
                                suggested_actions=[
                                    "Investigate recent changes",
                                    "Check for technical issues",
                                    "Review traffic quality"
                                ]
                            ))
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking performance degradation alerts: {str(e)}")
            return []

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    async def _get_test_configuration(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get test configuration"""
        try:
            config_key = f"ab_test_config:{test_id}"
            config_data = await self.redis_client.get(config_key)
            
            if config_data:
                return json.loads(config_data)
            
            return None
        except Exception as e:
            logger.error(f"Error getting test configuration: {str(e)}")
            return None

    async def _count_active_tests(self) -> int:
        """Count active tests"""
        try:
            pattern = "ab_test_config:*"
            keys = await self.redis_client.keys(pattern)
            
            active_count = 0
            for key in keys:
                test_data = await self.redis_client.get(key)
                if test_data:
                    test_config = json.loads(test_data)
                    if test_config.get('status') == 'active':
                        active_count += 1
            
            return active_count
        except Exception as e:
            logger.error(f"Error counting active tests: {str(e)}")
            return 0

    async def _store_alert(self, alert: DashboardAlert):
        """Store alert in Redis"""
        try:
            alert_key = f"dashboard_alert:{alert.alert_id}"
            alert_data = asdict(alert)
            
            # Convert datetime to string for JSON serialization
            alert_data['created_at'] = alert.created_at.isoformat()
            
            await self.redis_client.setex(
                alert_key,
                86400 * self.alert_retention_days,
                json.dumps(alert_data)
            )
            
            # Add to active alerts list
            await self.redis_client.sadd("active_dashboard_alerts", alert.alert_id)
            
        except Exception as e:
            logger.error(f"Error storing alert: {str(e)}")

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'ABTestingDashboard',
    'DashboardAlert',
    'PerformanceSnapshot',
    'DashboardSummary',
    'DashboardView',
    'MetricType',
    'AlertSeverity'
]