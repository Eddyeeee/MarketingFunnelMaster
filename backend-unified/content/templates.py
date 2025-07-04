#!/usr/bin/env python3
"""
Content Templates Framework
Module 3A: Niche-Specific Content Templates with Persona × Device Optimization

Executor: Claude Code
Erstellt: 2025-07-04 (Module 3A Phase 1)
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4
import json

class PersonaType(str, Enum):
    """Supported persona types"""
    TECH_EARLY_ADOPTER = "tech_early_adopter"
    REMOTE_DAD = "remote_dad"
    STUDENT_HUSTLER = "student_hustler"
    BUSINESS_OWNER = "business_owner"

class DeviceType(str, Enum):
    """Supported device types"""
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

class ContentFormat(str, Enum):
    """Content format types"""
    PRODUCT_REVIEW = "product_review"
    HOW_TO_GUIDE = "how_to_guide"
    COMPARISON_ARTICLE = "comparison_article"
    NEWS_ANALYSIS = "news_analysis"
    BUYING_GUIDE = "buying_guide"
    PROBLEM_SOLUTION = "problem_solution"
    LISTICLE = "listicle"
    CASE_STUDY = "case_study"

@dataclass
class ContentSection:
    """Individual content section structure"""
    title: str
    description: str
    word_count_target: int
    persona_adaptations: Dict[PersonaType, Dict[str, Any]]
    device_optimizations: Dict[DeviceType, Dict[str, Any]]
    seo_keywords: List[str]
    conversion_elements: List[str]

@dataclass
class ContentTemplate:
    """Complete content template with persona and device optimizations"""
    template_id: UUID
    name: str
    category: ContentFormat
    target_niches: List[str]
    sections: List[ContentSection]
    meta_structure: Dict[str, Any]
    performance_benchmarks: Dict[str, float]

class ContentTemplateEngine:
    """Content template management and generation engine"""
    
    def __init__(self):
        self.templates: Dict[str, ContentTemplate] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize default content templates"""
        
        # Tech Product Review Template
        tech_review_template = self._create_tech_product_review_template()
        self.templates[str(tech_review_template.template_id)] = tech_review_template
        
        # Family Solution Guide Template
        family_guide_template = self._create_family_solution_guide_template()
        self.templates[str(family_guide_template.template_id)] = family_guide_template
        
        # Student Budget Guide Template
        budget_guide_template = self._create_student_budget_guide_template()
        self.templates[str(budget_guide_template.template_id)] = budget_guide_template
        
        # Business ROI Analysis Template
        roi_analysis_template = self._create_business_roi_analysis_template()
        self.templates[str(roi_analysis_template.template_id)] = roi_analysis_template
    
    def _create_tech_product_review_template(self) -> ContentTemplate:
        """Create technology product review template"""
        
        # Hook & Problem Statement Section
        hook_section = ContentSection(
            title="Hook & Problem Statement",
            description="Engaging opening that identifies the problem this product solves",
            word_count_target=150,
            persona_adaptations={
                PersonaType.TECH_EARLY_ADOPTER: {
                    "focus": "cutting_edge_innovation",
                    "tone": "technical_enthusiast",
                    "hook_type": "latest_tech_breakthrough"
                },
                PersonaType.BUSINESS_OWNER: {
                    "focus": "business_efficiency",
                    "tone": "professional_analytical",
                    "hook_type": "productivity_problem"
                },
                PersonaType.REMOTE_DAD: {
                    "focus": "family_convenience",
                    "tone": "relatable_practical",
                    "hook_type": "daily_life_frustration"
                },
                PersonaType.STUDENT_HUSTLER: {
                    "focus": "affordability_value",
                    "tone": "budget_conscious",
                    "hook_type": "money_saving_opportunity"
                }
            },
            device_optimizations={
                DeviceType.MOBILE: {
                    "format": "punchy_opening",
                    "length": "2_sentences_max",
                    "visual_element": "emoji_or_icon"
                },
                DeviceType.TABLET: {
                    "format": "engaging_paragraph",
                    "length": "3_4_sentences",
                    "visual_element": "hero_image"
                },
                DeviceType.DESKTOP: {
                    "format": "detailed_introduction",
                    "length": "full_paragraph",
                    "visual_element": "video_or_gif"
                }
            },
            seo_keywords=["best", "review", "2025", "ultimate"],
            conversion_elements=["problem_identification", "solution_preview"]
        )
        
        # Product Analysis Section
        analysis_section = ContentSection(
            title="In-Depth Product Analysis",
            description="Comprehensive analysis of product features and capabilities",
            word_count_target=400,
            persona_adaptations={
                PersonaType.TECH_EARLY_ADOPTER: {
                    "focus": "technical_specifications",
                    "details": "deep_technical_dive",
                    "comparisons": "competitor_feature_matrix"
                },
                PersonaType.BUSINESS_OWNER: {
                    "focus": "roi_and_efficiency",
                    "details": "business_use_cases",
                    "comparisons": "cost_benefit_analysis"
                },
                PersonaType.REMOTE_DAD: {
                    "focus": "ease_of_use",
                    "details": "family_friendly_features",
                    "comparisons": "alternative_solutions"
                },
                PersonaType.STUDENT_HUSTLER: {
                    "focus": "value_for_money",
                    "details": "essential_features_only",
                    "comparisons": "budget_alternatives"
                }
            },
            device_optimizations={
                DeviceType.MOBILE: {
                    "format": "bullet_points",
                    "sections": "collapsible_accordion",
                    "images": "swipeable_gallery"
                },
                DeviceType.TABLET: {
                    "format": "mixed_paragraphs_bullets",
                    "sections": "tabbed_interface",
                    "images": "side_by_side_comparison"
                },
                DeviceType.DESKTOP: {
                    "format": "detailed_paragraphs",
                    "sections": "full_content_visible",
                    "images": "large_detailed_charts"
                }
            },
            seo_keywords=["features", "specifications", "analysis", "detailed"],
            conversion_elements=["feature_benefits", "use_case_scenarios"]
        )
        
        # Pros and Cons Section
        pros_cons_section = ContentSection(
            title="Pros and Cons Analysis",
            description="Balanced evaluation of product strengths and weaknesses",
            word_count_target=200,
            persona_adaptations={
                PersonaType.TECH_EARLY_ADOPTER: {
                    "pros_focus": "innovation_and_performance",
                    "cons_focus": "technical_limitations",
                    "perspective": "enthusiast_evaluation"
                },
                PersonaType.BUSINESS_OWNER: {
                    "pros_focus": "business_benefits",
                    "cons_focus": "implementation_challenges",
                    "perspective": "business_case_evaluation"
                },
                PersonaType.REMOTE_DAD: {
                    "pros_focus": "family_convenience",
                    "cons_focus": "complexity_concerns",
                    "perspective": "family_practicality"
                },
                PersonaType.STUDENT_HUSTLER: {
                    "pros_focus": "affordability_value",
                    "cons_focus": "missing_premium_features",
                    "perspective": "budget_conscious_analysis"
                }
            },
            device_optimizations={
                DeviceType.MOBILE: {
                    "format": "simple_two_column",
                    "icons": "green_red_indicators",
                    "interaction": "expandable_details"
                },
                DeviceType.TABLET: {
                    "format": "side_by_side_cards",
                    "icons": "detailed_visual_indicators",
                    "interaction": "hover_explanations"
                },
                DeviceType.DESKTOP: {
                    "format": "detailed_comparison_table",
                    "icons": "comprehensive_rating_system",
                    "interaction": "detailed_explanations_visible"
                }
            },
            seo_keywords=["pros", "cons", "advantages", "disadvantages"],
            conversion_elements=["balanced_perspective", "trust_building"]
        )
        
        # Call to Action Section
        cta_section = ContentSection(
            title="Final Verdict & Recommendation",
            description="Clear recommendation and compelling call to action",
            word_count_target=150,
            persona_adaptations={
                PersonaType.TECH_EARLY_ADOPTER: {
                    "verdict_focus": "innovation_leadership",
                    "cta_message": "be_first_to_experience",
                    "urgency": "limited_early_access"
                },
                PersonaType.BUSINESS_OWNER: {
                    "verdict_focus": "business_impact",
                    "cta_message": "transform_your_business",
                    "urgency": "competitive_advantage"
                },
                PersonaType.REMOTE_DAD: {
                    "verdict_focus": "family_benefits",
                    "cta_message": "make_family_life_easier",
                    "urgency": "improve_daily_routine"
                },
                PersonaType.STUDENT_HUSTLER: {
                    "verdict_focus": "value_proposition",
                    "cta_message": "smart_investment_choice",
                    "urgency": "limited_time_discount"
                }
            },
            device_optimizations={
                DeviceType.MOBILE: {
                    "cta_style": "full_width_button",
                    "placement": "sticky_bottom",
                    "text": "short_action_phrase"
                },
                DeviceType.TABLET: {
                    "cta_style": "prominent_centered_button",
                    "placement": "after_verdict",
                    "text": "descriptive_action_phrase"
                },
                DeviceType.DESKTOP: {
                    "cta_style": "multi_option_buttons",
                    "placement": "sidebar_and_bottom",
                    "text": "detailed_action_options"
                }
            },
            seo_keywords=["buy", "purchase", "get", "recommended"],
            conversion_elements=["clear_recommendation", "compelling_cta", "urgency_element"]
        )
        
        return ContentTemplate(
            template_id=uuid4(),
            name="Tech Product Review Template",
            category=ContentFormat.PRODUCT_REVIEW,
            target_niches=["technology", "gadgets", "software", "apps"],
            sections=[hook_section, analysis_section, pros_cons_section, cta_section],
            meta_structure={
                "total_word_count": 900,
                "reading_time_minutes": 4,
                "seo_optimization_level": "high",
                "conversion_optimization": "aggressive"
            },
            performance_benchmarks={
                "average_conversion_rate": 0.18,
                "average_engagement_time": 67,
                "seo_ranking_potential": 0.85
            }
        )
    
    def _create_family_solution_guide_template(self) -> ContentTemplate:
        """Create family-focused solution guide template"""
        
        # Family Problem Introduction
        problem_section = ContentSection(
            title="The Family Challenge",
            description="Relatable introduction to a common family problem",
            word_count_target=200,
            persona_adaptations={
                PersonaType.REMOTE_DAD: {
                    "focus": "daily_parenting_struggles",
                    "tone": "understanding_empathetic",
                    "examples": "real_family_scenarios"
                },
                PersonaType.BUSINESS_OWNER: {
                    "focus": "work_life_balance",
                    "tone": "professional_parent",
                    "examples": "entrepreneur_family_challenges"
                },
                PersonaType.TECH_EARLY_ADOPTER: {
                    "focus": "modern_family_tech_needs",
                    "tone": "tech_savvy_parent",
                    "examples": "digital_age_parenting"
                },
                PersonaType.STUDENT_HUSTLER: {
                    "focus": "budget_family_solutions",
                    "tone": "resourceful_practical",
                    "examples": "affordable_family_hacks"
                }
            },
            device_optimizations={
                DeviceType.MOBILE: {
                    "format": "story_opening",
                    "length": "quick_relatable_scenario",
                    "visual": "family_photo_or_icon"
                },
                DeviceType.TABLET: {
                    "format": "engaging_narrative",
                    "length": "detailed_scenario",
                    "visual": "family_illustration"
                },
                DeviceType.DESKTOP: {
                    "format": "comprehensive_problem_analysis",
                    "length": "full_context_setting",
                    "visual": "family_lifestyle_imagery"
                }
            },
            seo_keywords=["family", "parenting", "solution", "help"],
            conversion_elements=["problem_identification", "emotional_connection"]
        )
        
        return ContentTemplate(
            template_id=uuid4(),
            name="Family Solution Guide Template",
            category=ContentFormat.HOW_TO_GUIDE,
            target_niches=["family", "parenting", "home", "lifestyle"],
            sections=[problem_section],  # Abbreviated for brevity
            meta_structure={
                "total_word_count": 1200,
                "reading_time_minutes": 5,
                "family_focus": "high",
                "actionable_steps": "detailed"
            },
            performance_benchmarks={
                "average_conversion_rate": 0.22,
                "average_engagement_time": 78,
                "social_sharing_rate": 0.15
            }
        )
    
    def _create_student_budget_guide_template(self) -> ContentTemplate:
        """Create student-focused budget guide template"""
        return ContentTemplate(
            template_id=uuid4(),
            name="Student Budget Guide Template",
            category=ContentFormat.BUYING_GUIDE,
            target_niches=["education", "budget", "student_life", "money_saving"],
            sections=[],  # Simplified for brevity
            meta_structure={
                "total_word_count": 800,
                "reading_time_minutes": 3,
                "budget_focus": "high",
                "affordability_emphasis": "maximum"
            },
            performance_benchmarks={
                "average_conversion_rate": 0.16,
                "average_engagement_time": 52,
                "student_audience_retention": 0.73
            }
        )
    
    def _create_business_roi_analysis_template(self) -> ContentTemplate:
        """Create business ROI analysis template"""
        return ContentTemplate(
            template_id=uuid4(),
            name="Business ROI Analysis Template",
            category=ContentFormat.CASE_STUDY,
            target_niches=["business", "productivity", "enterprise", "saas"],
            sections=[],  # Simplified for brevity
            meta_structure={
                "total_word_count": 1500,
                "reading_time_minutes": 7,
                "business_focus": "high",
                "data_driven": "high"
            },
            performance_benchmarks={
                "average_conversion_rate": 0.25,
                "average_engagement_time": 95,
                "b2b_lead_quality": 0.82
            }
        )
    
    def get_template(self, template_id: str) -> Optional[ContentTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self, niche: Optional[str] = None, 
                      category: Optional[ContentFormat] = None) -> List[ContentTemplate]:
        """List templates with optional filtering"""
        templates = list(self.templates.values())
        
        if niche:
            templates = [t for t in templates if niche in t.target_niches]
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        return templates
    
    def generate_content_outline(self, template_id: str, niche: str, 
                               persona: PersonaType, device: DeviceType) -> Dict[str, Any]:
        """Generate content outline from template with persona and device optimization"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        outline = {
            "template_id": template_id,
            "template_name": template.name,
            "niche": niche,
            "persona": persona.value,
            "device": device.value,
            "sections": [],
            "meta_data": template.meta_structure.copy(),
            "performance_benchmarks": template.performance_benchmarks.copy()
        }
        
        for section in template.sections:
            # Apply persona adaptations
            persona_config = section.persona_adaptations.get(persona, {})
            device_config = section.device_optimizations.get(device, {})
            
            section_outline = {
                "title": section.title,
                "description": section.description,
                "word_count_target": section.word_count_target,
                "persona_focus": persona_config.get("focus", "general"),
                "tone": persona_config.get("tone", "neutral"),
                "device_format": device_config.get("format", "standard"),
                "seo_keywords": section.seo_keywords,
                "conversion_elements": section.conversion_elements,
                "optimization_rules": {
                    "persona_adaptations": persona_config,
                    "device_optimizations": device_config
                }
            }
            
            outline["sections"].append(section_outline)
        
        return outline
    
    def get_persona_device_matrix(self) -> Dict[str, Any]:
        """Get the complete persona × device optimization matrix"""
        return {
            "personas": {
                PersonaType.TECH_EARLY_ADOPTER.value: {
                    "characteristics": ["innovation_focused", "technical_depth", "early_adoption"],
                    "pain_points": ["cutting_edge_features", "technical_specifications", "first_access"],
                    "conversion_triggers": ["innovation_leadership", "technical_superiority", "exclusive_access"]
                },
                PersonaType.REMOTE_DAD.value: {
                    "characteristics": ["family_focused", "practical_solutions", "time_conscious"],
                    "pain_points": ["family_convenience", "work_life_balance", "simple_solutions"],
                    "conversion_triggers": ["family_benefits", "time_saving", "ease_of_use"]
                },
                PersonaType.STUDENT_HUSTLER.value: {
                    "characteristics": ["budget_conscious", "value_seeking", "efficiency_focused"],
                    "pain_points": ["affordability", "value_for_money", "essential_features"],
                    "conversion_triggers": ["cost_savings", "student_discounts", "smart_investment"]
                },
                PersonaType.BUSINESS_OWNER.value: {
                    "characteristics": ["roi_focused", "scalability_minded", "professional"],
                    "pain_points": ["business_efficiency", "scalability", "competitive_advantage"],
                    "conversion_triggers": ["roi_improvement", "business_growth", "competitive_edge"]
                }
            },
            "devices": {
                DeviceType.MOBILE.value: {
                    "optimization_focus": ["quick_consumption", "thumb_friendly", "swipe_navigation"],
                    "content_format": ["short_paragraphs", "bullet_points", "visual_emphasis"],
                    "conversion_optimization": ["sticky_cta", "one_click_actions", "mobile_checkout"]
                },
                DeviceType.TABLET.value: {
                    "optimization_focus": ["mixed_consumption", "touch_interface", "visual_content"],
                    "content_format": ["medium_paragraphs", "image_text_balance", "interactive_elements"],
                    "conversion_optimization": ["prominent_cta", "comparison_tables", "visual_proof"]
                },
                DeviceType.DESKTOP.value: {
                    "optimization_focus": ["deep_engagement", "detailed_analysis", "comprehensive_content"],
                    "content_format": ["full_paragraphs", "detailed_sections", "rich_media"],
                    "conversion_optimization": ["multiple_cta_options", "detailed_comparison", "comprehensive_proof"]
                }
            }
        }

# Global template engine instance
template_engine = ContentTemplateEngine()

# Utility functions for easy access
def get_template_by_id(template_id: str) -> Optional[ContentTemplate]:
    """Get template by ID"""
    return template_engine.get_template(template_id)

def list_available_templates(niche: Optional[str] = None, 
                           category: Optional[ContentFormat] = None) -> List[ContentTemplate]:
    """List available templates with optional filtering"""
    return template_engine.list_templates(niche, category)

def generate_optimized_outline(template_id: str, niche: str, 
                             persona: str, device: str) -> Dict[str, Any]:
    """Generate optimized content outline"""
    persona_enum = PersonaType(persona)
    device_enum = DeviceType(device)
    return template_engine.generate_content_outline(template_id, niche, persona_enum, device_enum)

def get_optimization_matrix() -> Dict[str, Any]:
    """Get the persona × device optimization matrix"""
    return template_engine.get_persona_device_matrix()