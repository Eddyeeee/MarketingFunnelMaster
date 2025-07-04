-- Migration: Create Journey Tracking Tables for Dynamic Customer Journey Engine
-- Module: 2B - Dynamic Customer Journey Engine
-- Created: 2024-07-04
-- Description: Core database schema for journey tracking, personalization, and optimization

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- JOURNEY SESSIONS TABLE
-- =============================================================================
CREATE TABLE journey_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) UNIQUE NOT NULL,
    user_id UUID,
    persona_type VARCHAR(50),
    persona_confidence FLOAT CHECK (persona_confidence >= 0 AND persona_confidence <= 1),
    device_type VARCHAR(20) CHECK (device_type IN ('mobile', 'tablet', 'desktop')),
    device_fingerprint TEXT,
    start_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_timestamp TIMESTAMP WITH TIME ZONE,
    current_stage VARCHAR(50) CHECK (current_stage IN ('awareness', 'consideration', 'decision', 'conversion', 'retention')),
    journey_path VARCHAR(100), -- 'mobile_tiktok_fast_track', 'desktop_research_deep', etc.
    conversion_probability FLOAT CHECK (conversion_probability >= 0 AND conversion_probability <= 1),
    total_touchpoints INTEGER DEFAULT 0,
    total_session_time INTEGER DEFAULT 0, -- in seconds
    entry_point JSONB,
    utm_data JSONB,
    referrer_data JSONB,
    exit_point JSONB,
    conversion_events JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for journey_sessions
CREATE INDEX idx_journey_sessions_session_id ON journey_sessions(session_id);
CREATE INDEX idx_journey_sessions_user_id ON journey_sessions(user_id);
CREATE INDEX idx_journey_sessions_persona_type ON journey_sessions(persona_type);
CREATE INDEX idx_journey_sessions_device_type ON journey_sessions(device_type);
CREATE INDEX idx_journey_sessions_current_stage ON journey_sessions(current_stage);
CREATE INDEX idx_journey_sessions_start_timestamp ON journey_sessions(start_timestamp);
CREATE INDEX idx_journey_sessions_conversion_probability ON journey_sessions(conversion_probability);
CREATE INDEX idx_journey_sessions_journey_path ON journey_sessions(journey_path);

-- Performance optimization index
CREATE INDEX idx_journey_sessions_performance 
ON journey_sessions(session_id, current_stage, conversion_probability);

-- =============================================================================
-- JOURNEY TOUCHPOINTS TABLE
-- =============================================================================
CREATE TABLE journey_touchpoints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) REFERENCES journey_sessions(session_id) ON DELETE CASCADE,
    touchpoint_sequence INTEGER NOT NULL,
    touchpoint_type VARCHAR(50) NOT NULL, -- 'page_view', 'interaction', 'conversion_event', 'exit_intent'
    page_url TEXT,
    page_title VARCHAR(255),
    interaction_type VARCHAR(50), -- 'click', 'scroll', 'swipe', 'hover', 'form_fill'
    interaction_data JSONB,
    engagement_score FLOAT CHECK (engagement_score >= 0 AND engagement_score <= 1),
    duration_seconds INTEGER,
    scroll_depth FLOAT CHECK (scroll_depth >= 0 AND scroll_depth <= 1),
    click_count INTEGER DEFAULT 0,
    conversion_value DECIMAL(10,2) DEFAULT 0.00,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    device_context JSONB,
    performance_metrics JSONB,
    personalization_applied JSONB,
    ab_test_variant VARCHAR(50),
    metadata JSONB
);

-- Indexes for journey_touchpoints
CREATE INDEX idx_journey_touchpoints_session_id ON journey_touchpoints(session_id);
CREATE INDEX idx_journey_touchpoints_touchpoint_type ON journey_touchpoints(touchpoint_type);
CREATE INDEX idx_journey_touchpoints_timestamp ON journey_touchpoints(timestamp);
CREATE INDEX idx_journey_touchpoints_engagement_score ON journey_touchpoints(engagement_score);
CREATE INDEX idx_journey_touchpoints_sequence ON journey_touchpoints(touchpoint_sequence);
CREATE INDEX idx_journey_touchpoints_interaction_type ON journey_touchpoints(interaction_type);

-- Composite index for performance queries
CREATE INDEX idx_journey_touchpoints_session_sequence 
ON journey_touchpoints(session_id, touchpoint_sequence);

-- =============================================================================
-- CONVERSION EVENTS TABLE
-- =============================================================================
CREATE TABLE conversion_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) REFERENCES journey_sessions(session_id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- 'email_signup', 'purchase', 'download', 'consultation_booking'
    event_value DECIMAL(10,2) DEFAULT 0.00,
    event_currency VARCHAR(3) DEFAULT 'EUR',
    funnel_step VARCHAR(50),
    conversion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    attribution_data JSONB,
    product_data JSONB,
    user_data JSONB,
    campaign_data JSONB,
    device_data JSONB,
    revenue_attributed DECIMAL(10,2) DEFAULT 0.00,
    commission_earned DECIMAL(10,2) DEFAULT 0.00,
    lifetime_value_prediction DECIMAL(10,2),
    metadata JSONB
);

-- Indexes for conversion_events
CREATE INDEX idx_conversion_events_session_id ON conversion_events(session_id);
CREATE INDEX idx_conversion_events_event_type ON conversion_events(event_type);
CREATE INDEX idx_conversion_events_timestamp ON conversion_events(conversion_timestamp);
CREATE INDEX idx_conversion_events_value ON conversion_events(event_value);
CREATE INDEX idx_conversion_events_funnel_step ON conversion_events(funnel_step);

-- =============================================================================
-- PERSONALIZATION DATA TABLE
-- =============================================================================
CREATE TABLE personalization_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) REFERENCES journey_sessions(session_id) ON DELETE CASCADE,
    user_id UUID,
    personalization_type VARCHAR(50), -- 'content', 'offer', 'layout', 'timing'
    personalization_strategy VARCHAR(100),
    variant_id VARCHAR(100),
    content_delivered JSONB,
    performance_metrics JSONB,
    user_response VARCHAR(50), -- 'positive', 'negative', 'neutral', 'no_response'
    engagement_time INTEGER,
    conversion_attributed BOOLEAN DEFAULT FALSE,
    ml_model_version VARCHAR(50),
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    applied_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Indexes for personalization_data
CREATE INDEX idx_personalization_data_session_id ON personalization_data(session_id);
CREATE INDEX idx_personalization_data_user_id ON personalization_data(user_id);
CREATE INDEX idx_personalization_data_type ON personalization_data(personalization_type);
CREATE INDEX idx_personalization_data_performance ON personalization_data(conversion_attributed);
CREATE INDEX idx_personalization_data_strategy ON personalization_data(personalization_strategy);
CREATE INDEX idx_personalization_data_variant ON personalization_data(variant_id);

-- =============================================================================
-- CROSS-DEVICE SESSIONS TABLE
-- =============================================================================
CREATE TABLE cross_device_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unified_session_id VARCHAR(100) UNIQUE NOT NULL,
    primary_session_id VARCHAR(100) REFERENCES journey_sessions(session_id),
    linked_session_ids TEXT[], -- Array of linked session IDs
    user_identifier VARCHAR(255), -- email, phone, or user ID
    linking_method VARCHAR(50), -- 'email', 'phone', 'user_id', 'fingerprint'
    device_sequence JSONB, -- Order of devices used
    cross_device_insights JSONB,
    total_cross_device_time INTEGER,
    unified_conversion_probability FLOAT CHECK (unified_conversion_probability >= 0 AND unified_conversion_probability <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for cross_device_sessions
CREATE INDEX idx_cross_device_sessions_unified_id ON cross_device_sessions(unified_session_id);
CREATE INDEX idx_cross_device_sessions_primary_id ON cross_device_sessions(primary_session_id);
CREATE INDEX idx_cross_device_sessions_user_identifier ON cross_device_sessions(user_identifier);
CREATE INDEX idx_cross_device_sessions_linking_method ON cross_device_sessions(linking_method);

-- =============================================================================
-- UX INTELLIGENCE INTEGRATION BRIDGE TABLES
-- =============================================================================

-- Bridge table connecting 2A sessions with 2B journey sessions
CREATE TABLE ux_journey_session_bridge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ux_session_id VARCHAR(100), -- References ux_intelligence_sessions(session_id)
    journey_session_id VARCHAR(100) REFERENCES journey_sessions(session_id),
    integration_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_flow_direction VARCHAR(20) CHECK (data_flow_direction IN ('ux_to_journey', 'journey_to_ux', 'bidirectional')),
    integration_status VARCHAR(20) DEFAULT 'active',
    metadata JSONB
);

-- Indexes for ux_journey_session_bridge
CREATE INDEX idx_ux_journey_bridge_ux_session ON ux_journey_session_bridge(ux_session_id);
CREATE INDEX idx_ux_journey_bridge_journey_session ON ux_journey_session_bridge(journey_session_id);
CREATE INDEX idx_ux_journey_bridge_status ON ux_journey_session_bridge(integration_status);

-- Bridge table for persona evolution tracking
CREATE TABLE persona_journey_evolution (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    session_id VARCHAR(100),
    original_persona_id UUID, -- References persona_profiles(id)
    evolved_persona_data JSONB,
    evolution_triggers JSONB,
    evolution_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    confidence_improvement FLOAT,
    journey_context JSONB
);

-- Indexes for persona_journey_evolution
CREATE INDEX idx_persona_evolution_user_id ON persona_journey_evolution(user_id);
CREATE INDEX idx_persona_evolution_session_id ON persona_journey_evolution(session_id);
CREATE INDEX idx_persona_evolution_original_persona ON persona_journey_evolution(original_persona_id);
CREATE INDEX idx_persona_evolution_timestamp ON persona_journey_evolution(evolution_timestamp);

-- =============================================================================
-- SCARCITY TRIGGER TRACKING TABLE
-- =============================================================================
CREATE TABLE scarcity_trigger_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) REFERENCES journey_sessions(session_id) ON DELETE CASCADE,
    trigger_type VARCHAR(50) NOT NULL, -- 'social_proof', 'time_pressure', 'exclusivity', 'inventory'
    trigger_strategy VARCHAR(100),
    trigger_content JSONB,
    trigger_timing INTEGER, -- seconds into session when triggered
    user_response VARCHAR(50), -- 'positive', 'negative', 'neutral', 'no_response'
    engagement_change FLOAT, -- change in engagement after trigger
    conversion_attributed BOOLEAN DEFAULT FALSE,
    trigger_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Indexes for scarcity_trigger_events
CREATE INDEX idx_scarcity_triggers_session_id ON scarcity_trigger_events(session_id);
CREATE INDEX idx_scarcity_triggers_type ON scarcity_trigger_events(trigger_type);
CREATE INDEX idx_scarcity_triggers_timestamp ON scarcity_trigger_events(trigger_timestamp);
CREATE INDEX idx_scarcity_triggers_conversion ON scarcity_trigger_events(conversion_attributed);

-- =============================================================================
-- JOURNEY ANALYTICS MATERIALIZED VIEWS
-- =============================================================================

-- Materialized view for journey funnel analytics
CREATE MATERIALIZED VIEW journey_funnel_analytics AS
SELECT 
    journey_path,
    current_stage,
    device_type,
    persona_type,
    DATE_TRUNC('day', start_timestamp) as date,
    COUNT(*) as session_count,
    AVG(conversion_probability) as avg_conversion_probability,
    AVG(total_session_time) as avg_session_time,
    AVG(total_touchpoints) as avg_touchpoints,
    COUNT(CASE WHEN conversion_events IS NOT NULL THEN 1 END) as conversions,
    COUNT(CASE WHEN conversion_events IS NOT NULL THEN 1 END)::FLOAT / COUNT(*) as conversion_rate
FROM journey_sessions 
WHERE start_timestamp >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY journey_path, current_stage, device_type, persona_type, DATE_TRUNC('day', start_timestamp);

-- Index for the materialized view
CREATE INDEX idx_journey_funnel_analytics_date ON journey_funnel_analytics(date);
CREATE INDEX idx_journey_funnel_analytics_path_stage ON journey_funnel_analytics(journey_path, current_stage);

-- Materialized view for personalization performance
CREATE MATERIALIZED VIEW personalization_performance_analytics AS
SELECT 
    personalization_type,
    personalization_strategy,
    variant_id,
    DATE_TRUNC('day', applied_timestamp) as date,
    COUNT(*) as applications,
    AVG(engagement_time) as avg_engagement_time,
    COUNT(CASE WHEN conversion_attributed = TRUE THEN 1 END) as conversions,
    COUNT(CASE WHEN conversion_attributed = TRUE THEN 1 END)::FLOAT / COUNT(*) as conversion_rate,
    AVG(confidence_score) as avg_confidence
FROM personalization_data
WHERE applied_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY personalization_type, personalization_strategy, variant_id, DATE_TRUNC('day', applied_timestamp);

-- Index for personalization analytics
CREATE INDEX idx_personalization_analytics_date ON personalization_performance_analytics(date);
CREATE INDEX idx_personalization_analytics_type_strategy ON personalization_performance_analytics(personalization_type, personalization_strategy);

-- =============================================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =============================================================================

-- Trigger to update journey_sessions.updated_at on any change
CREATE OR REPLACE FUNCTION update_journey_session_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_journey_session_updated_at
    BEFORE UPDATE ON journey_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_journey_session_updated_at();

-- Trigger to update cross_device_sessions.updated_at on any change
CREATE OR REPLACE FUNCTION update_cross_device_session_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_cross_device_session_updated_at
    BEFORE UPDATE ON cross_device_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_cross_device_session_updated_at();

-- =============================================================================
-- PERFORMANCE OPTIMIZATION
-- =============================================================================

-- Partitioning for journey_touchpoints (by month)
CREATE TABLE journey_touchpoints_template (
    LIKE journey_touchpoints INCLUDING ALL
);

-- Function to create monthly partitions
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name text, start_date date)
RETURNS void AS $$
DECLARE
    partition_name text;
    end_date date;
BEGIN
    partition_name := table_name || '_' || to_char(start_date, 'YYYY_MM');
    end_date := start_date + interval '1 month';
    
    EXECUTE format('CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
        partition_name, table_name, start_date, end_date);
    
    EXECUTE format('CREATE INDEX %I ON %I (session_id, timestamp)',
        'idx_' || partition_name || '_session_time', partition_name);
END;
$$ LANGUAGE plpgsql;

-- Create partitions for current and next 3 months
SELECT create_monthly_partition('journey_touchpoints', date_trunc('month', CURRENT_DATE + interval '0 month'));
SELECT create_monthly_partition('journey_touchpoints', date_trunc('month', CURRENT_DATE + interval '1 month'));
SELECT create_monthly_partition('journey_touchpoints', date_trunc('month', CURRENT_DATE + interval '2 month'));

-- =============================================================================
-- DATA VALIDATION FUNCTIONS
-- =============================================================================

-- Function to validate journey session data integrity
CREATE OR REPLACE FUNCTION validate_journey_session_integrity()
RETURNS TABLE(session_id VARCHAR, issue_type VARCHAR, issue_description TEXT) AS $$
BEGIN
    -- Check for sessions without touchpoints
    RETURN QUERY
    SELECT 
        js.session_id,
        'missing_touchpoints'::VARCHAR,
        'Journey session has no touchpoints recorded'::TEXT
    FROM journey_sessions js
    LEFT JOIN journey_touchpoints jt ON js.session_id = jt.session_id
    WHERE jt.session_id IS NULL
    AND js.start_timestamp < CURRENT_TIMESTAMP - INTERVAL '1 hour';
    
    -- Check for sessions with invalid conversion probabilities
    RETURN QUERY
    SELECT 
        js.session_id,
        'invalid_conversion_probability'::VARCHAR,
        'Conversion probability outside valid range'::TEXT
    FROM journey_sessions js
    WHERE js.conversion_probability < 0 OR js.conversion_probability > 1;
    
    -- Check for touchpoints with invalid engagement scores
    RETURN QUERY
    SELECT 
        jt.session_id,
        'invalid_engagement_score'::VARCHAR,
        'Touchpoint engagement score outside valid range'::TEXT
    FROM journey_touchpoints jt
    WHERE jt.engagement_score < 0 OR jt.engagement_score > 1;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- GRANT PERMISSIONS
-- =============================================================================

-- Grant permissions to application user (assuming 'app_user' role exists)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app_user;

-- =============================================================================
-- MIGRATION COMPLETION LOG
-- =============================================================================

-- Log migration completion
INSERT INTO migration_log (migration_name, executed_at, description) 
VALUES (
    '001_create_journey_tracking_tables',
    CURRENT_TIMESTAMP,
    'Created core journey tracking tables for Dynamic Customer Journey Engine Module 2B'
) ON CONFLICT DO NOTHING;

-- Migration completed successfully
COMMENT ON TABLE journey_sessions IS 'Core table tracking customer journey sessions with persona, device, and conversion data';
COMMENT ON TABLE journey_touchpoints IS 'Detailed tracking of user interactions and touchpoints within journey sessions';
COMMENT ON TABLE conversion_events IS 'Records all conversion events with attribution and revenue data';
COMMENT ON TABLE personalization_data IS 'Tracks personalization applications and their performance metrics';
COMMENT ON TABLE cross_device_sessions IS 'Manages cross-device journey continuity and unified session tracking';
COMMENT ON TABLE ux_journey_session_bridge IS 'Bridge table connecting UX Intelligence Engine (2A) with Journey Engine (2B)';
COMMENT ON TABLE persona_journey_evolution IS 'Tracks how personas evolve through journey interactions';
COMMENT ON TABLE scarcity_trigger_events IS 'Records scarcity trigger applications and their effectiveness';