/**
 * A/B Testing Hooks - Non-invasive integration with existing framework
 * Enhances A/B tests with "Making Websites Win" principles
 * Maintains complete fallback to original system
 */

import { knowledgeBridge, EnhancementResult } from '../services/knowledge-bridge';

interface ABTestConfig {
  test_name: string;
  test_type: string;
  variants: any[];
  success_metrics: string[];
  target_audience?: string;
  duration_days?: number;
  traffic_split?: number[];
}

interface EnhancedABTestConfig extends ABTestConfig {
  knowledge_enhanced: boolean;
  enhancement_details?: EnhancementResult;
  fallback_config: ABTestConfig;
}

/**
 * Main hook function to enhance A/B test configurations
 * Called before test creation in the existing framework
 */
export async function enhanceABTestConfig(originalConfig: ABTestConfig): Promise<EnhancedABTestConfig> {
  try {
    // Initialize knowledge bridge if not already done
    if (!knowledgeBridge.getStatus().initialized) {
      await knowledgeBridge.initialize();
    }

    // Apply knowledge enhancement
    const enhancement = await knowledgeBridge.enhanceABTest(originalConfig);

    // Return enhanced configuration with fallback
    return {
      ...enhancement.enhanced_config,
      knowledge_enhanced: enhancement.enhanced,
      enhancement_details: enhancement,
      fallback_config: originalConfig
    };

  } catch (error) {
    console.error('A/B Test enhancement failed, using original config:', error);
    
    // Complete fallback to original configuration
    return {
      ...originalConfig,
      knowledge_enhanced: false,
      enhancement_details: {
        enhanced: false,
        principles_applied: [],
        confidence_score: 0,
        fallback_used: true,
        original_config: originalConfig,
        enhanced_config: originalConfig
      },
      fallback_config: originalConfig
    };
  }
}

/**
 * Hook for variant generation with conversion principles
 */
export function generateConversionOptimizedVariants(baseVariant: any, testType: string): any[] {
  try {
    const variants = [baseVariant]; // Always include original

    // Apply Making Websites Win principles for variant generation
    switch (testType) {
      case 'headline':
        variants.push(...generateClarityVariants(baseVariant));
        break;
      
      case 'form':
        variants.push(...generateFrictionReductionVariants(baseVariant));
        break;
      
      case 'landing_page':
        variants.push(...generateMobileFirstVariants(baseVariant));
        break;
      
      default:
        // Apply general conversion principles
        variants.push(...generateGeneralOptimizedVariants(baseVariant));
    }

    return variants;

  } catch (error) {
    console.error('Variant generation failed, using base variant only:', error);
    return [baseVariant]; // Fallback to original
  }
}

/**
 * Generate clarity-focused variants (Principle 1: Clarity Over Creativity)
 */
function generateClarityVariants(baseVariant: any): any[] {
  return [
    {
      ...baseVariant,
      name: `${baseVariant.name}_clarity_enhanced`,
      changes: {
        ...baseVariant.changes,
        headline_style: 'direct_benefit',
        reading_level: 'grade_5',
        remove_jargon: true
      },
      principle_applied: 'clarity_over_creativity'
    },
    {
      ...baseVariant,
      name: `${baseVariant.name}_simple_language`,
      changes: {
        ...baseVariant.changes,
        word_choice: 'simple_common_words',
        sentence_structure: 'short_sentences',
        benefit_focus: true
      },
      principle_applied: 'clarity_over_creativity'
    }
  ];
}

/**
 * Generate friction reduction variants (Principle 2: Remove Friction)
 */
function generateFrictionReductionVariants(baseVariant: any): any[] {
  return [
    {
      ...baseVariant,
      name: `${baseVariant.name}_reduced_fields`,
      changes: {
        ...baseVariant.changes,
        form_fields: 'essential_only',
        optional_fields: 'mark_optional',
        progress_indicator: true
      },
      principle_applied: 'friction_reduction'
    },
    {
      ...baseVariant,
      name: `${baseVariant.name}_single_step`,
      changes: {
        ...baseVariant.changes,
        process_steps: 'combine_steps',
        inline_validation: true,
        auto_complete: true
      },
      principle_applied: 'friction_reduction'
    }
  ];
}

/**
 * Generate mobile-first variants (Principle 4: Mobile-First Optimization)
 */
function generateMobileFirstVariants(baseVariant: any): any[] {
  return [
    {
      ...baseVariant,
      name: `${baseVariant.name}_mobile_optimized`,
      changes: {
        ...baseVariant.changes,
        layout: 'mobile_first',
        touch_targets: 'minimum_44px',
        load_time_target: '3_seconds'
      },
      principle_applied: 'mobile_first_optimization'
    }
  ];
}

/**
 * Generate general optimized variants
 */
function generateGeneralOptimizedVariants(baseVariant: any): any[] {
  return [
    {
      ...baseVariant,
      name: `${baseVariant.name}_conversion_optimized`,
      changes: {
        ...baseVariant.changes,
        optimization_focus: 'conversion_rate',
        statistical_power: 'high',
        mobile_priority: true
      },
      principle_applied: 'general_optimization'
    }
  ];
}

/**
 * Hook for statistical significance validation
 */
export function validateStatisticalRequirements(testResults: any): any {
  try {
    const requirements = {
      confidence_level: 0.95,
      minimum_sample_size: 1000,
      minimum_conversions: 50,
      minimum_test_duration: 7
    };

    const validation = {
      is_valid: true,
      issues: [] as string[],
      recommendations: [] as string[]
    };

    // Check confidence level
    if (testResults.confidence_level < requirements.confidence_level) {
      validation.is_valid = false;
      validation.issues.push(`Confidence level ${testResults.confidence_level} below required ${requirements.confidence_level}`);
      validation.recommendations.push('Continue test until 95% confidence achieved');
    }

    // Check sample size
    if (testResults.sample_size < requirements.minimum_sample_size) {
      validation.is_valid = false;
      validation.issues.push(`Sample size ${testResults.sample_size} below required ${requirements.minimum_sample_size}`);
      validation.recommendations.push('Increase traffic or extend test duration');
    }

    // Check conversions
    if (testResults.conversions < requirements.minimum_conversions) {
      validation.is_valid = false;
      validation.issues.push(`Conversions ${testResults.conversions} below required ${requirements.minimum_conversions}`);
      validation.recommendations.push('Continue test to achieve minimum conversions');
    }

    // Check test duration
    if (testResults.duration_days < requirements.minimum_test_duration) {
      validation.is_valid = false;
      validation.issues.push(`Test duration ${testResults.duration_days} days below required ${requirements.minimum_test_duration}`);
      validation.recommendations.push('Run test for minimum 7 days to account for weekly patterns');
    }

    return {
      ...testResults,
      statistical_validation: validation,
      principle_applied: 'statistical_significance'
    };

  } catch (error) {
    console.error('Statistical validation failed:', error);
    return testResults; // Return original results on error
  }
}

/**
 * Hook for mobile-first metric weighting
 */
export function applyMobileFirstMetrics(metrics: any): any {
  try {
    const mobileWeights = {
      mobile_conversion_rate: 2.0,
      mobile_engagement: 1.5,
      mobile_load_time: 2.0
    };

    const weightedMetrics = { ...metrics };

    // Apply mobile-first weighting
    Object.keys(mobileWeights).forEach(metric => {
      if (metrics[metric] !== undefined) {
        weightedMetrics[`${metric}_weighted`] = metrics[metric] * mobileWeights[metric];
      }
    });

    // Calculate overall mobile performance score
    weightedMetrics.mobile_performance_score = (
      (weightedMetrics.mobile_conversion_rate_weighted || 0) +
      (weightedMetrics.mobile_engagement_weighted || 0) +
      (weightedMetrics.mobile_load_time_weighted || 0)
    ) / 3;

    return {
      ...weightedMetrics,
      principle_applied: 'mobile_first_optimization',
      original_metrics: metrics
    };

  } catch (error) {
    console.error('Mobile metric weighting failed:', error);
    return metrics; // Return original metrics on error
  }
}

/**
 * Emergency rollback function
 */
export function emergencyRollback(): void {
  try {
    knowledgeBridge.emergencyRollback();
    console.log('🚨 A/B Testing hooks emergency rollback completed');
  } catch (error) {
    console.error('Emergency rollback failed:', error);
  }
}

/**
 * Get enhancement status for monitoring
 */
export function getEnhancementStatus(): any {
  try {
    return {
      knowledge_bridge_status: knowledgeBridge.getStatus(),
      hooks_active: true,
      last_check: new Date().toISOString()
    };
  } catch (error) {
    return {
      knowledge_bridge_status: { error: 'Status check failed' },
      hooks_active: false,
      last_check: new Date().toISOString(),
      error: error.message
    };
  }
}

// Export types
export type { ABTestConfig, EnhancedABTestConfig };