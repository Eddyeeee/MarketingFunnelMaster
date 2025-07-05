# A/B Testing Framework Integration - Week 3 Implementation
# Module: 3A - Week 3 - A/B Testing Framework Integration
# Created: 2025-07-05

import asyncio
import json
import logging
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, PersonalizationData
from .personalization_engine_enhanced import EnhancedPersonalizationEngine
from .device_content_variant_generator import DeviceContentVariantGenerator, DeviceContentVariant
from .device_variant_integration import IntegratedDeviceAwarePersonalizationEngine
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# A/B TESTING MODELS AND ENUMS
# =============================================================================

class TestStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class TestType(Enum):
    CONTENT_VARIANT = "content_variant"
    DEVICE_OPTIMIZATION = "device_optimization"
    PERSONA_TARGETING = "persona_targeting"
    HYBRID_OPTIMIZATION = "hybrid_optimization"

class OptimizationGoal(Enum):
    CONVERSION_RATE = "conversion_rate"
    ENGAGEMENT_TIME = "engagement_time"
    CLICK_THROUGH_RATE = "click_through_rate"
    BOUNCE_RATE_REDUCTION = "bounce_rate_reduction"
    REVENUE_PER_VISITOR = "revenue_per_visitor"

class StatisticalSignificance(Enum):
    NOT_SIGNIFICANT = "not_significant"
    APPROACHING_SIGNIFICANCE = "approaching_significance"  # 80-95%
    SIGNIFICANT = "significant"  # 95%+
    HIGHLY_SIGNIFICANT = "highly_significant"  # 99%+

@dataclass
class ABTestVariant:
    """Individual A/B test variant"""
    variant_id: str
    variant_name: str
    test_id: str
    traffic_allocation: float  # 0.0 to 1.0
    content_config: Dict[str, Any]
    device_optimizations: Dict[str, Any]
    persona_targeting: List[str]
    performance_budget: Dict[str, Any]
    is_control: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

@dataclass
class ABTestResult:
    """A/B test results and statistics"""
    test_id: str
    variant_id: str
    total_sessions: int
    conversions: int
    conversion_rate: float
    engagement_metrics: Dict[str, float]
    performance_metrics: Dict[str, float]
    statistical_significance: StatisticalSignificance
    confidence_interval: Tuple[float, float]
    p_value: float
    effect_size: float
    sample_size_achieved: bool
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

@dataclass
class ABTest:
    """Complete A/B test configuration"""
    test_id: str
    test_name: str
    test_type: TestType
    optimization_goal: OptimizationGoal
    status: TestStatus
    variants: List[ABTestVariant]
    traffic_allocation: Dict[str, float]
    target_sample_size: int
    min_detectable_effect: float
    statistical_power: float
    significance_level: float
    start_date: datetime
    end_date: Optional[datetime]
    created_by: str
    device_targets: List[str]
    persona_targets: List[str]
    geographic_targeting: Optional[Dict[str, Any]] = None
    exclusion_rules: Optional[Dict[str, Any]] = None
    
    def is_active(self) -> bool:
        """Check if test is currently active"""
        now = datetime.utcnow()
        return (
            self.status == TestStatus.ACTIVE and
            self.start_date <= now and
            (self.end_date is None or now <= self.end_date)
        )

# =============================================================================
# A/B TESTING FRAMEWORK CORE
# =============================================================================

class ABTestingFramework:
    """Advanced A/B testing framework with real-time optimization"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.personalization_engine = EnhancedPersonalizationEngine(db)
        self.variant_generator = DeviceContentVariantGenerator()
        self.integrated_engine = IntegratedDeviceAwarePersonalizationEngine(db)
        
        # Real-time optimization settings
        self.real_time_optimization_enabled = True
        self.optimization_check_interval = 300  # 5 minutes
        self.min_sessions_for_optimization = 100
        self.significance_threshold = 0.95
        
        # Cross-test learning
        self.cross_test_learning_enabled = True
        self.learning_window_days = 30
        
    async def create_ab_test(self, test_config: Dict[str, Any]) -> ABTest:
        """Create a new A/B test"""
        try:
            logger.info(f"Creating A/B test: {test_config.get('test_name')}")
            
            # Generate unique test ID
            test_id = f"test_{uuid.uuid4().hex[:8]}_{int(datetime.utcnow().timestamp())}"
            
            # Validate test configuration
            await self._validate_test_config(test_config)
            
            # Create test variants
            variants = await self._create_test_variants(test_id, test_config)
            
            # Calculate traffic allocation
            traffic_allocation = self._calculate_traffic_allocation(variants, test_config)
            
            # Create AB test object
            ab_test = ABTest(
                test_id=test_id,
                test_name=test_config['test_name'],
                test_type=TestType(test_config['test_type']),
                optimization_goal=OptimizationGoal(test_config['optimization_goal']),
                status=TestStatus.DRAFT,
                variants=variants,
                traffic_allocation=traffic_allocation,
                target_sample_size=test_config.get('target_sample_size', 1000),
                min_detectable_effect=test_config.get('min_detectable_effect', 0.05),
                statistical_power=test_config.get('statistical_power', 0.8),
                significance_level=test_config.get('significance_level', 0.05),
                start_date=datetime.fromisoformat(test_config['start_date']),
                end_date=datetime.fromisoformat(test_config['end_date']) if test_config.get('end_date') else None,
                created_by=test_config.get('created_by', 'system'),
                device_targets=test_config.get('device_targets', ['mobile', 'desktop', 'tablet']),
                persona_targets=test_config.get('persona_targets', ['TechEarlyAdopter', 'RemoteDad', 'StudentHustler', 'BusinessOwner']),
                geographic_targeting=test_config.get('geographic_targeting'),
                exclusion_rules=test_config.get('exclusion_rules')
            )
            
            # Store test configuration
            await self._store_test_configuration(ab_test)
            
            # Initialize test analytics
            await self._initialize_test_analytics(ab_test)
            
            logger.info(f"A/B test created successfully: {test_id}")
            return ab_test
            
        except Exception as e:
            logger.error(f"Error creating A/B test: {str(e)}")
            raise

    async def assign_user_to_test_variant(self, session: JourneySession, 
                                        request_data: Dict[str, Any],
                                        context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Assign user to appropriate A/B test variant"""
        try:
            # Find active tests for this user
            active_tests = await self._get_active_tests_for_session(session, request_data)
            
            if not active_tests:
                return None
            
            # Select primary test (highest priority or most relevant)
            primary_test = await self._select_primary_test(active_tests, session, request_data)
            
            if not primary_test:
                return None
            
            # Check if user is already assigned to a variant
            existing_assignment = await self._get_existing_assignment(session.session_id, primary_test.test_id)
            
            if existing_assignment:
                variant = next((v for v in primary_test.variants if v.variant_id == existing_assignment['variant_id']), None)
            else:
                # Assign to variant based on traffic allocation
                variant = await self._assign_to_variant(session, primary_test)
                
                if variant:
                    await self._record_variant_assignment(session.session_id, primary_test.test_id, variant.variant_id)
            
            if not variant:
                return None
            
            # Generate optimized content for assigned variant
            optimized_content = await self._generate_variant_content(
                session, variant, primary_test, request_data, context
            )
            
            # Record test exposure
            await self._record_test_exposure(session.session_id, primary_test.test_id, variant.variant_id)
            
            # Return test assignment and content
            return {
                'test_id': primary_test.test_id,
                'variant_id': variant.variant_id,
                'variant_name': variant.variant_name,
                'is_control': variant.is_control,
                'content': optimized_content,
                'test_metadata': {
                    'test_name': primary_test.test_name,
                    'test_type': primary_test.test_type.value,
                    'optimization_goal': primary_test.optimization_goal.value
                }
            }
            
        except Exception as e:
            logger.error(f"Error assigning user to test variant: {str(e)}")
            return None

    async def record_conversion_event(self, session_id: str, event_type: str, 
                                    event_data: Dict[str, Any]) -> bool:
        """Record conversion event for A/B testing"""
        try:
            # Get current test assignment
            assignment = await self._get_current_assignment(session_id)
            
            if not assignment:
                return False
            
            # Record conversion
            conversion_data = {
                'session_id': session_id,
                'test_id': assignment['test_id'],
                'variant_id': assignment['variant_id'],
                'event_type': event_type,
                'event_data': event_data,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Store conversion in Redis for real-time processing
            conversion_key = f"ab_conversion:{assignment['test_id']}:{assignment['variant_id']}:{session_id}"
            await self.redis_client.setex(conversion_key, 86400, json.dumps(conversion_data))
            
            # Update variant conversion metrics
            await self._update_variant_metrics(assignment['test_id'], assignment['variant_id'], event_type, event_data)
            
            # Check if real-time optimization should be triggered
            if self.real_time_optimization_enabled:
                await self._check_real_time_optimization(assignment['test_id'])
            
            logger.info(f"Conversion recorded: {event_type} for test {assignment['test_id']}, variant {assignment['variant_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error recording conversion event: {str(e)}")
            return False

    async def get_test_results(self, test_id: str) -> Dict[str, Any]:
        """Get comprehensive test results and analytics"""
        try:
            # Get test configuration
            test_config = await self._get_test_configuration(test_id)
            
            if not test_config:
                return {'error': 'Test not found'}
            
            # Get variant results
            variant_results = []
            
            for variant in test_config.variants:
                result = await self._calculate_variant_results(test_id, variant.variant_id)
                variant_results.append({
                    'variant_id': variant.variant_id,
                    'variant_name': variant.variant_name,
                    'is_control': variant.is_control,
                    'traffic_allocation': variant.traffic_allocation,
                    **asdict(result)
                })
            
            # Calculate statistical significance
            significance_analysis = await self._calculate_statistical_significance(test_id, variant_results)
            
            # Generate insights and recommendations
            insights = await self._generate_test_insights(test_config, variant_results, significance_analysis)
            
            # Get cross-test learnings
            cross_test_learnings = await self._get_cross_test_learnings(test_config)
            
            return {
                'test_id': test_id,
                'test_config': {
                    'test_name': test_config.test_name,
                    'test_type': test_config.test_type.value,
                    'optimization_goal': test_config.optimization_goal.value,
                    'status': test_config.status.value,
                    'start_date': test_config.start_date.isoformat(),
                    'end_date': test_config.end_date.isoformat() if test_config.end_date else None
                },
                'variant_results': variant_results,
                'statistical_analysis': significance_analysis,
                'insights': insights,
                'cross_test_learnings': cross_test_learnings,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting test results: {str(e)}")
            return {'error': str(e)}

    # =============================================================================
    # REAL-TIME OPTIMIZATION ENGINE
    # =============================================================================

    async def real_time_optimization_check(self, test_id: str) -> Dict[str, Any]:
        """Perform real-time optimization check for a test"""
        try:
            logger.info(f"Running real-time optimization check for test: {test_id}")
            
            # Get current test results
            current_results = await self.get_test_results(test_id)
            
            if 'error' in current_results:
                return current_results
            
            # Check if optimization is needed
            optimization_decision = await self._evaluate_optimization_need(current_results)
            
            if optimization_decision['should_optimize']:
                # Perform optimization
                optimization_result = await self._perform_real_time_optimization(test_id, optimization_decision)
                
                return {
                    'test_id': test_id,
                    'optimization_performed': True,
                    'optimization_type': optimization_decision['optimization_type'],
                    'changes_made': optimization_result['changes'],
                    'expected_impact': optimization_result['expected_impact'],
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'test_id': test_id,
                    'optimization_performed': False,
                    'reason': optimization_decision['reason'],
                    'next_check_in': optimization_decision.get('next_check_in', self.optimization_check_interval),
                    'timestamp': datetime.utcnow().isoformat()
                }
            
        except Exception as e:
            logger.error(f"Error in real-time optimization check: {str(e)}")
            return {'error': str(e)}

    async def _evaluate_optimization_need(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if real-time optimization is needed"""
        variant_results = test_results['variant_results']
        statistical_analysis = test_results['statistical_analysis']
        
        # Check if we have enough data
        total_sessions = sum(variant['total_sessions'] for variant in variant_results)
        
        if total_sessions < self.min_sessions_for_optimization:
            return {
                'should_optimize': False,
                'reason': f'Insufficient data: {total_sessions} sessions (need {self.min_sessions_for_optimization})'
            }
        
        # Check for clear winner
        if statistical_analysis['overall_significance'] == StatisticalSignificance.SIGNIFICANT.value:
            best_variant = max(variant_results, key=lambda v: v['conversion_rate'])
            control_variant = next(v for v in variant_results if v['is_control'])
            
            improvement = (best_variant['conversion_rate'] - control_variant['conversion_rate']) / control_variant['conversion_rate']
            
            if improvement > 0.1:  # 10% improvement threshold
                return {
                    'should_optimize': True,
                    'optimization_type': 'early_winner_traffic_reallocation',
                    'winning_variant': best_variant['variant_id'],
                    'improvement': improvement
                }
        
        # Check for poor performing variants
        poor_performers = []
        control_conversion_rate = next(v['conversion_rate'] for v in variant_results if v['is_control'])
        
        for variant in variant_results:
            if not variant['is_control']:
                performance_ratio = variant['conversion_rate'] / control_conversion_rate
                if performance_ratio < 0.8 and variant['total_sessions'] > 50:  # 20% worse with enough data
                    poor_performers.append(variant['variant_id'])
        
        if poor_performers:
            return {
                'should_optimize': True,
                'optimization_type': 'poor_performer_reallocation',
                'poor_performers': poor_performers
            }
        
        # Check for traffic allocation optimization
        traffic_efficiency = await self._analyze_traffic_efficiency(variant_results)
        
        if traffic_efficiency['needs_reallocation']:
            return {
                'should_optimize': True,
                'optimization_type': 'traffic_efficiency_optimization',
                'reallocation_suggestion': traffic_efficiency['suggestion']
            }
        
        return {
            'should_optimize': False,
            'reason': 'No optimization needed at this time'
        }

    async def _perform_real_time_optimization(self, test_id: str, optimization_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Perform real-time optimization based on decision"""
        optimization_type = optimization_decision['optimization_type']
        changes_made = []
        expected_impact = {}
        
        if optimization_type == 'early_winner_traffic_reallocation':
            # Reallocate more traffic to winning variant
            winning_variant_id = optimization_decision['winning_variant']
            
            # Increase winner traffic to 70%, reduce others proportionally
            await self._reallocate_traffic(test_id, {winning_variant_id: 0.7})
            
            changes_made.append(f"Increased traffic to winning variant {winning_variant_id} to 70%")
            expected_impact['conversion_rate_improvement'] = optimization_decision['improvement'] * 0.7
            
        elif optimization_type == 'poor_performer_reallocation':
            # Reduce traffic to poor performers
            poor_performers = optimization_decision['poor_performers']
            
            for variant_id in poor_performers:
                await self._reallocate_traffic(test_id, {variant_id: 0.05})  # Minimal traffic
                changes_made.append(f"Reduced traffic to poor performer {variant_id} to 5%")
            
            expected_impact['efficiency_improvement'] = len(poor_performers) * 0.15
            
        elif optimization_type == 'traffic_efficiency_optimization':
            # Apply suggested reallocation
            suggestion = optimization_decision['reallocation_suggestion']
            await self._reallocate_traffic(test_id, suggestion)
            
            changes_made.append("Optimized traffic allocation for better efficiency")
            expected_impact['statistical_power_improvement'] = 0.1
        
        # Record optimization action
        await self._record_optimization_action(test_id, optimization_type, changes_made, expected_impact)
        
        return {
            'changes': changes_made,
            'expected_impact': expected_impact
        }

    # =============================================================================
    # CROSS-TEST LEARNING ENGINE
    # =============================================================================

    async def extract_cross_test_learnings(self, completed_test_ids: List[str]) -> Dict[str, Any]:
        """Extract learnings from completed tests for future optimization"""
        try:
            logger.info(f"Extracting cross-test learnings from {len(completed_test_ids)} tests")
            
            # Aggregate results from completed tests
            aggregated_insights = {
                'device_performance_patterns': {},
                'persona_optimization_patterns': {},
                'content_effectiveness_patterns': {},
                'timing_patterns': {},
                'interaction_patterns': {}
            }
            
            for test_id in completed_test_ids:
                test_results = await self.get_test_results(test_id)
                
                if 'error' not in test_results:
                    # Extract device-specific insights
                    await self._extract_device_insights(test_results, aggregated_insights['device_performance_patterns'])
                    
                    # Extract persona-specific insights
                    await self._extract_persona_insights(test_results, aggregated_insights['persona_optimization_patterns'])
                    
                    # Extract content effectiveness insights
                    await self._extract_content_insights(test_results, aggregated_insights['content_effectiveness_patterns'])
                    
                    # Extract timing insights
                    await self._extract_timing_insights(test_results, aggregated_insights['timing_patterns'])
                    
                    # Extract interaction insights
                    await self._extract_interaction_insights(test_results, aggregated_insights['interaction_patterns'])
            
            # Generate actionable recommendations
            recommendations = await self._generate_cross_test_recommendations(aggregated_insights)
            
            # Store learnings for future use
            await self._store_cross_test_learnings(aggregated_insights, recommendations)
            
            return {
                'insights': aggregated_insights,
                'recommendations': recommendations,
                'tests_analyzed': len(completed_test_ids),
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting cross-test learnings: {str(e)}")
            return {'error': str(e)}

    async def apply_learnings_to_new_test(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply cross-test learnings to optimize a new test configuration"""
        try:
            # Get relevant learnings
            learnings = await self._get_relevant_learnings(test_config)
            
            if not learnings:
                return test_config
            
            optimized_config = test_config.copy()
            
            # Apply device optimization learnings
            if 'device_targets' in optimized_config:
                device_optimizations = learnings.get('device_performance_patterns', {})
                optimized_config['device_optimizations'] = device_optimizations
            
            # Apply persona targeting learnings
            if 'persona_targets' in optimized_config:
                persona_optimizations = learnings.get('persona_optimization_patterns', {})
                optimized_config['persona_optimizations'] = persona_optimizations
            
            # Apply content effectiveness learnings
            content_optimizations = learnings.get('content_effectiveness_patterns', {})
            if content_optimizations:
                optimized_config['content_templates'] = content_optimizations
            
            # Apply timing learnings
            timing_optimizations = learnings.get('timing_patterns', {})
            if timing_optimizations:
                optimized_config['optimal_timing'] = timing_optimizations
            
            # Suggest optimal sample size based on learnings
            suggested_sample_size = await self._suggest_optimal_sample_size(test_config, learnings)
            optimized_config['suggested_sample_size'] = suggested_sample_size
            
            # Suggest traffic allocation based on learnings
            suggested_allocation = await self._suggest_traffic_allocation(test_config, learnings)
            optimized_config['suggested_traffic_allocation'] = suggested_allocation
            
            return {
                'original_config': test_config,
                'optimized_config': optimized_config,
                'applied_learnings': list(learnings.keys()),
                'optimization_score': await self._calculate_optimization_score(test_config, optimized_config)
            }
            
        except Exception as e:
            logger.error(f"Error applying learnings to new test: {str(e)}")
            return test_config

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    async def _validate_test_config(self, config: Dict[str, Any]):
        """Validate A/B test configuration"""
        required_fields = ['test_name', 'test_type', 'optimization_goal', 'start_date', 'variants']
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate test type
        if config['test_type'] not in [t.value for t in TestType]:
            raise ValueError(f"Invalid test type: {config['test_type']}")
        
        # Validate optimization goal
        if config['optimization_goal'] not in [g.value for g in OptimizationGoal]:
            raise ValueError(f"Invalid optimization goal: {config['optimization_goal']}")
        
        # Validate variants
        if len(config['variants']) < 2:
            raise ValueError("Test must have at least 2 variants")
        
        # Validate traffic allocation
        total_allocation = sum(v.get('traffic_allocation', 0) for v in config['variants'])
        if abs(total_allocation - 1.0) > 0.01:
            raise ValueError(f"Traffic allocation must sum to 1.0, got {total_allocation}")

    async def _create_test_variants(self, test_id: str, config: Dict[str, Any]) -> List[ABTestVariant]:
        """Create test variants from configuration"""
        variants = []
        
        for i, variant_config in enumerate(config['variants']):
            variant_id = f"{test_id}_variant_{i}"
            
            variant = ABTestVariant(
                variant_id=variant_id,
                variant_name=variant_config.get('name', f"Variant {i}"),
                test_id=test_id,
                traffic_allocation=variant_config.get('traffic_allocation', 1.0 / len(config['variants'])),
                content_config=variant_config.get('content_config', {}),
                device_optimizations=variant_config.get('device_optimizations', {}),
                persona_targeting=variant_config.get('persona_targeting', []),
                performance_budget=variant_config.get('performance_budget', {}),
                is_control=variant_config.get('is_control', i == 0)
            )
            
            variants.append(variant)
        
        return variants

    def _calculate_traffic_allocation(self, variants: List[ABTestVariant], config: Dict[str, Any]) -> Dict[str, float]:
        """Calculate traffic allocation for variants"""
        allocation = {}
        
        for variant in variants:
            allocation[variant.variant_id] = variant.traffic_allocation
        
        return allocation

    async def _store_test_configuration(self, test: ABTest):
        """Store test configuration in database and cache"""
        # Store in Redis for quick access
        test_data = {
            'test_id': test.test_id,
            'test_name': test.test_name,
            'test_type': test.test_type.value,
            'optimization_goal': test.optimization_goal.value,
            'status': test.status.value,
            'variants': [asdict(v) for v in test.variants],
            'traffic_allocation': test.traffic_allocation,
            'target_sample_size': test.target_sample_size,
            'start_date': test.start_date.isoformat(),
            'end_date': test.end_date.isoformat() if test.end_date else None,
            'device_targets': test.device_targets,
            'persona_targets': test.persona_targets
        }
        
        cache_key = f"ab_test_config:{test.test_id}"
        await self.redis_client.setex(cache_key, 86400, json.dumps(test_data))
        
        # Store in database for persistence
        # This would typically involve creating a proper database table
        # For now, we'll store in PersonalizationData table
        test_record = PersonalizationData(
            session_id=f"ab_test_{test.test_id}",
            personalization_type="ab_test_configuration",
            personalization_strategy=test.test_type.value,
            variant_id=test.test_id,
            content_delivered=test_data,
            ml_model_version="ab_testing_v1.0",
            confidence_score=1.0
        )
        
        self.db.add(test_record)
        await self.db.commit()

    async def _initialize_test_analytics(self, test: ABTest):
        """Initialize analytics tracking for the test"""
        for variant in test.variants:
            analytics_key = f"ab_analytics:{test.test_id}:{variant.variant_id}"
            initial_data = {
                'variant_id': variant.variant_id,
                'sessions': 0,
                'conversions': 0,
                'conversion_events': {},
                'performance_metrics': {},
                'engagement_metrics': {},
                'last_updated': datetime.utcnow().isoformat()
            }
            
            await self.redis_client.setex(analytics_key, 604800, json.dumps(initial_data))  # 7 days

    # Additional helper methods would be implemented here...
    # For brevity, I'm including the key framework structure

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'ABTestingFramework',
    'ABTest',
    'ABTestVariant',
    'ABTestResult',
    'TestStatus',
    'TestType',
    'OptimizationGoal',
    'StatisticalSignificance'
]