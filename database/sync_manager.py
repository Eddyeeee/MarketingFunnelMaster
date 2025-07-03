"""
Database Synchronization Manager for Agentic RAG System
Handles synchronization between Neon PostgreSQL and Neo4j databases
Version: 1.0.0
Created: 2025-07-03
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from uuid import UUID
import json
from enum import Enum

from models.unified_models import (
    UniversalEntity, EntityRelationship, PerformanceMetrics, 
    EntityType, RelationshipType, OutcomeEvent
)
from database.database_config import db_manager
from database.neo4j_manager import graph_manager

logger = logging.getLogger(__name__)

class SyncDirection(str, Enum):
    POSTGRES_TO_NEO4J = "postgres_to_neo4j"
    NEO4J_TO_POSTGRES = "neo4j_to_postgres"
    BIDIRECTIONAL = "bidirectional"

class ConflictResolution(str, Enum):
    LATEST_WINS = "latest_wins"
    POSTGRES_PRIORITY = "postgres_priority"
    NEO4J_PRIORITY = "neo4j_priority"
    MANUAL_REVIEW = "manual_review"

class SyncConfiguration:
    """Configuration for database synchronization"""
    
    def __init__(self):
        self.sync_frequency_seconds = 300  # 5 minutes
        self.batch_size = 100
        self.conflict_resolution = ConflictResolution.LATEST_WINS
        self.enable_real_time_sync = True
        self.sync_performance_metrics = True
        self.sync_learning_signals = True
        self.sync_relationships = True
        self.max_retry_attempts = 3
        self.retry_delay_seconds = 5

class SyncStatus:
    """Track synchronization status"""
    
    def __init__(self):
        self.last_sync_timestamp = None
        self.entities_synced = 0
        self.relationships_synced = 0
        self.conflicts_detected = 0
        self.conflicts_resolved = 0
        self.errors_encountered = 0
        self.sync_duration_seconds = 0.0
        self.next_scheduled_sync = None

class DatabaseSyncManager:
    """Manages synchronization between PostgreSQL and Neo4j databases"""
    
    def __init__(self, config: SyncConfiguration = None):
        self.config = config or SyncConfiguration()
        self.status = SyncStatus()
        self.is_syncing = False
        self.sync_lock = asyncio.Lock()
        
    async def initialize(self):
        """Initialize sync manager"""
        # Ensure both database managers are initialized
        if not db_manager.is_initialized:
            await db_manager.initialize()
        if not graph_manager.is_initialized:
            await graph_manager.initialize()
        
        logger.info("Database sync manager initialized")
    
    async def sync_entity(self, entity: UniversalEntity, 
                         direction: SyncDirection = SyncDirection.BIDIRECTIONAL) -> bool:
        """Sync a single entity between databases"""
        try:
            if direction in [SyncDirection.POSTGRES_TO_NEO4J, SyncDirection.BIDIRECTIONAL]:
                await self._sync_entity_to_neo4j(entity)
            
            if direction in [SyncDirection.NEO4J_TO_POSTGRES, SyncDirection.BIDIRECTIONAL]:
                await self._sync_entity_to_postgres(entity)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync entity {entity.id}: {e}")
            return False
    
    async def _sync_entity_to_postgres(self, entity: UniversalEntity) -> None:
        """Sync entity to PostgreSQL"""
        postgres_data = entity.to_postgres_dict()
        
        async with db_manager.get_connection() as conn:
            # Check if entity exists
            existing = await conn.fetchrow(
                "SELECT id, updated_at FROM documents WHERE id = $1",
                postgres_data["id"]
            )
            
            if existing:
                # Update existing entity
                if self._should_update(existing["updated_at"], entity.updated_at):
                    await conn.execute("""
                        UPDATE documents SET
                            title = $2,
                            source = $3,
                            content = $4,
                            content_type = $5,
                            metadata = $6,
                            engagement_score = $7,
                            conversion_rate = $8,
                            updated_at = $9,
                            content_vector = $10,
                            is_active = $11
                        WHERE id = $1
                    """, 
                    postgres_data["id"], postgres_data["title"], postgres_data["source"],
                    postgres_data["content"], postgres_data["content_type"], postgres_data["metadata"],
                    postgres_data["engagement_score"], postgres_data["conversion_rate"],
                    postgres_data["updated_at"], postgres_data["content_vector"],
                    postgres_data["is_active"]
                    )
            else:
                # Insert new entity
                await conn.execute("""
                    INSERT INTO documents (
                        id, title, source, content, content_type, metadata,
                        engagement_score, conversion_rate, created_at, updated_at,
                        content_vector, is_active
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                """,
                postgres_data["id"], postgres_data["title"], postgres_data["source"],
                postgres_data["content"], postgres_data["content_type"], postgres_data["metadata"],
                postgres_data["engagement_score"], postgres_data["conversion_rate"],
                postgres_data["created_at"], postgres_data["updated_at"],
                postgres_data["content_vector"], postgres_data["is_active"]
                )
    
    async def _sync_entity_to_neo4j(self, entity: UniversalEntity) -> None:
        """Sync entity to Neo4j"""
        neo4j_data = entity.to_neo4j_dict()
        
        # Check if entity exists in Neo4j
        existing_query = "MATCH (e:Entity {uuid: $uuid}) RETURN e.updated_at as updated_at"
        existing_result = await graph_manager.execute_query(
            existing_query, {"uuid": neo4j_data["uuid"]}
        )
        
        if existing_result:
            # Update existing entity
            existing_updated = existing_result[0]["updated_at"]
            if self._should_update(existing_updated, entity.updated_at):
                update_query = """
                    MATCH (e:Entity {uuid: $uuid})
                    SET e += $properties
                    RETURN e.uuid as uuid
                """
                await graph_manager.execute_query(
                    update_query, 
                    {"uuid": neo4j_data["uuid"], "properties": neo4j_data}
                )
        else:
            # Create new entity
            create_query = """
                CREATE (e:Entity $properties)
                RETURN e.uuid as uuid
            """
            await graph_manager.execute_query(
                create_query, {"properties": neo4j_data}
            )
    
    async def sync_relationship(self, relationship: EntityRelationship) -> bool:
        """Sync relationship to Neo4j (relationships are primarily stored in Neo4j)"""
        try:
            relationship_data = {
                "id": str(relationship.id),
                "relationship_type": relationship.relationship_type.value,
                "confidence_score": relationship.confidence,
                "strength": relationship.strength,
                "valid_from": relationship.valid_from,
                "valid_to": relationship.valid_to,
                "prediction_accuracy": relationship.performance.prediction_accuracy,
                "usage_count": relationship.usage_count,
                "properties": relationship.context_metadata,
                "created_at": relationship.valid_from,
                "updated_at": datetime.now()
            }
            
            # Check if relationship exists
            existing_query = """
                MATCH ()-[r:RELATIONSHIP {id: $id}]->()
                RETURN r.updated_at as updated_at
            """
            existing_result = await graph_manager.execute_query(
                existing_query, {"id": relationship_data["id"]}
            )
            
            if existing_result:
                # Update existing relationship
                update_query = """
                    MATCH ()-[r:RELATIONSHIP {id: $id}]->()
                    SET r += $properties
                    RETURN r.id as id
                """
                await graph_manager.execute_query(
                    update_query,
                    {"id": relationship_data["id"], "properties": relationship_data}
                )
            else:
                # Create new relationship
                create_query = """
                    MATCH (source:Entity {uuid: $source_uuid})
                    MATCH (target:Entity {uuid: $target_uuid})
                    CREATE (source)-[r:RELATIONSHIP $properties]->(target)
                    RETURN r.id as id
                """
                await graph_manager.execute_query(
                    create_query,
                    {
                        "source_uuid": str(relationship.source_entity_id),
                        "target_uuid": str(relationship.target_entity_id),
                        "properties": relationship_data
                    }
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync relationship {relationship.id}: {e}")
            return False
    
    async def sync_performance_metrics(self, entity_id: UUID, 
                                     metrics: PerformanceMetrics) -> bool:
        """Sync performance metrics across both databases"""
        try:
            # Update PostgreSQL
            async with db_manager.get_connection() as conn:
                await conn.execute("""
                    UPDATE documents SET
                        engagement_score = $2,
                        conversion_rate = $3,
                        updated_at = NOW()
                    WHERE id = $1
                """, str(entity_id), metrics.engagement_score, metrics.conversion_rate)
            
            # Update Neo4j
            await graph_manager.execute_query("""
                MATCH (e:Entity {uuid: $uuid})
                SET e.performance_score = $performance_score,
                    e.confidence_score = $confidence_score,
                    e.relevance_score = $relevance_score,
                    e.success_rate = $success_rate,
                    e.updated_at = datetime()
                RETURN e.uuid as uuid
            """, {
                "uuid": str(entity_id),
                "performance_score": metrics.relevance_score,
                "confidence_score": metrics.confidence_score,
                "relevance_score": metrics.relevance_score,
                "success_rate": metrics.success_rate
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync performance metrics for {entity_id}: {e}")
            return False
    
    async def full_sync(self, direction: SyncDirection = SyncDirection.BIDIRECTIONAL) -> Dict[str, Any]:
        """Perform full database synchronization"""
        async with self.sync_lock:
            if self.is_syncing:
                return {"status": "sync_already_in_progress"}
            
            self.is_syncing = True
            sync_start = datetime.now()
            
            try:
                self.status = SyncStatus()
                self.status.last_sync_timestamp = sync_start
                
                # Sync entities
                await self._sync_all_entities(direction)
                
                # Sync relationships
                if self.config.sync_relationships:
                    await self._sync_all_relationships()
                
                # Sync performance metrics
                if self.config.sync_performance_metrics:
                    await self._sync_all_performance_metrics()
                
                self.status.sync_duration_seconds = (datetime.now() - sync_start).total_seconds()
                self.status.next_scheduled_sync = datetime.now() + timedelta(
                    seconds=self.config.sync_frequency_seconds
                )
                
                return {
                    "status": "sync_completed",
                    "entities_synced": self.status.entities_synced,
                    "relationships_synced": self.status.relationships_synced,
                    "conflicts_resolved": self.status.conflicts_resolved,
                    "duration_seconds": self.status.sync_duration_seconds
                }
                
            except Exception as e:
                logger.error(f"Full sync failed: {e}")
                return {
                    "status": "sync_failed",
                    "error": str(e),
                    "duration_seconds": (datetime.now() - sync_start).total_seconds()
                }
            finally:
                self.is_syncing = False
    
    async def _sync_all_entities(self, direction: SyncDirection) -> None:
        """Sync all entities between databases"""
        if direction in [SyncDirection.POSTGRES_TO_NEO4J, SyncDirection.BIDIRECTIONAL]:
            # Get entities from PostgreSQL
            async with db_manager.get_connection() as conn:
                entities = await conn.fetch("""
                    SELECT id, title, source, content, content_type, metadata,
                           engagement_score, conversion_rate, created_at, updated_at,
                           is_active
                    FROM documents
                    WHERE is_active = true
                    ORDER BY updated_at DESC
                """)
                
                for entity_row in entities:
                    try:
                        # Convert to UniversalEntity and sync to Neo4j
                        entity = self._postgres_row_to_entity(entity_row)
                        await self._sync_entity_to_neo4j(entity)
                        self.status.entities_synced += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to sync entity {entity_row['id']}: {e}")
                        self.status.errors_encountered += 1
        
        if direction in [SyncDirection.NEO4J_TO_POSTGRES, SyncDirection.BIDIRECTIONAL]:
            # Get entities from Neo4j
            neo4j_entities = await graph_manager.execute_query("""
                MATCH (e:Entity)
                WHERE e.type IN ['document', 'chunk']
                RETURN e.uuid as uuid, e.name as name, e.type as type,
                       e.performance_score as performance_score,
                       e.confidence_score as confidence_score,
                       e.created_at as created_at,
                       e.updated_at as updated_at,
                       e.properties as properties
                ORDER BY e.updated_at DESC
            """)
            
            for entity_data in neo4j_entities:
                try:
                    # Convert to UniversalEntity and sync to PostgreSQL
                    entity = self._neo4j_data_to_entity(entity_data)
                    await self._sync_entity_to_postgres(entity)
                    self.status.entities_synced += 1
                    
                except Exception as e:
                    logger.error(f"Failed to sync entity {entity_data['uuid']}: {e}")
                    self.status.errors_encountered += 1
    
    async def _sync_all_relationships(self) -> None:
        """Sync all relationships from Neo4j"""
        relationships = await graph_manager.execute_query("""
            MATCH (source:Entity)-[r:RELATIONSHIP]->(target:Entity)
            RETURN r.id as id, source.uuid as source_uuid, target.uuid as target_uuid,
                   r.relationship_type as relationship_type, r.confidence_score as confidence,
                   r.strength as strength, r.usage_count as usage_count,
                   r.created_at as created_at, r.updated_at as updated_at
        """)
        
        for rel_data in relationships:
            self.status.relationships_synced += 1
    
    async def _sync_all_performance_metrics(self) -> None:
        """Sync performance metrics between databases"""
        # This could involve complex reconciliation logic
        # For now, we'll prioritize Neo4j performance data
        pass
    
    def _should_update(self, existing_timestamp: datetime, new_timestamp: datetime) -> bool:
        """Determine if entity should be updated based on timestamps"""
        if self.config.conflict_resolution == ConflictResolution.LATEST_WINS:
            return new_timestamp > existing_timestamp
        elif self.config.conflict_resolution == ConflictResolution.POSTGRES_PRIORITY:
            return True  # Always update from PostgreSQL
        elif self.config.conflict_resolution == ConflictResolution.NEO4J_PRIORITY:
            return False  # Never update from other source
        else:
            # Manual review - log conflict
            logger.warning(f"Conflict detected: existing={existing_timestamp}, new={new_timestamp}")
            self.status.conflicts_detected += 1
            return False
    
    def _postgres_row_to_entity(self, row) -> UniversalEntity:
        """Convert PostgreSQL row to UniversalEntity"""
        from models.unified_models import UniversalEntity, EntityType, PerformanceMetrics
        
        metadata = json.loads(row['metadata']) if row['metadata'] else {}
        
        performance = PerformanceMetrics(
            engagement_score=row['engagement_score'] or 0.0,
            conversion_rate=row['conversion_rate'] or 0.0
        )
        
        return UniversalEntity(
            id=UUID(row['id']),
            type=EntityType(row['content_type']),
            name=row['title'],
            content=row['content'],
            metadata=metadata,
            performance=performance,
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            is_active=row['is_active']
        )
    
    def _neo4j_data_to_entity(self, data) -> UniversalEntity:
        """Convert Neo4j data to UniversalEntity"""
        from models.unified_models import UniversalEntity, EntityType, PerformanceMetrics
        
        properties = data.get('properties', {})
        performance_data = properties.get('performance_metrics', {})
        
        performance = PerformanceMetrics(
            relevance_score=data.get('performance_score', 0.0),
            confidence_score=data.get('confidence_score', 0.0),
            **performance_data
        )
        
        return UniversalEntity(
            id=UUID(data['uuid']),
            type=EntityType(data['type']),
            name=data['name'],
            content=properties.get('content_preview', ''),
            metadata=properties,
            performance=performance,
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
    
    async def schedule_periodic_sync(self) -> None:
        """Schedule periodic synchronization"""
        while True:
            try:
                await asyncio.sleep(self.config.sync_frequency_seconds)
                
                if not self.is_syncing:
                    logger.info("Starting scheduled sync")
                    result = await self.full_sync()
                    logger.info(f"Scheduled sync completed: {result}")
                else:
                    logger.info("Skipping scheduled sync - sync already in progress")
                    
            except Exception as e:
                logger.error(f"Scheduled sync failed: {e}")
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get current synchronization status"""
        return {
            "is_syncing": self.is_syncing,
            "last_sync": self.status.last_sync_timestamp.isoformat() if self.status.last_sync_timestamp else None,
            "entities_synced": self.status.entities_synced,
            "relationships_synced": self.status.relationships_synced,
            "conflicts_detected": self.status.conflicts_detected,
            "conflicts_resolved": self.status.conflicts_resolved,
            "errors_encountered": self.status.errors_encountered,
            "last_sync_duration": self.status.sync_duration_seconds,
            "next_scheduled_sync": self.status.next_scheduled_sync.isoformat() if self.status.next_scheduled_sync else None
        }

# Global sync manager instance
sync_manager = DatabaseSyncManager()

# Helper functions
async def initialize_sync_manager():
    """Initialize the global sync manager"""
    await sync_manager.initialize()

async def sync_entity_across_databases(entity: UniversalEntity) -> bool:
    """Sync entity across all databases"""
    return await sync_manager.sync_entity(entity)

async def sync_performance_update(entity_id: UUID, metrics: PerformanceMetrics) -> bool:
    """Sync performance metrics update"""
    return await sync_manager.sync_performance_metrics(entity_id, metrics)

async def start_periodic_sync():
    """Start periodic synchronization in background"""
    asyncio.create_task(sync_manager.schedule_periodic_sync())

if __name__ == "__main__":
    # Test the sync manager
    async def test_sync():
        try:
            await initialize_sync_manager()
            
            # Get sync status
            status = await sync_manager.get_sync_status()
            print(f"Sync status: {status}")
            
            # Perform test sync
            result = await sync_manager.full_sync()
            print(f"Sync result: {result}")
            
        except Exception as e:
            print(f"Sync test failed: {e}")
    
    asyncio.run(test_sync())