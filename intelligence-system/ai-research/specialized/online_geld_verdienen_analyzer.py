#!/usr/bin/env python3
"""
Online Geld Verdienen Analyzer

Specialized analyzer for the German "Online Geld Verdienen" (Make Money Online) niche.
Focuses on German-specific strategies, influencers, and market dynamics.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import re

# Import base analyzers
import sys
sys.path.append(str(Path(__file__).parent.parent))
from analyzers.universal_niche_detector import UniversalNicheDetector, NicheDetectionResult
from analyzers.universal_creator_analyzer import UniversalCreatorAnalyzer, CreatorProfile, Platform
from analyzers.universal_pattern_extractor import UniversalPatternExtractor, PatternAnalysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OnlineGeldVerdienenCategory(Enum):
    """Categories within Online Geld Verdienen niche"""
    AFFILIATE_MARKETING = "affiliate_marketing"
    DROPSHIPPING = "dropshipping"
    ONLINE_BUSINESS = "online_business"
    TRADING_FOREX = "trading_forex"
    KRYPTO_TRADING = "krypto_trading"
    COACHING_CONSULTING = "coaching_consulting"
    DIGITALE_PRODUKTE = "digitale_produkte"
    PASSIVES_EINKOMMEN = "passives_einkommen"
    AMAZON_FBA = "amazon_fba"
    SOCIAL_MEDIA_MARKETING = "social_media_marketing"
    ONLINE_KURSE = "online_kurse"
    NETWORK_MARKETING = "network_marketing"

class GermanMarketTrend(Enum):
    """Current trends in German online money-making market"""
    KI_AUTOMATION = "ki_automation"
    NACHHALTIGKEIT = "nachhaltigkeit"
    PERSONLICHKEITSENTWICKLUNG = "personlichkeitsentwicklung"
    COMMUNITY_BUILDING = "community_building"
    VIDEO_CONTENT = "video_content"
    KURZE_AUFMERKSAMKEIT = "kurze_aufmerksamkeit"
    VERTRAUEN_AUTHENTIZITAT = "vertrauen_authentizitat"
    MOBILE_FIRST = "mobile_first"

@dataclass
class OnlineGeldVerdienenInfluencer:
    """Specialized influencer profile for Online Geld Verdienen niche"""
    # Basic Info
    name: str
    handle: str
    platforms: List[Platform]
    primary_platform: Platform
    
    # Metrics
    followers: Dict[str, int]
    engagement_rate: float
    estimated_monthly_revenue: float
    
    # Niche Specialization
    ogv_category: OnlineGeldVerdienenCategory
    sub_categories: List[OnlineGeldVerdienenCategory]
    target_audience: str  # Anfänger, Fortgeschrittene, Experten
    
    # German Market Specifics
    german_market_focus: float  # 0-1 how much they focus on German market
    uses_german_language: bool
    understands_german_regulations: bool
    german_payment_methods: List[str]
    
    # Business Model
    main_revenue_streams: List[str]
    pricing_tiers: Dict[str, float]
    customer_lifetime_value: float
    
    # Content Strategy
    content_pillars: List[str]
    posting_schedule: Dict[str, str]  # platform -> frequency
    content_quality_score: float
    
    # Current Strategies (2024/2025)
    trending_hooks: List[str]
    new_platform_strategies: List[str]
    ai_integration: List[str]
    community_strategies: List[str]
    
    # Success Metrics
    conversion_funnel_performance: Dict[str, float]
    customer_satisfaction_indicators: List[str]
    market_authority_score: float
    
    # Innovation & Trends
    pioneering_strategies: List[str]
    trend_adoption_speed: str  # early, fast, slow
    market_prediction_accuracy: float

@dataclass
class OnlineGeldVerdienenStrategy:
    """Specialized strategy for German online money-making market"""
    strategy_name: str
    category: OnlineGeldVerdienenCategory
    description: str
    
    # German Market Fit
    german_market_suitability: float
    regulatory_compliance: Dict[str, bool]
    cultural_fit_score: float
    
    # Implementation
    startup_cost: float
    time_to_first_euro: str
    scalability_rating: float
    difficulty_level: str  # Anfänger, Mittel, Fortgeschritten
    
    # Performance
    average_monthly_earnings: Dict[str, float]  # Anfänger, Fortgeschritten, Experte
    success_rate: float
    market_saturation: float
    
    # Requirements
    required_skills: List[str]
    required_tools: List[str]
    required_investment: float
    
    # Trends & Future
    trend_direction: str  # steigend, stabil, fallend
    ai_disruption_risk: float
    future_potential: float
    
    # Success Factors
    critical_success_factors: List[str]
    common_failure_points: List[str]
    optimization_opportunities: List[str]

class OnlineGeldVerdienenAnalyzer:
    """Specialized analyzer for German Online Geld Verdienen market"""
    
    def __init__(self, 
                 openai_api_key: str = None,
                 youtube_api_key: str = None):
        
        # Initialize base analyzers
        self.niche_detector = UniversalNicheDetector(openai_api_key)
        self.creator_analyzer = UniversalCreatorAnalyzer(youtube_api_key, openai_api_key)
        self.pattern_extractor = UniversalPatternExtractor(openai_api_key)
        
        # German-specific configurations
        self.german_keywords = self._load_german_keywords()
        self.german_platforms = self._configure_german_platforms()
        self.german_regulations = self._load_german_regulations()
        
        # Database setup
        self.database_path = self._get_database_path()
        self._initialize_ogv_database()
        
        # Analysis cache
        self.analysis_cache = {}
        
    def _get_database_path(self) -> str:
        """Get database path for OGV analysis"""
        base_path = Path(__file__).parent.parent.parent
        db_path = base_path / "databases" / "online_geld_verdienen.db"
        db_path.parent.mkdir(exist_ok=True)
        return str(db_path)
    
    def _initialize_ogv_database(self):
        """Initialize specialized database for OGV analysis"""
        
        schema_sql = """
        CREATE TABLE IF NOT EXISTS ogv_influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            handle TEXT,
            primary_platform TEXT,
            ogv_category TEXT,
            german_market_focus REAL,
            estimated_revenue REAL,
            followers_data TEXT, -- JSON
            content_strategy TEXT, -- JSON
            current_strategies_2024 TEXT, -- JSON
            performance_metrics TEXT, -- JSON
            market_analysis TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS ogv_strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_name TEXT NOT NULL,
            category TEXT,
            german_suitability REAL,
            startup_cost REAL,
            avg_monthly_earnings REAL,
            success_rate REAL,
            market_saturation REAL,
            strategy_data TEXT, -- JSON
            performance_data TEXT, -- JSON
            requirements_data TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS ogv_market_trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trend_name TEXT NOT NULL,
            trend_type TEXT,
            trend_strength REAL,
            german_relevance REAL,
            adoption_rate REAL,
            trend_data TEXT, -- JSON
            prediction_data TEXT, -- JSON
            first_observed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS ogv_success_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_name TEXT NOT NULL,
            pattern_type TEXT,
            effectiveness_score REAL,
            german_specific BOOLEAN,
            pattern_data TEXT, -- JSON
            usage_examples TEXT, -- JSON
            success_metrics TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS ogv_analysis_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            analysis_type TEXT,
            focus_category TEXT,
            influencers_analyzed INTEGER,
            strategies_identified INTEGER,
            patterns_extracted INTEGER,
            session_data TEXT, -- JSON
            results_summary TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_ogv_influencers_category ON ogv_influencers(ogv_category);
        CREATE INDEX IF NOT EXISTS idx_ogv_influencers_german_focus ON ogv_influencers(german_market_focus);
        CREATE INDEX IF NOT EXISTS idx_ogv_strategies_category ON ogv_strategies(category);
        CREATE INDEX IF NOT EXISTS idx_ogv_strategies_suitability ON ogv_strategies(german_suitability);
        CREATE INDEX IF NOT EXISTS idx_ogv_trends_strength ON ogv_market_trends(trend_strength);
        CREATE INDEX IF NOT EXISTS idx_ogv_patterns_effectiveness ON ogv_success_patterns(effectiveness_score);
        """
        
        with sqlite3.connect(self.database_path) as conn:
            conn.executescript(schema_sql)
    
    def _load_german_keywords(self) -> Dict[str, List[str]]:
        """Load German-specific keywords for OGV niche"""
        
        return {
            'general': [
                'online geld verdienen', 'geld verdienen im internet', 'nebeneinkommen online',
                'passives einkommen', 'finanzielle freiheit', 'online business aufbauen',
                'geld verdienen von zuhause', 'internet marketing', 'affiliate marketing',
                'dropshipping deutschland', 'online shop erstellen', 'digitale nomaden'
            ],
            'affiliate_marketing': [
                'affiliate marketing deutsch', 'partnerprogramme', 'provisionen verdienen',
                'digistore24', 'amazon partnerprogramm', 'affiliate links', 'performance marketing'
            ],
            'trading': [
                'forex trading', 'cfd trading', 'krypto trading', 'bitcoin verdienen',
                'trading strategien', 'daytrading', 'swing trading', 'investieren lernen'
            ],
            'business': [
                'online business', 'startup gründen', 'selbstständig machen',
                'digitale produkte verkaufen', 'online kurse erstellen', 'coaching business'
            ],
            'ecommerce': [
                'dropshipping', 'amazon fba', 'online shop', 'ebay verkaufen',
                'etsy shop', 'print on demand', 'product research'
            ],
            'content': [
                'youtube geld verdienen', 'instagram monetarisierung', 'tiktok creator fund',
                'influencer werden', 'social media marketing', 'content creator'
            ]
        }
    
    def _configure_german_platforms(self) -> Dict[Platform, Dict[str, Any]]:
        """Configure platform-specific settings for German market"""
        
        return {
            Platform.YOUTUBE: {
                'language_preference': 'de',
                'regional_focus': 'DACH',
                'monetization_threshold': 1000,  # subscribers
                'typical_cpm': 2.5,  # EUR
                'best_posting_times': ['18:00', '20:00', '21:00']
            },
            Platform.INSTAGRAM: {
                'language_preference': 'de',
                'regional_focus': 'DACH',
                'monetization_threshold': 10000,  # followers
                'engagement_benchmark': 3.5,  # %
                'best_posting_times': ['12:00', '17:00', '19:00']
            },
            Platform.TIKTOK: {
                'language_preference': 'de',
                'regional_focus': 'DACH',
                'monetization_threshold': 10000,  # followers
                'engagement_benchmark': 8.0,  # %
                'best_posting_times': ['16:00', '18:00', '20:00']
            },
            Platform.LINKEDIN: {
                'language_preference': 'de',
                'regional_focus': 'DACH',
                'monetization_threshold': 5000,  # connections
                'engagement_benchmark': 2.0,  # %
                'best_posting_times': ['08:00', '12:00', '17:00']
            }
        }
    
    def _load_german_regulations(self) -> Dict[str, Any]:
        """Load German legal and regulatory requirements"""
        
        return {
            'impressum_required': True,
            'datenschutz_required': True,
            'affiliate_disclosure_required': True,
            'tax_implications': {
                'gewerbeanmeldung_threshold': 410,  # EUR per year
                'umsatzsteuer_threshold': 22000,  # EUR per year
                'freiberufler_options': ['coaching', 'consulting', 'content_creation']
            },
            'restricted_markets': ['gambling', 'forex_retail', 'crypto_advice'],
            'payment_methods': ['sepa', 'paypal', 'klarna', 'sofort', 'giropay'],
            'gdpr_compliance': True,
            'advertising_restrictions': {
                'financial_products': 'strict',
                'health_claims': 'strict',
                'get_rich_quick': 'prohibited'
            }
        }
    
    async def analyze_ogv_market_comprehensive(self) -> Dict[str, Any]:
        """Comprehensive analysis of the German Online Geld Verdienen market"""
        
        logger.info("Starting comprehensive OGV market analysis...")
        
        session_id = f"ogv_comprehensive_{int(datetime.now().timestamp())}"
        
        try:
            # 1. Discover top OGV influencers
            influencers = await self._discover_ogv_influencers()
            
            # 2. Analyze current strategies
            strategies = await self._analyze_ogv_strategies()
            
            # 3. Identify market trends
            trends = await self._identify_ogv_trends()
            
            # 4. Extract success patterns
            patterns = await self._extract_ogv_success_patterns(influencers)
            
            # 5. Market opportunity analysis
            opportunities = await self._analyze_market_opportunities()
            
            # 6. Competitive landscape
            competition = await self._analyze_competitive_landscape(influencers)
            
            # 7. Generate insights and recommendations
            insights = await self._generate_ogv_insights(
                influencers, strategies, trends, patterns, opportunities, competition
            )
            
            # Save analysis session
            await self._save_analysis_session(
                session_id, 'comprehensive', 'all_categories',
                len(influencers), len(strategies), len(patterns),
                {
                    'influencers': influencers,
                    'strategies': strategies,
                    'trends': trends,
                    'patterns': patterns,
                    'opportunities': opportunities,
                    'competition': competition
                },
                insights
            )
            
            logger.info(f"Comprehensive OGV analysis completed: {session_id}")
            
            return {
                'session_id': session_id,
                'analysis_type': 'comprehensive',
                'market_overview': {
                    'total_influencers': len(influencers),
                    'active_strategies': len(strategies),
                    'trending_patterns': len(patterns),
                    'market_opportunities': len(opportunities)
                },
                'top_influencers': influencers[:10],
                'trending_strategies': strategies[:5],
                'market_trends': trends,
                'success_patterns': patterns,
                'opportunities': opportunities,
                'competitive_analysis': competition,
                'insights_and_recommendations': insights,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Comprehensive OGV analysis failed: {e}")
            raise
    
    async def _discover_ogv_influencers(self) -> List[OnlineGeldVerdienenInfluencer]:
        """Discover top Online Geld Verdienen influencers"""
        
        logger.info("Discovering OGV influencers...")
        
        influencers = []
        
        # Search for influencers in each OGV category
        for category in OnlineGeldVerdienenCategory:
            category_keywords = self._get_category_keywords(category)
            
            for platform in [Platform.YOUTUBE, Platform.INSTAGRAM, Platform.TIKTOK]:
                try:
                    # Use the universal creator analyzer
                    niche_insights = await self.creator_analyzer.get_niche_creator_insights(
                        niche=' '.join(category_keywords[:3]),
                        language='de'
                    )
                    
                    # Convert to OGV-specific profiles
                    for creator in niche_insights.top_creators[:5]:  # Top 5 per category/platform
                        ogv_influencer = await self._convert_to_ogv_influencer(creator, category)
                        if ogv_influencer:
                            influencers.append(ogv_influencer)
                    
                except Exception as e:
                    logger.warning(f"Failed to discover influencers for {category.value} on {platform.value}: {e}")
                    continue
        
        # Remove duplicates and rank by relevance
        unique_influencers = self._deduplicate_influencers(influencers)
        ranked_influencers = self._rank_influencers_by_ogv_relevance(unique_influencers)
        
        logger.info(f"Discovered {len(ranked_influencers)} unique OGV influencers")
        
        return ranked_influencers[:50]  # Top 50
    
    async def _analyze_ogv_strategies(self) -> List[OnlineGeldVerdienenStrategy]:
        """Analyze current OGV strategies in the German market"""
        
        logger.info("Analyzing OGV strategies...")
        
        strategies = []
        
        # Define current 2024/2025 strategies
        strategy_templates = [
            {
                'name': 'AI-gestütztes Affiliate Marketing',
                'category': OnlineGeldVerdienenCategory.AFFILIATE_MARKETING,
                'description': 'Verwendung von KI-Tools für Content-Erstellung und Optimierung',
                'startup_cost': 200.0,
                'time_to_first_euro': '2-4 Wochen',
                'difficulty': 'Mittel'
            },
            {
                'name': 'TikTok Dropshipping mit deutschen Lieferanten',
                'category': OnlineGeldVerdienenCategory.DROPSHIPPING,
                'description': 'Kurze Video-Ads auf TikTok mit lokalen Fulfillment-Partnern',
                'startup_cost': 1000.0,
                'time_to_first_euro': '1-3 Wochen',
                'difficulty': 'Mittel'
            },
            {
                'name': 'Digitale Coaching-Programme mit Community',
                'category': OnlineGeldVerdienenCategory.COACHING_CONSULTING,
                'description': 'Online-Kurse kombiniert mit exklusiven Community-Zugang',
                'startup_cost': 500.0,
                'time_to_first_euro': '4-8 Wochen',
                'difficulty': 'Fortgeschritten'
            },
            {
                'name': 'Krypto-Education mit Compliance-Focus',
                'category': OnlineGeldVerdienenCategory.KRYPTO_TRADING,
                'description': 'Bildungsbasierte Krypto-Inhalte unter Beachtung deutscher Regulierung',
                'startup_cost': 100.0,
                'time_to_first_euro': '6-12 Wochen',
                'difficulty': 'Fortgeschritten'
            },
            {
                'name': 'Nachhaltige Online-Business-Modelle',
                'category': OnlineGeldVerdienenCategory.ONLINE_BUSINESS,
                'description': 'ESG-konforme Geschäftsmodelle mit Nachhaltigkeitsfokus',
                'startup_cost': 800.0,
                'time_to_first_euro': '8-16 Wochen',
                'difficulty': 'Fortgeschritten'
            }
        ]
        
        # Create detailed strategy objects
        for template in strategy_templates:
            strategy = OnlineGeldVerdienenStrategy(
                strategy_name=template['name'],
                category=template['category'],
                description=template['description'],
                german_market_suitability=self._calculate_german_suitability(template),
                regulatory_compliance=self._assess_regulatory_compliance(template),
                cultural_fit_score=self._assess_cultural_fit(template),
                startup_cost=template['startup_cost'],
                time_to_first_euro=template['time_to_first_euro'],
                scalability_rating=self._assess_scalability(template),
                difficulty_level=template['difficulty'],
                average_monthly_earnings=self._estimate_earnings(template),
                success_rate=self._estimate_success_rate(template),
                market_saturation=self._assess_market_saturation(template),
                required_skills=self._identify_required_skills(template),
                required_tools=self._identify_required_tools(template),
                required_investment=template['startup_cost'],
                trend_direction=self._assess_trend_direction(template),
                ai_disruption_risk=self._assess_ai_risk(template),
                future_potential=self._assess_future_potential(template),
                critical_success_factors=self._identify_success_factors(template),
                common_failure_points=self._identify_failure_points(template),
                optimization_opportunities=self._identify_optimization_opportunities(template)
            )
            
            strategies.append(strategy)
        
        logger.info(f"Analyzed {len(strategies)} OGV strategies")
        
        return strategies
    
    async def _identify_ogv_trends(self) -> List[Dict[str, Any]]:
        """Identify current trends in German OGV market"""
        
        logger.info("Identifying OGV market trends...")
        
        trends = [
            {
                'trend_name': 'KI-Integration in Content-Erstellung',
                'trend_type': GermanMarketTrend.KI_AUTOMATION,
                'strength': 0.95,
                'german_relevance': 0.90,
                'adoption_rate': 0.75,
                'description': 'Massiver Einsatz von KI-Tools für Content, Automation und Personalisierung',
                'impact_areas': ['content_creation', 'customer_service', 'lead_generation'],
                'key_players': ['ChatGPT', 'Jasper', 'Copy.ai'],
                'timeline': '2024-2025',
                'predicted_longevity': 'long_term'
            },
            {
                'trend_name': 'Community-zentrierte Business-Modelle',
                'trend_type': GermanMarketTrend.COMMUNITY_BUILDING,
                'strength': 0.88,
                'german_relevance': 0.95,
                'adoption_rate': 0.65,
                'description': 'Fokus auf exklusive Communities statt nur Content-Konsum',
                'impact_areas': ['customer_retention', 'pricing_power', 'organic_growth'],
                'key_players': ['Discord', 'Telegram', 'Circle'],
                'timeline': '2024-ongoing',
                'predicted_longevity': 'long_term'
            },
            {
                'trend_name': 'Kurze Video-Inhalte dominieren',
                'trend_type': GermanMarketTrend.KURZE_AUFMERKSAMKEIT,
                'strength': 0.92,
                'german_relevance': 0.85,
                'adoption_rate': 0.80,
                'description': 'TikTok-Format erobert alle Plattformen, Aufmerksamkeitsspanne sinkt',
                'impact_areas': ['content_format', 'engagement_rates', 'ad_spending'],
                'key_players': ['TikTok', 'Instagram Reels', 'YouTube Shorts'],
                'timeline': '2023-2025',
                'predicted_longevity': 'medium_term'
            },
            {
                'trend_name': 'Vertrauen und Authentizität als USP',
                'trend_type': GermanMarketTrend.VERTRAUEN_AUTHENTIZITAT,
                'strength': 0.85,
                'german_relevance': 0.98,
                'adoption_rate': 0.60,
                'description': 'Deutsche Konsumenten fordern mehr Transparenz und echte Persönlichkeiten',
                'impact_areas': ['brand_building', 'conversion_rates', 'customer_loyalty'],
                'key_players': ['Micro-Influencer', 'Personal Brands'],
                'timeline': '2024-ongoing',
                'predicted_longevity': 'long_term'
            },
            {
                'trend_name': 'Nachhaltigkeit als Differenzierungsmerkmal',
                'trend_type': GermanMarketTrend.NACHHALTIGKEIT,
                'strength': 0.78,
                'german_relevance': 0.95,
                'adoption_rate': 0.45,
                'description': 'ESG-Kriterien werden auch im Online-Marketing wichtiger',
                'impact_areas': ['product_development', 'marketing_messaging', 'target_audience'],
                'key_players': ['B-Corp zertifizierte Unternehmen', 'Green-Tech Startups'],
                'timeline': '2024-2026',
                'predicted_longevity': 'long_term'
            }
        ]
        
        logger.info(f"Identified {len(trends)} major OGV trends")
        
        return trends
    
    async def _extract_ogv_success_patterns(self, influencers: List[OnlineGeldVerdienenInfluencer]) -> List[Dict[str, Any]]:
        """Extract success patterns from top OGV influencers"""
        
        logger.info("Extracting OGV success patterns...")
        
        patterns = []
        
        # Analyze content patterns from top influencers
        top_influencers = influencers[:20]  # Top 20 for pattern analysis
        
        content_data = []
        for influencer in top_influencers:
            content_sample = {
                'title': f"Content from {influencer.name}",
                'content': ' '.join(influencer.content_pillars),
                'platform': influencer.primary_platform.value,
                'engagement_rate': influencer.engagement_rate,
                'revenue': influencer.estimated_monthly_revenue,
                'category': influencer.ogv_category.value,
                'hooks': influencer.trending_hooks
            }
            content_data.append(content_sample)
        
        # Use universal pattern extractor
        if content_data:
            pattern_analysis = await self.pattern_extractor.analyze_universal_patterns(content_data)
            
            # Convert to OGV-specific patterns
            for hook in pattern_analysis.universal_hooks[:10]:
                patterns.append({
                    'pattern_type': 'hook_formula',
                    'pattern_name': f"OGV {hook.name}",
                    'effectiveness_score': hook.effectiveness_score,
                    'german_specific': True,
                    'pattern_data': {
                        'structure': hook.structure,
                        'examples': hook.examples,
                        'trigger': hook.trigger.value if hasattr(hook, 'trigger') else 'unknown',
                        'platform_compatibility': ['youtube', 'instagram', 'tiktok']
                    },
                    'usage_context': 'online_geld_verdienen',
                    'success_metrics': {
                        'conversion_rate': hook.effectiveness_score * 0.1,
                        'engagement_boost': hook.effectiveness_score * 20
                    }
                })
            
            for trigger in pattern_analysis.viral_triggers[:5]:
                patterns.append({
                    'pattern_type': 'viral_trigger',
                    'pattern_name': f"OGV {trigger.name}",
                    'effectiveness_score': trigger.effectiveness_score,
                    'german_specific': True,
                    'pattern_data': {
                        'description': trigger.description,
                        'trigger_type': trigger.trigger.value if hasattr(trigger, 'trigger') else 'unknown',
                        'implementation': trigger.implementation_guide if hasattr(trigger, 'implementation_guide') else ''
                    },
                    'usage_context': 'online_geld_verdienen',
                    'success_metrics': {
                        'viral_potential': trigger.effectiveness_score,
                        'audience_resonance': trigger.effectiveness_score * 0.9
                    }
                })
        
        # Add OGV-specific patterns
        ogv_specific_patterns = [
            {
                'pattern_type': 'pricing_psychology',
                'pattern_name': 'Deutsche Preispsychologie',
                'effectiveness_score': 0.85,
                'german_specific': True,
                'pattern_data': {
                    'preferred_price_points': [97, 197, 497, 997, 1997],
                    'payment_preferences': ['Ratenzahlung', 'SEPA', 'PayPal'],
                    'trust_signals': ['Geld-zurück-Garantie', 'Impressum', 'Kundenbewertungen'],
                    'cultural_considerations': ['Skepsis gegenüber "schnell reich werden"', 'Wertschätzung von Qualität']
                },
                'success_metrics': {
                    'conversion_improvement': 0.25,
                    'trust_increase': 0.40
                }
            },
            {
                'pattern_type': 'content_structure',
                'pattern_name': 'OGV Bildungsansatz',
                'effectiveness_score': 0.82,
                'german_specific': True,
                'pattern_data': {
                    'structure': 'Problem → Bildung → Lösung → Vertrauen → Angebot',
                    'educational_ratio': 0.8,  # 80% Bildung, 20% Verkauf
                    'proof_elements': ['Fallstudien', 'Transparente Zahlen', 'Schritt-für-Schritt'],
                    'trust_building': ['Persönliche Geschichte', 'Fehler eingestehen', 'Realistische Erwartungen']
                },
                'success_metrics': {
                    'audience_retention': 0.75,
                    'conversion_rate': 0.12
                }
            }
        ]
        
        patterns.extend(ogv_specific_patterns)
        
        logger.info(f"Extracted {len(patterns)} OGV success patterns")
        
        return patterns
    
    async def _analyze_market_opportunities(self) -> List[Dict[str, Any]]:
        """Analyze current market opportunities in German OGV space"""
        
        logger.info("Analyzing OGV market opportunities...")
        
        opportunities = [
            {
                'opportunity_name': 'KI-Tool Bewertung und Vergleich',
                'category': OnlineGeldVerdienenCategory.AFFILIATE_MARKETING,
                'market_size': 'mittel',
                'competition_level': 'niedrig',
                'entry_barrier': 'niedrig',
                'revenue_potential': 'hoch',
                'description': 'Objektive Bewertung und Vergleich von KI-Tools für Online-Unternehmer',
                'target_audience': 'Kleine Unternehmen und Solopreneure',
                'implementation_effort': 'mittel',
                'success_probability': 0.78,
                'risk_factors': ['Schnelle Marktveränderungen', 'Tool-Überangebot'],
                'success_factors': ['Objektive Tests', 'Deutsche Tutorials', 'Preis-Leistungs-Fokus']
            },
            {
                'opportunity_name': 'Compliance-konforme Krypto-Bildung',
                'category': OnlineGeldVerdienenCategory.KRYPTO_TRADING,
                'market_size': 'groß',
                'competition_level': 'mittel',
                'entry_barrier': 'hoch',
                'revenue_potential': 'sehr hoch',
                'description': 'Bildungsbasierte Krypto-Inhalte unter Beachtung deutscher BaFin-Regulierung',
                'target_audience': 'Konservative deutsche Investoren',
                'implementation_effort': 'hoch',
                'success_probability': 0.65,
                'risk_factors': ['Regulatorische Änderungen', 'Marktvolatilität'],
                'success_factors': ['Juristische Expertise', 'Konservative Herangehensweise', 'Bildungsfokus']
            },
            {
                'opportunity_name': 'Lokale Service-Marktplätze',
                'category': OnlineGeldVerdienenCategory.ONLINE_BUSINESS,
                'market_size': 'groß',
                'competition_level': 'hoch',
                'entry_barrier': 'mittel',
                'revenue_potential': 'hoch',
                'description': 'Hyperlokal fokussierte Service-Vermittlung mit Community-Aspekt',
                'target_audience': 'Lokale Dienstleister und Kunden',
                'implementation_effort': 'hoch',
                'success_probability': 0.55,
                'risk_factors': ['Starke Konkurrenz', 'Netzwerkeffekte nötig'],
                'success_factors': ['Lokaler Fokus', 'Community Building', 'Vertrauensaufbau']
            },
            {
                'opportunity_name': 'Nachhaltiges Affiliate Marketing',
                'category': OnlineGeldVerdienenCategory.AFFILIATE_MARKETING,
                'market_size': 'mittel',
                'competition_level': 'niedrig',
                'entry_barrier': 'niedrig',
                'revenue_potential': 'mittel',
                'description': 'Fokus auf nachhaltige Produkte und ESG-konforme Unternehmen',
                'target_audience': 'Umweltbewusste Konsumenten 25-45',
                'implementation_effort': 'mittel',
                'success_probability': 0.70,
                'risk_factors': ['Begrenztes Produktangebot', 'Niedrigere Provisionen'],
                'success_factors': ['Authentizität', 'Zielgruppen-Fit', 'Langfristige Perspektive']
            },
            {
                'opportunity_name': 'Senior-fokussierte Digitalisierung',
                'category': OnlineGeldVerdienenCategory.COACHING_CONSULTING,
                'market_size': 'groß',
                'competition_level': 'niedrig',
                'entry_barrier': 'mittel',
                'revenue_potential': 'hoch',
                'description': 'Digitalisierungs-Coaching für Menschen 50+',
                'target_audience': 'Senioren mit Interesse an Online-Aktivitäten',
                'implementation_effort': 'mittel',
                'success_probability': 0.72,
                'risk_factors': ['Langsame Adoption', 'Technologie-Skepsis'],
                'success_factors': ['Geduld und Empathie', 'Einfache Erklärungen', 'Persönlicher Support']
            }
        ]
        
        logger.info(f"Identified {len(opportunities)} market opportunities")
        
        return opportunities
    
    async def _analyze_competitive_landscape(self, influencers: List[OnlineGeldVerdienenInfluencer]) -> Dict[str, Any]:
        """Analyze competitive landscape in OGV market"""
        
        logger.info("Analyzing competitive landscape...")
        
        # Group influencers by category
        category_distribution = {}
        for influencer in influencers:
            category = influencer.ogv_category.value
            if category not in category_distribution:
                category_distribution[category] = []
            category_distribution[category].append(influencer)
        
        # Analyze competition in each category
        competitive_analysis = {}
        for category, category_influencers in category_distribution.items():
            competitive_analysis[category] = {
                'total_players': len(category_influencers),
                'market_concentration': self._calculate_market_concentration(category_influencers),
                'average_followers': np.mean([inf.followers.get('total', 0) for inf in category_influencers]),
                'average_revenue': np.mean([inf.estimated_monthly_revenue for inf in category_influencers]),
                'top_players': sorted(category_influencers, key=lambda x: x.estimated_monthly_revenue, reverse=True)[:3],
                'entry_barriers': self._assess_category_entry_barriers(category),
                'market_saturation': self._assess_category_saturation(category_influencers),
                'growth_potential': self._assess_category_growth_potential(category)
            }
        
        # Overall market analysis
        overall_analysis = {
            'total_tracked_influencers': len(influencers),
            'category_distribution': {cat: len(infs) for cat, infs in category_distribution.items()},
            'market_leaders': sorted(influencers, key=lambda x: x.estimated_monthly_revenue, reverse=True)[:10],
            'emerging_players': [inf for inf in influencers if inf.trend_adoption_speed == 'early'],
            'market_gaps': self._identify_market_gaps(category_distribution),
            'consolidation_trends': self._analyze_consolidation_trends(influencers),
            'innovation_hotspots': self._identify_innovation_hotspots(influencers)
        }
        
        return {
            'category_analysis': competitive_analysis,
            'overall_market': overall_analysis,
            'market_dynamics': {
                'competition_intensity': self._calculate_overall_competition_intensity(competitive_analysis),
                'innovation_rate': self._calculate_innovation_rate(influencers),
                'market_maturity': self._assess_market_maturity(competitive_analysis)
            }
        }
    
    async def _generate_ogv_insights(self, 
                                   influencers: List[OnlineGeldVerdienenInfluencer],
                                   strategies: List[OnlineGeldVerdienenStrategy],
                                   trends: List[Dict[str, Any]],
                                   patterns: List[Dict[str, Any]],
                                   opportunities: List[Dict[str, Any]],
                                   competition: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable insights and recommendations"""
        
        logger.info("Generating OGV insights and recommendations...")
        
        insights = {
            'market_overview': {
                'market_health': self._assess_market_health(influencers, trends),
                'growth_trajectory': self._analyze_growth_trajectory(trends),
                'key_success_drivers': self._identify_key_success_drivers(patterns),
                'market_challenges': self._identify_market_challenges(competition, trends)
            },
            
            'top_opportunities_2024_2025': [
                {
                    'opportunity': 'KI-Integration in bestehende Business-Modelle',
                    'potential': 'sehr hoch',
                    'timeframe': 'sofort',
                    'difficulty': 'mittel',
                    'reasoning': 'KI-Tools ermöglichen Skalierung ohne proportionale Kostensteigerung'
                },
                {
                    'opportunity': 'Community-zentrierte Premium-Angebote',
                    'potential': 'hoch',
                    'timeframe': '3-6 Monate',
                    'difficulty': 'mittel-hoch',
                    'reasoning': 'Deutsche Nutzer zahlen Premium für exklusiven Zugang und persönlichen Kontakt'
                },
                {
                    'opportunity': 'Compliance-konforme Fintech-Education',
                    'potential': 'sehr hoch',
                    'timeframe': '6-12 Monate',
                    'difficulty': 'hoch',
                    'reasoning': 'Hohe Nachfrage nach seriöser Finanz-Bildung unter Beachtung deutscher Regulierung'
                }
            ],
            
            'strategic_recommendations': {
                'for_beginners': [
                    'Start mit Affiliate Marketing in vertrauten Bereichen',
                    'Fokus auf Bildung und Mehrwert statt schnelle Verkäufe',
                    'Aufbau einer authentischen Personal Brand',
                    'Nutzung von KI-Tools zur Content-Optimierung'
                ],
                'for_intermediate': [
                    'Entwicklung eigener digitaler Produkte',
                    'Community-Building mit exklusiven Inhalten',
                    'Expansion auf mehrere Plattformen',
                    'Automatisierung wiederkehrender Prozesse'
                ],
                'for_advanced': [
                    'Aufbau von Ecosystem-Businesses',
                    'Internationale Expansion mit lokalem Fokus',
                    'Mentoring und Franchising-Modelle',
                    'Impact Investing und ESG-Integration'
                ]
            },
            
            'platform_specific_tactics': {
                'youtube': {
                    'optimal_content_length': '8-15 Minuten für Deep-Dive Content',
                    'posting_frequency': '2-3 Videos pro Woche',
                    'monetization_focus': 'AdSense + Affiliate + eigene Produkte',
                    'growth_hack': 'Tutorial-Serien mit Cliffhangern'
                },
                'instagram': {
                    'optimal_content_mix': '60% Reels, 30% Stories, 10% Posts',
                    'posting_frequency': 'Täglich Stories, 3-4 Reels/Woche',
                    'monetization_focus': 'Affiliate + Brand Partnerships',
                    'growth_hack': 'Behind-the-scenes authentischer Content'
                },
                'tiktok': {
                    'optimal_content_length': '15-30 Sekunden',
                    'posting_frequency': '1-2 Videos täglich',
                    'monetization_focus': 'Creator Fund + Affiliate Links',
                    'growth_hack': 'Trend-Adaptionen mit OGV-Twist'
                }
            },
            
            'risk_mitigation': {
                'regulatory_risks': [
                    'Regelmäßige Compliance-Checks',
                    'Juristische Beratung für neue Bereiche',
                    'Transparente Affiliate-Kennzeichnung',
                    'Datenschutz-konforme Datenverarbeitung'
                ],
                'market_risks': [
                    'Diversifikation der Einkommensströme',
                    'Aufbau direkter Kundenbeziehungen',
                    'Kontinuierliche Weiterbildung',
                    'Anpassungsfähige Business-Modelle'
                ],
                'platform_risks': [
                    'Multi-Platform-Präsenz',
                    'Eigene E-Mail-Liste aufbauen',
                    'Website als zentrale Anlaufstelle',
                    'Backup-Strategien für Content'
                ]
            },
            
            'success_metrics_to_track': [
                'Customer Lifetime Value (CLV)',
                'Customer Acquisition Cost (CAC)',
                'Engagement Rate nach Plattform',
                'Conversion Rate nach Traffic-Quelle',
                'Brand Awareness in Zielgruppe',
                'Community-Wachstumsrate',
                'Revenue per Follower',
                'Content Virality Score'
            ]
        }
        
        return insights
    
    # Helper methods for analysis
    def _get_category_keywords(self, category: OnlineGeldVerdienenCategory) -> List[str]:
        """Get keywords for specific OGV category"""
        category_keywords = {
            OnlineGeldVerdienenCategory.AFFILIATE_MARKETING: self.german_keywords['affiliate_marketing'],
            OnlineGeldVerdienenCategory.DROPSHIPPING: ['dropshipping', 'online shop', 'ecommerce'],
            OnlineGeldVerdienenCategory.TRADING_FOREX: ['forex', 'trading', 'devisen'],
            OnlineGeldVerdienenCategory.KRYPTO_TRADING: ['krypto', 'bitcoin', 'blockchain'],
            OnlineGeldVerdienenCategory.COACHING_CONSULTING: ['coaching', 'beratung', 'mentoring'],
            OnlineGeldVerdienenCategory.DIGITALE_PRODUKTE: ['digitale produkte', 'online kurse', 'ebooks'],
            OnlineGeldVerdienenCategory.PASSIVES_EINKOMMEN: ['passives einkommen', 'finanzielle freiheit'],
            OnlineGeldVerdienenCategory.AMAZON_FBA: ['amazon fba', 'private label', 'fulfillment'],
            OnlineGeldVerdienenCategory.SOCIAL_MEDIA_MARKETING: ['social media', 'influencer', 'content'],
            OnlineGeldVerdienenCategory.ONLINE_KURSE: ['online kurse', 'e-learning', 'weiterbildung'],
            OnlineGeldVerdienenCategory.NETWORK_MARKETING: ['network marketing', 'mlm', 'strukturvertrieb']
        }
        
        return category_keywords.get(category, self.german_keywords['general'])
    
    async def _convert_to_ogv_influencer(self, creator: CreatorProfile, category: OnlineGeldVerdienenCategory) -> Optional[OnlineGeldVerdienenInfluencer]:
        """Convert universal creator profile to OGV-specific profile"""
        
        try:
            # Calculate German market focus
            german_focus = self._calculate_german_market_focus(creator)
            
            # Skip if not German-focused enough
            if german_focus < 0.3:
                return None
            
            # Estimate revenue based on followers and engagement
            estimated_revenue = self._estimate_monthly_revenue(creator)
            
            # Determine sub-categories
            sub_categories = self._determine_sub_categories(creator, category)
            
            ogv_influencer = OnlineGeldVerdienenInfluencer(
                name=creator.name,
                handle=creator.handle,
                platforms=[creator.platform],
                primary_platform=creator.platform,
                followers=creator.followers,
                engagement_rate=creator.engagement_rate,
                estimated_monthly_revenue=estimated_revenue,
                ogv_category=category,
                sub_categories=sub_categories,
                target_audience=self._determine_target_audience(creator),
                german_market_focus=german_focus,
                uses_german_language=german_focus > 0.7,
                understands_german_regulations=german_focus > 0.8,
                german_payment_methods=['paypal', 'sepa'] if german_focus > 0.5 else [],
                main_revenue_streams=self._identify_revenue_streams(creator, category),
                pricing_tiers=self._estimate_pricing_tiers(creator, category),
                customer_lifetime_value=estimated_revenue * 6,  # Estimate 6x monthly
                content_pillars=creator.content_themes or [],
                posting_schedule={creator.platform.value: creator.posting_frequency},
                content_quality_score=creator.authenticity_score,
                trending_hooks=creator.hook_strategies if hasattr(creator, 'hook_strategies') else [],
                new_platform_strategies=[],
                ai_integration=[],
                community_strategies=[],
                conversion_funnel_performance={},
                customer_satisfaction_indicators=[],
                market_authority_score=creator.influence_score,
                pioneering_strategies=[],
                trend_adoption_speed='fast' if creator.influence_score > 0.8 else 'slow',
                market_prediction_accuracy=0.7  # Default estimate
            )
            
            return ogv_influencer
            
        except Exception as e:
            logger.warning(f"Failed to convert creator {creator.name} to OGV influencer: {e}")
            return None
    
    def _calculate_german_market_focus(self, creator: CreatorProfile) -> float:
        """Calculate how much a creator focuses on German market"""
        
        german_indicators = 0
        total_indicators = 5
        
        # Check language
        if creator.language == 'de':
            german_indicators += 1
        
        # Check region
        if creator.region in ['DE', 'AT', 'CH', 'germany', 'deutschland']:
            german_indicators += 1
        
        # Check content themes for German keywords
        content_text = ' '.join(creator.content_themes).lower()
        german_keywords_found = sum(1 for keyword in self.german_keywords['general'] if keyword in content_text)
        if german_keywords_found > 0:
            german_indicators += min(1, german_keywords_found / 3)
        
        # Check handle/name for German indicators
        name_text = f"{creator.name} {creator.handle}".lower()
        if any(indicator in name_text for indicator in ['de', 'deutsch', 'german', 'dach']):
            german_indicators += 1
        
        # Platform-specific checks
        platform_config = self.german_platforms.get(creator.platform, {})
        if platform_config.get('language_preference') == 'de':
            german_indicators += 0.5
        
        return min(1.0, german_indicators / total_indicators)
    
    def _estimate_monthly_revenue(self, creator: CreatorProfile) -> float:
        """Estimate monthly revenue based on creator metrics"""
        
        platform = creator.platform
        followers = creator.followers
        engagement_rate = creator.engagement_rate
        
        # Platform-specific revenue calculations
        if platform == Platform.YOUTUBE:
            # YouTube AdSense + Sponsorships + Affiliate
            monthly_views = followers * 4 * engagement_rate / 100  # Estimate monthly views
            ad_revenue = monthly_views * 0.002  # €2 per 1000 views (CPM)
            sponsor_revenue = followers * 0.01 if followers > 10000 else 0
            affiliate_revenue = followers * 0.005 if followers > 5000 else 0
            return ad_revenue + sponsor_revenue + affiliate_revenue
            
        elif platform == Platform.INSTAGRAM:
            # Sponsorships + Affiliate + Product sales
            if followers > 100000:
                return followers * 0.02
            elif followers > 10000:
                return followers * 0.01
            else:
                return followers * 0.005
                
        elif platform == Platform.TIKTOK:
            # Creator Fund + Sponsorships + Affiliate
            if followers > 100000:
                return followers * 0.015
            elif followers > 10000:
                return followers * 0.008
            else:
                return followers * 0.003
                
        else:
            # Generic calculation
            return followers * 0.005
    
    def _determine_sub_categories(self, creator: CreatorProfile, main_category: OnlineGeldVerdienenCategory) -> List[OnlineGeldVerdienenCategory]:
        """Determine sub-categories for a creator"""
        
        sub_cats = []
        content_text = ' '.join(creator.content_themes).lower()
        
        # Check for overlapping categories
        if 'affiliate' in content_text and main_category != OnlineGeldVerdienenCategory.AFFILIATE_MARKETING:
            sub_cats.append(OnlineGeldVerdienenCategory.AFFILIATE_MARKETING)
        
        if any(word in content_text for word in ['coaching', 'mentoring', 'beratung']):
            if main_category != OnlineGeldVerdienenCategory.COACHING_CONSULTING:
                sub_cats.append(OnlineGeldVerdienenCategory.COACHING_CONSULTING)
        
        if any(word in content_text for word in ['kurs', 'course', 'lernen']):
            if main_category != OnlineGeldVerdienenCategory.ONLINE_KURSE:
                sub_cats.append(OnlineGeldVerdienenCategory.ONLINE_KURSE)
        
        return sub_cats[:2]  # Maximum 2 sub-categories
    
    def _determine_target_audience(self, creator: CreatorProfile) -> str:
        """Determine target audience level"""
        
        content_text = ' '.join(creator.content_themes).lower()
        
        if any(word in content_text for word in ['anfänger', 'beginner', 'start', 'erste']):
            return 'Anfänger'
        elif any(word in content_text for word in ['fortgeschritten', 'advanced', 'profi', 'expert']):
            return 'Fortgeschrittene'
        else:
            return 'Gemischt'
    
    def _identify_revenue_streams(self, creator: CreatorProfile, category: OnlineGeldVerdienenCategory) -> List[str]:
        """Identify likely revenue streams for creator"""
        
        streams = []
        
        # Category-specific streams
        if category == OnlineGeldVerdienenCategory.AFFILIATE_MARKETING:
            streams.extend(['Affiliate Provisionen', 'Produktbewertungen', 'Bonus-Aktionen'])
        elif category == OnlineGeldVerdienenCategory.COACHING_CONSULTING:
            streams.extend(['1:1 Coaching', 'Gruppenprogramme', 'Online Kurse'])
        elif category == OnlineGeldVerdienenCategory.TRADING_FOREX:
            streams.extend(['Trading Kurse', 'Signal Services', 'Broker Provisionen'])
        
        # Platform-specific streams
        if creator.platform == Platform.YOUTUBE:
            streams.append('YouTube AdSense')
        
        # General streams based on following
        if creator.followers > 10000:
            streams.append('Brand Partnerships')
        
        if creator.followers > 50000:
            streams.append('Eigene Produkte')
        
        return list(set(streams))
    
    def _estimate_pricing_tiers(self, creator: CreatorProfile, category: OnlineGeldVerdienenCategory) -> Dict[str, float]:
        """Estimate pricing tiers for creator's offerings"""
        
        # Base pricing by category
        base_pricing = {
            OnlineGeldVerdienenCategory.AFFILIATE_MARKETING: {'low': 97, 'mid': 297, 'high': 997},
            OnlineGeldVerdienenCategory.COACHING_CONSULTING: {'low': 497, 'mid': 1497, 'high': 4997},
            OnlineGeldVerdienenCategory.TRADING_FOREX: {'low': 197, 'mid': 697, 'high': 1997},
            OnlineGeldVerdienenCategory.KRYPTO_TRADING: {'low': 297, 'mid': 897, 'high': 2997},
            OnlineGeldVerdienenCategory.ONLINE_KURSE: {'low': 149, 'mid': 497, 'high': 1497}
        }
        
        default_pricing = {'low': 197, 'mid': 597, 'high': 1497}
        pricing = base_pricing.get(category, default_pricing)
        
        # Adjust based on authority/influence
        authority_multiplier = 1 + (creator.influence_score - 0.5)
        for tier in pricing:
            pricing[tier] *= authority_multiplier
        
        return pricing
    
    def _deduplicate_influencers(self, influencers: List[OnlineGeldVerdienenInfluencer]) -> List[OnlineGeldVerdienenInfluencer]:
        """Remove duplicate influencers from list"""
        
        seen_handles = set()
        unique_influencers = []
        
        for influencer in influencers:
            if influencer.handle not in seen_handles:
                seen_handles.add(influencer.handle)
                unique_influencers.append(influencer)
        
        return unique_influencers
    
    def _rank_influencers_by_ogv_relevance(self, influencers: List[OnlineGeldVerdienenInfluencer]) -> List[OnlineGeldVerdienenInfluencer]:
        """Rank influencers by relevance to OGV niche"""
        
        def relevance_score(influencer):
            score = 0
            
            # German market focus (30%)
            score += influencer.german_market_focus * 0.3
            
            # Revenue potential (25%)
            revenue_score = min(1.0, influencer.estimated_monthly_revenue / 10000)
            score += revenue_score * 0.25
            
            # Market authority (20%)
            score += influencer.market_authority_score * 0.2
            
            # Engagement rate (15%)
            engagement_score = min(1.0, influencer.engagement_rate / 10)
            score += engagement_score * 0.15
            
            # Innovation/trend adoption (10%)
            trend_score = 1.0 if influencer.trend_adoption_speed == 'early' else 0.5
            score += trend_score * 0.1
            
            return score
        
        return sorted(influencers, key=relevance_score, reverse=True)
    
    # Additional helper methods (abbreviated for space)
    def _calculate_german_suitability(self, strategy_template: Dict) -> float:
        """Calculate German market suitability for strategy"""
        return 0.8  # Placeholder
    
    def _assess_regulatory_compliance(self, strategy_template: Dict) -> Dict[str, bool]:
        """Assess regulatory compliance for strategy"""
        return {'gdpr': True, 'impressum': True, 'tax': True}  # Placeholder
    
    def _assess_cultural_fit(self, strategy_template: Dict) -> float:
        """Assess cultural fit for German market"""
        return 0.85  # Placeholder
    
    def _assess_scalability(self, strategy_template: Dict) -> float:
        """Assess scalability of strategy"""
        return 0.7  # Placeholder
    
    def _estimate_earnings(self, strategy_template: Dict) -> Dict[str, float]:
        """Estimate earnings for different skill levels"""
        return {'anfänger': 500, 'fortgeschritten': 2000, 'experte': 5000}  # Placeholder
    
    def _estimate_success_rate(self, strategy_template: Dict) -> float:
        """Estimate success rate for strategy"""
        return 0.6  # Placeholder
    
    def _assess_market_saturation(self, strategy_template: Dict) -> float:
        """Assess market saturation for strategy"""
        return 0.4  # Placeholder
    
    def _identify_required_skills(self, strategy_template: Dict) -> List[str]:
        """Identify required skills for strategy"""
        return ['Marketing', 'Content Creation', 'Analytics']  # Placeholder
    
    def _identify_required_tools(self, strategy_template: Dict) -> List[str]:
        """Identify required tools for strategy"""
        return ['Website', 'Analytics Tool', 'Email Marketing']  # Placeholder
    
    def _assess_trend_direction(self, strategy_template: Dict) -> str:
        """Assess trend direction for strategy"""
        return 'steigend'  # Placeholder
    
    def _assess_ai_risk(self, strategy_template: Dict) -> float:
        """Assess AI disruption risk"""
        return 0.3  # Placeholder
    
    def _assess_future_potential(self, strategy_template: Dict) -> float:
        """Assess future potential"""
        return 0.8  # Placeholder
    
    def _identify_success_factors(self, strategy_template: Dict) -> List[str]:
        """Identify critical success factors"""
        return ['Konsistenz', 'Qualität', 'Authentizität']  # Placeholder
    
    def _identify_failure_points(self, strategy_template: Dict) -> List[str]:
        """Identify common failure points"""
        return ['Ungeduld', 'Mangelnde Konsistenz', 'Fehlende Zielgruppe']  # Placeholder
    
    def _identify_optimization_opportunities(self, strategy_template: Dict) -> List[str]:
        """Identify optimization opportunities"""
        return ['Automation', 'Personalisierung', 'A/B Testing']  # Placeholder
    
    # Market analysis helper methods (placeholders)
    def _calculate_market_concentration(self, influencers: List) -> float:
        return 0.6  # Placeholder
    
    def _assess_category_entry_barriers(self, category: str) -> str:
        return 'mittel'  # Placeholder
    
    def _assess_category_saturation(self, influencers: List) -> float:
        return 0.5  # Placeholder
    
    def _assess_category_growth_potential(self, category: str) -> float:
        return 0.7  # Placeholder
    
    def _identify_market_gaps(self, category_distribution: Dict) -> List[str]:
        return ['Senior-focused content', 'B2B automation']  # Placeholder
    
    def _analyze_consolidation_trends(self, influencers: List) -> Dict:
        return {'trend': 'increasing', 'rate': 0.1}  # Placeholder
    
    def _identify_innovation_hotspots(self, influencers: List) -> List[str]:
        return ['AI integration', 'Community platforms']  # Placeholder
    
    def _calculate_overall_competition_intensity(self, analysis: Dict) -> float:
        return 0.7  # Placeholder
    
    def _calculate_innovation_rate(self, influencers: List) -> float:
        return 0.8  # Placeholder
    
    def _assess_market_maturity(self, analysis: Dict) -> str:
        return 'growing'  # Placeholder
    
    def _assess_market_health(self, influencers: List, trends: List) -> str:
        return 'healthy'  # Placeholder
    
    def _analyze_growth_trajectory(self, trends: List) -> str:
        return 'positive'  # Placeholder
    
    def _identify_key_success_drivers(self, patterns: List) -> List[str]:
        return ['Authenticity', 'Value-first approach', 'Community building']  # Placeholder
    
    def _identify_market_challenges(self, competition: Dict, trends: List) -> List[str]:
        return ['Increasing competition', 'Platform dependency', 'Regulatory uncertainty']  # Placeholder
    
    async def _save_analysis_session(self, 
                                   session_id: str,
                                   analysis_type: str,
                                   focus_category: str,
                                   influencers_count: int,
                                   strategies_count: int,
                                   patterns_count: int,
                                   session_data: Dict,
                                   results_summary: Dict):
        """Save analysis session to database"""
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT INTO ogv_analysis_sessions 
                (session_id, analysis_type, focus_category, influencers_analyzed,
                 strategies_identified, patterns_extracted, session_data, results_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                analysis_type,
                focus_category,
                influencers_count,
                strategies_count,
                patterns_count,
                json.dumps(session_data, ensure_ascii=False),
                json.dumps(results_summary, ensure_ascii=False)
            ))
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get analysis statistics"""
        
        with sqlite3.connect(self.database_path) as conn:
            # Count records in each table
            influencers_count = conn.execute("SELECT COUNT(*) FROM ogv_influencers").fetchone()[0]
            strategies_count = conn.execute("SELECT COUNT(*) FROM ogv_strategies").fetchone()[0]
            trends_count = conn.execute("SELECT COUNT(*) FROM ogv_market_trends").fetchone()[0]
            patterns_count = conn.execute("SELECT COUNT(*) FROM ogv_success_patterns").fetchone()[0]
            sessions_count = conn.execute("SELECT COUNT(*) FROM ogv_analysis_sessions").fetchone()[0]
        
        return {
            'database_path': self.database_path,
            'total_influencers': influencers_count,
            'total_strategies': strategies_count,
            'total_trends': trends_count,
            'total_patterns': patterns_count,
            'total_sessions': sessions_count,
            'last_updated': datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    async def test_ogv_analysis():
        # Initialize analyzer
        analyzer = OnlineGeldVerdienenAnalyzer()
        
        # Run comprehensive analysis
        results = await analyzer.analyze_ogv_market_comprehensive()
        
        print("=== ONLINE GELD VERDIENEN MARKET ANALYSIS ===")
        print(f"Session ID: {results['session_id']}")
        print(f"Analysis Type: {results['analysis_type']}")
        print(f"Total Influencers: {results['market_overview']['total_influencers']}")
        print(f"Active Strategies: {results['market_overview']['active_strategies']}")
        print(f"Market Opportunities: {results['market_overview']['market_opportunities']}")
        
        print("\n=== TOP OPPORTUNITIES 2024/2025 ===")
        for opp in results['insights_and_recommendations']['top_opportunities_2024_2025']:
            print(f"• {opp['opportunity']} (Potential: {opp['potential']})")
        
        print("\n=== STRATEGIC RECOMMENDATIONS ===")
        for level, recommendations in results['insights_and_recommendations']['strategic_recommendations'].items():
            print(f"\n{level.upper()}:")
            for rec in recommendations[:2]:
                print(f"  • {rec}")
        
        print(f"\n=== ANALYSIS STATS ===")
        stats = analyzer.get_analysis_stats()
        print(f"Database Records: {stats}")
    
    # Run test
    asyncio.run(test_ogv_analysis())