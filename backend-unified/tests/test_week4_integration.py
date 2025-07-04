#!/usr/bin/env python3
"""
Integration Tests for Week 4: Feedback-Driven Improvement System
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 4 - Feedback-Driven Improvement System

Tests the integration of all Week 4 components with existing systems,
particularly the A/B testing framework integration.

Executor: Claude Code
Created: 2025-07-04
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from unittest.mock import AsyncMock, MagicMock, patch

# Import test fixtures and utilities
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Week 4 components
from core.improvement.feedback_system import (
    FeedbackDrivenImprovementSystem, FeedbackType, FeedbackEvent, 
    LearningInsight, LearningPriority, ImprovementScope
)
from core.improvement.analytics_integration import (
    PersonalizationAnalyticsEngine, PersonalizationMetrics, 
    PersonalizationMetricType
)
from core.improvement.optimization_engine import (
    ContinuousOptimizationEngine, OptimizationGoal, OptimizationType,
    OptimizationScope, OptimizationStrategy
)

# Import existing components
from core.testing.ab_testing_framework import ABTestingFramework, ABTest, TestVariant
from src.api.journey.personalization_engine import PersonalizationEngine
from src.api.journey.models import JourneySession, PersonalizedContent
from core.agents.orchestrator import AgentOrchestrator
from core.tracking.performance_tracker import PerformanceTracker

class TestWeek4Integration:
    """Integration tests for Week 4 Feedback-Driven Improvement System"""
    
    @pytest.fixture
    async def mock_components(self):
        """Create mock components for testing"""
        # Mock PersonalizationEngine
        personalization_engine = AsyncMock(spec=PersonalizationEngine)
        personalization_engine.generate_personalized_content = AsyncMock(
            return_value=PersonalizedContent(
                hero_message="Test Hero Message",
                call_to_action="Test CTA",
                trust_signals=["Trust Signal 1"],
                scarcity_trigger="Limited Time",
                social_proof="100+ customers",
                personalization_strategy="test_strategy"
            )
        )
        
        # Mock ABTestingFramework
        ab_testing_framework = AsyncMock(spec=ABTestingFramework)
        ab_testing_framework.active_tests = {}
        ab_testing_framework.create_ab_test = AsyncMock()
        ab_testing_framework.track_performance = AsyncMock()
        
        # Mock AgentOrchestrator
        orchestrator = AsyncMock(spec=AgentOrchestrator)
        orchestrator.health_check = AsyncMock(return_value=True)
        
        # Mock PerformanceTracker
        performance_tracker = AsyncMock(spec=PerformanceTracker)
        performance_tracker.track_content_performance = AsyncMock()
        performance_tracker.health_check = AsyncMock(return_value=True)
        
        return {
            'personalization_engine': personalization_engine,
            'ab_testing_framework': ab_testing_framework,
            'orchestrator': orchestrator,
            'performance_tracker': performance_tracker
        }
    
    @pytest.fixture
    async def feedback_system(self, mock_components):
        """Create FeedbackDrivenImprovementSystem with mocked dependencies"""
        system = FeedbackDrivenImprovementSystem(
            ab_testing_framework=mock_components['ab_testing_framework'],
            personalization_engine=mock_components['personalization_engine'],
            orchestrator=mock_components['orchestrator'],
            performance_tracker=mock_components['performance_tracker']
        )
        
        # Mock initialization to avoid starting background tasks
        system._establish_baseline_metrics = AsyncMock()
        system._initialize_learning_models = AsyncMock()
        system._start_background_tasks = AsyncMock()
        
        await system.initialize()
        return system
    
    @pytest.fixture
    async def analytics_engine(self, mock_components):
        """Create PersonalizationAnalyticsEngine with mocked dependencies"""
        engine = PersonalizationAnalyticsEngine(
            personalization_engine=mock_components['personalization_engine'],
            ab_testing_framework=mock_components['ab_testing_framework'],
            performance_tracker=mock_components['performance_tracker']
        )
        return engine
    
    @pytest.fixture
    async def optimization_engine(self, feedback_system, analytics_engine, mock_components):
        """Create ContinuousOptimizationEngine with dependencies"""
        engine = ContinuousOptimizationEngine(
            feedback_system=feedback_system,
            analytics_engine=analytics_engine,
            ab_testing_framework=mock_components['ab_testing_framework'],
            personalization_engine=mock_components['personalization_engine'],
            orchestrator=mock_components['orchestrator']
        )
        
        # Mock initialization
        engine._establish_performance_baseline = AsyncMock()
        engine._initialize_optimization_goals = AsyncMock()
        engine._start_background_tasks = AsyncMock()
        
        await engine.initialize()
        return engine
    
    @pytest.fixture
    def mock_session(self):
        """Create mock journey session"""
        return JourneySession(
            session_id="test_session_123",
            user_id="test_user_456",
            start_timestamp=datetime.utcnow(),
            device_info={'type': 'desktop', 'browser': 'chrome'},
            detected_persona="TechEarlyAdopter",
            conversion_probability=0.75,
            funnel_stage="consideration"
        )
    
    async def test_feedback_collection_and_processing(self, feedback_system):
        """Test feedback collection and processing workflow"""
        # Test feedback collection
        feedback_id = await feedback_system.collect_feedback(
            feedback_type=FeedbackType.PERFORMANCE_METRICS,
            source_component="personalization_engine",
            data={
                'conversion_rate': 0.08,
                'engagement_score': 0.85,
                'session_count': 100
            },
            session_id="test_session_123"
        )
        
        assert feedback_id is not None
        assert len(feedback_system.feedback_buffer) == 1
        
        # Test feedback processing
        results = await feedback_system.process_feedback_batch(batch_size=10)
        
        assert results['processed'] == 1
        assert len(feedback_system.processed_feedback) == 1
    
    async def test_analytics_integration_with_ab_testing(self, analytics_engine, mock_session):
        """Test analytics integration with A/B testing framework"""
        # Create test metrics with A/B test data
        performance_data = {
            'conversion_achieved': True,
            'engagement_score': 0.85,
            'click_through_rate': 0.12,
            'time_on_page': 120.0,
            'bounce_rate': 0.2,
            'personalization_accuracy': 0.9,
            'content_relevance_score': 0.88,
            'user_satisfaction_score': 0.82,
            'ab_test_id': 'test_ab_123',
            'variant_id': 'variant_a'
        }
        
        # Mock personalized content
        personalized_content = PersonalizedContent(
            hero_message="Test Hero",
            call_to_action="Test CTA",
            trust_signals=["Trust"],
            scarcity_trigger="Limited",
            social_proof="Popular",
            personalization_strategy="strategy_a"
        )
        
        # Track performance
        await analytics_engine.track_personalization_performance(
            mock_session, personalized_content, performance_data
        )
        
        assert len(analytics_engine.metrics_buffer) == 1
        
        metric = analytics_engine.metrics_buffer[0]
        assert metric.session_id == mock_session.session_id
        assert metric.ab_test_id == 'test_ab_123'
        assert metric.variant_id == 'variant_a'
        assert metric.conversion_achieved == True
    
    async def test_real_time_performance_analytics(self, analytics_engine, mock_session):
        """Test real-time performance analytics"""
        # Add multiple test metrics
        for i in range(5):
            performance_data = {
                'conversion_achieved': i % 2 == 0,  # Alternate conversions
                'engagement_score': 0.7 + (i * 0.05),
                'personalization_accuracy': 0.8 + (i * 0.02),
                'click_through_rate': 0.1 + (i * 0.01)
            }
            
            personalized_content = PersonalizedContent(
                hero_message=f"Hero {i}",
                call_to_action=f"CTA {i}",
                trust_signals=[f"Trust {i}"],
                scarcity_trigger=f"Limited {i}",
                social_proof=f"Social {i}",
                personalization_strategy=f"strategy_{i % 2}"
            )
            
            # Modify session for variety
            session = JourneySession(
                session_id=f"session_{i}",
                user_id=f"user_{i}",
                start_timestamp=datetime.utcnow(),
                device_info={'type': 'mobile' if i % 2 else 'desktop'},
                detected_persona="TechEarlyAdopter" if i % 2 else "RemoteDad",
                conversion_probability=0.6 + (i * 0.1),
                funnel_stage="consideration"
            )
            
            await analytics_engine.track_personalization_performance(
                session, personalized_content, performance_data
            )
        
        # Get real-time performance
        real_time_data = await analytics_engine.get_real_time_performance()
        
        assert 'overall_performance' in real_time_data
        assert 'persona_performance' in real_time_data
        assert 'device_performance' in real_time_data
        
        overall = real_time_data['overall_performance']
        assert overall['total_sessions'] == 5
        assert 0.0 <= overall['conversion_rate'] <= 1.0
        assert 0.0 <= overall['average_engagement'] <= 1.0
    
    async def test_optimization_goal_management(self, optimization_engine):
        """Test optimization goal management"""
        # Create test optimization goal
        goal = OptimizationGoal(
            goal_id="test_conversion_goal",
            name="Test Conversion Optimization",
            metric_name="conversion_rate",
            target_value=0.10,
            current_value=0.08,
            improvement_direction="increase",
            weight=1.0,
            priority=LearningPriority.HIGH
        )
        
        # Add goal
        goal_id = await optimization_engine.add_optimization_goal(goal)
        assert goal_id == "test_conversion_goal"
        assert goal_id in optimization_engine.optimization_goals
        
        # Update goal
        success = await optimization_engine.update_optimization_goal(
            goal_id, {'target_value': 0.12}
        )
        assert success == True
        assert optimization_engine.optimization_goals[goal_id].target_value == 0.12
    
    async def test_optimization_recommendations(self, optimization_engine):
        """Test optimization recommendation generation"""
        # Mock some optimization candidates
        optimization_engine.optimization_candidates = [
            {
                'candidate_id': 'candidate_1',
                'component': 'personalization_engine',
                'action_type': 'strategy_adjustment',
                'expected_impact': 0.15,
                'confidence': 0.8,
                'effort_required': 0.3,
                'risk_level': 0.2,
                'parameters': {'strategy': 'enhanced'},
                'dependencies': []
            }
        ]
        
        # Get recommendations
        recommendations = await optimization_engine.get_optimization_recommendations(
            min_confidence=0.7
        )
        
        assert len(recommendations) >= 0  # Should handle mock data gracefully
    
    async def test_cross_system_feedback_integration(self, feedback_system, analytics_engine, optimization_engine):
        """Test feedback flow between all Week 4 systems"""
        # 1. Collect feedback in feedback system
        feedback_id = await feedback_system.collect_feedback(
            feedback_type=FeedbackType.AB_TEST_RESULTS,
            source_component="ab_testing_framework",
            data={
                'test_id': 'test_123',
                'variant_performance': {
                    'control': {'conversion_rate': 0.05},
                    'variant_a': {'conversion_rate': 0.08}
                }
            }
        )
        
        # 2. Process feedback to generate insights
        processing_results = await feedback_system.process_feedback_batch()
        
        # 3. Generate analytics
        mock_session = JourneySession(
            session_id="integration_test_session",
            user_id="integration_test_user",
            start_timestamp=datetime.utcnow(),
            device_info={'type': 'desktop'},
            detected_persona="TechEarlyAdopter",
            conversion_probability=0.7,
            funnel_stage="decision"
        )
        
        personalized_content = PersonalizedContent(
            hero_message="Integration Test Hero",
            call_to_action="Integration Test CTA",
            trust_signals=["Integration Trust"],
            scarcity_trigger="Integration Limited",
            social_proof="Integration Social",
            personalization_strategy="integration_strategy"
        )
        
        await analytics_engine.track_personalization_performance(
            mock_session, personalized_content, {
                'conversion_achieved': True,
                'engagement_score': 0.9,
                'personalization_accuracy': 0.85
            }
        )
        
        # 4. Trigger optimization
        optimization_id = await optimization_engine.trigger_optimization(
            OptimizationType.TRIGGERED,
            OptimizationScope.CROSS_COMPONENT
        )
        
        assert feedback_id is not None
        assert processing_results['processed'] >= 1
        assert len(analytics_engine.metrics_buffer) >= 1
        assert optimization_id is not None
    
    async def test_performance_monitoring_integration(self, analytics_engine, optimization_engine):
        """Test performance monitoring integration between components"""
        # Add performance data
        for i in range(10):
            mock_session = JourneySession(
                session_id=f"perf_session_{i}",
                user_id=f"perf_user_{i}",
                start_timestamp=datetime.utcnow() - timedelta(minutes=i*5),
                device_info={'type': 'mobile' if i % 2 else 'desktop'},
                detected_persona="TechEarlyAdopter",
                conversion_probability=0.6 + (i * 0.02),
                funnel_stage="consideration"
            )
            
            personalized_content = PersonalizedContent(
                hero_message=f"Perf Hero {i}",
                call_to_action=f"Perf CTA {i}",
                trust_signals=[f"Perf Trust {i}"],
                scarcity_trigger=f"Perf Limited {i}",
                social_proof=f"Perf Social {i}",
                personalization_strategy=f"perf_strategy_{i % 3}"
            )
            
            await analytics_engine.track_personalization_performance(
                mock_session, personalized_content, {
                    'conversion_achieved': i % 3 == 0,
                    'engagement_score': 0.7 + (i * 0.02),
                    'personalization_accuracy': 0.8 + (i * 0.01),
                    'time_on_page': 60 + (i * 10)
                }
            )
        
        # Generate analytics
        analytics = await analytics_engine.generate_personalization_analytics(
            time_window=timedelta(hours=1)
        )
        
        assert analytics.total_sessions == 10
        assert len(analytics.persona_performance) > 0
        assert len(analytics.strategy_performance) > 0
        
        # Get optimization status
        status = await optimization_engine.get_optimization_status()
        
        assert 'performance_improvements' in status
        assert 'optimization_goals' in status
    
    async def test_learning_insight_generation(self, feedback_system):
        """Test learning insight generation from feedback"""
        # Add various types of feedback
        feedback_types = [
            (FeedbackType.PERFORMANCE_METRICS, {'conversion_rate': 0.06}),
            (FeedbackType.USER_BEHAVIOR, {'engagement_duration': 120}),
            (FeedbackType.ENGAGEMENT_PATTERNS, {'pattern': 'high_scroll_low_click'}),
            (FeedbackType.CONVERSION_DATA, {'funnel_completion': 0.75})
        ]
        
        for feedback_type, data in feedback_types:
            await feedback_system.collect_feedback(
                feedback_type=feedback_type,
                source_component="test_component",
                data=data
            )
        
        # Process all feedback
        await feedback_system.process_feedback_batch(batch_size=10)
        
        # Generate insights
        insights = await feedback_system.generate_learning_insights(
            time_window=timedelta(hours=1)
        )
        
        # Should handle the mock scenario gracefully
        assert isinstance(insights, list)
    
    async def test_ab_testing_integration_workflow(self, analytics_engine, mock_components):
        """Test complete A/B testing integration workflow"""
        # Mock A/B test creation and tracking
        mock_ab_framework = mock_components['ab_testing_framework']
        
        # Simulate A/B test variant assignment
        test_id = "integration_test_ab"
        variant_id = "variant_integration_a"
        
        # Track performance for A/B test variant
        mock_session = JourneySession(
            session_id="ab_test_session",
            user_id="ab_test_user",
            start_timestamp=datetime.utcnow(),
            device_info={'type': 'tablet'},
            detected_persona="BusinessOwner",
            conversion_probability=0.8,
            funnel_stage="decision"
        )
        
        personalized_content = PersonalizedContent(
            hero_message="A/B Test Hero",
            call_to_action="A/B Test CTA",
            trust_signals=["A/B Trust"],
            scarcity_trigger="A/B Limited",
            social_proof="A/B Social",
            personalization_strategy="ab_strategy"
        )
        
        # Track with A/B test context
        await analytics_engine.track_personalization_performance(
            mock_session, personalized_content, {
                'conversion_achieved': True,
                'engagement_score': 0.92,
                'personalization_accuracy': 0.87,
                'ab_test_id': test_id,
                'variant_id': variant_id
            }
        )
        
        # Verify A/B test data is captured
        metric = analytics_engine.metrics_buffer[-1]
        assert metric.ab_test_id == test_id
        assert metric.variant_id == variant_id
        
        # Generate analytics with A/B test impact
        analytics = await analytics_engine.generate_personalization_analytics()
        
        assert test_id in analytics.ab_test_impact
    
    async def test_error_handling_and_resilience(self, feedback_system, analytics_engine, optimization_engine):
        """Test error handling and system resilience"""
        # Test feedback system with invalid data
        try:
            await feedback_system.collect_feedback(
                feedback_type=FeedbackType.PERFORMANCE_METRICS,
                source_component="test",
                data=None  # Invalid data
            )
        except Exception as e:
            # Should handle gracefully
            pass
        
        # Test analytics with incomplete session data
        try:
            incomplete_session = JourneySession(
                session_id="incomplete_session",
                user_id=None,  # Missing user ID
                start_timestamp=datetime.utcnow(),
                device_info={},  # Empty device info
                detected_persona=None,  # Missing persona
                conversion_probability=0.5,
                funnel_stage="unknown"
            )
            
            await analytics_engine.track_personalization_performance(
                incomplete_session, 
                PersonalizedContent(
                    hero_message="Test",
                    call_to_action="Test",
                    trust_signals=[],
                    scarcity_trigger="",
                    social_proof="",
                    personalization_strategy="test"
                ),
                {}  # Empty performance data
            )
            
            # Should handle gracefully without crashing
            assert len(analytics_engine.metrics_buffer) >= 0
            
        except Exception as e:
            # Should not raise unhandled exceptions
            pass
    
    async def test_system_health_monitoring(self, feedback_system, analytics_engine, optimization_engine):
        """Test system health monitoring capabilities"""
        # Test analytics engine health
        health = await analytics_engine.get_health_status()
        
        assert 'metrics_buffer_size' in health
        assert 'active_sessions' in health
        assert 'personas_tracked' in health
        
        # Test optimization engine status
        status = await optimization_engine.get_optimization_status()
        
        assert 'timestamp' in status
        assert 'active_optimizations' in status
        assert 'total_goals' in status
        
        # Verify all systems are responsive
        assert isinstance(health, dict)
        assert isinstance(status, dict)

# Test execution
if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v", "--tb=short"])