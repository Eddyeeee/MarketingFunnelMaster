// Core Types for Next.js Component System

export type PersonaType = 
  | 'TechEarlyAdopter'
  | 'RemoteDad'
  | 'StudentHustler'
  | 'BusinessOwner'
  | 'unknown';

export type DeviceType = 
  | 'mobile'
  | 'tablet'
  | 'desktop';

export type BrandType = 
  | 'tech'
  | 'wealth'
  | 'crypto'
  | 'affiliate';

export interface BrandConfig {
  id: string;
  name: string;
  domain: string;
  industry: string;
  target_personas: PersonaType[];
  
  // Visual System
  design: {
    colors: {
      primary: string;
      secondary: string;
      accent: string;
      background: string;
      foreground: string;
      muted: string;
      border: string;
    };
    typography: {
      headings: string;
      body: string;
      mono: string;
    };
    spacing: {
      unit: number;
      scale: number[];
    };
    borderRadius: {
      sm: string;
      md: string;
      lg: string;
    };
  };
  
  // Content Strategy
  content: {
    messaging: {
      headline: string;
      subheadline: string;
      value_proposition: string;
      cta_primary: string;
      cta_secondary: string;
    };
    tone: 'professional' | 'friendly' | 'technical' | 'casual' | 'authoritative';
    voice: string;
  };
  
  // SEO Configuration
  seo: {
    title: string;
    description: string;
    keywords: string[];
    ogImage: string;
    ogImageAlt: string;
    twitterImage: string;
  };
  
  // Analytics Configuration
  analytics: {
    ga4_id?: string;
    gtm_id?: string;
    facebook_pixel_id?: string;
    custom_events: string[];
  };
  
  // Social Media
  social: {
    twitter?: string;
    linkedin?: string;
    facebook?: string;
    instagram?: string;
    youtube?: string;
    github?: string;
    discord?: string;
    telegram?: string;
  };
}

export interface PersonaConfig {
  type: PersonaType;
  
  // Behavioral Characteristics
  behavior: {
    decision_making: 'analytical' | 'intuitive' | 'social' | 'impulsive';
    information_processing: 'detailed' | 'summary' | 'visual' | 'interactive';
    trust_building: 'social_proof' | 'expert_authority' | 'peer_reviews' | 'guarantees';
    conversion_triggers: string[];
  };
  
  // UX Preferences
  ux: {
    navigation_style: 'exploratory' | 'linear' | 'hub_and_spoke' | 'guided';
    content_density: 'minimal' | 'moderate' | 'dense';
    interaction_patterns: string[];
    device_preferences: DeviceType[];
  };
  
  // Content Preferences
  content: {
    messaging_style: 'direct' | 'storytelling' | 'data_driven' | 'emotional';
    evidence_types: string[];
    content_formats: string[];
    engagement_patterns: string[];
  };
  
  // Conversion Optimization
  conversion: {
    primary_motivators: string[];
    objection_handling: string[];
    preferred_cta_style: 'urgent' | 'gentle' | 'social' | 'logical';
    optimal_funnel_length: 'short' | 'medium' | 'long';
  };
}

export interface ComponentVariant {
  type: 'hero' | 'navigation' | 'footer' | 'cta' | 'form' | 'testimonial';
  variant: string;
  persona_optimization: PersonaType[];
  device_optimization: DeviceType[];
  brand_compatibility: BrandType[];
  
  // Component Configuration
  config: {
    layout: string;
    features: string[];
    style_modifiers: string[];
    behavior_settings: Record<string, any>;
  };
  
  // Performance Settings
  performance: {
    lazy_load: boolean;
    critical_css: boolean;
    image_optimization: boolean;
    bundle_splitting: boolean;
  };
  
  // Analytics
  analytics: {
    track_interactions: boolean;
    custom_events: string[];
    conversion_goals: string[];
  };
}

export interface TemplateConfiguration {
  id: string;
  name: string;
  brand: BrandConfig;
  persona: PersonaConfig;
  
  // Template Structure
  structure: {
    pages: TemplatePageConfig[];
    components: ComponentVariant[];
    navigation: NavigationConfig;
    footer: FooterConfig;
  };
  
  // Content Configuration
  content: {
    static_content: Record<string, string>;
    dynamic_content: Record<string, any>;
    personalized_content: Record<PersonaType, any>;
  };
  
  // SEO Configuration
  seo: {
    meta_templates: Record<string, string>;
    structured_data: any[];
    sitemap_config: SitemapConfig;
    robots_config: RobotsConfig;
  };
  
  // Performance Configuration
  performance: {
    critical_css: string[];
    preload_resources: string[];
    lazy_load_components: string[];
    bundle_optimization: BundleConfig;
  };
}

export interface TemplatePageConfig {
  path: string;
  name: string;
  components: string[];
  layout: string;
  seo: {
    title: string;
    description: string;
    canonical?: string;
  };
  performance: {
    critical: boolean;
    preload: string[];
  };
}

export interface NavigationConfig {
  variant: 'default' | 'minimal' | 'sidebar';
  items: NavigationItem[];
  brand_customization: Record<string, any>;
  persona_adaptation: Record<PersonaType, any>;
}

export interface NavigationItem {
  href: string;
  label: string;
  icon?: string;
  persona_relevance?: PersonaType[];
  device_visibility?: DeviceType[];
  children?: NavigationItem[];
}

export interface FooterConfig {
  variant: 'default' | 'minimal' | 'extended';
  sections: FooterSection[];
  brand_customization: Record<string, any>;
  legal_links: string[];
}

export interface FooterSection {
  title: string;
  links: Array<{
    href: string;
    label: string;
    external?: boolean;
  }>;
  persona_relevance?: PersonaType[];
}

export interface SitemapConfig {
  url: string;
  pages: Array<{
    url: string;
    lastModified: string;
    changeFrequency: string;
    priority: number;
  }>;
}

export interface RobotsConfig {
  rules: Array<{
    userAgent: string;
    allow?: string[];
    disallow?: string[];
  }>;
  sitemap: string;
  host?: string;
}

export interface BundleConfig {
  code_splitting: boolean;
  tree_shaking: boolean;
  compression: boolean;
  chunk_optimization: boolean;
  vendor_splitting: boolean;
}

// Analytics and Performance Types
export interface PerformanceMetrics {
  lcp: number; // Largest Contentful Paint
  fid: number; // First Input Delay
  cls: number; // Cumulative Layout Shift
  fcp: number; // First Contentful Paint
  ttfb: number; // Time to First Byte
  bundle_size: number;
  page_load_time: number;
}

export interface AnalyticsEvent {
  name: string;
  category: string;
  action: string;
  label?: string;
  value?: number;
  custom_parameters?: Record<string, any>;
}

export interface ConversionGoal {
  id: string;
  name: string;
  type: 'page_view' | 'event' | 'custom';
  target: string;
  value?: number;
  persona_specific?: PersonaType[];
}

// API Response Types
export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp: string;
}

export interface GenerationResult {
  template_id: string;
  brand_config: BrandConfig;
  generated_files: string[];
  deployment_config: any;
  performance_score: number;
  quality_score: number;
  estimated_metrics: PerformanceMetrics;
}

// Error Types
export interface ComponentError {
  component: string;
  error: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  suggested_fix?: string;
}

export interface ValidationError {
  field: string;
  message: string;
  code: string;
}

// Hook Types
export interface UseBrandReturn {
  brand: BrandType;
  brandConfig: BrandConfig;
  setBrand: (brand: BrandType) => void;
  loading: boolean;
  error?: string;
}

export interface UsePersonaReturn {
  persona: PersonaType;
  personaConfig: PersonaConfig;
  confidence: number;
  setPersona: (persona: PersonaType) => void;
  detectPersona: () => Promise<void>;
  loading: boolean;
  error?: string;
}

export interface UseDeviceReturn {
  device: DeviceType;
  deviceInfo: {
    width: number;
    height: number;
    orientation: 'portrait' | 'landscape';
    touch: boolean;
    mobile: boolean;
    tablet: boolean;
    desktop: boolean;
  };
  setDevice: (device: DeviceType) => void;
}

export interface UseAnalyticsReturn {
  track: (event: AnalyticsEvent) => void;
  trackPageView: (path: string) => void;
  trackConversion: (goal: ConversionGoal) => void;
  identify: (userId: string, traits?: Record<string, any>) => void;
  reset: () => void;
}

// Component Props Types
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
  brand?: BrandType;
  persona?: PersonaType;
  device?: DeviceType;
  variant?: string;
}

export interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string[];
  canonical?: string;
  noindex?: boolean;
  nofollow?: boolean;
  openGraph?: {
    title?: string;
    description?: string;
    image?: string;
    type?: string;
  };
  twitter?: {
    card?: string;
    title?: string;
    description?: string;
    image?: string;
  };
}