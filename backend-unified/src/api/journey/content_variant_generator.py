# Content Variant Generator - Phase 3, Week 2
# Module: Advanced Device-Specific Content Variants
# Created: 2025-07-05

import asyncio
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from enum import Enum
from dataclasses import dataclass, asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, PersonalizationData
from .device_intelligence_enhanced import (
    AdvancedDeviceContext, ContentVariant, DeviceCapability, 
    NetworkSpeed, InteractionPattern
)
from ...utils.redis_client import get_redis_client
from ...utils.ml_models import ml_model_manager
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# CONTENT VARIANT GENERATION STRATEGIES
# =============================================================================

class ContentOptimizationStrategy(Enum):
    """Content optimization strategies for different scenarios"""
    ULTRA_FAST_MOBILE = "ultra_fast_mobile"
    BATTERY_SAVER = "battery_saver"
    DATA_SAVER = "data_saver"
    HIGH_PERFORMANCE = "high_performance"
    ACCESSIBILITY_FIRST = "accessibility_first"
    MINIMAL_BANDWIDTH = "minimal_bandwidth"
    RICH_INTERACTIVE = "rich_interactive"

@dataclass
class MediaOptimization:
    """Media optimization settings for different device classes"""
    image_quality: int  # 1-100
    image_format: str  # webp, jpg, png
    max_image_size: Tuple[int, int]
    video_enabled: bool
    video_quality: str  # 720p, 1080p, 4k
    animations_enabled: bool
    lazy_loading: bool
    preload_strategy: str

@dataclass 
class LayoutConfiguration:
    """Layout configuration for different devices"""
    container_width: str
    grid_columns: int
    spacing_unit: int
    font_scale: float
    line_height: float
    button_size: str
    touch_target_size: int
    navigation_style: str
    content_density: str

@dataclass
class PerformanceBudget:
    """Performance budget for content variants"""
    max_bundle_size_kb: int
    max_image_size_kb: int
    max_font_size_kb: int
    max_css_size_kb: int
    max_js_size_kb: int
    max_load_time_ms: int
    max_lcp_ms: int  # Largest Contentful Paint
    max_fid_ms: int  # First Input Delay
    max_cls_score: float  # Cumulative Layout Shift

# =============================================================================
# INTELLIGENT CONTENT VARIANT GENERATOR
# =============================================================================

class IntelligentContentVariantGenerator:
    """Generate optimized content variants based on device capabilities and context"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.ml_model = ml_model_manager.variant_generator
        
        # Content templates for different optimization strategies
        self.strategy_templates = {
            ContentOptimizationStrategy.ULTRA_FAST_MOBILE: self._get_ultra_fast_mobile_template(),
            ContentOptimizationStrategy.BATTERY_SAVER: self._get_battery_saver_template(),
            ContentOptimizationStrategy.DATA_SAVER: self._get_data_saver_template(),
            ContentOptimizationStrategy.HIGH_PERFORMANCE: self._get_high_performance_template(),
            ContentOptimizationStrategy.ACCESSIBILITY_FIRST: self._get_accessibility_template(),
            ContentOptimizationStrategy.MINIMAL_BANDWIDTH: self._get_minimal_bandwidth_template(),
            ContentOptimizationStrategy.RICH_INTERACTIVE: self._get_rich_interactive_template()
        }
    
    async def generate_content_variant(self, base_content: PersonalizedContent, 
                                     device_context: AdvancedDeviceContext,
                                     persona_type: str, session: JourneySession) -> ContentVariant:
        """Generate optimized content variant for specific device context"""
        try:
            logger.info(f"Generating content variant for device: {device_context.device_type.value}, "
                       f"capability: {device_context.device_capability.value}")
            
            # Step 1: Select optimization strategy
            strategy = await self._select_optimization_strategy(device_context, session)
            
            # Step 2: Generate variant content
            variant_content = await self._generate_variant_content(base_content, strategy, device_context, persona_type)
            
            # Step 3: Optimize media elements
            media_config = await self._optimize_media_elements(strategy, device_context)
            
            # Step 4: Configure layout
            layout_config = await self._configure_layout(device_context, strategy)
            
            # Step 5: Set performance budget
            performance_budget = await self._set_performance_budget(device_context, strategy)
            
            # Step 6: Apply accessibility optimizations
            accessibility_opts = await self._apply_accessibility_optimizations(device_context, variant_content)
            
            # Step 7: Generate interaction hints
            interaction_hints = await self._generate_interaction_hints(device_context, persona_type)
            
            # Create variant
            variant = ContentVariant(
                variant_id=self._generate_variant_id(device_context, strategy, persona_type),
                device_target=device_context.device_type,
                capability_target=device_context.device_capability,
                network_target=device_context.network_speed,
                content_format=device_context.preferred_content_format,
                hero_message=variant_content['hero_message'],
                hero_message_short=variant_content['hero_message_short'],
                hero_message_ultra_short=variant_content['hero_message_ultra_short'],
                call_to_action=variant_content['call_to_action'],
                cta_variations=variant_content['cta_variations'],
                trust_signals=variant_content['trust_signals'],
                social_proof=variant_content['social_proof'],
                media_elements=asdict(media_config),
                layout_config=asdict(layout_config),
                performance_budget=asdict(performance_budget),
                loading_strategy=self._determine_loading_strategy(device_context, strategy),
                interaction_hints=interaction_hints,
                accessibility_optimizations=accessibility_opts
            )
            
            # Cache variant for performance
            await self._cache_content_variant(session.session_id, variant)
            
            # Record variant generation
            await self._record_variant_generation(session, variant, strategy)
            
            logger.info(f"Content variant generated: {variant.variant_id}")
            return variant
            
        except Exception as e:
            logger.error(f"Error generating content variant: {str(e)}")
            return await self._generate_fallback_variant(base_content, device_context)
    
    async def _select_optimization_strategy(self, device_context: AdvancedDeviceContext, 
                                          session: JourneySession) -> ContentOptimizationStrategy:
        """Select the best optimization strategy based on device context"""
        
        # Battery saver mode
        if device_context.battery_level and device_context.battery_level < 0.2:
            return ContentOptimizationStrategy.BATTERY_SAVER
        
        # Data saver mode
        if device_context.data_saver_mode:
            return ContentOptimizationStrategy.DATA_SAVER
        
        # Accessibility requirements
        if device_context.accessibility_features:
            return ContentOptimizationStrategy.ACCESSIBILITY_FIRST
        
        # Network-based decisions
        if device_context.network_speed in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            return ContentOptimizationStrategy.MINIMAL_BANDWIDTH
        
        # Device capability-based decisions
        if device_context.device_capability == DeviceCapability.ULTRA_LOW:
            return ContentOptimizationStrategy.ULTRA_FAST_MOBILE
        elif device_context.device_capability == DeviceCapability.HIGH_PERFORMANCE:
            if device_context.network_speed in [NetworkSpeed.WIFI_FAST, NetworkSpeed.CELLULAR_5G]:
                return ContentOptimizationStrategy.RICH_INTERACTIVE
            else:
                return ContentOptimizationStrategy.HIGH_PERFORMANCE
        
        # Mobile-specific optimizations
        if (device_context.device_type == DeviceType.MOBILE and 
            device_context.interaction_pattern == InteractionPattern.QUICK_SCANNER):
            return ContentOptimizationStrategy.ULTRA_FAST_MOBILE
        
        # Default strategy
        return ContentOptimizationStrategy.HIGH_PERFORMANCE
    
    async def _generate_variant_content(self, base_content: PersonalizedContent, 
                                      strategy: ContentOptimizationStrategy,
                                      device_context: AdvancedDeviceContext,
                                      persona_type: str) -> Dict[str, Any]:
        """Generate content variants optimized for strategy and device"""
        
        template = self.strategy_templates[strategy]
        
        # Generate hero message variations
        hero_variations = await self._generate_hero_variations(
            base_content.hero_message, template, device_context, persona_type
        )
        
        # Generate CTA variations
        cta_variations = await self._generate_cta_variations(
            base_content.call_to_action, template, device_context, persona_type
        )
        
        # Optimize trust signals
        optimized_trust_signals = await self._optimize_trust_signals(
            base_content.trust_signals, template, device_context
        )
        
        # Optimize social proof
        optimized_social_proof = await self._optimize_social_proof(
            base_content.social_proof, template, device_context
        )
        
        return {
            'hero_message': hero_variations['standard'],
            'hero_message_short': hero_variations['short'],
            'hero_message_ultra_short': hero_variations['ultra_short'],
            'call_to_action': cta_variations['primary'],
            'cta_variations': cta_variations['alternatives'],
            'trust_signals': optimized_trust_signals,
            'social_proof': optimized_social_proof
        }
    
    async def _generate_hero_variations(self, base_hero: str, template: Dict[str, Any],
                                      device_context: AdvancedDeviceContext, 
                                      persona_type: str) -> Dict[str, str]:
        """Generate hero message variations for different contexts"""
        
        # Remove emojis for ultra-clean versions if needed
        clean_hero = self._remove_emojis(base_hero) if template.get('clean_text', False) else base_hero
        
        # Standard version (original or slightly modified)
        standard = clean_hero
        
        # Short version for medium constraints
        short = await self._create_short_version(clean_hero, template['short_length'])
        
        # Ultra-short version for severe constraints
        ultra_short = await self._create_ultra_short_version(clean_hero, template['ultra_short_length'])
        
        # Apply persona-specific optimization
        if persona_type == 'TechEarlyAdopter':
            standard = self._add_tech_appeal(standard)
            short = self._add_tech_appeal(short, brief=True)
        elif persona_type == 'StudentHustler':
            standard = self._add_value_appeal(standard)
            short = self._add_value_appeal(short, brief=True)
        elif persona_type == 'BusinessOwner':
            standard = self._add_roi_appeal(standard)
            short = self._add_roi_appeal(short, brief=True)
        elif persona_type == 'RemoteDad':
            standard = self._add_family_appeal(standard)
            short = self._add_family_appeal(short, brief=True)
        
        return {
            'standard': standard,
            'short': short,
            'ultra_short': ultra_short
        }
    
    async def _generate_cta_variations(self, base_cta: str, template: Dict[str, Any],
                                     device_context: AdvancedDeviceContext,
                                     persona_type: str) -> Dict[str, Any]:
        """Generate CTA variations optimized for device and persona"""
        
        # Primary CTA (optimized for device)
        if device_context.device_type == DeviceType.MOBILE:
            primary_cta = self._optimize_mobile_cta(base_cta, template)
        elif device_context.device_type == DeviceType.TABLET:
            primary_cta = self._optimize_tablet_cta(base_cta, template)
        else:
            primary_cta = self._optimize_desktop_cta(base_cta, template)
        
        # Alternative variations for A/B testing
        alternatives = [
            self._create_urgency_cta(base_cta),
            self._create_benefit_cta(base_cta, persona_type),
            self._create_action_cta(base_cta),
            self._create_discovery_cta(base_cta)
        ]
        
        # Filter based on template constraints
        if template.get('max_cta_length'):
            alternatives = [cta for cta in alternatives if len(cta) <= template['max_cta_length']]
        
        return {
            'primary': primary_cta,
            'alternatives': alternatives[:3]  # Limit to top 3 alternatives
        }
    
    async def _optimize_media_elements(self, strategy: ContentOptimizationStrategy,
                                     device_context: AdvancedDeviceContext) -> MediaOptimization:
        """Optimize media elements based on strategy and device capabilities"""
        
        # Base configuration
        base_config = {
            'image_quality': 85,
            'image_format': 'webp',
            'max_image_size': (1200, 800),
            'video_enabled': True,
            'video_quality': '1080p',
            'animations_enabled': True,
            'lazy_loading': True,
            'preload_strategy': 'metadata'
        }
        
        # Strategy-specific optimizations
        if strategy == ContentOptimizationStrategy.ULTRA_FAST_MOBILE:
            base_config.update({
                'image_quality': 60,
                'max_image_size': (600, 400),
                'video_enabled': False,
                'animations_enabled': False,
                'preload_strategy': 'none'
            })
        elif strategy == ContentOptimizationStrategy.DATA_SAVER:
            base_config.update({
                'image_quality': 50,
                'max_image_size': (400, 300),
                'video_enabled': False,
                'animations_enabled': False,
                'preload_strategy': 'none'
            })
        elif strategy == ContentOptimizationStrategy.BATTERY_SAVER:
            base_config.update({
                'image_quality': 70,
                'video_enabled': False,
                'animations_enabled': False,
                'preload_strategy': 'metadata'
            })
        elif strategy == ContentOptimizationStrategy.RICH_INTERACTIVE:
            base_config.update({
                'image_quality': 95,
                'max_image_size': (1920, 1080),
                'video_quality': '4k' if device_context.screen_size[0] >= 1920 else '1080p',
                'preload_strategy': 'auto'
            })
        
        # Device-specific adjustments
        if device_context.device_type == DeviceType.MOBILE:
            base_config['max_image_size'] = (
                min(base_config['max_image_size'][0], 800),
                min(base_config['max_image_size'][1], 600)
            )
        
        # Network-specific adjustments
        if device_context.network_speed in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            base_config.update({
                'image_quality': min(base_config['image_quality'], 60),
                'video_enabled': False,
                'preload_strategy': 'none'
            })
        
        return MediaOptimization(**base_config)
    
    async def _configure_layout(self, device_context: AdvancedDeviceContext,
                              strategy: ContentOptimizationStrategy) -> LayoutConfiguration:
        """Configure layout based on device and strategy"""
        
        # Base configuration
        if device_context.device_type == DeviceType.MOBILE:
            base_config = {
                'container_width': '100%',
                'grid_columns': 1,
                'spacing_unit': 16,
                'font_scale': 1.0,
                'line_height': 1.5,
                'button_size': 'large',
                'touch_target_size': 44,
                'navigation_style': 'hamburger',
                'content_density': 'comfortable'
            }
        elif device_context.device_type == DeviceType.TABLET:
            base_config = {
                'container_width': '90%',
                'grid_columns': 2,
                'spacing_unit': 20,
                'font_scale': 1.1,
                'line_height': 1.6,
                'button_size': 'medium',
                'touch_target_size': 40,
                'navigation_style': 'tab_bar',
                'content_density': 'comfortable'
            }
        else:  # Desktop
            base_config = {
                'container_width': '1200px',
                'grid_columns': 3,
                'spacing_unit': 24,
                'font_scale': 1.0,
                'line_height': 1.6,
                'button_size': 'medium',
                'touch_target_size': 32,
                'navigation_style': 'horizontal',
                'content_density': 'compact'
            }
        
        # Strategy adjustments
        if strategy == ContentOptimizationStrategy.ACCESSIBILITY_FIRST:
            base_config.update({
                'font_scale': base_config['font_scale'] * 1.2,
                'line_height': 1.8,
                'touch_target_size': max(base_config['touch_target_size'], 48),
                'content_density': 'spacious'
            })
        elif strategy == ContentOptimizationStrategy.ULTRA_FAST_MOBILE:
            base_config.update({
                'spacing_unit': base_config['spacing_unit'] * 0.8,
                'content_density': 'compact'
            })
        
        # High-DPI adjustments
        if device_context.pixel_density >= 2.0:
            base_config['font_scale'] *= 0.9  # Slightly smaller on high-DPI screens
        
        return LayoutConfiguration(**base_config)
    
    async def _set_performance_budget(self, device_context: AdvancedDeviceContext,
                                    strategy: ContentOptimizationStrategy) -> PerformanceBudget:
        """Set performance budget based on device capabilities and strategy"""
        
        # Base budget for medium performance devices
        base_budget = {
            'max_bundle_size_kb': 500,
            'max_image_size_kb': 200,
            'max_font_size_kb': 50,
            'max_css_size_kb': 100,
            'max_js_size_kb': 300,
            'max_load_time_ms': 3000,
            'max_lcp_ms': 2500,
            'max_fid_ms': 100,
            'max_cls_score': 0.1
        }
        
        # Adjust for device capability
        if device_context.device_capability == DeviceCapability.HIGH_PERFORMANCE:
            for key in base_budget:
                if 'kb' in key or 'ms' in key:
                    base_budget[key] = int(base_budget[key] * 1.5)
        elif device_context.device_capability == DeviceCapability.LOW_PERFORMANCE:
            for key in base_budget:
                if 'kb' in key or 'ms' in key:
                    base_budget[key] = int(base_budget[key] * 0.7)
        elif device_context.device_capability == DeviceCapability.ULTRA_LOW:
            for key in base_budget:
                if 'kb' in key or 'ms' in key:
                    base_budget[key] = int(base_budget[key] * 0.5)
        
        # Strategy-specific adjustments
        if strategy == ContentOptimizationStrategy.ULTRA_FAST_MOBILE:
            base_budget.update({
                'max_bundle_size_kb': 200,
                'max_image_size_kb': 50,
                'max_load_time_ms': 1500,
                'max_lcp_ms': 1200
            })
        elif strategy == ContentOptimizationStrategy.RICH_INTERACTIVE:
            base_budget.update({
                'max_bundle_size_kb': 1000,
                'max_image_size_kb': 500,
                'max_js_size_kb': 600
            })
        
        # Network-specific adjustments
        if device_context.network_speed in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            for key in ['max_bundle_size_kb', 'max_image_size_kb']:
                base_budget[key] = int(base_budget[key] * 0.4)
        
        return PerformanceBudget(**base_budget)
    
    async def _apply_accessibility_optimizations(self, device_context: AdvancedDeviceContext,
                                               variant_content: Dict[str, Any]) -> Dict[str, Any]:
        """Apply accessibility optimizations based on detected features"""
        optimizations = {}
        
        for feature in device_context.accessibility_features:
            if feature == 'screen_reader':
                optimizations['screen_reader'] = {
                    'aria_labels': True,
                    'alt_text_required': True,
                    'heading_structure': True,
                    'skip_links': True
                }
            elif feature == 'high_contrast':
                optimizations['high_contrast'] = {
                    'contrast_ratio': 7.0,  # WCAG AAA
                    'color_scheme': 'high_contrast',
                    'outline_thickness': '3px'
                }
            elif feature == 'reduced_motion':
                optimizations['reduced_motion'] = {
                    'disable_animations': True,
                    'disable_parallax': True,
                    'disable_auto_play': True
                }
            elif feature == 'large_text':
                optimizations['large_text'] = {
                    'font_size_multiplier': 1.5,
                    'line_height_multiplier': 1.3,
                    'touch_target_multiplier': 1.2
                }
        
        return optimizations
    
    async def _generate_interaction_hints(self, device_context: AdvancedDeviceContext,
                                        persona_type: str) -> List[str]:
        """Generate interaction hints based on device and persona"""
        hints = []
        
        # Device-specific hints
        if device_context.device_type == DeviceType.MOBILE:
            hints.extend(['swipe_navigation', 'touch_friendly', 'thumb_reachable'])
        elif device_context.device_type == DeviceType.TABLET:
            hints.extend(['touch_navigation', 'two_hand_friendly', 'landscape_optimized'])
        else:  # Desktop
            hints.extend(['keyboard_shortcuts', 'hover_states', 'precise_clicking'])
        
        # Interaction pattern hints
        if device_context.interaction_pattern == InteractionPattern.QUICK_SCANNER:
            hints.extend(['fast_loading', 'immediate_value', 'scannable_content'])
        elif device_context.interaction_pattern == InteractionPattern.METHODICAL_READER:
            hints.extend(['detailed_content', 'clear_hierarchy', 'progress_indicators'])
        elif device_context.interaction_pattern == InteractionPattern.COMPARISON_SHOPPER:
            hints.extend(['comparison_tables', 'feature_highlighting', 'side_by_side'])
        
        # Persona-specific hints
        if persona_type == 'TechEarlyAdopter':
            hints.extend(['advanced_features', 'technical_details', 'cutting_edge'])
        elif persona_type == 'StudentHustler':
            hints.extend(['price_focus', 'quick_decisions', 'mobile_first'])
        elif persona_type == 'BusinessOwner':
            hints.extend(['roi_calculator', 'data_heavy', 'professional'])
        elif persona_type == 'RemoteDad':
            hints.extend(['family_friendly', 'security_focus', 'practical'])
        
        return list(set(hints))  # Remove duplicates
    
    def _determine_loading_strategy(self, device_context: AdvancedDeviceContext,
                                   strategy: ContentOptimizationStrategy) -> str:
        """Determine optimal loading strategy"""
        
        if strategy in [ContentOptimizationStrategy.ULTRA_FAST_MOBILE, ContentOptimizationStrategy.DATA_SAVER]:
            return 'critical_path_first'
        elif device_context.device_capability == DeviceCapability.HIGH_PERFORMANCE:
            return 'progressive_enhancement'
        elif device_context.network_speed in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            return 'minimal_first'
        else:
            return 'balanced'
    
    # Strategy template definitions
    def _get_ultra_fast_mobile_template(self) -> Dict[str, Any]:
        return {
            'short_length': 30,
            'ultra_short_length': 15,
            'max_cta_length': 12,
            'clean_text': True,
            'emoji_limit': 1,
            'trust_signal_limit': 2
        }
    
    def _get_battery_saver_template(self) -> Dict[str, Any]:
        return {
            'short_length': 50,
            'ultra_short_length': 25,
            'max_cta_length': 15,
            'clean_text': False,
            'emoji_limit': 2,
            'trust_signal_limit': 3
        }
    
    def _get_data_saver_template(self) -> Dict[str, Any]:
        return {
            'short_length': 40,
            'ultra_short_length': 20,
            'max_cta_length': 10,
            'clean_text': True,
            'emoji_limit': 0,
            'trust_signal_limit': 2
        }
    
    def _get_high_performance_template(self) -> Dict[str, Any]:
        return {
            'short_length': 80,
            'ultra_short_length': 40,
            'max_cta_length': 25,
            'clean_text': False,
            'emoji_limit': 3,
            'trust_signal_limit': 5
        }
    
    def _get_accessibility_template(self) -> Dict[str, Any]:
        return {
            'short_length': 60,
            'ultra_short_length': 30,
            'max_cta_length': 20,
            'clean_text': True,
            'emoji_limit': 1,
            'trust_signal_limit': 4
        }
    
    def _get_minimal_bandwidth_template(self) -> Dict[str, Any]:
        return {
            'short_length': 35,
            'ultra_short_length': 18,
            'max_cta_length': 8,
            'clean_text': True,
            'emoji_limit': 0,
            'trust_signal_limit': 1
        }
    
    def _get_rich_interactive_template(self) -> Dict[str, Any]:
        return {
            'short_length': 100,
            'ultra_short_length': 50,
            'max_cta_length': 30,
            'clean_text': False,
            'emoji_limit': 5,
            'trust_signal_limit': 8
        }
    
    # Helper methods for content optimization
    def _remove_emojis(self, text: str) -> str:
        """Remove emojis from text"""
        import re
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text).strip()
    
    async def _create_short_version(self, text: str, max_length: int) -> str:
        """Create short version of text"""
        if len(text) <= max_length:
            return text
        
        # Try to cut at word boundary
        words = text.split()
        short_text = ""
        for word in words:
            if len(short_text + " " + word) <= max_length - 3:
                short_text += " " + word if short_text else word
            else:
                break
        
        return short_text + "..." if short_text else text[:max_length-3] + "..."
    
    async def _create_ultra_short_version(self, text: str, max_length: int) -> str:
        """Create ultra-short version of text"""
        if len(text) <= max_length:
            return text
        
        # Extract key words
        key_words = ['save', 'get', 'free', 'now', 'buy', 'start', 'join', 'try']
        words = text.lower().split()
        
        for key in key_words:
            if key in words:
                idx = words.index(key)
                fragment = ' '.join(words[idx:idx+2])
                if len(fragment) <= max_length:
                    return fragment.capitalize()
        
        # Fallback to truncation
        return text[:max_length-1] + "→"
    
    def _optimize_mobile_cta(self, cta: str, template: Dict[str, Any]) -> str:
        """Optimize CTA for mobile devices"""
        mobile_optimizations = {
            'Get Started': 'Start →',
            'Learn More': 'Learn →',
            'Sign Up Now': 'Join →',
            'Buy Now': 'Buy →',
            'Download': 'Get →',
            'Schedule': 'Book →'
        }
        
        for long_form, short_form in mobile_optimizations.items():
            if long_form.lower() in cta.lower():
                return short_form
        
        # Ensure CTA fits template constraints
        if len(cta) > template.get('max_cta_length', 15):
            return cta[:template['max_cta_length']-1] + "→"
        
        return cta + " →" if not cta.endswith("→") else cta
    
    def _optimize_tablet_cta(self, cta: str, template: Dict[str, Any]) -> str:
        """Optimize CTA for tablet devices"""
        return f"👆 {cta}" if not any(emoji in cta for emoji in ['👆', '▶️', '→']) else cta
    
    def _optimize_desktop_cta(self, cta: str, template: Dict[str, Any]) -> str:
        """Optimize CTA for desktop devices"""
        return cta  # Desktop can handle full CTAs
    
    def _add_tech_appeal(self, text: str, brief: bool = False) -> str:
        """Add tech appeal to content"""
        tech_prefixes = ['🚀', '⚡', '🔬'] if not brief else ['🚀']
        if not any(prefix in text for prefix in tech_prefixes):
            return f"🚀 {text}"
        return text
    
    def _add_value_appeal(self, text: str, brief: bool = False) -> str:
        """Add value appeal for students"""
        value_prefixes = ['💰', '🎓', '💸'] if not brief else ['💰']
        if not any(prefix in text for prefix in value_prefixes):
            return f"💰 {text}"
        return text
    
    def _add_roi_appeal(self, text: str, brief: bool = False) -> str:
        """Add ROI appeal for business owners"""
        roi_prefixes = ['📈', '💼', '🎯'] if not brief else ['📈']
        if not any(prefix in text for prefix in roi_prefixes):
            return f"📈 {text}"
        return text
    
    def _add_family_appeal(self, text: str, brief: bool = False) -> str:
        """Add family appeal for remote dads"""
        family_prefixes = ['👨‍👩‍👧‍👦', '🏡', '👪'] if not brief else ['🏡']
        if not any(prefix in text for prefix in family_prefixes):
            return f"🏡 {text}"
        return text
    
    def _create_urgency_cta(self, base_cta: str) -> str:
        """Create urgency-focused CTA"""
        return f"⚡ {base_cta} Now"
    
    def _create_benefit_cta(self, base_cta: str, persona_type: str) -> str:
        """Create benefit-focused CTA"""
        benefit_map = {
            'TechEarlyAdopter': 'Innovate',
            'StudentHustler': 'Save Big',
            'BusinessOwner': 'Grow Revenue',
            'RemoteDad': 'Secure Future'
        }
        benefit = benefit_map.get(persona_type, 'Get Benefits')
        return f"{benefit} → {base_cta}"
    
    def _create_action_cta(self, base_cta: str) -> str:
        """Create action-focused CTA"""
        return f"✓ {base_cta}"
    
    def _create_discovery_cta(self, base_cta: str) -> str:
        """Create discovery-focused CTA"""
        return f"Discover → {base_cta}"
    
    async def _optimize_trust_signals(self, trust_signals: List[str], 
                                    template: Dict[str, Any],
                                    device_context: AdvancedDeviceContext) -> List[str]:
        """Optimize trust signals for device and template"""
        limit = template.get('trust_signal_limit', 5)
        
        # Prioritize trust signals based on device type
        if device_context.device_type == DeviceType.MOBILE:
            # Mobile users prefer security and simplicity
            priority_order = ['secure', 'ssl', 'encrypted', 'verified', 'certified', 'guarantee']
        else:
            # Desktop users can handle more detailed trust signals
            priority_order = ['certified', 'verified', 'guarantee', 'secure', 'enterprise', 'compliant']
        
        # Sort trust signals by priority
        prioritized = []
        remaining = trust_signals.copy()
        
        for priority_term in priority_order:
            for signal in trust_signals:
                if priority_term.lower() in signal.lower() and signal not in prioritized:
                    prioritized.append(signal)
                    if signal in remaining:
                        remaining.remove(signal)
        
        # Add remaining signals
        prioritized.extend(remaining)
        
        return prioritized[:limit]
    
    async def _optimize_social_proof(self, social_proof: str, 
                                   template: Dict[str, Any],
                                   device_context: AdvancedDeviceContext) -> str:
        """Optimize social proof for device constraints"""
        if not social_proof:
            return social_proof
        
        # Mobile optimization
        if device_context.device_type == DeviceType.MOBILE and len(social_proof) > 40:
            # Extract numbers for mobile-friendly version
            import re
            numbers = re.findall(r'\d+[kKmM]?', social_proof)
            if numbers:
                return f"⭐ {numbers[0]}+ customers love us"
            else:
                return social_proof[:35] + "..."
        
        return social_proof
    
    def _generate_variant_id(self, device_context: AdvancedDeviceContext,
                           strategy: ContentOptimizationStrategy,
                           persona_type: str) -> str:
        """Generate unique variant ID"""
        components = [
            device_context.device_type.value,
            device_context.device_capability.value,
            device_context.network_speed.value,
            strategy.value,
            persona_type
        ]
        
        variant_string = "_".join(components)
        return hashlib.md5(variant_string.encode()).hexdigest()[:12]
    
    async def _cache_content_variant(self, session_id: str, variant: ContentVariant):
        """Cache content variant for performance"""
        try:
            cache_key = f"content_variant:{session_id}:{variant.variant_id}"
            cache_data = asdict(variant)
            cache_data['generated_at'] = datetime.utcnow().isoformat()
            
            await self.redis_client.setex(cache_key, 1800, json.dumps(cache_data))  # 30 min cache
        except Exception as e:
            logger.error(f"Error caching content variant: {str(e)}")
    
    async def _record_variant_generation(self, session: JourneySession, 
                                       variant: ContentVariant,
                                       strategy: ContentOptimizationStrategy):
        """Record variant generation in database"""
        try:
            personalization_record = PersonalizationData(
                session_id=session.session_id,
                personalization_type="content_variant",
                personalization_strategy=strategy.value,
                variant_id=variant.variant_id,
                content_delivered=asdict(variant),
                ml_model_version="variant_gen_v1.0",
                confidence_score=1.0,  # Variant generation always has full confidence
                device_optimization_applied=True
            )
            
            self.db.add(personalization_record)
            await self.db.commit()
            
        except Exception as e:
            logger.error(f"Error recording variant generation: {str(e)}")
    
    async def _generate_fallback_variant(self, base_content: PersonalizedContent,
                                       device_context: AdvancedDeviceContext) -> ContentVariant:
        """Generate fallback variant when main generation fails"""
        return ContentVariant(
            variant_id="fallback_variant",
            device_target=device_context.device_type,
            capability_target=DeviceCapability.MEDIUM_PERFORMANCE,
            network_target=NetworkSpeed.CELLULAR_4G,
            content_format="standard",
            hero_message=base_content.hero_message,
            hero_message_short=base_content.hero_message[:50] + "..." if len(base_content.hero_message) > 50 else base_content.hero_message,
            hero_message_ultra_short=base_content.hero_message[:25] + "..." if len(base_content.hero_message) > 25 else base_content.hero_message,
            call_to_action=base_content.call_to_action,
            cta_variations=[base_content.call_to_action],
            trust_signals=base_content.trust_signals[:3],
            social_proof=base_content.social_proof or "Trusted by thousands",
            media_elements=asdict(MediaOptimization(
                image_quality=75, image_format='jpg', max_image_size=(800, 600),
                video_enabled=False, video_quality='720p', animations_enabled=True,
                lazy_loading=True, preload_strategy='metadata'
            )),
            layout_config=asdict(LayoutConfiguration(
                container_width='100%', grid_columns=1, spacing_unit=16,
                font_scale=1.0, line_height=1.5, button_size='medium',
                touch_target_size=44, navigation_style='simple', content_density='comfortable'
            )),
            performance_budget=asdict(PerformanceBudget(
                max_bundle_size_kb=400, max_image_size_kb=150, max_font_size_kb=40,
                max_css_size_kb=80, max_js_size_kb=250, max_load_time_ms=3000,
                max_lcp_ms=2500, max_fid_ms=100, max_cls_score=0.1
            )),
            loading_strategy='balanced',
            interaction_hints=['touch_friendly', 'fast_loading'],
            accessibility_optimizations={}
        )

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'IntelligentContentVariantGenerator',
    'ContentVariant',
    'ContentOptimizationStrategy',
    'MediaOptimization',
    'LayoutConfiguration', 
    'PerformanceBudget'
]