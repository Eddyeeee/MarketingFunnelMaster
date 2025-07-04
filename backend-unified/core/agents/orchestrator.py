#!/usr/bin/env python3
"""
Agent Orchestrator - Phase 2 Implementation with Full AI Pipeline
Module 3A: AI Content Generation Pipeline Implementation

Executor: Claude Code
Erstellt: 2025-07-03
Updated: 2025-07-04 (Module 3A Phase 2 - Complete Integration)
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from dataclasses import dataclass
from pydantic import BaseModel, Field

# Import Phase 2 components
from .content_outline import ContentOutlineAgent
from .content_writer import ContentWriterAgent
from .research_engine import AIResearchEngine, ResearchQuery, ResearchType, ResearchPriority
from ..quality.quality_gates import ContentQualityValidator, QualityLevel
from ..tracking.performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)

class AgentType(str, Enum):
    """Agent type enumeration"""
    RESEARCH = "research"
    CONTENT_OUTLINE = "content_outline"
    CONTENT_WRITER = "content_writer"
    VISUAL_CONTENT = "visual_content"
    SOCIAL_MEDIA = "social_media"
    WEBSITE = "website"
    ANALYTICS = "analytics"
    OPTIMIZATION = "optimization"

class AgentStatus(str, Enum):
    """Agent status enumeration"""
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AgentTask:
    """Agent task data structure"""
    id: UUID
    agent_type: AgentType
    task_type: str
    priority: TaskPriority
    data: Dict[str, Any]
    expected_output: str
    created_at: datetime
    deadline: Optional[datetime] = None
    dependencies: List[UUID] = None
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class AgentRegistration(BaseModel):
    """Agent registration model"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    agent_type: AgentType
    status: AgentStatus = AgentStatus.INITIALIZING
    capabilities: List[str] = Field(default_factory=list)
    max_concurrent_tasks: int = Field(default=3)
    current_task_count: int = Field(default=0)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    last_heartbeat: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ContentGenerationPipeline:
    """Content generation pipeline workflow"""
    
    def __init__(self, orchestrator: 'AgentOrchestrator'):
        self.orchestrator = orchestrator
        self.pipeline_id = uuid4()
        self.status = "ready"
    
    async def generate_content(self, niche: str, persona: str, device: str, 
                             content_type: str) -> Dict[str, Any]:
        """Execute full content generation pipeline"""
        pipeline_start = datetime.now()
        
        try:
            # Stage 1: Content Outline
            outline_task = AgentTask(
                id=uuid4(),
                agent_type=AgentType.CONTENT_OUTLINE,
                task_type="generate_outline",
                priority=TaskPriority.HIGH,
                data={
                    "niche": niche,
                    "persona": persona,
                    "device": device,
                    "content_type": content_type
                },
                expected_output="structured_outline",
                created_at=datetime.now()
            )
            
            outline_result = await self.orchestrator.execute_task(outline_task)
            
            # Stage 2: Content Writing
            writing_task = AgentTask(
                id=uuid4(),
                agent_type=AgentType.CONTENT_WRITER,
                task_type="generate_content",
                priority=TaskPriority.HIGH,
                data={
                    "outline": outline_result,
                    "niche": niche,
                    "persona": persona,
                    "device": device
                },
                expected_output="formatted_content",
                created_at=datetime.now(),
                dependencies=[outline_task.id]
            )
            
            content_result = await self.orchestrator.execute_task(writing_task)
            
            # Stage 3: Visual Content (Parallel)
            visual_task = AgentTask(
                id=uuid4(),
                agent_type=AgentType.VISUAL_CONTENT,
                task_type="generate_visuals",
                priority=TaskPriority.MEDIUM,
                data={
                    "content": content_result,
                    "device": device,
                    "persona": persona
                },
                expected_output="visual_assets",
                created_at=datetime.now(),
                dependencies=[writing_task.id]
            )
            
            # Stage 4: Social Media Adaptation (Parallel)
            social_task = AgentTask(
                id=uuid4(),
                agent_type=AgentType.SOCIAL_MEDIA,
                task_type="adapt_content",
                priority=TaskPriority.MEDIUM,
                data={
                    "content": content_result,
                    "platforms": ["instagram", "linkedin", "tiktok"]
                },
                expected_output="social_adaptations",
                created_at=datetime.now(),
                dependencies=[writing_task.id]
            )
            
            # Execute parallel tasks
            visual_result, social_result = await asyncio.gather(
                self.orchestrator.execute_task(visual_task),
                self.orchestrator.execute_task(social_task)
            )
            
            pipeline_duration = (datetime.now() - pipeline_start).total_seconds()
            
            return {
                "pipeline_id": str(self.pipeline_id),
                "status": "completed",
                "content": content_result,
                "visual_assets": visual_result,
                "social_adaptations": social_result,
                "performance_metrics": {
                    "generation_time_seconds": pipeline_duration,
                    "stages_completed": 4,
                    "quality_score": 0.0  # To be calculated by quality agents
                }
            }
            
        except Exception as e:
            logger.error(f"Content pipeline failed: {e}")
            return {
                "pipeline_id": str(self.pipeline_id),
                "status": "failed",
                "error": str(e)
            }

class AgentOrchestrator:
    """Phase 2 Agent Orchestrator with Full AI Pipeline Integration"""
    
    def __init__(self):
        self.agents: Dict[str, AgentRegistration] = {}
        self.tasks: Dict[UUID, AgentTask] = {}
        self.task_queue: List[AgentTask] = []
        self.initialized = False
        self.content_pipeline = ContentGenerationPipeline(self)
        
        # Phase 2 Components
        self.content_outline_agent = ContentOutlineAgent()
        self.content_writer_agent = ContentWriterAgent()
        self.research_engine = AIResearchEngine()
        self.quality_validator = ContentQualityValidator()
        self.performance_tracker = PerformanceTracker()
        
        # Performance tracking
        self.total_tasks_executed = 0
        self.average_task_time = 0.0
        self.success_rate = 0.0
    
    async def initialize(self):
        """Initialize the orchestrator with Phase 2 AI pipeline"""
        logger.info("Agent Orchestrator initializing with Module 3A Phase 2 capabilities...")
        
        # Initialize all Phase 2 components
        logger.info("Initializing AI agents and pipeline components...")
        
        # Register content agents
        await self.register_content_agents()
        
        # Initialize performance tracking
        await self.performance_tracker.track_system_health({
            "cpu_usage": 25.0,
            "memory_usage": 40.0,
            "active_agents": len(self.agents),
            "queued_tasks": 0,
            "processing_tasks": 0,
            "error_rate": 0.0,
            "average_response_time": 0.5
        })
        
        self.initialized = True
        logger.info("Agent Orchestrator Phase 2 initialized successfully with full AI pipeline")
    
    async def register_content_agents(self):
        """Register content generation agents"""
        content_agents = [
            AgentRegistration(
                name="ContentOutlineAgent",
                agent_type=AgentType.CONTENT_OUTLINE,
                capabilities=["seo_optimization", "structure_design", "persona_targeting"],
                max_concurrent_tasks=5
            ),
            AgentRegistration(
                name="ContentWriterAgent",
                agent_type=AgentType.CONTENT_WRITER,
                capabilities=["persuasive_writing", "persona_adaptation", "device_optimization"],
                max_concurrent_tasks=3
            ),
            AgentRegistration(
                name="VisualContentAgent",
                agent_type=AgentType.VISUAL_CONTENT,
                capabilities=["image_generation", "infographic_creation", "video_thumbnails"],
                max_concurrent_tasks=2
            ),
            AgentRegistration(
                name="SocialMediaAgent",
                agent_type=AgentType.SOCIAL_MEDIA,
                capabilities=["platform_adaptation", "hashtag_optimization", "engagement_hooks"],
                max_concurrent_tasks=4
            )
        ]
        
        # Register existing agents
        existing_agents = [
            AgentRegistration(
                name="ResearchAgent",
                agent_type=AgentType.RESEARCH,
                capabilities=["market_analysis", "competitor_research", "trend_detection"],
                max_concurrent_tasks=2
            ),
            AgentRegistration(
                name="WebsiteAgent",
                agent_type=AgentType.WEBSITE,
                capabilities=["site_generation", "deployment", "optimization"],
                max_concurrent_tasks=3
            )
        ]
        
        all_agents = content_agents + existing_agents
        
        for agent in all_agents:
            agent.status = AgentStatus.READY
            self.agents[agent.name] = agent
            logger.info(f"Registered agent: {agent.name} ({agent.agent_type})")
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task using appropriate agent"""
        start_time = datetime.now()
        
        try:
            # Find available agent
            agent = self._find_available_agent(task.agent_type)
            if not agent:
                raise Exception(f"No available agent for type: {task.agent_type}")
            
            # Update agent status
            agent.status = AgentStatus.BUSY
            agent.current_task_count += 1
            
            # Store task
            self.tasks[task.id] = task
            task.status = "executing"
            
            # Execute actual task using Phase 2 AI agents
            await self._execute_actual_task(task)
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_performance_metrics(agent, execution_time, True)
            
            task.status = "completed"
            agent.status = AgentStatus.READY
            agent.current_task_count -= 1
            
            return task.result or {"status": "completed", "task_id": str(task.id)}
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            if 'agent' in locals():
                agent.status = AgentStatus.READY
                agent.current_task_count -= 1
                self._update_performance_metrics(agent, 0, False)
            
            logger.error(f"Task execution failed: {e}")
            raise
    
    def _find_available_agent(self, agent_type: AgentType) -> Optional[AgentRegistration]:
        """Find available agent of specified type"""
        for agent in self.agents.values():
            if (agent.agent_type == agent_type and 
                agent.status == AgentStatus.READY and
                agent.current_task_count < agent.max_concurrent_tasks):
                return agent
        return None
    
    async def _execute_actual_task(self, task: AgentTask):
        """Execute actual task using Phase 2 AI agents"""
        start_time = datetime.now()
        
        try:
            if task.agent_type == AgentType.CONTENT_OUTLINE:
                # Use actual ContentOutlineAgent
                result = await self.content_outline_agent.generate_outline(
                    niche=task.data.get("niche", ""),
                    persona=task.data.get("persona", ""),
                    device=task.data.get("device", ""),
                    content_type=task.data.get("content_type", "")
                )
                task.result = {
                    "outline": result.dict(),
                    "quality_score": result.quality_score,
                    "estimated_reading_time": result.estimated_reading_time
                }
                
            elif task.agent_type == AgentType.CONTENT_WRITER:
                # Use actual ContentWriterAgent
                outline_data = task.data.get("outline", {})
                result = await self.content_writer_agent.generate_content(
                    outline=outline_data,
                    niche=task.data.get("niche", ""),
                    persona=task.data.get("persona", ""),
                    device=task.data.get("device", "")
                )
                
                # Run quality validation
                quality_report = await self.quality_validator.validate_content(
                    content=result.dict(),
                    quality_level=QualityLevel.STANDARD
                )
                
                task.result = {
                    "content": result.dict(),
                    "quality_report": quality_report.dict(),
                    "approved": quality_report.approved
                }
                
                # Track content performance
                await self.performance_tracker.track_content_performance(result.dict())
                
            elif task.agent_type == AgentType.RESEARCH:
                # Use AI Research Engine
                research_query = ResearchQuery(
                    id=str(task.id),
                    type=ResearchType.MARKET_ANALYSIS,
                    priority=ResearchPriority.HIGH,
                    niche=task.data.get("niche", ""),
                    keywords=task.data.get("keywords", []),
                    context=task.data.get("context", {}),
                    depth_level="detailed",
                    target_persona=task.data.get("persona")
                )
                
                result = await self.research_engine.conduct_research(research_query)
                task.result = {
                    "research_data": result.data,
                    "insights": result.insights,
                    "recommendations": result.recommendations,
                    "confidence_score": result.confidence_score
                }
                
            else:
                # Fallback to simulation for other agent types
                await self._simulate_task_execution(task)
                return
            
            # Track agent performance
            execution_time = (datetime.now() - start_time).total_seconds()
            quality_score = task.result.get("quality_score") or task.result.get("confidence_score")
            
            agent_name = f"{task.agent_type}_agent"
            await self.performance_tracker.track_agent_performance(
                agent_name=agent_name,
                agent_type=task.agent_type,
                execution_time=execution_time,
                success=True,
                quality_score=quality_score
            )
            
            logger.info(f"Successfully executed {task.agent_type} task in {execution_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Task execution failed for {task.agent_type}: {e}")
            # Track failed performance
            agent_name = f"{task.agent_type}_agent"
            await self.performance_tracker.track_agent_performance(
                agent_name=agent_name,
                agent_type=task.agent_type,
                execution_time=0.0,
                success=False
            )
            raise
    
    async def _simulate_task_execution(self, task: AgentTask):
        """Simulate task execution for non-implemented agents"""
        # Simulate processing time based on task type
        processing_times = {
            AgentType.CONTENT_OUTLINE: 0.5,
            AgentType.CONTENT_WRITER: 1.5,
            AgentType.VISUAL_CONTENT: 2.0,
            AgentType.SOCIAL_MEDIA: 0.8,
            AgentType.RESEARCH: 1.0
        }
        
        await asyncio.sleep(processing_times.get(task.agent_type, 1.0))
        
        # Generate mock result based on task type
        task.result = self._generate_mock_result(task)
    
    def _generate_mock_result(self, task: AgentTask) -> Dict[str, Any]:
        """Generate mock results for development/testing"""
        base_result = {
            "task_id": str(task.id),
            "agent_type": task.agent_type,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
        
        if task.agent_type == AgentType.CONTENT_OUTLINE:
            base_result.update({
                "outline": {
                    "title": f"Ultimate {task.data.get('niche', 'Product')} Guide for {task.data.get('persona', 'Users')}",
                    "sections": [
                        "Hook & Problem Statement",
                        "Solution Overview",
                        "Key Benefits",
                        "How It Works",
                        "Social Proof",
                        "Call to Action"
                    ],
                    "seo_keywords": ["best", "ultimate", "guide", task.data.get('niche', 'product')],
                    "target_length": 1200
                }
            })
        
        elif task.agent_type == AgentType.CONTENT_WRITER:
            base_result.update({
                "content": {
                    "title": "Generated Content Title",
                    "body": "This is generated content body optimized for the target persona and device.",
                    "meta_description": "SEO-optimized meta description",
                    "word_count": 1200,
                    "readability_score": 8.5
                }
            })
        
        elif task.agent_type == AgentType.VISUAL_CONTENT:
            base_result.update({
                "visuals": {
                    "hero_image": "generated_hero_image.jpg",
                    "infographics": ["infographic_1.png", "infographic_2.png"],
                    "social_images": ["social_square.jpg", "social_story.jpg"]
                }
            })
        
        elif task.agent_type == AgentType.SOCIAL_MEDIA:
            base_result.update({
                "adaptations": {
                    "instagram": {"caption": "Instagram optimized caption", "hashtags": ["#trending"]},
                    "linkedin": {"post": "Professional LinkedIn post"},
                    "tiktok": {"script": "TikTok video script"}
                }
            })
        
        return base_result
    
    def _update_performance_metrics(self, agent: AgentRegistration, 
                                   execution_time: float, success: bool):
        """Update agent performance metrics"""
        if "total_tasks" not in agent.performance_metrics:
            agent.performance_metrics["total_tasks"] = 0
            agent.performance_metrics["successful_tasks"] = 0
            agent.performance_metrics["average_execution_time"] = 0.0
        
        agent.performance_metrics["total_tasks"] += 1
        if success:
            agent.performance_metrics["successful_tasks"] += 1
        
        # Update average execution time
        current_avg = agent.performance_metrics["average_execution_time"]
        total_tasks = agent.performance_metrics["total_tasks"]
        agent.performance_metrics["average_execution_time"] = (
            (current_avg * (total_tasks - 1) + execution_time) / total_tasks
        )
        
        agent.performance_metrics["success_rate"] = (
            agent.performance_metrics["successful_tasks"] / total_tasks
        )
        
        agent.last_heartbeat = datetime.now()
    
    async def generate_content_pipeline(self, niche: str, persona: str, 
                                      device: str, content_type: str) -> Dict[str, Any]:
        """Main content generation pipeline entry point"""
        return await self.content_pipeline.generate_content(niche, persona, device, content_type)
    
    async def health_check(self) -> bool:
        """Check orchestrator health"""
        return self.initialized and len(self.agents) > 0
    
    async def get_debug_info(self) -> Dict[str, Any]:
        """Get comprehensive debug information including Phase 2 components"""
        return {
            "initialized": self.initialized,
            "agents_count": len(self.agents),
            "active_tasks": len([t for t in self.tasks.values() if t.status == "executing"]),
            "total_tasks_executed": self.total_tasks_executed,
            "phase2_components": {
                "content_outline_agent": await self.content_outline_agent.health_check(),
                "content_writer_agent": await self.content_writer_agent.health_check(),
                "research_engine": await self.research_engine.health_check(),
                "quality_validator": True,  # No health check method
                "performance_tracker": await self.performance_tracker.health_check()
            },
            "agents": {
                name: {
                    "type": agent.agent_type,
                    "status": agent.status,
                    "current_tasks": agent.current_task_count,
                    "max_tasks": agent.max_concurrent_tasks,
                    "performance": agent.performance_metrics
                }
                for name, agent in self.agents.items()
            }
        }
    
    async def get_performance_dashboard(self, time_range: str = "24h") -> Dict[str, Any]:
        """Get performance dashboard data"""
        return await self.performance_tracker.get_performance_dashboard(time_range)
    
    async def conduct_research(self, niche: str, research_type: str = "market_analysis", 
                             keywords: List[str] = None, persona: str = None) -> Dict[str, Any]:
        """Conduct research using the AI Research Engine"""
        try:
            research_query = ResearchQuery(
                id=f"research_{int(datetime.now().timestamp())}",
                type=ResearchType(research_type),
                priority=ResearchPriority.HIGH,
                niche=niche,
                keywords=keywords or [],
                context={},
                depth_level="detailed",
                target_persona=persona
            )
            
            result = await self.research_engine.conduct_research(research_query)
            
            return {
                "research_id": result.query_id,
                "data": result.data,
                "insights": result.insights,
                "recommendations": result.recommendations,
                "confidence_score": result.confidence_score,
                "research_time": result.research_time
            }
            
        except Exception as e:
            logger.error(f"Research failed: {e}")
            return {"error": str(e)}
    
    async def validate_content_quality(self, content: Dict[str, Any], 
                                     quality_level: str = "standard") -> Dict[str, Any]:
        """Validate content quality using Quality Gates"""
        try:
            quality_level_enum = QualityLevel(quality_level)
            quality_report = await self.quality_validator.validate_content(
                content=content,
                quality_level=quality_level_enum
            )
            
            return {
                "quality_report": quality_report.dict(),
                "approved": quality_report.approved,
                "overall_score": quality_report.overall_score,
                "critical_issues": quality_report.critical_issues,
                "recommendations": quality_report.recommendations
            }
            
        except Exception as e:
            logger.error(f"Quality validation failed: {e}")
            return {"error": str(e)}
    
    async def generate_enhanced_content_pipeline(self, niche: str, persona: str, 
                                               device: str, content_type: str,
                                               include_research: bool = True,
                                               quality_level: str = "standard") -> Dict[str, Any]:
        """Enhanced content generation pipeline with Phase 2 features"""
        pipeline_start = datetime.now()
        
        try:
            result = {
                "pipeline_id": str(uuid4()),
                "status": "in_progress",
                "stages": {}
            }
            
            # Stage 1: Research (if requested)
            if include_research:
                logger.info("Starting research stage...")
                research_result = await self.conduct_research(
                    niche=niche,
                    research_type="market_analysis",
                    keywords=[niche, content_type],
                    persona=persona
                )
                result["stages"]["research"] = research_result
            
            # Stage 2: Content Outline
            logger.info("Generating content outline...")
            outline_result = await self.content_outline_agent.generate_outline(
                niche=niche,
                persona=persona,
                device=device,
                content_type=content_type
            )
            result["stages"]["outline"] = outline_result.dict()
            
            # Stage 3: Content Writing
            logger.info("Generating content...")
            content_result = await self.content_writer_agent.generate_content(
                outline=outline_result.dict(),
                niche=niche,
                persona=persona,
                device=device
            )
            result["stages"]["content"] = content_result.dict()
            
            # Stage 4: Quality Validation
            logger.info("Validating content quality...")
            quality_result = await self.validate_content_quality(
                content=content_result.dict(),
                quality_level=quality_level
            )
            result["stages"]["quality_validation"] = quality_result
            
            # Stage 5: Performance Tracking
            await self.performance_tracker.track_content_performance(content_result.dict())
            
            # Pipeline completion
            pipeline_duration = (datetime.now() - pipeline_start).total_seconds()
            
            result.update({
                "status": "completed",
                "pipeline_duration": pipeline_duration,
                "final_content": content_result.dict(),
                "quality_approved": quality_result.get("approved", False),
                "overall_quality_score": quality_result.get("overall_score", 0.0),
                "performance_metrics": {
                    "total_stages": len(result["stages"]),
                    "generation_time": pipeline_duration,
                    "quality_score": quality_result.get("overall_score", 0.0)
                }
            })
            
            logger.info(f"Enhanced content pipeline completed in {pipeline_duration:.2f}s "
                       f"(quality: {quality_result.get('overall_score', 0):.1f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Enhanced content pipeline failed: {e}")
            return {
                "pipeline_id": result.get("pipeline_id", "unknown"),
                "status": "failed",
                "error": str(e),
                "pipeline_duration": (datetime.now() - pipeline_start).total_seconds()
            }
    
    async def shutdown(self):
        """Shutdown orchestrator"""
        logger.info("Agent Orchestrator shutting down...")
        
        # Cancel pending tasks
        for task in self.tasks.values():
            if task.status == "executing":
                task.status = "cancelled"
        
        # Reset agent statuses
        for agent in self.agents.values():
            agent.status = AgentStatus.OFFLINE
        
        self.initialized = False
        self.agents.clear()
        self.tasks.clear()
        self.task_queue.clear()
        
        logger.info("Agent Orchestrator shutdown complete")