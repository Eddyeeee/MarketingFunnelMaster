# Unit Tests for Enhanced PersonalizationEngine - Phase 3, Week 1
# Module: Personalization Intelligence Testing
# Created: 2025-07-05

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
import json

from sqlalchemy.ext.asyncio import AsyncSession
from src.api.journey.personalization_engine_enhanced import (
    EnhancedPersonalizationEngine,
    PersonaDetector,
    DeviceOptimizer,
    MobileRenderingStrategy,
    TabletRenderingStrategy,
    DesktopRenderingStrategy,
    ContentEngineIntegration
)
from src.api.journey.models import (
    JourneySession,
    PersonaData,
    DeviceContext,
    DeviceType,
    PersonalizedContent,
    JourneyStage
)

# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_db():
    """Mock database session"""
    db = AsyncMock(spec=AsyncSession)
    return db

@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    redis_client = AsyncMock()
    redis_client.get.return_value = None
    redis_client.setex.return_value = True
    return redis_client

@pytest.fixture
def sample_journey_session():
    """Sample journey session for testing"""
    return JourneySession(
        session_id="test_session_123",
        user_id=None,
        persona_type="TechEarlyAdopter",
        device_type="mobile",
        current_stage=JourneyStage.AWARENESS.value,
        journey_path="mobile_tiktok_fast_track",
        conversion_probability=0.6,
        start_timestamp=datetime.utcnow() - timedelta(minutes=5),
        total_touchpoints=3
    )

@pytest.fixture
def sample_context():
    """Sample context data"""
    return {
        'search_terms': ['smart', 'gadget', 'tech'],
        'page_keywords': ['innovation', 'device'],
        'screen_size': '375x812',
        'user_agent': 'Mozilla/5.0 (iPhone)',
        'connection_speed': '4g',
        'avg_time_per_page': 45,
        'price_interactions': 2,
        'utm_source': 'tiktok'
    }

# =============================================================================
# PERSONA DETECTOR TESTS
# =============================================================================

class TestPersonaDetector:
    """Test PersonaDetector functionality"""
    
    @pytest.fixture
    def persona_detector(self):
        return PersonaDetector()
    
    @pytest.mark.asyncio
    async def test_detect_tech_early_adopter(self, persona_detector):
        """Test detection of TechEarlyAdopter persona"""
        user_data = {
            'search_terms': ['smart home', 'gadget', 'beta test'],
            'page_keywords': ['innovation', 'tech', 'app'],
            'interaction_patterns': ['quick_scroll', 'feature_exploration'],
            'device_type': 'mobile',
            'engagement_metrics': {
                'pages_viewed': 8,
                'avg_time_per_page': 30,
                'price_checks': 1,
                'data_interactions': 3
            }
        }
        
        result = await persona_detector.detect_persona(user_data)
        
        assert result.type == 'TechEarlyAdopter'
        assert result.confidence > 0.7
        assert 'scores' in result.attributes
    
    @pytest.mark.asyncio
    async def test_detect_remote_dad(self, persona_detector):
        """Test detection of RemoteDad persona"""
        user_data = {
            'search_terms': ['work from home', 'family friendly'],
            'page_keywords': ['remote', 'balance', 'secure'],
            'interaction_patterns': ['thorough_reading', 'comparison_shopping'],
            'device_type': 'desktop',
            'engagement_metrics': {
                'pages_viewed': 5,
                'avg_time_per_page': 150,
                'price_checks': 3,
                'data_interactions': 2
            }
        }
        
        with patch('datetime.datetime') as mock_datetime:
            # Set time to evening (21:00)
            mock_datetime.utcnow.return_value.hour = 21
            mock_datetime.utcnow.return_value.weekday.return_value = 6  # Sunday
            
            result = await persona_detector.detect_persona(user_data)
        
        assert result.type == 'RemoteDad'
        assert result.confidence > 0.6
    
    @pytest.mark.asyncio
    async def test_detect_student_hustler(self, persona_detector):
        """Test detection of StudentHustler persona"""
        user_data = {
            'search_terms': ['student discount', 'cheap', 'side hustle'],
            'page_keywords': ['save', 'budget', 'deal'],
            'interaction_patterns': ['price_checking', 'quick_decisions'],
            'device_type': 'mobile',
            'engagement_metrics': {
                'pages_viewed': 4,
                'avg_time_per_page': 20,
                'price_checks': 5,
                'data_interactions': 0
            }
        }
        
        result = await persona_detector.detect_persona(user_data)
        
        assert result.type == 'StudentHustler'
        assert result.confidence > 0.6
    
    @pytest.mark.asyncio
    async def test_detect_business_owner(self, persona_detector):
        """Test detection of BusinessOwner persona"""
        user_data = {
            'search_terms': ['ROI calculator', 'enterprise', 'scale business'],
            'page_keywords': ['growth', 'efficiency', 'business'],
            'interaction_patterns': ['data_analysis', 'roi_calculation'],
            'device_type': 'desktop',
            'engagement_metrics': {
                'pages_viewed': 10,
                'avg_time_per_page': 200,
                'price_checks': 0,
                'data_interactions': 12
            }
        }
        
        with patch('datetime.datetime') as mock_datetime:
            # Set time to business hours (10:00)
            mock_datetime.utcnow.return_value.hour = 10
            mock_datetime.utcnow.return_value.weekday.return_value = 2  # Wednesday
            
            result = await persona_detector.detect_persona(user_data)
        
        assert result.type == 'BusinessOwner'
        assert result.confidence > 0.7
    
    @pytest.mark.asyncio
    async def test_unknown_persona_detection(self, persona_detector):
        """Test handling of ambiguous user data"""
        user_data = {
            'search_terms': [],
            'page_keywords': [],
            'interaction_patterns': [],
            'device_type': 'tablet',
            'engagement_metrics': {}
        }
        
        result = await persona_detector.detect_persona(user_data)
        
        assert result.type in ['TechEarlyAdopter', 'RemoteDad', 'StudentHustler', 'BusinessOwner']
        assert result.confidence < 0.5  # Low confidence for ambiguous data

# =============================================================================
# DEVICE OPTIMIZER TESTS
# =============================================================================

class TestDeviceOptimizer:
    """Test DeviceOptimizer functionality"""
    
    @pytest.fixture
    def device_optimizer(self):
        return DeviceOptimizer()
    
    @pytest.fixture
    def sample_content(self):
        return PersonalizedContent(
            hero_message="This is a very long hero message that should be optimized for different devices to ensure readability",
            call_to_action="Schedule a Consultation Today",
            trust_signals=["Industry Certified", "24/7 Support", "Money Back Guarantee", "Free Shipping", "5-Star Reviews"],
            scarcity_trigger="Limited Time Offer - 50% OFF",
            social_proof="Join over 10,000 satisfied customers who have transformed their business",
            personalization_strategy="test_strategy"
        )
    
    @pytest.mark.asyncio
    async def test_mobile_optimization(self, device_optimizer, sample_content):
        """Test mobile device optimization"""
        device_context = DeviceContext(
            type=DeviceType.MOBILE,
            screen_size="375x812",
            user_agent="iPhone",
            connection_speed="4g"
        )
        
        result = await device_optimizer.optimize_for_device(sample_content, device_context)
        
        # Check mobile optimizations
        assert len(result.hero_message) <= 50 or '...' in result.hero_message
        assert '→' in result.call_to_action
        assert len(result.trust_signals) <= 3
        assert '📱' in result.scarcity_trigger
        if result.social_proof:
            assert len(result.social_proof) <= 40 or '...' in result.social_proof
    
    @pytest.mark.asyncio
    async def test_tablet_optimization(self, device_optimizer, sample_content):
        """Test tablet device optimization"""
        device_context = DeviceContext(
            type=DeviceType.TABLET,
            screen_size="768x1024",
            user_agent="iPad"
        )
        
        result = await device_optimizer.optimize_for_device(sample_content, device_context)
        
        # Check tablet optimizations
        assert len(result.hero_message) <= 80
        assert '👆' in result.call_to_action
        assert all('✓' in signal for signal in result.trust_signals)
    
    @pytest.mark.asyncio
    async def test_desktop_optimization(self, device_optimizer, sample_content):
        """Test desktop device optimization"""
        device_context = DeviceContext(
            type=DeviceType.DESKTOP,
            screen_size="1920x1080",
            user_agent="Chrome"
        )
        
        result = await device_optimizer.optimize_for_device(sample_content, device_context)
        
        # Check desktop optimizations
        # Desktop should have expanded trust signals
        assert any('guarantee' in signal.lower() and 'questions' in signal.lower() 
                  for signal in result.trust_signals)
        # Desktop social proof should be detailed
        if result.social_proof and len(sample_content.social_proof) < 100:
            assert 'case studies' in result.social_proof.lower()

# =============================================================================
# ENHANCED PERSONALIZATION ENGINE TESTS
# =============================================================================

class TestEnhancedPersonalizationEngine:
    """Test EnhancedPersonalizationEngine functionality"""
    
    @pytest.fixture
    def personalization_engine(self, mock_db, mock_redis):
        with patch('src.api.journey.personalization_engine_enhanced.get_redis_client', return_value=mock_redis):
            engine = EnhancedPersonalizationEngine(mock_db)
            return engine
    
    @pytest.mark.asyncio
    async def test_generate_personalized_content_tech_adopter_mobile(
        self, personalization_engine, sample_journey_session, sample_context, mock_redis
    ):
        """Test personalized content generation for TechEarlyAdopter on mobile"""
        # Setup
        sample_journey_session.persona_type = 'TechEarlyAdopter'
        sample_journey_session.device_type = 'mobile'
        
        # Mock ML model responses
        personalization_engine.personalization_model.score_variant = AsyncMock(return_value=0.85)
        
        # Execute
        result = await personalization_engine.generate_personalized_content(
            sample_journey_session, sample_context
        )
        
        # Verify
        assert isinstance(result, PersonalizedContent)
        assert 'tech' in result.hero_message.lower() or 'first' in result.hero_message.lower()
        assert len(result.hero_message) <= 50 or '🚀' in result.hero_message
        assert '→' in result.call_to_action
        assert len(result.trust_signals) <= 3
    
    @pytest.mark.asyncio
    async def test_generate_personalized_content_business_owner_desktop(
        self, personalization_engine, sample_journey_session, sample_context
    ):
        """Test personalized content generation for BusinessOwner on desktop"""
        # Setup
        sample_journey_session.persona_type = 'BusinessOwner'
        sample_journey_session.device_type = 'desktop'
        sample_journey_session.current_stage = JourneyStage.CONSIDERATION.value
        
        # Mock ML model responses
        personalization_engine.personalization_model.score_variant = AsyncMock(return_value=0.75)
        
        # Execute
        result = await personalization_engine.generate_personalized_content(
            sample_journey_session, sample_context
        )
        
        # Verify
        assert isinstance(result, PersonalizedContent)
        assert 'roi' in result.hero_message.lower() or 'scale' in result.hero_message.lower()
        assert 'ROI' in result.call_to_action or 'Executive' in result.call_to_action
        assert any('enterprise' in signal.lower() or 'custom' in signal.lower() 
                  for signal in result.trust_signals)
    
    @pytest.mark.asyncio
    async def test_ml_enhancement_low_conversion_probability(
        self, personalization_engine, sample_journey_session, sample_context
    ):
        """Test ML enhancements for low conversion probability"""
        # Setup
        sample_journey_session.conversion_probability = 0.2
        personalization_engine.personalization_model.score_variant = AsyncMock(return_value=0.4)
        
        # Execute
        result = await personalization_engine.generate_personalized_content(
            sample_journey_session, sample_context
        )
        
        # Verify ML enhancements for low conversion
        assert '🎁' in result.hero_message or '⚡' in result.scarcity_trigger
        assert '50% OFF' in str(result.scarcity_trigger) or 'Risk-Free' in str(result.trust_signals)
    
    @pytest.mark.asyncio
    async def test_fallback_content_on_error(
        self, personalization_engine, sample_journey_session, sample_context
    ):
        """Test fallback content generation on error"""
        # Setup - force an error
        personalization_engine.persona_detector.detect_persona = AsyncMock(
            side_effect=Exception("Test error")
        )
        
        # Execute
        result = await personalization_engine.generate_personalized_content(
            sample_journey_session, sample_context
        )
        
        # Verify fallback content
        assert isinstance(result, PersonalizedContent)
        assert result.personalization_strategy == 'fallback_content'
        assert 'Welcome' in result.hero_message
    
    @pytest.mark.asyncio
    async def test_persona_update_high_confidence(
        self, personalization_engine, sample_journey_session, sample_context, mock_db
    ):
        """Test session persona update with high confidence detection"""
        # Setup
        sample_journey_session.persona_type = 'unknown'
        
        # Execute
        await personalization_engine.generate_personalized_content(
            sample_journey_session, sample_context
        )
        
        # Verify persona update was attempted
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

# =============================================================================
# CONTENT ENGINE INTEGRATION TESTS
# =============================================================================

class TestContentEngineIntegration:
    """Test ContentEngineIntegration functionality"""
    
    @pytest.fixture
    def content_integration(self, personalization_engine):
        return ContentEngineIntegration(personalization_engine)
    
    @pytest.mark.asyncio
    async def test_get_personalized_content_for_landing_page(
        self, content_integration, sample_journey_session, sample_context
    ):
        """Test personalized content for landing page"""
        # Execute
        result = await content_integration.get_personalized_content_for_page(
            sample_journey_session, 'landing', sample_context
        )
        
        # Verify
        assert 'layout' in result
        assert result['layout'] == 'hero_centered'
        assert 'sections' in result
        assert 'hero' in result['sections']
        assert 'meta' in result
        assert 'structured_data' in result
    
    @pytest.mark.asyncio
    async def test_get_personalized_content_for_product_page(
        self, content_integration, sample_journey_session, sample_context
    ):
        """Test personalized content for product page"""
        # Execute
        result = await content_integration.get_personalized_content_for_page(
            sample_journey_session, 'product', sample_context
        )
        
        # Verify
        assert result['layout'] == 'product_showcase'
        assert 'features' in result['sections']
        assert 'pricing' in result['sections']
    
    @pytest.mark.asyncio
    async def test_get_personalized_content_for_checkout_page(
        self, content_integration, sample_journey_session, sample_context
    ):
        """Test personalized content for checkout page"""
        # Setup
        sample_journey_session.current_stage = JourneyStage.DECISION.value
        
        # Execute
        result = await content_integration.get_personalized_content_for_page(
            sample_journey_session, 'checkout', sample_context
        )
        
        # Verify
        assert result['layout'] == 'conversion_focused'
        assert 'trust_badges' in result['sections']
        assert 'payment' in result['sections']
        assert 'guarantees' in result['sections']
    
    @pytest.mark.asyncio
    async def test_meta_generation(self, content_integration, sample_journey_session, sample_context):
        """Test SEO meta tag generation"""
        # Execute
        result = await content_integration.get_personalized_content_for_page(
            sample_journey_session, 'landing', sample_context
        )
        
        # Verify meta tags
        assert 'title' in result['meta']
        assert 'description' in result['meta']
        assert 'og:title' in result['meta']
        assert 'twitter:card' in result['meta']
        # Ensure emojis are stripped from meta title
        assert '🔥' not in result['meta']['title']
        assert '⚡' not in result['meta']['title']

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestPersonaDeviceCombinations:
    """Test various persona-device combinations"""
    
    @pytest.fixture
    def personalization_engine(self, mock_db, mock_redis):
        with patch('src.api.journey.personalization_engine_enhanced.get_redis_client', return_value=mock_redis):
            engine = EnhancedPersonalizationEngine(mock_db)
            engine.personalization_model.score_variant = AsyncMock(return_value=0.8)
            return engine
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("persona,device,stage", [
        ("TechEarlyAdopter", "mobile", JourneyStage.AWARENESS.value),
        ("TechEarlyAdopter", "desktop", JourneyStage.CONSIDERATION.value),
        ("RemoteDad", "tablet", JourneyStage.AWARENESS.value),
        ("RemoteDad", "desktop", JourneyStage.DECISION.value),
        ("StudentHustler", "mobile", JourneyStage.DECISION.value),
        ("BusinessOwner", "desktop", JourneyStage.CONSIDERATION.value),
    ])
    async def test_persona_device_combinations(
        self, personalization_engine, persona, device, stage, sample_context
    ):
        """Test content generation for various persona-device-stage combinations"""
        # Setup
        session = JourneySession(
            session_id=f"test_{persona}_{device}_{stage}",
            persona_type=persona,
            device_type=device,
            current_stage=stage,
            journey_path="standard_conversion_funnel",
            conversion_probability=0.5,
            start_timestamp=datetime.utcnow(),
            total_touchpoints=5
        )
        
        # Execute
        result = await personalization_engine.generate_personalized_content(session, sample_context)
        
        # Verify
        assert isinstance(result, PersonalizedContent)
        assert result.personalization_strategy is not None
        
        # Verify persona-specific content
        if persona == "TechEarlyAdopter":
            assert any(word in result.hero_message.lower() 
                      for word in ['tech', 'innovation', 'feature', 'beta'])
        elif persona == "RemoteDad":
            assert any(word in result.hero_message.lower() 
                      for word in ['family', 'balance', 'work', 'secure'])
        elif persona == "StudentHustler":
            assert any(word in result.hero_message.lower() 
                      for word in ['student', 'save', 'earn', 'discount'])
        elif persona == "BusinessOwner":
            assert any(word in result.hero_message.lower() 
                      for word in ['business', 'scale', 'roi', 'enterprise'])
        
        # Verify device-specific optimizations
        if device == "mobile":
            assert len(result.trust_signals) <= 3
            assert '→' in result.call_to_action
        elif device == "desktop":
            # Desktop should have more detailed content
            assert len(result.hero_message) > 20

# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.fixture
    def personalization_engine(self, mock_db, mock_redis):
        with patch('src.api.journey.personalization_engine_enhanced.get_redis_client', return_value=mock_redis):
            engine = EnhancedPersonalizationEngine(mock_db)
            engine.personalization_model.score_variant = AsyncMock(return_value=0.8)
            return engine
    
    @pytest.mark.asyncio
    async def test_content_generation_performance(
        self, personalization_engine, sample_journey_session, sample_context
    ):
        """Test that content generation completes within acceptable time"""
        import time
        
        start_time = time.time()
        
        # Generate content 10 times
        for _ in range(10):
            await personalization_engine.generate_personalized_content(
                sample_journey_session, sample_context
            )
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        
        # Should complete in under 100ms on average
        assert avg_time < 0.1, f"Average generation time {avg_time:.3f}s exceeds 100ms limit"
    
    @pytest.mark.asyncio
    async def test_concurrent_content_generation(
        self, personalization_engine, sample_context
    ):
        """Test concurrent content generation for multiple sessions"""
        # Create multiple sessions
        sessions = []
        for i in range(20):
            session = JourneySession(
                session_id=f"concurrent_test_{i}",
                persona_type="TechEarlyAdopter" if i % 2 == 0 else "StudentHustler",
                device_type="mobile" if i % 3 == 0 else "desktop",
                current_stage=JourneyStage.AWARENESS.value,
                journey_path="standard_conversion_funnel",
                conversion_probability=0.5 + (i * 0.02),
                start_timestamp=datetime.utcnow(),
                total_touchpoints=i
            )
            sessions.append(session)
        
        # Generate content concurrently
        tasks = [
            personalization_engine.generate_personalized_content(session, sample_context)
            for session in sessions
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Verify all results
        assert len(results) == 20
        assert all(isinstance(r, PersonalizedContent) for r in results)
        # Verify variety in personalization strategies
        strategies = set(r.personalization_strategy for r in results)
        assert len(strategies) > 1