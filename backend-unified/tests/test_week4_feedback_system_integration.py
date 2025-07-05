#!/usr/bin/env python3
"""
Week 4 Feedback-Driven Improvement System Integration Tests
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 4 - Feedback-Driven Improvement System

Comprehensive integration tests for the complete feedback-driven improvement system,
validating all components working together seamlessly.

Executor: Claude Code
Created: 2025-07-05
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, List, Any

# Import system components
from ..core.improvement.feedback_system import (
    FeedbackDrivenImprovementSystem, FeedbackType, LearningInsight, 
    OptimizationAction, LearningPriority
)
from ..core.improvement.analytics_integration import (
    PerformanceAnalyticsEngine, PerformanceMetric, MetricType
)
from ..core.improvement.optimization_engine import (
    ContinuousOptimizationEngine, OptimizationType, OptimizationScope, OptimizationGoal
)
from ..core.improvement.feedback_integration_controller import (
    FeedbackIntegrationController, FeedbackLoopType
)
from ..core.testing.ab_testing_framework import ABTestingFramework
from ..src.api.journey.personalization_engine_enhanced import EnhancedPersonalizationEngine
from ..src.api.journey.models import JourneySession, PersonalizedContent

class TestFeedbackDrivenImprovementSystem:
    """Test suite for the complete feedback-driven improvement system"""
    
    @pytest.fixture
    async def setup_system_components(self):
        """Setup all system components for testing"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Create mock components
        mock_ab_testing = AsyncMock(spec=ABTestingFramework)
        mock_personalization = AsyncMock(spec=EnhancedPersonalizationEngine)
        mock_orchestrator = AsyncMock()
        mock_performance_tracker = AsyncMock()
        
        # Create analytics engine
        analytics_engine = PerformanceAnalyticsEngine(mock_db)
        
        # Create feedback system
        feedback_system = FeedbackDrivenImprovementSystem(
            mock_ab_testing, mock_personalization, mock_orchestrator, mock_performance_tracker
        )
        
        # Create optimization engine
        optimization_engine = ContinuousOptimizationEngine(
            feedback_system, analytics_engine, mock_ab_testing, 
            mock_personalization, mock_orchestrator
        )
        
        # Create integration controller
        integration_controller = FeedbackIntegrationController(
            feedback_system, analytics_engine, optimization_engine,
            mock_ab_testing, mock_personalization, mock_orchestrator
        )
        
        return {
            'analytics_engine': analytics_engine,
            'feedback_system': feedback_system,
            'optimization_engine': optimization_engine,
            'integration_controller': integration_controller,
            'mock_db': mock_db,
            'mock_ab_testing': mock_ab_testing,
            'mock_personalization': mock_personalization
        }
    
    @pytest.mark.asyncio
    async def test_complete_feedback_loop_integration(self, setup_system_components):
        """Test complete feedback loop from data collection to optimization"""
        components = await setup_system_components()
        
        integration_controller = components['integration_controller']
        feedback_system = components['feedback_system']
        analytics_engine = components['analytics_engine']
        optimization_engine = components['optimization_engine']
        
        # Initialize components
        await integration_controller.initialize()
        
        # Create test session
        test_session = MagicMock()
        test_session.session_id = "test_session_123"
        test_session.persona_type = "TechEarlyAdopter"
        test_session.device_type = "mobile"
        test_session.persona_confidence = 0.85
        test_session.current_stage = "consideration"
        test_session.device_info = {"user_agent": "test_agent"}
        
        # Create test personalized content
        test_content = MagicMock()
        test_content.personalization_strategy = "tech_adopter_mobile"
        
        # Test performance data
        performance_data = {
            'conversion_achieved': True,
            'engagement_score': 0.8,
            'personalization_effectiveness': 0.9,
            'engagement_metrics': {
                'time_on_page': 120,
                'click_through_rate': 0.15,
                'bounce_rate': 0.2
            }
        }
        
        # Step 1: Collect personalization feedback
        await integration_controller.collect_personalization_feedback(
            test_session, test_content, performance_data
        )
        
        # Verify analytics tracking
        assert len(analytics_engine.metrics_buffer) > 0
        
        # Step 2: Process feedback and generate insights
        insights = await feedback_system.generate_learning_insights()
        
        # Should generate insights from patterns if enough data
        assert isinstance(insights, list)
        
        # Step 3: Create optimization actions
        if insights:
            actions = await feedback_system.create_optimization_actions(insights)
            assert isinstance(actions, list)
        
        # Step 4: Trigger system-wide optimization
        optimization_result = await integration_controller.trigger_cross_component_optimization()
        
        # Verify optimization was triggered
        assert 'optimization_id' in optimization_result
        assert isinstance(optimization_result.get('success'), bool)
        
        # Step 5: Get integration status
        status = await integration_controller.get_integration_status()
        
        # Verify system health and feedback loops
        assert 'system_health_score' in status
        assert 'active_feedback_loops' in status
        assert status['system_health_score'] >= 0.0
        assert status['active_feedback_loops'] >= 0
    
    @pytest.mark.asyncio
    async def test_analytics_engine_performance_tracking(self, setup_system_components):
        """Test analytics engine performance tracking capabilities"""
        components = await setup_system_components()
        analytics_engine = components['analytics_engine']
        
        # Create test performance metrics
        test_metrics = [
            PerformanceMetric(
                metric_type=MetricType.CONVERSION_RATE,
                value=0.05,
                timestamp=datetime.utcnow(),
                context={'test': 'data'},
                session_id="session_1",
                persona_type="TechEarlyAdopter",
                device_type="mobile"
            ),
            PerformanceMetric(
                metric_type=MetricType.ENGAGEMENT_SCORE,
                value=0.75,
                timestamp=datetime.utcnow(),
                context={'test': 'data'},
                session_id="session_2",
                persona_type="RemoteDad",
                device_type="desktop"
            ),
            PerformanceMetric(
                metric_type=MetricType.PERSONALIZATION_EFFECTIVENESS,
                value=0.85,
                timestamp=datetime.utcnow(),
                context={'test': 'data'},
                session_id="session_3",
                persona_type="StudentHustler",
                device_type="mobile"
            )
        ]
        
        # Track all metrics
        for metric in test_metrics:
            await analytics_engine.track_performance_metric(metric)
        
        # Verify metrics are stored
        assert len(analytics_engine.metrics_buffer) == 3
        
        # Test personalization performance analysis
        analysis = await analytics_engine.analyze_personalization_performance(
            persona_type="TechEarlyAdopter",
            device_type="mobile",
            time_window_hours=1
        )
        
        # Should return analysis structure
        assert 'persona_type' in analysis
        assert 'device_type' in analysis
        assert analysis['persona_type'] == "TechEarlyAdopter"
        assert analysis['device_type'] == "mobile"
        
        # Test real-time dashboard data
        dashboard_data = await analytics_engine.get_real_time_dashboard_data()
        
        # Verify dashboard structure
        assert 'timestamp' in dashboard_data
        assert 'system_health_score' in dashboard_data
        
        # Test personalization effectiveness tracking
        await analytics_engine.track_personalization_effectiveness(
            session_id="test_session",
            personalization_strategy="test_strategy",
            persona_detected="TechEarlyAdopter",
            persona_confidence=0.9,
            conversion_outcome=True,
            engagement_metrics={'engagement_score': 0.8}
        )
        
        # Verify additional metric was tracked
        assert len(analytics_engine.metrics_buffer) == 4
    
    @pytest.mark.asyncio
    async def test_feedback_system_pattern_detection(self, setup_system_components):
        """Test feedback system pattern detection and learning"""
        components = await setup_system_components()
        feedback_system = components['feedback_system']
        
        # Initialize the system
        await feedback_system.initialize()
        
        # Create multiple feedback events to establish patterns
        for i in range(15):  # Need 10+ for pattern detection
            feedback_id = await feedback_system.collect_feedback(
                feedback_type=FeedbackType.PERSONALIZATION_EFFECTIVENESS,
                source_component="personalization_engine",
                data={
                    'conversion_rate': 0.05 + (i * 0.001),  # Increasing trend
                    'engagement_score': 0.7 + (i * 0.01),
                    'session_id': f'session_{i}',
                    'persona': 'TechEarlyAdopter',
                    'iteration': i
                },
                session_id=f'session_{i}',
                context={'test_iteration': i}
            )
            assert feedback_id is not None
        
        # Process feedback batch
        processing_result = await feedback_system.process_feedback_batch(batch_size=15)
        
        # Verify processing
        assert processing_result['processed'] == 15
        
        # Generate learning insights
        insights = await feedback_system.generate_learning_insights(
            time_window=timedelta(hours=1)
        )
        
        # Should generate insights from patterns
        assert isinstance(insights, list)
        
        # Create optimization actions from insights
        if insights:
            actions = await feedback_system.create_optimization_actions(insights)
            assert isinstance(actions, list)
            
            # Execute optimization actions
            if actions:
                execution_result = await feedback_system.execute_optimization_actions(max_actions=2)
                assert 'executed' in execution_result
                assert execution_result['executed'] <= 2
        
        # Get performance analytics
        analytics = await feedback_system.get_performance_analytics()
        
        # Verify analytics structure
        assert 'time_window' in analytics
        
        # Get improvement recommendations
        recommendations = await feedback_system.get_improvement_recommendations()
        
        # Verify recommendations
        assert isinstance(recommendations, list)
    
    @pytest.mark.asyncio
    async def test_optimization_engine_goal_management(self, setup_system_components):
        """Test optimization engine goal management and execution"""
        components = await setup_system_components()
        optimization_engine = components['optimization_engine']
        
        # Initialize the engine
        await optimization_engine.initialize()
        
        # Verify default goals were created
        assert len(optimization_engine.optimization_goals) >= 3
        
        # Create custom optimization goal
        custom_goal = OptimizationGoal(
            goal_id="test_custom_goal",
            name="Test Custom Goal",
            metric_name="custom_metric",
            target_value=0.8,
            current_value=0.6,
            improvement_direction="increase",
            weight=1.0,
            priority=LearningPriority.HIGH
        )
        
        # Add custom goal
        goal_id = await optimization_engine.add_optimization_goal(custom_goal)
        assert goal_id == "test_custom_goal"
        assert goal_id in optimization_engine.optimization_goals
        
        # Update goal
        update_success = await optimization_engine.update_optimization_goal(
            goal_id, {'target_value': 0.9}
        )
        assert update_success is True
        assert optimization_engine.optimization_goals[goal_id].target_value == 0.9
        
        # Trigger optimization
        optimization_id = await optimization_engine.trigger_optimization(
            optimization_type=OptimizationType.TRIGGERED,
            scope=OptimizationScope.SYSTEM_WIDE
        )
        
        assert optimization_id is not None
        assert len(optimization_engine.optimization_history) >= 1
        
        # Get optimization status
        status = await optimization_engine.get_optimization_status()
        
        # Verify status structure
        assert 'timestamp' in status
        assert 'total_goals' in status
        assert 'current_strategy' in status
        assert status['total_goals'] >= 4  # 3 default + 1 custom
        
        # Get optimization recommendations
        recommendations = await optimization_engine.get_optimization_recommendations()
        
        # Verify recommendations
        assert isinstance(recommendations, list)
        
        # Adjust optimization strategy
        strategy_success = await optimization_engine.adjust_optimization_strategy(
            strategy=optimization_engine.current_strategy,
            parameters={'risk_tolerance': 0.8}
        )
        assert strategy_success is True
    
    @pytest.mark.asyncio
    async def test_integration_controller_cross_component_coordination(self, setup_system_components):
        """Test integration controller cross-component coordination"""
        components = await setup_system_components()
        integration_controller = components['integration_controller']
        
        # Initialize integration controller
        await integration_controller.initialize()
        
        # Verify feedback loops were created
        assert len(integration_controller.feedback_loops) >= 4
        
        # Test A/B test feedback collection
        await integration_controller.collect_ab_test_feedback(
            test_id="test_ab_123",
            variant_id="variant_a",
            session_id="session_123",
            performance_data={
                'conversion_rate': 0.08,
                'engagement_score': 0.75,
                'click_through_rate': 0.12
            }
        )
        
        # Test user behavior feedback collection
        await integration_controller.collect_user_behavior_feedback(
            session_id="session_456",
            behavior_data={
                'engagement_score': 0.82,
                'time_on_page': 150,
                'scroll_depth': 0.8,
                'clicks': 5
            }
        )
        
        # Trigger cross-component optimization
        optimization_result = await integration_controller.trigger_cross_component_optimization()
        
        # Verify optimization execution
        assert 'optimization_id' in optimization_result
        assert 'success' in optimization_result
        
        # Get comprehensive integration status
        integration_status = await integration_controller.get_integration_status()
        
        # Verify status completeness
        required_fields = [
            'timestamp', 'system_health_score', 'active_feedback_loops',
            'learning_velocity', 'component_status', 'feedback_loop_details'
        ]
        
        for field in required_fields:
            assert field in integration_status
        
        # Get performance dashboard data
        dashboard_data = await integration_controller.get_performance_dashboard_data()
        
        # Verify dashboard data structure
        dashboard_sections = ['analytics', 'optimization', 'feedback_system', 'integration', 'summary']
        
        for section in dashboard_sections:
            assert section in dashboard_data
        
        # Verify summary metrics
        summary = dashboard_data['summary']
        assert 'overall_health' in summary
        assert 'learning_velocity' in summary
        assert 'feedback_loops_active' in summary
    
    @pytest.mark.asyncio
    async def test_end_to_end_improvement_workflow(self, setup_system_components):
        """Test complete end-to-end improvement workflow"""
        components = await setup_system_components()
        integration_controller = components['integration_controller']
        analytics_engine = components['analytics_engine']
        feedback_system = components['feedback_system']
        optimization_engine = components['optimization_engine']
        
        # Initialize all systems
        await integration_controller.initialize()
        
        # Simulate a complete user journey with feedback
        sessions = []
        for i in range(10):
            # Create test session
            session = MagicMock()
            session.session_id = f"end_to_end_session_{i}"
            session.persona_type = "TechEarlyAdopter" if i % 2 == 0 else "RemoteDad"
            session.device_type = "mobile" if i % 3 == 0 else "desktop"
            session.persona_confidence = 0.8 + (i * 0.01)
            session.current_stage = "consideration"
            session.device_info = {"user_agent": f"test_agent_{i}"}
            
            # Create personalized content
            content = MagicMock()
            content.personalization_strategy = f"{session.persona_type.lower()}_{session.device_type}"
            
            # Performance data with variation
            performance_data = {
                'conversion_achieved': i % 3 == 0,  # 33% conversion rate
                'engagement_score': 0.6 + (i * 0.02),  # Increasing engagement
                'personalization_effectiveness': 0.7 + (i * 0.015),
                'engagement_metrics': {
                    'time_on_page': 90 + (i * 5),
                    'click_through_rate': 0.1 + (i * 0.005),
                    'bounce_rate': 0.4 - (i * 0.01)
                }
            }
            
            # Collect feedback for each session
            await integration_controller.collect_personalization_feedback(
                session, content, performance_data
            )
            
            # Collect user behavior feedback
            await integration_controller.collect_user_behavior_feedback(
                session.session_id,
                {
                    'engagement_score': performance_data['engagement_score'],
                    'time_on_page': performance_data['engagement_metrics']['time_on_page'],
                    'interactions': i + 3
                }
            )
            
            sessions.append(session)
        
        # Allow feedback processing
        await asyncio.sleep(0.1)
        
        # Process all feedback
        processing_result = await feedback_system.process_feedback_batch(batch_size=50)
        assert processing_result['processed'] >= 10
        
        # Generate insights from collected data
        insights = await feedback_system.generate_learning_insights()
        
        # Create and execute optimization actions
        if insights:
            actions = await feedback_system.create_optimization_actions(insights)
            if actions:
                execution_result = await feedback_system.execute_optimization_actions()
                assert execution_result['executed'] >= 0
        
        # Trigger system-wide optimization
        optimization_result = await integration_controller.trigger_cross_component_optimization()
        assert optimization_result['success'] is not None
        
        # Verify system learned and improved
        final_status = await integration_controller.get_integration_status()
        
        # System should be healthy and active
        assert final_status['system_health_score'] > 0.5
        assert final_status['active_feedback_loops'] >= 4
        assert final_status['learning_velocity'] >= 0.0
        
        # Verify analytics captured the journey
        analytics_dashboard = await analytics_engine.get_real_time_dashboard_data()
        assert 'timestamp' in analytics_dashboard
        
        # Verify optimization system responded
        optimization_status = await optimization_engine.get_optimization_status()
        assert optimization_status['total_goals'] >= 3
        
        # Get final improvement recommendations
        recommendations = await feedback_system.get_improvement_recommendations()
        assert isinstance(recommendations, list)
        
        # Verify the system maintains state and continues learning
        performance_analytics = await feedback_system.get_performance_analytics()
        assert 'time_window' in performance_analytics
    
    @pytest.mark.asyncio
    async def test_system_error_handling_and_recovery(self, setup_system_components):
        """Test system error handling and recovery capabilities"""
        components = await setup_system_components()
        integration_controller = components['integration_controller']
        
        # Initialize system
        await integration_controller.initialize()
        
        # Test handling invalid feedback data
        try:
            await integration_controller.collect_personalization_feedback(
                None,  # Invalid session
                None,  # Invalid content
                {}     # Empty performance data
            )
        except Exception as e:
            # Should handle gracefully
            pass
        
        # System should still be operational
        status = await integration_controller.get_integration_status()
        assert 'system_health_score' in status
        
        # Test handling of invalid A/B test feedback
        try:
            await integration_controller.collect_ab_test_feedback(
                "",    # Empty test ID
                "",    # Empty variant ID
                "",    # Empty session ID
                {}     # Empty performance data
            )
        except Exception as e:
            # Should handle gracefully
            pass
        
        # Test recovery after errors
        valid_session = MagicMock()
        valid_session.session_id = "recovery_session"
        valid_session.persona_type = "TechEarlyAdopter"
        valid_session.device_type = "mobile"
        valid_session.persona_confidence = 0.8
        valid_session.current_stage = "consideration"
        valid_session.device_info = {"user_agent": "recovery_agent"}
        
        valid_content = MagicMock()
        valid_content.personalization_strategy = "recovery_strategy"
        
        valid_performance = {
            'conversion_achieved': True,
            'engagement_score': 0.9,
            'personalization_effectiveness': 0.85,
            'engagement_metrics': {'time_on_page': 120}
        }
        
        # Should work after errors
        await integration_controller.collect_personalization_feedback(
            valid_session, valid_content, valid_performance
        )
        
        # Verify system recovered
        final_status = await integration_controller.get_integration_status()
        assert final_status['system_health_score'] > 0.0

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])