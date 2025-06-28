import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

// Accessibility Context Types
interface AccessibilitySettings {
  highContrast: boolean;
  largeText: boolean;
  reducedMotion: boolean;
  screenReader: boolean;
  keyboardNavigation: boolean;
  focusVisible: boolean;
  colorBlindness: 'none' | 'protanopia' | 'deuteranopia' | 'tritanopia';
  fontSize: 'small' | 'medium' | 'large' | 'xl';
  announcements: string[];
}

interface AccessibilityContextType {
  settings: AccessibilitySettings;
  updateSetting: (key: keyof AccessibilitySettings, value: any) => void;
  announce: (message: string, priority?: 'polite' | 'assertive') => void;
  skipToContent: () => void;
  focusManager: {
    trapFocus: (element: HTMLElement) => () => void;
    restoreFocus: () => void;
    setFocusableElements: (selector: string) => NodeListOf<Element>;
  };
}

const AccessibilityContext = createContext<AccessibilityContextType | undefined>(undefined);

// Default settings
const defaultSettings: AccessibilitySettings = {
  highContrast: false,
  largeText: false,
  reducedMotion: false,
  screenReader: false,
  keyboardNavigation: true,
  focusVisible: true,
  colorBlindness: 'none',
  fontSize: 'medium',
  announcements: []
};

// Accessibility Provider Component
export function AccessibilityProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<AccessibilitySettings>(defaultSettings);
  const [previousFocus, setPreviousFocus] = useState<HTMLElement | null>(null);

  // Load settings from localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('accessibility-settings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings(prev => ({ ...prev, ...parsed }));
      } catch (error) {
        console.warn('Failed to parse accessibility settings:', error);
      }
    }

    // Detect user preferences
    detectUserPreferences();
  }, []);

  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem('accessibility-settings', JSON.stringify(settings));
    applyAccessibilitySettings(settings);
  }, [settings]);

  // Detect system preferences
  const detectUserPreferences = () => {
    // Reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      setSettings(prev => ({ ...prev, reducedMotion: true }));
    }

    // High contrast preference
    const prefersHighContrast = window.matchMedia('(prefers-contrast: high)').matches;
    if (prefersHighContrast) {
      setSettings(prev => ({ ...prev, highContrast: true }));
    }

    // Screen reader detection
    const hasScreenReader = 'speechSynthesis' in window || navigator.userAgent.includes('NVDA') || navigator.userAgent.includes('JAWS');
    if (hasScreenReader) {
      setSettings(prev => ({ ...prev, screenReader: true }));
    }
  };

  // Apply accessibility settings to DOM
  const applyAccessibilitySettings = (settings: AccessibilitySettings) => {
    const root = document.documentElement;
    
    // High contrast
    root.classList.toggle('high-contrast', settings.highContrast);
    
    // Large text
    root.classList.toggle('large-text', settings.largeText);
    
    // Reduced motion
    root.classList.toggle('reduced-motion', settings.reducedMotion);
    
    // Font size
    root.setAttribute('data-font-size', settings.fontSize);
    
    // Color blindness filters
    root.setAttribute('data-color-filter', settings.colorBlindness);
    
    // Focus visible
    root.classList.toggle('focus-visible-enabled', settings.focusVisible);
  };

  // Update setting function
  const updateSetting = (key: keyof AccessibilitySettings, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    
    // Analytics tracking
    if (window.gtag) {
      window.gtag('event', 'accessibility_setting_changed', {
        setting: key,
        value: value,
        event_category: 'accessibility'
      });
    }
  };

  // Screen reader announcements
  const announce = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', priority);
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);

    // Add to announcements history
    setSettings(prev => ({
      ...prev,
      announcements: [...prev.announcements.slice(-4), message]
    }));
  };

  // Skip to main content
  const skipToContent = () => {
    const mainContent = document.getElementById('main-content') || document.querySelector('main');
    if (mainContent) {
      mainContent.focus();
      mainContent.scrollIntoView({ behavior: 'smooth' });
      announce('Zum Hauptinhalt gesprungen', 'polite');
    }
  };

  // Focus management
  const focusManager = {
    trapFocus: (element: HTMLElement) => {
      const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const firstElement = focusableElements[0] as HTMLElement;
      const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

      const handleTabKey = (e: KeyboardEvent) => {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstElement) {
              e.preventDefault();
              lastElement.focus();
            }
          } else {
            if (document.activeElement === lastElement) {
              e.preventDefault();
              firstElement.focus();
            }
          }
        }
        
        if (e.key === 'Escape') {
          focusManager.restoreFocus();
        }
      };

      // Store current focus
      setPreviousFocus(document.activeElement as HTMLElement);
      
      // Focus first element
      firstElement?.focus();
      
      // Add event listener
      element.addEventListener('keydown', handleTabKey);
      
      // Return cleanup function
      return () => {
        element.removeEventListener('keydown', handleTabKey);
      };
    },

    restoreFocus: () => {
      if (previousFocus) {
        previousFocus.focus();
        setPreviousFocus(null);
      }
    },

    setFocusableElements: (selector: string) => {
      return document.querySelectorAll(selector);
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Alt + S: Skip to content
      if (e.altKey && e.key === 's') {
        e.preventDefault();
        skipToContent();
      }
      
      // Alt + M: Open accessibility menu
      if (e.altKey && e.key === 'm') {
        e.preventDefault();
        const accessibilityMenu = document.getElementById('accessibility-menu');
        if (accessibilityMenu) {
          accessibilityMenu.focus();
          announce('Barrierefreiheits-Menü geöffnet', 'assertive');
        }
      }
      
      // Alt + H: Toggle high contrast
      if (e.altKey && e.key === 'h') {
        e.preventDefault();
        updateSetting('highContrast', !settings.highContrast);
        announce(`Hoher Kontrast ${!settings.highContrast ? 'aktiviert' : 'deaktiviert'}`, 'assertive');
      }
      
      // Alt + T: Toggle large text
      if (e.altKey && e.key === 't') {
        e.preventDefault();
        updateSetting('largeText', !settings.largeText);
        announce(`Große Schrift ${!settings.largeText ? 'aktiviert' : 'deaktiviert'}`, 'assertive');
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [settings]);

  const contextValue: AccessibilityContextType = {
    settings,
    updateSetting,
    announce,
    skipToContent,
    focusManager
  };

  return (
    <AccessibilityContext.Provider value={contextValue}>
      {children}
      
      {/* Skip Link */}
      <a
        href="#main-content"
        className="skip-link sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-white focus:rounded-md"
        onClick={(e) => {
          e.preventDefault();
          skipToContent();
        }}
      >
        Zum Hauptinhalt springen (Alt + S)
      </a>

      {/* Live Region for Announcements */}
      <div
        id="announcements"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      />
      
      {/* Emergency Live Region */}
      <div
        id="emergency-announcements"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      />
    </AccessibilityContext.Provider>
  );
}

// Hook to use accessibility context
export function useAccessibility() {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within AccessibilityProvider');
  }
  return context;
}

// Accessibility Menu Component
export function AccessibilityMenu() {
  const { settings, updateSetting } = useAccessibility();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed top-4 right-4 z-50">
      <button
        id="accessibility-menu"
        onClick={() => setIsOpen(!isOpen)}
        className="p-3 bg-primary text-white rounded-full shadow-lg hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        aria-label="Barrierefreiheits-Einstellungen öffnen"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-16 right-0 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
            Barrierefreiheit
          </h3>
          
          <div className="space-y-4">
            {/* High Contrast */}
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.highContrast}
                onChange={(e) => updateSetting('highContrast', e.target.checked)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">
                Hoher Kontrast (Alt + H)
              </span>
            </label>

            {/* Large Text */}
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.largeText}
                onChange={(e) => updateSetting('largeText', e.target.checked)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">
                Große Schrift (Alt + T)
              </span>
            </label>

            {/* Reduced Motion */}
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.reducedMotion}
                onChange={(e) => updateSetting('reducedMotion', e.target.checked)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">
                Reduzierte Bewegungen
              </span>
            </label>

            {/* Font Size */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Schriftgröße
              </label>
              <select
                value={settings.fontSize}
                onChange={(e) => updateSetting('fontSize', e.target.value)}
                className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 text-sm"
              >
                <option value="small">Klein</option>
                <option value="medium">Normal</option>
                <option value="large">Groß</option>
                <option value="xl">Sehr groß</option>
              </select>
            </div>

            {/* Color Blindness Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Farbenblindheit-Filter
              </label>
              <select
                value={settings.colorBlindness}
                onChange={(e) => updateSetting('colorBlindness', e.target.value)}
                className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 text-sm"
              >
                <option value="none">Kein Filter</option>
                <option value="protanopia">Protanopie (Rot-Grün)</option>
                <option value="deuteranopia">Deuteranopie (Grün-Rot)</option>
                <option value="tritanopia">Tritanopie (Blau-Gelb)</option>
              </select>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-600">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Tastenkürzel: Alt + S (Zum Inhalt), Alt + M (Dieses Menü)
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AccessibilityProvider; 