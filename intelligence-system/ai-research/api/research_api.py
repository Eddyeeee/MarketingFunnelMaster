"""
FastAPI Research API - Bridge between Node.js and Python AI system
Provides REST endpoints for intelligent research capabilities
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
import json
from datetime import datetime

# Import our AI components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.ai_research_engine import AIResearchEngine, ResearchRequest, create_ai_research_engine
from analyzers.crypto_education_analyzer import CryptoEducationAnalyzer, create_crypto_analyzer

# FastAPI app
app = FastAPI(
    title="AI Research Engine API",
    description="Python-powered AI research system with ML and NLP capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
research_engine: Optional[AIResearchEngine] = None
crypto_analyzer: Optional[CryptoEducationAnalyzer] = None

# Pydantic models for API
class ResearchRequestModel(BaseModel):
    topic: str
    depth: str = "deep"
    persona_focus: Optional[str] = None
    competitor_analysis: bool = True
    market_sentiment: bool = True
    trend_prediction: bool = True
    content_clustering: bool = True
    ml_enhancement: bool = True

class CryptoAnalysisRequest(BaseModel):
    focus_area: str = "trading_education"
    depth: str = "comprehensive"
    include_simulations: bool = True

class QuickInsightRequest(BaseModel):
    query: str
    context: Optional[str] = None

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize AI components on startup"""
    global research_engine, crypto_analyzer
    
    try:
        # Load configuration
        config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        }
        
        # Initialize AI Research Engine
        research_engine = create_ai_research_engine(config)
        
        # Initialize Crypto Analyzer
        crypto_analyzer = create_crypto_analyzer()
        
        print("🧠 AI Research Engine API started successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize AI components: {e}")

# Health check
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Research Engine API is running",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "research_engine": research_engine is not None,
            "crypto_analyzer": crypto_analyzer is not None
        }
    }

# Main research endpoint
@app.post("/research/analyze")
async def conduct_research(request: ResearchRequestModel):
    """
    Conduct comprehensive AI-powered research on any topic
    """
    if not research_engine:
        raise HTTPException(status_code=503, detail="Research engine not available")
    
    try:
        # Convert to internal request format
        research_request = ResearchRequest(
            topic=request.topic,
            depth=request.depth,
            persona_focus=request.persona_focus,
            competitor_analysis=request.competitor_analysis,
            market_sentiment=request.market_sentiment,
            trend_prediction=request.trend_prediction,
            content_clustering=request.content_clustering,
            ml_enhancement=request.ml_enhancement
        )
        
        # Conduct research
        result = await research_engine.conduct_research(research_request)
        
        # Convert to JSON-serializable format
        return {
            "success": True,
            "topic": result.topic,
            "summary": result.summary,
            "key_insights": result.key_insights,
            "opportunities": result.opportunities,
            "competitors": result.competitors,
            "market_sentiment": result.market_sentiment,
            "trend_predictions": result.trend_predictions,
            "content_clusters": result.content_clusters,
            "confidence_score": result.confidence_score,
            "sources": result.sources,
            "knowledge_graph_entities": result.knowledge_graph_entities,
            "ml_patterns": result.ml_patterns,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

# Crypto-specific analysis endpoint
@app.post("/research/crypto-education")
async def analyze_crypto_education(request: CryptoAnalysisRequest):
    """
    Specialized analysis for crypto education market
    """
    if not crypto_analyzer:
        raise HTTPException(status_code=503, detail="Crypto analyzer not available")
    
    try:
        # Conduct comprehensive crypto education analysis
        result = await crypto_analyzer.analyze_crypto_education_market()
        
        return {
            "success": True,
            "analysis_type": "crypto_education_market",
            "focus_area": request.focus_area,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crypto analysis failed: {str(e)}")

# Quick insights endpoint
@app.post("/research/quick-insight")
async def get_quick_insight(request: QuickInsightRequest):
    """
    Get quick AI-powered insights for specific queries
    """
    if not research_engine:
        raise HTTPException(status_code=503, detail="Research engine not available")
    
    try:
        # Create quick research request
        quick_request = ResearchRequest(
            topic=request.query,
            depth="shallow",
            competitor_analysis=False,
            market_sentiment=True,
            trend_prediction=False,
            content_clustering=False,
            ml_enhancement=False
        )
        
        # Get quick analysis
        result = await research_engine.conduct_research(quick_request)
        
        return {
            "success": True,
            "query": request.query,
            "insight": result.summary,
            "key_points": result.key_insights[:3],  # Top 3 insights
            "confidence": result.confidence_score,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick insight failed: {str(e)}")

# Competitive analysis endpoint
@app.post("/research/competitors")
async def analyze_competitors(topic: str, num_competitors: int = 10):
    """
    Analyze competitors for a specific topic/market
    """
    if not research_engine:
        raise HTTPException(status_code=503, detail="Research engine not available")
    
    try:
        # Create competitor-focused request
        competitor_request = ResearchRequest(
            topic=f"competitors in {topic}",
            depth="medium",
            competitor_analysis=True,
            market_sentiment=False,
            trend_prediction=True,
            content_clustering=True,
            ml_enhancement=True
        )
        
        result = await research_engine.conduct_research(competitor_request)
        
        return {
            "success": True,
            "topic": topic,
            "competitors": result.competitors[:num_competitors],
            "market_analysis": result.summary,
            "competitive_gaps": result.opportunities,
            "trend_insights": result.trend_predictions,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Competitor analysis failed: {str(e)}")

# Content strategy endpoint
@app.post("/research/content-strategy")
async def generate_content_strategy(topic: str, target_audience: str = None):
    """
    Generate AI-powered content strategy
    """
    if not research_engine:
        raise HTTPException(status_code=503, detail="Research engine not available")
    
    try:
        research_topic = f"content strategy for {topic}"
        if target_audience:
            research_topic += f" targeting {target_audience}"
        
        strategy_request = ResearchRequest(
            topic=research_topic,
            depth="deep",
            persona_focus=target_audience,
            competitor_analysis=True,
            market_sentiment=True,
            trend_prediction=True,
            content_clustering=True,
            ml_enhancement=True
        )
        
        result = await research_engine.conduct_research(strategy_request)
        
        return {
            "success": True,
            "topic": topic,
            "target_audience": target_audience,
            "content_strategy": result.summary,
            "content_opportunities": result.opportunities,
            "content_clusters": result.content_clusters,
            "sentiment_analysis": result.market_sentiment,
            "recommended_topics": result.key_insights,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content strategy generation failed: {str(e)}")

# Trend analysis endpoint
@app.post("/research/trends")
async def analyze_trends(topic: str, timeframe: str = "6months"):
    """
    Analyze trends for a specific topic
    """
    if not research_engine:
        raise HTTPException(status_code=503, detail="Research engine not available")
    
    try:
        trend_request = ResearchRequest(
            topic=f"trends in {topic} over {timeframe}",
            depth="medium",
            competitor_analysis=False,
            market_sentiment=True,
            trend_prediction=True,
            content_clustering=False,
            ml_enhancement=True
        )
        
        result = await research_engine.conduct_research(trend_request)
        
        return {
            "success": True,
            "topic": topic,
            "timeframe": timeframe,
            "trend_analysis": result.summary,
            "trend_predictions": result.trend_predictions,
            "sentiment_trends": result.market_sentiment,
            "emerging_opportunities": result.opportunities,
            "confidence": result.confidence_score,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")

# Knowledge graph endpoint
@app.get("/research/knowledge-graph/{topic}")
async def get_knowledge_graph(topic: str):
    """
    Get knowledge graph data for a topic
    """
    if not research_engine:
        raise HTTPException(status_code=503, detail="Research engine not available")
    
    try:
        # Get knowledge graph entities for the topic
        kg_data = research_engine.knowledge_graph
        
        # Extract relevant nodes and edges
        nodes = []
        edges = []
        
        for node in kg_data.nodes():
            if topic.lower() in node.lower():
                nodes.append({
                    "id": node,
                    "label": node,
                    "type": kg_data.nodes[node].get("label", "entity")
                })
        
        for edge in kg_data.edges():
            if any(topic.lower() in n.lower() for n in edge):
                edges.append({
                    "source": edge[0],
                    "target": edge[1],
                    "weight": kg_data.edges[edge].get("weight", 1)
                })
        
        return {
            "success": True,
            "topic": topic,
            "nodes": nodes,
            "edges": edges,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge graph extraction failed: {str(e)}")

# Background task for learning
@app.post("/research/learn")
async def update_learning(background_tasks: BackgroundTasks, feedback_data: Dict[str, Any]):
    """
    Update learning algorithms with feedback
    """
    def update_learning_models(data):
        """Background task to update learning models"""
        try:
            if research_engine:
                # Update success patterns
                research_engine.success_patterns.append({
                    "feedback": data,
                    "timestamp": datetime.now().isoformat()
                })
            print(f"✅ Learning updated with feedback: {data}")
        except Exception as e:
            print(f"❌ Learning update failed: {e}")
    
    background_tasks.add_task(update_learning_models, feedback_data)
    
    return {
        "success": True,
        "message": "Learning update scheduled",
        "timestamp": datetime.now().isoformat()
    }

# System status endpoint
@app.get("/research/status")
async def get_system_status():
    """
    Get detailed system status
    """
    return {
        "system_status": "operational",
        "components": {
            "ai_research_engine": {
                "status": "running" if research_engine else "offline",
                "models_loaded": {
                    "chat_gpt": research_engine.chat_gpt is not None if research_engine else False,
                    "claude": research_engine.claude is not None if research_engine else False,
                    "nlp_model": research_engine.nlp_model is not None if research_engine else False
                } if research_engine else {}
            },
            "crypto_analyzer": {
                "status": "running" if crypto_analyzer else "offline",
                "sites_analyzed": len(crypto_analyzer.sites_data) if crypto_analyzer else 0,
                "patterns_identified": len(crypto_analyzer.patterns) if crypto_analyzer else 0
            }
        },
        "performance": {
            "uptime": "running",
            "memory_usage": "normal",
            "response_time": "fast"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)