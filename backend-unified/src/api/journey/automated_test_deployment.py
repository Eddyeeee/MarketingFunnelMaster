# Automated Test Configuration and Deployment - Week 3 Implementation
# Module: 3A - Week 3 - Automated A/B Test Configuration and Deployment System
# Created: 2025-07-05

import asyncio
import json
import logging
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, func, and_, or_

from .models import *
from .database_models import JourneySession, PersonalizationData
from .ab_testing_framework import (
    ABTestingFramework, ABTest, ABTestVariant, TestStatus, TestType, OptimizationGoal
)
from .cross_test_learning_engine import CrossTestLearningEngine
from ...utils.redis_client import get_redis_client
from ...config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# DEPLOYMENT MODELS AND ENUMS
# =============================================================================

class DeploymentStatus(Enum):
    PENDING = "pending"
    CONFIGURING = "configuring"
    VALIDATING = "validating"
    DEPLOYING = "deploying"
    ACTIVE = "active"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class ConfigurationSource(Enum):
    MANUAL = "manual"
    TEMPLATE = "template"
    AI_GENERATED = "ai_generated"
    LEARNING_BASED = "learning_based"

class ValidationLevel(Enum):
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"

@dataclass
class TestTemplate:
    """Test configuration template"""
    template_id: str
    template_name: str
    category: str
    description: str
    base_config: Dict[str, Any]
    variable_parameters: List[str]
    success_criteria: Dict[str, Any]
    estimated_duration_days: int
    confidence_level: float
    usage_count: int = 0
    last_used: datetime = None
    
    def __post_init__(self):
        if self.last_used is None:
            self.last_used = datetime.utcnow()

@dataclass
class DeploymentPlan:
    """Deployment execution plan"""
    plan_id: str
    test_config: Dict[str, Any]
    deployment_steps: List[Dict[str, Any]]
    validation_checks: List[Dict[str, Any]]
    rollback_plan: Dict[str, Any]
    estimated_duration_minutes: int
    risk_assessment: Dict[str, Any]
    dependencies: List[str]
    approval_required: bool

@dataclass
class DeploymentResult:
    """Result of test deployment"""
    deployment_id: str
    test_id: str
    status: DeploymentStatus
    steps_completed: List[str]
    steps_failed: List[str]
    validation_results: Dict[str, Any]
    error_messages: List[str]
    deployment_time_seconds: float
    rollback_triggered: bool
    post_deployment_checks: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

# =============================================================================
# AUTOMATED TEST DEPLOYMENT ENGINE
# =============================================================================

class AutomatedTestDeployment:
    """Automated A/B test configuration and deployment system"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = get_redis_client()
        self.ab_testing_framework = ABTestingFramework(db)
        self.learning_engine = CrossTestLearningEngine(db)
        
        # Deployment configuration
        self.auto_deployment_enabled = True
        self.max_concurrent_deployments = 3
        self.deployment_timeout_minutes = 30
        self.validation_timeout_minutes = 10
        
        # Template and learning configuration
        self.template_cache = {}
        self.learning_cache = {}
        
    async def create_test_from_template(self, template_id: str, 
                                      custom_parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create and deploy test from template"""
        try:
            logger.info(f"Creating test from template: {template_id}")
            
            # Get template configuration
            template = await self._get_test_template(template_id)
            if not template:
                return {'error': f'Template {template_id} not found'}
            
            # Generate test configuration from template
            test_config = await self._generate_config_from_template(template, custom_parameters)
            
            # Apply learning-based optimizations
            optimized_config = await self._apply_learning_optimizations(test_config)
            
            # Validate configuration
            validation_result = await self._validate_test_configuration(optimized_config)
            if not validation_result['valid']:
                return {
                    'error': 'Configuration validation failed',
                    'validation_errors': validation_result['errors']
                }
            
            # Create deployment plan
            deployment_plan = await self._create_deployment_plan(optimized_config)
            
            # Execute deployment if auto-deployment is enabled
            if self.auto_deployment_enabled:
                deployment_result = await self._execute_deployment(deployment_plan)
                
                return {
                    'test_id': deployment_result.test_id,
                    'deployment_id': deployment_result.deployment_id,
                    'status': deployment_result.status.value,
                    'template_used': template_id,
                    'optimizations_applied': optimized_config.get('optimizations_applied', []),
                    'deployment_result': asdict(deployment_result)
                }
            else:
                return {
                    'deployment_plan': asdict(deployment_plan),
                    'template_used': template_id,
                    'requires_approval': True
                }
                
        except Exception as e:
            logger.error(f"Error creating test from template: {str(e)}")
            return {'error': str(e)}
    
    async def auto_generate_test_configuration(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-generate test configuration based on requirements and learnings"""
        try:
            logger.info("Auto-generating test configuration from requirements")
            
            # Extract requirements
            optimization_goal = requirements.get('optimization_goal', 'conversion_rate')
            target_audience = requirements.get('target_audience', [])
            device_targets = requirements.get('device_targets', ['mobile', 'desktop'])
            traffic_percentage = requirements.get('traffic_percentage', 100)
            duration_days = requirements.get('duration_days', 14)
            
            # Get relevant learning patterns
            relevant_learnings = await self.learning_engine.predict_test_performance({
                'optimization_goal': optimization_goal,
                'target_audience': target_audience,
                'device_targets': device_targets
            })
            
            # Generate base configuration
            base_config = await self._generate_base_configuration(requirements)
            
            # Apply learning-based optimizations
            optimized_config = await self._apply_predictive_optimizations(
                base_config, relevant_learnings
            )
            
            # Generate variants based on learnings
            variants = await self._generate_optimal_variants(optimized_config, relevant_learnings)
            
            # Calculate traffic allocation
            traffic_allocation = await self._calculate_optimal_traffic_allocation(variants, relevant_learnings)
            
            # Create complete test configuration
            test_config = {
                'test_name': f"Auto-generated test - {datetime.utcnow().strftime('%Y%m%d_%H%M')}",
                'test_type': 'hybrid_optimization',
                'optimization_goal': optimization_goal,
                'variants': variants,
                'traffic_allocation': traffic_allocation,
                'target_sample_size': await self._calculate_optimal_sample_size(optimized_config),
                'start_date': datetime.utcnow().isoformat(),
                'end_date': (datetime.utcnow() + timedelta(days=duration_days)).isoformat(),
                'device_targets': device_targets,
                'persona_targets': target_audience,
                'auto_generated': True,
                'generation_source': 'ai_learning_system',
                'learning_confidence': relevant_learnings.confidence,
                'predicted_winner': relevant_learnings.predicted_winner,
                'estimated_performance': relevant_learnings.predicted_performance
            }
            
            return {
                'test_configuration': test_config,
                'generation_confidence': relevant_learnings.confidence,
                'supporting_patterns': relevant_learnings.supporting_patterns,
                'risk_factors': relevant_learnings.risk_factors,
                'optimization_suggestions': relevant_learnings.optimization_suggestions,
                'estimated_duration': relevant_learnings.expected_duration
            }
            
        except Exception as e:
            logger.error(f"Error auto-generating test configuration: {str(e)}")
            return {'error': str(e)}
    
    async def deploy_test_configuration(self, test_config: Dict[str, Any], 
                                      deployment_options: Dict[str, Any] = None) -> DeploymentResult:
        """Deploy test configuration with full automation"""
        try:
            logger.info(f"Deploying test configuration: {test_config.get('test_name', 'unnamed')}")
            
            deployment_id = f"deploy_{uuid.uuid4().hex[:8]}_{int(datetime.utcnow().timestamp())}"
            
            # Create deployment plan
            deployment_plan = await self._create_deployment_plan(test_config, deployment_options)
            
            # Execute deployment
            deployment_result = await self._execute_deployment(deployment_plan)
            
            # Post-deployment validation
            if deployment_result.status == DeploymentStatus.ACTIVE:
                post_deployment_checks = await self._run_post_deployment_checks(deployment_result.test_id)
                deployment_result.post_deployment_checks = post_deployment_checks
                
                if not post_deployment_checks.get('all_passed', False):
                    logger.warning(f"Post-deployment checks failed for test {deployment_result.test_id}")
                    
                    # Consider rollback if critical checks failed
                    if post_deployment_checks.get('critical_failures', False):
                        await self._trigger_rollback(deployment_result.test_id, "Critical post-deployment check failures")
                        deployment_result.rollback_triggered = True
                        deployment_result.status = DeploymentStatus.ROLLED_BACK
            
            # Record deployment
            await self._record_deployment_result(deployment_result)
            
            # Update template usage if applicable
            if test_config.get('template_id'):
                await self._update_template_usage(test_config['template_id'])
            
            return deployment_result
            
        except Exception as e:
            logger.error(f"Error deploying test configuration: {str(e)}")
            return DeploymentResult(
                deployment_id=deployment_id if 'deployment_id' in locals() else 'error',
                test_id='',
                status=DeploymentStatus.FAILED,
                steps_completed=[],
                steps_failed=['deployment_initiation'],
                validation_results={},
                error_messages=[str(e)],
                deployment_time_seconds=0.0,
                rollback_triggered=False,
                post_deployment_checks={}
            )
    
    async def create_test_template(self, template_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create reusable test template"""
        try:
            logger.info(f"Creating test template: {template_config.get('template_name', 'unnamed')}")
            
            template_id = f"template_{uuid.uuid4().hex[:8]}"
            
            # Validate template configuration
            validation_result = await self._validate_template_configuration(template_config)
            if not validation_result['valid']:
                return {
                    'error': 'Template validation failed',
                    'validation_errors': validation_result['errors']
                }
            
            # Create template object
            template = TestTemplate(
                template_id=template_id,
                template_name=template_config['template_name'],
                category=template_config.get('category', 'general'),
                description=template_config.get('description', ''),
                base_config=template_config['base_config'],
                variable_parameters=template_config.get('variable_parameters', []),
                success_criteria=template_config.get('success_criteria', {}),
                estimated_duration_days=template_config.get('estimated_duration_days', 14),
                confidence_level=template_config.get('confidence_level', 0.8)
            )
            
            # Store template
            await self._store_test_template(template)
            
            # Generate template validation tests
            validation_tests = await self._generate_template_validation_tests(template)
            
            return {
                'template_id': template_id,
                'template': asdict(template),
                'validation_tests': validation_tests,
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Error creating test template: {str(e)}")
            return {'error': str(e)}

    # =============================================================================
    # DEPLOYMENT EXECUTION METHODS
    # =============================================================================

    async def _execute_deployment(self, deployment_plan: DeploymentPlan) -> DeploymentResult:
        """Execute deployment plan"""
        start_time = datetime.utcnow()
        deployment_id = deployment_plan.plan_id
        
        steps_completed = []
        steps_failed = []
        error_messages = []
        validation_results = {}
        
        try:
            logger.info(f"Executing deployment plan: {deployment_id}")
            
            # Step 1: Pre-deployment validation
            logger.info("Step 1: Pre-deployment validation")
            pre_validation = await self._run_pre_deployment_validation(deployment_plan)
            validation_results['pre_deployment'] = pre_validation
            
            if not pre_validation.get('passed', False):
                steps_failed.append('pre_deployment_validation')
                error_messages.extend(pre_validation.get('errors', []))
                return self._create_failed_deployment_result(
                    deployment_id, '', steps_completed, steps_failed, 
                    validation_results, error_messages, start_time
                )
            
            steps_completed.append('pre_deployment_validation')
            
            # Step 2: Create test in framework
            logger.info("Step 2: Creating test in framework")
            test_creation_result = await self.ab_testing_framework.create_ab_test(deployment_plan.test_config)
            
            if not hasattr(test_creation_result, 'test_id'):
                steps_failed.append('test_creation')
                error_messages.append('Failed to create test in framework')
                return self._create_failed_deployment_result(
                    deployment_id, '', steps_completed, steps_failed,
                    validation_results, error_messages, start_time
                )
            
            test_id = test_creation_result.test_id
            steps_completed.append('test_creation')
            
            # Step 3: Configure traffic routing
            logger.info("Step 3: Configuring traffic routing")
            routing_result = await self._configure_traffic_routing(test_id, deployment_plan.test_config)
            validation_results['traffic_routing'] = routing_result
            
            if not routing_result.get('success', False):
                steps_failed.append('traffic_routing')
                error_messages.extend(routing_result.get('errors', []))
                await self._cleanup_failed_deployment(test_id)
                return self._create_failed_deployment_result(
                    deployment_id, test_id, steps_completed, steps_failed,
                    validation_results, error_messages, start_time
                )
            
            steps_completed.append('traffic_routing')
            
            # Step 4: Initialize monitoring
            logger.info("Step 4: Initializing monitoring")
            monitoring_result = await self._initialize_test_monitoring(test_id, deployment_plan.test_config)
            validation_results['monitoring'] = monitoring_result
            
            if not monitoring_result.get('success', False):
                steps_failed.append('monitoring_initialization')
                error_messages.extend(monitoring_result.get('errors', []))
                # Continue anyway as monitoring is not critical for test function
            else:
                steps_completed.append('monitoring_initialization')
            
            # Step 5: Activate test
            logger.info("Step 5: Activating test")
            activation_result = await self._activate_test(test_id)
            validation_results['test_activation'] = activation_result
            
            if not activation_result.get('success', False):
                steps_failed.append('test_activation')
                error_messages.extend(activation_result.get('errors', []))
                await self._cleanup_failed_deployment(test_id)
                return self._create_failed_deployment_result(
                    deployment_id, test_id, steps_completed, steps_failed,
                    validation_results, error_messages, start_time
                )
            
            steps_completed.append('test_activation')
            
            # Step 6: Final validation
            logger.info("Step 6: Final validation")
            final_validation = await self._run_final_deployment_validation(test_id)
            validation_results['final_validation'] = final_validation
            
            if not final_validation.get('passed', False):
                steps_failed.append('final_validation')
                error_messages.extend(final_validation.get('errors', []))
                # Don't fail deployment for final validation issues, but log them
                logger.warning(f"Final validation issues for test {test_id}: {final_validation.get('errors', [])}")
            else:
                steps_completed.append('final_validation')
            
            # Calculate deployment time
            end_time = datetime.utcnow()
            deployment_time = (end_time - start_time).total_seconds()
            
            logger.info(f"Deployment completed successfully: {test_id}")
            
            return DeploymentResult(
                deployment_id=deployment_id,
                test_id=test_id,
                status=DeploymentStatus.ACTIVE,
                steps_completed=steps_completed,
                steps_failed=steps_failed,
                validation_results=validation_results,
                error_messages=error_messages,
                deployment_time_seconds=deployment_time,
                rollback_triggered=False,
                post_deployment_checks={}
            )
            
        except Exception as e:
            logger.error(f"Error executing deployment: {str(e)}")
            error_messages.append(str(e))
            
            return self._create_failed_deployment_result(
                deployment_id, '', steps_completed, steps_failed,
                validation_results, error_messages, start_time
            )

    async def _create_deployment_plan(self, test_config: Dict[str, Any], 
                                    options: Dict[str, Any] = None) -> DeploymentPlan:
        """Create detailed deployment plan"""
        plan_id = f"plan_{uuid.uuid4().hex[:8]}"
        
        # Define deployment steps
        deployment_steps = [
            {
                'step': 'pre_deployment_validation',
                'description': 'Validate test configuration and prerequisites',
                'estimated_duration_seconds': 30,
                'critical': True
            },
            {
                'step': 'test_creation',
                'description': 'Create test in A/B testing framework',
                'estimated_duration_seconds': 60,
                'critical': True
            },
            {
                'step': 'traffic_routing',
                'description': 'Configure traffic routing and allocation',
                'estimated_duration_seconds': 120,
                'critical': True
            },
            {
                'step': 'monitoring_initialization',
                'description': 'Initialize performance monitoring',
                'estimated_duration_seconds': 45,
                'critical': False
            },
            {
                'step': 'test_activation',
                'description': 'Activate test and start traffic routing',
                'estimated_duration_seconds': 30,
                'critical': True
            },
            {
                'step': 'final_validation',
                'description': 'Validate test is running correctly',
                'estimated_duration_seconds': 60,
                'critical': False
            }
        ]
        
        # Define validation checks
        validation_checks = [
            {
                'check': 'configuration_syntax',
                'description': 'Validate configuration syntax and structure',
                'timeout_seconds': 10
            },
            {
                'check': 'traffic_allocation',
                'description': 'Validate traffic allocation sums to 100%',
                'timeout_seconds': 5
            },
            {
                'check': 'variant_configurations',
                'description': 'Validate all variant configurations',
                'timeout_seconds': 30
            },
            {
                'check': 'sample_size_feasibility',
                'description': 'Validate sample size is achievable',
                'timeout_seconds': 15
            }
        ]
        
        # Create rollback plan
        rollback_plan = {
            'steps': [
                'Deactivate test traffic routing',
                'Clean up test configuration',
                'Restore previous traffic routing',
                'Notify monitoring systems'
            ],
            'estimated_duration_seconds': 300,
            'automatic_triggers': [
                'Critical validation failure',
                'Traffic routing errors',
                'System health degradation'
            ]
        }
        
        # Assess deployment risk
        risk_assessment = await self._assess_deployment_risk(test_config)
        
        # Calculate estimated duration
        estimated_duration = sum(step['estimated_duration_seconds'] for step in deployment_steps)
        
        return DeploymentPlan(
            plan_id=plan_id,
            test_config=test_config,
            deployment_steps=deployment_steps,
            validation_checks=validation_checks,
            rollback_plan=rollback_plan,
            estimated_duration_minutes=estimated_duration // 60,
            risk_assessment=risk_assessment,
            dependencies=[],
            approval_required=risk_assessment.get('high_risk', False)
        )

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    def _create_failed_deployment_result(self, deployment_id: str, test_id: str,
                                       steps_completed: List[str], steps_failed: List[str],
                                       validation_results: Dict[str, Any], error_messages: List[str],
                                       start_time: datetime) -> DeploymentResult:
        """Create failed deployment result"""
        end_time = datetime.utcnow()
        deployment_time = (end_time - start_time).total_seconds()
        
        return DeploymentResult(
            deployment_id=deployment_id,
            test_id=test_id,
            status=DeploymentStatus.FAILED,
            steps_completed=steps_completed,
            steps_failed=steps_failed,
            validation_results=validation_results,
            error_messages=error_messages,
            deployment_time_seconds=deployment_time,
            rollback_triggered=False,
            post_deployment_checks={}
        )

    async def _assess_deployment_risk(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Assess deployment risk level"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check traffic percentage
            traffic_percentage = test_config.get('traffic_percentage', 100)
            if traffic_percentage > 50:
                risk_factors.append(f"High traffic allocation: {traffic_percentage}%")
                risk_score += 0.3
            
            # Check number of variants
            variant_count = len(test_config.get('variants', []))
            if variant_count > 3:
                risk_factors.append(f"High number of variants: {variant_count}")
                risk_score += 0.2
            
            # Check if it's an auto-generated test
            if test_config.get('auto_generated', False):
                risk_factors.append("Auto-generated configuration")
                risk_score += 0.1
            
            # Check optimization goal complexity
            optimization_goal = test_config.get('optimization_goal', 'conversion_rate')
            if optimization_goal in ['revenue_per_visitor', 'hybrid_optimization']:
                risk_factors.append("Complex optimization goal")
                risk_score += 0.2
            
            return {
                'risk_score': min(1.0, risk_score),
                'risk_level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low',
                'risk_factors': risk_factors,
                'high_risk': risk_score > 0.6,
                'requires_approval': risk_score > 0.6
            }
            
        except Exception as e:
            logger.error(f"Error assessing deployment risk: {str(e)}")
            return {
                'risk_score': 1.0,
                'risk_level': 'high',
                'risk_factors': ['Risk assessment failed'],
                'high_risk': True,
                'requires_approval': True
            }

# =============================================================================
# EXPORT FOR INTEGRATION
# =============================================================================

__all__ = [
    'AutomatedTestDeployment',
    'TestTemplate',
    'DeploymentPlan',
    'DeploymentResult',
    'DeploymentStatus',
    'ConfigurationSource',
    'ValidationLevel'
]