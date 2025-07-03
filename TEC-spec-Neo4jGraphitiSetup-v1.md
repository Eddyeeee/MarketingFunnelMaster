# TEC-spec-Neo4jGraphitiSetup-v1.md
# Neo4j + Graphiti Knowledge Graph Architecture for Agentic RAG

## Overview
This specification defines the Neo4j knowledge graph setup using the Graphiti library for temporal knowledge management, relationship tracking, and contextual understanding in the Agentic RAG system.

## Neo4j Database Architecture

### Connection Configuration
```python
# Neo4j connection settings
NEO4J_CONFIG = {
    "uri": "neo4j+s://your-instance.databases.neo4j.io",
    "username": "neo4j",
    "password": "${NEO4J_PASSWORD}",
    "database": "marketing_funnel_graph",
    "max_connection_lifetime": 30 * 60,  # 30 minutes
    "max_connection_pool_size": 50,
    "connection_timeout": 15,
    "max_retry_time": 30
}

# Graphiti configuration
GRAPHITI_CONFIG = {
    "temporal_resolution": "day",  # Track changes daily
    "confidence_threshold": 0.7,
    "max_entities_per_extraction": 50,
    "relationship_types": [
        "RELATES_TO", "PART_OF", "INFLUENCES", "CAUSED_BY", 
        "TEMPORAL_FOLLOWS", "CONTEXTUAL_SIMILAR", "OUTCOME_LEADS_TO"
    ]
}
```

### Core Graph Schema

#### 1. Entity Node Structure
```python
from graphiti import Graphiti
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class EntityType(str, Enum):
    DOCUMENT = "Document"
    CONCEPT = "Concept"
    PERSON = "Person"
    ORGANIZATION = "Organization"
    PRODUCT = "Product"
    STRATEGY = "Strategy"
    OUTCOME = "Outcome"
    METRIC = "Metric"

class GraphEntity(BaseModel):
    uuid: str
    name: str
    type: EntityType
    properties: Dict[str, Any]
    
    # Outcome tracking
    performance_score: float = 0.0
    confidence_score: float = 0.0
    relevance_score: float = 0.0
    
    # Temporal validity
    valid_from: datetime
    valid_to: Optional[datetime] = None
    
    # Source tracking
    source_document_id: Optional[str] = None
    extraction_confidence: float = 0.0
    
    # Learning signals
    user_interaction_count: int = 0
    success_rate: float = 0.0
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []
```

#### 2. Relationship Structure
```python
from enum import Enum

class RelationshipType(str, Enum):
    RELATES_TO = "RELATES_TO"
    PART_OF = "PART_OF"
    INFLUENCES = "INFLUENCES"
    CAUSED_BY = "CAUSED_BY"
    TEMPORAL_FOLLOWS = "TEMPORAL_FOLLOWS"
    CONTEXTUAL_SIMILAR = "CONTEXTUAL_SIMILAR"
    OUTCOME_LEADS_TO = "OUTCOME_LEADS_TO"
    COMPETES_WITH = "COMPETES_WITH"
    ENHANCES = "ENHANCES"

class GraphRelationship(BaseModel):
    id: str
    source_entity_uuid: str
    target_entity_uuid: str
    relationship_type: RelationshipType
    
    # Confidence and strength
    confidence_score: float
    strength: float  # 0.0 to 1.0
    
    # Temporal context
    valid_from: datetime
    valid_to: Optional[datetime] = None
    
    # Performance tracking
    prediction_accuracy: float = 0.0
    usage_count: int = 0
    
    # Properties
    properties: Dict[str, Any] = {}
    
    # Metadata
    created_at: datetime
    updated_at: datetime
```

#### 3. Temporal Snapshots
```python
class TemporalSnapshot(BaseModel):
    id: str
    entity_uuid: str
    timestamp: datetime
    
    # Snapshot data
    state: Dict[str, Any]
    performance_metrics: Dict[str, float]
    
    # Change tracking
    changed_properties: List[str]
    change_trigger: str  # "user_feedback", "performance_update", "new_data"
    
    # Validation
    validated: bool = False
    validation_confidence: float = 0.0
```

## Graphiti Integration

### 1. Enhanced Graphiti Client
```python
from graphiti import Graphiti
from typing import List, Dict, Optional
import asyncio

class EnhancedGraphitiClient:
    def __init__(self, neo4j_config: Dict, graphiti_config: Dict):
        self.graphiti = Graphiti(
            uri=neo4j_config["uri"],
            username=neo4j_config["username"],
            password=neo4j_config["password"],
            database=neo4j_config["database"]
        )
        self.config = graphiti_config
        
    async def initialize_schema(self):
        """Initialize the graph schema with constraints and indexes"""
        await self.graphiti.execute_query("""
            // Create unique constraints
            CREATE CONSTRAINT entity_uuid_unique IF NOT EXISTS
            FOR (e:Entity) REQUIRE e.uuid IS UNIQUE;
            
            CREATE CONSTRAINT relationship_id_unique IF NOT EXISTS
            FOR ()-[r:RELATIONSHIP]-() REQUIRE r.id IS UNIQUE;
            
            // Create indexes for performance
            CREATE INDEX entity_name_index IF NOT EXISTS
            FOR (e:Entity) ON (e.name);
            
            CREATE INDEX entity_type_index IF NOT EXISTS
            FOR (e:Entity) ON (e.type);
            
            CREATE INDEX entity_performance_index IF NOT EXISTS
            FOR (e:Entity) ON (e.performance_score);
            
            CREATE INDEX relationship_confidence_index IF NOT EXISTS
            FOR ()-[r:RELATIONSHIP]-() ON (r.confidence_score);
            
            CREATE INDEX temporal_validity_index IF NOT EXISTS
            FOR (e:Entity) ON (e.valid_from, e.valid_to);
        """)
        
    async def add_entity_with_outcomes(self, entity: GraphEntity) -> str:
        """Add entity with outcome tracking capabilities"""
        query = """
            CREATE (e:Entity {
                uuid: $uuid,
                name: $name,
                type: $type,
                properties: $properties,
                performance_score: $performance_score,
                confidence_score: $confidence_score,
                relevance_score: $relevance_score,
                valid_from: $valid_from,
                valid_to: $valid_to,
                source_document_id: $source_document_id,
                extraction_confidence: $extraction_confidence,
                user_interaction_count: $user_interaction_count,
                success_rate: $success_rate,
                created_at: $created_at,
                updated_at: $updated_at,
                tags: $tags
            })
            RETURN e.uuid as uuid
        """
        
        result = await self.graphiti.execute_query(query, **entity.dict())
        return result[0]["uuid"]
    
    async def create_relationship_with_tracking(self, relationship: GraphRelationship) -> str:
        """Create relationship with performance tracking"""
        query = """
            MATCH (source:Entity {uuid: $source_entity_uuid})
            MATCH (target:Entity {uuid: $target_entity_uuid})
            CREATE (source)-[r:RELATIONSHIP {
                id: $id,
                relationship_type: $relationship_type,
                confidence_score: $confidence_score,
                strength: $strength,
                valid_from: $valid_from,
                valid_to: $valid_to,
                prediction_accuracy: $prediction_accuracy,
                usage_count: $usage_count,
                properties: $properties,
                created_at: $created_at,
                updated_at: $updated_at
            }]->(target)
            RETURN r.id as relationship_id
        """
        
        result = await self.graphiti.execute_query(query, **relationship.dict())
        return result[0]["relationship_id"]
```

### 2. Temporal Knowledge Management
```python
class TemporalKnowledgeManager:
    def __init__(self, graphiti_client: EnhancedGraphitiClient):
        self.client = graphiti_client
        
    async def create_temporal_snapshot(self, entity_uuid: str, 
                                     trigger: str = "scheduled") -> str:
        """Create temporal snapshot of entity state"""
        query = """
            MATCH (e:Entity {uuid: $entity_uuid})
            CREATE (t:TemporalSnapshot {
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
                change_trigger: $trigger,
                validated: false,
                validation_confidence: 0.0
            })
            CREATE (e)-[:HAS_SNAPSHOT]->(t)
            RETURN t.id as snapshot_id
        """
        
        result = await self.client.graphiti.execute_query(
            query, 
            entity_uuid=entity_uuid, 
            trigger=trigger
        )
        return result[0]["snapshot_id"]
    
    async def track_entity_evolution(self, entity_uuid: str, 
                                   time_window_days: int = 30) -> List[Dict]:
        """Track how entity has evolved over time"""
        query = """
            MATCH (e:Entity {uuid: $entity_uuid})-[:HAS_SNAPSHOT]->(t:TemporalSnapshot)
            WHERE t.timestamp >= datetime() - duration({days: $time_window_days})
            RETURN t.timestamp as timestamp,
                   t.state as state,
                   t.performance_metrics as performance,
                   t.change_trigger as trigger
            ORDER BY t.timestamp ASC
        """
        
        result = await self.client.graphiti.execute_query(
            query, 
            entity_uuid=entity_uuid,
            time_window_days=time_window_days
        )
        return result
```

### 3. Contextual Search Engine
```python
class ContextualGraphSearch:
    def __init__(self, graphiti_client: EnhancedGraphitiClient):
        self.client = graphiti_client
        
    async def find_related_entities(self, entity_uuid: str, 
                                  max_depth: int = 3,
                                  min_confidence: float = 0.7) -> List[Dict]:
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
                   distance,
                   path_confidence,
                   performance,
                   (path_confidence * 0.5 + performance * 0.3 + (1.0/distance) * 0.2) as relevance_score
            ORDER BY relevance_score DESC
            LIMIT 20
        """
        
        result = await self.client.graphiti.execute_query(
            query,
            entity_uuid=entity_uuid,
            max_depth=max_depth,
            min_confidence=min_confidence
        )
        return result
    
    async def semantic_path_search(self, start_entity: str, 
                                 end_entity: str,
                                 max_hops: int = 4) -> List[Dict]:
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
            RETURN path,
                   path_length,
                   avg_confidence,
                   relationship_types,
                   (avg_confidence * 0.7 + (1.0/path_length) * 0.3) as path_strength
            ORDER BY path_strength DESC
            LIMIT 10
        """
        
        result = await self.client.graphiti.execute_query(
            query,
            start_entity=start_entity,
            end_entity=end_entity,
            max_hops=max_hops
        )
        return result
```

### 4. Performance-Driven Graph Updates
```python
class PerformanceGraphUpdater:
    def __init__(self, graphiti_client: EnhancedGraphitiClient):
        self.client = graphiti_client
        
    async def update_entity_performance(self, entity_uuid: str, 
                                      performance_metrics: Dict[str, float]):
        """Update entity performance based on real outcomes"""
        query = """
            MATCH (e:Entity {uuid: $entity_uuid})
            SET e.performance_score = $performance_score,
                e.confidence_score = $confidence_score,
                e.relevance_score = $relevance_score,
                e.success_rate = $success_rate,
                e.user_interaction_count = e.user_interaction_count + 1,
                e.updated_at = datetime()
            RETURN e.uuid as updated_uuid
        """
        
        await self.client.graphiti.execute_query(
            query,
            entity_uuid=entity_uuid,
            **performance_metrics
        )
        
        # Create temporal snapshot for tracking
        await self.client.temporal_manager.create_temporal_snapshot(
            entity_uuid, "performance_update"
        )
    
    async def strengthen_successful_relationships(self, 
                                               relationship_id: str,
                                               success_outcome: bool):
        """Strengthen or weaken relationships based on outcomes"""
        strength_delta = 0.1 if success_outcome else -0.05
        
        query = """
            MATCH ()-[r:RELATIONSHIP {id: $relationship_id}]-()
            SET r.strength = CASE 
                WHEN r.strength + $strength_delta > 1.0 THEN 1.0
                WHEN r.strength + $strength_delta < 0.0 THEN 0.0
                ELSE r.strength + $strength_delta
            END,
            r.usage_count = r.usage_count + 1,
            r.prediction_accuracy = CASE 
                WHEN $success_outcome THEN 
                    (r.prediction_accuracy * r.usage_count + 1.0) / (r.usage_count + 1)
                ELSE 
                    (r.prediction_accuracy * r.usage_count + 0.0) / (r.usage_count + 1)
            END,
            r.updated_at = datetime()
            RETURN r.id as updated_relationship_id
        """
        
        await self.client.graphiti.execute_query(
            query,
            relationship_id=relationship_id,
            strength_delta=strength_delta,
            success_outcome=success_outcome
        )
```

### 5. Graph Analytics and Insights
```python
class GraphAnalytics:
    def __init__(self, graphiti_client: EnhancedGraphitiClient):
        self.client = graphiti_client
        
    async def get_high_performance_entities(self, 
                                          entity_type: Optional[str] = None,
                                          limit: int = 20) -> List[Dict]:
        """Get top-performing entities"""
        type_filter = "AND e.type = $entity_type" if entity_type else ""
        
        query = f"""
            MATCH (e:Entity)
            WHERE e.performance_score > 0.5 {type_filter}
            RETURN e.uuid as uuid,
                   e.name as name,
                   e.type as type,
                   e.performance_score as performance,
                   e.confidence_score as confidence,
                   e.success_rate as success_rate,
                   e.user_interaction_count as interactions
            ORDER BY e.performance_score DESC
            LIMIT $limit
        """
        
        params = {"limit": limit}
        if entity_type:
            params["entity_type"] = entity_type
            
        result = await self.client.graphiti.execute_query(query, **params)
        return result
    
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
        
        result = await self.client.graphiti.execute_query(query)
        return {
            "relationship_analysis": result,
            "total_relationships": len(result),
            "high_accuracy_types": [
                r for r in result if r["avg_accuracy"] > 0.8
            ]
        }
    
    async def detect_knowledge_gaps(self) -> List[Dict]:
        """Detect potential knowledge gaps in the graph"""
        query = """
            MATCH (e:Entity)
            WHERE NOT (e)-[:RELATIONSHIP]-()
            RETURN e.uuid as isolated_entity_uuid,
                   e.name as entity_name,
                   e.type as entity_type,
                   e.performance_score as performance
            ORDER BY e.performance_score DESC
        """
        
        result = await self.client.graphiti.execute_query(query)
        return result
```

## Integration with Vector Database

### Cross-Modal Search Coordination
```python
class HybridSearchCoordinator:
    def __init__(self, 
                 graphiti_client: EnhancedGraphitiClient,
                 vector_db_client):
        self.graph_client = graphiti_client
        self.vector_client = vector_db_client
        
    async def hybrid_search(self, 
                          query: str,
                          query_embedding: List[float],
                          search_strategy: str = "adaptive") -> Dict[str, Any]:
        """Coordinate search across vector and graph databases"""
        
        # Step 1: Vector similarity search
        vector_results = await self.vector_client.search_chunks_weighted(
            query_embedding, match_count=20
        )
        
        # Step 2: Extract entities from vector results
        entity_uuids = []
        for result in vector_results:
            # Find graph entities related to this chunk
            related_entities = await self.graph_client.find_entities_by_document(
                result["document_id"]
            )
            entity_uuids.extend([e["uuid"] for e in related_entities])
        
        # Step 3: Graph-based expansion
        expanded_entities = []
        for entity_uuid in set(entity_uuids):
            related = await self.graph_client.find_related_entities(
                entity_uuid, max_depth=2
            )
            expanded_entities.extend(related)
        
        # Step 4: Re-rank results using graph context
        final_results = await self.rerank_with_graph_context(
            vector_results, expanded_entities
        )
        
        return {
            "results": final_results,
            "vector_count": len(vector_results),
            "graph_entities": len(expanded_entities),
            "search_strategy": search_strategy
        }
    
    async def rerank_with_graph_context(self, 
                                      vector_results: List[Dict],
                                      graph_entities: List[Dict]) -> List[Dict]:
        """Re-rank vector results using graph context"""
        # Implementation of sophisticated re-ranking algorithm
        # that combines vector similarity with graph connectivity
        pass
```

## Deployment and Monitoring

### Neo4j Cloud Setup
```python
# Neo4j Aura configuration
NEO4J_AURA_CONFIG = {
    "connection_uri": "neo4j+s://your-instance.databases.neo4j.io",
    "username": "neo4j",
    "password": "${NEO4J_PASSWORD}",
    "database": "neo4j",  # Default database
    "encrypted": True,
    "trust": "TRUST_SYSTEM_CA_SIGNED_CERTIFICATES",
    "max_connection_pool_size": 50,
    "connection_timeout": 15,
    "max_retry_time": 30
}

# Monitoring configuration
MONITORING_CONFIG = {
    "enable_query_logging": True,
    "slow_query_threshold_ms": 1000,
    "performance_sampling_rate": 0.1,
    "health_check_interval_seconds": 30
}
```

### Health Check and Performance Monitoring
```python
class GraphHealthMonitor:
    def __init__(self, graphiti_client: EnhancedGraphitiClient):
        self.client = graphiti_client
        
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check of the graph database"""
        try:
            # Basic connectivity
            await self.client.graphiti.execute_query("RETURN 1 as test")
            
            # Count entities and relationships
            counts = await self.client.graphiti.execute_query("""
                MATCH (e:Entity) 
                OPTIONAL MATCH ()-[r:RELATIONSHIP]->()
                RETURN COUNT(DISTINCT e) as entity_count,
                       COUNT(DISTINCT r) as relationship_count
            """)
            
            # Performance metrics
            performance = await self.client.graphiti.execute_query("""
                MATCH (e:Entity)
                RETURN AVG(e.performance_score) as avg_performance,
                       AVG(e.confidence_score) as avg_confidence,
                       COUNT(e) as total_entities
            """)
            
            return {
                "status": "healthy",
                "entity_count": counts[0]["entity_count"],
                "relationship_count": counts[0]["relationship_count"],
                "avg_performance": performance[0]["avg_performance"],
                "avg_confidence": performance[0]["avg_confidence"],
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
# Neo4j Configuration
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password
NEO4J_DATABASE=marketing_funnel_graph

# Graphiti Configuration
GRAPHITI_TEMPORAL_RESOLUTION=day
GRAPHITI_CONFIDENCE_THRESHOLD=0.7
GRAPHITI_MAX_ENTITIES_PER_EXTRACTION=50

# Performance Settings
GRAPH_MAX_SEARCH_DEPTH=3
GRAPH_MIN_CONFIDENCE_SCORE=0.6
GRAPH_CONNECTION_POOL_SIZE=50

# Monitoring
ENABLE_GRAPH_QUERY_LOGGING=true
SLOW_GRAPH_QUERY_THRESHOLD_MS=2000
GRAPH_HEALTH_CHECK_INTERVAL=30
```

This specification provides a comprehensive foundation for the Neo4j + Graphiti knowledge graph architecture, designed to work seamlessly with the vector database for a powerful hybrid RAG system focused on outcome-driven learning and continuous improvement.