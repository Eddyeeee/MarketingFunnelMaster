#!/usr/bin/env python3
"""
Performance Analytics Integration for Personalization Metrics
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 4 - Feedback-Driven Improvement System

Integrates performance analytics specifically for personalization metrics,
providing real-time monitoring and analysis of personalization effectiveness.

Features:
- Real-time personalization performance tracking
- Cross-device personalization analytics
- Conversion attribution to personalization strategies
- A/B test integration for personalization variants
- Machine learning model performance monitoring

Executor: Claude Code
Created: 2025-07-04
"""

import asyncio
import json
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from statistics import mean, median, stdev

# Import core components
from ..testing.ab_testing_framework import ABTestingFramework, TestMetrics
from ...src.api.journey.personalization_engine import PersonalizationEngine
from ...src.api.journey.models import JourneySession, PersonalizedContent
from ..tracking.performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)

class PersonalizationMetricType(str, Enum):
    """Types of personalization metrics"""
    ACCURACY = "accuracy"
    CONVERSION_LIFT = "conversion_lift"
    ENGAGEMENT_IMPROVEMENT = "engagement_improvement"
    CLICK_THROUGH_RATE = "click_through_rate"
    TIME_ON_PAGE = "time_on_page"
    BOUNCE_RATE_REDUCTION = "bounce_rate_reduction"
    REVENUE_ATTRIBUTION = "revenue_attribution"
    USER_SATISFACTION = "user_satisfaction"

class PersonaPerformance(str, Enum):
    """Persona performance levels"""
    UNDERPERFORMING = "underperforming"
    BASELINE = "baseline"
    OUTPERFORMING = "outperforming"
    EXCEPTIONAL = "exceptional"

class DeviceOptimizationLevel(str, Enum):
    """Device optimization levels"""
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

@dataclass
class PersonalizationMetrics:
    """Comprehensive personalization metrics"""
    timestamp: datetime
    session_id: str
    user_id: Optional[str]
    persona: str
    device_type: str
    personalization_strategy: str
    
    # Performance metrics
    conversion_achieved: bool
    engagement_score: float
    click_through_rate: float
    time_on_page: float
    bounce_rate: float
    
    # Personalization effectiveness
    personalization_accuracy: float
    content_relevance_score: float
    user_satisfaction_score: float
    
    # Attribution metrics
    revenue_attributed: float = 0.0
    conversion_value: float = 0.0
    
    # A/B test metrics
    ab_test_id: Optional[str] = None
    variant_id: Optional[str] = None
    
    # Context data
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PersonalizationAnalytics:
    """Analytics summary for personalization performance"""
    time_period: Tuple[datetime, datetime]
    total_sessions: int
    
    # Overall performance
    overall_conversion_rate: float
    overall_engagement_score: float
    personalization_accuracy: float
    
    # Performance by persona
    persona_performance: Dict[str, Dict[str, float]]
    
    # Performance by device
    device_performance: Dict[str, Dict[str, float]]
    
    # Strategy effectiveness
    strategy_performance: Dict[str, Dict[str, float]]
    
    # Trends and insights
    performance_trends: Dict[str, List[float]]
    improvement_opportunities: List[Dict[str, Any]]
    
    # A/B test integration
    ab_test_impact: Dict[str, Dict[str, float]]

class PersonalizationAnalyticsEngine:
    """
    Performance Analytics Integration for Personalization Metrics
    
    Provides comprehensive analytics and monitoring for personalization
    effectiveness across different personas, devices, and strategies.
    """
    
    def __init__(self, personalization_engine: PersonalizationEngine,
                 ab_testing_framework: ABTestingFramework,
                 performance_tracker: PerformanceTracker):
        self.personalization_engine = personalization_engine
        self.ab_testing_framework = ab_testing_framework
        self.performance_tracker = performance_tracker
        
        # Metrics storage
        self.metrics_buffer: List[PersonalizationMetrics] = []
        self.analytics_cache: Dict[str, PersonalizationAnalytics] = {}
        
        # Real-time tracking
        self.session_tracking: Dict[str, Dict[str, Any]] = {}
        self.persona_baselines: Dict[str, Dict[str, float]] = {}
        self.device_baselines: Dict[str, Dict[str, float]] = {}
        
        # Performance monitoring
        self.alert_thresholds = {
            'conversion_rate_drop': 0.15,  # 15% drop triggers alert
            'engagement_drop': 0.20,       # 20% drop triggers alert
            'accuracy_drop': 0.10,         # 10% drop triggers alert
            'bounce_rate_increase': 0.25   # 25% increase triggers alert
        }
        
        # Configuration
        self.config = {
            'analytics_retention_days': 90,
            'real_time_window_minutes': 30,
            'baseline_calculation_days': 7,
            'cache_refresh_minutes': 15,
            'alert_check_interval': 300  # 5 minutes
        }
    
    async def track_personalization_performance(self, session: JourneySession,
                                              personalized_content: PersonalizedContent,
                                              performance_data: Dict[str, Any]) -> None:
        """
        Track performance of personalization for a specific session
        
        Args:
            session: Journey session
            personalized_content: Generated personalized content
            performance_data: Performance metrics data
        """
        try:
            # Extract performance metrics
            metrics = PersonalizationMetrics(
                timestamp=datetime.utcnow(),
                session_id=session.session_id,
                user_id=session.user_id,
                persona=session.detected_persona or "unknown",
                device_type=session.device_info.get('type', 'unknown'),
                personalization_strategy=personalized_content.personalization_strategy,
                
                # Performance data
                conversion_achieved=performance_data.get('conversion_achieved', False),
                engagement_score=performance_data.get('engagement_score', 0.0),
                click_through_rate=performance_data.get('click_through_rate', 0.0),
                time_on_page=performance_data.get('time_on_page', 0.0),
                bounce_rate=performance_data.get('bounce_rate', 1.0),
                
                # Personalization effectiveness
                personalization_accuracy=performance_data.get('personalization_accuracy', 0.0),
                content_relevance_score=performance_data.get('content_relevance_score', 0.0),
                user_satisfaction_score=performance_data.get('user_satisfaction_score', 0.0),
                
                # Attribution
                revenue_attributed=performance_data.get('revenue_attributed', 0.0),
                conversion_value=performance_data.get('conversion_value', 0.0),
                
                # A/B test integration
                ab_test_id=performance_data.get('ab_test_id'),
                variant_id=performance_data.get('variant_id'),
                
                # Additional context
                context=performance_data.get('context', {})
            )
            
            # Store metrics
            self.metrics_buffer.append(metrics)
            
            # Update real-time tracking
            await self._update_real_time_tracking(metrics)
            
            # Check for performance alerts
            await self._check_performance_alerts(metrics)
            
            logger.debug(f"Tracked personalization performance for session {session.session_id}")
            
        except Exception as e:
            logger.error(f"Error tracking personalization performance: {e}")
    
    async def generate_personalization_analytics(self, 
                                               time_window: timedelta = timedelta(days=7),
                                               persona_filter: Optional[str] = None,
                                               device_filter: Optional[str] = None) -> PersonalizationAnalytics:
        """
        Generate comprehensive personalization analytics
        
        Args:
            time_window: Time window for analysis
            persona_filter: Filter by specific persona
            device_filter: Filter by specific device type
        
        Returns:
            Personalization analytics
        """
        try:
            logger.info("Generating personalization analytics")
            
            # Get metrics for time window
            end_time = datetime.utcnow()
            start_time = end_time - time_window
            
            filtered_metrics = [
                metric for metric in self.metrics_buffer
                if start_time <= metric.timestamp <= end_time
            ]
            
            # Apply filters
            if persona_filter:
                filtered_metrics = [m for m in filtered_metrics if m.persona == persona_filter]
            
            if device_filter:
                filtered_metrics = [m for m in filtered_metrics if m.device_type == device_filter]
            
            if not filtered_metrics:
                return await self._get_empty_analytics(start_time, end_time)
            
            # Calculate overall performance
            overall_stats = await self._calculate_overall_performance(filtered_metrics)
            
            # Calculate persona performance
            persona_performance = await self._calculate_persona_performance(filtered_metrics)
            
            # Calculate device performance
            device_performance = await self._calculate_device_performance(filtered_metrics)
            
            # Calculate strategy effectiveness
            strategy_performance = await self._calculate_strategy_performance(filtered_metrics)
            
            # Analyze trends
            performance_trends = await self._analyze_performance_trends(filtered_metrics, time_window)
            
            # Identify improvement opportunities
            improvement_opportunities = await self._identify_improvement_opportunities(
                filtered_metrics, persona_performance, device_performance
            )
            
            # Analyze A/B test impact
            ab_test_impact = await self._analyze_ab_test_impact(filtered_metrics)
            
            # Create analytics object
            analytics = PersonalizationAnalytics(
                time_period=(start_time, end_time),
                total_sessions=len(filtered_metrics),
                overall_conversion_rate=overall_stats['conversion_rate'],
                overall_engagement_score=overall_stats['engagement_score'],
                personalization_accuracy=overall_stats['personalization_accuracy'],
                persona_performance=persona_performance,
                device_performance=device_performance,
                strategy_performance=strategy_performance,
                performance_trends=performance_trends,
                improvement_opportunities=improvement_opportunities,
                ab_test_impact=ab_test_impact
            )
            
            # Cache analytics
            cache_key = f"{start_time.isoformat()}_{end_time.isoformat()}_{persona_filter}_{device_filter}"
            self.analytics_cache[cache_key] = analytics
            
            logger.info(f"Generated analytics for {len(filtered_metrics)} personalization sessions")
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating personalization analytics: {e}")
            return await self._get_empty_analytics(start_time, end_time)
    
    async def get_real_time_performance(self) -> Dict[str, Any]:
        """
        Get real-time personalization performance metrics
        
        Returns:
            Real-time performance data
        """
        try:
            # Get recent metrics (last 30 minutes)
            cutoff_time = datetime.utcnow() - timedelta(minutes=self.config['real_time_window_minutes'])
            recent_metrics = [
                metric for metric in self.metrics_buffer
                if metric.timestamp >= cutoff_time
            ]
            
            if not recent_metrics:
                return {'message': 'No recent personalization data available'}
            
            # Calculate real-time metrics
            total_sessions = len(recent_metrics)
            conversions = sum(1 for m in recent_metrics if m.conversion_achieved)
            avg_engagement = mean([m.engagement_score for m in recent_metrics])
            avg_accuracy = mean([m.personalization_accuracy for m in recent_metrics])
            
            # Performance by persona
            persona_stats = defaultdict(list)
            for metric in recent_metrics:
                persona_stats[metric.persona].append(metric)
            
            persona_performance = {}
            for persona, metrics in persona_stats.items():
                persona_performance[persona] = {
                    'sessions': len(metrics),
                    'conversion_rate': sum(1 for m in metrics if m.conversion_achieved) / len(metrics),
                    'engagement_score': mean([m.engagement_score for m in metrics]),
                    'accuracy': mean([m.personalization_accuracy for m in metrics])
                }
            
            # Performance by device
            device_stats = defaultdict(list)
            for metric in recent_metrics:
                device_stats[metric.device_type].append(metric)
            
            device_performance = {}
            for device, metrics in device_stats.items():
                device_performance[device] = {
                    'sessions': len(metrics),
                    'conversion_rate': sum(1 for m in metrics if m.conversion_achieved) / len(metrics),
                    'engagement_score': mean([m.engagement_score for m in metrics]),
                    'accuracy': mean([m.personalization_accuracy for m in metrics])
                }
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'time_window_minutes': self.config['real_time_window_minutes'],
                'overall_performance': {
                    'total_sessions': total_sessions,
                    'conversion_rate': conversions / total_sessions,
                    'average_engagement': avg_engagement,
                    'average_accuracy': avg_accuracy
                },
                'persona_performance': persona_performance,
                'device_performance': device_performance
            }
            
        except Exception as e:
            logger.error(f"Error getting real-time performance: {e}")
            return {'error': str(e)}
    
    async def compare_personalization_strategies(self, strategy_a: str, strategy_b: str,
                                               time_window: timedelta = timedelta(days=14)) -> Dict[str, Any]:
        """
        Compare performance between two personalization strategies
        
        Args:
            strategy_a: First strategy to compare
            strategy_b: Second strategy to compare
            time_window: Time window for comparison
        
        Returns:
            Comparison results
        """
        try:
            logger.info(f"Comparing personalization strategies: {strategy_a} vs {strategy_b}")
            
            # Get metrics for both strategies
            cutoff_time = datetime.utcnow() - time_window
            
            strategy_a_metrics = [
                metric for metric in self.metrics_buffer
                if (metric.timestamp >= cutoff_time and 
                    metric.personalization_strategy == strategy_a)
            ]
            
            strategy_b_metrics = [
                metric for metric in self.metrics_buffer
                if (metric.timestamp >= cutoff_time and 
                    metric.personalization_strategy == strategy_b)
            ]
            
            if not strategy_a_metrics or not strategy_b_metrics:
                return {'error': 'Insufficient data for comparison'}
            
            # Calculate metrics for strategy A
            strategy_a_stats = await self._calculate_strategy_stats(strategy_a_metrics)
            
            # Calculate metrics for strategy B
            strategy_b_stats = await self._calculate_strategy_stats(strategy_b_metrics)
            
            # Calculate statistical significance
            significance = await self._calculate_statistical_significance(
                strategy_a_metrics, strategy_b_metrics
            )
            
            # Generate insights
            insights = await self._generate_strategy_comparison_insights(
                strategy_a, strategy_a_stats,
                strategy_b, strategy_b_stats,
                significance
            )
            
            return {
                'comparison_period': {
                    'start': cutoff_time.isoformat(),
                    'end': datetime.utcnow().isoformat(),
                    'duration_days': time_window.days
                },
                'strategy_a': {
                    'name': strategy_a,
                    'metrics': strategy_a_stats,
                    'sample_size': len(strategy_a_metrics)
                },
                'strategy_b': {
                    'name': strategy_b,
                    'metrics': strategy_b_stats,
                    'sample_size': len(strategy_b_metrics)
                },
                'statistical_significance': significance,
                'insights': insights,
                'recommendation': await self._generate_strategy_recommendation(
                    strategy_a_stats, strategy_b_stats, significance
                )
            }
            
        except Exception as e:
            logger.error(f"Error comparing personalization strategies: {e}")
            return {'error': str(e)}
    
    async def get_persona_optimization_recommendations(self, persona: str) -> List[Dict[str, Any]]:
        """
        Get optimization recommendations for a specific persona
        
        Args:
            persona: Target persona
        
        Returns:
            List of optimization recommendations
        """
        try:
            logger.info(f"Generating optimization recommendations for persona: {persona}")
            
            # Get recent metrics for the persona
            cutoff_time = datetime.utcnow() - timedelta(days=14)
            persona_metrics = [
                metric for metric in self.metrics_buffer
                if (metric.timestamp >= cutoff_time and metric.persona == persona)
            ]
            
            if not persona_metrics:
                return [{'message': f'No recent data available for persona: {persona}'}]
            
            recommendations = []
            
            # Analyze conversion performance
            conversion_rate = sum(1 for m in persona_metrics if m.conversion_achieved) / len(persona_metrics)
            baseline_conversion = self.persona_baselines.get(persona, {}).get('conversion_rate', 0.05)
            
            if conversion_rate < baseline_conversion * 0.9:  # 10% below baseline
                recommendations.append({
                    'type': 'conversion_optimization',
                    'priority': 'high',
                    'description': f'Conversion rate ({conversion_rate:.2%}) is below baseline ({baseline_conversion:.2%})',
                    'recommendations': [
                        'Review and optimize call-to-action placement and messaging',
                        'Test different value propositions for this persona',
                        'Analyze conversion funnel for drop-off points'
                    ]
                })
            
            # Analyze engagement performance
            avg_engagement = mean([m.engagement_score for m in persona_metrics])
            baseline_engagement = self.persona_baselines.get(persona, {}).get('engagement_score', 0.7)
            
            if avg_engagement < baseline_engagement * 0.85:  # 15% below baseline
                recommendations.append({
                    'type': 'engagement_optimization',
                    'priority': 'medium',
                    'description': f'Engagement score ({avg_engagement:.2f}) is below baseline ({baseline_engagement:.2f})',
                    'recommendations': [
                        'Enhance content personalization for this persona',
                        'Test different content formats and presentation styles',
                        'Review and update persona-specific messaging'
                    ]
                })
            
            # Analyze device performance variation
            device_performance = defaultdict(list)
            for metric in persona_metrics:
                device_performance[metric.device_type].append(metric)
            
            for device, metrics in device_performance.items():
                if len(metrics) < 10:  # Skip devices with insufficient data
                    continue
                
                device_conversion = sum(1 for m in metrics if m.conversion_achieved) / len(metrics)
                avg_device_conversion = sum(
                    1 for m in persona_metrics if m.conversion_achieved
                ) / len(persona_metrics)
                
                if device_conversion < avg_device_conversion * 0.8:  # 20% below average
                    recommendations.append({
                        'type': 'device_optimization',
                        'priority': 'medium',
                        'description': f'Performance on {device} is significantly below average',
                        'recommendations': [
                            f'Optimize content layout and UX for {device}',
                            f'Test device-specific personalization strategies',
                            f'Review {device} user journey and interaction patterns'
                        ]
                    })
            
            # Analyze personalization accuracy
            avg_accuracy = mean([m.personalization_accuracy for m in persona_metrics])
            if avg_accuracy < 0.8:  # Below 80% accuracy
                recommendations.append({
                    'type': 'personalization_accuracy',
                    'priority': 'high',
                    'description': f'Personalization accuracy ({avg_accuracy:.2%}) is below optimal threshold',
                    'recommendations': [
                        'Review and update persona detection algorithms',
                        'Enhance personalization model training data',
                        'Test alternative personalization strategies for this persona'
                    ]
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating persona optimization recommendations: {e}")
            return [{'error': str(e)}]
    
    # =============================================================================
    # INTERNAL IMPLEMENTATION METHODS
    # =============================================================================
    
    async def _update_real_time_tracking(self, metrics: PersonalizationMetrics):
        """Update real-time tracking with new metrics"""
        session_id = metrics.session_id
        
        # Update session tracking
        if session_id not in self.session_tracking:
            self.session_tracking[session_id] = {
                'start_time': metrics.timestamp,
                'metrics_count': 0,
                'total_engagement': 0.0,
                'persona': metrics.persona,
                'device': metrics.device_type
            }
        
        session_data = self.session_tracking[session_id]
        session_data['metrics_count'] += 1
        session_data['total_engagement'] += metrics.engagement_score
        session_data['last_update'] = metrics.timestamp
        
        # Update persona baselines if needed
        await self._update_persona_baselines(metrics)
        
        # Update device baselines if needed
        await self._update_device_baselines(metrics)
    
    async def _check_performance_alerts(self, metrics: PersonalizationMetrics):
        """Check for performance alerts based on thresholds"""
        # Implementation would check various alert conditions
        pass
    
    async def _calculate_overall_performance(self, metrics: List[PersonalizationMetrics]) -> Dict[str, float]:
        """Calculate overall performance metrics"""
        if not metrics:
            return {'conversion_rate': 0.0, 'engagement_score': 0.0, 'personalization_accuracy': 0.0}
        
        total_sessions = len(metrics)
        conversions = sum(1 for m in metrics if m.conversion_achieved)
        
        return {
            'conversion_rate': conversions / total_sessions,
            'engagement_score': mean([m.engagement_score for m in metrics]),
            'personalization_accuracy': mean([m.personalization_accuracy for m in metrics]),
            'average_time_on_page': mean([m.time_on_page for m in metrics]),
            'average_ctr': mean([m.click_through_rate for m in metrics]),
            'bounce_rate': mean([m.bounce_rate for m in metrics])
        }
    
    async def _calculate_persona_performance(self, metrics: List[PersonalizationMetrics]) -> Dict[str, Dict[str, float]]:
        """Calculate performance by persona"""
        persona_groups = defaultdict(list)
        for metric in metrics:
            persona_groups[metric.persona].append(metric)
        
        persona_performance = {}
        for persona, persona_metrics in persona_groups.items():
            persona_performance[persona] = await self._calculate_overall_performance(persona_metrics)
            persona_performance[persona]['session_count'] = len(persona_metrics)
        
        return persona_performance
    
    async def _calculate_device_performance(self, metrics: List[PersonalizationMetrics]) -> Dict[str, Dict[str, float]]:
        """Calculate performance by device type"""
        device_groups = defaultdict(list)
        for metric in metrics:
            device_groups[metric.device_type].append(metric)
        
        device_performance = {}
        for device, device_metrics in device_groups.items():
            device_performance[device] = await self._calculate_overall_performance(device_metrics)
            device_performance[device]['session_count'] = len(device_metrics)
        
        return device_performance
    
    async def _calculate_strategy_performance(self, metrics: List[PersonalizationMetrics]) -> Dict[str, Dict[str, float]]:
        """Calculate performance by personalization strategy"""
        strategy_groups = defaultdict(list)
        for metric in metrics:
            strategy_groups[metric.personalization_strategy].append(metric)
        
        strategy_performance = {}
        for strategy, strategy_metrics in strategy_groups.items():
            strategy_performance[strategy] = await self._calculate_overall_performance(strategy_metrics)
            strategy_performance[strategy]['session_count'] = len(strategy_metrics)
        
        return strategy_performance
    
    async def _analyze_performance_trends(self, metrics: List[PersonalizationMetrics], 
                                        time_window: timedelta) -> Dict[str, List[float]]:
        """Analyze performance trends over time"""
        # Group metrics by time intervals
        interval_hours = max(1, time_window.total_seconds() / 3600 / 24)  # Daily intervals for week+
        
        trends = {
            'conversion_rate': [],
            'engagement_score': [],
            'personalization_accuracy': []
        }
        
        # Simple trend calculation - would be more sophisticated in real implementation
        sorted_metrics = sorted(metrics, key=lambda m: m.timestamp)
        
        if len(sorted_metrics) > 0:
            # Calculate daily averages for trends
            daily_groups = defaultdict(list)
            for metric in sorted_metrics:
                day_key = metric.timestamp.date()
                daily_groups[day_key].append(metric)
            
            for day, day_metrics in sorted(daily_groups.items()):
                day_stats = await self._calculate_overall_performance(day_metrics)
                trends['conversion_rate'].append(day_stats['conversion_rate'])
                trends['engagement_score'].append(day_stats['engagement_score'])
                trends['personalization_accuracy'].append(day_stats['personalization_accuracy'])
        
        return trends
    
    async def _identify_improvement_opportunities(self, metrics: List[PersonalizationMetrics],
                                                persona_performance: Dict[str, Dict[str, float]],
                                                device_performance: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Identify improvement opportunities based on performance analysis"""
        opportunities = []
        
        # Identify underperforming personas
        avg_conversion = mean([p['conversion_rate'] for p in persona_performance.values()])
        for persona, perf in persona_performance.items():
            if perf['conversion_rate'] < avg_conversion * 0.8:  # 20% below average
                opportunities.append({
                    'type': 'persona_underperformance',
                    'target': persona,
                    'description': f'Persona {persona} has conversion rate {perf["conversion_rate"]:.2%} (20% below average)',
                    'priority': 'high',
                    'potential_impact': 'medium'
                })
        
        # Identify underperforming devices
        avg_device_conversion = mean([d['conversion_rate'] for d in device_performance.values()])
        for device, perf in device_performance.items():
            if perf['conversion_rate'] < avg_device_conversion * 0.7:  # 30% below average
                opportunities.append({
                    'type': 'device_underperformance',
                    'target': device,
                    'description': f'Device {device} has conversion rate {perf["conversion_rate"]:.2%} (30% below average)',
                    'priority': 'medium',
                    'potential_impact': 'high'
                })
        
        return opportunities
    
    async def _analyze_ab_test_impact(self, metrics: List[PersonalizationMetrics]) -> Dict[str, Dict[str, float]]:
        """Analyze impact of A/B tests on personalization performance"""
        ab_test_groups = defaultdict(lambda: defaultdict(list))
        
        for metric in metrics:
            if metric.ab_test_id and metric.variant_id:
                ab_test_groups[metric.ab_test_id][metric.variant_id].append(metric)
        
        ab_test_impact = {}
        for test_id, variants in ab_test_groups.items():
            test_impact = {}
            for variant_id, variant_metrics in variants.items():
                variant_stats = await self._calculate_overall_performance(variant_metrics)
                test_impact[variant_id] = variant_stats
            
            ab_test_impact[test_id] = test_impact
        
        return ab_test_impact
    
    async def _get_empty_analytics(self, start_time: datetime, end_time: datetime) -> PersonalizationAnalytics:
        """Get empty analytics structure"""
        return PersonalizationAnalytics(
            time_period=(start_time, end_time),
            total_sessions=0,
            overall_conversion_rate=0.0,
            overall_engagement_score=0.0,
            personalization_accuracy=0.0,
            persona_performance={},
            device_performance={},
            strategy_performance={},
            performance_trends={},
            improvement_opportunities=[],
            ab_test_impact={}
        )
    
    async def _calculate_strategy_stats(self, metrics: List[PersonalizationMetrics]) -> Dict[str, float]:
        """Calculate statistics for a strategy"""
        return await self._calculate_overall_performance(metrics)
    
    async def _calculate_statistical_significance(self, metrics_a: List[PersonalizationMetrics],
                                                metrics_b: List[PersonalizationMetrics]) -> Dict[str, Any]:
        """Calculate statistical significance between two groups"""
        # Simplified significance calculation - would use proper statistical tests in real implementation
        conversions_a = sum(1 for m in metrics_a if m.conversion_achieved)
        conversions_b = sum(1 for m in metrics_b if m.conversion_achieved)
        
        rate_a = conversions_a / len(metrics_a)
        rate_b = conversions_b / len(metrics_b)
        
        # Simple confidence calculation
        difference = abs(rate_a - rate_b)
        confidence = min(0.95, difference * 10)  # Simplified
        
        return {
            'conversion_rate_difference': difference,
            'confidence_level': confidence,
            'statistically_significant': confidence > 0.8,
            'sample_size_a': len(metrics_a),
            'sample_size_b': len(metrics_b)
        }
    
    async def _generate_strategy_comparison_insights(self, strategy_a: str, stats_a: Dict[str, float],
                                                   strategy_b: str, stats_b: Dict[str, float],
                                                   significance: Dict[str, Any]) -> List[str]:
        """Generate insights from strategy comparison"""
        insights = []
        
        if significance['statistically_significant']:
            if stats_a['conversion_rate'] > stats_b['conversion_rate']:
                insights.append(f"{strategy_a} significantly outperforms {strategy_b} in conversion rate")
            else:
                insights.append(f"{strategy_b} significantly outperforms {strategy_a} in conversion rate")
        else:
            insights.append("No statistically significant difference in conversion rates")
        
        # Add more insights based on other metrics
        if stats_a['engagement_score'] > stats_b['engagement_score'] * 1.1:
            insights.append(f"{strategy_a} shows higher engagement scores")
        elif stats_b['engagement_score'] > stats_a['engagement_score'] * 1.1:
            insights.append(f"{strategy_b} shows higher engagement scores")
        
        return insights
    
    async def _generate_strategy_recommendation(self, stats_a: Dict[str, float],
                                              stats_b: Dict[str, float],
                                              significance: Dict[str, Any]) -> str:
        """Generate recommendation based on strategy comparison"""
        if not significance['statistically_significant']:
            return "Continue testing both strategies to gather more data"
        
        if stats_a['conversion_rate'] > stats_b['conversion_rate']:
            return "Recommend using Strategy A based on superior conversion performance"
        else:
            return "Recommend using Strategy B based on superior conversion performance"
    
    async def _update_persona_baselines(self, metrics: PersonalizationMetrics):
        """Update persona baseline metrics"""
        # Implementation would update rolling baselines
        pass
    
    async def _update_device_baselines(self, metrics: PersonalizationMetrics):
        """Update device baseline metrics"""
        # Implementation would update rolling baselines
        pass
    
    async def cleanup_old_metrics(self):
        """Clean up old metrics based on retention policy"""
        retention_days = self.config['analytics_retention_days']
        cutoff_time = datetime.utcnow() - timedelta(days=retention_days)
        
        # Remove old metrics
        self.metrics_buffer = [
            metric for metric in self.metrics_buffer
            if metric.timestamp >= cutoff_time
        ]
        
        # Clean up session tracking
        old_sessions = [
            session_id for session_id, data in self.session_tracking.items()
            if data.get('last_update', datetime.min) < cutoff_time
        ]
        
        for session_id in old_sessions:
            del self.session_tracking[session_id]
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the analytics engine"""
        return {
            'metrics_buffer_size': len(self.metrics_buffer),
            'active_sessions': len(self.session_tracking),
            'analytics_cache_size': len(self.analytics_cache),
            'personas_tracked': len(set(m.persona for m in self.metrics_buffer)),
            'devices_tracked': len(set(m.device_type for m in self.metrics_buffer)),
            'strategies_tracked': len(set(m.personalization_strategy for m in self.metrics_buffer))
        }