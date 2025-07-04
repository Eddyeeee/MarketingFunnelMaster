'use client';

import { useCallback } from 'react';
import { AnalyticsEvent, ConversionGoal, UseAnalyticsReturn } from '@/types';
import { useBrand } from './use-brand';
import { usePersona } from './use-persona';
import { useDevice } from './use-device';

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    fbq?: (...args: any[]) => void;
    analytics?: {
      track: (event: string, properties?: Record<string, any>) => void;
      identify: (userId: string, traits?: Record<string, any>) => void;
      page: (name?: string, properties?: Record<string, any>) => void;
    };
  }
}

export function useAnalytics(): UseAnalyticsReturn {
  const { brand, brandConfig } = useBrand();
  const { persona } = usePersona();
  const { device } = useDevice();

  const track = useCallback((event: AnalyticsEvent) => {
    if (typeof window === 'undefined') return;

    // Enhanced event data with context
    const enhancedEvent = {
      ...event,
      custom_parameters: {
        ...event.custom_parameters,
        brand,
        persona,
        device,
        timestamp: new Date().toISOString(),
        session_id: getSessionId(),
        page_url: window.location.href,
        page_title: document.title,
        referrer: document.referrer,
      },
    };

    // Google Analytics 4
    if (window.gtag && brandConfig.analytics.ga4_id) {
      window.gtag('event', event.name, {
        event_category: event.category,
        event_label: event.label,
        value: event.value,
        custom_map: enhancedEvent.custom_parameters,
        send_to: brandConfig.analytics.ga4_id,
      });
    }

    // Facebook Pixel
    if (window.fbq && brandConfig.analytics.facebook_pixel_id) {
      window.fbq('track', event.name, enhancedEvent.custom_parameters);
    }

    // Custom Analytics (e.g., Segment, Mixpanel)
    if (window.analytics) {
      window.analytics.track(event.name, enhancedEvent.custom_parameters);
    }

    // Console logging in development
    if (process.env.NODE_ENV === 'development') {
      console.log('Analytics Event:', enhancedEvent);
    }

    // Store event for offline sync if needed
    storeEventForOfflineSync(enhancedEvent);
  }, [brand, brandConfig, persona, device]);

  const trackPageView = useCallback((path: string) => {
    if (typeof window === 'undefined') return;

    const pageData = {
      page_location: window.location.href,
      page_path: path,
      page_title: document.title,
      brand,
      persona,
      device,
    };

    // Google Analytics 4
    if (window.gtag && brandConfig.analytics.ga4_id) {
      window.gtag('config', brandConfig.analytics.ga4_id, {
        page_location: pageData.page_location,
        page_title: pageData.page_title,
        custom_map: pageData,
      });
    }

    // Custom Analytics
    if (window.analytics) {
      window.analytics.page(pageData.page_title, pageData);
    }

    if (process.env.NODE_ENV === 'development') {
      console.log('Page View:', pageData);
    }
  }, [brand, brandConfig, persona, device]);

  const trackConversion = useCallback((goal: ConversionGoal) => {
    const conversionEvent: AnalyticsEvent = {
      name: 'conversion',
      category: 'conversion',
      action: goal.type,
      label: goal.name,
      value: goal.value,
      custom_parameters: {
        goal_id: goal.id,
        goal_type: goal.type,
        goal_target: goal.target,
        persona_specific: goal.persona_specific?.includes(persona),
      },
    };

    track(conversionEvent);

    // Additional conversion tracking
    if (typeof window !== 'undefined') {
      // Google Ads Conversion
      if (window.gtag) {
        window.gtag('event', 'conversion', {
          send_to: `AW-CONVERSION_ID/${goal.id}`,
          value: goal.value,
          currency: 'USD',
        });
      }

      // Facebook Conversion
      if (window.fbq) {
        window.fbq('track', 'Purchase', {
          value: goal.value,
          currency: 'USD',
          content_ids: [goal.id],
          content_type: 'product',
        });
      }
    }
  }, [track, persona]);

  const identify = useCallback((userId: string, traits?: Record<string, any>) => {
    if (typeof window === 'undefined') return;

    const userTraits = {
      ...traits,
      brand,
      persona,
      device,
      identified_at: new Date().toISOString(),
    };

    // Google Analytics 4 User ID
    if (window.gtag && brandConfig.analytics.ga4_id) {
      window.gtag('config', brandConfig.analytics.ga4_id, {
        user_id: userId,
        custom_map: userTraits,
      });
    }

    // Custom Analytics
    if (window.analytics) {
      window.analytics.identify(userId, userTraits);
    }

    // Store user ID for session
    if (typeof window !== 'undefined') {
      localStorage.setItem('analytics_user_id', userId);
      localStorage.setItem('analytics_user_traits', JSON.stringify(userTraits));
    }

    if (process.env.NODE_ENV === 'development') {
      console.log('User Identified:', { userId, traits: userTraits });
    }
  }, [brand, brandConfig, persona, device]);

  const reset = useCallback(() => {
    if (typeof window === 'undefined') return;

    // Clear stored user data
    localStorage.removeItem('analytics_user_id');
    localStorage.removeItem('analytics_user_traits');
    localStorage.removeItem('analytics_session_id');

    // Reset analytics tools
    if (window.analytics) {
      window.analytics.reset?.();
    }

    if (process.env.NODE_ENV === 'development') {
      console.log('Analytics Reset');
    }
  }, []);

  return {
    track,
    trackPageView,
    trackConversion,
    identify,
    reset,
  };
}

// Helper functions
function getSessionId(): string {
  if (typeof window === 'undefined') return '';

  let sessionId = localStorage.getItem('analytics_session_id');
  
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('analytics_session_id', sessionId);
  }
  
  return sessionId;
}

function storeEventForOfflineSync(event: any): void {
  if (typeof window === 'undefined') return;

  try {
    const offlineEvents = JSON.parse(
      localStorage.getItem('analytics_offline_events') || '[]'
    );
    
    offlineEvents.push(event);
    
    // Keep only last 100 events to prevent storage overflow
    if (offlineEvents.length > 100) {
      offlineEvents.splice(0, offlineEvents.length - 100);
    }
    
    localStorage.setItem('analytics_offline_events', JSON.stringify(offlineEvents));
  } catch (error) {
    console.warn('Failed to store offline analytics event:', error);
  }
}

// Enhanced tracking hooks for specific use cases
export function useTrackClick(elementName: string, category = 'interaction') {
  const { track } = useAnalytics();
  
  return useCallback(() => {
    track({
      name: 'click',
      category,
      action: 'click',
      label: elementName,
    });
  }, [track, elementName, category]);
}

export function useTrackFormSubmission(formName: string) {
  const { track } = useAnalytics();
  
  return useCallback((success: boolean, errorMessage?: string) => {
    track({
      name: success ? 'form_submit_success' : 'form_submit_error',
      category: 'form',
      action: 'submit',
      label: formName,
      custom_parameters: {
        success,
        error_message: errorMessage,
      },
    });
  }, [track, formName]);
}

export function useTrackPageSection(sectionName: string) {
  const { track } = useAnalytics();
  
  return useCallback((action: 'view' | 'interact' | 'complete') => {
    track({
      name: 'section_engagement',
      category: 'engagement',
      action,
      label: sectionName,
    });
  }, [track, sectionName]);
}

export function useTrackVideoEngagement(videoName: string) {
  const { track } = useAnalytics();
  
  return useCallback((action: 'play' | 'pause' | 'complete' | 'seek', currentTime?: number) => {
    track({
      name: 'video_engagement',
      category: 'media',
      action,
      label: videoName,
      value: currentTime,
      custom_parameters: {
        video_name: videoName,
        current_time: currentTime,
      },
    });
  }, [track, videoName]);
}

export function useTrackProductInteraction(productId: string) {
  const { track } = useAnalytics();
  
  return useCallback((action: 'view' | 'add_to_cart' | 'purchase' | 'wishlist', value?: number) => {
    track({
      name: 'product_interaction',
      category: 'ecommerce',
      action,
      label: productId,
      value,
      custom_parameters: {
        product_id: productId,
      },
    });
  }, [track, productId]);
}