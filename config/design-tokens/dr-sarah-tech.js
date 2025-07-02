/**
 * Design Tokens for Dr. Sarah Tech Persona
 * Sophisticated, data-driven design system
 * Target: Tech-savvy professionals who expect premium, detailed interfaces
 */

export const drSarahTechTokens = {
  // Color System - Tech-Forward & Professional
  colors: {
    primary: {
      50: '#f8fafc',   // Very light slate
      100: '#f1f5f9',  // Light slate tint
      200: '#e2e8f0',  // Medium light slate
      300: '#cbd5e1',  // Medium slate
      400: '#94a3b8',  // Medium dark slate
      500: '#0f172a',  // Primary deep tech blue/slate
      600: '#0c1420',  // Darker slate
      700: '#0a1018',  // Very dark slate
      800: '#070c12',  // Ultra dark slate
      900: '#04080c'   // Deepest slate
    },
    
    // Electric Cyan - Innovation & AI
    cyan: {
      50: '#ecfeff',   // Very light cyan tint
      100: '#cffafe',  // Light cyan tint
      200: '#a5f3fc',  // Medium light cyan
      300: '#67e8f9',  // Medium cyan
      400: '#22d3ee',  // Medium bright cyan
      500: '#06b6d4',  // Primary cyan - innovation
      600: '#0891b2',  // Darker cyan
      700: '#0e7490',  // Deep cyan
      800: '#155e75',  // Very dark cyan
      900: '#164e63'   // Deepest cyan
    },
    
    // Purple Gradient - AI/ML Industry Standard
    purple: {
      50: '#faf5ff',   // Very light purple tint
      100: '#f3e8ff',  // Light purple tint
      200: '#e9d5ff',  // Medium light purple
      300: '#d8b4fe',  // Medium purple
      400: '#c084fc',  // Medium bright purple
      500: '#7c3aed',  // Primary purple - AI association
      600: '#6d28d9',  // Darker purple
      700: '#5b21b6',  // Deep purple
      800: '#4c1d95',  // Very dark purple
      900: '#3c1874'   // Deepest purple
    },
    
    // Pink Accent - For gradients and highlights
    pink: {
      50: '#fdf2f8',   // Very light pink tint
      100: '#fce7f3',  // Light pink tint
      200: '#fbcfe8',  // Medium light pink
      300: '#f9a8d4',  // Medium pink
      400: '#f472b6',  // Medium bright pink
      500: '#ec4899',  // Primary pink - gradient partner
      600: '#db2777',  // Darker pink
      700: '#be185d',  // Deep pink
      800: '#9d174d',  // Very dark pink
      900: '#831843'   // Deepest pink
    },
    
    // Neutral System - High Contrast Professional
    neutral: {
      50: '#ffffff',   // Pure white
      100: '#f8fafc',  // Very light gray
      200: '#f1f5f9',  // Light gray
      300: '#e2e8f0',  // Medium light gray
      400: '#cbd5e1',  // Medium gray
      500: '#334155',  // Primary gray - cooler tone
      600: '#475569',  // Darker gray
      700: '#64748b',  // Deep gray
      800: '#1e293b',  // Very dark gray
      900: '#0f172a'   // Deepest gray
    },
    
    // Success Green - Results & Growth
    success: {
      50: '#f0fdf4',   // Very light green tint
      100: '#dcfce7',  // Light green tint
      200: '#bbf7d0',  // Medium light green
      300: '#86efac',  // Medium green
      400: '#4ade80',  // Medium bright green
      500: '#10b981',  // Primary success green
      600: '#059669',  // Darker green
      700: '#047857',  // Deep green
      800: '#065f46',  // Very dark green
      900: '#064e3b'   // Deepest green
    },
    
    // Semantic Colors
    success: '#10b981',  // Modern green
    warning: '#f59e0b',  // Amber
    error: '#ef4444',    // Modern red
    info: '#06b6d4'      // Cyan
  },

  // Typography System - Technical & Precise
  typography: {
    fontFamily: {
      primary: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      mono: ['JetBrains Mono', 'Monaco', 'Cascadia Code', 'monospace'],
      display: ['Inter', 'system-ui', 'sans-serif'] // Same as primary for consistency
    },
    
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],     // 12px
      sm: ['0.875rem', { lineHeight: '1.25rem' }], // 14px
      base: ['1rem', { lineHeight: '1.5rem' }],    // 16px - primary reading
      lg: ['1.125rem', { lineHeight: '1.75rem' }], // 18px
      xl: ['1.25rem', { lineHeight: '1.75rem' }],  // 20px
      '2xl': ['1.5rem', { lineHeight: '2rem' }],   // 24px
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }], // 30px
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],   // 36px
      '5xl': ['3rem', { lineHeight: '1' }],        // 48px - major headlines
      '6xl': ['3.75rem', { lineHeight: '1' }],     // 60px
      '7xl': ['4.5rem', { lineHeight: '1' }],      // 72px
      '8xl': ['6rem', { lineHeight: '1' }],        // 96px
      '9xl': ['8rem', { lineHeight: '1' }]         // 128px
    },
    
    fontWeight: {
      thin: '100',
      extralight: '200',
      light: '300',
      normal: '400',    // Body text
      medium: '500',    // Subheadings
      semibold: '600',  // Important content
      bold: '700',      // Headlines
      extrabold: '800', // Major headlines
      black: '900'      // Display text
    },
    
    lineHeight: {
      none: '1',
      tight: '1.25',    // Headlines
      snug: '1.375',    // Subheadings
      normal: '1.5',    // Body text
      relaxed: '1.625', // Longer content
      loose: '2'        // Special cases
    },
    
    letterSpacing: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0em',
      wide: '0.025em',    // Technical text
      wider: '0.05em',
      widest: '0.1em'     // Headers
    }
  },

  // Spacing System - Precise & Systematic
  spacing: {
    px: '1px',
    0: '0',
    0.5: '0.125rem', // 2px
    1: '0.25rem',    // 4px
    1.5: '0.375rem', // 6px
    2: '0.5rem',     // 8px
    2.5: '0.625rem', // 10px
    3: '0.75rem',    // 12px
    3.5: '0.875rem', // 14px
    4: '1rem',       // 16px - base unit
    5: '1.25rem',    // 20px
    6: '1.5rem',     // 24px
    7: '1.75rem',    // 28px
    8: '2rem',       // 32px
    9: '2.25rem',    // 36px
    10: '2.5rem',    // 40px
    11: '2.75rem',   // 44px
    12: '3rem',      // 48px
    14: '3.5rem',    // 56px
    16: '4rem',      // 64px
    20: '5rem',      // 80px
    24: '6rem',      // 96px
    28: '7rem',      // 112px
    32: '8rem',      // 128px
    36: '9rem',      // 144px
    40: '10rem',     // 160px
    44: '11rem',     // 176px
    48: '12rem',     // 192px
    52: '13rem',     // 208px
    56: '14rem',     // 224px
    60: '15rem',     // 240px
    64: '16rem',     // 256px
    72: '18rem',     // 288px
    80: '20rem',     // 320px
    96: '24rem'      // 384px
  },

  // Border Radius - Sharp & Modern
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    DEFAULT: '0.25rem', // 4px - buttons
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px - cards
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px - larger components
    '3xl': '1.5rem',  // 24px
    full: '9999px'    // Pills
  },

  // Box Shadow - Technical & Layered
  boxShadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    DEFAULT: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
    none: 'none',
    // Tech-specific shadows
    'tech-sm': '0 2px 4px 0 rgb(6 182 212 / 0.1)',
    'tech-md': '0 4px 8px 0 rgb(6 182 212 / 0.1), 0 2px 4px 0 rgb(124 58 237 / 0.05)',
    'tech-lg': '0 8px 16px 0 rgb(6 182 212 / 0.1), 0 4px 8px 0 rgb(124 58 237 / 0.05)'
  },

  // Gradients - AI/Tech Industry Standard
  gradients: {
    primary: 'linear-gradient(135deg, #7c3aed 0%, #ec4899 100%)',
    secondary: 'linear-gradient(135deg, #06b6d4 0%, #7c3aed 100%)',
    accent: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
    dark: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
    // Subtle gradients for backgrounds
    'bg-primary': 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
    'bg-secondary': 'linear-gradient(135deg, #ecfeff 0%, #f0fdf4 100%)'
  },

  // Component-Specific Tokens
  components: {
    // Button variants for tech audience
    button: {
      primary: {
        background: 'linear-gradient(135deg, #7c3aed 0%, #ec4899 100%)',
        color: '#ffffff',
        hover: 'linear-gradient(135deg, #6d28d9 0%, #db2777 100%)',
        shadow: 'tech-md',
        borderRadius: 'md'
      },
      secondary: {
        background: '#06b6d4',
        color: '#ffffff',
        hover: '#0891b2',
        shadow: 'tech-sm',
        borderRadius: 'md'
      },
      outline: {
        border: '#06b6d4',
        color: '#06b6d4',
        hover: '#ecfeff',
        shadow: 'none',
        borderRadius: 'md'
      },
      ghost: {
        background: 'transparent',
        color: '#334155',
        hover: '#f1f5f9',
        shadow: 'none',
        borderRadius: 'md'
      }
    },
    
    // Card styling for data presentation
    card: {
      background: '#ffffff',
      border: '#e2e8f0',
      shadow: 'lg',
      borderRadius: 'lg',
      padding: '24px',
      // Tech card variant
      tech: {
        background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
        border: '#cbd5e1',
        shadow: 'tech-lg',
        borderRadius: 'xl',
        padding: '32px'
      }
    },
    
    // Form elements for professional look
    form: {
      input: {
        border: '#cbd5e1',
        focus: '#06b6d4',
        background: '#ffffff',
        borderRadius: 'md',
        padding: '12px 16px',
        fontSize: 'base'
      },
      label: {
        color: '#0f172a',
        fontWeight: 'medium',
        fontSize: 'sm'
      },
      // Technical input variant
      technical: {
        fontFamily: 'mono',
        background: '#f8fafc',
        border: '#e2e8f0',
        borderRadius: 'sm'
      }
    },
    
    // Data visualization components
    chart: {
      primary: '#7c3aed',
      secondary: '#06b6d4',
      tertiary: '#10b981',
      quaternary: '#f59e0b',
      grid: '#e2e8f0',
      text: '#64748b',
      background: '#ffffff'
    },
    
    // Code and technical content
    code: {
      background: '#0f172a',
      color: '#e2e8f0',
      border: '#334155',
      borderRadius: 'md',
      fontFamily: 'mono',
      fontSize: 'sm'
    }
  },

  // Breakpoints - Desktop-first approach for this audience
  screens: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
    '3xl': '1920px'  // Large desktop displays
  },

  // Animation & Transitions - Smooth & Professional
  animation: {
    none: 'none',
    spin: 'spin 1s linear infinite',
    ping: 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
    pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    bounce: 'bounce 1s infinite',
    // Tech-specific animations
    'fade-in': 'fadeIn 0.3s ease-out',
    'slide-up': 'slideUp 0.4s ease-out',
    'slide-down': 'slideDown 0.4s ease-out',
    'scale-in': 'scaleIn 0.2s ease-out',
    'tech-glow': 'techGlow 2s ease-in-out infinite',
    'gradient-shift': 'gradientShift 3s ease-in-out infinite'
  },

  // Transition timing for professional feel
  transitionDuration: {
    75: '75ms',
    100: '100ms',
    150: '150ms',
    200: '200ms',   // Primary for interactions
    300: '300ms',   // Secondary animations
    500: '500ms',   // Complex animations
    700: '700ms',
    1000: '1000ms'
  },

  // Transition timing functions
  transitionTimingFunction: {
    DEFAULT: 'cubic-bezier(0.4, 0, 0.2, 1)',
    linear: 'linear',
    in: 'cubic-bezier(0.4, 0, 1, 1)',
    out: 'cubic-bezier(0, 0, 0.2, 1)',
    'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)'
  },

  // Z-index system for complex layouts
  zIndex: {
    auto: 'auto',
    0: '0',
    10: '10',      // Dropdowns
    20: '20',      // Sticky headers
    30: '30',      // Modals
    40: '40',      // Tooltips
    50: '50',      // Toast notifications
    60: '60',      // Loading overlays
    70: '70',      // Critical alerts
    80: '80',      // Maximum priority
    90: '90',      // Development tools
    100: '100'     // Absolute maximum
  }
};

// Export individual token categories for selective imports
export const {
  colors: sarahColors,
  typography: sarahTypography,
  spacing: sarahSpacing,
  borderRadius: sarahBorderRadius,
  boxShadow: sarahShadow,
  gradients: sarahGradients,
  components: sarahComponents
} = drSarahTechTokens;

export default drSarahTechTokens;