'use client';

import { useEffect } from 'react';
import { useDevice } from '@/hooks/use-device';
import { useAnalytics } from '@/hooks/use-analytics';

export function DeviceOptimizer() {
  const { device, deviceInfo } = useDevice();
  const { track } = useAnalytics();

  useEffect(() => {
    // Track device information for optimization
    track({
      name: 'device_detected',
      category: 'intelligence',
      action: 'detect',
      label: device,
      custom_parameters: {
        device_type: device,
        screen_width: deviceInfo.width,
        screen_height: deviceInfo.height,
        orientation: deviceInfo.orientation,
        touch_capable: deviceInfo.touch,
        user_agent: typeof navigator !== 'undefined' ? navigator.userAgent : '',
      },
    });

    // Apply device-specific optimizations
    if (typeof document !== 'undefined') {
      // Add device class to document body for CSS targeting
      document.body.classList.remove('device-mobile', 'device-tablet', 'device-desktop');
      document.body.classList.add(`device-${device}`);

      // Add touch class if device supports touch
      if (deviceInfo.touch) {
        document.body.classList.add('touch-device');
      } else {
        document.body.classList.add('no-touch');
      }

      // Set CSS custom properties for device-specific styling
      document.documentElement.style.setProperty('--device-width', `${deviceInfo.width}px`);
      document.documentElement.style.setProperty('--device-height', `${deviceInfo.height}px`);
      document.documentElement.style.setProperty('--device-orientation', deviceInfo.orientation);
    }
  }, [device, deviceInfo, track]);

  // This component doesn't render anything visible
  return null;
}