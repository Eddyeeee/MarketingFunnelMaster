import axios from 'axios';

export interface UpsellProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  digistoreId: string;
  digistoreUrl: string;
  commission: number; // in Prozent
  features: string[];
  bonusItems: string[];
}

export interface UpsellFlow {
  id: string;
  name: string;
  products: UpsellProduct[];
  sequence: number;
  conditions: {
    personaType?: string;
    minPurchaseAmount?: number;
    timeDelay?: number; // in Sekunden
  };
}

export class UpsellService {
  private upsellFlows: Map<string, UpsellFlow> = new Map();
  private digistoreConfig: {
    apiKey: string;
    baseUrl: string;
    webhookSecret: string;
  };

  constructor() {
    this.initializeUpsellFlows();
    this.digistoreConfig = {
      apiKey: process.env.DIGISTORE_API_KEY || '',
      baseUrl: 'https://api.digistore24.com',
      webhookSecret: process.env.DIGISTORE_WEBHOOK_SECRET || ''
    };
  }

  private initializeUpsellFlows(): void {
    // Q-Money Upsell Flow
    const qMoneyFlow: UpsellFlow = {
      id: 'qmoney_upsell',
      name: 'Q-Money Upsell Flow',
      products: [
        {
          id: 'qmoney_basic',
          name: 'Q-Money Basic',
          description: 'Der Grundkurs für Online-Geldverdienen',
          price: 297,
          currency: 'eur',
          digistoreId: 'qmoney_basic_123',
          digistoreUrl: 'https://www.digistore24.com/product/qmoney-basic',
          commission: 80, // 80% Partnerprovision
          features: [
            'Q-Money Grundkurs (Videokurs)',
            'Strategien für 500€+ monatlich',
            'Community-Zugang',
            'E-Mail-Support',
            'Bonus-Materialien'
          ],
          bonusItems: [
            'Q-Money Workbook (PDF)',
            'Strategie-Checkliste',
            'Community-Zugang',
            'E-Mail-Support'
          ]
        }
      ],
      sequence: 1,
      conditions: {
        personaType: 'all',
        timeDelay: 5 // 5 Sekunden nach Quiz-Abschluss
      }
    };

    // Cash Maximus Upsell Flow
    const cashMaximusFlow: UpsellFlow = {
      id: 'cashmaximus_upsell',
      name: 'Cash Maximus Upsell Flow',
      products: [
        {
          id: 'cashmaximus_premium',
          name: 'Cash Maximus Premium',
          description: 'Der erweiterte Kurs für 2000€+ monatlich',
          price: 597,
          currency: 'eur',
          digistoreId: 'cashmaximus_premium_456',
          digistoreUrl: 'https://www.digistore24.com/product/cashmaximus-premium',
          commission: 80, // 80% Partnerprovision
          features: [
            'Cash Maximus Premium Kurs',
            'Erweiterte Strategien',
            'VIP-Community',
            '1:1 Coaching Session',
            'Exklusive Tools',
            'Skalierungs-Strategien'
          ],
          bonusItems: [
            'Cash Maximus Workbook (PDF)',
            'VIP-Community-Zugang',
            '1:1 Coaching Session (30 Min)',
            'Exklusive Tools',
            'Skalierungs-Guide'
          ]
        }
      ],
      sequence: 2,
      conditions: {
        personaType: 'all',
        minPurchaseAmount: 297, // Nur nach Q-Money Kauf
        timeDelay: 10 // 10 Sekunden nach Q-Money Kauf
      }
    };

    this.upsellFlows.set(qMoneyFlow.id, qMoneyFlow);
    this.upsellFlows.set(cashMaximusFlow.id, cashMaximusFlow);
  }

  // Upsell Flow abrufen
  async getUpsellFlow(flowId: string): Promise<UpsellFlow | null> {
    return this.upsellFlows.get(flowId) || null;
  }

  // Alle Upsell Flows abrufen
  async getAllUpsellFlows(): Promise<UpsellFlow[]> {
    return Array.from(this.upsellFlows.values());
  }

  // Upsell Flow für Persona abrufen
  async getUpsellFlowForPersona(personaType: string, purchaseAmount: number = 0): Promise<UpsellFlow[]> {
    const flows: UpsellFlow[] = [];
    
    for (const flow of this.upsellFlows.values()) {
      const { conditions } = flow;
      
      // Prüfe Persona-Bedingung
      if (conditions.personaType && conditions.personaType !== 'all' && conditions.personaType !== personaType) {
        continue;
      }
      
      // Prüfe Mindestkaufbetrag
      if (conditions.minPurchaseAmount && purchaseAmount < conditions.minPurchaseAmount) {
        continue;
      }
      
      flows.push(flow);
    }
    
    return flows.sort((a, b) => a.sequence - b.sequence);
  }

  // Digistore24 Produkt erstellen
  async createDigistoreProduct(product: UpsellProduct): Promise<any> {
    try {
      const response = await axios.post(
        `${this.digistoreConfig.baseUrl}/products`,
        {
          name: product.name,
          description: product.description,
          price: product.price,
          currency: product.currency,
          commission: product.commission,
          features: product.features,
          bonus_items: product.bonusItems
        },
        {
          headers: {
            'Authorization': `Bearer ${this.digistoreConfig.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data;
    } catch (error) {
      console.error('Fehler beim Erstellen des Digistore24 Produkts:', error);
      throw error;
    }
  }

  // Digistore24 Verkauf registrieren
  async registerDigistoreSale(productId: string, customerData: any): Promise<any> {
    try {
      const response = await axios.post(
        `${this.digistoreConfig.baseUrl}/sales`,
        {
          product_id: productId,
          customer: customerData,
          commission: this.getProductCommission(productId)
        },
        {
          headers: {
            'Authorization': `Bearer ${this.digistoreConfig.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data;
    } catch (error) {
      console.error('Fehler beim Registrieren des Digistore24 Verkaufs:', error);
      throw error;
    }
  }

  // Produkt-Kommission abrufen
  private getProductCommission(productId: string): number {
    for (const flow of this.upsellFlows.values()) {
      const product = flow.products.find(p => p.id === productId);
      if (product) {
        return product.commission;
      }
    }
    return 0;
  }

  // Upsell-Statistiken
  async getUpsellStats(): Promise<any> {
    const stats = {
      totalFlows: this.upsellFlows.size,
      totalProducts: 0,
      totalCommission: 0,
      flows: []
    };

    for (const flow of this.upsellFlows.values()) {
      const flowStats = {
        id: flow.id,
        name: flow.name,
        products: flow.products.length,
        totalValue: flow.products.reduce((sum, p) => sum + p.price, 0),
        totalCommission: flow.products.reduce((sum, p) => sum + (p.price * p.commission / 100), 0)
      };
      
      stats.flows.push(flowStats);
      stats.totalProducts += flow.products.length;
      stats.totalCommission += flowStats.totalCommission;
    }

    return stats;
  }

  // Upsell-Tracking
  async trackUpsellEvent(eventType: string, flowId: string, productId: string, customerData: any): Promise<void> {
    const event = {
      type: eventType,
      flowId,
      productId,
      customerData,
      timestamp: new Date().toISOString()
    };

    // Hier würde normalerweise das Event in die Datenbank gespeichert
    console.log('Upsell Event:', event);
  }
}

export const upsellService = new UpsellService(); 