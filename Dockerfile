# Q-Money System - Production Dockerfile
# Multi-stage build for optimized production deployment

# ===== BUILD STAGE =====
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache libc6-compat

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY client/package*.json ./client/
COPY server/package*.json ./server/ 2>/dev/null || true

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build client
RUN cd client && npm run build

# Build server
RUN npm run build:server

# ===== PRODUCTION STAGE =====
FROM node:18-alpine AS production

# Install production dependencies
RUN apk add --no-cache \
    dumb-init \
    curl \
    && addgroup -g 1001 -S nodejs \
    && adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/client/dist ./client/dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose port
EXPOSE 3000

# Switch to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server/index.js"]

# ===== DEVELOPMENT STAGE =====
FROM node:18-alpine AS development

# Install development dependencies
RUN apk add --no-cache libc6-compat git

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev)
RUN npm ci

# Copy source code
COPY . .

# Expose ports
EXPOSE 3000 5173

# Start in development mode
CMD ["npm", "run", "dev"]

# ===== LABELS FOR METADATA =====
LABEL maintainer="Q-Money Team <support@q-money-system.com>"
LABEL version="2.0.0"
LABEL description="Q-Money Marketing Funnel System - Optimized for Performance & Accessibility"
LABEL org.opencontainers.image.source="https://github.com/q-money/marketing-funnel"
LABEL org.opencontainers.image.documentation="https://docs.q-money-system.com"
LABEL org.opencontainers.image.licenses="MIT" 