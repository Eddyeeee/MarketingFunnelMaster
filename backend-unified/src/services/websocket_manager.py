"""
WebSocket Manager for Real-Time Communication
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Manages WebSocket connections for real-time behavioral tracking,
A/B test updates, and conversion optimization events.
"""

import json
import asyncio
from typing import Dict, List, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
import logging
from datetime import datetime
from collections import defaultdict
import uuid

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages WebSocket connections and real-time broadcasting"""
    
    def __init__(self):
        # Active connections by session ID
        self.connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
        # Subscription management
        self.subscriptions: Dict[WebSocket, Set[str]] = defaultdict(set)
        
        # Message queue for offline users
        self.message_queue: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Connection statistics
        self.stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "connection_errors": 0
        }
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: Optional[str] = None):
        """Accept and register a new WebSocket connection"""
        
        try:
            await websocket.accept()
            
            # Add to connections
            self.connections[session_id].add(websocket)
            
            # Store metadata
            self.connection_metadata[websocket] = {
                "session_id": session_id,
                "user_id": user_id,
                "connected_at": datetime.now(),
                "last_activity": datetime.now(),
                "message_count": 0
            }
            
            # Default subscriptions for behavioral tracking
            self.subscriptions[websocket] = {
                "behavioral_events",
                "engagement_metrics", 
                "conversion_triggers"
            }
            
            # Update statistics
            self.stats["total_connections"] += 1
            self.stats["active_connections"] = len(self._get_all_connections())
            
            logger.info(f"WebSocket connected: session={session_id}, user={user_id}")
            
            # Send queued messages for this session
            await self._send_queued_messages(websocket, session_id)
            
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            self.stats["connection_errors"] += 1
            raise
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove WebSocket connection"""
        
        try:
            # Remove from connections
            if session_id in self.connections:
                self.connections[session_id].discard(websocket)
                
                # Clean up empty session entries
                if not self.connections[session_id]:
                    del self.connections[session_id]
            
            # Remove metadata
            if websocket in self.connection_metadata:
                metadata = self.connection_metadata[websocket]
                logger.info(
                    f"WebSocket disconnected: session={session_id}, "
                    f"duration={datetime.now() - metadata['connected_at']}, "
                    f"messages={metadata['message_count']}"
                )
                del self.connection_metadata[websocket]
            
            # Remove subscriptions
            if websocket in self.subscriptions:
                del self.subscriptions[websocket]
            
            # Update statistics
            self.stats["active_connections"] = len(self._get_all_connections())
            
        except Exception as e:
            logger.error(f"WebSocket disconnect error: {e}")
    
    async def send_to_session(self, session_id: str, message: Dict[str, Any]) -> bool:
        """Send message to all connections for a specific session"""
        
        if session_id not in self.connections:
            # Queue message for when session connects
            self.message_queue[session_id].append({
                **message,
                "queued_at": datetime.now().isoformat()
            })
            return False
        
        success_count = 0
        connections_to_remove = []
        
        for websocket in self.connections[session_id].copy():
            try:
                await websocket.send_json(message)
                
                # Update metadata
                if websocket in self.connection_metadata:
                    self.connection_metadata[websocket]["last_activity"] = datetime.now()
                    self.connection_metadata[websocket]["message_count"] += 1
                
                success_count += 1
                self.stats["messages_sent"] += 1
                
            except WebSocketDisconnect:
                connections_to_remove.append(websocket)
            except Exception as e:
                logger.error(f"Failed to send message to WebSocket: {e}")
                connections_to_remove.append(websocket)
        
        # Clean up dead connections
        for websocket in connections_to_remove:
            self.disconnect(websocket, session_id)
        
        return success_count > 0
    
    async def broadcast_to_session(self, session_id: str, message: Dict[str, Any]):
        """Broadcast message to all connections for a session (alias for send_to_session)"""
        return await self.send_to_session(session_id, message)
    
    async def send_to_user(self, user_id: str, message: Dict[str, Any]) -> int:
        """Send message to all sessions for a specific user"""
        
        success_count = 0
        
        # Find all sessions for this user
        user_sessions = set()
        for websocket, metadata in self.connection_metadata.items():
            if metadata.get("user_id") == user_id:
                user_sessions.add(metadata["session_id"])
        
        # Send to all user sessions
        for session_id in user_sessions:
            if await self.send_to_session(session_id, message):
                success_count += 1
        
        return success_count
    
    async def broadcast_to_all(self, message: Dict[str, Any], 
                              subscription_filter: Optional[str] = None) -> int:
        """Broadcast message to all active connections"""
        
        success_count = 0
        
        for websocket in self._get_all_connections():
            try:
                # Check subscription filter
                if subscription_filter:
                    if subscription_filter not in self.subscriptions.get(websocket, set()):
                        continue
                
                await websocket.send_json(message)
                
                # Update metadata
                if websocket in self.connection_metadata:
                    self.connection_metadata[websocket]["last_activity"] = datetime.now()
                    self.connection_metadata[websocket]["message_count"] += 1
                
                success_count += 1
                self.stats["messages_sent"] += 1
                
            except WebSocketDisconnect:
                # Connection will be cleaned up by the disconnect handler
                pass
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
        
        return success_count
    
    async def send_behavioral_event(self, session_id: str, event_data: Dict[str, Any]):
        """Send behavioral event update to session"""
        
        message = {
            "type": "behavioral_event",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "data": event_data
        }
        
        return await self.send_to_session(session_id, message)
    
    async def send_ab_test_update(self, session_id: str, test_id: str, update_data: Dict[str, Any]):
        """Send A/B test update to session"""
        
        message = {
            "type": "ab_test_update",
            "timestamp": datetime.now().isoformat(),
            "test_id": test_id,
            "session_id": session_id,
            "data": update_data
        }
        
        return await self.send_to_session(session_id, message)
    
    async def send_conversion_trigger(self, session_id: str, trigger_data: Dict[str, Any]):
        """Send conversion trigger notification to session"""
        
        message = {
            "type": "conversion_trigger",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "data": trigger_data
        }
        
        return await self.send_to_session(session_id, message)
    
    def update_subscriptions(self, websocket: WebSocket, subscriptions: List[str]):
        """Update subscription preferences for a connection"""
        
        self.subscriptions[websocket] = set(subscriptions)
        
        if websocket in self.connection_metadata:
            logger.info(
                f"Updated subscriptions for session "
                f"{self.connection_metadata[websocket]['session_id']}: {subscriptions}"
            )
    
    def get_session_connections(self, session_id: str) -> int:
        """Get number of active connections for a session"""
        return len(self.connections.get(session_id, set()))
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        
        active_sessions = len(self.connections)
        total_active_connections = len(self._get_all_connections())
        
        # Calculate average connections per session
        avg_connections_per_session = (
            total_active_connections / active_sessions if active_sessions > 0 else 0
        )
        
        return {
            **self.stats,
            "active_sessions": active_sessions,
            "active_connections": total_active_connections,
            "avg_connections_per_session": round(avg_connections_per_session, 2),
            "queued_messages": sum(len(queue) for queue in self.message_queue.values()),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_all_connections(self) -> List[WebSocket]:
        """Get all active WebSocket connections"""
        
        all_connections = []
        for session_connections in self.connections.values():
            all_connections.extend(session_connections)
        return all_connections
    
    async def _send_queued_messages(self, websocket: WebSocket, session_id: str):
        """Send queued messages to newly connected session"""
        
        if session_id in self.message_queue:
            queued_messages = self.message_queue[session_id]
            
            for message in queued_messages:
                try:
                    await websocket.send_json(message)
                    self.stats["messages_sent"] += 1
                except Exception as e:
                    logger.error(f"Failed to send queued message: {e}")
                    break
            
            # Clear queue after sending
            del self.message_queue[session_id]
            
            if queued_messages:
                logger.info(f"Sent {len(queued_messages)} queued messages to session {session_id}")
    
    async def cleanup_stale_connections(self, max_idle_minutes: int = 30):
        """Clean up stale connections that haven't been active"""
        
        now = datetime.now()
        stale_connections = []
        
        for websocket, metadata in self.connection_metadata.items():
            idle_minutes = (now - metadata["last_activity"]).total_seconds() / 60
            
            if idle_minutes > max_idle_minutes:
                stale_connections.append((websocket, metadata["session_id"]))
        
        # Disconnect stale connections
        for websocket, session_id in stale_connections:
            try:
                await websocket.close(code=1000, reason="Connection idle timeout")
                self.disconnect(websocket, session_id)
            except Exception as e:
                logger.error(f"Error closing stale connection: {e}")
        
        if stale_connections:
            logger.info(f"Cleaned up {len(stale_connections)} stale connections")
    
    async def ping_all_connections(self):
        """Send ping to all connections to check health"""
        
        ping_message = {
            "type": "ping",
            "timestamp": datetime.now().isoformat()
        }
        
        dead_connections = []
        
        for websocket in self._get_all_connections():
            try:
                await websocket.send_json(ping_message)
            except Exception:
                # Mark as dead
                session_id = self.connection_metadata.get(websocket, {}).get("session_id")
                if session_id:
                    dead_connections.append((websocket, session_id))
        
        # Clean up dead connections
        for websocket, session_id in dead_connections:
            self.disconnect(websocket, session_id)
        
        if dead_connections:
            logger.info(f"Removed {len(dead_connections)} dead connections during ping")