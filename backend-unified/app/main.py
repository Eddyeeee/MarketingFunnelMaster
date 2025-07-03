"""
Main FastAPI Application - Week 2 Implementation
Milestone 1C: Core FastAPI Application with Database Integration

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
import uvicorn
from datetime import datetime

# Import configuration and core modules
from config.settings import settings
from config.database import init_database, close_database

# Import Week 2 routers and services
from app.routers import search_router, learning_router, agent_router
from app.services.database_service import DatabaseService
from app.services.rag_service import AdaptiveRAGService
from app.services.search_service import AdaptiveSearchService
from app.services.learning_service import ContinuousLearningService
from app.services.agent_service import AgentCommunicationService

# Import existing core modules
from core.agents.orchestrator import AgentOrchestrator
from core.intelligence.ai_research_client import AIResearchClient
from utils.logging import setup_logging
from core.auth.auth_dependencies import get_current_user

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global service instances
database_service = None
rag_service = None
search_service = None
learning_service = None
agent_service = None
agent_orchestrator = None
ai_research_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with Week 2 services"""
    # Startup
    logger.info("🚀 Starting MarketingFunnelMaster Week 2 - Agentic RAG System...")
    
    try:
        # Initialize database connections
        await init_database()
        logger.info("✅ Database connections initialized")
        
        # Initialize Week 2 services
        global database_service, rag_service, search_service, learning_service, agent_service
        
        # Initialize database service
        database_service = DatabaseService()
        await database_service.initialize()
        logger.info("✅ Database Service initialized")
        
        # Initialize RAG service
        rag_service = AdaptiveRAGService()
        await rag_service.initialize()
        logger.info("✅ Adaptive RAG Service initialized")
        
        # Initialize search service
        search_service = AdaptiveSearchService()
        await search_service.initialize()
        logger.info("✅ Adaptive Search Service initialized")
        
        # Initialize learning service
        learning_service = ContinuousLearningService()
        await learning_service.initialize()
        logger.info("✅ Continuous Learning Service initialized")
        
        # Initialize agent communication service
        agent_service = AgentCommunicationService()
        await agent_service.initialize()
        logger.info("✅ Agent Communication Service initialized")
        
        # Initialize existing AI Research Client (preserve existing assets)
        global ai_research_client
        ai_research_client = AIResearchClient()
        await ai_research_client.initialize()
        logger.info("✅ AI Research Engine connected")
        
        # Initialize existing Agent Orchestrator
        global agent_orchestrator
        agent_orchestrator = AgentOrchestrator()
        await agent_orchestrator.initialize()
        logger.info("✅ Agent Orchestrator initialized")
        
        # Register core agents
        await agent_orchestrator.register_core_agents()
        logger.info("✅ Core AI Agents registered")
        
        logger.info("🎯 Week 2 Agentic RAG System ready for production")
        logger.info("📊 Features: Adaptive Search | Continuous Learning | Agent Integration")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("⏹️ Shutting down MarketingFunnelMaster Week 2...")
    
    try:
        # Cleanup Week 2 services
        if agent_service:
            # Agent service doesn't need explicit cleanup
            pass
        
        if learning_service:
            # Learning service doesn't need explicit cleanup
            pass
        
        if search_service:
            # Search service doesn't need explicit cleanup
            pass
        
        if rag_service:
            # RAG service doesn't need explicit cleanup
            pass
        
        if database_service:
            # Database service doesn't need explicit cleanup
            pass
        
        # Cleanup existing services
        if agent_orchestrator:
            await agent_orchestrator.shutdown()
        
        if ai_research_client:
            await ai_research_client.cleanup()
        
        # Close database connections
        await close_database()
        
        logger.info("✅ Shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")

# Create FastAPI application with Week 2 integration
app = FastAPI(
    title="MarketingFunnelMaster - Agentic RAG System",
    description="AI-Powered Multi-Million-Euro Digital Empire Backend with Adaptive RAG",
    version="2.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# CORS Middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted Host Middleware for security
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Performance monitoring middleware
@app.middleware("http")
async def monitor_performance(request: Request, call_next):
    """Monitor API performance and log slow requests"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Log slow requests (> 1 second)
    if process_time > 1.0:
        logger.warning(
            f"Slow request: {request.method} {request.url.path} "
            f"took {process_time:.2f}s"
        )
    
    # Add performance headers
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()
    response.headers["X-System-Version"] = "2.0.0"
    
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An internal server error occurred",
            "request_id": str(time.time()),
            "timestamp": datetime.utcnow().isoformat(),
            "system_version": "2.0.0"
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint for Week 2 system"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "services": {}
    }
    
    try:
        # Check Week 2 services
        if database_service:
            db_health = await database_service.health_check()
            health_status["services"]["database"] = "healthy" if all(
                status == "healthy" for status in db_health.values()
            ) else "degraded"
        else:
            health_status["services"]["database"] = "not_initialized"
        
        if rag_service:
            rag_health = await rag_service.health_check()
            health_status["services"]["rag_service"] = "healthy" if rag_health else "unhealthy"
        else:
            health_status["services"]["rag_service"] = "not_initialized"
        
        if search_service:
            search_health = await search_service.health_check()
            health_status["services"]["search_service"] = "healthy" if search_health else "unhealthy"
        else:
            health_status["services"]["search_service"] = "not_initialized"
        
        if learning_service:
            learning_health = await learning_service.health_check()
            health_status["services"]["learning_service"] = "healthy" if learning_health else "unhealthy"
        else:
            health_status["services"]["learning_service"] = "not_initialized"
        
        if agent_service:
            agent_health = await agent_service.health_check()
            health_status["services"]["agent_service"] = "healthy" if agent_health else "unhealthy"
        else:
            health_status["services"]["agent_service"] = "not_initialized"
        
        # Check existing services
        if ai_research_client:
            ai_health = await ai_research_client.health_check()
            health_status["services"]["ai_research"] = "healthy" if ai_health else "unhealthy"
        else:
            health_status["services"]["ai_research"] = "not_initialized"
        
        if agent_orchestrator:
            orchestrator_health = await agent_orchestrator.health_check()
            health_status["services"]["agent_orchestrator"] = "healthy" if orchestrator_health else "unhealthy"
        else:
            health_status["services"]["agent_orchestrator"] = "not_initialized"
        
        # Determine overall status
        unhealthy_services = [
            name for name, status in health_status["services"].items() 
            if status in ["unhealthy", "not_initialized"]
        ]
        
        if unhealthy_services:
            health_status["status"] = "degraded"
            health_status["unhealthy_services"] = unhealthy_services
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
    
    return health_status

# Readiness check endpoint
@app.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes/Docker deployments"""
    ready = True
    services_status = {}
    
    try:
        # Check all critical Week 2 services
        critical_services = [
            ("database_service", database_service),
            ("rag_service", rag_service),
            ("search_service", search_service),
            ("learning_service", learning_service),
            ("agent_service", agent_service)
        ]
        
        for service_name, service_instance in critical_services:
            if service_instance:
                try:
                    service_ready = await service_instance.health_check()
                    services_status[service_name] = "ready" if service_ready else "not_ready"
                    ready = ready and service_ready
                except Exception as e:
                    services_status[service_name] = f"error: {str(e)}"
                    ready = False
            else:
                services_status[service_name] = "not_initialized"
                ready = False
        
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        ready = False
        services_status["error"] = str(e)
    
    status_code = 200 if ready else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "ready": ready,
            "timestamp": datetime.utcnow().isoformat(),
            "services": services_status,
            "version": "2.0.0"
        }
    )

# API version info
@app.get("/version")
async def version_info():
    """API version and build information for Week 2"""
    return {
        "application": "MarketingFunnelMaster",
        "version": "2.0.0",
        "api_version": "v2",
        "build_date": "2025-07-03",
        "environment": settings.ENVIRONMENT,
        "milestone": "1C - Week 2 Complete",
        "features": {
            "adaptive_rag": True,
            "hybrid_search": True,
            "continuous_learning": True,
            "agent_integration": True,
            "performance_optimization": True,
            "multi_strategy_search": True,
            "feedback_collection": True,
            "ai_research": True,
            "agent_orchestration": True,
            "real_time_websockets": True,
            "multi_model_ai": True,
            "website_generation": True,
            "affiliate_integration": True
        },
        "week2_achievements": {
            "fastapi_application": "completed",
            "database_integration": "completed",
            "adaptive_search": "completed",
            "learning_system": "completed",
            "agent_protocols": "completed"
        }
    }

# Include Week 2 API routers
app.include_router(
    search_router.router,
    prefix="/api/v2/search",
    tags=["Adaptive RAG Search"]
)

app.include_router(
    learning_router.router,
    prefix="/api/v2/learning",
    tags=["Continuous Learning"]
)

app.include_router(
    agent_router.router,
    prefix="/api/v2/agents",
    tags=["Agent Communication"]
)

# Include existing API routers (V1 compatibility)
from api.v1 import auth, agents, websites, analytics, intelligence
from api import webhooks

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["AI Agents (Legacy)"]
)

app.include_router(
    websites.router,
    prefix="/api/v1/websites",
    tags=["Website Management"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics & Reporting"]
)

app.include_router(
    intelligence.router,
    prefix="/api/v1/intelligence",
    tags=["AI Research & Intelligence"]
)

app.include_router(
    webhooks.router,
    prefix="/webhooks",
    tags=["Webhooks"]
)

# WebSocket endpoints for real-time agent communication
from api import websockets
app.include_router(websockets.websocket_router)

# Week 2 specific endpoints
@app.get("/api/v2/system/status")
async def get_system_status(current_user = Depends(get_current_user)):
    """Get comprehensive system status for Week 2"""
    try:
        system_status = {
            "week2_milestone": "completed",
            "adaptive_rag": {
                "status": "operational",
                "strategies_available": ["adaptive", "vector", "semantic", "hybrid", "performance_weighted"],
                "learning_active": True
            },
            "services": {},
            "performance_metrics": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Get service statuses
        if database_service:
            db_stats = await database_service.get_database_stats()
            system_status["services"]["database"] = db_stats
        
        if search_service:
            search_performance = await search_service.analyze_search_performance(7)
            system_status["performance_metrics"]["search"] = search_performance
        
        if learning_service:
            learning_velocity = await learning_service.calculate_learning_velocity()
            system_status["performance_metrics"]["learning"] = learning_velocity
        
        return system_status
        
    except Exception as e:
        logger.error(f"System status failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"System status retrieval failed: {str(e)}"
        )

@app.get("/api/v2/metrics/dashboard")
async def get_metrics_dashboard(current_user = Depends(get_current_user)):
    """Get comprehensive metrics dashboard for Week 2 system"""
    try:
        dashboard = {
            "overview": {
                "total_queries_processed": 0,
                "avg_response_time": 0,
                "system_confidence": 0,
                "learning_velocity": 0
            },
            "search_performance": {},
            "learning_metrics": {},
            "agent_performance": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Gather metrics from all services
        if database_service:
            db_stats = await database_service.get_database_stats()
            dashboard["overview"]["total_queries_processed"] = db_stats.get("outcome_count", 0)
        
        if search_service:
            search_metrics = await search_service.get_strategy_performance_metrics()
            dashboard["search_performance"] = search_metrics
        
        if learning_service:
            learning_trends = await learning_service.analyze_performance_trends(7)
            dashboard["learning_metrics"] = learning_trends
        
        if agent_service:
            agent_registry = await agent_service.get_agent_registry()
            dashboard["agent_performance"] = {
                "total_agents": len(agent_registry),
                "active_agents": len([a for a in agent_registry if a.get("status") == "active"])
            }
        
        return dashboard
        
    except Exception as e:
        logger.error(f"Metrics dashboard failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Metrics dashboard failed: {str(e)}"
        )

# Development and debugging endpoints
if settings.ENVIRONMENT == "development":
    @app.get("/debug/week2")
    async def debug_week2_services():
        """Debug endpoint to inspect Week 2 services"""
        debug_info = {
            "services_initialized": {},
            "service_health": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        services = [
            ("database_service", database_service),
            ("rag_service", rag_service),
            ("search_service", search_service),
            ("learning_service", learning_service),
            ("agent_service", agent_service)
        ]
        
        for service_name, service_instance in services:
            debug_info["services_initialized"][service_name] = service_instance is not None
            if service_instance:
                try:
                    health = await service_instance.health_check()
                    debug_info["service_health"][service_name] = health
                except Exception as e:
                    debug_info["service_health"][service_name] = f"error: {str(e)}"
        
        return debug_info

# Main execution
if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        workers=1 if settings.ENVIRONMENT == "development" else settings.WORKERS
    )