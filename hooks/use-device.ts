'use client';

import { useState, useEffect } from 'react';
import { DeviceType, UseDeviceReturn } from '@/types';
import { debounce } from '@/lib/utils';

export function useDevice(): UseDeviceReturn {
  const [device, setDevice] = useState<DeviceType>('desktop');
  const [deviceInfo, setDeviceInfo] = useState({
    width: 0,
    height: 0,
    orientation: 'portrait' as 'portrait' | 'landscape',
    touch: false,
    mobile: false,
    tablet: false,
    desktop: false,
  });

  useEffect(() => {
    function updateDeviceInfo() {
      if (typeof window === 'undefined') return;

      const width = window.innerWidth;
      const height = window.innerHeight;
      const orientation = width > height ? 'landscape' : 'portrait';
      const touch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

      // Device type detection based on width
      let detectedDevice: DeviceType = 'desktop';
      if (width < 768) {
        detectedDevice = 'mobile';
      } else if (width < 1024) {
        detectedDevice = 'tablet';
      }

      // Additional touch-based refinement
      if (touch && width >= 768 && width < 1024) {
        detectedDevice = 'tablet';
      } else if (touch && width < 768) {
        detectedDevice = 'mobile';
      }

      const newDeviceInfo = {
        width,
        height,
        orientation,
        touch,
        mobile: detectedDevice === 'mobile',
        tablet: detectedDevice === 'tablet',
        desktop: detectedDevice === 'desktop',
      };

      setDevice(detectedDevice);
      setDeviceInfo(newDeviceInfo);
    }

    // Initial detection
    updateDeviceInfo();

    // Debounced resize handler to avoid excessive updates
    const debouncedUpdate = debounce(updateDeviceInfo, 150);
    
    window.addEventListener('resize', debouncedUpdate);
    window.addEventListener('orientationchange', debouncedUpdate);

    return () => {
      window.removeEventListener('resize', debouncedUpdate);
      window.removeEventListener('orientationchange', debouncedUpdate);
    };
  }, []);

  const setDeviceOverride = (newDevice: DeviceType) => {
    setDevice(newDevice);
    setDeviceInfo(prev => ({
      ...prev,
      mobile: newDevice === 'mobile',
      tablet: newDevice === 'tablet',
      desktop: newDevice === 'desktop',
    }));
  };

  return {
    device,
    deviceInfo,
    setDevice: setDeviceOverride,
  };
}