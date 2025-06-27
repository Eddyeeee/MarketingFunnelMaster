# Q-Money Financial Freedom Platform

## Overview

Q-Money is a comprehensive marketing funnel platform designed to promote financial freedom systems through multiple channels including quizzes, video sales letters (VSLs), bridge pages, and text sales letters (TSLs). The platform captures leads, tracks user engagement through analytics, and manages email marketing funnels to convert prospects into customers.

## System Architecture

The application follows a full-stack architecture with a clear separation between client and server components:

### Frontend Architecture
- **Framework**: React with TypeScript, built using Vite
- **UI Framework**: shadcn/ui components built on Radix UI primitives
- **Styling**: Tailwind CSS with custom Q-Money brand colors
- **State Management**: TanStack React Query for server state
- **Routing**: Wouter for lightweight client-side routing
- **Form Handling**: React Hook Form with Zod validation

### Backend Architecture
- **Runtime**: Node.js with Express.js
- **Language**: TypeScript with ES modules
- **Database**: PostgreSQL with Drizzle ORM
- **Database Provider**: Neon Database (serverless PostgreSQL)
- **Session Management**: Express sessions with PostgreSQL store
- **Development**: Hot module replacement via Vite integration

## Key Components

### Database Schema
The application uses four main database tables:
- **users**: Authentication and user management
- **leads**: Lead capture and funnel tracking
- **emailFunnels**: Email marketing campaign templates
- **analytics**: Event tracking and user behavior analysis

### Lead Management System
- Multi-step quiz system for lead qualification
- Lead capture forms with customizable fields
- Funnel attribution tracking (magic-profit, money-magnet)
- Source tracking (quiz, vsl, bridge, tsl)

### Analytics Integration
- Google Analytics 4 integration
- Custom event tracking for user interactions
- Page view tracking with automatic route detection
- Conversion funnel monitoring

### Marketing Funnels
- **Quiz Funnel**: Interactive questionnaire for lead qualification
- **VSL (Video Sales Letter)**: Video-based sales presentations
- **Bridge Page**: Resource hub with downloadable content
- **TSL (Text Sales Letter)**: Long-form written sales content

## Data Flow

1. **User Entry**: Users enter through various channels (direct, quiz, VSL)
2. **Lead Capture**: Contact information collected via forms
3. **Funnel Assignment**: Users assigned to appropriate marketing funnel
4. **Analytics Tracking**: All interactions tracked for optimization
5. **Email Follow-up**: Automated email sequences based on funnel type

## External Dependencies

### Core Dependencies
- **@neondatabase/serverless**: Serverless PostgreSQL connection
- **drizzle-orm**: Type-safe database ORM
- **@tanstack/react-query**: Server state management
- **@radix-ui/***: Accessible UI component primitives
- **wouter**: Lightweight React router
- **react-hook-form**: Form validation and handling
- **zod**: Schema validation

### Development Tools
- **Vite**: Build tool and development server
- **TypeScript**: Type safety and better DX
- **Tailwind CSS**: Utility-first styling
- **@replit/vite-plugin-***: Replit-specific development enhancements

## Deployment Strategy

### Development Environment
- Runs on Replit with Node.js 20
- PostgreSQL 16 database module
- Hot module replacement for rapid development
- Port 5000 for local development

### Production Build
- Vite builds optimized client bundle
- esbuild compiles server code for production
- Static assets served from dist/public
- Autoscale deployment target on Replit

### Environment Configuration
- Database connection via DATABASE_URL environment variable
- Google Analytics tracking via VITE_GA_MEASUREMENT_ID
- Session management with secure cookie settings

## Changelog

- June 27, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.