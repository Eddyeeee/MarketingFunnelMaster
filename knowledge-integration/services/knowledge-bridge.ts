/**
 * Knowledge Bridge Service - Pilot Implementation
 * Integrates "Making Websites Win" principles with A/B Testing Framework
 * Non-invasive enhancement with fallback safety
 */

import * as yaml from 'js-yaml';
import * as fs from 'fs';
import * as path from 'path';

interface ConversionPrinciple {
  id: string;
  name: string;
  description: string;
  confidence_score: number;
  application: any;
  ab_testing_rules: any;
}

interface EnhancementResult {
  enhanced: boolean;
  principles_applied: string[];
  confidence_score: number;
  fallback_used: boolean;
  original_config: any;
  enhanced_config: any;
}

interface KnowledgeConfig {
  enabled: boolean;
  confidence_threshold: number;
  fallback_enabled: boolean;
  strict_mode: boolean;
}

class KnowledgeBridge {
  private conversionRules: any = null;
  private config: KnowledgeConfig;
  private isInitialized = false;

  constructor() {
    this.config = {
      enabled: true,
      confidence_threshold: 0.7,
      fallback_enabled: true,
      strict_mode: false
    };
  }

  /**
   * Initialize the knowledge bridge with conversion rules
   */
  async initialize(): Promise<void> {
    try {
      const rulesPath = path.join(__dirname, '../books/making-websites-win/conversion-rules.yaml');
      const rulesContent = fs.readFileSync(rulesPath, 'utf8');
      this.conversionRules = yaml.load(rulesContent);
      this.isInitialized = true;
      
      console.log('✅ Knowledge Bridge initialized with Making Websites Win principles');
    } catch (error) {
      console.error('❌ Failed to initialize Knowledge Bridge:', error);
      this.isInitialized = false;
    }
  }

  /**
   * Enhance A/B test configuration with conversion principles
   */
  async enhanceABTest(originalConfig: any): Promise<EnhancementResult> {
    // Safety check: return original if not enabled or initialized
    if (!this.config.enabled || !this.isInitialized || !this.conversionRules) {
      return this.createFallbackResult(originalConfig, 'bridge_not_ready');
    }

    try {
      const enhancement = await this.applyConversionPrinciples(originalConfig);
      
      return {
        enhanced: true,
        principles_applied: enhancement.applied_principles,
        confidence_score: enhancement.confidence,
        fallback_used: false,
        original_config: originalConfig,
        enhanced_config: enhancement.config
      };

    } catch (error) {
      console.error('Enhancement failed, using fallback:', error);
      return this.createFallbackResult(originalConfig, 'enhancement_error');
    }
  }

  /**
   * Apply conversion principles to A/B test configuration
   */
  private async applyConversionPrinciples(config: any): Promise<any> {
    const principles = this.conversionRules.conversion_principles;
    const appliedPrinciples: string[] = [];
    let enhancedConfig = { ...config };
    let totalConfidence = 0;

    // Apply clarity over creativity principle
    if (this.shouldApplyPrinciple('clarity_over_creativity', config)) {
      enhancedConfig = this.applyClarityPrinciple(enhancedConfig, principles.clarity_over_creativity);
      appliedPrinciples.push('clarity_over_creativity');
      totalConfidence += principles.clarity_over_creativity.confidence_score;
    }

    // Apply friction reduction principle
    if (this.shouldApplyPrinciple('friction_reduction', config)) {
      enhancedConfig = this.applyFrictionReduction(enhancedConfig, principles.friction_reduction);
      appliedPrinciples.push('friction_reduction');
      totalConfidence += principles.friction_reduction.confidence_score;
    }

    // Apply single element testing principle
    if (this.shouldApplyPrinciple('single_element_testing', config)) {
      enhancedConfig = this.applySingleElementTesting(enhancedConfig, principles.single_element_testing);
      appliedPrinciples.push('single_element_testing');
      totalConfidence += principles.single_element_testing.confidence_score;
    }

    // Apply mobile-first optimization
    if (this.shouldApplyPrinciple('mobile_first_optimization', config)) {
      enhancedConfig = this.applyMobileFirstOptimization(enhancedConfig, principles.mobile_first_optimization);
      appliedPrinciples.push('mobile_first_optimization');
      totalConfidence += principles.mobile_first_optimization.confidence_score;
    }

    // Apply statistical significance requirements
    if (this.shouldApplyPrinciple('statistical_significance', config)) {
      enhancedConfig = this.applyStatisticalSignificance(enhancedConfig, principles.statistical_significance);
      appliedPrinciples.push('statistical_significance');
      totalConfidence += principles.statistical_significance.confidence_score;
    }

    const averageConfidence = appliedPrinciples.length > 0 ? totalConfidence / appliedPrinciples.length : 0;

    return {
      config: enhancedConfig,
      applied_principles: appliedPrinciples,
      confidence: averageConfidence
    };
  }

  /**
   * Apply clarity over creativity principle
   */
  private applyClarityPrinciple(config: any, principle: ConversionPrinciple): any {
    const enhanced = { ...config };

    // Add clarity-focused variant suggestions
    if (!enhanced.variant_suggestions) enhanced.variant_suggestions = [];
    
    enhanced.variant_suggestions.push({
      type: 'clarity_enhancement',
      principle: 'clarity_over_creativity',
      suggestions: [
        'Test simplified headline with direct benefit statement',
        'Create variant with 5th-grade reading level',
        'Remove jargon and replace with plain language'
      ]
    });

    // Enhance success metrics weighting
    if (!enhanced.success_metrics) enhanced.success_metrics = {};
    enhanced.success_metrics.mobile_weight = principle.ab_testing_rules.success_metrics.mobile_weight;

    // Add clarity validation
    enhanced.validation_rules = enhanced.validation_rules || [];
    enhanced.validation_rules.push({
      rule: 'clarity_check',
      description: 'Ensure variants prioritize clarity over creativity'
    });

    return enhanced;
  }

  /**
   * Apply friction reduction principle
   */
  private applyFrictionReduction(config: any, principle: ConversionPrinciple): any {
    const enhanced = { ...config };

    // Add friction reduction suggestions
    if (!enhanced.variant_suggestions) enhanced.variant_suggestions = [];
    
    enhanced.variant_suggestions.push({
      type: 'friction_reduction',
      principle: 'friction_reduction',
      suggestions: [
        'Test reduced form fields (remove non-essential)',
        'Create single-step variant of multi-step process',
        'Test optional vs required field variations'
      ]
    });

    // Add friction analysis
    enhanced.analysis_focus = enhanced.analysis_focus || [];
    enhanced.analysis_focus.push('form_abandonment', 'completion_rate', 'step_drop_off');

    return enhanced;
  }

  /**
   * Apply single element testing principle
   */
  private applySingleElementTesting(config: any, principle: ConversionPrinciple): any {
    const enhanced = { ...config };

    // Add single element validation
    enhanced.validation_rules = enhanced.validation_rules || [];
    enhanced.validation_rules.push({
      rule: 'single_element_only',
      description: 'Ensure only one element differs between variants',
      strict: principle.ab_testing_rules.enforcement.strict_mode
    });

    // Add attribution clarity
    enhanced.attribution_tracking = {
      enabled: true,
      require_clear_mapping: true,
      reject_multi_variable: principle.ab_testing_rules.enforcement.auto_reject_multi_variable
    };

    return enhanced;
  }

  /**
   * Apply mobile-first optimization principle
   */
  private applyMobileFirstOptimization(config: any, principle: ConversionPrinciple): any {
    const enhanced = { ...config };

    // Mobile-first metric weighting
    enhanced.metric_weighting = {
      mobile_conversion_rate: principle.ab_testing_rules.metric_weighting.mobile_conversion_rate,
      mobile_engagement: principle.ab_testing_rules.metric_weighting.mobile_engagement,
      mobile_load_time: principle.ab_testing_rules.metric_weighting.mobile_load_time
    };

    // Mobile requirements
    enhanced.variant_requirements = enhanced.variant_requirements || {};
    enhanced.variant_requirements.mobile_responsive = true;
    enhanced.variant_requirements.touch_optimized = true;
    enhanced.variant_requirements.mobile_load_time_max = principle.ab_testing_rules.variant_requirements.mobile_load_time_max;

    return enhanced;
  }

  /**
   * Apply statistical significance requirements
   */
  private applyStatisticalSignificance(config: any, principle: ConversionPrinciple): any {
    const enhanced = { ...config };

    // Statistical requirements
    enhanced.statistical_requirements = {
      confidence_level: principle.ab_testing_rules.significance_requirements.confidence_level,
      minimum_sample_size: principle.ab_testing_rules.significance_requirements.minimum_sample_size,
      minimum_conversions: principle.ab_testing_rules.significance_requirements.minimum_conversions,
      minimum_test_duration: principle.ab_testing_rules.significance_requirements.minimum_test_duration
    };

    // Early stopping prevention
    enhanced.early_stopping = {
      enabled: principle.ab_testing_rules.early_stopping.enabled,
      exception_criteria: principle.ab_testing_rules.early_stopping.exception_criteria
    };

    return enhanced;
  }

  /**
   * Determine if a principle should be applied
   */
  private shouldApplyPrinciple(principleId: string, config: any): boolean {
    const principle = this.conversionRules.conversion_principles[principleId];
    if (!principle) return false;

    // Check confidence threshold
    if (principle.confidence_score < this.config.confidence_threshold) {
      return false;
    }

    // Add specific logic for when each principle applies
    switch (principleId) {
      case 'clarity_over_creativity':
        return config.test_type === 'headline' || config.test_type === 'value_proposition';
      
      case 'friction_reduction':
        return config.test_type === 'form' || config.test_type === 'checkout';
      
      case 'single_element_testing':
        return true; // Always apply for good test design
      
      case 'mobile_first_optimization':
        return true; // Always apply for mobile performance
      
      case 'statistical_significance':
        return true; // Always apply for valid results
      
      default:
        return false;
    }
  }

  /**
   * Create fallback result when enhancement fails
   */
  private createFallbackResult(originalConfig: any, reason: string): EnhancementResult {
    console.log(`Using fallback for A/B test enhancement: ${reason}`);
    
    return {
      enhanced: false,
      principles_applied: [],
      confidence_score: 0,
      fallback_used: true,
      original_config: originalConfig,
      enhanced_config: originalConfig
    };
  }

  /**
   * Enable/disable knowledge enhancement
   */
  setEnabled(enabled: boolean): void {
    this.config.enabled = enabled;
    console.log(`Knowledge Bridge ${enabled ? 'enabled' : 'disabled'}`);
  }

  /**
   * Emergency rollback - disable all enhancements
   */
  emergencyRollback(): void {
    this.config.enabled = false;
    console.log('🚨 EMERGENCY ROLLBACK: Knowledge Bridge disabled');
  }

  /**
   * Get current enhancement status
   */
  getStatus(): any {
    return {
      initialized: this.isInitialized,
      enabled: this.config.enabled,
      confidence_threshold: this.config.confidence_threshold,
      principles_loaded: this.conversionRules ? Object.keys(this.conversionRules.conversion_principles || {}) : [],
      fallback_enabled: this.config.fallback_enabled
    };
  }
}

// Export singleton instance
export const knowledgeBridge = new KnowledgeBridge();

// Export class for testing
export { KnowledgeBridge };

// Export types
export type { EnhancementResult, ConversionPrinciple, KnowledgeConfig };