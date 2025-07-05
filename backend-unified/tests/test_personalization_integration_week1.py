# Integration Tests for Enhanced PersonalizationEngine - Phase 3, Week 1
# Module: Personalization Intelligence Integration Testing
# Created: 2025-07-05

import pytest
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.api.journey.models import *
from src.api.journey.database_models import Base, JourneySession as DBJourneySession
from src.api.journey.personalization_engine_enhanced import EnhancedPersonalizationEngine
from src.api.journey.personalization_controller_enhanced import router as enhanced_router
from src.main import app

# =============================================================================
# TEST CONFIGURATION
# =============================================================================

# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test persona-device combinations
TEST_COMBINATIONS = [
    # TechEarlyAdopter variations
    {"persona": "TechEarlyAdopter", "device": "mobile", "source": "tiktok", "stage": "awareness"},
    {"persona": "TechEarlyAdopter", "device": "tablet", "source": "youtube", "stage": "consideration"},
    {"persona": "TechEarlyAdopter", "device": "desktop", "source": "producthunt", "stage": "decision"},
    
    # RemoteDad variations
    {"persona": "RemoteDad", "device": "desktop", "source": "google", "stage": "awareness"},
    {"persona": "RemoteDad", "device": "tablet", "source": "facebook", "stage": "consideration"},
    {"persona": "RemoteDad", "device": "mobile", "source": "email", "stage": "decision"},
    
    # StudentHustler variations
    {"persona": "StudentHustler", "device": "mobile", "source": "instagram", "stage": "awareness"},
    {"persona": "StudentHustler", "device": "mobile", "source": "tiktok", "stage": "consideration"},
    {"persona": "StudentHustler", "device": "desktop", "source": "reddit", "stage": "decision"},
    
    # BusinessOwner variations
    {"persona": "BusinessOwner", "device": "desktop", "source": "linkedin", "stage": "awareness"},
    {"persona": "BusinessOwner", "device": "desktop", "source": "google", "stage": "consideration"},
    {"persona": "BusinessOwner", "device": "tablet", "source": "email", "stage": "decision"},
]

# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def test_db(test_engine):
    """Create test database session"""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture
def test_client():
    """Create test client for API testing"""
    # Add enhanced router to app
    app.include_router(enhanced_router)
    return TestClient(app)

@pytest.fixture
async def sample_sessions(test_db):
    """Create sample journey sessions for testing"""
    sessions = []
    
    for combo in TEST_COMBINATIONS[:6]:  # Create 6 test sessions
        session_id = f"test_{combo['persona']}_{combo['device']}_{combo['stage']}"
        session = DBJourneySession(
            session_id=session_id,
            persona_type=combo['persona'],
            device_type=combo['device'],
            current_stage=combo['stage'],
            journey_path="standard_conversion_funnel",
            conversion_probability=0.5,
            start_timestamp=datetime.utcnow(),
            total_touchpoints=3,
            source_channel=combo['source']
        )
        test_db.add(session)
        sessions.append(session_id)
    
    await test_db.commit()
    return sessions

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestPersonaDeviceIntegration:
    """Test integration of persona detection and device optimization"""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_combo", TEST_COMBINATIONS)
    async def test_end_to_end_personalization_flow(self, test_db, test_combo):
        """Test complete personalization flow for each persona-device combination"""
        # Create test session
        session_id = f"e2e_{test_combo['persona']}_{test_combo['device']}_{test_combo['stage']}"
        session = DBJourneySession(
            session_id=session_id,
            persona_type="unknown",  # Start with unknown persona
            device_type=test_combo['device'],
            current_stage=test_combo['stage'],
            journey_path="standard_conversion_funnel",
            conversion_probability=0.5,
            start_timestamp=datetime.utcnow(),
            total_touchpoints=0,
            source_channel=test_combo['source']
        )
        test_db.add(session)
        await test_db.commit()
        
        # Initialize engine
        engine = EnhancedPersonalizationEngine(test_db)
        
        # Prepare context data for persona detection
        context = self._get_context_for_persona(test_combo['persona'], test_combo['source'])
        
        # Generate personalized content
        result = await engine.generate_personalized_content(session, context)
        
        # Verify results
        assert result is not None
        assert isinstance(result, PersonalizedContent)
        
        # Verify persona was detected and updated
        await test_db.refresh(session)
        if context['search_terms']:  # If we provided good context
            assert session.persona_type == test_combo['persona']
        
        # Verify device optimization was applied
        if test_combo['device'] == 'mobile':
            assert len(result.hero_message) <= 50 or '...' in result.hero_message
            assert '→' in result.call_to_action
            assert len(result.trust_signals) <= 3
        elif test_combo['device'] == 'desktop':
            # Desktop should have more detailed content
            assert len(result.trust_signals) >= 3 or any('detail' in s.lower() for s in result.trust_signals)
        
        # Verify stage-appropriate content
        if test_combo['stage'] == 'awareness':
            assert any(word in result.hero_message.lower() 
                      for word in ['discover', 'new', 'first', 'introducing'])
        elif test_combo['stage'] == 'decision':
            assert result.scarcity_trigger is not None or 'now' in result.call_to_action.lower()
    
    @pytest.mark.asyncio
    async def test_persona_detection_accuracy(self, test_db):
        """Test accuracy of persona detection across different contexts"""
        engine = EnhancedPersonalizationEngine(test_db)
        
        test_cases = [
            {
                'expected_persona': 'TechEarlyAdopter',
                'user_data': {
                    'search_terms': ['beta test', 'new gadget', 'smart home'],
                    'page_keywords': ['innovation', 'technology', 'features'],
                    'interaction_patterns': ['quick_scroll', 'feature_exploration'],
                    'device_type': 'mobile',
                    'engagement_metrics': {'pages_viewed': 8, 'avg_time_per_page': 30}
                }
            },
            {
                'expected_persona': 'RemoteDad',
                'user_data': {
                    'search_terms': ['work from home setup', 'family friendly'],
                    'page_keywords': ['balance', 'secure', 'reliable'],
                    'interaction_patterns': ['thorough_reading', 'comparison_shopping'],
                    'device_type': 'desktop',
                    'engagement_metrics': {'pages_viewed': 5, 'avg_time_per_page': 180}
                }
            },
            {
                'expected_persona': 'StudentHustler',
                'user_data': {
                    'search_terms': ['student discount', 'cheap alternative'],
                    'page_keywords': ['save money', 'budget', 'deal'],
                    'interaction_patterns': ['price_checking', 'quick_decisions'],
                    'device_type': 'mobile',
                    'engagement_metrics': {'pages_viewed': 3, 'price_checks': 5}
                }
            },
            {
                'expected_persona': 'BusinessOwner',
                'user_data': {
                    'search_terms': ['ROI calculator', 'enterprise solution'],
                    'page_keywords': ['scale', 'growth', 'efficiency'],
                    'interaction_patterns': ['data_analysis', 'roi_calculation'],
                    'device_type': 'desktop',
                    'engagement_metrics': {'pages_viewed': 12, 'data_interactions': 15}
                }
            }
        ]
        
        correct_detections = 0
        total_tests = len(test_cases)
        
        for test_case in test_cases:
            result = await engine.persona_detector.detect_persona(test_case['user_data'])
            if result.type == test_case['expected_persona']:
                correct_detections += 1
                assert result.confidence > 0.6  # Should have decent confidence
        
        accuracy = correct_detections / total_tests
        assert accuracy >= 0.75  # Expect at least 75% accuracy
    
    @pytest.mark.asyncio
    async def test_device_optimization_consistency(self, test_db):
        """Test that device optimization is consistent across personas"""
        engine = EnhancedPersonalizationEngine(test_db)
        
        # Test content that should be optimized
        base_content = PersonalizedContent(
            hero_message="This is a very long hero message that should be optimized differently for each device type to ensure maximum readability and engagement",
            call_to_action="Schedule a Comprehensive Consultation Today",
            trust_signals=["Industry Certified", "24/7 Support", "Money Back Guarantee", "Free Shipping", "Expert Reviews"],
            scarcity_trigger="Limited Time Offer - Only 24 Hours Left",
            social_proof="Join over 10,000 satisfied customers who have transformed their lives",
            personalization_strategy="test_strategy"
        )
        
        # Test across all device types
        device_contexts = [
            DeviceContext(type=DeviceType.MOBILE, screen_size="375x812"),
            DeviceContext(type=DeviceType.TABLET, screen_size="768x1024"),
            DeviceContext(type=DeviceType.DESKTOP, screen_size="1920x1080")
        ]
        
        results = {}
        for device_context in device_contexts:
            optimized = await engine.device_optimizer.optimize_for_device(base_content, device_context)
            results[device_context.type] = optimized
        
        # Verify mobile is most concise
        assert len(results[DeviceType.MOBILE].hero_message) <= len(results[DeviceType.TABLET].hero_message)
        assert len(results[DeviceType.MOBILE].trust_signals) <= len(results[DeviceType.TABLET].trust_signals)
        
        # Verify desktop has most detail
        assert len(results[DeviceType.DESKTOP].trust_signals) >= len(results[DeviceType.TABLET].trust_signals)
    
    @pytest.mark.asyncio
    async def test_ml_enhancement_impact(self, test_db):
        """Test the impact of ML enhancements on personalization"""
        engine = EnhancedPersonalizationEngine(test_db)
        
        # Create two sessions with different conversion probabilities
        high_conversion_session = DBJourneySession(
            session_id="test_high_conversion",
            persona_type="TechEarlyAdopter",
            device_type="mobile",
            current_stage="decision",
            conversion_probability=0.8,
            start_timestamp=datetime.utcnow() - timedelta(minutes=10),
            total_touchpoints=5
        )
        
        low_conversion_session = DBJourneySession(
            session_id="test_low_conversion",
            persona_type="TechEarlyAdopter",
            device_type="mobile",
            current_stage="decision",
            conversion_probability=0.2,
            start_timestamp=datetime.utcnow() - timedelta(minutes=2),
            total_touchpoints=1
        )
        
        test_db.add(high_conversion_session)
        test_db.add(low_conversion_session)
        await test_db.commit()
        
        context = {'search_terms': ['gadget'], 'device_type': 'mobile'}
        
        # Generate content for both sessions
        high_conv_content = await engine.generate_personalized_content(high_conversion_session, context)
        low_conv_content = await engine.generate_personalized_content(low_conversion_session, context)
        
        # Low conversion should have stronger incentives
        assert low_conv_content.scarcity_trigger is not None
        assert '50% OFF' in str(low_conv_content.scarcity_trigger) or '🎁' in low_conv_content.hero_message
        
        # High conversion might have subtler approach
        # The ML model should recognize high conversion probability doesn't need aggressive tactics

# =============================================================================
# API INTEGRATION TESTS
# =============================================================================

class TestAPIIntegration:
    """Test API endpoints integration"""
    
    def test_enhanced_personalization_endpoint(self, test_client, sample_sessions):
        """Test enhanced personalization generation endpoint"""
        session_id = sample_sessions[0]
        
        request_data = {
            "session_id": session_id,
            "context_data": {
                "search_terms": ["tech", "gadget"],
                "page_keywords": ["innovation"],
                "screen_size": "375x812",
                "user_agent": "iPhone"
            },
            "optimization_level": "advanced",
            "enable_persona_detection": True,
            "enable_device_optimization": True
        }
        
        response = test_client.post(
            "/api/journey/personalization/v2/generate",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "personalized_content" in data
        assert "persona_detection" in data
        assert "device_optimization" in data
        assert "ml_insights" in data
    
    def test_persona_detection_endpoint(self, test_client, sample_sessions):
        """Test explicit persona detection endpoint"""
        session_id = sample_sessions[0]
        
        request_data = {
            "session_id": session_id,
            "user_data": {
                "search_terms": ["work from home", "family"],
                "page_keywords": ["balance", "secure"],
                "interaction_patterns": ["thorough_reading"],
                "device_type": "desktop",
                "engagement_metrics": {
                    "pages_viewed": 6,
                    "avg_time_per_page": 150
                }
            },
            "update_session": True
        }
        
        response = test_client.post(
            "/api/journey/personalization/v2/detect-persona",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "detected_persona" in data
        assert data["detected_persona"]["type"] == "RemoteDad"
        assert data["confidence_score"] > 0.5
    
    def test_device_optimization_endpoint(self, test_client):
        """Test device-specific optimization endpoint"""
        request_data = {
            "session_id": "test_device_opt",
            "content": {
                "hero_message": "This is a very long message that needs optimization",
                "call_to_action": "Get Started Today",
                "trust_signals": ["Certified", "Secure", "Trusted", "Reliable", "Fast"],
                "scarcity_trigger": "Limited Time Offer",
                "social_proof": "Join thousands of users",
                "personalization_strategy": "test"
            },
            "device_context": {
                "type": "mobile",
                "screen_size": "375x812",
                "user_agent": "iPhone",
                "connection_speed": "4g"
            }
        }
        
        response = test_client.post(
            "/api/journey/personalization/v2/optimize-for-device",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "optimized_content" in data
        
        # Verify optimization was applied
        original = data["original_content"]
        optimized = data["optimized_content"]
        assert len(optimized["trust_signals"]) <= 3  # Mobile optimization
        assert len(optimized["hero_message"]) <= len(original["hero_message"])
    
    def test_personalized_page_content_endpoint(self, test_client, sample_sessions):
        """Test personalized page content generation"""
        session_id = sample_sessions[0]
        
        # Test different page types
        page_types = ["landing", "product", "checkout"]
        
        for page_type in page_types:
            response = test_client.get(
                f"/api/journey/personalization/v2/page-content/{session_id}/{page_type}",
                params={"include_meta": True, "include_structured_data": True}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["page_type"] == page_type
            assert "content" in data
            
            content = data["content"]
            assert "layout" in content
            assert "sections" in content
            assert "meta" in content
            assert "structured_data" in content
            
            # Verify page-specific layouts
            if page_type == "landing":
                assert content["layout"] == "hero_centered"
            elif page_type == "product":
                assert content["layout"] == "product_showcase"
            elif page_type == "checkout":
                assert content["layout"] == "conversion_focused"
    
    def test_persona_performance_analytics_endpoint(self, test_client):
        """Test persona performance analytics endpoint"""
        response = test_client.get(
            "/api/journey/personalization/v2/analytics/persona-performance",
            params={"time_range": "7d", "include_device_breakdown": True}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "persona_performance" in data
        assert "aggregate_metrics" in data
        assert "insights" in data
        
        # Verify all personas are included
        personas = ["TechEarlyAdopter", "RemoteDad", "StudentHustler", "BusinessOwner"]
        for persona in personas:
            assert persona in data["persona_performance"]
            assert "device_breakdown" in data["persona_performance"][persona]

# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformanceIntegration:
    """Test performance characteristics of integrated system"""
    
    @pytest.mark.asyncio
    async def test_bulk_personalization_performance(self, test_db):
        """Test performance with multiple concurrent personalizations"""
        import time
        
        # Create 50 test sessions
        sessions = []
        for i in range(50):
            combo = TEST_COMBINATIONS[i % len(TEST_COMBINATIONS)]
            session = DBJourneySession(
                session_id=f"perf_test_{i}",
                persona_type=combo['persona'],
                device_type=combo['device'],
                current_stage=combo['stage'],
                conversion_probability=0.5 + (i % 5) * 0.1,
                start_timestamp=datetime.utcnow() - timedelta(minutes=i),
                total_touchpoints=i % 10
            )
            test_db.add(session)
            sessions.append(session)
        
        await test_db.commit()
        
        # Initialize engine
        engine = EnhancedPersonalizationEngine(test_db)
        
        # Generate personalized content for all sessions
        start_time = time.time()
        
        tasks = []
        for session in sessions:
            context = {
                'search_terms': ['test'],
                'device_type': session.device_type,
                'avg_time_per_page': 60
            }
            task = engine.generate_personalized_content(session, context)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_request = total_time / len(sessions)
        
        # Verify results
        assert len(results) == 50
        assert all(isinstance(r, PersonalizedContent) for r in results)
        
        # Performance assertions
        assert avg_time_per_request < 0.1  # Should average under 100ms per request
        assert total_time < 5.0  # Total should complete in under 5 seconds
        
        print(f"Bulk personalization performance: {avg_time_per_request*1000:.2f}ms per request")
    
    @pytest.mark.asyncio
    async def test_caching_effectiveness(self, test_db):
        """Test that caching improves performance for repeated requests"""
        import time
        
        # Create test session
        session = DBJourneySession(
            session_id="cache_test",
            persona_type="TechEarlyAdopter",
            device_type="mobile",
            current_stage="awareness",
            conversion_probability=0.6,
            start_timestamp=datetime.utcnow(),
            total_touchpoints=3
        )
        test_db.add(session)
        await test_db.commit()
        
        engine = EnhancedPersonalizationEngine(test_db)
        context = {'search_terms': ['gadget'], 'device_type': 'mobile'}
        
        # First request (cache miss)
        start_time = time.time()
        result1 = await engine.generate_personalized_content(session, context)
        first_request_time = time.time() - start_time
        
        # Second request (should hit cache)
        start_time = time.time()
        result2 = await engine.generate_personalized_content(session, context)
        second_request_time = time.time() - start_time
        
        # Cache should make second request faster
        assert second_request_time < first_request_time * 0.5  # At least 50% faster
        
        # Results should be consistent
        assert result1.personalization_strategy == result2.personalization_strategy

# =============================================================================
# HELPER METHODS
# =============================================================================

def _get_context_for_persona(persona: str, source: str) -> Dict[str, Any]:
    """Get appropriate context data for persona detection"""
    contexts = {
        'TechEarlyAdopter': {
            'search_terms': ['beta test', 'new tech', 'gadget'],
            'page_keywords': ['innovation', 'features', 'smart'],
            'interaction_patterns': ['quick_scroll', 'feature_exploration'],
            'avg_time_per_page': 30,
            'price_interactions': 1,
            'data_interactions': 5
        },
        'RemoteDad': {
            'search_terms': ['work from home', 'family', 'balance'],
            'page_keywords': ['secure', 'reliable', 'family-friendly'],
            'interaction_patterns': ['thorough_reading', 'comparison_shopping'],
            'avg_time_per_page': 150,
            'price_interactions': 3,
            'data_interactions': 2
        },
        'StudentHustler': {
            'search_terms': ['student discount', 'cheap', 'budget'],
            'page_keywords': ['save', 'deal', 'affordable'],
            'interaction_patterns': ['price_checking', 'quick_decisions'],
            'avg_time_per_page': 25,
            'price_interactions': 6,
            'data_interactions': 0
        },
        'BusinessOwner': {
            'search_terms': ['ROI', 'enterprise', 'scale'],
            'page_keywords': ['growth', 'efficiency', 'business'],
            'interaction_patterns': ['data_analysis', 'roi_calculation'],
            'avg_time_per_page': 200,
            'price_interactions': 0,
            'data_interactions': 15
        }
    }
    
    base_context = contexts.get(persona, {
        'search_terms': [],
        'page_keywords': [],
        'interaction_patterns': [],
        'avg_time_per_page': 60,
        'price_interactions': 2,
        'data_interactions': 3
    })
    
    base_context['utm_source'] = source
    base_context['referrer'] = f"https://{source}.com"
    
    return base_context