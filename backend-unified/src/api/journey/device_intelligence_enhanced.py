# Enhanced Device Intelligence System - Phase 3, Week 2
# Module: Advanced Device-Specific Content Variants  
# Created: 2025-07-05

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from enum import Enum
from dataclasses import dataclass
from user_agents import parse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, PersonalizationData
from ...utils.redis_client import get_redis_client
from ...utils.ml_models import ml_model_manager
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# ENHANCED DEVICE DETECTION MODELS
# =============================================================================

class DeviceCapability(Enum):
    """Device capability classifications"""
    HIGH_PERFORMANCE = "high_performance"
    MEDIUM_PERFORMANCE = "medium_performance" 
    LOW_PERFORMANCE = "low_performance"
    ULTRA_LOW = "ultra_low"

class NetworkSpeed(Enum):
    """Network connection speed classifications"""
    WIFI_FAST = "wifi_fast"
    WIFI_SLOW = "wifi_slow"
    CELLULAR_5G = "cellular_5g"
    CELLULAR_4G = "cellular_4g"
    CELLULAR_3G = "cellular_3g"
    CELLULAR_2G = "cellular_2g"

class InteractionPattern(Enum):
    """User interaction pattern classifications"""
    QUICK_SCANNER = "quick_scanner"
    METHODICAL_READER = "methodical_reader"
    COMPARISON_SHOPPER = "comparison_shopper"
    IMPULSE_BUYER = "impulse_buyer"
    RESEARCH_HEAVY = "research_heavy"

@dataclass
class AdvancedDeviceContext:
    """Advanced device context with comprehensive capabilities"""
    device_type: DeviceType
    screen_size: Tuple[int, int]
    pixel_density: float
    viewport_size: Tuple[int, int]
    user_agent: str
    browser_engine: str
    browser_version: str
    os_name: str
    os_version: str
    device_memory: Optional[int]
    hardware_concurrency: Optional[int]
    network_speed: NetworkSpeed
    connection_type: str
    touch_support: bool
    device_capability: DeviceCapability
    preferred_content_format: str
    battery_level: Optional[float]
    data_saver_mode: bool
    accessibility_features: List[str]
    interaction_pattern: InteractionPattern
    performance_score: float

@dataclass
class ContentVariant:
    """Content variant optimized for specific device characteristics"""
    variant_id: str
    device_target: DeviceType
    capability_target: DeviceCapability
    network_target: NetworkSpeed
    content_format: str
    hero_message: str
    hero_message_short: str
    hero_message_ultra_short: str
    call_to_action: str
    cta_variations: List[str]
    trust_signals: List[str]
    social_proof: str
    media_elements: Dict[str, Any]
    layout_config: Dict[str, Any]
    performance_budget: Dict[str, int]
    loading_strategy: str
    interaction_hints: List[str]
    accessibility_optimizations: Dict[str, Any]

# =============================================================================
# ADVANCED DEVICE DETECTION ENGINE
# =============================================================================

class AdvancedDeviceDetector:
    """Advanced device detection with comprehensive capability analysis"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.device_fingerprints = {}
        self.performance_models = {
            'mobile': self._load_mobile_performance_model(),
            'tablet': self._load_tablet_performance_model(),
            'desktop': self._load_desktop_performance_model()
        }
        
    async def detect_advanced_device_context(self, request_data: Dict[str, Any], session_id: str) -> AdvancedDeviceContext:
        """Detect comprehensive device context with advanced capabilities"""
        try:
            logger.info(f"Detecting advanced device context for session: {session_id}")
            
            # Parse user agent
            user_agent_string = request_data.get('user_agent', '')
            parsed_ua = parse(user_agent_string)
            
            # Extract basic device info
            device_type = self._detect_device_type(parsed_ua, request_data)
            screen_info = self._extract_screen_info(request_data)
            browser_info = self._extract_browser_info(parsed_ua)
            os_info = self._extract_os_info(parsed_ua)
            
            # Detect hardware capabilities
            hardware_caps = await self._detect_hardware_capabilities(request_data, session_id)
            
            # Analyze network conditions
            network_context = await self._analyze_network_conditions(request_data, session_id)
            
            # Determine device capability class
            device_capability = await self._classify_device_capability(
                device_type, hardware_caps, browser_info, os_info
            )
            
            # Detect interaction patterns
            interaction_pattern = await self._detect_interaction_pattern(session_id, request_data)
            
            # Calculate performance score
            performance_score = await self._calculate_performance_score(
                device_capability, network_context, hardware_caps
            )
            
            # Check for accessibility features
            accessibility_features = self._detect_accessibility_features(request_data)
            
            context = AdvancedDeviceContext(
                device_type=device_type,
                screen_size=screen_info['screen_size'],
                pixel_density=screen_info['pixel_density'],
                viewport_size=screen_info['viewport_size'],
                user_agent=user_agent_string,
                browser_engine=browser_info['engine'],
                browser_version=browser_info['version'],
                os_name=os_info['name'],
                os_version=os_info['version'],
                device_memory=hardware_caps.get('device_memory'),
                hardware_concurrency=hardware_caps.get('hardware_concurrency'),
                network_speed=network_context['speed'],
                connection_type=network_context['type'],
                touch_support=request_data.get('touch_support', device_type != DeviceType.DESKTOP),
                device_capability=device_capability,
                preferred_content_format=self._determine_content_format(device_capability, network_context),
                battery_level=request_data.get('battery_level'),
                data_saver_mode=request_data.get('data_saver_mode', False),
                accessibility_features=accessibility_features,
                interaction_pattern=interaction_pattern,
                performance_score=performance_score
            )
            
            # Cache device context for future requests
            await self._cache_device_context(session_id, context)
            
            logger.info(f"Advanced device context detected: {device_type.value}, capability: {device_capability.value}")
            return context
            
        except Exception as e:
            logger.error(f"Error detecting advanced device context: {str(e)}")
            return self._create_fallback_context(request_data)
    
    def _detect_device_type(self, parsed_ua: Any, request_data: Dict[str, Any]) -> DeviceType:
        """Enhanced device type detection"""
        # Check for explicit device indicators
        if request_data.get('is_mobile', False):
            return DeviceType.MOBILE
        if request_data.get('is_tablet', False):
            return DeviceType.TABLET
            
        # Analyze user agent
        if parsed_ua.is_mobile:
            # Further distinguish between mobile and tablet
            screen_width = request_data.get('screen_width', 0)
            if screen_width >= 768:  # iPad and large tablets
                return DeviceType.TABLET
            return DeviceType.MOBILE
        elif parsed_ua.is_tablet:
            return DeviceType.TABLET
        else:
            return DeviceType.DESKTOP
    
    def _extract_screen_info(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive screen information"""
        screen_width = request_data.get('screen_width', 1920)
        screen_height = request_data.get('screen_height', 1080)
        viewport_width = request_data.get('viewport_width', screen_width)
        viewport_height = request_data.get('viewport_height', screen_height)
        pixel_ratio = request_data.get('device_pixel_ratio', 1.0)
        
        return {
            'screen_size': (screen_width, screen_height),
            'viewport_size': (viewport_width, viewport_height),
            'pixel_density': pixel_ratio
        }
    
    def _extract_browser_info(self, parsed_ua: Any) -> Dict[str, str]:
        """Extract browser engine and version information"""
        browser_family = parsed_ua.browser.family.lower()
        browser_version = parsed_ua.browser.version_string
        
        # Map to engine
        engine_map = {
            'chrome': 'blink',
            'chromium': 'blink',
            'edge': 'blink',
            'opera': 'blink',
            'safari': 'webkit',
            'firefox': 'gecko',
            'ie': 'trident'
        }
        
        engine = engine_map.get(browser_family, 'unknown')
        
        return {
            'family': browser_family,
            'version': browser_version,
            'engine': engine
        }
    
    def _extract_os_info(self, parsed_ua: Any) -> Dict[str, str]:
        """Extract operating system information"""
        return {
            'name': parsed_ua.os.family.lower(),
            'version': parsed_ua.os.version_string
        }
    
    async def _detect_hardware_capabilities(self, request_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Detect hardware capabilities from client-side APIs"""
        capabilities = {}
        
        # Device memory (if available from navigator.deviceMemory)
        capabilities['device_memory'] = request_data.get('device_memory')
        
        # Hardware concurrency (CPU cores from navigator.hardwareConcurrency)
        capabilities['hardware_concurrency'] = request_data.get('hardware_concurrency')
        
        # GPU information (if available)
        capabilities['gpu_renderer'] = request_data.get('gpu_renderer')
        capabilities['gpu_vendor'] = request_data.get('gpu_vendor')
        
        # Storage estimates
        capabilities['storage_estimate'] = request_data.get('storage_estimate')
        
        # Connection information
        capabilities['connection_downlink'] = request_data.get('connection_downlink')
        capabilities['connection_effective_type'] = request_data.get('connection_effective_type')
        
        return capabilities
    
    async def _analyze_network_conditions(self, request_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Analyze network conditions and classify speed"""
        # Get connection info from Navigator.connection API
        effective_type = request_data.get('connection_effective_type', '4g')
        downlink = request_data.get('connection_downlink', 10.0)
        rtt = request_data.get('connection_rtt', 100)
        
        # Classify network speed
        if effective_type == 'slow-2g':
            speed = NetworkSpeed.CELLULAR_2G
        elif effective_type == '2g':
            speed = NetworkSpeed.CELLULAR_2G
        elif effective_type == '3g':
            speed = NetworkSpeed.CELLULAR_3G
        elif effective_type == '4g':
            if downlink >= 50:
                speed = NetworkSpeed.CELLULAR_5G
            else:
                speed = NetworkSpeed.CELLULAR_4G
        else:
            # Assume WiFi for unknown or fast connections
            if downlink >= 50:
                speed = NetworkSpeed.WIFI_FAST
            else:
                speed = NetworkSpeed.WIFI_SLOW
        
        return {
            'speed': speed,
            'type': effective_type,
            'downlink': downlink,
            'rtt': rtt
        }
    
    async def _classify_device_capability(self, device_type: DeviceType, hardware_caps: Dict[str, Any], 
                                        browser_info: Dict[str, str], os_info: Dict[str, str]) -> DeviceCapability:
        """Classify device into capability categories"""
        score = 0
        
        # Hardware scoring
        memory = hardware_caps.get('device_memory', 4)  # Default to 4GB
        if memory >= 8:
            score += 3
        elif memory >= 4:
            score += 2
        elif memory >= 2:
            score += 1
        
        cores = hardware_caps.get('hardware_concurrency', 4)  # Default to 4 cores
        if cores >= 8:
            score += 3
        elif cores >= 4:
            score += 2
        elif cores >= 2:
            score += 1
        
        # Device type factor
        if device_type == DeviceType.DESKTOP:
            score += 2
        elif device_type == DeviceType.TABLET:
            score += 1
        
        # Browser engine factor
        if browser_info['engine'] in ['blink', 'webkit']:
            score += 1
        
        # OS factor (newer versions generally more capable)
        if 'ios' in os_info['name'] and os_info['version'].startswith(('15', '16', '17')):
            score += 1
        elif 'android' in os_info['name'] and any(v in os_info['version'] for v in ['12', '13', '14']):
            score += 1
        elif 'windows' in os_info['name'] and '10' in os_info['version']:
            score += 1
        
        # Classify based on total score
        if score >= 8:
            return DeviceCapability.HIGH_PERFORMANCE
        elif score >= 5:
            return DeviceCapability.MEDIUM_PERFORMANCE
        elif score >= 2:
            return DeviceCapability.LOW_PERFORMANCE
        else:
            return DeviceCapability.ULTRA_LOW
    
    async def _detect_interaction_pattern(self, session_id: str, request_data: Dict[str, Any]) -> InteractionPattern:
        """Detect user interaction patterns from behavioral data"""
        try:
            # Get cached interaction data
            cache_key = f"interactions:{session_id}"
            interactions = await self.redis_client.get(cache_key)
            
            if not interactions:
                return InteractionPattern.METHODICAL_READER  # Default
            
            data = json.loads(interactions)
            
            # Analyze patterns
            avg_time_per_page = data.get('avg_time_per_page', 60)
            scroll_speed = data.get('scroll_speed', 1.0)
            click_frequency = data.get('click_frequency', 1.0)
            page_depth = data.get('page_depth', 1)
            comparison_views = data.get('comparison_views', 0)
            
            # Classification logic
            if avg_time_per_page < 30 and scroll_speed > 2.0:
                return InteractionPattern.QUICK_SCANNER
            elif comparison_views >= 3:
                return InteractionPattern.COMPARISON_SHOPPER
            elif avg_time_per_page > 120 and page_depth > 5:
                return InteractionPattern.RESEARCH_HEAVY
            elif click_frequency > 3.0 and avg_time_per_page < 60:
                return InteractionPattern.IMPULSE_BUYER
            else:
                return InteractionPattern.METHODICAL_READER
                
        except Exception as e:
            logger.error(f"Error detecting interaction pattern: {str(e)}")
            return InteractionPattern.METHODICAL_READER
    
    async def _calculate_performance_score(self, capability: DeviceCapability, 
                                         network: Dict[str, Any], hardware: Dict[str, Any]) -> float:
        """Calculate overall device performance score (0-1)"""
        score = 0.0
        
        # Device capability weight: 40%
        capability_scores = {
            DeviceCapability.HIGH_PERFORMANCE: 1.0,
            DeviceCapability.MEDIUM_PERFORMANCE: 0.7,
            DeviceCapability.LOW_PERFORMANCE: 0.4,
            DeviceCapability.ULTRA_LOW: 0.2
        }
        score += capability_scores[capability] * 0.4
        
        # Network speed weight: 30%
        network_scores = {
            NetworkSpeed.WIFI_FAST: 1.0,
            NetworkSpeed.WIFI_SLOW: 0.7,
            NetworkSpeed.CELLULAR_5G: 0.9,
            NetworkSpeed.CELLULAR_4G: 0.6,
            NetworkSpeed.CELLULAR_3G: 0.3,
            NetworkSpeed.CELLULAR_2G: 0.1
        }
        score += network_scores.get(network['speed'], 0.5) * 0.3
        
        # Hardware specifics weight: 30%
        memory_score = min(1.0, hardware.get('device_memory', 4) / 8.0)
        cores_score = min(1.0, hardware.get('hardware_concurrency', 4) / 8.0)
        score += (memory_score + cores_score) / 2 * 0.3
        
        return min(1.0, score)
    
    def _detect_accessibility_features(self, request_data: Dict[str, Any]) -> List[str]:
        """Detect enabled accessibility features"""
        features = []
        
        if request_data.get('prefers_reduced_motion', False):
            features.append('reduced_motion')
        if request_data.get('prefers_contrast', 'no-preference') != 'no-preference':
            features.append('high_contrast')
        if request_data.get('font_size_preference', 'normal') != 'normal':
            features.append('large_text')
        if request_data.get('screen_reader_detected', False):
            features.append('screen_reader')
        
        return features
    
    def _determine_content_format(self, capability: DeviceCapability, network: Dict[str, Any]) -> str:
        """Determine optimal content format based on device and network"""
        if capability == DeviceCapability.HIGH_PERFORMANCE and network['speed'] in [NetworkSpeed.WIFI_FAST, NetworkSpeed.CELLULAR_5G]:
            return 'rich_interactive'
        elif capability == DeviceCapability.MEDIUM_PERFORMANCE:
            return 'standard'
        elif network['speed'] in [NetworkSpeed.CELLULAR_2G, NetworkSpeed.CELLULAR_3G]:
            return 'minimal'
        else:
            return 'optimized'
    
    async def _cache_device_context(self, session_id: str, context: AdvancedDeviceContext):
        """Cache device context for performance"""
        try:
            cache_key = f"device_context:{session_id}"
            cache_data = {
                'device_type': context.device_type.value,
                'capability': context.device_capability.value,
                'network_speed': context.network_speed.value,
                'performance_score': context.performance_score,
                'interaction_pattern': context.interaction_pattern.value,
                'timestamp': datetime.utcnow().isoformat()
            }
            await self.redis_client.setex(cache_key, 3600, json.dumps(cache_data))  # Cache for 1 hour
        except Exception as e:
            logger.error(f"Error caching device context: {str(e)}")
    
    def _create_fallback_context(self, request_data: Dict[str, Any]) -> AdvancedDeviceContext:
        """Create fallback device context when detection fails"""
        return AdvancedDeviceContext(
            device_type=DeviceType.MOBILE,
            screen_size=(375, 667),
            pixel_density=2.0,
            viewport_size=(375, 667),
            user_agent=request_data.get('user_agent', ''),
            browser_engine='webkit',
            browser_version='unknown',
            os_name='unknown',
            os_version='unknown',
            device_memory=4,
            hardware_concurrency=4,
            network_speed=NetworkSpeed.CELLULAR_4G,
            connection_type='4g',
            touch_support=True,
            device_capability=DeviceCapability.MEDIUM_PERFORMANCE,
            preferred_content_format='standard',
            battery_level=None,
            data_saver_mode=False,
            accessibility_features=[],
            interaction_pattern=InteractionPattern.METHODICAL_READER,
            performance_score=0.6
        )
    
    def _load_mobile_performance_model(self) -> Dict[str, Any]:
        """Load mobile-specific performance benchmarks"""
        return {
            'viewport_thresholds': {
                'small': (0, 375),
                'medium': (376, 414),
                'large': (415, 500)
            },
            'memory_classes': {
                'low': (0, 2),
                'medium': (3, 4),
                'high': (5, 16)
            }
        }
    
    def _load_tablet_performance_model(self) -> Dict[str, Any]:
        """Load tablet-specific performance benchmarks"""
        return {
            'viewport_thresholds': {
                'small': (0, 768),
                'medium': (769, 1024),
                'large': (1025, 1366)
            },
            'memory_classes': {
                'low': (0, 3),
                'medium': (4, 6),
                'high': (7, 16)
            }
        }
    
    def _load_desktop_performance_model(self) -> Dict[str, Any]:
        """Load desktop-specific performance benchmarks"""
        return {
            'viewport_thresholds': {
                'small': (0, 1366),
                'medium': (1367, 1920),
                'large': (1921, 4096)
            },
            'memory_classes': {
                'low': (0, 4),
                'medium': (5, 8),
                'high': (9, 64)
            }
        }

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'AdvancedDeviceDetector',
    'AdvancedDeviceContext', 
    'ContentVariant',
    'DeviceCapability',
    'NetworkSpeed',
    'InteractionPattern'
]