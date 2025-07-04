# Advanced Device Detection Service - Week 2 Implementation
# Module: 3A - Week 2 - Advanced Device-Specific Content Variants
# Created: 2025-07-04

import asyncio
import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from user_agents import parse as parse_user_agent

logger = logging.getLogger(__name__)

# =============================================================================
# DEVICE DETECTION MODELS
# =============================================================================

@dataclass
class DeviceProfile:
    """Comprehensive device profile with capabilities"""
    device_type: str  # mobile, tablet, desktop
    device_category: str  # smartphone, tablet, laptop, desktop
    screen_size: str  # small, medium, large, extra_large
    orientation: str  # portrait, landscape
    touch_capable: bool
    performance_tier: str  # low, medium, high
    network_speed: str  # slow, medium, fast
    brand: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    browser: Optional[str] = None
    browser_version: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'device_type': self.device_type,
            'device_category': self.device_category,
            'screen_size': self.screen_size,
            'orientation': self.orientation,
            'touch_capable': self.touch_capable,
            'performance_tier': self.performance_tier,
            'network_speed': self.network_speed,
            'brand': self.brand,
            'model': self.model,
            'os': self.os,
            'os_version': self.os_version,
            'browser': self.browser,
            'browser_version': self.browser_version
        }

@dataclass
class ContentCapabilities:
    """Content rendering capabilities for device"""
    supports_video: bool
    supports_animations: bool
    supports_webgl: bool
    supports_webp: bool
    supports_svg: bool
    max_image_size: int  # in KB
    optimal_font_size: int  # in px
    optimal_button_size: int  # in px
    touch_target_size: int  # in px
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'supports_video': self.supports_video,
            'supports_animations': self.supports_animations,
            'supports_webgl': self.supports_webgl,
            'supports_webp': self.supports_webp,
            'supports_svg': self.supports_svg,
            'max_image_size': self.max_image_size,
            'optimal_font_size': self.optimal_font_size,
            'optimal_button_size': self.optimal_button_size,
            'touch_target_size': self.touch_target_size
        }

@dataclass
class UXOptimizations:
    """UX optimizations for specific device"""
    layout_strategy: str  # single_column, two_column, grid
    navigation_type: str  # hamburger, tab_bar, sidebar
    form_strategy: str  # single_page, multi_step, progressive
    cta_placement: str  # top, bottom, floating, sticky
    content_density: str  # compact, normal, spacious
    interaction_style: str  # touch, mouse, hybrid
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'layout_strategy': self.layout_strategy,
            'navigation_type': self.navigation_type,
            'form_strategy': self.form_strategy,
            'cta_placement': self.cta_placement,
            'content_density': self.content_density,
            'interaction_style': self.interaction_style
        }

# =============================================================================
# ADVANCED DEVICE DETECTION SERVICE
# =============================================================================

class AdvancedDeviceDetectionService:
    """Enhanced device detection with capability analysis"""
    
    def __init__(self):
        self.device_cache = {}
        self.capability_rules = self._initialize_capability_rules()
        self.ux_optimization_rules = self._initialize_ux_rules()
        
    async def detect_device_comprehensive(self, user_agent: str, client_hints: Optional[Dict[str, Any]] = None, 
                                        viewport: Optional[Dict[str, int]] = None) -> Tuple[DeviceProfile, ContentCapabilities, UXOptimizations]:
        """Comprehensive device detection with capabilities and UX optimizations"""
        try:
            # Parse user agent
            parsed_ua = parse_user_agent(user_agent)
            
            # Create base device profile
            device_profile = await self._create_device_profile(parsed_ua, client_hints, viewport)
            
            # Determine content capabilities
            content_capabilities = await self._determine_content_capabilities(device_profile, client_hints)
            
            # Generate UX optimizations
            ux_optimizations = await self._generate_ux_optimizations(device_profile, content_capabilities)
            
            # Cache result
            cache_key = self._generate_cache_key(user_agent, client_hints, viewport)
            self.device_cache[cache_key] = {
                'device_profile': device_profile,
                'content_capabilities': content_capabilities,
                'ux_optimizations': ux_optimizations,
                'timestamp': datetime.utcnow()
            }
            
            logger.debug(f"Comprehensive device detection completed: {device_profile.device_type}")
            return device_profile, content_capabilities, ux_optimizations
            
        except Exception as e:
            logger.error(f"Error in comprehensive device detection: {str(e)}")
            return await self._get_fallback_detection()
    
    async def _create_device_profile(self, parsed_ua: Any, client_hints: Optional[Dict[str, Any]], 
                                   viewport: Optional[Dict[str, int]]) -> DeviceProfile:
        """Create detailed device profile"""
        # Basic device type detection
        if parsed_ua.is_mobile:
            device_type = "mobile"
            device_category = "smartphone"
        elif parsed_ua.is_tablet:
            device_type = "tablet"
            device_category = "tablet"
        else:
            device_type = "desktop"
            device_category = "desktop" if not self._is_laptop(parsed_ua) else "laptop"
        
        # Screen size analysis
        screen_size = await self._determine_screen_size(device_type, viewport, client_hints)
        
        # Orientation detection
        orientation = await self._determine_orientation(viewport, device_type)
        
        # Performance tier analysis
        performance_tier = await self._analyze_performance_tier(parsed_ua, client_hints)
        
        # Network speed estimation
        network_speed = await self._estimate_network_speed(client_hints)
        
        return DeviceProfile(
            device_type=device_type,
            device_category=device_category,
            screen_size=screen_size,
            orientation=orientation,
            touch_capable=device_type in ["mobile", "tablet"],
            performance_tier=performance_tier,
            network_speed=network_speed,
            brand=self._extract_brand(parsed_ua),
            model=self._extract_model(parsed_ua),
            os=parsed_ua.os.family if parsed_ua.os else None,
            os_version=parsed_ua.os.version_string if parsed_ua.os else None,
            browser=parsed_ua.browser.family if parsed_ua.browser else None,
            browser_version=parsed_ua.browser.version_string if parsed_ua.browser else None
        )
    
    async def _determine_content_capabilities(self, device_profile: DeviceProfile, 
                                            client_hints: Optional[Dict[str, Any]]) -> ContentCapabilities:
        """Determine content rendering capabilities"""
        # Base capabilities by device type
        if device_profile.device_type == "mobile":
            base_capabilities = {
                'supports_video': True,
                'supports_animations': device_profile.performance_tier != "low",
                'supports_webgl': device_profile.performance_tier == "high",
                'supports_webp': True,
                'supports_svg': True,
                'max_image_size': 500 if device_profile.performance_tier == "low" else 1000,
                'optimal_font_size': 16,
                'optimal_button_size': 44,
                'touch_target_size': 44
            }
        elif device_profile.device_type == "tablet":
            base_capabilities = {
                'supports_video': True,
                'supports_animations': True,
                'supports_webgl': device_profile.performance_tier != "low",
                'supports_webp': True,
                'supports_svg': True,
                'max_image_size': 1500,
                'optimal_font_size': 18,
                'optimal_button_size': 48,
                'touch_target_size': 48
            }
        else:  # desktop
            base_capabilities = {
                'supports_video': True,
                'supports_animations': True,
                'supports_webgl': True,
                'supports_webp': True,
                'supports_svg': True,
                'max_image_size': 3000,
                'optimal_font_size': 16,
                'optimal_button_size': 40,
                'touch_target_size': 40
            }
        
        # Apply performance tier adjustments
        if device_profile.performance_tier == "low":
            base_capabilities['supports_animations'] = False
            base_capabilities['supports_webgl'] = False
            base_capabilities['max_image_size'] = min(base_capabilities['max_image_size'], 300)
        
        # Apply network speed adjustments
        if device_profile.network_speed == "slow":
            base_capabilities['max_image_size'] = min(base_capabilities['max_image_size'], 200)
            base_capabilities['supports_animations'] = False
        
        return ContentCapabilities(**base_capabilities)
    
    async def _generate_ux_optimizations(self, device_profile: DeviceProfile, 
                                       content_capabilities: ContentCapabilities) -> UXOptimizations:
        """Generate UX optimizations based on device capabilities"""
        optimizations = {}
        
        # Layout strategy
        if device_profile.device_type == "mobile":
            optimizations['layout_strategy'] = "single_column"
            optimizations['navigation_type'] = "hamburger" if device_profile.screen_size == "small" else "tab_bar"
            optimizations['form_strategy'] = "multi_step"
            optimizations['cta_placement'] = "floating"
            optimizations['content_density'] = "compact"
        elif device_profile.device_type == "tablet":
            optimizations['layout_strategy'] = "two_column" if device_profile.orientation == "landscape" else "single_column"
            optimizations['navigation_type'] = "tab_bar"
            optimizations['form_strategy'] = "progressive"
            optimizations['cta_placement'] = "sticky"
            optimizations['content_density'] = "normal"
        else:  # desktop
            optimizations['layout_strategy'] = "grid"
            optimizations['navigation_type'] = "sidebar"
            optimizations['form_strategy'] = "single_page"
            optimizations['cta_placement'] = "top"
            optimizations['content_density'] = "spacious"
        
        # Interaction style
        optimizations['interaction_style'] = "touch" if device_profile.touch_capable else "mouse"
        
        return UXOptimizations(**optimizations)
    
    async def _determine_screen_size(self, device_type: str, viewport: Optional[Dict[str, int]], 
                                   client_hints: Optional[Dict[str, Any]]) -> str:
        """Determine screen size category"""
        if viewport:
            width = viewport.get('width', 0)
            
            if device_type == "mobile":
                if width <= 360:
                    return "small"
                elif width <= 414:
                    return "medium"
                else:
                    return "large"
            elif device_type == "tablet":
                if width <= 768:
                    return "small"
                elif width <= 1024:
                    return "medium"
                else:
                    return "large"
            else:  # desktop
                if width <= 1366:
                    return "medium"
                elif width <= 1920:
                    return "large"
                else:
                    return "extra_large"
        
        # Fallback based on device type
        screen_size_defaults = {
            "mobile": "medium",
            "tablet": "medium",
            "desktop": "large"
        }
        return screen_size_defaults.get(device_type, "medium")
    
    async def _determine_orientation(self, viewport: Optional[Dict[str, int]], device_type: str) -> str:
        """Determine device orientation"""
        if viewport:
            width = viewport.get('width', 0)
            height = viewport.get('height', 0)
            
            if width > height:
                return "landscape"
            else:
                return "portrait"
        
        # Default orientation by device type
        if device_type == "mobile":
            return "portrait"
        else:
            return "landscape"
    
    async def _analyze_performance_tier(self, parsed_ua: Any, client_hints: Optional[Dict[str, Any]]) -> str:
        """Analyze device performance tier"""
        # Performance indicators
        performance_score = 50  # Base score
        
        # Browser-based performance hints
        if parsed_ua.browser:
            browser = parsed_ua.browser.family.lower()
            if 'chrome' in browser or 'firefox' in browser or 'safari' in browser:
                performance_score += 20
            elif 'edge' in browser:
                performance_score += 15
            else:
                performance_score -= 10
        
        # OS-based performance hints
        if parsed_ua.os:
            os_family = parsed_ua.os.family.lower()
            if 'ios' in os_family or 'mac' in os_family:
                performance_score += 15
            elif 'android' in os_family:
                # Android version matters for performance
                try:
                    version = float(parsed_ua.os.version_string.split('.')[0])
                    if version >= 10:
                        performance_score += 10
                    elif version >= 7:
                        performance_score += 5
                    else:
                        performance_score -= 10
                except:
                    pass
            elif 'windows' in os_family:
                performance_score += 10
        
        # Client hints analysis
        if client_hints:
            # Memory hints
            device_memory = client_hints.get('device-memory', 0)
            if device_memory >= 8:
                performance_score += 20
            elif device_memory >= 4:
                performance_score += 10
            elif device_memory >= 2:
                performance_score += 5
            else:
                performance_score -= 15
            
            # CPU hints
            hardware_concurrency = client_hints.get('hardware-concurrency', 0)
            if hardware_concurrency >= 8:
                performance_score += 15
            elif hardware_concurrency >= 4:
                performance_score += 10
            elif hardware_concurrency >= 2:
                performance_score += 5
        
        # Determine tier
        if performance_score >= 70:
            return "high"
        elif performance_score >= 50:
            return "medium"
        else:
            return "low"
    
    async def _estimate_network_speed(self, client_hints: Optional[Dict[str, Any]]) -> str:
        """Estimate network connection speed"""
        if client_hints:
            # Connection type hints
            connection_type = client_hints.get('connection-type', '').lower()
            effective_type = client_hints.get('effective-connection-type', '').lower()
            
            if 'wifi' in connection_type or '5g' in connection_type or 'ethernet' in connection_type:
                return "fast"
            elif '4g' in connection_type or effective_type in ['4g']:
                return "medium"
            elif '3g' in connection_type or effective_type in ['3g', 'slow-2g', '2g']:
                return "slow"
            
            # Bandwidth hints
            downlink = client_hints.get('downlink', 0)
            if downlink >= 10:
                return "fast"
            elif downlink >= 1.5:
                return "medium"
            elif downlink > 0:
                return "slow"
        
        return "medium"  # Default assumption
    
    def _extract_brand(self, parsed_ua: Any) -> Optional[str]:
        """Extract device brand from user agent"""
        ua_string = str(parsed_ua).lower()
        
        # Common mobile brands
        brands = {
            'iphone': 'Apple',
            'ipad': 'Apple',
            'samsung': 'Samsung',
            'huawei': 'Huawei',
            'xiaomi': 'Xiaomi',
            'oneplus': 'OnePlus',
            'google': 'Google',
            'lg': 'LG',
            'htc': 'HTC',
            'sony': 'Sony',
            'motorola': 'Motorola',
            'nokia': 'Nokia'
        }
        
        for pattern, brand in brands.items():
            if pattern in ua_string:
                return brand
        
        return None
    
    def _extract_model(self, parsed_ua: Any) -> Optional[str]:
        """Extract device model from user agent"""
        # This would be enhanced with more sophisticated model detection
        if hasattr(parsed_ua, 'device') and parsed_ua.device.model:
            return parsed_ua.device.model
        return None
    
    def _is_laptop(self, parsed_ua: Any) -> bool:
        """Determine if desktop device is a laptop"""
        # Heuristics for laptop detection
        ua_string = str(parsed_ua).lower()
        laptop_indicators = ['macbook', 'laptop', 'mobile', 'touch']
        
        for indicator in laptop_indicators:
            if indicator in ua_string:
                return True
        
        return False
    
    def _generate_cache_key(self, user_agent: str, client_hints: Optional[Dict[str, Any]], 
                           viewport: Optional[Dict[str, int]]) -> str:
        """Generate cache key for device detection result"""
        key_parts = [user_agent]
        
        if client_hints:
            key_parts.append(json.dumps(client_hints, sort_keys=True))
        
        if viewport:
            key_parts.append(json.dumps(viewport, sort_keys=True))
        
        return "|".join(key_parts)
    
    async def _get_fallback_detection(self) -> Tuple[DeviceProfile, ContentCapabilities, UXOptimizations]:
        """Fallback device detection when primary detection fails"""
        # Return conservative mobile-first defaults
        device_profile = DeviceProfile(
            device_type="mobile",
            device_category="smartphone",
            screen_size="medium",
            orientation="portrait",
            touch_capable=True,
            performance_tier="medium",
            network_speed="medium"
        )
        
        content_capabilities = ContentCapabilities(
            supports_video=True,
            supports_animations=True,
            supports_webgl=False,
            supports_webp=True,
            supports_svg=True,
            max_image_size=500,
            optimal_font_size=16,
            optimal_button_size=44,
            touch_target_size=44
        )
        
        ux_optimizations = UXOptimizations(
            layout_strategy="single_column",
            navigation_type="hamburger",
            form_strategy="multi_step",
            cta_placement="floating",
            content_density="compact",
            interaction_style="touch"
        )
        
        return device_profile, content_capabilities, ux_optimizations
    
    def _initialize_capability_rules(self) -> Dict[str, Any]:
        """Initialize device capability rules"""
        return {
            'video_support': {
                'high_performance': {'webm': True, 'mp4': True, 'max_resolution': '4K'},
                'medium_performance': {'webm': True, 'mp4': True, 'max_resolution': '1080p'},
                'low_performance': {'webm': False, 'mp4': True, 'max_resolution': '720p'}
            },
            'animation_support': {
                'high_performance': {'css_animations': True, 'js_animations': True, 'webgl': True},
                'medium_performance': {'css_animations': True, 'js_animations': True, 'webgl': False},
                'low_performance': {'css_animations': True, 'js_animations': False, 'webgl': False}
            }
        }
    
    def _initialize_ux_rules(self) -> Dict[str, Any]:
        """Initialize UX optimization rules"""
        return {
            'mobile': {
                'max_form_fields_per_step': 3,
                'min_touch_target_size': 44,
                'preferred_navigation': 'bottom_tabs',
                'scroll_behavior': 'smooth'
            },
            'tablet': {
                'max_form_fields_per_step': 5,
                'min_touch_target_size': 48,
                'preferred_navigation': 'sidebar',
                'scroll_behavior': 'smooth'
            },
            'desktop': {
                'max_form_fields_per_step': 8,
                'min_touch_target_size': 40,
                'preferred_navigation': 'top_nav',
                'scroll_behavior': 'auto'
            }
        }
    
    # =============================================================================
    # DEVICE-SPECIFIC OPTIMIZATION METHODS
    # =============================================================================
    
    async def get_device_optimizations(self, device_profile: DeviceProfile) -> Dict[str, Any]:
        """Get comprehensive device optimizations"""
        try:
            optimizations = {
                'performance': await self._get_performance_optimizations(device_profile),
                'content': await self._get_content_optimizations(device_profile),
                'interaction': await self._get_interaction_optimizations(device_profile),
                'layout': await self._get_layout_optimizations(device_profile)
            }
            
            return optimizations
            
        except Exception as e:
            logger.error(f"Error getting device optimizations: {str(e)}")
            return {}
    
    async def _get_performance_optimizations(self, device_profile: DeviceProfile) -> Dict[str, Any]:
        """Get performance-specific optimizations"""
        optimizations = {}
        
        if device_profile.performance_tier == "low":
            optimizations.update({
                'lazy_loading': True,
                'image_compression': 'high',
                'minimize_js': True,
                'disable_animations': True,
                'prefetch_critical_only': True
            })
        elif device_profile.performance_tier == "medium":
            optimizations.update({
                'lazy_loading': True,
                'image_compression': 'medium',
                'minimize_js': False,
                'disable_animations': False,
                'prefetch_critical_only': False
            })
        else:  # high performance
            optimizations.update({
                'lazy_loading': False,
                'image_compression': 'low',
                'minimize_js': False,
                'disable_animations': False,
                'prefetch_critical_only': False,
                'enable_advanced_features': True
            })
        
        return optimizations
    
    async def _get_content_optimizations(self, device_profile: DeviceProfile) -> Dict[str, Any]:
        """Get content-specific optimizations"""
        optimizations = {}
        
        if device_profile.device_type == "mobile":
            optimizations.update({
                'text_size': 'large',
                'line_height': 1.6,
                'content_width': '100%',
                'image_aspect_ratio': '16:9',
                'video_controls': 'touch_friendly'
            })
        elif device_profile.device_type == "tablet":
            optimizations.update({
                'text_size': 'medium',
                'line_height': 1.5,
                'content_width': '80%',
                'image_aspect_ratio': '4:3',
                'video_controls': 'standard'
            })
        else:  # desktop
            optimizations.update({
                'text_size': 'standard',
                'line_height': 1.4,
                'content_width': '70%',
                'image_aspect_ratio': '16:9',
                'video_controls': 'detailed'
            })
        
        return optimizations
    
    async def _get_interaction_optimizations(self, device_profile: DeviceProfile) -> Dict[str, Any]:
        """Get interaction-specific optimizations"""
        optimizations = {}
        
        if device_profile.touch_capable:
            optimizations.update({
                'hover_effects': False,
                'touch_feedback': True,
                'swipe_gestures': True,
                'pinch_zoom': device_profile.device_type == "mobile",
                'double_tap_zoom': device_profile.device_type == "mobile"
            })
        else:
            optimizations.update({
                'hover_effects': True,
                'touch_feedback': False,
                'swipe_gestures': False,
                'pinch_zoom': False,
                'double_tap_zoom': False,
                'keyboard_shortcuts': True
            })
        
        return optimizations
    
    async def _get_layout_optimizations(self, device_profile: DeviceProfile) -> Dict[str, Any]:
        """Get layout-specific optimizations"""
        optimizations = {}
        
        if device_profile.device_type == "mobile":
            optimizations.update({
                'columns': 1,
                'sidebar_position': 'hidden',
                'navigation_style': 'hamburger',
                'content_padding': 'minimal',
                'button_size': 'large'
            })
        elif device_profile.device_type == "tablet":
            optimizations.update({
                'columns': 2 if device_profile.orientation == "landscape" else 1,
                'sidebar_position': 'collapsible',
                'navigation_style': 'tabs',
                'content_padding': 'normal',
                'button_size': 'medium'
            })
        else:  # desktop
            optimizations.update({
                'columns': 3,
                'sidebar_position': 'fixed',
                'navigation_style': 'horizontal',
                'content_padding': 'spacious',
                'button_size': 'standard'
            })
        
        return optimizations

# =============================================================================
# SERVICE INITIALIZATION
# =============================================================================

# Global service instance
device_detection_service = AdvancedDeviceDetectionService()