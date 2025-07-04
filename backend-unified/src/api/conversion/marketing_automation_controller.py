"""
Marketing Automation Trigger System Controller
Module: 2C - Conversion & Marketing Automation
Created: 2024-07-04

Real-time marketing automation engine with behavioral triggering, multi-channel 
orchestration, and persona-based personalization for maximum conversion rates.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import uuid
import asyncio
import logging
from enum import Enum

from ..database.connection import get_database_connection
from ..services.automation_engine import AutomationEngine
from ..services.personalization_service import PersonalizationService
from ..services.channel_orchestrator import ChannelOrchestrator
from ..models.automation_models import (
    AutomationTrigger,
    AutomationAction,
    AutomationRule,
    AutomationExecution
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/automation", tags=["marketing-automation"])

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class AutomationType(str, Enum):
    BEHAVIORAL_TRIGGER = "behavioral_trigger"
    TIME_BASED = "time_based"
    EVENT_BASED = "event_based"
    CONDITIONAL = "conditional"
    SEQUENCE = "sequence"
    A_B_TEST = "ab_test"

class TriggerType(str, Enum):
    PAGE_VIEW = "page_view"
    SCROLL_DEPTH = "scroll_depth"
    TIME_ON_PAGE = "time_on_page"
    EXIT_INTENT = "exit_intent"
    ENGAGEMENT_THRESHOLD = "engagement_threshold"
    CONVERSION_ABANDONMENT = "conversion_abandonment"
    PURCHASE_COMPLETED = "purchase_completed"
    FORM_INTERACTION = "form_interaction"
    CUSTOM_EVENT = "custom_event"

class ChannelType(str, Enum):
    WEB = "web"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SOCIAL = "social"
    RETARGETING = "retargeting"

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"

class PersonaType(str, Enum):
    TECH_EARLY_ADOPTER = "TechEarlyAdopter"
    REMOTE_DAD = "RemoteDad"
    STUDENT_HUSTLER = "StudentHustler"
    BUSINESS_OWNER = "BusinessOwner"

class DeviceType(str, Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class TriggerCondition(BaseModel):
    field: str = Field(..., min_length=1)
    operator: str = Field(..., regex="^(eq|ne|gt|gte|lt|lte|contains|in|not_in)$")
    value: Union[str, int, float, List[Union[str, int, float]]]

class AutomationTriggerRequest(BaseModel):
    trigger_type: TriggerType
    conditions: List[TriggerCondition]
    persona_filters: Optional[List[PersonaType]] = None
    device_filters: Optional[List[DeviceType]] = None
    time_window_minutes: Optional[int] = Field(None, ge=1, le=1440)

class AutomationActionRequest(BaseModel):
    action_type: str = Field(..., min_length=1)
    channel: ChannelType
    content_template: str
    personalization_config: Optional[Dict[str, Any]] = None
    delay_seconds: int = Field(default=0, ge=0, le=86400)  # Max 24 hours
    priority: int = Field(default=5, ge=1, le=10)

class AutomationRuleRequest(BaseModel):
    rule_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    automation_type: AutomationType
    triggers: List[AutomationTriggerRequest]
    actions: List[AutomationActionRequest]
    
    # Execution settings
    active: bool = True
    max_executions_per_session: int = Field(default=3, ge=1, le=10)
    cooldown_minutes: int = Field(default=30, ge=1, le=1440)
    
    # Scheduling
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    timezone: str = Field(default="UTC")
    
    # A/B testing
    ab_test_enabled: bool = False
    ab_test_variants: Optional[List[Dict[str, Any]]] = None
    
    # Performance settings
    expected_engagement_lift: Optional[float] = Field(None, ge=0.0, le=10.0)
    expected_conversion_lift: Optional[float] = Field(None, ge=0.0, le=10.0)

class AutomationRuleResponse(BaseModel):
    rule_id: str
    rule_name: str
    automation_type: str
    status: str
    created_at: datetime
    performance_metrics: Dict[str, Any]

class AutomationExecutionRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    user_id: Optional[str] = Field(None, max_length=100)
    trigger_event: Dict[str, Any]
    context_data: Optional[Dict[str, Any]] = None
    force_execution: bool = False

class AutomationExecutionResponse(BaseModel):
    execution_id: str
    rule_id: str
    session_id: str
    execution_status: ExecutionStatus
    actions_executed: List[Dict[str, Any]]
    personalization_applied: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    processing_time_ms: int

class AutomationPerformanceRequest(BaseModel):
    rule_id: Optional[str] = None
    automation_type: Optional[AutomationType] = None
    time_range_hours: int = Field(default=24, ge=1, le=168)
    channel: Optional[ChannelType] = None

class AutomationPerformanceResponse(BaseModel):
    rule_id: str
    rule_name: str
    automation_type: str
    channel: str
    executions: int
    successful_executions: int
    success_rate: float
    avg_engagement_lift: float
    avg_conversion_lift: float
    roi_estimate: float

# =============================================================================
# PERSONA-BASED CONTENT MATRICES
# =============================================================================

class PersonaContentMatrix:
    """Content templates for different personas and devices"""
    
    CONTENT_TEMPLATES = {
        PersonaType.TECH_EARLY_ADOPTER: {
            DeviceType.MOBILE: {
                "hook_message": "🚀 Revolutionary tech breakthrough - be among the first!",
                "cta_text": "Get Early Access",
                "urgency_message": "Limited beta spots available",
                "social_proof": "Join 10,000+ tech innovators"
            },
            DeviceType.DESKTOP: {
                "hook_message": "Deep dive into cutting-edge technology",
                "cta_text": "Access Technical Documentation",
                "urgency_message": "Exclusive access ending soon",
                "social_proof": "Trusted by leading tech companies"
            },
            DeviceType.TABLET: {
                "hook_message": "Interactive tech showcase",
                "cta_text": "Explore Features",
                "urgency_message": "Preview access limited",
                "social_proof": "Featured by tech reviewers"
            }
        },
        PersonaType.REMOTE_DAD: {
            DeviceType.MOBILE: {
                "hook_message": "⚡ More time with family, less time working",
                "cta_text": "Save Time Now",
                "urgency_message": "Family time is precious",
                "social_proof": "5,000+ working parents love this"
            },
            DeviceType.DESKTOP: {
                "hook_message": "Work-life balance solution for busy parents",
                "cta_text": "Calculate Time Savings",
                "urgency_message": "Limited-time family discount",
                "social_proof": "Recommended by productivity experts"
            },
            DeviceType.TABLET: {
                "hook_message": "Family-friendly productivity boost",
                "cta_text": "Try Family Mode",
                "urgency_message": "Weekend special offer",
                "social_proof": "Featured in Working Parent Magazine"
            }
        },
        PersonaType.STUDENT_HUSTLER: {
            DeviceType.MOBILE: {
                "hook_message": "💰 Student discount: 50% OFF - Limited time!",
                "cta_text": "Claim Student Discount",
                "urgency_message": "Student pricing ends midnight",
                "social_proof": "Used by students at 500+ universities"
            },
            DeviceType.DESKTOP: {
                "hook_message": "Accelerate your career with student pricing",
                "cta_text": "Verify Student Status",
                "urgency_message": "Academic year discount ending",
                "social_proof": "Recommended by career counselors"
            },
            DeviceType.TABLET: {
                "hook_message": "Study smarter, not harder",
                "cta_text": "Start Free Study Trial",
                "urgency_message": "Semester special ending",
                "social_proof": "Featured in Student Success Magazine"
            }
        },
        PersonaType.BUSINESS_OWNER: {
            DeviceType.MOBILE: {
                "hook_message": "📈 ROI guaranteed or money back",
                "cta_text": "Calculate ROI",
                "urgency_message": "Q4 pricing lock expires soon",
                "social_proof": "Trusted by 10,000+ businesses"
            },
            DeviceType.DESKTOP: {
                "hook_message": "Enterprise-grade solution with proven ROI",
                "cta_text": "Request Enterprise Demo",
                "urgency_message": "Implementation slots filling fast",
                "social_proof": "Featured in Forbes, Inc., Entrepreneur"
            },
            DeviceType.TABLET: {
                "hook_message": "Business dashboard preview",
                "cta_text": "See Business Impact",
                "urgency_message": "Executive briefing slots limited",
                "social_proof": "Used by Fortune 500 companies"
            }
        }
    }
    
    @classmethod
    def get_content(cls, persona: PersonaType, device: DeviceType, content_type: str) -> str:
        """Get persona and device-specific content"""
        
        persona_content = cls.CONTENT_TEMPLATES.get(persona, {})
        device_content = persona_content.get(device, {})
        return device_content.get(content_type, "Default content")

# =============================================================================
# MARKETING AUTOMATION SERVICE
# =============================================================================

class MarketingAutomationService:
    """Core service for marketing automation orchestration"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.automation_engine = AutomationEngine(db_connection)
        self.personalization_service = PersonalizationService(db_connection)
        self.channel_orchestrator = ChannelOrchestrator(db_connection)
    
    async def create_automation_rule(self, request: AutomationRuleRequest) -> AutomationRuleResponse:
        """Create new automation rule"""
        
        rule_id = str(uuid.uuid4())
        
        try:
            # Store automation rule
            await self._store_automation_rule(rule_id, request)
            
            # Initialize performance tracking
            performance_metrics = await self._initialize_performance_tracking(rule_id)
            
            # Start rule if active
            if request.active:
                await self.automation_engine.activate_rule(rule_id)
            
            return AutomationRuleResponse(
                rule_id=rule_id,
                rule_name=request.rule_name,
                automation_type=request.automation_type.value,
                status="active" if request.active else "inactive",
                created_at=datetime.now(),
                performance_metrics=performance_metrics
            )
            
        except Exception as e:
            logger.error(f"Failed to create automation rule: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Rule creation failed: {str(e)}")
    
    async def _store_automation_rule(self, rule_id: str, request: AutomationRuleRequest):
        """Store automation rule in database"""
        
        # Store main rule
        rule_query = """
        INSERT INTO automation_rules (
            id, rule_name, description, automation_type, active,
            max_executions_per_session, cooldown_minutes, start_date, end_date,
            timezone, ab_test_enabled, ab_test_variants, expected_engagement_lift,
            expected_conversion_lift, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, CURRENT_TIMESTAMP)
        """
        
        await self.db.execute(
            rule_query,
            rule_id,
            request.rule_name,
            request.description,
            request.automation_type.value,
            request.active,
            request.max_executions_per_session,
            request.cooldown_minutes,
            request.start_date,
            request.end_date,
            request.timezone,
            request.ab_test_enabled,
            request.ab_test_variants,
            request.expected_engagement_lift,
            request.expected_conversion_lift
        )
        
        # Store triggers
        for i, trigger in enumerate(request.triggers):
            trigger_query = """
            INSERT INTO automation_triggers (
                id, rule_id, trigger_type, conditions, persona_filters,
                device_filters, time_window_minutes, order_index
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """
            
            persona_filters = [p.value for p in trigger.persona_filters] if trigger.persona_filters else None
            device_filters = [d.value for d in trigger.device_filters] if trigger.device_filters else None
            
            await self.db.execute(
                trigger_query,
                str(uuid.uuid4()),
                rule_id,
                trigger.trigger_type.value,
                [c.dict() for c in trigger.conditions],
                persona_filters,
                device_filters,
                trigger.time_window_minutes,
                i
            )
        
        # Store actions
        for i, action in enumerate(request.actions):
            action_query = """
            INSERT INTO automation_actions (
                id, rule_id, action_type, channel, content_template,
                personalization_config, delay_seconds, priority, order_index
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """
            
            await self.db.execute(
                action_query,
                str(uuid.uuid4()),
                rule_id,
                action.action_type,
                action.channel.value,
                action.content_template,
                action.personalization_config,
                action.delay_seconds,
                action.priority,
                i
            )
    
    async def _initialize_performance_tracking(self, rule_id: str) -> Dict[str, Any]:
        """Initialize performance tracking for automation rule"""
        
        return {
            "executions": 0,
            "successful_executions": 0,
            "success_rate": 0.0,
            "avg_engagement_lift": 0.0,
            "avg_conversion_lift": 0.0,
            "created_at": datetime.now().isoformat()
        }
    
    async def execute_automation(self, request: AutomationExecutionRequest) -> AutomationExecutionResponse:
        """Execute automation based on trigger event"""
        
        start_time = datetime.now()
        execution_id = str(uuid.uuid4())
        
        try:
            # Find matching automation rules
            matching_rules = await self._find_matching_rules(request)
            
            if not matching_rules:
                return AutomationExecutionResponse(
                    execution_id=execution_id,
                    rule_id="none",
                    session_id=request.session_id,
                    execution_status=ExecutionStatus.SKIPPED,
                    actions_executed=[],
                    personalization_applied={},
                    performance_metrics={},
                    processing_time_ms=0
                )
            
            # Execute the highest priority rule
            rule = matching_rules[0]
            
            # Check execution limits and cooldowns
            if not request.force_execution:
                execution_allowed = await self._check_execution_limits(rule['id'], request.session_id)
                if not execution_allowed:
                    return AutomationExecutionResponse(
                        execution_id=execution_id,
                        rule_id=rule['id'],
                        session_id=request.session_id,
                        execution_status=ExecutionStatus.SKIPPED,
                        actions_executed=[],
                        personalization_applied={},
                        performance_metrics={"skip_reason": "execution_limits"},
                        processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
                    )
            
            # Get user context for personalization
            user_context = await self._get_user_context(request.session_id, request.user_id)
            
            # Execute actions
            actions_executed = await self._execute_rule_actions(rule, request, user_context)
            
            # Apply personalization
            personalization_applied = await self._apply_personalization(rule, user_context, actions_executed)
            
            # Record execution
            await self._record_execution(execution_id, rule['id'], request, actions_executed, personalization_applied)
            
            # Update performance metrics
            performance_metrics = await self._update_performance_metrics(rule['id'], actions_executed)
            
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return AutomationExecutionResponse(
                execution_id=execution_id,
                rule_id=rule['id'],
                session_id=request.session_id,
                execution_status=ExecutionStatus.COMPLETED,
                actions_executed=actions_executed,
                personalization_applied=personalization_applied,
                performance_metrics=performance_metrics,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logger.error(f"Automation execution failed: {str(e)}")
            
            # Record failed execution
            await self._record_failed_execution(execution_id, request, str(e))
            
            return AutomationExecutionResponse(
                execution_id=execution_id,
                rule_id="error",
                session_id=request.session_id,
                execution_status=ExecutionStatus.FAILED,
                actions_executed=[],
                personalization_applied={},
                performance_metrics={"error": str(e)},
                processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )
    
    async def _find_matching_rules(self, request: AutomationExecutionRequest) -> List[Dict[str, Any]]:
        """Find automation rules that match the trigger event"""
        
        query = """
        SELECT ar.*, 
               array_agg(DISTINCT at.*) as triggers,
               array_agg(DISTINCT aa.*) as actions
        FROM automation_rules ar
        LEFT JOIN automation_triggers at ON ar.id = at.rule_id
        LEFT JOIN automation_actions aa ON ar.id = aa.rule_id
        WHERE ar.active = true
            AND (ar.start_date IS NULL OR ar.start_date <= CURRENT_TIMESTAMP)
            AND (ar.end_date IS NULL OR ar.end_date >= CURRENT_TIMESTAMP)
        GROUP BY ar.id
        ORDER BY ar.created_at DESC
        """
        
        rules = await self.db.fetch(query)
        
        matching_rules = []
        
        for rule in rules:
            # Check if trigger conditions match
            if await self._check_trigger_conditions(rule, request):
                matching_rules.append(dict(rule))
        
        return matching_rules
    
    async def _check_trigger_conditions(self, rule: Dict[str, Any], request: AutomationExecutionRequest) -> bool:
        """Check if trigger conditions are met"""
        
        triggers = rule.get('triggers', [])
        trigger_event = request.trigger_event
        
        for trigger in triggers:
            if not trigger:
                continue
                
            trigger_type = trigger.get('trigger_type')
            conditions = trigger.get('conditions', [])
            
            # Check if trigger type matches
            if trigger_type and trigger_type != trigger_event.get('type'):
                continue
            
            # Check conditions
            conditions_met = True
            for condition in conditions:
                if not self._evaluate_condition(condition, trigger_event):
                    conditions_met = False
                    break
            
            if conditions_met:
                return True
        
        return False
    
    def _evaluate_condition(self, condition: Dict[str, Any], event_data: Dict[str, Any]) -> bool:
        """Evaluate a single trigger condition"""
        
        field = condition.get('field')
        operator = condition.get('operator')
        expected_value = condition.get('value')
        
        actual_value = event_data.get(field)
        
        if actual_value is None:
            return False
        
        try:
            if operator == 'eq':
                return actual_value == expected_value
            elif operator == 'ne':
                return actual_value != expected_value
            elif operator == 'gt':
                return float(actual_value) > float(expected_value)
            elif operator == 'gte':
                return float(actual_value) >= float(expected_value)
            elif operator == 'lt':
                return float(actual_value) < float(expected_value)
            elif operator == 'lte':
                return float(actual_value) <= float(expected_value)
            elif operator == 'contains':
                return str(expected_value).lower() in str(actual_value).lower()
            elif operator == 'in':
                return actual_value in expected_value if isinstance(expected_value, list) else False
            elif operator == 'not_in':
                return actual_value not in expected_value if isinstance(expected_value, list) else True
            else:
                return False
        except (ValueError, TypeError):
            return False
    
    async def _check_execution_limits(self, rule_id: str, session_id: str) -> bool:
        """Check if execution is allowed based on limits and cooldowns"""
        
        query = """
        SELECT COUNT(*) as execution_count,
               MAX(execution_timestamp) as last_execution
        FROM marketing_automation_events
        WHERE rule_id = $1 AND session_id = $2
            AND execution_timestamp >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
        """
        
        result = await self.db.fetchrow(query, rule_id, session_id)
        
        if not result:
            return True
        
        execution_count = result['execution_count']
        last_execution = result['last_execution']
        
        # Check max executions per session (default from rule)
        if execution_count >= 3:  # This should come from rule config
            return False
        
        # Check cooldown period
        if last_execution:
            cooldown_minutes = 30  # This should come from rule config
            time_since_last = datetime.now() - last_execution
            if time_since_last.total_seconds() < (cooldown_minutes * 60):
                return False
        
        return True
    
    async def _get_user_context(self, session_id: str, user_id: Optional[str]) -> Dict[str, Any]:
        """Get user context for personalization"""
        
        # Get session data from journey_sessions
        session_query = """
        SELECT persona_type, device_type, current_stage, 
               engagement_score, conversion_probability
        FROM journey_sessions
        WHERE session_id = $1
        """
        
        session_data = await self.db.fetchrow(session_query, session_id)
        
        if not session_data:
            return {"persona": "unknown", "device": "unknown"}
        
        return {
            "persona": session_data['persona_type'],
            "device": session_data['device_type'],
            "stage": session_data['current_stage'],
            "engagement_score": session_data['engagement_score'],
            "conversion_probability": session_data['conversion_probability']
        }
    
    async def _execute_rule_actions(self, rule: Dict[str, Any], request: AutomationExecutionRequest, user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute all actions for an automation rule"""
        
        actions = rule.get('actions', [])
        executed_actions = []
        
        for action in actions:
            if not action:
                continue
            
            try:
                # Apply delay if specified
                delay_seconds = action.get('delay_seconds', 0)
                if delay_seconds > 0:
                    await asyncio.sleep(delay_seconds)
                
                # Execute action based on channel
                action_result = await self._execute_channel_action(action, user_context, request)
                
                executed_actions.append({
                    "action_id": action.get('id'),
                    "action_type": action.get('action_type'),
                    "channel": action.get('channel'),
                    "status": "completed",
                    "result": action_result,
                    "executed_at": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Action execution failed: {str(e)}")
                
                executed_actions.append({
                    "action_id": action.get('id'),
                    "action_type": action.get('action_type'),
                    "channel": action.get('channel'),
                    "status": "failed",
                    "error": str(e),
                    "executed_at": datetime.now().isoformat()
                })
        
        return executed_actions
    
    async def _execute_channel_action(self, action: Dict[str, Any], user_context: Dict[str, Any], request: AutomationExecutionRequest) -> Dict[str, Any]:
        """Execute action on specific channel"""
        
        channel = action.get('channel')
        action_type = action.get('action_type')
        content_template = action.get('content_template')
        
        # Get personalized content
        persona = user_context.get('persona', 'unknown')
        device = user_context.get('device', 'unknown')
        
        try:
            persona_enum = PersonaType(persona)
            device_enum = DeviceType(device)
        except ValueError:
            persona_enum = PersonaType.TECH_EARLY_ADOPTER
            device_enum = DeviceType.DESKTOP
        
        if channel == ChannelType.WEB:
            return await self._execute_web_action(action_type, content_template, persona_enum, device_enum, request)
        elif channel == ChannelType.EMAIL:
            return await self._execute_email_action(action_type, content_template, persona_enum, device_enum, request)
        elif channel == ChannelType.SMS:
            return await self._execute_sms_action(action_type, content_template, persona_enum, device_enum, request)
        elif channel == ChannelType.PUSH:
            return await self._execute_push_action(action_type, content_template, persona_enum, device_enum, request)
        else:
            return {"status": "unsupported_channel", "channel": channel}
    
    async def _execute_web_action(self, action_type: str, content_template: str, persona: PersonaType, device: DeviceType, request: AutomationExecutionRequest) -> Dict[str, Any]:
        """Execute web-based action"""
        
        if action_type == "show_exit_offer":
            content = PersonaContentMatrix.get_content(persona, device, "hook_message")
            cta = PersonaContentMatrix.get_content(persona, device, "cta_text")
            
            return {
                "action": "display_modal",
                "content": content,
                "cta": cta,
                "position": "center_overlay",
                "timing": "immediate"
            }
        
        elif action_type == "highlight_urgency":
            urgency_message = PersonaContentMatrix.get_content(persona, device, "urgency_message")
            
            return {
                "action": "add_urgency_banner",
                "content": urgency_message,
                "position": "top_banner",
                "style": "urgent"
            }
        
        elif action_type == "show_social_proof":
            social_proof = PersonaContentMatrix.get_content(persona, device, "social_proof")
            
            return {
                "action": "display_social_proof",
                "content": social_proof,
                "position": "sidebar",
                "animation": "slide_in"
            }
        
        elif action_type == "personalize_cta":
            cta = PersonaContentMatrix.get_content(persona, device, "cta_text")
            
            return {
                "action": "update_cta",
                "content": cta,
                "style": f"{persona.value.lower()}_{device.value}",
                "urgency": "medium"
            }
        
        else:
            return {
                "action": "generic_web_action",
                "content": content_template,
                "persona": persona.value,
                "device": device.value
            }
    
    async def _execute_email_action(self, action_type: str, content_template: str, persona: PersonaType, device: DeviceType, request: AutomationExecutionRequest) -> Dict[str, Any]:
        """Execute email action"""
        
        subject = PersonaContentMatrix.get_content(persona, device, "hook_message")
        cta = PersonaContentMatrix.get_content(persona, device, "cta_text")
        
        return {
            "action": "send_email",
            "subject": subject,
            "content": content_template,
            "cta": cta,
            "template": f"{persona.value.lower()}_email_template",
            "delivery_status": "queued"
        }
    
    async def _execute_sms_action(self, action_type: str, content_template: str, persona: PersonaType, device: DeviceType, request: AutomationExecutionRequest) -> Dict[str, Any]:
        """Execute SMS action"""
        
        message = PersonaContentMatrix.get_content(persona, device, "urgency_message")
        
        return {
            "action": "send_sms",
            "message": message[:160],  # SMS character limit
            "delivery_status": "queued"
        }
    
    async def _execute_push_action(self, action_type: str, content_template: str, persona: PersonaType, device: DeviceType, request: AutomationExecutionRequest) -> Dict[str, Any]:
        """Execute push notification action"""
        
        title = PersonaContentMatrix.get_content(persona, device, "hook_message")
        body = PersonaContentMatrix.get_content(persona, device, "urgency_message")
        
        return {
            "action": "send_push",
            "title": title,
            "body": body,
            "delivery_status": "queued"
        }
    
    async def _apply_personalization(self, rule: Dict[str, Any], user_context: Dict[str, Any], actions_executed: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply personalization to automation actions"""
        
        return {
            "persona_applied": user_context.get('persona', 'unknown'),
            "device_optimized": user_context.get('device', 'unknown'),
            "engagement_level": user_context.get('engagement_score', 0.5),
            "personalization_confidence": 0.85,
            "content_variants_used": len(actions_executed)
        }
    
    async def _record_execution(self, execution_id: str, rule_id: str, request: AutomationExecutionRequest, actions_executed: List[Dict[str, Any]], personalization_applied: Dict[str, Any]):
        """Record automation execution in database"""
        
        query = """
        INSERT INTO marketing_automation_events (
            id, rule_id, session_id, user_id, automation_type, automation_trigger,
            trigger_context, execution_status, execution_timestamp, execution_result,
            actions_executed, personalization_applied
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, CURRENT_TIMESTAMP, $9, $10, $11)
        """
        
        await self.db.execute(
            query,
            execution_id,
            rule_id,
            request.session_id,
            request.user_id,
            "behavioral_trigger",  # This should come from rule
            request.trigger_event.get('type', 'unknown'),
            request.trigger_event,
            ExecutionStatus.COMPLETED.value,
            {"status": "success", "actions_count": len(actions_executed)},
            actions_executed,
            personalization_applied
        )
    
    async def _record_failed_execution(self, execution_id: str, request: AutomationExecutionRequest, error: str):
        """Record failed automation execution"""
        
        query = """
        INSERT INTO marketing_automation_events (
            id, session_id, user_id, automation_trigger, trigger_context,
            execution_status, execution_timestamp, execution_result, error_message
        ) VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP, $7, $8)
        """
        
        await self.db.execute(
            query,
            execution_id,
            request.session_id,
            request.user_id,
            request.trigger_event.get('type', 'unknown'),
            request.trigger_event,
            ExecutionStatus.FAILED.value,
            {"status": "failed"},
            error
        )
    
    async def _update_performance_metrics(self, rule_id: str, actions_executed: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update performance metrics for automation rule"""
        
        successful_actions = sum(1 for action in actions_executed if action.get('status') == 'completed')
        total_actions = len(actions_executed)
        
        return {
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "success_rate": successful_actions / total_actions if total_actions > 0 else 0,
            "execution_timestamp": datetime.now().isoformat()
        }
    
    async def get_automation_performance(self, request: AutomationPerformanceRequest) -> List[AutomationPerformanceResponse]:
        """Get automation performance analytics"""
        
        conditions = ["mae.execution_timestamp >= CURRENT_TIMESTAMP - ($1 || ' hours')::INTERVAL"]
        params = [request.time_range_hours]
        param_count = 1
        
        if request.rule_id:
            param_count += 1
            conditions.append(f"mae.rule_id = ${param_count}")
            params.append(request.rule_id)
        
        if request.automation_type:
            param_count += 1
            conditions.append(f"ar.automation_type = ${param_count}")
            params.append(request.automation_type.value)
        
        if request.channel:
            param_count += 1
            conditions.append(f"aa.channel = ${param_count}")
            params.append(request.channel.value)
        
        where_clause = " AND ".join(conditions)
        
        query = f"""
        SELECT 
            ar.id as rule_id,
            ar.rule_name,
            ar.automation_type,
            aa.channel,
            COUNT(mae.id) as executions,
            COUNT(mae.id) FILTER (WHERE mae.execution_status = 'completed') as successful_executions,
            ROUND(
                (COUNT(mae.id) FILTER (WHERE mae.execution_status = 'completed')::NUMERIC / 
                 NULLIF(COUNT(mae.id), 0)) * 100, 2
            ) as success_rate,
            ROUND(AVG(ar.expected_engagement_lift), 2) as avg_engagement_lift,
            ROUND(AVG(ar.expected_conversion_lift), 2) as avg_conversion_lift,
            ROUND(AVG(ar.expected_engagement_lift) * COUNT(mae.id) * 0.1, 2) as roi_estimate
        FROM automation_rules ar
        LEFT JOIN automation_actions aa ON ar.id = aa.rule_id
        LEFT JOIN marketing_automation_events mae ON ar.id = mae.rule_id
        WHERE {where_clause}
        GROUP BY ar.id, ar.rule_name, ar.automation_type, aa.channel
        ORDER BY executions DESC
        """
        
        rows = await self.db.fetch(query, *params)
        
        return [
            AutomationPerformanceResponse(
                rule_id=row['rule_id'],
                rule_name=row['rule_name'],
                automation_type=row['automation_type'],
                channel=row['channel'] or 'unknown',
                executions=row['executions'],
                successful_executions=row['successful_executions'],
                success_rate=float(row['success_rate'] or 0),
                avg_engagement_lift=float(row['avg_engagement_lift'] or 0),
                avg_conversion_lift=float(row['avg_conversion_lift'] or 0),
                roi_estimate=float(row['roi_estimate'] or 0)
            )
            for row in rows
        ]

# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post("/rules", response_model=AutomationRuleResponse)
async def create_automation_rule(
    request: AutomationRuleRequest,
    db=Depends(get_database_connection)
):
    """
    Create new marketing automation rule
    
    - Supports behavioral, time-based, and event-based triggers
    - Multi-channel action orchestration (Web, Email, SMS, Push)
    - Persona and device-specific personalization
    - A/B testing capabilities
    """
    
    service = MarketingAutomationService(db)
    return await service.create_automation_rule(request)

@router.post("/execute", response_model=AutomationExecutionResponse)
async def execute_automation(
    request: AutomationExecutionRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_database_connection)
):
    """
    Execute automation based on trigger event
    
    - Real-time trigger evaluation (<100ms)
    - Persona-based personalization
    - Multi-channel action execution
    - Performance tracking and optimization
    """
    
    service = MarketingAutomationService(db)
    return await service.execute_automation(request)

@router.get("/performance", response_model=List[AutomationPerformanceResponse])
async def get_automation_performance(
    request: AutomationPerformanceRequest = Depends(),
    db=Depends(get_database_connection)
):
    """
    Get marketing automation performance analytics
    
    Returns performance metrics by automation rule, type, and channel
    """
    
    service = MarketingAutomationService(db)
    return await service.get_automation_performance(request)

@router.get("/rules")
async def list_automation_rules(
    active_only: bool = True,
    automation_type: Optional[AutomationType] = None,
    db=Depends(get_database_connection)
):
    """
    List automation rules with filtering options
    """
    
    conditions = []
    params = []
    
    if active_only:
        conditions.append("active = true")
    
    if automation_type:
        conditions.append("automation_type = $" + str(len(params) + 1))
        params.append(automation_type.value)
    
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
    SELECT id, rule_name, automation_type, active, created_at,
           expected_engagement_lift, expected_conversion_lift
    FROM automation_rules
    {where_clause}
    ORDER BY created_at DESC
    """
    
    rows = await db.fetch(query, *params)
    
    return [
        {
            "rule_id": row['id'],
            "rule_name": row['rule_name'],
            "automation_type": row['automation_type'],
            "active": row['active'],
            "created_at": row['created_at'].isoformat(),
            "expected_engagement_lift": row['expected_engagement_lift'],
            "expected_conversion_lift": row['expected_conversion_lift']
        }
        for row in rows
    ]

@router.put("/rules/{rule_id}/status")
async def update_rule_status(
    rule_id: str,
    active: bool,
    db=Depends(get_database_connection)
):
    """
    Update automation rule status (active/inactive)
    """
    
    query = """
    UPDATE automation_rules 
    SET active = $1, updated_at = CURRENT_TIMESTAMP
    WHERE id = $2
    RETURNING id, rule_name, active
    """
    
    result = await db.fetchrow(query, active, rule_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Automation rule not found")
    
    return {
        "rule_id": result['id'],
        "rule_name": result['rule_name'],
        "active": result['active'],
        "updated_at": datetime.now().isoformat()
    }

@router.get("/analytics/summary")
async def get_automation_analytics_summary(
    time_range_hours: int = Field(default=24, ge=1, le=168),
    db=Depends(get_database_connection)
):
    """
    Get automation analytics summary
    """
    
    query = """
    SELECT 
        automation_type,
        COUNT(*) as total_executions,
        COUNT(*) FILTER (WHERE execution_status = 'completed') as successful_executions,
        COUNT(DISTINCT session_id) as unique_sessions,
        ROUND(
            (COUNT(*) FILTER (WHERE execution_status = 'completed')::NUMERIC / 
             COUNT(*)::NUMERIC) * 100, 2
        ) as success_rate
    FROM marketing_automation_events
    WHERE execution_timestamp >= CURRENT_TIMESTAMP - ($1 || ' hours')::INTERVAL
    GROUP BY automation_type
    ORDER BY total_executions DESC
    """
    
    rows = await db.fetch(query, time_range_hours)
    
    return {
        "time_range_hours": time_range_hours,
        "summary": [
            {
                "automation_type": row['automation_type'],
                "total_executions": row['total_executions'],
                "successful_executions": row['successful_executions'],
                "unique_sessions": row['unique_sessions'],
                "success_rate": float(row['success_rate'] or 0)
            }
            for row in rows
        ]
    }