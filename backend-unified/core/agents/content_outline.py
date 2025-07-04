#!/usr/bin/env python3
"""
ContentOutlineAgent - AI-Powered Content Structure Generation
Module 3A: Phase 2 Implementation

Executor: Claude Code
Erstellt: 2025-07-04
Version: 1.0
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import json

logger = logging.getLogger(__name__)

@dataclass
class PersonaProfile:
    """User persona characteristics for content targeting"""
    name: str
    pain_points: List[str]
    goals: List[str]
    content_preferences: List[str]
    attention_span: int  # seconds
    decision_style: str  # analytical, emotional, social_proof
    tech_savviness: str  # low, medium, high

@dataclass
class DeviceOptimization:
    """Device-specific content optimization settings"""
    device_type: str  # mobile, tablet, desktop
    reading_pattern: str  # scanning, linear, deep_dive
    optimal_section_length: int  # words
    visual_ratio: float  # text to visual content ratio
    cta_frequency: int  # calls to action per section

@dataclass
class SEOStrategy:
    """SEO optimization parameters"""
    primary_keyword: str
    secondary_keywords: List[str]
    search_intent: str  # informational, commercial, transactional
    target_length: int  # words
    readability_target: float  # Flesch reading score
    semantic_keywords: List[str]

class ContentOutline(BaseModel):
    """Content outline structure"""
    title: str
    meta_description: str
    sections: List[Dict[str, Any]]
    seo_strategy: Dict[str, Any]
    persona_targeting: Dict[str, Any]
    device_optimization: Dict[str, Any]
    estimated_reading_time: int
    conversion_elements: List[str]
    quality_score: float = Field(default=0.0)

class ContentOutlineAgent:
    """AI agent for generating optimized content outlines"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.persona_database = self._load_persona_database()
        self.seo_templates = self._load_seo_templates()
        self.device_profiles = self._load_device_profiles()
        self.performance_metrics = {}
        
    def _load_persona_database(self) -> Dict[str, PersonaProfile]:
        """Load predefined persona profiles"""
        return {
            "TechEarlyAdopter": PersonaProfile(
                name="Tech Early Adopter",
                pain_points=["outdated_tech", "inefficiency", "missing_features"],
                goals=["cutting_edge_solutions", "productivity_gains", "innovation"],
                content_preferences=["technical_details", "comparisons", "specs"],
                attention_span=45,
                decision_style="analytical",
                tech_savviness="high"
            ),
            "RemoteDad": PersonaProfile(
                name="Remote Working Dad",
                pain_points=["work_life_balance", "family_time", "home_office_setup"],
                goals=["efficiency", "family_focus", "income_stability"],
                content_preferences=["practical_tips", "family_benefits", "time_saving"],
                attention_span=30,
                decision_style="emotional",
                tech_savviness="medium"
            ),
            "StudentHustler": PersonaProfile(
                name="Student Side Hustler",
                pain_points=["limited_budget", "time_constraints", "learning_curve"],
                goals=["affordable_solutions", "quick_results", "skill_building"],
                content_preferences=["step_by_step", "budget_friendly", "growth_hacks"],
                attention_span=20,
                decision_style="social_proof",
                tech_savviness="high"
            ),
            "BusinessOwner": PersonaProfile(
                name="Small Business Owner",
                pain_points=["scaling_challenges", "resource_limitations", "competition"],
                goals=["business_growth", "roi_maximization", "automation"],
                content_preferences=["case_studies", "roi_analysis", "implementation"],
                attention_span=60,
                decision_style="analytical",
                tech_savviness="medium"
            )
        }
    
    def _load_seo_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load SEO optimization templates"""
        return {
            "informational": {
                "title_pattern": "Ultimate Guide to {keyword} - {year} Edition",
                "meta_pattern": "Discover everything about {keyword}. Complete guide with {benefits}. Read now!",
                "structure": ["introduction", "what_is", "benefits", "how_to", "examples", "conclusion"],
                "keyword_density": 0.012,
                "readability_target": 65.0
            },
            "commercial": {
                "title_pattern": "Best {keyword} Solutions - Reviewed & Compared {year}",
                "meta_pattern": "Find the best {keyword} for your needs. Compare features, prices & reviews.",
                "structure": ["problem", "solution_overview", "comparison", "recommendation", "cta"],
                "keyword_density": 0.015,
                "readability_target": 70.0
            },
            "transactional": {
                "title_pattern": "{keyword} - Get Started Today | {brand}",
                "meta_pattern": "Start with {keyword} today. {benefit_1}, {benefit_2}, {benefit_3}. Try now!",
                "structure": ["hook", "problem", "solution", "benefits", "proof", "cta"],
                "keyword_density": 0.018,
                "readability_target": 75.0
            }
        }
    
    def _load_device_profiles(self) -> Dict[str, DeviceOptimization]:
        """Load device-specific optimization profiles"""
        return {
            "mobile": DeviceOptimization(
                device_type="mobile",
                reading_pattern="scanning",
                optimal_section_length=100,
                visual_ratio=0.4,
                cta_frequency=3
            ),
            "tablet": DeviceOptimization(
                device_type="tablet",
                reading_pattern="linear",
                optimal_section_length=200,
                visual_ratio=0.3,
                cta_frequency=2
            ),
            "desktop": DeviceOptimization(
                device_type="desktop",
                reading_pattern="deep_dive",
                optimal_section_length=300,
                visual_ratio=0.2,
                cta_frequency=1
            )
        }
    
    async def generate_outline(self, niche: str, persona: str, device: str, 
                             content_type: str, additional_context: Optional[Dict] = None) -> ContentOutline:
        """Generate optimized content outline"""
        start_time = datetime.now()
        
        try:
            # Get persona and device profiles
            persona_profile = self.persona_database.get(persona)
            device_profile = self.device_profiles.get(device)
            
            if not persona_profile or not device_profile:
                raise ValueError(f"Invalid persona ({persona}) or device ({device})")
            
            # Generate SEO strategy
            seo_strategy = await self._create_seo_strategy(niche, content_type, additional_context)
            
            # Create persona-specific sections
            sections = await self._create_content_sections(
                niche, persona_profile, device_profile, seo_strategy, content_type
            )
            
            # Generate title and meta description
            title = await self._generate_title(niche, persona_profile, seo_strategy)
            meta_description = await self._generate_meta_description(title, seo_strategy)
            
            # Calculate reading time and conversion elements
            estimated_reading_time = self._calculate_reading_time(sections, device_profile)
            conversion_elements = self._identify_conversion_elements(persona_profile, device_profile)
            
            # Create outline
            outline = ContentOutline(
                title=title,
                meta_description=meta_description,
                sections=sections,
                seo_strategy=seo_strategy,
                persona_targeting={
                    "persona": persona,
                    "pain_points": persona_profile.pain_points,
                    "goals": persona_profile.goals,
                    "decision_style": persona_profile.decision_style
                },
                device_optimization={
                    "device": device,
                    "reading_pattern": device_profile.reading_pattern,
                    "optimal_length": device_profile.optimal_section_length,
                    "visual_ratio": device_profile.visual_ratio
                },
                estimated_reading_time=estimated_reading_time,
                conversion_elements=conversion_elements
            )
            
            # Calculate quality score
            outline.quality_score = await self._calculate_quality_score(outline)
            
            # Update performance metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            await self._update_metrics(execution_time, outline.quality_score)
            
            logger.info(f"Generated outline for {niche}/{persona}/{device} in {execution_time:.2f}s")
            return outline
            
        except Exception as e:
            logger.error(f"Outline generation failed: {e}")
            raise
    
    async def _create_seo_strategy(self, niche: str, content_type: str, 
                                 context: Optional[Dict]) -> Dict[str, Any]:
        """Create SEO optimization strategy"""
        # Determine search intent
        intent_mapping = {
            "guide": "informational",
            "review": "commercial", 
            "landing": "transactional",
            "comparison": "commercial",
            "tutorial": "informational"
        }
        
        search_intent = intent_mapping.get(content_type, "informational")
        template = self.seo_templates[search_intent]
        
        # Generate keywords
        primary_keyword = f"{niche} {content_type}"
        secondary_keywords = [
            f"best {niche}",
            f"{niche} guide",
            f"how to {niche}",
            f"{niche} tips",
            f"{niche} benefits"
        ]
        
        semantic_keywords = await self._generate_semantic_keywords(niche, search_intent)
        
        return {
            "primary_keyword": primary_keyword,
            "secondary_keywords": secondary_keywords,
            "semantic_keywords": semantic_keywords,
            "search_intent": search_intent,
            "target_length": context.get("target_length", 1200) if context else 1200,
            "keyword_density": template["keyword_density"],
            "readability_target": template["readability_target"],
            "template": template
        }
    
    async def _generate_semantic_keywords(self, niche: str, intent: str) -> List[str]:
        """Generate semantic keywords for better SEO"""
        # Simulated semantic keyword generation
        base_keywords = {
            "smart_ring": ["wearable", "fitness_tracker", "health_monitor", "biometric"],
            "ai_tools": ["automation", "productivity", "efficiency", "workflow"],
            "productivity": ["time_management", "organization", "efficiency", "workflow"],
            "fitness": ["health", "wellness", "exercise", "training"],
            "business": ["entrepreneurship", "growth", "strategy", "success"]
        }
        
        return base_keywords.get(niche.lower(), [])
    
    async def _create_content_sections(self, niche: str, persona: PersonaProfile, 
                                     device: DeviceOptimization, seo_strategy: Dict,
                                     content_type: str) -> List[Dict[str, Any]]:
        """Create optimized content sections"""
        template_structure = seo_strategy["template"]["structure"]
        sections = []
        
        section_mapping = {
            "introduction": self._create_intro_section,
            "hook": self._create_hook_section,
            "problem": self._create_problem_section,
            "what_is": self._create_explanation_section,
            "solution": self._create_solution_section,
            "benefits": self._create_benefits_section,
            "how_to": self._create_howto_section,
            "comparison": self._create_comparison_section,
            "examples": self._create_examples_section,
            "proof": self._create_proof_section,
            "recommendation": self._create_recommendation_section,
            "cta": self._create_cta_section,
            "conclusion": self._create_conclusion_section
        }
        
        for i, section_type in enumerate(template_structure):
            if section_type in section_mapping:
                section = await section_mapping[section_type](
                    niche, persona, device, seo_strategy, i
                )
                sections.append(section)
        
        return sections
    
    async def _create_intro_section(self, niche: str, persona: PersonaProfile, 
                                  device: DeviceOptimization, seo_strategy: Dict, 
                                  index: int) -> Dict[str, Any]:
        """Create introduction section"""
        return {
            "type": "introduction",
            "title": f"The Complete {niche.title()} Guide",
            "content_points": [
                f"Discover why {niche} is revolutionizing {persona.goals[0]}",
                f"Learn how to overcome {persona.pain_points[0]}",
                f"Get actionable insights for immediate results"
            ],
            "target_length": device.optimal_section_length,
            "include_visual": True,
            "seo_focus": seo_strategy["primary_keyword"],
            "persona_hook": persona.content_preferences[0]
        }
    
    async def _create_hook_section(self, niche: str, persona: PersonaProfile, 
                                 device: DeviceOptimization, seo_strategy: Dict, 
                                 index: int) -> Dict[str, Any]:
        """Create attention-grabbing hook section"""
        hooks = {
            "TechEarlyAdopter": f"The {niche} innovation that's changing everything",
            "RemoteDad": f"How {niche} saves 2+ hours daily for family time",
            "StudentHustler": f"The $0-budget {niche} strategy that actually works",
            "BusinessOwner": f"Why successful businesses are switching to {niche}"
        }
        
        return {
            "type": "hook",
            "title": hooks.get(persona.name, f"Transform Your {niche} Experience"),
            "content_points": [
                "Attention-grabbing statistic or fact",
                "Relatable problem statement",
                "Promise of transformation"
            ],
            "target_length": min(device.optimal_section_length, 80),
            "include_visual": device.device_type == "mobile",
            "urgency_factor": "high" if persona.decision_style == "emotional" else "medium"
        }
    
    async def _create_problem_section(self, niche: str, persona: PersonaProfile, 
                                    device: DeviceOptimization, seo_strategy: Dict, 
                                    index: int) -> Dict[str, Any]:
        """Create problem identification section"""
        return {
            "type": "problem",
            "title": f"The {niche.title()} Challenge Most People Face",
            "content_points": [
                f"Common pain point: {persona.pain_points[0]}",
                f"Hidden challenge: {persona.pain_points[1] if len(persona.pain_points) > 1 else 'Hidden costs'}",
                "Why traditional solutions fail"
            ],
            "target_length": device.optimal_section_length,
            "include_visual": True,
            "emotional_trigger": persona.decision_style == "emotional",
            "social_proof": persona.decision_style == "social_proof"
        }
    
    async def _create_solution_section(self, niche: str, persona: PersonaProfile, 
                                     device: DeviceOptimization, seo_strategy: Dict, 
                                     index: int) -> Dict[str, Any]:
        """Create solution presentation section"""
        return {
            "type": "solution",
            "title": f"The Complete {niche.title()} Solution",
            "content_points": [
                f"How our approach solves {persona.pain_points[0]}",
                f"Unique advantage for {persona.goals[0]}",
                "Step-by-step implementation overview"
            ],
            "target_length": device.optimal_section_length * 1.5,
            "include_visual": True,
            "technical_depth": persona.tech_savviness,
            "proof_elements": ["case_study", "testimonial"] if persona.decision_style == "social_proof" else ["data", "logic"]
        }
    
    async def _create_benefits_section(self, niche: str, persona: PersonaProfile, 
                                     device: DeviceOptimization, seo_strategy: Dict, 
                                     index: int) -> Dict[str, Any]:
        """Create benefits section"""
        return {
            "type": "benefits",
            "title": f"Why {niche.title()} Works for {persona.name}",
            "content_points": [
                f"Primary benefit: {persona.goals[0]}",
                f"Secondary benefit: {persona.goals[1] if len(persona.goals) > 1 else 'Time saving'}",
                "Unexpected advantage",
                "Long-term value"
            ],
            "target_length": device.optimal_section_length,
            "include_visual": True,
            "benefit_format": "list" if device.device_type == "mobile" else "detailed",
            "quantify_benefits": persona.decision_style == "analytical"
        }
    
    async def _create_howto_section(self, niche: str, persona: PersonaProfile, 
                                  device: DeviceOptimization, seo_strategy: Dict, 
                                  index: int) -> Dict[str, Any]:
        """Create how-to section"""
        return {
            "type": "howto",
            "title": f"How to Get Started with {niche.title()}",
            "content_points": [
                "Step 1: Initial setup/preparation",
                "Step 2: Core implementation",
                "Step 3: Optimization and scaling",
                "Pro tips for success"
            ],
            "target_length": device.optimal_section_length * 2,
            "include_visual": True,
            "step_detail": persona.tech_savviness,
            "actionable_focus": True
        }
    
    async def _create_comparison_section(self, niche: str, persona: PersonaProfile, 
                                       device: DeviceOptimization, seo_strategy: Dict, 
                                       index: int) -> Dict[str, Any]:
        """Create comparison section"""
        return {
            "type": "comparison",
            "title": f"Comparing {niche.title()} Options",
            "content_points": [
                "Feature comparison table",
                "Price vs value analysis",
                "Use case recommendations",
                "Decision framework"
            ],
            "target_length": device.optimal_section_length * 1.5,
            "include_visual": True,
            "comparison_format": "table" if device.device_type != "mobile" else "list",
            "analytical_depth": persona.decision_style == "analytical"
        }
    
    async def _create_examples_section(self, niche: str, persona: PersonaProfile, 
                                     device: DeviceOptimization, seo_strategy: Dict, 
                                     index: int) -> Dict[str, Any]:
        """Create examples section"""
        return {
            "type": "examples",
            "title": f"Real {niche.title()} Success Stories",
            "content_points": [
                "Case study 1: Similar to persona",
                "Case study 2: Different use case",
                "Quick wins examples",
                "Common success patterns"
            ],
            "target_length": device.optimal_section_length,
            "include_visual": True,
            "story_format": "narrative" if persona.decision_style == "emotional" else "bullet_points",
            "relatability_focus": True
        }
    
    async def _create_proof_section(self, niche: str, persona: PersonaProfile, 
                                  device: DeviceOptimization, seo_strategy: Dict, 
                                  index: int) -> Dict[str, Any]:
        """Create social proof section"""
        return {
            "type": "proof",
            "title": f"Why Thousands Choose {niche.title()}",
            "content_points": [
                "User testimonials",
                "Usage statistics",
                "Expert endorsements",
                "Media mentions"
            ],
            "target_length": device.optimal_section_length * 0.8,
            "include_visual": True,
            "proof_type": "social" if persona.decision_style == "social_proof" else "logical",
            "trust_signals": True
        }
    
    async def _create_recommendation_section(self, niche: str, persona: PersonaProfile, 
                                           device: DeviceOptimization, seo_strategy: Dict, 
                                           index: int) -> Dict[str, Any]:
        """Create recommendation section"""
        return {
            "type": "recommendation",
            "title": f"Our Top {niche.title()} Recommendation",
            "content_points": [
                "Best overall choice explanation",
                "Why it fits your needs",
                "Getting started guide",
                "Expected results timeline"
            ],
            "target_length": device.optimal_section_length,
            "include_visual": True,
            "confidence_level": "high",
            "persona_alignment": persona.name
        }
    
    async def _create_cta_section(self, niche: str, persona: PersonaProfile, 
                                device: DeviceOptimization, seo_strategy: Dict, 
                                index: int) -> Dict[str, Any]:
        """Create call-to-action section"""
        cta_messages = {
            "TechEarlyAdopter": "Get early access to cutting-edge features",
            "RemoteDad": "Start saving time for your family today",
            "StudentHustler": "Begin your success journey now",
            "BusinessOwner": "Scale your business with proven solutions"
        }
        
        return {
            "type": "cta",
            "title": "Ready to Transform Your Results?",
            "content_points": [
                cta_messages.get(persona.name, "Take action today"),
                "Limited time offer/bonus",
                "Risk-free guarantee",
                "Next steps clarity"
            ],
            "target_length": device.optimal_section_length * 0.6,
            "include_visual": True,
            "urgency_level": "high" if persona.decision_style == "emotional" else "medium",
            "conversion_focus": True
        }
    
    async def _create_conclusion_section(self, niche: str, persona: PersonaProfile, 
                                       device: DeviceOptimization, seo_strategy: Dict, 
                                       index: int) -> Dict[str, Any]:
        """Create conclusion section"""
        return {
            "type": "conclusion",
            "title": f"Your {niche.title()} Success Starts Now",
            "content_points": [
                "Key takeaways summary",
                "Action steps reminder",
                "Future potential preview",
                "Community invitation"
            ],
            "target_length": device.optimal_section_length * 0.8,
            "include_visual": False,
            "summary_focus": True,
            "forward_looking": True
        }
    
    async def _create_explanation_section(self, niche: str, persona: PersonaProfile, 
                                        device: DeviceOptimization, seo_strategy: Dict, 
                                        index: int) -> Dict[str, Any]:
        """Create explanation section"""
        return {
            "type": "explanation",
            "title": f"What is {niche.title()}?",
            "content_points": [
                "Clear definition",
                "How it works overview",
                "Key components",
                "Why it matters"
            ],
            "target_length": device.optimal_section_length,
            "include_visual": True,
            "complexity_level": persona.tech_savviness,
            "educational_focus": True
        }
    
    async def _generate_title(self, niche: str, persona: PersonaProfile, 
                            seo_strategy: Dict) -> str:
        """Generate optimized title"""
        template = seo_strategy["template"]["title_pattern"]
        year = datetime.now().year
        
        title = template.format(
            keyword=seo_strategy["primary_keyword"],
            year=year,
            brand="MarketingFunnelMaster"
        )
        
        # Persona-specific title optimization
        if persona.name == "TechEarlyAdopter":
            title = f"Advanced {title}"
        elif persona.name == "StudentHustler":
            title = f"Budget-Friendly {title}"
        elif persona.name == "RemoteDad":
            title = f"Family-Focused {title}"
        elif persona.name == "BusinessOwner":
            title = f"Professional {title}"
        
        return title
    
    async def _generate_meta_description(self, title: str, seo_strategy: Dict) -> str:
        """Generate SEO-optimized meta description"""
        template = seo_strategy["template"]["meta_pattern"]
        
        meta = template.format(
            keyword=seo_strategy["primary_keyword"],
            benefits="proven strategies and expert insights",
            benefit_1="save time",
            benefit_2="increase efficiency", 
            benefit_3="boost results"
        )
        
        # Ensure under 160 characters
        if len(meta) > 160:
            meta = meta[:157] + "..."
        
        return meta
    
    def _calculate_reading_time(self, sections: List[Dict[str, Any]], 
                              device: DeviceOptimization) -> int:
        """Calculate estimated reading time in minutes"""
        total_words = sum(section.get("target_length", 200) for section in sections)
        
        # Adjust reading speed by device
        reading_speeds = {
            "mobile": 180,  # words per minute
            "tablet": 220,
            "desktop": 250
        }
        
        speed = reading_speeds.get(device.device_type, 220)
        return max(1, round(total_words / speed))
    
    def _identify_conversion_elements(self, persona: PersonaProfile, 
                                    device: DeviceOptimization) -> List[str]:
        """Identify key conversion elements for the content"""
        base_elements = ["headline", "value_proposition", "social_proof", "cta"]
        
        # Add persona-specific elements
        if persona.decision_style == "analytical":
            base_elements.extend(["data_points", "comparison_table", "roi_calculator"])
        elif persona.decision_style == "emotional":
            base_elements.extend(["storytelling", "urgency", "scarcity"])
        elif persona.decision_style == "social_proof":
            base_elements.extend(["testimonials", "case_studies", "user_count"])
        
        # Add device-specific elements
        if device.device_type == "mobile":
            base_elements.extend(["swipe_cta", "tap_to_call", "app_download"])
        elif device.device_type == "desktop":
            base_elements.extend(["detailed_form", "demo_request", "whitepaper"])
        
        return list(set(base_elements))
    
    async def _calculate_quality_score(self, outline: ContentOutline) -> float:
        """Calculate content outline quality score"""
        score = 0.0
        max_score = 100.0
        
        # SEO optimization (30 points)
        if outline.seo_strategy.get("primary_keyword"):
            score += 10
        if outline.seo_strategy.get("secondary_keywords"):
            score += 10
        if outline.meta_description and len(outline.meta_description) <= 160:
            score += 10
        
        # Content structure (30 points)
        if len(outline.sections) >= 5:
            score += 15
        if any(section.get("include_visual") for section in outline.sections):
            score += 15
        
        # Persona targeting (25 points)
        if outline.persona_targeting.get("persona"):
            score += 10
        if outline.persona_targeting.get("decision_style"):
            score += 15
        
        # Device optimization (15 points)
        if outline.device_optimization.get("device"):
            score += 10
        if outline.estimated_reading_time > 0:
            score += 5
        
        return min(score, max_score)
    
    async def _update_metrics(self, execution_time: float, quality_score: float):
        """Update agent performance metrics"""
        if "total_outlines" not in self.performance_metrics:
            self.performance_metrics = {
                "total_outlines": 0,
                "average_execution_time": 0.0,
                "average_quality_score": 0.0,
                "success_rate": 100.0
            }
        
        total = self.performance_metrics["total_outlines"]
        self.performance_metrics["total_outlines"] = total + 1
        
        # Update averages
        self.performance_metrics["average_execution_time"] = (
            (self.performance_metrics["average_execution_time"] * total + execution_time) / (total + 1)
        )
        
        self.performance_metrics["average_quality_score"] = (
            (self.performance_metrics["average_quality_score"] * total + quality_score) / (total + 1)
        )
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        return self.performance_metrics.copy()
    
    async def health_check(self) -> bool:
        """Check agent health status"""
        return len(self.persona_database) > 0 and len(self.device_profiles) > 0