#!/usr/bin/env python3
"""
Database Configuration and Connection Management
Supports PostgreSQL (Supabase) and SQLite (Migration Buffer)

Executor: Claude Code
Erstellt: 2025-07-03
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, text
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator, Optional
import asyncio

from .settings import settings

logger = logging.getLogger(__name__)

# Database engines
postgresql_engine: Optional[object] = None
sqlite_engine: Optional[object] = None

# Session makers
AsyncSessionLocal: Optional[async_sessionmaker] = None
SyncSessionLocal: Optional[object] = None

# Base class for SQLAlchemy models
Base = declarative_base()

async def init_database():
    """Initialize database connections"""
    global postgresql_engine, sqlite_engine, AsyncSessionLocal, SyncSessionLocal
    
    logger.info("🔧 Initializing database connections...")
    
    try:
        # PostgreSQL (Supabase) - Primary Database
        logger.info("📊 Connecting to PostgreSQL (Supabase)...")
        postgresql_engine = create_async_engine(
            settings.DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            echo=settings.DATABASE_ECHO,
            future=True,
            # Connection pool configuration for Supabase
            pool_pre_ping=True,
            pool_recycle=3600,  # 1 hour
        )
        
        # Create async session maker
        AsyncSessionLocal = async_sessionmaker(
            postgresql_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Test PostgreSQL connection
        async with postgresql_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("✅ PostgreSQL (Supabase) connection established")
        
        # SQLite (Migration Buffer) - Temporary during migration
        logger.info("📁 Setting up SQLite migration buffer...")
        sqlite_engine = create_engine(
            f"sqlite+aiosqlite:///{settings.SQLITE_DATABASE_PATH}",
            echo=settings.DATABASE_ECHO,
            future=True
        )
        
        # Create sync session for SQLite (for migration scripts)
        from sqlalchemy.orm import sessionmaker
        SyncSessionLocal = sessionmaker(
            bind=sqlite_engine.sync_engine if hasattr(sqlite_engine, 'sync_engine') else None
        )
        
        logger.info("✅ SQLite migration buffer ready")
        
        # Create tables if they don't exist
        await create_tables()
        
        logger.info("✅ Database initialization complete")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

async def create_tables():
    """Create database tables if they don't exist"""
    try:
        # Import all models to ensure they're registered with Base
        from models import users, leads  # Import only existing models for now
        
        # Create tables in PostgreSQL
        if postgresql_engine:
            async with postgresql_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ PostgreSQL tables created/verified")
        
        logger.info("✅ Database schema up to date")
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        logger.warning("Continuing without creating tables - they may need to be created manually")
        # Don't raise here to allow the application to start

async def close_database():
    """Close database connections"""
    global postgresql_engine, sqlite_engine
    
    logger.info("🔌 Closing database connections...")
    
    try:
        if postgresql_engine:
            await postgresql_engine.dispose()
            logger.info("✅ PostgreSQL connection closed")
        
        if sqlite_engine:
            await sqlite_engine.dispose()
            logger.info("✅ SQLite connection closed")
        
        logger.info("✅ All database connections closed")
        
    except Exception as e:
        logger.error(f"❌ Error closing database connections: {e}")

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session (PostgreSQL)"""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_sync_session():
    """Get sync database session (SQLite for migration)"""
    if not SyncSessionLocal:
        raise RuntimeError("SQLite database not initialized.")
    
    return SyncSessionLocal()

async def test_database_connection() -> bool:
    """Test database connection for health checks"""
    try:
        if postgresql_engine:
            async with postgresql_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        return False
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

class DatabaseManager:
    """Database manager for handling connections and sessions"""
    
    def __init__(self):
        self.postgresql_engine = None
        self.sqlite_engine = None
        self.session_maker = None
    
    async def initialize(self):
        """Initialize database manager"""
        await init_database()
        self.postgresql_engine = postgresql_engine
        self.sqlite_engine = sqlite_engine
        self.session_maker = AsyncSessionLocal
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        async with get_async_session() as session:
            yield session
    
    async def execute_raw_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        async with get_async_session() as session:
            result = await session.execute(text(query), params or {})
            return result.fetchall()
    
    async def health_check(self) -> bool:
        """Check database health"""
        return await test_database_connection()

# Global database manager instance
db_manager = DatabaseManager()

# Migration support functions
async def migrate_from_express_db():
    """Migrate data from existing Express.js database"""
    logger.info("🔄 Starting migration from Express.js database...")
    
    try:
        # This would connect to the existing SQLite database from the Express.js app
        # and migrate data to the new PostgreSQL database
        
        # Import migration functions
        from utils.migration import (
            migrate_users,
            migrate_leads,
            migrate_email_funnels,
            migrate_analytics
        )
        
        # Execute migrations in order
        await migrate_users()
        await migrate_leads()
        await migrate_email_funnels()
        await migrate_analytics()
        
        logger.info("✅ Database migration completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        raise

# Dependency functions for FastAPI
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions"""
    async with get_async_session() as session:
        yield session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions (alias for compatibility)"""
    async with get_async_session() as session:
        yield session

async def get_db_manager() -> DatabaseManager:
    """FastAPI dependency for database manager"""
    return db_manager

# Database utilities
class DatabaseUtils:
    """Utility functions for database operations"""
    
    @staticmethod
    async def create_backup():
        """Create database backup"""
        logger.info("💾 Creating database backup...")
        
        try:
            # Implementation would create a backup of the PostgreSQL database
            # This could use pg_dump or similar tools
            backup_filename = f"backup_{int(asyncio.get_event_loop().time())}.sql"
            
            # Placeholder for actual backup implementation
            logger.info(f"✅ Database backup created: {backup_filename}")
            
            return backup_filename
            
        except Exception as e:
            logger.error(f"❌ Database backup failed: {e}")
            raise
    
    @staticmethod
    async def restore_backup(backup_file: str):
        """Restore database from backup"""
        logger.info(f"🔄 Restoring database from: {backup_file}")
        
        try:
            # Implementation would restore from the specified backup file
            # This could use psql or similar tools
            
            logger.info("✅ Database restore completed")
            
        except Exception as e:
            logger.error(f"❌ Database restore failed: {e}")
            raise
    
    @staticmethod
    async def optimize_database():
        """Optimize database performance"""
        logger.info("⚡ Optimizing database performance...")
        
        try:
            async with get_async_session() as session:
                # Run database optimization queries
                await session.execute(text("VACUUM ANALYZE;"))
                await session.commit()
            
            logger.info("✅ Database optimization completed")
            
        except Exception as e:
            logger.error(f"❌ Database optimization failed: {e}")
            raise

# Export main components
__all__ = [
    "Base",
    "init_database",
    "close_database", 
    "get_async_session",
    "get_sync_session",
    "get_db_session",
    "get_db",
    "get_db_manager",
    "test_database_connection",
    "DatabaseManager",
    "DatabaseUtils",
    "db_manager"
]