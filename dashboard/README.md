# Intelligence Dashboard

Enterprise-grade intelligence dashboard with 2025-ready features for modern marketing automation.

## Features

### Core Infrastructure
- ✅ **WebSocket Real-time Updates** - Live data streaming with automatic reconnection
- ✅ **GraphQL API** - Efficient data fetching with subscriptions
- ✅ **Redis Caching** - High-performance data caching layer
- ✅ **TypeScript** - End-to-end type safety

### Dashboard Components
- ✅ **Live Process Viewer** - Real-time process monitoring with WebSocket integration
- ✅ **Search Interface** - AI-powered research data search with advanced filtering
- ✅ **Expandable Tree View** - Hierarchical data visualization with smart navigation
- ✅ **AI Metrics Dashboard** - Real-time AI search rankings and performance tracking

### 2025-Ready Features
- 🚀 **AI Metrics Dashboard** - Perplexity visibility, answer engine performance, voice search analytics
- 🚀 **Predictive Intelligence** - Trend prediction, viral probability, market opportunity alerts
- 🚀 **Multi-Channel Orchestrator** - Unified content distribution with platform-specific adaptations
- 🚀 **Revenue Intelligence** - Live revenue tracking with LTV calculations and channel attribution
- 🚀 **Automation Monitor** - Workflow health status with API usage monitoring
- 🚀 **Scaling Assistant** - Growth opportunity alerts with AI-powered recommendations

## Tech Stack

### Backend
- **Node.js + TypeScript** - Server runtime
- **Apollo Server** - GraphQL API with subscriptions
- **WebSocket Server** - Real-time communication
- **Redis** - Caching and session management
- **Express** - HTTP server framework

### Frontend
- **React 18** - UI framework with concurrent features
- **TypeScript** - Type safety
- **Apollo Client** - GraphQL client with caching
- **TailwindCSS** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Recharts** - Data visualization
- **Framer Motion** - Smooth animations

### Development
- **Vite** - Fast development server
- **ESLint + Prettier** - Code quality
- **Vitest** - Unit testing
- **Docker** - Containerization

## Quick Start

### Prerequisites
- Node.js 18+
- Redis server
- npm or yarn

### Installation

1. **Clone and setup**:
```bash
cd dashboard
npm install
```

2. **Environment Setup**:
```bash
# Server
cp server/.env.example server/.env
# Client  
cp client/.env.example client/.env
```

3. **Start Redis**:
```bash
# macOS with Homebrew
brew services start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

4. **Development**:
```bash
# Start all services
npm run dev

# Or individually
npm run dev:server  # GraphQL + WebSocket servers
npm run dev:client  # React development server
```

### Access Points
- **Dashboard**: http://localhost:3000
- **GraphQL Playground**: http://localhost:4000/graphql
- **WebSocket**: ws://localhost:4001

## Architecture

### Monorepo Structure
```
dashboard/
├── shared/           # Shared types and schemas
├── server/           # Backend services
│   ├── graphql/     # GraphQL schema and resolvers
│   ├── websocket/   # Real-time WebSocket server
│   └── redis/       # Cache layer
├── client/          # React frontend
│   ├── components/  # UI components
│   ├── features/    # Feature components
│   └── services/    # API clients
└── package.json     # Workspace configuration
```

### Data Flow
1. **Real-time Updates**: WebSocket → React State → UI
2. **GraphQL Queries**: Apollo Client → GraphQL Server → Redis Cache
3. **Subscriptions**: GraphQL Subscriptions → Real-time UI Updates

## Features in Detail

### Live Process Viewer
- Real-time process monitoring
- CPU, memory, and performance metrics
- Interactive logs with filtering
- Process control (start/stop/restart)

### Intelligence Search
- AI-powered research data search
- Hierarchical result visualization
- Entity extraction and sentiment analysis
- Search history and suggestions

### AI Metrics Dashboard
- Multi-platform performance tracking (Perplexity, ChatGPT, Claude, Bard)
- Search ranking trends
- Voice search analytics
- Competitor positioning analysis

### Tree View Component
- Expandable/collapsible nodes
- Virtual scrolling for large datasets
- Search and filtering
- Keyboard navigation support

## Development

### Available Scripts
```bash
# Development
npm run dev              # Start all services
npm run dev:server       # Backend only
npm run dev:client       # Frontend only

# Building
npm run build           # Build all packages
npm run build:server    # Build server
npm run build:client    # Build client

# Testing
npm test               # Run all tests
npm run test:coverage  # Test coverage report

# Code Quality
npm run lint           # ESLint check
npm run type-check     # TypeScript check
npm run format         # Prettier format
```

### Adding New Features

1. **GraphQL Schema**: Update `server/src/graphql/schema.ts`
2. **Resolvers**: Add to `server/src/graphql/resolvers.ts`
3. **Types**: Update `shared/src/types.ts`
4. **Components**: Create in `client/src/components/features/`

### WebSocket Events
```typescript
// Subscribe to channels
wsClient.subscribe('processes')
wsClient.subscribe('metrics')
wsClient.subscribe('revenue')

// Handle events
wsClient.on('process_update', (process) => {
  // Handle process update
})

wsClient.on('metric_update', (metrics) => {
  // Handle metrics update
})
```

## Deployment

### Production Build
```bash
npm run build
```

### Docker
```bash
# Build images
docker build -t intelligence-dashboard-server ./server
docker build -t intelligence-dashboard-client ./client

# Run with docker-compose
docker-compose up -d
```

### Environment Variables

#### Server (.env)
```bash
PORT=4000
WS_PORT=4001
REDIS_HOST=localhost
REDIS_PORT=6379
NODE_ENV=production
```

#### Client (.env)
```bash
VITE_GRAPHQL_URI=https://your-api.com/graphql
VITE_GRAPHQL_WS_URI=wss://your-api.com/graphql-ws
VITE_WS_URI=wss://your-api.com:4001
```

## Performance Optimization

### Caching Strategy
- **Redis**: API responses and computed data
- **Apollo Client**: GraphQL query caching
- **Browser**: Static assets and images

### Real-time Optimization
- WebSocket connection pooling
- Efficient data serialization
- Smart update batching

### Bundle Optimization
- Code splitting by route and feature
- Tree shaking for unused code
- Asset optimization and compression

## Monitoring

### Health Checks
- **Server**: `GET /health`
- **Metrics**: `GET /metrics`
- **WebSocket**: Connection status monitoring

### Performance Metrics
- API response times
- WebSocket message throughput
- Memory and CPU usage
- Cache hit rates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

### Code Standards
- TypeScript strict mode
- ESLint + Prettier configuration
- Component documentation
- Unit test coverage

## Roadmap

### Q1 2025
- [ ] Advanced predictive analytics
- [ ] Machine learning integration
- [ ] Enhanced data visualization
- [ ] Mobile responsive improvements

### Q2 2025
- [ ] Multi-tenant support
- [ ] Advanced security features
- [ ] API rate limiting
- [ ] Comprehensive audit logging

## License

MIT License - see LICENSE file for details

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review example implementations