# Cross-Test Learning Engine - Week 3 Implementation
# Module: 3A - Week 3 - Cross-Test Learning and Intelligence System
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
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_

from .models import *
from .database_models import JourneySession, PersonalizationData
from .ab_testing_framework import (
    ABTestingFramework, ABTest, ABTestVariant, TestStatus, TestType, OptimizationGoal
)
from .real_time_optimization_engine import RealTimeOptimizationEngine
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# LEARNING MODELS AND ENUMS
# =============================================================================

class LearningCategory(Enum):
    DEVICE_OPTIMIZATION = "device_optimization"
    PERSONA_TARGETING = "persona_targeting"
    CONTENT_EFFECTIVENESS = "content_effectiveness"
    TIMING_PATTERNS = "timing_patterns"
    INTERACTION_PATTERNS = "interaction_patterns"
    CONVERSION_TRIGGERS = "conversion_triggers"

class InsightType(Enum):
    DEVICE_PERFORMANCE = "device_performance"
    PERSONA_PREFERENCE = "persona_preference"
    CONTENT_PATTERN = "content_pattern"
    TEMPORAL_PATTERN = "temporal_pattern"
    BEHAVIORAL_PATTERN = "behavioral_pattern"
    OPTIMIZATION_PATTERN = "optimization_pattern"

class ConfidenceLevel(Enum):
    LOW = "low"           # < 50 tests or < 70% consistency
    MEDIUM = "medium"     # 50-100 tests or 70-85% consistency
    HIGH = "high"         # 100-200 tests or 85-95% consistency
    VERY_HIGH = "very_high"  # 200+ tests or 95%+ consistency

@dataclass
class CrossTestInsight:
    """Individual cross-test learning insight"""
    insight_id: str
    insight_type: InsightType
    category: LearningCategory
    pattern_description: str
    evidence_data: Dict[str, Any]
    confidence_level: ConfidenceLevel
    confidence_score: float  # 0-1
    supporting_tests: List[str]
    applicable_conditions: Dict[str, Any]
    impact_metrics: Dict[str, float]
    actionable_recommendations: List[str]
    statistical_significance: float
    discovered_at: datetime = None
    
    def __post_init__(self):
        if self.discovered_at is None:
            self.discovered_at = datetime.utcnow()

@dataclass
class LearningPattern:
    """Aggregated learning pattern from multiple insights"""
    pattern_id: str
    name: str
    category: LearningCategory
    pattern_strength: float  # 0-1
    consistency_score: float  # 0-1
    insights: List[CrossTestInsight]
    conditions: Dict[str, Any]
    recommendations: List[str]
    estimated_impact: Dict[str, float]
    validation_tests: List[str]
    last_validated: datetime = None
    
    def __post_init__(self):
        if self.last_validated is None:
            self.last_validated = datetime.utcnow()

@dataclass
class TestPrediction:
    """Prediction for a new test based on historical learnings"""
    test_config: Dict[str, Any]
    predicted_winner: str
    predicted_performance: Dict[str, float]
    confidence: float
    supporting_patterns: List[str]
    risk_factors: List[str]
    optimization_suggestions: List[str]
    expected_duration: int  # days

# =============================================================================
# CROSS-TEST LEARNING ENGINE
# =============================================================================

class CrossTestLearningEngine:
    """Advanced cross-test learning and pattern recognition system"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.ab_testing_framework = ABTestingFramework(db)
        self.optimization_engine = RealTimeOptimizationEngine(db)
        
        # Learning parameters
        self.min_tests_for_pattern = 5
        self.min_confidence_threshold = 0.7
        self.pattern_validation_window_days = 30
        self.learning_retention_days = 365
        
        # Pattern detection
        self.pattern_cache = {}
        self.insight_cache = {}
        
    async def extract_insights_from_completed_tests(self, test_ids: List[str] = None) -> Dict[str, Any]:
        """Extract comprehensive insights from completed tests"""
        try:
            logger.info(f"Extracting insights from {len(test_ids) if test_ids else 'all'} completed tests")
            
            # Get completed test data
            if test_ids:
                test_data = await self._get_multiple_test_data(test_ids)
            else:
                test_data = await self._get_all_completed_test_data()
            
            if not test_data:
                return {'error': 'No completed test data found'}
            
            # Extract insights by category
            insights = {
                'device_optimization_insights': await self._extract_device_optimization_insights(test_data),
                'persona_targeting_insights': await self._extract_persona_targeting_insights(test_data),
                'content_effectiveness_insights': await self._extract_content_effectiveness_insights(test_data),
                'timing_pattern_insights': await self._extract_timing_pattern_insights(test_data),
                'interaction_pattern_insights': await self._extract_interaction_pattern_insights(test_data),
                'conversion_trigger_insights': await self._extract_conversion_trigger_insights(test_data)
            }
            
            # Aggregate into learning patterns
            learning_patterns = await self._aggregate_insights_into_patterns(insights)
            
            # Validate patterns with statistical analysis
            validated_patterns = await self._validate_learning_patterns(learning_patterns)
            
            # Store insights for future use
            await self._store_learning_insights(insights, validated_patterns)
            
            # Generate actionable recommendations
            recommendations = await self._generate_actionable_recommendations(validated_patterns)
            
            return {
                'insights_extracted': sum(len(category_insights) for category_insights in insights.values()),
                'patterns_discovered': len(validated_patterns),
                'insights_by_category': {
                    category: len(category_insights) 
                    for category, category_insights in insights.items()
                },
                'learning_patterns': [asdict(pattern) for pattern in validated_patterns],
                'actionable_recommendations': recommendations,
                'tests_analyzed': len(test_data),
                'extraction_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting insights from completed tests: {str(e)}")
            return {'error': str(e)}
    
    async def predict_test_performance(self, new_test_config: Dict[str, Any]) -> TestPrediction:
        """Predict performance of a new test based on historical learnings"""
        try:
            logger.info(f"Predicting performance for new test: {new_test_config.get('test_name', 'unnamed')}")
            
            # Get relevant learning patterns
            relevant_patterns = await self._find_relevant_patterns(new_test_config)
            
            if not relevant_patterns:
                return TestPrediction(
                    test_config=new_test_config,
                    predicted_winner="insufficient_data",
                    predicted_performance={},
                    confidence=0.0,
                    supporting_patterns=[],
                    risk_factors=["No historical data available"],
                    optimization_suggestions=["Start with basic A/B test configuration"],
                    expected_duration=14
                )
            
            # Analyze test variants and predict performance
            variant_predictions = {}
            supporting_patterns = []
            
            for variant in new_test_config.get('variants', []):
                prediction = await self._predict_variant_performance(variant, relevant_patterns)
                variant_predictions[variant.get('variant_id', variant.get('name', 'unknown'))] = prediction
                
            # Determine predicted winner
            predicted_winner = max(
                variant_predictions.items(), 
                key=lambda x: x[1].get('predicted_conversion_rate', 0)
            )[0]
            
            # Calculate overall confidence
            confidence_scores = [p.get('confidence', 0) for p in variant_predictions.values()]
            overall_confidence = statistics.mean(confidence_scores) if confidence_scores else 0
            
            # Extract supporting patterns
            supporting_patterns = list(set(
                pattern for prediction in variant_predictions.values()
                for pattern in prediction.get('supporting_patterns', [])
            ))
            
            # Identify risk factors
            risk_factors = await self._identify_risk_factors(new_test_config, relevant_patterns)
            
            # Generate optimization suggestions
            optimization_suggestions = await self._generate_optimization_suggestions(
                new_test_config, relevant_patterns
            )
            
            # Estimate test duration
            expected_duration = await self._estimate_test_duration(new_test_config, relevant_patterns)
            
            return TestPrediction(
                test_config=new_test_config,
                predicted_winner=predicted_winner,
                predicted_performance=variant_predictions,
                confidence=overall_confidence,
                supporting_patterns=supporting_patterns,
                risk_factors=risk_factors,
                optimization_suggestions=optimization_suggestions,
                expected_duration=expected_duration
            )
            
        except Exception as e:
            logger.error(f"Error predicting test performance: {str(e)}")
            return TestPrediction(
                test_config=new_test_config,
                predicted_winner="error",
                predicted_performance={},
                confidence=0.0,
                supporting_patterns=[],
                risk_factors=[f"Prediction error: {str(e)}"],
                optimization_suggestions=[],
                expected_duration=14
            )
    
    async def apply_learnings_to_test_optimization(self, test_id: str) -> Dict[str, Any]:
        """Apply cross-test learnings to optimize a running test"""
        try:
            logger.info(f"Applying learnings to optimize test: {test_id}")
            
            # Get current test data
            test_data = await self._get_single_test_data(test_id)
            
            if not test_data:
                return {'error': 'Test data not found'}
            
            # Find applicable learning patterns
            applicable_patterns = await self._find_applicable_optimization_patterns(test_data)
            
            if not applicable_patterns:
                return {
                    'optimizations_applied': 0,
                    'message': 'No applicable learning patterns found'
                }
            
            # Generate optimization recommendations
            optimization_recommendations = []
            
            for pattern in applicable_patterns:
                recommendations = await self._generate_pattern_based_optimizations(test_data, pattern)
                optimization_recommendations.extend(recommendations)
            
            # Apply safe optimizations automatically
            auto_applied = []
            manual_review = []
            
            for recommendation in optimization_recommendations:
                if recommendation.get('confidence', 0) > 0.8 and recommendation.get('risk_level', 'medium') == 'low':
                    # Auto-apply high-confidence, low-risk optimizations
                    result = await self._apply_optimization_recommendation(test_id, recommendation)
                    if result['success']:
                        auto_applied.append(recommendation)
                else:
                    # Flag for manual review
                    manual_review.append(recommendation)
            
            # Update test with applied learnings
            await self._update_test_with_applied_learnings(test_id, auto_applied)
            
            return {
                'optimizations_applied': len(auto_applied),
                'optimizations_for_review': len(manual_review),
                'auto_applied_optimizations': auto_applied,
                'manual_review_optimizations': manual_review,
                'applicable_patterns': [pattern.pattern_id for pattern in applicable_patterns],
                'application_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error applying learnings to test optimization: {str(e)}")
            return {'error': str(e)}

    # =============================================================================
    # INSIGHT EXTRACTION METHODS
    # =============================================================================

    async def _extract_device_optimization_insights(self, test_data: List[Dict[str, Any]]) -> List[CrossTestInsight]:
        """Extract device-specific optimization insights"""
        insights = []
        device_performance = defaultdict(list)
        
        try:
            # Aggregate device performance data
            for test in test_data:
                for variant in test.get('variants', []):
                    device_data = variant.get('device_breakdown', {})
                    
                    for device_type, metrics in device_data.items():
                        device_performance[device_type].append({
                            'test_id': test['test_id'],
                            'variant_id': variant['variant_id'],
                            'conversion_rate': metrics.get('conversion_rate', 0),
                            'engagement_time': metrics.get('engagement_time', 0),
                            'bounce_rate': metrics.get('bounce_rate', 0),
                            'optimizations_applied': variant.get('device_optimizations', [])
                        })
            
            # Analyze patterns for each device type
            for device_type, performance_data in device_performance.items():
                if len(performance_data) >= self.min_tests_for_pattern:
                    # Find optimization patterns
                    optimization_patterns = await self._analyze_device_optimization_patterns(
                        device_type, performance_data
                    )
                    
                    for pattern in optimization_patterns:
                        insight = CrossTestInsight(
                            insight_id=f"device_{device_type}_{uuid.uuid4().hex[:8]}",
                            insight_type=InsightType.DEVICE_PERFORMANCE,
                            category=LearningCategory.DEVICE_OPTIMIZATION,
                            pattern_description=pattern['description'],
                            evidence_data=pattern['evidence'],
                            confidence_level=self._calculate_confidence_level(pattern['strength']),
                            confidence_score=pattern['strength'],
                            supporting_tests=pattern['supporting_tests'],
                            applicable_conditions={'device_type': device_type},
                            impact_metrics=pattern['impact_metrics'],
                            actionable_recommendations=pattern['recommendations'],
                            statistical_significance=pattern['p_value']
                        )
                        insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error extracting device optimization insights: {str(e)}")
            return []

    async def _extract_persona_targeting_insights(self, test_data: List[Dict[str, Any]]) -> List[CrossTestInsight]:
        """Extract persona-specific targeting insights"""
        insights = []
        persona_performance = defaultdict(list)
        
        try:
            # Aggregate persona performance data
            for test in test_data:
                for variant in test.get('variants', []):
                    persona_data = variant.get('persona_breakdown', {})
                    
                    for persona_type, metrics in persona_data.items():
                        persona_performance[persona_type].append({
                            'test_id': test['test_id'],
                            'variant_id': variant['variant_id'],
                            'conversion_rate': metrics.get('conversion_rate', 0),
                            'engagement_metrics': metrics.get('engagement_metrics', {}),
                            'content_preferences': variant.get('content_config', {}),
                            'targeting_strategy': variant.get('persona_targeting', [])
                        })
            
            # Analyze patterns for each persona
            for persona_type, performance_data in persona_performance.items():
                if len(performance_data) >= self.min_tests_for_pattern:
                    # Find content preferences and optimization patterns
                    persona_patterns = await self._analyze_persona_patterns(persona_type, performance_data)
                    
                    for pattern in persona_patterns:
                        insight = CrossTestInsight(
                            insight_id=f"persona_{persona_type}_{uuid.uuid4().hex[:8]}",
                            insight_type=InsightType.PERSONA_PREFERENCE,
                            category=LearningCategory.PERSONA_TARGETING,
                            pattern_description=pattern['description'],
                            evidence_data=pattern['evidence'],
                            confidence_level=self._calculate_confidence_level(pattern['strength']),
                            confidence_score=pattern['strength'],
                            supporting_tests=pattern['supporting_tests'],
                            applicable_conditions={'persona_type': persona_type},
                            impact_metrics=pattern['impact_metrics'],
                            actionable_recommendations=pattern['recommendations'],
                            statistical_significance=pattern['p_value']
                        )
                        insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error extracting persona targeting insights: {str(e)}")
            return []

    async def _extract_content_effectiveness_insights(self, test_data: List[Dict[str, Any]]) -> List[CrossTestInsight]:
        """Extract content effectiveness insights"""
        insights = []
        content_patterns = defaultdict(list)
        
        try:
            # Analyze content elements and their performance
            for test in test_data:
                for variant in test.get('variants', []):
                    content_config = variant.get('content_config', {})
                    performance = variant.get('performance_metrics', {})
                    
                    # Analyze different content elements
                    for element_type in ['hero_message', 'cta_style', 'trust_signals', 'urgency_elements']:
                        if element_type in content_config:
                            content_patterns[element_type].append({
                                'test_id': test['test_id'],
                                'variant_id': variant['variant_id'],
                                'content_value': content_config[element_type],
                                'conversion_rate': performance.get('conversion_rate', 0),
                                'engagement_rate': performance.get('engagement_rate', 0),
                                'click_through_rate': performance.get('click_through_rate', 0)
                            })
            
            # Find high-performing content patterns
            for element_type, element_data in content_patterns.items():
                if len(element_data) >= self.min_tests_for_pattern:
                    patterns = await self._analyze_content_effectiveness_patterns(element_type, element_data)
                    
                    for pattern in patterns:
                        insight = CrossTestInsight(
                            insight_id=f"content_{element_type}_{uuid.uuid4().hex[:8]}",
                            insight_type=InsightType.CONTENT_PATTERN,
                            category=LearningCategory.CONTENT_EFFECTIVENESS,
                            pattern_description=pattern['description'],
                            evidence_data=pattern['evidence'],
                            confidence_level=self._calculate_confidence_level(pattern['strength']),
                            confidence_score=pattern['strength'],
                            supporting_tests=pattern['supporting_tests'],
                            applicable_conditions={'content_element': element_type},
                            impact_metrics=pattern['impact_metrics'],
                            actionable_recommendations=pattern['recommendations'],
                            statistical_significance=pattern['p_value']
                        )
                        insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error extracting content effectiveness insights: {str(e)}")
            return []

    # =============================================================================
    # PATTERN ANALYSIS METHODS
    # =============================================================================

    async def _analyze_device_optimization_patterns(self, device_type: str, 
                                                  performance_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze device-specific optimization patterns"""
        patterns = []
        
        try:
            # Group by optimization strategies
            optimization_groups = defaultdict(list)
            
            for data_point in performance_data:
                optimizations = tuple(sorted(data_point.get('optimizations_applied', [])))
                optimization_groups[optimizations].append(data_point)
            
            # Compare performance across optimization strategies
            baseline_performance = statistics.mean([
                dp['conversion_rate'] for dp in performance_data 
                if not dp.get('optimizations_applied')
            ]) if any(not dp.get('optimizations_applied') for dp in performance_data) else 0
            
            for optimizations, group_data in optimization_groups.items():
                if len(group_data) >= 3 and optimizations:  # Need at least 3 tests with optimizations
                    avg_performance = statistics.mean([dp['conversion_rate'] for dp in group_data])
                    improvement = (avg_performance - baseline_performance) / baseline_performance if baseline_performance > 0 else 0
                    
                    if improvement > 0.05:  # 5% improvement threshold
                        patterns.append({
                            'description': f"Device optimization strategy '{', '.join(optimizations)}' shows {improvement:.1%} improvement on {device_type}",
                            'evidence': {
                                'optimization_strategy': list(optimizations),
                                'avg_performance': avg_performance,
                                'baseline_performance': baseline_performance,
                                'improvement': improvement,
                                'sample_size': len(group_data)
                            },
                            'strength': min(0.95, 0.5 + (improvement * 2)),  # Cap at 95%
                            'supporting_tests': [dp['test_id'] for dp in group_data],
                            'impact_metrics': {
                                'conversion_rate_lift': improvement,
                                'estimated_revenue_impact': improvement * 0.1  # Placeholder calculation
                            },
                            'recommendations': [
                                f"Apply {opt} optimization for {device_type} devices" 
                                for opt in optimizations
                            ],
                            'p_value': 0.05  # Placeholder - would need proper statistical test
                        })
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing device optimization patterns: {str(e)}")
            return []

    async def _analyze_persona_patterns(self, persona_type: str, 
                                      performance_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze persona-specific performance patterns"""
        patterns = []
        
        try:
            # Analyze content preferences
            content_performance = defaultdict(list)
            
            for data_point in performance_data:
                content_config = data_point.get('content_preferences', {})
                
                # Group by content characteristics
                for content_type, content_value in content_config.items():
                    content_performance[f"{content_type}:{content_value}"].append(
                        data_point['conversion_rate']
                    )
            
            # Find high-performing content combinations
            for content_key, performance_values in content_performance.items():
                if len(performance_values) >= 3:
                    avg_performance = statistics.mean(performance_values)
                    overall_avg = statistics.mean([dp['conversion_rate'] for dp in performance_data])
                    
                    if avg_performance > overall_avg * 1.1:  # 10% above average
                        improvement = (avg_performance - overall_avg) / overall_avg
                        
                        patterns.append({
                            'description': f"Persona {persona_type} responds {improvement:.1%} better to {content_key}",
                            'evidence': {
                                'content_characteristic': content_key,
                                'avg_performance': avg_performance,
                                'overall_avg': overall_avg,
                                'improvement': improvement,
                                'sample_size': len(performance_values)
                            },
                            'strength': min(0.95, 0.6 + (improvement * 1.5)),
                            'supporting_tests': [dp['test_id'] for dp in performance_data],
                            'impact_metrics': {
                                'conversion_rate_lift': improvement,
                                'persona_targeting_effectiveness': improvement * 0.8
                            },
                            'recommendations': [
                                f"Use {content_key} when targeting {persona_type}",
                                f"Prioritize {content_key} in persona-specific variants"
                            ],
                            'p_value': 0.05
                        })
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing persona patterns: {str(e)}")
            return []

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    def _calculate_confidence_level(self, strength: float) -> ConfidenceLevel:
        """Calculate confidence level based on pattern strength"""
        if strength >= 0.95:
            return ConfidenceLevel.VERY_HIGH
        elif strength >= 0.85:
            return ConfidenceLevel.HIGH
        elif strength >= 0.7:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    async def _get_all_completed_test_data(self) -> List[Dict[str, Any]]:
        """Get data from all completed tests"""
        try:
            # In a real implementation, this would query the database
            # For now, simulate with some sample data structure
            return []
        except Exception as e:
            logger.error(f"Error getting completed test data: {str(e)}")
            return []

    async def _store_learning_insights(self, insights: Dict[str, Any], patterns: List[LearningPattern]):
        """Store learning insights and patterns for future use"""
        try:
            # Store in Redis for quick access
            insights_key = f"cross_test_insights:{datetime.utcnow().date()}"
            insights_data = {
                'insights': insights,
                'patterns': [asdict(pattern) for pattern in patterns],
                'stored_at': datetime.utcnow().isoformat()
            }
            
            await self.redis_client.setex(insights_key, 86400 * 30, json.dumps(insights_data))  # 30 days
            
            # Store in database for long-term persistence
            learning_record = PersonalizationData(
                session_id=f"cross_test_learning_{datetime.utcnow().timestamp()}",
                personalization_type="cross_test_learning",
                personalization_strategy="pattern_extraction",
                variant_id="learning_system",
                content_delivered=insights_data,
                ml_model_version="cross_learning_v1.0",
                confidence_score=1.0
            )
            
            self.db.add(learning_record)
            await self.db.commit()
            
        except Exception as e:
            logger.error(f"Error storing learning insights: {str(e)}")

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'CrossTestLearningEngine',
    'CrossTestInsight',
    'LearningPattern',
    'TestPrediction',
    'LearningCategory',
    'InsightType',
    'ConfidenceLevel'
]