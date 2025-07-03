"""
Database Service - Week 2 Implementation
Milestone 1C: Strategic database management for Agentic RAG system

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func
from datetime import datetime, timedelta

from config.neon_database import get_neon_session, get_neon_engine
from config.database import get_sqlite_session, get_sqlite_engine
from models.unified_models import DocumentEntity, ChunkEntity, QueryEntity, ResponseEntity, OutcomeEvent

logger = logging.getLogger(__name__)

class DatabaseService:
    """Strategic database operations for Agentic RAG system"""
    
    def __init__(self):
        self.neon_engine = None
        self.sqlite_engine = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize database connections"""
        try:
            self.neon_engine = await get_neon_engine()
            self.sqlite_engine = await get_sqlite_engine()
            self._initialized = True
            logger.info("✅ Database service initialized")
        except Exception as e:
            logger.error(f"❌ Database service initialization failed: {e}")
            raise
    
    @asynccontextmanager
    async def get_vector_session(self):
        """Get Neon PostgreSQL session for vector operations"""
        if not self._initialized:
            await self.initialize()
        
        async with get_neon_session() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    @asynccontextmanager 
    async def get_operational_session(self):
        """Get SQLite session for operational data"""
        if not self._initialized:
            await self.initialize()
        
        async with get_sqlite_session() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def execute_vector_search(
        self, 
        query_embedding: List[float], 
        match_threshold: float = 0.8,
        match_count: int = 10,
        boost_performance: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute vector similarity search using Week 1 search_chunks_weighted function
        
        Leverages existing Neon PostgreSQL functions for optimal performance
        """
        try:
            async with self.get_vector_session() as session:
                # Use Week 1 search_chunks_weighted function
                query = text("""
                    SELECT * FROM search_chunks_weighted(
                        :query_embedding::vector,
                        :match_threshold,
                        :match_count,
                        :boost_performance
                    )
                """)
                
                result = await session.execute(query, {
                    "query_embedding": query_embedding,
                    "match_threshold": match_threshold,
                    "match_count": match_count,
                    "boost_performance": boost_performance
                })
                
                results = result.fetchall()
                
                # Convert to dictionaries for easier handling
                return [dict(row._mapping) for row in results]
                
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            raise
    
    async def execute_hybrid_search(
        self,
        query_embedding: List[float],
        query_text: str,
        match_threshold: float = 0.8,
        match_count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Execute hybrid search using Week 1 hybrid_search function
        
        Combines vector similarity with full-text search
        """
        try:
            async with self.get_vector_session() as session:
                # Use Week 1 hybrid_search function
                query = text("""
                    SELECT * FROM hybrid_search(
                        :query_embedding::vector,
                        :query_text,
                        :match_threshold,
                        :match_count
                    )
                """)
                
                result = await session.execute(query, {
                    "query_embedding": query_embedding,
                    "query_text": query_text,
                    "match_threshold": match_threshold,
                    "match_count": match_count
                })
                
                results = result.fetchall()
                return [dict(row._mapping) for row in results]
                
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            raise
    
    async def analyze_search_performance(
        self, 
        time_window_days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyze search performance using Week 1 analyze_search_performance function
        """
        try:
            async with self.get_vector_session() as session:
                query = text("SELECT * FROM analyze_search_performance(:time_window_days)")
                
                result = await session.execute(query, {
                    "time_window_days": time_window_days
                })
                
                performance_data = result.fetchone()
                
                if performance_data:
                    return dict(performance_data._mapping)
                else:
                    return {"message": "No performance data available"}
                    
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            raise
    
    async def store_query_outcome(
        self,
        query_id: str,
        response_id: str,
        outcome_data: Dict[str, Any],
        confidence_score: float
    ) -> bool:
        """Store query outcome for learning system"""
        try:
            async with self.get_vector_session() as session:
                # Insert into search_outcomes table (from Week 1 schema)
                query = text("""
                    INSERT INTO search_outcomes (
                        id, query_id, response_id, strategy_used, user_satisfaction,
                        relevance_scores, response_time, conversion_occurred,
                        confidence_score, created_at
                    ) VALUES (
                        gen_random_uuid(), :query_id, :response_id, :strategy_used,
                        :user_satisfaction, :relevance_scores, :response_time,
                        :conversion_occurred, :confidence_score, NOW()
                    )
                """)
                
                await session.execute(query, {
                    "query_id": query_id,
                    "response_id": response_id,
                    "strategy_used": outcome_data.get("strategy_used", "unknown"),
                    "user_satisfaction": outcome_data.get("user_satisfaction", 0.5),
                    "relevance_scores": outcome_data.get("relevance_scores", []),
                    "response_time": outcome_data.get("response_time", 0),
                    "conversion_occurred": outcome_data.get("conversion_occurred", False),
                    "confidence_score": confidence_score
                })
                
                await session.commit()
                return True
                
        except Exception as e:
            logger.error(f"Outcome storage failed: {e}")
            return False
    
    async def get_strategy_performance(self) -> Dict[str, Dict[str, float]]:
        """Get performance metrics by search strategy"""
        try:
            async with self.get_vector_session() as session:
                query = text("""
                    SELECT 
                        strategy_used,
                        AVG(user_satisfaction) as avg_satisfaction,
                        AVG(confidence_score) as avg_confidence,
                        AVG(response_time) as avg_response_time,
                        COUNT(*) as total_queries,
                        SUM(CASE WHEN conversion_occurred THEN 1 ELSE 0 END)::float / COUNT(*) as conversion_rate
                    FROM search_outcomes 
                    WHERE created_at >= NOW() - INTERVAL '7 days'
                    GROUP BY strategy_used
                """)
                
                result = await session.execute(query)
                strategies = result.fetchall()
                
                performance_data = {}
                for strategy in strategies:
                    performance_data[strategy.strategy_used] = {
                        "avg_satisfaction": float(strategy.avg_satisfaction or 0),
                        "avg_confidence": float(strategy.avg_confidence or 0),
                        "avg_response_time": float(strategy.avg_response_time or 0),
                        "total_queries": int(strategy.total_queries),
                        "conversion_rate": float(strategy.conversion_rate or 0)
                    }
                
                return performance_data
                
        except Exception as e:
            logger.error(f"Strategy performance analysis failed: {e}")
            return {}
    
    async def maintain_database(self) -> bool:
        """
        Execute database maintenance using Week 1 maintain_database function
        """
        try:
            async with self.get_vector_session() as session:
                query = text("SELECT maintain_database()")
                await session.execute(query)
                await session.commit()
                
                logger.info("✅ Database maintenance completed")
                return True
                
        except Exception as e:
            logger.error(f"Database maintenance failed: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health and connectivity"""
        health_status = {
            "neon_postgresql": "unknown",
            "sqlite": "unknown",
            "vector_search": "unknown",
            "learning_system": "unknown"
        }
        
        # Check Neon PostgreSQL
        try:
            async with self.get_vector_session() as session:
                await session.execute(text("SELECT 1"))
                health_status["neon_postgresql"] = "healthy"
                
                # Test vector operations
                test_vector = [0.1] * 1536  # OpenAI embedding size
                await session.execute(text("SELECT :vector::vector"), {"vector": test_vector})
                health_status["vector_search"] = "healthy"
                
        except Exception as e:
            logger.error(f"Neon health check failed: {e}")
            health_status["neon_postgresql"] = "unhealthy"
            health_status["vector_search"] = "unhealthy"
        
        # Check SQLite
        try:
            async with self.get_operational_session() as session:
                await session.execute(text("SELECT 1"))
                health_status["sqlite"] = "healthy"
                
        except Exception as e:
            logger.error(f"SQLite health check failed: {e}")
            health_status["sqlite"] = "unhealthy"
        
        # Check learning system tables
        try:
            async with self.get_vector_session() as session:
                await session.execute(text("SELECT COUNT(*) FROM search_outcomes"))
                health_status["learning_system"] = "healthy"
                
        except Exception as e:
            logger.error(f"Learning system health check failed: {e}")
            health_status["learning_system"] = "unhealthy"
        
        return health_status
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics for monitoring"""
        stats = {}
        
        try:
            async with self.get_vector_session() as session:
                # Document and chunk counts
                result = await session.execute(text("""
                    SELECT 
                        (SELECT COUNT(*) FROM documents) as document_count,
                        (SELECT COUNT(*) FROM chunks) as chunk_count,
                        (SELECT COUNT(*) FROM search_outcomes) as outcome_count
                """))
                
                row = result.fetchone()
                stats.update({
                    "document_count": int(row.document_count),
                    "chunk_count": int(row.chunk_count),
                    "outcome_count": int(row.outcome_count)
                })
                
                # Recent activity
                result = await session.execute(text("""
                    SELECT COUNT(*) as recent_queries
                    FROM search_outcomes 
                    WHERE created_at >= NOW() - INTERVAL '24 hours'
                """))
                
                row = result.fetchone()
                stats["recent_queries_24h"] = int(row.recent_queries)
                
        except Exception as e:
            logger.error(f"Database stats failed: {e}")
            stats["error"] = str(e)
        
        return stats