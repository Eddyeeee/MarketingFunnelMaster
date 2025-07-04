-- A/B Testing Framework Database Schema
-- Module: 2C - Conversion & Marketing Automation
-- Created: 2025-07-04

-- Create A/B Tests table
CREATE TABLE IF NOT EXISTS ab_tests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_name VARCHAR(255) NOT NULL,
    test_type VARCHAR(50) NOT NULL CHECK (test_type IN ('ab_test', 'multivariate', 'bandit', 'split_url')),
    hypothesis TEXT NOT NULL,
    
    -- Metrics configuration
    primary_metric VARCHAR(100) NOT NULL CHECK (primary_metric IN (
        'conversion_rate', 'revenue', 'engagement', 'retention', 
        'click_through_rate', 'time_on_page', 'bounce_rate'
    )),
    secondary_metrics TEXT[], -- Array of secondary metrics
    
    -- Statistical parameters
    confidence_level DECIMAL(3,2) NOT NULL DEFAULT 0.95 CHECK (confidence_level IN (0.90, 0.95, 0.99)),
    minimum_detectable_effect DECIMAL(4,3) NOT NULL DEFAULT 0.050 CHECK (minimum_detectable_effect > 0),
    statistical_power DECIMAL(3,2) NOT NULL DEFAULT 0.80 CHECK (statistical_power BETWEEN 0.70 AND 0.95),
    
    -- Test parameters
    max_duration_days INTEGER NOT NULL DEFAULT 30 CHECK (max_duration_days BETWEEN 1 AND 180),
    minimum_sample_size INTEGER NOT NULL DEFAULT 1000 CHECK (minimum_sample_size >= 100),
    required_sample_size INTEGER, -- Calculated required sample size
    
    -- Targeting
    target_url_pattern TEXT NOT NULL,
    audience_filters JSONB,
    device_targeting TEXT[], -- Array of device types
    
    -- Advanced settings
    auto_winner_threshold DECIMAL(3,2) NOT NULL DEFAULT 0.95 CHECK (auto_winner_threshold BETWEEN 0.90 AND 0.99),
    early_stopping_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    sequential_testing BOOLEAN NOT NULL DEFAULT FALSE,
    allocation_strategy VARCHAR(50) NOT NULL DEFAULT 'equal' CHECK (allocation_strategy IN ('equal', 'weighted', 'bandit', 'adaptive')),
    
    -- Status and timing
    status VARCHAR(50) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'running', 'paused', 'completed', 'stopped', 'inconclusive')),
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(100),
    
    -- Constraints
    CONSTRAINT valid_date_range CHECK (end_date IS NULL OR end_date > start_date),
    CONSTRAINT valid_status_dates CHECK (
        (status = 'draft' AND start_date IS NULL) OR
        (status IN ('running', 'paused', 'completed', 'stopped', 'inconclusive') AND start_date IS NOT NULL)
    )
);

-- Create indexes for ab_tests
CREATE INDEX idx_ab_tests_status ON ab_tests(status);
CREATE INDEX idx_ab_tests_created_at ON ab_tests(created_at);
CREATE INDEX idx_ab_tests_target_url ON ab_tests USING GIN (target_url_pattern gin_trgm_ops);

-- Create A/B Test Variants table
CREATE TABLE IF NOT EXISTS ab_test_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    
    -- Variant details
    variant_type VARCHAR(50) NOT NULL CHECK (variant_type IN ('control', 'variant')),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Variant configuration
    changes JSONB NOT NULL, -- JSON describing the changes to apply
    weight DECIMAL(3,2) NOT NULL DEFAULT 1.00 CHECK (weight BETWEEN 0 AND 1),
    
    -- Performance expectations
    baseline_conversion_rate DECIMAL(5,4) CHECK (baseline_conversion_rate BETWEEN 0 AND 1),
    expected_lift DECIMAL(4,3) CHECK (expected_lift BETWEEN -1 AND 10),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(test_id, name)
);

-- Create indexes for ab_test_variants
CREATE INDEX idx_ab_test_variants_test_id ON ab_test_variants(test_id);
CREATE INDEX idx_ab_test_variants_type ON ab_test_variants(variant_type);

-- Create Traffic Allocation table
CREATE TABLE IF NOT EXISTS ab_test_traffic_allocation (
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES ab_test_variants(id) ON DELETE CASCADE,
    allocation_percentage DECIMAL(5,4) NOT NULL CHECK (allocation_percentage BETWEEN 0 AND 1),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    
    PRIMARY KEY (test_id, variant_id)
);

-- Create index for traffic allocation
CREATE INDEX idx_traffic_allocation_test_id ON ab_test_traffic_allocation(test_id);

-- Create A/B Test Assignments table
CREATE TABLE IF NOT EXISTS ab_test_assignments (
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES ab_test_variants(id) ON DELETE CASCADE,
    
    -- User identification
    user_id VARCHAR(100),
    session_id VARCHAR(100) NOT NULL,
    
    -- Assignment context
    page_url TEXT NOT NULL,
    user_agent TEXT,
    device_type VARCHAR(50),
    assignment_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Assignment metadata
    assignment_method VARCHAR(50) NOT NULL DEFAULT 'hash_based',
    custom_attributes JSONB,
    
    -- Constraints
    PRIMARY KEY (test_id, COALESCE(user_id, ''), session_id),
    
    -- At least one of user_id or session_id must be provided
    CONSTRAINT valid_user_identification CHECK (user_id IS NOT NULL OR session_id IS NOT NULL)
);

-- Create indexes for ab_test_assignments
CREATE INDEX idx_ab_assignments_test_variant ON ab_test_assignments(test_id, variant_id);
CREATE INDEX idx_ab_assignments_user_id ON ab_test_assignments(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_ab_assignments_session_id ON ab_test_assignments(session_id);
CREATE INDEX idx_ab_assignments_timestamp ON ab_test_assignments(assignment_timestamp);

-- Create A/B Test Events table
CREATE TABLE IF NOT EXISTS ab_test_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES ab_test_variants(id) ON DELETE CASCADE,
    
    -- User identification
    user_id VARCHAR(100),
    session_id VARCHAR(100) NOT NULL,
    
    -- Event details
    event_type VARCHAR(100) NOT NULL,
    event_value DECIMAL(10,2), -- For revenue events
    event_properties JSONB,
    
    -- Timing
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Event metadata
    page_url TEXT,
    referrer TEXT,
    user_agent TEXT,
    device_type VARCHAR(50),
    
    -- Performance tracking
    server_processing_time_ms INTEGER,
    client_timestamp TIMESTAMP WITH TIME ZONE
);

-- Create indexes for ab_test_events
CREATE INDEX idx_ab_events_test_variant ON ab_test_events(test_id, variant_id);
CREATE INDEX idx_ab_events_session ON ab_test_events(session_id);
CREATE INDEX idx_ab_events_type ON ab_test_events(event_type);
CREATE INDEX idx_ab_events_timestamp ON ab_test_events(event_timestamp);
CREATE INDEX idx_ab_events_conversion ON ab_test_events(test_id, variant_id, event_type) 
    WHERE event_type = 'conversion';

-- Create A/B Test Statistics table (for real-time stats caching)
CREATE TABLE IF NOT EXISTS ab_test_statistics (
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES ab_test_variants(id) ON DELETE CASCADE,
    
    -- Basic metrics
    participants INTEGER NOT NULL DEFAULT 0,
    conversions INTEGER NOT NULL DEFAULT 0,
    conversion_rate DECIMAL(6,5) NOT NULL DEFAULT 0,
    
    -- Revenue metrics
    total_revenue DECIMAL(12,2) DEFAULT 0,
    revenue_per_visitor DECIMAL(8,2) DEFAULT 0,
    
    -- Engagement metrics
    total_events INTEGER DEFAULT 0,
    avg_time_on_page DECIMAL(8,2) DEFAULT 0,
    bounce_rate DECIMAL(5,4) DEFAULT 0,
    
    -- Statistical metrics
    confidence_interval_lower DECIMAL(6,5),
    confidence_interval_upper DECIMAL(6,5),
    p_value DECIMAL(10,8),
    statistical_significance BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    calculation_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (test_id, variant_id)
);

-- Create indexes for ab_test_statistics
CREATE INDEX idx_ab_stats_test_id ON ab_test_statistics(test_id);
CREATE INDEX idx_ab_stats_updated ON ab_test_statistics(updated_at);

-- Create A/B Test Results table (for finalized test results)
CREATE TABLE IF NOT EXISTS ab_test_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    
    -- Test outcome
    winning_variant_id UUID REFERENCES ab_test_variants(id),
    recommendation TEXT NOT NULL,
    confidence_score DECIMAL(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    
    -- Statistical summary
    statistical_significance JSONB NOT NULL,
    effect_size DECIMAL(6,4),
    practical_significance BOOLEAN,
    
    -- Business impact
    estimated_revenue_impact DECIMAL(12,2),
    estimated_conversion_lift DECIMAL(5,4),
    implementation_priority VARCHAR(50) CHECK (implementation_priority IN ('low', 'medium', 'high', 'critical')),
    
    -- Test quality metrics
    sample_size_adequacy BOOLEAN NOT NULL,
    test_duration_days INTEGER NOT NULL,
    data_quality_score DECIMAL(3,2) CHECK (data_quality_score BETWEEN 0 AND 1),
    
    -- Metadata
    analysis_completed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    analyzed_by VARCHAR(100),
    
    -- Constraints
    UNIQUE(test_id)
);

-- Create indexes for ab_test_results
CREATE INDEX idx_ab_results_test_id ON ab_test_results(test_id);
CREATE INDEX idx_ab_results_winning_variant ON ab_test_results(winning_variant_id);
CREATE INDEX idx_ab_results_completed ON ab_test_results(analysis_completed_at);

-- Create A/B Test Implementation Log table
CREATE TABLE IF NOT EXISTS ab_test_implementations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES ab_test_variants(id) ON DELETE CASCADE,
    
    -- Implementation details
    implementation_type VARCHAR(50) NOT NULL CHECK (implementation_type IN (
        'full_rollout', 'gradual_rollout', 'segment_rollout', 'canary_rollout'
    )),
    rollout_percentage DECIMAL(5,4) NOT NULL DEFAULT 1.0 CHECK (rollout_percentage BETWEEN 0 AND 1),
    target_segments TEXT[],
    
    -- Status tracking
    status VARCHAR(50) NOT NULL DEFAULT 'planned' CHECK (status IN (
        'planned', 'in_progress', 'completed', 'rolled_back', 'failed'
    )),
    
    -- Performance monitoring
    performance_metrics JSONB,
    rollback_reason TEXT,
    
    -- Timing
    planned_start_date TIMESTAMP WITH TIME ZONE,
    actual_start_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    implemented_by VARCHAR(100),
    
    -- Constraints
    CONSTRAINT valid_implementation_dates CHECK (
        actual_start_date IS NULL OR 
        planned_start_date IS NULL OR 
        actual_start_date >= planned_start_date - INTERVAL '1 day'
    )
);

-- Create indexes for ab_test_implementations
CREATE INDEX idx_ab_implementations_test_id ON ab_test_implementations(test_id);
CREATE INDEX idx_ab_implementations_status ON ab_test_implementations(status);
CREATE INDEX idx_ab_implementations_start_date ON ab_test_implementations(actual_start_date);

-- Create function to automatically calculate test statistics
CREATE OR REPLACE FUNCTION calculate_ab_test_statistics(p_test_id UUID)
RETURNS TABLE (
    variant_id UUID,
    participants INTEGER,
    conversions INTEGER,
    conversion_rate DECIMAL(6,5),
    total_revenue DECIMAL(12,2),
    revenue_per_visitor DECIMAL(8,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        v.id as variant_id,
        COUNT(DISTINCT a.session_id)::INTEGER as participants,
        COUNT(DISTINCT CASE WHEN e.event_type = 'conversion' THEN a.session_id END)::INTEGER as conversions,
        COALESCE(
            COUNT(DISTINCT CASE WHEN e.event_type = 'conversion' THEN a.session_id END)::DECIMAL / 
            NULLIF(COUNT(DISTINCT a.session_id), 0), 
            0
        )::DECIMAL(6,5) as conversion_rate,
        COALESCE(SUM(CASE WHEN e.event_type = 'conversion' THEN e.event_value END), 0)::DECIMAL(12,2) as total_revenue,
        COALESCE(
            SUM(CASE WHEN e.event_type = 'conversion' THEN e.event_value END)::DECIMAL / 
            NULLIF(COUNT(DISTINCT a.session_id), 0),
            0
        )::DECIMAL(8,2) as revenue_per_visitor
    FROM ab_test_variants v
    LEFT JOIN ab_test_assignments a ON v.id = a.variant_id
    LEFT JOIN ab_test_events e ON v.id = e.variant_id AND a.session_id = e.session_id
    WHERE v.test_id = p_test_id
    GROUP BY v.id
    ORDER BY v.variant_type DESC, v.name;
END;
$$ LANGUAGE plpgsql;

-- Create function to update statistics automatically
CREATE OR REPLACE FUNCTION update_ab_test_statistics_trigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Update statistics for the affected test
    INSERT INTO ab_test_statistics (test_id, variant_id, participants, conversions, conversion_rate, total_revenue, revenue_per_visitor)
    SELECT 
        NEW.test_id,
        stats.variant_id,
        stats.participants,
        stats.conversions,
        stats.conversion_rate,
        stats.total_revenue,
        stats.revenue_per_visitor
    FROM calculate_ab_test_statistics(NEW.test_id) stats
    ON CONFLICT (test_id, variant_id) 
    DO UPDATE SET
        participants = EXCLUDED.participants,
        conversions = EXCLUDED.conversions,
        conversion_rate = EXCLUDED.conversion_rate,
        total_revenue = EXCLUDED.total_revenue,
        revenue_per_visitor = EXCLUDED.revenue_per_visitor,
        updated_at = CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers to automatically update statistics
CREATE TRIGGER trigger_update_ab_stats_on_assignment
    AFTER INSERT OR UPDATE OR DELETE ON ab_test_assignments
    FOR EACH ROW
    EXECUTE FUNCTION update_ab_test_statistics_trigger();

CREATE TRIGGER trigger_update_ab_stats_on_event
    AFTER INSERT OR UPDATE OR DELETE ON ab_test_events
    FOR EACH ROW
    EXECUTE FUNCTION update_ab_test_statistics_trigger();

-- Add comments for documentation
COMMENT ON TABLE ab_tests IS 'A/B test configurations and metadata';
COMMENT ON TABLE ab_test_variants IS 'Test variants with their configurations';
COMMENT ON TABLE ab_test_traffic_allocation IS 'Traffic allocation percentages for each variant';
COMMENT ON TABLE ab_test_assignments IS 'User assignments to test variants';
COMMENT ON TABLE ab_test_events IS 'Events tracked for A/B tests (conversions, interactions, etc.)';
COMMENT ON TABLE ab_test_statistics IS 'Real-time statistics cache for A/B tests';
COMMENT ON TABLE ab_test_results IS 'Final results and recommendations for completed tests';
COMMENT ON TABLE ab_test_implementations IS 'Implementation tracking for winning variants';

-- Grant permissions (adjust as needed for your security model)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ab_testing_service;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ab_testing_service;