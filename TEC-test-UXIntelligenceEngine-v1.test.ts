/**
 * UXIntelligenceEngine Test Suite v1.0
 * Comprehensive testing for persona detection, device optimization, 
 * intent recognition, and real-time adaptation
 */

import { UXIntelligenceEngine } from './TEC-code-UXIntelligenceEngine-v1';

describe('UXIntelligenceEngine', () => {
  let engine: UXIntelligenceEngine;

  beforeEach(() => {
    engine = new UXIntelligenceEngine();
  });

  describe('Persona Detection', () => {
    test('should detect TechEarlyAdopter persona', () => {
      const userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.124';
      const behavior = {
        clickSpeed: 0.9,
        scrollPattern: 'fast' as const,
        navigationDepth: 8,
        timeDistribution: [120, 180, 90, 150],
        interactionStyle: 'exploratory' as const,
        sessionCount: 5,
        avgSessionDuration: 900
      };

      const persona = engine.personaDetection(userAgent, behavior);

      expect(persona.type).toBe('TechEarlyAdopter');
      expect(persona.confidence).toBeGreaterThan(70);
      expect(persona.characteristics.techSavviness).toBe('high');
    });

    test('should detect RemoteDad persona', () => {
      const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';
      const behavior = {
        clickSpeed: 0.4,
        scrollPattern: 'medium' as const,
        navigationDepth: 5,
        timeDistribution: [300, 240, 180, 120],
        interactionStyle: 'cautious' as const,
        sessionCount: 3,
        avgSessionDuration: 600
      };

      const persona = engine.personaDetection(userAgent, behavior);

      expect(persona.type).toBe('RemoteDad');
      expect(persona.characteristics.priceSensitivity).toBe('high');
      expect(persona.preferences.contentType).toBe('visual');
    });

    test('should detect StudentHustler persona', () => {
      const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36';
      const behavior = {
        clickSpeed: 0.8,
        scrollPattern: 'fast' as const,
        navigationDepth: 15,
        timeDistribution: [60, 90, 120, 45],
        interactionStyle: 'decisive' as const,
        sessionCount: 8,
        avgSessionDuration: 300
      };

      const persona = engine.personaDetection(userAgent, behavior);

      expect(persona.type).toBe('StudentHustler');
      expect(persona.characteristics.priceSensitivity).toBe('high');
      expect(persona.characteristics.purchaseUrgency).toBe('high');
    });

    test('should detect BusinessOwner persona', () => {
      const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';
      const behavior = {
        clickSpeed: 0.6,
        scrollPattern: 'medium' as const,
        navigationDepth: 7,
        timeDistribution: [180, 240, 300, 200],
        interactionStyle: 'decisive' as const,
        sessionCount: 4,
        avgSessionDuration: 720
      };

      const persona = engine.personaDetection(userAgent, behavior);

      expect(persona.type).toBe('BusinessOwner');
      expect(persona.characteristics.priceSensitivity).toBe('low');
      expect(persona.preferences.trustFactors).toContain('roi');
    });

    test('should handle edge cases with low confidence', () => {
      const userAgent = 'Mozilla/5.0 (compatible; unknown)';
      const behavior = {
        clickSpeed: 0.5,
        scrollPattern: 'medium' as const,
        navigationDepth: 1,
        timeDistribution: [30],
        interactionStyle: 'cautious' as const,
        sessionCount: 1,
        avgSessionDuration: 60
      };

      const persona = engine.personaDetection(userAgent, behavior);

      expect(persona.confidence).toBeLessThan(50);
      expect(persona.type).toBeDefined();
    });
  });

  describe('Device Optimization', () => {
    test('should optimize for mobile devices', () => {
      const device = {
        type: 'mobile' as const,
        screen: { width: 375, height: 667, pixelRatio: 2 },
        performance: { cpu: 'medium' as const, memory: 3, connection: 'medium' as const },
        input: { touch: true, mouse: false, keyboard: false },
        capabilities: { webgl: true, webp: true, modernJS: true }
      };

      const layout = engine.deviceOptimization(device);

      expect(layout.layout.columns).toBe(1);
      expect(layout.layout.navigation).toBe('hamburger');
      expect(layout.layout.cta).toBe('sticky-bottom');
      expect(layout.performance.maxLoadTime).toBe(3000);
    });

    test('should optimize for tablet devices', () => {
      const device = {
        type: 'tablet' as const,
        screen: { width: 768, height: 1024, pixelRatio: 2 },
        performance: { cpu: 'high' as const, memory: 4, connection: 'fast' as const },
        input: { touch: true, mouse: false, keyboard: false },
        capabilities: { webgl: true, webp: true, modernJS: true }
      };

      const layout = engine.deviceOptimization(device);

      expect(layout.layout.columns).toBe(2);
      expect(layout.layout.navigation).toBe('sidebar');
      expect(layout.layout.cta).toBe('floating');
    });

    test('should optimize for desktop devices', () => {
      const device = {
        type: 'desktop' as const,
        screen: { width: 1920, height: 1080, pixelRatio: 1 },
        performance: { cpu: 'high' as const, memory: 8, connection: 'fast' as const },
        input: { touch: false, mouse: true, keyboard: true },
        capabilities: { webgl: true, webp: true, modernJS: true }
      };

      const layout = engine.deviceOptimization(device);

      expect(layout.layout.columns).toBe(3);
      expect(layout.layout.navigation).toBe('horizontal');
      expect(layout.performance.maxLoadTime).toBe(2000);
    });

    test('should adjust for slow connection', () => {
      const device = {
        type: 'mobile' as const,
        screen: { width: 375, height: 667, pixelRatio: 2 },
        performance: { cpu: 'low' as const, memory: 2, connection: 'slow' as const },
        input: { touch: true, mouse: false, keyboard: false },
        capabilities: { webgl: false, webp: false, modernJS: false }
      };

      const layout = engine.deviceOptimization(device);

      expect(layout.performance.maxLoadTime).toBeGreaterThan(4000);
      expect(layout.assets.imageQuality).toBe('low');
      expect(layout.assets.videoAutoplay).toBe(false);
    });
  });

  describe('Intent Recognition', () => {
    test('should recognize high purchase intent', () => {
      const userPath = {
        pages: ['home', 'products', 'pricing', 'checkout', 'payment'],
        timestamps: [0, 30000, 60000, 120000, 180000],
        interactions: [
          { type: 'click' as const, element: 'cta-button', timestamp: 15000 },
          { type: 'scroll' as const, element: 'pricing-table', timestamp: 75000 },
          { type: 'form' as const, element: 'checkout-form', timestamp: 150000 },
          { type: 'click' as const, element: 'buy-now', timestamp: 170000 }
        ],
        referrer: 'google.com',
        exitPage: 'payment'
      };

      const intent = engine.intentRecognition(userPath);

      expect(intent.score).toBeGreaterThan(70);
      expect(intent.stage).toBe('purchase');
      expect(intent.predictedConversion).toBeGreaterThan(60);
    });

    test('should recognize medium purchase intent', () => {
      const userPath = {
        pages: ['home', 'products', 'blog', 'about'],
        timestamps: [0, 45000, 90000, 135000],
        interactions: [
          { type: 'scroll' as const, element: 'content', timestamp: 30000 },
          { type: 'click' as const, element: 'product-link', timestamp: 60000 },
          { type: 'hover' as const, element: 'navigation', timestamp: 100000 }
        ],
        referrer: 'facebook.com',
        exitPage: 'about'
      };

      const intent = engine.intentRecognition(userPath);

      expect(intent.score).toBeLessThan(70);
      expect(intent.score).toBeGreaterThan(30);
      expect(intent.stage).toBeOneOf(['awareness', 'consideration']);
    });

    test('should recognize low purchase intent', () => {
      const userPath = {
        pages: ['home', 'blog'],
        timestamps: [0, 15000],
        interactions: [
          { type: 'scroll' as const, element: 'content', timestamp: 10000 }
        ],
        referrer: 'direct',
        exitPage: 'blog'
      };

      const intent = engine.intentRecognition(userPath);

      expect(intent.score).toBeLessThan(40);
      expect(intent.stage).toBe('awareness');
      expect(intent.urgency).toBe('low');
    });

    test('should calculate urgency correctly', () => {
      const highUrgencyPath = {
        pages: ['home', 'pricing', 'checkout'],
        timestamps: [0, 30000, 60000],
        interactions: Array(20).fill(null).map((_, i) => ({
          type: 'click' as const,
          element: `element-${i}`,
          timestamp: i * 3000
        })),
        referrer: 'google.com',
        exitPage: 'checkout'
      };

      const intent = engine.intentRecognition(highUrgencyPath);

      expect(intent.urgency).toBe('high');
    });
  });

  describe('Real-time Adaptation', () => {
    test('should adapt for performance issues', () => {
      const metrics = {
        performance: {
          loadTime: 5000,
          renderTime: 1000,
          interactionDelay: 500
        },
        engagement: {
          scrollDepth: 0.8,
          timeOnPage: 120,
          clickThroughRate: 0.05,
          bounceRate: 0.3
        },
        conversion: {
          conversionRate: 0.03,
          abandonmentRate: 0.2,
          upsellRate: 0.1
        }
      };

      const adjustments = engine.realTimeAdaptation(metrics);

      expect(adjustments.performance).toBeDefined();
      expect(adjustments.performance!.enableLazyLoading).toBe(true);
      expect(adjustments.performance!.reduceImageQuality).toBe(true);
    });

    test('should adapt for low engagement', () => {
      const metrics = {
        performance: {
          loadTime: 2000,
          renderTime: 500,
          interactionDelay: 100
        },
        engagement: {
          scrollDepth: 0.1,
          timeOnPage: 15,
          clickThroughRate: 0.01,
          bounceRate: 0.8
        },
        conversion: {
          conversionRate: 0.02,
          abandonmentRate: 0.3,
          upsellRate: 0.05
        }
      };

      const adjustments = engine.realTimeAdaptation(metrics);

      expect(adjustments.engagement).toBeDefined();
      expect(adjustments.engagement!.addProgressIndicator).toBe(true);
      expect(adjustments.engagement!.addInteractiveElements).toBe(true);
    });

    test('should adapt for low conversion', () => {
      const metrics = {
        performance: {
          loadTime: 2000,
          renderTime: 500,
          interactionDelay: 100
        },
        engagement: {
          scrollDepth: 0.6,
          timeOnPage: 90,
          clickThroughRate: 0.03,
          bounceRate: 0.4
        },
        conversion: {
          conversionRate: 0.005,
          abandonmentRate: 0.7,
          upsellRate: 0.01
        }
      };

      const adjustments = engine.realTimeAdaptation(metrics);

      expect(adjustments.conversion).toBeDefined();
      expect(adjustments.conversion!.highlightValueProposition).toBe(true);
      expect(adjustments.conversion!.offerIncentives).toBe(true);
    });

    test('should not adapt when metrics are good', () => {
      const metrics = {
        performance: {
          loadTime: 1500,
          renderTime: 300,
          interactionDelay: 50
        },
        engagement: {
          scrollDepth: 0.7,
          timeOnPage: 180,
          clickThroughRate: 0.08,
          bounceRate: 0.2
        },
        conversion: {
          conversionRate: 0.05,
          abandonmentRate: 0.1,
          upsellRate: 0.15
        }
      };

      const adjustments = engine.realTimeAdaptation(metrics);

      expect(Object.keys(adjustments)).toHaveLength(0);
    });
  });

  describe('Integration Tests', () => {
    test('should provide comprehensive UX optimization', () => {
      const userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15';
      const behavior = {
        clickSpeed: 0.7,
        scrollPattern: 'medium' as const,
        navigationDepth: 6,
        timeDistribution: [90, 120, 150, 180],
        interactionStyle: 'cautious' as const,
        sessionCount: 3,
        avgSessionDuration: 540
      };
      const device = {
        type: 'mobile' as const,
        screen: { width: 375, height: 812, pixelRatio: 3 },
        performance: { cpu: 'medium' as const, memory: 4, connection: 'medium' as const },
        input: { touch: true, mouse: false, keyboard: false },
        capabilities: { webgl: true, webp: true, modernJS: true }
      };
      const userPath = {
        pages: ['home', 'products', 'pricing'],
        timestamps: [0, 60000, 120000],
        interactions: [
          { type: 'scroll' as const, element: 'content', timestamp: 30000 },
          { type: 'click' as const, element: 'product-link', timestamp: 75000 }
        ],
        referrer: 'google.com',
        exitPage: 'pricing'
      };
      const metrics = {
        performance: {
          loadTime: 2500,
          renderTime: 600,
          interactionDelay: 200
        },
        engagement: {
          scrollDepth: 0.4,
          timeOnPage: 120,
          clickThroughRate: 0.03,
          bounceRate: 0.5
        },
        conversion: {
          conversionRate: 0.02,
          abandonmentRate: 0.3,
          upsellRate: 0.08
        }
      };

      const result = engine.optimizeUX(userAgent, behavior, device, userPath, metrics);

      expect(result.persona).toBeDefined();
      expect(result.layout).toBeDefined();
      expect(result.intent).toBeDefined();
      expect(result.adjustments).toBeDefined();

      // Verify mobile optimization
      expect(result.layout.layout.columns).toBe(1);
      expect(result.layout.layout.navigation).toBe('hamburger');

      // Verify intent recognition
      expect(result.intent.stage).toBeOneOf(['awareness', 'consideration', 'decision']);

      // Verify persona detection
      expect(result.persona.type).toBeOneOf(['TechEarlyAdopter', 'RemoteDad', 'StudentHustler', 'BusinessOwner']);
    });

    test('should maintain state between calls', () => {
      const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';
      const behavior = {
        clickSpeed: 0.8,
        scrollPattern: 'fast' as const,
        navigationDepth: 10,
        timeDistribution: [60, 90, 120, 150],
        interactionStyle: 'exploratory' as const,
        sessionCount: 7,
        avgSessionDuration: 450
      };

      const persona = engine.personaDetection(userAgent, behavior);
      
      expect(engine.getCurrentPersona()).toEqual(persona);
      expect(engine.getCurrentPersona()?.type).toBe(persona.type);
    });
  });

  describe('Performance Tests', () => {
    test('should detect persona within performance threshold', () => {
      const userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36';
      const behavior = {
        clickSpeed: 0.9,
        scrollPattern: 'fast' as const,
        navigationDepth: 8,
        timeDistribution: [120, 180, 90, 150],
        interactionStyle: 'exploratory' as const,
        sessionCount: 5,
        avgSessionDuration: 900
      };

      const start = performance.now();
      engine.personaDetection(userAgent, behavior);
      const end = performance.now();

      expect(end - start).toBeLessThan(200); // 200ms threshold
    });

    test('should optimize device within performance threshold', () => {
      const device = {
        type: 'desktop' as const,
        screen: { width: 1920, height: 1080, pixelRatio: 1 },
        performance: { cpu: 'high' as const, memory: 8, connection: 'fast' as const },
        input: { touch: false, mouse: true, keyboard: true },
        capabilities: { webgl: true, webp: true, modernJS: true }
      };

      const start = performance.now();
      engine.deviceOptimization(device);
      const end = performance.now();

      expect(end - start).toBeLessThan(100); // 100ms threshold
    });

    test('should recognize intent within performance threshold', () => {
      const userPath = {
        pages: ['home', 'products', 'pricing', 'checkout'],
        timestamps: [0, 30000, 60000, 120000],
        interactions: Array(10).fill(null).map((_, i) => ({
          type: 'click' as const,
          element: `element-${i}`,
          timestamp: i * 10000
        })),
        referrer: 'google.com',
        exitPage: 'checkout'
      };

      const start = performance.now();
      engine.intentRecognition(userPath);
      const end = performance.now();

      expect(end - start).toBeLessThan(500); // 500ms threshold
    });

    test('should adapt in real-time within performance threshold', () => {
      const metrics = {
        performance: {
          loadTime: 4000,
          renderTime: 800,
          interactionDelay: 300
        },
        engagement: {
          scrollDepth: 0.2,
          timeOnPage: 30,
          clickThroughRate: 0.02,
          bounceRate: 0.7
        },
        conversion: {
          conversionRate: 0.01,
          abandonmentRate: 0.5,
          upsellRate: 0.03
        }
      };

      const start = performance.now();
      engine.realTimeAdaptation(metrics);
      const end = performance.now();

      expect(end - start).toBeLessThan(50); // 50ms threshold
    });
  });

  describe('Error Handling', () => {
    test('should handle invalid user agent gracefully', () => {
      const behavior = {
        clickSpeed: 0.5,
        scrollPattern: 'medium' as const,
        navigationDepth: 5,
        timeDistribution: [60, 90, 120],
        interactionStyle: 'cautious' as const,
        sessionCount: 2,
        avgSessionDuration: 300
      };

      expect(() => {
        engine.personaDetection('', behavior);
      }).not.toThrow();

      expect(() => {
        engine.personaDetection('invalid-user-agent', behavior);
      }).not.toThrow();
    });

    test('should handle empty user path gracefully', () => {
      const emptyPath = {
        pages: [],
        timestamps: [],
        interactions: [],
        referrer: '',
        exitPage: ''
      };

      expect(() => {
        engine.intentRecognition(emptyPath);
      }).not.toThrow();

      const intent = engine.intentRecognition(emptyPath);
      expect(intent.score).toBe(0);
      expect(intent.stage).toBe('awareness');
    });

    test('should handle extreme metric values', () => {
      const extremeMetrics = {
        performance: {
          loadTime: 999999,
          renderTime: 999999,
          interactionDelay: 999999
        },
        engagement: {
          scrollDepth: 999,
          timeOnPage: 999999,
          clickThroughRate: 999,
          bounceRate: 999
        },
        conversion: {
          conversionRate: 999,
          abandonmentRate: 999,
          upsellRate: 999
        }
      };

      expect(() => {
        engine.realTimeAdaptation(extremeMetrics);
      }).not.toThrow();
    });
  });
});

// Helper function for Jest custom matchers
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeOneOf(expected: any[]): R;
    }
  }
}

expect.extend({
  toBeOneOf(received, expected) {
    const pass = expected.includes(received);
    if (pass) {
      return {
        message: () => `expected ${received} not to be one of ${expected}`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${received} to be one of ${expected}`,
        pass: false,
      };
    }
  },
});

export {};