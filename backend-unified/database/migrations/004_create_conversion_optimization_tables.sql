-- Migration: Create conversion optimization tables for Milestone 2C
-- Module: 2C - Conversion & Marketing Automation
-- Created: 2024-07-04
-- Description: Creates tables for device-specific conversion optimization, behavioral tracking, and A/B testing

-- =============================================================================
-- CREATE DEVICE CONVERSION OPTIMIZATION TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS device_conversion_optimizations (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    
    -- Device and context data
    device_type VARCHAR(20) NOT NULL CHECK (device_type IN ('mobile', 'tablet', 'desktop')),
    device_fingerprint VARCHAR(255),
    traffic_source VARCHAR(50),
    persona_type VARCHAR(50),
    
    -- Optimization configuration
    optimization_flow VARCHAR(50) NOT NULL,
    ui_layout VARCHAR(30) NOT NULL,
    cta_configuration JSONB,
    content_configuration JSONB,
    timing_configuration JSONB,
    
    -- Performance metrics
    expected_conversion_rate FLOAT,
    actual_conversion_rate FLOAT,
    performance_metrics JSONB,
    
    -- Conversion triggers
    conversion_triggers JSONB,
    trigger_effectiveness JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_device_optimization_session_id 
        FOREIGN KEY (session_id) 
        REFERENCES journey_sessions(session_id) 
        ON DELETE CASCADE
);

-- =============================================================================
-- CREATE BEHAVIORAL TRACKING EVENTS TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS behavioral_tracking_events (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    
    -- Event data
    event_type VARCHAR(50) NOT NULL,
    event_category VARCHAR(50),
    event_action VARCHAR(100),
    event_label VARCHAR(255),
    event_value FLOAT,
    
    -- Context data
    page_url TEXT,
    page_title VARCHAR(255),
    referrer TEXT,
    user_agent TEXT,
    viewport_width INTEGER,
    viewport_height INTEGER,
    
    -- Interaction details
    element_id VARCHAR(100),
    element_class VARCHAR(255),
    element_text TEXT,
    element_position JSONB,
    interaction_type VARCHAR(50),
    interaction_duration INTEGER,
    
    -- Performance data
    page_load_time INTEGER,
    time_on_page INTEGER,
    scroll_depth FLOAT,
    engagement_score FLOAT,
    
    -- Custom event data
    custom_properties JSONB,
    
    -- Timestamps
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    server_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_behavioral_events_session_id 
        FOREIGN KEY (session_id) 
        REFERENCES journey_sessions(session_id) 
        ON DELETE CASCADE
);

-- =============================================================================
-- CREATE A/B TESTING FRAMEWORK TABLES
-- =============================================================================

-- A/B Tests table
CREATE TABLE IF NOT EXISTS ab_tests (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Test configuration
    test_name VARCHAR(255) NOT NULL,
    test_description TEXT,
    test_type VARCHAR(50) NOT NULL CHECK (test_type IN ('ab_test', 'multivariate', 'bandit', 'split_url')),
    test_status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (test_status IN ('draft', 'running', 'paused', 'completed', 'stopped')),
    
    -- Test parameters
    hypothesis TEXT,
    primary_metric VARCHAR(100) NOT NULL,
    secondary_metrics JSONB,
    minimum_sample_size INTEGER,
    confidence_level FLOAT DEFAULT 0.95,
    power_level FLOAT DEFAULT 0.80,
    minimum_detectable_effect FLOAT,
    
    -- Test targeting
    target_audience JSONB,
    traffic_allocation JSONB,
    
    -- Test variants
    control_variant JSONB NOT NULL,
    test_variants JSONB NOT NULL,
    
    -- Statistical configuration
    statistical_method VARCHAR(50) DEFAULT 'frequentist',
    early_stopping_enabled BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Metadata
    created_by VARCHAR(100),
    metadata JSONB
);

-- A/B Test Assignments table
CREATE TABLE IF NOT EXISTS ab_test_assignments (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Assignment data
    test_id UUID NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    variant_id VARCHAR(100) NOT NULL,
    variant_name VARCHAR(255) NOT NULL,
    
    -- Assignment context
    assignment_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    assignment_method VARCHAR(50) DEFAULT 'random',
    assignment_probability FLOAT,
    
    -- Conversion tracking
    converted BOOLEAN DEFAULT false,
    conversion_timestamp TIMESTAMP WITH TIME ZONE,
    conversion_value FLOAT,
    
    -- Additional metrics
    engagement_metrics JSONB,
    custom_metrics JSONB,
    
    -- Foreign key constraints
    CONSTRAINT fk_ab_assignment_test_id 
        FOREIGN KEY (test_id) 
        REFERENCES ab_tests(id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_ab_assignment_session_id 
        FOREIGN KEY (session_id) 
        REFERENCES journey_sessions(session_id) 
        ON DELETE CASCADE,
    
    -- Unique constraint to prevent duplicate assignments
    CONSTRAINT unique_test_session_assignment 
        UNIQUE (test_id, session_id)
);

-- =============================================================================
-- CREATE CONVERSION PSYCHOLOGY TRACKING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS psychology_optimizations (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    
    -- Psychology elements
    psychology_type VARCHAR(50) NOT NULL CHECK (psychology_type IN ('scarcity', 'social_proof', 'authority', 'urgency', 'reciprocity', 'commitment')),
    psychology_intensity FLOAT CHECK (psychology_intensity >= 0 AND psychology_intensity <= 1),
    psychology_configuration JSONB,
    
    -- Trust and ethics tracking
    trust_score FLOAT,
    ethics_score FLOAT,
    transparency_level FLOAT,
    manipulation_risk FLOAT,
    
    -- Performance tracking
    display_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    interaction_count INTEGER DEFAULT 0,
    engagement_duration INTEGER,
    conversion_impact FLOAT,
    
    -- A/B testing integration
    ab_test_id UUID,
    variant_id VARCHAR(100),
    
    -- Compliance and approval
    hitl_approved BOOLEAN DEFAULT false,
    approval_timestamp TIMESTAMP WITH TIME ZONE,
    approver_id VARCHAR(100),
    compliance_notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_psychology_session_id 
        FOREIGN KEY (session_id) 
        REFERENCES journey_sessions(session_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_psychology_ab_test_id 
        FOREIGN KEY (ab_test_id) 
        REFERENCES ab_tests(id) 
        ON DELETE SET NULL
);

-- =============================================================================
-- CREATE MARKETING AUTOMATION TRACKING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS marketing_automation_events (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    
    -- Automation data
    automation_type VARCHAR(50) NOT NULL,
    automation_trigger VARCHAR(100) NOT NULL,
    automation_channel VARCHAR(50) NOT NULL,
    automation_campaign_id VARCHAR(100),
    
    -- Trigger context
    trigger_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    trigger_context JSONB,
    trigger_conditions JSONB,
    
    -- Personalization data
    persona_type VARCHAR(50),
    device_type VARCHAR(20),
    personalization_config JSONB,
    content_variants JSONB,
    
    -- Execution data
    execution_status VARCHAR(20) DEFAULT 'pending' CHECK (execution_status IN ('pending', 'executing', 'completed', 'failed', 'skipped')),
    execution_timestamp TIMESTAMP WITH TIME ZONE,
    execution_duration INTEGER,
    execution_result JSONB,
    
    -- Performance metrics
    delivery_successful BOOLEAN,
    engagement_metrics JSONB,
    conversion_metrics JSONB,
    attribution_data JSONB,
    
    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_automation_session_id 
        FOREIGN KEY (session_id) 
        REFERENCES journey_sessions(session_id) 
        ON DELETE CASCADE
);

-- =============================================================================
-- CREATE HITL APPROVAL TRACKING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS hitl_approvals (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Request data
    request_type VARCHAR(50) NOT NULL,
    requester_agent VARCHAR(100) NOT NULL,
    request_description TEXT,
    request_context JSONB,
    
    -- Automation details
    automation_type VARCHAR(50),
    automation_scope JSONB,
    automation_parameters JSONB,
    
    -- Risk assessment
    risk_score FLOAT,
    risk_factors JSONB,
    business_impact JSONB,
    compliance_requirements JSONB,
    
    -- Approval workflow
    approval_status VARCHAR(20) DEFAULT 'pending' CHECK (approval_status IN ('pending', 'approved', 'rejected', 'conditional', 'deferred')),
    approval_category VARCHAR(50),
    assigned_approver VARCHAR(100),
    approval_conditions JSONB,
    approval_restrictions JSONB,
    
    -- Decision data
    decision_timestamp TIMESTAMP WITH TIME ZONE,
    decision_rationale TEXT,
    approver_notes TEXT,
    
    -- Implementation tracking
    implementation_status VARCHAR(20) DEFAULT 'not_started' CHECK (implementation_status IN ('not_started', 'in_progress', 'completed', 'failed', 'rolled_back')),
    implementation_timestamp TIMESTAMP WITH TIME ZONE,
    implementation_result JSONB,
    
    -- Monitoring and rollback
    monitoring_requirements JSONB,
    rollback_triggers JSONB,
    rollback_executed BOOLEAN DEFAULT false,
    rollback_timestamp TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Urgency and priority
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    urgency_level VARCHAR(20) DEFAULT 'normal' CHECK (urgency_level IN ('low', 'normal', 'high', 'emergency'))
);

-- =============================================================================
-- CREATE INDEXES FOR PERFORMANCE
-- =============================================================================

-- Device Conversion Optimization indexes
CREATE INDEX IF NOT EXISTS idx_device_optimization_session_id ON device_conversion_optimizations(session_id);
CREATE INDEX IF NOT EXISTS idx_device_optimization_device_type ON device_conversion_optimizations(device_type);
CREATE INDEX IF NOT EXISTS idx_device_optimization_persona ON device_conversion_optimizations(persona_type);
CREATE INDEX IF NOT EXISTS idx_device_optimization_flow ON device_conversion_optimizations(optimization_flow);
CREATE INDEX IF NOT EXISTS idx_device_optimization_created_at ON device_conversion_optimizations(created_at);

-- Behavioral Tracking Events indexes
CREATE INDEX IF NOT EXISTS idx_behavioral_events_session_id ON behavioral_tracking_events(session_id);
CREATE INDEX IF NOT EXISTS idx_behavioral_events_user_id ON behavioral_tracking_events(user_id);
CREATE INDEX IF NOT EXISTS idx_behavioral_events_type ON behavioral_tracking_events(event_type);
CREATE INDEX IF NOT EXISTS idx_behavioral_events_timestamp ON behavioral_tracking_events(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_behavioral_events_page_url ON behavioral_tracking_events(page_url);

-- A/B Testing indexes
CREATE INDEX IF NOT EXISTS idx_ab_tests_status ON ab_tests(test_status);
CREATE INDEX IF NOT EXISTS idx_ab_tests_created_at ON ab_tests(created_at);
CREATE INDEX IF NOT EXISTS idx_ab_test_assignments_test_id ON ab_test_assignments(test_id);
CREATE INDEX IF NOT EXISTS idx_ab_test_assignments_session_id ON ab_test_assignments(session_id);
CREATE INDEX IF NOT EXISTS idx_ab_test_assignments_converted ON ab_test_assignments(converted);

-- Psychology Optimizations indexes
CREATE INDEX IF NOT EXISTS idx_psychology_session_id ON psychology_optimizations(session_id);
CREATE INDEX IF NOT EXISTS idx_psychology_type ON psychology_optimizations(psychology_type);
CREATE INDEX IF NOT EXISTS idx_psychology_trust_score ON psychology_optimizations(trust_score);
CREATE INDEX IF NOT EXISTS idx_psychology_ab_test_id ON psychology_optimizations(ab_test_id);

-- Marketing Automation indexes
CREATE INDEX IF NOT EXISTS idx_automation_session_id ON marketing_automation_events(session_id);
CREATE INDEX IF NOT EXISTS idx_automation_type ON marketing_automation_events(automation_type);
CREATE INDEX IF NOT EXISTS idx_automation_trigger ON marketing_automation_events(automation_trigger);
CREATE INDEX IF NOT EXISTS idx_automation_status ON marketing_automation_events(execution_status);
CREATE INDEX IF NOT EXISTS idx_automation_timestamp ON marketing_automation_events(trigger_timestamp);

-- HITL Approvals indexes
CREATE INDEX IF NOT EXISTS idx_hitl_approval_status ON hitl_approvals(approval_status);
CREATE INDEX IF NOT EXISTS idx_hitl_approval_category ON hitl_approvals(approval_category);
CREATE INDEX IF NOT EXISTS idx_hitl_approval_priority ON hitl_approvals(priority);
CREATE INDEX IF NOT EXISTS idx_hitl_approval_created_at ON hitl_approvals(created_at);

-- Composite indexes for complex queries
CREATE INDEX IF NOT EXISTS idx_device_optimization_type_persona ON device_conversion_optimizations(device_type, persona_type);
CREATE INDEX IF NOT EXISTS idx_behavioral_events_session_type ON behavioral_tracking_events(session_id, event_type);
CREATE INDEX IF NOT EXISTS idx_ab_assignments_test_variant ON ab_test_assignments(test_id, variant_id);
CREATE INDEX IF NOT EXISTS idx_psychology_type_score ON psychology_optimizations(psychology_type, trust_score);
CREATE INDEX IF NOT EXISTS idx_automation_type_status ON marketing_automation_events(automation_type, execution_status);

-- GIN indexes for JSONB columns
CREATE INDEX IF NOT EXISTS idx_device_optimization_cta_gin ON device_conversion_optimizations USING GIN(cta_configuration);
CREATE INDEX IF NOT EXISTS idx_behavioral_events_properties_gin ON behavioral_tracking_events USING GIN(custom_properties);
CREATE INDEX IF NOT EXISTS idx_ab_tests_variants_gin ON ab_tests USING GIN(test_variants);
CREATE INDEX IF NOT EXISTS idx_psychology_config_gin ON psychology_optimizations USING GIN(psychology_configuration);
CREATE INDEX IF NOT EXISTS idx_automation_context_gin ON marketing_automation_events USING GIN(trigger_context);
CREATE INDEX IF NOT EXISTS idx_hitl_parameters_gin ON hitl_approvals USING GIN(automation_parameters);

-- =============================================================================
-- CREATE ANALYTICS FUNCTIONS
-- =============================================================================

-- Function to calculate device conversion performance
CREATE OR REPLACE FUNCTION calculate_device_conversion_performance(
    p_device_type VARCHAR(20) DEFAULT NULL,
    p_persona_type VARCHAR(50) DEFAULT NULL,
    p_time_range_hours INTEGER DEFAULT 24
) 
RETURNS TABLE (
    device_type VARCHAR(20),
    persona_type VARCHAR(50),
    optimization_flow VARCHAR(50),
    total_optimizations BIGINT,
    avg_expected_conversion NUMERIC,
    avg_actual_conversion NUMERIC,
    conversion_improvement NUMERIC,
    performance_score NUMERIC
) 
LANGUAGE SQL
STABLE
AS $$
    SELECT 
        dco.device_type,
        dco.persona_type,
        dco.optimization_flow,
        COUNT(*) as total_optimizations,
        ROUND(AVG(dco.expected_conversion_rate), 4) as avg_expected_conversion,
        ROUND(AVG(dco.actual_conversion_rate), 4) as avg_actual_conversion,
        ROUND(
            ((AVG(dco.actual_conversion_rate) - AVG(dco.expected_conversion_rate)) / 
             NULLIF(AVG(dco.expected_conversion_rate), 0)) * 100, 2
        ) as conversion_improvement,
        ROUND(AVG(dco.actual_conversion_rate) * 100, 2) as performance_score
    FROM device_conversion_optimizations dco
    WHERE dco.created_at >= CURRENT_TIMESTAMP - (p_time_range_hours || ' hours')::INTERVAL
        AND (p_device_type IS NULL OR dco.device_type = p_device_type)
        AND (p_persona_type IS NULL OR dco.persona_type = p_persona_type)
        AND dco.actual_conversion_rate IS NOT NULL
    GROUP BY dco.device_type, dco.persona_type, dco.optimization_flow
    ORDER BY performance_score DESC;
$$;

-- Function to get A/B test performance summary
CREATE OR REPLACE FUNCTION get_ab_test_performance(
    p_test_id UUID
) 
RETURNS TABLE (
    variant_id VARCHAR(100),
    variant_name VARCHAR(255),
    total_assignments BIGINT,
    conversions BIGINT,
    conversion_rate NUMERIC,
    avg_conversion_value NUMERIC,
    statistical_significance BOOLEAN
) 
LANGUAGE SQL
STABLE
AS $$
    SELECT 
        ata.variant_id,
        ata.variant_name,
        COUNT(*) as total_assignments,
        COUNT(*) FILTER (WHERE ata.converted = true) as conversions,
        ROUND(
            (COUNT(*) FILTER (WHERE ata.converted = true)::NUMERIC / COUNT(*)) * 100, 2
        ) as conversion_rate,
        ROUND(AVG(ata.conversion_value), 2) as avg_conversion_value,
        -- Simple significance check (requires >100 samples and >5% difference)
        (COUNT(*) > 100 AND 
         ABS((COUNT(*) FILTER (WHERE ata.converted = true)::NUMERIC / COUNT(*)) - 0.05) > 0.05
        ) as statistical_significance
    FROM ab_test_assignments ata
    WHERE ata.test_id = p_test_id
    GROUP BY ata.variant_id, ata.variant_name
    ORDER BY conversion_rate DESC;
$$;

-- Function to calculate psychology optimization effectiveness
CREATE OR REPLACE FUNCTION calculate_psychology_effectiveness(
    p_psychology_type VARCHAR(50) DEFAULT NULL,
    p_time_range_hours INTEGER DEFAULT 24
) 
RETURNS TABLE (
    psychology_type VARCHAR(50),
    total_displays BIGINT,
    avg_trust_score NUMERIC,
    avg_ethics_score NUMERIC,
    avg_engagement_duration NUMERIC,
    avg_conversion_impact NUMERIC,
    effectiveness_score NUMERIC
) 
LANGUAGE SQL
STABLE
AS $$
    SELECT 
        po.psychology_type,
        COUNT(*) as total_displays,
        ROUND(AVG(po.trust_score), 3) as avg_trust_score,
        ROUND(AVG(po.ethics_score), 3) as avg_ethics_score,
        ROUND(AVG(po.engagement_duration), 2) as avg_engagement_duration,
        ROUND(AVG(po.conversion_impact), 4) as avg_conversion_impact,
        ROUND(
            (AVG(po.trust_score) * 0.3 + 
             AVG(po.ethics_score) * 0.3 + 
             AVG(po.conversion_impact) * 0.4) * 100, 2
        ) as effectiveness_score
    FROM psychology_optimizations po
    WHERE po.created_at >= CURRENT_TIMESTAMP - (p_time_range_hours || ' hours')::INTERVAL
        AND (p_psychology_type IS NULL OR po.psychology_type = p_psychology_type)
        AND po.trust_score IS NOT NULL
        AND po.ethics_score IS NOT NULL
    GROUP BY po.psychology_type
    ORDER BY effectiveness_score DESC;
$$;

-- =============================================================================
-- CREATE MATERIALIZED VIEWS FOR ANALYTICS
-- =============================================================================

-- Conversion optimization performance view
CREATE MATERIALIZED VIEW IF NOT EXISTS conversion_optimization_analytics AS
SELECT 
    DATE_TRUNC('hour', dco.created_at) as hour_bucket,
    dco.device_type,
    dco.persona_type,
    dco.optimization_flow,
    dco.ui_layout,
    COUNT(*) as optimization_count,
    ROUND(AVG(dco.expected_conversion_rate), 4) as avg_expected_conversion,
    ROUND(AVG(dco.actual_conversion_rate), 4) as avg_actual_conversion,
    ROUND(
        ((AVG(dco.actual_conversion_rate) - AVG(dco.expected_conversion_rate)) / 
         NULLIF(AVG(dco.expected_conversion_rate), 0)) * 100, 2
    ) as avg_improvement_percentage,
    COUNT(DISTINCT dco.session_id) as unique_sessions
FROM device_conversion_optimizations dco
WHERE dco.created_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
    AND dco.actual_conversion_rate IS NOT NULL
GROUP BY 
    DATE_TRUNC('hour', dco.created_at),
    dco.device_type,
    dco.persona_type,
    dco.optimization_flow,
    dco.ui_layout;

-- Behavioral engagement analytics view
CREATE MATERIALIZED VIEW IF NOT EXISTS behavioral_engagement_analytics AS
SELECT 
    DATE_TRUNC('hour', bte.event_timestamp) as hour_bucket,
    bte.event_type,
    bte.event_category,
    js.persona_type,
    js.device_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT bte.session_id) as unique_sessions,
    ROUND(AVG(bte.engagement_score), 3) as avg_engagement_score,
    ROUND(AVG(bte.time_on_page), 2) as avg_time_on_page,
    ROUND(AVG(bte.scroll_depth), 3) as avg_scroll_depth
FROM behavioral_tracking_events bte
JOIN journey_sessions js ON bte.session_id = js.session_id
WHERE bte.event_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY 
    DATE_TRUNC('hour', bte.event_timestamp),
    bte.event_type,
    bte.event_category,
    js.persona_type,
    js.device_type;

-- Create indexes on materialized views
CREATE INDEX IF NOT EXISTS idx_conversion_analytics_hour_bucket ON conversion_optimization_analytics(hour_bucket);
CREATE INDEX IF NOT EXISTS idx_conversion_analytics_device_persona ON conversion_optimization_analytics(device_type, persona_type);
CREATE INDEX IF NOT EXISTS idx_behavioral_analytics_hour_bucket ON behavioral_engagement_analytics(hour_bucket);
CREATE INDEX IF NOT EXISTS idx_behavioral_analytics_event_type ON behavioral_engagement_analytics(event_type, event_category);

-- =============================================================================
-- CREATE UPDATE TRIGGERS
-- =============================================================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER
LANGUAGE PLPGSQL
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- Create update triggers for timestamp management
CREATE TRIGGER trigger_device_optimization_updated_at
    BEFORE UPDATE ON device_conversion_optimizations
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_psychology_optimization_updated_at
    BEFORE UPDATE ON psychology_optimizations
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_automation_events_updated_at
    BEFORE UPDATE ON marketing_automation_events
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_hitl_approvals_updated_at
    BEFORE UPDATE ON hitl_approvals
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_ab_tests_updated_at
    BEFORE UPDATE ON ab_tests
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

-- =============================================================================
-- MIGRATION COMPLETION LOG
-- =============================================================================

INSERT INTO migration_log (migration_name, description, executed_at)
VALUES (
    '004_create_conversion_optimization_tables',
    'Created comprehensive conversion optimization tables for Milestone 2C: device optimization, behavioral tracking, A/B testing, psychology tracking, marketing automation, and HITL approvals',
    CURRENT_TIMESTAMP
);

-- Migration completed successfully