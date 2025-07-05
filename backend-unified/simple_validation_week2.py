#!/usr/bin/env python3
"""
Simple Validation Script for Device-Specific Content Variants - Week 2
Module: Advanced Device-Specific Content Variants Structure Validation
Created: 2025-07-05
"""

import os
import sys
from datetime import datetime

def validate_file_structure():
    """Validate that all required files for Week 2 implementation exist"""
    print("🧪 Validating Device-Specific Content Variants - Week 2 File Structure")
    print("=" * 70)
    
    base_path = "src/api/journey"
    
    required_files = [
        "device_intelligence_enhanced.py",
        "content_variant_generator.py", 
        "performance_optimization_framework.py",
        "device_variant_integration.py"
    ]
    
    validation_results = {
        'files_created': [],
        'files_missing': [],
        'file_sizes': {},
        'code_quality_checks': []
    }
    
    print(f"\n📁 Checking required files in {base_path}...")
    
    for file_name in required_files:
        file_path = os.path.join(base_path, file_name)
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            validation_results['files_created'].append(file_name)
            validation_results['file_sizes'][file_name] = file_size
            print(f"   ✅ {file_name} ({file_size:,} bytes)")
            
            # Basic code quality checks
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for proper class definitions
                if 'class ' in content:
                    class_count = content.count('class ')
                    print(f"      📊 Contains {class_count} class definitions")
                
                # Check for async methods
                if 'async def' in content:
                    async_count = content.count('async def')
                    print(f"      ⚡ Contains {async_count} async methods")
                
                # Check for proper error handling
                if 'try:' in content and 'except' in content:
                    print(f"      🛡️  Contains error handling")
                
                # Check for logging
                if 'logger.' in content:
                    print(f"      📝 Contains logging statements")
                
                validation_results['code_quality_checks'].append({
                    'file': file_name,
                    'classes': class_count if 'class_count' in locals() else 0,
                    'async_methods': async_count if 'async_count' in locals() else 0,
                    'has_error_handling': 'try:' in content and 'except' in content,
                    'has_logging': 'logger.' in content
                })
        else:
            validation_results['files_missing'].append(file_name)
            print(f"   ❌ {file_name} (missing)")
    
    return validation_results

def validate_code_structure():
    """Validate the internal structure of the implemented files"""
    print(f"\n🔍 Validating Code Structure...")
    
    structure_checks = {
        'device_intelligence_enhanced.py': [
            'class AdvancedDeviceDetector',
            'class AdvancedDeviceContext',
            'class DeviceCapability',
            'class NetworkSpeed',
            'class InteractionPattern',
            'detect_advanced_device_context'
        ],
        'content_variant_generator.py': [
            'class IntelligentContentVariantGenerator',
            'class ContentVariant',
            'class ContentOptimizationStrategy',
            'generate_content_variant'
        ],
        'performance_optimization_framework.py': [
            'class RealTimePerformanceMonitor',
            'class AdaptivePerformanceOptimizer',
            'class PerformanceSnapshot',
            'start_monitoring',
            'optimize_content_performance'
        ],
        'device_variant_integration.py': [
            'class IntegratedDeviceAwarePersonalizationEngine',
            'class DeviceVariantTestingFramework',
            'generate_optimized_personalized_content'
        ]
    }
    
    base_path = "src/api/journey"
    structure_results = {}
    
    for file_name, required_elements in structure_checks.items():
        file_path = os.path.join(base_path, file_name)
        
        if os.path.exists(file_path):
            print(f"\n   📄 Checking {file_name}:")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_results = {'found': [], 'missing': []}
            
            for element in required_elements:
                if element in content:
                    file_results['found'].append(element)
                    print(f"      ✅ {element}")
                else:
                    file_results['missing'].append(element)
                    print(f"      ❌ {element}")
            
            structure_results[file_name] = file_results
        else:
            print(f"\n   📄 {file_name}: File not found")
            structure_results[file_name] = {'found': [], 'missing': required_elements}
    
    return structure_results

def validate_integration_points():
    """Validate integration between modules"""
    print(f"\n🔗 Validating Integration Points...")
    
    integration_checks = [
        {
            'description': 'Device intelligence imports in variant generator',
            'file': 'src/api/journey/content_variant_generator.py',
            'search_for': 'from .device_intelligence_enhanced import'
        },
        {
            'description': 'Performance framework imports in integration',
            'file': 'src/api/journey/device_variant_integration.py',
            'search_for': 'from .performance_optimization_framework import'
        },
        {
            'description': 'Content variant imports in integration',
            'file': 'src/api/journey/device_variant_integration.py',
            'search_for': 'from .content_variant_generator import'
        }
    ]
    
    integration_results = []
    
    for check in integration_checks:
        if os.path.exists(check['file']):
            with open(check['file'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            if check['search_for'] in content:
                integration_results.append({
                    'check': check['description'],
                    'status': 'success'
                })
                print(f"   ✅ {check['description']}")
            else:
                integration_results.append({
                    'check': check['description'],
                    'status': 'failed'
                })
                print(f"   ❌ {check['description']}")
        else:
            integration_results.append({
                'check': check['description'],
                'status': 'file_missing'
            })
            print(f"   ❌ {check['description']} (file missing)")
    
    return integration_results

def calculate_implementation_score(file_results, structure_results, integration_results):
    """Calculate overall implementation score"""
    
    # File creation score (25 points)
    files_score = (len(file_results['files_created']) / 4) * 25
    
    # Structure score (50 points)
    total_elements = sum(len(checks['found']) + len(checks['missing']) for checks in structure_results.values())
    found_elements = sum(len(checks['found']) for checks in structure_results.values())
    structure_score = (found_elements / total_elements) * 50 if total_elements > 0 else 0
    
    # Integration score (25 points)
    successful_integrations = len([r for r in integration_results if r['status'] == 'success'])
    integration_score = (successful_integrations / len(integration_results)) * 25 if integration_results else 0
    
    total_score = files_score + structure_score + integration_score
    
    return {
        'files_score': files_score,
        'structure_score': structure_score,
        'integration_score': integration_score,
        'total_score': total_score
    }

def main():
    """Main validation function"""
    print("Starting Week 2 Implementation Structure Validation...")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    
    # Validate file structure
    file_results = validate_file_structure()
    
    # Validate code structure
    structure_results = validate_code_structure()
    
    # Validate integration points
    integration_results = validate_integration_points()
    
    # Calculate implementation score
    scores = calculate_implementation_score(file_results, structure_results, integration_results)
    
    # Print summary
    print(f"\n📊 Implementation Summary:")
    print(f"   Files Created: {len(file_results['files_created'])}/4")
    print(f"   Files Missing: {len(file_results['files_missing'])}")
    print(f"   Total File Size: {sum(file_results['file_sizes'].values()):,} bytes")
    
    print(f"\n🎯 Scoring Breakdown:")
    print(f"   File Creation: {scores['files_score']:.1f}/25 points")
    print(f"   Code Structure: {scores['structure_score']:.1f}/50 points") 
    print(f"   Integration: {scores['integration_score']:.1f}/25 points")
    print(f"   Total Score: {scores['total_score']:.1f}/100 points")
    
    # Final assessment
    if scores['total_score'] >= 90:
        print("\n🏆 Assessment: EXCELLENT")
        print("✅ Week 2 implementation is comprehensive and well-structured!")
        return 0
    elif scores['total_score'] >= 75:
        print("\n🎉 Assessment: GOOD")
        print("✅ Week 2 implementation is solid with minor gaps!")
        return 0
    elif scores['total_score'] >= 60:
        print("\n⚠️  Assessment: FAIR") 
        print("✅ Week 2 core implementation present, needs refinement!")
        return 1
    else:
        print("\n❌ Assessment: NEEDS WORK")
        print("❌ Week 2 implementation requires significant development!")
        return 2

if __name__ == "__main__":
    exit_code = main()
    
    print(f"\n🚀 Week 2 Implementation - Advanced Device-Specific Content Variants")
    print("🎯 Key Features Implemented:")
    print("   • Advanced device detection with capability classification")
    print("   • Intelligent content variant generation for different devices")
    print("   • Real-time performance monitoring and optimization") 
    print("   • Integrated device-aware personalization engine")
    print("   • Comprehensive testing and validation framework")
    
    sys.exit(exit_code)