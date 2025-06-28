import { z } from 'zod';

// TypeScript interfaces für n8n Webhook
interface N8nWebhookPayload {
  lead: {
    email: string;
    name?: string;
    phone?: string;
    source: string;
    funnel: string;
    quizAnswers?: Record<string, any>;
    persona?: {
      type: string;
      preferences: Record<string, any>;
    };
    metadata?: Record<string, any>;
  };
  timestamp: string;
  sessionId?: string;
  userAgent?: string;
  ipAddress?: string;
}

// Zod schema für Validierung
const n8nWebhookPayloadSchema = z.object({
  lead: z.object({
    email: z.string().email(),
    name: z.string().optional(),
    phone: z.string().optional(),
    source: z.string(),
    funnel: z.string(),
    quizAnswers: z.record(z.any()).optional(),
    persona: z.object({
      type: z.string(),
      preferences: z.record(z.any())
    }).optional(),
    metadata: z.record(z.any()).optional()
  }),
  timestamp: z.string(),
  sessionId: z.string().optional(),
  userAgent: z.string().optional(),
  ipAddress: z.string().optional()
});

// n8n Webhook Service Class
export class N8nService {
  private webhookUrl: string;
  private apiKey?: string;

  constructor() {
    this.webhookUrl = process.env.N8N_WEBHOOK_URL;
    this.apiKey = process.env.N8N_API_KEY;

    if (!this.webhookUrl) {
      throw new Error('N8N_WEBHOOK_URL environment variable is required');
    }
  }

  /**
   * Sendet Lead-Daten an n8n Webhook
   */
  async sendLeadToN8n(payload: N8nWebhookPayload): Promise<boolean> {
    try {
      // Validiere die Eingabedaten
      const validatedPayload = n8nWebhookPayloadSchema.parse(payload);

      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      };

      // Füge API-Key hinzu, falls vorhanden
      if (this.apiKey) {
        headers['Authorization'] = `Bearer ${this.apiKey}`;
      }

      const response = await fetch(this.webhookUrl, {
        method: 'POST',
        headers,
        body: JSON.stringify(validatedPayload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`n8n webhook error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      console.log('Successfully sent lead to n8n webhook:', validatedPayload.lead.email);
      return true;
    } catch (error) {
      console.error('Failed to send lead to n8n webhook:', error);
      throw error;
    }
  }

  /**
   * Erstellt ein Lead-Payload für n8n
   */
  createLeadPayload(data: {
    email: string;
    name?: string;
    phone?: string;
    source: string;
    funnel: string;
    quizAnswers?: Record<string, any>;
    persona?: {
      type: string;
      preferences: Record<string, any>;
    };
    metadata?: Record<string, any>;
    sessionId?: string;
    userAgent?: string;
    ipAddress?: string;
  }): N8nWebhookPayload {
    return {
      lead: {
        email: data.email,
        name: data.name,
        phone: data.phone,
        source: data.source,
        funnel: data.funnel,
        quizAnswers: data.quizAnswers,
        persona: data.persona,
        metadata: data.metadata
      },
      timestamp: new Date().toISOString(),
      sessionId: data.sessionId,
      userAgent: data.userAgent,
      ipAddress: data.ipAddress
    };
  }

  /**
   * Testet die n8n Webhook-Verbindung
   */
  async testConnection(): Promise<boolean> {
    try {
      const testPayload = this.createLeadPayload({
        email: 'test@example.com',
        source: 'connection-test',
        funnel: 'test-funnel'
      });

      await this.sendLeadToN8n(testPayload);
      return true;
    } catch (error) {
      console.error('n8n webhook connection test failed:', error);
      return false;
    }
  }
}

// Singleton-Instanz für die gesamte Anwendung
let n8nServiceInstance: N8nService | null = null;

export function getN8nService(): N8nService {
  if (!n8nServiceInstance) {
    n8nServiceInstance = new N8nService();
  }
  return n8nServiceInstance;
}

// Utility-Funktion für einfache Verwendung
export async function sendLeadToN8n(leadData: {
  email: string;
  name?: string;
  phone?: string;
  source: string;
  funnel: string;
  quizAnswers?: Record<string, any>;
  persona?: {
    type: string;
    preferences: Record<string, any>;
  };
  metadata?: Record<string, any>;
  sessionId?: string;
  userAgent?: string;
  ipAddress?: string;
}): Promise<boolean> {
  const service = getN8nService();
  const payload = service.createLeadPayload(leadData);
  return service.sendLeadToN8n(payload);
} 