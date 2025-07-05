# A/B Testing Integration Layer - Week 3 Implementation
# Module: 3A - Week 3 - PersonalizationEngine-VariantGenerator-ABTesting Integration
# Created: 2025-07-05

import asyncio
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_

from .models import *
from .database_models import JourneySession, PersonalizationData
from .personalization_engine_enhanced import EnhancedPersonalizationEngine
from .device_content_variant_generator import DeviceContentVariantGenerator, DeviceContentVariant
from .device_variant_integration import IntegratedDeviceAwarePersonalizationEngine
from .ab_testing_framework import (
    ABTestingFramework, ABTest, ABTestVariant, TestStatus, TestType, OptimizationGoal
)
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# INTEGRATED A/B TESTING PERSONALIZATION ENGINE
# =============================================================================

class ABTestingPersonalizationEngine:
    """Integrated engine combining A/B testing with personalization and device optimization"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        
        # Initialize core components
        self.personalization_engine = EnhancedPersonalizationEngine(db)
        self.variant_generator = DeviceContentVariantGenerator()
        self.integrated_engine = IntegratedDeviceAwarePersonalizationEngine(db)
        self.ab_testing_framework = ABTestingFramework(db)
        
        # Performance tracking
        self.performance_cache = {}
        self.test_performance_threshold = 0.8
        
    async def generate_ab_tested_content(self, session: JourneySession,
                                       request_data: Dict[str, Any],
                                       context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content that combines A/B testing with personalization and device optimization"""
        try:
            logger.info(f"Generating A/B tested content for session: {session.session_id}")
            
            # Step 1: Check for active A/B tests
            test_assignment = await self.ab_testing_framework.assign_user_to_test_variant(
                session, request_data, context
            )
            
            if test_assignment:
                # User is in an A/B test - generate test-specific content
                logger.info(f"Session {session.session_id} assigned to test {test_assignment['test_id']}, variant {test_assignment['variant_id']}")
                
                # Generate personalized content based on A/B test variant
                personalized_content = await self._generate_ab_test_personalized_content(
                    session, test_assignment, request_data, context
                )
                
                # Add A/B test metadata
                personalized_content['ab_testing'] = {
                    'test_id': test_assignment['test_id'],
                    'variant_id': test_assignment['variant_id'],
                    'variant_name': test_assignment['variant_name'],
                    'is_control': test_assignment['is_control'],
                    'test_metadata': test_assignment['test_metadata']
                }
                
                # Record A/B test content delivery
                await self._record_ab_test_content_delivery(session, test_assignment, personalized_content)
                
                return personalized_content
                
            else:
                # No active A/B test - use standard optimization
                logger.info(f"No active A/B test for session {session.session_id}, using standard optimization")
                
                return await self.integrated_engine.generate_optimized_personalized_content(
                    session, request_data, context
                )
                
        except Exception as e:
            logger.error(f"Error generating A/B tested content: {str(e)}")
            # Fallback to standard optimization
            return await self.integrated_engine.generate_optimized_personalized_content(
                session, request_data, context
            )
    
    async def record_ab_test_interaction(self, session_id: str, interaction_data: Dict[str, Any]) -> bool:
        """Record user interaction for A/B testing analytics"""
        try:
            # Get current A/B test assignment
            assignment = await self._get_ab_test_assignment(session_id)
            
            if not assignment:
                return False
            
            # Enhance interaction data with A/B test context
            enhanced_interaction = {
                **interaction_data,
                'test_id': assignment['test_id'],
                'variant_id': assignment['variant_id'],
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Store interaction for analytics
            interaction_key = f"ab_interaction:{assignment['test_id']}:{assignment['variant_id']}:{session_id}:{datetime.utcnow().timestamp()}"
            await self.redis_client.setex(interaction_key, 86400, json.dumps(enhanced_interaction))
            
            # Update real-time metrics
            await self._update_ab_test_metrics(assignment['test_id'], assignment['variant_id'], interaction_data)
            
            # Check if this is a conversion event
            if interaction_data.get('event_type') in ['purchase', 'signup', 'download', 'contact']:
                await self.ab_testing_framework.record_conversion_event(
                    session_id, interaction_data['event_type'], interaction_data
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recording A/B test interaction: {str(e)}")
            return False
    
    async def get_ab_test_performance_dashboard(self, test_id: str = None) -> Dict[str, Any]:
        """Get comprehensive A/B test performance dashboard"""
        try:
            if test_id:
                # Get specific test performance
                test_results = await self.ab_testing_framework.get_test_results(test_id)
                
                # Enhance with personalization and device optimization insights
                enhanced_results = await self._enhance_test_results_with_insights(test_results)
                
                return {
                    'test_results': enhanced_results,
                    'performance_analysis': await self._analyze_test_performance(test_results),
                    'optimization_recommendations': await self._generate_optimization_recommendations(test_results)
                }
            else:
                # Get dashboard for all active tests
                active_tests = await self._get_active_tests()
                dashboard_data = []
                
                for test in active_tests:
                    test_summary = await self._get_test_summary(test['test_id'])
                    dashboard_data.append(test_summary)
                
                return {
                    'active_tests': dashboard_data,
                    'overall_statistics': await self._calculate_overall_statistics(dashboard_data),
                    'system_performance': await self._get_system_performance_metrics()
                }
                
        except Exception as e:
            logger.error(f"Error getting A/B test dashboard: {str(e)}")
            return {'error': str(e)}
    
    async def optimize_existing_tests(self) -> Dict[str, Any]:
        """Run optimization on all active A/B tests"""
        try:
            logger.info("Running optimization on all active A/B tests")
            
            active_tests = await self._get_active_tests()
            optimization_results = []
            
            for test in active_tests:
                test_id = test['test_id']
                
                # Run real-time optimization check
                optimization_result = await self.ab_testing_framework.real_time_optimization_check(test_id)
                optimization_results.append({
                    'test_id': test_id,
                    'test_name': test['test_name'],
                    **optimization_result
                })
                
                # If optimization was performed, update personalization strategies
                if optimization_result.get('optimization_performed'):
                    await self._update_personalization_strategies(test_id, optimization_result)
            
            return {
                'total_tests_checked': len(active_tests),
                'optimizations_performed': sum(1 for r in optimization_results if r.get('optimization_performed')),
                'optimization_results': optimization_results,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing existing tests: {str(e)}")
            return {'error': str(e)}

    # =============================================================================
    # A/B TEST CONTENT GENERATION
    # =============================================================================

    async def _generate_ab_test_personalized_content(self, session: JourneySession,
                                                   test_assignment: Dict[str, Any],
                                                   request_data: Dict[str, Any],
                                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized content based on A/B test variant configuration"""
        try:
            # Get test variant configuration
            variant_config = await self._get_variant_configuration(
                test_assignment['test_id'], test_assignment['variant_id']
            )
            
            if not variant_config:
                # Fallback to standard personalization
                return await self.integrated_engine.generate_optimized_personalized_content(
                    session, request_data, context
                )
            
            # Apply variant-specific personalization strategy
            modified_context = await self._apply_variant_context_modifications(context, variant_config)
            
            # Generate base personalized content with variant modifications
            if variant_config.get('use_enhanced_personalization', True):
                base_content = await self.personalization_engine.generate_personalized_content(
                    session, modified_context
                )
            else:
                # Use simplified personalization for control group
                base_content = await self._generate_simplified_personalized_content(session, modified_context)
            
            # Apply variant-specific device optimizations
            if variant_config.get('apply_device_optimization', True):
                device_context = await self._get_device_context(session, request_data)
                device_optimized_content = await self._apply_variant_device_optimizations(
                    base_content, device_context, variant_config
                )
            else:
                device_optimized_content = base_content
            
            # Apply variant-specific content modifications
            final_content = await self._apply_variant_content_modifications(
                device_optimized_content, variant_config
            )
            
            # Add variant tracking information
            final_content['variant_tracking'] = {
                'content_strategy': variant_config.get('content_strategy', 'standard'),
                'device_optimization_level': variant_config.get('device_optimization_level', 'standard'),
                'personalization_level': variant_config.get('personalization_level', 'enhanced')
            }
            
            return final_content
            
        except Exception as e:
            logger.error(f"Error generating A/B test personalized content: {str(e)}")
            # Fallback to standard optimization
            return await self.integrated_engine.generate_optimized_personalized_content(
                session, request_data, context
            )

    async def _apply_variant_context_modifications(self, context: Dict[str, Any], 
                                                 variant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply variant-specific modifications to context"""
        modified_context = context.copy()
        
        # Apply content emphasis modifications
        if 'content_emphasis' in variant_config:
            emphasis = variant_config['content_emphasis']
            
            if emphasis == 'urgency_focused':
                modified_context['urgency_level'] = 'high'
                modified_context['scarcity_emphasis'] = True
            elif emphasis == 'trust_focused':
                modified_context['trust_signal_emphasis'] = 'high'
                modified_context['social_proof_emphasis'] = True
            elif emphasis == 'benefit_focused':
                modified_context['benefit_emphasis'] = 'high'
                modified_context['feature_focus'] = 'benefits'
        
        # Apply targeting modifications
        if 'targeting_modifications' in variant_config:
            targeting = variant_config['targeting_modifications']
            modified_context.update(targeting)
        
        return modified_context

    async def _apply_variant_device_optimizations(self, content: PersonalizedContent,
                                                device_context: Dict[str, Any],
                                                variant_config: Dict[str, Any]) -> PersonalizedContent:
        """Apply variant-specific device optimizations"""
        optimization_level = variant_config.get('device_optimization_level', 'standard')
        
        if optimization_level == 'minimal':
            # Minimal device optimization - basic responsive design only
            return content
        elif optimization_level == 'enhanced':
            # Enhanced device optimization with aggressive mobile optimization
            if device_context.get('device_type') == 'mobile':
                optimized_content = content.model_copy()
                
                # More aggressive mobile optimization
                if len(optimized_content.hero_message) > 30:
                    optimized_content.hero_message = optimized_content.hero_message[:27] + "..."
                
                # Simplify trust signals for mobile
                if len(optimized_content.trust_signals) > 2:
                    optimized_content.trust_signals = optimized_content.trust_signals[:2]
                
                # Add mobile-specific urgency
                if not optimized_content.scarcity_trigger:
                    optimized_content.scarcity_trigger = "📱 Mobile Special: Limited Time!"
                
                return optimized_content
            else:
                return content
        else:
            # Standard device optimization
            device_profile = await self._create_device_profile(device_context)
            
            if device_profile:
                variants = await self.variant_generator.generate_device_variants(
                    content.dict(), device_profile, None, None
                )
                
                if variants:
                    best_variant = variants[0]  # Use highest scored variant
                    
                    # Convert device variant back to PersonalizedContent
                    return await self._convert_device_variant_to_content(best_variant, content)
            
            return content

    async def _apply_variant_content_modifications(self, content: PersonalizedContent,
                                                 variant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply variant-specific content modifications"""
        result = content.dict()
        
        # Apply content template modifications
        if 'content_template' in variant_config:
            template = variant_config['content_template']
            
            if template == 'concise':
                # Shorten all text elements
                if len(result['hero_message']) > 50:
                    result['hero_message'] = result['hero_message'][:47] + "..."
                
                if len(result['trust_signals']) > 3:
                    result['trust_signals'] = result['trust_signals'][:3]
                    
            elif template == 'detailed':
                # Expand content with more details
                result['hero_message'] = f"{result['hero_message']} - Complete solution for your needs"
                
                # Add more trust signals
                additional_signals = ["Expert Support", "Money-Back Guarantee", "Award-Winning"]
                result['trust_signals'].extend(additional_signals[:2])
        
        # Apply CTA modifications
        if 'cta_style' in variant_config:
            cta_style = variant_config['cta_style']
            
            if cta_style == 'urgent':
                result['call_to_action'] = f"🔥 {result['call_to_action']} Now!"
            elif cta_style == 'soft':
                result['call_to_action'] = result['call_to_action'].replace('Now', '').strip()
                if not result['call_to_action'].endswith('→'):
                    result['call_to_action'] += " →"
        
        # Apply layout modifications
        if 'layout_style' in variant_config:
            layout_style = variant_config['layout_style']
            result['layout_configuration'] = {
                'style': layout_style,
                'variant_id': variant_config.get('variant_id', 'unknown')
            }
        
        return result

    # =============================================================================
    # ANALYTICS AND PERFORMANCE TRACKING
    # =============================================================================

    async def _record_ab_test_content_delivery(self, session: JourneySession,
                                             test_assignment: Dict[str, Any],
                                             content: Dict[str, Any]):
        """Record A/B test content delivery for analytics"""
        try:
            delivery_data = {
                'session_id': session.session_id,
                'test_id': test_assignment['test_id'],
                'variant_id': test_assignment['variant_id'],
                'content_delivered': {
                    'hero_message_length': len(content.get('content', {}).get('hero_message', '')),
                    'trust_signals_count': len(content.get('content', {}).get('trust_signals', [])),
                    'has_scarcity_trigger': bool(content.get('content', {}).get('scarcity_trigger')),
                    'layout_style': content.get('layout_configuration', {}).get('style', 'standard'),
                    'device_optimizations': content.get('optimization', {})
                },
                'delivery_timestamp': datetime.utcnow().isoformat(),
                'persona_type': session.persona_type,
                'device_type': session.device_type
            }
            
            # Store delivery record
            delivery_key = f"ab_delivery:{test_assignment['test_id']}:{test_assignment['variant_id']}:{session.session_id}"
            await self.redis_client.setex(delivery_key, 86400, json.dumps(delivery_data))
            
            # Update variant session count
            await self._increment_variant_session_count(test_assignment['test_id'], test_assignment['variant_id'])
            
        except Exception as e:
            logger.error(f"Error recording A/B test content delivery: {str(e)}")

    async def _update_ab_test_metrics(self, test_id: str, variant_id: str, interaction_data: Dict[str, Any]):
        """Update real-time A/B test metrics"""
        try:
            metrics_key = f"ab_metrics:{test_id}:{variant_id}"
            current_metrics = await self.redis_client.get(metrics_key)
            
            if current_metrics:
                metrics = json.loads(current_metrics)
            else:
                metrics = {
                    'total_interactions': 0,
                    'click_through_rate': 0.0,
                    'engagement_time': 0.0,
                    'bounce_rate': 0.0,
                    'conversion_events': {},
                    'last_updated': datetime.utcnow().isoformat()
                }
            
            # Update interaction count
            metrics['total_interactions'] += 1
            
            # Update specific interaction metrics
            interaction_type = interaction_data.get('event_type', 'page_view')
            
            if interaction_type == 'click':
                metrics['total_clicks'] = metrics.get('total_clicks', 0) + 1
                metrics['click_through_rate'] = metrics['total_clicks'] / metrics['total_interactions']
            
            elif interaction_type == 'engagement':
                engagement_time = interaction_data.get('time_spent', 0)
                current_total_time = metrics.get('total_engagement_time', 0)
                metrics['total_engagement_time'] = current_total_time + engagement_time
                metrics['engagement_time'] = metrics['total_engagement_time'] / metrics['total_interactions']
            
            elif interaction_type in ['purchase', 'signup', 'download', 'contact']:
                if 'conversion_events' not in metrics:
                    metrics['conversion_events'] = {}
                metrics['conversion_events'][interaction_type] = metrics['conversion_events'].get(interaction_type, 0) + 1
            
            metrics['last_updated'] = datetime.utcnow().isoformat()
            
            # Store updated metrics
            await self.redis_client.setex(metrics_key, 86400, json.dumps(metrics))
            
        except Exception as e:
            logger.error(f"Error updating A/B test metrics: {str(e)}")

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    async def _get_ab_test_assignment(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current A/B test assignment for a session"""
        try:
            assignment_key = f"ab_assignment:{session_id}"
            assignment_data = await self.redis_client.get(assignment_key)
            
            if assignment_data:
                return json.loads(assignment_data)
            
            return None
        except Exception as e:
            logger.error(f"Error getting A/B test assignment: {str(e)}")
            return None

    async def _get_variant_configuration(self, test_id: str, variant_id: str) -> Optional[Dict[str, Any]]:
        """Get variant configuration for A/B test"""
        try:
            config_key = f"ab_test_config:{test_id}"
            test_config_data = await self.redis_client.get(config_key)
            
            if test_config_data:
                test_config = json.loads(test_config_data)
                
                for variant in test_config.get('variants', []):
                    if variant['variant_id'] == variant_id:
                        return variant
            
            return None
        except Exception as e:
            logger.error(f"Error getting variant configuration: {str(e)}")
            return None

    async def _get_active_tests(self) -> List[Dict[str, Any]]:
        """Get all active A/B tests"""
        try:
            # In a real implementation, this would query the database
            # For now, we'll simulate with Redis patterns
            pattern = "ab_test_config:*"
            keys = await self.redis_client.keys(pattern)
            
            active_tests = []
            for key in keys:
                test_data = await self.redis_client.get(key)
                if test_data:
                    test_config = json.loads(test_data)
                    if test_config.get('status') == 'active':
                        active_tests.append(test_config)
            
            return active_tests
        except Exception as e:
            logger.error(f"Error getting active tests: {str(e)}")
            return []

    async def _increment_variant_session_count(self, test_id: str, variant_id: str):
        """Increment session count for a variant"""
        try:
            counter_key = f"ab_sessions:{test_id}:{variant_id}"
            await self.redis_client.incr(counter_key)
            await self.redis_client.expire(counter_key, 604800)  # 7 days
        except Exception as e:
            logger.error(f"Error incrementing variant session count: {str(e)}")

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'ABTestingPersonalizationEngine'
]