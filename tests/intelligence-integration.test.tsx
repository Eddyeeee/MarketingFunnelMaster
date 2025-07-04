/**
 * Intelligence Integration Test Suite v2.0
 * Comprehensive testing for Module 3B Week 2 - Intelligence Integration
 * 
 * Tests persona detection, component adaptation, and analytics integration
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import { jest } from '@jest/globals';

// Mock implementations
jest.mock('@/lib/intelligence-engine');
jest.mock('@/lib/analytics-intelligence-bridge');
jest.mock('@/hooks/use-persona');

import { IntelligentHeroSection } from '@/components/business/intelligence/IntelligentHeroSection';
import { IntelligentCTA } from '@/components/business/intelligence/IntelligentCTA';
import { IntelligentNavigation } from '@/components/business/intelligence/IntelligentNavigation';
import { useIntelligence, useComponentIntelligence, usePersonaContent } from '@/hooks/use-intelligence';
import { useAnalyticsIntelligence } from '@/hooks/use-analytics-intelligence';

// Mock return values for intelligence hooks
const mockIntelligenceState = {
  persona: 'TechEarlyAdopter' as const,
  confidence: 85,
  device: 'desktop' as const,
  intent: 'consideration' as const,
  optimizations: {
    layout: {
      columns: 3,
      spacing: 'comfortable',
      navigation: 'horizontal',
      cta_placement: 'inline'
    },
    content: {
      density: 'dense',
      tone: 'technical',
      emphasis: 'interactive',
      trust_factors: ['tech-specs', 'reviews', 'innovation']
    },
    interactions: {
      input_method: 'mouse',
      response_time: 'delayed',
      feedback_style: 'subtle',
      guidance_level: 'minimal'
    },
    performance: {
      loading_priority: 'interactive',
      bundle_size: 'standard',
      prefetch_strategy: 'none',
      caching_level: 'smart'
    }
  },
  lastUpdate: Date.now(),
  isPersonaConfident: true,
  shouldOptimizeForMobile: false,
  shouldShowAdvancedFeatures: true,
  shouldUseUrgentCTA: false
};

const mockAnalytics = {
  trackEvent: jest.fn(),
  trackPersonaDetection: jest.fn(),
  trackComponentEngagement: jest.fn(),
  trackConversionEvent: jest.fn(),
  trackOptimizationApplied: jest.fn(),
  trackUserInteraction: jest.fn(),
  getRealTimeInsights: jest.fn(() => ({
    activeUsers: 5,
    topPersonas: { TechEarlyAdopter: 3, BusinessOwner: 2 },
    deviceDistribution: { desktop: 3, mobile: 2 }
  }))
};

// Mock the hooks
(useIntelligence as jest.Mock).mockReturnValue(mockIntelligenceState);
(useComponentIntelligence as jest.Mock).mockReturnValue({
  ...mockIntelligenceState,
  getLayoutClasses: () => 'grid-cols-3 gap-4 p-4',
  getContentClasses: () => 'text-sm leading-tight space-y-2',
  getInteractionClasses: () => 'mouse-optimized hover-effects',
  shouldUseCompactLayout: false,
  shouldUseDenseContent: true
});
(usePersonaContent as jest.Mock).mockReturnValue({
  persona: 'TechEarlyAdopter',
  confidence: 85,
  getPersonaText: (options: any) => options.TechEarlyAdopter || options.fallback,
  getPersonaCTA: () => 'Try Beta Access',
  getTrustFactors: () => ['tech-specs', 'reviews', 'innovation'],
  contentTone: 'technical',
  contentDensity: 'dense',
  contentEmphasis: 'interactive'
});
(useAnalyticsIntelligence as jest.Mock).mockReturnValue(mockAnalytics);

describe('Intelligence Integration - Persona Detection', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should detect TechEarlyAdopter persona and apply appropriate optimizations', () => {
    render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Check if persona-specific content is rendered
    expect(screen.getByText(/Next-Gen TestProduct: Revolutionary Technology/)).toBeInTheDocument();
    expect(screen.getByText(/Advanced algorithms and cutting-edge infrastructure/)).toBeInTheDocument();
    expect(screen.getByText(/Try Beta Access/)).toBeInTheDocument();
    
    // Check for persona confidence badge
    expect(screen.getByText(/Optimized for TechEarlyAdopter \(85% confidence\)/)).toBeInTheDocument();
  });

  test('should adapt content for different personas', () => {
    // Test RemoteDad persona
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      persona: 'RemoteDad',
      confidence: 75
    });
    (usePersonaContent as jest.Mock).mockReturnValue({
      persona: 'RemoteDad',
      confidence: 75,
      getPersonaText: (options: any) => options.RemoteDad || options.fallback,
      getPersonaCTA: () => 'Start Free Trial',
      getTrustFactors: () => ['family-friendly', 'value', 'reliability'],
      contentTone: 'casual',
      contentDensity: 'moderate'
    });

    render(<IntelligentHeroSection productName="TestProduct" />);
    
    expect(screen.getByText(/TestProduct: More Time for What Matters Most/)).toBeInTheDocument();
    expect(screen.getByText(/Spend less time on tedious tasks/)).toBeInTheDocument();
    expect(screen.getByText(/Start Free Trial/)).toBeInTheDocument();
  });

  test('should handle unknown persona with fallback content', () => {
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      persona: 'unknown',
      confidence: 20
    });
    (usePersonaContent as jest.Mock).mockReturnValue({
      persona: 'unknown',
      confidence: 20,
      getPersonaText: (options: any) => options.fallback,
      getPersonaCTA: () => 'Get Started',
      getTrustFactors: () => ['testimonials', 'social_proof'],
      contentTone: 'casual'
    });

    render(<IntelligentHeroSection productName="TestProduct" />);
    
    expect(screen.getByText(/Transform Your Life with TestProduct/)).toBeInTheDocument();
    expect(screen.getByText(/Get Started/)).toBeInTheDocument();
    // Should not show confidence badge for low confidence
    expect(screen.queryByText(/Optimized for/)).not.toBeInTheDocument();
  });
});

describe('Intelligence Integration - Device Optimization', () => {
  test('should optimize layout for mobile devices', () => {
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      device: 'mobile',
      shouldOptimizeForMobile: true
    });
    (useComponentIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      device: 'mobile',
      optimizations: {
        ...mockIntelligenceState.optimizations,
        layout: {
          columns: 1,
          spacing: 'compact',
          navigation: 'hamburger',
          cta_placement: 'sticky'
        }
      },
      getLayoutClasses: () => 'grid-cols-1 gap-2 p-2',
      shouldUseCompactLayout: true
    });

    render(<IntelligentCTA productName="TestProduct" />);
    
    // Should render mobile-optimized CTA
    const primaryButton = screen.getByRole('button', { name: /Try Beta Access/ });
    expect(primaryButton).toHaveClass('w-full'); // Mobile CTA should be full width
  });

  test('should optimize navigation for different devices', () => {
    // Test mobile navigation
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      device: 'mobile'
    });
    (useComponentIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      device: 'mobile',
      optimizations: {
        ...mockIntelligenceState.optimizations,
        layout: { ...mockIntelligenceState.optimizations.layout, navigation: 'hamburger' }
      }
    });

    render(<IntelligentNavigation brandName="TestBrand" />);
    
    // Should show hamburger menu for mobile
    expect(screen.getByRole('button', { name: /menu/i })).toBeInTheDocument();
  });
});

describe('Intelligence Integration - Intent Recognition', () => {
  test('should show urgency indicators for high purchase intent', () => {
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      intent: 'purchase',
      shouldUseUrgentCTA: true
    });

    render(<IntelligentCTA productName="TestProduct" />);
    
    // Should show urgency indicators
    expect(screen.getByText(/Special offer expires in/)).toBeInTheDocument();
    
    // CTA should have urgent styling
    const primaryButton = screen.getByRole('button');
    expect(primaryButton).toHaveTextContent(/🔥/); // Fire emoji for urgency
  });

  test('should adapt CTA based on intent level', () => {
    // Test awareness stage
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      intent: 'awareness'
    });
    (usePersonaContent as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      getPersonaCTA: () => 'Explore Features',
      getPersonaText: (options: any) => options.TechEarlyAdopter || options.fallback
    });

    const { rerender } = render(<IntelligentCTA productName="TestProduct" />);
    expect(screen.getByText(/Explore Features/)).toBeInTheDocument();

    // Test decision stage
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      intent: 'decision'
    });
    (usePersonaContent as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      getPersonaCTA: () => 'Get Early Access Now',
      getPersonaText: (options: any) => options.TechEarlyAdopter || options.fallback
    });

    rerender(<IntelligentCTA productName="TestProduct" />);
    expect(screen.getByText(/Get Early Access Now/)).toBeInTheDocument();
  });
});

describe('Intelligence Integration - Analytics Tracking', () => {
  test('should track persona detection events', async () => {
    render(<IntelligentHeroSection productName="TestProduct" />);
    
    await waitFor(() => {
      expect(mockAnalytics.trackPersonaDetection).toHaveBeenCalledWith('TechEarlyAdopter', 85);
    });
  });

  test('should track component interactions', async () => {
    const onCTAClick = jest.fn();
    render(<IntelligentCTA productName="TestProduct" primaryAction={onCTAClick} />);
    
    const primaryButton = screen.getByRole('button', { name: /Try Beta Access/ });
    fireEvent.click(primaryButton);
    
    expect(onCTAClick).toHaveBeenCalled();
    await waitFor(() => {
      expect(mockAnalytics.trackUserInteraction).toHaveBeenCalledWith(
        'CallToAction',
        'cta_click',
        expect.any(Number)
      );
    });
  });

  test('should track optimization applications', () => {
    render(<IntelligentHeroSection productName="TestProduct" />);
    
    expect(mockAnalytics.trackOptimizationApplied).toHaveBeenCalledWith(
      'persona_optimization',
      'HeroSection'
    );
  });

  test('should track component performance metrics', async () => {
    const { unmount } = render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Simulate component lifecycle
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 100));
    });
    
    unmount();
    
    await waitFor(() => {
      expect(mockAnalytics.trackEvent).toHaveBeenCalledWith(
        'component_unmount',
        expect.objectContaining({
          component_type: 'HeroSection',
          engagement_duration: expect.any(Number)
        })
      );
    });
  });
});

describe('Intelligence Integration - Component Adaptation', () => {
  test('should apply persona-specific styling and content', () => {
    render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Check for TechEarlyAdopter specific elements
    expect(screen.getByText(/Revolutionary Technology/)).toBeInTheDocument();
    expect(screen.getByText(/View Documentation/)).toBeInTheDocument();
    
    // Check for technical tone indicators
    const heroSection = screen.getByRole('region');
    expect(heroSection).toHaveClass('bg-gradient-to-br', 'from-slate-900');
  });

  test('should show persona-specific trust factors', () => {
    render(<IntelligentCTA productName="TestProduct" />);
    
    // Should show TechEarlyAdopter trust factors
    expect(screen.getByText(/tech-specs/)).toBeInTheDocument();
    expect(screen.getByText(/reviews/)).toBeInTheDocument();
    expect(screen.getByText(/innovation/)).toBeInTheDocument();
  });

  test('should adapt navigation items based on persona', () => {
    render(<IntelligentNavigation brandName="TestBrand" />);
    
    // Should show TechEarlyAdopter specific navigation items
    expect(screen.getByText(/API Docs/)).toBeInTheDocument();
    expect(screen.getByText(/Technical Specs/)).toBeInTheDocument();
  });
});

describe('Intelligence Integration - Real-time Adaptation', () => {
  test('should update optimizations when intelligence state changes', async () => {
    const { rerender } = render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Change persona
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      persona: 'BusinessOwner',
      confidence: 90
    });
    (usePersonaContent as jest.Mock).mockReturnValue({
      persona: 'BusinessOwner',
      confidence: 90,
      getPersonaText: (options: any) => options.BusinessOwner || options.fallback,
      getPersonaCTA: () => 'Schedule Demo',
      getTrustFactors: () => ['roi', 'scalability', 'support'],
      contentTone: 'professional'
    });

    rerender(<IntelligentHeroSection productName="TestProduct" />);
    
    await waitFor(() => {
      expect(screen.getByText(/Scale Your Business Exponentially/)).toBeInTheDocument();
      expect(screen.getByText(/Schedule Demo/)).toBeInTheDocument();
    });
  });

  test('should handle confidence changes appropriately', () => {
    // Test low confidence scenario
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      confidence: 30,
      isPersonaConfident: false
    });

    render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Should not show confidence badge for low confidence
    expect(screen.queryByText(/Optimized for/)).not.toBeInTheDocument();
  });
});

describe('Intelligence Integration - Error Handling', () => {
  test('should handle intelligence engine failures gracefully', () => {
    // Mock intelligence engine failure
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      error: 'Intelligence engine failed',
      persona: 'unknown',
      confidence: 0
    });

    render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Should still render with fallback content
    expect(screen.getByText(/Transform Your Life with TestProduct/)).toBeInTheDocument();
  });

  test('should handle analytics failures without breaking components', () => {
    // Mock analytics failure
    mockAnalytics.trackEvent.mockImplementation(() => {
      throw new Error('Analytics failed');
    });

    // Component should still render despite analytics failure
    expect(() => {
      render(<IntelligentHeroSection productName="TestProduct" />);
    }).not.toThrow();
  });
});

describe('Intelligence Integration - Performance', () => {
  test('should not cause excessive re-renders', () => {
    const renderSpy = jest.fn();
    
    const TestComponent = () => {
      renderSpy();
      return <IntelligentHeroSection productName="TestProduct" />;
    };

    const { rerender } = render(<TestComponent />);
    
    // Initial render
    expect(renderSpy).toHaveBeenCalledTimes(1);
    
    // Re-render with same props should not cause additional renders
    rerender(<TestComponent />);
    expect(renderSpy).toHaveBeenCalledTimes(2);
  });

  test('should handle rapid intelligence updates efficiently', async () => {
    const { rerender } = render(<IntelligentHeroSection productName="TestProduct" />);
    
    // Simulate rapid updates
    for (let i = 0; i < 10; i++) {
      (useIntelligence as jest.Mock).mockReturnValue({
        ...mockIntelligenceState,
        confidence: 50 + i * 5,
        lastUpdate: Date.now() + i
      });
      
      rerender(<IntelligentHeroSection productName="TestProduct" />);
    }
    
    // Should handle updates without errors
    expect(screen.getByText(/Revolutionary Technology/)).toBeInTheDocument();
  });
});

// Integration test suite summary
describe('Intelligence Integration - E2E Scenarios', () => {
  test('complete user journey with persona detection and optimization', async () => {
    // 1. Initial load with unknown persona
    (useIntelligence as jest.Mock).mockReturnValue({
      ...mockIntelligenceState,
      persona: 'unknown',
      confidence: 0
    });

    const { rerender } = render(
      <div>
        <IntelligentNavigation brandName="TestBrand" />
        <IntelligentHeroSection productName="TestProduct" />
        <IntelligentCTA productName="TestProduct" />
      </div>
    );

    // 2. Persona detection occurs
    await act(async () => {
      (useIntelligence as jest.Mock).mockReturnValue({
        ...mockIntelligenceState,
        persona: 'TechEarlyAdopter',
        confidence: 85
      });
      
      rerender(
        <div>
          <IntelligentNavigation brandName="TestBrand" />
          <IntelligentHeroSection productName="TestProduct" />
          <IntelligentCTA productName="TestProduct" />
        </div>
      );
    });

    // 3. Verify persona-specific optimizations are applied
    expect(screen.getByText(/API Docs/)).toBeInTheDocument();
    expect(screen.getByText(/Revolutionary Technology/)).toBeInTheDocument();
    expect(screen.getByText(/Try Beta Access/)).toBeInTheDocument();

    // 4. Verify analytics tracking
    await waitFor(() => {
      expect(mockAnalytics.trackPersonaDetection).toHaveBeenCalled();
      expect(mockAnalytics.trackOptimizationApplied).toHaveBeenCalled();
    });
  });
});

export { mockIntelligenceState, mockAnalytics };