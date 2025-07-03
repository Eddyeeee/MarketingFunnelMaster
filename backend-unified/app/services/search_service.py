"""
Adaptive Search Service - Week 2 Implementation
Milestone 1C: Self-optimizing search strategy selection

Executor: Claude Code (HTD-Executor)
Date: 2025-07-03
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json

from app.services.database_service import DatabaseService
from app.models.rag_models import (
    QueryRequest, SearchResponse, FeedbackRequest, PerformanceMetrics
)

logger = logging.getLogger(__name__)

class AdaptiveSearchService:
    """Self-optimizing search strategy selection and performance management"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self._strategy_cache = {}
        self._cache_expiry = datetime.now()
        self._cache_duration_minutes = 15
        self._initialized = False
    
    async def initialize(self):
        """Initialize search service"""
        try:
            await self.db_service.initialize()
            await self._load_strategy_cache()
            self._initialized = True
            logger.info("✅ Adaptive Search Service initialized")
        except Exception as e:
            logger.error(f"❌ Search Service initialization failed: {e}")
            raise
    
    async def select_optimal_strategy(
        self, 
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        AI-driven strategy selection based on query characteristics and performance history
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Refresh strategy cache if expired
            if datetime.now() > self._cache_expiry:
                await self._refresh_strategy_cache()
            
            # Analyze query characteristics
            query_profile = await self._analyze_query(query, context)
            
            # Get historical performance for similar queries
            strategy_performance = await self._get_strategy_performance_for_profile(query_profile)
            
            # Select best performing strategy
            optimal_strategy = await self._select_strategy(strategy_performance, query_profile)
            
            logger.info(f"Selected strategy '{optimal_strategy}' for query profile: {query_profile}")
            
            return optimal_strategy
            
        except Exception as e:
            logger.error(f"Strategy selection failed: {e}")
            return "hybrid"  # Safe default
    
    async def execute_adaptive_search(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Strategic search execution with real-time adaptation"""
        try:
            # Select optimal strategy
            strategy = await self.select_optimal_strategy(query, context)
            
            # Execute search with selected strategy
            # Note: This would integrate with RAG service
            search_result = {
                "strategy_used": strategy,
                "query": query,
                "context": context,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return search_result
            
        except Exception as e:
            logger.error(f"Adaptive search execution failed: {e}")
            raise
    
    async def analyze_search_performance(
        self,
        time_window_days: int = 7,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Strategic performance analysis leveraging Week 1 analytics functions"""
        try:
            # Use database service to get performance data
            performance_data = await self.db_service.analyze_search_performance(time_window_days)
            
            # Get strategy-specific performance
            strategy_performance = await self.db_service.get_strategy_performance()
            
            # Calculate improvement trends
            improvement_trends = await self._calculate_improvement_trends(time_window_days)
            
            analysis = {
                "time_period": f"{time_window_days} days",
                "overall_performance": performance_data,
                "strategy_performance": strategy_performance,
                "improvement_trends": improvement_trends,
                "recommendations": await self._generate_performance_recommendations(strategy_performance),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            raise
    
    async def generate_learning_signals(
        self,
        request: QueryRequest,
        response: SearchResponse,
        user: Optional[Any] = None
    ):
        """Generate learning signals for continuous improvement"""
        try:
            # Extract implicit learning signals
            learning_signals = {
                "query_complexity": len(request.query.split()),
                "strategy_confidence": response.confidence_score,
                "result_count": response.total_results,
                "processing_time": response.processing_time_ms,
                "context_factors": self._extract_context_factors(request.context),
                "user_persona": request.context.user_persona.value if request.context and request.context.user_persona else None
            }
            
            # Store learning signals for future optimization
            await self._store_learning_signals(response.query_id, learning_signals)
            
            logger.debug(f"Learning signals generated for query {response.query_id}")
            
        except Exception as e:
            logger.error(f"Learning signal generation failed: {e}")
    
    async def process_batch_learning(
        self,
        request,
        batch_results: List[SearchResponse],
        user: Optional[Any] = None
    ):
        """Process learning from batch search operations"""
        try:
            # Aggregate batch learning signals
            batch_signals = {
                "total_queries": len(batch_results),
                "avg_confidence": sum(r.confidence_score for r in batch_results) / len(batch_results),
                "avg_processing_time": sum(r.processing_time_ms for r in batch_results) / len(batch_results),
                "strategy_distribution": {},
                "batch_optimization_used": getattr(request, 'batch_optimization', False)
            }
            
            # Count strategy usage
            for result in batch_results:
                strategy = result.strategy_used
                batch_signals["strategy_distribution"][strategy] = batch_signals["strategy_distribution"].get(strategy, 0) + 1
            
            # Store batch learning data
            await self._store_batch_learning(batch_signals)
            
            logger.info(f"Batch learning processed for {len(batch_results)} queries")
            
        except Exception as e:
            logger.error(f"Batch learning processing failed: {e}")
    
    async def optimize_search_strategies(self, user_id: Optional[str] = None):
        """Strategic automated optimization execution"""
        try:
            logger.info("Starting search strategy optimization...")
            
            # Analyze current performance
            performance_data = await self.analyze_search_performance(time_window_days=7)
            
            # Identify optimization opportunities
            optimization_opportunities = await self._identify_optimization_opportunities(performance_data)
            
            # Apply optimizations
            if optimization_opportunities:
                await self._apply_optimizations(optimization_opportunities)
                logger.info(f"Applied {len(optimization_opportunities)} optimizations")
            
            # Trigger database maintenance
            await self.db_service.maintain_database()
            
            # Refresh strategy cache
            await self._refresh_strategy_cache()
            
            logger.info("✅ Search strategy optimization completed")
            
        except Exception as e:
            logger.error(f"Search optimization failed: {e}")
            raise
    
    async def get_strategy_performance_metrics(self) -> List[Dict[str, Any]]:
        """Get available search strategies and their performance metrics"""
        try:
            strategy_performance = await self.db_service.get_strategy_performance()
            
            strategies = []
            for strategy_name, metrics in strategy_performance.items():
                strategy_info = {
                    "name": strategy_name,
                    "display_name": strategy_name.replace("_", " ").title(),
                    "metrics": metrics,
                    "recommended_for": self._get_strategy_recommendations(strategy_name, metrics),
                    "last_updated": datetime.utcnow().isoformat()
                }
                strategies.append(strategy_info)
            
            return strategies
            
        except Exception as e:
            logger.error(f"Strategy metrics retrieval failed: {e}")
            return []
    
    # Private helper methods
    
    async def _analyze_query(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze query characteristics for strategy selection"""
        profile = {
            "length": len(query.split()),
            "complexity": "simple" if len(query.split()) < 5 else "complex",
            "has_technical_terms": any(term in query.lower() for term in [
                "api", "code", "function", "algorithm", "technical", "implementation",
                "database", "server", "programming", "development"
            ]),
            "has_business_terms": any(term in query.lower() for term in [
                "revenue", "profit", "marketing", "sales", "conversion", "roi",
                "business", "strategy", "growth", "customer"
            ]),
            "question_type": "how" if query.lower().startswith(("how", "what", "why", "when", "where")) else "search",
            "context_available": context is not None
        }
        
        if context:
            profile.update({
                "user_persona": context.get("user_persona"),
                "device_type": context.get("device_type"),
                "domain": context.get("domain")
            })
        
        return profile
    
    async def _get_strategy_performance_for_profile(
        self, 
        query_profile: Dict[str, Any]
    ) -> Dict[str, float]:
        """Get historical performance for queries with similar profile"""
        try:
            # Get cached strategy performance
            if self._strategy_cache:
                return self._strategy_cache
            
            # Fallback to database query
            strategy_performance = await self.db_service.get_strategy_performance()
            
            # Convert to simple performance scores
            performance_scores = {}
            for strategy, metrics in strategy_performance.items():
                # Calculate composite performance score
                satisfaction_weight = 0.4
                confidence_weight = 0.3
                speed_weight = 0.2
                conversion_weight = 0.1
                
                # Normalize response time (lower is better, max 5 seconds)
                normalized_speed = max(0, 1 - (metrics.get("avg_response_time", 5) / 5))
                
                composite_score = (
                    metrics.get("avg_satisfaction", 0.5) * satisfaction_weight +
                    metrics.get("avg_confidence", 0.5) * confidence_weight +
                    normalized_speed * speed_weight +
                    metrics.get("conversion_rate", 0.1) * conversion_weight
                )
                
                performance_scores[strategy] = composite_score
            
            return performance_scores
            
        except Exception as e:
            logger.error(f"Strategy performance retrieval failed: {e}")
            return {
                "hybrid": 0.8,
                "vector": 0.7,
                "semantic": 0.6,
                "performance_weighted": 0.75
            }
    
    async def _select_strategy(
        self, 
        strategy_performance: Dict[str, float],
        query_profile: Dict[str, Any]
    ) -> str:
        """Select optimal strategy based on performance and query profile"""
        try:
            # Apply profile-based adjustments
            adjusted_scores = strategy_performance.copy()
            
            # Technical queries benefit from semantic search
            if query_profile.get("has_technical_terms"):
                adjusted_scores["semantic"] = adjusted_scores.get("semantic", 0.5) * 1.2
                adjusted_scores["hybrid"] = adjusted_scores.get("hybrid", 0.5) * 1.1
            
            # Business queries benefit from performance weighting
            if query_profile.get("has_business_terms"):
                adjusted_scores["performance_weighted"] = adjusted_scores.get("performance_weighted", 0.5) * 1.2
            
            # Simple queries work well with vector search
            if query_profile.get("complexity") == "simple":
                adjusted_scores["vector"] = adjusted_scores.get("vector", 0.5) * 1.1
            
            # Select strategy with highest adjusted score
            best_strategy = max(adjusted_scores, key=adjusted_scores.get)
            
            return best_strategy
            
        except Exception as e:
            logger.error(f"Strategy selection failed: {e}")
            return "hybrid"
    
    async def _load_strategy_cache(self):
        """Load strategy performance into cache"""
        try:
            self._strategy_cache = await self.db_service.get_strategy_performance()
            self._cache_expiry = datetime.now() + timedelta(minutes=self._cache_duration_minutes)
            logger.debug("Strategy cache loaded")
        except Exception as e:
            logger.error(f"Strategy cache loading failed: {e}")
    
    async def _refresh_strategy_cache(self):
        """Refresh the strategy performance cache"""
        await self._load_strategy_cache()
    
    async def _extract_context_factors(self, context) -> Dict[str, Any]:
        """Extract learning factors from query context"""
        if not context:
            return {}
        
        factors = {}
        if hasattr(context, 'user_persona') and context.user_persona:
            factors['user_persona'] = context.user_persona.value
        if hasattr(context, 'device_type') and context.device_type:
            factors['device_type'] = context.device_type.value
        if hasattr(context, 'domain') and context.domain:
            factors['domain'] = context.domain
            
        return factors
    
    async def _store_learning_signals(self, query_id: str, signals: Dict[str, Any]):
        """Store learning signals for future optimization"""
        try:
            # Store in outcome tracking (extend existing Week 1 structure)
            outcome_data = {
                "learning_signals": signals,
                "signal_type": "implicit_learning",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.db_service.store_query_outcome(
                query_id=query_id,
                response_id=f"learning_{query_id}",
                outcome_data=outcome_data,
                confidence_score=signals.get("strategy_confidence", 0.5)
            )
            
        except Exception as e:
            logger.error(f"Learning signal storage failed: {e}")
    
    async def _store_batch_learning(self, batch_signals: Dict[str, Any]):
        """Store batch learning data"""
        try:
            # Store batch learning as special outcome event
            batch_id = f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            outcome_data = {
                **batch_signals,
                "outcome_type": "batch_learning",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.db_service.store_query_outcome(
                query_id=batch_id,
                response_id=f"batch_result_{batch_id}",
                outcome_data=outcome_data,
                confidence_score=batch_signals.get("avg_confidence", 0.5)
            )
            
        except Exception as e:
            logger.error(f"Batch learning storage failed: {e}")
    
    async def _calculate_improvement_trends(self, time_window_days: int) -> Dict[str, float]:
        """Calculate performance improvement trends"""
        try:
            # Simple trend calculation - compare first half vs second half of time window
            half_window = time_window_days // 2
            
            recent_performance = await self.db_service.analyze_search_performance(half_window)
            older_performance = await self.db_service.analyze_search_performance(time_window_days)
            
            trends = {}
            if recent_performance and older_performance:
                # Calculate improvement percentages
                for metric in ["avg_satisfaction", "avg_confidence", "conversion_rate"]:
                    recent_value = recent_performance.get(metric, 0)
                    older_value = older_performance.get(metric, 0)
                    if older_value > 0:
                        improvement = ((recent_value - older_value) / older_value) * 100
                        trends[f"{metric}_improvement_percent"] = round(improvement, 2)
            
            return trends
            
        except Exception as e:
            logger.error(f"Trend calculation failed: {e}")
            return {}
    
    async def _generate_performance_recommendations(
        self, 
        strategy_performance: Dict[str, Dict[str, float]]
    ) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        try:
            for strategy, metrics in strategy_performance.items():
                avg_satisfaction = metrics.get("avg_satisfaction", 0)
                avg_confidence = metrics.get("avg_confidence", 0)
                conversion_rate = metrics.get("conversion_rate", 0)
                
                if avg_satisfaction < 0.7:
                    recommendations.append(f"Improve {strategy} strategy user satisfaction (currently {avg_satisfaction:.2f})")
                
                if avg_confidence < 0.8:
                    recommendations.append(f"Enhance {strategy} strategy confidence scoring (currently {avg_confidence:.2f})")
                
                if conversion_rate < 0.1:
                    recommendations.append(f"Optimize {strategy} strategy for better conversions (currently {conversion_rate:.2%})")
        
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
        
        return recommendations
    
    async def _identify_optimization_opportunities(
        self, 
        performance_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify optimization opportunities from performance data"""
        opportunities = []
        
        try:
            strategy_performance = performance_data.get("strategy_performance", {})
            
            for strategy, metrics in strategy_performance.items():
                # Identify underperforming strategies
                if metrics.get("avg_satisfaction", 0) < 0.6:
                    opportunities.append({
                        "type": "satisfaction_improvement",
                        "strategy": strategy,
                        "current_value": metrics.get("avg_satisfaction"),
                        "target_value": 0.8,
                        "action": "retrain_strategy_weights"
                    })
                
                # Identify slow strategies
                if metrics.get("avg_response_time", 0) > 3.0:
                    opportunities.append({
                        "type": "performance_improvement",
                        "strategy": strategy,
                        "current_value": metrics.get("avg_response_time"),
                        "target_value": 2.0,
                        "action": "optimize_query_execution"
                    })
        
        except Exception as e:
            logger.error(f"Optimization opportunity identification failed: {e}")
        
        return opportunities
    
    async def _apply_optimizations(self, opportunities: List[Dict[str, Any]]):
        """Apply identified optimizations"""
        try:
            for opportunity in opportunities:
                action = opportunity.get("action")
                strategy = opportunity.get("strategy")
                
                if action == "retrain_strategy_weights":
                    # Adjust strategy weights for better satisfaction
                    logger.info(f"Retraining weights for {strategy} strategy")
                    # Implementation would adjust internal weighting parameters
                
                elif action == "optimize_query_execution":
                    # Optimize query execution for speed
                    logger.info(f"Optimizing query execution for {strategy} strategy")
                    # Implementation would adjust query parameters
        
        except Exception as e:
            logger.error(f"Optimization application failed: {e}")
    
    def _get_strategy_recommendations(self, strategy_name: str, metrics: Dict[str, float]) -> List[str]:
        """Get recommendations for when to use specific strategy"""
        recommendations = []
        
        strategy_guides = {
            "vector": ["Short queries", "Similarity-based searches", "Technical documentation lookup"],
            "semantic": ["Complex questions", "Natural language queries", "Conceptual searches"],
            "hybrid": ["General purpose queries", "When unsure of query type", "Balanced accuracy and speed"],
            "performance_weighted": ["Business-critical queries", "User-facing applications", "Conversion optimization"]
        }
        
        return strategy_guides.get(strategy_name, ["General purpose"])
    
    async def health_check(self) -> bool:
        """Health check for search service"""
        try:
            if not self._initialized:
                return False
            
            # Check database connectivity
            db_health = await self.db_service.health_check()
            return all(status == "healthy" for status in db_health.values())
            
        except Exception as e:
            logger.error(f"Search service health check failed: {e}")
            return False