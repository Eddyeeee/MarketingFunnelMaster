/**
 * Analytics Intelligence Hook v2.0
 * React hook for intelligent analytics tracking
 * 
 * Module 3B Week 2 - Analytics Integration
 */

'use client';

import { useCallback, useEffect, useRef } from 'react';
import { useIntelligence } from './use-intelligence';
import { analyticsIntelligenceBridge } from '@/lib/analytics-intelligence-bridge';
import { PersonaType } from '@/types';

interface UseAnalyticsIntelligenceReturn {
  // Core tracking methods
  trackEvent: (eventName: string, properties?: Record<string, any>) => void;
  trackPersonaDetection: (persona: PersonaType, confidence: number) => void;
  trackComponentEngagement: (componentType: string, engagementScore: number) => void;
  trackConversionEvent: (componentType: string, conversionValue: number) => void;
  trackPerformanceMetric: (componentType: string, performanceValue: number) => void;
  
  // Intelligence-specific tracking
  trackOptimizationApplied: (optimizationType: string, componentType: string) => void;
  trackPersonaCorrection: (predictedPersona: PersonaType, actualPersona: PersonaType) => void;
  trackIntentEscalation: (fromIntent: string, toIntent: string) => void;
  
  // Performance tracking
  trackComponentLoad: (componentType: string, loadTime: number) => void;
  trackComponentError: (componentType: string, error: Error) => void;
  trackUserInteraction: (componentType: string, interactionType: string, value?: number) => void;
  
  // Real-time insights
  getRealTimeInsights: () => any;
  getPersonaPerformance: (persona: PersonaType) => any;
  getDeviceOptimizationInsights: () => any;
  
  // Utility methods
  setUserId: (userId: string) => void;
  flushPendingEvents: () => void;
}

export function useAnalyticsIntelligence(): UseAnalyticsIntelligenceReturn {
  const { persona, confidence, device, intent } = useIntelligence();
  const lastPersonaRef = useRef<PersonaType>('unknown');
  const lastIntentRef = useRef<string>('awareness');
  const componentLoadTimesRef = useRef<Map<string, number>>(new Map());

  // Track persona changes
  useEffect(() => {
    if (persona !== lastPersonaRef.current && confidence > 50) {
      analyticsIntelligenceBridge.trackIntelligenceEvent({
        event: 'persona_detection',
        properties: {
          previous_persona: lastPersonaRef.current,
          new_persona: persona,
          confidence_score: confidence,
          detection_method: 'automatic'
        }
      });
      lastPersonaRef.current = persona;
    }
  }, [persona, confidence]);

  // Track intent changes
  useEffect(() => {
    if (intent !== lastIntentRef.current) {
      analyticsIntelligenceBridge.trackIntelligenceEvent({
        event: 'intent_change',
        properties: {
          previous_intent: lastIntentRef.current,
          new_intent: intent,
          persona: persona,
          confidence: confidence
        }
      });
      lastIntentRef.current = intent;
    }
  }, [intent, persona, confidence]);

  // Core tracking methods
  const trackEvent = useCallback((eventName: string, properties?: Record<string, any>) => {
    analyticsIntelligenceBridge.trackIntelligenceEvent({
      event: eventName,
      properties: {
        ...properties,
        tracked_at: Date.now(),
        page_url: window.location.href,
        referrer: document.referrer
      }
    });
  }, []);

  const trackPersonaDetection = useCallback((detectedPersona: PersonaType, confidenceScore: number) => {
    analyticsIntelligenceBridge.trackPersonaAccuracy(detectedPersona);
    trackEvent('persona_detected', {
      detected_persona: detectedPersona,
      confidence_score: confidenceScore,
      detection_timestamp: Date.now()
    });
  }, [trackEvent]);

  const trackComponentEngagement = useCallback((componentType: string, engagementScore: number) => {
    analyticsIntelligenceBridge.trackComponentPerformance(componentType, 'engagement', engagementScore);
    trackEvent('component_engagement', {
      component_type: componentType,
      engagement_score: engagementScore,
      persona: persona,
      device: device
    });
  }, [trackEvent, persona, device]);

  const trackConversionEvent = useCallback((componentType: string, conversionValue: number) => {
    analyticsIntelligenceBridge.trackComponentPerformance(componentType, 'conversion', conversionValue);
    trackEvent('conversion_event', {
      component_type: componentType,
      conversion_value: conversionValue,
      persona: persona,
      device: device,
      intent: intent
    });
  }, [trackEvent, persona, device, intent]);

  const trackPerformanceMetric = useCallback((componentType: string, performanceValue: number) => {
    analyticsIntelligenceBridge.trackComponentPerformance(componentType, 'performance', performanceValue);
    trackEvent('performance_metric', {
      component_type: componentType,
      performance_value: performanceValue,
      device: device
    });
  }, [trackEvent, device]);

  // Intelligence-specific tracking
  const trackOptimizationApplied = useCallback((optimizationType: string, componentType: string) => {
    trackEvent('optimization_applied', {
      optimization_type: optimizationType,
      component_type: componentType,
      persona: persona,
      device: device,
      confidence: confidence
    });
  }, [trackEvent, persona, device, confidence]);

  const trackPersonaCorrection = useCallback((predictedPersona: PersonaType, actualPersona: PersonaType) => {
    analyticsIntelligenceBridge.trackPersonaAccuracy(predictedPersona, actualPersona);
    trackEvent('persona_correction', {
      predicted_persona: predictedPersona,
      actual_persona: actualPersona,
      correction_source: 'user_feedback',
      previous_confidence: confidence
    });
  }, [trackEvent, confidence]);

  const trackIntentEscalation = useCallback((fromIntent: string, toIntent: string) => {
    trackEvent('intent_escalation', {
      from_intent: fromIntent,
      to_intent: toIntent,
      persona: persona,
      device: device,
      escalation_trigger: 'user_behavior'
    });
  }, [trackEvent, persona, device]);

  // Performance tracking
  const trackComponentLoad = useCallback((componentType: string, loadTime: number) => {
    componentLoadTimesRef.current.set(componentType, loadTime);
    trackPerformanceMetric(componentType, loadTime);
    
    trackEvent('component_load', {
      component_type: componentType,
      load_time: loadTime,
      performance_rating: loadTime < 100 ? 'excellent' : loadTime < 300 ? 'good' : 'poor'
    });
  }, [trackPerformanceMetric, trackEvent]);

  const trackComponentError = useCallback((componentType: string, error: Error) => {
    trackEvent('component_error', {
      component_type: componentType,
      error_message: error.message,
      error_stack: error.stack,
      persona: persona,
      device: device,
      timestamp: Date.now()
    });
  }, [trackEvent, persona, device]);

  const trackUserInteraction = useCallback((
    componentType: string, 
    interactionType: string, 
    value?: number
  ) => {
    trackEvent('user_interaction', {
      component_type: componentType,
      interaction_type: interactionType,
      interaction_value: value,
      persona: persona,
      device: device,
      intent: intent,
      timestamp: Date.now()
    });

    // Track engagement score based on interaction type
    const engagementScore = calculateEngagementScore(interactionType, value);
    if (engagementScore > 0) {
      trackComponentEngagement(componentType, engagementScore);
    }
  }, [trackEvent, trackComponentEngagement, persona, device, intent]);

  // Real-time insights
  const getRealTimeInsights = useCallback(() => {
    return analyticsIntelligenceBridge.getRealTimeInsights();
  }, []);

  const getPersonaPerformance = useCallback((targetPersona: PersonaType) => {
    return analyticsIntelligenceBridge.getPersonaPerformanceMetrics(targetPersona);
  }, []);

  const getDeviceOptimizationInsights = useCallback(() => {
    return analyticsIntelligenceBridge.getDeviceOptimizationInsights(device);
  }, [device]);

  // Utility methods
  const setUserId = useCallback((userId: string) => {
    analyticsIntelligenceBridge.setUserId(userId);
    trackEvent('user_identified', {
      user_id: userId,
      persona: persona,
      confidence: confidence
    });
  }, [trackEvent, persona, confidence]);

  const flushPendingEvents = useCallback(() => {
    // Force flush any pending analytics data
    trackEvent('manual_flush_requested');
  }, [trackEvent]);

  return {
    // Core tracking methods
    trackEvent,
    trackPersonaDetection,
    trackComponentEngagement,
    trackConversionEvent,
    trackPerformanceMetric,
    
    // Intelligence-specific tracking
    trackOptimizationApplied,
    trackPersonaCorrection,
    trackIntentEscalation,
    
    // Performance tracking
    trackComponentLoad,
    trackComponentError,
    trackUserInteraction,
    
    // Real-time insights
    getRealTimeInsights,
    getPersonaPerformance,
    getDeviceOptimizationInsights,
    
    // Utility methods
    setUserId,
    flushPendingEvents
  };
}

/**
 * Hook for component-specific analytics tracking
 */
export function useComponentAnalytics(componentType: string) {
  const analytics = useAnalyticsIntelligence();
  const mountTimeRef = useRef<number>(Date.now());
  const interactionCountRef = useRef<number>(0);
  const engagementStartRef = useRef<number>(Date.now());

  // Track component mount
  useEffect(() => {
    const mountTime = Date.now() - mountTimeRef.current;
    analytics.trackComponentLoad(componentType, mountTime);

    return () => {
      // Track component unmount and engagement duration
      const engagementDuration = Date.now() - engagementStartRef.current;
      analytics.trackEvent('component_unmount', {
        component_type: componentType,
        engagement_duration: engagementDuration,
        interaction_count: interactionCountRef.current
      });
    };
  }, [analytics, componentType]);

  // Component-specific tracking methods
  const trackInteraction = useCallback((interactionType: string, value?: number) => {
    interactionCountRef.current++;
    analytics.trackUserInteraction(componentType, interactionType, value);
  }, [analytics, componentType]);

  const trackError = useCallback((error: Error) => {
    analytics.trackComponentError(componentType, error);
  }, [analytics, componentType]);

  const trackOptimization = useCallback((optimizationType: string) => {
    analytics.trackOptimizationApplied(optimizationType, componentType);
  }, [analytics, componentType]);

  const trackConversion = useCallback((value: number = 1) => {
    analytics.trackConversionEvent(componentType, value);
  }, [analytics, componentType]);

  return {
    trackInteraction,
    trackError,
    trackOptimization,
    trackConversion,
    getComponentLoadTime: () => Date.now() - mountTimeRef.current,
    getInteractionCount: () => interactionCountRef.current
  };
}

/**
 * Hook for A/B testing with intelligent analytics
 */
export function useIntelligentABTesting(testName: string, variants: string[]) {
  const { persona, device, confidence } = useIntelligence();
  const analytics = useAnalyticsIntelligence();
  
  // Select variant based on persona and device
  const selectedVariant = useCallback(() => {
    // Intelligent variant selection based on persona
    const personaVariantMap: Record<PersonaType, number> = {
      'TechEarlyAdopter': 0,
      'RemoteDad': 1,
      'StudentHustler': 0,
      'BusinessOwner': 1,
      'unknown': Math.floor(Math.random() * variants.length)
    };

    const variantIndex = confidence > 70 
      ? personaVariantMap[persona] || 0
      : Math.floor(Math.random() * variants.length);

    return variants[variantIndex] || variants[0];
  }, [persona, confidence, variants]);

  const variant = selectedVariant();

  // Track variant assignment
  useEffect(() => {
    analytics.trackEvent('ab_test_variant_assigned', {
      test_name: testName,
      variant: variant,
      persona: persona,
      device: device,
      confidence: confidence,
      selection_method: confidence > 70 ? 'intelligent' : 'random'
    });
  }, [analytics, testName, variant, persona, device, confidence]);

  const trackVariantConversion = useCallback((conversionValue: number = 1) => {
    analytics.trackEvent('ab_test_conversion', {
      test_name: testName,
      variant: variant,
      conversion_value: conversionValue,
      persona: persona,
      device: device
    });
  }, [analytics, testName, variant, persona, device]);

  return {
    variant,
    trackConversion: trackVariantConversion
  };
}

// Utility function to calculate engagement score
function calculateEngagementScore(interactionType: string, value?: number): number {
  const baseScores: Record<string, number> = {
    'click': 10,
    'hover': 5,
    'scroll': 3,
    'focus': 7,
    'form_input': 15,
    'form_submit': 25,
    'cta_click': 30,
    'social_share': 20,
    'video_play': 15,
    'video_complete': 30,
    'download': 25,
    'purchase': 50
  };

  let score = baseScores[interactionType] || 1;
  
  // Apply value multiplier if provided
  if (value && value > 1) {
    score *= Math.min(value / 10, 3); // Cap multiplier at 3x
  }

  return Math.round(score);
}