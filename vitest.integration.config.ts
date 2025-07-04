import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    name: 'integration',
    environment: 'node',
    testTimeout: 30000,
    hookTimeout: 30000,
    include: ['**/*.integration.test.ts', '**/TEC-test-UXIntelligenceEngine-v1.test.ts'],
    setupFiles: ['./test/integration.setup.ts'],
    globalSetup: ['./test/global.setup.ts'],
    globals: true,
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: true
      }
    }
  },
  define: {
    'process.env.NODE_ENV': '"test"',
    'process.env.UX_ENGINE_ENABLED': '"true"',
    'process.env.STAGING_URL': '"http://localhost:3000"',
    'process.env.ANALYTICS_URL': '"http://localhost:8080"',
    'process.env.REDIS_URL': '"redis://localhost:6379"',
    'process.env.POSTGRES_URL': '"postgresql://analytics:password@localhost:5432/ux_analytics"'
  }
})