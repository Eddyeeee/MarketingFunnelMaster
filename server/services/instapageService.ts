import { z } from 'zod';

// Node.js types für process.env
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      INSTAPAGE_API_KEY: string;
      INSTAPAGE_ACCOUNT_ID: string;
      INSTAPAGE_BASE_URL?: string;
      NODE_ENV: 'development' | 'production' | 'test';
    }
  }
}

// TypeScript interfaces für Instapage API
interface InstapagePage {
  id: string;
  name: string;
  url: string;
  status: 'published' | 'draft' | 'archived';
  created_at: string;
  updated_at: string;
}

interface InstapagePageCreateRequest {
  name: string;
  template_id?: string;
  account_id: string;
}

interface InstapagePageDuplicateRequest {
  page_id: string;
  new_name: string;
  account_id: string;
}

// Zod schemas für Validierung
const instapagePageSchema = z.object({
  id: z.string(),
  name: z.string(),
  url: z.string().url(),
  status: z.enum(['published', 'draft', 'archived']),
  created_at: z.string(),
  updated_at: z.string()
});

const instapagePageCreateSchema = z.object({
  name: z.string().min(1),
  template_id: z.string().optional(),
  account_id: z.string().min(1)
});

const instapagePageDuplicateSchema = z.object({
  page_id: z.string().min(1),
  new_name: z.string().min(1),
  account_id: z.string().min(1)
});

// Instapage API Service Class
export class InstapageService {
  private apiKey: string;
  private accountId: string;
  private baseUrl: string;

  constructor() {
    this.apiKey = process.env.INSTAPAGE_API_KEY;
    this.accountId = process.env.INSTAPAGE_ACCOUNT_ID;
    this.baseUrl = process.env.INSTAPAGE_BASE_URL || 'https://api.instapage.com/api/1';

    if (!this.apiKey) {
      throw new Error('INSTAPAGE_API_KEY environment variable is required');
    }
    if (!this.accountId) {
      throw new Error('INSTAPAGE_ACCOUNT_ID environment variable is required');
    }
  }

  private async makeRequest<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultHeaders = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Instapage API error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      return data as T;
    } catch (error) {
      console.error('Instapage API request failed:', error);
      throw new Error(`Failed to communicate with Instapage API: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Holt alle Seiten des Accounts
   */
  async getPages(): Promise<InstapagePage[]> {
    try {
      const response = await this.makeRequest<{ data: InstapagePage[] }>(`/accounts/${this.accountId}/pages`);
      
      // Validiere die Antwort
      const pages = response.data.map(page => instapagePageSchema.parse(page));
      return pages;
    } catch (error) {
      console.error('Failed to fetch Instapage pages:', error);
      throw error;
    }
  }

  /**
   * Holt eine spezifische Seite
   */
  async getPage(pageId: string): Promise<InstapagePage> {
    try {
      const response = await this.makeRequest<{ data: InstapagePage }>(`/pages/${pageId}`);
      return instapagePageSchema.parse(response.data);
    } catch (error) {
      console.error(`Failed to fetch Instapage page ${pageId}:`, error);
      throw error;
    }
  }

  /**
   * Erstellt eine neue Seite
   */
  async createPage(pageData: InstapagePageCreateRequest): Promise<InstapagePage> {
    try {
      // Validiere die Eingabedaten
      const validatedData = instapagePageCreateSchema.parse(pageData);
      
      const response = await this.makeRequest<{ data: InstapagePage }>('/pages', {
        method: 'POST',
        body: JSON.stringify(validatedData)
      });
      
      return instapagePageSchema.parse(response.data);
    } catch (error) {
      console.error('Failed to create Instapage page:', error);
      throw error;
    }
  }

  /**
   * Dupliziert eine bestehende Seite
   */
  async duplicatePage(duplicateData: InstapagePageDuplicateRequest): Promise<InstapagePage> {
    try {
      // Validiere die Eingabedaten
      const validatedData = instapagePageDuplicateSchema.parse(duplicateData);
      
      const response = await this.makeRequest<{ data: InstapagePage }>(`/pages/${validatedData.page_id}/duplicate`, {
        method: 'POST',
        body: JSON.stringify({
          name: validatedData.new_name,
          account_id: validatedData.account_id
        })
      });
      
      return instapagePageSchema.parse(response.data);
    } catch (error) {
      console.error('Failed to duplicate Instapage page:', error);
      throw error;
    }
  }

  /**
   * Aktualisiert eine Seite
   */
  async updatePage(pageId: string, updates: Partial<InstapagePage>): Promise<InstapagePage> {
    try {
      const response = await this.makeRequest<{ data: InstapagePage }>(`/pages/${pageId}`, {
        method: 'PUT',
        body: JSON.stringify(updates)
      });
      
      return instapagePageSchema.parse(response.data);
    } catch (error) {
      console.error(`Failed to update Instapage page ${pageId}:`, error);
      throw error;
    }
  }

  /**
   * Löscht eine Seite
   */
  async deletePage(pageId: string): Promise<void> {
    try {
      await this.makeRequest(`/pages/${pageId}`, {
        method: 'DELETE'
      });
    } catch (error) {
      console.error(`Failed to delete Instapage page ${pageId}:`, error);
      throw error;
    }
  }

  /**
   * Erstellt eine personalisierte Landing Page basierend auf Persona
   */
  async createPersonalizedPage(
    templateId: string, 
    persona: {
      name: string;
      type: string;
      preferences: Record<string, any>;
    }
  ): Promise<InstapagePage> {
    try {
      // Erstelle einen personalisierten Namen für die Seite
      const pageName = `Q-Money ${persona.name} - ${persona.type} - ${new Date().toISOString().split('T')[0]}`;
      
      // Dupliziere die Template-Seite
      const duplicatedPage = await this.duplicatePage({
        page_id: templateId,
        new_name: pageName,
        account_id: this.accountId
      });

      // Hier könntest du später personalisierte Inhalte setzen
      // await this.updatePageContent(duplicatedPage.id, persona.preferences);
      
      return duplicatedPage;
    } catch (error) {
      console.error('Failed to create personalized page:', error);
      throw error;
    }
  }

  /**
   * Testet die API-Verbindung
   */
  async testConnection(): Promise<boolean> {
    try {
      await this.makeRequest(`/accounts/${this.accountId}`);
      return true;
    } catch (error) {
      console.error('Instapage API connection test failed:', error);
      return false;
    }
  }
}

// Singleton-Instanz für die gesamte Anwendung
let instapageServiceInstance: InstapageService | null = null;

export function getInstapageService(): InstapageService {
  if (!instapageServiceInstance) {
    instapageServiceInstance = new InstapageService();
  }
  return instapageServiceInstance;
}

// Utility-Funktionen für einfache Verwendung
export async function duplicatePage(templateId: string, newName: string): Promise<InstapagePage> {
  const service = getInstapageService();
  return service.duplicatePage({
    page_id: templateId,
    new_name: newName,
    account_id: process.env.INSTAPAGE_ACCOUNT_ID!
  });
}

export async function createPersonalizedPage(
  templateId: string, 
  persona: { name: string; type: string; preferences: Record<string, any> }
): Promise<InstapagePage> {
  const service = getInstapageService();
  return service.createPersonalizedPage(templateId, persona);
} 