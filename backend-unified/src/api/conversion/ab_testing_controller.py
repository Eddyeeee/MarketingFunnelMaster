"""
A/B Testing Framework Integration
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Advanced A/B testing system with intelligent variant generation, statistical analysis,
automated winner implementation, and real-time optimization.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import uuid
import json
import asyncio
import logging
from enum import Enum
import numpy as np
from scipy import stats
import hashlib

from ...database.connection import get_database_connection
from ...services.statistical_engine import StatisticalEngine
from ...services.variant_generator import VariantGenerator
from ...models.ab_testing_models import (
    ABTest,
    TestVariant,
    TestResult,
    StatisticalSignificance
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/ab-testing", tags=["ab-testing"])

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class TestType(str, Enum):
    AB_TEST = "ab_test"
    MULTIVARIATE = "multivariate"
    BANDIT = "bandit"
    SPLIT_URL = "split_url"

class TestStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INCONCLUSIVE = "inconclusive"

class MetricType(str, Enum):
    CONVERSION_RATE = "conversion_rate"
    REVENUE = "revenue"
    ENGAGEMENT = "engagement"
    RETENTION = "retention"
    CLICK_THROUGH_RATE = "click_through_rate"
    TIME_ON_PAGE = "time_on_page"
    BOUNCE_RATE = "bounce_rate"

class VariantType(str, Enum):
    CONTROL = "control"
    VARIANT = "variant"

class AllocationStrategy(str, Enum):
    EQUAL = "equal"
    WEIGHTED = "weighted"
    BANDIT = "bandit"
    ADAPTIVE = "adaptive"

class ConfidenceLevel(float, Enum):
    NINETY = 0.90
    NINETY_FIVE = 0.95
    NINETY_NINE = 0.99

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class TrafficAllocation(BaseModel):
    variant_id: str
    allocation_percentage: float = Field(..., ge=0.0, le=1.0)

class TestConfiguration(BaseModel):
    test_name: str = Field(..., min_length=1, max_length=255)
    test_type: TestType
    hypothesis: str = Field(..., min_length=1, max_length=1000)
    
    # Metrics
    primary_metric: MetricType
    secondary_metrics: List[MetricType] = []
    
    # Statistical parameters
    confidence_level: ConfidenceLevel = ConfidenceLevel.NINETY_FIVE
    minimum_detectable_effect: float = Field(default=0.05, ge=0.01, le=1.0)
    statistical_power: float = Field(default=0.80, ge=0.70, le=0.95)
    
    # Test parameters
    max_duration_days: int = Field(default=30, ge=1, le=180)
    minimum_sample_size: int = Field(default=1000, ge=100)
    traffic_allocation: List[TrafficAllocation]
    allocation_strategy: AllocationStrategy = AllocationStrategy.EQUAL
    
    # Targeting
    target_url_pattern: str = Field(..., min_length=1)
    audience_filters: Optional[Dict[str, Any]] = None
    device_targeting: Optional[List[str]] = None
    
    # Advanced settings
    auto_winner_threshold: float = Field(default=0.95, ge=0.90, le=0.99)
    early_stopping_enabled: bool = True
    sequential_testing: bool = False

class VariantConfiguration(BaseModel):
    variant_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    variant_type: VariantType
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    
    # Variant content
    changes: Dict[str, Any] = Field(..., description="JSON describing the changes to apply")
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Performance data
    baseline_conversion_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    expected_lift: Optional[float] = Field(None, ge=-1.0, le=10.0)

class ABTestRequest(BaseModel):
    configuration: TestConfiguration
    variants: List[VariantConfiguration]
    auto_start: bool = True

class VariantAssignmentRequest(BaseModel):
    test_id: str
    user_id: Optional[str] = None
    session_id: str
    page_url: str
    user_agent: Optional[str] = None
    device_type: Optional[str] = None
    custom_attributes: Optional[Dict[str, Any]] = None

class TestEventRequest(BaseModel):
    test_id: str
    variant_id: str
    user_id: Optional[str] = None
    session_id: str
    event_type: str
    event_value: Optional[float] = None
    event_properties: Optional[Dict[str, Any]] = None

class TestResultsResponse(BaseModel):
    test_id: str
    test_status: TestStatus
    start_date: datetime
    end_date: Optional[datetime]
    
    # Overall metrics
    total_participants: int
    total_conversions: int
    overall_conversion_rate: float
    
    # Variant performance
    variant_results: List[Dict[str, Any]]
    
    # Statistical analysis
    statistical_significance: Dict[str, Any]
    confidence_intervals: Dict[str, Any]
    p_values: Dict[str, Any]
    
    # Recommendations
    winning_variant: Optional[str]
    recommendation: str
    confidence_score: float
    
    # Metadata
    last_updated: datetime

class VariantAssignmentResponse(BaseModel):
    test_id: str
    variant_id: str
    variant_type: VariantType
    assignment_timestamp: datetime
    changes: Dict[str, Any]
    tracking_data: Dict[str, Any]

# =============================================================================
# A/B TESTING SERVICE
# =============================================================================

class ABTestingService:
    """Core service for A/B testing management and analysis"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.statistical_engine = StatisticalEngine()
        self.variant_generator = VariantGenerator()
    
    async def create_ab_test(self, request: ABTestRequest) -> Dict[str, Any]:
        """Create a new A/B test with statistical validation"""
        
        test_id = str(uuid.uuid4())
        
        try:
            # 1. Validate test configuration
            await self._validate_test_configuration(request)
            
            # 2. Calculate required sample size
            required_sample_size = self.statistical_engine.calculate_sample_size(
                baseline_rate=request.variants[0].baseline_conversion_rate or 0.05,
                minimum_detectable_effect=request.configuration.minimum_detectable_effect,
                confidence_level=request.configuration.confidence_level.value,
                statistical_power=request.configuration.statistical_power
            )
            
            # 3. Store test configuration
            await self._store_test_configuration(test_id, request, required_sample_size)
            
            # 4. Store variants
            for variant in request.variants:
                await self._store_test_variant(test_id, variant)
            
            # 5. Auto-start if requested
            if request.auto_start:
                await self._start_test(test_id)
            
            return {
                "test_id": test_id,
                "status": "running" if request.auto_start else "draft",
                "required_sample_size": required_sample_size,
                "estimated_duration_days": self._estimate_test_duration(required_sample_size),
                "variants": [
                    {
                        "variant_id": v.variant_id,
                        "name": v.name,
                        "type": v.variant_type.value,
                        "weight": v.weight
                    }
                    for v in request.variants
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to create A/B test: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Test creation failed: {str(e)}")
    
    async def _validate_test_configuration(self, request: ABTestRequest):
        """Validate A/B test configuration"""
        
        # Check for control variant
        control_variants = [v for v in request.variants if v.variant_type == VariantType.CONTROL]
        if len(control_variants) != 1:
            raise ValueError("Exactly one control variant is required")
        
        # Check traffic allocation adds to 100%
        total_allocation = sum(ta.allocation_percentage for ta in request.configuration.traffic_allocation)
        if abs(total_allocation - 1.0) > 0.01:
            raise ValueError("Traffic allocation must sum to 100%")
        
        # Check variant IDs match allocation
        variant_ids = {v.variant_id for v in request.variants}
        allocation_ids = {ta.variant_id for ta in request.configuration.traffic_allocation}
        if variant_ids != allocation_ids:
            raise ValueError("Variant IDs must match traffic allocation IDs")
        
        # Check minimum sample size is achievable
        estimated_traffic = await self._estimate_daily_traffic(request.configuration.target_url_pattern)
        if estimated_traffic * request.configuration.max_duration_days < request.configuration.minimum_sample_size:
            raise ValueError("Minimum sample size may not be achievable within max duration")
    
    async def _estimate_daily_traffic(self, url_pattern: str) -> int:
        """Estimate daily traffic for URL pattern"""
        
        # Simple estimation based on historical data
        query = """
        SELECT 
            COUNT(DISTINCT session_id) / GREATEST(DATE_PART('day', MAX(event_timestamp) - MIN(event_timestamp)), 1) as daily_sessions
        FROM behavioral_tracking_events
        WHERE page_url SIMILAR TO $1
            AND event_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
        """
        
        result = await self.db.fetchrow(query, url_pattern)
        return max(int(result['daily_sessions'] or 100), 100)  # Minimum 100 daily sessions
    
    async def _store_test_configuration(self, test_id: str, request: ABTestRequest, required_sample_size: int):
        """Store A/B test configuration in database"""
        
        config = request.configuration
        
        query = """
        INSERT INTO ab_tests (
            id, test_name, test_type, hypothesis, primary_metric, secondary_metrics,
            confidence_level, minimum_detectable_effect, statistical_power, max_duration_days,
            minimum_sample_size, required_sample_size, target_url_pattern, audience_filters,
            device_targeting, auto_winner_threshold, early_stopping_enabled, sequential_testing,
            allocation_strategy, status, created_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, CURRENT_TIMESTAMP
        )
        """
        
        await self.db.execute(
            query,
            test_id,
            config.test_name,
            config.test_type.value,
            config.hypothesis,
            config.primary_metric.value,
            [m.value for m in config.secondary_metrics],
            config.confidence_level.value,
            config.minimum_detectable_effect,
            config.statistical_power,
            config.max_duration_days,
            config.minimum_sample_size,
            required_sample_size,
            config.target_url_pattern,
            config.audience_filters,
            config.device_targeting,
            config.auto_winner_threshold,
            config.early_stopping_enabled,
            config.sequential_testing,
            config.allocation_strategy.value,
            TestStatus.DRAFT.value
        )
        
        # Store traffic allocation
        for allocation in config.traffic_allocation:
            await self.db.execute(
                """
                INSERT INTO ab_test_traffic_allocation (test_id, variant_id, allocation_percentage)
                VALUES ($1, $2, $3)
                """,
                test_id, allocation.variant_id, allocation.allocation_percentage
            )
    
    async def _store_test_variant(self, test_id: str, variant: VariantConfiguration):
        """Store test variant configuration"""
        
        query = """
        INSERT INTO ab_test_variants (
            id, test_id, variant_type, name, description, changes, weight,
            baseline_conversion_rate, expected_lift, created_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, CURRENT_TIMESTAMP
        )
        """
        
        await self.db.execute(
            query,
            variant.variant_id,
            test_id,
            variant.variant_type.value,
            variant.name,
            variant.description,
            variant.changes,
            variant.weight,
            variant.baseline_conversion_rate,
            variant.expected_lift
        )
    
    async def _start_test(self, test_id: str):
        """Start an A/B test"""
        
        await self.db.execute(
            """
            UPDATE ab_tests 
            SET status = $1, start_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE id = $2
            """,
            TestStatus.RUNNING.value, test_id
        )
    
    def _estimate_test_duration(self, required_sample_size: int, daily_traffic: int = 1000) -> int:
        """Estimate test duration in days"""
        
        # Conservative estimate assuming 50% traffic allocation and 80% participation
        effective_daily_participants = daily_traffic * 0.5 * 0.8
        return max(int(required_sample_size / effective_daily_participants), 7)  # Minimum 1 week
    
    async def get_variant_assignment(self, request: VariantAssignmentRequest) -> VariantAssignmentResponse:
        """Get variant assignment for user/session"""
        
        # Get test configuration
        test_query = """
        SELECT t.*, ta.variant_id, ta.allocation_percentage
        FROM ab_tests t
        JOIN ab_test_traffic_allocation ta ON t.id = ta.test_id
        WHERE t.id = $1 AND t.status = 'running'
        """
        
        test_data = await self.db.fetch(test_query, request.test_id)
        if not test_data:
            raise HTTPException(status_code=404, detail="Active test not found")
        
        # Check if user matches targeting criteria
        if not await self._matches_targeting_criteria(request, test_data[0]):
            raise HTTPException(status_code=403, detail="User does not match test criteria")
        
        # Check for existing assignment
        existing_assignment = await self._get_existing_assignment(request.test_id, request.session_id, request.user_id)
        if existing_assignment:
            return await self._build_assignment_response(existing_assignment)
        
        # Assign to variant
        variant_id = self._assign_to_variant(request, test_data)
        
        # Store assignment
        await self._store_variant_assignment(request, variant_id)
        
        # Get variant details
        variant_details = await self._get_variant_details(variant_id)
        
        return VariantAssignmentResponse(
            test_id=request.test_id,
            variant_id=variant_id,
            variant_type=VariantType(variant_details['variant_type']),
            assignment_timestamp=datetime.now(),
            changes=variant_details['changes'],
            tracking_data={
                "test_id": request.test_id,
                "variant_id": variant_id,
                "assignment_method": "hash_based",
                "session_id": request.session_id
            }
        )
    
    async def _matches_targeting_criteria(self, request: VariantAssignmentRequest, test_config: Dict) -> bool:
        """Check if user matches test targeting criteria"""
        
        # URL pattern matching
        import re
        url_pattern = test_config['target_url_pattern']
        if not re.match(url_pattern, request.page_url):
            return False
        
        # Device targeting
        if test_config['device_targeting'] and request.device_type:
            if request.device_type not in test_config['device_targeting']:
                return False
        
        # Audience filters (if any)
        if test_config['audience_filters']:
            # Implement custom audience filtering logic here
            pass
        
        return True
    
    async def _get_existing_assignment(self, test_id: str, session_id: str, user_id: Optional[str]) -> Optional[Dict]:
        """Check for existing variant assignment"""
        
        query = """
        SELECT variant_id, assignment_timestamp
        FROM ab_test_assignments
        WHERE test_id = $1 AND (session_id = $2 OR ($3 IS NOT NULL AND user_id = $3))
        ORDER BY assignment_timestamp DESC
        LIMIT 1
        """
        
        return await self.db.fetchrow(query, test_id, session_id, user_id)
    
    def _assign_to_variant(self, request: VariantAssignmentRequest, test_data: List[Dict]) -> str:
        """Assign user to variant using deterministic hashing"""
        
        # Create deterministic hash
        hash_input = f"{request.test_id}:{request.session_id or request.user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        hash_percentage = (hash_value % 10000) / 10000.0  # 0.0 to 1.0
        
        # Find variant based on cumulative allocation
        cumulative_allocation = 0.0
        for test_row in test_data:
            cumulative_allocation += test_row['allocation_percentage']
            if hash_percentage <= cumulative_allocation:
                return test_row['variant_id']
        
        # Fallback to last variant
        return test_data[-1]['variant_id']
    
    async def _store_variant_assignment(self, request: VariantAssignmentRequest, variant_id: str):
        """Store variant assignment"""
        
        query = """
        INSERT INTO ab_test_assignments (test_id, variant_id, user_id, session_id, page_url, user_agent, device_type, assignment_timestamp)
        VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP)
        ON CONFLICT (test_id, COALESCE(user_id, ''), session_id) 
        DO UPDATE SET variant_id = $2, assignment_timestamp = CURRENT_TIMESTAMP
        """
        
        await self.db.execute(
            query,
            request.test_id,
            variant_id,
            request.user_id,
            request.session_id,
            request.page_url,
            request.user_agent,
            request.device_type
        )
    
    async def _get_variant_details(self, variant_id: str) -> Dict:
        """Get variant configuration details"""
        
        query = """
        SELECT variant_type, name, description, changes
        FROM ab_test_variants
        WHERE id = $1
        """
        
        result = await self.db.fetchrow(query, variant_id)
        if not result:
            raise HTTPException(status_code=404, detail="Variant not found")
        
        return dict(result)
    
    async def _build_assignment_response(self, assignment: Dict) -> VariantAssignmentResponse:
        """Build assignment response from existing assignment"""
        
        variant_details = await self._get_variant_details(assignment['variant_id'])
        
        return VariantAssignmentResponse(
            test_id=assignment['test_id'],
            variant_id=assignment['variant_id'],
            variant_type=VariantType(variant_details['variant_type']),
            assignment_timestamp=assignment['assignment_timestamp'],
            changes=variant_details['changes'],
            tracking_data={
                "test_id": assignment['test_id'],
                "variant_id": assignment['variant_id'],
                "assignment_method": "existing",
                "assignment_timestamp": assignment['assignment_timestamp'].isoformat()
            }
        )
    
    async def track_test_event(self, request: TestEventRequest) -> Dict[str, Any]:
        """Track A/B test event (conversion, interaction, etc.)"""
        
        event_id = str(uuid.uuid4())
        
        try:
            # Store event
            await self._store_test_event(event_id, request)
            
            # Update real-time statistics
            await self._update_test_statistics(request.test_id)
            
            # Check for early stopping conditions
            should_stop, reason = await self._check_early_stopping(request.test_id)
            
            return {
                "event_id": event_id,
                "processed": True,
                "test_id": request.test_id,
                "variant_id": request.variant_id,
                "early_stopping": {
                    "should_stop": should_stop,
                    "reason": reason
                } if should_stop else None
            }
            
        except Exception as e:
            logger.error(f"Failed to track test event: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Event tracking failed: {str(e)}")
    
    async def _store_test_event(self, event_id: str, request: TestEventRequest):
        """Store A/B test event"""
        
        query = """
        INSERT INTO ab_test_events (
            id, test_id, variant_id, user_id, session_id, event_type, event_value, event_properties, event_timestamp
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, CURRENT_TIMESTAMP
        )
        """
        
        await self.db.execute(
            query,
            event_id,
            request.test_id,
            request.variant_id,
            request.user_id,
            request.session_id,
            request.event_type,
            request.event_value,
            request.event_properties
        )
    
    async def _update_test_statistics(self, test_id: str):
        """Update real-time test statistics"""
        
        # Calculate current statistics
        stats_query = """
        SELECT 
            v.id as variant_id,
            v.name as variant_name,
            v.variant_type,
            COUNT(DISTINCT a.session_id) as participants,
            COUNT(DISTINCT CASE WHEN e.event_type = 'conversion' THEN a.session_id END) as conversions,
            COALESCE(COUNT(DISTINCT CASE WHEN e.event_type = 'conversion' THEN a.session_id END)::float / 
                     NULLIF(COUNT(DISTINCT a.session_id), 0), 0) as conversion_rate
        FROM ab_test_variants v
        LEFT JOIN ab_test_assignments a ON v.id = a.variant_id
        LEFT JOIN ab_test_events e ON v.id = e.variant_id AND a.session_id = e.session_id
        WHERE v.test_id = $1
        GROUP BY v.id, v.name, v.variant_type
        """
        
        variant_stats = await self.db.fetch(stats_query, test_id)
        
        # Store updated statistics
        for stats in variant_stats:
            await self.db.execute(
                """
                INSERT INTO ab_test_statistics (test_id, variant_id, participants, conversions, conversion_rate, updated_at)
                VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP)
                ON CONFLICT (test_id, variant_id)
                DO UPDATE SET participants = $3, conversions = $4, conversion_rate = $5, updated_at = CURRENT_TIMESTAMP
                """,
                test_id, stats['variant_id'], stats['participants'], stats['conversions'], stats['conversion_rate']
            )
    
    async def _check_early_stopping(self, test_id: str) -> tuple[bool, Optional[str]]:
        """Check if test should be stopped early"""
        
        # Get test configuration
        test_config = await self.db.fetchrow(
            "SELECT early_stopping_enabled, auto_winner_threshold, minimum_sample_size FROM ab_tests WHERE id = $1",
            test_id
        )
        
        if not test_config['early_stopping_enabled']:
            return False, None
        
        # Get current statistics
        stats = await self.db.fetch(
            "SELECT * FROM ab_test_statistics WHERE test_id = $1",
            test_id
        )
        
        if len(stats) < 2:
            return False, None
        
        # Find control and best variant
        control_stats = next((s for s in stats if s['variant_type'] == 'control'), None)
        if not control_stats:
            return False, None
        
        # Check minimum sample size
        if control_stats['participants'] < test_config['minimum_sample_size']:
            return False, None
        
        # Perform statistical test
        for variant_stats in stats:
            if variant_stats['variant_type'] == 'control':
                continue
            
            significance = self.statistical_engine.calculate_significance(
                control_conversions=control_stats['conversions'],
                control_participants=control_stats['participants'],
                variant_conversions=variant_stats['conversions'],
                variant_participants=variant_stats['participants']
            )
            
            if significance['p_value'] < (1 - test_config['auto_winner_threshold']):
                if significance['lift'] > 0:
                    return True, f"Variant {variant_stats['variant_id']} is significantly better"
                else:
                    return True, f"Control is significantly better than variant {variant_stats['variant_id']}"
        
        return False, None
    
    async def get_test_results(self, test_id: str) -> TestResultsResponse:
        """Get comprehensive A/B test results with statistical analysis"""
        
        # Get test information
        test_info = await self.db.fetchrow(
            """
            SELECT * FROM ab_tests WHERE id = $1
            """,
            test_id
        )
        
        if not test_info:
            raise HTTPException(status_code=404, detail="Test not found")
        
        # Get variant statistics
        variant_stats = await self.db.fetch(
            """
            SELECT 
                v.id, v.name, v.variant_type,
                COALESCE(s.participants, 0) as participants,
                COALESCE(s.conversions, 0) as conversions,
                COALESCE(s.conversion_rate, 0) as conversion_rate
            FROM ab_test_variants v
            LEFT JOIN ab_test_statistics s ON v.id = s.variant_id
            WHERE v.test_id = $1
            ORDER BY v.variant_type DESC, v.name
            """,
            test_id
        )
        
        # Calculate statistical significance
        control_stats = next((s for s in variant_stats if s['variant_type'] == 'control'), None)
        statistical_results = {}
        confidence_intervals = {}
        p_values = {}
        winning_variant = None
        best_conversion_rate = 0
        
        if control_stats and control_stats['participants'] > 0:
            for variant in variant_stats:
                if variant['variant_type'] == 'control':
                    continue
                
                if variant['participants'] > 0:
                    significance = self.statistical_engine.calculate_significance(
                        control_conversions=control_stats['conversions'],
                        control_participants=control_stats['participants'],
                        variant_conversions=variant['conversions'],
                        variant_participants=variant['participants']
                    )
                    
                    statistical_results[variant['id']] = significance
                    confidence_intervals[variant['id']] = significance.get('confidence_interval', [0, 0])
                    p_values[variant['id']] = significance.get('p_value', 1.0)
                    
                    if variant['conversion_rate'] > best_conversion_rate:
                        best_conversion_rate = variant['conversion_rate']
                        if significance.get('is_significant', False):
                            winning_variant = variant['id']
        
        # Generate recommendation
        total_participants = sum(s['participants'] for s in variant_stats)
        recommendation = self._generate_recommendation(
            variant_stats, statistical_results, test_info, total_participants
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(statistical_results, total_participants, test_info)
        
        return TestResultsResponse(
            test_id=test_id,
            test_status=TestStatus(test_info['status']),
            start_date=test_info['start_date'] or test_info['created_at'],
            end_date=test_info['end_date'],
            total_participants=total_participants,
            total_conversions=sum(s['conversions'] for s in variant_stats),
            overall_conversion_rate=sum(s['conversions'] for s in variant_stats) / max(total_participants, 1),
            variant_results=[
                {
                    "variant_id": s['id'],
                    "variant_name": s['name'],
                    "variant_type": s['variant_type'],
                    "participants": s['participants'],
                    "conversions": s['conversions'],
                    "conversion_rate": s['conversion_rate'],
                    "lift": ((s['conversion_rate'] - control_stats['conversion_rate']) / control_stats['conversion_rate'] * 100) 
                           if control_stats and control_stats['conversion_rate'] > 0 else 0,
                    "statistical_significance": statistical_results.get(s['id'], {})
                }
                for s in variant_stats
            ],
            statistical_significance=statistical_results,
            confidence_intervals=confidence_intervals,
            p_values=p_values,
            winning_variant=winning_variant,
            recommendation=recommendation,
            confidence_score=confidence_score,
            last_updated=datetime.now()
        )
    
    def _generate_recommendation(self, variant_stats: List[Dict], statistical_results: Dict, 
                                test_info: Dict, total_participants: int) -> str:
        """Generate test recommendation based on results"""
        
        if total_participants < test_info['minimum_sample_size']:
            return f"Continue test - need {test_info['minimum_sample_size'] - total_participants} more participants"
        
        significant_winners = [
            variant_id for variant_id, stats in statistical_results.items()
            if stats.get('is_significant', False) and stats.get('lift', 0) > 0
        ]
        
        if significant_winners:
            best_winner = max(significant_winners, 
                            key=lambda vid: statistical_results[vid].get('lift', 0))
            return f"Implement variant {best_winner} - statistically significant improvement detected"
        
        significant_losers = [
            variant_id for variant_id, stats in statistical_results.items()
            if stats.get('is_significant', False) and stats.get('lift', 0) < 0
        ]
        
        if significant_losers:
            return "Stop test and implement control - variants are significantly worse"
        
        # Check test duration
        if test_info['start_date']:
            days_running = (datetime.now() - test_info['start_date']).days
            if days_running >= test_info['max_duration_days']:
                return "Stop test - maximum duration reached with inconclusive results"
        
        return "Continue test - insufficient evidence for decision"
    
    def _calculate_confidence_score(self, statistical_results: Dict, total_participants: int, test_info: Dict) -> float:
        """Calculate overall confidence score for test results"""
        
        base_confidence = min(total_participants / test_info['minimum_sample_size'], 1.0) * 0.6
        
        if statistical_results:
            # Average confidence from statistical tests
            statistical_confidence = np.mean([
                1 - stats.get('p_value', 1.0) for stats in statistical_results.values()
            ]) * 0.4
        else:
            statistical_confidence = 0.0
        
        return min(base_confidence + statistical_confidence, 1.0)

# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post("/tests", response_model=Dict[str, Any])
async def create_ab_test(
    request: ABTestRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_database_connection)
):
    """
    Create a new A/B test with intelligent configuration
    
    - Validates test parameters and statistical requirements
    - Calculates required sample sizes
    - Sets up variant assignments and traffic allocation
    - Optionally auto-starts the test
    """
    
    service = ABTestingService(db)
    return await service.create_ab_test(request)

@router.get("/assignment", response_model=VariantAssignmentResponse)
async def get_variant_assignment(
    test_id: str,
    session_id: str,
    page_url: str,
    user_id: Optional[str] = None,
    user_agent: Optional[str] = None,
    device_type: Optional[str] = None,
    db=Depends(get_database_connection)
):
    """
    Get variant assignment for user/session
    
    - Uses deterministic hashing for consistent assignments
    - Respects traffic allocation percentages
    - Handles targeting criteria
    - Returns variant configuration for frontend implementation
    """
    
    request = VariantAssignmentRequest(
        test_id=test_id,
        user_id=user_id,
        session_id=session_id,
        page_url=page_url,
        user_agent=user_agent,
        device_type=device_type
    )
    
    service = ABTestingService(db)
    return await service.get_variant_assignment(request)

@router.post("/events")
async def track_test_event(
    request: TestEventRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_database_connection)
):
    """
    Track A/B test events (conversions, interactions, etc.)
    
    - Records events for statistical analysis
    - Updates real-time test statistics
    - Checks for early stopping conditions
    - Triggers automated winner implementation if configured
    """
    
    service = ABTestingService(db)
    return await service.track_test_event(request)

@router.get("/tests/{test_id}/results", response_model=TestResultsResponse)
async def get_test_results(
    test_id: str,
    db=Depends(get_database_connection)
):
    """
    Get comprehensive A/B test results with statistical analysis
    
    - Provides real-time performance metrics
    - Includes statistical significance calculations
    - Shows confidence intervals and p-values
    - Generates implementation recommendations
    """
    
    service = ABTestingService(db)
    return await service.get_test_results(test_id)

@router.put("/tests/{test_id}/control")
async def control_test(
    test_id: str,
    action: str = Field(..., regex="^(start|pause|resume|stop)$"),
    reason: Optional[str] = None,
    db=Depends(get_database_connection)
):
    """
    Control A/B test execution (start, pause, resume, stop)
    """
    
    valid_transitions = {
        "start": [TestStatus.DRAFT],
        "pause": [TestStatus.RUNNING],
        "resume": [TestStatus.PAUSED],
        "stop": [TestStatus.RUNNING, TestStatus.PAUSED]
    }
    
    # Get current status
    current_status = await db.fetchval(
        "SELECT status FROM ab_tests WHERE id = $1",
        test_id
    )
    
    if not current_status:
        raise HTTPException(status_code=404, detail="Test not found")
    
    current_status_enum = TestStatus(current_status)
    
    if current_status_enum not in valid_transitions[action]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot {action} test in {current_status} status"
        )
    
    # Update status
    new_status = {
        "start": TestStatus.RUNNING,
        "pause": TestStatus.PAUSED,
        "resume": TestStatus.RUNNING,
        "stop": TestStatus.STOPPED
    }[action]
    
    update_fields = ["status = $2", "updated_at = CURRENT_TIMESTAMP"]
    params = [test_id, new_status.value]
    
    if action == "start":
        update_fields.append("start_date = CURRENT_TIMESTAMP")
    elif action == "stop":
        update_fields.append("end_date = CURRENT_TIMESTAMP")
    
    await db.execute(
        f"UPDATE ab_tests SET {', '.join(update_fields)} WHERE id = $1",
        *params
    )
    
    return {
        "test_id": test_id,
        "action": action,
        "previous_status": current_status,
        "new_status": new_status.value,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/tests")
async def list_ab_tests(
    status: Optional[TestStatus] = None,
    limit: int = Field(default=50, ge=1, le=100),
    offset: int = Field(default=0, ge=0),
    db=Depends(get_database_connection)
):
    """
    List A/B tests with optional filtering
    """
    
    conditions = []
    params = []
    param_count = 0
    
    if status:
        param_count += 1
        conditions.append(f"status = ${param_count}")
        params.append(status.value)
    
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    
    param_count += 1
    params.append(limit)
    limit_clause = f"LIMIT ${param_count}"
    
    param_count += 1
    params.append(offset)
    offset_clause = f"OFFSET ${param_count}"
    
    query = f"""
    SELECT 
        id, test_name, test_type, status, primary_metric, confidence_level,
        start_date, end_date, created_at, updated_at,
        (SELECT COUNT(*) FROM ab_test_assignments WHERE test_id = ab_tests.id) as participants
    FROM ab_tests
    {where_clause}
    ORDER BY created_at DESC
    {limit_clause} {offset_clause}
    """
    
    tests = await db.fetch(query, *params)
    
    return {
        "tests": [
            {
                "test_id": test['id'],
                "test_name": test['test_name'],
                "test_type": test['test_type'],
                "status": test['status'],
                "primary_metric": test['primary_metric'],
                "confidence_level": test['confidence_level'],
                "participants": test['participants'],
                "start_date": test['start_date'].isoformat() if test['start_date'] else None,
                "end_date": test['end_date'].isoformat() if test['end_date'] else None,
                "created_at": test['created_at'].isoformat(),
                "updated_at": test['updated_at'].isoformat() if test['updated_at'] else None
            }
            for test in tests
        ],
        "limit": limit,
        "offset": offset,
        "total_count": len(tests)  # In production, you'd want a separate count query
    }