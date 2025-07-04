#!/usr/bin/env python3
"""
Performance Tracking System - Real-time Agent & Content Performance Analytics
Module 3A: Phase 2 Implementation

Executor: Claude Code
Erstellt: 2025-07-04
Version: 1.0
"""

import logging
import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pydantic import BaseModel, Field
from enum import Enum
import statistics
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class MetricType(str, Enum):
    """Types of performance metrics"""
    AGENT_PERFORMANCE = "agent_performance"
    CONTENT_QUALITY = "content_quality"
    GENERATION_SPEED = "generation_speed"
    SYSTEM_HEALTH = "system_health"
    BUSINESS_IMPACT = "business_impact"
    USER_ENGAGEMENT = "user_engagement"

class AlertLevel(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    id: str
    type: MetricType
    name: str
    value: float
    unit: str
    timestamp: datetime
    context: Dict[str, Any] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.tags is None:
            self.tags = []

@dataclass
class PerformanceAlert:
    """Performance alert"""
    id: str
    level: AlertLevel
    message: str
    metric_type: MetricType
    threshold_value: float
    actual_value: float
    timestamp: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None

class AgentPerformanceData(BaseModel):
    """Agent performance tracking data"""
    agent_name: str
    agent_type: str
    total_tasks: int = Field(default=0)
    successful_tasks: int = Field(default=0)
    failed_tasks: int = Field(default=0)
    average_execution_time: float = Field(default=0.0)
    average_quality_score: float = Field(default=0.0)
    success_rate: float = Field(default=100.0)
    last_activity: datetime = Field(default_factory=datetime.now)
    performance_trend: str = Field(default="stable")  # improving, stable, declining

class ContentPerformanceData(BaseModel):
    """Content performance tracking data"""
    content_id: str
    content_type: str
    quality_score: float = Field(default=0.0)
    generation_time: float = Field(default=0.0)
    word_count: int = Field(default=0)
    readability_score: float = Field(default=0.0)
    seo_score: float = Field(default=0.0)
    engagement_prediction: float = Field(default=0.0)
    conversion_prediction: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.now)

class SystemHealthData(BaseModel):
    """System health tracking data"""
    timestamp: datetime = Field(default_factory=datetime.now)
    cpu_usage: float = Field(default=0.0)
    memory_usage: float = Field(default=0.0)
    active_agents: int = Field(default=0)
    queued_tasks: int = Field(default=0)
    processing_tasks: int = Field(default=0)
    error_rate: float = Field(default=0.0)
    average_response_time: float = Field(default=0.0)

class PerformanceTracker:
    """Comprehensive performance tracking and analytics system"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.metrics_buffer = deque(maxlen=10000)  # Rolling buffer of metrics
        self.alerts = deque(maxlen=1000)  # Rolling buffer of alerts
        
        # Performance data stores
        self.agent_performance = {}
        self.content_performance = {}
        self.system_health_history = deque(maxlen=100)
        
        # Aggregated statistics
        self.hourly_stats = defaultdict(dict)
        self.daily_stats = defaultdict(dict)
        
        # Alert thresholds
        self.alert_thresholds = self._initialize_alert_thresholds()
        
        # Performance trends
        self.trend_analysis = {}
        
        # Real-time monitoring flags
        self.monitoring_active = True
        self.last_health_check = datetime.now()
    
    def _initialize_alert_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize performance alert thresholds"""
        return {
            MetricType.AGENT_PERFORMANCE: {
                "success_rate_critical": 90.0,
                "success_rate_warning": 95.0,
                "avg_execution_time_warning": 5.0,
                "avg_execution_time_critical": 10.0,
                "quality_score_warning": 70.0,
                "quality_score_critical": 60.0
            },
            MetricType.CONTENT_QUALITY: {
                "quality_score_warning": 75.0,
                "quality_score_critical": 65.0,
                "readability_warning": 60.0,
                "readability_critical": 50.0,
                "seo_score_warning": 70.0,
                "seo_score_critical": 60.0
            },
            MetricType.GENERATION_SPEED: {
                "generation_time_warning": 3.0,
                "generation_time_critical": 5.0,
                "queue_length_warning": 10,
                "queue_length_critical": 20
            },
            MetricType.SYSTEM_HEALTH: {
                "cpu_usage_warning": 80.0,
                "cpu_usage_critical": 90.0,
                "memory_usage_warning": 85.0,
                "memory_usage_critical": 95.0,
                "error_rate_warning": 5.0,
                "error_rate_critical": 10.0
            }
        }
    
    async def track_agent_performance(self, agent_name: str, agent_type: str, 
                                    execution_time: float, success: bool, 
                                    quality_score: Optional[float] = None) -> None:
        """Track individual agent performance"""
        try:
            # Get or create agent performance data
            if agent_name not in self.agent_performance:
                self.agent_performance[agent_name] = AgentPerformanceData(
                    agent_name=agent_name,
                    agent_type=agent_type
                )
            
            perf_data = self.agent_performance[agent_name]
            
            # Update metrics
            perf_data.total_tasks += 1
            if success:
                perf_data.successful_tasks += 1
            else:
                perf_data.failed_tasks += 1
            
            # Update average execution time
            old_avg = perf_data.average_execution_time
            total_tasks = perf_data.total_tasks
            perf_data.average_execution_time = (
                (old_avg * (total_tasks - 1) + execution_time) / total_tasks
            )
            
            # Update quality score if provided
            if quality_score is not None:
                old_quality_avg = perf_data.average_quality_score
                successful_tasks = perf_data.successful_tasks
                if successful_tasks > 0:
                    perf_data.average_quality_score = (
                        (old_quality_avg * (successful_tasks - 1) + quality_score) / successful_tasks
                    )
            
            # Update success rate
            perf_data.success_rate = (perf_data.successful_tasks / perf_data.total_tasks) * 100
            
            # Update last activity
            perf_data.last_activity = datetime.now()
            
            # Update performance trend
            perf_data.performance_trend = await self._calculate_performance_trend(agent_name)
            
            # Record metrics
            await self._record_metric(
                PerformanceMetric(
                    id=f"agent_{agent_name}_{int(datetime.now().timestamp())}",
                    type=MetricType.AGENT_PERFORMANCE,
                    name="execution_time",
                    value=execution_time,
                    unit="seconds",
                    timestamp=datetime.now(),
                    context={"agent_name": agent_name, "success": success},
                    tags=[agent_type, "execution_time"]
                )
            )
            
            # Check for performance alerts
            await self._check_agent_performance_alerts(agent_name, perf_data)
            
            logger.debug(f"Updated performance for agent {agent_name}: "
                        f"success_rate={perf_data.success_rate:.1f}%, "
                        f"avg_time={perf_data.average_execution_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error tracking agent performance for {agent_name}: {e}")
    
    async def track_content_performance(self, content_data: Dict[str, Any]) -> None:
        """Track content generation performance"""
        try:
            content_id = content_data.get("id", f"content_{int(datetime.now().timestamp())}")
            
            # Extract performance metrics from content data
            metrics = content_data.get("metrics", {})
            seo_analysis = content_data.get("seo_analysis", {})
            
            # Create content performance record
            content_perf = ContentPerformanceData(
                content_id=content_id,
                content_type=content_data.get("type", "unknown"),
                quality_score=content_data.get("quality_score", 0.0),
                generation_time=content_data.get("generation_time", 0.0),
                word_count=metrics.get("word_count", 0),
                readability_score=metrics.get("readability_score", 0.0),
                seo_score=seo_analysis.get("overall_score", 0.0),
                engagement_prediction=metrics.get("engagement_score", 0.0),
                conversion_prediction=metrics.get("conversion_potential", 0.0)
            )
            
            # Store content performance
            self.content_performance[content_id] = content_perf
            
            # Record individual metrics
            await self._record_content_metrics(content_perf)
            
            # Check for content quality alerts
            await self._check_content_quality_alerts(content_perf)
            
            logger.debug(f"Tracked content performance for {content_id}: "
                        f"quality={content_perf.quality_score:.1f}, "
                        f"generation_time={content_perf.generation_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error tracking content performance: {e}")
    
    async def track_system_health(self, health_data: Dict[str, Any]) -> None:
        """Track system health metrics"""
        try:
            system_health = SystemHealthData(
                cpu_usage=health_data.get("cpu_usage", 0.0),
                memory_usage=health_data.get("memory_usage", 0.0),
                active_agents=health_data.get("active_agents", 0),
                queued_tasks=health_data.get("queued_tasks", 0),
                processing_tasks=health_data.get("processing_tasks", 0),
                error_rate=health_data.get("error_rate", 0.0),
                average_response_time=health_data.get("average_response_time", 0.0)
            )
            
            # Store in history
            self.system_health_history.append(system_health)
            
            # Record metrics
            await self._record_system_health_metrics(system_health)
            
            # Check for system health alerts
            await self._check_system_health_alerts(system_health)
            
            self.last_health_check = datetime.now()
            
            logger.debug(f"System health updated: CPU={system_health.cpu_usage:.1f}%, "
                        f"Memory={system_health.memory_usage:.1f}%, "
                        f"Active_agents={system_health.active_agents}")
            
        except Exception as e:
            logger.error(f"Error tracking system health: {e}")
    
    async def _record_metric(self, metric: PerformanceMetric) -> None:
        """Record a performance metric"""
        self.metrics_buffer.append(metric)
        
        # Update hourly/daily aggregations
        await self._update_aggregated_stats(metric)
    
    async def _record_content_metrics(self, content_perf: ContentPerformanceData) -> None:
        """Record content-specific metrics"""
        timestamp = content_perf.created_at
        
        metrics = [
            PerformanceMetric(
                id=f"content_quality_{content_perf.content_id}",
                type=MetricType.CONTENT_QUALITY,
                name="quality_score",
                value=content_perf.quality_score,
                unit="percentage",
                timestamp=timestamp,
                context={"content_id": content_perf.content_id},
                tags=[content_perf.content_type, "quality"]
            ),
            PerformanceMetric(
                id=f"content_generation_time_{content_perf.content_id}",
                type=MetricType.GENERATION_SPEED,
                name="generation_time",
                value=content_perf.generation_time,
                unit="seconds",
                timestamp=timestamp,
                context={"content_id": content_perf.content_id},
                tags=[content_perf.content_type, "generation_speed"]
            ),
            PerformanceMetric(
                id=f"content_readability_{content_perf.content_id}",
                type=MetricType.CONTENT_QUALITY,
                name="readability_score",
                value=content_perf.readability_score,
                unit="flesch_score",
                timestamp=timestamp,
                context={"content_id": content_perf.content_id},
                tags=[content_perf.content_type, "readability"]
            )
        ]
        
        for metric in metrics:
            await self._record_metric(metric)
    
    async def _record_system_health_metrics(self, health: SystemHealthData) -> None:
        """Record system health metrics"""
        metrics = [
            PerformanceMetric(
                id=f"system_cpu_{int(health.timestamp.timestamp())}",
                type=MetricType.SYSTEM_HEALTH,
                name="cpu_usage",
                value=health.cpu_usage,
                unit="percentage",
                timestamp=health.timestamp,
                tags=["system", "cpu"]
            ),
            PerformanceMetric(
                id=f"system_memory_{int(health.timestamp.timestamp())}",
                type=MetricType.SYSTEM_HEALTH,
                name="memory_usage",
                value=health.memory_usage,
                unit="percentage",
                timestamp=health.timestamp,
                tags=["system", "memory"]
            ),
            PerformanceMetric(
                id=f"system_agents_{int(health.timestamp.timestamp())}",
                type=MetricType.SYSTEM_HEALTH,
                name="active_agents",
                value=health.active_agents,
                unit="count",
                timestamp=health.timestamp,
                tags=["system", "agents"]
            )
        ]
        
        for metric in metrics:
            await self._record_metric(metric)
    
    async def _update_aggregated_stats(self, metric: PerformanceMetric) -> None:
        """Update hourly and daily aggregated statistics"""
        hour_key = metric.timestamp.strftime("%Y-%m-%d-%H")
        day_key = metric.timestamp.strftime("%Y-%m-%d")
        
        # Update hourly stats
        if hour_key not in self.hourly_stats:
            self.hourly_stats[hour_key] = defaultdict(list)
        
        self.hourly_stats[hour_key][f"{metric.type}_{metric.name}"].append(metric.value)
        
        # Update daily stats
        if day_key not in self.daily_stats:
            self.daily_stats[day_key] = defaultdict(list)
        
        self.daily_stats[day_key][f"{metric.type}_{metric.name}"].append(metric.value)
    
    async def _calculate_performance_trend(self, agent_name: str) -> str:
        """Calculate performance trend for an agent"""
        try:
            # Get recent metrics for this agent
            recent_metrics = [
                m for m in list(self.metrics_buffer)[-100:]  # Last 100 metrics
                if (m.type == MetricType.AGENT_PERFORMANCE and 
                    m.context.get("agent_name") == agent_name and
                    m.name == "execution_time")
            ]
            
            if len(recent_metrics) < 5:
                return "stable"  # Not enough data
            
            # Take last 10 measurements and compare with previous 10
            recent_values = [m.value for m in recent_metrics[-10:]]
            previous_values = [m.value for m in recent_metrics[-20:-10]] if len(recent_metrics) >= 20 else []
            
            if not previous_values:
                return "stable"
            
            recent_avg = statistics.mean(recent_values)
            previous_avg = statistics.mean(previous_values)
            
            # Calculate trend
            improvement_threshold = 0.1  # 10% improvement
            decline_threshold = 0.15     # 15% decline
            
            if recent_avg < previous_avg * (1 - improvement_threshold):
                return "improving"  # Execution time decreased (better)
            elif recent_avg > previous_avg * (1 + decline_threshold):
                return "declining"  # Execution time increased (worse)
            else:
                return "stable"
                
        except Exception as e:
            logger.error(f"Error calculating performance trend for {agent_name}: {e}")
            return "stable"
    
    async def _check_agent_performance_alerts(self, agent_name: str, 
                                            perf_data: AgentPerformanceData) -> None:
        """Check for agent performance alerts"""
        thresholds = self.alert_thresholds[MetricType.AGENT_PERFORMANCE]
        
        # Check success rate
        if perf_data.success_rate < thresholds["success_rate_critical"]:
            await self._create_alert(
                AlertLevel.CRITICAL,
                f"Agent {agent_name} success rate critically low: {perf_data.success_rate:.1f}%",
                MetricType.AGENT_PERFORMANCE,
                thresholds["success_rate_critical"],
                perf_data.success_rate
            )
        elif perf_data.success_rate < thresholds["success_rate_warning"]:
            await self._create_alert(
                AlertLevel.WARNING,
                f"Agent {agent_name} success rate below target: {perf_data.success_rate:.1f}%",
                MetricType.AGENT_PERFORMANCE,
                thresholds["success_rate_warning"],
                perf_data.success_rate
            )
        
        # Check execution time
        if perf_data.average_execution_time > thresholds["avg_execution_time_critical"]:
            await self._create_alert(
                AlertLevel.CRITICAL,
                f"Agent {agent_name} execution time critically high: {perf_data.average_execution_time:.2f}s",
                MetricType.AGENT_PERFORMANCE,
                thresholds["avg_execution_time_critical"],
                perf_data.average_execution_time
            )
        elif perf_data.average_execution_time > thresholds["avg_execution_time_warning"]:
            await self._create_alert(
                AlertLevel.WARNING,
                f"Agent {agent_name} execution time elevated: {perf_data.average_execution_time:.2f}s",
                MetricType.AGENT_PERFORMANCE,
                thresholds["avg_execution_time_warning"],
                perf_data.average_execution_time
            )
        
        # Check quality score
        if perf_data.average_quality_score > 0:  # Only check if we have quality data
            if perf_data.average_quality_score < thresholds["quality_score_critical"]:
                await self._create_alert(
                    AlertLevel.CRITICAL,
                    f"Agent {agent_name} quality score critically low: {perf_data.average_quality_score:.1f}",
                    MetricType.AGENT_PERFORMANCE,
                    thresholds["quality_score_critical"],
                    perf_data.average_quality_score
                )
            elif perf_data.average_quality_score < thresholds["quality_score_warning"]:
                await self._create_alert(
                    AlertLevel.WARNING,
                    f"Agent {agent_name} quality score below target: {perf_data.average_quality_score:.1f}",
                    MetricType.AGENT_PERFORMANCE,
                    thresholds["quality_score_warning"],
                    perf_data.average_quality_score
                )
    
    async def _check_content_quality_alerts(self, content_perf: ContentPerformanceData) -> None:
        """Check for content quality alerts"""
        thresholds = self.alert_thresholds[MetricType.CONTENT_QUALITY]
        
        # Check overall quality score
        if content_perf.quality_score < thresholds["quality_score_critical"]:
            await self._create_alert(
                AlertLevel.ERROR,
                f"Content {content_perf.content_id} quality critically low: {content_perf.quality_score:.1f}",
                MetricType.CONTENT_QUALITY,
                thresholds["quality_score_critical"],
                content_perf.quality_score
            )
        elif content_perf.quality_score < thresholds["quality_score_warning"]:
            await self._create_alert(
                AlertLevel.WARNING,
                f"Content {content_perf.content_id} quality below target: {content_perf.quality_score:.1f}",
                MetricType.CONTENT_QUALITY,
                thresholds["quality_score_warning"],
                content_perf.quality_score
            )
    
    async def _check_system_health_alerts(self, health: SystemHealthData) -> None:
        """Check for system health alerts"""
        thresholds = self.alert_thresholds[MetricType.SYSTEM_HEALTH]
        
        # Check CPU usage
        if health.cpu_usage > thresholds["cpu_usage_critical"]:
            await self._create_alert(
                AlertLevel.CRITICAL,
                f"System CPU usage critically high: {health.cpu_usage:.1f}%",
                MetricType.SYSTEM_HEALTH,
                thresholds["cpu_usage_critical"],
                health.cpu_usage
            )
        elif health.cpu_usage > thresholds["cpu_usage_warning"]:
            await self._create_alert(
                AlertLevel.WARNING,
                f"System CPU usage elevated: {health.cpu_usage:.1f}%",
                MetricType.SYSTEM_HEALTH,
                thresholds["cpu_usage_warning"],
                health.cpu_usage
            )
        
        # Check memory usage
        if health.memory_usage > thresholds["memory_usage_critical"]:
            await self._create_alert(
                AlertLevel.CRITICAL,
                f"System memory usage critically high: {health.memory_usage:.1f}%",
                MetricType.SYSTEM_HEALTH,
                thresholds["memory_usage_critical"],
                health.memory_usage
            )
        elif health.memory_usage > thresholds["memory_usage_warning"]:
            await self._create_alert(
                AlertLevel.WARNING,
                f"System memory usage elevated: {health.memory_usage:.1f}%",
                MetricType.SYSTEM_HEALTH,
                thresholds["memory_usage_warning"],
                health.memory_usage
            )
    
    async def _create_alert(self, level: AlertLevel, message: str, 
                          metric_type: MetricType, threshold_value: float, 
                          actual_value: float) -> None:
        """Create a performance alert"""
        alert = PerformanceAlert(
            id=f"alert_{int(datetime.now().timestamp())}_{len(self.alerts)}",
            level=level,
            message=message,
            metric_type=metric_type,
            threshold_value=threshold_value,
            actual_value=actual_value,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        
        # Log alert
        log_level = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.ERROR: logging.ERROR,
            AlertLevel.CRITICAL: logging.CRITICAL
        }.get(level, logging.INFO)
        
        logger.log(log_level, f"Performance Alert [{level.value.upper()}]: {message}")
    
    async def get_performance_dashboard(self, time_range: str = "24h") -> Dict[str, Any]:
        """Get comprehensive performance dashboard data"""
        try:
            end_time = datetime.now()
            
            # Calculate time range
            if time_range == "1h":
                start_time = end_time - timedelta(hours=1)
            elif time_range == "24h":
                start_time = end_time - timedelta(hours=24)
            elif time_range == "7d":
                start_time = end_time - timedelta(days=7)
            elif time_range == "30d":
                start_time = end_time - timedelta(days=30)
            else:
                start_time = end_time - timedelta(hours=24)
            
            # Get relevant metrics
            relevant_metrics = [
                m for m in self.metrics_buffer
                if start_time <= m.timestamp <= end_time
            ]
            
            # Agent performance summary
            agent_summary = await self._get_agent_performance_summary()
            
            # Content performance summary
            content_summary = await self._get_content_performance_summary(start_time)
            
            # System health summary
            system_summary = await self._get_system_health_summary()
            
            # Recent alerts
            recent_alerts = [
                alert for alert in self.alerts
                if start_time <= alert.timestamp <= end_time
            ]
            
            # Performance trends
            trends = await self._calculate_performance_trends(relevant_metrics)
            
            # Key metrics
            key_metrics = await self._calculate_key_metrics(relevant_metrics)
            
            dashboard = {
                "timestamp": end_time.isoformat(),
                "time_range": time_range,
                "summary": {
                    "total_agents": len(self.agent_performance),
                    "total_content_generated": len(self.content_performance),
                    "active_alerts": len([a for a in recent_alerts if not a.resolved]),
                    "system_health_score": await self._calculate_system_health_score()
                },
                "agent_performance": agent_summary,
                "content_performance": content_summary,
                "system_health": system_summary,
                "alerts": {
                    "total": len(recent_alerts),
                    "by_level": self._group_alerts_by_level(recent_alerts),
                    "recent": [asdict(alert) for alert in recent_alerts[-10:]]
                },
                "trends": trends,
                "key_metrics": key_metrics,
                "recommendations": await self._generate_performance_recommendations()
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error generating performance dashboard: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get agent performance summary"""
        if not self.agent_performance:
            return {"total_agents": 0}
        
        total_tasks = sum(agent.total_tasks for agent in self.agent_performance.values())
        total_successful = sum(agent.successful_tasks for agent in self.agent_performance.values())
        avg_success_rate = statistics.mean([agent.success_rate for agent in self.agent_performance.values()])
        avg_execution_time = statistics.mean([
            agent.average_execution_time for agent in self.agent_performance.values()
            if agent.average_execution_time > 0
        ]) if any(agent.average_execution_time > 0 for agent in self.agent_performance.values()) else 0.0
        
        # Top performing agents
        top_agents = sorted(
            self.agent_performance.values(),
            key=lambda x: (x.success_rate, -x.average_execution_time),
            reverse=True
        )[:5]
        
        return {
            "total_agents": len(self.agent_performance),
            "total_tasks": total_tasks,
            "total_successful": total_successful,
            "overall_success_rate": avg_success_rate,
            "average_execution_time": avg_execution_time,
            "top_performers": [
                {
                    "name": agent.agent_name,
                    "type": agent.agent_type,
                    "success_rate": agent.success_rate,
                    "avg_time": agent.average_execution_time,
                    "trend": agent.performance_trend
                }
                for agent in top_agents
            ],
            "by_type": self._group_agents_by_type()
        }
    
    async def _get_content_performance_summary(self, start_time: datetime) -> Dict[str, Any]:
        """Get content performance summary"""
        recent_content = [
            content for content in self.content_performance.values()
            if content.created_at >= start_time
        ]
        
        if not recent_content:
            return {"total_content": 0, "period": "no_data"}
        
        avg_quality = statistics.mean([content.quality_score for content in recent_content])
        avg_generation_time = statistics.mean([content.generation_time for content in recent_content])
        avg_readability = statistics.mean([content.readability_score for content in recent_content])
        
        return {
            "total_content": len(recent_content),
            "average_quality_score": avg_quality,
            "average_generation_time": avg_generation_time,
            "average_readability": avg_readability,
            "by_type": self._group_content_by_type(recent_content),
            "quality_distribution": self._calculate_quality_distribution(recent_content)
        }
    
    async def _get_system_health_summary(self) -> Dict[str, Any]:
        """Get system health summary"""
        if not self.system_health_history:
            return {"status": "no_data"}
        
        latest_health = self.system_health_history[-1]
        
        # Calculate averages over last 10 measurements
        recent_health = list(self.system_health_history)[-10:]
        avg_cpu = statistics.mean([h.cpu_usage for h in recent_health])
        avg_memory = statistics.mean([h.memory_usage for h in recent_health])
        avg_response_time = statistics.mean([h.average_response_time for h in recent_health])
        
        return {
            "current": {
                "cpu_usage": latest_health.cpu_usage,
                "memory_usage": latest_health.memory_usage,
                "active_agents": latest_health.active_agents,
                "queued_tasks": latest_health.queued_tasks,
                "error_rate": latest_health.error_rate
            },
            "averages": {
                "cpu_usage": avg_cpu,
                "memory_usage": avg_memory,
                "response_time": avg_response_time
            },
            "status": await self._determine_system_status(latest_health),
            "last_update": latest_health.timestamp.isoformat()
        }
    
    def _group_alerts_by_level(self, alerts: List[PerformanceAlert]) -> Dict[str, int]:
        """Group alerts by severity level"""
        counts = defaultdict(int)
        for alert in alerts:
            counts[alert.level.value] += 1
        return dict(counts)
    
    def _group_agents_by_type(self) -> Dict[str, Dict[str, Any]]:
        """Group agent performance by type"""
        by_type = defaultdict(list)
        
        for agent in self.agent_performance.values():
            by_type[agent.agent_type].append(agent)
        
        summary = {}
        for agent_type, agents in by_type.items():
            summary[agent_type] = {
                "count": len(agents),
                "avg_success_rate": statistics.mean([a.success_rate for a in agents]),
                "avg_execution_time": statistics.mean([
                    a.average_execution_time for a in agents if a.average_execution_time > 0
                ]) if any(a.average_execution_time > 0 for a in agents) else 0.0,
                "total_tasks": sum(a.total_tasks for a in agents)
            }
        
        return summary
    
    def _group_content_by_type(self, content_list: List[ContentPerformanceData]) -> Dict[str, Dict[str, Any]]:
        """Group content performance by type"""
        by_type = defaultdict(list)
        
        for content in content_list:
            by_type[content.content_type].append(content)
        
        summary = {}
        for content_type, contents in by_type.items():
            summary[content_type] = {
                "count": len(contents),
                "avg_quality": statistics.mean([c.quality_score for c in contents]),
                "avg_generation_time": statistics.mean([c.generation_time for c in contents]),
                "avg_word_count": statistics.mean([c.word_count for c in contents])
            }
        
        return summary
    
    def _calculate_quality_distribution(self, content_list: List[ContentPerformanceData]) -> Dict[str, int]:
        """Calculate quality score distribution"""
        distribution = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}
        
        for content in content_list:
            if content.quality_score >= 90:
                distribution["excellent"] += 1
            elif content.quality_score >= 75:
                distribution["good"] += 1
            elif content.quality_score >= 60:
                distribution["fair"] += 1
            else:
                distribution["poor"] += 1
        
        return distribution
    
    async def _calculate_performance_trends(self, metrics: List[PerformanceMetric]) -> Dict[str, str]:
        """Calculate performance trends from metrics"""
        trends = {}
        
        # Group metrics by type and name
        metric_groups = defaultdict(list)
        for metric in metrics:
            key = f"{metric.type}_{metric.name}"
            metric_groups[key].append(metric.value)
        
        # Calculate trends for each metric group
        for metric_key, values in metric_groups.items():
            if len(values) < 5:
                trends[metric_key] = "insufficient_data"
                continue
            
            # Compare first half with second half
            mid_point = len(values) // 2
            first_half = values[:mid_point]
            second_half = values[mid_point:]
            
            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)
            
            if second_avg > first_avg * 1.05:
                trends[metric_key] = "increasing"
            elif second_avg < first_avg * 0.95:
                trends[metric_key] = "decreasing"
            else:
                trends[metric_key] = "stable"
        
        return trends
    
    async def _calculate_key_metrics(self, metrics: List[PerformanceMetric]) -> Dict[str, float]:
        """Calculate key performance indicators"""
        key_metrics = {}
        
        # Group metrics by type
        by_type = defaultdict(list)
        for metric in metrics:
            by_type[metric.type].append(metric.value)
        
        # Calculate averages for each type
        for metric_type, values in by_type.items():
            if values:
                key_metrics[f"avg_{metric_type}"] = statistics.mean(values)
                key_metrics[f"max_{metric_type}"] = max(values)
                key_metrics[f"min_{metric_type}"] = min(values)
        
        return key_metrics
    
    async def _calculate_system_health_score(self) -> float:
        """Calculate overall system health score"""
        if not self.system_health_history:
            return 0.0
        
        latest_health = self.system_health_history[-1]
        
        # Calculate health score based on various factors
        cpu_score = max(0, 100 - latest_health.cpu_usage)
        memory_score = max(0, 100 - latest_health.memory_usage)
        error_score = max(0, 100 - latest_health.error_rate * 10)
        
        # Weight the scores
        health_score = (cpu_score * 0.3 + memory_score * 0.3 + error_score * 0.4)
        
        return min(100.0, max(0.0, health_score))
    
    async def _determine_system_status(self, health: SystemHealthData) -> str:
        """Determine system status based on health metrics"""
        if health.cpu_usage > 90 or health.memory_usage > 95 or health.error_rate > 10:
            return "critical"
        elif health.cpu_usage > 80 or health.memory_usage > 85 or health.error_rate > 5:
            return "warning"
        elif health.cpu_usage > 70 or health.memory_usage > 75 or health.error_rate > 2:
            return "caution"
        else:
            return "healthy"
    
    async def _generate_performance_recommendations(self) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        # Check agent performance
        poor_performing_agents = [
            agent for agent in self.agent_performance.values()
            if agent.success_rate < 95.0 or agent.average_execution_time > 3.0
        ]
        
        if poor_performing_agents:
            recommendations.append(
                f"Review performance of {len(poor_performing_agents)} underperforming agents"
            )
        
        # Check content quality
        recent_content = list(self.content_performance.values())[-50:]  # Last 50 pieces
        low_quality_count = len([c for c in recent_content if c.quality_score < 75.0])
        
        if low_quality_count > len(recent_content) * 0.2:  # More than 20% low quality
            recommendations.append("Implement stricter quality gates to improve content standards")
        
        # Check system health
        if self.system_health_history:
            latest_health = self.system_health_history[-1]
            if latest_health.cpu_usage > 80:
                recommendations.append("Consider scaling system resources due to high CPU usage")
            if latest_health.queued_tasks > 10:
                recommendations.append("Optimize task processing to reduce queue length")
        
        # Check alert frequency
        recent_alerts = [
            alert for alert in self.alerts
            if alert.timestamp > datetime.now() - timedelta(hours=24)
        ]
        
        if len(recent_alerts) > 10:
            recommendations.append("High alert frequency detected - review system stability")
        
        if not recommendations:
            recommendations.append("System performance is operating within normal parameters")
        
        return recommendations
    
    async def get_agent_metrics(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed metrics for a specific agent"""
        if agent_name not in self.agent_performance:
            return None
        
        agent_data = self.agent_performance[agent_name]
        
        # Get recent metrics for this agent
        recent_metrics = [
            m for m in list(self.metrics_buffer)[-200:]
            if (m.type == MetricType.AGENT_PERFORMANCE and 
                m.context.get("agent_name") == agent_name)
        ]
        
        return {
            "agent_info": asdict(agent_data),
            "recent_performance": [asdict(m) for m in recent_metrics[-20:]],
            "performance_history": await self._get_agent_performance_history(agent_name),
            "recommendations": await self._get_agent_recommendations(agent_data)
        }
    
    async def _get_agent_performance_history(self, agent_name: str) -> Dict[str, List[float]]:
        """Get performance history for an agent"""
        # This would typically query a time-series database
        # For now, return recent metrics from buffer
        recent_metrics = [
            m for m in list(self.metrics_buffer)
            if (m.type == MetricType.AGENT_PERFORMANCE and 
                m.context.get("agent_name") == agent_name)
        ]
        
        execution_times = [m.value for m in recent_metrics if m.name == "execution_time"]
        
        return {
            "execution_times": execution_times[-50:],  # Last 50 measurements
            "timestamps": [m.timestamp.isoformat() for m in recent_metrics[-50:]]
        }
    
    async def _get_agent_recommendations(self, agent_data: AgentPerformanceData) -> List[str]:
        """Get performance recommendations for a specific agent"""
        recommendations = []
        
        if agent_data.success_rate < 95.0:
            recommendations.append("Review error handling and input validation")
        
        if agent_data.average_execution_time > 3.0:
            recommendations.append("Optimize processing algorithms for better performance")
        
        if agent_data.performance_trend == "declining":
            recommendations.append("Investigate recent changes that may impact performance")
        
        if agent_data.average_quality_score < 75.0 and agent_data.average_quality_score > 0:
            recommendations.append("Review quality parameters and improve output standards")
        
        return recommendations
    
    async def export_performance_data(self, format: str = "json", 
                                    time_range: str = "24h") -> Dict[str, Any]:
        """Export performance data in specified format"""
        dashboard_data = await self.get_performance_dashboard(time_range)
        
        if format == "json":
            return dashboard_data
        elif format == "csv":
            # Convert to CSV-friendly format
            return {"message": "CSV export not implemented yet", "data": dashboard_data}
        else:
            return {"error": "Unsupported format", "supported": ["json", "csv"]}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        return {
            "monitoring_active": self.monitoring_active,
            "last_health_check": self.last_health_check.isoformat(),
            "metrics_buffer_size": len(self.metrics_buffer),
            "alerts_count": len(self.alerts),
            "tracked_agents": len(self.agent_performance),
            "tracked_content": len(self.content_performance),
            "system_health_records": len(self.system_health_history)
        }