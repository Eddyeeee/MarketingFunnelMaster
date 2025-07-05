# Real-Time Test Optimization Engine - Week 3 Implementation
# Module: 3A - Week 3 - Real-Time A/B Test Optimization
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
from scipy import stats
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_

from .models import *
from .database_models import JourneySession, PersonalizationData
from .ab_testing_framework import (
    ABTestingFramework, ABTest, ABTestVariant, ABTestResult, 
    TestStatus, TestType, OptimizationGoal, StatisticalSignificance
)
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# OPTIMIZATION MODELS AND ENUMS
# =============================================================================

class OptimizationType(Enum):
    TRAFFIC_REALLOCATION = "traffic_reallocation"
    EARLY_STOPPING = "early_stopping"
    VARIANT_MODIFICATION = "variant_modification"
    SAMPLE_SIZE_ADJUSTMENT = "sample_size_adjustment"
    TARGETING_REFINEMENT = "targeting_refinement"

class OptimizationTrigger(Enum):
    STATISTICAL_SIGNIFICANCE = "statistical_significance"
    POOR_PERFORMANCE = "poor_performance"
    INSUFFICIENT_TRAFFIC = "insufficient_traffic"
    CONVERSION_PLATEAU = "conversion_plateau"
    TIME_CONSTRAINT = "time_constraint"

class OptimizationDecision(Enum):
    CONTINUE = "continue"
    OPTIMIZE = "optimize"
    STOP_WINNER = "stop_winner"
    STOP_INCONCLUSIVE = "stop_inconclusive"
    EXTEND_TEST = "extend_test"

@dataclass
class OptimizationRecommendation:
    """Real-time optimization recommendation"""
    test_id: str
    optimization_type: OptimizationType
    trigger: OptimizationTrigger
    decision: OptimizationDecision
    confidence: float
    expected_impact: Dict[str, float]
    recommended_actions: List[str]
    risk_assessment: Dict[str, float]
    reasoning: str
    priority: int  # 1-5, 5 being highest priority
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

@dataclass
class OptimizationResult:
    """Result of an optimization action"""
    optimization_id: str
    test_id: str
    optimization_type: OptimizationType
    actions_taken: List[str]
    before_metrics: Dict[str, float]
    expected_after_metrics: Dict[str, float]
    success: bool
    error_message: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

@dataclass
class PerformanceMonitoringData:
    """Real-time performance monitoring data"""
    test_id: str
    variant_id: str
    current_sessions: int
    current_conversions: int
    conversion_rate: float
    conversion_rate_trend: List[float]  # Last 10 data points
    statistical_power: float
    time_to_significance: Optional[float]  # Estimated hours
    performance_score: float  # 0-100
    anomaly_detected: bool
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.utcnow()

# =============================================================================
# REAL-TIME OPTIMIZATION ENGINE
# =============================================================================

class RealTimeOptimizationEngine:
    """Advanced real-time optimization engine for A/B tests"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.ab_testing_framework = ABTestingFramework(db)
        
        # Optimization parameters
        self.monitoring_interval = 300  # 5 minutes
        self.min_sessions_for_optimization = 50
        self.significance_threshold = 0.95
        self.early_stopping_threshold = 0.99
        self.poor_performance_threshold = 0.5
        self.plateau_detection_window = 6  # hours
        
        # Risk management
        self.max_traffic_reallocation_per_hour = 0.1  # 10% max change per hour
        self.min_control_group_traffic = 0.2  # Always keep 20% for control
        
        # Performance tracking
        self.optimization_history = {}
        
    async def start_continuous_monitoring(self, test_ids: List[str]):
        """Start continuous monitoring for specified tests"""
        try:
            logger.info(f"Starting continuous monitoring for {len(test_ids)} tests")
            
            # Store monitoring configuration
            monitoring_config = {
                'test_ids': test_ids,
                'monitoring_interval': self.monitoring_interval,
                'started_at': datetime.utcnow().isoformat(),
                'status': 'active'
            }
            
            await self.redis_client.setex(
                'optimization_monitoring_config', 
                86400, 
                json.dumps(monitoring_config)
            )
            
            # Schedule monitoring tasks
            for test_id in test_ids:
                await self._schedule_monitoring_task(test_id)
            
            return {
                'status': 'monitoring_started',
                'test_count': len(test_ids),
                'monitoring_interval': self.monitoring_interval
            }
            
        except Exception as e:
            logger.error(f"Error starting continuous monitoring: {str(e)}")
            return {'error': str(e)}
    
    async def analyze_test_performance(self, test_id: str) -> Dict[str, Any]:
        """Analyze current test performance and generate optimization recommendations"""
        try:
            logger.info(f"Analyzing performance for test: {test_id}")
            
            # Get current test data
            test_data = await self._get_comprehensive_test_data(test_id)
            
            if not test_data:
                return {'error': 'Test not found or inactive'}
            
            # Perform statistical analysis
            statistical_analysis = await self._perform_statistical_analysis(test_data)
            
            # Detect anomalies and trends
            anomaly_analysis = await self._detect_anomalies(test_data)
            
            # Generate optimization recommendations
            recommendations = await self._generate_optimization_recommendations(
                test_data, statistical_analysis, anomaly_analysis
            )
            
            # Calculate performance metrics
            performance_metrics = await self._calculate_performance_metrics(test_data)
            
            # Risk assessment
            risk_assessment = await self._assess_optimization_risks(test_data, recommendations)
            
            return {
                'test_id': test_id,
                'performance_analysis': {
                    'statistical_analysis': statistical_analysis,
                    'anomaly_analysis': anomaly_analysis,
                    'performance_metrics': performance_metrics,
                    'risk_assessment': risk_assessment
                },
                'recommendations': [asdict(rec) for rec in recommendations],
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing test performance: {str(e)}")
            return {'error': str(e)}
    
    async def execute_optimization(self, test_id: str, 
                                 optimization_recommendation: OptimizationRecommendation) -> OptimizationResult:
        """Execute an optimization recommendation"""
        try:
            logger.info(f"Executing optimization for test {test_id}: {optimization_recommendation.optimization_type.value}")
            
            # Generate unique optimization ID
            optimization_id = f"opt_{uuid.uuid4().hex[:8]}_{int(datetime.utcnow().timestamp())}"
            
            # Get current metrics before optimization
            before_metrics = await self._get_current_test_metrics(test_id)
            
            # Execute optimization based on type
            if optimization_recommendation.optimization_type == OptimizationType.TRAFFIC_REALLOCATION:
                result = await self._execute_traffic_reallocation(
                    test_id, optimization_recommendation
                )
            elif optimization_recommendation.optimization_type == OptimizationType.EARLY_STOPPING:
                result = await self._execute_early_stopping(
                    test_id, optimization_recommendation
                )
            elif optimization_recommendation.optimization_type == OptimizationType.VARIANT_MODIFICATION:
                result = await self._execute_variant_modification(
                    test_id, optimization_recommendation
                )
            elif optimization_recommendation.optimization_type == OptimizationType.SAMPLE_SIZE_ADJUSTMENT:
                result = await self._execute_sample_size_adjustment(
                    test_id, optimization_recommendation
                )
            elif optimization_recommendation.optimization_type == OptimizationType.TARGETING_REFINEMENT:
                result = await self._execute_targeting_refinement(
                    test_id, optimization_recommendation
                )
            else:
                raise ValueError(f"Unsupported optimization type: {optimization_recommendation.optimization_type}")
            
            # Create optimization result
            optimization_result = OptimizationResult(
                optimization_id=optimization_id,
                test_id=test_id,
                optimization_type=optimization_recommendation.optimization_type,
                actions_taken=result['actions_taken'],
                before_metrics=before_metrics,
                expected_after_metrics=result['expected_metrics'],
                success=result['success'],
                error_message=result.get('error_message')
            )
            
            # Record optimization action
            await self._record_optimization_action(optimization_result)
            
            # Update monitoring with optimization
            await self._update_monitoring_with_optimization(test_id, optimization_result)
            
            logger.info(f"Optimization executed successfully: {optimization_id}")
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error executing optimization: {str(e)}")
            return OptimizationResult(
                optimization_id=f"error_{int(datetime.utcnow().timestamp())}",
                test_id=test_id,
                optimization_type=optimization_recommendation.optimization_type,
                actions_taken=[],
                before_metrics={},
                expected_after_metrics={},
                success=False,
                error_message=str(e)
            )
    
    async def get_optimization_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive optimization dashboard"""
        try:
            # Get all monitored tests
            monitored_tests = await self._get_monitored_tests()
            
            dashboard_data = []
            total_optimizations = 0
            active_alerts = []
            
            for test_id in monitored_tests:
                # Get test status
                test_status = await self._get_test_optimization_status(test_id)
                dashboard_data.append(test_status)
                
                total_optimizations += test_status.get('optimizations_count', 0)
                
                # Check for active alerts
                if test_status.get('alerts'):
                    active_alerts.extend(test_status['alerts'])
            
            # Calculate overall system performance
            system_performance = await self._calculate_system_optimization_performance()
            
            return {
                'overview': {
                    'total_monitored_tests': len(monitored_tests),
                    'total_optimizations': total_optimizations,
                    'active_alerts': len(active_alerts),
                    'system_performance_score': system_performance['overall_score']
                },
                'test_details': dashboard_data,
                'active_alerts': active_alerts,
                'system_performance': system_performance,
                'dashboard_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting optimization dashboard: {str(e)}")
            return {'error': str(e)}

    # =============================================================================
    # STATISTICAL ANALYSIS ENGINE
    # =============================================================================

    async def _perform_statistical_analysis(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis on test data"""
        try:
            variants = test_data['variants']
            control_variant = next(v for v in variants if v['is_control'])
            treatment_variants = [v for v in variants if not v['is_control']]
            
            analysis_results = {
                'control_performance': {
                    'conversion_rate': control_variant['conversion_rate'],
                    'sessions': control_variant['sessions'],
                    'conversions': control_variant['conversions']
                },
                'variant_comparisons': [],
                'overall_significance': StatisticalSignificance.NOT_SIGNIFICANT.value,
                'recommended_sample_size': 0,
                'current_power': 0.0,
                'time_to_significance': None
            }
            
            # Analyze each treatment variant against control
            for variant in treatment_variants:
                comparison = await self._compare_variants(control_variant, variant)
                analysis_results['variant_comparisons'].append(comparison)
            
            # Determine overall test significance
            significant_comparisons = [
                comp for comp in analysis_results['variant_comparisons']
                if comp['statistical_significance'] in [
                    StatisticalSignificance.SIGNIFICANT.value,
                    StatisticalSignificance.HIGHLY_SIGNIFICANT.value
                ]
            ]
            
            if significant_comparisons:
                analysis_results['overall_significance'] = StatisticalSignificance.SIGNIFICANT.value
            elif any(comp['statistical_significance'] == StatisticalSignificance.APPROACHING_SIGNIFICANCE.value 
                    for comp in analysis_results['variant_comparisons']):
                analysis_results['overall_significance'] = StatisticalSignificance.APPROACHING_SIGNIFICANCE.value
            
            # Calculate recommended sample size
            analysis_results['recommended_sample_size'] = await self._calculate_recommended_sample_size(
                control_variant['conversion_rate'], 0.05, 0.8, 0.05  # 5% MDE, 80% power, 5% significance
            )
            
            # Calculate current statistical power
            total_sessions = sum(v['sessions'] for v in variants)
            analysis_results['current_power'] = await self._calculate_current_power(
                control_variant['conversion_rate'], total_sessions, len(variants)
            )
            
            # Estimate time to significance
            if analysis_results['overall_significance'] == StatisticalSignificance.NOT_SIGNIFICANT.value:
                current_rate = total_sessions / max(1, (datetime.utcnow() - datetime.fromisoformat(test_data['start_date'])).total_seconds() / 3600)
                remaining_sessions = max(0, analysis_results['recommended_sample_size'] - total_sessions)
                analysis_results['time_to_significance'] = remaining_sessions / max(1, current_rate)
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error performing statistical analysis: {str(e)}")
            return {'error': str(e)}

    async def _compare_variants(self, control: Dict[str, Any], treatment: Dict[str, Any]) -> Dict[str, Any]:
        """Compare treatment variant against control using statistical tests"""
        try:
            # Prepare data for statistical test
            control_successes = control['conversions']
            control_trials = control['sessions']
            treatment_successes = treatment['conversions']
            treatment_trials = treatment['sessions']
            
            # Perform two-proportion z-test
            if control_trials > 0 and treatment_trials > 0:
                # Calculate pooled proportion
                pooled_p = (control_successes + treatment_successes) / (control_trials + treatment_trials)
                
                # Calculate standard error
                se = np.sqrt(pooled_p * (1 - pooled_p) * (1/control_trials + 1/treatment_trials))
                
                # Calculate z-score
                p1 = control_successes / control_trials
                p2 = treatment_successes / treatment_trials
                z_score = (p2 - p1) / se if se > 0 else 0
                
                # Calculate p-value (two-tailed test)
                p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
                
                # Calculate confidence interval for difference
                diff = p2 - p1
                margin_error = 1.96 * se  # 95% confidence interval
                ci_lower = diff - margin_error
                ci_upper = diff + margin_error
                
                # Determine statistical significance
                if p_value < 0.01:
                    significance = StatisticalSignificance.HIGHLY_SIGNIFICANT.value
                elif p_value < 0.05:
                    significance = StatisticalSignificance.SIGNIFICANT.value
                elif p_value < 0.2:
                    significance = StatisticalSignificance.APPROACHING_SIGNIFICANCE.value
                else:
                    significance = StatisticalSignificance.NOT_SIGNIFICANT.value
                
                # Calculate effect size (relative improvement)
                relative_improvement = (p2 - p1) / p1 if p1 > 0 else 0
                
                return {
                    'variant_id': treatment['variant_id'],
                    'control_conversion_rate': p1,
                    'treatment_conversion_rate': p2,
                    'absolute_difference': diff,
                    'relative_improvement': relative_improvement,
                    'statistical_significance': significance,
                    'p_value': p_value,
                    'z_score': z_score,
                    'confidence_interval': {'lower': ci_lower, 'upper': ci_upper},
                    'sample_sizes': {'control': control_trials, 'treatment': treatment_trials}
                }
            else:
                return {
                    'variant_id': treatment['variant_id'],
                    'error': 'Insufficient data for statistical comparison'
                }
                
        except Exception as e:
            logger.error(f"Error comparing variants: {str(e)}")
            return {
                'variant_id': treatment.get('variant_id', 'unknown'),
                'error': str(e)
            }

    async def _calculate_recommended_sample_size(self, baseline_rate: float, 
                                               min_detectable_effect: float,
                                               power: float, 
                                               significance: float) -> int:
        """Calculate recommended sample size for test"""
        try:
            # Use standard sample size calculation for two-proportion test
            alpha = significance
            beta = 1 - power
            
            p1 = baseline_rate
            p2 = baseline_rate * (1 + min_detectable_effect)
            
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = stats.norm.ppf(power)
            
            p_pooled = (p1 + p2) / 2
            
            numerator = (z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) + 
                        z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
            denominator = (p2 - p1) ** 2
            
            sample_size_per_variant = numerator / denominator if denominator > 0 else 1000
            
            return int(np.ceil(sample_size_per_variant))
            
        except Exception as e:
            logger.error(f"Error calculating sample size: {str(e)}")
            return 1000  # Default fallback

    # =============================================================================
    # OPTIMIZATION EXECUTION METHODS
    # =============================================================================

    async def _execute_traffic_reallocation(self, test_id: str, 
                                          recommendation: OptimizationRecommendation) -> Dict[str, Any]:
        """Execute traffic reallocation optimization"""
        try:
            # Get current traffic allocation
            current_allocation = await self._get_current_traffic_allocation(test_id)
            
            # Calculate new allocation based on performance
            new_allocation = await self._calculate_optimal_traffic_allocation(test_id, recommendation)
            
            # Validate allocation constraints
            validated_allocation = await self._validate_traffic_allocation(current_allocation, new_allocation)
            
            # Update traffic allocation
            success = await self._update_traffic_allocation(test_id, validated_allocation)
            
            if success:
                actions_taken = [
                    f"Reallocated traffic from {current_allocation} to {validated_allocation}",
                    "Updated routing configuration",
                    "Notified monitoring systems"
                ]
                
                expected_metrics = await self._predict_metrics_after_reallocation(
                    test_id, validated_allocation
                )
                
                return {
                    'success': True,
                    'actions_taken': actions_taken,
                    'expected_metrics': expected_metrics
                }
            else:
                return {
                    'success': False,
                    'actions_taken': [],
                    'expected_metrics': {},
                    'error_message': 'Failed to update traffic allocation'
                }
                
        except Exception as e:
            logger.error(f"Error executing traffic reallocation: {str(e)}")
            return {
                'success': False,
                'actions_taken': [],
                'expected_metrics': {},
                'error_message': str(e)
            }

    async def _execute_early_stopping(self, test_id: str, 
                                    recommendation: OptimizationRecommendation) -> Dict[str, Any]:
        """Execute early stopping optimization"""
        try:
            # Get test configuration
            test_config = await self._get_test_configuration(test_id)
            
            if not test_config:
                return {
                    'success': False,
                    'actions_taken': [],
                    'expected_metrics': {},
                    'error_message': 'Test configuration not found'
                }
            
            # Determine winning variant
            winning_variant = await self._determine_winning_variant(test_id)
            
            # Stop test and declare winner
            success = await self._stop_test_with_winner(test_id, winning_variant)
            
            if success:
                actions_taken = [
                    f"Stopped test early due to statistical significance",
                    f"Declared variant {winning_variant['variant_id']} as winner",
                    "Updated test status to completed",
                    "Generated final test report",
                    "Initiated winner rollout process"
                ]
                
                expected_metrics = {
                    'test_completion_time_saved': recommendation.expected_impact.get('time_saved', 0),
                    'additional_conversions_expected': recommendation.expected_impact.get('conversion_lift', 0),
                    'confidence_level': winning_variant.get('confidence', 0)
                }
                
                return {
                    'success': True,
                    'actions_taken': actions_taken,
                    'expected_metrics': expected_metrics
                }
            else:
                return {
                    'success': False,
                    'actions_taken': [],
                    'expected_metrics': {},
                    'error_message': 'Failed to stop test'
                }
                
        except Exception as e:
            logger.error(f"Error executing early stopping: {str(e)}")
            return {
                'success': False,
                'actions_taken': [],
                'expected_metrics': {},
                'error_message': str(e)
            }

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    async def _get_comprehensive_test_data(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive test data for analysis"""
        try:
            # Get test configuration
            test_config = await self._get_test_configuration(test_id)
            
            if not test_config:
                return None
            
            # Get performance data for all variants
            variants_data = []
            
            for variant in test_config.get('variants', []):
                variant_metrics = await self._get_variant_metrics(test_id, variant['variant_id'])
                variants_data.append({
                    'variant_id': variant['variant_id'],
                    'variant_name': variant.get('variant_name', variant['variant_id']),
                    'is_control': variant.get('is_control', False),
                    'traffic_allocation': variant.get('traffic_allocation', 0),
                    **variant_metrics
                })
            
            return {
                'test_id': test_id,
                'test_name': test_config.get('test_name', ''),
                'test_type': test_config.get('test_type', ''),
                'start_date': test_config.get('start_date', ''),
                'variants': variants_data,
                'target_sample_size': test_config.get('target_sample_size', 1000)
            }
            
        except Exception as e:
            logger.error(f"Error getting comprehensive test data: {str(e)}")
            return None

    async def _get_variant_metrics(self, test_id: str, variant_id: str) -> Dict[str, Any]:
        """Get current metrics for a specific variant"""
        try:
            # Get session count
            session_key = f"ab_sessions:{test_id}:{variant_id}"
            sessions = await self.redis_client.get(session_key)
            sessions_count = int(sessions) if sessions else 0
            
            # Get conversion count
            conversion_key = f"ab_conversions:{test_id}:{variant_id}"
            conversions = await self.redis_client.get(conversion_key)
            conversions_count = int(conversions) if conversions else 0
            
            # Calculate conversion rate
            conversion_rate = conversions_count / sessions_count if sessions_count > 0 else 0
            
            # Get additional metrics
            metrics_key = f"ab_metrics:{test_id}:{variant_id}"
            metrics_data = await self.redis_client.get(metrics_key)
            
            if metrics_data:
                metrics = json.loads(metrics_data)
            else:
                metrics = {}
            
            return {
                'sessions': sessions_count,
                'conversions': conversions_count,
                'conversion_rate': conversion_rate,
                'click_through_rate': metrics.get('click_through_rate', 0),
                'engagement_time': metrics.get('engagement_time', 0),
                'bounce_rate': metrics.get('bounce_rate', 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting variant metrics: {str(e)}")
            return {
                'sessions': 0,
                'conversions': 0,
                'conversion_rate': 0,
                'click_through_rate': 0,
                'engagement_time': 0,
                'bounce_rate': 0
            }

    async def _get_test_configuration(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get test configuration from cache or database"""
        try:
            config_key = f"ab_test_config:{test_id}"
            config_data = await self.redis_client.get(config_key)
            
            if config_data:
                return json.loads(config_data)
            
            return None
        except Exception as e:
            logger.error(f"Error getting test configuration: {str(e)}")
            return None

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'RealTimeOptimizationEngine',
    'OptimizationRecommendation',
    'OptimizationResult',
    'PerformanceMonitoringData',
    'OptimizationType',
    'OptimizationTrigger',
    'OptimizationDecision'
]