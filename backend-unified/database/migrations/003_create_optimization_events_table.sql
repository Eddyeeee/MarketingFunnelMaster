-- Migration: Create optimization_events table
-- Module: 2B - Dynamic Customer Journey Engine  
-- Created: 2024-07-04
-- Description: Creates table for tracking real-time optimization events

-- =============================================================================
-- CREATE OPTIMIZATION EVENTS TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS optimization_events (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    
    -- Optimization data
    optimization_type VARCHAR(50) NOT NULL,
    optimization_strategy VARCHAR(100),
    optimization_details JSONB,
    optimization_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Impact measurement
    expected_impact FLOAT,
    actual_impact FLOAT,
    impact_measurement_timestamp TIMESTAMP WITH TIME ZONE,
    
    -- Success metrics
    success_metrics JSONB,
    optimization_success BOOLEAN,
    
    -- Additional metadata
    ml_model_version VARCHAR(50),
    confidence_score FLOAT,
    metadata JSONB,
    
    -- Foreign key constraint
    CONSTRAINT fk_optimization_events_session_id 
        FOREIGN KEY (session_id) 
        REFERENCES journey_sessions(session_id) 
        ON DELETE CASCADE
);

-- =============================================================================
-- CREATE INDEXES FOR PERFORMANCE
-- =============================================================================

-- Primary query indexes
CREATE INDEX IF NOT EXISTS idx_optimization_events_session_id 
    ON optimization_events(session_id);

CREATE INDEX IF NOT EXISTS idx_optimization_events_type 
    ON optimization_events(optimization_type);

CREATE INDEX IF NOT EXISTS idx_optimization_events_strategy 
    ON optimization_events(optimization_strategy);

CREATE INDEX IF NOT EXISTS idx_optimization_events_timestamp 
    ON optimization_events(optimization_timestamp);

CREATE INDEX IF NOT EXISTS idx_optimization_events_success 
    ON optimization_events(optimization_success);

-- Composite indexes for analytics
CREATE INDEX IF NOT EXISTS idx_optimization_events_type_timestamp 
    ON optimization_events(optimization_type, optimization_timestamp);

CREATE INDEX IF NOT EXISTS idx_optimization_events_session_timestamp 
    ON optimization_events(session_id, optimization_timestamp);

CREATE INDEX IF NOT EXISTS idx_optimization_events_success_type 
    ON optimization_events(optimization_success, optimization_type);

-- GIN indexes for JSONB columns
CREATE INDEX IF NOT EXISTS idx_optimization_events_details_gin 
    ON optimization_events USING GIN(optimization_details);

CREATE INDEX IF NOT EXISTS idx_optimization_events_success_metrics_gin 
    ON optimization_events USING GIN(success_metrics);

CREATE INDEX IF NOT EXISTS idx_optimization_events_metadata_gin 
    ON optimization_events USING GIN(metadata);

-- =============================================================================
-- CREATE PARTITIONING BY TIMESTAMP (OPTIONAL FOR HIGH VOLUME)
-- =============================================================================

-- Note: For high-volume deployments, consider partitioning by month
-- This would require creating partition tables and partition constraints

-- Example partition setup (commented out for now):
-- CREATE TABLE optimization_events_2024_07 PARTITION OF optimization_events
--     FOR VALUES FROM ('2024-07-01') TO ('2024-08-01');

-- =============================================================================
-- OPTIMIZATION EVENT ANALYTICS FUNCTIONS
-- =============================================================================

-- Function to calculate optimization effectiveness
CREATE OR REPLACE FUNCTION calculate_optimization_effectiveness(
    p_session_id VARCHAR(100),
    p_time_range_hours INTEGER DEFAULT 24
) 
RETURNS TABLE (
    optimization_type VARCHAR(50),
    total_optimizations BIGINT,
    successful_optimizations BIGINT,
    success_rate NUMERIC,
    avg_expected_impact NUMERIC,
    avg_actual_impact NUMERIC
) 
LANGUAGE SQL
STABLE
AS $$
    SELECT 
        oe.optimization_type,
        COUNT(*) as total_optimizations,
        COUNT(*) FILTER (WHERE oe.optimization_success = true) as successful_optimizations,
        ROUND(
            (COUNT(*) FILTER (WHERE oe.optimization_success = true)::NUMERIC / COUNT(*)) * 100, 2
        ) as success_rate,
        ROUND(AVG(oe.expected_impact), 4) as avg_expected_impact,
        ROUND(AVG(oe.actual_impact), 4) as avg_actual_impact
    FROM optimization_events oe
    WHERE oe.session_id = p_session_id
        AND oe.optimization_timestamp >= CURRENT_TIMESTAMP - (p_time_range_hours || ' hours')::INTERVAL
    GROUP BY oe.optimization_type
    ORDER BY total_optimizations DESC;
$$;

-- Function to get optimization timeline for a session
CREATE OR REPLACE FUNCTION get_optimization_timeline(
    p_session_id VARCHAR(100)
)
RETURNS TABLE (
    optimization_timestamp TIMESTAMP WITH TIME ZONE,
    optimization_type VARCHAR(50),
    optimization_strategy VARCHAR(100),
    expected_impact FLOAT,
    actual_impact FLOAT,
    optimization_success BOOLEAN,
    time_since_session_start INTERVAL
)
LANGUAGE SQL
STABLE
AS $$
    SELECT 
        oe.optimization_timestamp,
        oe.optimization_type,
        oe.optimization_strategy,
        oe.expected_impact,
        oe.actual_impact,
        oe.optimization_success,
        (oe.optimization_timestamp - js.start_timestamp) as time_since_session_start
    FROM optimization_events oe
    JOIN journey_sessions js ON oe.session_id = js.session_id
    WHERE oe.session_id = p_session_id
    ORDER BY oe.optimization_timestamp;
$$;

-- =============================================================================
-- OPTIMIZATION PERFORMANCE MATERIALIZED VIEW
-- =============================================================================

-- Create materialized view for optimization performance analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS optimization_performance_analytics AS
SELECT 
    DATE_TRUNC('hour', oe.optimization_timestamp) as hour_bucket,
    oe.optimization_type,
    oe.optimization_strategy,
    js.persona_type,
    js.current_stage,
    js.device_type,
    COUNT(*) as optimization_count,
    COUNT(*) FILTER (WHERE oe.optimization_success = true) as successful_optimizations,
    ROUND(
        (COUNT(*) FILTER (WHERE oe.optimization_success = true)::NUMERIC / COUNT(*)) * 100, 2
    ) as success_rate,
    ROUND(AVG(oe.expected_impact), 4) as avg_expected_impact,
    ROUND(AVG(oe.actual_impact), 4) as avg_actual_impact,
    ROUND(AVG(oe.confidence_score), 4) as avg_confidence_score,
    COUNT(DISTINCT oe.session_id) as unique_sessions_optimized
FROM optimization_events oe
JOIN journey_sessions js ON oe.session_id = js.session_id
WHERE oe.optimization_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY 
    DATE_TRUNC('hour', oe.optimization_timestamp),
    oe.optimization_type,
    oe.optimization_strategy,
    js.persona_type,
    js.current_stage,
    js.device_type;

-- Create indexes on materialized view
CREATE INDEX IF NOT EXISTS idx_optimization_performance_hour_bucket 
    ON optimization_performance_analytics(hour_bucket);

CREATE INDEX IF NOT EXISTS idx_optimization_performance_type_strategy 
    ON optimization_performance_analytics(optimization_type, optimization_strategy);

CREATE INDEX IF NOT EXISTS idx_optimization_performance_persona_stage 
    ON optimization_performance_analytics(persona_type, current_stage);

-- =============================================================================
-- OPTIMIZATION CLEANUP PROCEDURES
-- =============================================================================

-- Function to clean up old optimization events (for data retention)
CREATE OR REPLACE FUNCTION cleanup_old_optimization_events(
    p_retention_days INTEGER DEFAULT 90
)
RETURNS INTEGER
LANGUAGE PLPGSQL
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM optimization_events 
    WHERE optimization_timestamp < CURRENT_TIMESTAMP - (p_retention_days || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Refresh materialized view after cleanup
    REFRESH MATERIALIZED VIEW optimization_performance_analytics;
    
    -- Log cleanup operation
    INSERT INTO migration_log (migration_name, description)
    VALUES (
        'optimization_events_cleanup_' || CURRENT_DATE,
        'Cleaned up ' || deleted_count || ' optimization events older than ' || p_retention_days || ' days'
    );
    
    RETURN deleted_count;
END;
$$;

-- =============================================================================
-- TRIGGERS FOR REAL-TIME ANALYTICS
-- =============================================================================

-- Function to update materialized view when optimization events change
CREATE OR REPLACE FUNCTION refresh_optimization_analytics()
RETURNS TRIGGER
LANGUAGE PLPGSQL
AS $$
BEGIN
    -- Refresh materialized view in background (requires pg_cron or similar)
    -- For now, we'll refresh it manually or via scheduled job
    -- REFRESH MATERIALIZED VIEW CONCURRENTLY optimization_performance_analytics;
    
    RETURN COALESCE(NEW, OLD);
END;
$$;

-- Create trigger for materialized view refresh
-- Note: This trigger would cause performance issues in high-volume scenarios
-- Consider using a scheduled job instead for production
CREATE TRIGGER trigger_refresh_optimization_analytics
    AFTER INSERT OR UPDATE OR DELETE ON optimization_events
    FOR EACH STATEMENT
    EXECUTE FUNCTION refresh_optimization_analytics();

-- =============================================================================
-- SECURITY AND PERMISSIONS
-- =============================================================================

-- Grant appropriate permissions
-- Note: Adjust these based on your application's user roles

-- Grant read/write access to application role
-- GRANT SELECT, INSERT, UPDATE, DELETE ON optimization_events TO app_user;
-- GRANT USAGE ON SEQUENCE optimization_events_id_seq TO app_user;

-- Grant read-only access to analytics role
-- GRANT SELECT ON optimization_events TO analytics_user;
-- GRANT SELECT ON optimization_performance_analytics TO analytics_user;

-- =============================================================================
-- MIGRATION COMPLETION LOG
-- =============================================================================

INSERT INTO migration_log (migration_name, description, executed_at)
VALUES (
    '003_create_optimization_events_table',
    'Created optimization_events table with indexes, functions, materialized views, and triggers for real-time optimization tracking',
    CURRENT_TIMESTAMP
);

-- Migration completed successfully