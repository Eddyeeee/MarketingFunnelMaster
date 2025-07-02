/**
 * Tailwind CSS Configuration for Dr. Sarah Tech Persona
 * Sophisticated, data-driven design system
 */

import { drSarahTechTokens } from '../design-tokens/dr-sarah-tech.js';

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
        primary: drSarahTechTokens.colors.primary,
        cyan: drSarahTechTokens.colors.cyan,
        purple: drSarahTechTokens.colors.purple,
        pink: drSarahTechTokens.colors.pink,
        neutral: drSarahTechTokens.colors.neutral,
        success: drSarahTechTokens.colors.success,
        
        // Semantic colors
        warning: drSarahTechTokens.colors.warning,
        error: drSarahTechTokens.colors.error,
        info: drSarahTechTokens.colors.info,
        
        // Brand-specific aliases
        'sarah-primary': drSarahTechTokens.colors.primary[500],
        'sarah-cyan': drSarahTechTokens.colors.cyan[500],
        'sarah-purple': drSarahTechTokens.colors.purple[500],
        'sarah-gradient-start': drSarahTechTokens.colors.purple[500],
        'sarah-gradient-end': drSarahTechTokens.colors.pink[500],
        'sarah-background': drSarahTechTokens.colors.neutral[50],
        'sarah-surface': drSarahTechTokens.colors.neutral[100],
        'sarah-text': drSarahTechTokens.colors.neutral[900],
        'sarah-text-secondary': drSarahTechTokens.colors.neutral[500]
      },
      
      // Typography from design tokens
      fontFamily: {
        sans: drSarahTechTokens.typography.fontFamily.primary,
        mono: drSarahTechTokens.typography.fontFamily.mono,
        display: drSarahTechTokens.typography.fontFamily.display
      },
      
      fontSize: drSarahTechTokens.typography.fontSize,
      fontWeight: drSarahTechTokens.typography.fontWeight,
      lineHeight: drSarahTechTokens.typography.lineHeight,
      letterSpacing: drSarahTechTokens.typography.letterSpacing,
      
      // Spacing system
      spacing: drSarahTechTokens.spacing,
      
      // Border radius
      borderRadius: drSarahTechTokens.borderRadius,
      
      // Box shadow
      boxShadow: drSarahTechTokens.boxShadow,
      
      // Gradients
      backgroundImage: {
        ...Object.fromEntries(
          Object.entries(drSarahTechTokens.gradients).map(([key, value]) => [`sarah-${key}`, value])
        ),
        // Additional tech-specific gradients
        'tech-mesh': 'radial-gradient(at 40% 20%, #7c3aed 0px, transparent 50%), radial-gradient(at 80% 0%, #06b6d4 0px, transparent 50%), radial-gradient(at 0% 50%, #ec4899 0px, transparent 50%)',
        'data-viz': 'linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%)',
        'ai-pattern': 'linear-gradient(45deg, #7c3aed 25%, transparent 25%), linear-gradient(-45deg, #06b6d4 25%, transparent 25%)'
      },
      
      // Animation
      animation: drSarahTechTokens.animation,
      transitionDuration: drSarahTechTokens.transitionDuration,
      transitionTimingFunction: drSarahTechTokens.transitionTimingFunction,
      
      // Z-index
      zIndex: drSarahTechTokens.zIndex,
      
      // Custom utilities for tech audience
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px',
        '2xl': '24px',
        '3xl': '32px'
      },
      
      // Typography scales for data presentation
      scale: {
        '102': '1.02',
        '103': '1.03',
        '97': '0.97',
        '98': '0.98'
      },
      
      // Additional breakpoints for large displays
      screens: {
        '3xl': '1920px',
        '4xl': '2560px'
      }
    },
  },
  plugins: [
    // Form styles plugin
    require('@tailwindcss/forms')({
      strategy: 'class'
    }),
    
    // Typography plugin
    require('@tailwindcss/typography'),
    
    // Container queries for responsive components
    require('@tailwindcss/container-queries'),
    
    // Custom plugin for Sarah-specific utilities
    function({ addUtilities, addComponents, theme }) {
      const newUtilities = {
        // Tech-focused button styles
        '.btn-sarah-primary': {
          background: theme('backgroundImage.sarah-primary'),
          color: theme('colors.white'),
          padding: `${theme('spacing.3')} ${theme('spacing.8')}`,
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          fontSize: theme('fontSize.base'),
          boxShadow: theme('boxShadow.tech-md'),
          transition: 'all 0.2s ease-out',
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: '0',
            left: '0',
            right: '0',
            bottom: '0',
            background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%)',
            opacity: '0',
            transition: 'opacity 0.2s ease-out'
          },
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: theme('boxShadow.tech-lg'),
            '&::before': {
              opacity: '1'
            }
          },
          '&:active': {
            transform: 'translateY(0)',
            boxShadow: theme('boxShadow.tech-sm')\n          }\n        },\n        \n        '.btn-sarah-secondary': {\n          backgroundColor: theme('colors.cyan.500'),\n          color: theme('colors.white'),\n          padding: `${theme('spacing.3')} ${theme('spacing.6')}`,\n          borderRadius: theme('borderRadius.md'),\n          fontWeight: theme('fontWeight.medium'),\n          fontSize: theme('fontSize.base'),\n          boxShadow: theme('boxShadow.tech-sm'),\n          transition: 'all 0.15s ease-out',\n          '&:hover': {\n            backgroundColor: theme('colors.cyan.600'),\n            boxShadow: theme('boxShadow.tech-md'),\n            transform: 'translateY(-1px)'\n          }\n        },\n        \n        '.btn-sarah-outline': {\n          backgroundColor: 'transparent',\n          color: theme('colors.cyan.600'),\n          border: `2px solid ${theme('colors.cyan.500')}`,\n          padding: `${theme('spacing.2.5')} ${theme('spacing.6')}`,\n          borderRadius: theme('borderRadius.md'),\n          fontWeight: theme('fontWeight.medium'),\n          fontSize: theme('fontSize.base'),\n          transition: 'all 0.15s ease-out',\n          '&:hover': {\n            backgroundColor: theme('colors.cyan.50'),\n            borderColor: theme('colors.cyan.600')\n          }\n        },\n        \n        // Data visualization card styles\n        '.card-sarah-data': {\n          backgroundColor: theme('colors.white'),\n          border: `1px solid ${theme('colors.neutral.200')}`,\n          borderRadius: theme('borderRadius.xl'),\n          padding: theme('spacing.8'),\n          boxShadow: theme('boxShadow.tech-lg'),\n          position: 'relative',\n          overflow: 'hidden',\n          '&::before': {\n            content: '""',\n            position: 'absolute',\n            top: '0',\n            left: '0',\n            right: '0',\n            height: '4px',\n            background: theme('backgroundImage.sarah-primary')\n          },\n          '&:hover': {\n            boxShadow: theme('boxShadow.tech-xl'),\n            transform: 'translateY(-4px)',\n            transition: 'all 0.3s ease-out'\n          }\n        },\n        \n        // Technical content card\n        '.card-sarah-tech': {\n          background: theme('backgroundImage.sarah-bg-primary'),\n          border: `1px solid ${theme('colors.neutral.300')}`,\n          borderRadius: theme('borderRadius.xl'),\n          padding: theme('spacing.8'),\n          boxShadow: theme('boxShadow.tech-lg'),\n          backdropFilter: 'blur(8px)'\n        },\n        \n        // Code block styles\n        '.code-sarah': {\n          backgroundColor: theme('colors.primary.500'),\n          color: theme('colors.neutral.200'),\n          fontFamily: theme('fontFamily.mono'),\n          fontSize: theme('fontSize.sm'),\n          borderRadius: theme('borderRadius.md'),\n          padding: theme('spacing.4'),\n          border: `1px solid ${theme('colors.primary.400')}`,\n          '& .token.keyword': {\n            color: theme('colors.cyan.400')\n          },\n          '& .token.string': {\n            color: theme('colors.success.400')\n          },\n          '& .token.function': {\n            color: theme('colors.purple.400')\n          }\n        },\n        \n        // Metric display styles\n        '.metric-sarah': {\n          textAlign: 'center',\n          padding: theme('spacing.6'),\n          borderRadius: theme('borderRadius.lg'),\n          background: theme('backgroundImage.sarah-bg-secondary'),\n          border: `1px solid ${theme('colors.success.200')}`,\n          '& .metric-value': {\n            fontSize: theme('fontSize.4xl'),\n            fontWeight: theme('fontWeight.bold'),\n            color: theme('colors.primary.500'),\n            lineHeight: theme('lineHeight.none')\n          },\n          '& .metric-label': {\n            fontSize: theme('fontSize.sm'),\n            fontWeight: theme('fontWeight.medium'),\n            color: theme('colors.neutral.600'),\n            textTransform: 'uppercase',\n            letterSpacing: theme('letterSpacing.wide'),\n            marginTop: theme('spacing.2')\n          },\n          '& .metric-change': {\n            fontSize: theme('fontSize.xs'),\n            fontWeight: theme('fontWeight.medium'),\n            marginTop: theme('spacing.1')\n          },\n          '& .metric-change.positive': {\n            color: theme('colors.success.600')\n          },\n          '& .metric-change.negative': {\n            color: theme('colors.error')\n          }\n        },\n        \n        // Professional badge styles\n        '.badge-sarah-pro': {\n          backgroundColor: theme('colors.purple.100'),\n          color: theme('colors.purple.800'),\n          padding: `${theme('spacing.1')} ${theme('spacing.3')}`,\n          borderRadius: theme('borderRadius.full'),\n          fontSize: theme('fontSize.xs'),\n          fontWeight: theme('fontWeight.semibold'),\n          textTransform: 'uppercase',\n          letterSpacing: theme('letterSpacing.wide'),\n          border: `1px solid ${theme('colors.purple.200')}`\n        },\n        \n        '.badge-sarah-tech': {\n          backgroundColor: theme('colors.cyan.100'),\n          color: theme('colors.cyan.800'),\n          padding: `${theme('spacing.1')} ${theme('spacing.3')}`,\n          borderRadius: theme('borderRadius.md'),\n          fontSize: theme('fontSize.xs'),\n          fontWeight: theme('fontWeight.medium'),\n          fontFamily: theme('fontFamily.mono'),\n          border: `1px solid ${theme('colors.cyan.200')}`\n        },\n        \n        // Interactive data table styles\n        '.table-sarah': {\n          width: '100%',\n          borderCollapse: 'separate',\n          borderSpacing: '0',\n          backgroundColor: theme('colors.white'),\n          borderRadius: theme('borderRadius.lg'),\n          overflow: 'hidden',\n          boxShadow: theme('boxShadow.lg'),\n          '& thead': {\n            backgroundColor: theme('colors.neutral.100')\n          },\n          '& th': {\n            padding: `${theme('spacing.4')} ${theme('spacing.6')}`,\n            fontSize: theme('fontSize.sm'),\n            fontWeight: theme('fontWeight.semibold'),\n            color: theme('colors.neutral.700'),\n            textAlign: 'left',\n            borderBottom: `1px solid ${theme('colors.neutral.200')}`\n          },\n          '& td': {\n            padding: `${theme('spacing.4')} ${theme('spacing.6')}`,\n            fontSize: theme('fontSize.sm'),\n            color: theme('colors.neutral.600'),\n            borderBottom: `1px solid ${theme('colors.neutral.100')}`\n          },\n          '& tr:hover td': {\n            backgroundColor: theme('colors.neutral.50')\n          }\n        },\n        \n        // Gradient text effects\n        '.text-sarah-gradient': {\n          background: theme('backgroundImage.sarah-primary'),\n          backgroundClip: 'text',\n          WebkitBackgroundClip: 'text',\n          color: 'transparent',\n          fontWeight: theme('fontWeight.bold')\n        },\n        \n        // Loading states\n        '.loading-sarah': {\n          position: 'relative',\n          overflow: 'hidden',\n          '&::after': {\n            content: '""',\n            position: 'absolute',\n            top: '0',\n            right: '0',\n            bottom: '0',\n            left: '0',\n            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent)',\n            transform: 'translateX(-100%)',\n            animation: 'shimmer 1.5s infinite'\n          }\n        }\n      };\n      \n      // Add keyframe animations\n      const keyframes = {\n        '@keyframes shimmer': {\n          '100%': {\n            transform: 'translateX(100%)'\n          }\n        },\n        '@keyframes techGlow': {\n          '0%, 100%': {\n            boxShadow: `0 0 20px ${theme('colors.cyan.500')}33`\n          },\n          '50%': {\n            boxShadow: `0 0 30px ${theme('colors.purple.500')}33`\n          }\n        },\n        '@keyframes gradientShift': {\n          '0%, 100%': {\n            backgroundPosition: '0% 50%'\n          },\n          '50%': {\n            backgroundPosition: '100% 50%'\n          }\n        }\n      };\n      \n      addUtilities(newUtilities);\n      addUtilities(keyframes);\n    }\n  ],\n};