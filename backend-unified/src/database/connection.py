"""
Database Connection Manager for Conversion & Marketing Automation
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Manages database connections for the A/B testing and behavioral tracking systems.
"""

import asyncpg
import os
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

# Database connection pool
_pool: Optional[asyncpg.Pool] = None

async def init_database_pool():
    """Initialize the database connection pool"""
    global _pool
    
    if _pool is None:
        try:
            # Database configuration from environment variables
            database_url = os.getenv(
                "DATABASE_URL",
                "postgresql://postgres:password@localhost:5432/marketing_funnel"
            )
            
            _pool = await asyncpg.create_pool(
                database_url,
                min_size=1,
                max_size=10,
                command_timeout=60,
                server_settings={
                    'jit': 'off'  # Disable JIT for better performance on small queries
                }
            )
            
            logger.info("✅ Database connection pool initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize database pool: {e}")
            raise

async def close_database_pool():
    """Close the database connection pool"""
    global _pool
    
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("✅ Database connection pool closed")

async def get_database_connection():
    """Get a database connection from the pool"""
    global _pool
    
    if _pool is None:
        await init_database_pool()
    
    try:
        async with _pool.acquire() as connection:
            yield connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

@asynccontextmanager
async def get_db_connection():
    """Context manager for database connections"""
    global _pool
    
    if _pool is None:
        await init_database_pool()
    
    connection = None
    try:
        connection = await _pool.acquire()
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if connection:
            await _pool.release(connection)

async def execute_migration(migration_sql: str):
    """Execute a database migration"""
    async with get_db_connection() as conn:
        try:
            await conn.execute(migration_sql)
            logger.info("✅ Migration executed successfully")
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise

async def check_database_health() -> bool:
    """Check if database is healthy"""
    try:
        async with get_db_connection() as conn:
            result = await conn.fetchval("SELECT 1")
            return result == 1
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False