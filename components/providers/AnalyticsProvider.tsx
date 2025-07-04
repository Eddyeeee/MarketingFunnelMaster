'use client';

import { ReactNode, useEffect } from 'react';
import { useBrand } from '@/hooks/use-brand';
import { usePathname } from 'next/navigation';
import { useAnalytics } from '@/hooks/use-analytics';

interface AnalyticsProviderProps {
  children: ReactNode;
}

export function AnalyticsProvider({ children }: AnalyticsProviderProps) {
  const { brandConfig } = useBrand();
  const { trackPageView } = useAnalytics();
  const pathname = usePathname();

  // Initialize analytics scripts
  useEffect(() => {
    // Google Analytics 4
    if (brandConfig.analytics.ga4_id) {
      initializeGA4(brandConfig.analytics.ga4_id);
    }

    // Google Tag Manager
    if (brandConfig.analytics.gtm_id) {
      initializeGTM(brandConfig.analytics.gtm_id);
    }

    // Facebook Pixel
    if (brandConfig.analytics.facebook_pixel_id) {
      initializeFacebookPixel(brandConfig.analytics.facebook_pixel_id);
    }
  }, [brandConfig]);

  // Track page views on route changes
  useEffect(() => {
    trackPageView(pathname);
  }, [pathname, trackPageView]);

  return <>{children}</>;
}

function initializeGA4(measurementId: string) {
  if (typeof window === 'undefined') return;

  // Load GA4 script
  const script = document.createElement('script');
  script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  script.async = true;
  document.head.appendChild(script);

  // Initialize gtag
  script.onload = () => {
    window.gtag = function() {
      (window as any).dataLayer = (window as any).dataLayer || [];
      (window as any).dataLayer.push(arguments);
    };

    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      page_title: document.title,
      page_location: window.location.href,
      send_page_view: true,
    });
  };
}

function initializeGTM(gtmId: string) {
  if (typeof window === 'undefined') return;

  // GTM script
  const script = document.createElement('script');
  script.innerHTML = `
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','${gtmId}');
  `;
  document.head.appendChild(script);

  // GTM noscript fallback
  const noscript = document.createElement('noscript');
  noscript.innerHTML = `
    <iframe src="https://www.googletagmanager.com/ns.html?id=${gtmId}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe>
  `;
  document.body.appendChild(noscript);
}

function initializeFacebookPixel(pixelId: string) {
  if (typeof window === 'undefined') return;

  // Facebook Pixel script
  const script = document.createElement('script');
  script.innerHTML = `
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '${pixelId}');
    fbq('track', 'PageView');
  `;
  document.head.appendChild(script);

  // Facebook Pixel noscript fallback
  const noscript = document.createElement('noscript');
  noscript.innerHTML = `
    <img height="1" width="1" style="display:none"
    src="https://www.facebook.com/tr?id=${pixelId}&ev=PageView&noscript=1" />
  `;
  document.body.appendChild(noscript);
}