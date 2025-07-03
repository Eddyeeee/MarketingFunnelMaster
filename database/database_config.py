"""
Database Configuration for Agentic RAG System
Handles Neon PostgreSQL and Neo4j connections with optimized pooling
Version: 1.0.0
Created: 2025-07-03
"""

import os
import asyncio
import asyncpg
from typing import Optional, Dict, Any, List
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    # Neon PostgreSQL configuration
    neon_host: str = os.getenv("NEON_HOST", "ep-xxx-xxx.us-east-1.aws.neon.tech")
    neon_port: int = int(os.getenv("NEON_PORT", "5432"))
    neon_database: str = os.getenv("NEON_DATABASE", "marketing_funnel_rag")
    neon_user: str = os.getenv("NEON_USER", "neon_user")
    neon_password: str = os.getenv("NEON_PASSWORD", "")
    neon_sslmode: str = os.getenv("NEON_SSLMODE", "require")
    
    # Connection pool settings
    pool_min_size: int = int(os.getenv("DB_MIN_CONNECTIONS", "5"))
    pool_max_size: int = int(os.getenv("DB_MAX_CONNECTIONS", "20"))
    pool_command_timeout: int = int(os.getenv("DB_COMMAND_TIMEOUT", "60"))
    
    # Performance settings
    enable_query_logging: bool = os.getenv("ENABLE_QUERY_LOGGING", "true").lower() == "true"
    slow_query_threshold_ms: int = int(os.getenv("SLOW_QUERY_THRESHOLD_MS", "1000"))
    
    def __post_init__(self):
        if not self.neon_password:
            raise ValueError("NEON_PASSWORD environment variable is required")

class NeonDatabaseManager:
    """Manages Neon PostgreSQL connections with optimized pooling"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None
        self.is_initialized = False
        
    async def initialize(self) -> None:
        """Initialize database connection pool"""
        if self.is_initialized:
            logger.warning("Database already initialized")
            return
            
        try:
            # Connection string
            connection_string = (
                f"postgresql://{self.config.neon_user}:{self.config.neon_password}"
                f"@{self.config.neon_host}:{self.config.neon_port}"
                f"/{self.config.neon_database}?sslmode={self.config.neon_sslmode}"
            )
            
            # Create connection pool
            self.pool = await asyncpg.create_pool(
                connection_string,
                min_size=self.config.pool_min_size,
                max_size=self.config.pool_max_size,
                command_timeout=self.config.pool_command_timeout,
                server_settings={
                    "application_name": "marketing_funnel_rag",
                    "jit": "off"  # Disable JIT for consistent performance
                }
            )
            
            # Test connection and verify extensions
            await self._verify_setup()
            
            self.is_initialized = True
            logger.info(f"Database pool initialized successfully with {self.config.pool_min_size}-{self.config.pool_max_size} connections")
            
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def _verify_setup(self) -> None:
        """Verify database setup and extensions"""
        async with self.pool.acquire() as conn:
            # Check PostgreSQL version
            version = await conn.fetchrow("SELECT version()")
            logger.info(f"PostgreSQL version: {version['version']}")
            
            # Check pgvector extension
            vector_ext = await conn.fetchrow(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
            )
            if not vector_ext['exists']:
                raise RuntimeError("pgvector extension not installed")
            logger.info("pgvector extension verified")
            
            # Check required tables
            tables = await conn.fetch("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename IN ('documents', 'chunks', 'search_outcomes', 'agent_performance', 'system_metrics')
            """)
            
            required_tables = {'documents', 'chunks', 'search_outcomes', 'agent_performance', 'system_metrics'}
            existing_tables = {row['tablename'] for row in tables}
            
            if not required_tables.issubset(existing_tables):
                missing = required_tables - existing_tables
                raise RuntimeError(f"Missing required tables: {missing}")
            
            logger.info("All required tables verified")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.is_initialized:
            await self.initialize()
            
        async with self.pool.acquire() as connection:
            yield connection
    
    async def execute_query(self, query: str, *args, fetch_type: str = "none") -> Any:
        """Execute query with performance monitoring"""
        start_time = datetime.now()
        
        try:
            async with self.get_connection() as conn:
                if fetch_type == "all":
                    result = await conn.fetch(query, *args)
                elif fetch_type == "one":
                    result = await conn.fetchrow(query, *args)
                elif fetch_type == "val":
                    result = await conn.fetchval(query, *args)
                else:  # execute only
                    result = await conn.execute(query, *args)
                
                # Log slow queries
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                if execution_time > self.config.slow_query_threshold_ms:
                    logger.warning(f"Slow query ({execution_time:.2f}ms): {query[:100]}...")
                
                return result
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.error(f"Query: {query[:200]}...")
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        try:
            start_time = datetime.now()
            
            async with self.get_connection() as conn:
                # Basic connectivity test
                await conn.execute("SELECT 1")
                
                # Check connection pool status
                pool_info = {
                    "size": self.pool.get_size(),
                    "max_size": self.pool.get_max_size(),
                    "min_size": self.pool.get_min_size(),
                    "idle_connections": self.pool.get_idle_size()
                }
                
                # Check table sizes
                table_sizes = await conn.fetch("""
                    SELECT 
                        schemaname,
                        tablename,
                        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                        pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY size_bytes DESC
                """)
                
                # Check index performance
                index_stats = await conn.fetch("""
                    SELECT 
                        schemaname,
                        tablename,
                        indexname,
                        idx_scan,
                        idx_tup_read,
                        idx_tup_fetch
                    FROM pg_stat_user_indexes
                    WHERE schemaname = 'public'
                    ORDER BY idx_scan DESC
                    LIMIT 10
                """)
                
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                
                return {
                    "status": "healthy",
                    "response_time_ms": response_time,
                    "pool_info": pool_info,
                    "table_sizes": [dict(row) for row in table_sizes],
                    "top_indexes": [dict(row) for row in index_stats],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def optimize_performance(self) -> Dict[str, Any]:
        """Run performance optimization tasks"""
        try:
            async with self.get_connection() as conn:
                # Run maintenance function
                await conn.execute("SELECT maintain_database()")
                
                # Update table statistics
                await conn.execute("ANALYZE")
                
                # Check for missing indexes
                missing_indexes = await conn.fetch("""
                    SELECT 
                        schemaname,
                        tablename,
                        seq_scan,
                        seq_tup_read,
                        idx_scan,
                        idx_tup_fetch
                    FROM pg_stat_user_tables
                    WHERE schemaname = 'public'
                    AND seq_scan > idx_scan
                    ORDER BY seq_tup_read DESC
                """)
                
                return {
                    "status": "optimization_completed",
                    "maintenance_run": True,
                    "statistics_updated": True,
                    "potential_missing_indexes": [dict(row) for row in missing_indexes],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Performance optimization failed: {e}")
            return {
                "status": "optimization_failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_performance_metrics(self, time_window_days: int = 7) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        try:
            async with self.get_connection() as conn:
                # Search performance analysis
                search_performance = await conn.fetch(
                    "SELECT * FROM analyze_search_performance($1)",
                    time_window_days
                )
                
                # System metrics
                system_metrics = await conn.fetch("""
                    SELECT 
                        AVG(average_response_time_ms) as avg_response_time,
                        AVG(search_accuracy) as avg_accuracy,
                        AVG(user_satisfaction_score) as avg_satisfaction,
                        SUM(total_queries_processed) as total_queries,
                        AVG(error_rate) as avg_error_rate
                    FROM system_metrics
                    WHERE measurement_start >= NOW() - INTERVAL '%s days'
                """, time_window_days)
                
                # Database statistics
                db_stats = await conn.fetchrow("""
                    SELECT 
                        pg_database_size(current_database()) as db_size_bytes,
                        pg_size_pretty(pg_database_size(current_database())) as db_size_pretty
                """)
                
                return {
                    "search_performance": [dict(row) for row in search_performance],
                    "system_metrics": dict(system_metrics[0]) if system_metrics else {},
                    "database_size": dict(db_stats),
                    "time_window_days": time_window_days,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def close(self) -> None:
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.is_initialized = False
            logger.info("Database pool closed")

# Singleton instance
_db_config = DatabaseConfig()
db_manager = NeonDatabaseManager(_db_config)

# Helper functions for common operations
async def initialize_database():
    """Initialize database connection"""
    await db_manager.initialize()

async def get_db_connection():
    """Get database connection context manager"""
    return db_manager.get_connection()

async def execute_query(query: str, *args, fetch_type: str = "none"):
    """Execute query with the global database manager"""
    return await db_manager.execute_query(query, *args, fetch_type=fetch_type)

async def health_check():
    """Perform database health check"""
    return await db_manager.health_check()

async def close_database():
    """Close database connections"""
    await db_manager.close()

# Configuration validation
def validate_configuration():
    """Validate database configuration"""
    required_env_vars = [
        "NEON_PASSWORD"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    logger.info("Database configuration validated successfully")

if __name__ == "__main__":
    # Test the database configuration
    async def test_database():
        try:
            validate_configuration()
            await initialize_database()
            
            # Test basic operations
            health = await health_check()
            print(f"Database health: {health['status']}")
            
            # Test query execution
            result = await execute_query("SELECT NOW() as current_time", fetch_type="one")
            print(f"Current time: {result['current_time']}")
            
            await close_database()
            print("Database test completed successfully!")
            
        except Exception as e:
            print(f"Database test failed: {e}")
    
    asyncio.run(test_database())