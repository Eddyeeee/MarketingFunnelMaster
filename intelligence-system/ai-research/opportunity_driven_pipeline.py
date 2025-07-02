#!/usr/bin/env python3
"""
Opportunity-Driven Research Pipeline

Automatically triggers creator analysis for ANY opportunity found by the intelligence system.
Completely automated workflow that:
1. Detects opportunity niche
2. Finds relevant creators
3. Analyzes their strategies
4. Generates custom approach
5. No manual configuration needed!
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
import sqlite3
from datetime import datetime, timedelta
import time
from pathlib import Path
import os

# Import our custom analyzers
from .analyzers.universal_niche_detector import UniversalNicheDetector, NicheDetectionResult, NicheCategory
from .analyzers.universal_creator_analyzer import UniversalCreatorAnalyzer, NicheCreatorInsights, CreatorProfile, Platform
from .analyzers.universal_pattern_extractor import UniversalPatternExtractor, PatternAnalysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PipelineStatus(Enum):
    """Pipeline execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class OpportunityType(Enum):
    """Types of opportunities the pipeline can handle"""
    AFFILIATE_PRODUCT = "affiliate_product"
    TRENDING_TOPIC = "trending_topic"
    SOCIAL_TREND = "social_trend"
    MARKET_GAP = "market_gap"
    SEASONAL_OPPORTUNITY = "seasonal_opportunity"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    CONTENT_OPPORTUNITY = "content_opportunity"

@dataclass
class OpportunityInput:
    """Input data for opportunity analysis"""
    opportunity_id: str
    opportunity_type: OpportunityType
    title: str
    description: str
    platform: str
    source: str
    metadata: Dict[str, Any]
    priority_score: float
    created_at: datetime
    raw_data: Dict[str, Any]

@dataclass
class CreatorIntelligenceResult:
    """Result of creator intelligence analysis"""
    opportunity_id: str
    niche_analysis: NicheDetectionResult
    creator_insights: NicheCreatorInsights
    pattern_analysis: PatternAnalysis
    recommended_strategy: Dict[str, Any]
    implementation_plan: List[Dict[str, Any]]
    success_probability: float
    investment_required: str
    timeline_estimate: str
    key_insights: List[str]
    competitive_advantages: List[str]
    potential_risks: List[str]
    next_actions: List[str]

@dataclass
class PipelineExecution:
    """Pipeline execution tracking"""
    execution_id: str
    opportunity_id: str
    status: PipelineStatus
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: float
    result: Optional[CreatorIntelligenceResult]
    error_message: Optional[str]
    progress_log: List[str]

class OpportunityDrivenPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self, 
                 config: Dict[str, Any] = None,
                 database_path: str = None):
        
        self.config = config or self._load_default_config()
        self.database_path = database_path or self._get_database_path()
        
        # Initialize analyzers
        self.niche_detector = UniversalNicheDetector(
            openai_api_key=self.config.get('openai_api_key'),
            claude_api_key=self.config.get('claude_api_key')
        )
        
        self.creator_analyzer = UniversalCreatorAnalyzer(
            youtube_api_key=self.config.get('youtube_api_key'),
            openai_api_key=self.config.get('openai_api_key'),
            claude_api_key=self.config.get('claude_api_key')
        )
        
        self.pattern_extractor = UniversalPatternExtractor(
            openai_api_key=self.config.get('openai_api_key')
        )
        
        # Initialize database
        self._initialize_database()
        
        # Execution tracking
        self.active_executions: Dict[str, PipelineExecution] = {}
        self.max_concurrent_executions = self.config.get('max_concurrent_executions', 3)
        
        # Queue for pending opportunities
        self.opportunity_queue: List[OpportunityInput] = []
        
        # Statistics
        self.stats = {
            'total_opportunities_processed': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'average_processing_time': 0.0,
            'niches_discovered': set(),
            'creators_analyzed': 0
        }
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            'max_concurrent_executions': 3,
            'max_creators_per_niche': 50,
            'analysis_timeout_minutes': 30,
            'retry_failed_analyses': True,
            'max_retries': 2,
            'save_detailed_logs': True,
            'auto_generate_reports': True,
            'notification_webhooks': [],
            'rate_limits': {
                'youtube_api': 100,  # requests per hour
                'openai_api': 50,    # requests per hour
                'general_scraping': 30  # requests per minute
            }
        }
    
    def _get_database_path(self) -> str:
        """Get database path"""
        base_path = Path(__file__).parent.parent
        db_path = base_path / "databases" / "creator_intelligence.db"
        db_path.parent.mkdir(exist_ok=True)
        return str(db_path)
    
    def _initialize_database(self):
        """Initialize SQLite database for pipeline data"""
        
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS pipeline_executions (
            execution_id TEXT PRIMARY KEY,
            opportunity_id TEXT NOT NULL,
            status TEXT NOT NULL,
            started_at TIMESTAMP NOT NULL,
            completed_at TIMESTAMP,
            duration_seconds REAL,
            error_message TEXT,
            progress_log TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS opportunity_analyses (
            opportunity_id TEXT PRIMARY KEY,
            opportunity_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            platform TEXT,
            source TEXT,
            metadata TEXT,
            priority_score REAL,
            niche_analysis TEXT,
            creator_insights TEXT,
            pattern_analysis TEXT,
            recommended_strategy TEXT,
            success_probability REAL,
            key_insights TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS discovered_niches (
            niche_id TEXT PRIMARY KEY,
            niche_name TEXT NOT NULL,
            category TEXT NOT NULL,
            confidence_score REAL,
            keywords TEXT,
            language TEXT,
            opportunities_count INTEGER DEFAULT 1,
            first_discovered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS analyzed_creators (
            creator_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            handle TEXT,
            url TEXT,
            followers INTEGER,
            engagement_rate REAL,
            niche TEXT,
            influence_score REAL,
            analysis_data TEXT,
            opportunities_related TEXT,
            first_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS extracted_patterns (
            pattern_id TEXT PRIMARY KEY,
            pattern_type TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            effectiveness_score REAL,
            frequency INTEGER,
            examples TEXT,
            applicable_niches TEXT,
            platform_compatibility TEXT,
            first_extracted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usage_count INTEGER DEFAULT 1
        );
        
        CREATE INDEX IF NOT EXISTS idx_executions_status ON pipeline_executions(status);
        CREATE INDEX IF NOT EXISTS idx_executions_opportunity ON pipeline_executions(opportunity_id);
        CREATE INDEX IF NOT EXISTS idx_analyses_type ON opportunity_analyses(opportunity_type);
        CREATE INDEX IF NOT EXISTS idx_analyses_priority ON opportunity_analyses(priority_score);
        CREATE INDEX IF NOT EXISTS idx_niches_category ON discovered_niches(category);
        CREATE INDEX IF NOT EXISTS idx_creators_platform ON analyzed_creators(platform);
        CREATE INDEX IF NOT EXISTS idx_creators_niche ON analyzed_creators(niche);
        CREATE INDEX IF NOT EXISTS idx_patterns_type ON extracted_patterns(pattern_type);
        """
        
        with sqlite3.connect(self.database_path) as conn:
            conn.executescript(create_tables_sql)
    
    def add_opportunity(self, opportunity: OpportunityInput) -> str:
        """Add opportunity to processing queue"""
        
        # Check if opportunity already exists
        if self._opportunity_exists(opportunity.opportunity_id):
            logger.info(f"Opportunity {opportunity.opportunity_id} already processed, skipping")
            return opportunity.opportunity_id
        
        # Add to queue
        self.opportunity_queue.append(opportunity)
        
        logger.info(f"Added opportunity '{opportunity.title}' to processing queue")
        
        # Start processing if under concurrent limit
        if len(self.active_executions) < self.max_concurrent_executions:
            asyncio.create_task(self._process_next_opportunity())
        
        return opportunity.opportunity_id
    
    def _opportunity_exists(self, opportunity_id: str) -> bool:
        """Check if opportunity has already been processed"""
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM opportunity_analyses WHERE opportunity_id = ?",
                (opportunity_id,)
            )
            count = cursor.fetchone()[0]
            return count > 0
    
    async def _process_next_opportunity(self):
        """Process the next opportunity in the queue"""
        
        if not self.opportunity_queue:
            return
        
        if len(self.active_executions) >= self.max_concurrent_executions:
            return
        
        # Get next opportunity
        opportunity = self.opportunity_queue.pop(0)
        
        # Create execution tracking
        execution_id = f"exec_{opportunity.opportunity_id}_{int(time.time())}"
        execution = PipelineExecution(
            execution_id=execution_id,
            opportunity_id=opportunity.opportunity_id,
            status=PipelineStatus.PENDING,
            started_at=datetime.now(),
            completed_at=None,
            duration_seconds=0.0,
            result=None,
            error_message=None,
            progress_log=[]
        )
        
        self.active_executions[execution_id] = execution
        
        try:
            # Process the opportunity
            result = await self._execute_pipeline(opportunity, execution)
            
            # Update execution
            execution.status = PipelineStatus.COMPLETED
            execution.completed_at = datetime.now()
            execution.duration_seconds = (execution.completed_at - execution.started_at).total_seconds()
            execution.result = result
            
            # Update statistics
            self.stats['successful_analyses'] += 1
            self.stats['total_opportunities_processed'] += 1
            
            logger.info(f"Successfully processed opportunity '{opportunity.title}' in {execution.duration_seconds:.1f}s")
            
        except Exception as e:
            # Handle error
            execution.status = PipelineStatus.FAILED
            execution.completed_at = datetime.now()
            execution.duration_seconds = (execution.completed_at - execution.started_at).total_seconds()
            execution.error_message = str(e)
            
            # Update statistics
            self.stats['failed_analyses'] += 1
            self.stats['total_opportunities_processed'] += 1
            
            logger.error(f"Failed to process opportunity '{opportunity.title}': {e}")
        
        finally:
            # Save execution to database
            self._save_execution(execution)
            
            # Remove from active executions
            del self.active_executions[execution_id]
            
            # Process next opportunity if queue not empty
            if self.opportunity_queue:
                asyncio.create_task(self._process_next_opportunity())
    
    async def _execute_pipeline(self, opportunity: OpportunityInput, execution: PipelineExecution) -> CreatorIntelligenceResult:
        """Execute the complete pipeline for an opportunity"""
        
        execution.progress_log.append(f"Starting pipeline for opportunity: {opportunity.title}")
        execution.status = PipelineStatus.RUNNING
        
        # Step 1: Detect niche
        execution.progress_log.append("Step 1: Detecting niche...")
        niche_analysis = await self._detect_opportunity_niche(opportunity, execution)
        
        # Step 2: Find creators in the niche
        execution.progress_log.append(f"Step 2: Finding creators in niche: {niche_analysis.primary_niche.value}")
        creator_insights = await self._analyze_niche_creators(niche_analysis, execution)
        
        # Step 3: Extract patterns from creators
        execution.progress_log.append("Step 3: Extracting universal patterns...")
        pattern_analysis = await self._extract_creator_patterns(creator_insights, execution)
        
        # Step 4: Generate strategy recommendations
        execution.progress_log.append("Step 4: Generating strategy recommendations...")
        strategy = await self._generate_strategy(opportunity, niche_analysis, creator_insights, pattern_analysis, execution)
        
        # Step 5: Create implementation plan
        execution.progress_log.append("Step 5: Creating implementation plan...")
        implementation_plan = await self._create_implementation_plan(strategy, execution)
        
        # Step 6: Calculate success metrics
        execution.progress_log.append("Step 6: Calculating success probability...")
        success_probability = self._calculate_success_probability(niche_analysis, creator_insights, pattern_analysis)
        
        # Step 7: Generate insights and recommendations
        execution.progress_log.append("Step 7: Generating final insights...")
        key_insights, competitive_advantages, potential_risks, next_actions = await self._generate_insights(
            opportunity, niche_analysis, creator_insights, pattern_analysis, strategy
        )
        
        # Create result
        result = CreatorIntelligenceResult(
            opportunity_id=opportunity.opportunity_id,
            niche_analysis=niche_analysis,
            creator_insights=creator_insights,
            pattern_analysis=pattern_analysis,
            recommended_strategy=strategy,
            implementation_plan=implementation_plan,
            success_probability=success_probability,
            investment_required="Medium",  # Would be calculated based on strategy
            timeline_estimate="2-4 weeks",  # Would be calculated based on implementation plan
            key_insights=key_insights,
            competitive_advantages=competitive_advantages,
            potential_risks=potential_risks,
            next_actions=next_actions
        )
        
        # Save result to database
        await self._save_analysis_result(opportunity, result)
        
        execution.progress_log.append("Pipeline completed successfully!")
        
        return result
    
    async def _detect_opportunity_niche(self, opportunity: OpportunityInput, execution: PipelineExecution) -> NicheDetectionResult:
        """Detect the niche of the opportunity"""
        
        # Prepare content for niche detection
        content = f"{opportunity.title} {opportunity.description}"
        additional_context = f"Platform: {opportunity.platform} Source: {opportunity.source}"
        
        # Add metadata context
        if opportunity.metadata:
            metadata_text = " ".join(str(v) for v in opportunity.metadata.values() if v)
            additional_context += f" {metadata_text}"
        
        # Detect niche
        niche_result = await self.niche_detector.detect_niche(content, additional_context)
        
        # Save niche to database
        await self._save_discovered_niche(niche_result)
        
        execution.progress_log.append(f"Detected niche: {niche_result.primary_niche.value} (confidence: {niche_result.confidence_score:.2f})")
        
        return niche_result
    
    async def _analyze_niche_creators(self, niche_analysis: NicheDetectionResult, execution: PipelineExecution) -> NicheCreatorInsights:
        """Analyze creators in the detected niche"""
        
        niche_name = niche_analysis.primary_niche.value.replace('_', ' ')
        language = niche_analysis.language
        
        # Get creator insights
        creator_insights = await self.creator_analyzer.get_niche_creator_insights(niche_name, language)
        
        # Save creators to database
        for creator in creator_insights.top_creators:
            await self._save_analyzed_creator(creator, niche_name)
        
        execution.progress_log.append(f"Found {len(creator_insights.top_creators)} creators, analyzed top {len(creator_insights.creator_analyses)}")
        
        # Update statistics
        self.stats['creators_analyzed'] += len(creator_insights.top_creators)
        self.stats['niches_discovered'].add(niche_name)
        
        return creator_insights
    
    async def _extract_creator_patterns(self, creator_insights: NicheCreatorInsights, execution: PipelineExecution) -> PatternAnalysis:
        """Extract patterns from creator content"""
        
        # Prepare content data for pattern extraction
        content_data = []
        
        for creator in creator_insights.top_creators[:10]:  # Analyze top 10 creators
            content_sample = {
                'title': f"Content from {creator.name}",
                'content': f"Creator in {creator.niche} with {creator.followers:,} followers",
                'platform': creator.platform.value,
                'engagement_rate': creator.engagement_rate,
                'views': creator.average_views,
                'niche': creator.niche,
                'content_style': creator.content_style
            }
            content_data.append(content_sample)
        
        # Extract patterns
        pattern_analysis = await self.pattern_extractor.analyze_universal_patterns(content_data)
        
        # Save patterns to database
        for pattern in pattern_analysis.viral_triggers + pattern_analysis.engagement_patterns:
            await self._save_extracted_pattern(pattern)
        
        execution.progress_log.append(f"Extracted {len(pattern_analysis.universal_hooks)} hooks, {len(pattern_analysis.viral_triggers)} viral triggers")
        
        return pattern_analysis
    
    async def _generate_strategy(self, 
                               opportunity: OpportunityInput,
                               niche_analysis: NicheDetectionResult,
                               creator_insights: NicheCreatorInsights,
                               pattern_analysis: PatternAnalysis,
                               execution: PipelineExecution) -> Dict[str, Any]:
        """Generate custom strategy based on analysis"""
        
        # Determine primary platform based on creator distribution
        platform_scores = creator_insights.platform_distribution
        primary_platform = max(platform_scores, key=platform_scores.get).value if platform_scores else "youtube"
        
        # Select top strategies from pattern analysis
        top_hooks = pattern_analysis.universal_hooks[:3]
        top_viral_triggers = pattern_analysis.viral_triggers[:3]
        top_engagement_tactics = pattern_analysis.engagement_patterns[:5]
        
        # Create strategy
        strategy = {
            'approach': 'creator_inspired_content',
            'primary_platform': primary_platform,
            'target_niche': niche_analysis.primary_niche.value,
            'content_strategy': {
                'primary_hook_formulas': [hook.name for hook in top_hooks],
                'viral_triggers': [trigger.name for trigger in top_viral_triggers],
                'engagement_tactics': [tactic.name for tactic in top_engagement_tactics],
                'content_formats': creator_insights.trending_formats[:3],
                'posting_frequency': 'daily' if primary_platform == 'tiktok' else 'weekly'
            },
            'creator_collaboration': {
                'target_creators': [creator.name for creator in creator_insights.top_creators[:5]],
                'collaboration_types': ['sponsored_content', 'affiliate_partnership', 'guest_appearance'],
                'budget_range': 'medium'
            },
            'monetization_strategy': {
                'primary_method': 'affiliate_marketing',
                'secondary_methods': creator_insights.monetization_trends[:3],
                'revenue_streams': ['commissions', 'sponsored_content', 'course_sales']
            },
            'competitive_positioning': {
                'unique_angles': niche_analysis.sub_niches[:3],
                'differentiation_strategy': 'authenticity_and_results',
                'target_audience': niche_analysis.target_audience
            }
        }
        
        execution.progress_log.append(f"Generated strategy for {primary_platform} with {len(top_hooks)} hook formulas")
        
        return strategy
    
    async def _create_implementation_plan(self, strategy: Dict[str, Any], execution: PipelineExecution) -> List[Dict[str, Any]]:
        """Create detailed implementation plan"""
        
        plan = [
            {
                'phase': 'Content Planning',
                'duration': '3-5 days',
                'tasks': [
                    'Research top-performing content in niche',
                    'Create content calendar with hook formulas',
                    'Develop brand voice and visual identity',
                    'Set up content creation workflow'
                ],
                'deliverables': ['Content calendar', 'Brand guidelines', 'Content templates']
            },
            {
                'phase': 'Platform Setup',
                'duration': '2-3 days',
                'tasks': [
                    f'Optimize {strategy["primary_platform"]} profile',
                    'Create compelling bio and profile picture',
                    'Set up analytics tracking',
                    'Research optimal posting times'
                ],
                'deliverables': ['Optimized profiles', 'Analytics setup', 'Posting schedule']
            },
            {
                'phase': 'Content Creation',
                'duration': '1-2 weeks',
                'tasks': [
                    'Create first batch of content using identified hooks',
                    'Test different viral triggers',
                    'Implement engagement tactics',
                    'A/B test thumbnail styles'
                ],
                'deliverables': ['Content library', 'Performance baselines', 'Optimization insights']
            },
            {
                'phase': 'Creator Outreach',
                'duration': '1 week',
                'tasks': [
                    'Identify collaboration opportunities',
                    'Craft personalized outreach messages',
                    'Negotiate partnership terms',
                    'Plan collaborative content'
                ],
                'deliverables': ['Outreach list', 'Partnership agreements', 'Collaboration calendar']
            },
            {
                'phase': 'Launch & Optimize',
                'duration': 'Ongoing',
                'tasks': [
                    'Execute content publishing schedule',
                    'Monitor performance metrics',
                    'Optimize based on results',
                    'Scale successful strategies'
                ],
                'deliverables': ['Live content', 'Performance reports', 'Optimization recommendations']
            }
        ]
        
        execution.progress_log.append(f"Created {len(plan)}-phase implementation plan")
        
        return plan
    
    def _calculate_success_probability(self, 
                                     niche_analysis: NicheDetectionResult,
                                     creator_insights: NicheCreatorInsights,
                                     pattern_analysis: PatternAnalysis) -> float:
        """Calculate probability of success based on analysis"""
        
        # Factors affecting success probability
        niche_confidence = niche_analysis.confidence_score
        creator_count = min(len(creator_insights.top_creators) / 50, 1.0)  # Normalize to 0-1
        pattern_effectiveness = np.mean([hook.effectiveness_score for hook in pattern_analysis.universal_hooks[:5]])
        market_size_score = 0.8 if niche_analysis.market_size == 'large' else 0.6 if niche_analysis.market_size == 'medium' else 0.4
        
        # Weighted calculation
        success_probability = (
            niche_confidence * 0.25 +
            creator_count * 0.25 +
            pattern_effectiveness * 0.30 +
            market_size_score * 0.20
        )
        
        return min(success_probability, 0.95)  # Cap at 95%
    
    async def _generate_insights(self,
                               opportunity: OpportunityInput,
                               niche_analysis: NicheDetectionResult,
                               creator_insights: NicheCreatorInsights,
                               pattern_analysis: PatternAnalysis,
                               strategy: Dict[str, Any]) -> Tuple[List[str], List[str], List[str], List[str]]:
        """Generate key insights and recommendations"""
        
        key_insights = [
            f"Niche '{niche_analysis.primary_niche.value}' shows {niche_analysis.confidence_score:.0%} match confidence",
            f"Found {len(creator_insights.top_creators)} active creators with avg {np.mean([c.engagement_rate for c in creator_insights.top_creators[:10]]):.1%} engagement",
            f"Top performing hook formula: '{pattern_analysis.universal_hooks[0].name}' with {pattern_analysis.universal_hooks[0].effectiveness_score:.0%} effectiveness",
            f"Primary platform recommendation: {strategy['primary_platform']} based on creator distribution",
            f"Monetization potential: {niche_analysis.monetization_potential} with {len(creator_insights.monetization_trends)} identified revenue streams"
        ]
        
        competitive_advantages = [
            "Data-driven content strategy based on successful creator analysis",
            "Proven hook formulas with documented effectiveness rates",
            "Direct insight into audience psychology and engagement patterns",
            "Identified collaboration opportunities with established creators",
            "Universal patterns that work across multiple platforms"
        ]
        
        potential_risks = [
            "High competition in established niches",
            "Platform algorithm changes affecting reach",
            "Creator partnership costs and availability",
            "Content saturation in popular topics",
            "Audience fatigue with similar content formats"
        ]
        
        next_actions = [
            "Set up accounts on recommended platforms",
            "Create first content batch using identified hook formulas",
            "Reach out to top 3 creators for collaboration opportunities",
            "Implement analytics tracking for performance monitoring",
            "Schedule content publication following optimal timing patterns"
        ]
        
        return key_insights, competitive_advantages, potential_risks, next_actions
    
    async def _save_analysis_result(self, opportunity: OpportunityInput, result: CreatorIntelligenceResult):
        """Save analysis result to database"""
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO opportunity_analyses 
                (opportunity_id, opportunity_type, title, description, platform, source, metadata, 
                 priority_score, niche_analysis, creator_insights, pattern_analysis, 
                 recommended_strategy, success_probability, key_insights, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                opportunity.opportunity_id,
                opportunity.opportunity_type.value,
                opportunity.title,
                opportunity.description,
                opportunity.platform,
                opportunity.source,
                json.dumps(opportunity.metadata),
                opportunity.priority_score,
                json.dumps(asdict(result.niche_analysis), default=str),
                json.dumps(asdict(result.creator_insights), default=str),
                json.dumps(asdict(result.pattern_analysis), default=str),
                json.dumps(result.recommended_strategy),
                result.success_probability,
                json.dumps(result.key_insights)
            ))
    
    async def _save_discovered_niche(self, niche_analysis: NicheDetectionResult):
        """Save discovered niche to database"""
        
        niche_id = f"niche_{niche_analysis.primary_niche.value}_{niche_analysis.language}"
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO discovered_niches 
                (niche_id, niche_name, category, confidence_score, keywords, language, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                niche_id,
                niche_analysis.primary_niche.value,
                niche_analysis.primary_niche.value,
                niche_analysis.confidence_score,
                json.dumps(niche_analysis.keywords),
                niche_analysis.language
            ))
    
    async def _save_analyzed_creator(self, creator: CreatorProfile, niche: str):
        """Save analyzed creator to database"""
        
        creator_id = f"creator_{creator.platform.value}_{creator.handle}"
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO analyzed_creators 
                (creator_id, name, platform, handle, url, followers, engagement_rate, 
                 niche, influence_score, analysis_data, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                creator_id,
                creator.name,
                creator.platform.value,
                creator.handle,
                creator.url,
                creator.followers,
                creator.engagement_rate,
                niche,
                creator.influence_score,
                json.dumps(asdict(creator), default=str)
            ))
    
    async def _save_extracted_pattern(self, pattern):
        """Save extracted pattern to database"""
        
        pattern_id = f"pattern_{pattern.pattern_type.value}_{pattern.name.lower().replace(' ', '_')}"
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO extracted_patterns 
                (pattern_id, pattern_type, name, description, effectiveness_score, 
                 frequency, examples, applicable_niches, platform_compatibility)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern_id,
                pattern.pattern_type.value,
                pattern.name,
                pattern.description,
                pattern.effectiveness_score,
                pattern.frequency,
                json.dumps(pattern.examples),
                json.dumps(pattern.applicable_niches),
                json.dumps(pattern.platform_compatibility)
            ))
    
    def _save_execution(self, execution: PipelineExecution):
        """Save execution details to database"""
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO pipeline_executions 
                (execution_id, opportunity_id, status, started_at, completed_at, 
                 duration_seconds, error_message, progress_log)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                execution.execution_id,
                execution.opportunity_id,
                execution.status.value,
                execution.started_at,
                execution.completed_at,
                execution.duration_seconds,
                execution.error_message,
                json.dumps(execution.progress_log)
            ))
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        
        return {
            'active_executions': len(self.active_executions),
            'queued_opportunities': len(self.opportunity_queue),
            'statistics': dict(self.stats),
            'configuration': self.config,
            'database_path': self.database_path
        }
    
    def get_analysis_results(self, opportunity_id: str = None) -> List[Dict[str, Any]]:
        """Get analysis results"""
        
        with sqlite3.connect(self.database_path) as conn:
            if opportunity_id:
                cursor = conn.execute("""
                    SELECT * FROM opportunity_analyses WHERE opportunity_id = ?
                """, (opportunity_id,))
            else:
                cursor = conn.execute("""
                    SELECT * FROM opportunity_analyses ORDER BY created_at DESC LIMIT 10
                """)
            
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                result = dict(zip(columns, row))
                results.append(result)
            
            return results
    
    async def process_opportunity_from_intelligence_system(self, intelligence_data: Dict[str, Any]) -> str:
        """Process opportunity directly from intelligence system data"""
        
        # Convert intelligence system data to OpportunityInput
        opportunity = OpportunityInput(
            opportunity_id=intelligence_data.get('id', f"opp_{int(time.time())}"),
            opportunity_type=OpportunityType.AFFILIATE_PRODUCT,  # Default, could be inferred
            title=intelligence_data.get('title', intelligence_data.get('product_name', 'Unknown Opportunity')),
            description=intelligence_data.get('description', intelligence_data.get('niche', '')),
            platform=intelligence_data.get('platform', 'unknown'),
            source=intelligence_data.get('source', 'intelligence_system'),
            metadata=intelligence_data,
            priority_score=intelligence_data.get('opportunity_score', 0.5),
            created_at=datetime.now(),
            raw_data=intelligence_data
        )
        
        return self.add_opportunity(opportunity)

# Example usage and integration
if __name__ == "__main__":
    async def test_pipeline():
        # Initialize pipeline
        pipeline = OpportunityDrivenPipeline({
            'openai_api_key': 'your_key_here',  # Would come from environment
            'youtube_api_key': 'your_key_here'
        })
        
        # Test opportunity
        test_opportunity = OpportunityInput(
            opportunity_id="test_crypto_course",
            opportunity_type=OpportunityType.AFFILIATE_PRODUCT,
            title="Cryptocurrency Trading Masterclass - High Commission Affiliate Product",
            description="Learn advanced crypto trading strategies with proven results. 50% commission rate.",
            platform="digistore24",
            source="affiliate_scanner",
            metadata={
                'commission_rate': '50%',
                'price': '$197',
                'gravity': 85,
                'category': 'finance'
            },
            priority_score=0.85,
            created_at=datetime.now(),
            raw_data={}
        )
        
        # Process opportunity
        opportunity_id = pipeline.add_opportunity(test_opportunity)
        
        print(f"Processing opportunity: {opportunity_id}")
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Check status
        status = pipeline.get_pipeline_status()
        print(f"Pipeline status: {status}")
        
        # Get results
        results = pipeline.get_analysis_results(opportunity_id)
        if results:
            result = results[0]
            print(f"Analysis completed with {result['success_probability']:.0%} success probability")
        
        return pipeline
    
    # Run test
    asyncio.run(test_pipeline())