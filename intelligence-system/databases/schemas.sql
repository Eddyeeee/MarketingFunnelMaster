-- Intelligence System Database Schema
-- SQLite schema optimized for opportunity tracking and analysis

-- Core opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    source TEXT NOT NULL, -- 'affiliate_scanner', 'social_trend_scanner', etc.
    type TEXT NOT NULL, -- 'affiliate_product', 'trending_topic', 'seasonal_timing', etc.
    category TEXT, -- 'finance', 'business', 'education', 'lifestyle'
    score INTEGER NOT NULL DEFAULT 0, -- 0-100 opportunity score
    status TEXT DEFAULT 'active', -- 'active', 'expired', 'converted', 'ignored'
    
    -- Discovery metadata
    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    
    -- Structured data (JSON fields for flexibility)
    metadata TEXT, -- JSON: source-specific data
    metrics TEXT, -- JSON: performance metrics
    tags TEXT, -- JSON: array of tags for filtering
    
    UNIQUE(id)
);

-- Affiliate opportunities specific data
CREATE TABLE IF NOT EXISTS affiliate_opportunities (
    opportunity_id TEXT PRIMARY KEY,
    product_id TEXT,
    vendor TEXT,
    commission_rate REAL NOT NULL,
    price REAL,
    currency TEXT DEFAULT 'USD',
    affiliate_url TEXT,
    
    -- Performance metrics
    gravity REAL DEFAULT 0, -- Product popularity/competition
    conversion_rate REAL DEFAULT 0,
    sales_count INTEGER DEFAULT 0,
    refund_rate REAL DEFAULT 0,
    avg_order_value REAL DEFAULT 0,
    
    -- Network information
    network TEXT NOT NULL, -- 'digistore24', 'clickbank', etc.
    network_product_id TEXT,
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

-- Social trend opportunities
CREATE TABLE IF NOT EXISTS social_trend_opportunities (
    opportunity_id TEXT PRIMARY KEY,
    platform TEXT NOT NULL, -- 'twitter', 'instagram', 'tiktok', etc.
    keyword TEXT NOT NULL,
    hashtag TEXT,
    
    -- Engagement metrics
    total_engagement INTEGER DEFAULT 0,
    average_engagement REAL DEFAULT 0,
    trend_velocity REAL DEFAULT 0, -- Rate of growth
    sentiment TEXT, -- 'positive', 'negative', 'neutral'
    
    -- Content analysis
    top_content TEXT, -- JSON: array of top performing content
    influencer_mentions INTEGER DEFAULT 0,
    viral_potential REAL DEFAULT 0,
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

-- Seasonal opportunities
CREATE TABLE IF NOT EXISTS seasonal_opportunities (
    opportunity_id TEXT PRIMARY KEY,
    season_type TEXT NOT NULL, -- 'holiday', 'weather', 'cultural', 'marketing_calendar'
    event_name TEXT,
    region TEXT, -- 'US', 'EU', 'DE', 'GLOBAL'
    
    -- Timing information
    start_date DATETIME,
    end_date DATETIME,
    preparation_days INTEGER DEFAULT 0,
    
    -- Historical data
    historical_performance REAL DEFAULT 0, -- 0-100 score
    competition_level REAL DEFAULT 50, -- 0-100 score
    market_demand REAL DEFAULT 50, -- 0-100 score
    
    -- Pattern information
    pattern_strength REAL DEFAULT 0, -- How strong this seasonal pattern is
    recurrence TEXT, -- 'annual', 'monthly', 'weekly'
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

-- Timing optimization opportunities
CREATE TABLE IF NOT EXISTS timing_opportunities (
    opportunity_id TEXT PRIMARY KEY,
    timing_type TEXT NOT NULL, -- 'market_timing', 'event_timing', 'cycle_timing'
    
    -- Event information (if event-based)
    event_name TEXT,
    event_date DATETIME,
    event_impact INTEGER, -- 1-10 scale
    days_until_event INTEGER,
    
    -- Market cycle information
    cycle_type TEXT, -- 'stock_market', 'crypto', 'business', 'consumer_spending'
    cycle_phase TEXT, -- Current phase of the cycle
    cycle_strength REAL DEFAULT 0, -- 0-100 strength of current phase
    
    -- Global activity metrics
    global_activity REAL DEFAULT 0, -- 0-100 current global market activity
    optimal_duration TEXT, -- How long this timing window lasts
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

-- Opportunity scoring history
CREATE TABLE IF NOT EXISTS opportunity_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    scored_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Score breakdown
    profitability_score REAL DEFAULT 0, -- 0-100
    trend_velocity_score REAL DEFAULT 0, -- 0-100
    timing_score REAL DEFAULT 0, -- 0-100
    competition_score REAL DEFAULT 0, -- 0-100
    
    -- Score weights used
    weights TEXT, -- JSON: scoring weights used
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

-- Opportunity actions and campaigns
CREATE TABLE IF NOT EXISTS opportunity_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id TEXT NOT NULL,
    action_type TEXT NOT NULL, -- 'campaign_created', 'content_generated', 'promotion_launched'
    action_status TEXT DEFAULT 'pending', -- 'pending', 'active', 'completed', 'failed'
    
    -- Action details
    title TEXT,
    description TEXT,
    action_data TEXT, -- JSON: action-specific data
    
    -- Performance tracking
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue REAL DEFAULT 0,
    cost REAL DEFAULT 0,
    roi REAL DEFAULT 0,
    
    -- Timing
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

-- Scanner performance tracking
CREATE TABLE IF NOT EXISTS scanner_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scanner_name TEXT NOT NULL,
    scan_started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    scan_completed_at DATETIME,
    scan_duration_ms INTEGER,
    
    -- Results
    opportunities_found INTEGER DEFAULT 0,
    opportunities_scored INTEGER DEFAULT 0,
    high_score_opportunities INTEGER DEFAULT 0, -- Score >= 80
    errors_encountered INTEGER DEFAULT 0,
    
    -- Resource usage
    api_calls_made INTEGER DEFAULT 0,
    data_processed TEXT, -- JSON: data processing metrics
    memory_usage TEXT, -- JSON: memory usage stats
    
    -- Status
    status TEXT DEFAULT 'running', -- 'running', 'completed', 'failed', 'timeout'
    error_details TEXT
);

-- Keyword and trend tracking
CREATE TABLE IF NOT EXISTS tracked_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    category TEXT,
    platforms TEXT, -- JSON: array of platforms to track
    
    -- Tracking settings
    is_active BOOLEAN DEFAULT 1,
    min_engagement INTEGER DEFAULT 1000,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_tracked_at DATETIME,
    
    -- Performance history
    total_opportunities INTEGER DEFAULT 0,
    avg_opportunity_score REAL DEFAULT 0,
    best_opportunity_score INTEGER DEFAULT 0,
    
    UNIQUE(keyword, category)
);

-- Market conditions tracking
CREATE TABLE IF NOT EXISTS market_conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    condition_date DATE NOT NULL,
    
    -- Economic indicators
    market_sentiment TEXT, -- 'bullish', 'bearish', 'neutral'
    volatility_index REAL DEFAULT 0,
    consumer_confidence REAL DEFAULT 0,
    
    -- Social media indicators
    social_media_activity REAL DEFAULT 0, -- Overall activity level
    trending_topics TEXT, -- JSON: array of trending topics
    viral_content_count INTEGER DEFAULT 0,
    
    -- Seasonal factors
    seasonal_multiplier REAL DEFAULT 1.0,
    holiday_factor REAL DEFAULT 1.0,
    weekend_factor REAL DEFAULT 1.0,
    
    -- Timing factors
    global_market_activity REAL DEFAULT 0, -- 0-100
    optimal_posting_hours TEXT, -- JSON: array of optimal hours by timezone
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(condition_date)
);

-- API usage and rate limiting
CREATE TABLE IF NOT EXISTS api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_provider TEXT NOT NULL, -- 'twitter', 'digistore24', etc.
    endpoint TEXT,
    
    -- Request tracking
    requests_made INTEGER DEFAULT 1,
    request_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    response_status INTEGER, -- HTTP status code
    response_time_ms INTEGER,
    
    -- Rate limiting
    rate_limit_remaining INTEGER,
    rate_limit_reset DATETIME,
    
    -- Usage optimization
    cache_hit BOOLEAN DEFAULT 0,
    data_cached BOOLEAN DEFAULT 0,
    
    -- Error tracking
    error_message TEXT,
    retry_count INTEGER DEFAULT 0
);

-- N8n workflow integration
CREATE TABLE IF NOT EXISTS n8n_workflows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_name TEXT NOT NULL,
    workflow_id TEXT,
    trigger_type TEXT NOT NULL, -- 'opportunity_found', 'high_score', 'seasonal', etc.
    
    -- Trigger conditions
    min_score INTEGER DEFAULT 70,
    required_categories TEXT, -- JSON: array of categories
    required_sources TEXT, -- JSON: array of sources
    trigger_conditions TEXT, -- JSON: complex trigger conditions
    
    -- Workflow details
    webhook_url TEXT,
    is_active BOOLEAN DEFAULT 1,
    execution_count INTEGER DEFAULT 0,
    last_executed_at DATETIME,
    
    -- Performance
    success_rate REAL DEFAULT 0, -- 0-1 success rate
    avg_execution_time_ms INTEGER DEFAULT 0,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(workflow_name)
);

-- N8n workflow executions
CREATE TABLE IF NOT EXISTS n8n_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id INTEGER NOT NULL,
    opportunity_id TEXT NOT NULL,
    
    -- Execution details
    execution_id TEXT, -- N8n execution ID
    status TEXT DEFAULT 'pending', -- 'pending', 'running', 'success', 'error'
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    execution_time_ms INTEGER,
    
    -- Results
    webhook_response TEXT, -- JSON: webhook response
    output_data TEXT, -- JSON: workflow output
    error_message TEXT,
    
    FOREIGN KEY (workflow_id) REFERENCES n8n_workflows(id),
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_opportunities_score ON opportunities(score DESC);
CREATE INDEX IF NOT EXISTS idx_opportunities_source ON opportunities(source);
CREATE INDEX IF NOT EXISTS idx_opportunities_category ON opportunities(category);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_discovered_at ON opportunities(discovered_at DESC);

CREATE INDEX IF NOT EXISTS idx_affiliate_commission_rate ON affiliate_opportunities(commission_rate DESC);
CREATE INDEX IF NOT EXISTS idx_affiliate_network ON affiliate_opportunities(network);

CREATE INDEX IF NOT EXISTS idx_social_platform ON social_trend_opportunities(platform);
CREATE INDEX IF NOT EXISTS idx_social_keyword ON social_trend_opportunities(keyword);
CREATE INDEX IF NOT EXISTS idx_social_trend_velocity ON social_trend_opportunities(trend_velocity DESC);

CREATE INDEX IF NOT EXISTS idx_seasonal_type ON seasonal_opportunities(season_type);
CREATE INDEX IF NOT EXISTS idx_seasonal_dates ON seasonal_opportunities(start_date, end_date);

CREATE INDEX IF NOT EXISTS idx_timing_type ON timing_opportunities(timing_type);
CREATE INDEX IF NOT EXISTS idx_timing_event_date ON timing_opportunities(event_date);

CREATE INDEX IF NOT EXISTS idx_scores_opportunity ON opportunity_scores(opportunity_id, scored_at DESC);
CREATE INDEX IF NOT EXISTS idx_actions_opportunity ON opportunity_actions(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_actions_type_status ON opportunity_actions(action_type, action_status);

CREATE INDEX IF NOT EXISTS idx_scanner_performance_name ON scanner_performance(scanner_name, scan_started_at DESC);
CREATE INDEX IF NOT EXISTS idx_keywords_active ON tracked_keywords(is_active, last_tracked_at);
CREATE INDEX IF NOT EXISTS idx_market_conditions_date ON market_conditions(condition_date DESC);

CREATE INDEX IF NOT EXISTS idx_api_usage_provider ON api_usage(api_provider, request_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_n8n_workflows_active ON n8n_workflows(is_active);
CREATE INDEX IF NOT EXISTS idx_n8n_executions_status ON n8n_executions(status, started_at DESC);

-- Views for common queries
CREATE VIEW IF NOT EXISTS high_score_opportunities AS
SELECT 
    o.*,
    CASE 
        WHEN o.source = 'affiliate_scanner' THEN ao.commission_rate
        WHEN o.source = 'social_trend_scanner' THEN sto.trend_velocity
        ELSE NULL 
    END as primary_metric
FROM opportunities o
LEFT JOIN affiliate_opportunities ao ON o.id = ao.opportunity_id
LEFT JOIN social_trend_opportunities sto ON o.id = sto.opportunity_id
WHERE o.score >= 80 AND o.status = 'active'
ORDER BY o.score DESC, o.discovered_at DESC;

CREATE VIEW IF NOT EXISTS recent_opportunities AS
SELECT 
    o.*,
    datetime(o.discovered_at, 'localtime') as local_discovered_at,
    CASE 
        WHEN o.expires_at IS NOT NULL 
        THEN CAST((julianday(o.expires_at) - julianday('now')) * 24 AS INTEGER)
        ELSE NULL 
    END as hours_until_expiry
FROM opportunities o
WHERE o.discovered_at >= datetime('now', '-7 days')
AND o.status = 'active'
ORDER BY o.discovered_at DESC;

CREATE VIEW IF NOT EXISTS scanner_summary AS
SELECT 
    scanner_name,
    COUNT(*) as total_scans,
    AVG(scan_duration_ms) as avg_duration_ms,
    SUM(opportunities_found) as total_opportunities,
    AVG(opportunities_found) as avg_opportunities_per_scan,
    SUM(high_score_opportunities) as total_high_score_opportunities,
    MAX(scan_completed_at) as last_scan_completed
FROM scanner_performance
WHERE status = 'completed'
GROUP BY scanner_name
ORDER BY total_high_score_opportunities DESC;

-- Triggers for maintaining data integrity and automation
CREATE TRIGGER IF NOT EXISTS update_opportunity_timestamp
AFTER UPDATE ON opportunities
BEGIN
    UPDATE opportunities 
    SET last_updated = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS log_opportunity_score_change
AFTER UPDATE OF score ON opportunities
WHEN OLD.score != NEW.score
BEGIN
    INSERT INTO opportunity_scores (opportunity_id, score)
    VALUES (NEW.id, NEW.score);
END;

CREATE TRIGGER IF NOT EXISTS cleanup_expired_opportunities
AFTER INSERT ON opportunities
BEGIN
    UPDATE opportunities 
    SET status = 'expired' 
    WHERE expires_at IS NOT NULL 
    AND expires_at < CURRENT_TIMESTAMP 
    AND status = 'active';
END;