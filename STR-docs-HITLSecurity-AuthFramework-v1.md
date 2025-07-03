# HITL-SECURITY-ENTSCHEIDUNGSVORLAGE: AUTHENTICATION & AUTHORIZATION FRAMEWORK

**Dokument ID:** STR-docs-HITLSecurity-AuthFramework-v1  
**Manager:** Claude Code (HTD-Manager-Ebene)  
**Erstellt:** 2025-07-03  
**Entscheidungstyp:** Security Architecture & Implementation  
**Genehmigung erforderlich:** Lead System Architect  

---

## 🎯 EXECUTIVE SUMMARY

**Kern-Empfehlung:** Multi-Tier Authentication & Authorization Framework mit JWT für User-Authentication und API Keys für Agent-to-Agent Communication, optimiert für das Multi-Millionen-Euro Digital Empire mit 1500+ Websites und 50+ AI Agents.

**Security-Ziele:**
- **Multi-Tier Authentication**: JWT (Users) + API Keys (Agents) + OAuth2 (External)
- **Zero-Trust Architecture**: Jede Anfrage authentifiziert und autorisiert
- **Agent-Integration**: Sichere Agent-zu-Agent-Kommunikation mit <50ms Latency
- **Scalable Security**: Support für 10,000+ concurrent requests mit Security-First

---

## 🔒 SECURITY ARCHITECTURE DESIGN

### **1. MULTI-TIER AUTHENTICATION LAYERS:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FRAMEWORK                     │
├─────────────────────────────────────────────────────────────────┤
│  🔐 Tier 1: User Authentication (Web Dashboard)                │
│  ├── JWT Tokens (24h expiry, refresh capability)               │
│  ├── Password + 2FA (TOTP/SMS optional)                        │
│  ├── OAuth2 Integration (Google, GitHub)                       │
│  └── Session Management with Redis                             │
├─────────────────────────────────────────────────────────────────┤
│  🤖 Tier 2: Agent Authentication (AI-to-AI)                    │
│  ├── API Keys with Scoped Permissions                          │
│  ├── Service-to-Service JWT (short-lived, 1h)                  │
│  ├── Mutual TLS for Critical Operations                        │
│  └── Rate Limiting per Agent Type                              │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Tier 3: External API Authentication                        │
│  ├── API Key Management (AWIN, Digistore24, N8N)              │
│  ├── OAuth2 Client Credentials Flow                            │
│  ├── Webhook Signature Validation                              │
│  └── IP Whitelisting for Sensitive Endpoints                  │
├─────────────────────────────────────────────────────────────────┤
│  ⚡ Tier 4: Real-time Authentication (WebSockets)              │
│  ├── JWT Token in WebSocket Handshake                          │
│  ├── Heartbeat-based Token Refresh                             │
│  ├── Agent Connection Validation                               │
│  └── Real-time Permission Updates                              │
└─────────────────────────────────────────────────────────────────┘
```

### **2. JWT TOKEN STRUCTURE:**
```json
{
  "header": {
    "typ": "JWT",
    "alg": "HS256",
    "kid": "mfm-2025-01"
  },
  "payload": {
    "iss": "marketingfunnelmaster.com",
    "sub": "user_12345",
    "aud": ["api.marketingfunnelmaster.com"],
    "exp": 1704096000,
    "iat": 1704009600,
    "nbf": 1704009600,
    "jti": "jwt_unique_id_12345",
    
    "user": {
      "id": "user_12345",
      "email": "user@example.com", 
      "role": "user",
      "subscription_tier": "pro",
      "permissions": [
        "websites.read",
        "websites.create",
        "agents.use",
        "intelligence.access"
      ],
      "limits": {
        "max_websites": 100,
        "max_ai_requests_per_month": 10000,
        "max_concurrent_agents": 10
      }
    },
    
    "session": {
      "session_id": "sess_67890",
      "ip_address": "192.168.1.100",
      "user_agent_hash": "ua_hash_12345",
      "created_at": 1704009600,
      "last_activity": 1704009600
    },
    
    "security": {
      "mfa_verified": true,
      "risk_level": "low",
      "device_trusted": true,
      "geo_location": "DE"
    }
  },
  "signature": "HMACSHA256_SIGNATURE"
}
```

### **3. API KEY STRUCTURE FOR AGENTS:**
```json
{
  "api_key_format": "mfm_agent_<agent_type>_<random_32_chars>",
  "examples": [
    "mfm_agent_opportunity_scanner_a1b2c3d4e5f6...",
    "mfm_agent_content_generator_x9y8z7w6v5u4...",
    "mfm_agent_website_builder_m3n2o1p9q8r7..."
  ],
  
  "api_key_metadata": {
    "key_id": "ak_12345",
    "agent_type": "opportunity_scanner",
    "agent_instance_id": "agent_instance_67890",
    "user_id": "user_12345",
    "scopes": [
      "research.conduct",
      "market.analyze",
      "trends.access",
      "affiliate.scan"
    ],
    "rate_limits": {
      "requests_per_minute": 500,
      "requests_per_hour": 10000,
      "concurrent_requests": 50
    },
    "restrictions": {
      "allowed_ips": ["192.168.1.0/24", "10.0.0.0/8"],
      "allowed_agents": ["content_generator", "website_builder"],
      "forbidden_operations": ["user.delete", "billing.modify"]
    },
    "created_at": "2025-07-03T00:00:00Z",
    "expires_at": "2026-07-03T00:00:00Z",
    "last_used": "2025-07-03T12:30:00Z",
    "usage_count": 45678
  }
}
```

---

## 🔧 IMPLEMENTATION SPECIFICATIONS

### **JWT AUTHENTICATION IMPLEMENTATION:**
```python
# JWT Service Implementation
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import secrets
import hashlib

class JWTService:
    """JWT token management service"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.issuer = "marketingfunnelmaster.com"
        self.audience = ["api.marketingfunnelmaster.com"]
    
    async def create_access_token(
        self, 
        user_id: str, 
        email: str,
        role: str,
        permissions: List[str],
        subscription_tier: str,
        session_data: Dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        # User limits based on subscription tier
        user_limits = self._get_user_limits(subscription_tier)
        
        payload = {
            # Standard JWT claims
            "iss": self.issuer,
            "sub": user_id,
            "aud": self.audience,
            "exp": expire,
            "iat": datetime.utcnow(),
            "nbf": datetime.utcnow(),
            "jti": f"jwt_{secrets.token_urlsafe(16)}",
            
            # User information
            "user": {
                "id": user_id,
                "email": email,
                "role": role,
                "subscription_tier": subscription_tier,
                "permissions": permissions,
                "limits": user_limits
            },
            
            # Session information
            "session": {
                "session_id": session_data.get("session_id"),
                "ip_address": session_data.get("ip_address"),
                "user_agent_hash": self._hash_user_agent(session_data.get("user_agent", "")),
                "created_at": int(datetime.utcnow().timestamp()),
                "last_activity": int(datetime.utcnow().timestamp())
            },
            
            # Security metadata
            "security": {
                "mfa_verified": session_data.get("mfa_verified", False),
                "risk_level": session_data.get("risk_level", "medium"),
                "device_trusted": session_data.get("device_trusted", False),
                "geo_location": session_data.get("geo_location", "unknown")
            }
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store token metadata in Redis for tracking
        await self._store_token_metadata(payload["jti"], user_id, expire)
        
        return token
    
    async def create_refresh_token(self, user_id: str, session_id: str) -> str:
        """Create refresh token"""
        expire = datetime.utcnow() + timedelta(days=30)
        
        payload = {
            "iss": self.issuer,
            "sub": user_id,
            "aud": self.audience,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "session_id": session_id,
            "jti": f"refresh_{secrets.token_urlsafe(16)}"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    async def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer
            )
            
            # Additional security checks
            if await self._is_token_blacklisted(payload.get("jti")):
                raise jwt.InvalidTokenError("Token is blacklisted")
            
            # Update last activity
            await self._update_token_activity(payload.get("jti"))
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")
    
    def _get_user_limits(self, subscription_tier: str) -> Dict:
        """Get user limits based on subscription tier"""
        limits_mapping = {
            "free": {
                "max_websites": 5,
                "max_ai_requests_per_month": 1000,
                "max_concurrent_agents": 2,
                "max_api_calls_per_minute": 10
            },
            "pro": {
                "max_websites": 100,
                "max_ai_requests_per_month": 10000,
                "max_concurrent_agents": 10,
                "max_api_calls_per_minute": 100
            },
            "enterprise": {
                "max_websites": 1500,
                "max_ai_requests_per_month": 100000,
                "max_concurrent_agents": 50,
                "max_api_calls_per_minute": 1000
            }
        }
        return limits_mapping.get(subscription_tier, limits_mapping["free"])
    
    def _hash_user_agent(self, user_agent: str) -> str:
        """Hash user agent for privacy"""
        return hashlib.sha256(user_agent.encode()).hexdigest()[:16]
```

### **API KEY MANAGEMENT FOR AGENTS:**
```python
# API Key Service for Agent Authentication
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class APIKeyService:
    """API Key management for AI agents"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.key_prefix = "mfm_agent_"
        self.metadata_prefix = "api_key_meta:"
    
    async def create_agent_api_key(
        self,
        user_id: str,
        agent_type: str,
        agent_instance_id: str,
        scopes: List[str],
        expires_in_days: int = 365
    ) -> Dict:
        """Create API key for AI agent"""
        
        # Generate secure API key
        random_part = secrets.token_urlsafe(32)
        api_key = f"{self.key_prefix}{agent_type}_{random_part}"
        
        # Generate key ID
        key_id = f"ak_{secrets.token_urlsafe(8)}"
        
        # Define rate limits based on agent type
        rate_limits = self._get_agent_rate_limits(agent_type)
        
        # Create metadata
        metadata = {
            "key_id": key_id,
            "api_key_hash": hashlib.sha256(api_key.encode()).hexdigest(),
            "agent_type": agent_type,
            "agent_instance_id": agent_instance_id,
            "user_id": user_id,
            "scopes": scopes,
            "rate_limits": rate_limits,
            "restrictions": self._get_agent_restrictions(agent_type),
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat(),
            "last_used": None,
            "usage_count": 0,
            "is_active": True
        }
        
        # Store in Redis
        await self.redis.setex(
            f"{self.metadata_prefix}{key_id}",
            expires_in_days * 24 * 60 * 60,
            json.dumps(metadata)
        )
        
        # Store key hash mapping
        await self.redis.setex(
            f"api_key_hash:{metadata['api_key_hash']}",
            expires_in_days * 24 * 60 * 60,
            key_id
        )
        
        return {
            "api_key": api_key,
            "key_id": key_id,
            "metadata": metadata
        }
    
    async def verify_api_key(self, api_key: str) -> Optional[Dict]:
        """Verify API key and return metadata"""
        try:
            # Hash the provided key
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Get key ID from hash
            key_id = await self.redis.get(f"api_key_hash:{key_hash}")
            if not key_id:
                return None
            
            # Get metadata
            metadata_json = await self.redis.get(f"{self.metadata_prefix}{key_id}")
            if not metadata_json:
                return None
            
            metadata = json.loads(metadata_json)
            
            # Check if key is active
            if not metadata.get("is_active", False):
                return None
            
            # Check expiration
            expires_at = datetime.fromisoformat(metadata["expires_at"])
            if datetime.utcnow() > expires_at:
                return None
            
            # Update usage statistics
            await self._update_api_key_usage(key_id, metadata)
            
            return metadata
            
        except Exception as e:
            logger.error(f"API key verification error: {e}")
            return None
    
    async def check_rate_limits(self, key_id: str, metadata: Dict) -> bool:
        """Check if API key is within rate limits"""
        rate_limits = metadata["rate_limits"]
        
        # Check requests per minute
        minute_key = f"rate_limit:minute:{key_id}:{int(datetime.utcnow().timestamp() // 60)}"
        minute_count = await self.redis.get(minute_key) or 0
        
        if int(minute_count) >= rate_limits["requests_per_minute"]:
            return False
        
        # Check requests per hour
        hour_key = f"rate_limit:hour:{key_id}:{int(datetime.utcnow().timestamp() // 3600)}"
        hour_count = await self.redis.get(hour_key) or 0
        
        if int(hour_count) >= rate_limits["requests_per_hour"]:
            return False
        
        # Increment counters
        await self.redis.incr(minute_key)
        await self.redis.expire(minute_key, 60)
        await self.redis.incr(hour_key)
        await self.redis.expire(hour_key, 3600)
        
        return True
    
    def _get_agent_rate_limits(self, agent_type: str) -> Dict:
        """Get rate limits based on agent type"""
        limits_mapping = {
            "opportunity_scanner": {
                "requests_per_minute": 500,
                "requests_per_hour": 10000,
                "concurrent_requests": 50
            },
            "content_generator": {
                "requests_per_minute": 200,
                "requests_per_hour": 5000,
                "concurrent_requests": 20
            },
            "website_builder": {
                "requests_per_minute": 100,
                "requests_per_hour": 2000,
                "concurrent_requests": 10
            },
            "seo_optimizer": {
                "requests_per_minute": 300,
                "requests_per_hour": 7500,
                "concurrent_requests": 30
            },
            "default": {
                "requests_per_minute": 100,
                "requests_per_hour": 1000,
                "concurrent_requests": 5
            }
        }
        return limits_mapping.get(agent_type, limits_mapping["default"])
    
    def _get_agent_restrictions(self, agent_type: str) -> Dict:
        """Get security restrictions based on agent type"""
        return {
            "allowed_ips": ["0.0.0.0/0"],  # Allow all IPs by default
            "allowed_agents": [],  # Empty means can communicate with all agents
            "forbidden_operations": [
                "user.delete",
                "billing.modify",
                "admin.access"
            ],
            "max_data_retention_days": 30
        }
```

---

## 🛡️ SECURITY HARDENING MEASURES

### **1. TOKEN SECURITY:**
```python
# Advanced Security Features
class SecurityHardening:
    """Advanced security measures for authentication"""
    
    async def detect_token_anomalies(self, token_payload: Dict, request_context: Dict) -> Dict:
        """Detect suspicious token usage patterns"""
        
        anomalies = []
        risk_score = 0
        
        # Geographic anomaly detection
        if self._detect_geographic_anomaly(token_payload, request_context):
            anomalies.append("geographic_anomaly")
            risk_score += 30
        
        # Device fingerprinting
        if self._detect_device_anomaly(token_payload, request_context):
            anomalies.append("device_anomaly")
            risk_score += 25
        
        # Usage pattern analysis
        if await self._detect_usage_anomaly(token_payload["user"]["id"]):
            anomalies.append("usage_pattern_anomaly")
            risk_score += 20
        
        # Time-based anomalies
        if self._detect_time_anomaly(token_payload, request_context):
            anomalies.append("time_anomaly")
            risk_score += 15
        
        return {
            "anomalies": anomalies,
            "risk_score": risk_score,
            "action_required": "block" if risk_score > 70 else "monitor" if risk_score > 40 else "allow"
        }
    
    async def implement_zero_trust(self, request: Dict) -> bool:
        """Implement zero-trust validation"""
        
        checks = [
            self._verify_request_signature(request),
            self._validate_request_timing(request),
            self._check_request_integrity(request),
            await self._validate_agent_identity(request),
            self._verify_operation_authorization(request)
        ]
        
        return all(checks)
```

### **2. AGENT-TO-AGENT AUTHENTICATION:**
```python
# Service-to-Service JWT for Agent Communication
class AgentAuthService:
    """Authentication service for agent-to-agent communication"""
    
    async def create_service_jwt(
        self,
        from_agent: str,
        to_agent: str,
        operation: str,
        expires_in_minutes: int = 60
    ) -> str:
        """Create short-lived JWT for agent communication"""
        
        expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        
        payload = {
            "iss": f"agent.{from_agent}",
            "aud": f"agent.{to_agent}",
            "sub": f"service_communication",
            "exp": expire,
            "iat": datetime.utcnow(),
            "operation": operation,
            "agent_auth": {
                "from_agent": from_agent,
                "to_agent": to_agent,
                "operation_scope": operation,
                "security_level": "high"
            }
        }
        
        return jwt.encode(payload, settings.AGENT_JWT_SECRET, algorithm="HS256")
    
    async def verify_agent_communication(self, token: str, expected_operation: str) -> bool:
        """Verify agent-to-agent communication token"""
        try:
            payload = jwt.decode(token, settings.AGENT_JWT_SECRET, algorithms=["HS256"])
            
            # Verify operation matches
            if payload.get("operation") != expected_operation:
                return False
            
            # Additional agent-specific validations
            return await self._validate_agent_permissions(payload)
            
        except jwt.InvalidTokenError:
            return False
```

---

## 📊 PERMISSION SYSTEM ARCHITECTURE

### **ROLE-BASED ACCESS CONTROL (RBAC):**
```json
{
  "roles": {
    "admin": {
      "permissions": ["*"],
      "description": "Full system access"
    },
    "user": {
      "permissions": [
        "websites.read",
        "websites.create",
        "websites.update", 
        "websites.delete:own",
        "agents.use",
        "intelligence.access",
        "analytics.read:own"
      ],
      "description": "Standard user access"
    },
    "agent": {
      "permissions": [
        "agents.communicate",
        "intelligence.process",
        "websites.generate",
        "content.create",
        "analytics.write"
      ],
      "description": "AI agent access"
    },
    "viewer": {
      "permissions": [
        "websites.read:own",
        "analytics.read:own"
      ],
      "description": "Read-only access"
    }
  },
  
  "permission_scopes": {
    "websites": ["read", "create", "update", "delete", "deploy"],
    "agents": ["use", "manage", "communicate", "monitor"],
    "intelligence": ["access", "process", "analyze"],
    "analytics": ["read", "write", "export"],
    "billing": ["read", "update"],
    "admin": ["access", "manage", "monitor"]
  }
}
```

---

## 🚨 KRITISCHE ENTSCHEIDUNGSPUNKTE

### **SOFORTIGE FREIGABE ERFORDERLICH:**

#### **1. JWT CONFIGURATION:**
- **Token Expiry**: 24h Access + 30d Refresh tokens
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Claims Structure**: User + Session + Security metadata
- **Storage**: Redis for token blacklisting and session management

#### **2. API KEY STRATEGY:**
- **Format**: `mfm_agent_{agent_type}_{random_32_chars}`
- **Scope-based Permissions**: Fine-grained agent capabilities
- **Rate Limiting**: Per-agent-type limits (100-500 req/min)
- **Expiry**: 1-year default with rotation capability

#### **3. SECURITY HARDENING:**
- **Zero-Trust Architecture**: Every request authenticated
- **Anomaly Detection**: Geographic, device, usage pattern monitoring
- **Agent-to-Agent**: Short-lived service JWTs (1h expiry)
- **Rate Limiting**: Multi-tier limits based on user/agent type

---

## 💰 SECURITY VS PERFORMANCE TRADE-OFFS

### **PERFORMANCE OPTIMIZATIONS:**
```python
# Performance-optimized security checks
class PerformanceOptimizedAuth:
    """Optimized authentication for high-throughput scenarios"""
    
    async def fast_token_validation(self, token: str) -> Optional[Dict]:
        """Optimized token validation with caching"""
        
        # 1. Check cache first (Redis)
        cached_payload = await self.redis.get(f"token_cache:{token[-16:]}")
        if cached_payload:
            return json.loads(cached_payload)
        
        # 2. Verify token signature
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # 3. Cache valid token for 5 minutes
            await self.redis.setex(
                f"token_cache:{token[-16:]}",
                300,  # 5 minutes
                json.dumps(payload)
            )
            
            return payload
            
        except jwt.InvalidTokenError:
            return None
```

### **SCALABILITY TARGETS:**
- **Token Validation**: <5ms average response time
- **API Key Lookup**: <2ms Redis-cached lookup
- **Rate Limit Check**: <1ms per request
- **Concurrent Authentication**: 10,000+ requests/second

---

## 🎯 IMPLEMENTATION TIMELINE

### **WEEK 1 SECURITY IMPLEMENTATION:**
```
DAY 1-2: JWT Service Implementation
├── Token generation and validation
├── Refresh token mechanism
├── Redis session storage
└── Basic RBAC implementation

DAY 3-4: API Key Management
├── Agent API key generation
├── Scope-based permissions
├── Rate limiting implementation
└── Usage tracking and analytics

DAY 5-6: Security Hardening
├── Anomaly detection implementation
├── Zero-trust validation
├── Agent-to-agent authentication
└── Security monitoring setup

DAY 7: Testing & Integration
├── Performance testing (10k+ req/s)
├── Security penetration testing
├── Integration with existing systems
└── Documentation and deployment
```

---

## 🎯 MANAGER-EMPFEHLUNG

**FREIGABE EMPFOHLEN:** JA ✅

**Begründung:**
1. **Multi-Tier Security**: JWT + API Keys + OAuth2 für comprehensive authentication
2. **Agent-Optimized**: Specialized authentication for 50+ AI agents
3. **Performance-First**: <5ms token validation for 10,000+ concurrent requests
4. **Zero-Trust Ready**: Every request authenticated with anomaly detection
5. **Scalable Design**: Support für 1500+ websites and millions of requests/day

**Kritische Erfolgsfaktoren:**
- Preserve existing user session compatibility during migration
- Ensure <50ms latency für agent-to-agent communication
- Implement comprehensive rate limiting to prevent abuse
- Zero-downtime deployment with fallback mechanisms

---

**🚀 BEREIT FÜR LEAD SYSTEM ARCHITECT SECURITY APPROVAL**

*Manager-Verantwortung: Security Implementation Oversight*  
*Protokoll: HTD-Manager → Human Security Leadership Approval*  
*Deadline: Sofortige Entscheidung für Week 1 Authentication-Implementation*