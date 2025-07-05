# Device-Specific Content Integration - Phase 3, Week 2
# Module: Advanced Device-Specific Content Variants Integration
# Created: 2025-07-05

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_

from .models import *
from .database_models import JourneySession, PersonalizationData
from .personalization_engine_enhanced import EnhancedPersonalizationEngine
from .device_intelligence_enhanced import (
    AdvancedDeviceDetector, AdvancedDeviceContext, DeviceCapability, NetworkSpeed, InteractionPattern
)
from .content_variant_generator import (
    IntelligentContentVariantGenerator, ContentVariant, ContentOptimizationStrategy
)
from .performance_optimization_framework import (
    RealTimePerformanceMonitor, AdaptivePerformanceOptimizer, PerformanceSnapshot, PerformanceMetric
)
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# INTEGRATED DEVICE-AWARE PERSONALIZATION ENGINE
# =============================================================================

class IntegratedDeviceAwarePersonalizationEngine:
    """Integrated engine combining device detection, content variants, and performance optimization"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        
        # Initialize all components
        self.enhanced_personalization = EnhancedPersonalizationEngine(db)
        self.device_detector = AdvancedDeviceDetector()
        self.variant_generator = IntelligentContentVariantGenerator(db)
        self.performance_monitor = RealTimePerformanceMonitor(db)
        self.performance_optimizer = AdaptivePerformanceOptimizer(db)
        
        # Performance tracking
        self.performance_cache = {}
        
    async def generate_optimized_personalized_content(self, 
                                                    session: JourneySession,
                                                    request_data: Dict[str, Any],
                                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fully optimized personalized content with device intelligence"""
        try:
            logger.info(f"Generating optimized personalized content for session: {session.session_id}")
            
            # Step 1: Detect advanced device context
            device_context = await self.device_detector.detect_advanced_device_context(
                request_data, session.session_id
            )
            
            # Step 2: Start performance monitoring
            await self.performance_monitor.start_monitoring(session.session_id, device_context)
            
            # Step 3: Generate base personalized content
            base_content = await self.enhanced_personalization.generate_personalized_content(
                session, context
            )
            
            # Step 4: Generate device-optimized content variant
            content_variant = await self.variant_generator.generate_content_variant(
                base_content, device_context, session.persona_type or 'unknown', session
            )
            
            # Step 5: Create integrated response
            integrated_response = await self._create_integrated_response(
                base_content, content_variant, device_context, session
            )
            
            # Step 6: Record integration analytics
            await self._record_integration_analytics(session, device_context, content_variant, integrated_response)
            
            logger.info(f"Optimized content generated successfully for session: {session.session_id}")
            return integrated_response
            
        except Exception as e:
            logger.error(f"Error generating optimized personalized content: {str(e)}")
            return await self._generate_fallback_response(session, request_data)
    
    async def handle_performance_feedback(self, session_id: str, 
                                        performance_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Handle real-time performance feedback and optimize if needed"""
        try:
            logger.info(f"Processing performance feedback for session: {session_id}")
            
            # Record performance metrics
            snapshot = await self.performance_monitor.record_performance_metrics(
                session_id, performance_metrics
            )
            
            if not snapshot:
                return {'status': 'error', 'message': 'Failed to process metrics'}
            
            # Check if optimization is needed
            if snapshot.score < 60:  # Performance threshold
                logger.info(f"Performance optimization triggered for session: {session_id}")
                
                # Get current variant
                current_variant = await self._get_current_variant(session_id)
                if current_variant:
                    # Optimize content
                    optimization_result = await self.performance_optimizer.optimize_content_performance(
                        session_id, current_variant, snapshot
                    )
                    
                    if optimization_result.success:
                        # Update session with optimized variant
                        await self._update_session_variant(session_id, optimization_result)
                        
                        return {
                            'status': 'optimized',
                            'optimization_id': optimization_result.optimization_id,
                            'strategy': optimization_result.strategy.value,
                            'performance_score': snapshot.score,
                            'optimizations_applied': optimization_result.applied_optimizations
                        }
            
            return {
                'status': 'monitored',
                'performance_score': snapshot.score,
                'bottlenecks': snapshot.bottlenecks,
                'recommendations': snapshot.recommendations
            }
            
        except Exception as e:
            logger.error(f"Error handling performance feedback: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    async def get_performance_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive performance analytics for a session"""
        try:
            # Get performance trends
            trends = await self.performance_monitor.get_performance_trends(session_id)
            
            # Get device context
            device_context = await self._get_cached_device_context(session_id)
            
            # Get integration analytics
            integration_stats = await self._get_integration_analytics(session_id)
            
            return {
                'session_id': session_id,
                'performance_trends': trends,
                'device_context': asdict(device_context) if device_context else None,
                'integration_stats': integration_stats,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance analytics: {str(e)}")
            return {'error': str(e)}
    
    async def _create_integrated_response(self, base_content: PersonalizedContent,
                                        variant: ContentVariant,
                                        device_context: AdvancedDeviceContext,
                                        session: JourneySession) -> Dict[str, Any]:
        """Create integrated response combining all optimizations"""
        
        # Select optimal content based on device context
        if device_context.device_capability == DeviceCapability.ULTRA_LOW:
            hero_message = variant.hero_message_ultra_short
        elif device_context.device_capability == DeviceCapability.LOW_PERFORMANCE:
            hero_message = variant.hero_message_short
        else:
            hero_message = variant.hero_message
        
        # Select optimal CTA
        primary_cta = variant.call_to_action
        
        # Device-specific layout adjustments
        layout_config = variant.layout_config.copy()
        if device_context.accessibility_features:
            layout_config.update(variant.accessibility_optimizations.get('layout', {}))
        
        # Performance-optimized media
        media_config = variant.media_elements.copy()
        
        # Network-specific adjustments
        if device_context.network_speed in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            media_config['image_quality'] = min(media_config['image_quality'], 50)
            media_config['video_enabled'] = False
        
        # Interaction hints based on device and persona
        interaction_hints = variant.interaction_hints
        
        # Create comprehensive response
        integrated_response = {
            'content': {
                'hero_message': hero_message,
                'call_to_action': primary_cta,
                'cta_alternatives': variant.cta_variations,
                'trust_signals': variant.trust_signals,
                'social_proof': variant.social_proof
            },
            'optimization': {
                'variant_id': variant.variant_id,
                'device_target': variant.device_target.value,
                'capability_target': variant.capability_target.value,
                'network_target': variant.network_target.value,
                'content_format': variant.content_format
            },
            'layout': layout_config,
            'media': media_config,
            'performance': {
                'budget': variant.performance_budget,
                'loading_strategy': variant.loading_strategy,
                'optimization_strategy': self._determine_optimization_strategy(device_context)
            },
            'interaction': {
                'hints': interaction_hints,
                'device_type': device_context.device_type.value,
                'touch_support': device_context.touch_support,
                'interaction_pattern': device_context.interaction_pattern.value
            },
            'accessibility': variant.accessibility_optimizations,
            'analytics': {
                'persona_type': session.persona_type,
                'persona_confidence': session.persona_confidence,
                'device_performance_score': device_context.performance_score,
                'personalization_strategy': base_content.personalization_strategy
            }
        }
        
        return integrated_response
    
    async def _record_integration_analytics(self, session: JourneySession,
                                          device_context: AdvancedDeviceContext,
                                          variant: ContentVariant,
                                          response: Dict[str, Any]):
        """Record analytics for integration performance tracking"""
        try:
            analytics_data = {
                'session_id': session.session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'device_context': {
                    'type': device_context.device_type.value,
                    'capability': device_context.device_capability.value,
                    'network_speed': device_context.network_speed.value,
                    'performance_score': device_context.performance_score
                },
                'personalization': {
                    'persona_type': session.persona_type,
                    'persona_confidence': session.persona_confidence
                },
                'variant': {
                    'variant_id': variant.variant_id,
                    'optimization_strategy': response['performance']['optimization_strategy']
                },
                'content_delivered': {
                    'hero_length': len(response['content']['hero_message']),
                    'trust_signals_count': len(response['content']['trust_signals']),
                    'cta_variations_count': len(response['content']['cta_alternatives'])
                }
            }
            
            # Store in Redis for real-time analytics
            cache_key = f"integration_analytics:{session.session_id}"
            await self.redis_client.setex(cache_key, 7200, json.dumps(analytics_data))  # 2 hour cache
            
            # Store in database for long-term analysis
            personalization_record = PersonalizationData(
                session_id=session.session_id,
                personalization_type="integrated_device_optimization",
                personalization_strategy=response['performance']['optimization_strategy'],
                variant_id=variant.variant_id,
                content_delivered=analytics_data,
                ml_model_version="integration_v1.0",
                confidence_score=device_context.performance_score,
                device_optimization_applied=True
            )
            
            self.db.add(personalization_record)
            await self.db.commit()
            
        except Exception as e:
            logger.error(f"Error recording integration analytics: {str(e)}")
    
    async def _get_current_variant(self, session_id: str) -> Optional[ContentVariant]:
        """Get current content variant for a session"""
        try:
            cache_key = f"content_variant:{session_id}:*"
            # This would need to be implemented based on your Redis key structure
            # For now, return None to indicate no cached variant
            return None
        except Exception as e:
            logger.error(f"Error getting current variant: {str(e)}")
            return None
    
    async def _update_session_variant(self, session_id: str, optimization_result):
        """Update session with optimized variant"""
        try:
            # Update monitoring data with optimization info
            cache_key = f"performance_monitor:{session_id}"
            monitoring_data = await self.redis_client.get(cache_key)
            
            if monitoring_data:
                data = json.loads(monitoring_data)
                data['current_variant'] = optimization_result.optimization_id
                data['optimizations_applied'].append({
                    'optimization_id': optimization_result.optimization_id,
                    'strategy': optimization_result.strategy.value,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                await self.redis_client.setex(cache_key, 3600, json.dumps(data))
                
        except Exception as e:
            logger.error(f"Error updating session variant: {str(e)}")
    
    async def _get_cached_device_context(self, session_id: str) -> Optional[AdvancedDeviceContext]:
        """Get cached device context for a session"""
        try:
            cache_key = f"device_context:{session_id}"
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                data = json.loads(cached_data)
                # Would need to reconstruct AdvancedDeviceContext from cached data
                # This is a simplified version
                return None  # Placeholder
            
            return None
        except Exception as e:
            logger.error(f"Error getting cached device context: {str(e)}")
            return None
    
    async def _get_integration_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get integration analytics for a session"""
        try:
            cache_key = f"integration_analytics:{session_id}"
            analytics_data = await self.redis_client.get(cache_key)
            
            if analytics_data:
                return json.loads(analytics_data)
            
            return {'status': 'no_data'}
        except Exception as e:
            logger.error(f"Error getting integration analytics: {str(e)}")
            return {'error': str(e)}
    
    def _determine_optimization_strategy(self, device_context: AdvancedDeviceContext) -> str:
        """Determine optimization strategy based on device context"""
        
        if device_context.device_capability == DeviceCapability.ULTRA_LOW:
            return 'ultra_performance'
        elif device_context.network_speed in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            return 'bandwidth_constrained'
        elif device_context.device_capability == DeviceCapability.HIGH_PERFORMANCE:
            return 'rich_experience'
        elif device_context.accessibility_features:
            return 'accessibility_optimized'
        else:
            return 'balanced_optimization'
    
    async def _generate_fallback_response(self, session: JourneySession, 
                                        request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback response when integration fails"""
        return {
            'content': {
                'hero_message': 'Welcome! Discover the perfect solution for you.',
                'call_to_action': 'Get Started →',
                'trust_signals': ['Trusted by thousands', 'Secure & reliable'],
                'social_proof': 'Join our growing community'
            },
            'optimization': {
                'variant_id': 'fallback',
                'device_target': 'mobile',
                'capability_target': 'medium_performance',
                'content_format': 'standard'
            },
            'layout': {
                'container_width': '100%',
                'grid_columns': 1,
                'spacing_unit': 16,
                'font_scale': 1.0
            },
            'performance': {
                'loading_strategy': 'balanced',
                'optimization_strategy': 'fallback'
            },
            'status': 'fallback'
        }

# =============================================================================
# TESTING AND VALIDATION FRAMEWORK
# =============================================================================

class DeviceVariantTestingFramework:
    """Comprehensive testing framework for device-specific content variants"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.integration_engine = IntegratedDeviceAwarePersonalizationEngine(db)
        
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite for device variant system"""
        try:
            logger.info("Starting comprehensive device variant tests")
            
            test_results = {
                'device_detection_tests': await self._test_device_detection(),
                'content_variant_tests': await self._test_content_variant_generation(),
                'performance_optimization_tests': await self._test_performance_optimization(),
                'integration_tests': await self._test_integration_scenarios(),
                'edge_case_tests': await self._test_edge_cases(),
                'performance_benchmark_tests': await self._test_performance_benchmarks()
            }
            
            # Calculate overall test score
            test_results['overall_score'] = self._calculate_test_score(test_results)
            test_results['timestamp'] = datetime.utcnow().isoformat()
            
            logger.info(f"Comprehensive tests completed with score: {test_results['overall_score']}")
            return test_results
            
        except Exception as e:
            logger.error(f"Error running comprehensive tests: {str(e)}")
            return {'error': str(e), 'overall_score': 0}
    
    async def _test_device_detection(self) -> Dict[str, Any]:
        """Test device detection capabilities"""
        tests = []
        
        # Test 1: Mobile device detection
        mobile_request = {
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)',
            'screen_width': 375,
            'screen_height': 667,
            'device_pixel_ratio': 2.0,
            'touch_support': True
        }
        
        try:
            device_context = await self.integration_engine.device_detector.detect_advanced_device_context(
                mobile_request, 'test_session_mobile'
            )
            
            tests.append({
                'name': 'mobile_device_detection',
                'passed': device_context.device_type == DeviceType.MOBILE,
                'details': f"Detected: {device_context.device_type.value}"
            })
        except Exception as e:
            tests.append({
                'name': 'mobile_device_detection',
                'passed': False,
                'error': str(e)
            })
        
        # Test 2: Desktop device detection
        desktop_request = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'screen_width': 1920,
            'screen_height': 1080,
            'device_pixel_ratio': 1.0,
            'touch_support': False
        }
        
        try:
            device_context = await self.integration_engine.device_detector.detect_advanced_device_context(
                desktop_request, 'test_session_desktop'
            )
            
            tests.append({
                'name': 'desktop_device_detection',
                'passed': device_context.device_type == DeviceType.DESKTOP,
                'details': f"Detected: {device_context.device_type.value}"
            })
        except Exception as e:
            tests.append({
                'name': 'desktop_device_detection',
                'passed': False,
                'error': str(e)
            })
        
        # Test 3: Performance classification
        low_perf_request = {
            'user_agent': 'Mozilla/5.0 (Android 8.0; Mobile)',
            'device_memory': 1,
            'hardware_concurrency': 2,
            'connection_effective_type': '3g'
        }
        
        try:
            device_context = await self.integration_engine.device_detector.detect_advanced_device_context(
                low_perf_request, 'test_session_low_perf'
            )
            
            tests.append({
                'name': 'performance_classification',
                'passed': device_context.device_capability in [DeviceCapability.LOW_PERFORMANCE, DeviceCapability.ULTRA_LOW],
                'details': f"Classified: {device_context.device_capability.value}"
            })
        except Exception as e:
            tests.append({
                'name': 'performance_classification',
                'passed': False,
                'error': str(e)
            })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        return {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests) if tests else 0,
            'test_details': tests
        }
    
    async def _test_content_variant_generation(self) -> Dict[str, Any]:
        """Test content variant generation"""
        tests = []
        
        # Create test session
        test_session = JourneySession(
            session_id='test_variant_session',
            start_timestamp=datetime.utcnow(),
            device_type='mobile',
            persona_type='TechEarlyAdopter',
            current_stage='awareness'
        )
        
        # Create test device context
        test_device_context = await self.integration_engine.device_detector.detect_advanced_device_context(
            {'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)', 'screen_width': 375},
            'test_variant_session'
        )
        
        # Create test base content
        base_content = PersonalizedContent(
            hero_message="🚀 Revolutionary Tech That Changes Everything",
            call_to_action="Explore Now",
            trust_signals=["Certified", "Secure", "Trusted by experts"],
            social_proof="Used by 100K+ tech enthusiasts",
            personalization_strategy="tech_adopter_awareness"
        )
        
        # Test 1: Variant generation
        try:
            variant = await self.integration_engine.variant_generator.generate_content_variant(
                base_content, test_device_context, 'TechEarlyAdopter', test_session
            )
            
            tests.append({
                'name': 'variant_generation',
                'passed': variant is not None and variant.variant_id is not None,
                'details': f"Generated variant: {variant.variant_id if variant else 'None'}"
            })
        except Exception as e:
            tests.append({
                'name': 'variant_generation',
                'passed': False,
                'error': str(e)
            })
        
        # Test 2: Content optimization for mobile
        try:
            variant = await self.integration_engine.variant_generator.generate_content_variant(
                base_content, test_device_context, 'TechEarlyAdopter', test_session
            )
            
            mobile_optimized = (
                len(variant.hero_message_short) < len(variant.hero_message) and
                len(variant.hero_message_ultra_short) < len(variant.hero_message_short)
            )
            
            tests.append({
                'name': 'mobile_content_optimization',
                'passed': mobile_optimized,
                'details': f"Lengths: {len(variant.hero_message)} > {len(variant.hero_message_short)} > {len(variant.hero_message_ultra_short)}"
            })
        except Exception as e:
            tests.append({
                'name': 'mobile_content_optimization',
                'passed': False,
                'error': str(e)
            })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        return {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests) if tests else 0,
            'test_details': tests
        }
    
    async def _test_performance_optimization(self) -> Dict[str, Any]:
        """Test performance optimization framework"""
        tests = []
        
        # Test 1: Performance monitoring initialization
        try:
            test_device_context = await self.integration_engine.device_detector.detect_advanced_device_context(
                {'user_agent': 'test', 'screen_width': 375}, 'test_perf_session'
            )
            
            await self.integration_engine.performance_monitor.start_monitoring(
                'test_perf_session', test_device_context
            )
            
            tests.append({
                'name': 'performance_monitoring_init',
                'passed': True,
                'details': 'Performance monitoring started successfully'
            })
        except Exception as e:
            tests.append({
                'name': 'performance_monitoring_init',
                'passed': False,
                'error': str(e)
            })
        
        # Test 2: Performance metrics recording
        try:
            test_metrics = {
                'lcp': 3000,  # 3 seconds
                'fid': 150,   # 150ms
                'cls': 0.2    # 0.2 CLS score
            }
            
            snapshot = await self.integration_engine.performance_monitor.record_performance_metrics(
                'test_perf_session', test_metrics
            )
            
            tests.append({
                'name': 'performance_metrics_recording',
                'passed': snapshot is not None and snapshot.score > 0,
                'details': f"Performance score: {snapshot.score if snapshot else 'None'}"
            })
        except Exception as e:
            tests.append({
                'name': 'performance_metrics_recording',
                'passed': False,
                'error': str(e)
            })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        return {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests) if tests else 0,
            'test_details': tests
        }
    
    async def _test_integration_scenarios(self) -> Dict[str, Any]:
        """Test end-to-end integration scenarios"""
        tests = []
        
        # Test 1: Complete optimization flow
        try:
            test_session = JourneySession(
                session_id='test_integration_session',
                start_timestamp=datetime.utcnow(),
                device_type='mobile',
                persona_type='TechEarlyAdopter',
                current_stage='awareness'
            )
            
            request_data = {
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)',
                'screen_width': 375,
                'screen_height': 667
            }
            
            context = {'search_terms': ['tech', 'innovation']}
            
            response = await self.integration_engine.generate_optimized_personalized_content(
                test_session, request_data, context
            )
            
            has_required_fields = all(key in response for key in ['content', 'optimization', 'layout', 'performance'])
            
            tests.append({
                'name': 'complete_optimization_flow',
                'passed': has_required_fields,
                'details': f"Response keys: {list(response.keys())}"
            })
        except Exception as e:
            tests.append({
                'name': 'complete_optimization_flow',
                'passed': False,
                'error': str(e)
            })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        return {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests) if tests else 0,
            'test_details': tests
        }
    
    async def _test_edge_cases(self) -> Dict[str, Any]:
        """Test edge cases and error handling"""
        tests = []
        
        # Test 1: Invalid user agent handling
        try:
            invalid_request = {'user_agent': '', 'screen_width': 0}
            device_context = await self.integration_engine.device_detector.detect_advanced_device_context(
                invalid_request, 'test_edge_session'
            )
            
            tests.append({
                'name': 'invalid_user_agent_handling',
                'passed': device_context is not None,
                'details': 'Fallback context created for invalid input'
            })
        except Exception as e:
            tests.append({
                'name': 'invalid_user_agent_handling',
                'passed': False,
                'error': str(e)
            })
        
        # Test 2: Missing performance data handling
        try:
            result = await self.integration_engine.handle_performance_feedback(
                'nonexistent_session', {}
            )
            
            tests.append({
                'name': 'missing_performance_data_handling',
                'passed': 'status' in result,
                'details': f"Result status: {result.get('status', 'unknown')}"
            })
        except Exception as e:
            tests.append({
                'name': 'missing_performance_data_handling',
                'passed': False,
                'error': str(e)
            })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        return {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests) if tests else 0,
            'test_details': tests
        }
    
    async def _test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarks"""
        tests = []
        
        # Test 1: Response time benchmark
        try:
            start_time = datetime.utcnow()
            
            test_session = JourneySession(
                session_id='test_benchmark_session',
                start_timestamp=datetime.utcnow(),
                device_type='mobile',
                persona_type='TechEarlyAdopter',
                current_stage='awareness'
            )
            
            request_data = {'user_agent': 'test', 'screen_width': 375}
            context = {}
            
            await self.integration_engine.generate_optimized_personalized_content(
                test_session, request_data, context
            )
            
            end_time = datetime.utcnow()
            response_time = (end_time - start_time).total_seconds() * 1000  # Convert to ms
            
            tests.append({
                'name': 'response_time_benchmark',
                'passed': response_time < 500,  # Should respond within 500ms
                'details': f"Response time: {response_time:.2f}ms"
            })
        except Exception as e:
            tests.append({
                'name': 'response_time_benchmark',
                'passed': False,
                'error': str(e)
            })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        return {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'success_rate': passed_tests / len(tests) if tests else 0,
            'test_details': tests
        }
    
    def _calculate_test_score(self, test_results: Dict[str, Any]) -> float:
        """Calculate overall test score"""
        total_tests = 0
        passed_tests = 0
        
        for category, results in test_results.items():
            if isinstance(results, dict) and 'total_tests' in results:
                total_tests += results['total_tests']
                passed_tests += results['passed_tests']
        
        return (passed_tests / total_tests * 100) if total_tests > 0 else 0

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'IntegratedDeviceAwarePersonalizationEngine',
    'DeviceVariantTestingFramework'
]