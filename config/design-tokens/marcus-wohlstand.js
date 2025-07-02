/**
 * Design Tokens for Marcus Wohlstand Persona
 * Trust-focused, authenticity-driven design system
 * Target: Financial freedom seekers who value personal connection and credibility
 */

export const marcusWohlstandTokens = {
  // Color System - Trust & Warmth Focused
  colors: {
    primary: {
      50: '#f0f4f8',   // Very light navy tint
      100: '#d6e4ed',  // Light navy tint
      200: '#adc8db',  // Medium light navy
      300: '#7aa3c4',  // Medium navy
      400: '#4a7aa7',  // Medium dark navy
      500: '#1e3a5f',  // Primary navy - financial stability
      600: '#1a3252',  // Darker navy
      700: '#152944',  // Very dark navy
      800: '#101f37',  // Ultra dark navy
      900: '#0a152a'   // Deepest navy
    },
    
    // Warm Gold - Prosperity & Achievement
    gold: {
      50: '#fefcf0',   // Very light gold tint
      100: '#fef7d3',  // Light gold tint
      200: '#fceba6',  // Medium light gold
      300: '#f8d572',  // Medium gold
      400: '#f2c142',  // Medium bright gold
      500: '#d4af37',  // Primary gold - wealth & wisdom
      600: '#b8962e',  // Darker gold
      700: '#967a24',  // Deep gold
      800: '#735e1c',  // Very dark gold
      900: '#4d3e12'   // Deepest gold
    },
    
    // Muted Green - Steady Growth
    growth: {
      50: '#f0f7f4',   // Very light green tint
      100: '#d3ebe0',  // Light green tint
      200: '#a7d7c1',  // Medium light green
      300: '#7bc3a2',  // Medium green
      400: '#5fad85',  // Medium bright green
      500: '#4a7c59',  // Primary green - steady growth
      600: '#3e6b4a',  // Darker green
      700: '#32563c',  // Deep green
      800: '#26412e',  // Very dark green
      900: '#1a2c20'   // Deepest green
    },
    
    // Neutral System - Professional & Approachable
    neutral: {
      50: '#fafafa',   // Almost white
      100: '#f4f4f5',  // Very light gray
      200: '#e4e4e7',  // Light gray
      300: '#d4d4d8',  // Medium light gray
      400: '#a1a1aa',  // Medium gray
      500: '#6b7280',  // Primary gray - warm undertone
      600: '#52525b',  // Darker gray
      700: '#3f3f46',  // Deep gray
      800: '#27272a',  // Very dark gray
      900: '#18181b'   // Deepest gray
    },
    
    // Trust Accent - Light Blue
    trust: {
      50: '#f0fdff',   // Very light blue tint
      100: '#e1f5fe',  // Light blue background
      200: '#b3e5fc',  // Medium light blue
      300: '#81d4fa',  // Medium blue
      400: '#4fc3f7',  // Medium bright blue
      500: '#29b6f6',  // Primary trust blue
      600: '#039be5',  // Darker blue
      700: '#0277bd',  // Deep blue
      800: '#01579b',  // Very dark blue
      900: '#013e7a'   // Deepest blue
    },
    
    // Semantic Colors
    success: '#4a7c59',  // Muted green
    warning: '#d4af37',  // Gold
    error: '#dc2626',    // Clear red for important alerts
    info: '#29b6f6'      // Trust blue
  },

  // Typography System - Trustworthy & Readable
  typography: {
    fontFamily: {
      primary: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      accent: ['Caveat', 'cursive'], // Handwritten for personal touch
      mono: ['JetBrains Mono', 'monospace']
    },
    
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],     // 12px
      sm: ['0.875rem', { lineHeight: '1.25rem' }], // 14px
      base: ['1rem', { lineHeight: '1.5rem' }],    // 16px - primary reading
      lg: ['1.125rem', { lineHeight: '1.75rem' }], // 18px
      xl: ['1.25rem', { lineHeight: '1.75rem' }],  // 20px
      '2xl': ['1.5rem', { lineHeight: '2rem' }],   // 24px
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }], // 30px
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],   // 36px - main headlines
      '5xl': ['3rem', { lineHeight: '1' }],        // 48px
      '6xl': ['3.75rem', { lineHeight: '1' }]      // 60px
    },
    
    fontWeight: {
      light: '300',
      normal: '400',  // Primary text weight
      medium: '500',  // Subheadings
      semibold: '600', // Important emphasis
      bold: '700'     // Headlines
    },
    
    lineHeight: {
      tight: '1.25',   // Headlines
      snug: '1.375',   // Subheadings
      normal: '1.5',   // Body text - optimal readability
      relaxed: '1.625', // Longer content
      loose: '2'       // Special cases
    },
    
    letterSpacing: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0em',      // Primary setting
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em'
    }
  },

  // Spacing System - Generous & Comfortable
  spacing: {
    px: '1px',
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px - base unit
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px - section spacing
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px - large section gaps
    16: '4rem',     // 64px - major sections
    20: '5rem',     // 80px
    24: '6rem',     // 96px - page sections
    32: '8rem',     // 128px
    40: '10rem',    // 160px
    48: '12rem',    // 192px
    56: '14rem',    // 224px
    64: '16rem'     // 256px
  },

  // Border Radius - Soft & Approachable
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    DEFAULT: '0.25rem', // 4px - primary buttons
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px - cards
    xl: '0.75rem',    // 12px - larger elements
    '2xl': '1rem',    // 16px
    '3xl': '1.5rem',  // 24px
    full: '9999px'    // Pills/badges
  },

  // Box Shadow - Subtle & Professional
  boxShadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    DEFAULT: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
    none: 'none'
  },

  // Component-Specific Tokens
  components: {
    // Button variants aligned with trust-building
    button: {
      primary: {
        background: '#1e3a5f', // Navy
        color: '#fafafa',      // Off-white
        hover: '#1a3252',      // Darker navy
        shadow: 'md'
      },
      secondary: {
        background: '#d4af37', // Gold
        color: '#18181b',      // Dark text
        hover: '#b8962e',      // Darker gold
        shadow: 'sm'
      },
      outline: {
        border: '#1e3a5f',     // Navy border
        color: '#1e3a5f',      // Navy text
        hover: '#f0f4f8',      // Light navy tint background
        shadow: 'none'
      }
    },
    
    // Card styling for testimonials and content
    card: {
      background: '#fafafa',   // Off-white
      border: '#e4e4e7',       // Light gray
      shadow: 'lg',
      borderRadius: 'lg',
      padding: '24px'          // Generous padding
    },
    
    // Form elements optimized for trust
    form: {
      input: {
        border: '#d4d4d8',     // Medium light gray
        focus: '#1e3a5f',      // Navy focus
        background: '#ffffff',  // Pure white
        borderRadius: 'md',
        padding: '12px 16px'
      },
      label: {
        color: '#3f3f46',      // Deep gray
        fontWeight: 'medium',
        fontSize: 'sm'
      }
    }
  },

  // Breakpoints - Mobile-first approach
  screens: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px'
  },

  // Animation & Transitions - Subtle & Professional
  animation: {
    none: 'none',
    spin: 'spin 1s linear infinite',
    ping: 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
    pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    bounce: 'bounce 1s infinite',
    // Custom animations for trust-building
    'fade-in': 'fadeIn 0.5s ease-in-out',
    'slide-up': 'slideUp 0.3s ease-out',
    'scale-in': 'scaleIn 0.2s ease-out'
  },

  // Transition timing optimized for perceived performance
  transitionDuration: {
    75: '75ms',
    100: '100ms',
    150: '150ms',   // Primary for hovers
    200: '200ms',   // Primary for focus states
    300: '300ms',   // Longer animations
    500: '500ms',
    700: '700ms',
    1000: '1000ms'
  },

  // Z-index system for layering
  zIndex: {
    auto: 'auto',
    0: '0',
    10: '10',      // Dropdowns
    20: '20',      // Sticky headers
    30: '30',      // Modals
    40: '40',      // Tooltips
    50: '50'       // Toast notifications
  }
};

// Export individual token categories for selective imports
export const {
  colors: marcusColors,
  typography: marcusTypography,
  spacing: marcusSpacing,
  borderRadius: marcusBorderRadius,
  boxShadow: marcusShadow,
  components: marcusComponents
} = marcusWohlstandTokens;

export default marcusWohlstandTokens;