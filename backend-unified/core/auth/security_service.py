#!/usr/bin/env python3
"""
Security Service Implementation
Advanced security hardening and anomaly detection

Executor: Claude Code
Erstellt: 2025-07-03
"""

import hashlib
import hmac
import secrets
import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import logging
import asyncio
from ipaddress import ip_address, ip_network

from config.settings import settings

logger = logging.getLogger(__name__)

class SecurityLevel(str, Enum):
    """Security risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(str, Enum):
    """Types of security threats"""
    BRUTE_FORCE = "brute_force"
    SUSPICIOUS_LOCATION = "suspicious_location"
    UNUSUAL_ACTIVITY = "unusual_activity"
    MULTIPLE_FAILURES = "multiple_failures"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    MALICIOUS_PAYLOAD = "malicious_payload"
    UNAUTHORIZED_ACCESS = "unauthorized_access"

@dataclass
class SecurityEvent:
    """Security event data structure"""
    user_id: str
    event_type: ThreatType
    severity: SecurityLevel
    ip_address: str
    user_agent: str
    timestamp: datetime
    details: Dict[str, any]
    action_taken: Optional[str] = None

@dataclass
class SecurityMetrics:
    """Security metrics for a user"""
    failed_login_attempts: int = 0
    suspicious_locations: int = 0
    unusual_activity_score: float = 0.0
    last_security_event: Optional[datetime] = None
    is_blocked: bool = False
    block_until: Optional[datetime] = None

class SecurityService:
    """Comprehensive security service with threat detection"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.security_prefix = "security:"
        self.blocked_ips: Set[str] = set()
        self.suspicious_patterns = self._load_suspicious_patterns()
        
    async def initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info("✅ Security Service Redis connection established")
        except Exception as e:
            logger.error(f"❌ Security Service Redis connection failed: {e}")
            raise
    
    async def analyze_login_attempt(
        self,
        user_id: str,
        ip_address: str,
        user_agent: str,
        success: bool,
        additional_context: Optional[Dict] = None
    ) -> SecurityEvent:
        """Analyze login attempt for security threats"""
        
        if not self.redis_client:
            await self.initialize_redis()
        
        try:
            # Get current security metrics
            metrics = await self._get_security_metrics(user_id)
            
            # Check IP reputation
            ip_reputation = await self._check_ip_reputation(ip_address)
            
            # Check for brute force attempts
            brute_force_risk = await self._check_brute_force(user_id, ip_address, success)
            
            # Check for suspicious location
            location_risk = await self._check_suspicious_location(user_id, ip_address)
            
            # Check user agent for anomalies
            ua_risk = await self._check_user_agent_anomalies(user_id, user_agent)
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(
                ip_reputation, brute_force_risk, location_risk, ua_risk
            )
            
            # Determine security level
            security_level = self._determine_security_level(risk_score)
            
            # Create security event
            event = SecurityEvent(
                user_id=user_id,
                event_type=ThreatType.BRUTE_FORCE if brute_force_risk > 0.7 else ThreatType.UNUSUAL_ACTIVITY,
                severity=security_level,
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.utcnow(),
                details={
                    "success": success,
                    "risk_score": risk_score,
                    "ip_reputation": ip_reputation,
                    "brute_force_risk": brute_force_risk,
                    "location_risk": location_risk,
                    "ua_risk": ua_risk,
                    "additional_context": additional_context or {}
                }
            )
            
            # Take action based on security level
            action = await self._take_security_action(event, metrics)
            event.action_taken = action
            
            # Log security event
            await self._log_security_event(event)
            
            # Update security metrics
            await self._update_security_metrics(user_id, event, success)
            
            return event
            
        except Exception as e:
            logger.error(f"❌ Security analysis error: {e}")
            # Return minimal event on error
            return SecurityEvent(
                user_id=user_id,
                event_type=ThreatType.UNUSUAL_ACTIVITY,
                severity=SecurityLevel.LOW,
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.utcnow(),
                details={"error": str(e)}
            )
    
    async def check_request_security(
        self,
        user_id: str,
        ip_address: str,
        endpoint: str,
        payload: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Tuple[bool, Optional[SecurityEvent]]:
        """Check if request is secure and should be allowed"""
        
        try:
            # Check if IP is blocked
            if await self._is_ip_blocked(ip_address):
                event = SecurityEvent(
                    user_id=user_id,
                    event_type=ThreatType.UNAUTHORIZED_ACCESS,
                    severity=SecurityLevel.HIGH,
                    ip_address=ip_address,
                    user_agent=headers.get("User-Agent", "Unknown") if headers else "Unknown",
                    timestamp=datetime.utcnow(),
                    details={"endpoint": endpoint, "reason": "blocked_ip"}
                )
                return False, event
            
            # Check if user is blocked
            if await self._is_user_blocked(user_id):
                event = SecurityEvent(
                    user_id=user_id,
                    event_type=ThreatType.UNAUTHORIZED_ACCESS,
                    severity=SecurityLevel.HIGH,
                    ip_address=ip_address,
                    user_agent=headers.get("User-Agent", "Unknown") if headers else "Unknown",
                    timestamp=datetime.utcnow(),
                    details={"endpoint": endpoint, "reason": "blocked_user"}
                )
                return False, event
            
            # Check for malicious payload
            if payload and await self._check_malicious_payload(payload):
                event = SecurityEvent(
                    user_id=user_id,
                    event_type=ThreatType.MALICIOUS_PAYLOAD,
                    severity=SecurityLevel.HIGH,
                    ip_address=ip_address,
                    user_agent=headers.get("User-Agent", "Unknown") if headers else "Unknown",
                    timestamp=datetime.utcnow(),
                    details={"endpoint": endpoint, "payload_size": len(str(payload))}
                )
                return False, event
            
            # Check for suspicious headers
            if headers and await self._check_suspicious_headers(headers):
                event = SecurityEvent(
                    user_id=user_id,
                    event_type=ThreatType.UNUSUAL_ACTIVITY,
                    severity=SecurityLevel.MEDIUM,
                    ip_address=ip_address,
                    user_agent=headers.get("User-Agent", "Unknown"),
                    timestamp=datetime.utcnow(),
                    details={"endpoint": endpoint, "suspicious_headers": True}
                )
                return True, event  # Allow but log
            
            return True, None
            
        except Exception as e:
            logger.error(f"❌ Request security check error: {e}")
            return True, None  # Fail open
    
    async def block_ip(self, ip_address: str, reason: str, duration_minutes: int = 60):
        """Block IP address for specified duration"""
        
        try:
            block_key = f"{self.security_prefix}blocked_ip:{ip_address}"
            block_data = {
                "reason": reason,
                "blocked_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(minutes=duration_minutes)).isoformat()
            }
            
            await self.redis_client.setex(
                block_key,
                duration_minutes * 60,
                json.dumps(block_data)
            )
            
            self.blocked_ips.add(ip_address)
            
            logger.warning(f"🚫 IP blocked: {ip_address} (reason: {reason}, duration: {duration_minutes}min)")
            
        except Exception as e:
            logger.error(f"❌ Error blocking IP: {e}")
    
    async def block_user(self, user_id: str, reason: str, duration_minutes: int = 60):
        """Block user for specified duration"""
        
        try:
            block_key = f"{self.security_prefix}blocked_user:{user_id}"
            block_data = {
                "reason": reason,
                "blocked_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(minutes=duration_minutes)).isoformat()
            }
            
            await self.redis_client.setex(
                block_key,
                duration_minutes * 60,
                json.dumps(block_data)
            )
            
            logger.warning(f"🚫 User blocked: {user_id} (reason: {reason}, duration: {duration_minutes}min)")
            
        except Exception as e:
            logger.error(f"❌ Error blocking user: {e}")
    
    async def get_security_dashboard(self, user_id: Optional[str] = None) -> Dict[str, any]:
        """Get security dashboard data"""
        
        try:
            # Get recent security events
            events = await self._get_recent_security_events(limit=50, user_id=user_id)
            
            # Get blocked IPs
            blocked_ips = await self._get_blocked_ips()
            
            # Get security metrics
            if user_id:
                metrics = await self._get_security_metrics(user_id)
                user_metrics = metrics.__dict__
            else:
                user_metrics = None
            
            # Calculate security statistics
            stats = await self._calculate_security_stats(events)
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "recent_events": [
                    {
                        "user_id": event.user_id,
                        "event_type": event.event_type,
                        "severity": event.severity,
                        "ip_address": event.ip_address,
                        "timestamp": event.timestamp.isoformat(),
                        "details": event.details
                    } for event in events
                ],
                "blocked_ips": blocked_ips,
                "user_metrics": user_metrics,
                "statistics": stats
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting security dashboard: {e}")
            return {}
    
    def _load_suspicious_patterns(self) -> Dict[str, List[str]]:
        """Load suspicious patterns for detection"""
        return {
            "sql_injection": [
                "union select", "drop table", "insert into", "delete from",
                "update set", "alter table", "create table", "exec(",
                "execute(", "sp_", "xp_", "@@version"
            ],
            "xss": [
                "<script", "javascript:", "onload=", "onerror=", "onclick=",
                "onmouseover=", "alert(", "document.cookie", "window.location"
            ],
            "path_traversal": [
                "../", "..\\", "..\\/", "..%2f", "..%5c", "/etc/passwd",
                "/windows/system32", "c:\\windows", "boot.ini"
            ],
            "command_injection": [
                "; ls", "| ls", "& ls", ";cat", "|cat", "&cat", "$(", "`",
                "nc ", "netcat", "wget ", "curl ", "bash", "sh "
            ]
        }
    
    async def _get_security_metrics(self, user_id: str) -> SecurityMetrics:
        """Get security metrics for user"""
        
        try:
            metrics_key = f"{self.security_prefix}metrics:{user_id}"
            metrics_data = await self.redis_client.get(metrics_key)
            
            if metrics_data:
                data = json.loads(metrics_data)
                return SecurityMetrics(
                    failed_login_attempts=data.get("failed_login_attempts", 0),
                    suspicious_locations=data.get("suspicious_locations", 0),
                    unusual_activity_score=data.get("unusual_activity_score", 0.0),
                    last_security_event=datetime.fromisoformat(data["last_security_event"]) if data.get("last_security_event") else None,
                    is_blocked=data.get("is_blocked", False),
                    block_until=datetime.fromisoformat(data["block_until"]) if data.get("block_until") else None
                )
            
            return SecurityMetrics()
            
        except Exception as e:
            logger.error(f"❌ Error getting security metrics: {e}")
            return SecurityMetrics()
    
    async def _check_ip_reputation(self, ip_address: str) -> float:
        """Check IP reputation (0.0 = good, 1.0 = bad)"""
        
        try:
            # Check against known bad IP ranges
            bad_ranges = [
                "10.0.0.0/8",      # Private networks (can be suspicious in some contexts)
                "127.0.0.0/8",     # Loopback
                "169.254.0.0/16",  # Link-local
                "192.168.0.0/16",  # Private
                "172.16.0.0/12"    # Private
            ]
            
            ip = ip_address(ip_address)
            
            # Check if IP is in suspicious ranges
            for bad_range in bad_ranges:
                if ip in ip_network(bad_range):
                    return 0.3  # Mild suspicion for private IPs
            
            # Check Redis cache for IP reputation
            reputation_key = f"{self.security_prefix}ip_reputation:{ip_address}"
            reputation_data = await self.redis_client.get(reputation_key)
            
            if reputation_data:
                data = json.loads(reputation_data)
                return data.get("reputation_score", 0.0)
            
            # Default reputation for unknown IPs
            return 0.1
            
        except Exception as e:
            logger.error(f"❌ Error checking IP reputation: {e}")
            return 0.0
    
    async def _check_brute_force(self, user_id: str, ip_address: str, success: bool) -> float:
        """Check for brute force attack patterns"""
        
        try:
            # Check failed attempts in last 15 minutes
            failed_key = f"{self.security_prefix}failed_attempts:{user_id}:{ip_address}"
            failed_count = await self.redis_client.get(failed_key)
            failed_count = int(failed_count) if failed_count else 0
            
            if not success:
                # Increment failed attempts
                await self.redis_client.incr(failed_key)
                await self.redis_client.expire(failed_key, 900)  # 15 minutes
                failed_count += 1
            else:
                # Reset failed attempts on success
                await self.redis_client.delete(failed_key)
            
            # Calculate brute force risk
            if failed_count >= 10:
                return 1.0  # High risk
            elif failed_count >= 5:
                return 0.7  # Medium-high risk
            elif failed_count >= 3:
                return 0.4  # Medium risk
            elif failed_count >= 1:
                return 0.2  # Low risk
            
            return 0.0
            
        except Exception as e:
            logger.error(f"❌ Error checking brute force: {e}")
            return 0.0
    
    async def _check_suspicious_location(self, user_id: str, ip_address: str) -> float:
        """Check for suspicious login location"""
        
        try:
            # Get user's known locations
            locations_key = f"{self.security_prefix}locations:{user_id}"
            known_locations = await self.redis_client.smembers(locations_key)
            
            # Simplified location check (in production, use IP geolocation service)
            ip_prefix = ".".join(ip_address.split(".")[:2])  # First two octets
            
            if not known_locations:
                # First time seeing this user, add location
                await self.redis_client.sadd(locations_key, ip_prefix)
                await self.redis_client.expire(locations_key, 86400 * 30)  # 30 days
                return 0.1  # Low risk for new users
            
            if ip_prefix in known_locations:
                return 0.0  # Known location
            
            # New location detected
            await self.redis_client.sadd(locations_key, ip_prefix)
            return 0.5  # Medium risk for new location
            
        except Exception as e:
            logger.error(f"❌ Error checking suspicious location: {e}")
            return 0.0
    
    async def _check_user_agent_anomalies(self, user_id: str, user_agent: str) -> float:
        """Check for user agent anomalies"""
        
        try:
            # Get user's known user agents
            ua_key = f"{self.security_prefix}user_agents:{user_id}"
            known_agents = await self.redis_client.smembers(ua_key)
            
            # Create simplified user agent signature
            ua_signature = self._create_ua_signature(user_agent)
            
            if not known_agents:
                # First time, add user agent
                await self.redis_client.sadd(ua_key, ua_signature)
                await self.redis_client.expire(ua_key, 86400 * 30)  # 30 days
                return 0.1
            
            if ua_signature in known_agents:
                return 0.0  # Known user agent
            
            # Check for suspicious patterns
            suspicious_keywords = ["bot", "crawler", "spider", "scan", "hack", "test"]
            user_agent_lower = user_agent.lower()
            
            for keyword in suspicious_keywords:
                if keyword in user_agent_lower:
                    return 0.8  # High risk for suspicious keywords
            
            # New user agent
            await self.redis_client.sadd(ua_key, ua_signature)
            return 0.3  # Medium risk for new user agent
            
        except Exception as e:
            logger.error(f"❌ Error checking user agent anomalies: {e}")
            return 0.0
    
    def _create_ua_signature(self, user_agent: str) -> str:
        """Create simplified user agent signature"""
        # Extract browser and OS info
        ua_lower = user_agent.lower()
        
        browser = "unknown"
        if "chrome" in ua_lower:
            browser = "chrome"
        elif "firefox" in ua_lower:
            browser = "firefox"
        elif "safari" in ua_lower:
            browser = "safari"
        elif "edge" in ua_lower:
            browser = "edge"
        
        os = "unknown"
        if "windows" in ua_lower:
            os = "windows"
        elif "mac" in ua_lower:
            os = "mac"
        elif "linux" in ua_lower:
            os = "linux"
        elif "android" in ua_lower:
            os = "android"
        elif "ios" in ua_lower:
            os = "ios"
        
        return f"{browser}_{os}"
    
    def _calculate_risk_score(self, *risks: float) -> float:
        """Calculate overall risk score from individual risks"""
        # Weighted average of risks
        weights = [0.3, 0.3, 0.2, 0.2]  # Adjust weights as needed
        weighted_sum = sum(risk * weight for risk, weight in zip(risks, weights))
        return min(weighted_sum, 1.0)
    
    def _determine_security_level(self, risk_score: float) -> SecurityLevel:
        """Determine security level from risk score"""
        if risk_score >= 0.8:
            return SecurityLevel.CRITICAL
        elif risk_score >= 0.6:
            return SecurityLevel.HIGH
        elif risk_score >= 0.3:
            return SecurityLevel.MEDIUM
        else:
            return SecurityLevel.LOW
    
    async def _take_security_action(self, event: SecurityEvent, metrics: SecurityMetrics) -> str:
        """Take appropriate security action based on event"""
        
        try:
            if event.severity == SecurityLevel.CRITICAL:
                # Block IP and user
                await self.block_ip(event.ip_address, f"Critical security event: {event.event_type}", 240)
                await self.block_user(event.user_id, f"Critical security event: {event.event_type}", 60)
                return "blocked_ip_and_user"
            
            elif event.severity == SecurityLevel.HIGH:
                # Block IP temporarily
                await self.block_ip(event.ip_address, f"High security event: {event.event_type}", 60)
                return "blocked_ip"
            
            elif event.severity == SecurityLevel.MEDIUM:
                # Increase monitoring
                return "increased_monitoring"
            
            else:
                # Log only
                return "logged_only"
                
        except Exception as e:
            logger.error(f"❌ Error taking security action: {e}")
            return "error"
    
    async def _log_security_event(self, event: SecurityEvent):
        """Log security event to Redis"""
        
        try:
            event_key = f"{self.security_prefix}events:{event.user_id}:{int(event.timestamp.timestamp())}"
            event_data = {
                "user_id": event.user_id,
                "event_type": event.event_type,
                "severity": event.severity,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "timestamp": event.timestamp.isoformat(),
                "details": event.details,
                "action_taken": event.action_taken
            }
            
            await self.redis_client.setex(
                event_key,
                86400 * 7,  # Keep for 7 days
                json.dumps(event_data)
            )
            
            # Add to global events list
            await self.redis_client.lpush(
                f"{self.security_prefix}events_list",
                json.dumps(event_data)
            )
            await self.redis_client.ltrim(f"{self.security_prefix}events_list", 0, 999)  # Keep last 1000 events
            
        except Exception as e:
            logger.error(f"❌ Error logging security event: {e}")
    
    async def _update_security_metrics(self, user_id: str, event: SecurityEvent, login_success: bool):
        """Update security metrics for user"""
        
        try:
            metrics = await self._get_security_metrics(user_id)
            
            if not login_success:
                metrics.failed_login_attempts += 1
            else:
                metrics.failed_login_attempts = 0
            
            if event.severity in [SecurityLevel.HIGH, SecurityLevel.CRITICAL]:
                metrics.unusual_activity_score = min(metrics.unusual_activity_score + 0.1, 1.0)
            
            metrics.last_security_event = event.timestamp
            
            # Save updated metrics
            metrics_key = f"{self.security_prefix}metrics:{user_id}"
            metrics_data = {
                "failed_login_attempts": metrics.failed_login_attempts,
                "suspicious_locations": metrics.suspicious_locations,
                "unusual_activity_score": metrics.unusual_activity_score,
                "last_security_event": metrics.last_security_event.isoformat() if metrics.last_security_event else None,
                "is_blocked": metrics.is_blocked,
                "block_until": metrics.block_until.isoformat() if metrics.block_until else None
            }
            
            await self.redis_client.setex(
                metrics_key,
                86400 * 30,  # Keep for 30 days
                json.dumps(metrics_data)
            )
            
        except Exception as e:
            logger.error(f"❌ Error updating security metrics: {e}")
    
    async def _is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP is blocked"""
        try:
            block_key = f"{self.security_prefix}blocked_ip:{ip_address}"
            return await self.redis_client.exists(block_key)
        except Exception as e:
            logger.error(f"❌ Error checking IP block: {e}")
            return False
    
    async def _is_user_blocked(self, user_id: str) -> bool:
        """Check if user is blocked"""
        try:
            block_key = f"{self.security_prefix}blocked_user:{user_id}"
            return await self.redis_client.exists(block_key)
        except Exception as e:
            logger.error(f"❌ Error checking user block: {e}")
            return False
    
    async def _check_malicious_payload(self, payload: Dict) -> bool:
        """Check if payload contains malicious content"""
        try:
            payload_str = json.dumps(payload).lower()
            
            # Check for suspicious patterns
            for category, patterns in self.suspicious_patterns.items():
                for pattern in patterns:
                    if pattern in payload_str:
                        logger.warning(f"🚨 Malicious payload detected: {category} - {pattern}")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error checking malicious payload: {e}")
            return False
    
    async def _check_suspicious_headers(self, headers: Dict) -> bool:
        """Check for suspicious HTTP headers"""
        try:
            suspicious_headers = {
                "x-forwarded-for": ["127.0.0.1", "localhost"],
                "x-real-ip": ["127.0.0.1", "localhost"],
                "user-agent": ["bot", "crawler", "spider", "scan"]
            }
            
            for header, suspicious_values in suspicious_headers.items():
                header_value = headers.get(header, "").lower()
                for suspicious_value in suspicious_values:
                    if suspicious_value in header_value:
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error checking suspicious headers: {e}")
            return False
    
    async def _get_recent_security_events(self, limit: int = 50, user_id: Optional[str] = None) -> List[SecurityEvent]:
        """Get recent security events"""
        try:
            events_list = await self.redis_client.lrange(f"{self.security_prefix}events_list", 0, limit - 1)
            
            events = []
            for event_json in events_list:
                try:
                    event_data = json.loads(event_json)
                    if user_id and event_data.get("user_id") != user_id:
                        continue
                    
                    event = SecurityEvent(
                        user_id=event_data["user_id"],
                        event_type=event_data["event_type"],
                        severity=event_data["severity"],
                        ip_address=event_data["ip_address"],
                        user_agent=event_data["user_agent"],
                        timestamp=datetime.fromisoformat(event_data["timestamp"]),
                        details=event_data["details"],
                        action_taken=event_data.get("action_taken")
                    )
                    events.append(event)
                except Exception as e:
                    logger.error(f"❌ Error parsing security event: {e}")
                    continue
            
            return events
            
        except Exception as e:
            logger.error(f"❌ Error getting recent security events: {e}")
            return []
    
    async def _get_blocked_ips(self) -> List[Dict]:
        """Get list of blocked IPs"""
        try:
            blocked_ips = []
            pattern = f"{self.security_prefix}blocked_ip:*"
            keys = await self.redis_client.keys(pattern)
            
            for key in keys:
                ip_address = key.replace(f"{self.security_prefix}blocked_ip:", "")
                block_data = await self.redis_client.get(key)
                if block_data:
                    data = json.loads(block_data)
                    blocked_ips.append({
                        "ip_address": ip_address,
                        "reason": data.get("reason"),
                        "blocked_at": data.get("blocked_at"),
                        "expires_at": data.get("expires_at")
                    })
            
            return blocked_ips
            
        except Exception as e:
            logger.error(f"❌ Error getting blocked IPs: {e}")
            return []
    
    async def _calculate_security_stats(self, events: List[SecurityEvent]) -> Dict:
        """Calculate security statistics"""
        try:
            stats = {
                "total_events": len(events),
                "by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
                "by_type": {},
                "unique_users": set(),
                "unique_ips": set()
            }
            
            for event in events:
                stats["by_severity"][event.severity] += 1
                stats["by_type"][event.event_type] = stats["by_type"].get(event.event_type, 0) + 1
                stats["unique_users"].add(event.user_id)
                stats["unique_ips"].add(event.ip_address)
            
            stats["unique_users"] = len(stats["unique_users"])
            stats["unique_ips"] = len(stats["unique_ips"])
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error calculating security stats: {e}")
            return {}


class SecurityHardening:
    """Security hardening utilities"""
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use PBKDF2 with SHA-256
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return key.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash"""
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return key.hex() == hashed_password
    
    @staticmethod
    def create_hmac_signature(data: str, secret: str) -> str:
        """Create HMAC signature"""
        return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()
    
    @staticmethod
    def verify_hmac_signature(data: str, signature: str, secret: str) -> bool:
        """Verify HMAC signature"""
        expected_signature = hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input"""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript', 'onload', 'onerror']
        sanitized = input_str
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()

# Global security service instance
security_service = SecurityService()