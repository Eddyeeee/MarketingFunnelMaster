# TEC-spec-FastAPIIntegration-v1.md
# FastAPI Integration Plan for Hybrid Agentic RAG Architecture

## Overview
This specification defines the FastAPI integration architecture that coordinates the hybrid vector-graph RAG system, enabling seamless interaction between Neon PostgreSQL, Neo4j, and the AI agent network.

## Architecture Overview

### Core FastAPI Structure
```
FastAPI Application
├── API Routes (Public Interface)
├── Service Layer (Business Logic)
├── Database Layer (Data Access)
├── Agent Integration (AI Orchestration)
├── Monitoring Layer (Performance Tracking)
└── Background Tasks (Async Processing)
```

### Integration Components
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import asyncio
from typing import List, Dict, Optional, Any
import logging

# Core application configuration
class ApplicationConfig:
    def __init__(self):
        self.app_name = "Marketing Funnel RAG System"
        self.version = "1.0.0"
        self.debug = False
        
        # Database configurations
        self.neon_config = {
            "host": "ep-xxx-xxx.us-east-1.aws.neon.tech",
            "port": 5432,
            "database": "marketing_funnel_rag",
            "user": "neon_user",
            "password": "${NEON_PASSWORD}",
            "sslmode": "require"
        }
        
        self.neo4j_config = {
            "uri": "neo4j+s://your-instance.databases.neo4j.io",
            "username": "neo4j",
            "password": "${NEO4J_PASSWORD}",
            "database": "marketing_funnel_graph"
        }
        
        # Agent configuration
        self.agent_config = {
            "max_concurrent_agents": 10,
            "agent_timeout_seconds": 30,
            "retry_attempts": 3
        }

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    # Startup
    await initialize_database_pools()
    await initialize_agent_network()
    await start_background_tasks()
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    await cleanup_database_pools()
    await shutdown_agent_network()
    logger.info("Application shutdown complete")

# Initialize FastAPI app
app = FastAPI(
    title="Marketing Funnel RAG System",
    description="Hybrid Vector-Graph RAG with Agentic Intelligence",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Database Integration Layer

### 1. Unified Database Manager
```python
from databases import Database
from neo4j import AsyncGraphDatabase
import asyncpg
from typing import Union

class DatabaseManager:
    def __init__(self, config: ApplicationConfig):
        self.config = config
        self.postgres_pool = None
        self.neo4j_driver = None
        
    async def initialize_postgres(self):
        """Initialize PostgreSQL connection pool"""
        try:
            self.postgres_pool = await asyncpg.create_pool(
                host=self.config.neon_config["host"],
                port=self.config.neon_config["port"],
                database=self.config.neon_config["database"],
                user=self.config.neon_config["user"],
                password=self.config.neon_config["password"],
                ssl=self.config.neon_config["sslmode"],
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            logger.info("PostgreSQL pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            raise
    
    async def initialize_neo4j(self):
        """Initialize Neo4j driver"""
        try:
            self.neo4j_driver = AsyncGraphDatabase.driver(
                self.config.neo4j_config["uri"],
                auth=(
                    self.config.neo4j_config["username"],
                    self.config.neo4j_config["password"]
                ),
                max_connection_lifetime=30 * 60,
                max_connection_pool_size=50
            )
            logger.info("Neo4j driver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j: {e}")
            raise
    
    async def get_postgres_connection(self):
        """Get PostgreSQL connection from pool"""
        if not self.postgres_pool:
            await self.initialize_postgres()
        return self.postgres_pool.acquire()
    
    async def get_neo4j_session(self):
        """Get Neo4j session"""
        if not self.neo4j_driver:
            await self.initialize_neo4j()
        return self.neo4j_driver.session()
    
    async def close_connections(self):
        """Close all database connections"""
        if self.postgres_pool:
            await self.postgres_pool.close()
        if self.neo4j_driver:
            await self.neo4j_driver.close()

# Global database manager instance
db_manager = DatabaseManager(ApplicationConfig())
```

### 2. Service Layer Architecture
```python
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

class SearchRequest(BaseModel):
    query: str
    search_type: str = "adaptive"  # vector, graph, hybrid, adaptive
    max_results: int = 10
    confidence_threshold: float = 0.5
    include_metadata: bool = True
    user_context: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    id: UUID
    content: str
    relevance_score: float
    source_type: str
    metadata: Dict[str, Any]
    confidence_score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    search_strategy_used: str
    response_time_ms: float
    query_id: UUID

class BaseService(ABC):
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.logger = logging.getLogger(self.__class__.__name__)

class VectorSearchService(BaseService):
    """Service for vector database operations"""
    
    async def search_documents(self, 
                              query_embedding: List[float],
                              max_results: int = 10,
                              confidence_threshold: float = 0.5) -> List[SearchResult]:
        """Search documents using vector similarity"""
        async with self.db.get_postgres_connection() as conn:
            query = """
                SELECT id, content, title, metadata,
                       1 - (content_vector <=> $1) as similarity
                FROM documents
                WHERE 1 - (content_vector <=> $1) > $2
                ORDER BY content_vector <=> $1
                LIMIT $3
            """
            
            rows = await conn.fetch(query, query_embedding, confidence_threshold, max_results)
            
            results = []
            for row in rows:
                result = SearchResult(
                    id=row['id'],
                    content=row['content'],
                    relevance_score=row['similarity'],
                    source_type="document",
                    metadata=row['metadata'],
                    confidence_score=row['similarity']
                )
                results.append(result)
            
            return results
    
    async def search_chunks(self,
                          query_embedding: List[float],
                          max_results: int = 10,
                          boost_performance: bool = True) -> List[SearchResult]:
        """Search chunks with performance boosting"""
        async with self.db.get_postgres_connection() as conn:
            query = """
                SELECT * FROM search_chunks_weighted($1, $2, $3, $4)
            """
            
            rows = await conn.fetch(
                query, 
                query_embedding, 
                0.5,  # threshold
                max_results,
                boost_performance
            )
            
            results = []
            for row in rows:
                result = SearchResult(
                    id=row['id'],
                    content=row['content'],
                    relevance_score=row['final_score'],
                    source_type="chunk",
                    metadata={"performance_score": row['performance_score']},
                    confidence_score=row['similarity']
                )
                results.append(result)
            
            return results

class GraphSearchService(BaseService):
    """Service for graph database operations"""
    
    async def find_related_entities(self,
                                  entity_id: UUID,
                                  max_depth: int = 3,
                                  min_confidence: float = 0.7) -> List[SearchResult]:
        """Find contextually related entities"""
        async with self.db.get_neo4j_session() as session:
            query = """
                MATCH (start:Entity {uuid: $entity_id})
                MATCH path = (start)-[r:RELATIONSHIP*1..$max_depth]-(related:Entity)
                WHERE ALL(rel in relationships(path) WHERE rel.confidence_score >= $min_confidence)
                WITH related, 
                     length(path) as distance,
                     AVG([rel in relationships(path) | rel.confidence_score]) as path_confidence
                RETURN related.uuid as id,
                       related.name as name,
                       related.properties as properties,
                       path_confidence,
                       distance
                ORDER BY path_confidence DESC
                LIMIT 20
            """
            
            result = await session.run(query, 
                                     entity_id=str(entity_id),
                                     max_depth=max_depth,
                                     min_confidence=min_confidence)
            
            entities = []
            async for record in result:
                entity = SearchResult(
                    id=UUID(record['id']),
                    content=record['name'],
                    relevance_score=record['path_confidence'],
                    source_type="graph_entity",
                    metadata={
                        "properties": record['properties'],
                        "distance": record['distance']
                    },
                    confidence_score=record['path_confidence']
                )
                entities.append(entity)
            
            return entities
    
    async def semantic_path_search(self,
                                 start_entity: UUID,
                                 end_entity: UUID,
                                 max_hops: int = 4) -> List[Dict[str, Any]]:
        """Find semantic paths between entities"""
        async with self.db.get_neo4j_session() as session:
            query = """
                MATCH (start:Entity {uuid: $start_entity})
                MATCH (end:Entity {uuid: $end_entity})
                MATCH path = shortestPath((start)-[r:RELATIONSHIP*1..$max_hops]-(end))
                WHERE ALL(rel in relationships(path) WHERE rel.confidence_score >= 0.6)
                WITH path, 
                     length(path) as path_length,
                     AVG([rel in relationships(path) | rel.confidence_score]) as avg_confidence
                RETURN nodes(path) as entities,
                       relationships(path) as relationships,
                       path_length,
                       avg_confidence
                ORDER BY avg_confidence DESC
                LIMIT 10
            """
            
            result = await session.run(query,
                                     start_entity=str(start_entity),
                                     end_entity=str(end_entity),
                                     max_hops=max_hops)
            
            paths = []
            async for record in result:
                path = {
                    "entities": [dict(entity) for entity in record['entities']],
                    "relationships": [dict(rel) for rel in record['relationships']],
                    "path_length": record['path_length'],
                    "confidence": record['avg_confidence']
                }
                paths.append(path)
            
            return paths

class HybridSearchService(BaseService):
    """Service coordinating hybrid search across vector and graph databases"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)
        self.vector_service = VectorSearchService(db_manager)
        self.graph_service = GraphSearchService(db_manager)
    
    async def adaptive_search(self, request: SearchRequest) -> SearchResponse:
        """Intelligently choose search strategy based on query analysis"""
        start_time = time.time()
        query_id = uuid4()
        
        # Step 1: Analyze query to determine best strategy
        strategy = await self.analyze_query_strategy(request.query)
        
        # Step 2: Generate embedding for vector search
        query_embedding = await self.generate_embedding(request.query)
        
        # Step 3: Execute search based on strategy
        if strategy == "vector":
            results = await self.vector_only_search(query_embedding, request)
        elif strategy == "graph":
            results = await self.graph_only_search(request)
        else:  # hybrid
            results = await self.hybrid_search(query_embedding, request)
        
        # Step 4: Track search outcome
        response_time = (time.time() - start_time) * 1000
        await self.track_search_outcome(query_id, request, results, strategy, response_time)
        
        return SearchResponse(
            results=results,
            total_results=len(results),
            search_strategy_used=strategy,
            response_time_ms=response_time,
            query_id=query_id
        )
    
    async def hybrid_search(self, 
                          query_embedding: List[float],
                          request: SearchRequest) -> List[SearchResult]:
        """Execute hybrid search combining vector and graph results"""
        # Get vector results
        vector_results = await self.vector_service.search_chunks(
            query_embedding, 
            max_results=request.max_results * 2  # Get more for reranking
        )
        
        # Extract entities from vector results for graph expansion
        entity_ids = await self.extract_entities_from_results(vector_results)
        
        # Get graph-based expansions
        graph_results = []
        for entity_id in entity_ids[:5]:  # Limit to top 5 entities
            related = await self.graph_service.find_related_entities(
                entity_id, max_depth=2, min_confidence=0.6
            )
            graph_results.extend(related)
        
        # Combine and rerank results
        combined_results = await self.rerank_hybrid_results(
            vector_results, graph_results, request
        )
        
        return combined_results[:request.max_results]
    
    async def rerank_hybrid_results(self,
                                   vector_results: List[SearchResult],
                                   graph_results: List[SearchResult],
                                   request: SearchRequest) -> List[SearchResult]:
        """Rerank results combining vector similarity and graph connectivity"""
        # Create unified scoring
        all_results = {}
        
        # Add vector results with base score
        for result in vector_results:
            all_results[result.id] = {
                "result": result,
                "vector_score": result.relevance_score,
                "graph_score": 0.0,
                "connectivity_bonus": 0.0
            }
        
        # Add graph connectivity bonuses
        for result in graph_results:
            if result.id in all_results:
                all_results[result.id]["graph_score"] = result.relevance_score
                all_results[result.id]["connectivity_bonus"] = 0.2
            else:
                all_results[result.id] = {
                    "result": result,
                    "vector_score": 0.0,
                    "graph_score": result.relevance_score,
                    "connectivity_bonus": 0.0
                }
        
        # Calculate final scores
        final_results = []
        for item in all_results.values():
            final_score = (
                item["vector_score"] * 0.6 +
                item["graph_score"] * 0.3 +
                item["connectivity_bonus"] * 0.1
            )
            
            result = item["result"]
            result.relevance_score = final_score
            final_results.append(result)
        
        # Sort by final score
        final_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return final_results
```

## API Routes

### 1. Search Endpoints
```python
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
import asyncio

router = APIRouter(prefix="/api/v1", tags=["search"])

@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    background_tasks: BackgroundTasks,
    hybrid_service: HybridSearchService = Depends(get_hybrid_service)
):
    """Main search endpoint with adaptive strategy selection"""
    try:
        response = await hybrid_service.adaptive_search(request)
        
        # Schedule background learning task
        background_tasks.add_task(
            update_search_performance,
            response.query_id,
            request,
            response
        )
        
        return response
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search operation failed")

@router.post("/search/stream")
async def stream_search(
    request: SearchRequest,
    hybrid_service: HybridSearchService = Depends(get_hybrid_service)
):
    """Streaming search endpoint for real-time results"""
    
    async def generate_stream():
        try:
            async for result in hybrid_service.stream_search(request):
                yield f"data: {json.dumps(result.dict())}\n\n"
        except Exception as e:
            error_data = {"error": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/plain")

@router.get("/search/{query_id}/results")
async def get_search_results(
    query_id: UUID,
    hybrid_service: HybridSearchService = Depends(get_hybrid_service)
):
    """Retrieve cached search results"""
    try:
        results = await hybrid_service.get_cached_results(query_id)
        if not results:
            raise HTTPException(status_code=404, detail="Search results not found")
        return results
    except Exception as e:
        logger.error(f"Failed to retrieve results: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve results")
```

### 2. Learning and Feedback Endpoints
```python
@router.post("/feedback")
async def submit_feedback(
    query_id: UUID,
    feedback: Dict[str, Any],
    background_tasks: BackgroundTasks,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Submit user feedback for learning optimization"""
    try:
        await learning_service.process_feedback(query_id, feedback)
        
        # Schedule background learning update
        background_tasks.add_task(
            update_learning_models,
            query_id,
            feedback
        )
        
        return {"status": "feedback_received", "query_id": query_id}
    except Exception as e:
        logger.error(f"Feedback processing failed: {e}")
        raise HTTPException(status_code=500, detail="Feedback processing failed")

@router.get("/analytics/performance")
async def get_performance_analytics(
    time_window_days: int = 7,
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get system performance analytics"""
    try:
        analytics = await analytics_service.get_performance_metrics(time_window_days)
        return analytics
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Analytics retrieval failed")
```

### 3. Health and Monitoring Endpoints
```python
@router.get("/health")
async def health_check():
    """System health check"""
    try:
        # Check database connections
        postgres_health = await db_manager.check_postgres_health()
        neo4j_health = await db_manager.check_neo4j_health()
        
        # Check agent network
        agent_health = await check_agent_network_health()
        
        return {
            "status": "healthy",
            "databases": {
                "postgres": postgres_health,
                "neo4j": neo4j_health
            },
            "agents": agent_health,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now()
        }

@router.get("/metrics")
async def get_system_metrics():
    """Get detailed system metrics"""
    try:
        metrics = await collect_system_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        raise HTTPException(status_code=500, detail="Metrics collection failed")
```

## Background Tasks and Optimization

### 1. Performance Optimization Tasks
```python
async def update_search_performance(query_id: UUID, 
                                   request: SearchRequest,
                                   response: SearchResponse):
    """Background task to update search performance metrics"""
    try:
        # Update performance metrics
        await update_query_performance(query_id, response.response_time_ms)
        
        # Update result relevance scores
        await update_result_relevance(response.results)
        
        # Trigger learning optimization if needed
        await trigger_learning_optimization(query_id)
        
    except Exception as e:
        logger.error(f"Performance update failed: {e}")

async def update_learning_models(query_id: UUID, feedback: Dict[str, Any]):
    """Background task to update learning models based on feedback"""
    try:
        # Process feedback signals
        await process_feedback_signals(query_id, feedback)
        
        # Update entity performance scores
        await update_entity_scores(query_id, feedback)
        
        # Adjust search strategies
        await adjust_search_strategies(feedback)
        
    except Exception as e:
        logger.error(f"Learning model update failed: {e}")

async def optimize_database_performance():
    """Background task for database optimization"""
    try:
        # Optimize vector indexes
        await optimize_vector_indexes()
        
        # Clean up old search outcomes
        await cleanup_old_outcomes()
        
        # Update performance statistics
        await update_performance_statistics()
        
    except Exception as e:
        logger.error(f"Database optimization failed: {e}")
```

### 2. Dependency Injection
```python
from functools import lru_cache

@lru_cache()
def get_hybrid_service() -> HybridSearchService:
    """Get hybrid search service instance"""
    return HybridSearchService(db_manager)

@lru_cache()
def get_learning_service() -> LearningService:
    """Get learning service instance"""
    return LearningService(db_manager)

@lru_cache()
def get_analytics_service() -> AnalyticsService:
    """Get analytics service instance"""
    return AnalyticsService(db_manager)
```

## Configuration and Deployment

### 1. Environment Configuration
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    neon_password: str
    neo4j_password: str
    
    # API settings
    api_key: str
    cors_origins: List[str] = ["*"]
    
    # Performance settings
    max_concurrent_searches: int = 100
    search_timeout_seconds: int = 30
    
    # Learning settings
    learning_rate: float = 0.01
    confidence_threshold: float = 0.7
    
    # Monitoring settings
    enable_metrics: bool = True
    metrics_interval_seconds: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Application Startup
```python
# Include routers
app.include_router(router)

# Add custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Initialize services
async def initialize_services():
    """Initialize all services"""
    await db_manager.initialize_postgres()
    await db_manager.initialize_neo4j()
    await initialize_agent_network()
    await start_background_optimizations()

# Startup event
@app.on_event("startup")
async def startup_event():
    await initialize_services()
    logger.info("FastAPI application started successfully")
```

This FastAPI integration provides a robust, scalable foundation for the hybrid RAG system with comprehensive monitoring, learning capabilities, and performance optimization.