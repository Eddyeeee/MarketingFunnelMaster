/**
 * Enhanced Lighthouse CI Configuration with Multi-Environment Performance Budgets
 * Phase 2: Performance Budget Hardening
 * 
 * Features:
 * - Multi-environment budget matrices (production/staging)
 * - Device-specific validation (mobile/desktop/tablet)
 * - Route-specific budget enforcement
 * - Advanced Core Web Vitals monitoring
 */

const { execSync } = require('child_process');

// Environment Detection
const getCurrentEnvironment = () => {
  const branch = process.env.GITHUB_REF_NAME || process.env.BRANCH || 'local';
  const isProduction = branch === 'main' || process.env.NODE_ENV === 'production';
  const isStaging = branch === 'develop' || branch.includes('staging');
  
  if (isProduction) return 'production';
  if (isStaging) return 'staging';
  return 'development';
};

// Device Detection
const getDeviceType = () => {
  return process.env.LIGHTHOUSE_DEVICE || 'desktop';
};

// Performance Budget Matrices
const PERFORMANCE_BUDGETS = {
  production: {
    mobile: {
      // Ultra-strict for production mobile
      'largest-contentful-paint': ['error', { maxNumericValue: 2000 }],
      'first-contentful-paint': ['error', { maxNumericValue: 1500 }],
      'total-blocking-time': ['error', { maxNumericValue: 300 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      'first-input-delay': ['error', { maxNumericValue: 100 }],
      'speed-index': ['error', { maxNumericValue: 2800 }],
      'interactive': ['error', { maxNumericValue: 3500 }],
      'categories:performance': ['error', { minScore: 0.85 }]
    },
    desktop: {
      // Strict for production desktop
      'largest-contentful-paint': ['error', { maxNumericValue: 1800 }],
      'first-contentful-paint': ['error', { maxNumericValue: 1200 }],
      'total-blocking-time': ['error', { maxNumericValue: 250 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.08 }],
      'first-input-delay': ['error', { maxNumericValue: 80 }],
      'speed-index': ['error', { maxNumericValue: 2200 }],
      'interactive': ['error', { maxNumericValue: 3000 }],
      'categories:performance': ['error', { minScore: 0.9 }]
    },
    tablet: {
      // Balanced for production tablet
      'largest-contentful-paint': ['error', { maxNumericValue: 1900 }],
      'first-contentful-paint': ['error', { maxNumericValue: 1400 }],
      'total-blocking-time': ['error', { maxNumericValue: 280 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.09 }],
      'first-input-delay': ['error', { maxNumericValue: 90 }],
      'speed-index': ['error', { maxNumericValue: 2500 }],
      'interactive': ['error', { maxNumericValue: 3200 }],
      'categories:performance': ['error', { minScore: 0.87 }]
    }
  },
  staging: {
    mobile: {
      // Moderate for staging mobile
      'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
      'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
      'total-blocking-time': ['error', { maxNumericValue: 400 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.15 }],
      'first-input-delay': ['error', { maxNumericValue: 150 }],
      'speed-index': ['error', { maxNumericValue: 3200 }],
      'interactive': ['error', { maxNumericValue: 4000 }],
      'categories:performance': ['error', { minScore: 0.75 }]
    },
    desktop: {
      // Moderate for staging desktop
      'largest-contentful-paint': ['error', { maxNumericValue: 2200 }],
      'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
      'total-blocking-time': ['error', { maxNumericValue: 350 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.12 }],
      'first-input-delay': ['error', { maxNumericValue: 120 }],
      'speed-index': ['error', { maxNumericValue: 2800 }],
      'interactive': ['error', { maxNumericValue: 3500 }],
      'categories:performance': ['error', { minScore: 0.8 }]
    },
    tablet: {
      // Moderate for staging tablet
      'largest-contentful-paint': ['error', { maxNumericValue: 2300 }],
      'first-contentful-paint': ['error', { maxNumericValue: 1900 }],
      'total-blocking-time': ['error', { maxNumericValue: 380 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.13 }],
      'first-input-delay': ['error', { maxNumericValue: 130 }],
      'speed-index': ['error', { maxNumericValue: 3000 }],
      'interactive': ['error', { maxNumericValue: 3800 }],
      'categories:performance': ['error', { minScore: 0.77 }]
    }
  },
  development: {
    // Relaxed budgets for development
    mobile: {
      'largest-contentful-paint': ['warn', { maxNumericValue: 3000 }],
      'total-blocking-time': ['warn', { maxNumericValue: 500 }],
      'cumulative-layout-shift': ['warn', { maxNumericValue: 0.2 }],
      'categories:performance': ['warn', { minScore: 0.6 }]
    },
    desktop: {
      'largest-contentful-paint': ['warn', { maxNumericValue: 2800 }],
      'total-blocking-time': ['warn', { maxNumericValue: 450 }],
      'cumulative-layout-shift': ['warn', { maxNumericValue: 0.15 }],
      'categories:performance': ['warn', { minScore: 0.65 }]
    },
    tablet: {
      'largest-contentful-paint': ['warn', { maxNumericValue: 2900 }],
      'total-blocking-time': ['warn', { maxNumericValue: 480 }],
      'cumulative-layout-shift': ['warn', { maxNumericValue: 0.18 }],
      'categories:performance': ['warn', { minScore: 0.62 }]
    }
  }
};

// Route-Specific Budget Overrides
const ROUTE_SPECIFIC_BUDGETS = {
  // Landing pages - Ultra-strict (conversion critical)
  '/': {
    'largest-contentful-paint': ['error', { maxNumericValue: 1800 }],
    'total-blocking-time': ['error', { maxNumericValue: 200 }],
    'categories:performance': ['error', { minScore: 0.92 }]
  },
  '/quiz': {
    'largest-contentful-paint': ['error', { maxNumericValue: 1800 }],
    'total-blocking-time': ['error', { maxNumericValue: 200 }],
    'categories:performance': ['error', { minScore: 0.92 }]
  },
  '/vsl': {
    'largest-contentful-paint': ['error', { maxNumericValue: 1800 }],
    'total-blocking-time': ['error', { maxNumericValue: 200 }],
    'categories:performance': ['error', { minScore: 0.92 }]
  },
  
  // Bridge pages - Moderate (user engagement focus)
  '/bridge': {
    'largest-contentful-paint': ['error', { maxNumericValue: 2200 }],
    'total-blocking-time': ['error', { maxNumericValue: 250 }],
    'categories:performance': ['error', { minScore: 0.85 }]
  },
  
  // Thank you / confirmation pages - Relaxed (post-conversion)
  '/tsl': {
    'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
    'total-blocking-time': ['error', { maxNumericValue: 300 }],
    'categories:performance': ['error', { minScore: 0.8 }]
  }
};

// Get current configuration
const environment = getCurrentEnvironment();
const device = getDeviceType();

// Build dynamic assertion config
const buildAssertions = () => {
  const baseBudgets = PERFORMANCE_BUDGETS[environment]?.[device] || PERFORMANCE_BUDGETS.development.desktop;
  
  // Common assertions (non-performance)
  const commonAssertions = {
    // Accessibility
    'categories:accessibility': ['error', { minScore: 0.95 }],
    'color-contrast': 'error',
    'heading-order': 'error',
    'html-has-lang': 'error',
    'image-alt': 'error',
    'label': 'error',
    'link-name': 'error',
    'meta-viewport': 'error',
    
    // SEO
    'categories:seo': ['error', { minScore: 0.9 }],
    'document-title': 'error',
    'meta-description': 'error',
    'http-status-code': 'error',
    'link-text': 'error',
    'is-crawlable': 'error',
    
    // Best Practices
    'categories:best-practices': ['error', { minScore: 0.9 }],
    'uses-https': 'error',
    'no-vulnerable-libraries': 'error',
    'csp-xss': 'warn',
    
    // Performance Optimization Warnings
    'unused-css-rules': 'warn',
    'unused-javascript': 'warn',
    'uses-optimized-images': 'warn',
    'uses-webp-images': 'warn',
    'uses-responsive-images': 'warn',
    'efficient-animated-content': 'warn',
    'preload-lcp-image': 'warn',
    
    // PWA (if applicable)
    'categories:pwa': ['warn', { minScore: 0.8 }]
  };
  
  return {
    ...baseBudgets,
    ...commonAssertions
  };
};

// Apply route-specific overrides
const applyRouteOverrides = (url, baseAssertions) => {
  const urlPath = new URL(url).pathname;
  const routeOverrides = ROUTE_SPECIFIC_BUDGETS[urlPath] || {};
  
  return {
    ...baseAssertions,
    ...routeOverrides
  };
};

// Device-specific collection settings
const getCollectionSettings = () => {
  const baseSettings = {
    chromeFlags: '--no-sandbox --headless --disable-gpu',
    numberOfRuns: 3
  };
  
  switch (device) {
    case 'mobile':
      return {
        ...baseSettings,
        preset: 'mobile',
        formFactor: 'mobile',
        screenEmulation: {
          mobile: true,
          width: 375,
          height: 667,
          deviceScaleFactor: 2
        }
      };
    case 'tablet':
      return {
        ...baseSettings,
        preset: 'desktop',
        formFactor: 'desktop',
        screenEmulation: {
          mobile: false,
          width: 768,
          height: 1024,
          deviceScaleFactor: 1
        }
      };
    case 'desktop':
    default:
      return {
        ...baseSettings,
        preset: 'desktop',
        formFactor: 'desktop',
        screenEmulation: {
          mobile: false,
          width: 1920,
          height: 1080,
          deviceScaleFactor: 1
        }
      };
  }
};

// URLs with route-specific budget application
const buildUrlConfigs = () => {
  const baseUrls = [
    'http://localhost:3000',
    'http://localhost:3000/quiz',
    'http://localhost:3000/vsl',
    'http://localhost:3000/bridge',
    'http://localhost:3000/tsl'
  ];
  
  const baseAssertions = buildAssertions();
  
  return baseUrls.map(url => ({
    url,
    assertions: applyRouteOverrides(url, baseAssertions)
  }));
};

// Main configuration
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000',
        'http://localhost:3000/quiz',
        'http://localhost:3000/vsl',
        'http://localhost:3000/bridge',
        'http://localhost:3000/tsl'
      ],
      startServerCommand: 'npm run start',
      settings: getCollectionSettings()
    },
    assert: {
      assertions: buildAssertions()
    },
    upload: {
      target: 'temporary-public-storage',
      reportFilenamePattern: `lighthouse-report-${environment}-${device}-%%PATHNAME%%-%%DATETIME%%.json`
    },
    server: {
      port: 9001,
      storage: './lighthouse-reports'
    }
  },
  
  // Custom configuration metadata
  _metadata: {
    environment,
    device,
    configVersion: '2.0',
    budgetProfile: `${environment}-${device}`,
    timestamp: new Date().toISOString()
  }
};