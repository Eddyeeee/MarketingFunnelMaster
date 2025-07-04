# Device-Specific Content Variant Generator - Week 2 Implementation
# Module: 3A - Week 2 - Advanced Device-Specific Content Variants
# Created: 2025-07-04

import asyncio
import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from .device_detection_service import DeviceProfile, ContentCapabilities, UXOptimizations

logger = logging.getLogger(__name__)

# =============================================================================
# CONTENT VARIANT MODELS
# =============================================================================

@dataclass
class DeviceContentVariant:
    """Device-optimized content variant"""
    variant_id: str
    device_type: str
    content_type: str  # hero, cta, form, media, navigation
    content_data: Dict[str, Any]
    optimizations_applied: List[str]
    performance_score: Optional[float] = None
    conversion_impact: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'variant_id': self.variant_id,
            'device_type': self.device_type,
            'content_type': self.content_type,
            'content_data': self.content_data,
            'optimizations_applied': self.optimizations_applied,
            'performance_score': self.performance_score,
            'conversion_impact': self.conversion_impact
        }

@dataclass
class ContentOptimizationRule:
    """Rule for content optimization"""
    rule_id: str
    device_types: List[str]
    conditions: Dict[str, Any]
    transformations: Dict[str, Any]
    expected_impact: float
    priority: int
    
    def applies_to_device(self, device_profile: DeviceProfile) -> bool:
        """Check if rule applies to device"""
        if device_profile.device_type not in self.device_types:
            return False
        
        # Check conditions
        for condition, value in self.conditions.items():
            if condition == "screen_size" and device_profile.screen_size != value:
                return False
            elif condition == "performance_tier" and device_profile.performance_tier != value:
                return False
            elif condition == "orientation" and device_profile.orientation != value:
                return False
            elif condition == "touch_capable" and device_profile.touch_capable != value:
                return False
        
        return True

# =============================================================================
# DEVICE CONTENT VARIANT GENERATOR
# =============================================================================

class DeviceContentVariantGenerator:
    """Advanced content variant generator for device-specific optimization"""
    
    def __init__(self):
        self.optimization_rules = self._initialize_optimization_rules()
        self.content_templates = self._initialize_content_templates()
        self.performance_data = {}
        self.variant_cache = {}
        
    async def generate_device_variants(self, base_content: Dict[str, Any], 
                                     device_profile: DeviceProfile,
                                     content_capabilities: ContentCapabilities,
                                     ux_optimizations: UXOptimizations) -> List[DeviceContentVariant]:
        """Generate device-optimized content variants"""
        try:
            variants = []
            
            # Generate variants for different content types
            content_types = ['hero', 'cta', 'form', 'media', 'navigation']
            
            for content_type in content_types:
                variant = await self._generate_content_variant(
                    base_content, content_type, device_profile, 
                    content_capabilities, ux_optimizations
                )
                if variant:
                    variants.append(variant)
            
            # Apply cross-content optimizations
            optimized_variants = await self._apply_cross_content_optimizations(
                variants, device_profile, content_capabilities
            )
            
            # Score and rank variants
            scored_variants = await self._score_variants(optimized_variants, device_profile)
            
            logger.info(f"Generated {len(scored_variants)} device variants for {device_profile.device_type}")
            return scored_variants
            
        except Exception as e:
            logger.error(f"Error generating device variants: {str(e)}")
            return []
    
    async def _generate_content_variant(self, base_content: Dict[str, Any], 
                                      content_type: str,
                                      device_profile: DeviceProfile,
                                      content_capabilities: ContentCapabilities,
                                      ux_optimizations: UXOptimizations) -> Optional[DeviceContentVariant]:
        """Generate variant for specific content type"""
        try:
            # Get relevant optimization rules
            applicable_rules = [
                rule for rule in self.optimization_rules[content_type]
                if rule.applies_to_device(device_profile)
            ]
            
            if not applicable_rules:
                return None
            
            # Sort rules by priority and expected impact
            applicable_rules.sort(key=lambda r: (r.priority, r.expected_impact), reverse=True)
            
            # Apply transformations
            variant_content = base_content.copy()
            applied_optimizations = []
            
            for rule in applicable_rules:
                transformed_content, optimization_applied = await self._apply_transformation(
                    variant_content, rule, device_profile, content_capabilities, ux_optimizations
                )
                
                if optimization_applied:
                    variant_content = transformed_content
                    applied_optimizations.append(rule.rule_id)
            
            # Create variant
            variant = DeviceContentVariant(
                variant_id=f"{content_type}_{device_profile.device_type}_{datetime.utcnow().timestamp()}",
                device_type=device_profile.device_type,
                content_type=content_type,
                content_data=variant_content,
                optimizations_applied=applied_optimizations
            )
            
            return variant
            
        except Exception as e:
            logger.error(f"Error generating {content_type} variant: {str(e)}")
            return None
    
    async def _apply_transformation(self, content: Dict[str, Any], 
                                  rule: ContentOptimizationRule,
                                  device_profile: DeviceProfile,
                                  content_capabilities: ContentCapabilities,
                                  ux_optimizations: UXOptimizations) -> Tuple[Dict[str, Any], bool]:
        """Apply transformation rule to content"""
        try:
            transformed_content = content.copy()
            optimization_applied = False
            
            for transformation_type, transformation_data in rule.transformations.items():
                if transformation_type == "text_optimization":
                    transformed_content, applied = await self._apply_text_optimization(
                        transformed_content, transformation_data, device_profile
                    )
                    optimization_applied = optimization_applied or applied
                    
                elif transformation_type == "layout_optimization":
                    transformed_content, applied = await self._apply_layout_optimization(
                        transformed_content, transformation_data, device_profile, ux_optimizations
                    )
                    optimization_applied = optimization_applied or applied
                    
                elif transformation_type == "media_optimization":
                    transformed_content, applied = await self._apply_media_optimization(
                        transformed_content, transformation_data, device_profile, content_capabilities
                    )
                    optimization_applied = optimization_applied or applied
                    
                elif transformation_type == "interaction_optimization":
                    transformed_content, applied = await self._apply_interaction_optimization(
                        transformed_content, transformation_data, device_profile, ux_optimizations
                    )
                    optimization_applied = optimization_applied or applied
            
            return transformed_content, optimization_applied
            
        except Exception as e:
            logger.error(f"Error applying transformation: {str(e)}")
            return content, False
    
    async def _apply_text_optimization(self, content: Dict[str, Any], 
                                     transformation_data: Dict[str, Any],
                                     device_profile: DeviceProfile) -> Tuple[Dict[str, Any], bool]:
        """Apply text-specific optimizations"""
        optimized_content = content.copy()
        applied = False
        
        # Text length optimization
        if "max_length" in transformation_data:
            max_length = transformation_data["max_length"]
            
            for field in ["hero_message", "call_to_action", "description"]:
                if field in optimized_content and len(optimized_content[field]) > max_length:
                    original_text = optimized_content[field]
                    optimized_content[field] = await self._truncate_text_intelligently(
                        original_text, max_length
                    )
                    applied = True
        
        # Font size optimization
        if "font_size" in transformation_data:
            optimized_content["font_size"] = transformation_data["font_size"]
            applied = True
        
        # Reading level optimization
        if "reading_level" in transformation_data:
            target_level = transformation_data["reading_level"]
            
            for field in ["hero_message", "description"]:
                if field in optimized_content:
                    optimized_content[field] = await self._adjust_reading_level(
                        optimized_content[field], target_level
                    )
                    applied = True
        
        # Mobile-specific text optimizations
        if device_profile.device_type == "mobile":
            # Make CTAs more action-oriented
            if "call_to_action" in optimized_content:
                optimized_content["call_to_action"] = await self._optimize_mobile_cta(
                    optimized_content["call_to_action"]
                )
                applied = True
            
            # Add emoji for visual appeal on mobile
            if "add_emojis" in transformation_data and transformation_data["add_emojis"]:
                for field in ["hero_message", "call_to_action"]:
                    if field in optimized_content and not self._has_emojis(optimized_content[field]):
                        optimized_content[field] = await self._add_contextual_emojis(
                            optimized_content[field], field
                        )
                        applied = True
        
        return optimized_content, applied
    
    async def _apply_layout_optimization(self, content: Dict[str, Any], 
                                       transformation_data: Dict[str, Any],
                                       device_profile: DeviceProfile,
                                       ux_optimizations: UXOptimizations) -> Tuple[Dict[str, Any], bool]:
        """Apply layout-specific optimizations"""
        optimized_content = content.copy()
        applied = False
        
        # Layout structure optimization
        if "layout_structure" in transformation_data:
            optimized_content["layout"] = {
                "structure": transformation_data["layout_structure"],
                "device_type": device_profile.device_type,
                "orientation": device_profile.orientation
            }
            applied = True
        
        # Spacing optimization
        if "spacing" in transformation_data:
            spacing_config = transformation_data["spacing"]
            optimized_content["spacing"] = {
                "padding": spacing_config.get("padding", "normal"),
                "margin": spacing_config.get("margin", "normal"),
                "line_height": spacing_config.get("line_height", 1.5)
            }
            applied = True
        
        # Grid/column optimization
        if "columns" in transformation_data:
            column_count = transformation_data["columns"]
            if device_profile.device_type == "mobile":
                column_count = min(column_count, 1)  # Force single column on mobile
            elif device_profile.device_type == "tablet":
                column_count = min(column_count, 2)  # Max 2 columns on tablet
            
            optimized_content["layout_columns"] = column_count
            applied = True
        
        # Navigation optimization
        if "navigation" in transformation_data:
            nav_config = transformation_data["navigation"]
            optimized_content["navigation"] = {
                "type": ux_optimizations.navigation_type,
                "position": nav_config.get("position", "top"),
                "style": nav_config.get("style", "minimal")
            }
            applied = True
        
        return optimized_content, applied
    
    async def _apply_media_optimization(self, content: Dict[str, Any], 
                                      transformation_data: Dict[str, Any],
                                      device_profile: DeviceProfile,
                                      content_capabilities: ContentCapabilities) -> Tuple[Dict[str, Any], bool]:
        """Apply media-specific optimizations"""
        optimized_content = content.copy()
        applied = False
        
        # Image optimization
        if "images" in transformation_data and "images" in content:
            image_config = transformation_data["images"]
            optimized_images = []
            
            for image in content["images"]:
                optimized_image = image.copy()
                
                # Size optimization
                if content_capabilities.max_image_size:
                    optimized_image["max_size"] = content_capabilities.max_image_size
                
                # Format optimization
                if content_capabilities.supports_webp:
                    optimized_image["preferred_format"] = "webp"
                else:
                    optimized_image["preferred_format"] = "jpg"
                
                # Quality optimization based on device
                if device_profile.performance_tier == "low":
                    optimized_image["quality"] = "low"
                elif device_profile.performance_tier == "medium":
                    optimized_image["quality"] = "medium"
                else:
                    optimized_image["quality"] = "high"
                
                # Lazy loading optimization
                if device_profile.network_speed == "slow":
                    optimized_image["lazy_load"] = True
                
                optimized_images.append(optimized_image)
            
            optimized_content["images"] = optimized_images
            applied = True
        
        # Video optimization
        if "videos" in transformation_data and "videos" in content:
            video_config = transformation_data["videos"]
            optimized_videos = []
            
            for video in content["videos"]:
                optimized_video = video.copy()
                
                # Autoplay optimization
                if device_profile.device_type == "mobile":
                    optimized_video["autoplay"] = False  # Save battery and data
                    optimized_video["muted"] = True
                else:
                    optimized_video["autoplay"] = video_config.get("autoplay", False)
                
                # Quality optimization
                if device_profile.performance_tier == "low" or device_profile.network_speed == "slow":
                    optimized_video["max_resolution"] = "720p"
                elif device_profile.performance_tier == "medium":
                    optimized_video["max_resolution"] = "1080p"
                else:
                    optimized_video["max_resolution"] = "4K"
                
                # Controls optimization
                if device_profile.touch_capable:
                    optimized_video["controls"] = "touch_friendly"
                else:
                    optimized_video["controls"] = "standard"
                
                optimized_videos.append(optimized_video)
            
            optimized_content["videos"] = optimized_videos
            applied = True
        
        return optimized_content, applied
    
    async def _apply_interaction_optimization(self, content: Dict[str, Any], 
                                            transformation_data: Dict[str, Any],
                                            device_profile: DeviceProfile,
                                            ux_optimizations: UXOptimizations) -> Tuple[Dict[str, Any], bool]:
        """Apply interaction-specific optimizations"""
        optimized_content = content.copy()
        applied = False
        
        # Button optimization
        if "buttons" in transformation_data:
            button_config = transformation_data["buttons"]
            
            if "buttons" in content:
                optimized_buttons = []
                
                for button in content["buttons"]:
                    optimized_button = button.copy()
                    
                    # Size optimization based on device
                    if device_profile.touch_capable:
                        optimized_button["min_size"] = content_capabilities.touch_target_size
                        optimized_button["padding"] = "large"
                    else:
                        optimized_button["min_size"] = 32
                        optimized_button["padding"] = "normal"
                    
                    # Style optimization
                    if device_profile.device_type == "mobile":
                        optimized_button["style"] = "full_width"
                        optimized_button["corner_radius"] = "rounded"
                    else:
                        optimized_button["style"] = "auto_width"
                        optimized_button["corner_radius"] = "slightly_rounded"
                    
                    # Feedback optimization
                    if device_profile.touch_capable:
                        optimized_button["feedback"] = "haptic"
                    else:
                        optimized_button["feedback"] = "visual"
                    
                    optimized_buttons.append(optimized_button)
                
                optimized_content["buttons"] = optimized_buttons
                applied = True
        
        # Form optimization
        if "forms" in transformation_data and "forms" in content:
            form_config = transformation_data["forms"]
            
            for form in content["forms"]:
                optimized_form = form.copy()
                
                # Field layout optimization
                if device_profile.device_type == "mobile":
                    optimized_form["layout"] = "single_column"
                    optimized_form["fields_per_step"] = 2
                elif device_profile.device_type == "tablet":
                    optimized_form["layout"] = "two_column"
                    optimized_form["fields_per_step"] = 4
                else:
                    optimized_form["layout"] = "flexible"
                    optimized_form["fields_per_step"] = 6
                
                # Input optimization
                if device_profile.touch_capable:
                    optimized_form["input_height"] = "large"
                    optimized_form["keyboard_type"] = "adaptive"
                else:
                    optimized_form["input_height"] = "standard"
                    optimized_form["keyboard_type"] = "standard"
                
                # Validation optimization
                if device_profile.device_type == "mobile":
                    optimized_form["validation"] = "inline"
                else:
                    optimized_form["validation"] = "on_submit"
                
                optimized_content["forms"] = [optimized_form]
                applied = True
        
        return optimized_content, applied
    
    async def _apply_cross_content_optimizations(self, variants: List[DeviceContentVariant],
                                               device_profile: DeviceProfile,
                                               content_capabilities: ContentCapabilities) -> List[DeviceContentVariant]:
        """Apply optimizations across content types"""
        try:
            optimized_variants = []
            
            # Group variants by device type
            device_variants = {}
            for variant in variants:
                if variant.device_type not in device_variants:
                    device_variants[variant.device_type] = []
                device_variants[variant.device_type].append(variant)
            
            # Apply cross-content optimizations for each device type
            for device_type, type_variants in device_variants.items():
                # Ensure consistency across content types
                consistent_variants = await self._ensure_content_consistency(type_variants)
                
                # Apply performance optimizations
                performance_optimized = await self._apply_performance_optimizations(
                    consistent_variants, device_profile, content_capabilities
                )
                
                optimized_variants.extend(performance_optimized)
            
            return optimized_variants
            
        except Exception as e:
            logger.error(f"Error applying cross-content optimizations: {str(e)}")
            return variants
    
    async def _ensure_content_consistency(self, variants: List[DeviceContentVariant]) -> List[DeviceContentVariant]:
        """Ensure consistency across content variants"""
        if not variants:
            return variants
        
        # Extract common styling elements
        common_style = self._extract_common_style(variants)
        
        # Apply common style to all variants
        consistent_variants = []
        for variant in variants:
            consistent_variant = variant
            consistent_variant.content_data["common_style"] = common_style
            consistent_variants.append(consistent_variant)
        
        return consistent_variants
    
    def _extract_common_style(self, variants: List[DeviceContentVariant]) -> Dict[str, Any]:
        """Extract common styling elements from variants"""
        common_style = {
            "color_scheme": "primary",
            "typography": "consistent",
            "spacing": "uniform",
            "animation_style": "subtle"
        }
        
        # Analyze variants to extract actual common elements
        if variants:
            first_variant = variants[0]
            if "font_size" in first_variant.content_data:
                common_style["font_size"] = first_variant.content_data["font_size"]
        
        return common_style
    
    async def _apply_performance_optimizations(self, variants: List[DeviceContentVariant],
                                             device_profile: DeviceProfile,
                                             content_capabilities: ContentCapabilities) -> List[DeviceContentVariant]:
        """Apply performance-based optimizations"""
        optimized_variants = []
        
        for variant in variants:
            optimized_variant = variant
            
            # Performance tier-based optimizations
            if device_profile.performance_tier == "low":
                # Minimize resource usage
                optimized_variant.content_data["minimize_resources"] = True
                optimized_variant.content_data["disable_animations"] = True
                optimized_variant.optimizations_applied.append("low_performance_optimization")
            
            # Network speed optimizations
            if device_profile.network_speed == "slow":
                # Aggressive compression and lazy loading
                optimized_variant.content_data["aggressive_compression"] = True
                optimized_variant.content_data["lazy_load_everything"] = True
                optimized_variant.optimizations_applied.append("slow_network_optimization")
            
            optimized_variants.append(optimized_variant)
        
        return optimized_variants
    
    async def _score_variants(self, variants: List[DeviceContentVariant], 
                            device_profile: DeviceProfile) -> List[DeviceContentVariant]:
        """Score variants based on expected performance"""
        scored_variants = []
        
        for variant in variants:
            # Calculate performance score
            performance_score = await self._calculate_performance_score(variant, device_profile)
            
            # Calculate conversion impact
            conversion_impact = await self._calculate_conversion_impact(variant, device_profile)
            
            variant.performance_score = performance_score
            variant.conversion_impact = conversion_impact
            
            scored_variants.append(variant)
        
        # Sort by combined score
        scored_variants.sort(
            key=lambda v: (v.performance_score or 0) * 0.6 + (v.conversion_impact or 0) * 0.4,
            reverse=True
        )
        
        return scored_variants
    
    async def _calculate_performance_score(self, variant: DeviceContentVariant, 
                                         device_profile: DeviceProfile) -> float:
        """Calculate expected performance score for variant"""
        score = 0.5  # Base score
        
        # Device type compatibility
        if variant.device_type == device_profile.device_type:
            score += 0.2
        
        # Optimization alignment
        optimization_bonus = len(variant.optimizations_applied) * 0.05
        score += min(optimization_bonus, 0.3)
        
        # Performance tier considerations
        if device_profile.performance_tier == "low":
            if "low_performance_optimization" in variant.optimizations_applied:
                score += 0.15
        elif device_profile.performance_tier == "high":
            if "advanced_features" in variant.content_data:
                score += 0.1
        
        return max(0.0, min(1.0, score))
    
    async def _calculate_conversion_impact(self, variant: DeviceContentVariant, 
                                         device_profile: DeviceProfile) -> float:
        """Calculate expected conversion impact for variant"""
        impact = 0.5  # Base impact
        
        # Content type specific impacts
        if variant.content_type == "cta":
            if device_profile.device_type == "mobile":
                if "full_width" in str(variant.content_data):
                    impact += 0.15
        elif variant.content_type == "form":
            if device_profile.touch_capable:
                if "touch_friendly" in str(variant.content_data):
                    impact += 0.1
        
        # Device-specific optimizations
        if device_profile.device_type == "mobile":
            if "mobile_optimization" in variant.optimizations_applied:
                impact += 0.2
        
        return max(0.0, min(1.0, impact))
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    async def _truncate_text_intelligently(self, text: str, max_length: int) -> str:
        """Intelligently truncate text while preserving meaning"""
        if len(text) <= max_length:
            return text
        
        # Try to truncate at sentence boundaries
        sentences = text.split('.')
        result = ""
        
        for sentence in sentences:
            if len(result + sentence + ".") <= max_length:
                result += sentence + "."
            else:
                break
        
        if not result:
            # Fallback to word boundaries
            words = text.split()
            result = ""
            for word in words:
                if len(result + " " + word) <= max_length - 3:
                    result += " " + word if result else word
                else:
                    break
            result += "..."
        
        return result.strip()
    
    async def _adjust_reading_level(self, text: str, target_level: str) -> str:
        """Adjust text reading level"""
        if target_level == "simple":
            # Replace complex words with simpler alternatives
            replacements = {
                "utilize": "use",
                "demonstrate": "show",
                "facilitate": "help",
                "optimize": "improve",
                "implement": "start"
            }
            
            for complex_word, simple_word in replacements.items():
                text = text.replace(complex_word, simple_word)
        
        return text
    
    async def _optimize_mobile_cta(self, cta_text: str) -> str:
        """Optimize CTA text for mobile"""
        # Make more action-oriented and urgent
        if not any(word in cta_text.lower() for word in ["get", "start", "join", "buy", "try"]):
            cta_text = f"Get {cta_text}"
        
        # Add mobile-friendly elements
        if len(cta_text) > 20:
            cta_text = await self._truncate_text_intelligently(cta_text, 20)
        
        return cta_text
    
    def _has_emojis(self, text: str) -> bool:
        """Check if text contains emojis"""
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
        return bool(emoji_pattern.search(text))
    
    async def _add_contextual_emojis(self, text: str, field_type: str) -> str:
        """Add contextual emojis to text"""
        emoji_map = {
            "hero_message": ["🚀", "✨", "🔥", "💡"],
            "call_to_action": ["👉", "⚡", "🎯", "💎"]
        }
        
        emojis = emoji_map.get(field_type, ["✨"])
        selected_emoji = emojis[0]  # Simple selection logic
        
        return f"{selected_emoji} {text}"
    
    def _initialize_optimization_rules(self) -> Dict[str, List[ContentOptimizationRule]]:
        """Initialize content optimization rules"""
        rules = {
            "hero": [
                ContentOptimizationRule(
                    rule_id="mobile_hero_short",
                    device_types=["mobile"],
                    conditions={"screen_size": "small"},
                    transformations={
                        "text_optimization": {
                            "max_length": 60,
                            "add_emojis": True,
                            "reading_level": "simple"
                        }
                    },
                    expected_impact=0.15,
                    priority=1
                ),
                ContentOptimizationRule(
                    rule_id="desktop_hero_detailed",
                    device_types=["desktop"],
                    conditions={},
                    transformations={
                        "text_optimization": {
                            "max_length": 120,
                            "reading_level": "detailed"
                        }
                    },
                    expected_impact=0.10,
                    priority=2
                )
            ],
            "cta": [
                ContentOptimizationRule(
                    rule_id="mobile_cta_prominent",
                    device_types=["mobile"],
                    conditions={"touch_capable": True},
                    transformations={
                        "interaction_optimization": {
                            "buttons": {
                                "size": "large",
                                "style": "full_width",
                                "prominence": "high"
                            }
                        }
                    },
                    expected_impact=0.25,
                    priority=1
                ),
                ContentOptimizationRule(
                    rule_id="desktop_cta_hover",
                    device_types=["desktop"],
                    conditions={"touch_capable": False},
                    transformations={
                        "interaction_optimization": {
                            "buttons": {
                                "hover_effects": True,
                                "style": "auto_width"
                            }
                        }
                    },
                    expected_impact=0.12,
                    priority=2
                )
            ],
            "form": [
                ContentOptimizationRule(
                    rule_id="mobile_form_simple",
                    device_types=["mobile"],
                    conditions={},
                    transformations={
                        "interaction_optimization": {
                            "forms": {
                                "layout": "single_column",
                                "steps": "multi_step",
                                "fields_per_step": 2
                            }
                        }
                    },
                    expected_impact=0.20,
                    priority=1
                )
            ],
            "media": [
                ContentOptimizationRule(
                    rule_id="low_performance_media",
                    device_types=["mobile", "tablet", "desktop"],
                    conditions={"performance_tier": "low"},
                    transformations={
                        "media_optimization": {
                            "images": {
                                "quality": "low",
                                "lazy_load": True
                            },
                            "videos": {
                                "autoplay": False,
                                "max_resolution": "720p"
                            }
                        }
                    },
                    expected_impact=0.18,
                    priority=1
                )
            ],
            "navigation": [
                ContentOptimizationRule(
                    rule_id="mobile_navigation_hamburger",
                    device_types=["mobile"],
                    conditions={"screen_size": "small"},
                    transformations={
                        "layout_optimization": {
                            "navigation": {
                                "type": "hamburger",
                                "position": "top",
                                "style": "minimal"
                            }
                        }
                    },
                    expected_impact=0.08,
                    priority=1
                )
            ]
        }
        
        return rules
    
    def _initialize_content_templates(self) -> Dict[str, Any]:
        """Initialize content templates for different devices"""
        return {
            "mobile": {
                "hero": {
                    "structure": "vertical",
                    "text_alignment": "center",
                    "image_position": "top"
                },
                "cta": {
                    "width": "full",
                    "position": "bottom_sticky",
                    "style": "primary"
                }
            },
            "tablet": {
                "hero": {
                    "structure": "horizontal",
                    "text_alignment": "left",
                    "image_position": "right"
                },
                "cta": {
                    "width": "auto",
                    "position": "inline",
                    "style": "prominent"
                }
            },
            "desktop": {
                "hero": {
                    "structure": "grid",
                    "text_alignment": "left",
                    "image_position": "right"
                },
                "cta": {
                    "width": "auto",
                    "position": "inline",
                    "style": "standard"
                }
            }
        }

# =============================================================================
# SERVICE INITIALIZATION
# =============================================================================

# Global service instance
device_content_variant_generator = DeviceContentVariantGenerator()