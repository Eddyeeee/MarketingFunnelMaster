#!/usr/bin/env python3
"""
Knowledge Layer Integration Module
Connects extracted knowledge from books, courses, and videos to the A/B Testing Framework

This module enables:
- Loading conversion rules from knowledge extractions
- Generating A/B test hypotheses from book principles
- Applying proven conversion strategies to variant generation
- Continuous learning from test results back to knowledge base

Created: 2025-01-05
"""

import yaml
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeRule:
    """Represents a conversion rule from the knowledge layer"""
    rule_id: str
    name: str
    description: str
    conditions: List[str]
    actions: List[Dict[str, Any]]
    metrics: List[str]
    expected_impact: str
    source_book: str = ""
    source_principle: str = ""

@dataclass
class TestHypothesis:
    """A/B test hypothesis generated from knowledge rules"""
    hypothesis_id: str
    name: str
    hypothesis: str
    base_rule_id: str
    control_description: str
    variant_changes: List[Dict[str, Any]]
    success_metrics: Dict[str, Any]
    minimum_sample_size: int
    source_knowledge: str

class KnowledgeLayerIntegration:
    """
    Integrates extracted knowledge into the A/B Testing Framework
    """
    
    def __init__(self, knowledge_base_path: str = "knowledge-layer"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.loaded_rules: Dict[str, KnowledgeRule] = {}
        self.generated_hypotheses: Dict[str, TestHypothesis] = {}
        self.test_results_feedback: List[Dict[str, Any]] = []
        
        # Initialize knowledge base
        self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> None:
        """Load all conversion rules from the knowledge base"""
        try:
            rules_path = self.knowledge_base_path / "rules" / "conversion-rules.yaml"
            
            if rules_path.exists():
                with open(rules_path, 'r') as f:
                    rules_data = yaml.safe_load(f)
                
                # Load conversion rules
                for category, rules in rules_data.get('conversion_rules', {}).items():
                    for rule in rules:
                        knowledge_rule = KnowledgeRule(
                            rule_id=rule['rule_id'],
                            name=rule['name'],
                            description=rule['description'],
                            conditions=rule.get('conditions', []),
                            actions=rule.get('actions', []),
                            metrics=rule.get('metrics', []),
                            expected_impact=rule.get('expected_impact', 'Unknown'),
                            source_book=rules_data['metadata'].get('source_books', [''])[0],
                            source_principle=category
                        )
                        self.loaded_rules[rule['rule_id']] = knowledge_rule
                
                logger.info(f"Loaded {len(self.loaded_rules)} conversion rules from knowledge base")
            else:
                logger.warning(f"No conversion rules found at {rules_path}")
                
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def generate_test_config_from_knowledge(self, 
                                          target_metric: str = "conversion_rate",
                                          persona: Optional[str] = None,
                                          device_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate A/B test configuration based on knowledge rules
        
        Args:
            target_metric: Primary metric to optimize
            persona: Target persona (e.g., "TechEarlyAdopter")
            device_type: Target device type (e.g., "mobile")
        
        Returns:
            Test configuration for ABTestingFramework
        """
        try:
            # Find applicable rules based on conditions
            applicable_rules = self._find_applicable_rules(persona, device_type)
            
            if not applicable_rules:
                logger.warning("No applicable rules found for given conditions")
                return {}
            
            # Select the most impactful rule
            selected_rule = self._select_best_rule(applicable_rules, target_metric)
            
            # Generate test hypothesis
            hypothesis = self._generate_hypothesis_from_rule(selected_rule, persona, device_type)
            
            # Create test configuration
            test_config = {
                'name': f"Knowledge-Based Test: {selected_rule.name}",
                'description': f"Testing principle from {selected_rule.source_book}: {selected_rule.description}",
                'test_type': 'content_variant',
                'target_metric': target_metric,
                'minimum_sample_size': hypothesis.minimum_sample_size,
                'significance_threshold': 0.05,
                'personalization_context': {
                    'persona': persona,
                    'device_type': device_type,
                    'knowledge_rule_id': selected_rule.rule_id
                },
                'variant_generation_hints': {
                    'base_principle': selected_rule.source_principle,
                    'expected_changes': hypothesis.variant_changes,
                    'success_indicators': hypothesis.success_metrics
                }
            }
            
            # Store generated hypothesis
            self.generated_hypotheses[hypothesis.hypothesis_id] = hypothesis
            
            logger.info(f"Generated test config from knowledge rule: {selected_rule.rule_id}")
            return test_config
            
        except Exception as e:
            logger.error(f"Error generating test config from knowledge: {e}")
            return {}
    
    def enhance_variant_with_knowledge(self, 
                                     variant_data: Dict[str, Any],
                                     rule_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhance a variant with knowledge-based modifications
        
        Args:
            variant_data: Original variant data
            rule_id: Specific rule to apply (optional)
        
        Returns:
            Enhanced variant data
        """
        try:
            # Select rule if not specified
            if not rule_id:
                # Find the best matching rule based on variant type
                rule = self._match_rule_to_variant(variant_data)
            else:
                rule = self.loaded_rules.get(rule_id)
            
            if not rule:
                return variant_data
            
            # Apply rule actions to variant
            enhanced_data = variant_data.copy()
            
            for action in rule.actions:
                action_type = action.get('type')
                config = action.get('config', {})
                
                if action_type == 'content_placement':
                    enhanced_data['content_modifications'] = {
                        'position': config.get('position', 'above_fold'),
                        'prominence': config.get('prominence', 'high')
                    }
                
                elif action_type == 'copy_optimization':
                    enhanced_data['copy_style'] = {
                        'style': config.get('style', 'benefit_focused'),
                        'readability_target': config.get('readability_score', '>70')
                    }
                
                elif action_type == 'ui_adjustment':
                    enhanced_data['ui_modifications'] = {
                        'cta_size': config.get('cta_size', 'standard'),
                        'spacing': config.get('spacing', 'normal'),
                        'font_size': config.get('font_size', 'default')
                    }
            
            # Add knowledge metadata
            enhanced_data['knowledge_enhanced'] = {
                'rule_id': rule.rule_id,
                'rule_name': rule.name,
                'expected_impact': rule.expected_impact,
                'source': rule.source_book
            }
            
            logger.debug(f"Enhanced variant with knowledge rule: {rule.rule_id}")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error enhancing variant with knowledge: {e}")
            return variant_data
    
    def analyze_test_results_for_learning(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze A/B test results to extract learnings for the knowledge base
        
        Args:
            test_results: Test results from ABTestingFramework
        
        Returns:
            Learning insights to add to knowledge base
        """
        try:
            test_id = test_results.get('test_id')
            variant_metrics = test_results.get('variant_metrics', {})
            
            # Find the knowledge rule used in this test
            personalization_context = test_results.get('personalization_context', {})
            rule_id = personalization_context.get('knowledge_rule_id')
            
            if not rule_id or rule_id not in self.loaded_rules:
                return {'message': 'No knowledge rule associated with this test'}
            
            rule = self.loaded_rules[rule_id]
            
            # Analyze performance against expectations
            winning_variant = self._identify_winning_variant(variant_metrics)
            actual_impact = self._calculate_actual_impact(variant_metrics)
            
            # Generate learning insights
            learning_insights = {
                'test_id': test_id,
                'rule_id': rule_id,
                'rule_name': rule.name,
                'expected_impact': rule.expected_impact,
                'actual_impact': actual_impact,
                'performance_match': self._evaluate_performance_match(rule.expected_impact, actual_impact),
                'winning_variant': winning_variant,
                'key_learnings': self._extract_key_learnings(test_results, rule),
                'recommendation': self._generate_recommendation(actual_impact, rule),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Store feedback for continuous improvement
            self.test_results_feedback.append(learning_insights)
            
            # Update knowledge base if significant learning
            if learning_insights['performance_match'] != 'as_expected':
                self._update_knowledge_base(learning_insights)
            
            logger.info(f"Analyzed test results for rule {rule_id}: {learning_insights['performance_match']}")
            return learning_insights
            
        except Exception as e:
            logger.error(f"Error analyzing test results for learning: {e}")
            return {'error': str(e)}
    
    def get_applicable_rules_for_scenario(self, scenario: Dict[str, Any]) -> List[KnowledgeRule]:
        """
        Get all applicable knowledge rules for a given scenario
        
        Args:
            scenario: Dictionary containing persona, device_type, page_type, etc.
        
        Returns:
            List of applicable knowledge rules
        """
        persona = scenario.get('persona')
        device_type = scenario.get('device_type')
        page_type = scenario.get('page_type')
        
        applicable_rules = []
        
        for rule in self.loaded_rules.values():
            if self._rule_matches_scenario(rule, persona, device_type, page_type):
                applicable_rules.append(rule)
        
        # Sort by expected impact
        applicable_rules.sort(key=lambda r: self._parse_impact_percentage(r.expected_impact), reverse=True)
        
        return applicable_rules
    
    def export_test_hypotheses(self) -> List[Dict[str, Any]]:
        """
        Export all generated test hypotheses for A/B testing
        
        Returns:
            List of test hypotheses ready for implementation
        """
        hypotheses = []
        
        for hypothesis in self.generated_hypotheses.values():
            hypothesis_dict = asdict(hypothesis)
            hypothesis_dict['ready_for_testing'] = True
            hypothesis_dict['priority_score'] = self._calculate_hypothesis_priority(hypothesis)
            hypotheses.append(hypothesis_dict)
        
        # Sort by priority
        hypotheses.sort(key=lambda h: h['priority_score'], reverse=True)
        
        return hypotheses
    
    # =============================================================================
    # INTERNAL HELPER METHODS
    # =============================================================================
    
    def _find_applicable_rules(self, persona: Optional[str], device_type: Optional[str]) -> List[KnowledgeRule]:
        """Find rules that match the given conditions"""
        applicable_rules = []
        
        for rule in self.loaded_rules.values():
            # Check if rule conditions match
            conditions_met = True
            
            for condition in rule.conditions:
                if persona and f"persona == '{persona}'" in condition:
                    continue
                elif device_type and f"device_type == '{device_type}'" in condition:
                    continue
                elif "==" in condition and (persona or device_type):
                    # Condition doesn't match our criteria
                    conditions_met = False
                    break
            
            if conditions_met:
                applicable_rules.append(rule)
        
        return applicable_rules
    
    def _select_best_rule(self, rules: List[KnowledgeRule], target_metric: str) -> KnowledgeRule:
        """Select the best rule based on expected impact and relevance"""
        # Simple selection based on expected impact
        # In production, this would use ML to predict best rule
        best_rule = max(rules, key=lambda r: self._parse_impact_percentage(r.expected_impact))
        return best_rule
    
    def _parse_impact_percentage(self, impact_str: str) -> float:
        """Parse impact string to get percentage value"""
        import re
        match = re.search(r'(\d+)%', impact_str)
        if match:
            return float(match.group(1))
        return 0.0
    
    def _generate_hypothesis_from_rule(self, rule: KnowledgeRule, 
                                     persona: Optional[str], 
                                     device_type: Optional[str]) -> TestHypothesis:
        """Generate a test hypothesis from a knowledge rule"""
        hypothesis_id = f"HYPO-{rule.rule_id}-{uuid.uuid4().hex[:8]}"
        
        # Build hypothesis statement
        hypothesis_statement = f"Applying {rule.name} will improve conversion rate by {rule.expected_impact}"
        if persona:
            hypothesis_statement += f" for {persona} users"
        if device_type:
            hypothesis_statement += f" on {device_type} devices"
        
        # Extract variant changes from rule actions
        variant_changes = []
        for action in rule.actions:
            variant_changes.append({
                'type': action.get('type'),
                'config': action.get('config', {})
            })
        
        # Define success metrics
        success_metrics = {
            'primary': rule.metrics[0] if rule.metrics else 'conversion_rate',
            'secondary': rule.metrics[1:] if len(rule.metrics) > 1 else []
        }
        
        # Calculate sample size based on expected impact
        impact_pct = self._parse_impact_percentage(rule.expected_impact)
        minimum_sample_size = int(2000 / (impact_pct / 10)) if impact_pct > 0 else 2000
        
        return TestHypothesis(
            hypothesis_id=hypothesis_id,
            name=f"{rule.name} Test",
            hypothesis=hypothesis_statement,
            base_rule_id=rule.rule_id,
            control_description="Current version without knowledge-based optimizations",
            variant_changes=variant_changes,
            success_metrics=success_metrics,
            minimum_sample_size=minimum_sample_size,
            source_knowledge=f"{rule.source_book} - {rule.source_principle}"
        )
    
    def _match_rule_to_variant(self, variant_data: Dict[str, Any]) -> Optional[KnowledgeRule]:
        """Match a variant to the most appropriate knowledge rule"""
        variant_type = variant_data.get('type', '')
        
        # Simple matching based on variant type
        for rule in self.loaded_rules.values():
            for action in rule.actions:
                if action.get('type') in variant_type or variant_type in str(action):
                    return rule
        
        return None
    
    def _identify_winning_variant(self, variant_metrics: Dict[str, Any]) -> str:
        """Identify the winning variant from metrics"""
        best_variant = None
        best_conversion = 0.0
        
        for variant_id, metrics in variant_metrics.items():
            if isinstance(metrics, dict) and metrics.get('conversion_rate', 0) > best_conversion:
                best_conversion = metrics['conversion_rate']
                best_variant = variant_id
        
        return best_variant or 'no_winner'
    
    def _calculate_actual_impact(self, variant_metrics: Dict[str, Any]) -> str:
        """Calculate actual impact from test results"""
        control_metrics = None
        best_variant_metrics = None
        
        for variant_id, metrics in variant_metrics.items():
            if isinstance(metrics, dict):
                if 'control' in variant_id:
                    control_metrics = metrics
                elif not best_variant_metrics or metrics.get('conversion_rate', 0) > best_variant_metrics.get('conversion_rate', 0):
                    best_variant_metrics = metrics
        
        if control_metrics and best_variant_metrics:
            control_rate = control_metrics.get('conversion_rate', 0)
            variant_rate = best_variant_metrics.get('conversion_rate', 0)
            
            if control_rate > 0:
                impact_pct = ((variant_rate - control_rate) / control_rate) * 100
                return f"{impact_pct:.1f}% {'increase' if impact_pct > 0 else 'decrease'}"
        
        return "Unable to calculate"
    
    def _evaluate_performance_match(self, expected: str, actual: str) -> str:
        """Evaluate if actual performance matched expectations"""
        expected_pct = self._parse_impact_percentage(expected)
        actual_pct = self._parse_impact_percentage(actual)
        
        if abs(expected_pct - actual_pct) < 5:
            return "as_expected"
        elif actual_pct > expected_pct:
            return "exceeded_expectations"
        else:
            return "below_expectations"
    
    def _extract_key_learnings(self, test_results: Dict[str, Any], rule: KnowledgeRule) -> List[str]:
        """Extract key learnings from test results"""
        learnings = []
        
        # Add basic learnings
        insights = test_results.get('insights', [])
        if insights:
            learnings.extend(insights[:3])  # Top 3 insights
        
        # Add rule-specific learning
        learnings.append(f"Knowledge rule '{rule.name}' was tested in production")
        
        return learnings
    
    def _generate_recommendation(self, actual_impact: str, rule: KnowledgeRule) -> str:
        """Generate recommendation based on test results"""
        impact_pct = self._parse_impact_percentage(actual_impact)
        
        if impact_pct > 10:
            return f"Strongly recommend implementing {rule.name} across all similar pages"
        elif impact_pct > 5:
            return f"Recommend gradual rollout of {rule.name} with continued monitoring"
        elif impact_pct > 0:
            return f"Consider {rule.name} for specific high-value segments only"
        else:
            return f"Do not implement {rule.name} - explore alternative approaches"
    
    def _update_knowledge_base(self, learning_insights: Dict[str, Any]) -> None:
        """Update knowledge base with new learnings"""
        try:
            # Create learning record
            learning_record = {
                'learning_id': f"LEARN-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
                'source_test': learning_insights['test_id'],
                'rule_id': learning_insights['rule_id'],
                'performance_match': learning_insights['performance_match'],
                'actual_impact': learning_insights['actual_impact'],
                'key_learnings': learning_insights['key_learnings'],
                'timestamp': learning_insights['timestamp']
            }
            
            # Save to learnings file
            learnings_path = self.knowledge_base_path / "extracted" / "test_learnings.yaml"
            learnings_path.parent.mkdir(parents=True, exist_ok=True)
            
            existing_learnings = []
            if learnings_path.exists():
                with open(learnings_path, 'r') as f:
                    data = yaml.safe_load(f) or {}
                    existing_learnings = data.get('learnings', [])
            
            existing_learnings.append(learning_record)
            
            with open(learnings_path, 'w') as f:
                yaml.dump({
                    'metadata': {
                        'last_updated': datetime.utcnow().isoformat(),
                        'total_learnings': len(existing_learnings)
                    },
                    'learnings': existing_learnings
                }, f, default_flow_style=False)
            
            logger.info(f"Updated knowledge base with learning: {learning_record['learning_id']}")
            
        except Exception as e:
            logger.error(f"Error updating knowledge base: {e}")
    
    def _rule_matches_scenario(self, rule: KnowledgeRule, persona: Optional[str], 
                             device_type: Optional[str], page_type: Optional[str]) -> bool:
        """Check if a rule matches the given scenario"""
        for condition in rule.conditions:
            # Simple string matching for conditions
            if persona and persona not in condition:
                continue
            if device_type and device_type not in condition:
                continue
            if page_type and page_type not in condition:
                continue
            
            # If we get here, at least one condition is relevant
            return True
        
        # Rules without specific conditions are always applicable
        return len(rule.conditions) == 0
    
    def _calculate_hypothesis_priority(self, hypothesis: TestHypothesis) -> float:
        """Calculate priority score for a hypothesis"""
        # Base priority on expected impact and sample size efficiency
        impact = self._parse_impact_percentage(
            self.loaded_rules[hypothesis.base_rule_id].expected_impact
        )
        
        # Lower sample size requirement = higher priority
        sample_efficiency = 5000 / hypothesis.minimum_sample_size
        
        return impact * sample_efficiency