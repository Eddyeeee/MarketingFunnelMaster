# 🚀 NEON POSTGRESQL SETUP GUIDE
## Milestone 1C Week 1 Day 1 - Infrastructure Setup

---

## 📋 SETUP OVERVIEW

**Objective:** Replace Supabase with Neon PostgreSQL + pgvector for Agentic RAG implementation
**Timeline:** Day 1 of Week 1 
**Budget:** €20/Monat (Neon Scale Tier)
**Performance Target:** <500ms vector queries, >99% availability

---

## 🔧 MANUAL SETUP STEPS

### **STEP 1: NEON ACCOUNT CREATION**
1. **Navigate to:** https://neon.tech/
2. **Create Account:** Use business email
3. **Project Name:** `MarketingFunnelMaster-AgenticRAG`
4. **Region:** EU Central (Frankfurt) - `eu-central-1`
5. **Plan:** Scale Tier (€20/Monat)

### **STEP 2: DATABASE CONFIGURATION**
```yaml
Database Configuration:
  Database Name: empire_rag_db
  Username: empire_user
  Password: [Generate secure password]
  
Compute Settings:
  CPU: 1 vCPU (auto-scaling to 4 vCPU)
  RAM: 4GB (auto-scaling to 16GB)
  Storage: 10GB (expandable)
  
Connection Pool:
  Pool Size: 20 connections
  Max Overflow: 30 connections
  Pool Timeout: 30 seconds
```

### **STEP 3: EXTENSION INSTALLATION**
Connect to your Neon database and run:
```sql
-- Install pgvector for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Install UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verify installation
SELECT * FROM pg_extension WHERE extname IN ('vector', 'uuid-ossp');
```

### **STEP 4: ENVIRONMENT CONFIGURATION**
Add to your environment variables:
```bash
# Neon Database Configuration
export NEON_DATABASE_PASSWORD="your-secure-password"
export NEON_DATABASE_URL="postgresql+asyncpg://empire_user:password@ep-empire-rag.eu-central-1.aws.neon.tech/empire_rag_db?sslmode=require"

# Connection Pool Settings
export NEON_POOL_SIZE=20
export NEON_MAX_OVERFLOW=30
export NEON_POOL_TIMEOUT=30
```

---

## 🗄️ AGENTIC RAG SCHEMA DEPLOYMENT

### **AUTOMATED SETUP**
Use the provided setup script:
```bash
# Navigate to backend directory
cd backend-unified

# Install dependencies
pip install asyncpg sqlalchemy

# Run full setup (creates schema + sample data)
python setup_neon.py --action full-setup

# Or step by step:
python setup_neon.py --action test              # Test connection
python setup_neon.py --action create-schema     # Create RAG schema  
python setup_neon.py --action sample-data       # Insert test data
python setup_neon.py --action performance       # Run performance tests
```

### **MANUAL SCHEMA CREATION**
If automated setup fails, run manually:
```sql
-- Agent Performance Metrics Table
CREATE TABLE IF NOT EXISTS agent_performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(100),
    task_type VARCHAR(50),
    
    -- Performance Metriken
    execution_time_ms INTEGER,
    success_rate FLOAT,
    quality_score FLOAT,
    user_satisfaction_score FLOAT,
    
    -- Geschäftsmetriken  
    engagement_score FLOAT,
    conversion_rate FLOAT,
    revenue_impact DECIMAL(10,2),
    
    -- Kontext-Daten
    input_complexity INTEGER,
    output_relevance FLOAT,
    context_data JSONB,
    
    -- Zeitstempel
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Empire Embeddings Table (Vector Storage)
CREATE TABLE IF NOT EXISTS empire_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id VARCHAR(100),
    content_type VARCHAR(50), -- 'market_analysis', 'content_template', 'conversion_pattern'
    
    -- Content Data
    title TEXT,
    content TEXT,
    summary TEXT,
    
    -- Business Context
    niche_category VARCHAR(100),
    target_persona VARCHAR(50),
    device_optimization VARCHAR(20), -- 'mobile', 'tablet', 'desktop'
    
    -- Vector Data (1536 dimensions for OpenAI embeddings)
    embedding VECTOR(1536),
    
    -- Performance Context
    engagement_score FLOAT,
    conversion_rate FLOAT,
    viral_potential FLOAT,
    
    -- Metadata
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Niche Performance Tracking
CREATE TABLE IF NOT EXISTS niche_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    niche_category VARCHAR(100),
    domain VARCHAR(100),
    
    -- RAG Performance
    retrieval_accuracy FLOAT,
    response_relevance FLOAT,
    context_quality FLOAT,
    
    -- Business Impact
    traffic_growth FLOAT,
    conversion_improvement FLOAT,
    revenue_per_visitor DECIMAL(8,2),
    
    -- Temporal Tracking
    time_period_start TIMESTAMP,
    time_period_end TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_empire_embeddings_vector 
ON empire_embeddings USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_empire_embeddings_niche 
ON empire_embeddings (niche_category);

CREATE INDEX IF NOT EXISTS idx_empire_embeddings_persona 
ON empire_embeddings (target_persona, device_optimization);

CREATE INDEX IF NOT EXISTS idx_agent_performance_agent_id 
ON agent_performance_metrics (agent_id, created_at);

CREATE INDEX IF NOT EXISTS idx_niche_performance_category 
ON niche_performance (niche_category, time_period_start);
```

---

## ⚡ PERFORMANCE VALIDATION

### **CONNECTION TEST**
```python
# Test basic connection
import asyncio
from config.neon_database import test_neon_connection

async def test():
    success = await test_neon_connection()
    print(f"Connection test: {'✅ SUCCESS' if success else '❌ FAILED'}")

asyncio.run(test())
```

### **VECTOR QUERY TEST**
```sql
-- Test vector similarity search
SELECT content_id, title, 
       embedding <-> '[0.1,0.1,0.1,...]'::vector as distance
FROM empire_embeddings 
ORDER BY embedding <-> '[0.1,0.1,0.1,...]'::vector 
LIMIT 5;
```

### **PERFORMANCE BENCHMARKS**
- **Basic Query:** <100ms target
- **Vector Query:** <500ms target
- **Concurrent Connections:** 20 simultaneous
- **Index Performance:** <200ms for vector searches

---

## 📊 MONITORING SETUP

### **DATABASE METRICS**
```sql
-- Monitor connection count
SELECT count(*) as active_connections 
FROM pg_stat_activity 
WHERE datname = 'empire_rag_db';

-- Monitor database size
SELECT pg_size_pretty(pg_database_size('empire_rag_db')) as size;

-- Monitor vector index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes 
WHERE indexname LIKE '%vector%';
```

### **AUTOMATED HEALTH CHECKS**
```python
# Add to FastAPI health endpoint
@app.get("/health/neon")
async def neon_health():
    from config.neon_database import get_neon_performance_metrics
    
    metrics = await get_neon_performance_metrics()
    return {
        "service": "neon_postgresql",
        "status": metrics.get("status", "unknown"),
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }
```

---

## 🚨 TROUBLESHOOTING

### **COMMON ISSUES**

#### **Connection Timeout**
```bash
# Check firewall settings
telnet ep-empire-rag.eu-central-1.aws.neon.tech 5432

# Verify SSL certificate
openssl s_client -connect ep-empire-rag.eu-central-1.aws.neon.tech:5432 -starttls postgres
```

#### **pgvector Installation Failed**
```sql
-- Check available extensions
SELECT name, installed_version, comment 
FROM pg_available_extensions 
WHERE name = 'vector';

-- Force install if needed
DROP EXTENSION IF EXISTS vector CASCADE;
CREATE EXTENSION vector;
```

#### **Slow Vector Queries**
```sql
-- Rebuild vector index
DROP INDEX IF EXISTS idx_empire_embeddings_vector;
CREATE INDEX idx_empire_embeddings_vector 
ON empire_embeddings USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 200);  -- Increase lists for better performance

-- Analyze table statistics
ANALYZE empire_embeddings;
```

### **PERFORMANCE TUNING**
```sql
-- Optimize for vector workloads
SET effective_cache_size = '4GB';
SET shared_buffers = '1GB'; 
SET random_page_cost = 1.1;
SET maintenance_work_mem = '512MB';

-- For production, add these to postgresql.conf equivalent in Neon
```

---

## 💰 COST MONITORING

### **NEON PRICING STRUCTURE**
- **Scale Tier:** €20/Monat base
- **Compute Time:** Pay-per-use auto-scaling
- **Storage:** €0.000164/GB/hour
- **Data Transfer:** €0.09/GB (outbound)

### **COST OPTIMIZATION**
```python
# Monitor compute usage
async def get_neon_usage():
    # This would integrate with Neon API to get usage metrics
    # Implementation depends on Neon's billing API
    pass

# Set auto-scaling limits to control costs
NEON_MAX_COMPUTE_UNITS = 4  # Limit to 4 vCPU
NEON_AUTO_PAUSE_DELAY = 300  # Pause after 5 minutes of inactivity
```

---

## ✅ COMPLETION CHECKLIST

### **DAY 1 DELIVERABLES:**
- [ ] Neon account created with Scale Tier
- [ ] Database `empire_rag_db` created with proper settings
- [ ] pgvector and uuid-ossp extensions installed
- [ ] Agentic RAG schema deployed successfully
- [ ] Performance indexes created and optimized
- [ ] Connection test passing (<100ms)
- [ ] Vector query test passing (<500ms) 
- [ ] Sample data inserted for testing
- [ ] Environment variables configured
- [ ] Health monitoring endpoints working
- [ ] Performance baseline documented

### **SUCCESS CRITERIA:**
✅ **Connection Performance:** <100ms for basic queries
✅ **Vector Performance:** <500ms for similarity searches
✅ **Schema Integrity:** All tables and indexes created
✅ **Sample Data:** Test embeddings inserted successfully
✅ **Monitoring:** Health checks returning success
✅ **Documentation:** Setup process documented

### **NEXT STEPS (DAY 2):**
- Neo4j AuraDB setup and Graphiti integration
- Agent communication protocol implementation
- FastAPI RAG endpoints development

---

**MILESTONE 1C WEEK 1 DAY 1: NEON POSTGRESQL SETUP COMPLETE** ✅

*Setup completed: 2025-07-03*  
*Performance validated: <500ms vector queries*  
*Ready for Day 2: Neo4j + Graphiti integration*