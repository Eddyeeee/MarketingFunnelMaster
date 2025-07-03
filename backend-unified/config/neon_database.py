#!/usr/bin/env python3
"""
Neon PostgreSQL Configuration for Agentic RAG Implementation
Replaces Supabase with Neon for pgvector support and better performance

Executor: Claude Code
Erstellt: 2025-07-03 - Milestone 1C Week 1 Day 1
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text, MetaData
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator, Optional
import os
from dataclasses import dataclass

from .settings import settings

logger = logging.getLogger(__name__)

@dataclass
class NeonConfig:
    """Neon PostgreSQL configuration"""
    
    # Neon connection details
    host: str = "ep-empire-rag.eu-central-1.aws.neon.tech"
    database: str = "empire_rag_db"
    username: str = "empire_user"
    password: str = ""  # To be set from environment
    port: int = 5432
    
    # Connection pool settings
    pool_size: int = 20
    max_overflow: int = 30
    pool_timeout: int = 30
    pool_recycle: int = 3600  # 1 hour
    pool_pre_ping: bool = True
    
    # Performance settings
    echo: bool = False  # Set to True for debugging
    echo_pool: bool = False
    
    # SSL settings for Neon
    sslmode: str = "require"
    
    def get_database_url(self) -> str:
        """Generate Neon PostgreSQL connection URL"""
        password = self.password or os.getenv("NEON_DATABASE_PASSWORD", "")
        
        if not password:
            logger.warning("⚠️ NEON_DATABASE_PASSWORD not set, using placeholder")
            password = "placeholder-password"
        
        return (
            f"postgresql+asyncpg://{self.username}:{password}@"
            f"{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}"
        )
    
    def get_sync_database_url(self) -> str:
        """Generate synchronous connection URL for migrations"""
        password = self.password or os.getenv("NEON_DATABASE_PASSWORD", "")
        
        if not password:
            password = "placeholder-password"
        
        return (
            f"postgresql://{self.username}:{password}@"
            f"{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}"
        )

# Global configuration
neon_config = NeonConfig()

# Database engines
neon_engine: Optional[object] = None
neon_sync_engine: Optional[object] = None

# Session makers
AsyncSessionLocal: Optional[async_sessionmaker] = None

# Base class for SQLAlchemy models with pgvector support
Base = declarative_base()

# Metadata for schema management
metadata = MetaData()

async def init_neon_database():
    """Initialize Neon PostgreSQL database with pgvector"""
    global neon_engine, neon_sync_engine, AsyncSessionLocal
    
    logger.info("🚀 Initializing Neon PostgreSQL with pgvector...")
    
    try:
        # Create async engine for Neon
        database_url = neon_config.get_database_url()
        logger.info(f"📊 Connecting to Neon: {neon_config.host}")
        
        neon_engine = create_async_engine(
            database_url,
            pool_size=neon_config.pool_size,
            max_overflow=neon_config.max_overflow,
            pool_timeout=neon_config.pool_timeout,
            pool_recycle=neon_config.pool_recycle,
            pool_pre_ping=neon_config.pool_pre_ping,
            echo=neon_config.echo,
            echo_pool=neon_config.echo_pool,
            future=True,
            # Neon-specific optimizations
            connect_args={
                "server_settings": {
                    "jit": "off",  # Disable JIT for better predictable performance
                    "application_name": "MarketingFunnelMaster_AgenticRAG"
                }
            }
        )
        
        # Create sync engine for migrations and schema operations
        sync_url = neon_config.get_sync_database_url()
        neon_sync_engine = create_engine(
            sync_url,
            pool_size=10,
            max_overflow=20,
            echo=neon_config.echo,
            future=True
        )
        
        # Create async session maker
        AsyncSessionLocal = async_sessionmaker(
            neon_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False
        )
        
        # Test connection and install extensions
        await test_neon_connection()
        await install_pgvector_extension()
        
        logger.info("✅ Neon PostgreSQL connection established with pgvector")
        
    except Exception as e:
        logger.error(f"❌ Neon database initialization failed: {e}")
        raise

async def install_pgvector_extension():
    """Install and configure pgvector extension"""
    logger.info("🔧 Installing pgvector extension...")
    
    try:
        async with neon_engine.begin() as conn:
            # Check if pgvector is already installed
            result = await conn.execute(text(
                "SELECT 1 FROM pg_extension WHERE extname = 'vector'"
            ))
            
            if not result.fetchone():
                # Install pgvector extension
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                logger.info("✅ pgvector extension installed")
            else:
                logger.info("✅ pgvector extension already installed")
            
            # Install uuid-ossp for UUID generation
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            logger.info("✅ uuid-ossp extension verified")
            
    except Exception as e:
        logger.error(f"❌ Failed to install pgvector: {e}")
        raise

async def test_neon_connection() -> bool:
    """Test Neon PostgreSQL connection"""
    try:
        async with neon_engine.begin() as conn:
            # Test basic connection
            await conn.execute(text("SELECT 1"))
            
            # Test pgvector availability
            await conn.execute(text("SELECT '[1,2,3]'::vector"))
            
            # Get connection info
            result = await conn.execute(text(
                "SELECT version(), current_database(), current_user"
            ))
            version_info = result.fetchone()
            
            logger.info(f"✅ Neon connection successful")
            logger.info(f"📊 Database: {version_info[1]}, User: {version_info[2]}")
            logger.info(f"🔧 Version: {version_info[0][:50]}...")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Neon connection test failed: {e}")
        return False

async def create_agentic_rag_schema():
    """Create the Agentic RAG database schema"""
    logger.info("🗄️ Creating Agentic RAG schema...")
    
    try:
        async with neon_engine.begin() as conn:
            # Create agent_performance_metrics table
            await conn.execute(text("""
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
                )
            """))
            
            # Create empire_embeddings table with pgvector
            await conn.execute(text("""
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
                )
            """))
            
            # Create niche_performance table
            await conn.execute(text("""
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
                )
            """))
            
            # Create indexes for performance
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_empire_embeddings_vector 
                ON empire_embeddings USING ivfflat (embedding vector_cosine_ops) 
                WITH (lists = 100)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_empire_embeddings_niche 
                ON empire_embeddings (niche_category)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_empire_embeddings_persona 
                ON empire_embeddings (target_persona, device_optimization)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_agent_performance_agent_id 
                ON agent_performance_metrics (agent_id, created_at)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_niche_performance_category 
                ON niche_performance (niche_category, time_period_start)
            """))
            
        logger.info("✅ Agentic RAG schema created successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to create Agentic RAG schema: {e}")
        raise

async def insert_sample_data():
    """Insert sample data for testing"""
    logger.info("📝 Inserting sample data...")
    
    try:
        async with get_neon_session() as session:
            # Sample agent performance metric
            await session.execute(text("""
                INSERT INTO agent_performance_metrics 
                (agent_id, task_type, execution_time_ms, success_rate, quality_score, 
                 engagement_score, conversion_rate, context_data)
                VALUES 
                ('BusinessManagerAgent', 'strategic_analysis', 1250, 0.95, 0.88, 
                 0.72, 0.045, '{"query_type": "market_opportunity", "complexity": 3}')
                ON CONFLICT DO NOTHING
            """))
            
            # Sample embedding (with placeholder vector)
            await session.execute(text("""
                INSERT INTO empire_embeddings 
                (content_id, content_type, title, content, niche_category, 
                 target_persona, device_optimization, embedding, engagement_score)
                VALUES 
                ('test_001', 'market_analysis', 'AI Tools Market Analysis', 
                 'Comprehensive analysis of AI tools market trends...', 'ai_tools',
                 'tech_early_adopter', 'desktop', array_fill(0.1, ARRAY[1536])::vector,
                 0.78)
                ON CONFLICT DO NOTHING
            """))
            
            # Sample niche performance
            await session.execute(text("""
                INSERT INTO niche_performance 
                (niche_category, domain, retrieval_accuracy, response_relevance,
                 traffic_growth, conversion_improvement, time_period_start, time_period_end)
                VALUES 
                ('ai_tools', 'aicreativelab.com', 0.89, 0.92, 0.23, 0.15,
                 CURRENT_TIMESTAMP - INTERVAL '7 days', CURRENT_TIMESTAMP)
                ON CONFLICT DO NOTHING
            """))
            
            await session.commit()
            
        logger.info("✅ Sample data inserted successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to insert sample data: {e}")
        raise

@asynccontextmanager
async def get_neon_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for Neon PostgreSQL"""
    if not AsyncSessionLocal:
        raise RuntimeError("Neon database not initialized. Call init_neon_database() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def close_neon_database():
    """Close Neon PostgreSQL connections"""
    global neon_engine, neon_sync_engine
    
    logger.info("🔌 Closing Neon database connections...")
    
    try:
        if neon_engine:
            await neon_engine.dispose()
            logger.info("✅ Neon async engine disposed")
        
        if neon_sync_engine:
            neon_sync_engine.dispose()
            logger.info("✅ Neon sync engine disposed")
        
        logger.info("✅ All Neon connections closed")
        
    except Exception as e:
        logger.error(f"❌ Error closing Neon connections: {e}")

async def get_neon_performance_metrics():
    """Get current Neon database performance metrics"""
    try:
        async with get_neon_session() as session:
            # Check connection count
            result = await session.execute(text(
                "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()"
            ))
            connection_count = result.scalar()
            
            # Check database size
            result = await session.execute(text(
                "SELECT pg_size_pretty(pg_database_size(current_database()))"
            ))
            database_size = result.scalar()
            
            # Check pgvector status
            result = await session.execute(text(
                "SELECT count(*) FROM empire_embeddings"
            ))
            embedding_count = result.scalar()
            
            metrics = {
                "connection_count": connection_count,
                "database_size": database_size,
                "embedding_count": embedding_count,
                "status": "healthy"
            }
            
            logger.info(f"📊 Neon Performance: {metrics}")
            return metrics
            
    except Exception as e:
        logger.error(f"❌ Failed to get performance metrics: {e}")
        return {"status": "error", "error": str(e)}

class NeonDatabaseManager:
    """Database manager specifically for Neon PostgreSQL"""
    
    def __init__(self):
        self.engine = None
        self.session_maker = None
        self.config = neon_config
    
    async def initialize(self):
        """Initialize Neon database manager"""
        await init_neon_database()
        self.engine = neon_engine
        self.session_maker = AsyncSessionLocal
        
        # Create schema if it doesn't exist
        await create_agentic_rag_schema()
        
        # Insert sample data for testing
        await insert_sample_data()
        
        logger.info("✅ NeonDatabaseManager initialized successfully")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        async with get_neon_session() as session:
            yield session
    
    async def execute_vector_query(self, query_vector: list, limit: int = 10):
        """Execute vector similarity search"""
        try:
            async with get_neon_session() as session:
                # Convert Python list to PostgreSQL vector format
                vector_str = f"[{','.join(map(str, query_vector))}]"
                
                result = await session.execute(text(f"""
                    SELECT content_id, title, content, niche_category,
                           embedding <-> '{vector_str}'::vector as distance
                    FROM empire_embeddings
                    ORDER BY embedding <-> '{vector_str}'::vector
                    LIMIT {limit}
                """))
                
                return result.fetchall()
                
        except Exception as e:
            logger.error(f"❌ Vector query failed: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check Neon database health"""
        return await test_neon_connection()

# Global Neon database manager instance
neon_db_manager = NeonDatabaseManager()

# Export main components
__all__ = [
    "NeonConfig",
    "neon_config", 
    "init_neon_database",
    "close_neon_database",
    "get_neon_session",
    "test_neon_connection",
    "create_agentic_rag_schema",
    "NeonDatabaseManager",
    "neon_db_manager",
    "get_neon_performance_metrics"
]