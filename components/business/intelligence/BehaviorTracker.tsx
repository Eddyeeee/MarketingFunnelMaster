'use client';

import { useEffect, useRef } from 'react';
import { useAnalytics } from '@/hooks/use-analytics';
import { usePersona } from '@/hooks/use-persona';
import { debounce } from '@/lib/utils';

export function BehaviorTracker() {
  const { track } = useAnalytics();
  const { persona } = usePersona();
  const startTime = useRef(Date.now());
  const scrollDepth = useRef(0);
  const clickCount = useRef(0);

  useEffect(() => {
    // Track page engagement time
    const trackEngagementTime = () => {
      const timeOnPage = Date.now() - startTime.current;
      
      track({
        name: 'page_engagement',
        category: 'engagement',
        action: 'time_on_page',
        label: 'session_end',
        value: Math.round(timeOnPage / 1000), // Convert to seconds
        custom_parameters: {
          time_on_page_seconds: Math.round(timeOnPage / 1000),
          scroll_depth_percent: scrollDepth.current,
          click_count: clickCount.current,
          persona,
        },
      });
    };

    // Track scroll depth
    const trackScrollDepth = debounce(() => {
      const windowHeight = window.innerHeight;
      const documentHeight = Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      const currentScrollDepth = Math.round(
        ((scrollTop + windowHeight) / documentHeight) * 100
      );
      
      if (currentScrollDepth > scrollDepth.current) {
        scrollDepth.current = Math.min(100, currentScrollDepth);
        
        // Track scroll milestones
        if (scrollDepth.current >= 25 && scrollDepth.current < 50) {
          track({
            name: 'scroll_depth',
            category: 'engagement',
            action: 'scroll',
            label: '25_percent',
            value: 25,
          });
        } else if (scrollDepth.current >= 50 && scrollDepth.current < 75) {
          track({
            name: 'scroll_depth',
            category: 'engagement',
            action: 'scroll',
            label: '50_percent',
            value: 50,
          });
        } else if (scrollDepth.current >= 75 && scrollDepth.current < 90) {
          track({
            name: 'scroll_depth',
            category: 'engagement',
            action: 'scroll',
            label: '75_percent',
            value: 75,
          });
        } else if (scrollDepth.current >= 90) {
          track({
            name: 'scroll_depth',
            category: 'engagement',
            action: 'scroll',
            label: '90_percent',
            value: 90,
          });
        }
      }
    }, 500);

    // Track clicks
    const trackClicks = (event: MouseEvent) => {
      clickCount.current++;
      
      const target = event.target as HTMLElement;
      const tagName = target.tagName.toLowerCase();
      const className = target.className;
      const id = target.id;
      
      track({
        name: 'click_interaction',
        category: 'engagement',
        action: 'click',
        label: tagName,
        custom_parameters: {
          element_tag: tagName,
          element_class: className,
          element_id: id,
          click_count: clickCount.current,
          time_to_click: Date.now() - startTime.current,
        },
      });
    };

    // Track mouse movement patterns (simplified)
    let mouseMovements = 0;
    const trackMouseMovement = debounce(() => {
      mouseMovements++;
      
      if (mouseMovements % 50 === 0) { // Track every 50 movements
        track({
          name: 'mouse_activity',
          category: 'engagement',
          action: 'movement',
          label: 'activity_burst',
          value: mouseMovements,
        });
      }
    }, 100);

    // Track keyboard interactions
    const trackKeyboard = (event: KeyboardEvent) => {
      track({
        name: 'keyboard_interaction',
        category: 'engagement',
        action: 'keypress',
        label: event.key,
        custom_parameters: {
          key: event.key,
          ctrl_key: event.ctrlKey,
          alt_key: event.altKey,
          shift_key: event.shiftKey,
        },
      });
    };

    // Track page visibility changes
    const trackVisibilityChange = () => {
      const isVisible = !document.hidden;
      
      track({
        name: 'page_visibility',
        category: 'engagement',
        action: isVisible ? 'visible' : 'hidden',
        label: 'visibility_change',
        custom_parameters: {
          visibility_state: document.visibilityState,
          time_on_page: Date.now() - startTime.current,
        },
      });
    };

    // Add event listeners
    window.addEventListener('scroll', trackScrollDepth);
    document.addEventListener('click', trackClicks);
    document.addEventListener('mousemove', trackMouseMovement);
    document.addEventListener('keydown', trackKeyboard);
    document.addEventListener('visibilitychange', trackVisibilityChange);
    window.addEventListener('beforeunload', trackEngagementTime);

    // Cleanup function
    return () => {
      window.removeEventListener('scroll', trackScrollDepth);
      document.removeEventListener('click', trackClicks);
      document.removeEventListener('mousemove', trackMouseMovement);
      document.removeEventListener('keydown', trackKeyboard);
      document.removeEventListener('visibilitychange', trackVisibilityChange);
      window.removeEventListener('beforeunload', trackEngagementTime);
      
      // Track final engagement time
      trackEngagementTime();
    };
  }, [track, persona]);

  // Track initial page load
  useEffect(() => {
    track({
      name: 'page_load',
      category: 'engagement',
      action: 'load',
      label: 'initial_load',
      custom_parameters: {
        load_time: Date.now() - startTime.current,
        referrer: document.referrer,
        user_agent: navigator.userAgent,
      },
    });
  }, [track]);

  // This component doesn't render anything visible
  return null;
}