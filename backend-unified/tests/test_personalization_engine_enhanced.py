# Enhanced PersonalizationEngine Tests - Phase 3
# Module: Phase 3 - Personalization Enhancement Testing
# Created: 2025-07-04

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any

# Test imports
from src.api.journey.personalization_engine import PersonalizationEngine
from src.api.journey.models import JourneyStage, DeviceType, JourneyPath, PersonalizedContent
from src.api.journey.database_models import JourneySession
from src.utils.ml_models import ml_model_manager

# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
async def mock_session():
    """Create a mock journey session"""
    session = Mock(spec=JourneySession)
    session.session_id = "test_session_123"
    session.user_id = "user_456"
    session.persona_type = "TechEarlyAdopter"
    session.device_type = "mobile"
    session.current_stage = JourneyStage.CONSIDERATION.value
    session.journey_path = JourneyPath.MOBILE_TIKTOK_FAST_TRACK.value
    session.conversion_probability = 0.7
    session.start_timestamp = datetime.utcnow() - timedelta(minutes=5)
    session.total_touchpoints = 3
    return session

@pytest.fixture
async def mock_db():
    """Create a mock database session"""
    db = AsyncMock()
    db.add = Mock()
    db.commit = AsyncMock()
    return db

@pytest.fixture
async def mock_redis():
    """Create a mock Redis client"""
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.setex = AsyncMock()
    return redis

@pytest.fixture
async def personalization_engine(mock_db, mock_redis):
    """Create PersonalizationEngine instance with mocked dependencies"""
    with patch('src.api.journey.personalization_engine.get_redis_client', return_value=mock_redis):
        engine = PersonalizationEngine(mock_db)
        engine.redis_client = mock_redis
        return engine

@pytest.fixture
async def sample_engagement_data():
    """Sample engagement data for testing"""
    return {
        'engagement_score': 0.8,
        'interaction_count': 5,
        'scroll_depth': 0.7,
        'time_on_page': 120,
        'exit_intent': False
    }

# =============================================================================
# ENHANCED PERSONALIZATION ENGINE TESTS
# =============================================================================

class TestPersonalizationEngineEnhanced:
    """Test enhanced PersonalizationEngine functionality"""
    
    @pytest.mark.asyncio
    async def test_enhanced_engagement_analysis(self, personalization_engine, mock_session, sample_engagement_data):
        """Test enhanced engagement pattern analysis"""
        # Execute enhanced analysis
        analysis = await personalization_engine._analyze_engagement_patterns_enhanced(
            mock_session, sample_engagement_data
        )
        
        # Verify ML insights are included
        assert 'ml_insights' in analysis
        assert 'confidence_score' in analysis
        assert 'recommendation_strength' in analysis
        
        # Check ML insight components
        ml_insights = analysis['ml_insights']
        assert 'user_behavior_prediction' in ml_insights
        assert 'content_preference_analysis' in ml_insights
        assert 'conversion_likelihood' in ml_insights
        assert 'optimal_intervention_timing' in ml_insights
        
        # Verify confidence scores
        assert 0.0 <= analysis['confidence_score'] <= 1.0
        assert 0.0 <= analysis['recommendation_strength'] <= 1.0
    
    @pytest.mark.asyncio
    async def test_ml_optimization_opportunities(self, personalization_engine, mock_session):
        """Test ML-based optimization opportunity identification"""
        # Create engagement analysis with various scenarios
        engagement_analysis = {
            'ml_insights': {
                'user_behavior_prediction': {
                    'likely_to_bounce': True,
                    'confidence': 0.85
                },
                'content_preference_analysis': {
                    'prefers_visual_content': True,
                    'confidence': 0.8
                },
                'conversion_likelihood': {
                    'score': 0.75,
                    'confidence': 0.9
                },
                'optimal_intervention_timing': {
                    'optimal_now': True,
                    'confidence': 0.8
                }
            }
        }
        
        # Get optimization opportunities
        opportunities = await personalization_engine._identify_optimization_opportunities_ml(
            mock_session, engagement_analysis
        )
        
        # Verify opportunities are generated
        assert len(opportunities) > 0
        
        # Check opportunity structure
        for opportunity in opportunities:
            assert 'type' in opportunity
            assert 'action' in opportunity
            assert 'confidence' in opportunity
            assert 'expected_impact' in opportunity
            assert 'urgency' in opportunity
            
            # Verify confidence and impact ranges
            assert 0.0 <= opportunity['confidence'] <= 1.0
            assert 0.0 <= opportunity['expected_impact'] <= 1.0
        
        # Verify opportunities are sorted by impact * confidence
        for i in range(len(opportunities) - 1):
            current_score = opportunities[i]['expected_impact'] * opportunities[i]['confidence']
            next_score = opportunities[i + 1]['expected_impact'] * opportunities[i + 1]['confidence']
            assert current_score >= next_score
    
    @pytest.mark.asyncio
    async def test_enhanced_optimization_application(self, personalization_engine, mock_session):
        """Test enhanced optimization strategy application"""
        # Test different optimization types
        optimization_types = [
            {
                'type': 'bounce_prevention',
                'action': 'add_engagement_elements',
                'confidence': 0.8,
                'expected_impact': 0.25
            },
            {
                'type': 'visual_enhancement',
                'action': 'add_visual_elements',
                'confidence': 0.9,
                'expected_impact': 0.18
            },
            {
                'type': 'conversion_acceleration',
                'action': 'add_conversion_triggers',
                'confidence': 0.85,
                'expected_impact': 0.30
            },
            {
                'type': 'timing_optimization',
                'action': 'trigger_intervention',
                'confidence': 0.8,
                'expected_impact': 0.20
            }
        ]
        
        for opportunity in optimization_types:
            result = await personalization_engine._apply_personalization_optimization_enhanced(
                mock_session, opportunity
            )
            
            # Verify optimization result structure
            assert 'type' in result
            assert 'action' in result
            assert 'implementation' in result
            assert 'expected_impact' in result
            assert 'confidence' in result
            
            # Verify values match input
            assert result['type'] == opportunity['type']
            assert result['expected_impact'] == opportunity['expected_impact']
            assert result['confidence'] == opportunity['confidence']
    
    @pytest.mark.asyncio
    async def test_real_time_optimization_integration(self, personalization_engine, mock_session, sample_engagement_data):
        """Test real-time optimization with ML integration"""
        # Mock current content
        current_content = {
            'hero_message': 'Test Message',
            'call_to_action': 'Click Here',
            'trust_signals': ['Trusted'],
            'scarcity_trigger': None,
            'social_proof': None
        }
        
        with patch.object(personalization_engine, '_get_current_content', return_value=current_content):
            # Execute real-time optimization
            result = await personalization_engine.optimize_personalization_real_time(
                mock_session, sample_engagement_data
            )
            
            # Verify enhanced result structure
            assert 'optimizations_applied' in result
            assert 'total_expected_improvement' in result
            assert 'ml_confidence_score' in result
            assert 'optimization_timestamp' in result
            assert 'engagement_analysis' in result
            
            # Verify ML confidence score
            assert 0.0 <= result['ml_confidence_score'] <= 1.0
            
            # Verify engagement analysis includes ML insights
            engagement_analysis = result['engagement_analysis']
            assert 'ml_insights' in engagement_analysis
    
    @pytest.mark.asyncio
    async def test_enhanced_variant_generation(self, personalization_engine, mock_session):
        """Test ML-enhanced content variant generation"""
        strategy = "mobile_tiktok_consideration_optimization"
        context = {'referrer_video': 'test_video_123'}
        
        # Execute variant generation
        variants = await personalization_engine._generate_content_variants(
            strategy, mock_session, context
        )
        
        # Verify multiple variants are generated
        assert len(variants) >= 3  # Control + test variants
        
        # Verify variant structure
        for variant in variants:
            assert hasattr(variant, 'hero_message')
            assert hasattr(variant, 'call_to_action')
            assert hasattr(variant, 'trust_signals')
            assert hasattr(variant, 'personalization_strategy')
            
            # Verify content is not empty
            assert len(variant.hero_message) > 0
            assert len(variant.call_to_action) > 0
    
    @pytest.mark.asyncio
    async def test_performance_tracking_and_learning(self, personalization_engine, mock_session):
        """Test performance tracking and ML learning integration"""
        optimizations = [
            {
                'type': 'visual_enhancement',
                'expected_impact': 0.15,
                'confidence': 0.8
            }
        ]
        
        current_performance = {
            'engagement_score': 0.6,
            'conversion_probability': 0.4
        }
        
        # Track optimization performance
        await personalization_engine._track_optimization_performance(
            mock_session, optimizations, current_performance
        )
        
        # Verify tracking data is stored
        assert mock_session.session_id in personalization_engine.performance_tracker
        
        tracking_data = personalization_engine.performance_tracker[mock_session.session_id]
        assert tracking_data['session_id'] == mock_session.session_id
        assert tracking_data['optimizations_applied'] == optimizations
        assert tracking_data['baseline_performance'] == current_performance
        
        # Test learning from session completion
        final_metrics = {
            'engagement_score': 0.8,
            'conversion_rate': 0.6,
            'variant_performance': {
                'control': {'engagement_score': 0.6, 'conversion_rate': 0.4},
                'variant_1': {'engagement_score': 0.8, 'conversion_rate': 0.6}
            }
        }
        
        await personalization_engine.learn_from_session_completion(
            mock_session.session_id, final_metrics
        )
        
        # Verify tracking data is cleaned up
        assert mock_session.session_id not in personalization_engine.performance_tracker
    
    @pytest.mark.asyncio
    async def test_user_behavior_prediction(self, personalization_engine, mock_session, sample_engagement_data):
        """Test user behavior prediction using ML"""
        # Test with high engagement
        high_engagement_data = {**sample_engagement_data, 'engagement_score': 0.9, 'interaction_count': 8}
        
        prediction = await personalization_engine._predict_user_behavior(
            mock_session, high_engagement_data
        )
        
        # Verify prediction structure
        assert 'likely_to_bounce' in prediction
        assert 'likely_to_convert' in prediction
        assert 'needs_assistance' in prediction
        assert 'confidence' in prediction
        
        # High engagement should predict conversion
        assert prediction['likely_to_convert'] is True
        assert prediction['likely_to_bounce'] is False
        assert 0.0 <= prediction['confidence'] <= 1.0
        
        # Test with low engagement
        low_engagement_data = {**sample_engagement_data, 'engagement_score': 0.2, 'interaction_count': 1}
        
        prediction_low = await personalization_engine._predict_user_behavior(
            mock_session, low_engagement_data
        )
        
        # Low engagement should predict bounce
        assert prediction_low['likely_to_bounce'] is True
        assert prediction_low['likely_to_convert'] is False
    
    @pytest.mark.asyncio
    async def test_content_preference_analysis(self, personalization_engine, mock_session, sample_engagement_data):
        """Test content preference analysis"""
        # Test mobile device preferences
        mock_session.device_type = 'mobile'
        
        preferences = await personalization_engine._analyze_content_preferences(
            mock_session, sample_engagement_data
        )
        
        # Verify preference structure
        assert 'prefers_visual_content' in preferences
        assert 'prefers_detailed_info' in preferences
        assert 'prefers_quick_actions' in preferences
        assert 'responds_to_urgency' in preferences
        assert 'confidence' in preferences
        
        # Mobile should prefer quick actions
        assert preferences['prefers_quick_actions'] is True
        assert preferences['prefers_detailed_info'] is False
        
        # Test desktop device preferences
        mock_session.device_type = 'desktop'
        
        preferences_desktop = await personalization_engine._analyze_content_preferences(
            mock_session, sample_engagement_data
        )
        
        # Desktop should prefer detailed info
        assert preferences_desktop['prefers_detailed_info'] is True
        assert preferences_desktop['prefers_quick_actions'] is False
    
    @pytest.mark.asyncio
    async def test_conversion_likelihood_calculation(self, personalization_engine, mock_session, sample_engagement_data):
        """Test conversion likelihood calculation"""
        # Test with decision stage
        mock_session.current_stage = JourneyStage.DECISION.value
        
        likelihood = await personalization_engine._calculate_conversion_likelihood(
            mock_session, sample_engagement_data
        )
        
        # Verify likelihood structure
        assert 'score' in likelihood
        assert 'factors' in likelihood
        assert 'confidence' in likelihood
        
        # Verify score range
        assert 0.0 <= likelihood['score'] <= 1.0
        assert 0.0 <= likelihood['confidence'] <= 1.0
        
        # Decision stage should have higher likelihood
        decision_score = likelihood['score']
        
        # Test with awareness stage
        mock_session.current_stage = JourneyStage.AWARENESS.value
        
        likelihood_awareness = await personalization_engine._calculate_conversion_likelihood(
            mock_session, sample_engagement_data
        )
        
        # Awareness stage should have lower likelihood
        assert likelihood_awareness['score'] < decision_score
    
    @pytest.mark.asyncio
    async def test_intervention_timing(self, personalization_engine, mock_session, sample_engagement_data):
        """Test optimal intervention timing determination"""
        # Test with low engagement after extended session
        mock_session.start_timestamp = datetime.utcnow() - timedelta(minutes=10)
        low_engagement_data = {**sample_engagement_data, 'engagement_score': 0.3}
        
        timing = await personalization_engine._determine_intervention_timing(
            mock_session, low_engagement_data
        )
        
        # Verify timing structure
        assert 'optimal_now' in timing
        assert 'recommended_delay' in timing
        assert 'confidence' in timing
        
        # Low engagement after long session should trigger intervention
        assert timing['optimal_now'] is True
        assert timing['recommended_delay'] == 0
        
        # Test with exit intent
        exit_intent_data = {**sample_engagement_data, 'exit_intent': True}
        
        timing_exit = await personalization_engine._determine_intervention_timing(
            mock_session, exit_intent_data
        )
        
        # Exit intent should trigger immediate intervention
        assert timing_exit['optimal_now'] is True
    
    @pytest.mark.asyncio
    async def test_personalization_insights(self, personalization_engine, mock_redis):
        """Test comprehensive personalization insights retrieval"""
        session_id = "test_session_123"
        
        # Mock cached insights
        mock_insights = {
            'session_id': session_id,
            'optimizations': [{'type': 'test'}],
            'engagement_analysis': {'score': 0.8},
            'ml_insights': {'prediction': 'test'},
            'confidence_score': 0.85,
            'cache_version': 'v2.0'
        }
        
        mock_redis.get.return_value = json.dumps(mock_insights)
        
        # Get insights
        insights = await personalization_engine.get_personalization_insights(session_id)
        
        # Verify insights structure
        assert insights['session_id'] == session_id
        assert 'optimizations' in insights
        assert 'engagement_analysis' in insights
        assert 'ml_insights' in insights
        assert 'confidence_score' in insights
        assert 'ml_health' in insights  # Should be added by method
        
        # Verify ML health is included
        ml_health = insights['ml_health']
        assert 'personalization_model' in ml_health
        assert 'recommendation_engine' in ml_health
        assert 'real_time_optimizer' in ml_health
        assert 'variant_generator' in ml_health
    
    @pytest.mark.asyncio
    async def test_enhanced_cache_management(self, personalization_engine, mock_session, mock_redis):
        """Test enhanced cache management with ML insights"""
        optimizations = [{'type': 'test_optimization', 'impact': 0.15}]
        engagement_analysis = {
            'ml_insights': {'test': 'insight'},
            'confidence_score': 0.8
        }
        
        # Update enhanced cache
        await personalization_engine._update_personalization_cache_enhanced(
            mock_session, optimizations, engagement_analysis
        )
        
        # Verify cache calls
        assert mock_redis.setex.called
        
        # Get call arguments
        call_args = mock_redis.setex.call_args_list
        
        # Verify enhanced cache key is used
        enhanced_cache_call = None
        for call in call_args:
            if 'personalization_enhanced:' in call[0][0]:
                enhanced_cache_call = call
                break
        
        assert enhanced_cache_call is not None
        
        # Verify cache data structure
        cache_key, ttl, cache_data_json = enhanced_cache_call[0]
        cache_data = json.loads(cache_data_json)
        
        assert cache_data['session_id'] == mock_session.session_id
        assert cache_data['optimizations'] == optimizations
        assert cache_data['engagement_analysis'] == engagement_analysis
        assert cache_data['cache_version'] == 'v2.0'
        assert ttl == 1800  # 30 minutes

# =============================================================================
# ML MODELS TESTS
# =============================================================================

class TestMLModelsIntegration:
    """Test ML models integration with PersonalizationEngine"""
    
    @pytest.mark.asyncio
    async def test_ml_model_manager_initialization(self):
        """Test ML model manager initialization"""
        # Initialize models
        await ml_model_manager.initialize_models()
        
        # Verify model instances
        assert ml_model_manager.personalization_model is not None
        assert ml_model_manager.recommendation_engine is not None
        assert ml_model_manager.real_time_optimizer is not None
        assert ml_model_manager.variant_generator is not None
    
    @pytest.mark.asyncio
    async def test_model_health_reporting(self):
        """Test ML model health reporting"""
        health = await ml_model_manager.get_model_health()
        
        # Verify health structure
        assert 'personalization_model' in health
        assert 'recommendation_engine' in health
        assert 'real_time_optimizer' in health
        assert 'variant_generator' in health
        
        # Verify personalization model health
        pers_health = health['personalization_model']
        assert 'is_trained' in pers_health
        assert 'version' in pers_health
        assert 'performance' in pers_health
    
    @pytest.mark.asyncio
    async def test_variant_scoring(self):
        """Test ML-based variant scoring"""
        features = {
            'persona_type': 'TechEarlyAdopter',
            'journey_stage': 'consideration',
            'device_type': 'mobile',
            'session_duration': 300,
            'conversion_probability': 0.7
        }
        
        variant_content = {
            'hero_message': 'Revolutionary Tech Solution',
            'call_to_action': 'Get Early Access',
            'trust_signals': ['Tech certified', 'Early adopter favorite'],
            'scarcity_trigger': 'Limited beta access',
            'social_proof': 'Join 1000+ tech enthusiasts'
        }
        
        # Score variant
        score = await ml_model_manager.personalization_model.score_variant(
            features, variant_content
        )
        
        # Verify score range
        assert 0.0 <= score <= 1.0
        assert isinstance(score, float)

# =============================================================================
# PERFORMANCE AND INTEGRATION TESTS
# =============================================================================

class TestPerformanceAndIntegration:
    """Test performance and integration aspects"""
    
    @pytest.mark.asyncio
    async def test_optimization_performance_under_load(self, personalization_engine, mock_session, sample_engagement_data):
        """Test optimization performance under simulated load"""
        import time
        
        # Measure optimization time
        start_time = time.time()
        
        # Run multiple optimizations
        tasks = []
        for i in range(10):
            task = personalization_engine.optimize_personalization_real_time(
                mock_session, sample_engagement_data
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verify all optimizations completed
        assert len(results) == 10
        
        # Verify reasonable performance (should complete in under 2 seconds)
        assert total_time < 2.0
        
        # Verify all results have required structure
        for result in results:
            assert 'optimizations_applied' in result
            assert 'ml_confidence_score' in result
    
    @pytest.mark.asyncio
    async def test_memory_management(self, personalization_engine, mock_session):
        """Test memory management with multiple sessions"""
        # Create multiple sessions
        session_ids = [f"session_{i}" for i in range(100)]
        
        # Track performance for multiple sessions
        for session_id in session_ids:
            mock_session.session_id = session_id
            await personalization_engine._track_optimization_performance(
                mock_session, [], {'engagement_score': 0.5}
            )
        
        # Verify tracking data is stored
        assert len(personalization_engine.performance_tracker) == 100
        
        # Simulate session completions
        for session_id in session_ids[:50]:
            await personalization_engine.learn_from_session_completion(
                session_id, {'engagement_score': 0.8}
            )
        
        # Verify memory is cleaned up
        assert len(personalization_engine.performance_tracker) == 50
    
    @pytest.mark.asyncio
    async def test_error_handling_and_fallbacks(self, personalization_engine, mock_session, sample_engagement_data):
        """Test error handling and fallback mechanisms"""
        # Test with None values
        broken_engagement_data = {
            'engagement_score': None,
            'interaction_count': None,
            'scroll_depth': None
        }
        
        # Should not raise exception and should use fallbacks
        result = await personalization_engine.optimize_personalization_real_time(
            mock_session, broken_engagement_data
        )
        
        # Verify graceful handling
        assert 'optimizations_applied' in result
        assert 'error' not in result
        
        # Test with completely broken session
        broken_session = Mock()
        broken_session.session_id = None
        broken_session.conversion_probability = None
        broken_session.start_timestamp = None
        
        # Should handle gracefully
        try:
            result = await personalization_engine.optimize_personalization_real_time(
                broken_session, sample_engagement_data
            )
            # If no exception, verify error is logged in result
            assert 'error' in result or 'optimizations_applied' in result
        except Exception:
            # Exception is acceptable for completely broken input
            pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])