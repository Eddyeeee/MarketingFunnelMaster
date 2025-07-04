-- Migration: Extend Existing Tables for Journey Engine Integration
-- Module: 2B - Dynamic Customer Journey Engine
-- Created: 2024-07-04
-- Description: Extends existing 2A tables with journey-specific fields

-- =============================================================================
-- EXTEND EXISTING USER_PROFILES TABLE
-- =============================================================================

-- Add journey-specific columns to existing user_profiles table
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS journey_history JSONB;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS journey_preferences JSONB;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS scarcity_sensitivity FLOAT CHECK (scarcity_sensitivity >= 0 AND scarcity_sensitivity <= 1);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS personalization_consent BOOLEAN DEFAULT TRUE;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS cross_device_consent BOOLEAN DEFAULT TRUE;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS journey_history_summary JSONB;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_journey_session_id VARCHAR(100);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferred_journey_path VARCHAR(100);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS conversion_patterns JSONB;

-- Add indexes for new user_profiles columns
CREATE INDEX IF NOT EXISTS idx_user_profiles_journey_session ON user_profiles(last_journey_session_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_journey_path ON user_profiles(preferred_journey_path);
CREATE INDEX IF NOT EXISTS idx_user_profiles_scarcity_sensitivity ON user_profiles(scarcity_sensitivity);

-- =============================================================================
-- EXTEND EXISTING PERSONA_PROFILES TABLE
-- =============================================================================

-- Add journey-specific columns to existing persona_profiles table
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS journey_behavior_patterns JSONB;
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS decision_speed VARCHAR(20) CHECK (decision_speed IN ('fast', 'moderate', 'deliberate', 'slow'));
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS personalization_receptivity VARCHAR(20) CHECK (personalization_receptivity IN ('high', 'medium', 'low'));
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS journey_continuity_preference VARCHAR(20) CHECK (journey_continuity_preference IN ('high', 'medium', 'low'));
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS scarcity_trigger_preferences JSONB;
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS optimal_journey_timing JSONB;
ALTER TABLE persona_profiles ADD COLUMN IF NOT EXISTS cross_device_behavior JSONB;

-- Add indexes for new persona_profiles columns
CREATE INDEX IF NOT EXISTS idx_persona_profiles_decision_speed ON persona_profiles(decision_speed);
CREATE INDEX IF NOT EXISTS idx_persona_profiles_personalization_receptivity ON persona_profiles(personalization_receptivity);
CREATE INDEX IF NOT EXISTS idx_persona_profiles_journey_continuity ON persona_profiles(journey_continuity_preference);

-- =============================================================================
-- EXTEND EXISTING DEVICE_OPTIMIZATIONS TABLE
-- =============================================================================

-- Add journey-specific columns to existing device_optimizations table
ALTER TABLE device_optimizations ADD COLUMN IF NOT EXISTS journey_stage_optimizations JSONB;
ALTER TABLE device_optimizations ADD COLUMN IF NOT EXISTS cross_device_optimizations JSONB;
ALTER TABLE device_optimizations ADD COLUMN IF NOT EXISTS journey_performance_metrics JSONB;
ALTER TABLE device_optimizations ADD COLUMN IF NOT EXISTS personalization_constraints JSONB;
ALTER TABLE device_optimizations ADD COLUMN IF NOT EXISTS scarcity_display_preferences JSONB;
ALTER TABLE device_optimizations ADD COLUMN IF NOT EXISTS conversion_flow_optimizations JSONB;

-- Add indexes for new device_optimizations columns
CREATE INDEX IF NOT EXISTS idx_device_optimizations_journey_stage ON device_optimizations USING GIN (journey_stage_optimizations);
CREATE INDEX IF NOT EXISTS idx_device_optimizations_cross_device ON device_optimizations USING GIN (cross_device_optimizations);

-- =============================================================================
-- EXTEND EXISTING INTENT_PROFILES TABLE
-- =============================================================================

-- Add journey-specific columns to existing intent_profiles table
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS journey_progression_intent FLOAT CHECK (journey_progression_intent >= 0 AND journey_progression_intent <= 1);
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS conversion_probability FLOAT CHECK (conversion_probability >= 0 AND conversion_probability <= 1);
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS optimal_intervention_timing INTEGER;
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS scarcity_trigger_readiness FLOAT CHECK (scarcity_trigger_readiness >= 0 AND scarcity_trigger_readiness <= 1);
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS personalization_receptivity_score FLOAT CHECK (personalization_receptivity_score >= 0 AND personalization_receptivity_score <= 1);
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS next_stage_prediction VARCHAR(50);
ALTER TABLE intent_profiles ADD COLUMN IF NOT EXISTS journey_completion_likelihood FLOAT CHECK (journey_completion_likelihood >= 0 AND journey_completion_likelihood <= 1);

-- Add indexes for new intent_profiles columns
CREATE INDEX IF NOT EXISTS idx_intent_profiles_journey_progression ON intent_profiles(journey_progression_intent);
CREATE INDEX IF NOT EXISTS idx_intent_profiles_conversion_probability ON intent_profiles(conversion_probability);
CREATE INDEX IF NOT EXISTS idx_intent_profiles_scarcity_readiness ON intent_profiles(scarcity_trigger_readiness);
CREATE INDEX IF NOT EXISTS idx_intent_profiles_next_stage ON intent_profiles(next_stage_prediction);

-- =============================================================================
-- EXTEND EXISTING PERFORMANCE_METRICS TABLE
-- =============================================================================

-- Add journey-specific metrics to existing performance_metrics table
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS journey_completion_rate FLOAT CHECK (journey_completion_rate >= 0 AND journey_completion_rate <= 1);
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS average_journey_time INTEGER;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS personalization_lift FLOAT;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS scarcity_conversion_rate FLOAT CHECK (scarcity_conversion_rate >= 0 AND scarcity_conversion_rate <= 1);
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS cross_device_continuity_rate FLOAT CHECK (cross_device_continuity_rate >= 0 AND cross_device_continuity_rate <= 1);
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS journey_stage_progression_rates JSONB;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS touchpoint_effectiveness_scores JSONB;

-- Add indexes for new performance_metrics columns
CREATE INDEX IF NOT EXISTS idx_performance_metrics_journey_completion ON performance_metrics(journey_completion_rate);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_journey_time ON performance_metrics(average_journey_time);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_personalization_lift ON performance_metrics(personalization_lift);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_scarcity_conversion ON performance_metrics(scarcity_conversion_rate);

-- =============================================================================
-- CREATE MIGRATION LOG TABLE IF NOT EXISTS
-- =============================================================================

CREATE TABLE IF NOT EXISTS migration_log (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) UNIQUE NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    rollback_script TEXT
);

-- =============================================================================
-- UPDATE EXISTING FUNCTIONS FOR JOURNEY COMPATIBILITY
-- =============================================================================

-- Function to migrate existing user data to journey-compatible format
CREATE OR REPLACE FUNCTION migrate_user_data_for_journey_engine()
RETURNS TABLE(user_id UUID, migration_status VARCHAR, details TEXT) AS $$
BEGIN
    -- Update existing users with default journey preferences
    UPDATE user_profiles 
    SET 
        journey_preferences = jsonb_build_object(
            'preferred_interaction_style', 'adaptive',
            'content_depth_preference', 'medium',
            'scarcity_sensitivity_level', 'medium'
        ),
        scarcity_sensitivity = 0.5,
        personalization_consent = TRUE,
        cross_device_consent = TRUE
    WHERE journey_preferences IS NULL;
    
    -- Return migration results
    RETURN QUERY
    SELECT 
        up.id as user_id,
        'migrated'::VARCHAR as migration_status,
        'Added default journey preferences and consents'::TEXT as details
    FROM user_profiles up
    WHERE up.journey_preferences IS NOT NULL;
END;
$$ LANGUAGE plpgsql;

-- Function to update persona profiles with journey behavior defaults
CREATE OR REPLACE FUNCTION update_persona_profiles_for_journey_engine()
RETURNS TABLE(persona_id UUID, update_status VARCHAR, details TEXT) AS $$
BEGIN
    -- Update TechEarlyAdopter personas
    UPDATE persona_profiles 
    SET 
        decision_speed = 'fast',
        personalization_receptivity = 'high',
        journey_continuity_preference = 'medium',
        journey_behavior_patterns = jsonb_build_object(
            'engagement_style', 'interactive',
            'content_consumption', 'quick_scan',
            'conversion_triggers', ['social_proof', 'innovation_signals']
        )
    WHERE persona_type = 'TechEarlyAdopter' AND journey_behavior_patterns IS NULL;
    
    -- Update RemoteDad personas
    UPDATE persona_profiles 
    SET 
        decision_speed = 'moderate',
        personalization_receptivity = 'medium',
        journey_continuity_preference = 'high',
        journey_behavior_patterns = jsonb_build_object(
            'engagement_style', 'thoughtful',
            'content_consumption', 'detailed_review',
            'conversion_triggers', ['family_benefits', 'time_savings']
        )
    WHERE persona_type = 'RemoteDad' AND journey_behavior_patterns IS NULL;
    
    -- Update StudentHustler personas
    UPDATE persona_profiles 
    SET 
        decision_speed = 'fast',
        personalization_receptivity = 'high',
        journey_continuity_preference = 'low',
        journey_behavior_patterns = jsonb_build_object(
            'engagement_style', 'impulse_driven',
            'content_consumption', 'visual_first',
            'conversion_triggers', ['price_sensitivity', 'quick_wins']
        )
    WHERE persona_type = 'StudentHustler' AND journey_behavior_patterns IS NULL;
    
    -- Update BusinessOwner personas
    UPDATE persona_profiles 
    SET 
        decision_speed = 'deliberate',
        personalization_receptivity = 'medium',
        journey_continuity_preference = 'high',
        journey_behavior_patterns = jsonb_build_object(
            'engagement_style', 'analytical',
            'content_consumption', 'comprehensive_research',
            'conversion_triggers', ['roi_analysis', 'expert_validation']
        )
    WHERE persona_type = 'BusinessOwner' AND journey_behavior_patterns IS NULL;
    
    -- Return update results
    RETURN QUERY
    SELECT 
        pp.id as persona_id,
        'updated'::VARCHAR as update_status,
        ('Updated persona: ' || pp.persona_type)::TEXT as details
    FROM persona_profiles pp
    WHERE pp.journey_behavior_patterns IS NOT NULL;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- CREATE VIEWS FOR UNIFIED DATA ACCESS
-- =============================================================================

-- View combining user profiles with journey data
CREATE OR REPLACE VIEW unified_user_profiles AS
SELECT 
    up.id,
    up.email,
    up.created_at,
    up.updated_at,
    -- Original user profile data
    up.demographics,
    up.preferences,
    up.behavior_patterns,
    -- Journey-specific data
    up.journey_history,
    up.journey_preferences,
    up.scarcity_sensitivity,
    up.personalization_consent,
    up.cross_device_consent,
    up.journey_history_summary,
    up.last_journey_session_id,
    up.preferred_journey_path,
    up.conversion_patterns,
    -- Latest journey session data
    js.current_stage as current_journey_stage,
    js.conversion_probability as latest_conversion_probability,
    js.device_type as latest_device_type,
    js.persona_type as latest_persona_type
FROM user_profiles up
LEFT JOIN journey_sessions js ON up.last_journey_session_id = js.session_id;

-- View combining persona profiles with journey insights
CREATE OR REPLACE VIEW enhanced_persona_profiles AS
SELECT 
    pp.id,
    pp.persona_type,
    pp.confidence_score,
    pp.created_at,
    pp.updated_at,
    -- Original persona data
    pp.characteristics,
    pp.preferences,
    pp.behavioral_indicators,
    -- Journey-enhanced data
    pp.journey_behavior_patterns,
    pp.decision_speed,
    pp.personalization_receptivity,
    pp.journey_continuity_preference,
    pp.scarcity_trigger_preferences,
    pp.optimal_journey_timing,
    pp.cross_device_behavior,
    -- Aggregated journey performance
    COUNT(js.id) as total_journey_sessions,
    AVG(js.conversion_probability) as avg_conversion_probability,
    AVG(js.total_session_time) as avg_session_time
FROM persona_profiles pp
LEFT JOIN journey_sessions js ON pp.persona_type = js.persona_type
GROUP BY pp.id, pp.persona_type, pp.confidence_score, pp.created_at, pp.updated_at,
         pp.characteristics, pp.preferences, pp.behavioral_indicators,
         pp.journey_behavior_patterns, pp.decision_speed, pp.personalization_receptivity,
         pp.journey_continuity_preference, pp.scarcity_trigger_preferences,
         pp.optimal_journey_timing, pp.cross_device_behavior;

-- =============================================================================
-- DATA VALIDATION AND CLEANUP
-- =============================================================================

-- Function to validate extended schema integrity
CREATE OR REPLACE FUNCTION validate_extended_schema_integrity()
RETURNS TABLE(table_name TEXT, column_name TEXT, validation_status VARCHAR, issue_description TEXT) AS $$
BEGIN
    -- Check user_profiles journey data
    RETURN QUERY
    SELECT 
        'user_profiles'::TEXT,
        'scarcity_sensitivity'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END::VARCHAR,
        CASE WHEN COUNT(*) = 0 THEN 'All values within valid range' 
             ELSE COUNT(*)::TEXT || ' records with invalid scarcity_sensitivity values' END::TEXT
    FROM user_profiles 
    WHERE scarcity_sensitivity < 0 OR scarcity_sensitivity > 1;
    
    -- Check persona_profiles decision_speed values
    RETURN QUERY
    SELECT 
        'persona_profiles'::TEXT,
        'decision_speed'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END::VARCHAR,
        CASE WHEN COUNT(*) = 0 THEN 'All values valid' 
             ELSE COUNT(*)::TEXT || ' records with invalid decision_speed values' END::TEXT
    FROM persona_profiles 
    WHERE decision_speed NOT IN ('fast', 'moderate', 'deliberate', 'slow') AND decision_speed IS NOT NULL;
    
    -- Check intent_profiles conversion_probability values
    RETURN QUERY
    SELECT 
        'intent_profiles'::TEXT,
        'conversion_probability'::TEXT,
        CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END::VARCHAR,
        CASE WHEN COUNT(*) = 0 THEN 'All values within valid range' 
             ELSE COUNT(*)::TEXT || ' records with invalid conversion_probability values' END::TEXT
    FROM intent_profiles 
    WHERE conversion_probability < 0 OR conversion_probability > 1;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- MIGRATION COMPLETION
-- =============================================================================

-- Log migration completion
INSERT INTO migration_log (migration_name, executed_at, description, rollback_script) 
VALUES (
    '002_extend_existing_tables',
    CURRENT_TIMESTAMP,
    'Extended existing 2A tables with journey-specific fields for seamless 2B integration',
    '-- Rollback script would drop added columns and functions'
) ON CONFLICT (migration_name) DO NOTHING;

-- Add comments for extended tables
COMMENT ON COLUMN user_profiles.journey_history IS 'Historical journey data and patterns for personalization';
COMMENT ON COLUMN user_profiles.scarcity_sensitivity IS 'User sensitivity to scarcity triggers (0.0 to 1.0)';
COMMENT ON COLUMN persona_profiles.decision_speed IS 'How quickly this persona type makes purchase decisions';
COMMENT ON COLUMN intent_profiles.conversion_probability IS 'ML-predicted probability of conversion based on journey data';
COMMENT ON COLUMN performance_metrics.journey_completion_rate IS 'Rate of successful journey completions';

-- Migration completed successfully
SELECT 'Migration 002_extend_existing_tables completed successfully' as status;