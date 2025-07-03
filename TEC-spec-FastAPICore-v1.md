# FASTAPI KERN-ARCHITEKTUR SPEZIFIKATION V1.0

**Dokument ID:** TEC-spec-FastAPICore-v1  
**Manager:** Claude Code (HTD-Manager-Ebene)  
**Erstellt:** 2025-07-03  
**Ziel:** Unified FastAPI Backend-Architektur für Multi-Millionen-Euro Digital Empire  
**Integration:** Bestehende AI-Intelligence + neue Skalierungs-Features  

---

## 🎯 ARCHITEKTUR-ZIELE

### **UNIFIED BACKEND VISION:**
- **Konsolidierung**: Express.js + Python FastAPI → Einheitliche FastAPI-Architektur
- **AI-Integration**: Nahtlose Einbindung bestehender Intelligence-Systeme
- **Skalierung**: Support für 1500+ Websites mit Agent-Orchestrierung
- **Performance**: <200ms API Response Times, 10,000+ concurrent requests

### **BESTEHENDE ASSETS PRESERVATION:**
- **Python AI Research Engine**: Vollständige Integration (ChromaDB, NetworkX, Multi-Model AI)
- **OpportunityScanner**: Enhanced real-time capabilities
- **Database Models**: Drizzle ORM Schema-Migration zu SQLAlchemy
- **External APIs**: AWIN, Digistore24, N8N seamless transition

---

## 🏗️ KERN-ARCHITEKTUR DESIGN

### **MICROSERVICES-ARCHITEKTUR:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI UNIFIED BACKEND                      │
├─────────────────────────────────────────────────────────────────┤
│  🎯 API Gateway Layer                                           │
│  ├── Authentication & Authorization (JWT + API Keys)           │
│  ├── Rate Limiting & Request Validation                        │
│  ├── Load Balancing & Service Discovery                        │
│  └── WebSocket Manager (Real-time Agent Communication)         │
├─────────────────────────────────────────────────────────────────┤
│  🤖 AI Agent Orchestration Layer                               │
│  ├── OpportunityScanner (Enhanced)                             │
│  ├── ContentGeneratorAgent                                     │ 
│  ├── WebsiteBuilderAgent                                       │
│  ├── SEOOptimizationAgent                                      │
│  └── MonetizationAgent                                         │
├─────────────────────────────────────────────────────────────────┤
│  🧠 Intelligence Core (Existing + Enhanced)                    │
│  ├── Multi-Model AI Research (GPT-4, Claude, Gemini)          │
│  ├── Knowledge Graph (NetworkX + ChromaDB)                     │
│  ├── ML Pipeline (scikit-learn, spaCy, NLTK)                  │
│  └── Real-time Market Analysis                                 │
├─────────────────────────────────────────────────────────────────┤
│  💾 Data & Storage Layer                                       │
│  ├── PostgreSQL (Supabase) - Primary Database                 │
│  ├── SQLite (Migration Buffer)                                 │
│  ├── ChromaDB (Vector Storage)                                 │
│  └── Redis (Caching + Session Storage)                         │
├─────────────────────────────────────────────────────────────────┤
│  🔌 External Integration Layer                                 │
│  ├── AWIN Affiliate Network                                    │
│  ├── Digistore24 Sales Tracking                               │
│  ├── N8N Workflow Automation                                   │
│  ├── Email Services (SendGrid, Mailgun)                       │
│  └── Cloud Infrastructure (Hetzner, Cloudflare)               │
└─────────────────────────────────────────────────────────────────┘
```

### **FASTAPI CORE COMPONENTS:**
```python
# Core FastAPI Application Structure
fastapi_core/
├── main.py                    # FastAPI Application Entry Point
├── config/                    # Configuration Management
│   ├── settings.py           # Environment-based settings
│   ├── database.py           # Database connections
│   └── external_apis.py      # External service configs
├── api/                       # API Route Modules
│   ├── v1/                   # API Version 1
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── agents.py        # AI Agent management
│   │   ├── websites.py      # Website operations
│   │   ├── analytics.py     # Analytics & reporting
│   │   └── intelligence.py  # AI Research integration
│   └── webhooks/             # Webhook handlers
├── core/                      # Core Business Logic
│   ├── agents/               # AI Agent implementations
│   ├── intelligence/         # Existing AI engine integration
│   ├── website_generator/    # Website creation logic
│   └── monetization/         # Revenue optimization
├── models/                    # Database Models (SQLAlchemy)
├── schemas/                   # Pydantic Models
├── services/                  # Business Logic Services
├── utils/                     # Utility Functions
└── tests/                     # Comprehensive Test Suite
```

---

## 🔧 TECHNOLOGIE-STACK INTEGRATION

### **CORE FASTAPI STACK:**
```python
# requirements.txt - Enhanced
fastapi==0.104.1              # Modern FastAPI
uvicorn[standard]==0.24.0     # ASGI Server
sqlalchemy==2.0.23            # ORM (Migration from Drizzle)
alembic==1.13.1              # Database Migrations
pydantic==2.5.0              # Data Validation
redis==5.0.1                 # Caching & Sessions
celery==5.3.4                # Background Tasks
websockets==12.0             # Real-time Communication

# AI & ML (Existing Integration)
openai==1.3.7                # GPT-4 Integration
anthropic==0.7.8             # Claude Integration
google-cloud-aiplatform       # Gemini Integration
chromadb==0.4.18             # Vector Database
networkx==3.2.1              # Knowledge Graph
scikit-learn==1.3.2          # ML Pipeline
spacy==3.7.2                 # NLP Processing
nltk==3.8.1                  # Text Analysis

# Database & Storage
asyncpg==0.29.0              # PostgreSQL Async Driver
aiosqlite==0.19.0            # SQLite Async (Migration)
supabase==2.0.2              # Supabase Integration

# External Integrations (Existing)
httpx==0.25.2                # Async HTTP Client
aiofiles==23.2.1             # Async File Operations
pillow==10.1.0               # Image Processing
beautifulsoup4==4.12.2       # Web Scraping
selenium==4.16.0             # Browser Automation
```

### **DATABASE MIGRATION STRATEGY:**
```python
# Migration from Drizzle ORM (TypeScript) to SQLAlchemy (Python)

# Current Drizzle Schema → SQLAlchemy Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    quiz_answers = Column(JSON)  # Preserve existing JSON data
    persona = Column(String)
    funnel_stage = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="leads")

# Migration Process:
# 1. Run side-by-side (SQLite + PostgreSQL)
# 2. Data synchronization scripts
# 3. Gradual endpoint migration
# 4. Full cutover with rollback capability
```

---

## 🤖 AI AGENT INTEGRATION PROTOKOLL

### **ENHANCED AGENT ORCHESTRATION:**
```python
# AI Agent Base Class with Enhanced Communication
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

class AIAgent(ABC):
    """Base class for all AI agents in the system"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.status = "idle"
        self.last_activity = datetime.utcnow()
        self.message_queue = asyncio.Queue()
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a specific task assigned to this agent"""
        pass
    
    async def send_message(self, target_agent: str, message: Dict[str, Any]):
        """Send message to another agent"""
        await agent_orchestrator.route_message(
            from_agent=self.agent_id,
            to_agent=target_agent,
            message=message
        )
    
    async def receive_message(self) -> Dict[str, Any]:
        """Receive message from message queue"""
        return await self.message_queue.get()

# Enhanced OpportunityScanner (Existing System Upgrade)
class OpportunityScannerAgent(AIAgent):
    """Enhanced version of existing OpportunityScanner"""
    
    def __init__(self):
        super().__init__("opportunity_scanner", {})
        self.ai_research_client = AIResearchClient()  # Existing Python AI
        self.awin_scanner = AWINScanner()  # Existing integration
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan for market opportunities"""
        if task["type"] == "market_scan":
            # Use existing AI research engine
            research_results = await self.ai_research_client.analyze(
                topic=task["topic"],
                depth="deep",
                competitor_analysis=True
            )
            
            # Enhanced with real-time AWIN data
            affiliate_opportunities = await self.awin_scanner.find_programs(
                niche=task["topic"]
            )
            
            return {
                "research": research_results,
                "affiliate_programs": affiliate_opportunities,
                "confidence_score": self._calculate_confidence(research_results),
                "next_actions": self._suggest_actions(research_results)
            }
```

### **REAL-TIME AGENT COMMUNICATION:**
```python
# WebSocket Manager for Real-time Agent Communication
class AgentWebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.agent_subscriptions: Dict[str, List[str]] = {}
    
    async def connect_agent(self, agent_id: str, websocket: WebSocket):
        """Connect agent to WebSocket"""
        await websocket.accept()
        self.active_connections[agent_id] = websocket
        logger.info(f"Agent {agent_id} connected via WebSocket")
    
    async def broadcast_to_agents(self, message: Dict[str, Any], agent_ids: List[str] = None):
        """Broadcast message to specific agents or all agents"""
        target_agents = agent_ids or list(self.active_connections.keys())
        
        for agent_id in target_agents:
            if agent_id in self.active_connections:
                try:
                    await self.active_connections[agent_id].send_json(message)
                except ConnectionClosedError:
                    await self.disconnect_agent(agent_id)
```

---

## 📊 API ENDPOINT ARCHITECTURE

### **CORE API ROUTES:**
```python
# API Router Structure
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

# Authentication Router
auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.post("/login")
async def login(credentials: LoginSchema) -> TokenResponse:
    """User authentication"""
    pass

@auth_router.post("/api-key")
async def generate_api_key(user: User = Depends(get_current_user)) -> APIKeyResponse:
    """Generate API key for agent integration"""
    pass

# AI Agent Management Router
agents_router = APIRouter(prefix="/agents", tags=["ai-agents"])

@agents_router.get("/")
async def list_agents() -> List[AgentStatus]:
    """List all available AI agents and their status"""
    pass

@agents_router.post("/{agent_id}/tasks")
async def assign_task(agent_id: str, task: TaskSchema) -> TaskResponse:
    """Assign task to specific AI agent"""
    pass

@agents_router.get("/{agent_id}/status")
async def get_agent_status(agent_id: str) -> AgentStatus:
    """Get current status of specific agent"""
    pass

# Website Management Router (New Core Feature)
websites_router = APIRouter(prefix="/websites", tags=["website-management"])

@websites_router.post("/generate")
async def generate_website(request: WebsiteGenerationRequest) -> WebsiteResponse:
    """Generate new website based on market research"""
    pass

@websites_router.get("/")
async def list_websites(limit: int = 50, offset: int = 0) -> List[WebsiteInfo]:
    """List all managed websites"""
    pass

@websites_router.get("/{website_id}/analytics")
async def get_website_analytics(website_id: str, period: str = "7d") -> AnalyticsData:
    """Get analytics for specific website"""
    pass

# Intelligence Integration Router (Enhanced Existing)
intelligence_router = APIRouter(prefix="/intelligence", tags=["ai-research"])

@intelligence_router.post("/research")
async def conduct_research(request: ResearchRequest) -> ResearchResponse:
    """Enhanced version of existing AI research endpoint"""
    pass

@intelligence_router.post("/opportunity-scan")
async def scan_opportunities(request: OpportunityScanRequest) -> OpportunityResponse:
    """Real-time opportunity scanning"""
    pass

@intelligence_router.get("/trends")
async def get_market_trends(industry: str, period: str = "30d") -> TrendData:
    """Get market trends for specific industry"""
    pass
```

### **WEBSOCKET ENDPOINTS:**
```python
# Real-time WebSocket Endpoints
@app.websocket("/ws/agents/{agent_id}")
async def agent_websocket(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for agent communication"""
    await websocket_manager.connect_agent(agent_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await agent_orchestrator.handle_agent_message(agent_id, data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect_agent(agent_id)

@app.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    """Real-time dashboard updates"""
    await websocket.accept()
    try:
        while True:
            # Send real-time metrics, agent status, website performance
            metrics = await get_real_time_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(5)  # Update every 5 seconds
    except WebSocketDisconnect:
        pass
```

---

## 🔒 SECURITY & AUTHENTICATION

### **MULTI-TIER AUTHENTICATION:**
```python
# JWT + API Key Authentication System
class AuthenticationService:
    def __init__(self):
        self.jwt_secret = settings.JWT_SECRET
        self.api_key_prefix = "mfm_"
    
    async def create_jwt_token(self, user_id: str, permissions: List[str]) -> str:
        """Create JWT token for user authentication"""
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    async def create_api_key(self, user_id: str, scope: List[str]) -> str:
        """Create API key for agent/service authentication"""
        key_data = {
            "user_id": user_id,
            "scope": scope,
            "created_at": datetime.utcnow().isoformat()
        }
        api_key = f"{self.api_key_prefix}{secrets.token_urlsafe(32)}"
        await redis.setex(f"api_key:{api_key}", 86400 * 365, json.dumps(key_data))
        return api_key

# Permission-based Access Control
class PermissionChecker:
    PERMISSIONS = {
        "agents.read": "Read agent status and information",
        "agents.manage": "Create, update, and delete agents",
        "websites.read": "Read website information and analytics",
        "websites.manage": "Create, update, and deploy websites",
        "intelligence.use": "Use AI research and analysis features",
        "admin.full": "Full administrative access"
    }
    
    async def check_permission(self, user_id: str, required_permission: str) -> bool:
        """Check if user has required permission"""
        user_permissions = await get_user_permissions(user_id)
        return required_permission in user_permissions or "admin.full" in user_permissions
```

---

## 📈 PERFORMANCE & MONITORING

### **PERFORMANCE OPTIMIZATION:**
```python
# Async Performance Optimizations
from fastapi import BackgroundTasks
import asyncio
from concurrent.futures import ThreadPoolExecutor

class PerformanceManager:
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.cache = Redis()
    
    async def cache_decorator(self, key: str, ttl: int = 300):
        """Redis caching decorator for expensive operations"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                cached_result = await self.cache.get(key)
                if cached_result:
                    return json.loads(cached_result)
                
                result = await func(*args, **kwargs)
                await self.cache.setex(key, ttl, json.dumps(result, default=str))
                return result
            return wrapper
        return decorator
    
    async def background_task(self, task_func, *args, **kwargs):
        """Execute task in background"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, task_func, *args, **kwargs)

# API Response Time Monitoring
@app.middleware("http")
async def monitor_response_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log slow requests
    if process_time > 1.0:  # Log requests slower than 1 second
        logger.warning(f"Slow request: {request.url.path} took {process_time:.2f}s")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

## 🔄 MIGRATION & DEPLOYMENT STRATEGY

### **PHASED MIGRATION APPROACH:**
```
PHASE 1: INFRASTRUCTURE SETUP (Week 1)
├── FastAPI Core Application Setup
├── Database Migration (SQLite → PostgreSQL)
├── Basic API Endpoints (Auth, Health Checks)
└── CI/CD Pipeline Integration

PHASE 2: AI INTEGRATION (Week 2)
├── Existing AI Research Engine Integration
├── OpportunityScanner Enhancement
├── Agent Communication Protocol
└── WebSocket Real-time Features

PHASE 3: FEATURE MIGRATION (Week 3)
├── Website Generation API
├── Analytics & Reporting
├── External Service Integrations (AWIN, Digistore24)
└── N8N Workflow Integration

PHASE 4: OPTIMIZATION & SCALING (Week 4)
├── Performance Tuning
├── Load Testing & Optimization
├── Monitoring & Alerting Setup
└── Production Deployment
```

### **ROLLBACK STRATEGY:**
- **Parallel Deployment**: New FastAPI runs alongside existing Express.js
- **Feature Flagging**: Gradual migration of endpoints
- **Data Synchronization**: Real-time sync between old and new systems
- **Instant Rollback**: DNS-level switching for immediate fallback

---

## 🎯 SUCCESS METRICS

### **PERFORMANCE TARGETS:**
- **API Response Time**: <200ms average, <500ms 95th percentile
- **Throughput**: 10,000+ concurrent requests
- **Agent Communication**: <50ms inter-agent message latency
- **Database Performance**: <100ms query time average
- **Uptime**: 99.9% availability

### **SCALABILITY TARGETS:**
- **Websites Managed**: Support for 1500+ websites
- **AI Agents**: 50+ concurrent agents
- **Background Tasks**: 1000+ tasks/minute processing
- **Real-time Connections**: 500+ WebSocket connections

---

**🎯 MANAGER-STATUS:** FastAPI Kern-Architektur vollständig spezifiziert. Integration bestehender AI-Systeme geplant.

**🚀 NÄCHSTER SCHRITT:** AI-Agent-Integration-Protokoll entwickeln für nahtlose Kommunikation.