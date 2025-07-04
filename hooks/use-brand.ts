'use client';

import { useState, useEffect, useContext, createContext } from 'react';
import { BrandType, BrandConfig, UseBrandReturn } from '@/types';
import { getFromStorage, setToStorage } from '@/lib/utils';

// Default brand configurations
const defaultBrandConfigs: Record<BrandType, BrandConfig> = {
  tech: {
    id: 'tech',
    name: 'TechFlow',
    domain: 'techflow.com',
    industry: 'Technology',
    target_personas: ['TechEarlyAdopter', 'BusinessOwner'],
    design: {
      colors: {
        primary: 'hsl(220, 100%, 60%)',
        secondary: 'hsl(170, 100%, 40%)',
        accent: 'hsl(280, 100%, 70%)',
        background: 'hsl(0, 0%, 100%)',
        foreground: 'hsl(224, 71.4%, 4.1%)',
        muted: 'hsl(220, 14.3%, 95.9%)',
        border: 'hsl(220, 13%, 91%)',
      },
      typography: {
        headings: 'Inter',
        body: 'Inter',
        mono: 'JetBrains Mono',
      },
      spacing: {
        unit: 4,
        scale: [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
      },
      borderRadius: {
        sm: '0.25rem',
        md: '0.5rem',
        lg: '0.75rem',
      },
    },
    content: {
      messaging: {
        headline: 'Accelerate Your Technical Journey',
        subheadline: 'Cutting-edge tools for modern developers',
        value_proposition: 'Build faster, scale smarter, innovate continuously',
        cta_primary: 'Start Building',
        cta_secondary: 'View Demo',
      },
      tone: 'technical',
      voice: 'Expert, innovative, precise',
    },
    seo: {
      title: 'TechFlow - Advanced Development Tools',
      description: 'Accelerate your technical journey with cutting-edge development tools and frameworks.',
      keywords: ['development', 'tools', 'technology', 'programming', 'software'],
      ogImage: '/images/tech-og.png',
      ogImageAlt: 'TechFlow - Advanced Development Tools',
      twitterImage: '/images/tech-twitter.png',
    },
    analytics: {
      ga4_id: 'G-TECH123456',
      custom_events: ['tech_demo_view', 'api_docs_access', 'tool_download'],
    },
    social: {
      twitter: '@techflow',
      github: 'techflow',
      linkedin: 'techflow',
    },
  },
  wealth: {
    id: 'wealth',
    name: 'WealthMax',
    domain: 'wealthmax.com',
    industry: 'Finance',
    target_personas: ['BusinessOwner', 'RemoteDad'],
    design: {
      colors: {
        primary: 'hsl(45, 100%, 50%)',
        secondary: 'hsl(120, 100%, 30%)',
        accent: 'hsl(15, 100%, 60%)',
        background: 'hsl(0, 0%, 100%)',
        foreground: 'hsl(224, 71.4%, 4.1%)',
        muted: 'hsl(220, 14.3%, 95.9%)',
        border: 'hsl(220, 13%, 91%)',
      },
      typography: {
        headings: 'Playfair Display',
        body: 'Inter',
        mono: 'Source Code Pro',
      },
      spacing: {
        unit: 4,
        scale: [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
      },
      borderRadius: {
        sm: '0.375rem',
        md: '0.5rem',
        lg: '0.75rem',
      },
    },
    content: {
      messaging: {
        headline: 'Maximize Your Financial Potential',
        subheadline: 'Smart strategies for lasting wealth',
        value_proposition: 'Build wealth, secure your future, achieve financial freedom',
        cta_primary: 'Start Growing',
        cta_secondary: 'Learn More',
      },
      tone: 'professional',
      voice: 'Authoritative, trustworthy, results-focused',
    },
    seo: {
      title: 'WealthMax - Financial Growth Strategies',
      description: 'Maximize your financial potential with proven wealth-building strategies and expert guidance.',
      keywords: ['wealth', 'finance', 'investment', 'money', 'financial freedom'],
      ogImage: '/images/wealth-og.png',
      ogImageAlt: 'WealthMax - Financial Growth Strategies',
      twitterImage: '/images/wealth-twitter.png',
    },
    analytics: {
      ga4_id: 'G-WEALTH123456',
      custom_events: ['wealth_calculator_use', 'strategy_download', 'consultation_book'],
    },
    social: {
      twitter: '@wealthmax',
      linkedin: 'wealthmax',
      youtube: 'wealthmax',
    },
  },
  crypto: {
    id: 'crypto',
    name: 'CryptoFlow',
    domain: 'cryptoflow.com',
    industry: 'Cryptocurrency',
    target_personas: ['TechEarlyAdopter', 'StudentHustler'],
    design: {
      colors: {
        primary: 'hsl(280, 100%, 60%)',
        secondary: 'hsl(45, 100%, 50%)',
        accent: 'hsl(180, 100%, 40%)',
        background: 'hsl(0, 0%, 100%)',
        foreground: 'hsl(224, 71.4%, 4.1%)',
        muted: 'hsl(220, 14.3%, 95.9%)',
        border: 'hsl(220, 13%, 91%)',
      },
      typography: {
        headings: 'Space Grotesk',
        body: 'Inter',
        mono: 'Fira Code',
      },
      spacing: {
        unit: 4,
        scale: [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
      },
      borderRadius: {
        sm: '0.5rem',
        md: '0.75rem',
        lg: '1rem',
      },
    },
    content: {
      messaging: {
        headline: 'Navigate the Crypto Revolution',
        subheadline: 'Advanced tools for digital asset mastery',
        value_proposition: 'Trade smarter, invest wisely, dominate DeFi',
        cta_primary: 'Start Trading',
        cta_secondary: 'Explore Tools',
      },
      tone: 'technical',
      voice: 'Cutting-edge, dynamic, innovative',
    },
    seo: {
      title: 'CryptoFlow - Advanced Crypto Trading Tools',
      description: 'Navigate the crypto revolution with advanced trading tools and DeFi strategies.',
      keywords: ['crypto', 'cryptocurrency', 'trading', 'DeFi', 'blockchain'],
      ogImage: '/images/crypto-og.png',
      ogImageAlt: 'CryptoFlow - Advanced Crypto Trading Tools',
      twitterImage: '/images/crypto-twitter.png',
    },
    analytics: {
      ga4_id: 'G-CRYPTO123456',
      custom_events: ['trading_tool_use', 'defi_guide_view', 'portfolio_tracker_access'],
    },
    social: {
      twitter: '@cryptoflow',
      discord: 'cryptoflow',
      telegram: 'cryptoflow',
    },
  },
  affiliate: {
    id: 'affiliate',
    name: 'AffiliPro',
    domain: 'affilipro.com',
    industry: 'Affiliate Marketing',
    target_personas: ['BusinessOwner', 'StudentHustler'],
    design: {
      colors: {
        primary: 'hsl(200, 100%, 60%)',
        secondary: 'hsl(320, 100%, 50%)',
        accent: 'hsl(80, 100%, 50%)',
        background: 'hsl(0, 0%, 100%)',
        foreground: 'hsl(224, 71.4%, 4.1%)',
        muted: 'hsl(220, 14.3%, 95.9%)',
        border: 'hsl(220, 13%, 91%)',
      },
      typography: {
        headings: 'Montserrat',
        body: 'Inter',
        mono: 'Source Code Pro',
      },
      spacing: {
        unit: 4,
        scale: [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
      },
      borderRadius: {
        sm: '0.25rem',
        md: '0.5rem',
        lg: '0.75rem',
      },
    },
    content: {
      messaging: {
        headline: 'Professional Affiliate Marketing',
        subheadline: 'Scale your affiliate business to new heights',
        value_proposition: 'Optimize campaigns, maximize conversions, grow revenue',
        cta_primary: 'Start Scaling',
        cta_secondary: 'View Results',
      },
      tone: 'professional',
      voice: 'Results-driven, strategic, growth-focused',
    },
    seo: {
      title: 'AffiliPro - Professional Affiliate Marketing Tools',
      description: 'Scale your affiliate business with professional marketing tools and proven strategies.',
      keywords: ['affiliate marketing', 'conversion optimization', 'marketing tools', 'revenue growth'],
      ogImage: '/images/affiliate-og.png',
      ogImageAlt: 'AffiliPro - Professional Affiliate Marketing Tools',
      twitterImage: '/images/affiliate-twitter.png',
    },
    analytics: {
      ga4_id: 'G-AFFILIATE123456',
      custom_events: ['campaign_created', 'conversion_tracked', 'revenue_report_view'],
    },
    social: {
      twitter: '@affilipro',
      linkedin: 'affilipro',
      facebook: 'affilipro',
    },
  },
};

// Brand Context
const BrandContext = createContext<UseBrandReturn | undefined>(undefined);

export function useBrand(): UseBrandReturn {
  const context = useContext(BrandContext);
  if (!context) {
    throw new Error('useBrand must be used within a BrandProvider');
  }
  return context;
}

// Brand Hook Implementation
export function useBrandInternal(): UseBrandReturn {
  const [brand, setBrandState] = useState<BrandType>('tech');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>();

  // Load brand from storage or URL on mount
  useEffect(() => {
    try {
      // Check URL params first (for brand-specific domains)
      if (typeof window !== 'undefined') {
        const urlParams = new URLSearchParams(window.location.search);
        const urlBrand = urlParams.get('brand') as BrandType;
        
        if (urlBrand && Object.keys(defaultBrandConfigs).includes(urlBrand)) {
          setBrandState(urlBrand);
          setToStorage('selectedBrand', urlBrand);
        } else {
          // Check hostname for brand detection
          const hostname = window.location.hostname;
          const detectedBrand = detectBrandFromHostname(hostname);
          if (detectedBrand) {
            setBrandState(detectedBrand);
            setToStorage('selectedBrand', detectedBrand);
          } else {
            // Fall back to stored brand
            const storedBrand = getFromStorage<BrandType>('selectedBrand', 'tech');
            setBrandState(storedBrand);
          }
        }
      }
    } catch (err) {
      setError('Failed to load brand configuration');
      console.error('Brand loading error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const setBrand = (newBrand: BrandType) => {
    try {
      setBrandState(newBrand);
      setToStorage('selectedBrand', newBrand);
      setError(undefined);
    } catch (err) {
      setError('Failed to save brand configuration');
      console.error('Brand saving error:', err);
    }
  };

  const brandConfig = defaultBrandConfigs[brand];

  return {
    brand,
    brandConfig,
    setBrand,
    loading,
    error,
  };
}

// Helper function to detect brand from hostname
function detectBrandFromHostname(hostname: string): BrandType | null {
  const brandDomains: Record<string, BrandType> = {
    'techflow.com': 'tech',
    'wealthmax.com': 'wealth',
    'cryptoflow.com': 'crypto',
    'affilipro.com': 'affiliate',
    // Add development domains
    'localhost:3000': 'tech', // default for development
  };

  // Check exact match first
  if (brandDomains[hostname]) {
    return brandDomains[hostname];
  }

  // Check partial matches for subdomains
  for (const [domain, brand] of Object.entries(brandDomains)) {
    if (hostname.includes(domain.split('.')[0])) {
      return brand;
    }
  }

  return null;
}

// Brand configuration utilities
export function getBrandConfig(brandType: BrandType): BrandConfig {
  return defaultBrandConfigs[brandType];
}

export function getAllBrands(): BrandType[] {
  return Object.keys(defaultBrandConfigs) as BrandType[];
}

export function isBrandValid(brand: string): brand is BrandType {
  return Object.keys(defaultBrandConfigs).includes(brand);
}

// Brand-specific utilities
export function getBrandColors(brand: BrandType) {
  return defaultBrandConfigs[brand].design.colors;
}

export function getBrandTypography(brand: BrandType) {
  return defaultBrandConfigs[brand].design.typography;
}

export function getBrandMessaging(brand: BrandType) {
  return defaultBrandConfigs[brand].content.messaging;
}

export { BrandContext, defaultBrandConfigs };