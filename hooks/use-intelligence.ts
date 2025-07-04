/**
 * Intelligence Hook v2.0
 * React hook for UX Intelligence Engine integration
 * 
 * Module 3B Week 2 - Intelligence Integration
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { intelligenceEngine, IntelligenceState, ComponentOptimizations } from '@/lib/intelligence-engine';
import { PersonaType, DeviceType } from '@/types';

interface UseIntelligenceReturn {
  // Current intelligence state
  persona: PersonaType;
  confidence: number;
  device: DeviceType;
  intent: 'awareness' | 'consideration' | 'decision' | 'purchase';
  
  // Optimization data
  optimizations: ComponentOptimizations;
  
  // Component-specific optimizations
  getComponentOptimizations: (componentType: string) => ComponentOptimizations;
  
  // State management
  loading: boolean;
  error: string | null;
  lastUpdate: number;
  
  // Actions
  forceUpdate: () => Promise<void>;
  subscribe: (callback: (state: IntelligenceState) => void) => () => void;
  
  // Convenience methods
  isPersonaConfident: boolean;
  shouldOptimizeForMobile: boolean;
  shouldShowAdvancedFeatures: boolean;
  shouldUseUrgentCTA: boolean;
}

export function useIntelligence(): UseIntelligenceReturn {
  const [state, setState] = useState<IntelligenceState>(intelligenceEngine.getCurrentState());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Subscribe to intelligence updates
  useEffect(() => {
    const unsubscribe = intelligenceEngine.subscribe((newState) => {
      setState(newState);
      setError(null);
    });

    return unsubscribe;
  }, []);

  // Force intelligence update
  const forceUpdate = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      await intelligenceEngine.forceUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Intelligence update failed');
    } finally {
      setLoading(false);
    }
  }, []);

  // Get component-specific optimizations
  const getComponentOptimizations = useCallback((componentType: string): ComponentOptimizations => {
    return intelligenceEngine.getOptimizationsForComponent(componentType);
  }, []);

  // Subscribe to updates
  const subscribe = useCallback((callback: (state: IntelligenceState) => void) => {
    return intelligenceEngine.subscribe(callback);
  }, []);

  // Convenience computed values
  const isPersonaConfident = state.confidence >= 70;
  const shouldOptimizeForMobile = state.device === 'mobile';
  const shouldShowAdvancedFeatures = state.persona === 'TechEarlyAdopter' || state.persona === 'BusinessOwner';
  const shouldUseUrgentCTA = state.intent === 'decision' || state.intent === 'purchase';

  return {
    // Current state
    persona: state.persona,
    confidence: state.confidence,
    device: state.device,
    intent: state.intent,
    optimizations: state.optimization,
    
    // Methods
    getComponentOptimizations,
    forceUpdate,
    subscribe,
    
    // State flags
    loading,
    error,
    lastUpdate: state.lastUpdate,
    
    // Convenience flags
    isPersonaConfident,
    shouldOptimizeForMobile,
    shouldShowAdvancedFeatures,
    shouldUseUrgentCTA
  };
}

/**
 * Hook for component-specific intelligence optimizations
 */
export function useComponentIntelligence(componentType: string) {
  const { getComponentOptimizations, persona, device, intent, confidence } = useIntelligence();
  
  const [optimizations, setOptimizations] = useState<ComponentOptimizations>(() => 
    getComponentOptimizations(componentType)
  );

  // Update optimizations when intelligence state changes
  useEffect(() => {
    const newOptimizations = getComponentOptimizations(componentType);
    setOptimizations(newOptimizations);
  }, [getComponentOptimizations, componentType, persona, device, intent, confidence]);

  return {
    optimizations,
    persona,
    device,
    intent,
    confidence,
    
    // Component-specific convenience methods
    getLayoutClasses: () => generateLayoutClasses(optimizations.layout),
    getContentClasses: () => generateContentClasses(optimizations.content),
    getInteractionClasses: () => generateInteractionClasses(optimizations.interactions),
    getPerformanceSettings: () => optimizations.performance,
    
    // Component behavior flags
    shouldUseCompactLayout: optimizations.layout.spacing === 'compact',
    shouldUseDenseContent: optimizations.content.density === 'dense',
    shouldUseImmediateResponse: optimizations.interactions.response_time === 'immediate',
    shouldPrioritizeContent: optimizations.performance.loading_priority === 'content'
  };
}

/**
 * Hook for persona-driven content adaptation
 */
export function usePersonaContent() {
  const { persona, confidence, optimizations } = useIntelligence();
  
  const getPersonaText = useCallback((options: {
    TechEarlyAdopter: string;
    RemoteDad: string;
    StudentHustler: string;
    BusinessOwner: string;
    fallback: string;
  }): string => {
    if (confidence < 50) return options.fallback;
    return options[persona] || options.fallback;
  }, [persona, confidence]);

  const getPersonaCTA = useCallback((urgency: 'low' | 'medium' | 'high' = 'medium'): string => {
    const ctaMap: Record<PersonaType, Record<string, string>> = {
      TechEarlyAdopter: {
        low: 'Explore Features',
        medium: 'Try Beta Access',
        high: 'Get Early Access Now'
      },
      RemoteDad: {
        low: 'Learn More',
        medium: 'Start Free Trial',
        high: 'Secure Your Family\'s Future'
      },
      StudentHustler: {
        low: 'Check It Out',
        medium: 'Get Student Discount',
        high: 'Claim Limited Offer'
      },
      BusinessOwner: {
        low: 'Schedule Demo',
        medium: 'Start Enterprise Trial',
        high: 'Book Strategy Call Now'
      },
      unknown: {
        low: 'Learn More',
        medium: 'Get Started',
        high: 'Try Now'
      }
    };

    return ctaMap[persona]?.[urgency] || ctaMap.unknown[urgency];
  }, [persona]);

  const getTrustFactors = useCallback((): string[] => {
    return optimizations.content.trust_factors;
  }, [optimizations.content.trust_factors]);

  return {
    persona,
    confidence,
    getPersonaText,
    getPersonaCTA,
    getTrustFactors,
    contentTone: optimizations.content.tone,
    contentDensity: optimizations.content.density,
    contentEmphasis: optimizations.content.emphasis
  };
}

// Utility functions for generating CSS classes
function generateLayoutClasses(layout: ComponentOptimizations['layout']): string {
  const classes = [];
  
  // Column classes
  classes.push(`grid-cols-${layout.columns}`);
  
  // Spacing classes
  switch (layout.spacing) {
    case 'compact':
      classes.push('gap-2', 'p-2');
      break;
    case 'comfortable':
      classes.push('gap-4', 'p-4');
      break;
    case 'spacious':
      classes.push('gap-6', 'p-6');
      break;
  }
  
  // Navigation classes
  switch (layout.navigation) {
    case 'hamburger':
      classes.push('nav-hamburger');
      break;
    case 'sidebar':
      classes.push('nav-sidebar');
      break;
    case 'horizontal':
      classes.push('nav-horizontal');
      break;
  }
  
  // CTA placement
  switch (layout.cta_placement) {
    case 'sticky':
      classes.push('cta-sticky');
      break;
    case 'floating':
      classes.push('cta-floating');
      break;
    case 'inline':
      classes.push('cta-inline');
      break;
  }
  
  return classes.join(' ');
}

function generateContentClasses(content: ComponentOptimizations['content']): string {
  const classes = [];
  
  // Density classes
  switch (content.density) {
    case 'minimal':
      classes.push('text-lg', 'leading-relaxed', 'space-y-6');
      break;
    case 'moderate':
      classes.push('text-base', 'leading-normal', 'space-y-4');
      break;
    case 'dense':
      classes.push('text-sm', 'leading-tight', 'space-y-2');
      break;
  }
  
  // Tone classes
  switch (content.tone) {
    case 'casual':
      classes.push('font-normal', 'text-warm');
      break;
    case 'professional':
      classes.push('font-medium', 'text-neutral');
      break;
    case 'technical':
      classes.push('font-mono', 'text-cool');
      break;
  }
  
  // Emphasis classes
  switch (content.emphasis) {
    case 'visual':
      classes.push('image-heavy', 'visual-focus');
      break;
    case 'textual':
      classes.push('text-heavy', 'reading-focus');
      break;
    case 'interactive':
      classes.push('interactive-heavy', 'engagement-focus');
      break;
  }
  
  return classes.join(' ');
}

function generateInteractionClasses(interactions: ComponentOptimizations['interactions']): string {
  const classes = [];
  
  // Input method classes
  switch (interactions.input_method) {
    case 'touch':
      classes.push('touch-optimized', 'large-targets');
      break;
    case 'mouse':
      classes.push('mouse-optimized', 'hover-effects');
      break;
    case 'keyboard':
      classes.push('keyboard-optimized', 'focus-visible');
      break;
  }
  
  // Response time classes
  switch (interactions.response_time) {
    case 'immediate':
      classes.push('instant-feedback');
      break;
    case 'delayed':
      classes.push('delayed-feedback');
      break;
    case 'progressive':
      classes.push('progressive-feedback');
      break;
  }
  
  // Feedback style classes
  switch (interactions.feedback_style) {
    case 'subtle':
      classes.push('subtle-feedback');
      break;
    case 'prominent':
      classes.push('prominent-feedback');
      break;
    case 'animated':
      classes.push('animated-feedback');
      break;
  }
  
  // Guidance level classes
  switch (interactions.guidance_level) {
    case 'minimal':
      classes.push('minimal-guidance');
      break;
    case 'moderate':
      classes.push('moderate-guidance');
      break;
    case 'comprehensive':
      classes.push('comprehensive-guidance');
      break;
  }
  
  return classes.join(' ');
}