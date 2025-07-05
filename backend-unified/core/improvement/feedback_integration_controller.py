#!/usr/bin/env python3
"""
Feedback Integration Controller - Week 4 Implementation
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 4 - Feedback-Driven Improvement System

Integrates all feedback-driven components into a unified system with
cross-component feedback loops and coordinated optimization.

Features:
- Unified feedback collection across all components
- Cross-component learning coordination
- Integrated optimization orchestration
- Real-time performance monitoring
- Automated improvement workflows

Executor: Claude Code
Created: 2025-07-05
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Import improvement system components
from .feedback_system import FeedbackDrivenImprovementSystem, FeedbackType, LearningInsight
from .analytics_integration import PerformanceAnalyticsEngine, PerformanceMetric, MetricType
from .optimization_engine import ContinuousOptimizationEngine, OptimizationType, OptimizationScope

# Import core system components
from ..testing.ab_testing_framework import ABTestingFramework
from ...src.api.journey.personalization_engine_enhanced import EnhancedPersonalizationEngine
from ...src.api.journey.models import JourneySession, PersonalizedContent
from ..agents.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)

class FeedbackLoopType(str, Enum):
    """Types of feedback loops"""
    PERSONALIZATION_PERFORMANCE = "personalization_performance"
    AB_TEST_RESULTS = "ab_test_results"
    USER_BEHAVIOR = "user_behavior"
    SYSTEM_PERFORMANCE = "system_performance"
    CROSS_COMPONENT = "cross_component"

@dataclass
class FeedbackLoopStatus:
    """Status of a feedback loop"""
    loop_id: str
    loop_type: FeedbackLoopType
    source_component: str
    target_component: str
    is_active: bool
    last_feedback_time: datetime
    feedback_count: int
    effectiveness_score: float

@dataclass
class IntegrationMetrics:
    """Integration system metrics"""
    timestamp: datetime
    total_feedback_events: int
    active_feedback_loops: int
    learning_velocity: float
    optimization_frequency: float
    cross_component_correlations: int
    system_health_score: float

class FeedbackIntegrationController:
    """
    Feedback Integration Controller for coordinated improvement system
    
    Coordinates all feedback-driven components to create a unified
    improvement system with cross-component learning and optimization.
    """
    
    def __init__(self,
                 feedback_system: FeedbackDrivenImprovementSystem,
                 analytics_engine: PerformanceAnalyticsEngine,
                 optimization_engine: ContinuousOptimizationEngine,
                 ab_testing_framework: ABTestingFramework,
                 personalization_engine: EnhancedPersonalizationEngine,
                 orchestrator: AgentOrchestrator):
        
        # Core components
        self.feedback_system = feedback_system
        self.analytics_engine = analytics_engine
        self.optimization_engine = optimization_engine
        self.ab_testing_framework = ab_testing_framework
        self.personalization_engine = personalization_engine
        self.orchestrator = orchestrator
        
        # Feedback loop management
        self.feedback_loops: Dict[str, FeedbackLoopStatus] = {}
        self.integration_metrics: List[IntegrationMetrics] = []
        
        # Component event handlers
        self.component_handlers = {
            'personalization_engine': self._handle_personalization_feedback,
            'ab_testing_framework': self._handle_ab_test_feedback,
            'analytics_engine': self._handle_analytics_feedback,
            'optimization_engine': self._handle_optimization_feedback
        }
        
        # Cross-component correlations
        self.correlation_patterns: Dict[str, List[Dict[str, Any]]] = {}
        
        # Configuration
        self.config = {
            'feedback_integration_interval': 60,  # 1 minute
            'correlation_analysis_interval': 300,  # 5 minutes
            'health_check_interval': 180,  # 3 minutes
            'metrics_retention_hours': 24,
            'min_correlation_confidence': 0.7,
            'max_feedback_loops': 50
        }
        
        # Background tasks
        self.integration_task = None
        self.correlation_task = None
        self.health_monitor_task = None
        
    async def initialize(self):
        """Initialize the feedback integration controller"""
        try:
            logger.info("Initializing Feedback Integration Controller...")
            
            # Initialize feedback loops
            await self._setup_core_feedback_loops()
            
            # Start background tasks
            await self._start_background_tasks()
            
            logger.info("Feedback Integration Controller initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing feedback integration controller: {e}")
            raise
    
    async def collect_personalization_feedback(self, 
                                             session: JourneySession,
                                             personalized_content: PersonalizedContent,
                                             performance_data: Dict[str, Any]) -> None:
        """
        Collect and integrate personalization feedback
        
        Args:
            session: Journey session
            personalized_content: Generated personalized content
            performance_data: Performance metrics
        """
        try:
            # Collect analytics feedback
            await self.analytics_engine.track_personalization_effectiveness(
                session_id=session.session_id,
                personalization_strategy=personalized_content.personalization_strategy,
                persona_detected=session.persona_type or "unknown",
                persona_confidence=session.persona_confidence or 0.5,
                conversion_outcome=performance_data.get('conversion_achieved', False),
                engagement_metrics=performance_data.get('engagement_metrics', {})
            )
            
            # Create performance metric
            personalization_metric = PerformanceMetric(
                metric_type=MetricType.PERSONALIZATION_EFFECTIVENESS,
                value=performance_data.get('personalization_effectiveness', 0.5),
                timestamp=datetime.utcnow(),
                context={
                    'personalization_strategy': personalized_content.personalization_strategy,
                    'persona_type': session.persona_type,
                    'device_type': session.device_type
                },
                session_id=session.session_id,
                persona_type=session.persona_type,
                device_type=session.device_type
            )
            
            # Track in analytics engine
            await self.analytics_engine.track_performance_metric(personalization_metric)
            
            # Collect feedback in improvement system
            await self.feedback_system.collect_feedback(
                feedback_type=FeedbackType.PERSONALIZATION_EFFECTIVENESS,
                source_component="personalization_engine",
                data={
                    'session_id': session.session_id,
                    'personalization_strategy': personalized_content.personalization_strategy,
                    'persona_detected': session.persona_type,
                    'persona_confidence': session.persona_confidence,
                    'performance_data': performance_data
                },
                session_id=session.session_id,
                context={
                    'device_type': session.device_type,
                    'user_agent': session.device_info.get('user_agent', ''),
                    'journey_stage': session.current_stage
                }
            )
            
            # Update feedback loop status
            await self._update_feedback_loop_status(
                "personalization_performance", 
                "personalization_engine",
                performance_data.get('personalization_effectiveness', 0.5)
            )
            
        except Exception as e:
            logger.error(f"Error collecting personalization feedback: {e}")
    
    async def collect_ab_test_feedback(self,
                                     test_id: str,
                                     variant_id: str,
                                     session_id: str,
                                     performance_data: Dict[str, Any]) -> None:
        """
        Collect and integrate A/B test feedback
        
        Args:
            test_id: A/B test identifier
            variant_id: Test variant identifier
            session_id: Session identifier
            performance_data: Performance metrics
        """
        try:
            # Track A/B test performance
            await self.ab_testing_framework.track_performance(
                session_id=session_id,
                test_id=test_id,
                performance_data=performance_data
            )
            
            # Create performance metric
            ab_test_metric = PerformanceMetric(
                metric_type=MetricType.AB_TEST_PERFORMANCE,
                value=performance_data.get('conversion_rate', 0.0),
                timestamp=datetime.utcnow(),
                context={
                    'test_id': test_id,
                    'variant_id': variant_id,
                    'performance_data': performance_data
                },
                session_id=session_id,
                variant_id=variant_id
            )
            
            # Track in analytics engine
            await self.analytics_engine.track_performance_metric(ab_test_metric)
            
            # Collect feedback in improvement system
            await self.feedback_system.collect_feedback(
                feedback_type=FeedbackType.AB_TEST_RESULTS,
                source_component="ab_testing_framework",
                data={
                    'test_id': test_id,
                    'variant_id': variant_id,
                    'session_id': session_id,
                    'performance_data': performance_data
                },
                session_id=session_id,
                context={
                    'test_metadata': await self._get_test_metadata(test_id)
                }
            )
            
            # Update feedback loop status
            await self._update_feedback_loop_status(
                "ab_test_results",
                "ab_testing_framework", 
                performance_data.get('conversion_rate', 0.0)
            )
            
        except Exception as e:
            logger.error(f"Error collecting A/B test feedback: {e}")
    
    async def collect_user_behavior_feedback(self,
                                           session_id: str,
                                           behavior_data: Dict[str, Any]) -> None:
        """
        Collect and integrate user behavior feedback
        
        Args:
            session_id: Session identifier
            behavior_data: User behavior metrics
        """
        try:
            # Create engagement metric
            engagement_metric = PerformanceMetric(
                metric_type=MetricType.ENGAGEMENT_SCORE,
                value=behavior_data.get('engagement_score', 0.5),
                timestamp=datetime.utcnow(),
                context=behavior_data,
                session_id=session_id
            )
            
            # Track in analytics engine
            await self.analytics_engine.track_performance_metric(engagement_metric)
            
            # Collect feedback in improvement system
            await self.feedback_system.collect_feedback(
                feedback_type=FeedbackType.USER_BEHAVIOR,
                source_component="user_interface",
                data=behavior_data,
                session_id=session_id
            )
            
            # Update feedback loop status
            await self._update_feedback_loop_status(
                "user_behavior",
                "user_interface",
                behavior_data.get('engagement_score', 0.5)
            )
            
        except Exception as e:
            logger.error(f"Error collecting user behavior feedback: {e}")
    
    async def trigger_cross_component_optimization(self) -> Dict[str, Any]:
        """
        Trigger optimization across multiple components
        
        Returns:
            Optimization results
        """
        try:
            logger.info("Triggering cross-component optimization")
            
            # Get insights from feedback system
            insights = await self.feedback_system.generate_learning_insights()
            
            # Create optimization actions
            actions = await self.feedback_system.create_optimization_actions(insights)
            
            # Execute cross-component optimization
            optimization_id = await self.optimization_engine.trigger_optimization(
                optimization_type=OptimizationType.TRIGGERED,
                scope=OptimizationScope.CROSS_COMPONENT
            )
            
            # Execute improvement actions
            execution_result = await self.feedback_system.execute_optimization_actions()
            
            # Collect cross-component feedback
            await self.feedback_system.collect_feedback(
                feedback_type=FeedbackType.PERFORMANCE_METRICS,
                source_component="integration_controller",
                data={
                    'optimization_id': optimization_id,
                    'insights_generated': len(insights),
                    'actions_created': len(actions),
                    'execution_result': execution_result
                }
            )
            
            return {
                'optimization_id': optimization_id,
                'insights_generated': len(insights),
                'actions_created': len(actions),
                'execution_result': execution_result,
                'success': execution_result.get('successful', 0) > 0
            }
            
        except Exception as e:
            logger.error(f"Error in cross-component optimization: {e}")
            return {'error': str(e), 'success': False}
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """
        Get comprehensive integration status
        
        Returns:
            Integration status information
        """
        try:
            # Get current metrics
            current_time = datetime.utcnow()
            
            # Calculate system health
            health_score = await self._calculate_system_health()
            
            # Get active feedback loops
            active_loops = [loop for loop in self.feedback_loops.values() if loop.is_active]
            
            # Get recent integration metrics
            recent_metrics = [
                metric for metric in self.integration_metrics
                if metric.timestamp >= current_time - timedelta(hours=1)
            ]
            
            # Calculate learning velocity
            learning_velocity = await self._calculate_learning_velocity()
            
            # Get correlation insights
            correlations = await self._get_correlation_insights()
            
            return {
                'timestamp': current_time.isoformat(),
                'system_health_score': health_score,
                'active_feedback_loops': len(active_loops),
                'total_feedback_loops': len(self.feedback_loops),
                'learning_velocity': learning_velocity,
                'recent_metrics': {
                    'count': len(recent_metrics),
                    'avg_feedback_events': sum(m.total_feedback_events for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0,
                    'avg_optimization_frequency': sum(m.optimization_frequency for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0
                },
                'correlation_insights': correlations,
                'component_status': await self._get_component_status(),
                'feedback_loop_details': {
                    loop.loop_id: {
                        'type': loop.loop_type.value,
                        'source': loop.source_component,
                        'target': loop.target_component,
                        'active': loop.is_active,
                        'effectiveness': loop.effectiveness_score,
                        'feedback_count': loop.feedback_count
                    }
                    for loop in self.feedback_loops.values()
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting integration status: {e}")
            return {'error': str(e)}
    
    async def get_performance_dashboard_data(self) -> Dict[str, Any]:
        """
        Get comprehensive performance dashboard data
        
        Returns:
            Dashboard data
        """
        try:
            # Get analytics dashboard data
            analytics_data = await self.analytics_engine.get_real_time_dashboard_data()
            
            # Get optimization status
            optimization_status = await self.optimization_engine.get_optimization_status()
            
            # Get feedback system analytics
            feedback_analytics = await self.feedback_system.get_performance_analytics()
            
            # Get integration status
            integration_status = await self.get_integration_status()
            
            # Combine all data
            dashboard_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'analytics': analytics_data,
                'optimization': optimization_status,
                'feedback_system': feedback_analytics,
                'integration': integration_status,
                'summary': {
                    'overall_health': integration_status.get('system_health_score', 0.0),
                    'active_optimizations': optimization_status.get('active_optimizations', 0),
                    'learning_velocity': integration_status.get('learning_velocity', 0.0),
                    'feedback_loops_active': integration_status.get('active_feedback_loops', 0)
                }
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error getting performance dashboard data: {e}")
            return {'error': str(e)}
    
    # =============================================================================
    # INTERNAL IMPLEMENTATION METHODS
    # =============================================================================
    
    async def _setup_core_feedback_loops(self):
        """Setup core feedback loops between components"""
        try:
            # Personalization -> Analytics feedback loop
            await self._create_feedback_loop(
                loop_type=FeedbackLoopType.PERSONALIZATION_PERFORMANCE,
                source_component="personalization_engine",
                target_component="analytics_engine"
            )
            
            # A/B Testing -> Analytics feedback loop
            await self._create_feedback_loop(
                loop_type=FeedbackLoopType.AB_TEST_RESULTS,
                source_component="ab_testing_framework",
                target_component="analytics_engine"
            )
            
            # Analytics -> Optimization feedback loop
            await self._create_feedback_loop(
                loop_type=FeedbackLoopType.SYSTEM_PERFORMANCE,
                source_component="analytics_engine",
                target_component="optimization_engine"
            )
            
            # Cross-component feedback loop
            await self._create_feedback_loop(
                loop_type=FeedbackLoopType.CROSS_COMPONENT,
                source_component="optimization_engine",
                target_component="personalization_engine"
            )
            
            logger.info(f"Created {len(self.feedback_loops)} core feedback loops")
            
        except Exception as e:
            logger.error(f"Error setting up feedback loops: {e}")
            raise
    
    async def _create_feedback_loop(self,
                                  loop_type: FeedbackLoopType,
                                  source_component: str,
                                  target_component: str) -> str:
        """Create a feedback loop between components"""
        try:
            loop_id = f"{source_component}_to_{target_component}_{loop_type.value}"
            
            feedback_loop = FeedbackLoopStatus(
                loop_id=loop_id,
                loop_type=loop_type,
                source_component=source_component,
                target_component=target_component,
                is_active=True,
                last_feedback_time=datetime.utcnow(),
                feedback_count=0,
                effectiveness_score=0.5
            )
            
            self.feedback_loops[loop_id] = feedback_loop
            
            logger.debug(f"Created feedback loop: {loop_id}")
            return loop_id
            
        except Exception as e:
            logger.error(f"Error creating feedback loop: {e}")
            raise
    
    async def _update_feedback_loop_status(self,
                                         loop_type: str,
                                         source_component: str,
                                         effectiveness_score: float) -> None:
        """Update feedback loop status"""
        try:
            # Find matching loop
            matching_loops = [
                loop for loop in self.feedback_loops.values()
                if (loop.source_component == source_component and
                    loop_type in loop.loop_type.value)
            ]
            
            for loop in matching_loops:
                loop.last_feedback_time = datetime.utcnow()
                loop.feedback_count += 1
                
                # Update effectiveness score using exponential moving average
                alpha = 0.1  # Learning rate
                loop.effectiveness_score = (
                    alpha * effectiveness_score + 
                    (1 - alpha) * loop.effectiveness_score
                )
                
        except Exception as e:
            logger.error(f"Error updating feedback loop status: {e}")
    
    async def _start_background_tasks(self):
        """Start background integration tasks"""
        try:
            # Start integration monitor
            self.integration_task = asyncio.create_task(
                self._integration_monitor_loop()
            )
            
            # Start correlation analyzer
            self.correlation_task = asyncio.create_task(
                self._correlation_analysis_loop()
            )
            
            # Start health monitor
            self.health_monitor_task = asyncio.create_task(
                self._health_monitor_loop()
            )
            
            logger.info("Background integration tasks started")
            
        except Exception as e:
            logger.error(f"Error starting background tasks: {e}")
            raise
    
    async def _integration_monitor_loop(self):
        """Background loop for integration monitoring"""
        while True:
            try:
                await asyncio.sleep(self.config['feedback_integration_interval'])
                
                # Collect integration metrics
                await self._collect_integration_metrics()
                
                # Check for stale feedback loops
                await self._check_feedback_loop_health()
                
            except Exception as e:
                logger.error(f"Error in integration monitor loop: {e}")
                await asyncio.sleep(30)  # Wait before retry
    
    async def _correlation_analysis_loop(self):
        """Background loop for correlation analysis"""
        while True:
            try:
                await asyncio.sleep(self.config['correlation_analysis_interval'])
                
                # Analyze cross-component correlations
                await self._analyze_cross_component_correlations()
                
            except Exception as e:
                logger.error(f"Error in correlation analysis loop: {e}")
                await asyncio.sleep(60)  # Wait before retry
    
    async def _health_monitor_loop(self):
        """Background loop for health monitoring"""
        while True:
            try:
                await asyncio.sleep(self.config['health_check_interval'])
                
                # Check system health
                health_score = await self._calculate_system_health()
                
                # Log health issues
                if health_score < 0.7:
                    logger.warning(f"System health below threshold: {health_score:.2f}")
                
            except Exception as e:
                logger.error(f"Error in health monitor loop: {e}")
                await asyncio.sleep(60)  # Wait before retry
    
    async def _collect_integration_metrics(self):
        """Collect integration system metrics"""
        try:
            # Count feedback events
            total_feedback = sum(loop.feedback_count for loop in self.feedback_loops.values())
            
            # Count active loops
            active_loops = sum(1 for loop in self.feedback_loops.values() if loop.is_active)
            
            # Calculate learning velocity
            learning_velocity = await self._calculate_learning_velocity()
            
            # Calculate optimization frequency
            optimization_frequency = await self._calculate_optimization_frequency()
            
            # Count correlations
            correlations = sum(len(patterns) for patterns in self.correlation_patterns.values())
            
            # Calculate system health
            health_score = await self._calculate_system_health()
            
            # Create metrics
            metrics = IntegrationMetrics(
                timestamp=datetime.utcnow(),
                total_feedback_events=total_feedback,
                active_feedback_loops=active_loops,
                learning_velocity=learning_velocity,
                optimization_frequency=optimization_frequency,
                cross_component_correlations=correlations,
                system_health_score=health_score
            )
            
            # Store metrics
            self.integration_metrics.append(metrics)
            
            # Clean up old metrics
            cutoff_time = datetime.utcnow() - timedelta(hours=self.config['metrics_retention_hours'])
            self.integration_metrics = [
                m for m in self.integration_metrics
                if m.timestamp >= cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Error collecting integration metrics: {e}")
    
    async def _calculate_system_health(self) -> float:
        """Calculate overall system health score"""
        try:
            health_components = []
            
            # Feedback loop health (25%)
            active_loops = sum(1 for loop in self.feedback_loops.values() if loop.is_active)
            total_loops = len(self.feedback_loops)
            loop_health = active_loops / total_loops if total_loops > 0 else 0.0
            health_components.append(loop_health * 0.25)
            
            # Effectiveness health (25%)
            effectiveness_scores = [loop.effectiveness_score for loop in self.feedback_loops.values()]
            avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0.0
            health_components.append(avg_effectiveness * 0.25)
            
            # Learning velocity health (25%)
            learning_velocity = await self._calculate_learning_velocity()
            velocity_health = min(1.0, learning_velocity / 0.1)  # Normalize to 0.1 as max
            health_components.append(velocity_health * 0.25)
            
            # Component availability health (25%)
            component_health = await self._calculate_component_health()
            health_components.append(component_health * 0.25)
            
            return sum(health_components)
            
        except Exception as e:
            logger.error(f"Error calculating system health: {e}")
            return 0.5
    
    async def _calculate_learning_velocity(self) -> float:
        """Calculate system learning velocity"""
        try:
            # Get recent insights
            recent_insights = [
                insight for insight in self.feedback_system.learning_insights.values()
                if insight.timestamp >= datetime.utcnow() - timedelta(hours=1)
            ]
            
            # Calculate insights per hour
            return len(recent_insights)
            
        except Exception as e:
            logger.error(f"Error calculating learning velocity: {e}")
            return 0.0
    
    async def _calculate_optimization_frequency(self) -> float:
        """Calculate optimization frequency"""
        try:
            # Get recent optimizations
            recent_optimizations = [
                opt for opt in self.optimization_engine.optimization_history
                if opt.timestamp >= datetime.utcnow() - timedelta(hours=1)
            ]
            
            # Calculate optimizations per hour
            return len(recent_optimizations)
            
        except Exception as e:
            logger.error(f"Error calculating optimization frequency: {e}")
            return 0.0
    
    async def _calculate_component_health(self) -> float:
        """Calculate component availability health"""
        try:
            # Check if components are responding
            components = [
                self.feedback_system,
                self.analytics_engine,
                self.optimization_engine,
                self.ab_testing_framework,
                self.personalization_engine
            ]
            
            # Simple health check - all components are available
            return 1.0  # In real implementation, would ping each component
            
        except Exception as e:
            logger.error(f"Error calculating component health: {e}")
            return 0.0
    
    # Additional placeholder methods for comprehensive functionality
    async def _handle_personalization_feedback(self, data: Dict[str, Any]) -> None:
        """Handle feedback from personalization engine"""
        pass
    
    async def _handle_ab_test_feedback(self, data: Dict[str, Any]) -> None:
        """Handle feedback from A/B testing framework"""
        pass
    
    async def _handle_analytics_feedback(self, data: Dict[str, Any]) -> None:
        """Handle feedback from analytics engine"""
        pass
    
    async def _handle_optimization_feedback(self, data: Dict[str, Any]) -> None:
        """Handle feedback from optimization engine"""
        pass
    
    async def _get_test_metadata(self, test_id: str) -> Dict[str, Any]:
        """Get metadata for A/B test"""
        return {}
    
    async def _check_feedback_loop_health(self) -> None:
        """Check health of feedback loops"""
        pass
    
    async def _analyze_cross_component_correlations(self) -> None:
        """Analyze correlations between components"""
        pass
    
    async def _get_correlation_insights(self) -> List[Dict[str, Any]]:
        """Get correlation insights"""
        return []
    
    async def _get_component_status(self) -> Dict[str, Any]:
        """Get status of all components"""
        return {}
    
    async def shutdown(self):
        """Shutdown the integration controller"""
        logger.info("Shutting down Feedback Integration Controller...")
        
        # Cancel background tasks
        if self.integration_task:
            self.integration_task.cancel()
        
        if self.correlation_task:
            self.correlation_task.cancel()
        
        if self.health_monitor_task:
            self.health_monitor_task.cancel()
        
        logger.info("Feedback Integration Controller shutdown complete")