# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Development
```bash
# Start development for specific products
npm run dev:qmoney        # Q-Money product
npm run dev:remotecash     # Remote Cash Flow product  
npm run dev:cryptoflow     # Crypto Flow Master product
npm run dev:affiliatepro   # Affiliate Pro product

# General development (client + server)
npm run dev                # Full stack dev server
npm run dev:client         # Frontend only
```

### Testing
```bash
npm test                   # Run all tests
npm run test:watch         # Run tests in watch mode
npm run test:coverage      # Generate coverage report
npm run test:ui            # Run tests with UI
```

### Code Quality
```bash
npm run lint               # Check ESLint issues
npm run lint:fix           # Fix ESLint issues
npm run type-check         # TypeScript type checking
npm run format             # Format code with Prettier
npm run format:check       # Check code formatting
```

### Building & Deployment
```bash
# Build specific products
npm run build:qmoney       # Build Q-Money
npm run build:remotecash   # Build Remote Cash Flow
npm run build:cryptoflow   # Build Crypto Flow Master
npm run build:affiliatepro # Build Affiliate Pro

# Deploy to platforms
npm run deploy:qmoney:vercel    # Deploy Q-Money to Vercel
npm run deploy:qmoney:netlify   # Deploy Q-Money to Netlify
npm run deploy:qmoney:docker    # Deploy Q-Money with Docker
```

### Performance & Security
```bash
npm run lighthouse         # Run Lighthouse performance test
npm run performance:test   # Run performance benchmarks
npm run security:audit     # Security audit
npm run analyze            # Bundle size analysis
```

## High-Level Architecture

### Multi-Product Marketing Funnel System
This is a sophisticated marketing funnel platform supporting multiple products through a single codebase. The system uses dynamic configuration to serve different products with unique branding, pricing, and content.

### Core Flow Architecture
1. **Landing Page** → Initial entry with live visitor counter and social proof
2. **Quiz System** → Interactive persona detection (6 distinct personas)
3. **VSL (Video Sales Letter)** → Multiple implementations (Animated, Intelligent, Psychological)
4. **Bridge Page** → Transition with countdown and urgency mechanics
5. **Payment** → Stripe direct + Digistore24 affiliate integration

### Key Architectural Patterns

#### Product Configuration System
- Products defined in `config/products.json`
- Dynamic theming based on `PRODUCT_ID` environment variable
- Shared components with product-specific customization
- Per-product pricing, content, and branding

#### Database Architecture
- SQLite with Drizzle ORM (`shared/schema.ts`)
- Tables: leads, analytics, upsells, sales, sessions
- JSON fields for flexible data storage
- Migration system in `migrations/`

#### Service Layer Pattern
Backend services in `server/services/`:
- `productService.ts` - Product configuration management
- `emailService.ts` - SMTP/Mailchimp/ConvertKit integration
- `paymentService.ts` - Stripe/Digistore24 processing
- `analyticsService.ts` - Event tracking and metrics
- `upsellService.ts` - Upsell flow management
- `vslService.ts` - VSL content delivery

#### Frontend Architecture
- React with TypeScript
- TanStack Query for server state
- Tailwind CSS with custom design system
- Radix UI for accessible components
- React Hook Form + Zod for forms
- Custom hooks for analytics, performance, and mobile

#### Persona-Based Targeting
Six personas with unique content flows:
1. StarterKapital - Young professionals
2. FeierabendKapital - Side income seekers
3. RemoteCashflow - Remote work enthusiasts
4. RentenRendite - Pre-retirees
5. ElternEinkommen - Parents seeking income
6. ZeitReich - Freedom seekers

### Environment Configuration
Required environment variables for production:
- `PRODUCT_ID` - Active product identifier
- `STRIPE_SECRET_KEY` - Stripe payment processing
- `DIGISTORE24_API_KEY` - Affiliate sales
- `SMTP_*` - Email configuration
- `GA_MEASUREMENT_ID` - Google Analytics
- `FB_PIXEL_ID` - Facebook tracking

### Testing Strategy
- Unit tests with Vitest and React Testing Library
- Global mocks for DOM APIs in `client/src/test-setup.ts`
- Test files alongside components (`__tests__/`)
- Coverage reporting with v8 provider

### N8n Workflow Automation
Integration with n8n for:
- Social media content automation
- Email sequence management
- Lead nurturing workflows
- Human-in-the-loop control points
See `n8n-workflows/` for workflow definitions

### Performance Optimization
- Code splitting with React.lazy
- Asset optimization with Vite
- Lighthouse score target: 95+
- CDN-ready static assets
- PWA capabilities