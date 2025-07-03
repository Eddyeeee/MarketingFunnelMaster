"""
Neo4j Knowledge Graph Manager for Agentic RAG System
Handles Neo4j connections and Graphiti integration with performance optimization
Version: 1.0.0
Created: 2025-07-03
"""

import os
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
from uuid import uuid4, UUID

from neo4j import AsyncGraphDatabase, AsyncSession
from neo4j.exceptions import ServiceUnavailable, TransientError
import aiofiles

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class Neo4jConfig:
    """Neo4j configuration settings"""
    uri: str = os.getenv("NEO4J_URI", "neo4j+s://your-instance.databases.neo4j.io")
    username: str = os.getenv("NEO4J_USERNAME", "neo4j")
    password: str = os.getenv("NEO4J_PASSWORD", "")
    database: str = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Connection settings
    max_connection_lifetime: int = int(os.getenv("NEO4J_MAX_CONNECTION_LIFETIME", "1800"))  # 30 minutes
    max_connection_pool_size: int = int(os.getenv("NEO4J_MAX_CONNECTION_POOL_SIZE", "50"))
    connection_timeout: int = int(os.getenv("NEO4J_CONNECTION_TIMEOUT", "15"))
    max_retry_time: int = int(os.getenv("NEO4J_MAX_RETRY_TIME", "30"))
    
    # Performance settings
    enable_query_logging: bool = os.getenv("ENABLE_GRAPH_QUERY_LOGGING", "true").lower() == "true"
    slow_query_threshold_ms: int = int(os.getenv("SLOW_GRAPH_QUERY_THRESHOLD_MS", "2000"))
    
    def __post_init__(self):
        if not self.password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")

class GraphEntity:
    """Represents a graph entity with outcome tracking"""
    
    def __init__(self, uuid: str, name: str, entity_type: str, properties: Dict[str, Any] = None):
        self.uuid = uuid
        self.name = name
        self.type = entity_type
        self.properties = properties or {}
        
        # Performance metrics
        self.performance_score = 0.0
        self.confidence_score = 0.5
        self.relevance_score = 0.0
        self.success_rate = 0.0
        
        # Temporal tracking
        self.valid_from = datetime.now()
        self.valid_to = None
        
        # Source tracking
        self.source_document_id = None
        self.extraction_confidence = 1.0
        
        # Learning signals
        self.user_interaction_count = 0
        
        # Metadata
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tags = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary for Neo4j storage"""
        return {
            "uuid": self.uuid,
            "name": self.name,
            "type": self.type,
            "properties": self.properties,
            "performance_score": self.performance_score,
            "confidence_score": self.confidence_score,
            "relevance_score": self.relevance_score,
            "success_rate": self.success_rate,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
            "source_document_id": self.source_document_id,
            "extraction_confidence": self.extraction_confidence,
            "user_interaction_count": self.user_interaction_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags
        }

class GraphRelationship:
    """Represents a graph relationship with performance tracking"""
    
    def __init__(self, source_uuid: str, target_uuid: str, relationship_type: str):
        self.id = str(uuid4())
        self.source_uuid = source_uuid
        self.target_uuid = target_uuid
        self.relationship_type = relationship_type
        
        # Strength and confidence
        self.confidence_score = 0.5
        self.strength = 0.5
        
        # Performance tracking
        self.prediction_accuracy = 0.0
        self.usage_count = 0
        
        # Temporal validity
        self.valid_from = datetime.now()
        self.valid_to = None
        
        # Properties
        self.properties = {}
        
        # Metadata
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary for Neo4j storage"""
        return {
            "id": self.id,
            "relationship_type": self.relationship_type,
            "confidence_score": self.confidence_score,
            "strength": self.strength,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
            "prediction_accuracy": self.prediction_accuracy,
            "usage_count": self.usage_count,
            "properties": self.properties,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Neo4jManager:
    """Manages Neo4j connections and operations with performance optimization"""
    
    def __init__(self, config: Neo4jConfig):
        self.config = config
        self.driver = None
        self.is_initialized = False
        
    async def initialize(self) -> None:
        """Initialize Neo4j driver and verify connection"""
        if self.is_initialized:
            logger.warning("Neo4j already initialized")
            return
            
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.config.uri,
                auth=(self.config.username, self.config.password),
                max_connection_lifetime=self.config.max_connection_lifetime,
                max_connection_pool_size=self.config.max_connection_pool_size,
                connection_timeout=self.config.connection_timeout,
                max_retry_time=self.config.max_retry_time
            )
            
            # Verify connection
            await self._verify_connection()
            
            # Run setup script if needed
            await self._ensure_schema_setup()
            
            self.is_initialized = True
            logger.info("Neo4j driver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j driver: {e}")
            raise
    
    async def _verify_connection(self) -> None:
        """Verify Neo4j connection and check database health"""
        try:
            async with self.driver.session(database=self.config.database) as session:
                result = await session.run("RETURN 1 as test")
                record = await result.single()
                if record["test"] != 1:
                    raise RuntimeError("Connection test failed")
                
                # Check Neo4j version
                version_result = await session.run("CALL dbms.components() YIELD versions RETURN versions[0] as version")
                version_record = await version_result.single()
                logger.info(f"Neo4j version: {version_record['version']}")
                
        except Exception as e:
            logger.error(f"Neo4j connection verification failed: {e}")
            raise
    
    async def _ensure_schema_setup(self) -> None:
        """Ensure database schema is properly set up"""
        try:
            # Check if schema is already set up
            async with self.driver.session(database=self.config.database) as session:
                result = await session.run("MATCH (s:Entity {name: 'System'}) RETURN count(s) as system_count")
                record = await result.single()
                
                if record["system_count"] == 0:
                    logger.info("Setting up Neo4j schema...")
                    # Read and execute setup script
                    setup_script_path = os.path.join(os.path.dirname(__file__), "neo4j_setup.cypher")
                    if os.path.exists(setup_script_path):
                        async with aiofiles.open(setup_script_path, 'r') as f:
                            setup_script = await f.read()
                        
                        # Execute setup commands
                        commands = [cmd.strip() for cmd in setup_script.split(';') if cmd.strip()]
                        for command in commands:
                            if command:
                                await session.run(command)
                        
                        logger.info("Neo4j schema setup completed")
                    else:
                        logger.warning("Setup script not found, assuming schema is already configured")
                else:
                    logger.info("Neo4j schema already configured")
                    
        except Exception as e:
            logger.error(f"Schema setup failed: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """Get Neo4j session"""
        if not self.is_initialized:
            await self.initialize()
        return self.driver.session(database=self.config.database)
    
    async def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute Cypher query with performance monitoring"""
        start_time = datetime.now()
        parameters = parameters or {}
        
        try:
            async with self.get_session() as session:
                result = await session.run(query, parameters)
                records = await result.data()
                
                # Log slow queries
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                if execution_time > self.config.slow_query_threshold_ms:
                    logger.warning(f"Slow query ({execution_time:.2f}ms): {query[:100]}...")
                
                return records
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.error(f"Query: {query[:200]}...")
            raise
    
    async def add_entity(self, entity: GraphEntity) -> str:
        """Add entity to the knowledge graph"""
        query = """
            CREATE (e:Entity $properties)
            RETURN e.uuid as uuid
        """
        
        result = await self.execute_query(query, {"properties": entity.to_dict()})
        return result[0]["uuid"]
    
    async def update_entity_performance(self, entity_uuid: str, performance_metrics: Dict[str, float]) -> bool:
        """Update entity performance metrics with temporal tracking"""
        query = """
            MATCH (e:Entity {uuid: $entity_uuid})
            SET e.performance_score = $performance_score,
                e.confidence_score = coalesce($confidence_score, e.confidence_score),
                e.relevance_score = coalesce($relevance_score, e.relevance_score),
                e.success_rate = coalesce($success_rate, e.success_rate),
                e.user_interaction_count = e.user_interaction_count + 1,
                e.updated_at = datetime()
            CREATE (snapshot:TemporalSnapshot {
                id: randomUUID(),
                entity_uuid: $entity_uuid,
                timestamp: datetime(),
                state: e.properties,
                performance_metrics: {
                    performance_score: e.performance_score,
                    confidence_score: e.confidence_score,
                    relevance_score: e.relevance_score,
                    success_rate: e.success_rate
                },
                changed_properties: ["performance_metrics"],
                change_trigger: "performance_update",
                validated: false,
                validation_confidence: 0.0
            })
            CREATE (e)-[:HAS_SNAPSHOT]->(snapshot)
            RETURN e.uuid as updated_uuid
        """
        
        try:
            result = await self.execute_query(query, {
                "entity_uuid": entity_uuid,
                **performance_metrics
            })
            return len(result) > 0
        except Exception as e:
            logger.error(f"Failed to update entity performance: {e}")
            return False
    
    async def create_relationship(self, relationship: GraphRelationship) -> str:
        """Create relationship between entities"""
        query = """
            MATCH (source:Entity {uuid: $source_uuid})
            MATCH (target:Entity {uuid: $target_uuid})
            CREATE (source)-[r:RELATIONSHIP $properties]->(target)
            RETURN r.id as relationship_id
        """
        
        result = await self.execute_query(query, {
            "source_uuid": relationship.source_uuid,
            "target_uuid": relationship.target_uuid,
            "properties": relationship.to_dict()
        })
        return result[0]["relationship_id"]
    
    async def find_related_entities(self, entity_uuid: str, max_depth: int = 3, 
                                   min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """Find contextually related entities"""
        query = """
            MATCH (start:Entity {uuid: $entity_uuid})
            MATCH path = (start)-[r:RELATIONSHIP*1..$max_depth]-(related:Entity)
            WHERE ALL(rel in relationships(path) WHERE rel.confidence_score >= $min_confidence)
            WITH related, 
                 length(path) as distance,
                 AVG([rel in relationships(path) | rel.confidence_score]) as path_confidence,
                 related.performance_score as performance
            RETURN related.uuid as uuid,
                   related.name as name,
                   related.type as type,
                   related.properties as properties,
                   distance,
                   path_confidence,
                   performance,
                   (path_confidence * 0.5 + performance * 0.3 + (1.0/distance) * 0.2) as relevance_score
            ORDER BY relevance_score DESC
            LIMIT 20
        """
        
        return await self.execute_query(query, {
            "entity_uuid": entity_uuid,
            "max_depth": max_depth,
            "min_confidence": min_confidence
        })
    
    async def semantic_path_search(self, start_entity: str, end_entity: str, 
                                  max_hops: int = 4) -> List[Dict[str, Any]]:
        """Find semantic paths between entities"""
        query = """
            MATCH (start:Entity {uuid: $start_entity})
            MATCH (end:Entity {uuid: $end_entity})
            MATCH path = shortestPath((start)-[r:RELATIONSHIP*1..$max_hops]-(end))
            WHERE ALL(rel in relationships(path) WHERE rel.confidence_score >= 0.6)
            WITH path, 
                 length(path) as path_length,
                 AVG([rel in relationships(path) | rel.confidence_score]) as avg_confidence,
                 [rel in relationships(path) | rel.relationship_type] as relationship_types
            RETURN [n in nodes(path) | {uuid: n.uuid, name: n.name, type: n.type}] as entities,
                   [r in relationships(path) | {type: r.relationship_type, confidence: r.confidence_score}] as relationships,
                   path_length,
                   avg_confidence,
                   relationship_types,
                   (avg_confidence * 0.7 + (1.0/path_length) * 0.3) as path_strength
            ORDER BY path_strength DESC
            LIMIT 10
        """
        
        return await self.execute_query(query, {
            "start_entity": start_entity,
            "end_entity": end_entity,
            "max_hops": max_hops
        })
    
    async def intelligent_entity_search(self, search_term: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Intelligent entity search with relevance scoring"""
        query = """
            MATCH (e:Entity)
            WHERE e.name CONTAINS $search_term 
               OR any(tag in e.tags WHERE tag CONTAINS $search_term)
               OR e.description CONTAINS $search_term
            WITH e, 
                 CASE 
                     WHEN e.name CONTAINS $search_term THEN 1.0
                     WHEN any(tag in e.tags WHERE tag CONTAINS $search_term) THEN 0.8
                     ELSE 0.6
                 END as name_score,
                 e.performance_score as performance_score,
                 e.confidence_score as confidence_score
            WITH e, (name_score * 0.4 + performance_score * 0.3 + confidence_score * 0.3) as relevance_score
            ORDER BY relevance_score DESC
            LIMIT $limit
            RETURN e.uuid as uuid,
                   e.name as name,
                   e.type as type,
                   e.properties as properties,
                   e.performance_score as performance_score,
                   e.confidence_score as confidence_score,
                   relevance_score
        """
        
        return await self.execute_query(query, {
            "search_term": search_term,
            "limit": limit
        })
    
    async def analyze_relationship_patterns(self) -> Dict[str, Any]:
        """Analyze relationship patterns and effectiveness"""
        query = """
            MATCH ()-[r:RELATIONSHIP]-()
            RETURN r.relationship_type as type,
                   COUNT(*) as count,
                   AVG(r.confidence_score) as avg_confidence,
                   AVG(r.strength) as avg_strength,
                   AVG(r.prediction_accuracy) as avg_accuracy,
                   SUM(r.usage_count) as total_usage
            ORDER BY avg_accuracy DESC
        """
        
        result = await self.execute_query(query)
        return {
            "relationship_analysis": result,
            "total_relationships": len(result),
            "high_accuracy_types": [r for r in result if r["avg_accuracy"] > 0.8]
        }
    
    async def detect_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """Detect isolated entities that may indicate knowledge gaps"""
        query = """
            MATCH (e:Entity)
            WHERE NOT (e)-[:RELATIONSHIP]-()
            RETURN e.uuid as isolated_entity_uuid,
                   e.name as entity_name,
                   e.type as entity_type,
                   e.performance_score as performance,
                   CASE 
                       WHEN e.performance_score > 0.7 THEN "high"
                       WHEN e.performance_score > 0.4 THEN "medium"
                       ELSE "low"
                   END as isolation_risk
            ORDER BY e.performance_score DESC
        """
        
        return await self.execute_query(query)
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health metrics"""
        query = """
            MATCH (e:Entity) 
            OPTIONAL MATCH ()-[r:RELATIONSHIP]->()
            OPTIONAL MATCH (t:TemporalSnapshot)
            RETURN {
                total_entities: count(DISTINCT e),
                total_relationships: count(DISTINCT r),
                total_snapshots: count(DISTINCT t),
                avg_performance: avg(e.performance_score),
                avg_confidence: avg(e.confidence_score),
                high_performers: size([entity IN collect(DISTINCT e) WHERE entity.performance_score > 0.8]),
                timestamp: toString(datetime())
            } as health
        """
        
        result = await self.execute_query(query)
        return result[0]["health"]
    
    async def optimize_performance(self) -> Dict[str, Any]:
        """Run performance optimization on the knowledge graph"""
        query = """
            // Update relationship strengths based on usage
            MATCH ()-[r:RELATIONSHIP]->()
            WHERE r.usage_count > 0
            SET r.strength = CASE 
                WHEN r.prediction_accuracy > 0.8 THEN least(r.strength + 0.1, 1.0)
                WHEN r.prediction_accuracy < 0.3 THEN greatest(r.strength - 0.05, 0.0)
                ELSE r.strength
            END,
            r.updated_at = datetime()
            
            // Clean up old temporal snapshots (keep last 30 days)
            WITH count(r) as relationships_updated
            MATCH (t:TemporalSnapshot)
            WHERE t.timestamp < datetime() - duration({days: 30})
            DETACH DELETE t
            
            RETURN relationships_updated, count(t) as snapshots_cleaned
        """
        
        result = await self.execute_query(query)
        return {
            "relationships_updated": result[0]["relationships_updated"],
            "snapshots_cleaned": result[0]["snapshots_cleaned"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def close(self) -> None:
        """Close Neo4j driver"""
        if self.driver:
            await self.driver.close()
            self.is_initialized = False
            logger.info("Neo4j driver closed")

# Singleton instance
_neo4j_config = Neo4jConfig()
graph_manager = Neo4jManager(_neo4j_config)

# Helper functions
async def initialize_graph():
    """Initialize Neo4j connection"""
    await graph_manager.initialize()

async def get_graph_session():
    """Get Neo4j session"""
    return await graph_manager.get_session()

async def execute_graph_query(query: str, parameters: Dict[str, Any] = None):
    """Execute graph query with the global manager"""
    return await graph_manager.execute_query(query, parameters)

async def close_graph():
    """Close graph connections"""
    await graph_manager.close()

# Configuration validation
def validate_graph_configuration():
    """Validate Neo4j configuration"""
    required_env_vars = ["NEO4J_PASSWORD"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    logger.info("Neo4j configuration validated successfully")

if __name__ == "__main__":
    # Test the Neo4j configuration
    async def test_graph():
        try:
            validate_graph_configuration()
            await initialize_graph()
            
            # Test basic operations
            health = await graph_manager.get_system_health()
            print(f"Graph health: {health}")
            
            # Test entity search
            results = await graph_manager.intelligent_entity_search("System", limit=5)
            print(f"Search results: {len(results)} entities found")
            
            await close_graph()
            print("Graph test completed successfully!")
            
        except Exception as e:
            print(f"Graph test failed: {e}")
    
    asyncio.run(test_graph())