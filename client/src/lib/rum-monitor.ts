/**
 * Real User Monitoring (RUM) Integration
 * Tag 4: Advanced Monitoring Integration
 * 
 * Features:
 * - Core Web Vitals tracking (LCP, FID, CLS, TTFB)
 * - Custom business metrics correlation
 * - Performance budget violation detection
 * - Real-time alerting integration
 * - User experience correlation with conversion rates
 */

interface PerformanceMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  timestamp: number;
  url: string;
  userAgent: string;
  connection?: string;
  device?: string;
  persona?: string;
}

interface BusinessMetric {
  type: 'conversion' | 'engagement' | 'bounce' | 'revenue';
  value: number;
  timestamp: number;
  correlatedPerformance?: PerformanceMetric[];
}

interface RUMConfig {
  endpoint: string;
  apiKey: string;
  enableCoreWebVitals: boolean;
  enableBusinessCorrelation: boolean;
  enableBudgetMonitoring: boolean;
  enablePersonaTracking: boolean;
  samplingRate: number;
  bufferSize: number;
  flushInterval: number;
}

// Performance Budget Thresholds (aligned with lighthouse-budgets.config.js)
const PERFORMANCE_BUDGETS = {
  'largest-contentful-paint': {
    good: 2500,
    poor: 4000
  },
  'first-input-delay': {
    good: 100,
    poor: 300
  },
  'cumulative-layout-shift': {
    good: 0.1,
    poor: 0.25
  },
  'first-contentful-paint': {
    good: 1800,
    poor: 3000
  },
  'time-to-first-byte': {
    good: 800,
    poor: 1800
  }
};

class RealUserMonitor {
  private config: RUMConfig;
  private metricsBuffer: PerformanceMetric[] = [];
  private businessMetricsBuffer: BusinessMetric[] = [];
  private flushTimer: NodeJS.Timeout | null = null;
  private isEnabled: boolean = false;
  private sessionId: string;
  private userId?: string;
  private persona?: string;

  constructor(config: Partial<RUMConfig> = {}) {
    this.config = {
      endpoint: '/api/metrics/rum',
      apiKey: process.env.NEXT_PUBLIC_RUM_API_KEY || '',
      enableCoreWebVitals: true,
      enableBusinessCorrelation: true,
      enableBudgetMonitoring: true,
      enablePersonaTracking: true,
      samplingRate: 1.0, // 100% sampling for development, adjust for production
      bufferSize: 50,
      flushInterval: 30000, // 30 seconds
      ...config
    };

    this.sessionId = this.generateSessionId();
    this.isEnabled = this.shouldSample();

    if (this.isEnabled) {
      this.initialize();
    }
  }

  private generateSessionId(): string {
    return `rum_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private shouldSample(): boolean {
    return Math.random() < this.config.samplingRate;
  }

  private initialize(): void {
    // Initialize Web Vitals tracking
    if (this.config.enableCoreWebVitals) {
      this.setupWebVitalsTracking();
    }

    // Initialize business metrics correlation
    if (this.config.enableBusinessCorrelation) {
      this.setupBusinessMetricsTracking();
    }

    // Initialize persona detection
    if (this.config.enablePersonaTracking) {
      this.detectPersona();
    }

    // Setup periodic flush
    this.startPeriodicFlush();

    // Setup page visibility change handler
    this.setupVisibilityChangeHandler();

    console.log('🔍 RUM Monitor initialized', {
      sessionId: this.sessionId,
      samplingRate: this.config.samplingRate,
      features: {
        coreWebVitals: this.config.enableCoreWebVitals,
        businessCorrelation: this.config.enableBusinessCorrelation,
        budgetMonitoring: this.config.enableBudgetMonitoring,
        personaTracking: this.config.enablePersonaTracking
      }
    });
  }

  private setupWebVitalsTracking(): void {
    // Track LCP (Largest Contentful Paint)
    this.observePerformanceEntry('largest-contentful-paint', (entries) => {
      const lcp = entries[entries.length - 1];
      this.trackMetric('largest-contentful-paint', lcp.startTime);
    });

    // Track FID (First Input Delay)
    this.observePerformanceEntry('first-input', (entries) => {
      entries.forEach(entry => {
        const fid = entry.processingStart - entry.startTime;
        this.trackMetric('first-input-delay', fid);
      });
    });

    // Track CLS (Cumulative Layout Shift)
    let clsValue = 0;
    this.observePerformanceEntry('layout-shift', (entries) => {
      entries.forEach(entry => {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      });
      this.trackMetric('cumulative-layout-shift', clsValue);
    });

    // Track FCP (First Contentful Paint)
    this.observePerformanceEntry('paint', (entries) => {
      const fcp = entries.find(entry => entry.name === 'first-contentful-paint');
      if (fcp) {
        this.trackMetric('first-contentful-paint', fcp.startTime);
      }
    });

    // Track TTFB (Time to First Byte)
    this.observeNavigationTiming();
  }

  private observePerformanceEntry(entryType: string, callback: (entries: any[]) => void): void {
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          callback(list.getEntries());
        });
        observer.observe({ entryTypes: [entryType] });
      } catch (error) {
        console.warn(`Failed to observe ${entryType}:`, error);
      }
    }
  }

  private observeNavigationTiming(): void {
    if ('performance' in window && 'timing' in performance) {
      window.addEventListener('load', () => {
        setTimeout(() => {
          const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
          if (navigation) {
            const ttfb = navigation.responseStart - navigation.fetchStart;
            this.trackMetric('time-to-first-byte', ttfb);
          }
        }, 0);
      });
    }
  }

  private trackMetric(name: string, value: number): void {
    if (!this.isEnabled) return;

    const rating = this.getRating(name, value);
    const metric: PerformanceMetric = {
      name,
      value,
      rating,
      timestamp: Date.now(),
      url: window.location.href,
      userAgent: navigator.userAgent,
      connection: this.getConnectionInfo(),
      device: this.getDeviceType(),
      persona: this.persona
    };

    this.metricsBuffer.push(metric);

    // Check for budget violations
    if (this.config.enableBudgetMonitoring) {
      this.checkBudgetViolation(metric);
    }

    // Flush if buffer is full
    if (this.metricsBuffer.length >= this.config.bufferSize) {
      this.flush();
    }

    console.log('📊 RUM Metric tracked:', { name, value, rating });
  }

  private getRating(metricName: string, value: number): 'good' | 'needs-improvement' | 'poor' {
    const budget = PERFORMANCE_BUDGETS[metricName as keyof typeof PERFORMANCE_BUDGETS];
    if (!budget) return 'good';

    if (value <= budget.good) return 'good';
    if (value <= budget.poor) return 'needs-improvement';
    return 'poor';
  }

  private getConnectionInfo(): string {
    const connection = (navigator as any).connection || (navigator as any).mozConnection || (navigator as any).webkitConnection;
    return connection ? `${connection.effectiveType || 'unknown'}_${connection.downlink || 0}mbps` : 'unknown';
  }

  private getDeviceType(): string {
    const userAgent = navigator.userAgent;
    if (/tablet|ipad|playbook|silk/i.test(userAgent)) return 'tablet';
    if (/mobile|iphone|ipod|android|blackberry|opera|mini|windows\sce|palm|smartphone|iemobile/i.test(userAgent)) return 'mobile';
    return 'desktop';
  }

  private detectPersona(): void {
    // Persona detection based on behavior patterns
    // This can be enhanced with ML models or user segmentation
    const userAgent = navigator.userAgent;
    const screenSize = `${window.screen.width}x${window.screen.height}`;
    const timeOfDay = new Date().getHours();

    let persona = 'Unknown';

    // Simple persona detection logic (can be enhanced)
    if (/iPhone|iPad/i.test(userAgent) && timeOfDay >= 18) {
      persona = 'RemoteDad';
    } else if (screenSize.includes('1920') && timeOfDay >= 9 && timeOfDay <= 17) {
      persona = 'BusinessOwner';
    } else if (/Android/i.test(userAgent) && timeOfDay >= 20) {
      persona = 'StudentHustler';
    } else if (/Chrome/i.test(userAgent) && !userAgent.includes('Mobile')) {
      persona = 'TechEarlyAdopter';
    }

    this.persona = persona;
  }

  private checkBudgetViolation(metric: PerformanceMetric): void {
    if (metric.rating === 'poor') {
      console.warn('🚨 Performance Budget Violation Detected:', metric);
      
      // Send immediate alert for critical violations
      this.sendImmediateAlert({
        type: 'budget_violation',
        metric: metric.name,
        value: metric.value,
        threshold: PERFORMANCE_BUDGETS[metric.name as keyof typeof PERFORMANCE_BUDGETS]?.poor,
        url: metric.url,
        sessionId: this.sessionId,
        persona: this.persona
      });
    }
  }

  private setupBusinessMetricsTracking(): void {
    // Track conversion events
    this.trackConversionEvents();
    
    // Track engagement metrics
    this.trackEngagementMetrics();
    
    // Track bounce rate correlation
    this.trackBounceRate();
  }

  private trackConversionEvents(): void {
    // Listen for conversion events (can be triggered by business logic)
    window.addEventListener('conversion', (event: any) => {
      const conversionMetric: BusinessMetric = {
        type: 'conversion',
        value: event.detail.value || 1,
        timestamp: Date.now(),
        correlatedPerformance: this.getRecentPerformanceMetrics()
      };
      
      this.businessMetricsBuffer.push(conversionMetric);
      console.log('💰 Conversion tracked with performance correlation');
    });
  }

  private trackEngagementMetrics(): void {
    let engagementStartTime = Date.now();
    
    // Track scroll depth
    let maxScrollDepth = 0;
    window.addEventListener('scroll', () => {
      const scrollDepth = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
      maxScrollDepth = Math.max(maxScrollDepth, scrollDepth);
    });

    // Track time on page
    window.addEventListener('beforeunload', () => {
      const timeOnPage = Date.now() - engagementStartTime;
      const engagementMetric: BusinessMetric = {
        type: 'engagement',
        value: timeOnPage,
        timestamp: Date.now(),
        correlatedPerformance: this.getRecentPerformanceMetrics()
      };
      
      this.businessMetricsBuffer.push(engagementMetric);
    });
  }

  private trackBounceRate(): void {
    let hasInteracted = false;
    const interactionEvents = ['click', 'scroll', 'keydown', 'touchstart'];
    
    interactionEvents.forEach(eventType => {
      window.addEventListener(eventType, () => {
        if (!hasInteracted) {
          hasInteracted = true;
          // User has interacted, not a bounce
        }
      }, { once: true });
    });

    window.addEventListener('beforeunload', () => {
      if (!hasInteracted) {
        const bounceMetric: BusinessMetric = {
          type: 'bounce',
          value: 1,
          timestamp: Date.now(),
          correlatedPerformance: this.getRecentPerformanceMetrics()
        };
        
        this.businessMetricsBuffer.push(bounceMetric);
      }
    });
  }

  private getRecentPerformanceMetrics(): PerformanceMetric[] {
    const fiveMinutesAgo = Date.now() - (5 * 60 * 1000);
    return this.metricsBuffer.filter(metric => metric.timestamp > fiveMinutesAgo);
  }

  private startPeriodicFlush(): void {
    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.config.flushInterval);
  }

  private setupVisibilityChangeHandler(): void {
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // Page is being hidden, flush immediately
        this.flush();
      }
    });
  }

  private async flush(): Promise<void> {
    if (this.metricsBuffer.length === 0 && this.businessMetricsBuffer.length === 0) {
      return;
    }

    const payload = {
      sessionId: this.sessionId,
      userId: this.userId,
      persona: this.persona,
      timestamp: Date.now(),
      performanceMetrics: [...this.metricsBuffer],
      businessMetrics: [...this.businessMetricsBuffer],
      environment: process.env.NODE_ENV,
      version: process.env.NEXT_PUBLIC_APP_VERSION,
      url: window.location.href
    };

    try {
      const response = await fetch(this.config.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`,
          'X-RUM-Session': this.sessionId
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        console.log('📊 RUM data flushed successfully', {
          performanceMetrics: this.metricsBuffer.length,
          businessMetrics: this.businessMetricsBuffer.length
        });
        
        // Clear buffers
        this.metricsBuffer = [];
        this.businessMetricsBuffer = [];
      } else {
        console.error('Failed to flush RUM data:', response.status);
      }
    } catch (error) {
      console.error('Error flushing RUM data:', error);
    }
  }

  private async sendImmediateAlert(alert: any): Promise<void> {
    try {
      await fetch('/api/alerts/performance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`
        },
        body: JSON.stringify(alert)
      });
    } catch (error) {
      console.error('Error sending performance alert:', error);
    }
  }

  // Public API methods
  public setUserId(userId: string): void {
    this.userId = userId;
  }

  public setPersona(persona: string): void {
    this.persona = persona;
  }

  public trackCustomMetric(name: string, value: number, metadata?: any): void {
    const customMetric: PerformanceMetric = {
      name: `custom_${name}`,
      value,
      rating: 'good', // Custom metrics don't have predefined ratings
      timestamp: Date.now(),
      url: window.location.href,
      userAgent: navigator.userAgent,
      connection: this.getConnectionInfo(),
      device: this.getDeviceType(),
      persona: this.persona
    };

    this.metricsBuffer.push(customMetric);
  }

  public trackBusinessEvent(type: BusinessMetric['type'], value: number): void {
    const businessMetric: BusinessMetric = {
      type,
      value,
      timestamp: Date.now(),
      correlatedPerformance: this.getRecentPerformanceMetrics()
    };

    this.businessMetricsBuffer.push(businessMetric);

    // Dispatch custom event for other parts of the application
    window.dispatchEvent(new CustomEvent('rum-business-event', {
      detail: businessMetric
    }));
  }

  public forceFlush(): Promise<void> {
    return this.flush();
  }

  public destroy(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
    }
    
    // Final flush before destroying
    this.flush();
    
    this.isEnabled = false;
    console.log('🔍 RUM Monitor destroyed');
  }
}

// Global RUM instance
let rumInstance: RealUserMonitor | null = null;

export function initializeRUM(config?: Partial<RUMConfig>): RealUserMonitor {
  if (rumInstance) {
    console.warn('RUM already initialized');
    return rumInstance;
  }

  rumInstance = new RealUserMonitor(config);
  
  // Expose to window for debugging
  if (typeof window !== 'undefined') {
    (window as any).rum = rumInstance;
  }

  return rumInstance;
}

export function getRUM(): RealUserMonitor | null {
  return rumInstance;
}

export { RealUserMonitor, type PerformanceMetric, type BusinessMetric, type RUMConfig };