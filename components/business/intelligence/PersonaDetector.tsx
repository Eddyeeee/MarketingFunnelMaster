'use client';

import { useEffect } from 'react';
import { usePersona } from '@/hooks/use-persona';
import { useAnalytics } from '@/hooks/use-analytics';

export function PersonaDetector() {
  const { persona, confidence, detectPersona } = usePersona();
  const { track } = useAnalytics();

  useEffect(() => {
    // Start persona detection after component mounts
    const startDetection = async () => {
      try {
        await detectPersona();
        
        // Track successful persona detection
        track({
          name: 'persona_detected',
          category: 'intelligence',
          action: 'detect',
          label: persona,
          value: confidence,
          custom_parameters: {
            detected_persona: persona,
            confidence_score: confidence,
            detection_method: 'automatic',
          },
        });
      } catch (error) {
        console.error('Persona detection failed:', error);
        
        track({
          name: 'persona_detection_error',
          category: 'intelligence',
          action: 'error',
          label: 'detection_failed',
        });
      }
    };

    // Only run detection if persona is unknown or confidence is low
    if (persona === 'unknown' || confidence < 50) {
      // Delay detection to allow page to load and collect behavior data
      const timeoutId = setTimeout(startDetection, 2000);
      return () => clearTimeout(timeoutId);
    }
  }, [detectPersona, persona, confidence, track]);

  // This component doesn't render anything visible
  return null;
}