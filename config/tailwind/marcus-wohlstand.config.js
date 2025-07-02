/**
 * Tailwind CSS Configuration for Marcus Wohlstand Persona
 * Trust-focused, authenticity-driven design system
 */

import { marcusWohlstandTokens } from '../design-tokens/marcus-wohlstand.js';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './client/src/**/*.{js,ts,jsx,tsx}',
    './client/index.html',
  ],
  theme: {
    extend: {
      // Color system from design tokens
      colors: {
        primary: marcusWohlstandTokens.colors.primary,
        gold: marcusWohlstandTokens.colors.gold,
        growth: marcusWohlstandTokens.colors.growth,
        neutral: marcusWohlstandTokens.colors.neutral,
        trust: marcusWohlstandTokens.colors.trust,
        
        // Semantic colors
        success: marcusWohlstandTokens.colors.success,
        warning: marcusWohlstandTokens.colors.warning,
        error: marcusWohlstandTokens.colors.error,
        info: marcusWohlstandTokens.colors.info,
        
        // Brand-specific aliases
        'marcus-navy': marcusWohlstandTokens.colors.primary[500],
        'marcus-gold': marcusWohlstandTokens.colors.gold[500],
        'marcus-growth': marcusWohlstandTokens.colors.growth[500],
        'marcus-background': marcusWohlstandTokens.colors.neutral[50],
        'marcus-text': marcusWohlstandTokens.colors.neutral[900],
        'marcus-text-secondary': marcusWohlstandTokens.colors.neutral[600]
      },
      
      // Typography from design tokens
      fontFamily: {
        sans: marcusWohlstandTokens.typography.fontFamily.primary,
        accent: marcusWohlstandTokens.typography.fontFamily.accent,
        mono: marcusWohlstandTokens.typography.fontFamily.mono
      },
      
      fontSize: marcusWohlstandTokens.typography.fontSize,
      fontWeight: marcusWohlstandTokens.typography.fontWeight,
      lineHeight: marcusWohlstandTokens.typography.lineHeight,
      letterSpacing: marcusWohlstandTokens.typography.letterSpacing,
      
      // Spacing system
      spacing: marcusWohlstandTokens.spacing,
      
      // Border radius
      borderRadius: marcusWohlstandTokens.borderRadius,
      
      // Box shadow
      boxShadow: marcusWohlstandTokens.boxShadow,
      
      // Animation
      animation: marcusWohlstandTokens.animation,
      transitionDuration: marcusWohlstandTokens.transitionDuration,
      
      // Z-index
      zIndex: marcusWohlstandTokens.zIndex,
      
      // Custom utilities for Marcus persona
      backgroundImage: {
        'marcus-gradient': 'linear-gradient(135deg, #1e3a5f 0%, #d4af37 100%)',
        'marcus-subtle': 'linear-gradient(135deg, #fafafa 0%, #f4f4f5 100%)',
        'trust-gradient': 'linear-gradient(135deg, #e1f5fe 0%, #f0f4f8 100%)'
      },
      
      // Component-specific extensions
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px'
      }
    },
  },
  plugins: [
    // Add form styles plugin for better form styling
    require('@tailwindcss/forms')({
      strategy: 'class'
    }),
    
    // Add typography plugin for better text styling
    require('@tailwindcss/typography'),
    
    // Custom plugin for Marcus-specific utilities
    function({ addUtilities, theme }) {
      const newUtilities = {
        // Trust-building button styles
        '.btn-marcus-primary': {
          backgroundColor: theme('colors.primary.500'),
          color: theme('colors.neutral.50'),
          padding: `${theme('spacing.3')} ${theme('spacing.6')}`,
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.medium'),
          fontSize: theme('fontSize.base'),
          boxShadow: theme('boxShadow.md'),
          transition: 'all 0.15s ease-in-out',
          '&:hover': {
            backgroundColor: theme('colors.primary.600'),
            boxShadow: theme('boxShadow.lg'),
            transform: 'translateY(-1px)'
          },
          '&:active': {
            transform: 'translateY(0)',
            boxShadow: theme('boxShadow.sm')
          }
        },
        
        '.btn-marcus-secondary': {
          backgroundColor: theme('colors.gold.500'),
          color: theme('colors.neutral.900'),
          padding: `${theme('spacing.3')} ${theme('spacing.6')}`,
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.medium'),
          fontSize: theme('fontSize.base'),
          boxShadow: theme('boxShadow.sm'),
          transition: 'all 0.15s ease-in-out',
          '&:hover': {
            backgroundColor: theme('colors.gold.600'),
            boxShadow: theme('boxShadow.md'),
            transform: 'translateY(-1px)'
          }
        },
        
        // Trust signal card styles
        '.card-marcus-trust': {
          backgroundColor: theme('colors.neutral.50'),
          border: `1px solid ${theme('colors.neutral.200')}`,
          borderRadius: theme('borderRadius.lg'),
          padding: theme('spacing.6'),
          boxShadow: theme('boxShadow.lg'),
          '&:hover': {
            boxShadow: theme('boxShadow.xl'),
            transform: 'translateY(-2px)',
            transition: 'all 0.2s ease-out'
          }
        },
        
        // Personal story text styles
        '.text-marcus-story': {
          fontFamily: theme('fontFamily.accent'),
          fontSize: theme('fontSize.lg'),
          lineHeight: theme('lineHeight.relaxed'),
          color: theme('colors.primary.700'),
          fontStyle: 'italic'
        },
        
        // Credibility indicator styles
        '.badge-marcus-credibility': {
          backgroundColor: theme('colors.trust.100'),
          color: theme('colors.trust.800'),
          padding: `${theme('spacing.1')} ${theme('spacing.3')}`,
          borderRadius: theme('borderRadius.full'),
          fontSize: theme('fontSize.sm'),
          fontWeight: theme('fontWeight.medium'),
          border: `1px solid ${theme('colors.trust.200')}`
        },
        
        // Testimonial styles
        '.testimonial-marcus': {
          backgroundColor: theme('colors.growth.50'),
          borderLeft: `4px solid ${theme('colors.growth.500')}`,
          padding: theme('spacing.6'),
          borderRadius: theme('borderRadius.lg'),
          fontStyle: 'italic',
          '& .testimonial-quote': {
            fontSize: theme('fontSize.lg'),
            lineHeight: theme('lineHeight.relaxed'),
            color: theme('colors.neutral.700')
          },
          '& .testimonial-author': {
            fontSize: theme('fontSize.sm'),
            fontWeight: theme('fontWeight.medium'),
            color: theme('colors.growth.700'),
            marginTop: theme('spacing.4')
          }
        }
      };
      
      addUtilities(newUtilities);
    }
  ],
};
