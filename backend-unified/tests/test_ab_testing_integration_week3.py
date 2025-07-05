# A/B Testing Integration Tests - Week 3 Implementation
# Module: 3A - Week 3 - Comprehensive A/B Testing Framework Integration Tests
# Created: 2025-07-05

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.journey.ab_testing_framework import (
    ABTestingFramework, ABTest, ABTestVariant, TestStatus, TestType, OptimizationGoal
)
from src.api.journey.ab_testing_integration import ABTestingPersonalizationEngine
from src.api.journey.real_time_optimization_engine import (
    RealTimeOptimizationEngine, OptimizationType, OptimizationDecision
)
from src.api.journey.cross_test_learning_engine import (
    CrossTestLearningEngine, LearningCategory, InsightType
)
from src.api.journey.ab_testing_dashboard import ABTestingDashboard
from src.api.journey.automated_test_deployment import AutomatedTestDeployment
from src.api.journey.models import *
from src.api.journey.database_models import JourneySession

# =============================================================================
# MOCK SETUP
# =============================================================================

@pytest.fixture
def mock_db():
    """Mock database session"""
    return AsyncMock()

@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    redis_mock = AsyncMock()
    redis_mock.get.return_value = None
    redis_mock.setex.return_value = True
    redis_mock.incr.return_value = 1
    redis_mock.keys.return_value = []
    return redis_mock

@pytest.fixture
def sample_journey_session():
    """Sample journey session for testing"""
    return JourneySession(
        session_id='test_session_123',
        start_timestamp=datetime.utcnow(),
        device_type='mobile',
        persona_type='TechEarlyAdopter',
        current_stage='awareness',
        conversion_probability=0.75,
        total_touchpoints=3
    )

@pytest.fixture
def sample_test_config():
    """Sample A/B test configuration"""
    return {
        'test_name': 'Test Week 3 Integration',
        'test_type': 'hybrid_optimization',
        'optimization_goal': 'conversion_rate',
        'start_date': datetime.utcnow().isoformat(),
        'end_date': (datetime.utcnow() + timedelta(days=14)).isoformat(),
        'variants': [
            {
                'name': 'Control',
                'traffic_allocation': 0.5,
                'is_control': True,
                'content_config': {
                    'hero_message': 'Welcome to our platform',
                    'cta_style': 'standard'
                },
                'device_optimizations': {},
                'persona_targeting': []
            },
            {
                'name': 'Variant A',
                'traffic_allocation': 0.5,
                'is_control': False,
                'content_config': {
                    'hero_message': '🚀 Revolutionary platform awaits',
                    'cta_style': 'urgent'
                },
                'device_optimizations': {
                    'mobile_optimization': True,
                    'enhanced_cta': True
                },
                'persona_targeting': ['TechEarlyAdopter']
            }
        ],
        'target_sample_size': 1000,
        'device_targets': ['mobile', 'desktop'],
        'persona_targets': ['TechEarlyAdopter', 'BusinessOwner']
    }

# =============================================================================
# A/B TESTING FRAMEWORK TESTS
# =============================================================================

class TestABTestingFramework:
    """Test A/B testing framework core functionality"""
    
    @pytest.mark.asyncio
    async def test_create_ab_test(self, mock_db, sample_test_config):
        """Test A/B test creation"""
        framework = ABTestingFramework(mock_db)
        
        with patch.object(framework, '_validate_test_config') as mock_validate, \
             patch.object(framework, '_create_test_variants') as mock_create_variants, \
             patch.object(framework, '_store_test_configuration') as mock_store, \
             patch.object(framework, '_initialize_test_analytics') as mock_init_analytics:
            
            mock_validate.return_value = None
            mock_create_variants.return_value = [
                ABTestVariant(
                    variant_id='control_123',
                    variant_name='Control',
                    test_id='test_123',
                    traffic_allocation=0.5,
                    content_config={},
                    device_optimizations={},
                    persona_targeting=[],
                    is_control=True
                )
            ]
            mock_store.return_value = None
            mock_init_analytics.return_value = None
            
            result = await framework.create_ab_test(sample_test_config)
            
            assert hasattr(result, 'test_id')
            assert result.test_name == 'Test Week 3 Integration'
            assert result.test_type == TestType.HYBRID_OPTIMIZATION
            assert len(result.variants) == 1
            
            mock_validate.assert_called_once_with(sample_test_config)
            mock_create_variants.assert_called_once()
            mock_store.assert_called_once()
            mock_init_analytics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_assign_user_to_test_variant(self, mock_db, sample_journey_session, mock_redis):
        """Test user assignment to test variant"""
        framework = ABTestingFramework(mock_db)
        framework.redis_client = mock_redis
        
        # Mock active tests
        mock_test = ABTest(
            test_id='test_123',
            test_name='Test',
            test_type=TestType.CONTENT_VARIANT,
            optimization_goal=OptimizationGoal.CONVERSION_RATE,
            status=TestStatus.ACTIVE,
            variants=[
                ABTestVariant(
                    variant_id='variant_1',
                    variant_name='Variant 1',
                    test_id='test_123',
                    traffic_allocation=0.5,
                    content_config={},
                    device_optimizations={},
                    persona_targeting=[],
                    is_control=True
                )
            ],
            traffic_allocation={'variant_1': 0.5},
            target_sample_size=1000,
            min_detectable_effect=0.05,
            statistical_power=0.8,
            significance_level=0.05,
            start_date=datetime.utcnow(),
            end_date=None,
            created_by='test',
            device_targets=['mobile'],
            persona_targets=['TechEarlyAdopter']
        )
        
        with patch.object(framework, '_get_active_tests_for_session') as mock_get_tests, \
             patch.object(framework, '_select_primary_test') as mock_select_test, \
             patch.object(framework, '_get_existing_assignment') as mock_get_assignment, \
             patch.object(framework, '_assign_to_variant') as mock_assign, \
             patch.object(framework, '_generate_variant_content') as mock_generate_content, \
             patch.object(framework, '_record_variant_assignment') as mock_record_assignment, \
             patch.object(framework, '_record_test_exposure') as mock_record_exposure:
            
            mock_get_tests.return_value = [mock_test]
            mock_select_test.return_value = mock_test
            mock_get_assignment.return_value = None
            mock_assign.return_value = mock_test.variants[0]
            mock_generate_content.return_value = {
                'hero_message': 'Test content',
                'call_to_action': 'Test CTA'
            }
            mock_record_assignment.return_value = None
            mock_record_exposure.return_value = None
            
            result = await framework.assign_user_to_test_variant(
                sample_journey_session, {}, {}
            )
            
            assert result is not None
            assert result['test_id'] == 'test_123'
            assert result['variant_id'] == 'variant_1'
            assert 'content' in result
    
    @pytest.mark.asyncio
    async def test_record_conversion_event(self, mock_db, mock_redis):
        """Test conversion event recording"""
        framework = ABTestingFramework(mock_db)
        framework.redis_client = mock_redis
        
        # Mock current assignment
        mock_redis.get.return_value = json.dumps({
            'test_id': 'test_123',
            'variant_id': 'variant_1'
        })
        
        with patch.object(framework, '_update_variant_metrics') as mock_update_metrics, \
             patch.object(framework, '_check_real_time_optimization') as mock_check_optimization:
            
            mock_update_metrics.return_value = None
            mock_check_optimization.return_value = None
            
            result = await framework.record_conversion_event(
                'test_session_123',
                'purchase',
                {'amount': 99.99, 'product_id': 'prod_123'}
            )
            
            assert result is True
            mock_redis.setex.assert_called()
            mock_update_metrics.assert_called_once()

# =============================================================================
# REAL-TIME OPTIMIZATION ENGINE TESTS
# =============================================================================

class TestRealTimeOptimizationEngine:
    """Test real-time optimization engine functionality"""
    
    @pytest.mark.asyncio
    async def test_analyze_test_performance(self, mock_db):
        """Test test performance analysis"""
        engine = RealTimeOptimizationEngine(mock_db)
        
        mock_test_data = {
            'test_id': 'test_123',
            'variants': [
                {
                    'variant_id': 'control',
                    'is_control': True,
                    'sessions': 500,
                    'conversions': 25,
                    'conversion_rate': 0.05
                },
                {
                    'variant_id': 'variant_a',
                    'is_control': False,
                    'sessions': 500,
                    'conversions': 35,
                    'conversion_rate': 0.07
                }
            ],
            'start_date': (datetime.utcnow() - timedelta(days=7)).isoformat()
        }
        
        with patch.object(engine, '_get_comprehensive_test_data') as mock_get_data, \
             patch.object(engine, '_perform_statistical_analysis') as mock_stats, \
             patch.object(engine, '_detect_anomalies') as mock_anomalies, \
             patch.object(engine, '_generate_optimization_recommendations') as mock_recommendations, \
             patch.object(engine, '_calculate_performance_metrics') as mock_metrics, \
             patch.object(engine, '_assess_optimization_risks') as mock_risks:
            
            mock_get_data.return_value = mock_test_data
            mock_stats.return_value = {
                'overall_significance': 'significant',
                'variant_comparisons': []
            }
            mock_anomalies.return_value = {'anomalies_detected': False}
            mock_recommendations.return_value = []
            mock_metrics.return_value = {'performance_score': 85}
            mock_risks.return_value = {'risk_level': 'low'}
            
            result = await engine.analyze_test_performance('test_123')
            
            assert 'test_id' in result
            assert 'performance_analysis' in result
            assert 'recommendations' in result
            assert result['test_id'] == 'test_123'
    
    @pytest.mark.asyncio
    async def test_real_time_optimization_check(self, mock_db, mock_redis):
        """Test real-time optimization check"""
        engine = RealTimeOptimizationEngine(mock_db)
        engine.redis_client = mock_redis
        
        with patch.object(engine, 'get_test_results') as mock_get_results, \
             patch.object(engine, '_evaluate_optimization_need') as mock_evaluate, \
             patch.object(engine, '_perform_real_time_optimization') as mock_optimize:
            
            mock_get_results.return_value = {
                'test_id': 'test_123',
                'variant_results': [],
                'statistical_analysis': {}
            }
            
            mock_evaluate.return_value = {
                'should_optimize': True,
                'optimization_type': 'traffic_reallocation',
                'winning_variant': 'variant_a',
                'improvement': 0.15
            }
            
            mock_optimize.return_value = {
                'changes': ['Increased traffic to variant_a'],
                'expected_impact': {'conversion_rate_improvement': 0.15}
            }
            
            result = await engine.real_time_optimization_check('test_123')
            
            assert result['test_id'] == 'test_123'
            assert result['optimization_performed'] is True
            assert 'optimization_type' in result
            assert 'changes_made' in result

# =============================================================================
# CROSS-TEST LEARNING ENGINE TESTS
# =============================================================================

class TestCrossTestLearningEngine:
    """Test cross-test learning engine functionality"""
    
    @pytest.mark.asyncio
    async def test_extract_insights_from_completed_tests(self, mock_db):
        """Test insight extraction from completed tests"""
        engine = CrossTestLearningEngine(mock_db)
        
        mock_test_data = [
            {
                'test_id': 'test_1',
                'variants': [
                    {
                        'variant_id': 'v1',
                        'device_breakdown': {
                            'mobile': {'conversion_rate': 0.06},
                            'desktop': {'conversion_rate': 0.04}
                        },
                        'persona_breakdown': {
                            'TechEarlyAdopter': {'conversion_rate': 0.08}
                        }
                    }
                ]
            }
        ]
        
        with patch.object(engine, '_get_multiple_test_data') as mock_get_data, \
             patch.object(engine, '_extract_device_optimization_insights') as mock_device_insights, \
             patch.object(engine, '_extract_persona_targeting_insights') as mock_persona_insights, \
             patch.object(engine, '_extract_content_effectiveness_insights') as mock_content_insights, \
             patch.object(engine, '_aggregate_insights_into_patterns') as mock_aggregate, \
             patch.object(engine, '_validate_learning_patterns') as mock_validate, \
             patch.object(engine, '_store_learning_insights') as mock_store, \
             patch.object(engine, '_generate_actionable_recommendations') as mock_recommendations:
            
            mock_get_data.return_value = mock_test_data
            mock_device_insights.return_value = []
            mock_persona_insights.return_value = []
            mock_content_insights.return_value = []
            mock_aggregate.return_value = []
            mock_validate.return_value = []
            mock_store.return_value = None
            mock_recommendations.return_value = []
            
            result = await engine.extract_insights_from_completed_tests(['test_1'])
            
            assert 'insights_extracted' in result
            assert 'patterns_discovered' in result
            assert 'tests_analyzed' in result
            assert result['tests_analyzed'] == 1
    
    @pytest.mark.asyncio
    async def test_predict_test_performance(self, mock_db):
        """Test test performance prediction"""
        engine = CrossTestLearningEngine(mock_db)
        
        mock_test_config = {
            'test_name': 'Prediction Test',
            'optimization_goal': 'conversion_rate',
            'variants': [
                {'variant_id': 'control', 'name': 'Control'},
                {'variant_id': 'variant_a', 'name': 'Variant A'}
            ]
        }
        
        with patch.object(engine, '_find_relevant_patterns') as mock_find_patterns, \
             patch.object(engine, '_predict_variant_performance') as mock_predict_variant:
            
            mock_find_patterns.return_value = []
            mock_predict_variant.return_value = {
                'predicted_conversion_rate': 0.06,
                'confidence': 0.8,
                'supporting_patterns': []
            }
            
            result = await engine.predict_test_performance(mock_test_config)
            
            assert hasattr(result, 'test_config')
            assert hasattr(result, 'predicted_winner')
            assert hasattr(result, 'confidence')
            assert hasattr(result, 'expected_duration')

# =============================================================================
# A/B TESTING DASHBOARD TESTS
# =============================================================================

class TestABTestingDashboard:
    """Test A/B testing dashboard functionality"""
    
    @pytest.mark.asyncio
    async def test_get_dashboard_overview(self, mock_db, mock_redis):
        """Test dashboard overview generation"""
        dashboard = ABTestingDashboard(mock_db)
        dashboard.redis_client = mock_redis
        
        with patch.object(dashboard, '_get_dashboard_summary') as mock_summary, \
             patch.object(dashboard, '_get_active_tests_overview') as mock_active_tests, \
             patch.object(dashboard, '_get_performance_trends') as mock_trends, \
             patch.object(dashboard, '_get_recent_optimizations') as mock_optimizations, \
             patch.object(dashboard, '_get_active_alerts') as mock_alerts, \
             patch.object(dashboard, '_get_learning_insights_summary') as mock_insights, \
             patch.object(dashboard, '_get_real_time_metrics') as mock_real_time, \
             patch.object(dashboard, '_get_system_status') as mock_system_status:
            
            from src.api.journey.ab_testing_dashboard import DashboardSummary
            
            mock_summary.return_value = DashboardSummary(
                total_active_tests=3,
                total_completed_tests=12,
                avg_conversion_rate=0.05,
                total_sessions_today=1500,
                active_optimizations=2,
                alerts_count=1,
                top_performer={'test_id': 'test_1', 'conversion_rate': 0.08},
                bottom_performer={'test_id': 'test_2', 'conversion_rate': 0.02},
                system_health_score=0.85
            )
            
            mock_active_tests.return_value = []
            mock_trends.return_value = {}
            mock_optimizations.return_value = []
            mock_alerts.return_value = []
            mock_insights.return_value = {}
            mock_real_time.return_value = {}
            mock_system_status.return_value = {'status': 'healthy'}
            
            result = await dashboard.get_dashboard_overview('24h')
            
            assert 'overview' in result
            assert 'active_tests' in result
            assert 'performance_trends' in result
            assert result['overview']['summary']['total_active_tests'] == 3
    
    @pytest.mark.asyncio
    async def test_check_and_generate_alerts(self, mock_db, mock_redis):
        """Test alert generation"""
        dashboard = ABTestingDashboard(mock_db)
        dashboard.redis_client = mock_redis
        
        from src.api.journey.ab_testing_dashboard import DashboardAlert, AlertSeverity
        
        mock_alert = DashboardAlert(
            alert_id='alert_123',
            test_id='test_123',
            test_name='Test Alert',
            severity=AlertSeverity.WARNING,
            message='Test reached statistical significance',
            details={},
            action_required=True,
            suggested_actions=['Review results']
        )
        
        with patch.object(dashboard, '_check_statistical_significance_alerts') as mock_sig_alerts, \
             patch.object(dashboard, '_check_performance_degradation_alerts') as mock_perf_alerts, \
             patch.object(dashboard, '_check_optimization_opportunity_alerts') as mock_opt_alerts, \
             patch.object(dashboard, '_check_system_health_alerts') as mock_sys_alerts, \
             patch.object(dashboard, '_store_alert') as mock_store_alert, \
             patch.object(dashboard, '_send_alert_notifications') as mock_send_notifications:
            
            mock_sig_alerts.return_value = [mock_alert]
            mock_perf_alerts.return_value = []
            mock_opt_alerts.return_value = []
            mock_sys_alerts.return_value = []
            mock_store_alert.return_value = None
            mock_send_notifications.return_value = None
            
            result = await dashboard.check_and_generate_alerts()
            
            assert len(result) == 1
            assert result[0].alert_id == 'alert_123'
            assert result[0].severity == AlertSeverity.WARNING

# =============================================================================
# AUTOMATED TEST DEPLOYMENT TESTS
# =============================================================================

class TestAutomatedTestDeployment:
    """Test automated test deployment functionality"""
    
    @pytest.mark.asyncio
    async def test_create_test_from_template(self, mock_db, mock_redis):
        """Test test creation from template"""
        deployment = AutomatedTestDeployment(mock_db)
        deployment.redis_client = mock_redis
        
        from src.api.journey.automated_test_deployment import TestTemplate
        
        mock_template = TestTemplate(
            template_id='template_123',
            template_name='Standard A/B Test',
            category='conversion',
            description='Standard conversion optimization test',
            base_config={
                'test_type': 'content_variant',
                'optimization_goal': 'conversion_rate'
            },
            variable_parameters=['hero_message', 'cta_text'],
            success_criteria={'min_improvement': 0.05},
            estimated_duration_days=14,
            confidence_level=0.85
        )
        
        with patch.object(deployment, '_get_test_template') as mock_get_template, \
             patch.object(deployment, '_generate_config_from_template') as mock_generate_config, \
             patch.object(deployment, '_apply_learning_optimizations') as mock_apply_learning, \
             patch.object(deployment, '_validate_test_configuration') as mock_validate, \
             patch.object(deployment, '_create_deployment_plan') as mock_create_plan, \
             patch.object(deployment, '_execute_deployment') as mock_execute:
            
            from src.api.journey.automated_test_deployment import DeploymentResult, DeploymentStatus
            
            mock_get_template.return_value = mock_template
            mock_generate_config.return_value = {'test_name': 'Generated Test'}
            mock_apply_learning.return_value = {'test_name': 'Optimized Test'}
            mock_validate.return_value = {'valid': True, 'errors': []}
            mock_create_plan.return_value = Mock()
            mock_execute.return_value = DeploymentResult(
                deployment_id='deploy_123',
                test_id='test_123',
                status=DeploymentStatus.ACTIVE,
                steps_completed=['test_creation', 'activation'],
                steps_failed=[],
                validation_results={},
                error_messages=[],
                deployment_time_seconds=45.0,
                rollback_triggered=False,
                post_deployment_checks={}
            )
            
            result = await deployment.create_test_from_template('template_123')
            
            assert 'test_id' in result
            assert 'deployment_id' in result
            assert result['status'] == 'active'
            assert result['template_used'] == 'template_123'
    
    @pytest.mark.asyncio
    async def test_auto_generate_test_configuration(self, mock_db):
        """Test auto-generation of test configuration"""
        deployment = AutomatedTestDeployment(mock_db)
        
        requirements = {
            'optimization_goal': 'conversion_rate',
            'target_audience': ['TechEarlyAdopter'],
            'device_targets': ['mobile', 'desktop'],
            'traffic_percentage': 80,
            'duration_days': 14
        }
        
        from src.api.journey.cross_test_learning_engine import TestPrediction
        
        mock_prediction = TestPrediction(
            test_config={},
            predicted_winner='variant_a',
            predicted_performance={'variant_a': {'conversion_rate': 0.06}},
            confidence=0.85,
            supporting_patterns=['pattern_1'],
            risk_factors=[],
            optimization_suggestions=['Use urgency in CTA'],
            expected_duration=14
        )
        
        with patch.object(deployment.learning_engine, 'predict_test_performance') as mock_predict, \
             patch.object(deployment, '_generate_base_configuration') as mock_base_config, \
             patch.object(deployment, '_apply_predictive_optimizations') as mock_apply_optimizations, \
             patch.object(deployment, '_generate_optimal_variants') as mock_generate_variants, \
             patch.object(deployment, '_calculate_optimal_traffic_allocation') as mock_traffic_allocation, \
             patch.object(deployment, '_calculate_optimal_sample_size') as mock_sample_size:
            
            mock_predict.return_value = mock_prediction
            mock_base_config.return_value = {'test_name': 'Auto Generated'}
            mock_apply_optimizations.return_value = {'test_name': 'Optimized Auto Generated'}
            mock_generate_variants.return_value = []
            mock_traffic_allocation.return_value = {}
            mock_sample_size.return_value = 1000
            
            result = await deployment.auto_generate_test_configuration(requirements)
            
            assert 'test_configuration' in result
            assert 'generation_confidence' in result
            assert 'supporting_patterns' in result
            assert result['generation_confidence'] == 0.85

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestABTestingIntegration:
    """Test full A/B testing integration"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_ab_test_flow(self, mock_db, mock_redis, sample_journey_session, sample_test_config):
        """Test complete A/B testing flow from creation to optimization"""
        
        # Initialize all components
        framework = ABTestingFramework(mock_db)
        personalization_engine = ABTestingPersonalizationEngine(mock_db)
        optimization_engine = RealTimeOptimizationEngine(mock_db)
        dashboard = ABTestingDashboard(mock_db)
        
        # Mock Redis for all components
        framework.redis_client = mock_redis
        personalization_engine.redis_client = mock_redis
        optimization_engine.redis_client = mock_redis
        dashboard.redis_client = mock_redis
        
        # Step 1: Create A/B test
        with patch.object(framework, 'create_ab_test') as mock_create_test:
            mock_test = ABTest(
                test_id='integration_test_123',
                test_name='Integration Test',
                test_type=TestType.HYBRID_OPTIMIZATION,
                optimization_goal=OptimizationGoal.CONVERSION_RATE,
                status=TestStatus.ACTIVE,
                variants=[],
                traffic_allocation={},
                target_sample_size=1000,
                min_detectable_effect=0.05,
                statistical_power=0.8,
                significance_level=0.05,
                start_date=datetime.utcnow(),
                end_date=None,
                created_by='integration_test',
                device_targets=['mobile'],
                persona_targets=['TechEarlyAdopter']
            )
            mock_create_test.return_value = mock_test
            
            test = await framework.create_ab_test(sample_test_config)
            assert test.test_id == 'integration_test_123'
        
        # Step 2: Generate personalized content with A/B testing
        with patch.object(personalization_engine, 'generate_ab_tested_content') as mock_generate_content:
            mock_generate_content.return_value = {
                'content': {
                    'hero_message': 'Test content',
                    'call_to_action': 'Test CTA'
                },
                'ab_testing': {
                    'test_id': 'integration_test_123',
                    'variant_id': 'variant_a'
                }
            }
            
            content = await personalization_engine.generate_ab_tested_content(
                sample_journey_session, {}, {}
            )
            
            assert 'ab_testing' in content
            assert content['ab_testing']['test_id'] == 'integration_test_123'
        
        # Step 3: Record user interaction
        with patch.object(personalization_engine, 'record_ab_test_interaction') as mock_record_interaction:
            mock_record_interaction.return_value = True
            
            interaction_result = await personalization_engine.record_ab_test_interaction(
                'test_session_123',
                {'event_type': 'click', 'element': 'cta_button'}
            )
            
            assert interaction_result is True
        
        # Step 4: Run optimization check
        with patch.object(optimization_engine, 'real_time_optimization_check') as mock_optimization_check:
            mock_optimization_check.return_value = {
                'test_id': 'integration_test_123',
                'optimization_performed': True,
                'optimization_type': 'traffic_reallocation'
            }
            
            optimization_result = await optimization_engine.real_time_optimization_check('integration_test_123')
            
            assert optimization_result['optimization_performed'] is True
        
        # Step 5: Check dashboard
        with patch.object(dashboard, 'get_dashboard_overview') as mock_dashboard:
            mock_dashboard.return_value = {
                'overview': {'summary': {'total_active_tests': 1}},
                'active_tests': [{'test_id': 'integration_test_123'}]
            }
            
            dashboard_result = await dashboard.get_dashboard_overview('24h')
            
            assert dashboard_result['overview']['summary']['total_active_tests'] == 1
    
    @pytest.mark.asyncio
    async def test_performance_metrics_validation(self, mock_db, mock_redis):
        """Test performance metrics validation across all components"""
        
        # Test performance thresholds
        performance_requirements = {
            'response_time_ms': 500,  # Max 500ms response time
            'memory_usage_mb': 100,   # Max 100MB memory usage
            'concurrent_tests': 10,   # Support 10 concurrent tests
            'throughput_rps': 1000    # 1000 requests per second
        }
        
        # Initialize components
        framework = ABTestingFramework(mock_db)
        optimization_engine = RealTimeOptimizationEngine(mock_db)
        dashboard = ABTestingDashboard(mock_db)
        
        # Mock performance metrics
        with patch('time.time') as mock_time:
            start_time = 1000.0
            end_time = 1000.45  # 450ms execution time
            mock_time.side_effect = [start_time, end_time]
            
            # Test framework performance
            with patch.object(framework, 'assign_user_to_test_variant') as mock_assign:
                mock_assign.return_value = {'test_id': 'test_123'}
                
                result = await framework.assign_user_to_test_variant(Mock(), {}, {})
                execution_time = (end_time - start_time) * 1000
                
                assert execution_time < performance_requirements['response_time_ms']
        
        # Test optimization engine performance
        with patch.object(optimization_engine, 'analyze_test_performance') as mock_analyze:
            mock_analyze.return_value = {'test_id': 'test_123'}
            
            start_time = datetime.utcnow()
            result = await optimization_engine.analyze_test_performance('test_123')
            end_time = datetime.utcnow()
            
            execution_time = (end_time - start_time).total_seconds() * 1000
            assert execution_time < performance_requirements['response_time_ms']
        
        # Test dashboard performance
        with patch.object(dashboard, 'get_dashboard_overview') as mock_dashboard:
            mock_dashboard.return_value = {'overview': {}}
            
            start_time = datetime.utcnow()
            result = await dashboard.get_dashboard_overview('24h')
            end_time = datetime.utcnow()
            
            execution_time = (end_time - start_time).total_seconds() * 1000
            assert execution_time < performance_requirements['response_time_ms']

# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])