"""
Agent Router - Week 2 Implementation
Milestone 1C: Agent communication protocols and JSON-API compliance

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import uuid

from app.services.agent_service import AgentCommunicationService
from app.models.rag_models import (
    AgentQueryRequest, AgentQueryResponse, AgentFeedbackRequest
)
from core.auth.auth_dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize agent communication service
agent_service = AgentCommunicationService()

@router.post("/query", response_model=AgentQueryResponse)
async def agent_query_endpoint(
    agent_request: AgentQueryRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Strategic agent-to-agent communication endpoint
    
    Implements CLAUDE.md JSON-API protocol for agent communication:
    - Agent authentication and authorization
    - Query processing with agent context
    - RAG execution with agent-specific optimization
    """
    try:
        logger.info(f"Processing agent query from {agent_request.agent_id}")
        
        # Agent authentication and authorization
        agent_identity = await agent_service.authenticate_agent(agent_request.agent_id)
        
        if not agent_identity:
            raise HTTPException(
                status_code=401,
                detail="Agent authentication failed"
            )
        
        # Validate agent protocol compliance
        protocol_valid = await agent_service.validate_agent_protocol(agent_request.dict())
        
        if not protocol_valid:
            raise HTTPException(
                status_code=400,
                detail="Agent request does not comply with CLAUDE.md protocol"
            )
        
        # Query processing with agent context
        enhanced_query = await agent_service.enhance_query_with_agent_context(
            agent_request.query, agent_identity
        )
        
        # Execute RAG with agent-specific optimization
        response = await agent_service.execute_with_agent_context(
            agent_request=agent_request,
            enhanced_query=enhanced_query,
            agent_identity=agent_identity
        )
        
        # Background learning from agent interaction
        background_tasks.add_task(
            agent_service.process_agent_learning,
            agent_request, response, agent_identity
        )
        
        logger.info(f"Agent query completed for {agent_request.agent_id}: {response.status}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent query processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent query processing failed: {str(e)}"
        )

@router.post("/feedback")
async def agent_feedback_endpoint(
    feedback: AgentFeedbackRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Strategic agent feedback collection for learning
    
    Collects feedback from agents for continuous system improvement
    """
    try:
        logger.info(f"Processing agent feedback from {feedback.agent_id}")
        
        # Process agent feedback
        feedback_processed = await agent_service.collect_agent_feedback(feedback)
        
        # Background learning update
        background_tasks.add_task(
            agent_service.update_agent_learning,
            feedback
        )
        
        return {
            "feedback_processed": feedback_processed,
            "learning_update_triggered": True,
            "agent_id": feedback.agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent feedback processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent feedback processing failed: {str(e)}"
        )

@router.get("/registry")
async def get_agent_registry(
    current_user = Depends(get_current_user)
):
    """
    Get registry of available agents and their capabilities
    
    Provides discovery mechanism for agent ecosystem
    """
    try:
        registry = await agent_service.get_agent_registry()
        
        return {
            "agents": registry,
            "total_agents": len(registry),
            "registry_version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent registry retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent registry retrieval failed: {str(e)}"
        )

@router.post("/register")
async def register_new_agent(
    agent_info: Dict[str, Any],
    current_user = Depends(get_current_user)
):
    """
    Register new agent in the ecosystem
    
    Allows dynamic agent registration following CLAUDE.md protocols
    """
    try:
        logger.info(f"Registering new agent: {agent_info.get('agent_id', 'unknown')}")
        
        # Validate agent information
        validation_result = await agent_service.validate_agent_registration(agent_info)
        
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Agent registration validation failed: {validation_result['errors']}"
            )
        
        # Register agent
        registration_result = await agent_service.register_agent(agent_info)
        
        return {
            "agent_registered": registration_result["success"],
            "agent_id": registration_result["agent_id"],
            "capabilities": registration_result["capabilities"],
            "registration_timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent registration failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent registration failed: {str(e)}"
        )

@router.get("/capabilities/{agent_id}")
async def get_agent_capabilities(
    agent_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get specific agent capabilities and status
    """
    try:
        capabilities = await agent_service.get_agent_capabilities(agent_id)
        
        if not capabilities:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_id} not found"
            )
        
        return capabilities
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent capabilities retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent capabilities retrieval failed: {str(e)}"
        )

@router.post("/orchestrate")
async def orchestrate_multi_agent_task(
    orchestration_request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Orchestrate multi-agent task execution
    
    Coordinates multiple agents for complex task completion
    """
    try:
        logger.info(f"Orchestrating multi-agent task: {orchestration_request.get('task_id', 'unknown')}")
        
        # Background orchestration
        background_tasks.add_task(
            agent_service.orchestrate_agents,
            orchestration_request
        )
        
        orchestration_id = str(uuid.uuid4())
        
        return {
            "orchestration_id": orchestration_id,
            "orchestration_started": True,
            "estimated_completion": "5-10 minutes",
            "agents_involved": orchestration_request.get("agents", []),
            "task_priority": orchestration_request.get("priority", "medium"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent orchestration failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent orchestration failed: {str(e)}"
        )

@router.get("/performance/{agent_id}")
async def get_agent_performance_metrics(
    agent_id: str,
    time_window_days: int = 7,
    current_user = Depends(get_current_user)
):
    """
    Get performance metrics for specific agent
    """
    try:
        performance_metrics = await agent_service.get_agent_performance_metrics(
            agent_id=agent_id,
            time_window_days=time_window_days
        )
        
        return performance_metrics
        
    except Exception as e:
        logger.error(f"Agent performance metrics failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent performance metrics failed: {str(e)}"
        )

@router.post("/communication/protocol-test")
async def test_agent_communication_protocol(
    protocol_test: Dict[str, Any],
    current_user = Depends(get_current_user)
):
    """
    Test agent communication protocol compliance
    
    Validates agent communication against CLAUDE.md specification
    """
    try:
        test_result = await agent_service.test_communication_protocol(protocol_test)
        
        return {
            "protocol_compliance": test_result["compliant"],
            "test_results": test_result["results"],
            "recommendations": test_result["recommendations"],
            "test_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Protocol test failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Protocol test failed: {str(e)}"
        )

# Health check for agent system
@router.get("/health")
async def agent_system_health_check():
    """Health check for agent communication system"""
    try:
        agent_health = await agent_service.health_check()
        
        return {
            "status": "healthy" if agent_health else "unhealthy",
            "agent_system": "operational" if agent_health else "degraded",
            "communication_protocols": "active" if agent_health else "inactive",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }