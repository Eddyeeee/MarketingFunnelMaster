# TEC-spec-NeonDatabaseSetup-v1.md
# Neon PostgreSQL + pgvector Configuration for Agentic RAG

## Overview
This specification defines the Neon PostgreSQL database setup with pgvector extension for the Agentic RAG system, optimized for outcome-driven learning and high-performance vector operations.

## Database Architecture

### Connection Configuration
```python
# Database connection settings
DATABASE_CONFIG = {
    "host": "ep-xxx-xxx.us-east-1.aws.neon.tech",
    "port": 5432,
    "database": "marketing_funnel_rag",
    "user": "neon_user",
    "password": "${NEON_PASSWORD}",
    "sslmode": "require",
    "options": "-c statement_timeout=30s"
}

# Connection pooling
POOL_CONFIG = {
    "min_size": 5,
    "max_size": 20,
    "command_timeout": 60,
    "server_settings": {
        "application_name": "marketing_funnel_rag",
        "jit": "off"
    }
}
```

### Core Database Schema

#### 1. Documents Table
```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table for source content
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50) DEFAULT 'text',
    metadata JSONB DEFAULT '{}',
    
    -- Outcome tracking fields
    engagement_score FLOAT DEFAULT 0.0,
    conversion_rate FLOAT DEFAULT 0.0,
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    
    -- Temporal tracking
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Search optimization
    content_vector vector(1536) -- OpenAI embedding dimension
);

-- Indexes for performance
CREATE INDEX idx_documents_source ON documents(source);
CREATE INDEX idx_documents_content_type ON documents(content_type);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);
CREATE INDEX idx_documents_engagement ON documents(engagement_score DESC);
CREATE INDEX idx_documents_conversion ON documents(conversion_rate DESC);

-- Vector similarity search index (HNSW for production)
CREATE INDEX idx_documents_content_vector ON documents 
USING hnsw (content_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

#### 2. Chunks Table
```sql
-- Chunks table for semantic segmentation
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),
    
    -- Chunk metadata
    chunk_index INTEGER NOT NULL,
    token_count INTEGER,
    overlap_tokens INTEGER DEFAULT 0,
    
    -- Performance metrics
    relevance_score FLOAT DEFAULT 0.0,
    click_through_rate FLOAT DEFAULT 0.0,
    dwell_time_seconds FLOAT DEFAULT 0.0,
    
    -- Learning signals
    user_feedback_score FLOAT,
    confidence_score FLOAT DEFAULT 0.0,
    
    -- Temporal data
    created_at TIMESTAMP DEFAULT NOW(),
    last_retrieved TIMESTAMP,
    retrieval_count INTEGER DEFAULT 0,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Performance indexes
CREATE INDEX idx_chunks_document_id ON chunks(document_id);
CREATE INDEX idx_chunks_chunk_index ON chunks(chunk_index);
CREATE INDEX idx_chunks_relevance ON chunks(relevance_score DESC);
CREATE INDEX idx_chunks_ctr ON chunks(click_through_rate DESC);
CREATE INDEX idx_chunks_retrieval_count ON chunks(retrieval_count DESC);

-- Vector similarity index
CREATE INDEX idx_chunks_embedding ON chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

#### 3. Search Outcomes Table
```sql
-- Search outcomes for learning optimization
CREATE TABLE search_outcomes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id UUID NOT NULL,
    query_text TEXT NOT NULL,
    
    -- Search strategy used
    search_strategy VARCHAR(50) NOT NULL, -- 'vector', 'hybrid', 'graph'
    
    -- Results metadata
    results_count INTEGER NOT NULL,
    top_chunk_ids UUID[],
    relevance_scores FLOAT[],
    
    -- Performance metrics
    response_time_ms FLOAT NOT NULL,
    total_tokens INTEGER,
    
    -- User interaction data
    user_satisfaction INTEGER, -- 1-5 scale
    clicked_results INTEGER[],
    session_id UUID,
    
    -- Learning signals
    conversion_achieved BOOLEAN DEFAULT FALSE,
    downstream_actions TEXT[],
    
    -- Temporal data
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Additional metadata
    metadata JSONB DEFAULT '{}'
);

-- Analytics indexes
CREATE INDEX idx_search_outcomes_query_id ON search_outcomes(query_id);
CREATE INDEX idx_search_outcomes_strategy ON search_outcomes(search_strategy);
CREATE INDEX idx_search_outcomes_satisfaction ON search_outcomes(user_satisfaction DESC);
CREATE INDEX idx_search_outcomes_conversion ON search_outcomes(conversion_achieved);
CREATE INDEX idx_search_outcomes_created_at ON search_outcomes(created_at DESC);
```

#### 4. Agent Performance Table
```sql
-- Agent performance tracking
CREATE TABLE agent_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_name VARCHAR(100) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    
    -- Performance metrics
    success_rate FLOAT DEFAULT 0.0,
    average_response_time_ms FLOAT DEFAULT 0.0,
    confidence_calibration FLOAT DEFAULT 0.0,
    
    -- Learning metrics
    improvement_rate FLOAT DEFAULT 0.0,
    error_patterns JSONB DEFAULT '{}',
    
    -- Temporal tracking
    measurement_period_start TIMESTAMP NOT NULL,
    measurement_period_end TIMESTAMP NOT NULL,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Performance indexes
CREATE INDEX idx_agent_performance_agent_name ON agent_performance(agent_name);
CREATE INDEX idx_agent_performance_task_type ON agent_performance(task_type);
CREATE INDEX idx_agent_performance_success_rate ON agent_performance(success_rate DESC);
CREATE INDEX idx_agent_performance_period ON agent_performance(measurement_period_start DESC);
```

## Optimized Search Functions

### 1. Vector Similarity Search
```sql
-- Optimized vector similarity search with outcome weighting
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
```

### 2. Hybrid Search Function
```sql
-- Hybrid search combining vector similarity and text search
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
```

### 3. Performance Analytics Function
```sql
-- Analyze search performance patterns
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
```

## Connection Management

### AsyncPG Connection Pool
```python
import asyncpg
from typing import Optional
import logging

class NeonDatabasePool:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                host=DATABASE_CONFIG["host"],
                port=DATABASE_CONFIG["port"],
                database=DATABASE_CONFIG["database"],
                user=DATABASE_CONFIG["user"],
                password=DATABASE_CONFIG["password"],
                ssl=DATABASE_CONFIG["sslmode"],
                min_size=POOL_CONFIG["min_size"],
                max_size=POOL_CONFIG["max_size"],
                command_timeout=POOL_CONFIG["command_timeout"],
                server_settings=POOL_CONFIG["server_settings"]
            )
            self.logger.info("Database pool initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            await self.initialize()
        return self.pool.acquire()
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.logger.info("Database pool closed")
```

## Performance Optimization

### 1. Vector Index Optimization
```sql
-- Monitor vector index performance
CREATE OR REPLACE FUNCTION optimize_vector_indexes() RETURNS VOID AS $$
BEGIN
    -- Analyze table statistics
    ANALYZE chunks;
    ANALYZE documents;
    
    -- Rebuild indexes if needed (during maintenance windows)
    -- REINDEX INDEX CONCURRENTLY idx_chunks_embedding;
    -- REINDEX INDEX CONCURRENTLY idx_documents_content_vector;
END;
$$ LANGUAGE plpgsql;
```

### 2. Automated Maintenance
```sql
-- Automated maintenance function
CREATE OR REPLACE FUNCTION maintain_database() RETURNS VOID AS $$
BEGIN
    -- Update document engagement scores
    UPDATE documents 
    SET engagement_score = (
        SELECT AVG(relevance_score) 
        FROM chunks 
        WHERE chunks.document_id = documents.id
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
    );
END;
$$ LANGUAGE plpgsql;
```

## Monitoring and Observability

### Health Check Function
```python
async def database_health_check(pool: asyncpg.Pool) -> dict:
    """Check database health and performance"""
    try:
        async with pool.acquire() as conn:
            # Check connection
            await conn.execute("SELECT 1")
            
            # Check vector extension
            result = await conn.fetchrow(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
            )
            
            # Check table sizes
            table_sizes = await conn.fetch("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            
            return {
                "status": "healthy",
                "vector_extension": result["exists"],
                "table_sizes": dict(table_sizes),
                "timestamp": datetime.now()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now()
        }
```

## Environment Configuration

### Environment Variables
```bash
# Neon Database Configuration
NEON_PASSWORD=your_secure_password
DATABASE_URL=postgresql://neon_user:${NEON_PASSWORD}@ep-xxx-xxx.us-east-1.aws.neon.tech/marketing_funnel_rag?sslmode=require

# Performance Tuning
PGVECTOR_HNSW_M=16
PGVECTOR_HNSW_EF_CONSTRUCTION=64
PGVECTOR_HNSW_EF_SEARCH=32

# Connection Pool Settings
DB_MIN_CONNECTIONS=5
DB_MAX_CONNECTIONS=20
DB_COMMAND_TIMEOUT=60

# Monitoring
ENABLE_QUERY_LOGGING=true
SLOW_QUERY_THRESHOLD_MS=1000
```

This specification provides a comprehensive foundation for the Neon PostgreSQL + pgvector setup, optimized for outcome-driven learning and high-performance vector operations in the Agentic RAG system.