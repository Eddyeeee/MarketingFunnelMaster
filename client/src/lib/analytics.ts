// Define the gtag function globally
declare global {
  interface Window {
    dataLayer: any[];
    gtag: (...args: any[]) => void;
  }
}

// UTM Parameter Interface
interface UTMParams {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_term?: string;
  utm_content?: string;
  gclid?: string;
  fbclid?: string;
}

// Session Tracking Interface
interface SessionData {
  sessionId: string;
  startTime: number;
  pageViews: number;
  utmParams: UTMParams;
  referrer: string;
  userAgent: string;
}

// Initialize Google Analytics
export const initGA = () => {
  const measurementId = import.meta.env.VITE_GA_MEASUREMENT_ID;

  if (!measurementId) {
    console.warn('Missing required Google Analytics key: VITE_GA_MEASUREMENT_ID');
    return;
  }

  // Add Google Analytics script to the head
  const script1 = document.createElement('script');
  script1.async = true;
  script1.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(script1);

  // Initialize gtag
  const script2 = document.createElement('script');
  script2.innerHTML = `
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '${measurementId}');
  `;
  document.head.appendChild(script2);
};

// Extract UTM parameters from URL
export const extractUTMParams = (): UTMParams => {
  if (typeof window === 'undefined') return {};
  
  const urlParams = new URLSearchParams(window.location.search);
  return {
    utm_source: urlParams.get('utm_source') || undefined,
    utm_medium: urlParams.get('utm_medium') || undefined,
    utm_campaign: urlParams.get('utm_campaign') || undefined,
    utm_term: urlParams.get('utm_term') || undefined,
    utm_content: urlParams.get('utm_content') || undefined,
    gclid: urlParams.get('gclid') || undefined,
    fbclid: urlParams.get('fbclid') || undefined,
  };
};

// Generate or retrieve session ID
export const getSessionId = (): string => {
  if (typeof window === 'undefined') return 'server-session';
  
  let sessionId = sessionStorage.getItem('qmoney_session_id');
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    sessionStorage.setItem('qmoney_session_id', sessionId);
  }
  return sessionId;
};

// Initialize session tracking
export const initSessionTracking = (): SessionData => {
  const sessionId = getSessionId();
  const utmParams = extractUTMParams();
  
  const sessionData: SessionData = {
    sessionId,
    startTime: Date.now(),
    pageViews: 1,
    utmParams,
    referrer: document.referrer,
    userAgent: navigator.userAgent
  };
  
  // Store session data
  sessionStorage.setItem('qmoney_session_data', JSON.stringify(sessionData));
  
  return sessionData;
};

// Get current session data
export const getSessionData = (): SessionData | null => {
  if (typeof window === 'undefined') return null;
  
  const stored = sessionStorage.getItem('qmoney_session_data');
  if (!stored) return null;
  
  try {
    return JSON.parse(stored);
  } catch {
    return null;
  }
};

// Update session data
export const updateSessionData = (updates: Partial<SessionData>) => {
  if (typeof window === 'undefined') return;
  
  const current = getSessionData();
  if (!current) return;
  
  const updated = { ...current, ...updates };
  sessionStorage.setItem('qmoney_session_data', JSON.stringify(updated));
};

// Track page views - useful for single-page applications
export const trackPageView = (url: string) => {
  if (typeof window === 'undefined' || !window.gtag) return;
  
  const measurementId = import.meta.env.VITE_GA_MEASUREMENT_ID;
  if (!measurementId) return;
  
  // Update session data
  const sessionData = getSessionData();
  if (sessionData) {
    updateSessionData({ pageViews: sessionData.pageViews + 1 });
  }
  
  window.gtag('config', measurementId, {
    page_path: url
  });
};

// Track events with enhanced data
export const trackEvent = (
  action: string, 
  category?: string, 
  label?: string, 
  value?: number,
  customData?: Record<string, any>
) => {
  if (typeof window === 'undefined' || !window.gtag) return;
  
  const sessionData = getSessionData();
  const utmParams = extractUTMParams();
  
  const eventData: any = {
    event_category: category,
    event_label: label,
    value: value,
    session_id: sessionData?.sessionId,
    page_views: sessionData?.pageViews,
    time_on_page: sessionData ? Date.now() - sessionData.startTime : 0,
    ...utmParams,
    ...customData
  };
  
  window.gtag('event', action, eventData);
};

// Track conversion events with full context
export const trackConversion = (
  eventName: string,
  value?: number,
  currency: string = 'EUR',
  additionalData?: Record<string, any>
) => {
  if (typeof window === 'undefined' || !window.gtag) return;
  
  const sessionData = getSessionData();
  const utmParams = extractUTMParams();
  
  const conversionData = {
    value: value,
    currency: currency,
    session_id: sessionData?.sessionId,
    page_views: sessionData?.pageViews,
    time_on_page: sessionData ? Date.now() - sessionData.startTime : 0,
    referrer: sessionData?.referrer,
    ...utmParams,
    ...additionalData
  };
  
  window.gtag('event', eventName, conversionData);
  
  // Also send to our analytics endpoint
  sendAnalyticsEvent(eventName, conversionData);
};

// Send analytics event to our backend
export const sendAnalyticsEvent = async (
  event: string,
  data: Record<string, any>
) => {
  try {
    const sessionData = getSessionData();
    const utmParams = extractUTMParams();
    
    const analyticsData = {
      page: window.location.pathname,
      event,
      data: {
        ...data,
        sessionId: sessionData?.sessionId,
        utmParams,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString()
      }
    };
    
    await fetch('/api/analytics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(analyticsData)
    });
  } catch (error) {
    console.warn('Failed to send analytics event:', error);
  }
};

// Enhanced lead tracking with full context
export const trackLeadCapture = async (
  leadData: {
    email: string;
    name?: string;
    phone?: string;
    source: string;
    funnel?: string;
    quizAnswers?: Record<string, string>;
    persona?: Record<string, any>;
  }
) => {
  const sessionData = getSessionData();
  const utmParams = extractUTMParams();
  
  // Track in Google Analytics
  trackConversion('lead_capture', 1, 'EUR', {
    lead_source: leadData.source,
    lead_funnel: leadData.funnel,
    has_quiz_answers: !!leadData.quizAnswers,
    has_persona: !!leadData.persona
  });
  
  // Prepare data for capture-lead endpoint
  const captureData = {
    ...leadData,
    utmSource: utmParams.utm_source,
    utmMedium: utmParams.utm_medium,
    utmCampaign: utmParams.utm_campaign,
    utmTerm: utmParams.utm_term,
    utmContent: utmParams.utm_content,
    gclid: utmParams.gclid,
    fbclid: utmParams.fbclid,
    sessionId: sessionData?.sessionId,
    pageUrl: window.location.href,
    referrer: sessionData?.referrer,
    customFields: {
      pageViews: sessionData?.pageViews,
      timeOnPage: sessionData ? Date.now() - sessionData.startTime : 0,
      userAgent: navigator.userAgent
    }
  };
  
  return captureData;
};