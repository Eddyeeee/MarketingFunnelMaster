# ML Models for Personalization Engine Enhancement - Phase 3
# Module: Phase 3 - Personalization Enhancement
# Created: 2025-07-04

import asyncio
import json
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib
import pandas as pd
from ..config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# ENHANCED ML MODELS FOR PERSONALIZATION
# =============================================================================

@dataclass
class PersonalizationFeatures:
    """Feature set for personalization ML models"""
    persona_type: str
    journey_stage: str
    device_type: str
    session_duration: float
    interaction_count: int
    scroll_depth: float
    conversion_probability: float
    time_of_day: int
    day_of_week: int
    is_returning_visitor: bool
    engagement_score: float
    content_consumption_rate: float
    source_channel: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for ML processing"""
        return {
            'persona_type': self.persona_type,
            'journey_stage': self.journey_stage,
            'device_type': self.device_type,
            'session_duration': self.session_duration,
            'interaction_count': self.interaction_count,
            'scroll_depth': self.scroll_depth,
            'conversion_probability': self.conversion_probability,
            'time_of_day': self.time_of_day,
            'day_of_week': self.day_of_week,
            'is_returning_visitor': self.is_returning_visitor,
            'engagement_score': self.engagement_score,
            'content_consumption_rate': self.content_consumption_rate,
            'source_channel': self.source_channel
        }

class PersonalizationModel:
    """Enhanced ML model for personalization decisions"""
    
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.feature_scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.model_version = "v2.0"
        self.performance_metrics = {}
        
    async def score_variant(self, features: Dict[str, Any], variant_content: Dict[str, Any]) -> float:
        """Score a content variant based on features"""
        try:
            # Extract features for ML model
            feature_vector = self._extract_features(features, variant_content)
            
            if not self.is_trained:
                # Use heuristic scoring if model not trained
                return self._heuristic_scoring(features, variant_content)
            
            # Scale features
            scaled_features = self.feature_scaler.transform([feature_vector])
            
            # Predict score
            score = self.model.predict(scaled_features)[0]
            
            # Normalize to 0-1 range
            score = max(0.0, min(1.0, score))
            
            logger.debug(f"ML model scored variant: {score}")
            return score
            
        except Exception as e:
            logger.error(f"Error scoring variant: {str(e)}")
            return self._heuristic_scoring(features, variant_content)
    
    def _extract_features(self, session_features: Dict[str, Any], variant_content: Dict[str, Any]) -> List[float]:
        """Extract numeric features for ML model"""
        features = []
        
        # Encode categorical features
        persona_encoded = self._encode_feature('persona_type', session_features.get('persona_type', 'unknown'))
        stage_encoded = self._encode_feature('journey_stage', session_features.get('journey_stage', 'awareness'))
        device_encoded = self._encode_feature('device_type', session_features.get('device_type', 'mobile'))
        
        features.extend([
            persona_encoded,
            stage_encoded,
            device_encoded,
            session_features.get('session_duration', 0),
            session_features.get('conversion_probability', 0.5),
            len(variant_content.get('hero_message', '')),
            len(variant_content.get('call_to_action', '')),
            len(variant_content.get('trust_signals', [])),
            1.0 if variant_content.get('scarcity_trigger') else 0.0,
            1.0 if variant_content.get('social_proof') else 0.0
        ])
        
        return features
    
    def _encode_feature(self, feature_name: str, value: str) -> float:
        """Encode categorical feature"""
        if feature_name not in self.label_encoders:
            self.label_encoders[feature_name] = LabelEncoder()
            # Fit with common values
            common_values = {
                'persona_type': ['TechEarlyAdopter', 'RemoteDad', 'StudentHustler', 'BusinessOwner'],
                'journey_stage': ['awareness', 'consideration', 'decision', 'conversion'],
                'device_type': ['mobile', 'tablet', 'desktop']
            }
            self.label_encoders[feature_name].fit(common_values.get(feature_name, [value]))
        
        try:
            return float(self.label_encoders[feature_name].transform([value])[0])
        except ValueError:
            return 0.0
    
    def _heuristic_scoring(self, features: Dict[str, Any], variant_content: Dict[str, Any]) -> float:
        """Fallback heuristic scoring when ML model unavailable"""
        score = 0.5  # Base score
        
        # Persona-based adjustments
        persona = features.get('persona_type', 'unknown')
        if persona == 'TechEarlyAdopter':
            if 'tech' in variant_content.get('hero_message', '').lower():
                score += 0.2
        elif persona == 'StudentHustler':
            if any(word in variant_content.get('hero_message', '').lower() 
                   for word in ['student', 'save', 'discount', 'cheap']):
                score += 0.2
        
        # Stage-based adjustments
        stage = features.get('journey_stage', 'awareness')
        if stage == 'decision':
            if variant_content.get('scarcity_trigger'):
                score += 0.15
        elif stage == 'awareness':
            if len(variant_content.get('trust_signals', [])) > 2:
                score += 0.1
        
        # Device-based adjustments
        device = features.get('device_type', 'mobile')
        if device == 'mobile':
            if len(variant_content.get('hero_message', '')) < 50:
                score += 0.1
        elif device == 'desktop':
            if len(variant_content.get('hero_message', '')) > 30:
                score += 0.1
        
        return max(0.0, min(1.0, score))
    
    async def train_model(self, training_data: List[Dict[str, Any]]):
        """Train the personalization model"""
        try:
            if len(training_data) < 10:
                logger.warning("Insufficient training data for ML model")
                return
            
            # Prepare training data
            X = []
            y = []
            
            for record in training_data:
                features = self._extract_features(record['features'], record['variant_content'])
                X.append(features)
                y.append(record['performance_score'])
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            X_train_scaled = self.feature_scaler.fit_transform(X_train)
            X_test_scaled = self.feature_scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            mse = np.mean((y_test - y_pred) ** 2)
            
            self.performance_metrics = {
                'mse': mse,
                'r2_score': self.model.score(X_test_scaled, y_test),
                'training_samples': len(training_data),
                'last_trained': datetime.utcnow().isoformat()
            }
            
            self.is_trained = True
            logger.info(f"ML model trained successfully. MSE: {mse:.4f}")
            
        except Exception as e:
            logger.error(f"Error training ML model: {str(e)}")
            self.is_trained = False
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.feature_scaler,
                'encoders': self.label_encoders,
                'is_trained': self.is_trained,
                'version': self.model_version,
                'metrics': self.performance_metrics
            }
            joblib.dump(model_data, filepath)
            logger.info(f"Model saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.feature_scaler = model_data['scaler']
            self.label_encoders = model_data['encoders']
            self.is_trained = model_data['is_trained']
            self.model_version = model_data['version']
            self.performance_metrics = model_data['metrics']
            logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.is_trained = False


class RecommendationEngine:
    """Enhanced recommendation engine for personalization"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.recommendation_patterns = {}
        
    async def score_recommendation(self, session_features: Dict[str, Any], recommendation: Dict[str, Any]) -> float:
        """Score a recommendation based on session context"""
        try:
            # Extract features
            feature_vector = self._extract_recommendation_features(session_features, recommendation)
            
            if not self.is_trained:
                return self._heuristic_recommendation_scoring(session_features, recommendation)
            
            # Scale features
            scaled_features = self.feature_scaler.transform([feature_vector])
            
            # Predict probability
            probabilities = self.model.predict_proba(scaled_features)[0]
            
            # Return probability of positive outcome
            return probabilities[1] if len(probabilities) > 1 else probabilities[0]
            
        except Exception as e:
            logger.error(f"Error scoring recommendation: {str(e)}")
            return self._heuristic_recommendation_scoring(session_features, recommendation)
    
    def _extract_recommendation_features(self, session_features: Dict[str, Any], recommendation: Dict[str, Any]) -> List[float]:
        """Extract features for recommendation scoring"""
        features = []
        
        # Session features
        features.extend([
            self._encode_feature('persona_type', session_features.get('persona_type', 'unknown')),
            self._encode_feature('journey_stage', session_features.get('journey_stage', 'awareness')),
            self._encode_feature('device_type', session_features.get('device_type', 'mobile')),
            session_features.get('conversion_probability', 0.5)
        ])
        
        # Recommendation features
        features.extend([
            self._encode_feature('recommendation_type', recommendation.get('type', 'unknown')),
            self._encode_feature('priority', recommendation.get('priority', 'medium')),
            len(recommendation.get('content', '')),
            recommendation.get('expected_impact', 0.0)
        ])
        
        return features
    
    def _encode_feature(self, feature_name: str, value: str) -> float:
        """Encode categorical feature for recommendations"""
        if feature_name not in self.label_encoders:
            self.label_encoders[feature_name] = LabelEncoder()
            # Fit with common values
            common_values = {
                'persona_type': ['TechEarlyAdopter', 'RemoteDad', 'StudentHustler', 'BusinessOwner'],
                'journey_stage': ['awareness', 'consideration', 'decision', 'conversion'],
                'device_type': ['mobile', 'tablet', 'desktop'],
                'recommendation_type': ['content_enhancement', 'social_proof', 'comparison_tools', 'trust_building', 'scarcity_activation', 'friction_reduction'],
                'priority': ['low', 'medium', 'high']
            }
            self.label_encoders[feature_name].fit(common_values.get(feature_name, [value]))
        
        try:
            return float(self.label_encoders[feature_name].transform([value])[0])
        except ValueError:
            return 0.0
    
    def _heuristic_recommendation_scoring(self, session_features: Dict[str, Any], recommendation: Dict[str, Any]) -> float:
        """Fallback heuristic scoring for recommendations"""
        score = 0.5  # Base score
        
        # Priority-based adjustment
        priority = recommendation.get('priority', 'medium')
        if priority == 'high':
            score += 0.2
        elif priority == 'low':
            score -= 0.1
        
        # Stage-based relevance
        stage = session_features.get('journey_stage', 'awareness')
        rec_type = recommendation.get('type', 'unknown')
        
        stage_relevance = {
            'awareness': ['content_enhancement', 'social_proof'],
            'consideration': ['comparison_tools', 'trust_building'],
            'decision': ['scarcity_activation', 'friction_reduction']
        }
        
        if rec_type in stage_relevance.get(stage, []):
            score += 0.15
        
        # Device-based relevance
        device = session_features.get('device_type', 'mobile')
        if device == 'mobile' and rec_type == 'friction_reduction':
            score += 0.1
        elif device == 'desktop' and rec_type == 'comparison_tools':
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    async def train_recommendation_model(self, training_data: List[Dict[str, Any]]):
        """Train the recommendation model"""
        try:
            if len(training_data) < 10:
                logger.warning("Insufficient training data for recommendation model")
                return
            
            # Prepare training data
            X = []
            y = []
            
            for record in training_data:
                features = self._extract_recommendation_features(record['session_features'], record['recommendation'])
                X.append(features)
                y.append(record['success'])  # Binary success indicator
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            X_train_scaled = self.feature_scaler.fit_transform(X_train)
            X_test_scaled = self.feature_scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.is_trained = True
            logger.info(f"Recommendation model trained successfully. Accuracy: {accuracy:.4f}")
            
        except Exception as e:
            logger.error(f"Error training recommendation model: {str(e)}")
            self.is_trained = False


class RealTimeOptimizer:
    """Real-time optimization engine for personalization"""
    
    def __init__(self):
        self.optimization_rules = {}
        self.performance_cache = {}
        self.learning_rate = 0.01
        
    async def optimize_content_real_time(self, session_id: str, current_performance: Dict[str, Any], content: Dict[str, Any]) -> Dict[str, Any]:
        """Apply real-time content optimizations"""
        try:
            optimizations = []
            
            # Analyze current performance
            engagement_score = current_performance.get('engagement_score', 0.5)
            conversion_probability = current_performance.get('conversion_probability', 0.5)
            
            # Apply optimization rules
            if engagement_score < 0.4:
                # Low engagement - enhance visual appeal
                optimizations.append({
                    'type': 'visual_enhancement',
                    'action': 'add_emojis_and_formatting',
                    'expected_impact': 0.15
                })
            
            if conversion_probability < 0.3:
                # Low conversion - add urgency
                optimizations.append({
                    'type': 'urgency_boost',
                    'action': 'add_scarcity_trigger',
                    'expected_impact': 0.20
                })
            
            # Cache performance for learning
            self.performance_cache[session_id] = {
                'timestamp': datetime.utcnow(),
                'performance': current_performance,
                'optimizations': optimizations
            }
            
            return {
                'optimizations': optimizations,
                'total_expected_impact': sum(opt['expected_impact'] for opt in optimizations),
                'optimization_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in real-time optimization: {str(e)}")
            return {'optimizations': [], 'total_expected_impact': 0.0}
    
    async def learn_from_performance(self, session_id: str, final_performance: Dict[str, Any]):
        """Learn from final performance to improve future optimizations"""
        try:
            if session_id not in self.performance_cache:
                return
            
            cached_data = self.performance_cache[session_id]
            initial_performance = cached_data['performance']
            applied_optimizations = cached_data['optimizations']
            
            # Calculate actual impact
            actual_impact = final_performance.get('engagement_score', 0) - initial_performance.get('engagement_score', 0)
            
            # Update optimization rules based on performance
            for optimization in applied_optimizations:
                opt_type = optimization['type']
                expected_impact = optimization['expected_impact']
                
                if opt_type not in self.optimization_rules:
                    self.optimization_rules[opt_type] = {'success_rate': 0.5, 'avg_impact': 0.1}
                
                # Update success metrics
                if actual_impact > 0:
                    self.optimization_rules[opt_type]['success_rate'] += self.learning_rate
                    self.optimization_rules[opt_type]['avg_impact'] += self.learning_rate * actual_impact
                else:
                    self.optimization_rules[opt_type]['success_rate'] -= self.learning_rate
                
                # Clamp values
                self.optimization_rules[opt_type]['success_rate'] = max(0.0, min(1.0, self.optimization_rules[opt_type]['success_rate']))
                self.optimization_rules[opt_type]['avg_impact'] = max(0.0, min(1.0, self.optimization_rules[opt_type]['avg_impact']))
            
            # Clean up cache
            del self.performance_cache[session_id]
            
            logger.debug(f"Learned from session {session_id}: actual_impact={actual_impact}")
            
        except Exception as e:
            logger.error(f"Error learning from performance: {str(e)}")


class ContentVariantGenerator:
    """Advanced content variant generation for A/B testing"""
    
    def __init__(self):
        self.variant_strategies = {}
        self.performance_history = {}
        
    async def generate_variants(self, base_content: Dict[str, Any], variant_count: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple content variants for A/B testing"""
        try:
            variants = []
            
            # Include base content as control
            variants.append({
                **base_content,
                'variant_id': 'control',
                'variant_type': 'control'
            })
            
            # Generate test variants
            for i in range(variant_count):
                variant = await self._create_variant(base_content, f'variant_{i+1}')
                variants.append(variant)
            
            return variants
            
        except Exception as e:
            logger.error(f"Error generating variants: {str(e)}")
            return [base_content]
    
    async def _create_variant(self, base_content: Dict[str, Any], variant_id: str) -> Dict[str, Any]:
        """Create a specific variant with strategic modifications"""
        variant = base_content.copy()
        variant['variant_id'] = variant_id
        
        # Apply variant-specific modifications
        if variant_id == 'variant_1':
            # Urgency-focused variant
            variant['hero_message'] = self._add_urgency_to_message(variant.get('hero_message', ''))
            variant['scarcity_trigger'] = '⚡ Limited Time: 50% OFF - Only 24 hours left!'
            variant['variant_type'] = 'urgency_focused'
            
        elif variant_id == 'variant_2':
            # Social proof-focused variant
            variant['hero_message'] = self._add_social_proof_to_message(variant.get('hero_message', ''))
            variant['social_proof'] = '🎉 Join 50,000+ satisfied customers!'
            variant['variant_type'] = 'social_proof_focused'
            
        elif variant_id == 'variant_3':
            # Benefit-focused variant
            variant['hero_message'] = self._add_benefits_to_message(variant.get('hero_message', ''))
            variant['trust_signals'] = variant.get('trust_signals', []) + ['💰 Save time and money', '📈 Proven results']
            variant['variant_type'] = 'benefit_focused'
        
        return variant
    
    def _add_urgency_to_message(self, message: str) -> str:
        """Add urgency elements to message"""
        urgency_prefixes = ['⚡ Act Fast:', '🔥 Limited Time:', '⏰ Hurry:']
        if not any(prefix in message for prefix in urgency_prefixes):
            return f"⚡ Act Fast: {message}"
        return message
    
    def _add_social_proof_to_message(self, message: str) -> str:
        """Add social proof elements to message"""
        social_prefixes = ['🎉 Trending:', '👥 Join thousands:', '⭐ Top-rated:']
        if not any(prefix in message for prefix in social_prefixes):
            return f"🎉 Trending: {message}"
        return message
    
    def _add_benefits_to_message(self, message: str) -> str:
        """Add benefit elements to message"""
        benefit_prefixes = ['💰 Save more:', '📈 Get results:', '🚀 Boost performance:']
        if not any(prefix in message for prefix in benefit_prefixes):
            return f"💰 Save more: {message}"
        return message
    
    async def optimize_variants_from_performance(self, variant_performance: Dict[str, Dict[str, Any]]):
        """Optimize future variant generation based on performance data"""
        try:
            # Analyze which variant strategies perform best
            best_performing_strategy = None
            best_performance = 0
            
            for variant_id, performance in variant_performance.items():
                if variant_id == 'control':
                    continue
                    
                engagement_score = performance.get('engagement_score', 0)
                conversion_rate = performance.get('conversion_rate', 0)
                combined_score = engagement_score * 0.6 + conversion_rate * 0.4
                
                if combined_score > best_performance:
                    best_performance = combined_score
                    best_performing_strategy = performance.get('variant_type', 'unknown')
            
            # Update strategy weights
            if best_performing_strategy:
                if best_performing_strategy not in self.variant_strategies:
                    self.variant_strategies[best_performing_strategy] = {'weight': 1.0, 'success_count': 0}
                
                self.variant_strategies[best_performing_strategy]['weight'] += 0.1
                self.variant_strategies[best_performing_strategy]['success_count'] += 1
                
                logger.info(f"Optimized variant strategy: {best_performing_strategy} (weight: {self.variant_strategies[best_performing_strategy]['weight']:.2f})")
            
        except Exception as e:
            logger.error(f"Error optimizing variants from performance: {str(e)}")


# =============================================================================
# MODEL FACTORY AND MANAGEMENT
# =============================================================================

class MLModelManager:
    """Centralized manager for all ML models"""
    
    def __init__(self):
        self.personalization_model = PersonalizationModel()
        self.recommendation_engine = RecommendationEngine()
        self.real_time_optimizer = RealTimeOptimizer()
        self.variant_generator = ContentVariantGenerator()
        self.model_registry = {}
        
    async def initialize_models(self):
        """Initialize all ML models"""
        try:
            # Try to load existing models
            model_paths = {
                'personalization': '/tmp/personalization_model.pkl',
                'recommendation': '/tmp/recommendation_model.pkl'
            }
            
            for model_type, path in model_paths.items():
                try:
                    if model_type == 'personalization':
                        self.personalization_model.load_model(path)
                    elif model_type == 'recommendation':
                        self.recommendation_engine.load_model(path)
                except Exception as e:
                    logger.warning(f"Could not load {model_type} model: {str(e)}")
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {str(e)}")
    
    async def get_model_health(self) -> Dict[str, Any]:
        """Get health status of all models"""
        return {
            'personalization_model': {
                'is_trained': self.personalization_model.is_trained,
                'version': self.personalization_model.model_version,
                'performance': self.personalization_model.performance_metrics
            },
            'recommendation_engine': {
                'is_trained': self.recommendation_engine.is_trained,
                'patterns_learned': len(self.recommendation_engine.recommendation_patterns)
            },
            'real_time_optimizer': {
                'rules_learned': len(self.real_time_optimizer.optimization_rules),
                'active_sessions': len(self.real_time_optimizer.performance_cache)
            },
            'variant_generator': {
                'strategies_learned': len(self.variant_generator.variant_strategies),
                'performance_history': len(self.variant_generator.performance_history)
            }
        }

# Global model manager instance
ml_model_manager = MLModelManager()