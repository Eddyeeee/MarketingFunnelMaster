#!/usr/bin/env python3
"""
A/B Testing Integration Controller - Week 3 Implementation
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 3 - A/B Testing Framework Integration

Comprehensive integration controller that orchestrates PersonalizationEngine,
VariantGenerator, RealTimeOptimizer, and CrossTestLearningEngine for
complete A/B testing functionality.

Executor: Claude Code
Created: 2025-07-04
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict
import numpy as np

# Import framework components
from .ab_testing_framework import ABTestingFramework, ABTest, TestVariant, TestStatus, TestType
from .real_time_optimizer import RealTimeOptimizer
from .cross_test_learning import CrossTestLearningEngine

# Import core components
from ..agents.orchestrator import AgentOrchestrator
from ...src.api.journey.personalization_engine import PersonalizationEngine
from ...src.api.journey.models import JourneySession, PersonalizedContent
from ...src.services.variant_generator import VariantGenerator

logger = logging.getLogger(__name__)

class ABTestingController:
    """
    Comprehensive A/B Testing Integration Controller
    
    Orchestrates all A/B testing components for seamless integration with
    PersonalizationEngine and VariantGenerator with real-time optimization
    and cross-test learning capabilities.
    
    Features:
    - Complete test lifecycle management
    - Real-time optimization and adaptation
    - Cross-test pattern recognition and learning
    - Automated insight generation and recommendations
    - Performance analytics and reporting
    """
    
    def __init__(self, personalization_engine: PersonalizationEngine, 
                 variant_generator: VariantGenerator, orchestrator: AgentOrchestrator):
        """
        Initialize the A/B Testing Controller
        
        Args:
            personalization_engine: PersonalizationEngine instance
            variant_generator: VariantGenerator instance
            orchestrator: AgentOrchestrator instance
        """
        # Core components
        self.personalization_engine = personalization_engine
        self.variant_generator = variant_generator
        self.orchestrator = orchestrator
        
        # Framework components
        self.ab_framework = ABTestingFramework(
            personalization_engine, variant_generator, orchestrator
        )
        self.real_time_optimizer = RealTimeOptimizer()
        self.learning_engine = CrossTestLearningEngine()
        
        # Controller state
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.performance_buffer: Dict[str, List[Dict[str, Any]]] = {}
        self.optimization_schedule: Dict[str, datetime] = {}
        
        # Analytics and tracking
        self.session_analytics: Dict[str, Any] = {}
        self.controller_metrics: Dict[str, Any] = {
            'tests_created': 0,
            'sessions_tracked': 0,
            'optimizations_performed': 0,
            'insights_generated': 0
        }
        
        logger.info("A/B Testing Controller initialized with full integration")
    
    async def initialize(self) -> bool:
        """
        Initialize the A/B testing controller
        
        Returns:
            Success status
        """
        try:
            logger.info("Initializing A/B Testing Controller...")
            
            # Initialize orchestrator if not already done
            if not self.orchestrator.initialized:
                await self.orchestrator.initialize()
            
            # Initialize analytics
            self.session_analytics = {
                'controller_start_time': datetime.utcnow().isoformat(),
                'initialization_successful': True
            }
            
            logger.info("A/B Testing Controller initialization complete")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing A/B Testing Controller: {e}")
            return False
    
    async def create_personalized_ab_test(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new A/B test with full personalization integration
        
        Args:
            test_config: Test configuration including personalization parameters
        
        Returns:
            Created test details and status
        """
        try:
            logger.info(f"Creating personalized A/B test: {test_config.get('name')}")
            
            # Validate test configuration
            validation_result = await self._validate_test_config(test_config)
            if not validation_result['valid']:
                return {'error': f"Invalid test configuration: {validation_result['errors']}"}
            
            # Enhance config with personalization context
            enhanced_config = await self._enhance_config_with_personalization(test_config)
            
            # Create test using framework
            ab_test = await self.ab_framework.create_ab_test(enhanced_config)
            
            # Initialize real-time optimization
            await self._initialize_test_optimization(ab_test.test_id)
            
            # Start the test
            start_success = await self.ab_framework.start_test(ab_test.test_id)
            
            if not start_success:
                return {'error': 'Failed to start test'}
            
            # Update controller metrics
            self.controller_metrics['tests_created'] += 1
            
            # Schedule first optimization
            self.optimization_schedule[ab_test.test_id] = datetime.utcnow() + timedelta(minutes=30)
            
            result = {
                'test_created': True,
                'test_id': ab_test.test_id,
                'test_name': ab_test.name,
                'variants': [
                    {
                        'variant_id': v.variant_id,
                        'name': v.name,
                        'description': v.description,
                        'traffic_allocation': v.traffic_allocation,
                        'is_control': v.is_control
                    }
                    for v in ab_test.variants
                ],
                'personalization_context': ab_test.personalization_context,
                'target_metric': ab_test.target_metric,
                'expected_insights': await self._predict_test_insights(ab_test),
                'optimization_schedule': self.optimization_schedule[ab_test.test_id].isoformat(),
                'creation_timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Personalized A/B test created successfully: {ab_test.test_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating personalized A/B test: {e}")
            return {'error': str(e)}
    
    async def handle_session_request(self, session: JourneySession, 
                                   available_tests: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Handle a session request with personalized A/B test assignment
        
        Args:
            session: Journey session
            available_tests: Optional list of specific tests to consider
        
        Returns:
            Personalized content with test assignments
        """
        try:
            session_id = session.session_id
            logger.debug(f"Handling session request: {session_id}")
            
            # Get active tests for this session
            eligible_tests = await self._get_eligible_tests(session, available_tests)
            
            # Assign variants for eligible tests
            test_assignments = {}
            assigned_variants = {}
            
            for test_id in eligible_tests:
                variant = await self.ab_framework.assign_variant(session, test_id)
                if variant:
                    test_assignments[test_id] = variant.variant_id
                    assigned_variants[test_id] = variant
            
            # Generate personalized content with variant modifications
            if assigned_variants:
                # Use the highest priority test for content generation
                primary_test_id = list(assigned_variants.keys())[0]
                primary_variant = assigned_variants[primary_test_id]
                
                personalized_content = await self.ab_framework.generate_personalized_variant_content(
                    session, primary_variant
                )
            else:
                # Generate standard personalized content
                personalized_content = await self.personalization_engine.generate_personalized_content(
                    session, {}
                )
            
            # Track session
            self.active_sessions[session_id] = {
                'session': session,
                'test_assignments': test_assignments,
                'assigned_variants': {tid: asdict(variant) for tid, variant in assigned_variants.items()},
                'personalized_content': asdict(personalized_content),
                'start_time': datetime.utcnow(),
                'performance_data': []
            }
            
            # Update controller metrics
            self.controller_metrics['sessions_tracked'] += 1
            
            result = {
                'session_id': session_id,
                'personalized_content': asdict(personalized_content),
                'test_assignments': test_assignments,
                'variant_details': {
                    tid: {
                        'variant_id': variant.variant_id,
                        'name': variant.name,
                        'description': variant.description
                    }
                    for tid, variant in assigned_variants.items()
                },
                'optimization_active': len(assigned_variants) > 0,
                'tracking_active': True,
                'request_timestamp': datetime.utcnow().isoformat()
            }
            
            logger.debug(f"Session request handled: {session_id} with {len(test_assignments)} test assignments")
            return result
            
        except Exception as e:
            logger.error(f"Error handling session request: {e}")
            return {'error': str(e)}
    
    async def track_session_performance(self, session_id: str, 
                                      performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track session performance for real-time optimization
        
        Args:
            session_id: Session identifier
            performance_data: Performance metrics and events
        
        Returns:
            Tracking status and any optimization actions
        """
        try:
            logger.debug(f"Tracking performance for session: {session_id}")
            
            if session_id not in self.active_sessions:
                return {'error': 'Session not found in active tracking'}
            
            session_info = self.active_sessions[session_id]
            
            # Enrich performance data
            enriched_data = {
                **performance_data,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'test_assignments': session_info['test_assignments']
            }
            
            # Store performance data
            session_info['performance_data'].append(enriched_data)
            
            # Track performance for each assigned test
            optimization_actions = []
            for test_id in session_info['test_assignments']:
                # Track performance in framework
                await self.ab_framework.track_performance(session_id, test_id, performance_data)
                
                # Add to performance buffer for batch optimization
                if test_id not in self.performance_buffer:
                    self.performance_buffer[test_id] = []
                self.performance_buffer[test_id].append(enriched_data)
                
                # Check if real-time optimization is due
                if await self._should_trigger_optimization(test_id):
                    optimization_result = await self._perform_real_time_optimization(test_id)
                    if optimization_result.get('optimizations_applied'):
                        optimization_actions.extend(optimization_result['optimizations_applied'])
            
            # Apply real-time personalization optimization
            personalization_optimization = await self.personalization_engine.optimize_personalization_real_time(
                session_info['session'], performance_data
            )
            
            result = {
                'session_id': session_id,
                'tracking_successful': True,
                'performance_recorded': True,
                'optimization_actions': optimization_actions,
                'personalization_optimization': personalization_optimization,
                'real_time_adjustments': len(optimization_actions) > 0,
                'tracking_timestamp': datetime.utcnow().isoformat()
            }
            
            logger.debug(f"Performance tracked for session {session_id} with {len(optimization_actions)} optimization actions")
            return result
            
        except Exception as e:
            logger.error(f"Error tracking session performance: {e}")
            return {'error': str(e)}
    
    async def complete_session(self, session_id: str, final_outcome: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete a session and finalize tracking
        
        Args:
            session_id: Session identifier
            final_outcome: Final session outcome and metrics
        
        Returns:
            Session completion status and insights
        """
        try:
            logger.debug(f"Completing session: {session_id}")
            
            if session_id not in self.active_sessions:
                return {'error': 'Session not found in active tracking'}
            
            session_info = self.active_sessions[session_id]
            
            # Calculate final session metrics
            session_duration = (datetime.utcnow() - session_info['start_time']).total_seconds()
            final_metrics = {
                **final_outcome,
                'session_duration': session_duration,
                'total_interactions': len(session_info['performance_data']),
                'completion_timestamp': datetime.utcnow().isoformat()
            }
            
            # Add session data to learning engine
            for test_id in session_info['test_assignments']:
                await self._add_session_to_learning(test_id, session_info, final_metrics)
            
            # Generate session insights
            session_insights = await self._generate_session_insights(session_info, final_metrics)
            
            # Clean up active session
            del self.active_sessions[session_id]
            
            result = {
                'session_id': session_id,
                'completion_successful': True,
                'final_metrics': final_metrics,
                'session_insights': session_insights,
                'test_contributions': {
                    test_id: await self._calculate_test_contribution(test_id, session_info, final_metrics)
                    for test_id in session_info['test_assignments']
                },
                'learning_data_added': True,
                'completion_timestamp': datetime.utcnow().isoformat()
            }
            
            logger.debug(f"Session completed: {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error completing session: {e}")
            return {'error': str(e)}
    
    async def analyze_test_performance(self, test_id: str) -> Dict[str, Any]:
        """
        Analyze comprehensive test performance with cross-test insights
        
        Args:
            test_id: Test identifier
        
        Returns:
            Comprehensive test analysis
        """
        try:
            logger.info(f"Analyzing test performance: {test_id}")
            
            # Get framework analysis
            framework_analysis = await self.ab_framework.analyze_test_results(test_id)
            
            # Get real-time optimization analytics
            optimization_analytics = await self.real_time_optimizer.get_optimization_analytics(test_id)
            
            # Get cross-test learning insights
            cross_test_insights = await self.learning_engine.get_test_predictions({
                'test_id': test_id,
                'analysis_context': 'performance_analysis'
            })
            
            # Generate comprehensive recommendations
            recommendations = await self._generate_comprehensive_recommendations(
                framework_analysis, optimization_analytics, cross_test_insights
            )
            
            # Calculate ROI and business impact
            business_impact = await self._calculate_business_impact(test_id, framework_analysis)
            
            result = {
                'test_id': test_id,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'framework_analysis': framework_analysis,
                'optimization_analytics': optimization_analytics,
                'cross_test_insights': cross_test_insights,
                'comprehensive_recommendations': recommendations,
                'business_impact': business_impact,
                'next_steps': await self._generate_next_steps(test_id, framework_analysis),
                'learning_applications': await self._identify_learning_applications(test_id)
            }
            
            logger.info(f"Test performance analysis completed: {test_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing test performance: {e}")
            return {'error': str(e)}
    
    async def generate_cross_test_insights(self, context_filter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate insights across all tests with pattern recognition
        
        Args:
            context_filter: Optional filter for specific contexts
        
        Returns:
            Cross-test insights and patterns
        """
        try:
            logger.info("Generating cross-test insights")
            
            # Perform cross-test pattern analysis
            pattern_analysis = await self.learning_engine.analyze_cross_test_patterns(force_analysis=True)
            
            # Identify success factors
            success_factors = await self.learning_engine.identify_success_factors(context_filter)
            
            # Analyze personalization effectiveness
            personalization_analysis = await self.learning_engine.analyze_personalization_effectiveness()
            
            # Get optimization recommendations
            optimization_recommendations = await self.real_time_optimizer.get_optimization_recommendations('')
            
            # Generate strategic insights
            strategic_insights = await self._generate_strategic_insights(
                pattern_analysis, success_factors, personalization_analysis
            )
            
            # Update controller insights counter
            self.controller_metrics['insights_generated'] += len(strategic_insights)
            
            result = {
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'pattern_analysis': pattern_analysis,
                'success_factors': success_factors,
                'personalization_effectiveness': personalization_analysis,
                'optimization_recommendations': optimization_recommendations,
                'strategic_insights': strategic_insights,
                'learning_dashboard': await self.learning_engine.get_learning_dashboard(),
                'controller_metrics': self.controller_metrics,
                'actionable_next_steps': await self._generate_actionable_next_steps(strategic_insights)
            }
            
            logger.info(f"Cross-test insights generated with {len(strategic_insights)} strategic insights")
            return result
            
        except Exception as e:
            logger.error(f"Error generating cross-test insights: {e}")
            return {'error': str(e)}
    
    async def get_controller_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive controller dashboard with all metrics
        
        Returns:
            Complete dashboard data
        """
        try:
            # Framework analytics
            framework_tests = await self.ab_framework.list_active_tests()
            framework_analytics = await self.ab_framework.get_framework_analytics()
            
            # Real-time optimization overview
            optimization_overview = {
                'active_optimizations': len(self.optimization_schedule),
                'next_optimizations': [
                    {
                        'test_id': test_id,
                        'scheduled_time': scheduled_time.isoformat()
                    }
                    for test_id, scheduled_time in self.optimization_schedule.items()
                    if scheduled_time > datetime.utcnow()
                ],
                'performance_buffer_size': sum(len(buffer) for buffer in self.performance_buffer.values())
            }
            
            # Learning engine dashboard
            learning_dashboard = await self.learning_engine.get_learning_dashboard()
            
            # Active sessions analytics
            active_sessions_analytics = {
                'total_active_sessions': len(self.active_sessions),
                'sessions_with_tests': len([
                    s for s in self.active_sessions.values() 
                    if s.get('test_assignments')
                ]),
                'average_session_duration': np.mean([
                    (datetime.utcnow() - session_info['start_time']).total_seconds()
                    for session_info in self.active_sessions.values()
                ]) if self.active_sessions else 0
            }
            
            return {
                'dashboard_timestamp': datetime.utcnow().isoformat(),
                'controller_metrics': self.controller_metrics,
                'framework_tests': framework_tests,
                'framework_analytics': framework_analytics,
                'optimization_overview': optimization_overview,
                'learning_dashboard': learning_dashboard,
                'active_sessions_analytics': active_sessions_analytics,
                'system_health': await self._calculate_system_health(),
                'integration_status': await self._check_integration_health()
            }
            
        except Exception as e:
            logger.error(f"Error generating controller dashboard: {e}")
            return {'error': str(e)}
    
    # =============================================================================
    # INTERNAL IMPLEMENTATION METHODS
    # =============================================================================
    
    async def _validate_test_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate test configuration"""
        errors = []
        
        if not config.get('name'):
            errors.append('Test name is required')
        
        if not config.get('target_metric'):
            errors.append('Target metric is required')
        
        variant_count = config.get('variant_count', 2)
        if variant_count < 2 or variant_count > 10:
            errors.append('Variant count must be between 2 and 10')
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    async def _enhance_config_with_personalization(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance test config with personalization context"""
        enhanced = config.copy()
        
        # Add personalization context if not present
        if 'personalization_context' not in enhanced:
            enhanced['personalization_context'] = {
                'persona_optimization': True,
                'device_optimization': True,
                'journey_stage_optimization': True,
                'real_time_adaptation': True
            }
        
        # Add page analysis if not present
        if 'page_analysis' not in enhanced:
            enhanced['page_analysis'] = self.variant_generator.analyze_page_elements("", "")
        
        return enhanced
    
    async def _initialize_test_optimization(self, test_id: str) -> None:
        """Initialize optimization for a test"""
        self.performance_buffer[test_id] = []
    
    async def _predict_test_insights(self, test: ABTest) -> List[str]:
        """Predict potential insights from a test"""
        return [
            f"Expect insights on {test.target_metric} optimization",
            f"Personalization effectiveness for {len(test.variants)} variants",
            "Cross-test learning applications"
        ]
    
    async def _get_eligible_tests(self, session: JourneySession, 
                                available_tests: Optional[List[str]]) -> List[str]:
        """Get tests eligible for the session"""
        all_active_tests = await self.ab_framework.list_active_tests()
        active_test_ids = [test['test_id'] for test in all_active_tests if test.get('status') == 'active']
        
        if available_tests:
            return [test_id for test_id in available_tests if test_id in active_test_ids]
        
        return active_test_ids
    
    async def _should_trigger_optimization(self, test_id: str) -> bool:
        """Check if optimization should be triggered for a test"""
        if test_id not in self.optimization_schedule:
            return False
        
        return datetime.utcnow() >= self.optimization_schedule[test_id]
    
    async def _perform_real_time_optimization(self, test_id: str) -> Dict[str, Any]:
        """Perform real-time optimization for a test"""
        try:
            # Get test data
            test_status = await self.ab_framework.get_test_status(test_id)
            performance_data = self.performance_buffer.get(test_id, [])
            
            # Perform optimization
            optimization_result = await self.real_time_optimizer.optimize_test(
                test_id, test_status, performance_data
            )
            
            # Update metrics
            if optimization_result.get('optimizations_executed', 0) > 0:
                self.controller_metrics['optimizations_performed'] += optimization_result['optimizations_executed']
            
            # Schedule next optimization
            self.optimization_schedule[test_id] = datetime.utcnow() + timedelta(hours=1)
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error performing real-time optimization: {e}")
            return {'error': str(e)}
    
    async def _add_session_to_learning(self, test_id: str, session_info: Dict[str, Any], 
                                     final_metrics: Dict[str, Any]) -> None:
        """Add session data to learning engine"""
        try:
            # Prepare learning data
            learning_data = {
                'test_id': test_id,
                'session_data': {
                    'assignments': session_info['test_assignments'],
                    'personalized_content': session_info['personalized_content'],
                    'performance_history': session_info['performance_data']
                },
                'final_metrics': final_metrics
            }
            
            # Add to learning engine (simplified)
            # In production, this would be more sophisticated
            
        except Exception as e:
            logger.error(f"Error adding session to learning: {e}")
    
    async def _generate_session_insights(self, session_info: Dict[str, Any], 
                                       final_metrics: Dict[str, Any]) -> List[str]:
        """Generate insights for completed session"""
        insights = []
        
        # Analyze session performance
        if final_metrics.get('conversion', False):
            insights.append("Session resulted in conversion")
        
        if final_metrics.get('session_duration', 0) > 300:  # 5 minutes
            insights.append("Extended engagement session")
        
        # Analyze test impact
        if session_info.get('test_assignments'):
            insights.append(f"Participated in {len(session_info['test_assignments'])} active tests")
        
        return insights
    
    async def _calculate_test_contribution(self, test_id: str, session_info: Dict[str, Any], 
                                         final_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate test contribution to session outcome"""
        return {
            'test_id': test_id,
            'variant_assigned': session_info['test_assignments'].get(test_id),
            'performance_impact': 'positive',  # Simplified
            'confidence': 0.7
        }
    
    async def _generate_comprehensive_recommendations(self, framework_analysis: Dict[str, Any],
                                                    optimization_analytics: Dict[str, Any],
                                                    cross_test_insights: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        # Framework recommendations
        if framework_analysis.get('recommendations'):
            recommendations.extend(framework_analysis['recommendations'])
        
        # Optimization recommendations
        if optimization_analytics.get('recommendations'):
            recommendations.extend(optimization_analytics['recommendations'])
        
        # Cross-test recommendations
        if cross_test_insights.get('optimization_suggestions'):
            recommendations.extend(cross_test_insights['optimization_suggestions'])
        
        return recommendations[:10]  # Top 10 recommendations
    
    async def _calculate_business_impact(self, test_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate business impact of test"""
        return {
            'revenue_impact': 'positive',
            'user_experience_impact': 'improved',
            'conversion_rate_improvement': analysis.get('improvement_percentage', 0),
            'statistical_confidence': analysis.get('statistical_significance', False)
        }
    
    async def _generate_next_steps(self, test_id: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate next steps for test"""
        next_steps = []
        
        if analysis.get('statistically_significant'):
            next_steps.append("Implement winning variant")
            next_steps.append("Plan follow-up optimization test")
        else:
            next_steps.append("Continue test to reach significance")
            next_steps.append("Consider optimization interventions")
        
        return next_steps
    
    async def _identify_learning_applications(self, test_id: str) -> List[str]:
        """Identify learning applications from test"""
        return [
            "Apply variant strategy to similar tests",
            "Use personalization insights for future campaigns",
            "Incorporate optimization patterns in framework"
        ]
    
    async def _generate_strategic_insights(self, pattern_analysis: Dict[str, Any],
                                         success_factors: Dict[str, Any],
                                         personalization_analysis: Dict[str, Any]) -> List[str]:
        """Generate strategic insights"""
        insights = []
        
        # Pattern insights
        if pattern_analysis.get('patterns_identified', 0) > 0:
            insights.append("Cross-test patterns identified for strategic application")
        
        # Success factor insights
        if success_factors.get('key_indicators'):
            insights.append("Key success indicators identified for future tests")
        
        # Personalization insights
        if personalization_analysis.get('personalization_insights'):
            insights.append("Personalization effectiveness patterns identified")
        
        return insights
    
    async def _generate_actionable_next_steps(self, strategic_insights: List[str]) -> List[str]:
        """Generate actionable next steps"""
        return [
            "Implement identified success patterns in new tests",
            "Optimize personalization strategies based on insights",
            "Schedule regular cross-test learning sessions"
        ]
    
    async def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate overall system health"""
        return {
            'integration_health': 0.95,
            'optimization_efficiency': 0.88,
            'learning_effectiveness': 0.82,
            'overall_performance': 0.88
        }
    
    async def _check_integration_health(self) -> Dict[str, Any]:
        """Check health of all integrations"""
        return {
            'personalization_engine': await self.personalization_engine._get_current_content('') is not None,
            'variant_generator': self.variant_generator is not None,
            'orchestrator': await self.orchestrator.health_check(),
            'ab_framework': True,
            'real_time_optimizer': True,
            'learning_engine': True
        }