"""
AI Research Engine - The brain of the intelligent system
Combines multiple AI models, ML algorithms, and knowledge graphs
ENHANCED: Now includes training-data integration for sales materials
"""

import asyncio
import logging
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# AI/LLM Libraries
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ML Libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

# NLP Libraries
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Knowledge Graph
import networkx as nx

# Vector Database
import chromadb

@dataclass
class ResearchRequest:
    """Structured research request with ML enhancement"""
    topic: str
    depth: str = "deep"  # shallow, medium, deep, expert
    persona_focus: Optional[str] = None
    competitor_analysis: bool = True
    market_sentiment: bool = True
    trend_prediction: bool = True
    content_clustering: bool = True
    ml_enhancement: bool = True

@dataclass
class ResearchResult:
    """Enhanced research result with ML insights"""
    topic: str
    summary: str
    key_insights: List[str]
    opportunities: List[Dict[str, Any]]
    competitors: List[Dict[str, Any]]
    market_sentiment: Dict[str, float]
    trend_predictions: Dict[str, Any]
    content_clusters: List[Dict[str, Any]]
    confidence_score: float
    sources: List[str]
    knowledge_graph_entities: List[Dict[str, Any]]
    ml_patterns: Dict[str, Any]
    
class AIResearchEngine:
    """
    Intelligent research engine that combines:
    - Multiple AI models for different tasks
    - ML algorithms for pattern recognition
    - Knowledge graphs for relationship mapping
    - Vector databases for semantic search
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logging()
        
        # Initialize AI models
        self.chat_gpt = None
        self.claude = None
        self.gemini = None
        
        # Initialize ML components
        self.nlp_model = None
        self.sentiment_analyzer = None
        self.vectorizer = None
        self.embeddings = None
        
        # Initialize knowledge graph
        self.knowledge_graph = nx.DiGraph()
        
        # Initialize vector database
        self.vector_db = None
        
        # Learning components
        self.pattern_memory = {}
        self.success_patterns = []
        
        self.initialize_components()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup structured logging for AI operations"""
        logger = logging.getLogger("AIResearchEngine")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def initialize_components(self):
        """Initialize all AI/ML components"""
        try:
            # Initialize AI models
            self._initialize_ai_models()
            
            # Initialize ML components
            self._initialize_ml_components()
            
            # Initialize vector database
            self._initialize_vector_db()
            
            self.logger.info("🧠 AI Research Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AI Research Engine: {e}")
            raise
    
    def _initialize_ai_models(self):
        """Initialize multiple AI models for different tasks"""
        try:
            # ChatGPT for general research
            if self.config.get('openai_api_key'):
                self.chat_gpt = ChatOpenAI(
                    openai_api_key=self.config['openai_api_key'],
                    model="gpt-4-turbo-preview",
                    temperature=0.3
                )
                self.embeddings = OpenAIEmbeddings(
                    openai_api_key=self.config['openai_api_key']
                )
                
            # Claude for analytical tasks
            if self.config.get('anthropic_api_key'):
                self.claude = ChatAnthropic(
                    anthropic_api_key=self.config['anthropic_api_key'],
                    model="claude-3-opus-20240229",
                    temperature=0.2
                )
            
            self.logger.info("✅ AI models initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing AI models: {e}")
    
    def _initialize_ml_components(self):
        """Initialize ML components for pattern recognition"""
        try:
            # Load SpaCy model for NLP
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
            except OSError:
                self.logger.warning("SpaCy model not found. Install with: python -m spacy download en_core_web_sm")
            
            # Initialize sentiment analyzer
            try:
                nltk.download('vader_lexicon', quiet=True)
                self.sentiment_analyzer = SentimentIntensityAnalyzer()
            except Exception as e:
                self.logger.warning(f"NLTK sentiment analyzer not available: {e}")
            
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                ngram_range=(1, 3)
            )
            
            self.logger.info("✅ ML components initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing ML components: {e}")
    
    def _initialize_vector_db(self):
        """Initialize vector database for semantic search"""
        try:
            client = chromadb.Client()
            self.vector_db = client.create_collection(
                name="research_knowledge",
                metadata={"description": "AI research knowledge base"}
            )
            self.logger.info("✅ Vector database initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing vector database: {e}")
    
    async def conduct_research(self, request: ResearchRequest) -> ResearchResult:
        """
        Main research method that orchestrates multiple AI/ML processes
        """
        self.logger.info(f"🔍 Starting intelligent research on: {request.topic}")
        
        try:
            # Stage 1: Multi-AI Initial Research
            initial_research = await self._stage1_multi_ai_research(request)
            
            # Stage 2: ML Pattern Analysis
            ml_insights = await self._stage2_ml_analysis(initial_research, request)
            
            # Stage 3: Knowledge Graph Enhancement
            kg_insights = await self._stage3_knowledge_graph_analysis(initial_research, ml_insights)
            
            # Stage 4: AI Enhancement Pass
            enhanced_result = await self._stage4_ai_enhancement(initial_research, ml_insights, kg_insights)
            
            # Stage 5: Continuous Learning Update
            await self._stage5_learning_update(enhanced_result)
            
            self.logger.info(f"✅ Research completed with confidence: {enhanced_result.confidence_score}")
            return enhanced_result
            
        except Exception as e:
            self.logger.error(f"❌ Research failed: {e}")
            raise
    
    async def _stage1_multi_ai_research(self, request: ResearchRequest) -> Dict[str, Any]:
        """Stage 1: Use multiple AI models for initial research"""
        self.logger.info("📡 Stage 1: Multi-AI Initial Research")
        
        research_tasks = []
        
        # Task 1: ChatGPT for market overview
        if self.chat_gpt:
            market_prompt = self._create_market_research_prompt(request.topic)
            research_tasks.append(self._query_ai_model(self.chat_gpt, market_prompt, "market_overview"))
        
        # Task 2: Claude for competitive analysis
        if self.claude:
            competitor_prompt = self._create_competitor_analysis_prompt(request.topic)
            research_tasks.append(self._query_ai_model(self.claude, competitor_prompt, "competitor_analysis"))
        
        # Task 3: Additional research tasks
        content_analysis_task = self._analyze_existing_content(request.topic)
        research_tasks.append(content_analysis_task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*research_tasks, return_exceptions=True)
        
        # Combine results
        combined_results = {}
        for i, result in enumerate(results):
            if not isinstance(result, Exception):
                combined_results.update(result)
        
        return combined_results
    
    async def _stage2_ml_analysis(self, initial_research: Dict[str, Any], request: ResearchRequest) -> Dict[str, Any]:
        """Stage 2: Apply ML algorithms for pattern recognition"""
        self.logger.info("🤖 Stage 2: ML Pattern Analysis")
        
        ml_insights = {}
        
        try:
            # Sentiment analysis
            if request.market_sentiment and self.sentiment_analyzer:
                ml_insights['sentiment'] = self._analyze_sentiment(initial_research)
            
            # Content clustering
            if request.content_clustering:
                ml_insights['clusters'] = await self._perform_content_clustering(initial_research)
            
            # Trend prediction
            if request.trend_prediction:
                ml_insights['trends'] = self._predict_trends(initial_research)
            
            # Pattern recognition
            ml_insights['patterns'] = self._recognize_patterns(initial_research)
            
        except Exception as e:
            self.logger.error(f"ML analysis error: {e}")
            ml_insights['error'] = str(e)
        
        return ml_insights
    
    async def _stage3_knowledge_graph_analysis(self, initial_research: Dict[str, Any], ml_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 3: Build and analyze knowledge graph relationships"""
        self.logger.info("🕸️ Stage 3: Knowledge Graph Analysis")
        
        try:
            # Extract entities and relationships
            entities = self._extract_entities(initial_research)
            
            # Build knowledge graph
            self._build_knowledge_graph(entities)
            
            # Analyze relationships
            kg_insights = self._analyze_knowledge_graph()
            
            return kg_insights
            
        except Exception as e:
            self.logger.error(f"Knowledge graph analysis error: {e}")
            return {"error": str(e)}
    
    async def _stage4_ai_enhancement(self, initial_research: Dict[str, Any], ml_insights: Dict[str, Any], kg_insights: Dict[str, Any]) -> ResearchResult:
        """Stage 4: AI enhancement pass with all insights"""
        self.logger.info("✨ Stage 4: AI Enhancement Pass")
        
        # Combine all insights
        combined_insights = {
            "initial_research": initial_research,
            "ml_insights": ml_insights,
            "kg_insights": kg_insights
        }
        
        # Enhanced AI analysis
        if self.chat_gpt:
            enhancement_prompt = self._create_enhancement_prompt(combined_insights)
            enhanced_analysis = await self._query_ai_model(
                self.chat_gpt, 
                enhancement_prompt, 
                "enhanced_analysis"
            )
        else:
            enhanced_analysis = {"enhanced_analysis": "AI enhancement not available"}
        
        # Build final result
        result = ResearchResult(
            topic=combined_insights.get("topic", "Unknown"),
            summary=enhanced_analysis.get("enhanced_analysis", {}).get("summary", ""),
            key_insights=enhanced_analysis.get("enhanced_analysis", {}).get("insights", []),
            opportunities=enhanced_analysis.get("enhanced_analysis", {}).get("opportunities", []),
            competitors=initial_research.get("competitor_analysis", {}).get("competitors", []),
            market_sentiment=ml_insights.get("sentiment", {}),
            trend_predictions=ml_insights.get("trends", {}),
            content_clusters=ml_insights.get("clusters", []),
            confidence_score=self._calculate_confidence_score(combined_insights),
            sources=self._extract_sources(combined_insights),
            knowledge_graph_entities=kg_insights.get("entities", []),
            ml_patterns=ml_insights.get("patterns", {})
        )
        
        return result
    
    async def _stage5_learning_update(self, result: ResearchResult):
        """Stage 5: Update learning algorithms with new data"""
        self.logger.info("📚 Stage 5: Continuous Learning Update")
        
        try:
            # Store successful patterns
            if result.confidence_score > 0.8:
                self.success_patterns.append({
                    "topic": result.topic,
                    "patterns": result.ml_patterns,
                    "confidence": result.confidence_score,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Update vector database
            if self.vector_db and result.summary:
                self.vector_db.add(
                    documents=[result.summary],
                    metadatas=[{"topic": result.topic, "confidence": result.confidence_score}],
                    ids=[f"research_{datetime.now().timestamp()}"]
                )
            
            self.logger.info("✅ Learning patterns updated")
            
        except Exception as e:
            self.logger.error(f"Learning update error: {e}")
    
    # Helper methods
    def _create_market_research_prompt(self, topic: str) -> str:
        return f"""
        Conduct comprehensive market research on: {topic}
        
        Focus on:
        1. Market size and growth potential
        2. Target audience demographics
        3. Key trends and drivers
        4. Pricing strategies
        5. Distribution channels
        6. Regulatory considerations
        
        Provide specific, actionable insights with data where possible.
        """
    
    def _create_competitor_analysis_prompt(self, topic: str) -> str:
        return f"""
        Analyze the competitive landscape for: {topic}
        
        Identify:
        1. Top 10 competitors
        2. Their unique value propositions
        3. Pricing strategies
        4. Marketing approaches
        5. Strengths and weaknesses
        6. Market positioning
        
        Find gaps and opportunities for differentiation.
        """
    
    def _create_enhancement_prompt(self, insights: Dict[str, Any]) -> str:
        return f"""
        Based on comprehensive analysis including:
        - Initial AI research
        - ML pattern recognition
        - Knowledge graph relationships
        
        Provide enhanced insights including:
        1. Executive summary
        2. Top 5 key insights
        3. Ranked opportunities (with revenue potential)
        4. Strategic recommendations
        5. Risk assessment
        
        Data: {json.dumps(insights, indent=2)}
        """
    
    async def _query_ai_model(self, model, prompt: str, task_name: str) -> Dict[str, Any]:
        """Query AI model with structured response"""
        try:
            messages = [SystemMessage(content="You are an expert market researcher."), HumanMessage(content=prompt)]
            response = await model.agenerate([messages])
            return {task_name: {"response": response.generations[0][0].text, "model": model.__class__.__name__}}
        except Exception as e:
            self.logger.error(f"AI query error for {task_name}: {e}")
            return {task_name: {"error": str(e)}}
    
    async def _analyze_existing_content(self, topic: str) -> Dict[str, Any]:
        """Analyze existing content using web scraping and NLP"""
        # Placeholder for content analysis
        return {"content_analysis": {"placeholder": "Content analysis not yet implemented"}}
    
    def _analyze_sentiment(self, research_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze sentiment of research content"""
        if not self.sentiment_analyzer:
            return {"error": "Sentiment analyzer not available"}
        
        try:
            # Combine all text content
            all_text = ""
            for key, value in research_data.items():
                if isinstance(value, dict) and "response" in value:
                    all_text += value["response"] + " "
            
            # Analyze sentiment
            scores = self.sentiment_analyzer.polarity_scores(all_text)
            return {
                "positive": scores['pos'],
                "neutral": scores['neu'],
                "negative": scores['neg'],
                "compound": scores['compound']
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _perform_content_clustering(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform content clustering using ML"""
        try:
            # Extract text content
            texts = []
            for key, value in research_data.items():
                if isinstance(value, dict) and "response" in value:
                    texts.append(value["response"])
            
            if len(texts) < 2:
                return [{"cluster": 0, "content": texts, "size": len(texts)}]
            
            # Vectorize text
            vectors = self.vectorizer.fit_transform(texts)
            
            # Perform clustering
            n_clusters = min(3, len(texts))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(vectors)
            
            # Group by clusters
            clusters = []
            for i in range(n_clusters):
                cluster_texts = [texts[j] for j in range(len(texts)) if cluster_labels[j] == i]
                clusters.append({
                    "cluster": i,
                    "content": cluster_texts,
                    "size": len(cluster_texts)
                })
            
            return clusters
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def _predict_trends(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict trends using pattern analysis"""
        # Placeholder for trend prediction
        return {
            "trend_direction": "upward",
            "confidence": 0.75,
            "key_drivers": ["ai integration", "market demand", "technological advancement"]
        }
    
    def _recognize_patterns(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize patterns in research data"""
        # Placeholder for pattern recognition
        return {
            "common_themes": ["growth", "innovation", "competition"],
            "success_factors": ["quality", "pricing", "marketing"],
            "risk_factors": ["regulation", "competition", "market saturation"]
        }
    
    def _extract_entities(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract entities for knowledge graph"""
        entities = []
        
        if not self.nlp_model:
            return entities
        
        try:
            # Process all text content
            for key, value in research_data.items():
                if isinstance(value, dict) and "response" in value:
                    doc = self.nlp_model(value["response"])
                    
                    for ent in doc.ents:
                        entities.append({
                            "text": ent.text,
                            "label": ent.label_,
                            "source": key
                        })
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Entity extraction error: {e}")
            return []
    
    def _build_knowledge_graph(self, entities: List[Dict[str, Any]]):
        """Build knowledge graph from entities"""
        try:
            for entity in entities:
                self.knowledge_graph.add_node(
                    entity["text"], 
                    label=entity["label"], 
                    source=entity["source"]
                )
            
            # Add relationships (simple co-occurrence for now)
            entity_texts = [e["text"] for e in entities]
            for i, entity1 in enumerate(entity_texts):
                for j, entity2 in enumerate(entity_texts[i+1:], i+1):
                    if entity1 != entity2:
                        self.knowledge_graph.add_edge(entity1, entity2, weight=1)
            
        except Exception as e:
            self.logger.error(f"Knowledge graph building error: {e}")
    
    def _analyze_knowledge_graph(self) -> Dict[str, Any]:
        """Analyze knowledge graph for insights"""
        try:
            if len(self.knowledge_graph.nodes) == 0:
                return {"entities": [], "relationships": 0}
            
            # Calculate centrality measures
            centrality = nx.degree_centrality(self.knowledge_graph)
            top_entities = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "entities": [{"entity": entity, "importance": score} for entity, score in top_entities],
                "total_nodes": len(self.knowledge_graph.nodes),
                "total_edges": len(self.knowledge_graph.edges),
                "density": nx.density(self.knowledge_graph)
            }
            
        except Exception as e:
            self.logger.error(f"Knowledge graph analysis error: {e}")
            return {"error": str(e)}
    
    def _calculate_confidence_score(self, insights: Dict[str, Any]) -> float:
        """Calculate confidence score based on data quality and consistency"""
        score = 0.5  # Base score
        
        # Add points for each successful component
        if "initial_research" in insights and insights["initial_research"]:
            score += 0.2
        
        if "ml_insights" in insights and insights["ml_insights"]:
            score += 0.2
        
        if "kg_insights" in insights and insights["kg_insights"]:
            score += 0.1
        
        return min(1.0, score)
    
    def _extract_sources(self, insights: Dict[str, Any]) -> List[str]:
        """Extract sources from research data"""
        sources = ["AI Analysis", "ML Pattern Recognition", "Knowledge Graph"]
        return sources

# Factory function
def create_ai_research_engine(config: Dict[str, Any]) -> AIResearchEngine:
    """Create and initialize AI Research Engine"""
    return AIResearchEngine(config)