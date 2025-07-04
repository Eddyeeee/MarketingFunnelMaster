"""
Real-Time Behavioral Tracking API Controller
Module: 2C - Conversion & Marketing Automation
Created: 2024-07-04

Advanced behavioral tracking with WebSocket streaming, cross-device continuity,
and real-time trigger automation for conversion optimization.
"""

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import uuid
import json
import asyncio
import logging
from enum import Enum

from ...database.connection import get_database_connection
from ...services.websocket_manager import WebSocketManager
from ...services.trigger_engine import TriggerEngine
from ...models.behavioral_models import (
    BehavioralEvent,
    BehavioralInsights,
    TriggerResponse,
    EngagementMetrics
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/behavioral", tags=["behavioral-tracking"])

# WebSocket Manager for real-time streaming
websocket_manager = WebSocketManager()

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class EventType(str, Enum):
    PAGE_VIEW = "page_view"
    SCROLL = "scroll"
    CLICK = "click"
    HOVER = "hover"
    FORM_INTERACTION = "form_interaction"
    PURCHASE = "purchase"
    EXIT_INTENT = "exit_intent"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    CONVERSION = "conversion"
    ENGAGEMENT_THRESHOLD = "engagement_threshold"
    TIME_MILESTONE = "time_milestone"
    CUSTOM = "custom"

class EventCategory(str, Enum):
    NAVIGATION = "navigation"
    INTERACTION = "interaction"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    ERROR = "error"

class InteractionType(str, Enum):
    CLICK = "click"
    TOUCH = "touch"
    SWIPE = "swipe"
    SCROLL = "scroll"
    HOVER = "hover"
    FOCUS = "focus"
    BLUR = "blur"
    DRAG = "drag"
    PINCH = "pinch"
    ZOOM = "zoom"

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ElementPosition(BaseModel):
    x: int
    y: int
    width: Optional[int] = None
    height: Optional[int] = None

class ViewportInfo(BaseModel):
    width: int
    height: int
    device_pixel_ratio: Optional[float] = 1.0

class PerformanceMetrics(BaseModel):
    page_load_time: Optional[int] = None
    time_to_first_byte: Optional[int] = None
    dom_content_loaded: Optional[int] = None
    first_contentful_paint: Optional[int] = None

class BehavioralEventRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    user_id: Optional[str] = Field(None, max_length=100)
    
    # Event data
    event_type: EventType
    event_category: EventCategory
    event_action: str = Field(..., max_length=100)
    event_label: Optional[str] = Field(None, max_length=255)
    event_value: Optional[float] = None
    
    # Context data
    page_url: str = Field(..., max_length=2000)
    page_title: Optional[str] = Field(None, max_length=255)
    referrer: Optional[str] = Field(None, max_length=2000)
    user_agent: Optional[str] = Field(None, max_length=1000)
    viewport: Optional[ViewportInfo] = None
    
    # Interaction details
    element_id: Optional[str] = Field(None, max_length=100)
    element_class: Optional[str] = Field(None, max_length=255)
    element_text: Optional[str] = Field(None, max_length=1000)
    element_position: Optional[ElementPosition] = None
    interaction_type: Optional[InteractionType] = None
    interaction_duration: Optional[int] = None
    
    # Performance and engagement
    performance_metrics: Optional[PerformanceMetrics] = None
    time_on_page: Optional[int] = None
    scroll_depth: Optional[float] = Field(None, ge=0.0, le=1.0)
    engagement_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    # Custom properties
    custom_properties: Optional[Dict[str, Any]] = None
    
    # Timestamps
    client_timestamp: Optional[datetime] = None

class BehavioralEventResponse(BaseModel):
    event_id: str
    processed: bool
    processing_time_ms: int
    triggers_fired: List[Dict[str, Any]]
    insights: Optional[Dict[str, Any]] = None

class BehavioralInsightsRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    time_window_minutes: int = Field(default=30, ge=1, le=1440)  # Max 24 hours
    event_types: Optional[List[EventType]] = None
    include_predictions: bool = True

class BehavioralInsightsResponse(BaseModel):
    session_id: Optional[str]
    user_id: Optional[str]
    time_window: int
    
    # Behavioral patterns
    dominant_behavior_pattern: str
    engagement_level: str
    conversion_probability: float
    intent_signals: List[str]
    
    # Metrics
    total_events: int
    unique_pages: int
    session_duration: int
    avg_time_per_page: float
    scroll_completion_rate: float
    interaction_rate: float
    
    # Predictions
    next_action_prediction: Optional[Dict[str, Any]] = None
    optimal_intervention_timing: Optional[Dict[str, Any]] = None
    conversion_likelihood: Optional[Dict[str, Any]] = None

class RealTimeStreamRequest(BaseModel):
    session_id: str
    subscriptions: List[str] = Field(default=["behavioral_events", "engagement_metrics", "conversion_triggers"])

# =============================================================================
# BEHAVIORAL TRACKING SERVICE
# =============================================================================

class BehavioralTrackingService:
    """Core service for real-time behavioral tracking and analysis"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.trigger_engine = TriggerEngine(db_connection)
    
    async def process_behavioral_event(self, event: BehavioralEventRequest) -> BehavioralEventResponse:
        """Process incoming behavioral event and trigger automations"""
        
        start_time = datetime.now()
        event_id = str(uuid.uuid4())
        
        try:
            # 1. Store event in database
            await self._store_behavioral_event(event_id, event)
            
            # 2. Calculate real-time insights
            insights = await self._calculate_real_time_insights(event)
            
            # 3. Check for automation triggers
            triggers_fired = await self.trigger_engine.check_behavioral_triggers(event, insights)
            
            # 4. Update user engagement metrics
            await self._update_engagement_metrics(event, insights)
            
            # 5. Stream to WebSocket subscribers
            await self._stream_to_subscribers(event, insights, triggers_fired)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return BehavioralEventResponse(
                event_id=event_id,
                processed=True,
                processing_time_ms=int(processing_time),
                triggers_fired=triggers_fired,
                insights=insights
            )
            
        except Exception as e:
            logger.error(f"Behavioral event processing failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Event processing failed: {str(e)}")
    
    async def _store_behavioral_event(self, event_id: str, event: BehavioralEventRequest):
        """Store behavioral event in database"""
        
        query = """
        INSERT INTO behavioral_tracking_events (
            id, session_id, user_id, event_type, event_category, event_action, event_label, event_value,
            page_url, page_title, referrer, user_agent, viewport_width, viewport_height,
            element_id, element_class, element_text, element_position, interaction_type, interaction_duration,
            page_load_time, time_on_page, scroll_depth, engagement_score, custom_properties,
            event_timestamp, server_timestamp
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,
            $21, $22, $23, $24, $25, $26, CURRENT_TIMESTAMP
        )
        """
        
        viewport_width = event.viewport.width if event.viewport else None
        viewport_height = event.viewport.height if event.viewport else None
        page_load_time = event.performance_metrics.page_load_time if event.performance_metrics else None
        element_position_json = event.element_position.dict() if event.element_position else None
        
        await self.db.execute(
            query,
            event_id,
            event.session_id,
            event.user_id,
            event.event_type.value,
            event.event_category.value,
            event.event_action,
            event.event_label,
            event.event_value,
            event.page_url,
            event.page_title,
            event.referrer,
            event.user_agent,
            viewport_width,
            viewport_height,
            event.element_id,
            event.element_class,
            event.element_text,
            element_position_json,
            event.interaction_type.value if event.interaction_type else None,
            event.interaction_duration,
            page_load_time,
            event.time_on_page,
            event.scroll_depth,
            event.engagement_score,
            event.custom_properties,
            event.client_timestamp or datetime.now()
        )
    
    async def _calculate_real_time_insights(self, event: BehavioralEventRequest) -> Dict[str, Any]:
        """Calculate real-time behavioral insights"""
        
        # Get recent behavioral data for the session
        recent_events_query = """
        SELECT event_type, event_category, time_on_page, scroll_depth, engagement_score,
               event_timestamp, interaction_type
        FROM behavioral_tracking_events
        WHERE session_id = $1 
            AND event_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 minutes'
        ORDER BY event_timestamp DESC
        LIMIT 50
        """
        
        recent_events = await self.db.fetch(recent_events_query, event.session_id)
        
        # Calculate behavioral pattern
        behavior_pattern = self._analyze_behavior_pattern(recent_events, event)
        
        # Calculate engagement level
        engagement_level = self._calculate_engagement_level(recent_events, event)
        
        # Calculate conversion probability
        conversion_probability = self._calculate_conversion_probability(recent_events, event)
        
        # Predict next action
        next_action_prediction = self._predict_next_action(recent_events, event)
        
        return {
            "behavior_pattern": behavior_pattern,
            "engagement_level": engagement_level,
            "conversion_probability": conversion_probability,
            "next_action_prediction": next_action_prediction,
            "session_event_count": len(recent_events) + 1,
            "average_engagement": sum(e.get('engagement_score', 0) or 0 for e in recent_events) / max(len(recent_events), 1),
            "time_patterns": self._analyze_time_patterns(recent_events)
        }
    
    def _analyze_behavior_pattern(self, recent_events: List[Dict], current_event: BehavioralEventRequest) -> str:
        """Analyze user behavior pattern"""
        
        if not recent_events:
            return "new_session"
        
        # Count event types
        event_types = [e['event_type'] for e in recent_events]
        interaction_types = [e['interaction_type'] for e in recent_events if e['interaction_type']]
        
        # Analyze patterns
        if event_types.count('scroll') > len(event_types) * 0.4:
            if any('comparison' in str(e.get('page_url', '')) for e in recent_events):
                return "research_focused"
            else:
                return "content_scanner"
        
        elif event_types.count('click') > len(event_types) * 0.3:
            return "high_engagement"
        
        elif current_event.time_on_page and current_event.time_on_page > 180000:  # > 3 minutes
            return "deep_reader"
        
        elif 'swipe' in interaction_types or 'touch' in interaction_types:
            return "mobile_browser"
        
        else:
            return "standard_visitor"
    
    def _calculate_engagement_level(self, recent_events: List[Dict], current_event: BehavioralEventRequest) -> str:
        """Calculate engagement level"""
        
        if current_event.engagement_score:
            score = current_event.engagement_score
        else:
            # Calculate based on behavior
            scores = [e.get('engagement_score', 0.5) or 0.5 for e in recent_events]
            score = sum(scores) / max(len(scores), 1)
        
        if score >= 0.8:
            return "very_high"
        elif score >= 0.6:
            return "high"
        elif score >= 0.4:
            return "medium"
        elif score >= 0.2:
            return "low"
        else:
            return "very_low"
    
    def _calculate_conversion_probability(self, recent_events: List[Dict], current_event: BehavioralEventRequest) -> float:
        """Calculate conversion probability based on behavioral signals"""
        
        base_probability = 0.1  # 10% base rate
        
        # Engagement factor
        if current_event.engagement_score:
            engagement_factor = current_event.engagement_score * 0.3
        else:
            engagement_factor = 0.15
        
        # Time on page factor
        time_factor = 0
        if current_event.time_on_page:
            if current_event.time_on_page > 120000:  # > 2 minutes
                time_factor = 0.2
            elif current_event.time_on_page > 60000:  # > 1 minute
                time_factor = 0.1
        
        # Interaction depth factor
        interaction_factor = min(len(recent_events) * 0.02, 0.3)
        
        # Page depth factor
        unique_pages = len(set(e.get('page_url') for e in recent_events if e.get('page_url')))
        page_factor = min(unique_pages * 0.05, 0.2)
        
        # Conversion signals factor
        conversion_signals = 0
        if any('pricing' in str(e.get('page_url', '')) for e in recent_events):
            conversion_signals += 0.1
        if any('checkout' in str(e.get('page_url', '')) for e in recent_events):
            conversion_signals += 0.2
        if current_event.event_type == EventType.FORM_INTERACTION:
            conversion_signals += 0.15
        
        total_probability = base_probability + engagement_factor + time_factor + interaction_factor + page_factor + conversion_signals
        
        return min(total_probability, 0.95)  # Cap at 95%
    
    def _predict_next_action(self, recent_events: List[Dict], current_event: BehavioralEventRequest) -> Dict[str, Any]:
        """Predict user's next likely action"""
        
        # Analyze recent patterns
        recent_types = [e['event_type'] for e in recent_events[-5:]]  # Last 5 events
        
        predictions = {
            "action": "continue_browsing",
            "probability": 0.6,
            "timing": "within_30_seconds",
            "confidence": 0.7
        }
        
        # Pattern-based predictions
        if recent_types.count('scroll') >= 3:
            predictions.update({
                "action": "scroll_or_navigate",
                "probability": 0.8,
                "timing": "within_10_seconds"
            })
        
        elif current_event.event_type == EventType.EXIT_INTENT:
            predictions.update({
                "action": "leave_site",
                "probability": 0.9,
                "timing": "immediate"
            })
        
        elif 'pricing' in current_event.page_url:
            predictions.update({
                "action": "view_comparison_or_purchase",
                "probability": 0.7,
                "timing": "within_60_seconds"
            })
        
        elif current_event.engagement_score and current_event.engagement_score > 0.8:
            predictions.update({
                "action": "engage_with_content",
                "probability": 0.85,
                "timing": "within_15_seconds"
            })
        
        return predictions
    
    def _analyze_time_patterns(self, recent_events: List[Dict]) -> Dict[str, Any]:
        """Analyze timing patterns in user behavior"""
        
        if len(recent_events) < 2:
            return {"pattern": "insufficient_data"}
        
        # Calculate time intervals between events
        intervals = []
        for i in range(1, len(recent_events)):
            if recent_events[i-1]['event_timestamp'] and recent_events[i]['event_timestamp']:
                interval = (recent_events[i-1]['event_timestamp'] - recent_events[i]['event_timestamp']).total_seconds()
                intervals.append(abs(interval))
        
        if not intervals:
            return {"pattern": "no_time_data"}
        
        avg_interval = sum(intervals) / len(intervals)
        
        if avg_interval < 5:
            return {"pattern": "rapid_interaction", "avg_interval": avg_interval}
        elif avg_interval < 30:
            return {"pattern": "active_browsing", "avg_interval": avg_interval}
        elif avg_interval < 120:
            return {"pattern": "deliberate_reading", "avg_interval": avg_interval}
        else:
            return {"pattern": "slow_browsing", "avg_interval": avg_interval}
    
    async def _update_engagement_metrics(self, event: BehavioralEventRequest, insights: Dict[str, Any]):
        """Update real-time engagement metrics for the session"""
        
        # This would typically update a cache or real-time metrics store
        # For now, we'll log the metrics
        logger.info(f"Engagement metrics updated for session {event.session_id}: {insights}")
    
    async def _stream_to_subscribers(self, event: BehavioralEventRequest, insights: Dict[str, Any], triggers_fired: List[Dict[str, Any]]):
        """Stream behavioral data to WebSocket subscribers"""
        
        stream_data = {
            "type": "behavioral_event",
            "timestamp": datetime.now().isoformat(),
            "session_id": event.session_id,
            "event": {
                "type": event.event_type.value,
                "category": event.event_category.value,
                "action": event.event_action,
                "engagement_score": event.engagement_score,
                "conversion_probability": insights.get("conversion_probability", 0)
            },
            "insights": insights,
            "triggers": triggers_fired
        }
        
        await websocket_manager.broadcast_to_session(event.session_id, stream_data)
    
    async def get_behavioral_insights(self, request: BehavioralInsightsRequest) -> BehavioralInsightsResponse:
        """Get comprehensive behavioral insights for a session or user"""
        
        # Build query conditions
        conditions = []
        params = []
        param_count = 0
        
        if request.session_id:
            param_count += 1
            conditions.append(f"session_id = ${param_count}")
            params.append(request.session_id)
        
        if request.user_id:
            param_count += 1
            conditions.append(f"user_id = ${param_count}")
            params.append(request.user_id)
        
        param_count += 1
        conditions.append(f"event_timestamp >= CURRENT_TIMESTAMP - (${param_count} || ' minutes')::INTERVAL")
        params.append(request.time_window_minutes)
        
        if request.event_types:
            param_count += 1
            conditions.append(f"event_type = ANY(${param_count})")
            params.append([et.value for et in request.event_types])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # Get behavioral data
        query = f"""
        SELECT 
            event_type, event_category, event_action,
            time_on_page, scroll_depth, engagement_score,
            page_url, interaction_type, event_timestamp,
            COUNT(*) OVER() as total_events,
            COUNT(DISTINCT page_url) OVER() as unique_pages
        FROM behavioral_tracking_events
        WHERE {where_clause}
        ORDER BY event_timestamp DESC
        """
        
        events = await self.db.fetch(query, *params)
        
        if not events:
            raise HTTPException(status_code=404, detail="No behavioral data found")
        
        # Calculate insights
        insights = self._calculate_comprehensive_insights(events, request)
        
        return BehavioralInsightsResponse(**insights)
    
    def _calculate_comprehensive_insights(self, events: List[Dict], request: BehavioralInsightsRequest) -> Dict[str, Any]:
        """Calculate comprehensive behavioral insights"""
        
        if not events:
            return {"error": "No events to analyze"}
        
        total_events = events[0]['total_events']
        unique_pages = events[0]['unique_pages']
        
        # Calculate session duration
        if len(events) > 1:
            session_duration = (events[0]['event_timestamp'] - events[-1]['event_timestamp']).total_seconds()
        else:
            session_duration = 0
        
        # Calculate average time per page
        time_values = [e['time_on_page'] for e in events if e['time_on_page']]
        avg_time_per_page = sum(time_values) / len(time_values) if time_values else 0
        
        # Calculate scroll completion rate
        scroll_values = [e['scroll_depth'] for e in events if e['scroll_depth']]
        scroll_completion_rate = sum(scroll_values) / len(scroll_values) if scroll_values else 0
        
        # Calculate interaction rate
        interaction_events = [e for e in events if e['event_category'] == 'interaction']
        interaction_rate = len(interaction_events) / total_events if total_events > 0 else 0
        
        # Determine dominant behavior pattern
        event_types = [e['event_type'] for e in events]
        most_common_event = max(set(event_types), key=event_types.count) if event_types else 'unknown'
        
        behavior_patterns = {
            'scroll': 'content_scanner',
            'click': 'interactive_user',
            'page_view': 'navigator',
            'hover': 'explorer'
        }
        dominant_pattern = behavior_patterns.get(most_common_event, 'unknown')
        
        # Calculate engagement level
        engagement_scores = [e['engagement_score'] for e in events if e['engagement_score']]
        avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0.5
        
        if avg_engagement >= 0.8:
            engagement_level = "very_high"
        elif avg_engagement >= 0.6:
            engagement_level = "high"
        elif avg_engagement >= 0.4:
            engagement_level = "medium"
        else:
            engagement_level = "low"
        
        # Calculate conversion probability
        conversion_probability = self._calculate_conversion_probability(events, None)
        
        # Identify intent signals
        intent_signals = []
        page_urls = [e['page_url'] for e in events if e['page_url']]
        
        if any('pricing' in url for url in page_urls):
            intent_signals.append('pricing_interest')
        if any('features' in url for url in page_urls):
            intent_signals.append('feature_research')
        if any('comparison' in url for url in page_urls):
            intent_signals.append('comparison_shopping')
        if interaction_rate > 0.3:
            intent_signals.append('high_engagement')
        if avg_time_per_page > 120:
            intent_signals.append('deep_interest')
        
        insights = {
            "session_id": request.session_id,
            "user_id": request.user_id,
            "time_window": request.time_window_minutes,
            "dominant_behavior_pattern": dominant_pattern,
            "engagement_level": engagement_level,
            "conversion_probability": conversion_probability,
            "intent_signals": intent_signals,
            "total_events": total_events,
            "unique_pages": unique_pages,
            "session_duration": int(session_duration),
            "avg_time_per_page": avg_time_per_page / 1000 if avg_time_per_page else 0,  # Convert to seconds
            "scroll_completion_rate": scroll_completion_rate,
            "interaction_rate": interaction_rate
        }
        
        # Add predictions if requested
        if request.include_predictions:
            insights.update({
                "next_action_prediction": self._predict_next_action(events, None),
                "optimal_intervention_timing": {
                    "recommended_timing": "within_30_seconds" if conversion_probability > 0.6 else "within_2_minutes",
                    "intervention_type": "conversion_assist" if conversion_probability > 0.7 else "engagement_boost",
                    "confidence": 0.8
                },
                "conversion_likelihood": {
                    "probability": conversion_probability,
                    "factors": intent_signals,
                    "timeline": "within_24_hours" if conversion_probability > 0.5 else "within_week"
                }
            })
        
        return insights

# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post("/events", response_model=BehavioralEventResponse)
async def track_behavioral_event(
    event: BehavioralEventRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_database_connection)
):
    """
    Track behavioral event with real-time processing and automation triggering
    
    - Processes event in <50ms
    - Triggers real-time automations
    - Streams to WebSocket subscribers
    - Calculates engagement insights
    """
    
    service = BehavioralTrackingService(db)
    return await service.process_behavioral_event(event)

@router.post("/events/batch")
async def track_behavioral_events_batch(
    events: List[BehavioralEventRequest],
    background_tasks: BackgroundTasks,
    db=Depends(get_database_connection)
):
    """
    Track multiple behavioral events in batch for improved performance
    """
    
    if len(events) > 100:
        raise HTTPException(status_code=400, detail="Batch size limited to 100 events")
    
    service = BehavioralTrackingService(db)
    results = []
    
    for event in events:
        try:
            result = await service.process_behavioral_event(event)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process event in batch: {str(e)}")
            results.append({
                "event_id": None,
                "processed": False,
                "error": str(e)
            })
    
    return {
        "batch_size": len(events),
        "processed_count": sum(1 for r in results if r.get('processed', False)),
        "failed_count": sum(1 for r in results if not r.get('processed', False)),
        "results": results
    }

@router.get("/insights", response_model=BehavioralInsightsResponse)
async def get_behavioral_insights(
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    time_window_minutes: int = Field(default=30, ge=1, le=1440),
    include_predictions: bool = True,
    db=Depends(get_database_connection)
):
    """
    Get comprehensive behavioral insights and predictions
    
    - Analyzes behavior patterns
    - Calculates conversion probability
    - Provides next action predictions
    - Includes optimal intervention timing
    """
    
    if not session_id and not user_id:
        raise HTTPException(status_code=400, detail="Either session_id or user_id must be provided")
    
    request = BehavioralInsightsRequest(
        session_id=session_id,
        user_id=user_id,
        time_window_minutes=time_window_minutes,
        include_predictions=include_predictions
    )
    
    service = BehavioralTrackingService(db)
    return await service.get_behavioral_insights(request)

@router.websocket("/stream/{session_id}")
async def behavioral_stream(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time behavioral event streaming
    
    Streams:
    - Behavioral events as they occur
    - Real-time engagement metrics
    - Conversion triggers and automations
    - Behavioral insights and predictions
    """
    
    await websocket_manager.connect(websocket, session_id)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection_established",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "subscriptions": ["behavioral_events", "engagement_metrics", "conversion_triggers"]
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for client messages (heartbeat, subscription changes, etc.)
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "heartbeat":
                    await websocket.send_json({
                        "type": "heartbeat_response",
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif message.get("type") == "update_subscriptions":
                    # Handle subscription updates
                    new_subscriptions = message.get("subscriptions", [])
                    await websocket.send_json({
                        "type": "subscriptions_updated",
                        "subscriptions": new_subscriptions,
                        "timestamp": datetime.now().isoformat()
                    })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error for session {session_id}: {str(e)}")
                break
    
    finally:
        websocket_manager.disconnect(websocket, session_id)

@router.get("/analytics/engagement")
async def get_engagement_analytics(
    time_range_hours: int = Field(default=24, ge=1, le=168),
    group_by: str = Field(default="hour", regex="^(hour|day|device|event_type)$"),
    db=Depends(get_database_connection)
):
    """
    Get behavioral engagement analytics
    """
    
    if group_by == "hour":
        time_bucket = "DATE_TRUNC('hour', event_timestamp)"
    elif group_by == "day":
        time_bucket = "DATE_TRUNC('day', event_timestamp)"
    else:
        time_bucket = "DATE_TRUNC('hour', event_timestamp)"
    
    query = f"""
    SELECT 
        {time_bucket} as time_bucket,
        event_type,
        event_category,
        COUNT(*) as event_count,
        COUNT(DISTINCT session_id) as unique_sessions,
        ROUND(AVG(engagement_score), 3) as avg_engagement_score,
        ROUND(AVG(time_on_page / 1000.0), 2) as avg_time_on_page_seconds,
        ROUND(AVG(scroll_depth), 3) as avg_scroll_depth
    FROM behavioral_tracking_events
    WHERE event_timestamp >= CURRENT_TIMESTAMP - ($1 || ' hours')::INTERVAL
        AND engagement_score IS NOT NULL
    GROUP BY time_bucket, event_type, event_category
    ORDER BY time_bucket DESC, event_count DESC
    """
    
    rows = await db.fetch(query, time_range_hours)
    
    return {
        "time_range_hours": time_range_hours,
        "group_by": group_by,
        "analytics": [
            {
                "time_bucket": row['time_bucket'].isoformat(),
                "event_type": row['event_type'],
                "event_category": row['event_category'],
                "event_count": row['event_count'],
                "unique_sessions": row['unique_sessions'],
                "avg_engagement_score": float(row['avg_engagement_score'] or 0),
                "avg_time_on_page_seconds": float(row['avg_time_on_page_seconds'] or 0),
                "avg_scroll_depth": float(row['avg_scroll_depth'] or 0)
            }
            for row in rows
        ]
    }

@router.get("/patterns/{session_id}")
async def get_session_behavior_patterns(
    session_id: str,
    db=Depends(get_database_connection)
):
    """
    Get detailed behavior patterns for a specific session
    """
    
    query = """
    SELECT 
        event_type,
        event_category,
        event_action,
        page_url,
        interaction_type,
        time_on_page,
        scroll_depth,
        engagement_score,
        event_timestamp,
        element_id,
        element_class
    FROM behavioral_tracking_events
    WHERE session_id = $1
    ORDER BY event_timestamp ASC
    """
    
    events = await db.fetch(query, session_id)
    
    if not events:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Analyze patterns
    pattern_analysis = {
        "session_id": session_id,
        "total_events": len(events),
        "session_duration": (events[-1]['event_timestamp'] - events[0]['event_timestamp']).total_seconds() if len(events) > 1 else 0,
        "unique_pages": len(set(e['page_url'] for e in events if e['page_url'])),
        "event_timeline": [
            {
                "timestamp": event['event_timestamp'].isoformat(),
                "event_type": event['event_type'],
                "event_category": event['event_category'],
                "event_action": event['event_action'],
                "page_url": event['page_url'],
                "engagement_score": event['engagement_score'],
                "time_on_page": event['time_on_page'],
                "scroll_depth": event['scroll_depth']
            }
            for event in events
        ],
        "engagement_progression": [e['engagement_score'] for e in events if e['engagement_score']],
        "page_flow": [e['page_url'] for e in events if e['page_url']]
    }
    
    return pattern_analysis