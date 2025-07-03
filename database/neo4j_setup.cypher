// Neo4j Knowledge Graph Setup for Agentic RAG System
// Version: 1.0.0
// Created: 2025-07-03

// Create unique constraints for entity identification
CREATE CONSTRAINT entity_uuid_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.uuid IS UNIQUE;

CREATE CONSTRAINT relationship_id_unique IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT temporal_snapshot_id_unique IF NOT EXISTS
FOR (t:TemporalSnapshot) REQUIRE t.id IS UNIQUE;

// Create indexes for performance optimization
CREATE INDEX entity_name_index IF NOT EXISTS
FOR (e:Entity) ON (e.name);

CREATE INDEX entity_type_index IF NOT EXISTS
FOR (e:Entity) ON (e.type);

CREATE INDEX entity_performance_index IF NOT EXISTS
FOR (e:Entity) ON (e.performance_score);

CREATE INDEX entity_confidence_index IF NOT EXISTS
FOR (e:Entity) ON (e.confidence_score);

CREATE INDEX entity_temporal_index IF NOT EXISTS
FOR (e:Entity) ON (e.valid_from, e.valid_to);

CREATE INDEX relationship_type_index IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.relationship_type);

CREATE INDEX relationship_confidence_index IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.confidence_score);

CREATE INDEX relationship_strength_index IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.strength);

CREATE INDEX relationship_temporal_index IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.valid_from, r.valid_to);

CREATE INDEX temporal_snapshot_timestamp_index IF NOT EXISTS
FOR (t:TemporalSnapshot) ON (t.timestamp);

CREATE INDEX temporal_snapshot_entity_index IF NOT EXISTS
FOR (t:TemporalSnapshot) ON (t.entity_uuid);

// Create composite indexes for complex queries
CREATE INDEX entity_performance_type_index IF NOT EXISTS
FOR (e:Entity) ON (e.type, e.performance_score);

CREATE INDEX relationship_type_confidence_index IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.relationship_type, r.confidence_score);

// Full-text search indexes for content
CREATE FULLTEXT INDEX entity_content_search IF NOT EXISTS
FOR (e:Entity) ON EACH [e.name, e.description];

// Create initial system entities
CREATE (system:Entity {
    uuid: randomUUID(),
    name: "System",
    type: "system",
    description: "Root system entity for the Agentic RAG system",
    performance_score: 1.0,
    confidence_score: 1.0,
    relevance_score: 1.0,
    valid_from: datetime(),
    source_document_id: null,
    extraction_confidence: 1.0,
    user_interaction_count: 0,
    success_rate: 1.0,
    created_at: datetime(),
    updated_at: datetime(),
    tags: ["system", "root"],
    properties: {
        version: "1.0.0",
        environment: "production",
        capabilities: ["search", "learning", "optimization"]
    }
});

// Create performance tracking entity
CREATE (performance:Entity {
    uuid: randomUUID(),
    name: "Performance Tracker",
    type: "metric",
    description: "Tracks system-wide performance metrics",
    performance_score: 0.0,
    confidence_score: 1.0,
    relevance_score: 1.0,
    valid_from: datetime(),
    source_document_id: null,
    extraction_confidence: 1.0,
    user_interaction_count: 0,
    success_rate: 0.0,
    created_at: datetime(),
    updated_at: datetime(),
    tags: ["performance", "metrics", "system"],
    properties: {
        metric_type: "system_performance",
        measurement_frequency: "real_time"
    }
});

// Create learning system entity
CREATE (learning:Entity {
    uuid: randomUUID(),
    name: "Learning System",
    type: "agent",
    description: "Self-learning optimization agent",
    performance_score: 0.0,
    confidence_score: 0.5,
    relevance_score: 1.0,
    valid_from: datetime(),
    source_document_id: null,
    extraction_confidence: 1.0,
    user_interaction_count: 0,
    success_rate: 0.0,
    created_at: datetime(),
    updated_at: datetime(),
    tags: ["learning", "ai", "optimization"],
    properties: {
        agent_type: "learning_optimizer",
        learning_rate: 0.01,
        adaptation_speed: "medium"
    }
});

// Create relationships between system entities
MATCH (system:Entity {name: "System"}), (performance:Entity {name: "Performance Tracker"})
CREATE (system)-[:RELATIONSHIP {
    id: randomUUID(),
    relationship_type: "MONITORS",
    confidence_score: 1.0,
    strength: 1.0,
    valid_from: datetime(),
    prediction_accuracy: 0.0,
    usage_count: 0,
    properties: {
        monitoring_type: "continuous",
        update_frequency: "real_time"
    },
    created_at: datetime(),
    updated_at: datetime()
}]->(performance);

MATCH (system:Entity {name: "System"}), (learning:Entity {name: "Learning System"})
CREATE (system)-[:RELATIONSHIP {
    id: randomUUID(),
    relationship_type: "CONTAINS",
    confidence_score: 1.0,
    strength: 1.0,
    valid_from: datetime(),
    prediction_accuracy: 0.0,
    usage_count: 0,
    properties: {
        containment_type: "subsystem",
        integration_level: "deep"
    },
    created_at: datetime(),
    updated_at: datetime()
}]->(learning);

MATCH (learning:Entity {name: "Learning System"}), (performance:Entity {name: "Performance Tracker"})
CREATE (learning)-[:RELATIONSHIP {
    id: randomUUID(),
    relationship_type: "OPTIMIZES",
    confidence_score: 0.8,
    strength: 0.9,
    valid_from: datetime(),
    prediction_accuracy: 0.0,
    usage_count: 0,
    properties: {
        optimization_type: "continuous_improvement",
        feedback_loop: "real_time"
    },
    created_at: datetime(),
    updated_at: datetime()
}]->(performance);

// Create sample document entities for testing
CREATE (doc1:Entity {
    uuid: randomUUID(),
    name: "Marketing Strategy Guide",
    type: "document",
    description: "Comprehensive guide for digital marketing strategies",
    performance_score: 0.0,
    confidence_score: 0.7,
    relevance_score: 0.8,
    valid_from: datetime(),
    source_document_id: "doc_001",
    extraction_confidence: 0.9,
    user_interaction_count: 0,
    success_rate: 0.0,
    created_at: datetime(),
    updated_at: datetime(),
    tags: ["marketing", "strategy", "digital"],
    properties: {
        document_type: "guide",
        word_count: 5000,
        topics: ["SEO", "content marketing", "social media"]
    }
});

CREATE (concept1:Entity {
    uuid: randomUUID(),
    name: "SEO Optimization",
    type: "concept",
    description: "Search engine optimization techniques and strategies",
    performance_score: 0.0,
    confidence_score: 0.8,
    relevance_score: 0.9,
    valid_from: datetime(),
    source_document_id: "doc_001",
    extraction_confidence: 0.85,
    user_interaction_count: 0,
    success_rate: 0.0,
    created_at: datetime(),
    updated_at: datetime(),
    tags: ["seo", "optimization", "search"],
    properties: {
        concept_type: "technique",
        difficulty_level: "intermediate",
        related_tools: ["Google Analytics", "Search Console"]
    }
});

// Create relationship between document and concept
MATCH (doc1:Entity {name: "Marketing Strategy Guide"}), (concept1:Entity {name: "SEO Optimization"})
CREATE (doc1)-[:RELATIONSHIP {
    id: randomUUID(),
    relationship_type: "CONTAINS",
    confidence_score: 0.9,
    strength: 0.8,
    valid_from: datetime(),
    prediction_accuracy: 0.0,
    usage_count: 0,
    properties: {
        section: "Chapter 3",
        relevance: "high",
        coverage: "detailed"
    },
    created_at: datetime(),
    updated_at: datetime()
}]->(concept1);

// Create initial temporal snapshot
MATCH (system:Entity {name: "System"})
CREATE (snapshot:TemporalSnapshot {
    id: randomUUID(),
    entity_uuid: system.uuid,
    timestamp: datetime(),
    state: system.properties,
    performance_metrics: {
        performance_score: system.performance_score,
        confidence_score: system.confidence_score,
        relevance_score: system.relevance_score,
        success_rate: system.success_rate
    },
    changed_properties: ["created"],
    change_trigger: "system_initialization",
    validated: true,
    validation_confidence: 1.0
})
CREATE (system)-[:HAS_SNAPSHOT]->(snapshot);

// Create procedures for common operations

// Procedure to add entity with performance tracking
CALL apoc.custom.asProcedure(
'addEntityWithTracking',
'MERGE (e:Entity {uuid: $uuid}) 
 SET e += $properties,
     e.created_at = datetime(),
     e.updated_at = datetime(),
     e.performance_score = coalesce($properties.performance_score, 0.0),
     e.confidence_score = coalesce($properties.confidence_score, 0.5)
 RETURN e',
'write',
[['uuid','STRING'], ['properties','MAP']],
[['entity','NODE']],
'Add entity with automatic performance tracking setup'
);

// Procedure to create relationship with validation
CALL apoc.custom.asProcedure(
'createValidatedRelationship',
'MATCH (source:Entity {uuid: $source_uuid}), (target:Entity {uuid: $target_uuid})
 CREATE (source)-[r:RELATIONSHIP {
     id: randomUUID(),
     relationship_type: $relationship_type,
     confidence_score: $confidence_score,
     strength: coalesce($strength, 0.5),
     valid_from: datetime(),
     prediction_accuracy: 0.0,
     usage_count: 0,
     properties: coalesce($properties, {}),
     created_at: datetime(),
     updated_at: datetime()
 }]->(target)
 RETURN r',
'write',
[['source_uuid','STRING'], ['target_uuid','STRING'], ['relationship_type','STRING'], ['confidence_score','FLOAT'], ['strength','FLOAT'], ['properties','MAP']],
[['relationship','RELATIONSHIP']],
'Create relationship with automatic validation and tracking'
);

// Procedure to update entity performance
CALL apoc.custom.asProcedure(
'updateEntityPerformance',
'MATCH (e:Entity {uuid: $entity_uuid})
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
 RETURN e, snapshot',
'write',
[['entity_uuid','STRING'], ['performance_score','FLOAT'], ['confidence_score','FLOAT'], ['relevance_score','FLOAT'], ['success_rate','FLOAT']],
[['entity','NODE'], ['snapshot','NODE']],
'Update entity performance metrics with temporal tracking'
);

// Procedure for intelligent entity search
CALL apoc.custom.asProcedure(
'intelligentEntitySearch',
'MATCH (e:Entity)
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
 RETURN e, relevance_score',
'read',
[['search_term','STRING'], ['limit','INTEGER']],
[['entity','NODE'], ['relevance_score','FLOAT']],
'Intelligent entity search with relevance scoring'
);

// Procedure for relationship strength analysis
CALL apoc.custom.asProcedure(
'analyzeRelationshipStrength',
'MATCH (source:Entity)-[r:RELATIONSHIP]->(target:Entity)
 WHERE r.relationship_type = $relationship_type
 WITH r, 
      r.confidence_score * 0.4 + 
      r.strength * 0.3 + 
      (r.usage_count / 100.0) * 0.2 +
      r.prediction_accuracy * 0.1 as composite_strength
 RETURN 
     r.relationship_type as type,
     avg(composite_strength) as avg_strength,
     count(r) as total_relationships,
     max(composite_strength) as max_strength,
     min(composite_strength) as min_strength',
'read',
[['relationship_type','STRING']],
[['type','STRING'], ['avg_strength','FLOAT'], ['total_relationships','INTEGER'], ['max_strength','FLOAT'], ['min_strength','FLOAT']],
'Analyze relationship strength patterns'
);

// Create monitoring queries for health checks
// Query to check system health
CALL apoc.custom.asFunction(
'systemHealthCheck',
'MATCH (e:Entity) 
 OPTIONAL MATCH ()-[r:RELATIONSHIP]->()
 RETURN {
     total_entities: count(DISTINCT e),
     total_relationships: count(DISTINCT r),
     avg_performance: avg(e.performance_score),
     avg_confidence: avg(e.confidence_score),
     high_performers: size([e IN collect(DISTINCT e) WHERE e.performance_score > 0.8]),
     timestamp: toString(datetime())
 }',
'read',
null,
'MAP',
'Get comprehensive system health metrics'
);

// Query to detect knowledge gaps
CALL apoc.custom.asFunction(
'detectKnowledgeGaps',
'MATCH (e:Entity)
 WHERE NOT (e)-[:RELATIONSHIP]-()
 RETURN collect({
     uuid: e.uuid,
     name: e.name,
     type: e.type,
     performance_score: e.performance_score,
     isolation_risk: CASE 
         WHEN e.performance_score > 0.7 THEN "high"
         WHEN e.performance_score > 0.4 THEN "medium"
         ELSE "low"
     END
 })',
'read',
null,
'LIST OF MAP',
'Detect isolated entities that may indicate knowledge gaps'
);

// Performance optimization procedures
CALL apoc.custom.asProcedure(
'optimizePerformance',
'// Update relationship strengths based on usage
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
 
 RETURN relationships_updated, count(t) as snapshots_cleaned',
'write',
null,
[['relationships_updated','INTEGER'], ['snapshots_cleaned','INTEGER']],
'Optimize graph performance by updating strengths and cleaning old data'
);

// Success verification
MATCH (e:Entity)
OPTIONAL MATCH ()-[r:RELATIONSHIP]->()
OPTIONAL MATCH (t:TemporalSnapshot)
RETURN 
    count(DISTINCT e) as total_entities,
    count(DISTINCT r) as total_relationships, 
    count(DISTINCT t) as total_snapshots,
    "Neo4j knowledge graph setup completed successfully!" as status;