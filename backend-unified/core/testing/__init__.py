"""
A/B Testing Framework Integration Package - Week 3 Implementation
Module 3A: AI Content Generation Pipeline Integration
Milestone: Week 3 - A/B Testing Framework Integration

Complete A/B testing framework with PersonalizationEngine integration,
real-time optimization, and cross-test learning capabilities.

Components:
- ABTestingFramework: Core A/B testing functionality
- RealTimeOptimizer: Real-time test optimization engine  
- CrossTestLearningEngine: Cross-test pattern analysis and learning

Executor: Claude Code
Created: 2025-07-04
"""

from .ab_testing_framework import (
    ABTestingFramework,
    ABTest,
    TestVariant,
    TestMetrics,
    TestStatus,
    TestType,
    StatisticalSignificance
)

from .real_time_optimizer import (
    RealTimeOptimizer,
    OptimizationType,
    OptimizationTrigger,
    OptimizationAction,
    PerformanceWindow
)

from .cross_test_learning import (
    CrossTestLearningEngine,
    LearningPattern,
    InsightCategory,
    TestInsight,
    CrossTestPattern,
    LearningModel
)

__all__ = [
    # Core Framework
    'ABTestingFramework',
    'ABTest',
    'TestVariant', 
    'TestMetrics',
    'TestStatus',
    'TestType',
    'StatisticalSignificance',
    
    # Real-time Optimization
    'RealTimeOptimizer',
    'OptimizationType',
    'OptimizationTrigger',
    'OptimizationAction',
    'PerformanceWindow',
    
    # Cross-test Learning
    'CrossTestLearningEngine',
    'LearningPattern',
    'InsightCategory',
    'TestInsight',
    'CrossTestPattern',
    'LearningModel'
]

# Version information
__version__ = '1.0.0'
__author__ = 'Claude Code'
__description__ = 'A/B Testing Framework with AI Integration and Real-time Optimization'