# Enhanced Personalization Engine - Phase 3, Week 1
# Module: Personalization Intelligence Enhancement
# Created: 2025-07-05

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_
from sqlalchemy.orm import selectinload

from .models import *
from .database_models import JourneySession, PersonalizationData
from ...utils.redis_client import get_redis_client
from ...utils.ml_models import PersonalizationModel, RecommendationEngine, RealTimeOptimizer, ContentVariantGenerator, ml_model_manager
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# ENHANCED PERSONA DETECTION MODELS
# =============================================================================

class PersonaDetector:
    """Advanced persona detection with improved accuracy"""
    
    def __init__(self):
        self.behavioral_patterns = {
            'TechEarlyAdopter': {
                'keywords': ['tech', 'gadget', 'smart', 'app', 'device', 'innovation', 'beta'],
                'behaviors': ['quick_scroll', 'feature_exploration', 'spec_comparison'],
                'time_patterns': {'peak_hours': [9, 12, 14, 18, 20], 'weekend_active': True},
                'device_preference': ['mobile', 'tablet'],
                'engagement_style': 'exploratory'
            },
            'RemoteDad': {
                'keywords': ['family', 'work from home', 'remote', 'balance', 'kids', 'secure'],
                'behaviors': ['thorough_reading', 'comparison_shopping', 'review_checking'],
                'time_patterns': {'peak_hours': [6, 8, 21, 22], 'weekend_active': True},
                'device_preference': ['desktop', 'tablet'],
                'engagement_style': 'methodical'
            },
            'StudentHustler': {
                'keywords': ['student', 'save', 'budget', 'discount', 'deal', 'cheap', 'side hustle'],
                'behaviors': ['price_checking', 'discount_seeking', 'quick_decisions'],
                'time_patterns': {'peak_hours': [11, 15, 17, 22, 23], 'weekend_active': False},
                'device_preference': ['mobile'],
                'engagement_style': 'value_focused'
            },
            'BusinessOwner': {
                'keywords': ['ROI', 'scale', 'business', 'enterprise', 'growth', 'efficiency'],
                'behaviors': ['data_analysis', 'roi_calculation', 'team_consultation'],
                'time_patterns': {'peak_hours': [8, 10, 14, 16], 'weekend_active': False},
                'device_preference': ['desktop'],
                'engagement_style': 'analytical'
            }
        }
    
    async def detect_persona(self, user_data: Dict[str, Any]) -> PersonaData:
        """Detect user persona with enhanced accuracy"""
        try:
            scores = {}
            
            # Extract features
            keywords = user_data.get('search_terms', []) + user_data.get('page_keywords', [])
            behaviors = user_data.get('interaction_patterns', [])
            current_hour = datetime.utcnow().hour
            is_weekend = datetime.utcnow().weekday() >= 5
            device_type = user_data.get('device_type', 'mobile')
            
            # Score each persona
            for persona, patterns in self.behavioral_patterns.items():
                score = 0.0
                
                # Keyword matching (30% weight)
                keyword_matches = sum(1 for kw in keywords if any(p in kw.lower() for p in patterns['keywords']))
                score += (keyword_matches / max(len(keywords), 1)) * 0.3
                
                # Behavior matching (25% weight)
                behavior_matches = sum(1 for b in behaviors if b in patterns['behaviors'])
                score += (behavior_matches / max(len(behaviors), 1)) * 0.25
                
                # Time pattern matching (20% weight)
                if current_hour in patterns['time_patterns']['peak_hours']:
                    score += 0.1
                if is_weekend == patterns['time_patterns']['weekend_active']:
                    score += 0.1
                
                # Device preference (15% weight)
                if device_type in patterns['device_preference']:
                    score += 0.15
                
                # Engagement style (10% weight)
                engagement_score = self._calculate_engagement_style_match(
                    user_data.get('engagement_metrics', {}),
                    patterns['engagement_style']
                )
                score += engagement_score * 0.1
                
                scores[persona] = score
            
            # Select best matching persona
            best_persona = max(scores.items(), key=lambda x: x[1])
            
            return PersonaData(
                type=best_persona[0],
                confidence=min(0.95, best_persona[1]),  # Cap at 95% confidence
                attributes={
                    'scores': scores,
                    'detection_method': 'enhanced_behavioral',
                    'timestamp': datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error detecting persona: {str(e)}")
            return PersonaData(
                type='unknown',
                confidence=0.0,
                attributes={'error': str(e)}
            )
    
    def _calculate_engagement_style_match(self, metrics: Dict[str, Any], style: str) -> float:
        """Calculate match between user engagement and persona style"""
        if style == 'exploratory':
            # Tech early adopters explore many features quickly
            return min(1.0, metrics.get('pages_viewed', 0) / 10.0)
        elif style == 'methodical':
            # Remote dads read thoroughly
            return min(1.0, metrics.get('avg_time_per_page', 0) / 120.0)
        elif style == 'value_focused':
            # Students focus on price/value pages
            return min(1.0, metrics.get('price_checks', 0) / 5.0)
        elif style == 'analytical':
            # Business owners analyze data
            return min(1.0, metrics.get('data_interactions', 0) / 8.0)
        return 0.5

# =============================================================================
# DEVICE-SPECIFIC RENDERING STRATEGIES
# =============================================================================

class DeviceOptimizer:
    """Optimize content rendering for different devices"""
    
    def __init__(self):
        self.device_strategies = {
            'mobile': MobileRenderingStrategy(),
            'tablet': TabletRenderingStrategy(),
            'desktop': DesktopRenderingStrategy()
        }
    
    async def optimize_for_device(self, content: PersonalizedContent, device_context: DeviceContext) -> PersonalizedContent:
        """Optimize content for specific device"""
        device_type = device_context.type.value
        strategy = self.device_strategies.get(device_type, self.device_strategies['mobile'])
        
        return await strategy.optimize(content, device_context)

class MobileRenderingStrategy:
    """Mobile-specific content optimization"""
    
    async def optimize(self, content: PersonalizedContent, context: DeviceContext) -> PersonalizedContent:
        """Optimize content for mobile devices"""
        optimized = content.model_copy()
        
        # Shorten messages for mobile
        if len(optimized.hero_message) > 50:
            optimized.hero_message = self._create_mobile_hook(optimized.hero_message)
        
        # Simplify CTAs
        optimized.call_to_action = self._simplify_cta(optimized.call_to_action)
        
        # Limit trust signals to top 3
        if len(optimized.trust_signals) > 3:
            optimized.trust_signals = optimized.trust_signals[:3]
        
        # Add mobile-specific urgency
        if optimized.scarcity_trigger:
            optimized.scarcity_trigger = f"📱 {optimized.scarcity_trigger}"
        
        # Mobile-optimized social proof
        if optimized.social_proof and len(optimized.social_proof) > 40:
            optimized.social_proof = self._compress_social_proof(optimized.social_proof)
        
        return optimized
    
    def _create_mobile_hook(self, message: str) -> str:
        """Create punchy mobile hook from longer message"""
        # Extract key words and create hook
        key_words = ['save', 'get', 'free', 'now', 'today', 'exclusive']
        words = message.lower().split()
        
        for key in key_words:
            if key in words:
                return f"🔥 {key.capitalize()} {' '.join(words[words.index(key):words.index(key)+3])}"
        
        # Fallback: use first 40 chars
        return message[:40] + "..."
    
    def _simplify_cta(self, cta: str) -> str:
        """Simplify CTA for mobile"""
        mobile_ctas = {
            'Get Started': 'Start Now →',
            'Learn More': 'See How →',
            'Sign Up Now': 'Join →',
            'Buy Now': 'Get It →',
            'Schedule Consultation': 'Book Call →'
        }
        
        for long_cta, short_cta in mobile_ctas.items():
            if long_cta.lower() in cta.lower():
                return short_cta
        
        # Keep original if no match, but ensure it's short
        return cta if len(cta) <= 15 else cta[:12] + "→"
    
    def _compress_social_proof(self, social_proof: str) -> str:
        """Compress social proof for mobile"""
        # Extract numbers and key phrases
        import re
        numbers = re.findall(r'\d+[kK]?[mM]?', social_proof)
        
        if numbers:
            return f"⭐ {numbers[0]}+ happy customers"
        
        # Fallback
        return social_proof[:35] + "..."

class TabletRenderingStrategy:
    """Tablet-specific content optimization"""
    
    async def optimize(self, content: PersonalizedContent, context: DeviceContext) -> PersonalizedContent:
        """Optimize content for tablet devices"""
        optimized = content.model_copy()
        
        # Tablet gets balanced content - not too short, not too long
        if len(optimized.hero_message) > 80:
            optimized.hero_message = optimized.hero_message[:75] + "..."
        
        # Keep all trust signals but format for tablet
        optimized.trust_signals = [f"✓ {signal}" for signal in optimized.trust_signals]
        
        # Tablet-friendly CTAs
        optimized.call_to_action = f"👆 {optimized.call_to_action}"
        
        return optimized

class DesktopRenderingStrategy:
    """Desktop-specific content optimization"""
    
    async def optimize(self, content: PersonalizedContent, context: DeviceContext) -> PersonalizedContent:
        """Optimize content for desktop devices"""
        optimized = content.model_copy()
        
        # Desktop can handle longer, more detailed content
        
        # Expand trust signals with more detail
        expanded_signals = []
        for signal in optimized.trust_signals:
            if 'guarantee' in signal.lower():
                expanded_signals.append(f"{signal} - No questions asked")
            elif 'certified' in signal.lower():
                expanded_signals.append(f"{signal} - Industry leading standards")
            else:
                expanded_signals.append(signal)
        optimized.trust_signals = expanded_signals
        
        # Add analytical elements to CTA
        if 'BusinessOwner' in content.personalization_strategy:
            optimized.call_to_action = f"{optimized.call_to_action} (ROI Calculator Available)"
        
        # Desktop users appreciate detailed social proof
        if optimized.social_proof and len(optimized.social_proof) < 100:
            optimized.social_proof = f"{optimized.social_proof} - Read detailed case studies"
        
        return optimized

# =============================================================================
# ENHANCED PERSONALIZATION ENGINE
# =============================================================================

class EnhancedPersonalizationEngine:
    """Enhanced personalization engine with Phase 3 improvements"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.persona_detector = PersonaDetector()
        self.device_optimizer = DeviceOptimizer()
        self.personalization_model = ml_model_manager.personalization_model
        self.recommendation_engine = ml_model_manager.recommendation_engine
        self.real_time_optimizer = ml_model_manager.real_time_optimizer
        self.variant_generator = ml_model_manager.variant_generator
        self.performance_tracker = {}
        
    async def generate_personalized_content(self, session: JourneySession, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate personalized content with enhanced persona and device optimization"""
        try:
            logger.info(f"Generating enhanced personalized content for session: {session.session_id}")
            
            # Step 1: Enhanced persona detection
            user_data = await self._gather_user_data(session, context)
            persona_data = await self.persona_detector.detect_persona(user_data)
            
            # Update session with detected persona if confidence is high
            if persona_data.confidence > 0.7:
                session.persona_type = persona_data.type
                await self._update_session_persona(session, persona_data)
            
            # Step 2: Get device context
            device_context = DeviceContext(
                type=DeviceType(session.device_type),
                screen_size=context.get('screen_size'),
                user_agent=context.get('user_agent'),
                connection_speed=context.get('connection_speed', 'wifi')
            )
            
            # Step 3: Generate base personalized content
            base_content = await self._generate_persona_specific_content(session, persona_data, context)
            
            # Step 4: Apply device-specific optimizations
            optimized_content = await self.device_optimizer.optimize_for_device(base_content, device_context)
            
            # Step 5: Apply ML-based enhancements
            ml_enhanced_content = await self._apply_ml_enhancements(optimized_content, session, persona_data)
            
            # Step 6: Record personalization application
            await self._record_enhanced_personalization(session, persona_data, ml_enhanced_content)
            
            logger.info(f"Enhanced personalized content generated: persona={persona_data.type}, device={device_context.type}")
            return ml_enhanced_content
            
        except Exception as e:
            logger.error(f"Error generating enhanced personalized content: {str(e)}")
            return await self._generate_fallback_content(session)
    
    async def _gather_user_data(self, session: JourneySession, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather comprehensive user data for persona detection"""
        user_data = {
            'search_terms': context.get('search_terms', []),
            'page_keywords': context.get('page_keywords', []),
            'interaction_patterns': await self._analyze_interaction_patterns(session),
            'device_type': session.device_type,
            'engagement_metrics': {
                'pages_viewed': session.total_touchpoints,
                'avg_time_per_page': context.get('avg_time_per_page', 60),
                'price_checks': context.get('price_interactions', 0),
                'data_interactions': context.get('data_interactions', 0)
            },
            'referrer': context.get('referrer', ''),
            'utm_source': context.get('utm_source', '')
        }
        
        return user_data
    
    async def _analyze_interaction_patterns(self, session: JourneySession) -> List[str]:
        """Analyze user interaction patterns"""
        patterns = []
        
        # Check cache for interaction history
        cache_key = f"interactions:{session.session_id}"
        interactions = await self.redis_client.get(cache_key)
        
        if interactions:
            interaction_data = json.loads(interactions)
            
            # Analyze patterns
            if interaction_data.get('quick_scroll_count', 0) > 3:
                patterns.append('quick_scroll')
            if interaction_data.get('feature_clicks', 0) > 5:
                patterns.append('feature_exploration')
            if interaction_data.get('comparison_views', 0) > 0:
                patterns.append('spec_comparison')
            if interaction_data.get('review_time', 0) > 120:
                patterns.append('thorough_reading')
            if interaction_data.get('price_checks', 0) > 2:
                patterns.append('price_checking')
        
        return patterns
    
    async def _generate_persona_specific_content(self, session: JourneySession, persona_data: PersonaData, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate content specific to detected persona"""
        persona_type = persona_data.type
        current_stage = session.current_stage
        
        # Use persona-specific content generators
        if persona_type == 'TechEarlyAdopter':
            return await self._generate_tech_adopter_content(session, current_stage, context)
        elif persona_type == 'RemoteDad':
            return await self._generate_remote_dad_content(session, current_stage, context)
        elif persona_type == 'StudentHustler':
            return await self._generate_student_hustler_content(session, current_stage, context)
        elif persona_type == 'BusinessOwner':
            return await self._generate_business_owner_content(session, current_stage, context)
        else:
            return await self._generate_standard_personalization(session, context)
    
    async def _generate_tech_adopter_content(self, session: JourneySession, stage: str, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate content for TechEarlyAdopter persona"""
        if stage == JourneyStage.AWARENESS.value:
            return PersonalizedContent(
                hero_message="🚀 Be First: Next-Gen Tech That's Breaking the Internet",
                call_to_action="Explore Cutting-Edge Features →",
                trust_signals=["Beta Access Available", "Featured on ProductHunt", "GitHub Integration"],
                scarcity_trigger="⚡ Early Bird: 40% OFF for first 100 users",
                social_proof="Join 5K+ tech innovators already using this",
                personalization_strategy="tech_adopter_awareness"
            )
        elif stage == JourneyStage.CONSIDERATION.value:
            return PersonalizedContent(
                hero_message="🔬 Deep Dive: Technical Specs & Performance Benchmarks",
                call_to_action="See Full Tech Stack →",
                trust_signals=["Open Source", "API Documentation", "Developer Community"],
                scarcity_trigger=None,
                social_proof="Recommended by top developers on Reddit",
                personalization_strategy="tech_adopter_consideration"
            )
        else:  # Decision stage
            return PersonalizedContent(
                hero_message="⚡ Ready to Revolutionize Your Workflow?",
                call_to_action="Get Instant Access →",
                trust_signals=["SSL Encrypted", "OAuth Integration", "24/7 Dev Support"],
                scarcity_trigger="🎯 Special: Lifetime Pro Access - 24h only",
                social_proof="CTO of TechCorp: 'Game-changing innovation'",
                personalization_strategy="tech_adopter_decision"
            )
    
    async def _generate_remote_dad_content(self, session: JourneySession, stage: str, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate content for RemoteDad persona"""
        if stage == JourneyStage.AWARENESS.value:
            return PersonalizedContent(
                hero_message="👨‍👩‍👧‍👦 Perfect Work-Life Balance for Remote Parents",
                call_to_action="See How It Works →",
                trust_signals=["Family-Friendly", "Secure & Private", "Recommended by Parents"],
                scarcity_trigger=None,
                social_proof="Trusted by 10K+ remote working parents",
                personalization_strategy="remote_dad_awareness"
            )
        elif stage == JourneyStage.CONSIDERATION.value:
            return PersonalizedContent(
                hero_message="📊 Compare Features: Find What Works for Your Family",
                call_to_action="View Comparison Guide →",
                trust_signals=["30-Day Trial", "No Hidden Fees", "Cancel Anytime"],
                scarcity_trigger=None,
                social_proof="Sarah M.: 'Finally, a solution that understands parents!'",
                personalization_strategy="remote_dad_consideration"
            )
        else:  # Decision stage
            return PersonalizedContent(
                hero_message="🏡 Invest in Your Family's Future Today",
                call_to_action="Start Your Free Trial →",
                trust_signals=["Money-Back Guarantee", "Family Plan Available", "Priority Support"],
                scarcity_trigger="👨‍👩‍👧 Family Special: Save 25% on annual plan",
                social_proof="Join thousands of happy remote-working families",
                personalization_strategy="remote_dad_decision"
            )
    
    async def _generate_student_hustler_content(self, session: JourneySession, stage: str, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate content for StudentHustler persona"""
        if stage == JourneyStage.AWARENESS.value:
            return PersonalizedContent(
                hero_message="💰 Student Special: Turn Your Skills into Cash",
                call_to_action="Get Started Free →",
                trust_signals=["No Credit Card Required", "Student Verified", "Instant Setup"],
                scarcity_trigger="🎓 Student Discount: 60% OFF with .edu email",
                social_proof="5K+ students already earning extra income",
                personalization_strategy="student_hustler_awareness"
            )
        elif stage == JourneyStage.CONSIDERATION.value:
            return PersonalizedContent(
                hero_message="📱 Works Around Your Class Schedule",
                call_to_action="See Success Stories →",
                trust_signals=["Flexible Hours", "Mobile Friendly", "Quick Payouts"],
                scarcity_trigger="⏰ Flash Sale: Extra 20% OFF - Next 2 hours",
                social_proof="Jake earned $500 last month between classes",
                personalization_strategy="student_hustler_consideration"
            )
        else:  # Decision stage
            return PersonalizedContent(
                hero_message="🚀 Start Earning Today - No Experience Needed",
                call_to_action="Claim Student Deal →",
                trust_signals=["PayPal/Venmo Payouts", "Cancel Anytime", "Free Training"],
                scarcity_trigger="💸 TODAY ONLY: Get $20 signup bonus",
                social_proof="Avg student earns $300/month",
                personalization_strategy="student_hustler_decision"
            )
    
    async def _generate_business_owner_content(self, session: JourneySession, stage: str, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate content for BusinessOwner persona"""
        if stage == JourneyStage.AWARENESS.value:
            return PersonalizedContent(
                hero_message="📈 Enterprise Solution: Scale Your Business 10X",
                call_to_action="Request Executive Brief →",
                trust_signals=["Fortune 500 Clients", "SOC 2 Compliant", "Enterprise SLA"],
                scarcity_trigger=None,
                social_proof="Trusted by 200+ industry leaders",
                personalization_strategy="business_owner_awareness"
            )
        elif stage == JourneyStage.CONSIDERATION.value:
            return PersonalizedContent(
                hero_message="💼 ROI Calculator: See Your Potential Returns",
                call_to_action="Calculate Your ROI →",
                trust_signals=["Custom Pricing", "Dedicated Account Manager", "White-Label Options"],
                scarcity_trigger=None,
                social_proof="Average client sees 300% ROI in 6 months",
                personalization_strategy="business_owner_consideration"
            )
        else:  # Decision stage
            return PersonalizedContent(
                hero_message="🎯 Ready to Transform Your Business?",
                call_to_action="Schedule Strategy Call →",
                trust_signals=["Implementation Support", "Training Included", "Success Guarantee"],
                scarcity_trigger="📅 Limited Spots: Free consultation this week",
                social_proof="CEO of GrowthCo: 'Best investment we made this year'",
                personalization_strategy="business_owner_decision"
            )
    
    async def _apply_ml_enhancements(self, content: PersonalizedContent, session: JourneySession, persona_data: PersonaData) -> PersonalizedContent:
        """Apply ML-based content enhancements"""
        try:
            # Prepare features for ML model
            features = {
                'persona_type': persona_data.type,
                'persona_confidence': persona_data.confidence,
                'journey_stage': session.current_stage,
                'device_type': session.device_type,
                'session_duration': (datetime.utcnow() - session.start_timestamp).total_seconds(),
                'conversion_probability': session.conversion_probability
            }
            
            # Get ML recommendations for content optimization
            ml_suggestions = await self.personalization_model.score_variant(features, content.dict())
            
            # Apply high-confidence suggestions
            if ml_suggestions > 0.8:
                # Content is already well-optimized
                return content
            elif ml_suggestions > 0.6:
                # Apply minor enhancements
                content = await self._apply_minor_ml_enhancements(content, features)
            else:
                # Apply major enhancements
                content = await self._apply_major_ml_enhancements(content, features)
            
            return content
            
        except Exception as e:
            logger.error(f"Error applying ML enhancements: {str(e)}")
            return content
    
    async def _apply_minor_ml_enhancements(self, content: PersonalizedContent, features: Dict[str, Any]) -> PersonalizedContent:
        """Apply minor ML-suggested enhancements"""
        enhanced = content.model_copy()
        
        # Add urgency if conversion probability is moderate
        if features['conversion_probability'] > 0.5 and not enhanced.scarcity_trigger:
            enhanced.scarcity_trigger = "🔥 Special Offer: Limited Time Only"
        
        # Strengthen CTA for high engagement
        if features['session_duration'] > 120:
            enhanced.call_to_action = f"⭐ {enhanced.call_to_action}"
        
        return enhanced
    
    async def _apply_major_ml_enhancements(self, content: PersonalizedContent, features: Dict[str, Any]) -> PersonalizedContent:
        """Apply major ML-suggested enhancements"""
        enhanced = content.model_copy()
        
        # Complete content overhaul based on ML insights
        if features['conversion_probability'] < 0.3:
            # Low conversion probability - add strong incentives
            enhanced.hero_message = f"🎁 EXCLUSIVE: {enhanced.hero_message}"
            enhanced.scarcity_trigger = "⚡ 50% OFF - Today Only!"
            enhanced.trust_signals.append("🔒 Risk-Free Trial")
        
        # Adjust for device-specific improvements
        if features['device_type'] == 'mobile' and features['session_duration'] < 30:
            # Quick mobile session - ultra-concise messaging
            enhanced.hero_message = enhanced.hero_message[:30] + " →"
            enhanced.call_to_action = "Tap Here →"
        
        return enhanced
    
    async def _update_session_persona(self, session: JourneySession, persona_data: PersonaData):
        """Update session with detected persona"""
        try:
            stmt = update(JourneySession).where(
                JourneySession.session_id == session.session_id
            ).values(
                persona_type=persona_data.type,
                persona_confidence=persona_data.confidence,
                last_updated=datetime.utcnow()
            )
            await self.db.execute(stmt)
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error updating session persona: {str(e)}")
    
    async def _record_enhanced_personalization(self, session: JourneySession, persona_data: PersonaData, content: PersonalizedContent):
        """Record enhanced personalization data"""
        try:
            # Create unique variant ID
            variant_data = f"{persona_data.type}_{session.device_type}_{content.personalization_strategy}"
            variant_id = hashlib.md5(variant_data.encode()).hexdigest()[:8]
            
            personalization_record = PersonalizationData(
                session_id=session.session_id,
                personalization_type="enhanced_content",
                personalization_strategy=content.personalization_strategy,
                variant_id=variant_id,
                content_delivered=content.dict(),
                ml_model_version="v2.0",
                confidence_score=persona_data.confidence,
                persona_data=persona_data.dict(),
                device_optimization_applied=True
            )
            
            self.db.add(personalization_record)
            await self.db.commit()
            
            # Cache for real-time access
            cache_key = f"enhanced_personalization:{session.session_id}:latest"
            cache_data = {
                'content': content.dict(),
                'persona': persona_data.dict(),
                'timestamp': datetime.utcnow().isoformat()
            }
            await self.redis_client.setex(cache_key, 1800, json.dumps(cache_data))
            
        except Exception as e:
            logger.error(f"Error recording enhanced personalization: {str(e)}")
    
    async def _generate_standard_personalization(self, session: JourneySession, context: Dict[str, Any]) -> PersonalizedContent:
        """Generate standard personalization when persona is unknown"""
        return PersonalizedContent(
            hero_message="Discover the Perfect Solution for You",
            call_to_action="Learn More →",
            trust_signals=["Trusted by Thousands", "5-Star Rated", "Secure & Reliable"],
            social_proof="Join our growing community",
            personalization_strategy="standard_unknown_persona"
        )
    
    async def _generate_fallback_content(self, session: JourneySession) -> PersonalizedContent:
        """Generate fallback content when personalization fails"""
        return PersonalizedContent(
            hero_message="Welcome! Find What You're Looking For",
            call_to_action="Get Started →",
            trust_signals=["Quality Guaranteed", "Expert Support"],
            social_proof="Thousands of satisfied customers",
            personalization_strategy="fallback_content"
        )

# =============================================================================
# INTEGRATION WITH CONTENT ENGINE
# =============================================================================

class ContentEngineIntegration:
    """Integration layer between PersonalizationEngine and ContentEngine"""
    
    def __init__(self, personalization_engine: EnhancedPersonalizationEngine):
        self.personalization_engine = personalization_engine
        self.content_cache = {}
        
    async def get_personalized_content_for_page(self, session: JourneySession, page_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized content for a specific page type"""
        try:
            # Get base personalized content
            personalized_content = await self.personalization_engine.generate_personalized_content(session, context)
            
            # Adapt content for specific page types
            page_content = await self._adapt_content_for_page(personalized_content, page_type, session)
            
            # Add page-specific elements
            page_content['meta'] = await self._generate_page_meta(personalized_content, page_type)
            page_content['structured_data'] = await self._generate_structured_data(session, page_type)
            
            return page_content
            
        except Exception as e:
            logger.error(f"Error getting personalized page content: {str(e)}")
            return self._get_default_page_content(page_type)
    
    async def _adapt_content_for_page(self, content: PersonalizedContent, page_type: str, session: JourneySession) -> Dict[str, Any]:
        """Adapt personalized content for specific page types"""
        base_content = content.dict()
        
        if page_type == 'landing':
            return {
                **base_content,
                'layout': 'hero_centered',
                'sections': ['hero', 'benefits', 'social_proof', 'cta']
            }
        elif page_type == 'product':
            return {
                **base_content,
                'layout': 'product_showcase',
                'sections': ['hero', 'features', 'pricing', 'reviews', 'cta']
            }
        elif page_type == 'checkout':
            return {
                **base_content,
                'layout': 'conversion_focused',
                'sections': ['trust_badges', 'order_summary', 'payment', 'guarantees']
            }
        else:
            return base_content
    
    async def _generate_page_meta(self, content: PersonalizedContent, page_type: str) -> Dict[str, str]:
        """Generate SEO meta tags based on personalized content"""
        base_title = content.hero_message.replace('🔥', '').replace('⚡', '').strip()
        
        return {
            'title': f"{base_title} | {page_type.capitalize()}",
            'description': f"{content.social_proof} {content.call_to_action}",
            'og:title': base_title,
            'og:description': content.social_proof or base_title,
            'twitter:card': 'summary_large_image'
        }
    
    async def _generate_structured_data(self, session: JourneySession, page_type: str) -> Dict[str, Any]:
        """Generate structured data for SEO"""
        return {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': page_type.capitalize(),
            'dateModified': datetime.utcnow().isoformat(),
            'audience': {
                '@type': 'Audience',
                'audienceType': session.persona_type
            }
        }
    
    def _get_default_page_content(self, page_type: str) -> Dict[str, Any]:
        """Get default page content as fallback"""
        return {
            'hero_message': 'Welcome',
            'call_to_action': 'Learn More',
            'trust_signals': ['Secure', 'Trusted'],
            'layout': 'default',
            'sections': ['hero', 'content', 'cta']
        }