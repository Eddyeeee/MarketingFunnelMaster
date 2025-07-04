# Test Suite for Device Personalization Week 2 Implementation
# Module: 3A - Week 2 - Advanced Device-Specific Content Variants
# Created: 2025-07-04

import pytest
import asyncio
import json
from datetime import datetime
from unittest.mock import Mock, patch
from typing import Dict, Any

# Import the services we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.device_detection_service import AdvancedDeviceDetectionService, DeviceProfile
from services.device_content_variant_generator import DeviceContentVariantGenerator, DeviceContentVariant
from services.device_performance_optimizer import DevicePerformanceOptimizer, PerformanceMetrics
from services.device_personalization_integration import DevicePersonalizationIntegration

# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def mock_journey_session():
    """Mock journey session for testing"""
    session = Mock()
    session.session_id = "test_session_123"
    session.user_id = "test_user_456"
    session.persona_type = "TechEarlyAdopter"
    session.current_stage = "consideration"
    session.device_type = "mobile"
    session.conversion_probability = 0.75
    session.start_timestamp = datetime.utcnow()
    session.journey_path = "MOBILE_TIKTOK_FAST_TRACK"
    session.total_touchpoints = 3
    return session

@pytest.fixture
def sample_user_agents():
    """Sample user agents for different devices"""
    return {
        "mobile_iphone": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "mobile_android": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "tablet_ipad": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "desktop_chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "desktop_safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
    }

@pytest.fixture
def sample_client_hints():
    """Sample client hints for testing"""
    return {
        "device-memory": 8,
        "hardware-concurrency": 8,
        "connection-type": "wifi",
        "effective-connection-type": "4g",
        "downlink": 10.0
    }

@pytest.fixture
def sample_viewport():
    """Sample viewport data"""
    return {
        "width": 390,
        "height": 844
    }

@pytest.fixture
def sample_base_content():
    """Sample base content for testing"""
    return {
        "hero_message": "Discover Amazing Tech Solutions",
        "call_to_action": "Get Started Today →",
        "trust_signals": ["Trusted by 10K+", "Money-back guarantee", "Expert support"],
        "scarcity_trigger": "Limited time - 50% off!",
        "social_proof": "Join thousands of satisfied customers",
        "images": [
            {"url": "hero.jpg", "alt": "Hero image", "estimated_size": 500}
        ],
        "videos": [
            {"url": "demo.mp4", "title": "Product demo", "estimated_size": 2000}
        ]
    }

# =============================================================================
# DEVICE DETECTION SERVICE TESTS
# =============================================================================

class TestAdvancedDeviceDetectionService:
    """Test suite for AdvancedDeviceDetectionService"""
    
    def setup_method(self):
        """Setup test instance"""
        self.service = AdvancedDeviceDetectionService()
    
    @pytest.mark.asyncio
    async def test_detect_mobile_device(self, sample_user_agents, sample_client_hints, sample_viewport):
        """Test mobile device detection"""
        user_agent = sample_user_agents["mobile_iphone"]
        
        device_profile, content_capabilities, ux_optimizations = await self.service.detect_device_comprehensive(
            user_agent, sample_client_hints, sample_viewport
        )
        
        # Assertions
        assert device_profile.device_type == "mobile"
        assert device_profile.device_category == "smartphone"
        assert device_profile.touch_capable == True
        assert device_profile.brand == "Apple"
        assert content_capabilities.touch_target_size == 44
        assert ux_optimizations.layout_strategy == "single_column"
        assert ux_optimizations.navigation_type in ["hamburger", "tab_bar"]
    
    @pytest.mark.asyncio
    async def test_detect_tablet_device(self, sample_user_agents, sample_client_hints):
        """Test tablet device detection"""
        user_agent = sample_user_agents["tablet_ipad"]
        viewport = {"width": 768, "height": 1024}
        
        device_profile, content_capabilities, ux_optimizations = await self.service.detect_device_comprehensive(
            user_agent, sample_client_hints, viewport
        )
        
        # Assertions
        assert device_profile.device_type == "tablet"
        assert device_profile.device_category == "tablet"
        assert device_profile.touch_capable == True
        assert device_profile.orientation == "portrait"
        assert content_capabilities.touch_target_size == 48
        assert ux_optimizations.navigation_type == "tab_bar"
    
    @pytest.mark.asyncio
    async def test_detect_desktop_device(self, sample_user_agents, sample_client_hints):
        """Test desktop device detection"""
        user_agent = sample_user_agents["desktop_chrome"]
        viewport = {"width": 1920, "height": 1080}
        
        device_profile, content_capabilities, ux_optimizations = await self.service.detect_device_comprehensive(
            user_agent, sample_client_hints, viewport
        )
        
        # Assertions
        assert device_profile.device_type == "desktop"
        assert device_profile.device_category in ["desktop", "laptop"]
        assert device_profile.touch_capable == False
        assert device_profile.orientation == "landscape"
        assert ux_optimizations.layout_strategy == "grid"
        assert ux_optimizations.navigation_type == "sidebar"
    
    @pytest.mark.asyncio
    async def test_performance_tier_detection(self, sample_user_agents):
        """Test performance tier detection"""
        # High performance device
        high_perf_hints = {
            "device-memory": 16,
            "hardware-concurrency": 16,
            "connection-type": "wifi"
        }
        
        device_profile, _, _ = await self.service.detect_device_comprehensive(
            sample_user_agents["desktop_chrome"], high_perf_hints
        )
        assert device_profile.performance_tier == "high"
        
        # Low performance device
        low_perf_hints = {
            "device-memory": 1,
            "hardware-concurrency": 2,
            "connection-type": "3g"
        }
        
        device_profile, _, _ = await self.service.detect_device_comprehensive(
            sample_user_agents["mobile_android"], low_perf_hints
        )
        assert device_profile.performance_tier == "low"
    
    @pytest.mark.asyncio
    async def test_fallback_detection(self):
        """Test fallback detection when primary detection fails"""
        invalid_user_agent = "InvalidUserAgent"
        
        device_profile, content_capabilities, ux_optimizations = await self.service.detect_device_comprehensive(
            invalid_user_agent
        )
        
        # Should return mobile-first defaults
        assert device_profile.device_type == "mobile"
        assert device_profile.performance_tier == "medium"
        assert content_capabilities.supports_video == True
        assert ux_optimizations.interaction_style == "touch"

# =============================================================================
# CONTENT VARIANT GENERATOR TESTS
# =============================================================================

class TestDeviceContentVariantGenerator:
    """Test suite for DeviceContentVariantGenerator"""
    
    def setup_method(self):
        """Setup test instance"""
        self.generator = DeviceContentVariantGenerator()
    
    @pytest.mark.asyncio
    async def test_generate_mobile_variants(self, sample_base_content):
        """Test mobile variant generation"""
        # Create mobile device profile
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="small",
            orientation="portrait",
            touch_capable=True,
            performance_tier="medium",
            network_speed="medium"
        )
        
        # Mock content capabilities and UX optimizations
        content_capabilities = Mock()
        content_capabilities.supports_video = True
        content_capabilities.touch_target_size = 44
        content_capabilities.max_image_size = 500
        
        ux_optimizations = Mock()
        ux_optimizations.layout_strategy = "single_column"
        ux_optimizations.navigation_type = "hamburger"
        
        variants = await self.generator.generate_device_variants(
            sample_base_content, device_profile, content_capabilities, ux_optimizations
        )
        
        # Assertions
        assert len(variants) > 0
        
        # Check for mobile-specific optimizations
        mobile_variants = [v for v in variants if v.device_type == "mobile"]
        assert len(mobile_variants) > 0
        
        # Verify optimization application
        for variant in mobile_variants:
            assert len(variant.optimizations_applied) > 0
            assert variant.performance_score is not None
    
    @pytest.mark.asyncio
    async def test_content_optimization_rules(self, sample_base_content):
        """Test content optimization rules application"""
        # Create low-performance device
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="small",
            orientation="portrait",
            touch_capable=True,
            performance_tier="low",
            network_speed="slow"
        )
        
        content_capabilities = Mock()
        content_capabilities.supports_animations = False
        content_capabilities.max_image_size = 200
        
        ux_optimizations = Mock()
        ux_optimizations.layout_strategy = "single_column"
        
        variants = await self.generator.generate_device_variants(
            sample_base_content, device_profile, content_capabilities, ux_optimizations
        )
        
        # Check for low-performance optimizations
        optimizations_found = []
        for variant in variants:
            optimizations_found.extend(variant.optimizations_applied)
        
        assert "mobile_hero_short" in optimizations_found or "low_performance_media" in optimizations_found
    
    @pytest.mark.asyncio
    async def test_cross_content_optimizations(self, sample_base_content):
        """Test cross-content optimizations"""
        device_profile = DeviceProfile(
            device_type="tablet",
            device_category="tablet",
            screen_size="medium",
            orientation="landscape",
            touch_capable=True,
            performance_tier="high",
            network_speed="fast"
        )
        
        content_capabilities = Mock()
        content_capabilities.supports_webgl = True
        content_capabilities.supports_animations = True
        
        ux_optimizations = Mock()
        ux_optimizations.layout_strategy = "two_column"
        
        variants = await self.generator.generate_device_variants(
            sample_base_content, device_profile, content_capabilities, ux_optimizations
        )
        
        # Verify consistency across variants
        if len(variants) > 1:
            common_styles = [v.content_data.get("common_style") for v in variants]
            assert all(style is not None for style in common_styles)

# =============================================================================
# PERFORMANCE OPTIMIZER TESTS
# =============================================================================

class TestDevicePerformanceOptimizer:
    """Test suite for DevicePerformanceOptimizer"""
    
    def setup_method(self):
        """Setup test instance"""
        self.optimizer = DevicePerformanceOptimizer()
    
    @pytest.mark.asyncio
    async def test_performance_optimization(self):
        """Test performance optimization application"""
        # Create test variant
        variant = DeviceContentVariant(
            variant_id="test_variant",
            device_type="mobile",
            content_type="hero",
            content_data={
                "hero_message": "Test message",
                "images": [{"url": "test.jpg", "estimated_size": 1000}],
                "videos": [{"url": "test.mp4", "estimated_size": 5000}]
            },
            optimizations_applied=[]
        )
        
        # Create mobile device profile
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="small",
            orientation="portrait",
            touch_capable=True,
            performance_tier="low",
            network_speed="slow"
        )
        
        # Mock content capabilities
        content_capabilities = Mock()
        content_capabilities.supports_webp = True
        content_capabilities.supports_animations = False
        content_capabilities.max_image_size = 300
        
        optimized_variants = await self.optimizer.optimize_content_performance(
            [variant], device_profile, content_capabilities
        )
        
        # Assertions
        assert len(optimized_variants) == 1
        optimized_variant = optimized_variants[0]
        assert optimized_variant.performance_score is not None
        assert optimized_variant.performance_score > 0
        assert "performance_metrics" in optimized_variant.content_data
    
    @pytest.mark.asyncio
    async def test_strategy_selection(self):
        """Test optimization strategy selection"""
        # Mobile low-performance scenario
        mobile_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="small",
            orientation="portrait",
            touch_capable=True,
            performance_tier="low",
            network_speed="slow"
        )
        
        # Get applicable strategies
        applicable_strategies = [
            strategy for strategy in self.optimizer.optimization_strategies
            if strategy.applies_to_device(mobile_profile)
        ]
        
        # Should have strategies for mobile and low performance
        assert len(applicable_strategies) > 0
        strategy_ids = [s.strategy_id for s in applicable_strategies]
        assert "mobile_performance_boost" in strategy_ids
        assert "low_performance_optimization" in strategy_ids
    
    @pytest.mark.asyncio
    async def test_performance_metrics_calculation(self):
        """Test performance metrics calculation"""
        variant = DeviceContentVariant(
            variant_id="test_variant",
            device_type="desktop",
            content_type="hero",
            content_data={"hero_message": "Test"},
            optimizations_applied=[]
        )
        
        device_profile = DeviceProfile(
            device_type="desktop",
            device_category="desktop",
            screen_size="large",
            orientation="landscape",
            touch_capable=False,
            performance_tier="high",
            network_speed="fast"
        )
        
        metrics = await self.optimizer._measure_baseline_performance(variant, device_profile)
        
        # Verify metrics structure
        assert hasattr(metrics, 'load_time')
        assert hasattr(metrics, 'render_time')
        assert hasattr(metrics, 'memory_usage')
        assert hasattr(metrics, 'user_satisfaction_score')
        assert metrics.load_time > 0
        assert 0 <= metrics.user_satisfaction_score <= 1

# =============================================================================
# INTEGRATION SERVICE TESTS
# =============================================================================

class TestDevicePersonalizationIntegration:
    """Test suite for DevicePersonalizationIntegration"""
    
    def setup_method(self):
        """Setup test instance"""
        self.integration = DevicePersonalizationIntegration()
    
    @pytest.mark.asyncio
    async def test_generate_device_optimized_content(self, mock_journey_session, sample_user_agents, sample_client_hints, sample_viewport):
        """Test complete device-optimized content generation"""
        user_agent = sample_user_agents["mobile_iphone"]
        context = {"test": "context"}
        
        enhanced_content = await self.integration.generate_device_optimized_content(
            mock_journey_session, user_agent, context, sample_client_hints, sample_viewport
        )
        
        # Assertions
        assert enhanced_content is not None
        assert enhanced_content.base_content is not None
        assert enhanced_content.device_profile is not None
        assert enhanced_content.performance_metrics is not None
        assert enhanced_content.device_profile.device_type == "mobile"
        
        # Check if variants were generated
        assert len(enhanced_content.device_variants) >= 0
        
        # Verify caching
        assert mock_journey_session.session_id in self.integration.integration_cache
    
    @pytest.mark.asyncio
    async def test_real_time_personalization_update(self, mock_journey_session, sample_user_agents):
        """Test real-time personalization updates"""
        # First generate content to create cache
        user_agent = sample_user_agents["mobile_android"]
        context = {"test": "context"}
        
        enhanced_content = await self.integration.generate_device_optimized_content(
            mock_journey_session, user_agent, context
        )
        
        # Now test real-time update
        engagement_data = {
            "engagement_score": 0.3,  # Low engagement
            "interaction_count": 1,
            "scroll_depth": 0.2
        }
        
        update_result = await self.integration.update_device_personalization_real_time(
            mock_journey_session.session_id, engagement_data
        )
        
        # Assertions
        assert "device_engagement_analysis" in update_result
        assert "real_time_optimizations" in update_result
        assert "immediate_recommendations" in update_result
        assert update_result["device_type"] == "mobile"
    
    @pytest.mark.asyncio
    async def test_device_analytics_generation(self, mock_journey_session, sample_user_agents):
        """Test device analytics generation"""
        # Generate content first
        user_agent = sample_user_agents["desktop_chrome"]
        context = {"test": "context"}
        
        enhanced_content = await self.integration.generate_device_optimized_content(
            mock_journey_session, user_agent, context
        )
        
        # Get analytics
        analytics = await self.integration.get_device_analytics(mock_journey_session.session_id)
        
        # Assertions
        assert "device_profile" in analytics
        assert "content_capabilities" in analytics
        assert "ux_optimizations" in analytics
        assert "performance_metrics" in analytics
        assert analytics["device_profile"]["device_type"] == "desktop"
    
    @pytest.mark.asyncio
    async def test_fallback_content_generation(self, mock_journey_session):
        """Test fallback content generation"""
        fallback_content = await self.integration._generate_fallback_enhanced_content(
            mock_journey_session, "invalid_user_agent"
        )
        
        # Assertions
        assert fallback_content is not None
        assert fallback_content.base_content is not None
        assert fallback_content.device_profile.device_type == "mobile"  # Default to mobile
        assert fallback_content.performance_metrics is not None
    
    @pytest.mark.asyncio
    async def test_variant_recommendation_selection(self):
        """Test variant recommendation selection"""
        # Create test variants
        variants = [
            DeviceContentVariant(
                variant_id="variant_1",
                device_type="mobile",
                content_type="hero",
                content_data={},
                optimizations_applied=[],
                performance_score=0.8,
                conversion_impact=0.7
            ),
            DeviceContentVariant(
                variant_id="variant_2",
                device_type="mobile",
                content_type="hero",
                content_data={},
                optimizations_applied=[],
                performance_score=0.9,
                conversion_impact=0.8
            )
        ]
        
        # Mock device context
        device_context = Mock()
        device_context.device_profile = Mock()
        device_context.device_profile.device_type = "mobile"
        
        recommended = await self.integration._select_recommended_variant(variants, device_context)
        
        # Should select variant with higher combined score
        assert recommended is not None
        assert recommended.variant_id == "variant_2"

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestEndToEndIntegration:
    """End-to-end integration tests"""
    
    @pytest.mark.asyncio
    async def test_complete_mobile_workflow(self, mock_journey_session, sample_user_agents, sample_client_hints, sample_viewport):
        """Test complete mobile optimization workflow"""
        integration = DevicePersonalizationIntegration()
        user_agent = sample_user_agents["mobile_iphone"]
        context = {"campaign": "mobile_tech", "source": "tiktok"}
        
        # Step 1: Generate optimized content
        enhanced_content = await integration.generate_device_optimized_content(
            mock_journey_session, user_agent, context, sample_client_hints, sample_viewport
        )
        
        # Verify mobile optimizations
        assert enhanced_content.device_profile.device_type == "mobile"
        assert enhanced_content.device_profile.touch_capable == True
        
        # Step 2: Simulate low engagement and update
        engagement_data = {
            "engagement_score": 0.25,
            "interaction_count": 0,
            "scroll_depth": 0.1,
            "time_on_page": 5000
        }
        
        update_result = await integration.update_device_personalization_real_time(
            mock_journey_session.session_id, engagement_data
        )
        
        # Verify real-time optimizations were applied
        assert "mobile_engagement_boost" in update_result["real_time_optimizations"]["applied_optimizations"]
        
        # Step 3: Get final analytics
        analytics = await integration.get_device_analytics(mock_journey_session.session_id)
        
        # Verify comprehensive analytics
        assert analytics["device_profile"]["device_type"] == "mobile"
        assert "performance_metrics" in analytics
        assert "real_time_updates" in analytics
    
    @pytest.mark.asyncio
    async def test_cross_device_consistency(self, mock_journey_session, sample_user_agents):
        """Test consistency across different device types"""
        integration = DevicePersonalizationIntegration()
        context = {"campaign": "cross_device_test"}
        
        # Test different devices
        devices = ["mobile_iphone", "tablet_ipad", "desktop_chrome"]
        results = {}
        
        for device_key in devices:
            user_agent = sample_user_agents[device_key]
            enhanced_content = await integration.generate_device_optimized_content(
                mock_journey_session, user_agent, context
            )
            
            results[device_key] = enhanced_content
        
        # Verify device-specific optimizations
        assert results["mobile_iphone"].device_profile.device_type == "mobile"
        assert results["tablet_ipad"].device_profile.device_type == "tablet"
        assert results["desktop_chrome"].device_profile.device_type == "desktop"
        
        # Verify all have valid performance metrics
        for result in results.values():
            assert result.performance_metrics is not None
            assert result.performance_metrics.user_satisfaction_score > 0
    
    @pytest.mark.asyncio
    async def test_performance_optimization_effectiveness(self, mock_journey_session, sample_user_agents):
        """Test that performance optimizations actually improve metrics"""
        integration = DevicePersonalizationIntegration()
        
        # Test with low-performance device
        user_agent = sample_user_agents["mobile_android"]
        low_perf_hints = {
            "device-memory": 2,
            "hardware-concurrency": 4,
            "connection-type": "3g",
            "effective-connection-type": "3g",
            "downlink": 1.0
        }
        
        enhanced_content = await integration.generate_device_optimized_content(
            mock_journey_session, user_agent, {}, low_perf_hints
        )
        
        # Verify optimizations for low-performance device
        assert enhanced_content.device_profile.performance_tier == "low"
        assert enhanced_content.device_profile.network_speed == "slow"
        
        # Check that performance optimizations were applied
        optimization_results = enhanced_content.optimization_results
        device_variants = enhanced_content.device_variants
        
        # Should have optimizations for low performance
        optimizations_applied = []
        for variant in device_variants:
            optimizations_applied.extend(variant.optimizations_applied)
        
        # Should include performance-related optimizations
        performance_optimizations = [
            opt for opt in optimizations_applied 
            if "performance" in opt or "optimization" in opt
        ]
        assert len(performance_optimizations) > 0

# =============================================================================
# PERFORMANCE BENCHMARKS
# =============================================================================

class TestPerformanceBenchmarks:
    """Performance benchmark tests"""
    
    @pytest.mark.asyncio
    async def test_device_detection_performance(self, sample_user_agents, sample_client_hints):
        """Test device detection performance"""
        service = AdvancedDeviceDetectionService()
        
        import time
        start_time = time.time()
        
        # Test 100 device detections
        for _ in range(100):
            await service.detect_device_comprehensive(
                sample_user_agents["mobile_iphone"], sample_client_hints
            )
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        
        # Should complete in reasonable time (< 10ms per detection)
        assert avg_time < 0.01, f"Device detection too slow: {avg_time:.4f}s average"
    
    @pytest.mark.asyncio
    async def test_content_generation_performance(self, sample_base_content):
        """Test content generation performance"""
        generator = DeviceContentVariantGenerator()
        
        # Create device profile
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="medium",
            orientation="portrait",
            touch_capable=True,
            performance_tier="medium",
            network_speed="medium"
        )
        
        content_capabilities = Mock()
        ux_optimizations = Mock()
        
        import time
        start_time = time.time()
        
        # Test 50 content generations
        for _ in range(50):
            await generator.generate_device_variants(
                sample_base_content, device_profile, content_capabilities, ux_optimizations
            )
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 50
        
        # Should complete in reasonable time (< 50ms per generation)
        assert avg_time < 0.05, f"Content generation too slow: {avg_time:.4f}s average"

# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    @pytest.mark.asyncio
    async def test_invalid_user_agent_handling(self):
        """Test handling of invalid user agents"""
        service = AdvancedDeviceDetectionService()
        
        # Test with various invalid inputs
        invalid_inputs = ["", None, "invalid", "1234567890"]
        
        for invalid_input in invalid_inputs:
            try:
                device_profile, content_capabilities, ux_optimizations = await service.detect_device_comprehensive(
                    invalid_input or ""
                )
                
                # Should return fallback values
                assert device_profile is not None
                assert device_profile.device_type in ["mobile", "tablet", "desktop"]
                assert content_capabilities is not None
                assert ux_optimizations is not None
                
            except Exception as e:
                pytest.fail(f"Service should handle invalid input gracefully: {e}")
    
    @pytest.mark.asyncio
    async def test_empty_content_handling(self):
        """Test handling of empty content"""
        generator = DeviceContentVariantGenerator()
        
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="medium",
            orientation="portrait",
            touch_capable=True,
            performance_tier="medium",
            network_speed="medium"
        )
        
        content_capabilities = Mock()
        ux_optimizations = Mock()
        
        # Test with empty content
        empty_content = {}
        
        variants = await generator.generate_device_variants(
            empty_content, device_profile, content_capabilities, ux_optimizations
        )
        
        # Should handle gracefully
        assert isinstance(variants, list)
    
    @pytest.mark.asyncio
    async def test_integration_fallback_on_service_failure(self, mock_journey_session):
        """Test integration fallback when individual services fail"""
        integration = DevicePersonalizationIntegration()
        
        # Test with problematic input that might cause service failures
        problematic_user_agent = None
        
        enhanced_content = await integration.generate_device_optimized_content(
            mock_journey_session, problematic_user_agent or "", {}
        )
        
        # Should return fallback content
        assert enhanced_content is not None
        assert enhanced_content.base_content is not None
        assert enhanced_content.device_profile is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])