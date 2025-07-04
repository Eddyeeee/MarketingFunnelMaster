// Global setup for integration tests
import { setupStagingEnvironment } from './integration.setup';

export default async function globalSetup() {
  console.log('🚀 Starting global setup for UX Intelligence Engine integration tests');
  
  try {
    // Verify staging environment is ready
    await setupStagingEnvironment();
    
    console.log('✅ Global setup completed successfully');
  } catch (error) {
    console.error('❌ Global setup failed:', error);
    throw error;
  }
}