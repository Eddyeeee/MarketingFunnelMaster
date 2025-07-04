"""
Behavioral Trigger Engine for Real-Time Marketing Automation
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Advanced trigger engine that processes behavioral events and fires
real-time marketing automation based on user actions and patterns.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TriggerType(str, Enum):
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    CONDITIONAL = "conditional"
    THRESHOLD = "threshold"
    SEQUENCE = "sequence"

class TriggerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    EXPIRED = "expired"

class ActionType(str, Enum):
    EMAIL = "email"
    POPUP = "popup"
    REDIRECT = "redirect"
    PERSONALIZATION = "personalization"
    DISCOUNT = "discount"
    NOTIFICATION = "notification"
    AB_TEST_ASSIGNMENT = "ab_test_assignment"
    CONTENT_CHANGE = "content_change"

class TriggerCondition:
    """Represents a trigger condition"""
    
    def __init__(self, 
                 field: str, 
                 operator: str, 
                 value: Any, 
                 condition_type: str = "simple"):
        self.field = field
        self.operator = operator  # eq, ne, gt, lt, gte, lte, contains, in, not_in
        self.value = value
        self.condition_type = condition_type  # simple, aggregate, temporal
    
    def evaluate(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> bool:
        """Evaluate the condition against data"""
        
        try:
            # Get field value from data
            field_value = self._get_field_value(data, self.field)
            
            if field_value is None:
                return False
            
            # Evaluate based on operator
            if self.operator == "eq":
                return field_value == self.value
            elif self.operator == "ne":
                return field_value != self.value
            elif self.operator == "gt":
                return field_value > self.value
            elif self.operator == "lt":
                return field_value < self.value
            elif self.operator == "gte":
                return field_value >= self.value
            elif self.operator == "lte":
                return field_value <= self.value
            elif self.operator == "contains":
                return str(self.value).lower() in str(field_value).lower()
            elif self.operator == "in":
                return field_value in self.value
            elif self.operator == "not_in":
                return field_value not in self.value
            elif self.operator == "exists":
                return field_value is not None
            elif self.operator == "not_exists":
                return field_value is None
            else:
                logger.warning(f"Unknown operator: {self.operator}")
                return False
                
        except Exception as e:
            logger.error(f"Condition evaluation error: {e}")
            return False
    
    def _get_field_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Get nested field value using dot notation"""
        
        try:
            value = data
            for key in field_path.split('.'):
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return None
            return value
        except Exception:
            return None

class TriggerAction:
    """Represents a trigger action"""
    
    def __init__(self, 
                 action_type: ActionType, 
                 parameters: Dict[str, Any],
                 delay_seconds: int = 0):
        self.action_type = action_type
        self.parameters = parameters
        self.delay_seconds = delay_seconds
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the trigger action"""
        
        try:
            if self.delay_seconds > 0:
                await asyncio.sleep(self.delay_seconds)
            
            # Execute based on action type
            if self.action_type == ActionType.EMAIL:
                return await self._send_email(context)
            elif self.action_type == ActionType.POPUP:
                return await self._show_popup(context)
            elif self.action_type == ActionType.REDIRECT:
                return await self._redirect_user(context)
            elif self.action_type == ActionType.PERSONALIZATION:
                return await self._apply_personalization(context)
            elif self.action_type == ActionType.DISCOUNT:
                return await self._apply_discount(context)
            elif self.action_type == ActionType.NOTIFICATION:
                return await self._send_notification(context)
            elif self.action_type == ActionType.AB_TEST_ASSIGNMENT:
                return await self._assign_ab_test(context)
            elif self.action_type == ActionType.CONTENT_CHANGE:
                return await self._change_content(context)
            else:
                logger.warning(f"Unknown action type: {self.action_type}")
                return {"status": "error", "message": "Unknown action type"}
                
        except Exception as e:
            logger.error(f"Action execution error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _send_email(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Send email action"""
        # Implementation would integrate with email service
        return {
            "status": "success",
            "action": "email_sent",
            "template": self.parameters.get("template"),
            "recipient": context.get("user_id")
        }
    
    async def _show_popup(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Show popup action"""
        return {
            "status": "success",
            "action": "popup_triggered",
            "popup_type": self.parameters.get("popup_type"),
            "content": self.parameters.get("content"),
            "session_id": context.get("session_id")
        }
    
    async def _redirect_user(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Redirect user action"""
        return {
            "status": "success",
            "action": "redirect_triggered",
            "url": self.parameters.get("url"),
            "session_id": context.get("session_id")
        }
    
    async def _apply_personalization(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply personalization action"""
        return {
            "status": "success",
            "action": "personalization_applied",
            "changes": self.parameters.get("changes"),
            "session_id": context.get("session_id")
        }
    
    async def _apply_discount(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply discount action"""
        return {
            "status": "success",
            "action": "discount_applied",
            "discount_code": self.parameters.get("discount_code"),
            "discount_amount": self.parameters.get("discount_amount"),
            "session_id": context.get("session_id")
        }
    
    async def _send_notification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Send notification action"""
        return {
            "status": "success",
            "action": "notification_sent",
            "message": self.parameters.get("message"),
            "session_id": context.get("session_id")
        }
    
    async def _assign_ab_test(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assign A/B test action"""
        return {
            "status": "success",
            "action": "ab_test_assigned",
            "test_id": self.parameters.get("test_id"),
            "variant_id": self.parameters.get("variant_id"),
            "session_id": context.get("session_id")
        }
    
    async def _change_content(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Change content action"""
        return {
            "status": "success",
            "action": "content_changed",
            "element": self.parameters.get("element"),
            "content": self.parameters.get("content"),
            "session_id": context.get("session_id")
        }

class Trigger:
    """Represents a complete trigger with conditions and actions"""
    
    def __init__(self, 
                 trigger_id: str,
                 name: str,
                 trigger_type: TriggerType,
                 conditions: List[TriggerCondition],
                 actions: List[TriggerAction],
                 priority: int = 0,
                 max_executions: Optional[int] = None,
                 cooldown_seconds: int = 0):
        self.trigger_id = trigger_id
        self.name = name
        self.trigger_type = trigger_type
        self.conditions = conditions
        self.actions = actions
        self.priority = priority
        self.max_executions = max_executions
        self.cooldown_seconds = cooldown_seconds
        
        # Runtime state
        self.status = TriggerStatus.ACTIVE
        self.execution_count = 0
        self.last_execution = None
        self.created_at = datetime.now()
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        """Check if trigger can be executed"""
        
        # Check status
        if self.status != TriggerStatus.ACTIVE:
            return False
        
        # Check max executions
        if self.max_executions and self.execution_count >= self.max_executions:
            return False
        
        # Check cooldown
        if (self.cooldown_seconds > 0 and 
            self.last_execution and 
            (datetime.now() - self.last_execution).total_seconds() < self.cooldown_seconds):
            return False
        
        return True
    
    def evaluate_conditions(self, data: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate all trigger conditions"""
        
        if not self.conditions:
            return True
        
        # All conditions must be true (AND logic)
        for condition in self.conditions:
            if not condition.evaluate(data, context):
                return False
        
        return True
    
    async def execute(self, data: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute trigger actions"""
        
        if not self.can_execute(context):
            return []
        
        if not self.evaluate_conditions(data, context):
            return []
        
        # Execute all actions
        results = []
        for action in self.actions:
            try:
                result = await action.execute(context)
                results.append({
                    "trigger_id": self.trigger_id,
                    "action_type": action.action_type.value,
                    "result": result,
                    "executed_at": datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Action execution failed: {e}")
                results.append({
                    "trigger_id": self.trigger_id,
                    "action_type": action.action_type.value,
                    "result": {"status": "error", "message": str(e)},
                    "executed_at": datetime.now().isoformat()
                })
        
        # Update execution state
        self.execution_count += 1
        self.last_execution = datetime.now()
        
        return results

class TriggerEngine:
    """Main trigger engine for processing behavioral events"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.triggers: List[Trigger] = []
        self.trigger_stats = {
            "total_triggers": 0,
            "active_triggers": 0,
            "executions_today": 0,
            "success_rate": 1.0
        }
    
    async def initialize(self):
        """Initialize trigger engine and load triggers"""
        await self.load_triggers_from_database()
        logger.info(f"Trigger engine initialized with {len(self.triggers)} triggers")
    
    async def load_triggers_from_database(self):
        """Load triggers from database"""
        try:
            # This would load from database in production
            # For now, create some default triggers
            await self._create_default_triggers()
        except Exception as e:
            logger.error(f"Failed to load triggers: {e}")
    
    async def _create_default_triggers(self):
        """Create default behavioral triggers"""
        
        # Exit intent trigger
        exit_intent_trigger = Trigger(
            trigger_id="exit_intent_popup",
            name="Exit Intent Popup",
            trigger_type=TriggerType.IMMEDIATE,
            conditions=[
                TriggerCondition("event_type", "eq", "exit_intent")
            ],
            actions=[
                TriggerAction(
                    ActionType.POPUP,
                    {
                        "popup_type": "exit_intent",
                        "content": "Wait! Don't leave yet. Get 20% off your first order.",
                        "discount_code": "SAVE20"
                    }
                )
            ],
            max_executions=1,
            cooldown_seconds=3600  # 1 hour cooldown
        )
        
        # High engagement trigger
        high_engagement_trigger = Trigger(
            trigger_id="high_engagement_offer",
            name="High Engagement Offer",
            trigger_type=TriggerType.THRESHOLD,
            conditions=[
                TriggerCondition("engagement_score", "gte", 0.8),
                TriggerCondition("time_on_page", "gt", 120000)  # 2 minutes
            ],
            actions=[
                TriggerAction(
                    ActionType.POPUP,
                    {
                        "popup_type": "special_offer",
                        "content": "You seem really interested! Here's an exclusive offer just for you.",
                        "discount_code": "EXCLUSIVE15"
                    },
                    delay_seconds=30
                )
            ],
            max_executions=1,
            cooldown_seconds=86400  # 24 hours
        )
        
        # Cart abandonment trigger
        cart_abandonment_trigger = Trigger(
            trigger_id="cart_abandonment",
            name="Cart Abandonment Recovery",
            trigger_type=TriggerType.DELAYED,
            conditions=[
                TriggerCondition("event_type", "eq", "cart_addition"),
                TriggerCondition("page_url", "contains", "checkout")
            ],
            actions=[
                TriggerAction(
                    ActionType.EMAIL,
                    {
                        "template": "cart_abandonment",
                        "subject": "Complete your purchase and save 10%",
                        "discount_code": "COMPLETE10"
                    },
                    delay_seconds=1800  # 30 minutes
                )
            ]
        )
        
        # Mobile user personalization
        mobile_personalization_trigger = Trigger(
            trigger_id="mobile_personalization",
            name="Mobile User Personalization",
            trigger_type=TriggerType.IMMEDIATE,
            conditions=[
                TriggerCondition("device_type", "eq", "mobile"),
                TriggerCondition("event_type", "eq", "page_view")
            ],
            actions=[
                TriggerAction(
                    ActionType.PERSONALIZATION,
                    {
                        "changes": {
                            "layout": "mobile_optimized",
                            "cta_size": "large",
                            "form_style": "simplified"
                        }
                    }
                )
            ],
            max_executions=1
        )
        
        # Add triggers to engine
        self.triggers.extend([
            exit_intent_trigger,
            high_engagement_trigger,
            cart_abandonment_trigger,
            mobile_personalization_trigger
        ])
        
        # Update stats
        self.trigger_stats["total_triggers"] = len(self.triggers)
        self.trigger_stats["active_triggers"] = len([
            t for t in self.triggers if t.status == TriggerStatus.ACTIVE
        ])
    
    async def check_behavioral_triggers(self, event_data: Any, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check and execute relevant triggers for behavioral event"""
        
        # Convert event data to dict for processing
        if hasattr(event_data, 'dict'):
            event_dict = event_data.dict()
        else:
            event_dict = event_data
        
        # Create context
        context = {
            "session_id": event_dict.get("session_id"),
            "user_id": event_dict.get("user_id"),
            "timestamp": datetime.now().isoformat(),
            "insights": insights
        }
        
        # Combine event data and insights
        trigger_data = {**event_dict, **insights}
        
        # Sort triggers by priority (higher first)
        sorted_triggers = sorted(self.triggers, key=lambda t: t.priority, reverse=True)
        
        all_results = []
        
        for trigger in sorted_triggers:
            try:
                results = await trigger.execute(trigger_data, context)
                all_results.extend(results)
                
                # Log successful executions
                if results:
                    logger.info(f"Trigger '{trigger.name}' executed with {len(results)} actions")
                    
            except Exception as e:
                logger.error(f"Trigger execution failed for '{trigger.name}': {e}")
        
        # Update stats
        if all_results:
            self.trigger_stats["executions_today"] += len(all_results)
        
        return all_results
    
    def add_trigger(self, trigger: Trigger):
        """Add a new trigger to the engine"""
        
        self.triggers.append(trigger)
        self.trigger_stats["total_triggers"] = len(self.triggers)
        self.trigger_stats["active_triggers"] = len([
            t for t in self.triggers if t.status == TriggerStatus.ACTIVE
        ])
        
        logger.info(f"Added trigger: {trigger.name}")
    
    def remove_trigger(self, trigger_id: str) -> bool:
        """Remove a trigger from the engine"""
        
        for i, trigger in enumerate(self.triggers):
            if trigger.trigger_id == trigger_id:
                removed_trigger = self.triggers.pop(i)
                logger.info(f"Removed trigger: {removed_trigger.name}")
                
                # Update stats
                self.trigger_stats["total_triggers"] = len(self.triggers)
                self.trigger_stats["active_triggers"] = len([
                    t for t in self.triggers if t.status == TriggerStatus.ACTIVE
                ])
                
                return True
        
        return False
    
    def get_trigger_stats(self) -> Dict[str, Any]:
        """Get trigger engine statistics"""
        
        return {
            **self.trigger_stats,
            "triggers_by_status": {
                status.value: len([t for t in self.triggers if t.status == status])
                for status in TriggerStatus
            },
            "triggers_by_type": {
                trigger_type.value: len([t for t in self.triggers if t.trigger_type == trigger_type])
                for trigger_type in TriggerType
            },
            "last_updated": datetime.now().isoformat()
        }
    
    async def cleanup_expired_triggers(self):
        """Clean up expired or inactive triggers"""
        
        before_count = len(self.triggers)
        
        # Remove expired triggers
        self.triggers = [
            t for t in self.triggers 
            if t.status != TriggerStatus.EXPIRED
        ]
        
        after_count = len(self.triggers)
        
        if before_count != after_count:
            logger.info(f"Cleaned up {before_count - after_count} expired triggers")
            
            # Update stats
            self.trigger_stats["total_triggers"] = after_count
            self.trigger_stats["active_triggers"] = len([
                t for t in self.triggers if t.status == TriggerStatus.ACTIVE
            ])