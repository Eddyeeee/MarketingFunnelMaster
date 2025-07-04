'use client';

import { useEffect } from 'react';
import { useAnalytics } from '@/hooks/use-analytics';

interface PerformanceMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
}

export function PerformanceMonitor() {
  const { track } = useAnalytics();

  useEffect(() => {
    // Function to get performance rating based on thresholds
    const getPerformanceRating = (name: string, value: number): 'good' | 'needs-improvement' | 'poor' => {
      const thresholds = {
        LCP: { good: 2500, poor: 4000 },
        FID: { good: 100, poor: 300 },
        CLS: { good: 0.1, poor: 0.25 },
        FCP: { good: 1800, poor: 3000 },
        TTFB: { good: 800, poor: 1800 },
      };

      const threshold = thresholds[name as keyof typeof thresholds];
      if (!threshold) return 'good';

      if (value <= threshold.good) return 'good';
      if (value <= threshold.poor) return 'needs-improvement';
      return 'poor';
    };

    // Function to track a performance metric
    const trackMetric = (metric: PerformanceMetric) => {
      track({
        name: 'web_vital',
        category: 'performance',
        action: 'measure',
        label: metric.name,
        value: Math.round(metric.value),
        custom_parameters: {
          metric_name: metric.name,
          metric_value: metric.value,
          metric_rating: metric.rating,
          url: window.location.href,
          user_agent: navigator.userAgent,
        },
      });

      // Console log in development
      if (process.env.NODE_ENV === 'development') {
        console.log(`Web Vital [${metric.name}]:`, {
          value: metric.value,
          rating: metric.rating,
        });
      }
    };

    // Largest Contentful Paint (LCP)
    const observeLCP = () => {
      if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          const lastEntry = entries[entries.length - 1];
          
          const metric: PerformanceMetric = {
            name: 'LCP',
            value: lastEntry.startTime,
            rating: getPerformanceRating('LCP', lastEntry.startTime),
          };
          
          trackMetric(metric);
        });

        try {
          observer.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {
          console.warn('LCP observation not supported');
        }
      }
    };

    // First Input Delay (FID)
    const observeFID = () => {
      if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          
          entries.forEach((entry) => {
            const metric: PerformanceMetric = {
              name: 'FID',
              value: entry.processingStart - entry.startTime,
              rating: getPerformanceRating('FID', entry.processingStart - entry.startTime),
            };
            
            trackMetric(metric);
          });
        });

        try {
          observer.observe({ entryTypes: ['first-input'] });
        } catch (e) {
          console.warn('FID observation not supported');
        }
      }
    };

    // Cumulative Layout Shift (CLS)
    const observeCLS = () => {
      if ('PerformanceObserver' in window) {
        let clsValue = 0;
        let clsEntries: PerformanceEntry[] = [];

        const observer = new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          
          entries.forEach((entry) => {
            // Only count layout shifts without recent user input
            if (!(entry as any).hadRecentInput) {
              clsValue += (entry as any).value;
              clsEntries.push(entry);
            }
          });
        });

        try {
          observer.observe({ entryTypes: ['layout-shift'] });
          
          // Track CLS on page unload
          window.addEventListener('beforeunload', () => {
            const metric: PerformanceMetric = {
              name: 'CLS',
              value: clsValue,
              rating: getPerformanceRating('CLS', clsValue),
            };
            
            trackMetric(metric);
          });
        } catch (e) {
          console.warn('CLS observation not supported');
        }
      }
    };

    // First Contentful Paint (FCP)
    const observeFCP = () => {
      if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          
          entries.forEach((entry) => {
            if (entry.name === 'first-contentful-paint') {
              const metric: PerformanceMetric = {
                name: 'FCP',
                value: entry.startTime,
                rating: getPerformanceRating('FCP', entry.startTime),
              };
              
              trackMetric(metric);
            }
          });
        });

        try {
          observer.observe({ entryTypes: ['paint'] });
        } catch (e) {
          console.warn('FCP observation not supported');
        }
      }
    };

    // Time to First Byte (TTFB)
    const measureTTFB = () => {
      if ('performance' in window && 'getEntriesByType' in performance) {
        const navigationEntries = performance.getEntriesByType('navigation') as PerformanceNavigationTiming[];
        
        if (navigationEntries.length > 0) {
          const navEntry = navigationEntries[0];
          const ttfb = navEntry.responseStart - navEntry.requestStart;
          
          const metric: PerformanceMetric = {
            name: 'TTFB',
            value: ttfb,
            rating: getPerformanceRating('TTFB', ttfb),
          };
          
          trackMetric(metric);
        }
      }
    };

    // Custom metrics
    const trackCustomMetrics = () => {
      // JavaScript bundle size
      if ('performance' in window) {
        const resourceEntries = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
        
        let totalJSSize = 0;
        let totalCSSSize = 0;
        
        resourceEntries.forEach((entry) => {
          if (entry.name.includes('.js')) {
            totalJSSize += entry.transferSize || 0;
          } else if (entry.name.includes('.css')) {
            totalCSSSize += entry.transferSize || 0;
          }
        });

        track({
          name: 'bundle_size',
          category: 'performance',
          action: 'measure',
          label: 'resource_sizes',
          custom_parameters: {
            total_js_size: totalJSSize,
            total_css_size: totalCSSSize,
            total_resources: resourceEntries.length,
          },
        });
      }

      // Memory usage (if available)
      if ('memory' in performance) {
        const memoryInfo = (performance as any).memory;
        
        track({
          name: 'memory_usage',
          category: 'performance',
          action: 'measure',
          label: 'memory',
          custom_parameters: {
            used_js_heap_size: memoryInfo.usedJSHeapSize,
            total_js_heap_size: memoryInfo.totalJSHeapSize,
            js_heap_size_limit: memoryInfo.jsHeapSizeLimit,
          },
        });
      }
    };

    // Start observing all metrics
    observeLCP();
    observeFID();
    observeCLS();
    observeFCP();
    
    // Measure TTFB and custom metrics after a short delay
    setTimeout(() => {
      measureTTFB();
      trackCustomMetrics();
    }, 1000);

    // Track page load performance
    window.addEventListener('load', () => {
      const loadTime = performance.now();
      
      track({
        name: 'page_load_time',
        category: 'performance',
        action: 'measure',
        label: 'total_load_time',
        value: Math.round(loadTime),
        custom_parameters: {
          load_time_ms: loadTime,
          page_url: window.location.href,
        },
      });
    });

  }, [track]);

  // This component doesn't render anything visible
  return null;
}