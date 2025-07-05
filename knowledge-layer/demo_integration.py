#!/usr/bin/env python3
"""
Knowledge Layer Integration Demonstration
Shows how extracted knowledge from "Making Websites Win" enhances A/B Testing

This demo:
1. Loads conversion principles from the book
2. Generates A/B test hypotheses
3. Creates enhanced test variants
4. Shows how test results feed back into the knowledge base

Created: 2025-01-05
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from integration.knowledge_layer_integration import KnowledgeLayerIntegration

async def main():
    """Demonstrate Knowledge Layer integration with A/B Testing"""
    
    print("=" * 80)
    print("KNOWLEDGE LAYER INTEGRATION DEMO")
    print("Source: 'Making Websites Win' by Dr. Karl Blanks & Ben Jesson")
    print("=" * 80)
    print()
    
    # Initialize Knowledge Layer Integration
    knowledge_integration = KnowledgeLayerIntegration()
    
    # 1. Show loaded conversion rules
    print("1. LOADED CONVERSION RULES FROM KNOWLEDGE BASE")
    print("-" * 50)
    for rule_id, rule in knowledge_integration.loaded_rules.items():
        print(f"Rule: {rule.name} ({rule_id})")
        print(f"  Description: {rule.description}")
        print(f"  Expected Impact: {rule.expected_impact}")
        print(f"  Source: {rule.source_principle}")
        print()
    
    # 2. Generate A/B test for mobile users
    print("\n2. GENERATING A/B TEST FOR MOBILE USERS")
    print("-" * 50)
    
    mobile_test_config = knowledge_integration.generate_test_config_from_knowledge(
        target_metric="conversion_rate",
        persona="TechEarlyAdopter",
        device_type="mobile"
    )
    
    print("Generated Test Configuration:")
    print(json.dumps(mobile_test_config, indent=2))
    
    # 3. Show applicable rules for different scenarios
    print("\n\n3. APPLICABLE RULES FOR DIFFERENT SCENARIOS")
    print("-" * 50)
    
    scenarios = [
        {"persona": "RemoteDad", "device_type": "desktop", "page_type": "landing"},
        {"persona": "StudentHustler", "device_type": "mobile", "page_type": "pricing"},
        {"persona": "BusinessOwner", "device_type": "tablet", "page_type": "landing"}
    ]
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario}")
        applicable_rules = knowledge_integration.get_applicable_rules_for_scenario(scenario)
        print(f"Found {len(applicable_rules)} applicable rules:")
        for rule in applicable_rules[:3]:  # Top 3
            print(f"  - {rule.name}: {rule.expected_impact}")
    
    # 4. Enhance a variant with knowledge
    print("\n\n4. ENHANCING VARIANT WITH KNOWLEDGE")
    print("-" * 50)
    
    sample_variant = {
        "variant_id": "test_variant_1",
        "type": "content_variant",
        "changes": ["headline", "cta_button"]
    }
    
    enhanced_variant = knowledge_integration.enhance_variant_with_knowledge(
        sample_variant,
        rule_id="VP-001"  # Value Proposition rule
    )
    
    print("Original Variant:")
    print(json.dumps(sample_variant, indent=2))
    print("\nEnhanced Variant:")
    print(json.dumps(enhanced_variant, indent=2))
    
    # 5. Simulate test results and learning
    print("\n\n5. SIMULATING TEST RESULTS AND LEARNING")
    print("-" * 50)
    
    # Simulate test results
    simulated_results = {
        "test_id": "test_123",
        "test_name": "Knowledge-Based Test: 5-Second Value Clear",
        "personalization_context": {
            "knowledge_rule_id": "VP-001"
        },
        "variant_metrics": {
            "control": {
                "conversion_rate": 0.025,  # 2.5%
                "engagement_score": 0.45,
                "sample_size": 1000
            },
            "variant_1": {
                "conversion_rate": 0.032,  # 3.2% (28% improvement)
                "engagement_score": 0.52,
                "sample_size": 1000
            }
        },
        "insights": [
            "Clear value proposition increased conversions by 28%",
            "Mobile users responded particularly well to simplified messaging",
            "5-second comprehension test validated - 85% understood value"
        ]
    }
    
    learning_insights = knowledge_integration.analyze_test_results_for_learning(simulated_results)
    
    print("Learning Insights:")
    print(json.dumps(learning_insights, indent=2))
    
    # 6. Export prioritized test hypotheses
    print("\n\n6. PRIORITIZED TEST HYPOTHESES")
    print("-" * 50)
    
    hypotheses = knowledge_integration.export_test_hypotheses()
    
    print(f"Generated {len(hypotheses)} test hypotheses:")
    for i, hypothesis in enumerate(hypotheses[:5], 1):  # Top 5
        print(f"\n{i}. {hypothesis['name']}")
        print(f"   Hypothesis: {hypothesis['hypothesis']}")
        print(f"   Priority Score: {hypothesis['priority_score']:.2f}")
        print(f"   Min Sample Size: {hypothesis['minimum_sample_size']}")
        print(f"   Source: {hypothesis['source_knowledge']}")
    
    # 7. Integration with existing A/B Testing Framework
    print("\n\n7. INTEGRATION POINTS WITH A/B TESTING FRAMEWORK")
    print("-" * 50)
    
    integration_points = {
        "1. Test Creation": {
            "Method": "generate_test_config_from_knowledge()",
            "Purpose": "Generate test configs based on proven principles",
            "Example": "VP-001 rule → Value Proposition A/B test"
        },
        "2. Variant Enhancement": {
            "Method": "enhance_variant_with_knowledge()",
            "Purpose": "Apply book principles to variant generation",
            "Example": "Mobile optimization rules for thumb-friendly CTAs"
        },
        "3. Results Analysis": {
            "Method": "analyze_test_results_for_learning()",
            "Purpose": "Feed test results back to knowledge base",
            "Example": "28% conversion lift validates VP-001 principle"
        },
        "4. Continuous Learning": {
            "Method": "Knowledge base updates",
            "Purpose": "Refine principles based on real-world results",
            "Example": "Adjust expected impact based on actual performance"
        }
    }
    
    for point, details in integration_points.items():
        print(f"\n{point}:")
        for key, value in details.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE - Knowledge Layer is ready for integration!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())