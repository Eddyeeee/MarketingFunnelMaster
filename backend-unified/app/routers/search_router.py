"""
RAG Search Router - Week 2 Implementation
Milestone 1C: Adaptive RAG Search Endpoints

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import time
import logging
from datetime import datetime

from app.services.rag_service import AdaptiveRAGService
from app.services.search_service import AdaptiveSearchService
from app.models.rag_models import (
    QueryRequest, SearchResponse, BulkQueryRequest, 
    SearchStrategy, DeviceType, UserPersona
)
from core.auth.auth_dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
rag_service = AdaptiveRAGService()
search_service = AdaptiveSearchService()

@router.post("/query", response_model=SearchResponse)
async def execute_search_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Execute adaptive RAG search query with multi-strategy coordination
    
    Strategic implementation of hybrid search following Week 2 plan:
    - Vector similarity (40%)
    - Semantic search (30%) 
    - Performance weighting (30%)
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing search query: {request.query[:50]}...")
        
        # Execute adaptive RAG search
        response = await rag_service.execute_hybrid_search(
            query=request.query,
            strategy=request.search_strategy,
            context=request.context,
            user_id=current_user.id if current_user else None
        )
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        response.processing_time_ms = processing_time
        
        # Background learning signal generation
        background_tasks.add_task(
            search_service.generate_learning_signals,
            request, response, current_user
        )
        
        # Log performance metrics
        logger.info(
            f"Search completed: {processing_time}ms, "
            f"confidence: {response.confidence_score:.2f}, "
            f"strategy: {response.strategy_used}"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Search query failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search processing failed: {str(e)}"
        )

@router.post("/bulk", response_model=Dict[str, Any])
async def execute_bulk_search(
    request: BulkQueryRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Execute multiple search queries with batch optimization
    
    Optimized for agent-to-agent communication and bulk processing
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing bulk search: {len(request.queries)} queries")
        
        # Execute batch search with optimization
        batch_results = await rag_service.execute_bulk_search(
            queries=request.queries,
            batch_optimization=request.batch_optimization,
            user_id=current_user.id if current_user else None
        )
        
        # Calculate batch performance metrics
        total_processing_time = int((time.time() - start_time) * 1000)
        avg_processing_time = total_processing_time / len(request.queries)
        
        # Background batch learning
        background_tasks.add_task(
            search_service.process_batch_learning,
            request, batch_results, current_user
        )
        
        response = {
            "batch_results": batch_results,
            "batch_performance": {
                "total_queries": len(request.queries),
                "total_processing_time_ms": total_processing_time,
                "avg_processing_time_ms": int(avg_processing_time),
                "batch_optimization_used": request.batch_optimization,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        logger.info(f"Bulk search completed: {total_processing_time}ms for {len(request.queries)} queries")
        
        return response
        
    except Exception as e:
        logger.error(f"Bulk search failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Bulk search processing failed: {str(e)}"
        )

@router.get("/strategies", response_model=List[Dict[str, Any]])
async def get_available_strategies():
    """
    Get available search strategies and their performance metrics
    """
    try:
        strategies = await search_service.get_strategy_performance_metrics()
        return strategies
        
    except Exception as e:
        logger.error(f"Strategy retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Strategy retrieval failed: {str(e)}"
        )

@router.get("/performance", response_model=Dict[str, Any])
async def get_search_performance(
    time_window_days: int = 7,
    current_user = Depends(get_current_user)
):
    """
    Get search performance analytics for optimization
    
    Leverages Week 1 analyze_search_performance function
    """
    try:
        performance_data = await search_service.analyze_search_performance(
            time_window_days=time_window_days,
            user_id=current_user.id if current_user else None
        )
        
        return performance_data
        
    except Exception as e:
        logger.error(f"Performance analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Performance analysis failed: {str(e)}"
        )

@router.post("/optimize", response_model=Dict[str, Any])
async def trigger_search_optimization(
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Trigger search strategy optimization based on performance data
    
    Uses continuous learning from Week 2 plan
    """
    try:
        # Background optimization task
        background_tasks.add_task(
            search_service.optimize_search_strategies,
            user_id=current_user.id if current_user else None
        )
        
        return {
            "optimization_triggered": True,
            "message": "Search optimization started in background",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Search optimization trigger failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search optimization failed: {str(e)}"
        )

# Health check for search system
@router.get("/health")
async def search_health_check():
    """Health check for search services"""
    try:
        rag_health = await rag_service.health_check()
        search_health = await search_service.health_check()
        
        return {
            "status": "healthy" if rag_health and search_health else "degraded",
            "services": {
                "rag_service": "healthy" if rag_health else "unhealthy",
                "search_service": "healthy" if search_health else "unhealthy"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Search health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }