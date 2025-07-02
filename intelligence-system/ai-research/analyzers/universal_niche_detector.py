#!/usr/bin/env python3
"""
Universal Niche Detection Engine

Automatically detects and categorizes niches from any opportunity, product, or content.
Works with German and international markets. Fully niche-agnostic.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import re
from datetime import datetime
import spacy
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NicheCategory(Enum):
    """Universal niche categories"""
    FINANCE = "finance"
    HEALTH_FITNESS = "health_fitness"
    TECHNOLOGY = "technology"
    BUSINESS = "business"
    EDUCATION = "education"
    LIFESTYLE = "lifestyle"
    ENTERTAINMENT = "entertainment"
    RELATIONSHIPS = "relationships"
    PERSONAL_DEVELOPMENT = "personal_development"
    FOOD_COOKING = "food_cooking"
    TRAVEL = "travel"
    FASHION_BEAUTY = "fashion_beauty"
    HOME_GARDEN = "home_garden"
    PARENTING = "parenting"
    SPORTS = "sports"
    GAMING = "gaming"
    ARTS_CRAFTS = "arts_crafts"
    AUTOMOTIVE = "automotive"
    PETS = "pets"
    SPIRITUALITY = "spirituality"
    SCIENCE = "science"
    POLITICS = "politics"
    ENVIRONMENT = "environment"
    UNKNOWN = "unknown"

@dataclass
class NicheDetectionResult:
    """Result of niche detection analysis"""
    primary_niche: NicheCategory
    secondary_niches: List[NicheCategory]
    confidence_score: float
    keywords: List[str]
    target_audience: Dict[str, Any]
    market_size: str
    competition_level: str
    trend_direction: str
    monetization_potential: str
    language: str
    regional_focus: List[str]
    sub_niches: List[str]
    related_topics: List[str]

class NicheKeywords:
    """Universal niche keywords in multiple languages"""
    
    KEYWORDS = {
        NicheCategory.FINANCE: {
            'de': ['geld', 'finanzen', 'investment', 'trading', 'aktien', 'krypto', 'bitcoin', 'sparen', 'budget', 'schulden', 'kredit', 'rente', 'versicherung', 'steuern', 'passives einkommen', 'reich werden'],
            'en': ['money', 'finance', 'investment', 'trading', 'stocks', 'crypto', 'bitcoin', 'saving', 'budget', 'debt', 'credit', 'retirement', 'insurance', 'taxes', 'passive income', 'wealth'],
            'context': ['portfolio', 'dividend', 'compound interest', 'financial freedom', 'side hustle', 'cash flow']
        },
        NicheCategory.HEALTH_FITNESS: {
            'de': ['gesundheit', 'fitness', 'abnehmen', 'diät', 'sport', 'training', 'yoga', 'ernährung', 'meditation', 'wellness', 'mental health', 'supplements'],
            'en': ['health', 'fitness', 'weight loss', 'diet', 'workout', 'exercise', 'yoga', 'nutrition', 'meditation', 'wellness', 'mental health', 'supplements'],
            'context': ['transformation', 'mindfulness', 'muscle building', 'cardio', 'strength training', 'healthy lifestyle']
        },
        NicheCategory.TECHNOLOGY: {
            'de': ['technologie', 'software', 'programmieren', 'ki', 'artificial intelligence', 'gadgets', 'apps', 'digitalisierung', 'automation', 'cybersecurity'],
            'en': ['technology', 'software', 'programming', 'ai', 'artificial intelligence', 'gadgets', 'apps', 'digital', 'automation', 'cybersecurity'],
            'context': ['innovation', 'startup', 'saas', 'machine learning', 'blockchain', 'iot', 'cloud computing']
        },
        NicheCategory.BUSINESS: {
            'de': ['business', 'unternehmen', 'startup', 'marketing', 'verkauf', 'kundenservice', 'führung', 'management', 'produktivität', 'erfolg'],
            'en': ['business', 'entrepreneur', 'startup', 'marketing', 'sales', 'customer service', 'leadership', 'management', 'productivity', 'success'],
            'context': ['scaling', 'growth hacking', 'conversion', 'branding', 'networking', 'B2B', 'B2C']
        },
        NicheCategory.EDUCATION: {
            'de': ['bildung', 'lernen', 'kurs', 'training', 'schule', 'universität', 'weiterbildung', 'sprachen', 'fähigkeiten', 'zertifizierung'],
            'en': ['education', 'learning', 'course', 'training', 'school', 'university', 'skills', 'certification', 'language', 'knowledge'],
            'context': ['online learning', 'skill development', 'professional development', 'tutorial', 'masterclass']
        },
        NicheCategory.LIFESTYLE: {
            'de': ['lifestyle', 'leben', 'freizeit', 'hobby', 'mode', 'design', 'wohnen', 'reisen', 'unterhaltung', 'kultur'],
            'en': ['lifestyle', 'living', 'leisure', 'hobby', 'fashion', 'design', 'home', 'travel', 'entertainment', 'culture'],
            'context': ['minimalism', 'luxury', 'sustainable living', 'work-life balance', 'self-care']
        },
        NicheCategory.PERSONAL_DEVELOPMENT: {
            'de': ['persönlichkeitsentwicklung', 'selbstverbesserung', 'motivation', 'mindset', 'erfolg', 'ziele', 'produktivität', 'selbstvertrauen'],
            'en': ['personal development', 'self improvement', 'motivation', 'mindset', 'success', 'goals', 'productivity', 'confidence'],
            'context': ['self-help', 'life coaching', 'habits', 'time management', 'goal setting', 'mindfulness']
        }
    }

class UniversalNicheDetector:
    """Universal niche detection engine that works with any content or opportunity"""
    
    def __init__(self, openai_api_key: str = None, claude_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.claude_api_key = claude_api_key
        
        # Initialize NLP models
        try:
            self.nlp_de = spacy.load("de_core_news_sm")
        except OSError:
            logger.warning("German spaCy model not found, using English")
            self.nlp_de = None
            
        try:
            self.nlp_en = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("English spaCy model not found")
            self.nlp_en = None
        
        # Initialize ML models
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 3)
        )
        
        # Initialize AI models
        if openai_api_key:
            self.openai_llm = ChatOpenAI(
                openai_api_key=openai_api_key,
                model_name="gpt-4",
                temperature=0.1
            )
        else:
            self.openai_llm = None
            
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
    
    def detect_language(self, text: str) -> str:
        """Detect the primary language of the text"""
        try:
            import langdetect
            return langdetect.detect(text)
        except:
            # Fallback: simple heuristic
            german_words = ['der', 'die', 'das', 'und', 'ich', 'ist', 'nicht', 'mit', 'für', 'auf', 'ein', 'eine']
            english_words = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was']
            
            text_lower = text.lower()
            german_count = sum(1 for word in german_words if word in text_lower)
            english_count = sum(1 for word in english_words if word in text_lower)
            
            return 'de' if german_count > english_count else 'en'
    
    def extract_keywords(self, text: str, language: str = 'en') -> List[str]:
        """Extract relevant keywords from text using NLP"""
        if not text:
            return []
        
        # Use appropriate spaCy model
        nlp = self.nlp_de if language == 'de' and self.nlp_de else self.nlp_en
        if not nlp:
            # Fallback to simple tokenization
            stop_words = set(stopwords.words('german' if language == 'de' else 'english'))
            tokens = word_tokenize(text.lower())
            keywords = [token for token in tokens if token.isalpha() and token not in stop_words and len(token) > 2]
            return keywords[:20]
        
        doc = nlp(text)
        
        # Extract entities, nouns, and important phrases
        keywords = []
        
        # Named entities
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']:
                keywords.append(ent.text.lower())
        
        # Important nouns and adjectives
        for token in doc:
            if (token.pos_ in ['NOUN', 'ADJ'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                keywords.append(token.lemma_.lower())
        
        # Noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:
                keywords.append(chunk.text.lower())
        
        return list(set(keywords))[:20]
    
    def calculate_keyword_scores(self, keywords: List[str], language: str = 'en') -> Dict[NicheCategory, float]:
        """Calculate niche scores based on keyword matching"""
        scores = {niche: 0.0 for niche in NicheCategory}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            for niche, niche_keywords in NicheKeywords.KEYWORDS.items():
                # Check direct language match
                lang_keywords = niche_keywords.get(language, [])
                if any(nk in keyword_lower or keyword_lower in nk for nk in lang_keywords):
                    scores[niche] += 2.0
                
                # Check context keywords
                context_keywords = niche_keywords.get('context', [])
                if any(ck in keyword_lower or keyword_lower in ck for ck in context_keywords):
                    scores[niche] += 1.5
                
                # Check other language for broader coverage
                other_lang = 'en' if language == 'de' else 'de'
                other_keywords = niche_keywords.get(other_lang, [])
                if any(ok in keyword_lower or keyword_lower in ok for ok in other_keywords):
                    scores[niche] += 1.0
        
        # Normalize scores
        max_score = max(scores.values()) if scores.values() else 1
        if max_score > 0:
            scores = {niche: score / max_score for niche, score in scores.items()}
        
        return scores
    
    async def ai_enhanced_detection(self, text: str, keywords: List[str], language: str = 'en') -> Dict[str, Any]:
        """Use AI to enhance niche detection with deeper analysis"""
        if not self.openai_llm:
            return {}
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"""You are an expert market analyst and niche detection specialist.
            
            Analyze the following content and provide detailed insights:
            
            Language: {language}
            
            Your task:
            1. Identify the primary niche/market category
            2. Identify 2-3 secondary niches
            3. Determine target audience demographics
            4. Assess market size (Small/Medium/Large)
            5. Evaluate competition level (Low/Medium/High)
            6. Analyze trend direction (Growing/Stable/Declining)
            7. Rate monetization potential (Low/Medium/High)
            8. Identify regional focus areas
            9. List 3-5 specific sub-niches
            10. Suggest related topics for content expansion
            
            Respond in JSON format with these exact keys:
            - primary_niche: string
            - secondary_niches: array of strings
            - target_audience: object with age_range, gender, interests, pain_points
            - market_size: string
            - competition_level: string
            - trend_direction: string
            - monetization_potential: string
            - regional_focus: array of strings
            - sub_niches: array of strings
            - related_topics: array of strings
            - confidence_score: number (0-1)
            """),
            HumanMessage(content=f"Content to analyze:\n\n{text}\n\nExtracted keywords: {', '.join(keywords)}")
        ])
        
        try:
            response = await self.openai_llm.apredict_messages(prompt.format_messages())
            
            # Parse JSON response
            content = response.content
            # Extract JSON from response if it's wrapped in markdown
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            return json.loads(content.strip())
            
        except Exception as e:
            logger.error(f"AI enhancement failed: {e}")
            return {}
    
    def analyze_content_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze content patterns to better understand the niche"""
        patterns = {
            'content_type': self._detect_content_type(text),
            'emotional_tone': self._analyze_emotional_tone(text),
            'complexity_level': self._assess_complexity(text),
            'audience_sophistication': self._assess_audience_sophistication(text),
            'call_to_action_strength': self._analyze_cta_strength(text),
            'urgency_level': self._detect_urgency_signals(text),
            'social_proof_presence': self._detect_social_proof(text),
            'problem_solution_focus': self._analyze_problem_solution_focus(text)
        }
        
        return patterns
    
    def _detect_content_type(self, text: str) -> str:
        """Detect the type of content (educational, sales, entertainment, etc.)"""
        sales_indicators = ['buy', 'purchase', 'order', 'limited time', 'discount', 'offer', 'deal']
        educational_indicators = ['learn', 'discover', 'understand', 'guide', 'tutorial', 'step-by-step']
        entertainment_indicators = ['funny', 'hilarious', 'amazing', 'incredible', 'shocking', 'unbelievable']
        
        text_lower = text.lower()
        
        sales_score = sum(1 for indicator in sales_indicators if indicator in text_lower)
        educational_score = sum(1 for indicator in educational_indicators if indicator in text_lower)
        entertainment_score = sum(1 for indicator in entertainment_indicators if indicator in text_lower)
        
        if sales_score > educational_score and sales_score > entertainment_score:
            return 'sales'
        elif educational_score > entertainment_score:
            return 'educational'
        elif entertainment_score > 0:
            return 'entertainment'
        else:
            return 'informational'
    
    def _analyze_emotional_tone(self, text: str) -> str:
        """Analyze the emotional tone of the content"""
        positive_words = ['great', 'amazing', 'excellent', 'wonderful', 'fantastic', 'love', 'best', 'perfect']
        negative_words = ['problem', 'issue', 'mistake', 'wrong', 'bad', 'worst', 'hate', 'terrible']
        urgency_words = ['now', 'urgent', 'immediate', 'quickly', 'fast', 'hurry', 'limited', 'deadline']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        
        if urgency_count > 2:
            return 'urgent'
        elif positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _assess_complexity(self, text: str) -> str:
        """Assess the complexity level of the content"""
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        complex_words = ['implementation', 'methodology', 'sophisticated', 'comprehensive', 'analyze', 'evaluate']
        complex_count = sum(1 for word in complex_words if word in text.lower())
        
        if avg_sentence_length > 20 or complex_count > 3:
            return 'high'
        elif avg_sentence_length > 10 or complex_count > 1:
            return 'medium'
        else:
            return 'low'
    
    def _assess_audience_sophistication(self, text: str) -> str:
        """Assess the target audience sophistication level"""
        beginner_indicators = ['basic', 'simple', 'easy', 'beginner', 'start', 'introduction', 'first time']
        advanced_indicators = ['advanced', 'expert', 'professional', 'sophisticated', 'complex', 'detailed']
        
        text_lower = text.lower()
        
        beginner_count = sum(1 for indicator in beginner_indicators if indicator in text_lower)
        advanced_count = sum(1 for indicator in advanced_indicators if indicator in text_lower)
        
        if advanced_count > beginner_count:
            return 'advanced'
        elif beginner_count > 0:
            return 'beginner'
        else:
            return 'intermediate'
    
    def _analyze_cta_strength(self, text: str) -> str:
        """Analyze the strength of call-to-action elements"""
        strong_cta = ['buy now', 'order today', 'get started', 'sign up', 'download now', 'claim your']
        weak_cta = ['check out', 'learn more', 'find out', 'discover', 'explore']
        
        text_lower = text.lower()
        
        strong_count = sum(1 for cta in strong_cta if cta in text_lower)
        weak_count = sum(1 for cta in weak_cta if cta in text_lower)
        
        if strong_count > 0:
            return 'strong'
        elif weak_count > 0:
            return 'weak'
        else:
            return 'none'
    
    def _detect_urgency_signals(self, text: str) -> str:
        """Detect urgency signals in the content"""
        urgency_signals = ['limited time', 'expires', 'deadline', 'hurry', 'act fast', 'only', 'last chance']
        
        text_lower = text.lower()
        urgency_count = sum(1 for signal in urgency_signals if signal in text_lower)
        
        if urgency_count >= 3:
            return 'high'
        elif urgency_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _detect_social_proof(self, text: str) -> bool:
        """Detect presence of social proof elements"""
        social_proof_indicators = ['testimonial', 'review', 'customer', 'client', 'success story', 'case study', 'rating']
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in social_proof_indicators)
    
    def _analyze_problem_solution_focus(self, text: str) -> str:
        """Analyze whether content focuses on problems or solutions"""
        problem_words = ['problem', 'issue', 'challenge', 'difficulty', 'struggle', 'pain', 'frustration']
        solution_words = ['solution', 'fix', 'solve', 'answer', 'resolve', 'help', 'improve']
        
        text_lower = text.lower()
        
        problem_count = sum(1 for word in problem_words if word in text_lower)
        solution_count = sum(1 for word in solution_words if word in text_lower)
        
        if solution_count > problem_count:
            return 'solution_focused'
        elif problem_count > solution_count:
            return 'problem_focused'
        else:
            return 'balanced'
    
    async def detect_niche(self, content: str, additional_context: str = "") -> NicheDetectionResult:
        """Main method to detect niche from any content"""
        
        # Combine content and context
        full_text = f"{content} {additional_context}".strip()
        
        if not full_text:
            return NicheDetectionResult(
                primary_niche=NicheCategory.UNKNOWN,
                secondary_niches=[],
                confidence_score=0.0,
                keywords=[],
                target_audience={},
                market_size="unknown",
                competition_level="unknown",
                trend_direction="unknown",
                monetization_potential="unknown",
                language="en",
                regional_focus=[],
                sub_niches=[],
                related_topics=[]
            )
        
        # Detect language
        language = self.detect_language(full_text)
        
        # Extract keywords
        keywords = self.extract_keywords(full_text, language)
        
        # Calculate keyword-based scores
        keyword_scores = self.calculate_keyword_scores(keywords, language)
        
        # Analyze content patterns
        content_patterns = self.analyze_content_patterns(full_text)
        
        # Get AI-enhanced analysis
        ai_analysis = await self.ai_enhanced_detection(full_text, keywords, language)
        
        # Determine primary niche
        primary_niche = max(keyword_scores, key=keyword_scores.get)
        primary_score = keyword_scores[primary_niche]
        
        # If keyword matching didn't find a strong match, try to infer from AI analysis
        if primary_score < 0.3 and ai_analysis.get('primary_niche'):
            try:
                ai_primary = ai_analysis['primary_niche'].lower().replace(' ', '_').replace('-', '_')
                for niche in NicheCategory:
                    if niche.value in ai_primary or ai_primary in niche.value:
                        primary_niche = niche
                        primary_score = ai_analysis.get('confidence_score', 0.5)
                        break
            except:
                pass
        
        # Determine secondary niches
        secondary_niches = []
        sorted_scores = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        for niche, score in sorted_scores[1:4]:  # Top 3 after primary
            if score > 0.2 and niche != primary_niche:
                secondary_niches.append(niche)
        
        # Build result
        result = NicheDetectionResult(
            primary_niche=primary_niche,
            secondary_niches=secondary_niches,
            confidence_score=max(primary_score, ai_analysis.get('confidence_score', 0.0)),
            keywords=keywords,
            target_audience=ai_analysis.get('target_audience', {}),
            market_size=ai_analysis.get('market_size', 'unknown'),
            competition_level=ai_analysis.get('competition_level', 'unknown'),
            trend_direction=ai_analysis.get('trend_direction', 'unknown'),
            monetization_potential=ai_analysis.get('monetization_potential', 'unknown'),
            language=language,
            regional_focus=ai_analysis.get('regional_focus', []),
            sub_niches=ai_analysis.get('sub_niches', []),
            related_topics=ai_analysis.get('related_topics', [])
        )
        
        return result
    
    async def analyze_opportunity_niche(self, opportunity_data: Dict[str, Any]) -> NicheDetectionResult:
        """Analyze niche from opportunity data structure"""
        
        # Extract relevant text from opportunity data
        content_parts = []
        
        # Common opportunity fields
        if 'title' in opportunity_data:
            content_parts.append(opportunity_data['title'])
        if 'description' in opportunity_data:
            content_parts.append(opportunity_data['description'])
        if 'category' in opportunity_data:
            content_parts.append(opportunity_data['category'])
        if 'tags' in opportunity_data:
            content_parts.extend(opportunity_data['tags'])
        if 'keywords' in opportunity_data:
            content_parts.extend(opportunity_data['keywords'])
        
        # Platform-specific fields
        if 'product_name' in opportunity_data:
            content_parts.append(opportunity_data['product_name'])
        if 'vendor' in opportunity_data:
            content_parts.append(opportunity_data['vendor'])
        if 'niche' in opportunity_data:
            content_parts.append(opportunity_data['niche'])
        
        content = ' '.join(str(part) for part in content_parts if part)
        
        # Add additional context
        additional_context = ""
        if 'platform' in opportunity_data:
            additional_context += f"Platform: {opportunity_data['platform']} "
        if 'commission_rate' in opportunity_data:
            additional_context += f"Commission: {opportunity_data['commission_rate']} "
        if 'price' in opportunity_data:
            additional_context += f"Price: {opportunity_data['price']} "
        
        return await self.detect_niche(content, additional_context)

# Example usage and testing
if __name__ == "__main__":
    async def test_niche_detection():
        # Initialize detector
        detector = UniversalNicheDetector()
        
        # Test cases
        test_cases = [
            {
                'content': 'Learn how to make money online with cryptocurrency trading. Bitcoin and Ethereum strategies for passive income.',
                'expected': NicheCategory.FINANCE
            },
            {
                'content': 'Transform your body in 30 days with this fitness program. Lose weight, build muscle, and improve your health.',
                'expected': NicheCategory.HEALTH_FITNESS
            },
            {
                'content': 'Programmierkurs für Anfänger: Lerne Python und Web-Entwicklung. Künstliche Intelligenz und Machine Learning.',
                'expected': NicheCategory.TECHNOLOGY
            },
            {
                'content': 'Start your own business and become an entrepreneur. Marketing strategies for small business success.',
                'expected': NicheCategory.BUSINESS
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n--- Test Case {i+1} ---")
            print(f"Content: {test_case['content']}")
            
            result = await detector.detect_niche(test_case['content'])
            
            print(f"Detected Niche: {result.primary_niche}")
            print(f"Expected: {test_case['expected']}")
            print(f"Confidence: {result.confidence_score:.2f}")
            print(f"Keywords: {result.keywords[:5]}")
            print(f"Language: {result.language}")
            print(f"Secondary Niches: {[n.value for n in result.secondary_niches]}")
            
            if result.target_audience:
                print(f"Target Audience: {result.target_audience}")
            
            print(f"Match: {'✓' if result.primary_niche == test_case['expected'] else '✗'}")
    
    # Run tests
    asyncio.run(test_niche_detection())