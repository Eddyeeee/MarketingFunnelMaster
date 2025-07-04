'use client';

import { useState, useEffect, useContext, createContext } from 'react';
import { PersonaType, PersonaConfig, UsePersonaReturn } from '@/types';
import { getFromStorage, setToStorage } from '@/lib/utils';

// Default persona configurations
const defaultPersonaConfigs: Record<PersonaType, PersonaConfig> = {
  TechEarlyAdopter: {
    type: 'TechEarlyAdopter',
    behavior: {
      decision_making: 'analytical',
      information_processing: 'detailed',
      trust_building: 'expert_authority',
      conversion_triggers: ['innovation_advantage', 'technical_specs', 'early_access'],
    },
    ux: {
      navigation_style: 'exploratory',
      content_density: 'dense',
      interaction_patterns: ['hover_previews', 'keyboard_shortcuts', 'advanced_filters'],
      device_preferences: ['desktop', 'mobile'],
    },
    content: {
      messaging_style: 'data_driven',
      evidence_types: ['technical_documentation', 'code_examples', 'performance_benchmarks'],
      content_formats: ['interactive_demos', 'technical_blogs', 'video_tutorials'],
      engagement_patterns: ['deep_dive_reading', 'tool_exploration', 'community_discussion'],
    },
    conversion: {
      primary_motivators: ['competitive_advantage', 'efficiency_gains', 'innovation_leadership'],
      objection_handling: ['security_concerns', 'integration_complexity', 'learning_curve'],
      preferred_cta_style: 'logical',
      optimal_funnel_length: 'medium',
    },
  },
  RemoteDad: {
    type: 'RemoteDad',
    behavior: {
      decision_making: 'social',
      information_processing: 'summary',
      trust_building: 'peer_reviews',
      conversion_triggers: ['family_benefit', 'time_savings', 'work_life_balance'],
    },
    ux: {
      navigation_style: 'linear',
      content_density: 'moderate',
      interaction_patterns: ['simple_navigation', 'clear_categories', 'family_focused_content'],
      device_preferences: ['mobile', 'tablet'],
    },
    content: {
      messaging_style: 'storytelling',
      evidence_types: ['testimonials', 'success_stories', 'family_impact_cases'],
      content_formats: ['video_stories', 'infographics', 'quick_guides'],
      engagement_patterns: ['casual_browsing', 'social_sharing', 'recommendation_seeking'],
    },
    conversion: {
      primary_motivators: ['family_welfare', 'financial_security', 'time_freedom'],
      objection_handling: ['budget_constraints', 'time_commitment', 'family_impact'],
      preferred_cta_style: 'gentle',
      optimal_funnel_length: 'short',
    },
  },
  StudentHustler: {
    type: 'StudentHustler',
    behavior: {
      decision_making: 'impulsive',
      information_processing: 'visual',
      trust_building: 'social_proof',
      conversion_triggers: ['price_advantage', 'quick_results', 'peer_validation'],
    },
    ux: {
      navigation_style: 'guided',
      content_density: 'minimal',
      interaction_patterns: ['swipe_gestures', 'quick_actions', 'mobile_first'],
      device_preferences: ['mobile', 'tablet'],
    },
    content: {
      messaging_style: 'energetic',
      evidence_types: ['peer_testimonials', 'quick_wins', 'social_media_proof'],
      content_formats: ['short_videos', 'memes', 'quick_tips'],
      engagement_patterns: ['fast_consumption', 'social_sharing', 'trend_following'],
    },
    conversion: {
      primary_motivators: ['affordability', 'speed_to_results', 'social_status'],
      objection_handling: ['limited_budget', 'time_constraints', 'skepticism'],
      preferred_cta_style: 'urgent',
      optimal_funnel_length: 'short',
    },
  },
  BusinessOwner: {
    type: 'BusinessOwner',
    behavior: {
      decision_making: 'analytical',
      information_processing: 'detailed',
      trust_building: 'expert_authority',
      conversion_triggers: ['roi_potential', 'scalability', 'competitive_advantage'],
    },
    ux: {
      navigation_style: 'hub_and_spoke',
      content_density: 'dense',
      interaction_patterns: ['comparison_tools', 'detailed_analysis', 'consultation_booking'],
      device_preferences: ['desktop', 'tablet'],
    },
    content: {
      messaging_style: 'professional',
      evidence_types: ['case_studies', 'roi_calculations', 'industry_reports'],
      content_formats: ['whitepapers', 'webinars', 'detailed_guides'],
      engagement_patterns: ['thorough_research', 'comparison_shopping', 'expert_consultation'],
    },
    conversion: {
      primary_motivators: ['business_growth', 'efficiency_improvement', 'market_leadership'],
      objection_handling: ['implementation_cost', 'change_management', 'roi_uncertainty'],
      preferred_cta_style: 'professional',
      optimal_funnel_length: 'long',
    },
  },
  unknown: {
    type: 'unknown',
    behavior: {
      decision_making: 'social',
      information_processing: 'summary',
      trust_building: 'social_proof',
      conversion_triggers: ['value_proposition', 'social_proof', 'ease_of_use'],
    },
    ux: {
      navigation_style: 'linear',
      content_density: 'moderate',
      interaction_patterns: ['simple_navigation', 'clear_categories'],
      device_preferences: ['desktop', 'mobile', 'tablet'],
    },
    content: {
      messaging_style: 'friendly',
      evidence_types: ['testimonials', 'basic_features', 'simple_benefits'],
      content_formats: ['overview_videos', 'simple_guides', 'faq'],
      engagement_patterns: ['casual_browsing', 'feature_exploration'],
    },
    conversion: {
      primary_motivators: ['clear_value', 'ease_of_use', 'trust_building'],
      objection_handling: ['price_concerns', 'complexity_fears', 'trust_issues'],
      preferred_cta_style: 'gentle',
      optimal_funnel_length: 'medium',
    },
  },
};

// Persona Context
const PersonaContext = createContext<UsePersonaReturn | undefined>(undefined);

export function usePersona(): UsePersonaReturn {
  const context = useContext(PersonaContext);
  if (!context) {
    throw new Error('usePersona must be used within a PersonaProvider');
  }
  return context;
}

// Persona Hook Implementation
export function usePersonaInternal(): UsePersonaReturn {
  const [persona, setPersonaState] = useState<PersonaType>('unknown');
  const [confidence, setConfidence] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>();

  // Load persona from storage on mount
  useEffect(() => {
    try {
      const storedPersona = getFromStorage<PersonaType>('detectedPersona', 'unknown');
      const storedConfidence = getFromStorage<number>('personaConfidence', 0);
      
      setPersonaState(storedPersona);
      setConfidence(storedConfidence);
    } catch (err) {
      setError('Failed to load persona data');
      console.error('Persona loading error:', err);
    }
  }, []);

  const setPersona = (newPersona: PersonaType) => {
    try {
      setPersonaState(newPersona);
      setConfidence(100); // Manual setting has high confidence
      setToStorage('detectedPersona', newPersona);
      setToStorage('personaConfidence', 100);
      setError(undefined);
    } catch (err) {
      setError('Failed to save persona data');
      console.error('Persona saving error:', err);
    }
  };

  const detectPersona = async () => {
    setLoading(true);
    setError(undefined);

    try {
      // Collect user behavior data
      const behaviorData = await collectBehaviorData();
      
      // Analyze behavior and determine persona
      const detectionResult = await analyzeUserBehavior(behaviorData);
      
      setPersonaState(detectionResult.persona);
      setConfidence(detectionResult.confidence);
      
      // Store results
      setToStorage('detectedPersona', detectionResult.persona);
      setToStorage('personaConfidence', detectionResult.confidence);
      setToStorage('lastPersonaDetection', Date.now());
      
    } catch (err) {
      setError('Failed to detect persona');
      console.error('Persona detection error:', err);
    } finally {
      setLoading(false);
    }
  };

  const personaConfig = defaultPersonaConfigs[persona];

  return {
    persona,
    personaConfig,
    confidence,
    setPersona,
    detectPersona,
    loading,
    error,
  };
}

// Behavior data collection
async function collectBehaviorData() {
  const data = {
    // Device information
    device: {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      touchCapability: 'ontouchstart' in window,
      screenSize: {
        width: window.screen.width,
        height: window.screen.height,
      },
      viewportSize: {
        width: window.innerWidth,
        height: window.innerHeight,
      },
    },
    
    // Time-based behavior
    timeOnSite: getTimeOnSite(),
    visitFrequency: getVisitFrequency(),
    timeOfDay: new Date().getHours(),
    dayOfWeek: new Date().getDay(),
    
    // Navigation behavior
    pageViews: getPageViewHistory(),
    scrollDepth: await measureScrollDepth(),
    clickPatterns: getClickPatterns(),
    
    // Content preferences
    contentInteractions: getContentInteractions(),
    searchQueries: getSearchHistory(),
    
    // Technical indicators
    browserFeatures: getBrowserFeatures(),
    connectionSpeed: await measureConnectionSpeed(),
    
    // Social/External indicators
    referrer: document.referrer,
    utmParameters: getUTMParameters(),
  };

  return data;
}

// Persona analysis algorithm
async function analyzeUserBehavior(behaviorData: any): Promise<{
  persona: PersonaType;
  confidence: number;
}> {
  const scores: Record<PersonaType, number> = {
    TechEarlyAdopter: 0,
    RemoteDad: 0,
    StudentHustler: 0,
    BusinessOwner: 0,
    unknown: 0,
  };

  // Analyze device preferences
  if (behaviorData.device.screenSize.width >= 1920) {
    scores.TechEarlyAdopter += 15;
    scores.BusinessOwner += 10;
  }
  
  if (behaviorData.device.touchCapability && behaviorData.device.screenSize.width < 768) {
    scores.StudentHustler += 15;
    scores.RemoteDad += 10;
  }

  // Analyze time patterns
  const hour = behaviorData.timeOfDay;
  if (hour >= 9 && hour <= 17) {
    scores.BusinessOwner += 10;
  } else if (hour >= 18 && hour <= 22) {
    scores.RemoteDad += 15;
  } else if (hour >= 22 || hour <= 2) {
    scores.TechEarlyAdopter += 10;
    scores.StudentHustler += 10;
  }

  // Analyze navigation behavior
  if (behaviorData.scrollDepth > 80) {
    scores.TechEarlyAdopter += 10;
    scores.BusinessOwner += 10;
  }
  
  if (behaviorData.timeOnSite < 30) {
    scores.StudentHustler += 10;
  } else if (behaviorData.timeOnSite > 300) {
    scores.TechEarlyAdopter += 15;
    scores.BusinessOwner += 10;
  }

  // Analyze content preferences
  const visitedPages = behaviorData.pageViews || [];
  
  if (visitedPages.some((page: string) => 
    page.includes('api') || page.includes('docs') || page.includes('technical'))) {
    scores.TechEarlyAdopter += 20;
  }
  
  if (visitedPages.some((page: string) => 
    page.includes('pricing') || page.includes('roi') || page.includes('enterprise'))) {
    scores.BusinessOwner += 15;
  }
  
  if (visitedPages.some((page: string) => 
    page.includes('student') || page.includes('discount') || page.includes('quick'))) {
    scores.StudentHustler += 15;
  }

  // Analyze referrer patterns
  if (behaviorData.referrer.includes('github') || 
      behaviorData.referrer.includes('stackoverflow') ||
      behaviorData.referrer.includes('dev.to')) {
    scores.TechEarlyAdopter += 15;
  }
  
  if (behaviorData.referrer.includes('linkedin')) {
    scores.BusinessOwner += 10;
    scores.RemoteDad += 5;
  }
  
  if (behaviorData.referrer.includes('instagram') || 
      behaviorData.referrer.includes('tiktok') ||
      behaviorData.referrer.includes('twitter')) {
    scores.StudentHustler += 10;
  }

  // Analyze UTM parameters
  const utm = behaviorData.utmParameters;
  if (utm.campaign?.includes('tech') || utm.source?.includes('developer')) {
    scores.TechEarlyAdopter += 10;
  }

  // Find highest scoring persona
  const sortedPersonas = Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .filter(([persona]) => persona !== 'unknown');

  const [topPersona, topScore] = sortedPersonas[0] || ['unknown', 0];
  const [secondPersona, secondScore] = sortedPersonas[1] || ['unknown', 0];

  // Calculate confidence based on score separation
  const scoreDifference = topScore - secondScore;
  const confidence = Math.min(100, Math.max(0, (scoreDifference / topScore) * 100));

  // Minimum confidence threshold
  if (confidence < 30 || topScore < 20) {
    return { persona: 'unknown', confidence: 0 };
  }

  return {
    persona: topPersona as PersonaType,
    confidence: Math.round(confidence),
  };
}

// Helper functions for behavior data collection
function getTimeOnSite(): number {
  const sessionStart = getFromStorage('sessionStart', Date.now());
  return Math.round((Date.now() - sessionStart) / 1000);
}

function getVisitFrequency(): number {
  const visits = getFromStorage('visitCount', 0);
  setToStorage('visitCount', visits + 1);
  return visits;
}

function getPageViewHistory(): string[] {
  return getFromStorage('pageViewHistory', []);
}

async function measureScrollDepth(): Promise<number> {
  return new Promise((resolve) => {
    const maxScroll = Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight
    );
    
    const currentScroll = window.pageYOffset + window.innerHeight;
    const scrollPercentage = (currentScroll / maxScroll) * 100;
    
    resolve(Math.min(100, scrollPercentage));
  });
}

function getClickPatterns(): any[] {
  return getFromStorage('clickPatterns', []);
}

function getContentInteractions(): any[] {
  return getFromStorage('contentInteractions', []);
}

function getSearchHistory(): string[] {
  return getFromStorage('searchHistory', []);
}

function getBrowserFeatures(): any {
  return {
    webgl: !!window.WebGLRenderingContext,
    webrtc: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
    serviceWorker: 'serviceWorker' in navigator,
    localStorage: !!window.localStorage,
    indexedDB: !!window.indexedDB,
  };
}

async function measureConnectionSpeed(): Promise<number> {
  // Simple connection speed estimation
  const startTime = performance.now();
  try {
    await fetch('/favicon.ico', { cache: 'no-store' });
    const endTime = performance.now();
    return endTime - startTime;
  } catch {
    return 1000; // Default value if test fails
  }
}

function getUTMParameters(): any {
  const urlParams = new URLSearchParams(window.location.search);
  return {
    source: urlParams.get('utm_source'),
    medium: urlParams.get('utm_medium'),
    campaign: urlParams.get('utm_campaign'),
    term: urlParams.get('utm_term'),
    content: urlParams.get('utm_content'),
  };
}

// Persona utilities
export function getPersonaConfig(personaType: PersonaType): PersonaConfig {
  return defaultPersonaConfigs[personaType];
}

export function getAllPersonas(): PersonaType[] {
  return Object.keys(defaultPersonaConfigs) as PersonaType[];
}

export function isPersonaValid(persona: string): persona is PersonaType {
  return Object.keys(defaultPersonaConfigs).includes(persona);
}

export { PersonaContext, defaultPersonaConfigs };