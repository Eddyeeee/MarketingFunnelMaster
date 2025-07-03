"""
Agent Communication Service - Week 2 Implementation
Milestone 1C: Strategic agent integration following CLAUDE.md protocols

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import uuid

from app.services.database_service import DatabaseService
from app.services.rag_service import AdaptiveRAGService
from app.models.rag_models import (
    AgentQueryRequest, AgentQueryResponse, AgentFeedbackRequest
)

logger = logging.getLogger(__name__)

class AgentCommunicationService:
    """Strategic agent integration following CLAUDE.md protocols"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.rag_service = AdaptiveRAGService()
        self._agent_registry = {}
        self._agent_performance_cache = {}
        self._protocol_version = "1.0.0"
        self._initialized = False
    
    async def initialize(self):
        """Initialize agent communication service"""
        try:
            await self.db_service.initialize()
            await self.rag_service.initialize()
            await self._load_agent_registry()
            self._initialized = True
            logger.info("✅ Agent Communication Service initialized")
        except Exception as e:
            logger.error(f"❌ Agent Communication Service initialization failed: {e}")
            raise
    
    async def authenticate_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Agent authentication and authorization
        
        Returns agent identity if authentication successful
        """
        try:
            # Check agent registry
            if agent_id in self._agent_registry:
                agent_info = self._agent_registry[agent_id]
                
                # Verify agent is active
                if agent_info.get("status") == "active":
                    return {
                        "agent_id": agent_id,
                        "capabilities": agent_info.get("capabilities", []),
                        "priority_level": agent_info.get("priority_level", "medium"),
                        "authenticated_at": datetime.utcnow().isoformat()
                    }
            
            logger.warning(f"Agent authentication failed for {agent_id}")
            return None
            
        except Exception as e:
            logger.error(f"Agent authentication error: {e}")
            return None
    
    async def validate_agent_protocol(self, agent_request: Dict[str, Any]) -> bool:
        """
        Protocol validation per CLAUDE.md agent_protocol specification
        
        Validates JSON-API protocol compliance
        """
        try:
            required_fields = [
                "agent_id", "task_type", "priority", "query", "expected_output"
            ]
            
            # Check required fields
            for field in required_fields:
                if field not in agent_request:
                    logger.warning(f"Protocol validation failed: missing field {field}")
                    return False
            
            # Validate task_type
            valid_task_types = ["research", "content", "technical", "monetization"]
            if agent_request["task_type"] not in valid_task_types:
                logger.warning(f"Protocol validation failed: invalid task_type {agent_request['task_type']}")
                return False
            
            # Validate priority
            valid_priorities = ["low", "medium", "high", "critical"]
            if agent_request["priority"] not in valid_priorities:
                logger.warning(f"Protocol validation failed: invalid priority {agent_request['priority']}")
                return False
            
            logger.debug(f"Protocol validation successful for agent {agent_request['agent_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Protocol validation error: {e}")
            return False
    
    async def enhance_query_with_agent_context(
        self, 
        query: str, 
        agent_identity: Dict[str, Any]
    ) -> str:
        """Agent-specific query enhancement"""
        try:
            agent_capabilities = agent_identity.get("capabilities", [])
            priority_level = agent_identity.get("priority_level", "medium")
            
            # Add agent context to query
            enhanced_query = f"[AGENT_CONTEXT: {agent_identity['agent_id']}] {query}"
            
            # Add capability hints for specialized agents
            if "research" in agent_capabilities:
                enhanced_query += " [RESEARCH_FOCUS]"
            if "technical" in agent_capabilities:
                enhanced_query += " [TECHNICAL_DETAIL]"
            if "monetization" in agent_capabilities:
                enhanced_query += " [BUSINESS_FOCUS]"
            
            # Priority enhancement
            if priority_level == "high" or priority_level == "critical":
                enhanced_query += " [HIGH_PRIORITY]"
            
            return enhanced_query
            
        except Exception as e:
            logger.error(f"Query enhancement failed: {e}")
            return query  # Return original query as fallback
    
    async def execute_with_agent_context(
        self,
        agent_request: AgentQueryRequest,
        enhanced_query: str,
        agent_identity: Dict[str, Any]
    ) -> AgentQueryResponse:
        """Strategic query execution with agent context"""
        try:
            start_time = datetime.utcnow()
            
            # Determine search strategy based on agent type
            search_strategy = await self._select_agent_search_strategy(
                agent_request.task_type, agent_identity
            )
            
            # Create query context for RAG
            query_context = {
                "agent_id": agent_request.agent_id,
                "task_type": agent_request.task_type,
                "priority": agent_request.priority,
                "expected_output": agent_request.expected_output
            }
            
            # Execute RAG search with agent optimization
            rag_response = await self.rag_service.execute_hybrid_search(
                query=enhanced_query,
                strategy=search_strategy,
                context=query_context,
                user_id=f"agent_{agent_request.agent_id}"
            )
            
            # Process results for agent consumption
            agent_response_data = await self._format_agent_response(
                rag_response, agent_request, agent_identity
            )
            
            # Calculate execution time
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Create processing chain for transparency
            processing_chain = [
                f"agent_authentication:{agent_request.agent_id}",
                f"protocol_validation:passed",
                f"query_enhancement:{search_strategy}",
                f"rag_execution:{rag_response.strategy_used}",
                f"response_formatting:completed"
            ]
            
            response = AgentQueryResponse(
                agent_response=agent_response_data,
                confidence_score=rag_response.confidence_score,
                processing_chain=processing_chain,
                execution_time_ms=execution_time,
                status="success"
            )
            
            logger.info(f"Agent query executed successfully for {agent_request.agent_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Agent query execution failed: {e}")
            
            # Return error response
            return AgentQueryResponse(
                agent_response={"error": str(e)},
                confidence_score=0.0,
                processing_chain=[f"error:{str(e)}"],
                execution_time_ms=0,
                status="error"
            )
    
    async def collect_agent_feedback(self, feedback: AgentFeedbackRequest) -> bool:
        """Collect feedback from agents for learning"""
        try:
            logger.info(f"Collecting agent feedback from {feedback.agent_id}")
            
            # Store agent feedback for learning
            feedback_data = {
                "agent_id": feedback.agent_id,
                "query_id": feedback.query_id,
                "outcome_success": feedback.outcome_success,
                "performance_metrics": feedback.performance_metrics,
                "improvement_suggestions": feedback.improvement_suggestions,
                "feedback_type": "agent",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Calculate confidence based on agent feedback
            confidence_score = 0.9 if feedback.outcome_success else 0.3
            
            # Store using database service
            success = await self.db_service.store_query_outcome(
                query_id=feedback.query_id,
                response_id=f"agent_feedback_{feedback.agent_id}",
                outcome_data=feedback_data,
                confidence_score=confidence_score
            )
            
            if success:
                # Update agent performance cache
                await self._update_agent_performance_cache(feedback)
            
            return success
            
        except Exception as e:
            logger.error(f"Agent feedback collection failed: {e}")
            return False
    
    async def process_agent_learning(
        self,
        agent_request: AgentQueryRequest,
        response: AgentQueryResponse,
        agent_identity: Dict[str, Any]
    ):
        """Background task to process learning from agent interactions"""
        try:
            learning_data = {
                "agent_id": agent_request.agent_id,
                "task_type": agent_request.task_type,
                "priority": agent_request.priority,
                "response_confidence": response.confidence_score,
                "execution_time": response.execution_time_ms,
                "processing_chain": response.processing_chain,
                "success": response.status == "success"
            }
            
            # Store learning data
            await self._store_agent_learning_data(learning_data)
            
            logger.debug(f"Agent learning processed for {agent_request.agent_id}")
            
        except Exception as e:
            logger.error(f"Agent learning processing failed: {e}")
    
    async def update_agent_learning(self, feedback: AgentFeedbackRequest):
        """Update agent learning models based on feedback"""
        try:
            # Update agent-specific learning parameters
            agent_id = feedback.agent_id
            performance_metrics = feedback.performance_metrics
            
            # Update performance cache
            if agent_id not in self._agent_performance_cache:
                self._agent_performance_cache[agent_id] = {
                    "success_rate": [],
                    "response_times": [],
                    "confidence_scores": []
                }
            
            # Add new performance data
            self._agent_performance_cache[agent_id]["success_rate"].append(
                1.0 if feedback.outcome_success else 0.0
            )
            
            # Keep only recent data (last 100 interactions)
            for metric in self._agent_performance_cache[agent_id]:
                if len(self._agent_performance_cache[agent_id][metric]) > 100:
                    self._agent_performance_cache[agent_id][metric] = \
                        self._agent_performance_cache[agent_id][metric][-100:]
            
            logger.debug(f"Agent learning updated for {agent_id}")
            
        except Exception as e:
            logger.error(f"Agent learning update failed: {e}")
    
    async def get_agent_registry(self) -> List[Dict[str, Any]]:
        """Get registry of available agents and their capabilities"""
        try:
            agents = []
            for agent_id, agent_info in self._agent_registry.items():
                agent_data = {
                    "agent_id": agent_id,
                    "capabilities": agent_info.get("capabilities", []),
                    "status": agent_info.get("status", "unknown"),
                    "priority_level": agent_info.get("priority_level", "medium"),
                    "last_active": agent_info.get("last_active", "unknown"),
                    "performance_summary": await self._get_agent_performance_summary(agent_id)
                }
                agents.append(agent_data)
            
            return agents
            
        except Exception as e:
            logger.error(f"Agent registry retrieval failed: {e}")
            return []
    
    async def validate_agent_registration(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate agent registration information"""
        validation_result = {"valid": True, "errors": []}
        
        try:
            required_fields = ["agent_id", "capabilities", "task_types"]
            
            for field in required_fields:
                if field not in agent_info:
                    validation_result["errors"].append(f"Missing required field: {field}")
                    validation_result["valid"] = False
            
            # Validate agent_id uniqueness
            if agent_info.get("agent_id") in self._agent_registry:
                validation_result["errors"].append("Agent ID already exists")
                validation_result["valid"] = False
            
            # Validate capabilities
            valid_capabilities = ["research", "content", "technical", "monetization", "analytics"]
            for capability in agent_info.get("capabilities", []):
                if capability not in valid_capabilities:
                    validation_result["errors"].append(f"Invalid capability: {capability}")
                    validation_result["valid"] = False
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Agent registration validation failed: {e}")
            return {"valid": False, "errors": [str(e)]}
    
    async def register_agent(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        """Register new agent in the ecosystem"""
        try:
            agent_id = agent_info["agent_id"]
            
            # Prepare agent registry entry
            registry_entry = {
                "agent_id": agent_id,
                "capabilities": agent_info["capabilities"],
                "task_types": agent_info["task_types"],
                "priority_level": agent_info.get("priority_level", "medium"),
                "status": "active",
                "registered_at": datetime.utcnow().isoformat(),
                "last_active": datetime.utcnow().isoformat()
            }
            
            # Add to registry
            self._agent_registry[agent_id] = registry_entry
            
            # Initialize performance cache
            self._agent_performance_cache[agent_id] = {
                "success_rate": [],
                "response_times": [],
                "confidence_scores": []
            }
            
            logger.info(f"Agent registered successfully: {agent_id}")
            
            return {
                "success": True,
                "agent_id": agent_id,
                "capabilities": agent_info["capabilities"]
            }
            
        except Exception as e:
            logger.error(f"Agent registration failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_agent_capabilities(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get specific agent capabilities and status"""
        try:
            if agent_id in self._agent_registry:
                agent_info = self._agent_registry[agent_id]
                performance_summary = await self._get_agent_performance_summary(agent_id)
                
                return {
                    "agent_id": agent_id,
                    "capabilities": agent_info.get("capabilities", []),
                    "task_types": agent_info.get("task_types", []),
                    "status": agent_info.get("status", "unknown"),
                    "priority_level": agent_info.get("priority_level", "medium"),
                    "performance": performance_summary,
                    "last_active": agent_info.get("last_active", "unknown")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Agent capabilities retrieval failed: {e}")
            return None
    
    async def orchestrate_agents(self, orchestration_request: Dict[str, Any]):
        """Background task to orchestrate multiple agents"""
        try:
            task_id = orchestration_request.get("task_id", str(uuid.uuid4()))
            agents = orchestration_request.get("agents", [])
            task_description = orchestration_request.get("task_description", "")
            
            logger.info(f"Orchestrating task {task_id} with {len(agents)} agents")
            
            # Simple sequential orchestration (can be enhanced for parallel)
            orchestration_results = []
            
            for agent_config in agents:
                agent_id = agent_config.get("agent_id")
                agent_task = agent_config.get("task", task_description)
                
                # Execute agent task (would normally call agent endpoints)
                result = {
                    "agent_id": agent_id,
                    "task": agent_task,
                    "status": "completed",
                    "execution_time": 1000,  # Simulated
                    "timestamp": datetime.utcnow().isoformat()
                }
                orchestration_results.append(result)
            
            # Store orchestration results
            await self._store_orchestration_results(task_id, orchestration_results)
            
            logger.info(f"Task orchestration completed: {task_id}")
            
        except Exception as e:
            logger.error(f"Agent orchestration failed: {e}")
    
    async def get_agent_performance_metrics(
        self, 
        agent_id: str, 
        time_window_days: int = 7
    ) -> Dict[str, Any]:
        """Get performance metrics for specific agent"""
        try:
            if agent_id not in self._agent_performance_cache:
                return {"error": "Agent performance data not found"}
            
            cache_data = self._agent_performance_cache[agent_id]
            
            # Calculate metrics
            success_rates = cache_data.get("success_rate", [])
            response_times = cache_data.get("response_times", [])
            confidence_scores = cache_data.get("confidence_scores", [])
            
            metrics = {
                "agent_id": agent_id,
                "time_window_days": time_window_days,
                "total_interactions": len(success_rates),
                "success_rate": sum(success_rates) / len(success_rates) if success_rates else 0,
                "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                "avg_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Agent performance metrics failed: {e}")
            return {"error": str(e)}
    
    async def test_communication_protocol(self, protocol_test: Dict[str, Any]) -> Dict[str, Any]:
        """Test agent communication protocol compliance"""
        try:
            test_results = {
                "compliant": True,
                "results": [],
                "recommendations": []
            }
            
            # Test required fields
            required_fields = ["agent_id", "task_type", "priority", "query", "expected_output"]
            for field in required_fields:
                if field in protocol_test:
                    test_results["results"].append(f"✅ {field}: present")
                else:
                    test_results["results"].append(f"❌ {field}: missing")
                    test_results["compliant"] = False
                    test_results["recommendations"].append(f"Add required field: {field}")
            
            # Test value validity
            if "task_type" in protocol_test:
                valid_types = ["research", "content", "technical", "monetization"]
                if protocol_test["task_type"] in valid_types:
                    test_results["results"].append("✅ task_type: valid")
                else:
                    test_results["results"].append("❌ task_type: invalid")
                    test_results["compliant"] = False
                    test_results["recommendations"].append(f"Use valid task_type: {valid_types}")
            
            if "priority" in protocol_test:
                valid_priorities = ["low", "medium", "high", "critical"]
                if protocol_test["priority"] in valid_priorities:
                    test_results["results"].append("✅ priority: valid")
                else:
                    test_results["results"].append("❌ priority: invalid")
                    test_results["compliant"] = False
                    test_results["recommendations"].append(f"Use valid priority: {valid_priorities}")
            
            return test_results
            
        except Exception as e:
            logger.error(f"Protocol test failed: {e}")
            return {"compliant": False, "error": str(e), "results": [], "recommendations": []}
    
    # Private helper methods
    
    async def _load_agent_registry(self):
        """Load agent registry (from database or config)"""
        try:
            # Initialize with core agents from CLAUDE.md
            core_agents = {
                "BusinessManagerAgent": {
                    "capabilities": ["strategy", "planning", "management"],
                    "task_types": ["research", "monetization"],
                    "priority_level": "high",
                    "status": "active"
                },
                "OpportunityScanner": {
                    "capabilities": ["research", "analysis", "trend_detection"],
                    "task_types": ["research"],
                    "priority_level": "high",
                    "status": "active"
                },
                "ContentWriterAgent": {
                    "capabilities": ["content", "writing", "seo"],
                    "task_types": ["content"],
                    "priority_level": "medium",
                    "status": "active"
                },
                "WebsiteGeneratorAgent": {
                    "capabilities": ["technical", "web_development", "automation"],
                    "task_types": ["technical"],
                    "priority_level": "medium",
                    "status": "active"
                }
            }
            
            for agent_id, agent_info in core_agents.items():
                agent_info.update({
                    "agent_id": agent_id,
                    "registered_at": datetime.utcnow().isoformat(),
                    "last_active": datetime.utcnow().isoformat()
                })
                self._agent_registry[agent_id] = agent_info
                
                # Initialize performance cache
                self._agent_performance_cache[agent_id] = {
                    "success_rate": [],
                    "response_times": [],
                    "confidence_scores": []
                }
            
            logger.info(f"Agent registry loaded with {len(core_agents)} core agents")
            
        except Exception as e:
            logger.error(f"Agent registry loading failed: {e}")
    
    async def _select_agent_search_strategy(self, task_type: str, agent_identity: Dict[str, Any]) -> str:
        """Select optimal search strategy based on agent type"""
        try:
            # Strategy mapping based on agent task type
            strategy_mapping = {
                "research": "semantic",           # Research agents prefer semantic search
                "content": "hybrid",             # Content agents need balanced approach
                "technical": "vector",           # Technical agents prefer precise vector search
                "monetization": "performance_weighted"  # Business agents want performance-optimized
            }
            
            return strategy_mapping.get(task_type, "hybrid")
            
        except Exception as e:
            logger.error(f"Strategy selection failed: {e}")
            return "hybrid"
    
    async def _format_agent_response(
        self,
        rag_response,
        agent_request: AgentQueryRequest,
        agent_identity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format RAG response for agent consumption"""
        try:
            # Extract and format results based on expected output
            expected_output = agent_request.expected_output.lower()
            
            formatted_response = {
                "query_id": rag_response.query_id,
                "results_count": rag_response.total_results,
                "confidence": rag_response.confidence_score,
                "strategy_used": rag_response.strategy_used,
                "processing_time_ms": rag_response.processing_time_ms
            }
            
            # Format results based on expected output type
            if "json" in expected_output:
                formatted_response["results"] = [
                    {
                        "content": result.content,
                        "relevance": result.relevance_score,
                        "source": result.source_id,
                        "metadata": result.metadata
                    }
                    for result in rag_response.results
                ]
            elif "summary" in expected_output:
                # Create summary from top results
                top_contents = [result.content for result in rag_response.results[:3]]
                formatted_response["summary"] = " ".join(top_contents)[:500] + "..."
            elif "list" in expected_output:
                formatted_response["items"] = [
                    result.content for result in rag_response.results
                ]
            else:
                # Default format
                formatted_response["results"] = [
                    result.dict() for result in rag_response.results
                ]
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Response formatting failed: {e}")
            return {"error": str(e)}
    
    async def _update_agent_performance_cache(self, feedback: AgentFeedbackRequest):
        """Update agent performance cache with feedback"""
        try:
            agent_id = feedback.agent_id
            
            if agent_id not in self._agent_performance_cache:
                self._agent_performance_cache[agent_id] = {
                    "success_rate": [],
                    "response_times": [],
                    "confidence_scores": []
                }
            
            # Add performance metrics
            cache = self._agent_performance_cache[agent_id]
            cache["success_rate"].append(1.0 if feedback.outcome_success else 0.0)
            
            # Extract metrics from feedback
            metrics = feedback.performance_metrics
            if "response_time" in metrics:
                cache["response_times"].append(metrics["response_time"])
            if "confidence" in metrics:
                cache["confidence_scores"].append(metrics["confidence"])
            
        except Exception as e:
            logger.error(f"Performance cache update failed: {e}")
    
    async def _get_agent_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get performance summary for agent"""
        try:
            if agent_id not in self._agent_performance_cache:
                return {"status": "no_data"}
            
            cache = self._agent_performance_cache[agent_id]
            success_rates = cache.get("success_rate", [])
            
            if not success_rates:
                return {"status": "insufficient_data"}
            
            return {
                "total_interactions": len(success_rates),
                "success_rate": sum(success_rates) / len(success_rates),
                "last_interaction": datetime.utcnow().isoformat(),
                "performance_trend": "stable"  # Simplified
            }
            
        except Exception as e:
            logger.error(f"Performance summary failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _store_agent_learning_data(self, learning_data: Dict[str, Any]):
        """Store agent learning data for analysis"""
        try:
            # Store using database service outcome tracking
            await self.db_service.store_query_outcome(
                query_id=f"agent_learning_{learning_data['agent_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                response_id=f"learning_data_{uuid.uuid4()}",
                outcome_data=learning_data,
                confidence_score=learning_data.get("response_confidence", 0.5)
            )
            
        except Exception as e:
            logger.error(f"Agent learning data storage failed: {e}")
    
    async def _store_orchestration_results(self, task_id: str, results: List[Dict[str, Any]]):
        """Store orchestration results"""
        try:
            orchestration_data = {
                "task_id": task_id,
                "results": results,
                "orchestration_type": "sequential",
                "completed_at": datetime.utcnow().isoformat()
            }
            
            await self.db_service.store_query_outcome(
                query_id=f"orchestration_{task_id}",
                response_id=f"orchestration_result_{task_id}",
                outcome_data=orchestration_data,
                confidence_score=1.0
            )
            
        except Exception as e:
            logger.error(f"Orchestration results storage failed: {e}")
    
    async def health_check(self) -> bool:
        """Health check for agent communication service"""
        try:
            if not self._initialized:
                return False
            
            # Check database connectivity
            db_health = await self.db_service.health_check()
            db_healthy = all(status == "healthy" for status in db_health.values())
            
            # Check RAG service
            rag_healthy = await self.rag_service.health_check()
            
            # Check agent registry
            registry_healthy = len(self._agent_registry) > 0
            
            return db_healthy and rag_healthy and registry_healthy
            
        except Exception as e:
            logger.error(f"Agent service health check failed: {e}")
            return False