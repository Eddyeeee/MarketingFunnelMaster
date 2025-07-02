-- Creator Intelligence Database Schema
-- Stores all creator intelligence data, patterns, and analysis results

-- Main opportunity analyses table
CREATE TABLE IF NOT EXISTS opportunity_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id TEXT UNIQUE NOT NULL,
    opportunity_type TEXT NOT NULL, -- affiliate_product, social_trend, etc.
    title TEXT NOT NULL,
    description TEXT,
    platform TEXT,
    source TEXT,
    scanner_source TEXT, -- which scanner found this
    metadata TEXT, -- JSON metadata from original opportunity
    priority_score REAL DEFAULT 0.5,
    
    -- Niche Analysis Results
    niche_primary TEXT,
    niche_secondary TEXT, -- JSON array
    niche_confidence REAL DEFAULT 0.0,
    niche_keywords TEXT, -- JSON array
    niche_language TEXT DEFAULT 'en',
    niche_market_size TEXT,
    niche_competition_level TEXT,
    niche_trend_direction TEXT,
    niche_monetization_potential TEXT,
    
    -- Creator Intelligence Results
    creators_found INTEGER DEFAULT 0,
    top_creators TEXT, -- JSON array of top creators
    platform_distribution TEXT, -- JSON object
    common_strategies TEXT, -- JSON array
    trending_formats TEXT, -- JSON array
    monetization_trends TEXT, -- JSON array
    
    -- Pattern Analysis Results
    universal_hooks TEXT, -- JSON array
    viral_triggers TEXT, -- JSON array
    engagement_tactics TEXT, -- JSON array
    content_structures TEXT, -- JSON array
    thumbnail_patterns TEXT, -- JSON array
    
    -- Strategy Recommendations
    recommended_approach TEXT,
    primary_platform TEXT,
    content_strategy TEXT, -- JSON object
    creator_collaboration TEXT, -- JSON object
    monetization_strategy TEXT, -- JSON object
    competitive_positioning TEXT, -- JSON object
    
    -- Implementation Plan
    implementation_plan TEXT, -- JSON array of phases
    timeline_estimate TEXT,
    investment_required TEXT,
    next_actions TEXT, -- JSON array
    
    -- Success Metrics
    success_probability REAL DEFAULT 0.5,
    key_insights TEXT, -- JSON array
    competitive_advantages TEXT, -- JSON array
    potential_risks TEXT, -- JSON array
    
    -- Analysis Metadata
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER,
    analysis_version TEXT DEFAULT '1.0.0',
    data_sources TEXT, -- JSON array
    
    -- Tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discovered niches table
CREATE TABLE IF NOT EXISTS discovered_niches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    niche_id TEXT UNIQUE NOT NULL,
    niche_name TEXT NOT NULL,
    category TEXT NOT NULL,
    confidence_score REAL DEFAULT 0.0,
    keywords TEXT, -- JSON array
    target_audience TEXT, -- JSON object
    market_size TEXT,
    competition_level TEXT,
    trend_direction TEXT,
    monetization_potential TEXT,
    language TEXT DEFAULT 'en',
    regional_focus TEXT, -- JSON array
    sub_niches TEXT, -- JSON array
    related_topics TEXT, -- JSON array
    
    -- Tracking
    opportunities_count INTEGER DEFAULT 1,
    first_discovered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_creators_found INTEGER DEFAULT 0,
    avg_success_probability REAL DEFAULT 0.0
);

-- Analyzed creators table
CREATE TABLE IF NOT EXISTS analyzed_creators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    handle TEXT,
    url TEXT,
    
    -- Creator Metrics
    followers INTEGER DEFAULT 0,
    subscriber_count INTEGER DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    average_views INTEGER DEFAULT 0,
    engagement_rate REAL DEFAULT 0.0,
    influence_score REAL DEFAULT 0.0,
    authenticity_score REAL DEFAULT 0.0,
    
    -- Creator Profile
    niche TEXT,
    sub_niches TEXT, -- JSON array
    content_themes TEXT, -- JSON array
    posting_frequency TEXT,
    audience_demographics TEXT, -- JSON object
    content_style TEXT,
    language TEXT DEFAULT 'en',
    region TEXT,
    growth_trend TEXT,
    
    -- Content Analysis
    top_content_formats TEXT, -- JSON array
    hook_strategies TEXT, -- JSON array
    thumbnail_patterns TEXT, -- JSON array
    engagement_tactics TEXT, -- JSON array
    viral_content_analysis TEXT, -- JSON object
    content_patterns TEXT, -- JSON object
    
    -- Business Intelligence
    monetization_methods TEXT, -- JSON array
    brand_partnerships TEXT, -- JSON array
    collaboration_potential TEXT,
    competitive_advantages TEXT, -- JSON array
    collaboration_opportunities TEXT, -- JSON array
    content_gaps TEXT, -- JSON array
    recommended_strategies TEXT, -- JSON array
    
    -- Analysis Metadata
    opportunities_related TEXT, -- JSON array of opportunity IDs
    analysis_depth TEXT DEFAULT 'basic', -- basic, detailed, comprehensive
    last_content_update TIMESTAMP,
    
    -- Tracking
    first_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_count INTEGER DEFAULT 1
);

-- Extracted patterns table
CREATE TABLE IF NOT EXISTS extracted_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id TEXT UNIQUE NOT NULL,
    pattern_type TEXT NOT NULL, -- hook_formula, viral_trigger, engagement_tactic, etc.
    name TEXT NOT NULL,
    description TEXT,
    
    -- Pattern Effectiveness
    effectiveness_score REAL DEFAULT 0.0,
    frequency INTEGER DEFAULT 0,
    success_rate REAL DEFAULT 0.0,
    confidence_level REAL DEFAULT 0.0,
    
    -- Pattern Details
    structure TEXT, -- Pattern structure/formula
    trigger_type TEXT, -- curiosity, fear, desire, etc.
    examples TEXT, -- JSON array
    variations TEXT, -- JSON array
    implementation_guide TEXT,
    psychological_principle TEXT,
    
    -- Applicability
    applicable_niches TEXT, -- JSON array
    platform_compatibility TEXT, -- JSON array
    optimal_length INTEGER,
    platform_specific TEXT, -- JSON object
    
    -- Performance Metrics
    success_metrics TEXT, -- JSON object
    usage_examples TEXT, -- JSON array of real usage examples
    
    -- Pattern Origins
    extracted_from TEXT, -- JSON array of source creators/content
    source_niches TEXT, -- JSON array
    discovery_method TEXT, -- nlp, ai_analysis, manual
    
    -- Tracking
    first_extracted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usage_count INTEGER DEFAULT 1,
    validation_status TEXT DEFAULT 'pending' -- pending, validated, rejected
);

-- Pipeline executions table
CREATE TABLE IF NOT EXISTS pipeline_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id TEXT UNIQUE NOT NULL,
    opportunity_id TEXT NOT NULL,
    scanner_source TEXT,
    
    -- Execution Status
    status TEXT NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration_seconds REAL DEFAULT 0.0,
    
    -- Progress Tracking
    current_phase TEXT,
    progress_percentage INTEGER DEFAULT 0,
    progress_log TEXT, -- JSON array of progress messages
    
    -- Results
    result_summary TEXT, -- JSON object with key results
    error_message TEXT,
    warning_messages TEXT, -- JSON array
    
    -- Performance Metrics
    creators_discovered INTEGER DEFAULT 0,
    patterns_extracted INTEGER DEFAULT 0,
    processing_time_breakdown TEXT, -- JSON object
    
    -- Configuration
    analysis_config TEXT, -- JSON object
    python_version TEXT,
    
    -- Tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creator collaboration tracking
CREATE TABLE IF NOT EXISTS creator_collaborations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collaboration_id TEXT UNIQUE NOT NULL,
    opportunity_id TEXT NOT NULL,
    creator_id TEXT NOT NULL,
    
    -- Collaboration Details
    collaboration_type TEXT, -- sponsored_content, affiliate_partnership, guest_appearance
    status TEXT DEFAULT 'potential', -- potential, contacted, negotiating, agreed, active, completed
    
    -- Outreach
    outreach_date TIMESTAMP,
    outreach_method TEXT, -- email, dm, agent, etc.
    outreach_message TEXT,
    response_date TIMESTAMP,
    response_summary TEXT,
    
    -- Terms
    proposed_terms TEXT, -- JSON object
    agreed_terms TEXT, -- JSON object
    contract_signed BOOLEAN DEFAULT FALSE,
    payment_structure TEXT,
    deliverables TEXT, -- JSON array
    
    -- Performance
    content_created TEXT, -- JSON array of content IDs/URLs
    performance_metrics TEXT, -- JSON object
    roi_estimate REAL,
    actual_roi REAL,
    
    -- Notes
    notes TEXT,
    tags TEXT, -- JSON array
    
    -- Tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunity_analyses(opportunity_id),
    FOREIGN KEY (creator_id) REFERENCES analyzed_creators(creator_id)
);

-- Content performance tracking
CREATE TABLE IF NOT EXISTS content_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id TEXT UNIQUE NOT NULL,
    opportunity_id TEXT,
    creator_id TEXT,
    
    -- Content Details
    title TEXT,
    content_type TEXT, -- video, post, story, etc.
    platform TEXT,
    url TEXT,
    hook_used TEXT,
    pattern_applied TEXT, -- JSON array of pattern IDs
    
    -- Performance Metrics
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    engagement_rate REAL DEFAULT 0.0,
    click_through_rate REAL DEFAULT 0.0,
    conversion_rate REAL DEFAULT 0.0,
    
    -- Business Metrics
    leads_generated INTEGER DEFAULT 0,
    sales_generated INTEGER DEFAULT 0,
    revenue_generated REAL DEFAULT 0.0,
    cost_per_acquisition REAL DEFAULT 0.0,
    
    -- Content Analysis
    sentiment_score REAL DEFAULT 0.0,
    viral_score REAL DEFAULT 0.0,
    authenticity_score REAL DEFAULT 0.0,
    
    -- Tracking
    published_at TIMESTAMP,
    tracked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunity_analyses(opportunity_id),
    FOREIGN KEY (creator_id) REFERENCES analyzed_creators(creator_id)
);

-- Success stories and case studies
CREATE TABLE IF NOT EXISTS success_stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_id TEXT UNIQUE NOT NULL,
    opportunity_id TEXT NOT NULL,
    
    -- Story Details
    title TEXT NOT NULL,
    description TEXT,
    industry TEXT,
    niche TEXT,
    
    -- Success Metrics
    initial_investment REAL,
    revenue_generated REAL,
    profit_margin REAL,
    roi_percentage REAL,
    time_to_success_days INTEGER,
    
    -- Strategy Used
    strategies_applied TEXT, -- JSON array
    creators_involved TEXT, -- JSON array
    patterns_used TEXT, -- JSON array
    platforms_used TEXT, -- JSON array
    
    -- Lessons Learned
    key_insights TEXT, -- JSON array
    what_worked TEXT, -- JSON array
    what_didnt_work TEXT, -- JSON array
    recommendations TEXT, -- JSON array
    
    -- Documentation
    screenshots TEXT, -- JSON array of screenshot URLs
    metrics_snapshots TEXT, -- JSON array of metric screenshots
    timeline TEXT, -- JSON array of timeline events
    
    -- Sharing
    is_public BOOLEAN DEFAULT FALSE,
    case_study_url TEXT,
    testimonial TEXT,
    
    -- Tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunity_analyses(opportunity_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_opportunity_analyses_type ON opportunity_analyses(opportunity_type);
CREATE INDEX IF NOT EXISTS idx_opportunity_analyses_scanner ON opportunity_analyses(scanner_source);
CREATE INDEX IF NOT EXISTS idx_opportunity_analyses_niche ON opportunity_analyses(niche_primary);
CREATE INDEX IF NOT EXISTS idx_opportunity_analyses_success ON opportunity_analyses(success_probability);
CREATE INDEX IF NOT EXISTS idx_opportunity_analyses_timestamp ON opportunity_analyses(analysis_timestamp);

CREATE INDEX IF NOT EXISTS idx_niches_category ON discovered_niches(category);
CREATE INDEX IF NOT EXISTS idx_niches_confidence ON discovered_niches(confidence_score);
CREATE INDEX IF NOT EXISTS idx_niches_language ON discovered_niches(language);

CREATE INDEX IF NOT EXISTS idx_creators_platform ON analyzed_creators(platform);
CREATE INDEX IF NOT EXISTS idx_creators_niche ON analyzed_creators(niche);
CREATE INDEX IF NOT EXISTS idx_creators_influence ON analyzed_creators(influence_score);
CREATE INDEX IF NOT EXISTS idx_creators_followers ON analyzed_creators(followers);

CREATE INDEX IF NOT EXISTS idx_patterns_type ON extracted_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_patterns_effectiveness ON extracted_patterns(effectiveness_score);
CREATE INDEX IF NOT EXISTS idx_patterns_trigger ON extracted_patterns(trigger_type);

CREATE INDEX IF NOT EXISTS idx_executions_status ON pipeline_executions(status);
CREATE INDEX IF NOT EXISTS idx_executions_opportunity ON pipeline_executions(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_executions_scanner ON pipeline_executions(scanner_source);

CREATE INDEX IF NOT EXISTS idx_collaborations_status ON creator_collaborations(status);
CREATE INDEX IF NOT EXISTS idx_collaborations_opportunity ON creator_collaborations(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_collaborations_creator ON creator_collaborations(creator_id);

CREATE INDEX IF NOT EXISTS idx_content_platform ON content_performance(platform);
CREATE INDEX IF NOT EXISTS idx_content_performance ON content_performance(engagement_rate);
CREATE INDEX IF NOT EXISTS idx_content_conversion ON content_performance(conversion_rate);

CREATE INDEX IF NOT EXISTS idx_success_roi ON success_stories(roi_percentage);
CREATE INDEX IF NOT EXISTS idx_success_niche ON success_stories(niche);

-- Views for common queries
CREATE VIEW IF NOT EXISTS top_performing_opportunities AS
SELECT 
    opportunity_id,
    title,
    niche_primary,
    success_probability,
    creators_found,
    recommended_approach,
    primary_platform,
    analysis_timestamp
FROM opportunity_analyses 
WHERE success_probability > 0.7
ORDER BY success_probability DESC, creators_found DESC;

CREATE VIEW IF NOT EXISTS creator_influence_ranking AS
SELECT 
    name,
    platform,
    niche,
    followers,
    engagement_rate,
    influence_score,
    analysis_count,
    last_updated
FROM analyzed_creators 
ORDER BY influence_score DESC, followers DESC;

CREATE VIEW IF NOT EXISTS viral_pattern_effectiveness AS
SELECT 
    name,
    pattern_type,
    effectiveness_score,
    usage_count,
    applicable_niches,
    platform_compatibility,
    validation_status
FROM extracted_patterns 
WHERE effectiveness_score > 0.7
ORDER BY effectiveness_score DESC, usage_count DESC;

CREATE VIEW IF NOT EXISTS niche_opportunity_summary AS
SELECT 
    n.niche_name,
    n.category,
    n.market_size,
    n.competition_level,
    n.opportunities_count,
    n.total_creators_found,
    n.avg_success_probability,
    COUNT(oa.id) as recent_opportunities
FROM discovered_niches n
LEFT JOIN opportunity_analyses oa ON n.niche_name = oa.niche_primary 
WHERE oa.analysis_timestamp > datetime('now', '-30 days')
GROUP BY n.niche_id
ORDER BY n.avg_success_probability DESC, n.opportunities_count DESC;

-- Triggers for automatic updates
CREATE TRIGGER IF NOT EXISTS update_opportunity_timestamp 
AFTER UPDATE ON opportunity_analyses
BEGIN
    UPDATE opportunity_analyses SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_niche_stats
AFTER INSERT ON opportunity_analyses
BEGIN
    UPDATE discovered_niches 
    SET 
        opportunities_count = opportunities_count + 1,
        total_creators_found = total_creators_found + NEW.creators_found,
        avg_success_probability = (avg_success_probability * (opportunities_count - 1) + NEW.success_probability) / opportunities_count,
        last_updated = CURRENT_TIMESTAMP
    WHERE niche_name = NEW.niche_primary;
END;

CREATE TRIGGER IF NOT EXISTS update_creator_analysis_count
AFTER UPDATE ON analyzed_creators
BEGIN
    UPDATE analyzed_creators 
    SET 
        analysis_count = analysis_count + 1,
        last_updated = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_pattern_usage
AFTER INSERT ON content_performance
BEGIN
    UPDATE extracted_patterns 
    SET usage_count = usage_count + 1 
    WHERE pattern_id IN (
        SELECT json_each.value 
        FROM json_each(NEW.pattern_applied)
    );
END;