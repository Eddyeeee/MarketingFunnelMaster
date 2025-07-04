/**
 * Intelligence Engine Integration v2.0
 * Integrates UX Intelligence Engine with Component System
 * 
 * Module 3B Week 2 - Intelligence Integration
 */

import { UXIntelligenceEngine } from '../TEC-code-UXIntelligenceEngine-v1';
import { PersonaType, DeviceType, PersonaConfig } from '@/types';

// Enhanced interfaces for intelligence integration
interface IntelligenceState {
  persona: PersonaType;
  confidence: number;
  device: DeviceType;
  intent: PurchaseIntentLevel;
  optimization: ComponentOptimizations;
  lastUpdate: number;
}

interface ComponentOptimizations {
  layout: LayoutOptimizations;
  content: ContentOptimizations;
  interactions: InteractionOptimizations;
  performance: PerformanceOptimizations;
}

interface LayoutOptimizations {
  columns: number;
  spacing: 'compact' | 'comfortable' | 'spacious';
  navigation: 'hamburger' | 'sidebar' | 'horizontal';
  cta_placement: 'sticky' | 'floating' | 'inline';
}

interface ContentOptimizations {
  density: 'minimal' | 'moderate' | 'dense';
  tone: 'casual' | 'professional' | 'technical';
  emphasis: 'visual' | 'textual' | 'interactive';
  trust_factors: string[];
}

interface InteractionOptimizations {
  input_method: 'touch' | 'mouse' | 'keyboard';
  response_time: 'immediate' | 'delayed' | 'progressive';
  feedback_style: 'subtle' | 'prominent' | 'animated';
  guidance_level: 'minimal' | 'moderate' | 'comprehensive';
}

interface PerformanceOptimizations {
  loading_priority: 'content' | 'images' | 'interactive';
  bundle_size: 'minimal' | 'standard' | 'full';
  prefetch_strategy: 'none' | 'next_page' | 'full_journey';
  caching_level: 'basic' | 'aggressive' | 'smart';
}

type PurchaseIntentLevel = 'awareness' | 'consideration' | 'decision' | 'purchase';

class IntelligenceEngine {
  private uxEngine: UXIntelligenceEngine;
  private state: IntelligenceState;
  private subscribers: Set<(state: IntelligenceState) => void>;
  private updateInterval: number = 5000; // 5 seconds
  private behaviorTracker: BehaviorTracker;

  constructor() {
    this.uxEngine = new UXIntelligenceEngine();
    this.subscribers = new Set();
    this.behaviorTracker = new BehaviorTracker();
    
    this.state = {
      persona: 'unknown',
      confidence: 0,
      device: this.detectDevice(),
      intent: 'awareness',
      optimization: this.getDefaultOptimizations(),
      lastUpdate: Date.now()
    };

    this.initializeTracking();
  }

  // Public API methods
  public subscribe(callback: (state: IntelligenceState) => void): () => void {
    this.subscribers.add(callback);
    return () => this.subscribers.delete(callback);
  }

  public getCurrentState(): IntelligenceState {
    return { ...this.state };
  }

  public async forceUpdate(): Promise<void> {
    await this.updateIntelligence();
  }

  public getOptimizationsForComponent(componentType: string): ComponentOptimizations {
    const baseOptimizations = this.state.optimization;
    
    // Component-specific optimizations
    switch (componentType) {
      case 'HeroSection':
        return {
          ...baseOptimizations,
          layout: {
            ...baseOptimizations.layout,
            cta_placement: this.state.device === 'mobile' ? 'sticky' : 'inline'
          }
        };
      case 'Navigation':
        return {
          ...baseOptimizations,
          interactions: {
            ...baseOptimizations.interactions,
            guidance_level: this.state.persona === 'TechEarlyAdopter' ? 'minimal' : 'moderate'
          }
        };
      case 'CallToAction':
        return {
          ...baseOptimizations,
          content: {
            ...baseOptimizations.content,
            tone: this.getCTATone()
          }
        };
      default:
        return baseOptimizations;
    }
  }

  // Private methods
  private async initializeTracking(): Promise<void> {
    // Start continuous intelligence updates
    setInterval(() => {
      this.updateIntelligence();
    }, this.updateInterval);

    // Initial intelligence gathering
    await this.updateIntelligence();
  }

  private async updateIntelligence(): Promise<void> {
    try {
      const behaviorData = await this.behaviorTracker.collectBehaviorData();
      const deviceCapabilities = this.getDeviceCapabilities();
      const userPath = this.behaviorTracker.getUserPath();
      const currentMetrics = this.behaviorTracker.getMetrics();

      // Run UX Intelligence Engine
      const intelligence = this.uxEngine.optimizeUX(
        navigator.userAgent,
        behaviorData,
        deviceCapabilities,
        userPath,
        currentMetrics
      );

      // Update state with new intelligence
      this.state = {
        persona: this.mapPersonaType(intelligence.persona.type),
        confidence: intelligence.persona.confidence,
        device: this.detectDevice(),
        intent: intelligence.intent.stage as PurchaseIntentLevel,
        optimization: this.mapOptimizations(intelligence),
        lastUpdate: Date.now()
      };

      // Notify subscribers
      this.notifySubscribers();

    } catch (error) {
      console.error('Intelligence update failed:', error);
    }
  }

  private detectDevice(): DeviceType {
    const width = window.innerWidth;
    
    if (width < 768) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  }

  private getDeviceCapabilities(): any {
    return {
      type: this.detectDevice(),
      screen: {
        width: window.innerWidth,
        height: window.innerHeight,
        pixelRatio: window.devicePixelRatio || 1
      },
      performance: {
        cpu: this.estimateCPUPerformance(),
        memory: (navigator as any).deviceMemory || 4,
        connection: this.getConnectionType()
      },
      input: {
        touch: 'ontouchstart' in window,
        mouse: window.matchMedia('(pointer: fine)').matches,
        keyboard: true
      },
      capabilities: {
        webgl: !!window.WebGLRenderingContext,
        webp: this.supportsWebP(),
        modernJS: this.supportsModernJS()
      }
    };
  }

  private mapPersonaType(uxPersonaType: string): PersonaType {
    const mapping: Record<string, PersonaType> = {
      'TechEarlyAdopter': 'TechEarlyAdopter',
      'RemoteDad': 'RemoteDad',
      'StudentHustler': 'StudentHustler',
      'BusinessOwner': 'BusinessOwner'
    };
    
    return mapping[uxPersonaType] || 'unknown';
  }

  private mapOptimizations(intelligence: any): ComponentOptimizations {
    const layout = intelligence.layout.layout;
    const persona = intelligence.persona;
    const device = this.detectDevice();
    
    return {
      layout: {
        columns: layout.columns,
        spacing: device === 'mobile' ? 'compact' : 'comfortable',
        navigation: layout.navigation,
        cta_placement: layout.cta
      },
      content: {
        density: this.getContentDensity(persona.type),
        tone: this.getContentTone(persona.type),
        emphasis: this.getContentEmphasis(persona.type, device),
        trust_factors: persona.preferences.trustFactors
      },
      interactions: {
        input_method: device === 'mobile' ? 'touch' : 'mouse',
        response_time: device === 'mobile' ? 'immediate' : 'delayed',
        feedback_style: this.getFeedbackStyle(persona.type),
        guidance_level: this.getGuidanceLevel(persona.type)
      },
      performance: {
        loading_priority: this.getLoadingPriority(device),
        bundle_size: device === 'mobile' ? 'minimal' : 'standard',
        prefetch_strategy: intelligence.intent.stage === 'decision' ? 'next_page' : 'none',
        caching_level: 'smart'
      }
    };
  }

  private getDefaultOptimizations(): ComponentOptimizations {
    return {
      layout: {
        columns: 1,
        spacing: 'comfortable',
        navigation: 'horizontal',
        cta_placement: 'inline'
      },
      content: {
        density: 'moderate',
        tone: 'casual',
        emphasis: 'visual',
        trust_factors: ['social_proof', 'testimonials']
      },
      interactions: {
        input_method: 'mouse',
        response_time: 'delayed',
        feedback_style: 'subtle',
        guidance_level: 'moderate'
      },
      performance: {
        loading_priority: 'content',
        bundle_size: 'standard',
        prefetch_strategy: 'none',
        caching_level: 'basic'
      }
    };
  }

  private getContentDensity(personaType: string): 'minimal' | 'moderate' | 'dense' {
    const densityMap: Record<string, 'minimal' | 'moderate' | 'dense'> = {
      'TechEarlyAdopter': 'dense',
      'BusinessOwner': 'dense',
      'RemoteDad': 'moderate',
      'StudentHustler': 'minimal'
    };
    
    return densityMap[personaType] || 'moderate';
  }

  private getContentTone(personaType: string): 'casual' | 'professional' | 'technical' {
    const toneMap: Record<string, 'casual' | 'professional' | 'technical'> = {
      'TechEarlyAdopter': 'technical',
      'BusinessOwner': 'professional',
      'RemoteDad': 'casual',
      'StudentHustler': 'casual'
    };
    
    return toneMap[personaType] || 'casual';
  }

  private getContentEmphasis(personaType: string, device: DeviceType): 'visual' | 'textual' | 'interactive' {
    if (device === 'mobile') return 'visual';
    
    const emphasisMap: Record<string, 'visual' | 'textual' | 'interactive'> = {
      'TechEarlyAdopter': 'interactive',
      'BusinessOwner': 'textual',
      'RemoteDad': 'visual',
      'StudentHustler': 'visual'
    };
    
    return emphasisMap[personaType] || 'visual';
  }

  private getFeedbackStyle(personaType: string): 'subtle' | 'prominent' | 'animated' {
    const styleMap: Record<string, 'subtle' | 'prominent' | 'animated'> = {
      'TechEarlyAdopter': 'subtle',
      'BusinessOwner': 'prominent',
      'RemoteDad': 'animated',
      'StudentHustler': 'animated'
    };
    
    return styleMap[personaType] || 'subtle';
  }

  private getGuidanceLevel(personaType: string): 'minimal' | 'moderate' | 'comprehensive' {
    const guidanceMap: Record<string, 'minimal' | 'moderate' | 'comprehensive'> = {
      'TechEarlyAdopter': 'minimal',
      'BusinessOwner': 'moderate',
      'RemoteDad': 'comprehensive',
      'StudentHustler': 'moderate'
    };
    
    return guidanceMap[personaType] || 'moderate';
  }

  private getLoadingPriority(device: DeviceType): 'content' | 'images' | 'interactive' {
    if (device === 'mobile') return 'content';
    if (device === 'tablet') return 'images';
    return 'interactive';
  }

  private getCTATone(): 'casual' | 'professional' | 'technical' {
    const intentMap: Record<PurchaseIntentLevel, 'casual' | 'professional' | 'technical'> = {
      'awareness': 'casual',
      'consideration': 'professional',
      'decision': 'professional',
      'purchase': 'professional'
    };
    
    return intentMap[this.state.intent] || 'casual';
  }

  private notifySubscribers(): void {
    this.subscribers.forEach(callback => {
      try {
        callback(this.state);
      } catch (error) {
        console.error('Subscriber callback error:', error);
      }
    });
  }

  // Utility methods
  private estimateCPUPerformance(): 'low' | 'medium' | 'high' {
    const cores = navigator.hardwareConcurrency || 4;
    if (cores <= 2) return 'low';
    if (cores <= 4) return 'medium';
    return 'high';
  }

  private getConnectionType(): 'slow' | 'medium' | 'fast' {
    const connection = (navigator as any).connection || {};
    const effectiveType = connection.effectiveType || '4g';
    
    if (effectiveType === 'slow-2g' || effectiveType === '2g') return 'slow';
    if (effectiveType === '3g') return 'medium';
    return 'fast';
  }

  private supportsWebP(): boolean {
    const canvas = document.createElement('canvas');
    return canvas.toDataURL('image/webp').startsWith('data:image/webp');
  }

  private supportsModernJS(): boolean {
    try {
      eval('(() => {})');
      return true;
    } catch {
      return false;
    }
  }
}

class BehaviorTracker {
  private behaviorData: any = {};
  private userPath: any[] = [];
  private metrics: any = {};

  async collectBehaviorData(): Promise<any> {
    return {
      clickSpeed: this.calculateClickSpeed(),
      scrollPattern: this.getScrollPattern(),
      navigationDepth: this.userPath.length,
      timeDistribution: this.getTimeDistribution(),
      interactionStyle: this.getInteractionStyle(),
      sessionCount: this.getSessionCount(),
      avgSessionDuration: this.getAverageSessionDuration()
    };
  }

  getUserPath(): any {
    return {
      pages: this.userPath.map(p => p.page),
      timestamps: this.userPath.map(p => p.timestamp),
      interactions: this.userPath.flatMap(p => p.interactions || []),
      referrer: document.referrer,
      exitPage: window.location.pathname
    };
  }

  getMetrics(): any {
    return {
      performance: {
        loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
        renderTime: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
        interactionDelay: 0
      },
      engagement: {
        scrollDepth: this.calculateScrollDepth(),
        timeOnPage: this.getTimeOnPage(),
        clickThroughRate: this.calculateCTR(),
        bounceRate: this.calculateBounceRate()
      },
      conversion: {
        conversionRate: 0,
        abandonmentRate: 0,
        upsellRate: 0
      }
    };
  }

  private calculateClickSpeed(): number {
    // Implementation for click speed calculation
    return 0.5; // Placeholder
  }

  private getScrollPattern(): 'slow' | 'medium' | 'fast' {
    // Implementation for scroll pattern detection
    return 'medium'; // Placeholder
  }

  private getTimeDistribution(): number[] {
    // Implementation for time distribution analysis
    return [1, 2, 3, 4, 5]; // Placeholder
  }

  private getInteractionStyle(): 'cautious' | 'exploratory' | 'decisive' {
    // Implementation for interaction style detection
    return 'exploratory'; // Placeholder
  }

  private getSessionCount(): number {
    const sessions = localStorage.getItem('sessionCount');
    return sessions ? parseInt(sessions) : 1;
  }

  private getAverageSessionDuration(): number {
    // Implementation for average session duration
    return 300; // Placeholder: 5 minutes
  }

  private calculateScrollDepth(): number {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    return Math.min(100, (scrollTop + windowHeight) / documentHeight * 100);
  }

  private getTimeOnPage(): number {
    const sessionStart = performance.timing.navigationStart;
    return (Date.now() - sessionStart) / 1000;
  }

  private calculateCTR(): number {
    // Implementation for click-through rate calculation
    return 0.05; // Placeholder
  }

  private calculateBounceRate(): number {
    // Implementation for bounce rate calculation
    return 0.3; // Placeholder
  }
}

// Create and export singleton instance
export const intelligenceEngine = new IntelligenceEngine();
export type { IntelligenceState, ComponentOptimizations };