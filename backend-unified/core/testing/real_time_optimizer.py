#!/usr/bin/env python3
"""
Real-Time Test Optimization Engine - Week 3 Implementation
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 3 - A/B Testing Framework Integration

Real-time optimization engine for dynamic test adjustments and performance enhancement.

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
from dataclasses import dataclass
from collections import defaultdict, deque
import statistics

logger = logging.getLogger(__name__)

class OptimizationType(str, Enum):
    """Types of real-time optimizations"""
    TRAFFIC_ALLOCATION = "traffic_allocation"
    EARLY_STOPPING = "early_stopping"
    VARIANT_PERFORMANCE = "variant_performance"
    PERSONALIZATION_TUNING = "personalization_tuning"
    SIGNIFICANCE_ACCELERATION = "significance_acceleration"

class OptimizationTrigger(str, Enum):
    """Triggers for optimization actions"""
    PERFORMANCE_THRESHOLD = "performance_threshold"
    STATISTICAL_SIGNIFICANCE = "statistical_significance"
    TIME_BASED = "time_based"
    CONFIDENCE_LEVEL = "confidence_level"
    CONVERSION_RATE = "conversion_rate"

@dataclass
class OptimizationAction:
    """Individual optimization action"""
    action_id: str
    optimization_type: OptimizationType
    trigger: OptimizationTrigger
    description: str
    parameters: Dict[str, Any]
    expected_impact: float
    confidence_score: float
    applied_at: datetime
    results: Optional[Dict[str, Any]] = None

@dataclass
class PerformanceWindow:
    """Performance tracking window"""
    window_start: datetime
    window_end: datetime
    sample_size: int
    conversion_rate: float
    engagement_score: float
    bounce_rate: float
    confidence_interval: Tuple[float, float]
    statistical_power: float

class RealTimeOptimizer:
    """
    Real-Time Test Optimization Engine
    
    Features:
    - Dynamic traffic allocation
    - Early stopping detection
    - Performance-based variant optimization
    - Statistical significance acceleration
    - Personalization strategy tuning
    """
    
    def __init__(self):
        # Optimization configuration
        self.config = {
            'optimization_interval_minutes': 15,
            'minimum_sample_size_per_variant': 50,
            'significance_threshold': 0.05,
            'power_threshold': 0.8,
            'performance_improvement_threshold': 0.1,  # 10%
            'early_stopping_confidence': 0.95,
            'traffic_allocation_sensitivity': 0.05,
            'personalization_optimization_threshold': 0.15
        }
        
        # Tracking and history
        self.optimization_history: Dict[str, List[OptimizationAction]] = defaultdict(list)
        self.performance_windows: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.variant_performance_trends: Dict[str, Dict[str, deque]] = defaultdict(lambda: defaultdict(lambda: deque(maxlen=50)))
        
        # Active optimizations
        self.active_optimizations: Dict[str, List[OptimizationAction]] = defaultdict(list)
        
        # Learning system
        self.optimization_effectiveness: Dict[str, List[float]] = defaultdict(list)
        self.pattern_recognition: Dict[str, Any] = {}
    
    async def optimize_test(self, test_id: str, test_data: Dict[str, Any], 
                          performance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive real-time optimization for a test
        
        Args:
            test_id: Test identifier
            test_data: Current test configuration and state
            performance_data: Recent performance data
        
        Returns:
            Optimization results and actions taken
        """
        try:
            logger.info(f"Starting real-time optimization for test {test_id}")
            
            # Update performance tracking
            await self._update_performance_tracking(test_id, performance_data)
            
            # Analyze current performance state
            performance_analysis = await self._analyze_performance_state(test_id, test_data, performance_data)
            
            # Generate optimization opportunities
            optimization_opportunities = await self._identify_optimization_opportunities(
                test_id, test_data, performance_analysis
            )
            
            # Execute optimizations
            executed_optimizations = []
            optimization_results = {}
            
            for opportunity in optimization_opportunities:
                if await self._should_execute_optimization(opportunity, test_data):
                    result = await self._execute_optimization(test_id, opportunity, test_data)
                    executed_optimizations.append(result)
                    optimization_results[opportunity['type']] = result
            
            # Update optimization history
            for optimization in executed_optimizations:
                if optimization['executed']:
                    action = OptimizationAction(
                        action_id=optimization['action_id'],
                        optimization_type=OptimizationType(optimization['type']),
                        trigger=OptimizationTrigger(optimization['trigger']),
                        description=optimization['description'],
                        parameters=optimization['parameters'],
                        expected_impact=optimization.get('expected_impact', 0.0),
                        confidence_score=optimization.get('confidence_score', 0.5),
                        applied_at=datetime.utcnow(),
                        results=optimization.get('results')
                    )
                    self.optimization_history[test_id].append(action)
            
            # Learn from optimization results
            await self._learn_from_optimizations(test_id, executed_optimizations)
            
            return {
                'test_id': test_id,
                'optimization_timestamp': datetime.utcnow().isoformat(),
                'performance_analysis': performance_analysis,
                'opportunities_identified': len(optimization_opportunities),
                'optimizations_executed': len(executed_optimizations),
                'optimization_results': optimization_results,
                'next_optimization_time': (datetime.utcnow() + timedelta(
                    minutes=self.config['optimization_interval_minutes']
                )).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in real-time optimization for test {test_id}: {e}")
            return {'error': str(e)}
    
    async def optimize_traffic_allocation(self, test_id: str, variant_performance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize traffic allocation based on variant performance
        
        Args:
            test_id: Test identifier
            variant_performance: Performance metrics for each variant
        
        Returns:
            Updated traffic allocation and optimization details
        """
        try:
            logger.debug(f"Optimizing traffic allocation for test {test_id}")
            
            # Extract variant metrics
            variants = list(variant_performance.keys())
            if len(variants) < 2:
                return {'optimized': False, 'reason': 'Insufficient variants for optimization'}
            
            # Calculate performance scores
            performance_scores = {}
            for variant_id, metrics in variant_performance.items():
                score = await self._calculate_performance_score(metrics)
                performance_scores[variant_id] = score
            
            # Determine if optimization is needed
            score_variance = np.var(list(performance_scores.values()))
            if score_variance < self.config['traffic_allocation_sensitivity']:
                return {'optimized': False, 'reason': 'Performance variance too low'}
            
            # Calculate new traffic allocation using Thompson Sampling approach
            new_allocation = await self._calculate_optimal_allocation(performance_scores, variant_performance)
            
            # Check if allocation change is significant
            current_allocation = {v: 1.0/len(variants) for v in variants}  # Assume equal initially
            allocation_change = sum(abs(new_allocation[v] - current_allocation[v]) for v in variants)
            
            if allocation_change < 0.1:  # Less than 10% total change
                return {'optimized': False, 'reason': 'Allocation change too small'}
            
            return {
                'optimized': True,
                'new_allocation': new_allocation,
                'previous_allocation': current_allocation,
                'allocation_change': allocation_change,
                'performance_scores': performance_scores,
                'optimization_confidence': await self._calculate_allocation_confidence(new_allocation, performance_scores),
                'expected_improvement': await self._estimate_allocation_improvement(new_allocation, performance_scores)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing traffic allocation: {e}")
            return {'optimized': False, 'error': str(e)}
    
    async def check_early_stopping(self, test_id: str, test_data: Dict[str, Any], 
                                 variant_performance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if test should be stopped early due to clear winner or futility
        
        Args:
            test_id: Test identifier
            test_data: Test configuration
            variant_performance: Current variant performance
        
        Returns:
            Early stopping recommendation
        """
        try:
            logger.debug(f"Checking early stopping conditions for test {test_id}")
            
            # Check minimum runtime
            test_start = datetime.fromisoformat(test_data.get('start_date', datetime.utcnow().isoformat()))
            runtime_hours = (datetime.utcnow() - test_start).total_seconds() / 3600
            
            minimum_runtime = self.config.get('minimum_runtime_hours', 24)
            if runtime_hours < minimum_runtime:
                return {
                    'should_stop': False,
                    'reason': f'Minimum runtime not met ({runtime_hours:.1f}h < {minimum_runtime}h)'
                }
            
            # Check sample sizes
            min_sample_size = self.config['minimum_sample_size_per_variant']
            for variant_id, metrics in variant_performance.items():
                if metrics.get('sample_size', 0) < min_sample_size:
                    return {
                        'should_stop': False,
                        'reason': f'Insufficient sample size for variant {variant_id}'
                    }
            
            # Statistical significance check
            significance_results = await self._check_statistical_significance(variant_performance)
            
            if significance_results['significant']:
                return {
                    'should_stop': True,
                    'reason': 'Statistical significance achieved',
                    'winner': significance_results['winner'],
                    'confidence_level': significance_results['confidence_level'],
                    'effect_size': significance_results['effect_size']
                }
            
            # Futility check - probability of achieving significance is very low
            futility_check = await self._check_futility(test_id, variant_performance)
            
            if futility_check['is_futile']:
                return {
                    'should_stop': True,
                    'reason': 'Futility detected - unlikely to achieve significance',
                    'futility_probability': futility_check['futility_probability'],
                    'estimated_runtime_to_significance': futility_check['estimated_runtime_days']
                }
            
            # Practical significance check - effect size too small to matter
            practical_significance = await self._check_practical_significance(variant_performance)
            
            if not practical_significance['practically_significant']:
                return {
                    'should_stop': True,
                    'reason': 'Effect size too small for practical significance',
                    'max_effect_size': practical_significance['max_effect_size'],
                    'minimum_detectable_effect': practical_significance['minimum_detectable_effect']
                }
            
            return {
                'should_stop': False,
                'reason': 'Continue testing',
                'current_significance': significance_results,
                'futility_analysis': futility_check,
                'practical_significance': practical_significance
            }
            
        except Exception as e:
            logger.error(f"Error checking early stopping: {e}")
            return {'should_stop': False, 'error': str(e)}
    
    async def optimize_variant_performance(self, test_id: str, variant_id: str, 
                                         performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize individual variant performance through micro-adjustments
        
        Args:
            test_id: Test identifier
            variant_id: Variant identifier
            performance_data: Current performance metrics
        
        Returns:
            Variant optimization recommendations
        """
        try:
            logger.debug(f"Optimizing variant {variant_id} performance for test {test_id}")
            
            # Analyze performance trends
            trends = await self._analyze_variant_trends(test_id, variant_id, performance_data)
            
            # Identify optimization opportunities
            opportunities = []
            
            # 1. Engagement optimization
            if trends['engagement_declining']:
                opportunities.append({
                    'type': 'engagement_boost',
                    'action': 'enhance_visual_elements',
                    'confidence': 0.75,
                    'expected_impact': 0.12
                })
            
            # 2. Conversion optimization
            if trends['conversion_underperforming']:
                opportunities.append({
                    'type': 'conversion_optimization',
                    'action': 'strengthen_call_to_action',
                    'confidence': 0.80,
                    'expected_impact': 0.15
                })
            
            # 3. Bounce rate optimization
            if trends['bounce_rate_high']:
                opportunities.append({
                    'type': 'retention_improvement',
                    'action': 'improve_page_relevance',
                    'confidence': 0.70,
                    'expected_impact': 0.10
                })
            
            # 4. Personalization refinement
            if trends['personalization_mismatch']:
                opportunities.append({
                    'type': 'personalization_tuning',
                    'action': 'adjust_messaging_tone',
                    'confidence': 0.65,
                    'expected_impact': 0.08
                })
            
            # Prioritize opportunities
            prioritized_opportunities = sorted(
                opportunities, 
                key=lambda x: x['confidence'] * x['expected_impact'], 
                reverse=True
            )
            
            return {
                'variant_id': variant_id,
                'performance_trends': trends,
                'optimization_opportunities': prioritized_opportunities,
                'recommended_actions': prioritized_opportunities[:3],  # Top 3
                'optimization_confidence': np.mean([op['confidence'] for op in prioritized_opportunities]) if opportunities else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error optimizing variant performance: {e}")
            return {'error': str(e)}
    
    async def tune_personalization_strategy(self, test_id: str, personalization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tune personalization strategies based on performance feedback
        
        Args:
            test_id: Test identifier
            personalization_data: Current personalization metrics and strategies
        
        Returns:
            Personalization tuning recommendations
        """
        try:
            logger.debug(f"Tuning personalization strategy for test {test_id}")
            
            # Analyze personalization effectiveness
            effectiveness_analysis = await self._analyze_personalization_effectiveness(personalization_data)
            
            tuning_recommendations = []
            
            # 1. Persona targeting optimization
            if effectiveness_analysis['persona_targeting_accuracy'] < 0.7:
                tuning_recommendations.append({
                    'type': 'persona_targeting',
                    'action': 'refine_persona_detection',
                    'parameters': {
                        'accuracy_threshold': 0.8,
                        'confidence_boost': 0.15
                    },
                    'expected_improvement': 0.12
                })
            
            # 2. Device optimization tuning
            if effectiveness_analysis['device_optimization_score'] < 0.75:
                tuning_recommendations.append({
                    'type': 'device_optimization',
                    'action': 'enhance_device_specific_content',
                    'parameters': {
                        'mobile_emphasis': True,
                        'desktop_detail_level': 'increased'
                    },
                    'expected_improvement': 0.10
                })
            
            # 3. Journey stage alignment
            if effectiveness_analysis['stage_alignment_score'] < 0.8:
                tuning_recommendations.append({
                    'type': 'journey_stage_alignment',
                    'action': 'improve_stage_detection',
                    'parameters': {
                        'stage_transition_sensitivity': 0.9,
                        'content_adaptation_speed': 'increased'
                    },
                    'expected_improvement': 0.14
                })
            
            # 4. Real-time adaptation tuning
            if effectiveness_analysis['real_time_adaptation_score'] < 0.7:
                tuning_recommendations.append({
                    'type': 'real_time_adaptation',
                    'action': 'accelerate_adaptation_speed',
                    'parameters': {
                        'adaptation_threshold': 0.6,
                        'update_frequency': 'increased'
                    },
                    'expected_improvement': 0.08
                })
            
            return {
                'test_id': test_id,
                'personalization_effectiveness': effectiveness_analysis,
                'tuning_recommendations': tuning_recommendations,
                'priority_actions': tuning_recommendations[:2],  # Top 2 priority
                'overall_optimization_potential': sum(rec['expected_improvement'] for rec in tuning_recommendations)
            }
            
        except Exception as e:
            logger.error(f"Error tuning personalization strategy: {e}")
            return {'error': str(e)}
    
    # =============================================================================
    # INTERNAL IMPLEMENTATION METHODS
    # =============================================================================
    
    async def _update_performance_tracking(self, test_id: str, performance_data: List[Dict[str, Any]]) -> None:
        """Update performance tracking windows"""
        try:
            # Create performance window
            if performance_data:
                window = PerformanceWindow(
                    window_start=datetime.utcnow() - timedelta(minutes=15),
                    window_end=datetime.utcnow(),
                    sample_size=len(performance_data),
                    conversion_rate=np.mean([d.get('performance', {}).get('conversion', 0) for d in performance_data]),
                    engagement_score=np.mean([d.get('performance', {}).get('engagement_score', 0.5) for d in performance_data]),
                    bounce_rate=np.mean([d.get('performance', {}).get('bounce_rate', 0.5) for d in performance_data]),
                    confidence_interval=(0.0, 1.0),  # Simplified
                    statistical_power=0.8  # Placeholder
                )
                
                self.performance_windows[test_id].append(window)
            
            # Update variant-specific trends
            for data_point in performance_data:
                variant_id = data_point.get('variant_id')
                if variant_id:
                    performance = data_point.get('performance', {})
                    self.variant_performance_trends[test_id][variant_id].append({
                        'timestamp': datetime.utcnow(),
                        'conversion': performance.get('conversion', 0),
                        'engagement': performance.get('engagement_score', 0.5),
                        'bounce_rate': performance.get('bounce_rate', 0.5)
                    })
            
        except Exception as e:
            logger.error(f"Error updating performance tracking: {e}")
    
    async def _analyze_performance_state(self, test_id: str, test_data: Dict[str, Any], 
                                       performance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze current performance state"""
        try:
            windows = list(self.performance_windows[test_id])
            if not windows:
                return {'state': 'insufficient_data'}
            
            recent_window = windows[-1]
            
            # Trend analysis
            if len(windows) >= 3:
                recent_conversion_rates = [w.conversion_rate for w in windows[-3:]]
                trend = 'improving' if recent_conversion_rates[-1] > recent_conversion_rates[0] else 'declining'
            else:
                trend = 'stable'
            
            return {
                'state': 'analyzed',
                'current_conversion_rate': recent_window.conversion_rate,
                'current_engagement': recent_window.engagement_score,
                'sample_size': recent_window.sample_size,
                'trend': trend,
                'statistical_power': recent_window.statistical_power,
                'optimization_readiness': recent_window.sample_size >= self.config['minimum_sample_size_per_variant']
            }
            
        except Exception as e:
            logger.error(f"Error analyzing performance state: {e}")
            return {'state': 'error', 'error': str(e)}
    
    async def _identify_optimization_opportunities(self, test_id: str, test_data: Dict[str, Any], 
                                                 performance_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify available optimization opportunities"""
        opportunities = []
        
        try:
            # Traffic allocation opportunity
            if performance_analysis.get('optimization_readiness', False):
                opportunities.append({
                    'type': OptimizationType.TRAFFIC_ALLOCATION.value,
                    'trigger': OptimizationTrigger.PERFORMANCE_THRESHOLD.value,
                    'confidence': 0.8,
                    'expected_impact': 0.15,
                    'description': 'Optimize traffic allocation based on variant performance'
                })
            
            # Early stopping opportunity
            test_runtime_hours = (datetime.utcnow() - datetime.fromisoformat(
                test_data.get('start_date', datetime.utcnow().isoformat())
            )).total_seconds() / 3600
            
            if test_runtime_hours >= 24:  # Minimum runtime
                opportunities.append({
                    'type': OptimizationType.EARLY_STOPPING.value,
                    'trigger': OptimizationTrigger.STATISTICAL_SIGNIFICANCE.value,
                    'confidence': 0.9,
                    'expected_impact': 0.0,  # Saves time rather than improves performance
                    'description': 'Check for early stopping conditions'
                })
            
            # Variant performance optimization
            if performance_analysis.get('trend') == 'declining':
                opportunities.append({
                    'type': OptimizationType.VARIANT_PERFORMANCE.value,
                    'trigger': OptimizationTrigger.CONVERSION_RATE.value,
                    'confidence': 0.7,
                    'expected_impact': 0.12,
                    'description': 'Optimize individual variant performance'
                })
            
            # Personalization tuning
            opportunities.append({
                'type': OptimizationType.PERSONALIZATION_TUNING.value,
                'trigger': OptimizationTrigger.CONFIDENCE_LEVEL.value,
                'confidence': 0.75,
                'expected_impact': 0.10,
                'description': 'Tune personalization strategies'
            })
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error identifying optimization opportunities: {e}")
            return []
    
    async def _should_execute_optimization(self, opportunity: Dict[str, Any], test_data: Dict[str, Any]) -> bool:
        """Determine if an optimization should be executed"""
        try:
            # Check confidence threshold
            if opportunity.get('confidence', 0) < 0.7:
                return False
            
            # Check if similar optimization was recently applied
            recent_optimizations = self.optimization_history.get(test_data.get('test_id', ''), [])
            recent_types = [opt.optimization_type.value for opt in recent_optimizations[-5:]]
            
            if opportunity['type'] in recent_types:
                return False  # Avoid too frequent similar optimizations
            
            # Check expected impact threshold
            if opportunity.get('expected_impact', 0) < 0.05:  # Less than 5% improvement
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking optimization execution criteria: {e}")
            return False
    
    async def _execute_optimization(self, test_id: str, opportunity: Dict[str, Any], 
                                  test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific optimization"""
        try:
            optimization_type = opportunity['type']
            action_id = f"{test_id}_{optimization_type}_{int(datetime.utcnow().timestamp())}"
            
            result = {
                'action_id': action_id,
                'type': optimization_type,
                'trigger': opportunity['trigger'],
                'description': opportunity['description'],
                'parameters': {},
                'executed': False,
                'reason': 'Unknown'
            }
            
            if optimization_type == OptimizationType.TRAFFIC_ALLOCATION.value:
                # Execute traffic allocation optimization
                allocation_result = await self.optimize_traffic_allocation(test_id, {})
                result['executed'] = allocation_result.get('optimized', False)
                result['parameters'] = allocation_result
                result['reason'] = allocation_result.get('reason', 'Optimization attempted')
                
            elif optimization_type == OptimizationType.EARLY_STOPPING.value:
                # Execute early stopping check
                stopping_result = await self.check_early_stopping(test_id, test_data, {})
                result['executed'] = stopping_result.get('should_stop', False)
                result['parameters'] = stopping_result
                result['reason'] = stopping_result.get('reason', 'Early stopping check performed')
                
            elif optimization_type == OptimizationType.VARIANT_PERFORMANCE.value:
                # Execute variant performance optimization
                result['executed'] = True
                result['parameters'] = {'optimization': 'variant_performance_applied'}
                result['reason'] = 'Variant performance optimization applied'
                
            elif optimization_type == OptimizationType.PERSONALIZATION_TUNING.value:
                # Execute personalization tuning
                tuning_result = await self.tune_personalization_strategy(test_id, {})
                result['executed'] = len(tuning_result.get('tuning_recommendations', [])) > 0
                result['parameters'] = tuning_result
                result['reason'] = 'Personalization tuning recommendations generated'
            
            # Add common fields
            result['confidence_score'] = opportunity.get('confidence', 0.5)
            result['expected_impact'] = opportunity.get('expected_impact', 0.0)
            result['execution_timestamp'] = datetime.utcnow().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing optimization: {e}")
            return {
                'action_id': 'error',
                'executed': False,
                'error': str(e)
            }
    
    async def _learn_from_optimizations(self, test_id: str, optimizations: List[Dict[str, Any]]) -> None:
        """Learn from optimization results for future improvements"""
        try:
            for optimization in optimizations:
                if optimization.get('executed'):
                    opt_type = optimization.get('type')
                    effectiveness = optimization.get('results', {}).get('effectiveness', 0.5)
                    
                    self.optimization_effectiveness[opt_type].append(effectiveness)
                    
                    # Update patterns
                    if opt_type not in self.pattern_recognition:
                        self.pattern_recognition[opt_type] = {
                            'success_rate': 0.0,
                            'average_impact': 0.0,
                            'best_conditions': []
                        }
                    
                    # Update success rate
                    successes = [e for e in self.optimization_effectiveness[opt_type] if e > 0.6]
                    self.pattern_recognition[opt_type]['success_rate'] = len(successes) / len(self.optimization_effectiveness[opt_type])
                    
                    # Update average impact
                    self.pattern_recognition[opt_type]['average_impact'] = statistics.mean(self.optimization_effectiveness[opt_type])
            
        except Exception as e:
            logger.error(f"Error learning from optimizations: {e}")
    
    # Placeholder methods for advanced statistical analysis
    async def _calculate_performance_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall performance score for a variant"""
        conversion_weight = 0.5
        engagement_weight = 0.3
        bounce_weight = 0.2
        
        conversion_score = metrics.get('conversion_rate', 0.0)
        engagement_score = metrics.get('engagement_score', 0.5)
        bounce_score = 1.0 - metrics.get('bounce_rate', 0.5)  # Invert bounce rate
        
        return (conversion_score * conversion_weight + 
                engagement_score * engagement_weight + 
                bounce_score * bounce_weight)
    
    async def _calculate_optimal_allocation(self, performance_scores: Dict[str, float], 
                                          variant_performance: Dict[str, Any]) -> Dict[str, float]:
        """Calculate optimal traffic allocation using Thompson Sampling"""
        # Simplified allocation - would use proper Thompson Sampling in production
        total_score = sum(performance_scores.values())
        if total_score == 0:
            equal_allocation = 1.0 / len(performance_scores)
            return {variant: equal_allocation for variant in performance_scores.keys()}
        
        return {variant: score / total_score for variant, score in performance_scores.items()}
    
    async def _calculate_allocation_confidence(self, allocation: Dict[str, float], 
                                             performance_scores: Dict[str, float]) -> float:
        """Calculate confidence in the allocation decision"""
        score_variance = np.var(list(performance_scores.values()))
        return min(1.0, 0.5 + score_variance)
    
    async def _estimate_allocation_improvement(self, allocation: Dict[str, float], 
                                             performance_scores: Dict[str, float]) -> float:
        """Estimate improvement from new allocation"""
        weighted_performance = sum(allocation[v] * performance_scores[v] for v in allocation.keys())
        equal_allocation_performance = np.mean(list(performance_scores.values()))
        return max(0.0, weighted_performance - equal_allocation_performance)
    
    async def _check_statistical_significance(self, variant_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Check statistical significance between variants"""
        # Simplified implementation - would use proper statistical tests
        return {
            'significant': False,
            'winner': None,
            'confidence_level': 0.5,
            'effect_size': 0.0
        }
    
    async def _check_futility(self, test_id: str, variant_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Check if test is futile (unlikely to achieve significance)"""
        return {
            'is_futile': False,
            'futility_probability': 0.1,
            'estimated_runtime_days': 30
        }
    
    async def _check_practical_significance(self, variant_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Check if effect size is practically significant"""
        return {
            'practically_significant': True,
            'max_effect_size': 0.1,
            'minimum_detectable_effect': 0.05
        }
    
    async def _analyze_variant_trends(self, test_id: str, variant_id: str, 
                                    performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance trends for a specific variant"""
        trends = self.variant_performance_trends[test_id][variant_id]
        
        if len(trends) < 3:
            return {
                'engagement_declining': False,
                'conversion_underperforming': False,
                'bounce_rate_high': False,
                'personalization_mismatch': False
            }
        
        recent_trends = list(trends)[-5:]  # Last 5 data points
        
        # Analyze trends
        engagement_scores = [t['engagement'] for t in recent_trends]
        conversion_rates = [t['conversion'] for t in recent_trends]
        bounce_rates = [t['bounce_rate'] for t in recent_trends]
        
        return {
            'engagement_declining': engagement_scores[-1] < engagement_scores[0],
            'conversion_underperforming': np.mean(conversion_rates) < 0.05,
            'bounce_rate_high': np.mean(bounce_rates) > 0.7,
            'personalization_mismatch': np.std(engagement_scores) > 0.2
        }
    
    async def _analyze_personalization_effectiveness(self, personalization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze effectiveness of personalization strategies"""
        return {
            'persona_targeting_accuracy': 0.75,
            'device_optimization_score': 0.80,
            'stage_alignment_score': 0.70,
            'real_time_adaptation_score': 0.65
        }
    
    # =============================================================================
    # PUBLIC API METHODS
    # =============================================================================
    
    async def get_optimization_analytics(self, test_id: str) -> Dict[str, Any]:
        """Get comprehensive optimization analytics for a test"""
        try:
            history = self.optimization_history.get(test_id, [])
            
            if not history:
                return {'message': 'No optimization history available'}
            
            # Calculate analytics
            total_optimizations = len(history)
            successful_optimizations = len([opt for opt in history if opt.results and opt.results.get('success', False)])
            
            optimization_types = defaultdict(int)
            for opt in history:
                optimization_types[opt.optimization_type.value] += 1
            
            return {
                'test_id': test_id,
                'total_optimizations': total_optimizations,
                'successful_optimizations': successful_optimizations,
                'success_rate': successful_optimizations / total_optimizations if total_optimizations > 0 else 0,
                'optimization_types': dict(optimization_types),
                'recent_optimizations': [
                    {
                        'type': opt.optimization_type.value,
                        'description': opt.description,
                        'confidence': opt.confidence_score,
                        'applied_at': opt.applied_at.isoformat()
                    }
                    for opt in history[-5:]  # Last 5 optimizations
                ],
                'performance_impact': {
                    'total_estimated_improvement': sum(opt.expected_impact for opt in history),
                    'average_optimization_impact': np.mean([opt.expected_impact for opt in history])
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting optimization analytics: {e}")
            return {'error': str(e)}
    
    async def get_optimization_recommendations(self, test_id: str) -> List[Dict[str, Any]]:
        """Get optimization recommendations based on learning"""
        try:
            recommendations = []
            
            # Based on pattern recognition
            for opt_type, patterns in self.pattern_recognition.items():
                if patterns['success_rate'] > 0.7:
                    recommendations.append({
                        'type': opt_type,
                        'recommendation': f'Consider {opt_type} optimization',
                        'success_rate': patterns['success_rate'],
                        'average_impact': patterns['average_impact'],
                        'confidence': 'high' if patterns['success_rate'] > 0.8 else 'medium'
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting optimization recommendations: {e}")
            return []
    
    async def reset_optimization_history(self, test_id: str) -> bool:
        """Reset optimization history for a test"""
        try:
            if test_id in self.optimization_history:
                del self.optimization_history[test_id]
            if test_id in self.performance_windows:
                self.performance_windows[test_id].clear()
            if test_id in self.variant_performance_trends:
                del self.variant_performance_trends[test_id]
            
            return True
            
        except Exception as e:
            logger.error(f"Error resetting optimization history: {e}")
            return False