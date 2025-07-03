"""
Adaptive RAG Service - Week 2 Implementation
Milestone 1C: Strategic RAG coordination with multiple search strategies

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import time
import json

from app.services.database_service import DatabaseService
from app.models.rag_models import (
    QueryRequest, SearchResponse, SearchResult, SearchStrategy,
    QueryContext, BulkQueryRequest
)
from core.intelligence.ai_research_client import AIResearchClient

logger = logging.getLogger(__name__)

class AdaptiveRAGService:
    """Strategic RAG coordination with multiple search strategies"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.ai_client = None
        self._strategy_weights = {
            "vector": 0.4,      # 40% vector similarity
            "semantic": 0.3,    # 30% semantic search  
            "performance": 0.3  # 30% performance weighting
        }
        self._initialized = False
    
    async def initialize(self):
        """Initialize RAG service with database and AI connections"""
        try:
            await self.db_service.initialize()
            self.ai_client = AIResearchClient()
            await self.ai_client.initialize()
            self._initialized = True
            logger.info("✅ Adaptive RAG Service initialized")
        except Exception as e:
            logger.error(f"❌ RAG Service initialization failed: {e}")
            raise
    
    async def execute_hybrid_search(
        self,
        query: str,
        strategy: SearchStrategy = SearchStrategy.ADAPTIVE,
        context: Optional[QueryContext] = None,
        user_id: Optional[str] = None
    ) -> SearchResponse:
        """
        Strategic multi-strategy search coordination
        
        Implements Week 2 plan: 40% vector + 30% semantic + 30% performance
        """
        if not self._initialized:
            await self.initialize()
        
        start_time = time.time()
        query_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Executing hybrid search for query: {query[:50]}...")
            
            # Generate query embedding using AI client
            query_embedding = await self._generate_embedding(query)
            
            # Strategy selection based on request
            if strategy == SearchStrategy.ADAPTIVE:
                selected_strategy = await self._select_optimal_strategy(query, context)
            else:
                selected_strategy = strategy.value
            
            # Execute search based on selected strategy
            search_results = await self._execute_strategy(
                selected_strategy, query, query_embedding, context
            )
            
            # Calculate overall confidence score
            confidence_score = await self._calculate_confidence(search_results, context)
            
            # Create response
            response = SearchResponse(
                results=search_results,
                total_results=len(search_results),
                confidence_score=confidence_score,
                strategy_used=selected_strategy,
                query_id=query_id,
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
            
            # Store for learning (background task)
            asyncio.create_task(self._store_query_outcome(query_id, response, user_id))
            
            logger.info(f"Search completed: {response.processing_time_ms}ms, confidence: {confidence_score:.2f}")
            
            return response
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            raise
    
    async def execute_bulk_search(
        self,
        queries: List[QueryRequest],
        batch_optimization: bool = True,
        user_id: Optional[str] = None
    ) -> List[SearchResponse]:
        """
        Execute multiple search queries with batch optimization
        
        Optimized for agent-to-agent communication
        """
        start_time = time.time()
        results = []
        
        try:
            if batch_optimization and len(queries) > 5:
                # Parallel execution for batch optimization
                tasks = [
                    self.execute_hybrid_search(
                        query.query, query.search_strategy, query.context, user_id
                    )
                    for query in queries
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Handle exceptions in results
                processed_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        logger.error(f"Bulk search query {i} failed: {result}")
                        # Create error response
                        error_response = SearchResponse(
                            results=[],
                            total_results=0,
                            confidence_score=0.0,
                            strategy_used="error",
                            query_id=str(uuid.uuid4()),
                            processing_time_ms=0
                        )
                        processed_results.append(error_response)
                    else:
                        processed_results.append(result)
                        
                results = processed_results
                
            else:
                # Sequential execution for smaller batches
                for query in queries:
                    try:
                        result = await self.execute_hybrid_search(
                            query.query, query.search_strategy, query.context, user_id
                        )
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Sequential search failed: {e}")
                        results.append(SearchResponse(
                            results=[], total_results=0, confidence_score=0.0,
                            strategy_used="error", query_id=str(uuid.uuid4()),
                            processing_time_ms=0
                        ))
            
            total_time = int((time.time() - start_time) * 1000)
            logger.info(f"Bulk search completed: {len(queries)} queries in {total_time}ms")
            
            return results
            
        except Exception as e:
            logger.error(f"Bulk search failed: {e}")
            raise
    
    async def _execute_strategy(
        self,
        strategy: str,
        query: str,
        query_embedding: List[float],
        context: Optional[QueryContext]
    ) -> List[SearchResult]:
        """Execute specific search strategy"""
        
        if strategy == "vector":
            return await self._vector_search(query_embedding, context)
        elif strategy == "semantic":
            return await self._semantic_search(query, context)
        elif strategy == "hybrid":
            return await self._hybrid_search(query, query_embedding, context)
        elif strategy == "performance_weighted":
            return await self._performance_weighted_search(query_embedding, context)
        else:
            # Default to hybrid for unknown strategies
            return await self._hybrid_search(query, query_embedding, context)
    
    async def _vector_search(
        self, 
        query_embedding: List[float], 
        context: Optional[QueryContext]
    ) -> List[SearchResult]:
        """Vector similarity search using Week 1 functions"""
        try:
            # Use database service for vector search
            raw_results = await self.db_service.execute_vector_search(
                query_embedding=query_embedding,
                match_threshold=0.8,
                match_count=10,
                boost_performance=True
            )
            
            # Convert to SearchResult objects
            search_results = []
            for result in raw_results:
                search_result = SearchResult(
                    content=result.get('content', ''),
                    relevance_score=float(result.get('similarity', 0.0)),
                    confidence_score=float(result.get('confidence', 0.0)),
                    source_id=result.get('document_id'),
                    chunk_id=result.get('chunk_id'),
                    metadata=result.get('metadata', {})
                )
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    async def _semantic_search(
        self, 
        query: str, 
        context: Optional[QueryContext]
    ) -> List[SearchResult]:
        """Semantic search with full-text capabilities"""
        try:
            # Generate embedding for hybrid search
            query_embedding = await self._generate_embedding(query)
            
            # Use hybrid search from database service
            raw_results = await self.db_service.execute_hybrid_search(
                query_embedding=query_embedding,
                query_text=query,
                match_threshold=0.7,
                match_count=10
            )
            
            # Convert results
            search_results = []
            for result in raw_results:
                search_result = SearchResult(
                    content=result.get('content', ''),
                    relevance_score=float(result.get('combined_score', 0.0)),
                    confidence_score=float(result.get('confidence', 0.0)),
                    source_id=result.get('document_id'),
                    chunk_id=result.get('chunk_id'),
                    metadata=result.get('metadata', {})
                )
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
    
    async def _hybrid_search(
        self,
        query: str,
        query_embedding: List[float],
        context: Optional[QueryContext]
    ) -> List[SearchResult]:
        """
        Strategic hybrid search coordination
        
        Combines vector (40%) + semantic (30%) + performance (30%)
        """
        try:
            # Execute searches in parallel
            vector_task = self._vector_search(query_embedding, context)
            semantic_task = self._semantic_search(query, context)
            
            vector_results, semantic_results = await asyncio.gather(
                vector_task, semantic_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(vector_results, Exception):
                logger.error(f"Vector search in hybrid failed: {vector_results}")
                vector_results = []
            if isinstance(semantic_results, Exception):
                logger.error(f"Semantic search in hybrid failed: {semantic_results}")
                semantic_results = []
            
            # Coordinate results with strategic weighting
            coordinated_results = await self._coordinate_results(
                vector_results, semantic_results, context
            )
            
            return coordinated_results
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            return []
    
    async def _performance_weighted_search(
        self,
        query_embedding: List[float],
        context: Optional[QueryContext]
    ) -> List[SearchResult]:
        """Performance-weighted search using historical data"""
        try:
            # Use vector search with performance boosting
            raw_results = await self.db_service.execute_vector_search(
                query_embedding=query_embedding,
                match_threshold=0.75,
                match_count=15,
                boost_performance=True  # Enable performance weighting
            )
            
            # Convert and apply additional performance weighting
            search_results = []
            for result in raw_results:
                # Boost confidence based on historical performance
                base_confidence = float(result.get('confidence', 0.0))
                performance_boost = float(result.get('performance_score', 1.0))
                boosted_confidence = min(base_confidence * performance_boost, 1.0)
                
                search_result = SearchResult(
                    content=result.get('content', ''),
                    relevance_score=float(result.get('similarity', 0.0)),
                    confidence_score=boosted_confidence,
                    source_id=result.get('document_id'),
                    chunk_id=result.get('chunk_id'),
                    metadata={
                        **result.get('metadata', {}),
                        'performance_boost': performance_boost
                    }
                )
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Performance weighted search failed: {e}")
            return []
    
    async def _coordinate_results(
        self,
        vector_results: List[SearchResult],
        semantic_results: List[SearchResult],
        context: Optional[QueryContext]
    ) -> List[SearchResult]:
        """Strategic result coordination with confidence scoring"""
        try:
            # Create result map by chunk_id for deduplication
            result_map = {}
            
            # Add vector results with 40% weight
            for result in vector_results:
                chunk_id = result.chunk_id or result.source_id
                if chunk_id:
                    result_map[chunk_id] = {
                        "result": result,
                        "vector_score": result.relevance_score * 0.4,
                        "semantic_score": 0.0,
                        "sources": ["vector"]
                    }
            
            # Add semantic results with 30% weight
            for result in semantic_results:
                chunk_id = result.chunk_id or result.source_id
                if chunk_id:
                    if chunk_id in result_map:
                        # Update existing result
                        result_map[chunk_id]["semantic_score"] = result.relevance_score * 0.3
                        result_map[chunk_id]["sources"].append("semantic")
                    else:
                        # New result from semantic only
                        result_map[chunk_id] = {
                            "result": result,
                            "vector_score": 0.0,
                            "semantic_score": result.relevance_score * 0.3,
                            "sources": ["semantic"]
                        }
            
            # Calculate coordinated scores and create final results
            coordinated_results = []
            for chunk_id, data in result_map.items():
                # Calculate combined score with performance weighting (30%)
                performance_weight = 0.3
                base_score = data["vector_score"] + data["semantic_score"]
                performance_score = data["result"].confidence_score * performance_weight
                
                final_score = base_score + performance_score
                
                # Update result with coordinated scoring
                final_result = SearchResult(
                    content=data["result"].content,
                    relevance_score=min(final_score, 1.0),
                    confidence_score=data["result"].confidence_score,
                    source_id=data["result"].source_id,
                    chunk_id=data["result"].chunk_id,
                    metadata={
                        **data["result"].metadata,
                        "coordination_sources": data["sources"],
                        "vector_contribution": data["vector_score"],
                        "semantic_contribution": data["semantic_score"],
                        "performance_contribution": performance_score
                    }
                )
                coordinated_results.append(final_result)
            
            # Sort by relevance score and return top results
            coordinated_results.sort(key=lambda x: x.relevance_score, reverse=True)
            return coordinated_results[:10]
            
        except Exception as e:
            logger.error(f"Result coordination failed: {e}")
            # Return vector results as fallback
            return vector_results[:10] if vector_results else semantic_results[:10]
    
    async def _select_optimal_strategy(
        self,
        query: str,
        context: Optional[QueryContext]
    ) -> str:
        """AI-driven strategy selection based on query characteristics"""
        try:
            # Get strategy performance data
            strategy_performance = await self.db_service.get_strategy_performance()
            
            # Analyze query characteristics
            query_length = len(query.split())
            has_technical_terms = any(term in query.lower() for term in [
                "api", "code", "function", "algorithm", "technical", "implementation"
            ])
            
            # Strategy selection logic
            if query_length < 3:
                # Short queries work better with vector search
                return "vector"
            elif has_technical_terms:
                # Technical queries benefit from semantic search
                return "semantic"
            elif context and context.user_persona in ["BusinessOwner", "TechEarlyAdopter"]:
                # Business users prefer performance-optimized results
                return "performance_weighted"
            else:
                # Default to hybrid for complex queries
                return "hybrid"
                
        except Exception as e:
            logger.error(f"Strategy selection failed: {e}")
            return "hybrid"  # Safe default
    
    async def _calculate_confidence(
        self,
        search_results: List[SearchResult],
        context: Optional[QueryContext]
    ) -> float:
        """Calculate overall confidence score for search results"""
        if not search_results:
            return 0.0
        
        # Weighted average of individual confidence scores
        total_confidence = sum(result.confidence_score for result in search_results)
        avg_confidence = total_confidence / len(search_results)
        
        # Adjust based on result count and context
        result_count_factor = min(len(search_results) / 10, 1.0)  # More results = higher confidence
        context_factor = 1.0
        
        if context and context.user_persona:
            # Adjust confidence based on persona
            persona_adjustments = {
                "TechEarlyAdopter": 1.1,
                "BusinessOwner": 1.05,
                "RemoteDad": 1.0,
                "StudentHustler": 0.95
            }
            context_factor = persona_adjustments.get(context.user_persona.value, 1.0)
        
        final_confidence = avg_confidence * result_count_factor * context_factor
        return min(final_confidence, 1.0)
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate text embedding using AI client"""
        try:
            if self.ai_client:
                embedding = await self.ai_client.generate_embedding(text)
                return embedding
            else:
                # Fallback: create dummy embedding
                logger.warning("AI client not available, using dummy embedding")
                return [0.1] * 1536  # OpenAI embedding size
                
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return [0.1] * 1536  # Fallback
    
    async def _store_query_outcome(
        self,
        query_id: str,
        response: SearchResponse,
        user_id: Optional[str]
    ):
        """Store query outcome for learning system"""
        try:
            outcome_data = {
                "strategy_used": response.strategy_used,
                "user_satisfaction": 0.8,  # Default - will be updated with feedback
                "relevance_scores": [r.relevance_score for r in response.results],
                "response_time": response.processing_time_ms,
                "conversion_occurred": False,  # Will be updated with feedback
                "user_id": user_id
            }
            
            await self.db_service.store_query_outcome(
                query_id=query_id,
                response_id=str(uuid.uuid4()),
                outcome_data=outcome_data,
                confidence_score=response.confidence_score
            )
            
        except Exception as e:
            logger.error(f"Outcome storage failed: {e}")
    
    async def health_check(self) -> bool:
        """Health check for RAG service"""
        try:
            if not self._initialized:
                return False
            
            # Check database connectivity
            db_health = await self.db_service.health_check()
            db_healthy = all(status == "healthy" for status in db_health.values())
            
            # Check AI client
            ai_healthy = True
            if self.ai_client:
                ai_healthy = await self.ai_client.health_check()
            
            return db_healthy and ai_healthy
            
        except Exception as e:
            logger.error(f"RAG service health check failed: {e}")
            return False