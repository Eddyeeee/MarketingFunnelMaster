/**
 * Analytics Intelligence Bridge v2.0
 * Real-time analytics integration with UX Intelligence Engine
 * 
 * Module 3B Week 2 - Analytics Integration
 */

import { intelligenceEngine, IntelligenceState } from './intelligence-engine';
import { PersonaType, DeviceType } from '@/types';

// Analytics event types for intelligence tracking
interface IntelligenceEvent {
  event: string;
  timestamp: number;
  persona: PersonaType;
  confidence: number;
  device: DeviceType;
  intent: string;
  optimization_applied: string;
  component_type?: string;
  user_id?: string;
  session_id: string;
  properties: Record<string, any>;
}

interface ComponentPerformanceMetric {
  component_type: string;
  persona: PersonaType;
  device: DeviceType;
  optimization: string;
  metric_type: 'engagement' | 'conversion' | 'performance';
  metric_value: number;
  timestamp: number;
  session_id: string;
}

interface PersonaAccuracyMetric {
  predicted_persona: PersonaType;
  actual_persona?: PersonaType;
  confidence: number;
  accuracy_score?: number;
  correction_applied: boolean;
  timestamp: number;
  session_id: string;
}

interface OptimizationEffectiveness {
  optimization_id: string;
  optimization_type: string;
  persona: PersonaType;
  device: DeviceType;
  before_metric: number;
  after_metric: number;
  improvement_percentage: number;
  statistical_significance: number;
  timestamp: number;
}

class AnalyticsIntelligenceBridge {
  private sessionId: string;
  private userId?: string;
  private events: IntelligenceEvent[] = [];
  private performanceMetrics: ComponentPerformanceMetric[] = [];
  private accuracyMetrics: PersonaAccuracyMetric[] = [];
  private optimizationEffectiveness: OptimizationEffectiveness[] = [];
  
  // Real-time analytics endpoints
  private analyticsEndpoint = '/api/analytics/intelligence';
  private metricsEndpoint = '/api/analytics/metrics';
  private feedbackEndpoint = '/api/analytics/feedback';
  
  // Batch processing settings
  private batchSize = 10;
  private flushInterval = 5000; // 5 seconds
  private batchTimer?: NodeJS.Timeout;

  constructor() {
    this.sessionId = this.generateSessionId();
    this.initializeTracking();
    this.setupBatchProcessing();
  }

  // Public API methods
  public setUserId(userId: string): void {
    this.userId = userId;
  }

  public trackIntelligenceEvent(event: Partial<IntelligenceEvent>): void {
    const currentState = intelligenceEngine.getCurrentState();
    
    const intelligenceEvent: IntelligenceEvent = {
      event: event.event || 'intelligence_update',
      timestamp: Date.now(),
      persona: currentState.persona,
      confidence: currentState.confidence,
      device: currentState.device,
      intent: currentState.intent,
      optimization_applied: this.serializeOptimization(currentState.optimization),
      component_type: event.component_type,
      user_id: this.userId,
      session_id: this.sessionId,
      properties: event.properties || {}
    };

    this.events.push(intelligenceEvent);
    this.processEventForRealTimeInsights(intelligenceEvent);
  }

  public trackComponentPerformance(
    componentType: string,
    metricType: 'engagement' | 'conversion' | 'performance',
    value: number
  ): void {
    const currentState = intelligenceEngine.getCurrentState();
    
    const metric: ComponentPerformanceMetric = {
      component_type: componentType,
      persona: currentState.persona,
      device: currentState.device,
      optimization: this.getActiveOptimizationForComponent(componentType),
      metric_type: metricType,
      metric_value: value,
      timestamp: Date.now(),
      session_id: this.sessionId
    };

    this.performanceMetrics.push(metric);
    this.analyzePerformanceImprovement(metric);
  }

  public trackPersonaAccuracy(predictedPersona: PersonaType, actualPersona?: PersonaType): void {
    const currentState = intelligenceEngine.getCurrentState();
    
    const accuracyMetric: PersonaAccuracyMetric = {
      predicted_persona: predictedPersona,
      actual_persona: actualPersona,
      confidence: currentState.confidence,
      accuracy_score: actualPersona ? (predictedPersona === actualPersona ? 100 : 0) : undefined,
      correction_applied: !!actualPersona && predictedPersona !== actualPersona,
      timestamp: Date.now(),
      session_id: this.sessionId
    };

    this.accuracyMetrics.push(accuracyMetric);
    
    if (accuracyMetric.correction_applied) {
      this.handlePersonaCorrectionFeedback(accuracyMetric);
    }
  }

  public trackOptimizationEffectiveness(
    optimizationId: string,
    optimizationType: string,
    beforeMetric: number,
    afterMetric: number
  ): void {
    const currentState = intelligenceEngine.getCurrentState();
    const improvement = ((afterMetric - beforeMetric) / beforeMetric) * 100;
    
    const effectiveness: OptimizationEffectiveness = {
      optimization_id: optimizationId,
      optimization_type: optimizationType,
      persona: currentState.persona,
      device: currentState.device,
      before_metric: beforeMetric,
      after_metric: afterMetric,
      improvement_percentage: improvement,
      statistical_significance: this.calculateStatisticalSignificance(beforeMetric, afterMetric),
      timestamp: Date.now()
    };

    this.optimizationEffectiveness.push(effectiveness);
    this.updateIntelligenceBasedOnEffectiveness(effectiveness);
  }

  // Real-time analytics methods
  public getPersonaPerformanceMetrics(persona: PersonaType): ComponentPerformanceMetric[] {
    return this.performanceMetrics.filter(metric => metric.persona === persona);
  }

  public getDeviceOptimizationInsights(device: DeviceType): any {
    const deviceMetrics = this.performanceMetrics.filter(metric => metric.device === device);
    
    return {
      avgEngagement: this.calculateAverageMetric(deviceMetrics, 'engagement'),
      avgConversion: this.calculateAverageMetric(deviceMetrics, 'conversion'),
      avgPerformance: this.calculateAverageMetric(deviceMetrics, 'performance'),
      totalSessions: new Set(deviceMetrics.map(m => m.session_id)).size,
      bestOptimizations: this.getBestOptimizations(deviceMetrics)
    };
  }

  public getRealTimeInsights(): any {
    const recentEvents = this.events.filter(event => 
      Date.now() - event.timestamp < 300000 // Last 5 minutes
    );

    return {
      activeUsers: new Set(recentEvents.map(e => e.session_id)).size,
      topPersonas: this.getTopPersonas(recentEvents),
      deviceDistribution: this.getDeviceDistribution(recentEvents),
      intentDistribution: this.getIntentDistribution(recentEvents),
      optimizationPerformance: this.getOptimizationPerformance(),
      personaAccuracy: this.getPersonaAccuracy()
    };
  }

  // Private methods
  private initializeTracking(): void {
    // Subscribe to intelligence engine updates
    intelligenceEngine.subscribe((state: IntelligenceState) => {
      this.trackIntelligenceEvent({
        event: 'intelligence_state_update',
        properties: {
          persona_changed: true,
          new_confidence: state.confidence,
          optimization_changed: true
        }
      });
    });

    // Track page visibility changes
    document.addEventListener('visibilitychange', () => {
      this.trackIntelligenceEvent({
        event: document.hidden ? 'page_hidden' : 'page_visible',
        properties: {
          visibility_state: document.visibilityState
        }
      });
    });

    // Track performance metrics
    this.setupPerformanceObserver();
  }

  private setupPerformanceObserver(): void {
    if ('PerformanceObserver' in window) {
      // Track Core Web Vitals
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.trackIntelligenceEvent({
            event: 'core_web_vital',
            properties: {
              metric_name: entry.name,
              metric_value: entry.value,
              rating: this.getWebVitalRating(entry.name, entry.value)
            }
          });
        }
      }).observe({ entryTypes: ['web-vitals'] });

      // Track user interactions
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.trackIntelligenceEvent({
            event: 'user_interaction',
            properties: {
              interaction_type: entry.name,
              duration: entry.duration,
              start_time: entry.startTime
            }
          });
        }
      }).observe({ entryTypes: ['event'] });
    }
  }

  private setupBatchProcessing(): void {
    this.batchTimer = setInterval(() => {
      this.flushBatchedData();
    }, this.flushInterval);

    // Flush on page unload
    window.addEventListener('beforeunload', () => {
      this.flushBatchedData();
    });
  }

  private async flushBatchedData(): Promise<void> {
    if (this.events.length === 0) return;

    const batchData = {
      events: this.events.splice(0, this.batchSize),
      performance_metrics: this.performanceMetrics.splice(0, this.batchSize),
      accuracy_metrics: this.accuracyMetrics.splice(0, this.batchSize),
      optimization_effectiveness: this.optimizationEffectiveness.splice(0, this.batchSize),
      session_id: this.sessionId,
      user_id: this.userId,
      timestamp: Date.now()
    };

    try {
      await this.sendToAnalytics(batchData);
    } catch (error) {
      console.error('Failed to send analytics batch:', error);
      // Re-add failed events back to queue
      this.events.unshift(...batchData.events);
      this.performanceMetrics.unshift(...batchData.performance_metrics);
    }
  }

  private async sendToAnalytics(data: any): Promise<void> {
    const response = await fetch(this.analyticsEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`Analytics request failed: ${response.status}`);
    }
  }

  private processEventForRealTimeInsights(event: IntelligenceEvent): void {
    // Check for anomalies or significant changes
    if (event.event === 'intelligence_state_update') {
      this.detectPersonaShift(event);
      this.detectIntentEscalation(event);
    }

    // Update real-time dashboard if available
    this.updateRealTimeDashboard(event);
  }

  private analyzePerformanceImprovement(metric: ComponentPerformanceMetric): void {
    // Compare with historical data for the same component/persona/device combination
    const historicalMetrics = this.performanceMetrics.filter(m =>
      m.component_type === metric.component_type &&
      m.persona === metric.persona &&
      m.device === metric.device &&
      m.metric_type === metric.metric_type &&
      Date.now() - m.timestamp < 86400000 // Last 24 hours
    );

    if (historicalMetrics.length > 5) {
      const avgHistorical = historicalMetrics.reduce((sum, m) => sum + m.metric_value, 0) / historicalMetrics.length;
      const improvement = ((metric.metric_value - avgHistorical) / avgHistorical) * 100;

      if (Math.abs(improvement) > 10) { // Significant change
        this.trackIntelligenceEvent({
          event: 'performance_change_detected',
          component_type: metric.component_type,
          properties: {
            improvement_percentage: improvement,
            current_value: metric.metric_value,
            historical_average: avgHistorical,
            metric_type: metric.metric_type
          }
        });
      }
    }
  }

  private handlePersonaCorrectionFeedback(accuracyMetric: PersonaAccuracyMetric): void {
    // Send feedback to improve persona detection
    this.trackIntelligenceEvent({
      event: 'persona_correction_feedback',
      properties: {
        predicted_persona: accuracyMetric.predicted_persona,
        actual_persona: accuracyMetric.actual_persona,
        confidence: accuracyMetric.confidence,
        correction_source: 'user_feedback'
      }
    });

    // Update intelligence engine with corrected persona
    // Note: This would integrate with the intelligence engine's learning system
  }

  private updateIntelligenceBasedOnEffectiveness(effectiveness: OptimizationEffectiveness): void {
    // If optimization shows significant positive impact, increase its weight
    if (effectiveness.improvement_percentage > 20 && effectiveness.statistical_significance > 0.95) {
      this.trackIntelligenceEvent({
        event: 'optimization_success',
        properties: {
          optimization_id: effectiveness.optimization_id,
          optimization_type: effectiveness.optimization_type,
          improvement: effectiveness.improvement_percentage,
          action: 'increase_weight'
        }
      });
    }
    
    // If optimization shows negative impact, decrease its weight
    else if (effectiveness.improvement_percentage < -10 && effectiveness.statistical_significance > 0.95) {
      this.trackIntelligenceEvent({
        event: 'optimization_failure',
        properties: {
          optimization_id: effectiveness.optimization_id,
          optimization_type: effectiveness.optimization_type,
          decline: effectiveness.improvement_percentage,
          action: 'decrease_weight'
        }
      });
    }
  }

  // Utility methods
  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private serializeOptimization(optimization: any): string {
    return JSON.stringify({
      layout: optimization.layout.spacing,
      content: optimization.content.density,
      interaction: optimization.interactions.response_time,
      performance: optimization.performance.loading_priority
    });
  }

  private getActiveOptimizationForComponent(componentType: string): string {
    const optimizations = intelligenceEngine.getOptimizationsForComponent(componentType);
    return this.serializeOptimization(optimizations);
  }

  private calculateStatisticalSignificance(before: number, after: number): number {
    // Simplified statistical significance calculation
    // In production, this would use proper statistical tests
    const difference = Math.abs(after - before);
    const average = (before + after) / 2;
    return Math.min(1.0, difference / average);
  }

  private calculateAverageMetric(metrics: ComponentPerformanceMetric[], type: string): number {
    const filteredMetrics = metrics.filter(m => m.metric_type === type);
    if (filteredMetrics.length === 0) return 0;
    return filteredMetrics.reduce((sum, m) => sum + m.metric_value, 0) / filteredMetrics.length;
  }

  private getBestOptimizations(metrics: ComponentPerformanceMetric[]): string[] {
    const optimizationPerformance = new Map<string, number[]>();
    
    metrics.forEach(metric => {
      if (!optimizationPerformance.has(metric.optimization)) {
        optimizationPerformance.set(metric.optimization, []);
      }
      optimizationPerformance.get(metric.optimization)!.push(metric.metric_value);
    });

    return Array.from(optimizationPerformance.entries())
      .map(([optimization, values]) => ({
        optimization,
        avgValue: values.reduce((a, b) => a + b, 0) / values.length
      }))
      .sort((a, b) => b.avgValue - a.avgValue)
      .slice(0, 3)
      .map(item => item.optimization);
  }

  private getTopPersonas(events: IntelligenceEvent[]): Record<PersonaType, number> {
    const personaCounts: Record<string, number> = {};
    
    events.forEach(event => {
      personaCounts[event.persona] = (personaCounts[event.persona] || 0) + 1;
    });

    return personaCounts as Record<PersonaType, number>;
  }

  private getDeviceDistribution(events: IntelligenceEvent[]): Record<DeviceType, number> {
    const deviceCounts: Record<string, number> = {};
    
    events.forEach(event => {
      deviceCounts[event.device] = (deviceCounts[event.device] || 0) + 1;
    });

    return deviceCounts as Record<DeviceType, number>;
  }

  private getIntentDistribution(events: IntelligenceEvent[]): Record<string, number> {
    const intentCounts: Record<string, number> = {};
    
    events.forEach(event => {
      intentCounts[event.intent] = (intentCounts[event.intent] || 0) + 1;
    });

    return intentCounts;
  }

  private getOptimizationPerformance(): any {
    return this.optimizationEffectiveness.reduce((acc, oe) => {
      if (!acc[oe.optimization_type]) {
        acc[oe.optimization_type] = {
          total_tests: 0,
          avg_improvement: 0,
          success_rate: 0
        };
      }
      
      acc[oe.optimization_type].total_tests++;
      acc[oe.optimization_type].avg_improvement += oe.improvement_percentage;
      if (oe.improvement_percentage > 0) {
        acc[oe.optimization_type].success_rate++;
      }
      
      return acc;
    }, {} as Record<string, any>);
  }

  private getPersonaAccuracy(): number {
    const accurateMetrics = this.accuracyMetrics.filter(m => m.accuracy_score === 100);
    return this.accuracyMetrics.length > 0 
      ? (accurateMetrics.length / this.accuracyMetrics.length) * 100 
      : 0;
  }

  private detectPersonaShift(event: IntelligenceEvent): void {
    // Implementation for detecting significant persona changes
  }

  private detectIntentEscalation(event: IntelligenceEvent): void {
    // Implementation for detecting intent escalation
  }

  private updateRealTimeDashboard(event: IntelligenceEvent): void {
    // Implementation for real-time dashboard updates
  }

  private getWebVitalRating(metric: string, value: number): 'good' | 'needs-improvement' | 'poor' {
    const thresholds: Record<string, [number, number]> = {
      'CLS': [0.1, 0.25],
      'FID': [100, 300],
      'LCP': [2500, 4000],
      'FCP': [1800, 3000],
      'TTFB': [800, 1800]
    };

    const [good, poor] = thresholds[metric] || [0, Infinity];
    
    if (value <= good) return 'good';
    if (value <= poor) return 'needs-improvement';
    return 'poor';
  }
}

// Create and export singleton instance
export const analyticsIntelligenceBridge = new AnalyticsIntelligenceBridge();
export type { IntelligenceEvent, ComponentPerformanceMetric, PersonaAccuracyMetric };