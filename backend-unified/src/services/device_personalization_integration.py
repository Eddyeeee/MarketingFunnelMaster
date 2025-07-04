# Device Personalization Integration - Week 2 Implementation
# Module: 3A - Week 2 - Advanced Device-Specific Content Variants
# Created: 2025-07-04

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

from .device_detection_service import AdvancedDeviceDetectionService, DeviceProfile, ContentCapabilities, UXOptimizations
from .device_content_variant_generator import DeviceContentVariantGenerator, DeviceContentVariant
from .device_performance_optimizer import DevicePerformanceOptimizer, PerformanceMetrics, OptimizationResult
from ..api.journey.personalization_engine import PersonalizationEngine
from ..api.journey.models import PersonalizedContent, JourneySession

logger = logging.getLogger(__name__)

# =============================================================================
# INTEGRATION MODELS
# =============================================================================

@dataclass
class DevicePersonalizationContext:
    """Context for device-specific personalization"""
    session: JourneySession
    device_profile: DeviceProfile
    content_capabilities: ContentCapabilities
    ux_optimizations: UXOptimizations
    user_agent: str
    client_hints: Optional[Dict[str, Any]]
    viewport: Optional[Dict[str, int]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'session_id': self.session.session_id,
            'device_profile': self.device_profile.to_dict(),
            'content_capabilities': self.content_capabilities.to_dict(),
            'ux_optimizations': self.ux_optimizations.to_dict(),
            'user_agent': self.user_agent,
            'client_hints': self.client_hints,
            'viewport': self.viewport
        }

@dataclass
class EnhancedPersonalizedContent:
    """Enhanced personalized content with device-specific optimizations"""
    base_content: PersonalizedContent
    device_variants: List[DeviceContentVariant]
    performance_metrics: PerformanceMetrics
    optimization_results: List[OptimizationResult]
    device_profile: DeviceProfile
    recommended_variant: Optional[DeviceContentVariant]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'base_content': self.base_content.dict() if hasattr(self.base_content, 'dict') else str(self.base_content),
            'device_variants': [v.to_dict() for v in self.device_variants],
            'performance_metrics': self.performance_metrics.to_dict(),
            'optimization_results': [r.to_dict() for r in self.optimization_results],
            'device_profile': self.device_profile.to_dict(),
            'recommended_variant': self.recommended_variant.to_dict() if self.recommended_variant else None
        }

# =============================================================================
# DEVICE PERSONALIZATION INTEGRATION SERVICE
# =============================================================================

class DevicePersonalizationIntegration:
    """Integration service connecting device detection with personalization engine"""
    
    def __init__(self):
        self.device_detection_service = AdvancedDeviceDetectionService()
        self.content_variant_generator = DeviceContentVariantGenerator()
        self.performance_optimizer = DevicePerformanceOptimizer()
        self.integration_cache = {}
        self.performance_tracking = {}
        
    async def generate_device_optimized_content(self, session: JourneySession,
                                              user_agent: str,
                                              context: Dict[str, Any],
                                              client_hints: Optional[Dict[str, Any]] = None,
                                              viewport: Optional[Dict[str, int]] = None) -> EnhancedPersonalizedContent:
        """Generate device-optimized personalized content"""
        try:
            logger.info(f"Generating device-optimized content for session: {session.session_id}")
            
            # Step 1: Comprehensive device detection
            device_profile, content_capabilities, ux_optimizations = await self.device_detection_service.detect_device_comprehensive(
                user_agent, client_hints, viewport
            )
            
            # Step 2: Create device personalization context
            device_context = DevicePersonalizationContext(
                session=session,
                device_profile=device_profile,
                content_capabilities=content_capabilities,
                ux_optimizations=ux_optimizations,
                user_agent=user_agent,
                client_hints=client_hints,
                viewport=viewport
            )
            
            # Step 3: Generate base personalized content using existing engine
            base_content = await self._generate_base_personalized_content(session, context)
            
            # Step 4: Generate device-specific content variants
            device_variants = await self.content_variant_generator.generate_device_variants(
                base_content.dict() if hasattr(base_content, 'dict') else self._convert_content_to_dict(base_content),
                device_profile,
                content_capabilities,
                ux_optimizations
            )
            
            # Step 5: Apply performance optimizations
            optimized_variants = await self.performance_optimizer.optimize_content_performance(
                device_variants,
                device_profile,
                content_capabilities
            )
            
            # Step 6: Select recommended variant
            recommended_variant = await self._select_recommended_variant(
                optimized_variants, device_context
            )
            
            # Step 7: Generate performance metrics
            performance_metrics = await self._generate_performance_metrics(
                recommended_variant, device_profile
            )
            
            # Step 8: Collect optimization results
            optimization_results = self._extract_optimization_results(optimized_variants)
            
            # Step 9: Create enhanced content
            enhanced_content = EnhancedPersonalizedContent(
                base_content=base_content,
                device_variants=optimized_variants,
                performance_metrics=performance_metrics,
                optimization_results=optimization_results,
                device_profile=device_profile,
                recommended_variant=recommended_variant
            )
            
            # Step 10: Cache and track
            await self._cache_integration_result(session.session_id, enhanced_content)
            await self._track_performance_metrics(session.session_id, device_context, enhanced_content)
            
            logger.info(f"Device-optimized content generated successfully: {device_profile.device_type}")
            return enhanced_content
            
        except Exception as e:
            logger.error(f"Error generating device-optimized content: {str(e)}")
            # Return fallback content
            return await self._generate_fallback_enhanced_content(session, user_agent)
    
    async def update_device_personalization_real_time(self, session_id: str,
                                                     engagement_data: Dict[str, Any],
                                                     performance_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update device personalization in real-time based on engagement"""
        try:
            logger.debug(f"Updating device personalization for session: {session_id}")
            
            # Get cached integration context
            cached_context = self.integration_cache.get(session_id)
            if not cached_context:
                logger.warning(f"No cached context found for session: {session_id}")
                return {"error": "No cached context found"}
            
            enhanced_content = cached_context['enhanced_content']
            device_context = cached_context['device_context']
            
            # Analyze engagement with device context
            device_engagement_analysis = await self._analyze_device_engagement(
                engagement_data, device_context, enhanced_content
            )
            
            # Apply device-specific optimizations
            real_time_optimizations = await self._apply_device_real_time_optimizations(
                device_engagement_analysis, device_context
            )
            
            # Update performance tracking
            if performance_data:
                await self._update_performance_tracking(session_id, performance_data, device_context)
            
            # Generate recommendations for immediate improvements
            immediate_recommendations = await self._generate_immediate_device_recommendations(
                device_engagement_analysis, device_context
            )
            
            result = {
                "device_engagement_analysis": device_engagement_analysis,
                "real_time_optimizations": real_time_optimizations,
                "immediate_recommendations": immediate_recommendations,
                "device_type": device_context.device_profile.device_type,
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
            
            # Update cache
            cached_context['last_update'] = datetime.utcnow()
            cached_context['real_time_data'] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Error updating device personalization: {str(e)}")
            return {"error": str(e)}
    
    async def get_device_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive device analytics for session"""
        try:
            # Get cached data
            cached_context = self.integration_cache.get(session_id)
            performance_data = self.performance_tracking.get(session_id, {})
            
            if not cached_context:
                return {"error": "No data available for session"}
            
            enhanced_content = cached_context['enhanced_content']
            device_context = cached_context['device_context']
            
            # Compile analytics
            analytics = {
                "device_profile": device_context.device_profile.to_dict(),
                "content_capabilities": device_context.content_capabilities.to_dict(),
                "ux_optimizations": device_context.ux_optimizations.to_dict(),
                "variant_count": len(enhanced_content.device_variants),
                "performance_metrics": enhanced_content.performance_metrics.to_dict(),
                "optimization_count": len(enhanced_content.optimization_results),
                "recommended_variant": enhanced_content.recommended_variant.to_dict() if enhanced_content.recommended_variant else None,
                "performance_tracking": performance_data,
                "real_time_updates": cached_context.get('real_time_data', {}),
                "cache_timestamp": cached_context.get('timestamp', datetime.utcnow()).isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting device analytics: {str(e)}")
            return {"error": str(e)}
    
    # =============================================================================
    # INTEGRATION HELPER METHODS
    # =============================================================================
    
    async def _generate_base_personalized_content(self, session: JourneySession, 
                                                context: Dict[str, Any]) -> PersonalizedContent:
        """Generate base personalized content using existing engine"""
        try:
            # This would integrate with the existing PersonalizationEngine
            # For now, we'll create a mock PersonalizationEngine instance
            from sqlalchemy.ext.asyncio import AsyncSession
            
            # Create a mock session for the PersonalizationEngine
            # In real implementation, this would use the actual database session
            db_session = None  # This would be injected
            
            # Create mock PersonalizedContent based on session data
            base_content = PersonalizedContent(
                hero_message=f"Discover Perfect Solutions for {session.persona_type}",
                call_to_action="Get Started Today →",
                trust_signals=["Trusted by thousands", "Money-back guarantee", "Expert support"],
                scarcity_trigger="Limited time offer - 50% off!",
                social_proof="Join 10,000+ satisfied customers",
                personalization_strategy="device_integration_base"
            )
            
            return base_content
            
        except Exception as e:
            logger.error(f"Error generating base personalized content: {str(e)}")
            # Return fallback content
            return PersonalizedContent(
                hero_message="Discover Amazing Solutions",
                call_to_action="Get Started →",
                trust_signals=["Trusted quality"],
                social_proof="Join our community",
                personalization_strategy="fallback"
            )
    
    def _convert_content_to_dict(self, content: PersonalizedContent) -> Dict[str, Any]:
        """Convert PersonalizedContent to dictionary"""
        if hasattr(content, 'dict'):
            return content.dict()
        
        # Manual conversion for compatibility
        return {
            "hero_message": getattr(content, 'hero_message', ''),
            "call_to_action": getattr(content, 'call_to_action', ''),
            "trust_signals": getattr(content, 'trust_signals', []),
            "scarcity_trigger": getattr(content, 'scarcity_trigger', None),
            "social_proof": getattr(content, 'social_proof', None),
            "personalization_strategy": getattr(content, 'personalization_strategy', 'default')
        }
    
    async def _select_recommended_variant(self, variants: List[DeviceContentVariant],
                                        device_context: DevicePersonalizationContext) -> Optional[DeviceContentVariant]:
        """Select the best variant for the device"""
        if not variants:
            return None
        
        # Score variants based on device compatibility and performance
        scored_variants = []
        
        for variant in variants:
            score = 0.0
            
            # Device type match
            if variant.device_type == device_context.device_profile.device_type:
                score += 0.3
            
            # Performance score
            if variant.performance_score:
                score += variant.performance_score * 0.4
            
            # Conversion impact
            if variant.conversion_impact:
                score += variant.conversion_impact * 0.3
            
            scored_variants.append((variant, score))
        
        # Select highest scoring variant
        if scored_variants:
            return max(scored_variants, key=lambda x: x[1])[0]
        
        return variants[0]  # Fallback to first variant
    
    async def _generate_performance_metrics(self, variant: Optional[DeviceContentVariant],
                                          device_profile: DeviceProfile) -> PerformanceMetrics:
        """Generate performance metrics for recommended variant"""
        if variant and variant.content_data.get('performance_metrics'):
            # Convert from dict if already available
            metrics_data = variant.content_data['performance_metrics']
            return PerformanceMetrics(
                load_time=metrics_data.get('load_time', 2.0),
                render_time=metrics_data.get('render_time', 1.0),
                interaction_delay=metrics_data.get('interaction_delay', 50.0),
                memory_usage=metrics_data.get('memory_usage', 50000.0),
                cpu_usage=metrics_data.get('cpu_usage', 30.0),
                network_usage=metrics_data.get('network_usage', 1000.0),
                battery_impact=metrics_data.get('battery_impact', 5.0),
                user_satisfaction_score=metrics_data.get('user_satisfaction_score', 0.8),
                timestamp=datetime.utcnow()
            )
        
        # Generate estimated metrics
        return PerformanceMetrics(
            load_time=2.0 if device_profile.performance_tier == "high" else 4.0,
            render_time=0.8 if device_profile.performance_tier == "high" else 1.5,
            interaction_delay=30.0 if device_profile.touch_capable else 20.0,
            memory_usage=40000.0 if device_profile.performance_tier == "high" else 60000.0,
            cpu_usage=25.0 if device_profile.performance_tier == "high" else 40.0,
            network_usage=800.0,
            battery_impact=3.0 if device_profile.device_type == "mobile" else 1.0,
            user_satisfaction_score=0.85,
            timestamp=datetime.utcnow()
        )
    
    def _extract_optimization_results(self, variants: List[DeviceContentVariant]) -> List[OptimizationResult]:
        """Extract optimization results from variants"""
        optimization_results = []
        
        for variant in variants:
            if 'optimization_results' in variant.content_data:
                for result_data in variant.content_data['optimization_results']:
                    # This would normally deserialize from the stored data
                    # For now, we'll create a mock result
                    pass
        
        return optimization_results
    
    async def _analyze_device_engagement(self, engagement_data: Dict[str, Any],
                                       device_context: DevicePersonalizationContext,
                                       enhanced_content: EnhancedPersonalizedContent) -> Dict[str, Any]:
        """Analyze engagement with device-specific context"""
        analysis = {
            "device_type": device_context.device_profile.device_type,
            "engagement_score": engagement_data.get('engagement_score', 0.5),
            "interaction_patterns": await self._analyze_interaction_patterns(engagement_data, device_context),
            "performance_impact": await self._analyze_performance_impact(engagement_data, enhanced_content),
            "optimization_effectiveness": await self._analyze_optimization_effectiveness(engagement_data, enhanced_content),
            "device_specific_insights": await self._generate_device_insights(engagement_data, device_context)
        }
        
        return analysis
    
    async def _analyze_interaction_patterns(self, engagement_data: Dict[str, Any],
                                          device_context: DevicePersonalizationContext) -> Dict[str, Any]:
        """Analyze interaction patterns for device type"""
        patterns = {
            "touch_interactions": 0,
            "scroll_behavior": "normal",
            "click_accuracy": 1.0,
            "gesture_usage": False
        }
        
        if device_context.device_profile.touch_capable:
            patterns["touch_interactions"] = engagement_data.get('touch_count', 0)
            patterns["gesture_usage"] = engagement_data.get('gesture_count', 0) > 0
        
        patterns["scroll_behavior"] = engagement_data.get('scroll_pattern', 'normal')
        patterns["click_accuracy"] = engagement_data.get('click_accuracy', 1.0)
        
        return patterns
    
    async def _analyze_performance_impact(self, engagement_data: Dict[str, Any],
                                        enhanced_content: EnhancedPersonalizedContent) -> Dict[str, Any]:
        """Analyze performance impact on engagement"""
        return {
            "load_time_impact": self._calculate_load_time_impact(engagement_data, enhanced_content),
            "render_quality_impact": self._calculate_render_impact(engagement_data, enhanced_content),
            "responsiveness_impact": self._calculate_responsiveness_impact(engagement_data, enhanced_content)
        }
    
    def _calculate_load_time_impact(self, engagement_data: Dict[str, Any],
                                  enhanced_content: EnhancedPersonalizedContent) -> float:
        """Calculate load time impact on engagement"""
        load_time = enhanced_content.performance_metrics.load_time
        engagement_score = engagement_data.get('engagement_score', 0.5)
        
        # Negative correlation between load time and engagement
        if load_time > 3.0:
            return max(0, engagement_score - ((load_time - 3.0) * 0.1))
        
        return engagement_score
    
    def _calculate_render_impact(self, engagement_data: Dict[str, Any],
                               enhanced_content: EnhancedPersonalizedContent) -> float:
        """Calculate render quality impact"""
        render_time = enhanced_content.performance_metrics.render_time
        return max(0, 1.0 - (render_time / 5.0))  # Normalized to 0-1
    
    def _calculate_responsiveness_impact(self, engagement_data: Dict[str, Any],
                                       enhanced_content: EnhancedPersonalizedContent) -> float:
        """Calculate responsiveness impact"""
        interaction_delay = enhanced_content.performance_metrics.interaction_delay
        return max(0, 1.0 - (interaction_delay / 100.0))  # Normalized to 0-1
    
    async def _analyze_optimization_effectiveness(self, engagement_data: Dict[str, Any],
                                                enhanced_content: EnhancedPersonalizedContent) -> Dict[str, Any]:
        """Analyze effectiveness of applied optimizations"""
        effectiveness = {
            "overall_effectiveness": 0.8,  # Mock value
            "best_performing_optimization": "image_optimization",
            "least_effective_optimization": "code_splitting",
            "recommendation": "Continue current optimization strategy"
        }
        
        return effectiveness
    
    async def _generate_device_insights(self, engagement_data: Dict[str, Any],
                                      device_context: DevicePersonalizationContext) -> Dict[str, Any]:
        """Generate device-specific insights"""
        insights = {
            "device_optimization_score": 0.85,
            "ux_alignment_score": 0.90,
            "performance_satisfaction": 0.88,
            "recommendations": [
                f"Continue optimizing for {device_context.device_profile.device_type}",
                f"Consider {device_context.ux_optimizations.layout_strategy} layout improvements"
            ]
        }
        
        return insights
    
    async def _apply_device_real_time_optimizations(self, device_engagement_analysis: Dict[str, Any],
                                                   device_context: DevicePersonalizationContext) -> Dict[str, Any]:
        """Apply real-time optimizations based on device engagement"""
        optimizations = {
            "applied_optimizations": [],
            "performance_adjustments": {},
            "ux_adjustments": {}
        }
        
        engagement_score = device_engagement_analysis.get('engagement_score', 0.5)
        
        # Low engagement optimizations
        if engagement_score < 0.4:
            if device_context.device_profile.device_type == "mobile":
                optimizations["applied_optimizations"].append("mobile_engagement_boost")
                optimizations["ux_adjustments"]["increase_touch_targets"] = True
            
            optimizations["performance_adjustments"]["reduce_animations"] = True
        
        # High engagement optimizations
        elif engagement_score > 0.8:
            optimizations["applied_optimizations"].append("performance_enhancement")
            optimizations["performance_adjustments"]["enable_advanced_features"] = True
        
        return optimizations
    
    async def _generate_immediate_device_recommendations(self, device_engagement_analysis: Dict[str, Any],
                                                       device_context: DevicePersonalizationContext) -> List[Dict[str, Any]]:
        """Generate immediate recommendations for device optimization"""
        recommendations = []
        
        device_type = device_context.device_profile.device_type
        engagement_score = device_engagement_analysis.get('engagement_score', 0.5)
        
        if engagement_score < 0.5:
            recommendations.append({
                "type": "performance_improvement",
                "action": f"Optimize content loading for {device_type}",
                "priority": "high",
                "expected_impact": 0.15
            })
        
        if device_type == "mobile" and engagement_score < 0.6:
            recommendations.append({
                "type": "mobile_ux_improvement",
                "action": "Increase touch target sizes and spacing",
                "priority": "medium",
                "expected_impact": 0.10
            })
        
        return recommendations
    
    async def _cache_integration_result(self, session_id: str, enhanced_content: EnhancedPersonalizedContent) -> None:
        """Cache integration result for future access"""
        self.integration_cache[session_id] = {
            'enhanced_content': enhanced_content,
            'device_context': DevicePersonalizationContext(
                session=enhanced_content.base_content,  # This would be properly structured
                device_profile=enhanced_content.device_profile,
                content_capabilities=None,  # Would be included
                ux_optimizations=None,  # Would be included
                user_agent="",  # Would be included
                client_hints=None,
                viewport=None
            ),
            'timestamp': datetime.utcnow()
        }
    
    async def _track_performance_metrics(self, session_id: str,
                                       device_context: DevicePersonalizationContext,
                                       enhanced_content: EnhancedPersonalizedContent) -> None:
        """Track performance metrics for analysis"""
        self.performance_tracking[session_id] = {
            'device_type': device_context.device_profile.device_type,
            'performance_tier': device_context.device_profile.performance_tier,
            'metrics': enhanced_content.performance_metrics.to_dict(),
            'optimization_count': len(enhanced_content.optimization_results),
            'variant_count': len(enhanced_content.device_variants),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _update_performance_tracking(self, session_id: str,
                                         performance_data: Dict[str, Any],
                                         device_context: DevicePersonalizationContext) -> None:
        """Update performance tracking with real-time data"""
        if session_id in self.performance_tracking:
            tracking_data = self.performance_tracking[session_id]
            tracking_data['real_time_metrics'] = performance_data
            tracking_data['last_update'] = datetime.utcnow().isoformat()
    
    async def _generate_fallback_enhanced_content(self, session: JourneySession, 
                                                user_agent: str) -> EnhancedPersonalizedContent:
        """Generate fallback enhanced content when main process fails"""
        # Create minimal device profile
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="medium",
            orientation="portrait",
            touch_capable=True,
            performance_tier="medium",
            network_speed="medium"
        )
        
        # Create basic content
        base_content = PersonalizedContent(
            hero_message="Discover Great Solutions",
            call_to_action="Get Started →",
            trust_signals=["Trusted quality"],
            social_proof="Join our community",
            personalization_strategy="fallback"
        )
        
        # Create basic metrics
        performance_metrics = PerformanceMetrics(
            load_time=3.0,
            render_time=1.0,
            interaction_delay=50.0,
            memory_usage=50000.0,
            cpu_usage=30.0,
            network_usage=1000.0,
            battery_impact=5.0,
            user_satisfaction_score=0.7,
            timestamp=datetime.utcnow()
        )
        
        return EnhancedPersonalizedContent(
            base_content=base_content,
            device_variants=[],
            performance_metrics=performance_metrics,
            optimization_results=[],
            device_profile=device_profile,
            recommended_variant=None
        )

# =============================================================================
# SERVICE INITIALIZATION
# =============================================================================

# Global service instance
device_personalization_integration = DevicePersonalizationIntegration()