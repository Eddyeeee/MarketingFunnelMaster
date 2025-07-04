# Device Performance Optimization Framework - Week 2 Implementation
# Module: 3A - Week 2 - Advanced Device-Specific Content Variants
# Created: 2025-07-04

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from .device_detection_service import DeviceProfile, ContentCapabilities, UXOptimizations
from .device_content_variant_generator import DeviceContentVariant

logger = logging.getLogger(__name__)

# =============================================================================
# PERFORMANCE OPTIMIZATION MODELS
# =============================================================================

@dataclass
class PerformanceMetrics:
    """Performance metrics for device-specific content"""
    load_time: float
    render_time: float
    interaction_delay: float
    memory_usage: float
    cpu_usage: float
    network_usage: float
    battery_impact: float
    user_satisfaction_score: float
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'load_time': self.load_time,
            'render_time': self.render_time,
            'interaction_delay': self.interaction_delay,
            'memory_usage': self.memory_usage,
            'cpu_usage': self.cpu_usage,
            'network_usage': self.network_usage,
            'battery_impact': self.battery_impact,
            'user_satisfaction_score': self.user_satisfaction_score,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class OptimizationStrategy:
    """Performance optimization strategy"""
    strategy_id: str
    device_types: List[str]
    performance_targets: Dict[str, float]
    optimization_techniques: List[str]
    resource_constraints: Dict[str, float]
    expected_improvement: float
    priority: int
    
    def applies_to_device(self, device_profile: DeviceProfile) -> bool:
        """Check if strategy applies to device"""
        return device_profile.device_type in self.device_types

@dataclass
class OptimizationResult:
    """Result of performance optimization"""
    optimization_id: str
    strategy_applied: str
    baseline_metrics: PerformanceMetrics
    optimized_metrics: PerformanceMetrics
    improvement_percentage: Dict[str, float]
    techniques_used: List[str]
    resource_savings: Dict[str, float]
    success: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'optimization_id': self.optimization_id,
            'strategy_applied': self.strategy_applied,
            'baseline_metrics': self.baseline_metrics.to_dict(),
            'optimized_metrics': self.optimized_metrics.to_dict(),
            'improvement_percentage': self.improvement_percentage,
            'techniques_used': self.techniques_used,
            'resource_savings': self.resource_savings,
            'success': self.success
        }

# =============================================================================
# DEVICE PERFORMANCE OPTIMIZER
# =============================================================================

class DevicePerformanceOptimizer:
    """Advanced performance optimization framework for device-specific content"""
    
    def __init__(self):
        self.optimization_strategies = self._initialize_optimization_strategies()
        self.performance_cache = {}
        self.optimization_history = {}
        self.baseline_metrics = {}
        self.adaptive_thresholds = self._initialize_adaptive_thresholds()
        
    async def optimize_content_performance(self, content_variants: List[DeviceContentVariant],
                                         device_profile: DeviceProfile,
                                         content_capabilities: ContentCapabilities,
                                         target_metrics: Optional[Dict[str, float]] = None) -> List[DeviceContentVariant]:
        """Optimize content variants for device-specific performance"""
        try:
            optimized_variants = []
            
            # Get applicable optimization strategies
            applicable_strategies = [
                strategy for strategy in self.optimization_strategies
                if strategy.applies_to_device(device_profile)
            ]
            
            # Sort strategies by priority and expected improvement
            applicable_strategies.sort(key=lambda s: (s.priority, s.expected_improvement), reverse=True)
            
            for variant in content_variants:
                # Measure baseline performance
                baseline_metrics = await self._measure_baseline_performance(variant, device_profile)
                
                # Apply optimization strategies
                optimized_variant = variant
                optimization_results = []
                
                for strategy in applicable_strategies:
                    if await self._should_apply_strategy(strategy, baseline_metrics, target_metrics):
                        optimized_variant, result = await self._apply_optimization_strategy(
                            optimized_variant, strategy, device_profile, content_capabilities
                        )
                        
                        if result.success:
                            optimization_results.append(result)
                
                # Validate final performance
                final_metrics = await self._measure_final_performance(optimized_variant, device_profile)
                
                # Update variant with performance data
                optimized_variant.performance_score = await self._calculate_performance_score(final_metrics)
                optimized_variant.content_data['performance_metrics'] = final_metrics.to_dict()
                optimized_variant.content_data['optimization_results'] = [r.to_dict() for r in optimization_results]
                
                optimized_variants.append(optimized_variant)
            
            # Cache optimization results
            await self._cache_optimization_results(device_profile, optimized_variants)
            
            logger.info(f"Optimized {len(optimized_variants)} variants for {device_profile.device_type}")
            return optimized_variants
            
        except Exception as e:
            logger.error(f"Error optimizing content performance: {str(e)}")
            return content_variants
    
    async def _measure_baseline_performance(self, variant: DeviceContentVariant, 
                                          device_profile: DeviceProfile) -> PerformanceMetrics:
        """Measure baseline performance metrics for content variant"""
        try:
            # Simulate performance measurement based on content analysis
            content_size = await self._estimate_content_size(variant.content_data)
            complexity_score = await self._calculate_content_complexity(variant.content_data)
            
            # Device-specific performance estimation
            device_factor = await self._get_device_performance_factor(device_profile)
            
            # Calculate estimated metrics
            load_time = (content_size / 1000) * device_factor['load_multiplier']
            render_time = complexity_score * device_factor['render_multiplier']
            interaction_delay = 50 + (complexity_score * 10) if device_profile.touch_capable else 20
            memory_usage = content_size * 0.5 * device_factor['memory_multiplier']
            cpu_usage = complexity_score * device_factor['cpu_multiplier']
            network_usage = content_size
            battery_impact = (cpu_usage + memory_usage) * 0.1 if device_profile.device_type == "mobile" else 0
            user_satisfaction_score = max(0, 1.0 - (load_time / 10) - (render_time / 5))
            
            return PerformanceMetrics(
                load_time=load_time,
                render_time=render_time,
                interaction_delay=interaction_delay,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                network_usage=network_usage,
                battery_impact=battery_impact,
                user_satisfaction_score=user_satisfaction_score,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error measuring baseline performance: {str(e)}")
            return await self._get_default_metrics()
    
    async def _apply_optimization_strategy(self, variant: DeviceContentVariant,
                                         strategy: OptimizationStrategy,
                                         device_profile: DeviceProfile,
                                         content_capabilities: ContentCapabilities) -> Tuple[DeviceContentVariant, OptimizationResult]:
        """Apply specific optimization strategy to content variant"""
        try:
            baseline_metrics = await self._measure_baseline_performance(variant, device_profile)
            optimized_variant = variant
            techniques_used = []
            
            # Apply optimization techniques
            for technique in strategy.optimization_techniques:
                if technique == "image_optimization":
                    optimized_variant, applied = await self._apply_image_optimization(
                        optimized_variant, device_profile, content_capabilities
                    )
                    if applied:
                        techniques_used.append(technique)
                
                elif technique == "code_splitting":
                    optimized_variant, applied = await self._apply_code_splitting(
                        optimized_variant, device_profile
                    )
                    if applied:
                        techniques_used.append(technique)
                
                elif technique == "lazy_loading":
                    optimized_variant, applied = await self._apply_lazy_loading(
                        optimized_variant, device_profile
                    )
                    if applied:
                        techniques_used.append(technique)
                
                elif technique == "resource_preloading":
                    optimized_variant, applied = await self._apply_resource_preloading(
                        optimized_variant, device_profile
                    )
                    if applied:
                        techniques_used.append(technique)
                
                elif technique == "compression":
                    optimized_variant, applied = await self._apply_compression(
                        optimized_variant, device_profile
                    )
                    if applied:
                        techniques_used.append(technique)
                
                elif technique == "caching_optimization":
                    optimized_variant, applied = await self._apply_caching_optimization(
                        optimized_variant, device_profile
                    )
                    if applied:
                        techniques_used.append(technique)
                
                elif technique == "animation_optimization":
                    optimized_variant, applied = await self._apply_animation_optimization(
                        optimized_variant, device_profile, content_capabilities
                    )
                    if applied:
                        techniques_used.append(technique)
            
            # Measure optimized performance
            optimized_metrics = await self._measure_final_performance(optimized_variant, device_profile)
            
            # Calculate improvements
            improvement_percentage = await self._calculate_improvement_percentage(
                baseline_metrics, optimized_metrics
            )
            
            # Calculate resource savings
            resource_savings = await self._calculate_resource_savings(
                baseline_metrics, optimized_metrics
            )
            
            # Determine success
            success = await self._evaluate_optimization_success(
                improvement_percentage, strategy.performance_targets
            )
            
            result = OptimizationResult(
                optimization_id=f"{strategy.strategy_id}_{int(time.time())}",
                strategy_applied=strategy.strategy_id,
                baseline_metrics=baseline_metrics,
                optimized_metrics=optimized_metrics,
                improvement_percentage=improvement_percentage,
                techniques_used=techniques_used,
                resource_savings=resource_savings,
                success=success
            )
            
            return optimized_variant, result
            
        except Exception as e:
            logger.error(f"Error applying optimization strategy: {str(e)}")
            return variant, OptimizationResult(
                optimization_id="error",
                strategy_applied=strategy.strategy_id,
                baseline_metrics=await self._get_default_metrics(),
                optimized_metrics=await self._get_default_metrics(),
                improvement_percentage={},
                techniques_used=[],
                resource_savings={},
                success=False
            )
    
    # =============================================================================
    # OPTIMIZATION TECHNIQUE IMPLEMENTATIONS
    # =============================================================================
    
    async def _apply_image_optimization(self, variant: DeviceContentVariant,
                                      device_profile: DeviceProfile,
                                      content_capabilities: ContentCapabilities) -> Tuple[DeviceContentVariant, bool]:
        """Apply image optimization techniques"""
        optimized_variant = variant
        applied = False
        
        if "images" in variant.content_data:
            optimized_images = []
            
            for image in variant.content_data["images"]:
                optimized_image = image.copy()
                
                # Format optimization
                if content_capabilities.supports_webp:
                    optimized_image["format"] = "webp"
                    applied = True
                
                # Size optimization based on device
                if device_profile.device_type == "mobile":
                    optimized_image["max_width"] = 800
                    optimized_image["quality"] = 75
                elif device_profile.device_type == "tablet":
                    optimized_image["max_width"] = 1200
                    optimized_image["quality"] = 80
                else:
                    optimized_image["max_width"] = 1920
                    optimized_image["quality"] = 85
                
                # Responsive images
                optimized_image["srcset"] = await self._generate_responsive_srcset(
                    optimized_image, device_profile
                )
                applied = True
                
                # Lazy loading for non-critical images
                if image.get("priority", "normal") != "critical":
                    optimized_image["lazy_load"] = True
                    applied = True
                
                optimized_images.append(optimized_image)
            
            optimized_variant.content_data["images"] = optimized_images
        
        return optimized_variant, applied
    
    async def _apply_code_splitting(self, variant: DeviceContentVariant,
                                  device_profile: DeviceProfile) -> Tuple[DeviceContentVariant, bool]:
        """Apply code splitting optimization"""
        optimized_variant = variant
        applied = False
        
        # Split code based on device capabilities
        if device_profile.performance_tier == "low":
            # Aggressive code splitting for low-performance devices
            optimized_variant.content_data["code_splitting"] = {
                "strategy": "aggressive",
                "chunk_size": "small",
                "defer_non_critical": True
            }
            applied = True
        elif device_profile.performance_tier == "medium":
            # Moderate code splitting
            optimized_variant.content_data["code_splitting"] = {
                "strategy": "moderate",
                "chunk_size": "medium",
                "defer_non_critical": False
            }
            applied = True
        
        return optimized_variant, applied
    
    async def _apply_lazy_loading(self, variant: DeviceContentVariant,
                                device_profile: DeviceProfile) -> Tuple[DeviceContentVariant, bool]:
        """Apply lazy loading optimization"""
        optimized_variant = variant
        applied = False
        
        # Apply lazy loading based on device and network conditions
        if device_profile.network_speed == "slow" or device_profile.performance_tier == "low":
            # Aggressive lazy loading
            optimized_variant.content_data["lazy_loading"] = {
                "images": True,
                "videos": True,
                "iframes": True,
                "non_critical_css": True,
                "below_fold_content": True
            }
            applied = True
        else:
            # Standard lazy loading
            optimized_variant.content_data["lazy_loading"] = {
                "images": True,
                "videos": True,
                "below_fold_content": True
            }
            applied = True
        
        return optimized_variant, applied
    
    async def _apply_resource_preloading(self, variant: DeviceContentVariant,
                                       device_profile: DeviceProfile) -> Tuple[DeviceContentVariant, bool]:
        """Apply resource preloading optimization"""
        optimized_variant = variant
        applied = False
        
        # Preload critical resources based on device capabilities
        if device_profile.performance_tier == "high" and device_profile.network_speed == "fast":
            # Aggressive preloading for high-performance devices
            optimized_variant.content_data["preloading"] = {
                "critical_css": True,
                "critical_fonts": True,
                "hero_images": True,
                "next_page_resources": True
            }
            applied = True
        elif device_profile.performance_tier == "medium":
            # Conservative preloading
            optimized_variant.content_data["preloading"] = {
                "critical_css": True,
                "critical_fonts": True,
                "hero_images": True
            }
            applied = True
        
        return optimized_variant, applied
    
    async def _apply_compression(self, variant: DeviceContentVariant,
                               device_profile: DeviceProfile) -> Tuple[DeviceContentVariant, bool]:
        """Apply compression optimization"""
        optimized_variant = variant
        applied = False
        
        # Apply compression based on device and network
        if device_profile.network_speed == "slow":
            # Aggressive compression for slow networks
            optimized_variant.content_data["compression"] = {
                "gzip": True,
                "brotli": True,
                "css_minification": True,
                "js_minification": True,
                "html_minification": True,
                "image_compression": "high"
            }
            applied = True
        else:
            # Standard compression
            optimized_variant.content_data["compression"] = {
                "gzip": True,
                "css_minification": True,
                "js_minification": True,
                "image_compression": "medium"
            }
            applied = True
        
        return optimized_variant, applied
    
    async def _apply_caching_optimization(self, variant: DeviceContentVariant,
                                        device_profile: DeviceProfile) -> Tuple[DeviceContentVariant, bool]:
        """Apply caching optimization"""
        optimized_variant = variant
        applied = False
        
        # Set up caching strategy based on device
        if device_profile.device_type == "mobile":
            # Conservative caching for mobile to save storage
            optimized_variant.content_data["caching"] = {
                "strategy": "conservative",
                "max_cache_size": "50MB",
                "cache_duration": "1day",
                "cache_images": False,
                "cache_videos": False
            }
            applied = True
        else:
            # Aggressive caching for desktop/tablet
            optimized_variant.content_data["caching"] = {
                "strategy": "aggressive",
                "max_cache_size": "200MB",
                "cache_duration": "7days",
                "cache_images": True,
                "cache_videos": True
            }
            applied = True
        
        return optimized_variant, applied
    
    async def _apply_animation_optimization(self, variant: DeviceContentVariant,
                                          device_profile: DeviceProfile,
                                          content_capabilities: ContentCapabilities) -> Tuple[DeviceContentVariant, bool]:
        """Apply animation optimization"""
        optimized_variant = variant
        applied = False
        
        # Optimize animations based on device capabilities
        if not content_capabilities.supports_animations:
            # Disable animations for low-performance devices
            optimized_variant.content_data["animations"] = {
                "enabled": False,
                "fallback": "static_images"
            }
            applied = True
        elif device_profile.performance_tier == "low":
            # Simplified animations
            optimized_variant.content_data["animations"] = {
                "enabled": True,
                "complexity": "low",
                "duration": "short",
                "easing": "linear"
            }
            applied = True
        elif content_capabilities.supports_webgl and device_profile.performance_tier == "high":
            # Advanced animations for high-performance devices
            optimized_variant.content_data["animations"] = {
                "enabled": True,
                "complexity": "high",
                "webgl": True,
                "hardware_acceleration": True
            }
            applied = True
        
        return optimized_variant, applied
    
    # =============================================================================
    # PERFORMANCE MEASUREMENT AND CALCULATION METHODS
    # =============================================================================
    
    async def _measure_final_performance(self, variant: DeviceContentVariant,
                                        device_profile: DeviceProfile) -> PerformanceMetrics:
        """Measure final performance after optimizations"""
        # This would be similar to baseline measurement but accounting for optimizations
        baseline_metrics = await self._measure_baseline_performance(variant, device_profile)
        
        # Apply improvement factors based on optimizations
        improvement_factor = await self._calculate_optimization_improvement_factor(variant)
        
        return PerformanceMetrics(
            load_time=baseline_metrics.load_time * improvement_factor['load_time'],
            render_time=baseline_metrics.render_time * improvement_factor['render_time'],
            interaction_delay=baseline_metrics.interaction_delay * improvement_factor['interaction_delay'],
            memory_usage=baseline_metrics.memory_usage * improvement_factor['memory_usage'],
            cpu_usage=baseline_metrics.cpu_usage * improvement_factor['cpu_usage'],
            network_usage=baseline_metrics.network_usage * improvement_factor['network_usage'],
            battery_impact=baseline_metrics.battery_impact * improvement_factor['battery_impact'],
            user_satisfaction_score=min(1.0, baseline_metrics.user_satisfaction_score * improvement_factor['user_satisfaction']),
            timestamp=datetime.utcnow()
        )
    
    async def _calculate_optimization_improvement_factor(self, variant: DeviceContentVariant) -> Dict[str, float]:
        """Calculate improvement factors based on applied optimizations"""
        factors = {
            'load_time': 1.0,
            'render_time': 1.0,
            'interaction_delay': 1.0,
            'memory_usage': 1.0,
            'cpu_usage': 1.0,
            'network_usage': 1.0,
            'battery_impact': 1.0,
            'user_satisfaction': 1.0
        }
        
        # Apply factors based on optimizations
        if "compression" in variant.content_data:
            factors['load_time'] *= 0.7  # 30% improvement
            factors['network_usage'] *= 0.6  # 40% reduction
        
        if "lazy_loading" in variant.content_data:
            factors['load_time'] *= 0.8  # 20% improvement
            factors['memory_usage'] *= 0.9  # 10% reduction
        
        if "image_optimization" in variant.content_data:
            factors['load_time'] *= 0.85  # 15% improvement
            factors['network_usage'] *= 0.75  # 25% reduction
        
        if "caching" in variant.content_data:
            factors['load_time'] *= 0.5  # 50% improvement for cached content
        
        if "code_splitting" in variant.content_data:
            factors['load_time'] *= 0.9  # 10% improvement
            factors['memory_usage'] *= 0.85  # 15% reduction
        
        # User satisfaction improves with all optimizations
        avg_improvement = 1 - ((factors['load_time'] + factors['render_time']) / 2)
        factors['user_satisfaction'] = 1.0 + (avg_improvement * 0.5)
        
        return factors
    
    async def _calculate_improvement_percentage(self, baseline: PerformanceMetrics,
                                              optimized: PerformanceMetrics) -> Dict[str, float]:
        """Calculate percentage improvement for each metric"""
        return {
            'load_time': self._calculate_percentage_improvement(baseline.load_time, optimized.load_time),
            'render_time': self._calculate_percentage_improvement(baseline.render_time, optimized.render_time),
            'interaction_delay': self._calculate_percentage_improvement(baseline.interaction_delay, optimized.interaction_delay),
            'memory_usage': self._calculate_percentage_improvement(baseline.memory_usage, optimized.memory_usage),
            'cpu_usage': self._calculate_percentage_improvement(baseline.cpu_usage, optimized.cpu_usage),
            'network_usage': self._calculate_percentage_improvement(baseline.network_usage, optimized.network_usage),
            'battery_impact': self._calculate_percentage_improvement(baseline.battery_impact, optimized.battery_impact),
            'user_satisfaction_score': ((optimized.user_satisfaction_score - baseline.user_satisfaction_score) / baseline.user_satisfaction_score) * 100
        }
    
    def _calculate_percentage_improvement(self, baseline: float, optimized: float) -> float:
        """Calculate percentage improvement (negative means reduction which is good for most metrics)"""
        if baseline == 0:
            return 0
        return ((baseline - optimized) / baseline) * 100
    
    async def _calculate_resource_savings(self, baseline: PerformanceMetrics,
                                        optimized: PerformanceMetrics) -> Dict[str, float]:
        """Calculate resource savings"""
        return {
            'memory_saved_mb': (baseline.memory_usage - optimized.memory_usage) / 1024,
            'network_saved_kb': (baseline.network_usage - optimized.network_usage) / 1024,
            'battery_saved_percent': ((baseline.battery_impact - optimized.battery_impact) / baseline.battery_impact) * 100 if baseline.battery_impact > 0 else 0,
            'time_saved_ms': baseline.load_time - optimized.load_time
        }
    
    async def _calculate_performance_score(self, metrics: PerformanceMetrics) -> float:
        """Calculate overall performance score"""
        # Weighted performance score (0-1 scale)
        load_score = max(0, 1 - (metrics.load_time / 10))  # 10s is poor
        render_score = max(0, 1 - (metrics.render_time / 5))  # 5s is poor
        interaction_score = max(0, 1 - (metrics.interaction_delay / 100))  # 100ms is poor
        memory_score = max(0, 1 - (metrics.memory_usage / 100000))  # 100MB is high
        satisfaction_score = metrics.user_satisfaction_score
        
        # Weighted average
        performance_score = (
            load_score * 0.3 +
            render_score * 0.2 +
            interaction_score * 0.2 +
            memory_score * 0.1 +
            satisfaction_score * 0.2
        )
        
        return max(0.0, min(1.0, performance_score))
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    async def _estimate_content_size(self, content_data: Dict[str, Any]) -> float:
        """Estimate content size in KB"""
        base_size = 100  # Base HTML/CSS/JS
        
        # Images
        if "images" in content_data:
            for image in content_data["images"]:
                base_size += image.get("estimated_size", 500)  # Default 500KB per image
        
        # Videos
        if "videos" in content_data:
            for video in content_data["videos"]:
                base_size += video.get("estimated_size", 5000)  # Default 5MB per video
        
        # Text content
        text_content = str(content_data.get("hero_message", "")) + str(content_data.get("description", ""))
        base_size += len(text_content) * 0.001  # 1 byte per character
        
        return base_size
    
    async def _calculate_content_complexity(self, content_data: Dict[str, Any]) -> float:
        """Calculate content complexity score (0-1)"""
        complexity = 0.1  # Base complexity
        
        # Count interactive elements
        if "buttons" in content_data:
            complexity += len(content_data["buttons"]) * 0.1
        
        if "forms" in content_data:
            complexity += len(content_data["forms"]) * 0.2
        
        if "animations" in content_data and content_data["animations"].get("enabled", False):
            complexity += 0.3
        
        if "videos" in content_data:
            complexity += len(content_data["videos"]) * 0.2
        
        return min(1.0, complexity)
    
    async def _get_device_performance_factor(self, device_profile: DeviceProfile) -> Dict[str, float]:
        """Get performance factors for device type"""
        if device_profile.performance_tier == "low":
            return {
                'load_multiplier': 2.0,
                'render_multiplier': 3.0,
                'memory_multiplier': 1.5,
                'cpu_multiplier': 2.5
            }
        elif device_profile.performance_tier == "medium":
            return {
                'load_multiplier': 1.2,
                'render_multiplier': 1.5,
                'memory_multiplier': 1.1,
                'cpu_multiplier': 1.3
            }
        else:  # high performance
            return {
                'load_multiplier': 0.8,
                'render_multiplier': 0.7,
                'memory_multiplier': 0.9,
                'cpu_multiplier': 0.8
            }
    
    async def _generate_responsive_srcset(self, image: Dict[str, Any], 
                                        device_profile: DeviceProfile) -> str:
        """Generate responsive image srcset"""
        base_url = image.get("url", "")
        
        if device_profile.device_type == "mobile":
            return f"{base_url}?w=400 400w, {base_url}?w=800 800w"
        elif device_profile.device_type == "tablet":
            return f"{base_url}?w=600 600w, {base_url}?w=1200 1200w"
        else:
            return f"{base_url}?w=800 800w, {base_url}?w=1600 1600w, {base_url}?w=2400 2400w"
    
    async def _should_apply_strategy(self, strategy: OptimizationStrategy,
                                   baseline_metrics: PerformanceMetrics,
                                   target_metrics: Optional[Dict[str, float]]) -> bool:
        """Determine if optimization strategy should be applied"""
        # Always apply if no targets specified
        if not target_metrics:
            return True
        
        # Check if current performance meets targets
        current_performance = {
            'load_time': baseline_metrics.load_time,
            'render_time': baseline_metrics.render_time,
            'memory_usage': baseline_metrics.memory_usage,
            'user_satisfaction_score': baseline_metrics.user_satisfaction_score
        }
        
        # Apply strategy if any target is not met
        for metric, target in target_metrics.items():
            if metric in current_performance:
                if metric == 'user_satisfaction_score':
                    # Higher is better for satisfaction
                    if current_performance[metric] < target:
                        return True
                else:
                    # Lower is better for other metrics
                    if current_performance[metric] > target:
                        return True
        
        return False
    
    async def _evaluate_optimization_success(self, improvement_percentage: Dict[str, float],
                                           performance_targets: Dict[str, float]) -> bool:
        """Evaluate if optimization was successful"""
        # Consider successful if any significant improvement achieved
        significant_improvements = [
            improvement_percentage.get('load_time', 0) > 10,
            improvement_percentage.get('render_time', 0) > 10,
            improvement_percentage.get('memory_usage', 0) > 15,
            improvement_percentage.get('user_satisfaction_score', 0) > 5
        ]
        
        return any(significant_improvements)
    
    async def _get_default_metrics(self) -> PerformanceMetrics:
        """Get default performance metrics"""
        return PerformanceMetrics(
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
    
    async def _cache_optimization_results(self, device_profile: DeviceProfile,
                                        optimized_variants: List[DeviceContentVariant]) -> None:
        """Cache optimization results for future use"""
        cache_key = f"optimization:{device_profile.device_type}:{device_profile.performance_tier}"
        
        cache_data = {
            'device_profile': device_profile.to_dict(),
            'optimization_count': len(optimized_variants),
            'avg_performance_score': sum(v.performance_score or 0 for v in optimized_variants) / len(optimized_variants),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.performance_cache[cache_key] = cache_data
    
    def _initialize_optimization_strategies(self) -> List[OptimizationStrategy]:
        """Initialize performance optimization strategies"""
        return [
            OptimizationStrategy(
                strategy_id="mobile_performance_boost",
                device_types=["mobile"],
                performance_targets={"load_time": 2.0, "memory_usage": 30000},
                optimization_techniques=["image_optimization", "lazy_loading", "compression", "code_splitting"],
                resource_constraints={"max_memory": 50000, "max_network": 1000},
                expected_improvement=0.35,
                priority=1
            ),
            OptimizationStrategy(
                strategy_id="low_performance_optimization",
                device_types=["mobile", "tablet", "desktop"],
                performance_targets={"load_time": 4.0, "render_time": 2.0},
                optimization_techniques=["compression", "lazy_loading", "animation_optimization"],
                resource_constraints={"max_memory": 40000, "max_cpu": 50},
                expected_improvement=0.40,
                priority=1
            ),
            OptimizationStrategy(
                strategy_id="slow_network_optimization",
                device_types=["mobile", "tablet", "desktop"],
                performance_targets={"network_usage": 500, "load_time": 5.0},
                optimization_techniques=["compression", "image_optimization", "lazy_loading"],
                resource_constraints={"max_network": 500},
                expected_improvement=0.45,
                priority=1
            ),
            OptimizationStrategy(
                strategy_id="desktop_enhancement",
                device_types=["desktop"],
                performance_targets={"load_time": 1.0, "render_time": 0.5},
                optimization_techniques=["resource_preloading", "caching_optimization", "image_optimization"],
                resource_constraints={},
                expected_improvement=0.25,
                priority=2
            ),
            OptimizationStrategy(
                strategy_id="tablet_balanced_optimization",
                device_types=["tablet"],
                performance_targets={"load_time": 2.5, "memory_usage": 60000},
                optimization_techniques=["image_optimization", "caching_optimization", "lazy_loading"],
                resource_constraints={"max_memory": 80000},
                expected_improvement=0.30,
                priority=2
            )
        ]
    
    def _initialize_adaptive_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize adaptive performance thresholds"""
        return {
            "mobile": {
                "load_time_excellent": 1.5,
                "load_time_good": 3.0,
                "load_time_poor": 5.0,
                "memory_usage_good": 30000,
                "memory_usage_poor": 60000
            },
            "tablet": {
                "load_time_excellent": 1.0,
                "load_time_good": 2.5,
                "load_time_poor": 4.0,
                "memory_usage_good": 50000,
                "memory_usage_poor": 100000
            },
            "desktop": {
                "load_time_excellent": 0.8,
                "load_time_good": 2.0,
                "load_time_poor": 3.0,
                "memory_usage_good": 80000,
                "memory_usage_poor": 150000
            }
        }

# =============================================================================
# SERVICE INITIALIZATION
# =============================================================================

# Global service instance
device_performance_optimizer = DevicePerformanceOptimizer()