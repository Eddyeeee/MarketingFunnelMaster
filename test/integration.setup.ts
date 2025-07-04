// Integration test setup for UX Intelligence Engine staging environment
import { expect } from 'vitest'

// Extend expect with custom matchers
declare global {
  namespace Vi {
    interface AsymmetricMatchersContaining {
      toBeOneOf(expected: any[]): any;
    }
  }
}

expect.extend({
  toBeOneOf(received: any, expected: any[]) {
    const pass = expected.includes(received);
    if (pass) {
      return {
        message: () => `expected ${received} not to be one of ${expected}`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${received} to be one of ${expected}`,
        pass: false,
      };
    }
  },
});

// Global test configuration
global.fetch = global.fetch || require('node-fetch');

// Test environment configuration
const STAGING_CONFIG = {
  baseUrl: process.env.STAGING_URL || 'http://localhost:3000',
  analyticsUrl: process.env.ANALYTICS_URL || 'http://localhost:8080',
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  postgresUrl: process.env.POSTGRES_URL || 'postgresql://analytics:password@localhost:5432/ux_analytics',
  timeout: 30000
};

// Make configuration available globally
(global as any).STAGING_CONFIG = STAGING_CONFIG;

// Health check function for staging services
export async function waitForService(url: string, timeout = 30000): Promise<boolean> {
  const start = Date.now();
  
  while (Date.now() - start < timeout) {
    try {
      const response = await fetch(`${url}/health`);
      if (response.ok) {
        return true;
      }
    } catch (error) {
      // Service not ready yet
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return false;
}

// Setup function to verify staging environment
export async function setupStagingEnvironment(): Promise<void> {
  console.log('Setting up staging environment for integration tests...');
  
  // Check if staging services are running
  const services = [
    { name: 'Main Application', url: STAGING_CONFIG.baseUrl },
    { name: 'Analytics Service', url: STAGING_CONFIG.analyticsUrl }
  ];
  
  for (const service of services) {
    console.log(`Checking ${service.name}...`);
    const isReady = await waitForService(service.url, 30000);
    
    if (!isReady) {
      throw new Error(`${service.name} is not ready at ${service.url}. Please start the staging environment first.`);
    }
    
    console.log(`✅ ${service.name} is ready`);
  }
  
  console.log('✅ Staging environment setup complete');
}