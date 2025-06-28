// Service Layer Index
// Zentrale Verwaltung aller externen API-Services

export { 
  InstapageService, 
  getInstapageService, 
  duplicatePage, 
  createPersonalizedPage 
} from './instapageService';

export { 
  N8nService, 
  getN8nService, 
  sendLeadToN8n 
} from './n8nService';

// Service Manager für zentrale Verwaltung
export class ServiceManager {
  private static instance: ServiceManager;
  private services: Map<string, any> = new Map();

  private constructor() {}

  static getInstance(): ServiceManager {
    if (!ServiceManager.instance) {
      ServiceManager.instance = new ServiceManager();
    }
    return ServiceManager.instance;
  }

  /**
   * Registriert einen Service
   */
  registerService(name: string, service: any): void {
    this.services.set(name, service);
  }

  /**
   * Holt einen registrierten Service
   */
  getService<T>(name: string): T | null {
    return this.services.get(name) || null;
  }

  /**
   * Testet alle Services
   */
  async testAllServices(): Promise<Record<string, boolean>> {
    const results: Record<string, boolean> = {};

    // Test Instapage Service
    try {
      const instapageService = this.getService('instapage');
      if (instapageService) {
        results.instapage = await instapageService.testConnection();
      }
    } catch (error) {
      results.instapage = false;
    }

    // Test n8n Service
    try {
      const n8nService = this.getService('n8n');
      if (n8nService) {
        results.n8n = await n8nService.testConnection();
      }
    } catch (error) {
      results.n8n = false;
    }

    return results;
  }

  /**
   * Initialisiert alle Services
   */
  async initializeServices(): Promise<void> {
    try {
      // Initialisiere Instapage Service
      if (process.env.ENABLE_INSTAPAGE_INTEGRATION === 'true') {
        const { getInstapageService } = await import('./instapageService');
        this.registerService('instapage', getInstapageService());
      }

      // Initialisiere n8n Service
      if (process.env.ENABLE_N8N_INTEGRATION === 'true') {
        const { getN8nService } = await import('./n8nService');
        this.registerService('n8n', getN8nService());
      }

      console.log('All services initialized successfully');
    } catch (error) {
      console.error('Failed to initialize services:', error);
      throw error;
    }
  }
}

// Export der Service Manager Instanz
export const serviceManager = ServiceManager.getInstance(); 