#!/usr/bin/env python3
"""
Research Data Ingestion & Learning System

Accepts external research data from manual research (Gemini, ChatGPT, etc.)
and trains the Creator Analyzer to perform this research autonomously in the future.

Specifically designed for German online marketing influencer research.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
import sqlite3
from datetime import datetime
import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchSource(Enum):
    """Sources of research data"""
    MANUAL_GEMINI = "manual_gemini"
    MANUAL_CHATGPT = "manual_chatgpt"
    MANUAL_HUMAN = "manual_human"
    AUTOMATED_SCAN = "automated_scan"
    WEB_SCRAPING = "web_scraping"
    API_DISCOVERY = "api_discovery"

class InfluencerTier(Enum):
    """Influencer tier classification"""
    MEGA = "mega"           # 1M+ followers
    MACRO = "macro"         # 100K-1M followers
    MICRO = "micro"         # 10K-100K followers
    NANO = "nano"           # 1K-10K followers

@dataclass
class GermanInfluencerProfile:
    """Complete German influencer profile from research"""
    name: str
    handle: str
    platforms: List[str]
    primary_platform: str
    followers: Dict[str, int]  # platform -> follower count
    tier: InfluencerTier
    niche: str
    sub_niches: List[str]
    
    # Content Analysis
    content_themes: List[str]
    posting_frequency: str
    content_formats: List[str]
    
    # Funnel Structure
    funnel_type: str
    funnel_stages: List[str]
    lead_magnets: List[str]
    pricing_strategy: Dict[str, Any]
    products_services: List[Dict[str, Any]]
    
    # 2024/2025 Strategies
    current_hooks: List[str]
    hook_patterns: List[str]
    trending_strategies: List[str]
    content_innovations: List[str]
    
    # Performance Metrics
    engagement_rate: float
    estimated_revenue: str
    conversion_indicators: List[str]
    
    # Research Metadata
    research_source: ResearchSource
    research_date: datetime
    confidence_score: float
    verification_status: str
    
    # URLs and References
    profile_urls: Dict[str, str]
    funnel_examples: List[str]
    case_study_links: List[str]

@dataclass
class FunnelStructure:
    """Detailed funnel structure analysis"""
    influencer_name: str
    funnel_name: str
    funnel_type: str  # webinar, course, coaching, product, etc.
    
    # Funnel Stages
    awareness_stage: Dict[str, Any]
    interest_stage: Dict[str, Any]
    consideration_stage: Dict[str, Any]
    conversion_stage: Dict[str, Any]
    retention_stage: Dict[str, Any]
    
    # Pricing Structure
    entry_price: float
    mid_tier_price: float
    premium_price: float
    pricing_psychology: List[str]
    
    # Current Hooks & Strategies
    primary_hooks: List[str]
    secondary_hooks: List[str]
    urgency_tactics: List[str]
    social_proof_elements: List[str]
    
    # 2024/2025 Innovations
    new_strategies: List[str]
    trend_adaptations: List[str]
    platform_specific_tactics: Dict[str, List[str]]
    
    # Performance Data
    estimated_conversion_rate: float
    estimated_monthly_revenue: float
    success_indicators: List[str]

class ResearchDataIngestion:
    """Main class for ingesting and learning from research data"""
    
    def __init__(self, database_path: str = None):
        self.database_path = database_path or self._get_database_path()
        self.learning_models = {}
        self.pattern_extractors = {}
        
        # Initialize database
        self._initialize_training_database()
        
        # Initialize ML models for pattern learning
        self._initialize_learning_models()
        
        # Statistics
        self.ingestion_stats = {
            'total_influencers_processed': 0,
            'german_influencers': 0,
            'funnels_analyzed': 0,
            'hooks_learned': 0,
            'strategies_identified': 0,
            'patterns_extracted': 0
        }
    
    def _get_database_path(self) -> str:
        """Get database path for training data"""
        base_path = Path(__file__).parent.parent.parent
        db_path = base_path / "databases" / "research_training.db"
        db_path.parent.mkdir(exist_ok=True)
        return str(db_path)
    
    def _initialize_training_database(self):
        """Initialize database for storing training data"""
        
        schema_sql = """
        CREATE TABLE IF NOT EXISTS german_influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            handle TEXT,
            primary_platform TEXT,
            tier TEXT,
            niche TEXT,
            followers_data TEXT, -- JSON
            content_analysis TEXT, -- JSON
            funnel_structure TEXT, -- JSON
            current_strategies TEXT, -- JSON
            performance_metrics TEXT, -- JSON
            research_metadata TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS funnel_structures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER,
            funnel_name TEXT NOT NULL,
            funnel_type TEXT,
            stages_data TEXT, -- JSON
            pricing_data TEXT, -- JSON
            hooks_strategies TEXT, -- JSON
            performance_data TEXT, -- JSON
            innovations_2024_2025 TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (influencer_id) REFERENCES german_influencers(id)
        );
        
        CREATE TABLE IF NOT EXISTS learned_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT NOT NULL, -- hook, funnel, strategy, etc.
            pattern_name TEXT NOT NULL,
            pattern_data TEXT, -- JSON
            effectiveness_score REAL,
            frequency_count INTEGER DEFAULT 1,
            source_influencers TEXT, -- JSON array
            market_segment TEXT, -- german_online_marketing, etc.
            confidence_level REAL,
            first_observed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS hook_formulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hook_text TEXT NOT NULL,
            hook_category TEXT, -- curiosity, fear, desire, etc.
            structure_pattern TEXT,
            german_specific BOOLEAN DEFAULT TRUE,
            effectiveness_score REAL,
            usage_examples TEXT, -- JSON
            source_influencer TEXT,
            platform_optimized TEXT,
            trend_period TEXT, -- 2024, 2025, etc.
            psychological_trigger TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS strategy_innovations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_name TEXT NOT NULL,
            strategy_description TEXT,
            implementation_details TEXT, -- JSON
            target_audience TEXT,
            required_resources TEXT, -- JSON
            expected_results TEXT, -- JSON
            risk_factors TEXT, -- JSON
            source_influencers TEXT, -- JSON
            trend_status TEXT, -- emerging, established, declining
            market_fit_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS research_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_name TEXT NOT NULL,
            research_source TEXT,
            researcher_name TEXT,
            session_date TIMESTAMP,
            influencers_researched INTEGER DEFAULT 0,
            patterns_discovered INTEGER DEFAULT 0,
            quality_score REAL,
            notes TEXT,
            raw_data_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_influencers_niche ON german_influencers(niche);
        CREATE INDEX IF NOT EXISTS idx_influencers_tier ON german_influencers(tier);
        CREATE INDEX IF NOT EXISTS idx_patterns_type ON learned_patterns(pattern_type);
        CREATE INDEX IF NOT EXISTS idx_hooks_category ON hook_formulas(hook_category);
        CREATE INDEX IF NOT EXISTS idx_strategies_trend ON strategy_innovations(trend_status);
        """
        
        with sqlite3.connect(self.database_path) as conn:
            conn.executescript(schema_sql)
    
    def _initialize_learning_models(self):
        """Initialize ML models for pattern learning"""
        
        # Hook pattern analyzer
        self.learning_models['hook_analyzer'] = TfidfVectorizer(
            max_features=500,
            stop_words=None,  # Keep German words
            ngram_range=(1, 3)
        )
        
        # Strategy clustering
        self.learning_models['strategy_clusterer'] = KMeans(
            n_clusters=10,
            random_state=42
        )
        
        # Funnel pattern extractor
        self.learning_models['funnel_analyzer'] = TfidfVectorizer(
            max_features=300,
            ngram_range=(1, 2)
        )
        
        logger.info("Learning models initialized")
    
    async def ingest_research_session(self, 
                                    session_name: str,
                                    researcher_name: str,
                                    research_source: ResearchSource,
                                    data: Dict[str, Any]) -> str:
        """Ingest a complete research session"""
        
        session_id = f"session_{int(datetime.now().timestamp())}"
        
        logger.info(f"Starting ingestion of research session: {session_name}")
        
        try:
            # Process influencers
            influencers_processed = 0
            if 'influencers' in data:
                for influencer_data in data['influencers']:
                    await self.ingest_influencer_profile(influencer_data, research_source)
                    influencers_processed += 1
            
            # Process funnel structures
            funnels_processed = 0
            if 'funnels' in data:
                for funnel_data in data['funnels']:
                    await self.ingest_funnel_structure(funnel_data)
                    funnels_processed += 1
            
            # Process hooks and strategies
            hooks_processed = 0
            if 'hooks' in data:
                for hook_data in data['hooks']:
                    await self.ingest_hook_formula(hook_data)
                    hooks_processed += 1
            
            strategies_processed = 0
            if 'strategies' in data:
                for strategy_data in data['strategies']:
                    await self.ingest_strategy_innovation(strategy_data)
                    strategies_processed += 1
            
            # Save session metadata
            await self._save_research_session(
                session_name, researcher_name, research_source,
                influencers_processed, hooks_processed + strategies_processed
            )
            
            # Update statistics
            self.ingestion_stats['total_influencers_processed'] += influencers_processed
            self.ingestion_stats['funnels_analyzed'] += funnels_processed
            self.ingestion_stats['hooks_learned'] += hooks_processed
            self.ingestion_stats['strategies_identified'] += strategies_processed
            
            # Learn patterns from new data
            await self.learn_patterns_from_session()
            
            logger.info(f"Research session ingested successfully: {influencers_processed} influencers, {funnels_processed} funnels, {hooks_processed} hooks, {strategies_processed} strategies")
            
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to ingest research session: {e}")
            raise
    
    async def ingest_influencer_profile(self, 
                                      influencer_data: Dict[str, Any],
                                      research_source: ResearchSource) -> int:
        """Ingest a single influencer profile"""
        
        try:
            # Parse influencer data
            profile = GermanInfluencerProfile(
                name=influencer_data.get('name', ''),
                handle=influencer_data.get('handle', ''),
                platforms=influencer_data.get('platforms', []),
                primary_platform=influencer_data.get('primary_platform', ''),
                followers=influencer_data.get('followers', {}),
                tier=InfluencerTier(influencer_data.get('tier', 'micro')),
                niche=influencer_data.get('niche', 'online_marketing'),
                sub_niches=influencer_data.get('sub_niches', []),
                content_themes=influencer_data.get('content_themes', []),
                posting_frequency=influencer_data.get('posting_frequency', ''),
                content_formats=influencer_data.get('content_formats', []),
                funnel_type=influencer_data.get('funnel_type', ''),
                funnel_stages=influencer_data.get('funnel_stages', []),
                lead_magnets=influencer_data.get('lead_magnets', []),
                pricing_strategy=influencer_data.get('pricing_strategy', {}),
                products_services=influencer_data.get('products_services', []),
                current_hooks=influencer_data.get('current_hooks', []),
                hook_patterns=influencer_data.get('hook_patterns', []),
                trending_strategies=influencer_data.get('trending_strategies', []),
                content_innovations=influencer_data.get('content_innovations', []),
                engagement_rate=influencer_data.get('engagement_rate', 0.0),
                estimated_revenue=influencer_data.get('estimated_revenue', ''),
                conversion_indicators=influencer_data.get('conversion_indicators', []),
                research_source=research_source,
                research_date=datetime.now(),
                confidence_score=influencer_data.get('confidence_score', 0.8),
                verification_status=influencer_data.get('verification_status', 'manual'),
                profile_urls=influencer_data.get('profile_urls', {}),
                funnel_examples=influencer_data.get('funnel_examples', []),
                case_study_links=influencer_data.get('case_study_links', [])
            )
            
            # Save to database
            influencer_id = await self._save_influencer_profile(profile)
            
            logger.info(f"Ingested influencer profile: {profile.name}")
            
            return influencer_id
            
        except Exception as e:
            logger.error(f"Failed to ingest influencer profile: {e}")
            raise
    
    async def ingest_funnel_structure(self, funnel_data: Dict[str, Any]) -> int:
        """Ingest a funnel structure"""
        
        try:
            funnel = FunnelStructure(
                influencer_name=funnel_data.get('influencer_name', ''),
                funnel_name=funnel_data.get('funnel_name', ''),
                funnel_type=funnel_data.get('funnel_type', ''),
                awareness_stage=funnel_data.get('awareness_stage', {}),
                interest_stage=funnel_data.get('interest_stage', {}),
                consideration_stage=funnel_data.get('consideration_stage', {}),
                conversion_stage=funnel_data.get('conversion_stage', {}),
                retention_stage=funnel_data.get('retention_stage', {}),
                entry_price=funnel_data.get('entry_price', 0.0),
                mid_tier_price=funnel_data.get('mid_tier_price', 0.0),
                premium_price=funnel_data.get('premium_price', 0.0),
                pricing_psychology=funnel_data.get('pricing_psychology', []),
                primary_hooks=funnel_data.get('primary_hooks', []),
                secondary_hooks=funnel_data.get('secondary_hooks', []),
                urgency_tactics=funnel_data.get('urgency_tactics', []),
                social_proof_elements=funnel_data.get('social_proof_elements', []),
                new_strategies=funnel_data.get('new_strategies', []),
                trend_adaptations=funnel_data.get('trend_adaptations', []),
                platform_specific_tactics=funnel_data.get('platform_specific_tactics', {}),
                estimated_conversion_rate=funnel_data.get('estimated_conversion_rate', 0.0),
                estimated_monthly_revenue=funnel_data.get('estimated_monthly_revenue', 0.0),
                success_indicators=funnel_data.get('success_indicators', [])
            )
            
            funnel_id = await self._save_funnel_structure(funnel)
            
            logger.info(f"Ingested funnel structure: {funnel.funnel_name}")
            
            return funnel_id
            
        except Exception as e:
            logger.error(f"Failed to ingest funnel structure: {e}")
            raise
    
    async def ingest_hook_formula(self, hook_data: Dict[str, Any]) -> int:
        """Ingest a hook formula"""
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute("""
                    INSERT INTO hook_formulas 
                    (hook_text, hook_category, structure_pattern, german_specific,
                     effectiveness_score, usage_examples, source_influencer,
                     platform_optimized, trend_period, psychological_trigger)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    hook_data.get('hook_text', ''),
                    hook_data.get('hook_category', ''),
                    hook_data.get('structure_pattern', ''),
                    hook_data.get('german_specific', True),
                    hook_data.get('effectiveness_score', 0.0),
                    json.dumps(hook_data.get('usage_examples', [])),
                    hook_data.get('source_influencer', ''),
                    hook_data.get('platform_optimized', ''),
                    hook_data.get('trend_period', '2024'),
                    hook_data.get('psychological_trigger', '')
                ))
                
                hook_id = cursor.lastrowid
                
            logger.info(f"Ingested hook formula: {hook_data.get('hook_text', '')[:50]}...")
            
            return hook_id
            
        except Exception as e:
            logger.error(f"Failed to ingest hook formula: {e}")
            raise
    
    async def ingest_strategy_innovation(self, strategy_data: Dict[str, Any]) -> int:
        """Ingest a strategy innovation"""
        
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute("""
                    INSERT INTO strategy_innovations 
                    (strategy_name, strategy_description, implementation_details,
                     target_audience, required_resources, expected_results,
                     risk_factors, source_influencers, trend_status, market_fit_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    strategy_data.get('strategy_name', ''),
                    strategy_data.get('strategy_description', ''),
                    json.dumps(strategy_data.get('implementation_details', {})),
                    strategy_data.get('target_audience', ''),
                    json.dumps(strategy_data.get('required_resources', [])),
                    json.dumps(strategy_data.get('expected_results', {})),
                    json.dumps(strategy_data.get('risk_factors', [])),
                    json.dumps(strategy_data.get('source_influencers', [])),
                    strategy_data.get('trend_status', 'emerging'),
                    strategy_data.get('market_fit_score', 0.0)
                ))
                
                strategy_id = cursor.lastrowid
                
            logger.info(f"Ingested strategy innovation: {strategy_data.get('strategy_name', '')}")
            
            return strategy_id
            
        except Exception as e:
            logger.error(f"Failed to ingest strategy innovation: {e}")
            raise
    
    async def learn_patterns_from_session(self):
        """Learn patterns from the latest ingested data"""
        
        logger.info("Learning patterns from ingested data...")
        
        try:
            # Learn hook patterns
            await self._learn_hook_patterns()
            
            # Learn funnel patterns
            await self._learn_funnel_patterns()
            
            # Learn strategy patterns
            await self._learn_strategy_patterns()
            
            # Update pattern database
            await self._update_learned_patterns()
            
            logger.info("Pattern learning completed")
            
        except Exception as e:
            logger.error(f"Failed to learn patterns: {e}")
    
    async def _learn_hook_patterns(self):
        """Learn hook patterns from ingested data"""
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT hook_text, hook_category, psychological_trigger, effectiveness_score
                FROM hook_formulas 
                WHERE german_specific = 1
                ORDER BY created_at DESC
                LIMIT 100
            """)
            
            hooks_data = cursor.fetchall()
            
        if not hooks_data:
            return
        
        # Extract hook texts for pattern analysis
        hook_texts = [row[0] for row in hooks_data]
        
        # Analyze patterns
        try:
            hook_vectors = self.learning_models['hook_analyzer'].fit_transform(hook_texts)
            
            # Cluster similar hooks
            n_clusters = min(5, len(hook_texts))
            if n_clusters > 1:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(hook_vectors)
                
                # Store cluster patterns
                for i, cluster in enumerate(set(clusters)):
                    cluster_hooks = [hook_texts[j] for j, c in enumerate(clusters) if c == cluster]
                    
                    pattern_data = {
                        'cluster_id': int(cluster),
                        'representative_hooks': cluster_hooks[:3],
                        'pattern_strength': float(np.mean([row[3] for j, row in enumerate(hooks_data) if clusters[j] == cluster])),
                        'hook_count': len(cluster_hooks)
                    }
                    
                    await self._save_learned_pattern(
                        'hook_cluster',
                        f'German Hook Pattern {cluster}',
                        pattern_data,
                        pattern_data['pattern_strength']
                    )
            
        except Exception as e:
            logger.warning(f"Hook pattern learning failed: {e}")
    
    async def _learn_funnel_patterns(self):
        """Learn funnel patterns from ingested data"""
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT funnel_type, stages_data, pricing_data, performance_data
                FROM funnel_structures 
                ORDER BY created_at DESC
                LIMIT 50
            """)
            
            funnels_data = cursor.fetchall()
            
        if not funnels_data:
            return
        
        # Analyze funnel types and structures
        funnel_types = {}
        for row in funnels_data:
            funnel_type = row[0]
            if funnel_type not in funnel_types:
                funnel_types[funnel_type] = []
            
            funnel_types[funnel_type].append({
                'stages': json.loads(row[1]) if row[1] else {},
                'pricing': json.loads(row[2]) if row[2] else {},
                'performance': json.loads(row[3]) if row[3] else {}
            })
        
        # Extract patterns for each funnel type
        for funnel_type, funnels in funnel_types.items():
            if len(funnels) >= 2:  # Need at least 2 examples to find patterns
                
                pattern_data = {
                    'funnel_type': funnel_type,
                    'common_stages': self._extract_common_funnel_stages(funnels),
                    'pricing_patterns': self._extract_pricing_patterns(funnels),
                    'performance_metrics': self._extract_performance_patterns(funnels),
                    'sample_count': len(funnels)
                }
                
                await self._save_learned_pattern(
                    'funnel_structure',
                    f'German {funnel_type} Funnel Pattern',
                    pattern_data,
                    0.8  # Default confidence
                )
    
    async def _learn_strategy_patterns(self):
        """Learn strategy patterns from ingested data"""
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT strategy_name, implementation_details, trend_status, market_fit_score
                FROM strategy_innovations 
                WHERE trend_status IN ('emerging', 'established')
                ORDER BY market_fit_score DESC
                LIMIT 30
            """)
            
            strategies_data = cursor.fetchall()
            
        if not strategies_data:
            return
        
        # Group strategies by trend status
        emerging_strategies = []
        established_strategies = []
        
        for row in strategies_data:
            strategy_data = {
                'name': row[0],
                'implementation': json.loads(row[1]) if row[1] else {},
                'market_fit': row[3]
            }
            
            if row[2] == 'emerging':
                emerging_strategies.append(strategy_data)
            else:
                established_strategies.append(strategy_data)
        
        # Save strategy patterns
        if emerging_strategies:
            await self._save_learned_pattern(
                'emerging_strategies',
                'German Emerging Marketing Strategies 2024/2025',
                {
                    'strategies': emerging_strategies[:5],  # Top 5
                    'average_market_fit': np.mean([s['market_fit'] for s in emerging_strategies]),
                    'trend_indicators': self._extract_trend_indicators(emerging_strategies)
                },
                0.9
            )
        
        if established_strategies:
            await self._save_learned_pattern(
                'established_strategies',
                'German Established Marketing Strategies',
                {
                    'strategies': established_strategies[:5],  # Top 5
                    'average_market_fit': np.mean([s['market_fit'] for s in established_strategies]),
                    'success_factors': self._extract_success_factors(established_strategies)
                },
                0.95
            )
    
    def _extract_common_funnel_stages(self, funnels: List[Dict]) -> List[str]:
        """Extract common funnel stages from multiple funnels"""
        stage_counts = {}
        
        for funnel in funnels:
            stages = funnel.get('stages', {})
            for stage_name in stages.keys():
                stage_counts[stage_name] = stage_counts.get(stage_name, 0) + 1
        
        # Return stages that appear in at least 50% of funnels
        threshold = len(funnels) * 0.5
        return [stage for stage, count in stage_counts.items() if count >= threshold]
    
    def _extract_pricing_patterns(self, funnels: List[Dict]) -> Dict[str, Any]:
        """Extract pricing patterns from multiple funnels"""
        prices = []
        
        for funnel in funnels:
            pricing = funnel.get('pricing', {})
            if pricing:
                prices.append(pricing)
        
        if not prices:
            return {}
        
        return {
            'common_price_points': self._find_common_price_points(prices),
            'pricing_strategies': self._identify_pricing_strategies(prices),
            'average_ranges': self._calculate_price_ranges(prices)
        }
    
    def _extract_performance_patterns(self, funnels: List[Dict]) -> Dict[str, Any]:
        """Extract performance patterns from multiple funnels"""
        performances = []
        
        for funnel in funnels:
            performance = funnel.get('performance', {})
            if performance:
                performances.append(performance)
        
        if not performances:
            return {}
        
        return {
            'average_conversion_rates': self._calculate_average_conversions(performances),
            'success_indicators': self._identify_success_indicators(performances),
            'performance_benchmarks': self._establish_benchmarks(performances)
        }
    
    def _extract_trend_indicators(self, strategies: List[Dict]) -> List[str]:
        """Extract trend indicators from emerging strategies"""
        # Simplified implementation
        indicators = []
        for strategy in strategies:
            impl = strategy.get('implementation', {})
            if 'ai' in str(impl).lower():
                indicators.append('AI Integration')
            if 'video' in str(impl).lower():
                indicators.append('Video Content Focus')
            if 'automation' in str(impl).lower():
                indicators.append('Marketing Automation')
        
        return list(set(indicators))
    
    def _extract_success_factors(self, strategies: List[Dict]) -> List[str]:
        """Extract success factors from established strategies"""
        # Simplified implementation
        factors = []
        high_performing = [s for s in strategies if s['market_fit'] > 0.8]
        
        for strategy in high_performing:
            impl = strategy.get('implementation', {})
            if 'personalization' in str(impl).lower():
                factors.append('Personalization')
            if 'community' in str(impl).lower():
                factors.append('Community Building')
            if 'value' in str(impl).lower():
                factors.append('Value-First Approach')
        
        return list(set(factors))
    
    def _find_common_price_points(self, prices: List[Dict]) -> List[float]:
        """Find common price points across funnels"""
        # Simplified implementation
        all_prices = []
        for pricing in prices:
            for key, value in pricing.items():
                if isinstance(value, (int, float)) and value > 0:
                    all_prices.append(float(value))
        
        if not all_prices:
            return []
        
        # Find clusters of similar prices
        unique_prices = list(set(all_prices))
        unique_prices.sort()
        
        return unique_prices[:5]  # Return top 5 most common price points
    
    def _identify_pricing_strategies(self, prices: List[Dict]) -> List[str]:
        """Identify pricing strategies from pricing data"""
        strategies = []
        
        for pricing in prices:
            if len(pricing) >= 3:
                strategies.append('Tiered Pricing')
            if any('free' in str(k).lower() for k in pricing.keys()):
                strategies.append('Freemium Model')
            if any(v > 1000 for v in pricing.values() if isinstance(v, (int, float))):
                strategies.append('Premium Positioning')
        
        return list(set(strategies))
    
    def _calculate_price_ranges(self, prices: List[Dict]) -> Dict[str, float]:
        """Calculate average price ranges"""
        all_prices = []
        for pricing in prices:
            for value in pricing.values():
                if isinstance(value, (int, float)) and value > 0:
                    all_prices.append(float(value))
        
        if not all_prices:
            return {}
        
        return {
            'min_price': min(all_prices),
            'max_price': max(all_prices),
            'average_price': np.mean(all_prices),
            'median_price': np.median(all_prices)
        }
    
    def _calculate_average_conversions(self, performances: List[Dict]) -> Dict[str, float]:
        """Calculate average conversion rates"""
        conversions = []
        
        for perf in performances:
            if 'conversion_rate' in perf:
                conversions.append(float(perf['conversion_rate']))
        
        if not conversions:
            return {}
        
        return {
            'average_conversion': np.mean(conversions),
            'median_conversion': np.median(conversions),
            'best_conversion': max(conversions)
        }
    
    def _identify_success_indicators(self, performances: List[Dict]) -> List[str]:
        """Identify common success indicators"""
        indicators = set()
        
        for perf in performances:
            for key in perf.keys():
                if 'rate' in key.lower() or 'score' in key.lower():
                    indicators.add(key)
        
        return list(indicators)
    
    def _establish_benchmarks(self, performances: List[Dict]) -> Dict[str, Any]:
        """Establish performance benchmarks"""
        benchmarks = {}
        
        # Collect all numeric performance metrics
        metrics = {}
        for perf in performances:
            for key, value in perf.items():
                if isinstance(value, (int, float)):
                    if key not in metrics:
                        metrics[key] = []
                    metrics[key].append(float(value))
        
        # Calculate benchmarks for each metric
        for metric, values in metrics.items():
            if values:
                benchmarks[metric] = {
                    'average': np.mean(values),
                    'top_quartile': np.percentile(values, 75),
                    'top_10_percent': np.percentile(values, 90)
                }
        
        return benchmarks
    
    async def _save_influencer_profile(self, profile: GermanInfluencerProfile) -> int:
        """Save influencer profile to database"""
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                INSERT INTO german_influencers 
                (name, handle, primary_platform, tier, niche, followers_data,
                 content_analysis, funnel_structure, current_strategies,
                 performance_metrics, research_metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.name,
                profile.handle,
                profile.primary_platform,
                profile.tier.value,
                profile.niche,
                json.dumps(profile.followers),
                json.dumps({
                    'content_themes': profile.content_themes,
                    'posting_frequency': profile.posting_frequency,
                    'content_formats': profile.content_formats
                }),
                json.dumps({
                    'funnel_type': profile.funnel_type,
                    'funnel_stages': profile.funnel_stages,
                    'lead_magnets': profile.lead_magnets,
                    'pricing_strategy': profile.pricing_strategy,
                    'products_services': profile.products_services
                }),
                json.dumps({
                    'current_hooks': profile.current_hooks,
                    'hook_patterns': profile.hook_patterns,
                    'trending_strategies': profile.trending_strategies,
                    'content_innovations': profile.content_innovations
                }),
                json.dumps({
                    'engagement_rate': profile.engagement_rate,
                    'estimated_revenue': profile.estimated_revenue,
                    'conversion_indicators': profile.conversion_indicators
                }),
                json.dumps({
                    'research_source': profile.research_source.value,
                    'research_date': profile.research_date.isoformat(),
                    'confidence_score': profile.confidence_score,
                    'verification_status': profile.verification_status,
                    'profile_urls': profile.profile_urls,
                    'funnel_examples': profile.funnel_examples,
                    'case_study_links': profile.case_study_links
                })
            ))
            
            return cursor.lastrowid
    
    async def _save_funnel_structure(self, funnel: FunnelStructure) -> int:
        """Save funnel structure to database"""
        
        # First, find the influencer ID
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT id FROM german_influencers WHERE name = ?
            """, (funnel.influencer_name,))
            
            result = cursor.fetchone()
            influencer_id = result[0] if result else None
            
            # Insert funnel structure
            cursor = conn.execute("""
                INSERT INTO funnel_structures 
                (influencer_id, funnel_name, funnel_type, stages_data,
                 pricing_data, hooks_strategies, performance_data, innovations_2024_2025)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                influencer_id,
                funnel.funnel_name,
                funnel.funnel_type,
                json.dumps({
                    'awareness_stage': funnel.awareness_stage,
                    'interest_stage': funnel.interest_stage,
                    'consideration_stage': funnel.consideration_stage,
                    'conversion_stage': funnel.conversion_stage,
                    'retention_stage': funnel.retention_stage
                }),
                json.dumps({
                    'entry_price': funnel.entry_price,
                    'mid_tier_price': funnel.mid_tier_price,
                    'premium_price': funnel.premium_price,
                    'pricing_psychology': funnel.pricing_psychology
                }),
                json.dumps({
                    'primary_hooks': funnel.primary_hooks,
                    'secondary_hooks': funnel.secondary_hooks,
                    'urgency_tactics': funnel.urgency_tactics,
                    'social_proof_elements': funnel.social_proof_elements
                }),
                json.dumps({
                    'estimated_conversion_rate': funnel.estimated_conversion_rate,
                    'estimated_monthly_revenue': funnel.estimated_monthly_revenue,
                    'success_indicators': funnel.success_indicators
                }),
                json.dumps({
                    'new_strategies': funnel.new_strategies,
                    'trend_adaptations': funnel.trend_adaptations,
                    'platform_specific_tactics': funnel.platform_specific_tactics
                })
            ))
            
            return cursor.lastrowid
    
    async def _save_learned_pattern(self, 
                                  pattern_type: str,
                                  pattern_name: str,
                                  pattern_data: Dict[str, Any],
                                  effectiveness_score: float):
        """Save a learned pattern to database"""
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO learned_patterns 
                (pattern_type, pattern_name, pattern_data, effectiveness_score,
                 market_segment, confidence_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pattern_type,
                pattern_name,
                json.dumps(pattern_data),
                effectiveness_score,
                'german_online_marketing',
                0.8  # Default confidence
            ))
    
    async def _save_research_session(self,
                                   session_name: str,
                                   researcher_name: str,
                                   research_source: ResearchSource,
                                   influencers_count: int,
                                   patterns_count: int):
        """Save research session metadata"""
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT INTO research_sessions 
                (session_name, research_source, researcher_name, session_date,
                 influencers_researched, patterns_discovered, quality_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session_name,
                research_source.value,
                researcher_name,
                datetime.now(),
                influencers_count,
                patterns_count,
                0.9  # Default quality score
            ))
    
    async def _update_learned_patterns(self):
        """Update pattern statistics and effectiveness scores"""
        
        with sqlite3.connect(self.database_path) as conn:
            # Update frequency counts
            conn.execute("""
                UPDATE learned_patterns 
                SET frequency_count = frequency_count + 1,
                    last_updated = CURRENT_TIMESTAMP
                WHERE pattern_type IN ('hook_cluster', 'funnel_structure', 'emerging_strategies')
            """)
            
        self.ingestion_stats['patterns_extracted'] += 1
    
    def get_ingestion_stats(self) -> Dict[str, Any]:
        """Get current ingestion statistics"""
        return {
            **self.ingestion_stats,
            'database_path': self.database_path,
            'last_updated': datetime.now().isoformat()
        }
    
    async def export_learned_patterns(self, pattern_type: str = None) -> Dict[str, Any]:
        """Export learned patterns for use in autonomous research"""
        
        with sqlite3.connect(self.database_path) as conn:
            if pattern_type:
                cursor = conn.execute("""
                    SELECT pattern_name, pattern_data, effectiveness_score, confidence_level
                    FROM learned_patterns 
                    WHERE pattern_type = ?
                    ORDER BY effectiveness_score DESC
                """, (pattern_type,))
            else:
                cursor = conn.execute("""
                    SELECT pattern_type, pattern_name, pattern_data, effectiveness_score, confidence_level
                    FROM learned_patterns 
                    ORDER BY pattern_type, effectiveness_score DESC
                """)
            
            patterns = cursor.fetchall()
            
        if not patterns:
            return {}
        
        exported_patterns = {}
        for row in patterns:
            if pattern_type:
                pattern_name, pattern_data, effectiveness, confidence = row
                pattern_key = pattern_name
            else:
                pattern_type_key, pattern_name, pattern_data, effectiveness, confidence = row
                if pattern_type_key not in exported_patterns:
                    exported_patterns[pattern_type_key] = {}
                pattern_key = pattern_name
            
            try:
                data = json.loads(pattern_data)
                if pattern_type:
                    exported_patterns[pattern_key] = {
                        'data': data,
                        'effectiveness_score': effectiveness,
                        'confidence_level': confidence
                    }
                else:
                    exported_patterns[pattern_type_key][pattern_key] = {
                        'data': data,
                        'effectiveness_score': effectiveness,
                        'confidence_level': confidence
                    }
            except json.JSONDecodeError:
                continue
        
        return exported_patterns

# Example usage and testing
if __name__ == "__main__":
    async def test_ingestion():
        # Initialize ingestion system
        ingestion_system = ResearchDataIngestion()
        
        # Example research data
        example_data = {
            'influencers': [
                {
                    'name': 'Tobias Beck',
                    'handle': '@tobiasxbeck',
                    'platforms': ['Instagram', 'YouTube', 'LinkedIn'],
                    'primary_platform': 'Instagram',
                    'followers': {'instagram': 850000, 'youtube': 320000},
                    'tier': 'macro',
                    'niche': 'personal_development',
                    'sub_niches': ['business_mindset', 'success_coaching'],
                    'content_themes': ['Mindset', 'Erfolg', 'Persönlichkeitsentwicklung'],
                    'funnel_type': 'coaching_program',
                    'current_hooks': [
                        'Das haben 99% der Menschen noch nie gehört...',
                        'Warum reiche Menschen anders denken',
                        'Der Mindset-Fehler, der dich arm hält'
                    ],
                    'pricing_strategy': {'entry': 97, 'premium': 2997},
                    'confidence_score': 0.95
                }
            ],
            'hooks': [
                {
                    'hook_text': 'Das haben 99% der Menschen noch nie gehört...',
                    'hook_category': 'curiosity',
                    'effectiveness_score': 0.89,
                    'german_specific': True,
                    'psychological_trigger': 'exclusivity'
                }
            ],
            'strategies': [
                {
                    'strategy_name': 'Story-driven Content Marketing',
                    'strategy_description': 'Personal story integration in all content',
                    'trend_status': 'established',
                    'market_fit_score': 0.92
                }
            ]
        }
        
        # Ingest the data
        session_id = await ingestion_system.ingest_research_session(
            session_name="German Marketing Influencers Research",
            researcher_name="Manual Research",
            research_source=ResearchSource.MANUAL_HUMAN,
            data=example_data
        )
        
        print(f"Research session ingested: {session_id}")
        print(f"Stats: {ingestion_system.get_ingestion_stats()}")
        
        # Export learned patterns
        patterns = await ingestion_system.export_learned_patterns()
        print(f"Learned patterns: {json.dumps(patterns, indent=2, ensure_ascii=False)}")
    
    # Run test
    asyncio.run(test_ingestion())