import { useEffect, useState, useCallback } from 'react';

interface PerformanceMetrics {
  lcp: number | null;
  fid: number | null;
  cls: number | null;
  fcp: number | null;
  ttfb: number | null;
}

export function usePerformance() {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    lcp: null,
    fid: null,
    cls: null,
    fcp: null,
    ttfb: null
  });

  const [performanceScore, setPerformanceScore] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate performance measurement
    setTimeout(() => {
      setMetrics({
        lcp: 1500,
        fid: 50,
        cls: 0.05,
        fcp: 1200,
        ttfb: 400
      });
      setPerformanceScore(95);
      setIsLoading(false);
    }, 1000);
  }, []);

  const getOptimizationSuggestions = useCallback(() => {
    const suggestions: string[] = [];
    
    if (metrics.lcp && metrics.lcp > 2500) {
      suggestions.push('Optimize Largest Contentful Paint');
    }
    
    if (metrics.fid && metrics.fid > 100) {
      suggestions.push('Reduce First Input Delay');
    }
    
    return suggestions;
  }, [metrics]);

  return {
    metrics,
    performanceScore,
    isLoading,
    getOptimizationSuggestions
  };
}

export default usePerformance; 