-- Neon PostgreSQL Database Setup for Agentic RAG System
-- Version: 1.0.0
-- Created: 2025-07-03

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create documents table with vector embeddings
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50) DEFAULT 'text',
    metadata JSONB DEFAULT '{}',
    
    -- Outcome tracking fields
    engagement_score FLOAT DEFAULT 0.0 CHECK (engagement_score >= 0.0 AND engagement_score <= 1.0),
    conversion_rate FLOAT DEFAULT 0.0 CHECK (conversion_rate >= 0.0 AND conversion_rate <= 1.0),
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    
    -- Temporal tracking
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Search optimization
    content_vector vector(1536), -- OpenAI embedding dimension
    
    -- Performance metrics
    citation_count INTEGER DEFAULT 0,
    reference_count INTEGER DEFAULT 0,
    
    -- Content metrics
    word_count INTEGER DEFAULT 0,
    reading_time_minutes FLOAT DEFAULT 0.0,
    complexity_score FLOAT DEFAULT 0.0 CHECK (complexity_score >= 0.0 AND complexity_score <= 1.0),
    
    -- Processing status
    chunks_generated BOOLEAN DEFAULT FALSE,
    graph_entities_extracted BOOLEAN DEFAULT FALSE,
    
    -- Lifecycle
    is_active BOOLEAN DEFAULT TRUE,
    retirement_date TIMESTAMP,
    replacement_id UUID
);

-- Create chunks table for semantic segmentation
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),
    
    -- Chunk metadata
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    token_count INTEGER CHECK (token_count >= 0),
    overlap_tokens INTEGER DEFAULT 0 CHECK (overlap_tokens >= 0),
    
    -- Performance metrics
    relevance_score FLOAT DEFAULT 0.0 CHECK (relevance_score >= 0.0 AND relevance_score <= 1.0),
    click_through_rate FLOAT DEFAULT 0.0 CHECK (click_through_rate >= 0.0 AND click_through_rate <= 1.0),
    dwell_time_seconds FLOAT DEFAULT 0.0 CHECK (dwell_time_seconds >= 0.0),
    
    -- Learning signals
    user_feedback_score FLOAT CHECK (user_feedback_score >= 1.0 AND user_feedback_score <= 5.0),
    confidence_score FLOAT DEFAULT 0.0 CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    
    -- Temporal data
    created_at TIMESTAMP DEFAULT NOW(),
    last_retrieved TIMESTAMP,
    retrieval_count INTEGER DEFAULT 0,
    
    -- Context
    preceding_chunk_id UUID,
    following_chunk_id UUID,
    
    -- Quality metrics
    coherence_score FLOAT DEFAULT 0.0 CHECK (coherence_score >= 0.0 AND coherence_score <= 1.0),
    information_density FLOAT DEFAULT 0.0 CHECK (information_density >= 0.0 AND information_density <= 1.0),
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Create search outcomes table for learning optimization
CREATE TABLE search_outcomes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_id UUID NOT NULL,
    query_text TEXT NOT NULL,
    
    -- Search strategy used
    search_strategy VARCHAR(50) NOT NULL CHECK (search_strategy IN ('vector', 'graph', 'hybrid', 'adaptive')),
    
    -- Results metadata
    results_count INTEGER NOT NULL CHECK (results_count >= 0),
    top_chunk_ids UUID[],
    relevance_scores FLOAT[],
    
    -- Performance metrics
    response_time_ms FLOAT NOT NULL CHECK (response_time_ms >= 0.0),
    total_tokens INTEGER,
    
    -- User interaction data
    user_satisfaction INTEGER CHECK (user_satisfaction >= 1 AND user_satisfaction <= 5),
    clicked_results INTEGER[],
    session_id UUID,
    
    -- Learning signals
    conversion_achieved BOOLEAN DEFAULT FALSE,
    downstream_actions TEXT[],
    
    -- Query processing
    intent_classification VARCHAR(100),
    complexity_level INTEGER DEFAULT 1 CHECK (complexity_level >= 1 AND complexity_level <= 5),
    
    -- Temporal data
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Additional metadata
    metadata JSONB DEFAULT '{}'
);

-- Create agent performance table
CREATE TABLE agent_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name VARCHAR(100) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    
    -- Performance metrics
    success_rate FLOAT DEFAULT 0.0 CHECK (success_rate >= 0.0 AND success_rate <= 1.0),
    average_response_time_ms FLOAT DEFAULT 0.0 CHECK (average_response_time_ms >= 0.0),
    error_rate FLOAT DEFAULT 0.0 CHECK (error_rate >= 0.0 AND error_rate <= 1.0),
    
    -- Learning metrics
    improvement_rate FLOAT DEFAULT 0.0 CHECK (improvement_rate >= 0.0 AND improvement_rate <= 1.0),
    knowledge_freshness FLOAT DEFAULT 1.0 CHECK (knowledge_freshness >= 0.0 AND knowledge_freshness <= 1.0),
    
    -- Resource usage
    compute_cost_per_task FLOAT DEFAULT 0.0 CHECK (compute_cost_per_task >= 0.0),
    memory_usage_mb FLOAT DEFAULT 0.0 CHECK (memory_usage_mb >= 0.0),
    
    -- Interaction history
    total_tasks_completed INTEGER DEFAULT 0 CHECK (total_tasks_completed >= 0),
    total_errors INTEGER DEFAULT 0 CHECK (total_errors >= 0),
    last_error_timestamp TIMESTAMP,
    
    -- Temporal tracking
    measurement_period_start TIMESTAMP NOT NULL,
    measurement_period_end TIMESTAMP NOT NULL,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Create system metrics table
CREATE TABLE system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Performance metrics
    total_queries_processed INTEGER DEFAULT 0 CHECK (total_queries_processed >= 0),
    average_response_time_ms FLOAT DEFAULT 0.0 CHECK (average_response_time_ms >= 0.0),
    search_accuracy FLOAT DEFAULT 0.0 CHECK (search_accuracy >= 0.0 AND search_accuracy <= 1.0),
    user_satisfaction_score FLOAT DEFAULT 0.0 CHECK (user_satisfaction_score >= 0.0 AND user_satisfaction_score <= 5.0),
    
    -- Resource utilization
    cpu_usage_percent FLOAT DEFAULT 0.0 CHECK (cpu_usage_percent >= 0.0 AND cpu_usage_percent <= 100.0),
    memory_usage_mb FLOAT DEFAULT 0.0 CHECK (memory_usage_mb >= 0.0),
    storage_usage_gb FLOAT DEFAULT 0.0 CHECK (storage_usage_gb >= 0.0),
    
    -- Database performance
    vector_db_response_time_ms FLOAT DEFAULT 0.0 CHECK (vector_db_response_time_ms >= 0.0),
    graph_db_response_time_ms FLOAT DEFAULT 0.0 CHECK (graph_db_response_time_ms >= 0.0),
    
    -- Learning system performance
    learning_iterations_completed INTEGER DEFAULT 0 CHECK (learning_iterations_completed >= 0),
    performance_improvements_applied INTEGER DEFAULT 0 CHECK (performance_improvements_applied >= 0),
    
    -- Error tracking
    error_rate FLOAT DEFAULT 0.0 CHECK (error_rate >= 0.0 AND error_rate <= 1.0),
    critical_errors INTEGER DEFAULT 0 CHECK (critical_errors >= 0),
    
    -- Temporal
    measurement_start TIMESTAMP NOT NULL,
    measurement_end TIMESTAMP NOT NULL,
    
    -- Trends
    performance_trend FLOAT DEFAULT 0.0 CHECK (performance_trend >= -1.0 AND performance_trend <= 1.0),
    improvement_velocity FLOAT DEFAULT 0.0 CHECK (improvement_velocity >= 0.0)
);

-- Create indexes for optimal performance
-- Documents table indexes
CREATE INDEX idx_documents_source ON documents(source);
CREATE INDEX idx_documents_content_type ON documents(content_type);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);
CREATE INDEX idx_documents_engagement ON documents(engagement_score DESC);
CREATE INDEX idx_documents_conversion ON documents(conversion_rate DESC);
CREATE INDEX idx_documents_active ON documents(is_active);
CREATE INDEX idx_documents_processing ON documents(chunks_generated, graph_entities_extracted);

-- Vector similarity search index (HNSW for production)
CREATE INDEX idx_documents_content_vector ON documents 
USING hnsw (content_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Chunks table indexes
CREATE INDEX idx_chunks_document_id ON chunks(document_id);
CREATE INDEX idx_chunks_chunk_index ON chunks(chunk_index);
CREATE INDEX idx_chunks_relevance ON chunks(relevance_score DESC);
CREATE INDEX idx_chunks_ctr ON chunks(click_through_rate DESC);
CREATE INDEX idx_chunks_retrieval_count ON chunks(retrieval_count DESC);
CREATE INDEX idx_chunks_created_at ON chunks(created_at DESC);

-- Vector similarity index for chunks
CREATE INDEX idx_chunks_embedding ON chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Search outcomes indexes
CREATE INDEX idx_search_outcomes_query_id ON search_outcomes(query_id);
CREATE INDEX idx_search_outcomes_strategy ON search_outcomes(search_strategy);
CREATE INDEX idx_search_outcomes_satisfaction ON search_outcomes(user_satisfaction DESC);
CREATE INDEX idx_search_outcomes_conversion ON search_outcomes(conversion_achieved);
CREATE INDEX idx_search_outcomes_created_at ON search_outcomes(created_at DESC);
CREATE INDEX idx_search_outcomes_response_time ON search_outcomes(response_time_ms);

-- Agent performance indexes
CREATE INDEX idx_agent_performance_agent_name ON agent_performance(agent_name);
CREATE INDEX idx_agent_performance_task_type ON agent_performance(task_type);
CREATE INDEX idx_agent_performance_success_rate ON agent_performance(success_rate DESC);
CREATE INDEX idx_agent_performance_period ON agent_performance(measurement_period_start DESC);

-- System metrics indexes
CREATE INDEX idx_system_metrics_measurement_start ON system_metrics(measurement_start DESC);
CREATE INDEX idx_system_metrics_performance_trend ON system_metrics(performance_trend DESC);

-- Create optimized search functions
-- Vector similarity search with outcome weighting
CREATE OR REPLACE FUNCTION search_chunks_weighted(
    query_embedding vector(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INTEGER DEFAULT 10,
    boost_performance BOOLEAN DEFAULT TRUE
) RETURNS TABLE (
    id UUID,
    content TEXT,
    similarity FLOAT,
    performance_score FLOAT,
    final_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.content,
        1 - (c.embedding <=> query_embedding) as similarity,
        CASE 
            WHEN boost_performance THEN 
                (c.relevance_score * 0.3 + c.click_through_rate * 0.4 + c.confidence_score * 0.3)
            ELSE 0.0
        END as performance_score,
        CASE 
            WHEN boost_performance THEN
                (1 - (c.embedding <=> query_embedding)) * 0.7 + 
                (c.relevance_score * 0.3 + c.click_through_rate * 0.4 + c.confidence_score * 0.3) * 0.3
            ELSE (1 - (c.embedding <=> query_embedding))
        END as final_score
    FROM chunks c
    WHERE 1 - (c.embedding <=> query_embedding) > match_threshold
    ORDER BY final_score DESC
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Hybrid search function combining vector and text search
CREATE OR REPLACE FUNCTION hybrid_search(
    query_embedding vector(1536),
    query_text TEXT,
    match_threshold FLOAT DEFAULT 0.5,
    match_count INTEGER DEFAULT 10
) RETURNS TABLE (
    id UUID,
    content TEXT,
    vector_score FLOAT,
    text_score FLOAT,
    hybrid_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.content,
        1 - (c.embedding <=> query_embedding) as vector_score,
        ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', query_text)) as text_score,
        (1 - (c.embedding <=> query_embedding)) * 0.7 + 
        ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', query_text)) * 0.3 as hybrid_score
    FROM chunks c
    WHERE 
        (1 - (c.embedding <=> query_embedding) > match_threshold OR
         to_tsvector('english', c.content) @@ plainto_tsquery('english', query_text))
    ORDER BY hybrid_score DESC
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Performance analytics function
CREATE OR REPLACE FUNCTION analyze_search_performance(
    time_window_days INTEGER DEFAULT 7
) RETURNS TABLE (
    search_strategy VARCHAR(50),
    avg_satisfaction FLOAT,
    avg_response_time FLOAT,
    conversion_rate FLOAT,
    total_searches BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        so.search_strategy,
        AVG(so.user_satisfaction::FLOAT) as avg_satisfaction,
        AVG(so.response_time_ms) as avg_response_time,
        AVG(CASE WHEN so.conversion_achieved THEN 1.0 ELSE 0.0 END) as conversion_rate,
        COUNT(*) as total_searches
    FROM search_outcomes so
    WHERE so.created_at >= NOW() - INTERVAL '%s days'
    GROUP BY so.search_strategy
    ORDER BY avg_satisfaction DESC;
END;
$$ LANGUAGE plpgsql;

-- Database maintenance function
CREATE OR REPLACE FUNCTION maintain_database() RETURNS VOID AS $$
BEGIN
    -- Update document engagement scores
    UPDATE documents 
    SET engagement_score = (
        SELECT COALESCE(AVG(relevance_score), 0.0)
        FROM chunks 
        WHERE chunks.document_id = documents.id
    );
    
    -- Update document updated_at timestamp
    UPDATE documents 
    SET updated_at = NOW()
    WHERE id IN (
        SELECT DISTINCT document_id 
        FROM chunks 
        WHERE last_retrieved > documents.updated_at
    );
    
    -- Clean up old search outcomes (keep last 30 days)
    DELETE FROM search_outcomes 
    WHERE created_at < NOW() - INTERVAL '30 days';
    
    -- Update chunk performance metrics
    UPDATE chunks 
    SET confidence_score = LEAST(
        relevance_score * 0.4 + 
        click_through_rate * 0.6,
        1.0
    )
    WHERE relevance_score > 0 OR click_through_rate > 0;
    
    -- Update statistics
    ANALYZE documents;
    ANALYZE chunks;
    ANALYZE search_outcomes;
END;
$$ LANGUAGE plpgsql;

-- Vector index optimization function
CREATE OR REPLACE FUNCTION optimize_vector_indexes() RETURNS VOID AS $$
BEGIN
    -- Analyze table statistics
    ANALYZE chunks;
    ANALYZE documents;
    
    -- Note: Index rebuilding should be done during maintenance windows
    -- REINDEX INDEX CONCURRENTLY idx_chunks_embedding;
    -- REINDEX INDEX CONCURRENTLY idx_documents_content_vector;
    
    -- Log optimization completion
    INSERT INTO system_metrics (
        measurement_start,
        measurement_end,
        learning_iterations_completed,
        performance_improvements_applied
    ) VALUES (
        NOW() - INTERVAL '1 minute',
        NOW(),
        1,
        1
    );
END;
$$ LANGUAGE plpgsql;

-- Create update triggers for timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update triggers
CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create table-level comments for documentation
COMMENT ON TABLE documents IS 'Main documents table with vector embeddings and performance tracking';
COMMENT ON TABLE chunks IS 'Document chunks with embeddings and retrieval optimization';
COMMENT ON TABLE search_outcomes IS 'Search outcomes for learning and optimization';
COMMENT ON TABLE agent_performance IS 'Agent performance tracking and metrics';
COMMENT ON TABLE system_metrics IS 'System-wide performance and health metrics';

-- Create initial system metrics record
INSERT INTO system_metrics (
    measurement_start,
    measurement_end,
    total_queries_processed,
    search_accuracy,
    user_satisfaction_score
) VALUES (
    NOW(),
    NOW(),
    0,
    0.0,
    0.0
);

-- Success message
SELECT 'Neon PostgreSQL database setup completed successfully!' as status;