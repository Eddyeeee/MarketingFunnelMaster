#!/usr/bin/env python3
"""
ContentWriterAgent - AI-Powered Content Generation
Module 3A: Phase 2 Implementation

Executor: Claude Code
Erstellt: 2025-07-04
Version: 1.0
"""

import logging
import asyncio
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import json

logger = logging.getLogger(__name__)

@dataclass
class WritingStyle:
    """Writing style parameters for different personas"""
    tone: str  # professional, conversational, authoritative, friendly
    complexity: str  # simple, medium, advanced
    sentence_length: str  # short, medium, long
    paragraph_length: int  # sentences per paragraph
    active_voice_ratio: float  # percentage of active voice
    personal_pronouns: bool  # use you/your vs third person

@dataclass
class ContentMetrics:
    """Content quality and performance metrics"""
    word_count: int
    readability_score: float
    keyword_density: float
    sentiment_score: float
    engagement_score: float
    conversion_potential: float

class GeneratedContent(BaseModel):
    """Generated content structure"""
    title: str
    meta_description: str
    content_sections: List[Dict[str, Any]]
    full_content: str
    metrics: Dict[str, Any]
    seo_analysis: Dict[str, Any]
    conversion_elements: List[str]
    quality_score: float = Field(default=0.0)
    generation_time: float = Field(default=0.0)

class ContentWriterAgent:
    """AI agent for generating high-quality, conversion-optimized content"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.writing_styles = self._load_writing_styles()
        self.content_templates = self._load_content_templates()
        self.conversion_patterns = self._load_conversion_patterns()
        self.performance_metrics = {}
        
    def _load_writing_styles(self) -> Dict[str, WritingStyle]:
        """Load persona-specific writing styles"""
        return {
            "TechEarlyAdopter": WritingStyle(
                tone="authoritative",
                complexity="advanced",
                sentence_length="medium",
                paragraph_length=3,
                active_voice_ratio=0.8,
                personal_pronouns=True
            ),
            "RemoteDad": WritingStyle(
                tone="friendly",
                complexity="simple",
                sentence_length="short",
                paragraph_length=2,
                active_voice_ratio=0.9,
                personal_pronouns=True
            ),
            "StudentHustler": WritingStyle(
                tone="conversational",
                complexity="medium",
                sentence_length="short",
                paragraph_length=2,
                active_voice_ratio=0.85,
                personal_pronouns=True
            ),
            "BusinessOwner": WritingStyle(
                tone="professional",
                complexity="advanced",
                sentence_length="medium",
                paragraph_length=4,
                active_voice_ratio=0.75,
                personal_pronouns=False
            )
        }
    
    def _load_content_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load content generation templates"""
        return {
            "introduction": {
                "hook_patterns": [
                    "Did you know that {statistic}?",
                    "Imagine if you could {benefit} in just {timeframe}.",
                    "What if I told you that {surprising_fact}?",
                    "The secret to {goal} isn't what you think."
                ],
                "problem_statements": [
                    "Most people struggle with {pain_point} because {reason}.",
                    "Traditional {method} fails to deliver {desired_outcome}.",
                    "The biggest challenge in {field} is {obstacle}."
                ],
                "solution_previews": [
                    "That's where {solution} comes in.",
                    "Here's how to solve this once and for all:",
                    "The answer lies in {approach}."
                ]
            },
            "benefits": {
                "benefit_frameworks": [
                    "Feature → Advantage → Benefit",
                    "Before → After → Bridge",
                    "Problem → Agitation → Solution"
                ],
                "proof_elements": [
                    "statistical_evidence",
                    "case_studies",
                    "expert_testimonials",
                    "user_reviews"
                ]
            },
            "howto": {
                "step_structures": [
                    "Step {number}: {action_title}",
                    "Phase {number}: {phase_name}",
                    "{number}. {instruction}"
                ],
                "explanation_patterns": [
                    "Here's how: {detailed_explanation}",
                    "The process is simple: {step_by_step}",
                    "Follow this framework: {framework}"
                ]
            },
            "conclusion": {
                "summary_patterns": [
                    "To recap, {key_points}",
                    "The bottom line: {main_takeaway}",
                    "Remember these key insights: {insights}"
                ],
                "next_steps": [
                    "Your next move is to {action}",
                    "Start by {first_step}",
                    "Begin your journey with {starting_point}"
                ]
            }
        }
    
    def _load_conversion_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load conversion optimization patterns"""
        return {
            "urgency": {
                "time_based": [
                    "Limited time offer",
                    "Only available this week",
                    "Don't wait - act now"
                ],
                "scarcity": [
                    "Limited spots available",
                    "Only {number} left in stock",
                    "Exclusive access for {group}"
                ]
            },
            "social_proof": {
                "testimonials": [
                    "Here's what {customer} says:",
                    "{customer_count}+ happy customers",
                    "Trusted by industry leaders"
                ],
                "statistics": [
                    "{percentage}% of users see results",
                    "Over {number} success stories",
                    "Average improvement of {metric}"
                ]
            },
            "trust_building": {
                "guarantees": [
                    "30-day money-back guarantee",
                    "Risk-free trial",
                    "100% satisfaction guaranteed"
                ],
                "credentials": [
                    "Backed by research",
                    "Industry certified",
                    "Expert approved"
                ]
            }
        }
    
    async def generate_content(self, outline: Dict[str, Any], niche: str, 
                             persona: str, device: str) -> GeneratedContent:
        """Generate complete content from outline"""
        start_time = datetime.now()
        
        try:
            # Get writing style for persona
            writing_style = self.writing_styles.get(persona)
            if not writing_style:
                raise ValueError(f"Unknown persona: {persona}")
            
            # Extract outline data
            title = outline.get("title", "")
            sections = outline.get("sections", [])
            seo_strategy = outline.get("seo_strategy", {})
            device_optimization = outline.get("device_optimization", {})
            
            # Generate content sections
            content_sections = []
            full_content_parts = []
            
            for section in sections:
                generated_section = await self._generate_section_content(
                    section, writing_style, seo_strategy, device, niche, persona
                )
                content_sections.append(generated_section)
                full_content_parts.append(generated_section["content"])
            
            # Combine full content
            full_content = "\n\n".join(full_content_parts)
            
            # Generate meta description
            meta_description = await self._generate_meta_description(
                title, full_content, seo_strategy
            )
            
            # Analyze content metrics
            metrics = await self._analyze_content_metrics(
                full_content, seo_strategy, writing_style
            )
            
            # SEO analysis
            seo_analysis = await self._perform_seo_analysis(
                full_content, title, meta_description, seo_strategy
            )
            
            # Identify conversion elements
            conversion_elements = await self._identify_conversion_elements(
                content_sections, persona, device
            )
            
            # Create generated content object
            generated_content = GeneratedContent(
                title=title,
                meta_description=meta_description,
                content_sections=content_sections,
                full_content=full_content,
                metrics=metrics,
                seo_analysis=seo_analysis,
                conversion_elements=conversion_elements,
                generation_time=(datetime.now() - start_time).total_seconds()
            )
            
            # Calculate quality score
            generated_content.quality_score = await self._calculate_content_quality_score(
                generated_content
            )
            
            # Update performance metrics
            await self._update_metrics(generated_content)
            
            logger.info(f"Generated content for {niche}/{persona}/{device} "
                       f"({metrics['word_count']} words) in {generated_content.generation_time:.2f}s")
            
            return generated_content
            
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            raise
    
    async def _generate_section_content(self, section: Dict[str, Any], 
                                      writing_style: WritingStyle,
                                      seo_strategy: Dict[str, Any],
                                      device: str, niche: str, persona: str) -> Dict[str, Any]:
        """Generate content for a specific section"""
        section_type = section.get("type", "")
        title = section.get("title", "")
        content_points = section.get("content_points", [])
        target_length = section.get("target_length", 200)
        
        # Generate section content based on type
        if section_type == "introduction":
            content = await self._generate_introduction_content(
                title, content_points, writing_style, seo_strategy, niche, persona
            )
        elif section_type == "hook":
            content = await self._generate_hook_content(
                title, content_points, writing_style, persona, device
            )
        elif section_type == "problem":
            content = await self._generate_problem_content(
                title, content_points, writing_style, persona
            )
        elif section_type == "solution":
            content = await self._generate_solution_content(
                title, content_points, writing_style, niche, persona
            )
        elif section_type == "benefits":
            content = await self._generate_benefits_content(
                title, content_points, writing_style, persona
            )
        elif section_type == "howto":
            content = await self._generate_howto_content(
                title, content_points, writing_style, persona
            )
        elif section_type == "comparison":
            content = await self._generate_comparison_content(
                title, content_points, writing_style, device, persona
            )
        elif section_type == "examples":
            content = await self._generate_examples_content(
                title, content_points, writing_style, persona
            )
        elif section_type == "proof":
            content = await self._generate_proof_content(
                title, content_points, writing_style, persona
            )
        elif section_type == "cta":
            content = await self._generate_cta_content(
                title, content_points, writing_style, persona, device
            )
        elif section_type == "conclusion":
            content = await self._generate_conclusion_content(
                title, content_points, writing_style, persona
            )
        else:
            content = await self._generate_generic_content(
                title, content_points, writing_style, target_length
            )
        
        # Apply device-specific formatting
        formatted_content = await self._apply_device_formatting(content, device)
        
        # Inject SEO elements
        seo_optimized_content = await self._inject_seo_elements(
            formatted_content, seo_strategy, section_type
        )
        
        return {
            "type": section_type,
            "title": title,
            "content": seo_optimized_content,
            "word_count": len(seo_optimized_content.split()),
            "include_visual": section.get("include_visual", False),
            "conversion_elements": section.get("conversion_focus", False)
        }
    
    async def _generate_introduction_content(self, title: str, points: List[str],
                                           style: WritingStyle, seo: Dict[str, Any],
                                           niche: str, persona: str) -> str:
        """Generate introduction section content"""
        templates = self.content_templates["introduction"]
        
        # Select hook pattern based on persona
        hook_pattern = templates["hook_patterns"][0]  # Simplified selection
        hook = hook_pattern.format(
            statistic="85% of people struggle with " + niche,
            benefit="master " + niche,
            timeframe="30 days",
            surprising_fact=f"{niche} can transform your daily routine",
            goal=niche + " success"
        )
        
        # Problem statement
        problem = templates["problem_statements"][0].format(
            pain_point=niche + " optimization",
            reason="they lack the right strategy",
            method=niche + " approaches",
            desired_outcome="consistent results",
            field=niche,
            obstacle="information overload"
        )
        
        # Solution preview
        solution = templates["solution_previews"][0].format(
            solution=f"our proven {niche} framework",
            approach=f"systematic {niche} methodology"
        )
        
        # Combine based on writing style
        if style.tone == "conversational":
            content = f"{hook}\n\n{problem}\n\n{solution}\n\nIn this guide, you'll discover:"
        else:
            content = f"{hook} {problem} {solution}\n\nThis comprehensive guide covers:"
        
        # Add bullet points
        for point in points:
            content += f"\n• {point}"
        
        return content
    
    async def _generate_hook_content(self, title: str, points: List[str],
                                   style: WritingStyle, persona: str, device: str) -> str:
        """Generate attention-grabbing hook content"""
        # Persona-specific hooks
        hooks = {
            "TechEarlyAdopter": "The latest breakthrough in technology is here, and it's going to change everything you thought you knew.",
            "RemoteDad": "What if you could reclaim 2+ hours every day to spend with your family?",
            "StudentHustler": "The $0 strategy that's helping students build successful side businesses.",
            "BusinessOwner": "Why top companies are switching to this game-changing approach."
        }
        
        hook = hooks.get(persona, "Discover the secret that industry leaders don't want you to know.")
        
        # Device-specific formatting
        if device == "mobile":
            # Short, punchy sentences for mobile
            content = f"{hook}\n\nHere's what you need to know:\n"
            for point in points[:3]:  # Limit points on mobile
                content += f"→ {point}\n"
        else:
            # More detailed for desktop
            content = f"{hook}\n\n"
            for point in points:
                content += f"{point}. "
        
        return content.strip()
    
    async def _generate_problem_content(self, title: str, points: List[str],
                                      style: WritingStyle, persona: str) -> str:
        """Generate problem identification content"""
        # Persona-specific problem framing
        problem_intros = {
            "TechEarlyAdopter": "Even with access to the latest technology, most people still struggle with",
            "RemoteDad": "Balancing work and family life becomes especially challenging when dealing with",
            "StudentHustler": "Limited budgets and time constraints make it difficult to overcome",
            "BusinessOwner": "Growing a business while managing resources effectively requires solving"
        }
        
        intro = problem_intros.get(persona, "The biggest challenge most people face is")
        
        content = f"{intro} the following issues:\n\n"
        
        for i, point in enumerate(points, 1):
            if style.tone == "conversational":
                content += f"{i}. {point} - and it's more common than you think.\n\n"
            else:
                content += f"{i}. {point}\n\n"
        
        # Add emotional connection
        if persona == "RemoteDad":
            content += "Sound familiar? You're not alone in feeling overwhelmed by these challenges."
        elif persona == "StudentHustler":
            content += "If this resonates with you, you're in good company - thousands of students face these exact same obstacles."
        
        return content
    
    async def _generate_solution_content(self, title: str, points: List[str],
                                       style: WritingStyle, niche: str, persona: str) -> str:
        """Generate solution presentation content"""
        # Solution introduction
        solution_intros = {
            "TechEarlyAdopter": f"Our advanced {niche} system solves these problems through innovative technology and proven methodologies.",
            "RemoteDad": f"The {niche} solution is designed specifically for busy parents who need results without complexity.",
            "StudentHustler": f"This budget-friendly {niche} approach gives you maximum results with minimal investment.",
            "BusinessOwner": f"Our enterprise-grade {niche} solution scales with your business needs."
        }
        
        intro = solution_intros.get(persona, f"The comprehensive {niche} solution addresses these challenges systematically.")
        
        content = f"{intro}\n\n"
        
        # Add solution points
        for point in points:
            content += f"✓ {point}\n\n"
        
        # Add credibility elements
        if style.tone == "professional":
            content += "This methodology has been tested and refined through extensive real-world application."
        else:
            content += "Thousands of people have already transformed their results using this exact approach."
        
        return content
    
    async def _generate_benefits_content(self, title: str, points: List[str],
                                       style: WritingStyle, persona: str) -> str:
        """Generate benefits section content"""
        # Benefits introduction
        benefits_intros = {
            "TechEarlyAdopter": "The technical advantages and competitive benefits include:",
            "RemoteDad": "Here's how this will improve your work-life balance:",
            "StudentHustler": "The benefits that matter most to students:",
            "BusinessOwner": "The business impact and ROI you can expect:"
        }
        
        intro = benefits_intros.get(persona, "Key benefits include:")
        
        content = f"{intro}\n\n"
        
        # Format benefits based on persona preference
        for i, point in enumerate(points, 1):
            if persona == "BusinessOwner":
                # More formal, analytical
                content += f"• {point}: Directly impacts business efficiency and growth potential\n\n"
            elif persona == "RemoteDad":
                # Emotional, family-focused
                content += f"• {point} - giving you more quality time with your family\n\n"
            else:
                # Standard format
                content += f"• {point}\n\n"
        
        return content
    
    async def _generate_howto_content(self, title: str, points: List[str],
                                    style: WritingStyle, persona: str) -> str:
        """Generate how-to section content"""
        content = f"Follow this step-by-step process:\n\n"
        
        for i, point in enumerate(points, 1):
            if style.complexity == "simple":
                content += f"Step {i}: {point}\n\n"
            else:
                content += f"**Step {i}: {point}**\n\nDetailed implementation notes go here.\n\n"
        
        # Add persona-specific tips
        if persona == "TechEarlyAdopter":
            content += "**Pro Tips:** Advanced users can optimize this process further by..."
        elif persona == "StudentHustler":
            content += "**Money-Saving Tip:** You can reduce costs by starting with..."
        
        return content
    
    async def _generate_comparison_content(self, title: str, points: List[str],
                                         style: WritingStyle, device: str, persona: str) -> str:
        """Generate comparison section content"""
        if device == "mobile":
            # Simple list format for mobile
            content = "Here's how different options compare:\n\n"
            for point in points:
                content += f"• {point}\n"
        else:
            # Table format for desktop
            content = "Detailed comparison:\n\n"
            content += "| Feature | Option A | Option B | Our Recommendation |\n"
            content += "|---------|----------|----------|-------------------|\n"
            content += "| Value | High | Medium | Highest |\n"
            content += "| Ease of Use | Medium | High | High |\n"
            content += "| Results | Good | Average | Excellent |\n\n"
            
            for point in points:
                content += f"{point}\n\n"
        
        return content
    
    async def _generate_examples_content(self, title: str, points: List[str],
                                       style: WritingStyle, persona: str) -> str:
        """Generate examples/case studies content"""
        content = "Real success stories:\n\n"
        
        # Persona-specific case studies
        case_studies = {
            "TechEarlyAdopter": "Sarah, a software engineer, increased her productivity by 40% using our advanced automation features.",
            "RemoteDad": "Mike, a father of two, now saves 2 hours daily and has dinner with his family every night.",
            "StudentHustler": "Jake built a $1,000/month side business while maintaining his 4.0 GPA.",
            "BusinessOwner": "Lisa scaled her agency from $50K to $200K annual revenue in just 8 months."
        }
        
        case_study = case_studies.get(persona, "John achieved remarkable results using our system.")
        content += f"**Case Study 1:** {case_study}\n\n"
        
        for point in points:
            content += f"• {point}\n"
        
        return content
    
    async def _generate_proof_content(self, title: str, points: List[str],
                                    style: WritingStyle, persona: str) -> str:
        """Generate social proof content"""
        # Persona-specific proof elements
        if persona == "BusinessOwner":
            content = "**Industry Recognition:**\n\n"
            content += "• Featured in leading business publications\n"
            content += "• Trusted by Fortune 500 companies\n"
            content += "• 98% customer satisfaction rate\n\n"
        else:
            content = "**What Users Say:**\n\n"
            content += '"This completely changed my approach" - Alex M.\n\n'
            content += '"Results in just 2 weeks" - Maria K.\n\n'
            content += '"Worth every penny" - David L.\n\n'
        
        for point in points:
            content += f"• {point}\n"
        
        return content
    
    async def _generate_cta_content(self, title: str, points: List[str],
                                  style: WritingStyle, persona: str, device: str) -> str:
        """Generate call-to-action content"""
        # Persona-specific CTA messaging
        cta_messages = {
            "TechEarlyAdopter": "Ready to unlock advanced capabilities?",
            "RemoteDad": "Start saving time for your family today:",
            "StudentHustler": "Begin your success journey now:",
            "BusinessOwner": "Scale your business with proven results:"
        }
        
        main_cta = cta_messages.get(persona, "Take action today:")
        
        content = f"## {main_cta}\n\n"
        
        for point in points:
            content += f"✓ {point}\n"
        
        # Device-specific CTA buttons
        if device == "mobile":
            content += "\n**[GET STARTED NOW - TAP HERE]**\n"
        else:
            content += "\n**[Start Your Free Trial - Click Here]**\n"
        
        # Add urgency/scarcity if appropriate for persona
        if persona in ["StudentHustler", "RemoteDad"]:
            content += "\n*Limited time: Save 30% this week only*"
        
        return content
    
    async def _generate_conclusion_content(self, title: str, points: List[str],
                                         style: WritingStyle, persona: str) -> str:
        """Generate conclusion content"""
        content = "## Key Takeaways\n\n"
        
        for point in points:
            content += f"• {point}\n"
        
        content += "\n"
        
        # Persona-specific closing
        closings = {
            "TechEarlyAdopter": "Stay ahead of the curve and implement these advanced strategies today.",
            "RemoteDad": "Your family deserves the best version of you - make the change today.",
            "StudentHustler": "Your future success starts with the actions you take right now.",
            "BusinessOwner": "Transform your business outcomes with these proven strategies."
        }
        
        closing = closings.get(persona, "Take action and transform your results today.")
        content += closing
        
        return content
    
    async def _generate_generic_content(self, title: str, points: List[str],
                                      style: WritingStyle, target_length: int) -> str:
        """Generate generic content for undefined section types"""
        content = f"## {title}\n\n"
        
        for point in points:
            content += f"{point}. "
            # Add filler content to reach target length
            if len(content.split()) < target_length:
                content += "This section provides detailed information and actionable insights. "
        
        return content
    
    async def _apply_device_formatting(self, content: str, device: str) -> str:
        """Apply device-specific formatting"""
        if device == "mobile":
            # Shorter paragraphs, more line breaks
            formatted = content.replace(". ", ".\n\n")
            # Convert long lists to shorter ones
            formatted = re.sub(r'(\n• .*?\n• .*?\n• .*?\n)', r'\1\n', formatted)
        elif device == "tablet":
            # Medium formatting
            formatted = content.replace(". ", ". ")
        else:  # desktop
            # Longer paragraphs, fewer line breaks
            formatted = content
        
        return formatted
    
    async def _inject_seo_elements(self, content: str, seo_strategy: Dict[str, Any],
                                 section_type: str) -> str:
        """Inject SEO elements into content"""
        primary_keyword = seo_strategy.get("primary_keyword", "")
        secondary_keywords = seo_strategy.get("secondary_keywords", [])
        
        # Natural keyword injection based on section type
        if section_type == "introduction" and primary_keyword:
            # Ensure primary keyword appears early
            if primary_keyword.lower() not in content.lower():
                content = content.replace("this guide", f"this {primary_keyword} guide", 1)
        
        # Add semantic keywords naturally
        semantic_keywords = seo_strategy.get("semantic_keywords", [])
        for keyword in semantic_keywords[:2]:  # Limit to avoid over-optimization
            if keyword not in content.lower():
                content += f" This {keyword} approach ensures optimal results."
        
        return content
    
    async def _generate_meta_description(self, title: str, content: str,
                                       seo_strategy: Dict[str, Any]) -> str:
        """Generate SEO-optimized meta description"""
        primary_keyword = seo_strategy.get("primary_keyword", "")
        
        # Extract first compelling sentence
        sentences = content.split(". ")
        first_sentence = sentences[0] if sentences else title
        
        # Create meta description
        meta = f"Discover {primary_keyword} strategies that work. {first_sentence}. Get proven results today!"
        
        # Ensure under 160 characters
        if len(meta) > 160:
            meta = meta[:157] + "..."
        
        return meta
    
    async def _analyze_content_metrics(self, content: str, seo_strategy: Dict[str, Any],
                                     writing_style: WritingStyle) -> Dict[str, Any]:
        """Analyze content quality metrics"""
        words = content.split()
        word_count = len(words)
        
        # Calculate readability (simplified Flesch score)
        sentences = len([s for s in content.split('.') if s.strip()])
        avg_sentence_length = word_count / max(sentences, 1)
        readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * 1.5)  # Simplified
        readability_score = max(0, min(100, readability_score))
        
        # Calculate keyword density
        primary_keyword = seo_strategy.get("primary_keyword", "").lower()
        keyword_count = content.lower().count(primary_keyword) if primary_keyword else 0
        keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0
        
        # Sentiment analysis (simplified)
        positive_words = ["great", "excellent", "amazing", "powerful", "effective", "proven"]
        negative_words = ["difficult", "challenging", "problem", "struggle", "fail"]
        
        positive_count = sum(content.lower().count(word) for word in positive_words)
        negative_count = sum(content.lower().count(word) for word in negative_words)
        sentiment_score = (positive_count - negative_count) / max(word_count / 100, 1)
        
        # Engagement score (based on structure and elements)
        engagement_indicators = ["?", "!", "you", "your", "how to", "step", "tip"]
        engagement_count = sum(content.lower().count(indicator) for indicator in engagement_indicators)
        engagement_score = min(100, (engagement_count / word_count) * 1000)
        
        # Conversion potential (based on CTA and persuasive elements)
        conversion_indicators = ["now", "today", "start", "get", "free", "limited", "guarantee"]
        conversion_count = sum(content.lower().count(indicator) for indicator in conversion_indicators)
        conversion_potential = min(100, (conversion_count / word_count) * 500)
        
        return {
            "word_count": word_count,
            "readability_score": round(readability_score, 1),
            "keyword_density": round(keyword_density, 2),
            "sentiment_score": round(sentiment_score, 2),
            "engagement_score": round(engagement_score, 1),
            "conversion_potential": round(conversion_potential, 1)
        }
    
    async def _perform_seo_analysis(self, content: str, title: str, meta_description: str,
                                  seo_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive SEO analysis"""
        primary_keyword = seo_strategy.get("primary_keyword", "").lower()
        secondary_keywords = seo_strategy.get("secondary_keywords", [])
        
        analysis = {
            "title_optimization": {
                "has_primary_keyword": primary_keyword in title.lower(),
                "length_optimal": 30 <= len(title) <= 60,
                "score": 0
            },
            "meta_description_optimization": {
                "has_primary_keyword": primary_keyword in meta_description.lower(),
                "length_optimal": 120 <= len(meta_description) <= 160,
                "score": 0
            },
            "content_optimization": {
                "keyword_in_first_paragraph": False,
                "keyword_density_optimal": False,
                "has_headings": False,
                "score": 0
            },
            "overall_score": 0
        }
        
        # Check keyword in first paragraph
        first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
        analysis["content_optimization"]["keyword_in_first_paragraph"] = primary_keyword in first_paragraph.lower()
        
        # Check keyword density
        word_count = len(content.split())
        keyword_count = content.lower().count(primary_keyword)
        keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0
        analysis["content_optimization"]["keyword_density_optimal"] = 0.5 <= keyword_density <= 2.5
        
        # Check for headings
        analysis["content_optimization"]["has_headings"] = "##" in content or "#" in content
        
        # Calculate scores
        title_score = sum([
            analysis["title_optimization"]["has_primary_keyword"] * 50,
            analysis["title_optimization"]["length_optimal"] * 50
        ])
        analysis["title_optimization"]["score"] = title_score
        
        meta_score = sum([
            analysis["meta_description_optimization"]["has_primary_keyword"] * 50,
            analysis["meta_description_optimization"]["length_optimal"] * 50
        ])
        analysis["meta_description_optimization"]["score"] = meta_score
        
        content_score = sum([
            analysis["content_optimization"]["keyword_in_first_paragraph"] * 30,
            analysis["content_optimization"]["keyword_density_optimal"] * 40,
            analysis["content_optimization"]["has_headings"] * 30
        ])
        analysis["content_optimization"]["score"] = content_score
        
        analysis["overall_score"] = (title_score + meta_score + content_score) / 3
        
        return analysis
    
    async def _identify_conversion_elements(self, sections: List[Dict[str, Any]], 
                                          persona: str, device: str) -> List[str]:
        """Identify conversion elements in the content"""
        elements = []
        
        for section in sections:
            if section.get("conversion_elements"):
                elements.append(f"conversion_cta_in_{section['type']}")
            
            if "cta" in section.get("type", ""):
                elements.append("primary_call_to_action")
            
            if "proof" in section.get("type", ""):
                elements.append("social_proof")
            
            if "benefits" in section.get("type", ""):
                elements.append("value_proposition")
        
        # Add persona-specific elements
        if persona == "StudentHustler":
            elements.append("price_emphasis")
        elif persona == "BusinessOwner":
            elements.append("roi_focus")
        
        # Add device-specific elements
        if device == "mobile":
            elements.append("mobile_optimized_cta")
        
        return list(set(elements))
    
    async def _calculate_content_quality_score(self, content: GeneratedContent) -> float:
        """Calculate overall content quality score"""
        score = 0.0
        max_score = 100.0
        
        # Content metrics (40 points)
        metrics = content.metrics
        if metrics["word_count"] >= 800:  # Adequate length
            score += 10
        if metrics["readability_score"] >= 60:  # Good readability
            score += 10
        if 0.5 <= metrics["keyword_density"] <= 2.5:  # Optimal keyword density
            score += 10
        if metrics["engagement_score"] >= 50:  # Good engagement
            score += 10
        
        # SEO optimization (30 points)
        seo = content.seo_analysis
        score += (seo["overall_score"] / 100) * 30
        
        # Content structure (20 points)
        if len(content.content_sections) >= 5:  # Good structure
            score += 10
        if any("cta" in section["type"] for section in content.content_sections):  # Has CTA
            score += 10
        
        # Conversion elements (10 points)
        if len(content.conversion_elements) >= 3:
            score += 10
        
        return min(score, max_score)
    
    async def _update_metrics(self, content: GeneratedContent):
        """Update agent performance metrics"""
        if "total_content" not in self.performance_metrics:
            self.performance_metrics = {
                "total_content": 0,
                "average_generation_time": 0.0,
                "average_quality_score": 0.0,
                "average_word_count": 0.0,
                "success_rate": 100.0
            }
        
        total = self.performance_metrics["total_content"]
        self.performance_metrics["total_content"] = total + 1
        
        # Update averages
        self.performance_metrics["average_generation_time"] = (
            (self.performance_metrics["average_generation_time"] * total + content.generation_time) / (total + 1)
        )
        
        self.performance_metrics["average_quality_score"] = (
            (self.performance_metrics["average_quality_score"] * total + content.quality_score) / (total + 1)
        )
        
        self.performance_metrics["average_word_count"] = (
            (self.performance_metrics["average_word_count"] * total + content.metrics["word_count"]) / (total + 1)
        )
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        return self.performance_metrics.copy()
    
    async def health_check(self) -> bool:
        """Check agent health status"""
        return len(self.writing_styles) > 0 and len(self.content_templates) > 0