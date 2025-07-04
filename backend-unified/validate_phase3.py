#!/usr/bin/env python3
"""
Phase 3 Implementation Validation Script
Tests the enhanced PersonalizationEngine implementation
"""

import sys
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock

def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        print("Testing imports...")
        
        # Test ML models import
        from src.utils.ml_models import (
            PersonalizationModel, 
            RecommendationEngine, 
            RealTimeOptimizer, 
            ContentVariantGenerator,
            ml_model_manager
        )
        print("✓ ML models imported successfully")
        
        # Test personalization engine import
        from src.api.journey.personalization_engine import PersonalizationEngine
        print("✓ PersonalizationEngine imported successfully")
        
        # Test models import
        from src.api.journey.models import (
            JourneyStage, 
            DeviceType, 
            JourneyPath, 
            PersonalizedContent
        )
        print("✓ Journey models imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        return False

async def test_ml_models():
    """Test ML models functionality"""
    try:
        print("\nTesting ML models...")
        
        from src.utils.ml_models import ml_model_manager
        
        # Test model manager initialization
        await ml_model_manager.initialize_models()
        print("✓ ML model manager initialized")
        
        # Test model health
        health = await ml_model_manager.get_model_health()
        assert 'personalization_model' in health
        assert 'recommendation_engine' in health
        print("✓ Model health check passed")
        
        # Test personalization model scoring
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
            'trust_signals': ['Tech certified'],
            'scarcity_trigger': 'Limited beta access',
            'social_proof': 'Join 1000+ tech enthusiasts'
        }
        
        score = await ml_model_manager.personalization_model.score_variant(
            features, variant_content
        )
        assert 0.0 <= score <= 1.0
        print(f"✓ Variant scoring works (score: {score:.3f})")
        
        return True
        
    except Exception as e:
        print(f"✗ ML models error: {str(e)}")
        return False

async def test_personalization_engine():
    """Test enhanced PersonalizationEngine functionality"""
    try:
        print("\nTesting PersonalizationEngine...")
        
        from src.api.journey.personalization_engine import PersonalizationEngine
        from src.api.journey.models import JourneyStage, DeviceType, JourneyPath
        
        # Create mock dependencies
        mock_db = AsyncMock()
        mock_redis = AsyncMock()
        mock_redis.get = AsyncMock(return_value=None)
        mock_redis.setex = AsyncMock()
        
        # Create mock session
        mock_session = Mock()
        mock_session.session_id = "test_session_123"
        mock_session.user_id = "user_456"
        mock_session.persona_type = "TechEarlyAdopter"
        mock_session.device_type = "mobile"
        mock_session.current_stage = JourneyStage.CONSIDERATION.value
        mock_session.journey_path = JourneyPath.MOBILE_TIKTOK_FAST_TRACK.value
        mock_session.conversion_probability = 0.7
        mock_session.start_timestamp = datetime.utcnow() - timedelta(minutes=5)
        mock_session.total_touchpoints = 3
        
        # Create engine instance
        engine = PersonalizationEngine(mock_db)
        engine.redis_client = mock_redis
        print("✓ PersonalizationEngine created")
        
        # Test enhanced engagement analysis
        engagement_data = {
            'engagement_score': 0.8,
            'interaction_count': 5,
            'scroll_depth': 0.7,
            'time_on_page': 120,
            'exit_intent': False
        }
        
        analysis = await engine._analyze_engagement_patterns_enhanced(
            mock_session, engagement_data
        )
        assert 'ml_insights' in analysis
        assert 'confidence_score' in analysis
        print("✓ Enhanced engagement analysis works")
        
        # Test ML optimization opportunities
        opportunities = await engine._identify_optimization_opportunities_ml(
            mock_session, analysis
        )
        assert isinstance(opportunities, list)
        print(f"✓ ML optimization opportunities identified ({len(opportunities)} found)")
        
        # Test user behavior prediction
        prediction = await engine._predict_user_behavior(mock_session, engagement_data)
        assert 'confidence' in prediction
        print("✓ User behavior prediction works")
        
        # Test content preference analysis
        preferences = await engine._analyze_content_preferences(mock_session, engagement_data)
        assert 'confidence' in preferences
        print("✓ Content preference analysis works")
        
        # Test conversion likelihood calculation
        likelihood = await engine._calculate_conversion_likelihood(mock_session, engagement_data)
        assert 'score' in likelihood
        assert 0.0 <= likelihood['score'] <= 1.0
        print(f"✓ Conversion likelihood calculation works (score: {likelihood['score']:.3f})")
        
        return True
        
    except Exception as e:
        print(f"✗ PersonalizationEngine error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_integration():
    """Test integration between components"""
    try:
        print("\nTesting integration...")
        
        from src.api.journey.personalization_engine import PersonalizationEngine
        from src.api.journey.models import JourneyStage, PersonalizedContent
        
        # Create mock dependencies
        mock_db = AsyncMock()
        mock_redis = AsyncMock()
        mock_redis.get = AsyncMock(return_value=None)
        mock_redis.setex = AsyncMock()
        
        # Create mock session
        mock_session = Mock()
        mock_session.session_id = "integration_test_123"
        mock_session.user_id = "user_789"
        mock_session.persona_type = "BusinessOwner"
        mock_session.device_type = "desktop"
        mock_session.current_stage = JourneyStage.DECISION.value
        mock_session.conversion_probability = 0.8
        mock_session.start_timestamp = datetime.utcnow() - timedelta(minutes=10)
        
        # Create engine
        engine = PersonalizationEngine(mock_db)
        engine.redis_client = mock_redis
        
        # Test personalized content generation
        context = {'test': 'context'}
        content = await engine.generate_personalized_content(mock_session, context)
        assert isinstance(content, PersonalizedContent)
        assert len(content.hero_message) > 0
        print("✓ Personalized content generation works")
        
        # Test real-time optimization (mocked)
        engagement_data = {
            'engagement_score': 0.6,
            'interaction_count': 3,
            'scroll_depth': 0.5
        }
        
        # Mock _get_current_content method
        async def mock_get_current_content(session_id):
            return {
                'hero_message': 'Test Message',
                'call_to_action': 'Click Here',
                'trust_signals': ['Trusted'],
                'scarcity_trigger': None,
                'social_proof': None
            }
        
        engine._get_current_content = mock_get_current_content
        
        optimization_result = await engine.optimize_personalization_real_time(
            mock_session, engagement_data
        )
        assert 'optimizations_applied' in optimization_result
        assert 'ml_confidence_score' in optimization_result
        print("✓ Real-time optimization integration works")
        
        # Test performance tracking
        await engine._track_optimization_performance(
            mock_session, [], {'engagement_score': 0.6}
        )
        assert mock_session.session_id in engine.performance_tracker
        print("✓ Performance tracking works")
        
        # Test learning from completion
        await engine.learn_from_session_completion(
            mock_session.session_id, {'engagement_score': 0.8}
        )
        assert mock_session.session_id not in engine.performance_tracker
        print("✓ Learning from session completion works")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_performance():
    """Test basic performance characteristics"""
    try:
        print("\nTesting performance...")
        
        import time
        from src.utils.ml_models import PersonalizationModel
        
        # Test model scoring performance
        model = PersonalizationModel()
        
        features = {
            'persona_type': 'TechEarlyAdopter',
            'journey_stage': 'consideration',
            'device_type': 'mobile',
            'session_duration': 300,
            'conversion_probability': 0.7
        }
        
        variant_content = {
            'hero_message': 'Test message',
            'call_to_action': 'Test CTA',
            'trust_signals': ['Test'],
            'scarcity_trigger': None,
            'social_proof': None
        }
        
        # Time multiple scoring operations
        start_time = time.time()
        
        scores = []
        for i in range(100):
            score = await model.score_variant(features, variant_content)
            scores.append(score)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        assert len(scores) == 100
        assert total_time < 2.0  # Should complete in under 2 seconds
        
        print(f"✓ Performance test passed (100 scorings in {total_time:.3f}s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance error: {str(e)}")
        return False

async def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Phase 3: Personalization Enhancement - Validation Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(test_imports())
    results.append(await test_ml_models())
    results.append(await test_personalization_engine())
    results.append(await test_integration())
    results.append(await test_performance())
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results)
    
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("✅ ALL TESTS PASSED - Phase 3 implementation is ready!")
        return 0
    else:
        print(f"❌ {total_tests - passed_tests} TESTS FAILED - Review implementation")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))