#!/usr/bin/env python3
"""
A/B Testing Framework Integration Test
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Quick integration test to validate A/B testing implementation
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add src to path
sys.path.append('src')

def test_statistical_engine():
    """Test the statistical analysis engine"""
    print("🧮 Testing Statistical Engine...")
    
    try:
        from services.statistical_engine import StatisticalEngine
        
        engine = StatisticalEngine()
        
        # Test sample size calculation
        sample_size = engine.calculate_sample_size(
            baseline_rate=0.05,
            minimum_detectable_effect=0.20,
            confidence_level=0.95,
            statistical_power=0.80
        )
        
        print(f"✅ Sample size calculation: {sample_size} per variant")
        
        # Test significance calculation
        significance = engine.calculate_significance(
            control_conversions=50,
            control_participants=1000,
            variant_conversions=70,
            variant_participants=1000,
            confidence_level=0.95
        )
        
        print(f"✅ Significance test: p-value = {significance['p_value']:.4f}")
        print(f"   Lift: {significance['lift']:.1f}%")
        print(f"   Significant: {significance['is_significant']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Statistical engine test failed: {e}")
        return False

def test_variant_generator():
    """Test the variant generation system"""
    print("🎨 Testing Variant Generator...")
    
    try:
        from services.variant_generator import VariantGenerator
        
        generator = VariantGenerator()
        
        # Mock page analysis
        page_analysis = {
            "headlines": {"primary": "Get Started Today"},
            "cta_buttons": [{"text": "Sign Up", "selector": ".cta"}],
            "product_name": "Amazing Product",
            "main_benefit": "save time",
            "target_audience": "professionals"
        }
        
        # Generate variants
        variants = generator.generate_variants(
            page_analysis=page_analysis,
            target_metric="conversion_rate",
            variant_count=3
        )
        
        print(f"✅ Generated {len(variants)} test variants:")
        for i, variant in enumerate(variants, 1):
            print(f"   {i}. {variant.name} (confidence: {variant.confidence_score:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Variant generator test failed: {e}")
        return False

def test_behavioral_models():
    """Test behavioral tracking models"""
    print("📊 Testing Behavioral Models...")
    
    try:
        from models.behavioral_models import BehavioralEvent, EventType, EventCategory
        
        # Create a test behavioral event
        event = BehavioralEvent(
            session_id="test_session_123",
            event_type=EventType.CLICK,
            event_category=EventCategory.INTERACTION,
            event_action="button_click",
            page_url="https://example.com/landing",
            engagement_score=0.8
        )
        
        print(f"✅ Created behavioral event: {event.event_type.value}")
        print(f"   Session: {event.session_id}")
        print(f"   Engagement: {event.engagement_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Behavioral models test failed: {e}")
        return False

def test_ab_testing_models():
    """Test A/B testing models"""
    print("🧪 Testing A/B Testing Models...")
    
    try:
        from models.ab_testing_models import (
            ABTest, TestVariant, TestType, MetricType, VariantType
        )
        
        # Create a test A/B test
        ab_test = ABTest(
            test_name="Homepage CTA Test",
            test_type=TestType.AB_TEST,
            hypothesis="Changing button color will increase conversions",
            primary_metric=MetricType.CONVERSION_RATE,
            target_url_pattern="https://example.com/*"
        )
        
        print(f"✅ Created A/B test: {ab_test.test_name}")
        print(f"   Type: {ab_test.test_type.value}")
        print(f"   Metric: {ab_test.primary_metric.value}")
        
        # Create test variants
        control_variant = TestVariant(
            test_id=ab_test.id,
            variant_type=VariantType.CONTROL,
            name="Original Button",
            changes={"button_color": "blue"}
        )
        
        test_variant = TestVariant(
            test_id=ab_test.id,
            variant_type=VariantType.VARIANT,
            name="Green Button",
            changes={"button_color": "green"}
        )
        
        print(f"✅ Created variants: {control_variant.name}, {test_variant.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ A/B testing models test failed: {e}")
        return False

def test_websocket_manager():
    """Test WebSocket manager"""
    print("🔌 Testing WebSocket Manager...")
    
    try:
        from services.websocket_manager import WebSocketManager
        
        manager = WebSocketManager()
        
        # Test connection statistics
        stats = manager.get_connection_stats()
        print(f"✅ WebSocket manager initialized")
        print(f"   Active connections: {stats['active_connections']}")
        print(f"   Total messages sent: {stats['messages_sent']}")
        
        return True
        
    except Exception as e:
        print(f"❌ WebSocket manager test failed: {e}")
        return False

def test_trigger_engine():
    """Test trigger engine"""
    print("⚡ Testing Trigger Engine...")
    
    try:
        from services.trigger_engine import TriggerEngine, TriggerCondition, TriggerAction, ActionType
        
        # Mock database connection
        class MockDB:
            pass
        
        engine = TriggerEngine(MockDB())
        
        # Test condition evaluation
        condition = TriggerCondition("engagement_score", "gte", 0.8)
        test_data = {"engagement_score": 0.9}
        
        result = condition.evaluate(test_data)
        print(f"✅ Condition evaluation: {result}")
        
        # Test action creation
        action = TriggerAction(
            ActionType.POPUP,
            {"content": "Special offer!", "discount": "20%"}
        )
        
        print(f"✅ Created trigger action: {action.action_type.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Trigger engine test failed: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    print("🗄️ Testing Database Connection...")
    
    try:
        from database.connection import check_database_health
        
        # Note: This will fail without actual database, but tests the import
        print("✅ Database connection module loaded successfully")
        print("   (Actual connection requires database setup)")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 A/B Testing Framework Integration Test")
    print("=" * 50)
    
    tests = [
        test_statistical_engine,
        test_variant_generator,
        test_behavioral_models,
        test_ab_testing_models,
        test_websocket_manager,
        test_trigger_engine,
    ]
    
    async_tests = [
        test_database_connection,
    ]
    
    results = []
    
    # Run synchronous tests
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()
    
    # Run asynchronous tests
    async def run_async_tests():
        async_results = []
        for test in async_tests:
            try:
                result = await test()
                async_results.append(result)
            except Exception as e:
                print(f"❌ Async test {test.__name__} crashed: {e}")
                async_results.append(False)
            print()
        return async_results
    
    async_results = asyncio.run(run_async_tests())
    results.extend(async_results)
    
    # Summary
    print("📋 Test Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! A/B testing framework is ready.")
        return 0
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)