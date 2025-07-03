#!/usr/bin/env python3
"""
MarketingFunnelMaster - Unified FastAPI Backend
Version: 1.0
Main Application Entry Point

Executor: Claude Code (HTD-Executor-Ebene)
Erstellt: 2025-07-03
"""

from fastapi import FastAPI, Request, HTTPException
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
from api.v1 import auth, agents, websites, analytics, intelligence
from api.webhooks import webhooks
from core.agents.orchestrator import AgentOrchestrator
from core.intelligence.ai_research_client import AIResearchClient
from utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global instances
agent_orchestrator = None
ai_research_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("🚀 Starting MarketingFunnelMaster Unified Backend...")
    
    # Initialize database connections
    await init_database()
    logger.info("✅ Database connections initialized")
    
    # Initialize AI Research Client (preserve existing assets)
    global ai_research_client
    ai_research_client = AIResearchClient()
    await ai_research_client.initialize()
    logger.info("✅ AI Research Engine connected")
    
    # Initialize Agent Orchestrator
    global agent_orchestrator
    agent_orchestrator = AgentOrchestrator()
    await agent_orchestrator.initialize()
    logger.info("✅ Agent Orchestrator initialized")
    
    # Register core agents
    await agent_orchestrator.register_core_agents()
    logger.info("✅ Core AI Agents registered")
    
    logger.info("🎯 MarketingFunnelMaster Backend ready for 1500+ websites")
    
    yield
    
    # Shutdown
    logger.info("⏹️ Shutting down MarketingFunnelMaster Backend...")
    
    # Cleanup agent orchestrator
    if agent_orchestrator:
        await agent_orchestrator.shutdown()
    
    # Cleanup AI research client
    if ai_research_client:
        await ai_research_client.cleanup()
    
    # Close database connections
    await close_database()
    
    logger.info("✅ Shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="MarketingFunnelMaster - Unified Backend",
    description="AI-Powered Multi-Million-Euro Digital Empire Backend",
    version="1.0.0",
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
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancer"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "services": {
            "database": "connected",
            "ai_research": "connected" if ai_research_client else "disconnected",
            "agent_orchestrator": "running" if agent_orchestrator else "stopped"
        }
    }

# Readiness check endpoint
@app.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes/Docker deployments"""
    # Check if all critical services are ready
    ready = True
    services_status = {}
    
    # Check database connection
    try:
        from config.database import test_database_connection
        db_ready = await test_database_connection()
        services_status["database"] = "ready" if db_ready else "not_ready"
        ready = ready and db_ready
    except Exception as e:
        services_status["database"] = f"error: {str(e)}"
        ready = False
    
    # Check AI research engine
    if ai_research_client:
        ai_ready = await ai_research_client.health_check()
        services_status["ai_research"] = "ready" if ai_ready else "not_ready"
        ready = ready and ai_ready
    else:
        services_status["ai_research"] = "not_initialized"
        ready = False
    
    # Check agent orchestrator
    if agent_orchestrator:
        orchestrator_ready = await agent_orchestrator.health_check()
        services_status["agent_orchestrator"] = "ready" if orchestrator_ready else "not_ready"
        ready = ready and orchestrator_ready
    else:
        services_status["agent_orchestrator"] = "not_initialized"
        ready = False
    
    status_code = 200 if ready else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "ready": ready,
            "timestamp": datetime.utcnow().isoformat(),
            "services": services_status
        }
    )

# API version info
@app.get("/version")
async def version_info():
    """API version and build information"""
    return {
        "application": "MarketingFunnelMaster",
        "version": "1.0.0",
        "api_version": "v1",
        "build_date": "2025-07-03",
        "environment": settings.ENVIRONMENT,
        "features": {
            "ai_research": True,
            "agent_orchestration": True,
            "real_time_websockets": True,
            "multi_model_ai": True,
            "website_generation": True,
            "affiliate_integration": True
        }
    }

# Include API routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["AI Agents"]
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
from api.websockets import websocket_router
app.include_router(websocket_router)

# Development and debugging endpoints
if settings.ENVIRONMENT == "development":
    @app.get("/debug/agents")
    async def debug_agents():
        """Debug endpoint to inspect active agents"""
        if not agent_orchestrator:
            return {"error": "Agent orchestrator not initialized"}
        
        return await agent_orchestrator.get_debug_info()
    
    @app.get("/debug/ai-research")
    async def debug_ai_research():
        """Debug endpoint to inspect AI research engine"""
        if not ai_research_client:
            return {"error": "AI research client not initialized"}
        
        return await ai_research_client.get_debug_info()

# Main execution
if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        workers=1 if settings.ENVIRONMENT == "development" else settings.WORKERS
    )