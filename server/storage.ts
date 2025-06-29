import { 
  leads, 
  emailFunnels, 
  analytics, 
  upsellFlows,
  upsellProducts,
  upsellEvents,
  digistoreSales,
  type Lead, 
  type InsertLead, 
  type EmailFunnel, 
  type InsertEmailFunnel, 
  type Analytics, 
  type InsertAnalytics,
  type UpsellFlow,
  type InsertUpsellFlow,
  type UpsellProduct,
  type InsertUpsellProduct,
  type UpsellEvent,
  type InsertUpsellEvent,
  type DigistoreSale,
  type InsertDigistoreSale,
  users, 
  type User, 
  type InsertUser 
} from "@shared/schema";

export interface IStorage {
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  createLead(lead: InsertLead): Promise<Lead>;
  getLeads(): Promise<Lead[]>;
  getLeadsByFunnel(funnel: string): Promise<Lead[]>;
  createEmailFunnel(funnel: InsertEmailFunnel): Promise<EmailFunnel>;
  getEmailFunnels(): Promise<EmailFunnel[]>;
  getEmailFunnel(id: number): Promise<EmailFunnel | undefined>;
  createAnalyticsEvent(event: InsertAnalytics): Promise<Analytics>;
  getAnalytics(page?: string): Promise<Analytics[]>;
  // Upsell Methods
  createUpsellFlow(flow: InsertUpsellFlow): Promise<UpsellFlow>;
  getUpsellFlows(): Promise<UpsellFlow[]>;
  getUpsellFlow(flowId: string): Promise<UpsellFlow | undefined>;
  createUpsellProduct(product: InsertUpsellProduct): Promise<UpsellProduct>;
  getUpsellProducts(): Promise<UpsellProduct[]>;
  getUpsellProductsByFlow(flowId: string): Promise<UpsellProduct[]>;
  createUpsellEvent(event: InsertUpsellEvent): Promise<UpsellEvent>;
  getUpsellEvents(): Promise<UpsellEvent[]>;
  getUpsellEventsByFlow(flowId: string): Promise<UpsellEvent[]>;
  createDigistoreSale(sale: InsertDigistoreSale): Promise<DigistoreSale>;
  getDigistoreSales(): Promise<DigistoreSale[]>;
  getAnalyticsEvents(): Promise<Analytics[]>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private leads: Map<number, Lead>;
  private emailFunnels: Map<number, EmailFunnel>;
  private analytics: Map<number, Analytics>;
  private upsellFlows: Map<number, UpsellFlow>;
  private upsellProducts: Map<number, UpsellProduct>;
  private upsellEvents: Map<number, UpsellEvent>;
  private digistoreSales: Map<number, DigistoreSale>;
  private currentUserId: number;
  private currentLeadId: number;
  private currentFunnelId: number;
  private currentAnalyticsId: number;
  private currentUpsellFlowId: number;
  private currentUpsellProductId: number;
  private currentUpsellEventId: number;
  private currentDigistoreSaleId: number;

  constructor() {
    this.users = new Map();
    this.leads = new Map();
    this.emailFunnels = new Map();
    this.analytics = new Map();
    this.upsellFlows = new Map();
    this.upsellProducts = new Map();
    this.upsellEvents = new Map();
    this.digistoreSales = new Map();
    this.currentUserId = 1;
    this.currentLeadId = 1;
    this.currentFunnelId = 1;
    this.currentAnalyticsId = 1;
    this.currentUpsellFlowId = 1;
    this.currentUpsellProductId = 1;
    this.currentUpsellEventId = 1;
    this.currentDigistoreSaleId = 1;

    // Initialize with sample data
    this.initializeEmailFunnels();
    this.initializeUpsellFlows();
  }

  private initializeEmailFunnels() {
    const funnel1: EmailFunnel = {
      id: 1,
      name: "Magic Profit Funnel",
      emails: JSON.stringify([
        {
          subject: "Willkommen bei Magic Profit - Dein Start in die finanzielle Freiheit",
          body: "Hallo {firstName},\n\nwillkommen bei Magic Profit! Du hast den ersten Schritt zu deiner finanziellen Freiheit gemacht...",
          delay: 0
        },
        {
          subject: "Die 3 größten Fehler beim Geld verdienen (und wie du sie vermeidest)",
          body: "Hallo {firstName},\n\ndie meisten Menschen machen diese 3 kritischen Fehler...",
          delay: 24
        },
        {
          subject: "Warum 90% der Menschen niemals finanziell frei werden",
          body: "Hallo {firstName},\n\nstatistisch gesehen werden 90% der Menschen niemals finanziell frei...",
          delay: 72
        }
      ]),
      createdAt: new Date()
    };

    const funnel2: EmailFunnel = {
      id: 2,
      name: "Money Magnet Funnel",
      emails: JSON.stringify([
        {
          subject: "Money Magnet System - Deine Reise zu 5.000€+ beginnt jetzt",
          body: "Hallo {firstName},\n\nherzlichen Glückwunsch zu deiner Entscheidung für das Money Magnet System...",
          delay: 0
        },
        {
          subject: "Das Geheimnis der Reichen: Multiple Einkommensströme",
          body: "Hallo {firstName},\n\nreiche Menschen haben im Durchschnitt 7 verschiedene Einkommensquellen...",
          delay: 24
        },
        {
          subject: "Automatisierung: Wie du im Schlaf Geld verdienst",
          body: "Hallo {firstName},\n\nstell dir vor, du wachst auf und hast über Nacht 200€ verdient...",
          delay: 48
        }
      ]),
      createdAt: new Date()
    };

    this.emailFunnels.set(1, funnel1);
    this.emailFunnels.set(2, funnel2);
    this.currentFunnelId = 3;
  }

  private initializeUpsellFlows() {
    // Q-Money Upsell Flow
    const qmoneyFlow: UpsellFlow = {
      id: 1,
      flowId: 'qmoney_upsell',
      name: 'Q-Money Upsell Flow',
      description: 'Der Grundkurs für Online-Geldverdienen',
      sequence: 1,
      conditions: JSON.stringify({
        personaType: 'all',
        timeDelay: 5
      }),
      isActive: 'true',
      createdAt: new Date()
    };

    // Cash Maximus Upsell Flow
    const cashMaximusFlow: UpsellFlow = {
      id: 2,
      flowId: 'cashmaximus_upsell',
      name: 'Cash Maximus Upsell Flow',
      description: 'Der erweiterte Kurs für 2000€+ monatlich',
      sequence: 2,
      conditions: JSON.stringify({
        personaType: 'all',
        minPurchaseAmount: 297,
        timeDelay: 10
      }),
      isActive: 'true',
      createdAt: new Date()
    };

    this.upsellFlows.set(1, qmoneyFlow);
    this.upsellFlows.set(2, cashMaximusFlow);
    this.currentUpsellFlowId = 3;

    // Q-Money Product
    const qmoneyProduct: UpsellProduct = {
      id: 1,
      productId: 'qmoney_basic',
      flowId: 'qmoney_upsell',
      name: 'Q-Money Basic',
      description: 'Der Grundkurs für Online-Geldverdienen',
      price: 29700, // 297€ in Cent
      currency: 'eur',
      digistoreId: 'qmoney_basic_123',
      digistoreUrl: 'https://www.digistore24.com/product/qmoney-basic',
      commission: 80,
      features: JSON.stringify([
        'Q-Money Grundkurs (Videokurs)',
        'Strategien für 500€+ monatlich',
        'Community-Zugang',
        'E-Mail-Support',
        'Bonus-Materialien'
      ]),
      bonusItems: JSON.stringify([
        'Q-Money Workbook (PDF)',
        'Strategie-Checkliste',
        'Community-Zugang',
        'E-Mail-Support'
      ]),
      isActive: 'true',
      createdAt: new Date()
    };

    // Cash Maximus Product
    const cashMaximusProduct: UpsellProduct = {
      id: 2,
      productId: 'cashmaximus_premium',
      flowId: 'cashmaximus_upsell',
      name: 'Cash Maximus Premium',
      description: 'Der erweiterte Kurs für 2000€+ monatlich',
      price: 59700, // 597€ in Cent
      currency: 'eur',
      digistoreId: 'cashmaximus_premium_456',
      digistoreUrl: 'https://www.digistore24.com/product/cashmaximus-premium',
      commission: 80,
      features: JSON.stringify([
        'Cash Maximus Premium Kurs',
        'Erweiterte Strategien',
        'VIP-Community',
        '1:1 Coaching Session',
        'Exklusive Tools',
        'Skalierungs-Strategien'
      ]),
      bonusItems: JSON.stringify([
        'Cash Maximus Workbook (PDF)',
        'VIP-Community-Zugang',
        '1:1 Coaching Session (30 Min)',
        'Exklusive Tools',
        'Skalierungs-Guide'
      ]),
      isActive: 'true',
      createdAt: new Date()
    };

    this.upsellProducts.set(1, qmoneyProduct);
    this.upsellProducts.set(2, cashMaximusProduct);
    this.currentUpsellProductId = 3;
  }

  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentUserId++;
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  async createLead(insertLead: InsertLead): Promise<Lead> {
    const id = this.currentLeadId++;
    const lead: Lead = { 
      ...insertLead,
      id,
      source: insertLead.source || null,
      firstName: insertLead.firstName || null,
      lastName: insertLead.lastName || null,
      phone: insertLead.phone || null,
      quizAnswers: insertLead.quizAnswers || null,
      funnel: insertLead.funnel || null,
      createdAt: new Date()
    };
    this.leads.set(id, lead);
    return lead;
  }

  async getLeads(): Promise<Lead[]> {
    return Array.from(this.leads.values());
  }

  async getLeadsByFunnel(funnel: string): Promise<Lead[]> {
    return Array.from(this.leads.values()).filter(lead => lead.funnel === funnel);
  }

  async createEmailFunnel(insertFunnel: InsertEmailFunnel): Promise<EmailFunnel> {
    const id = this.currentFunnelId++;
    const funnel: EmailFunnel = {
      ...insertFunnel,
      id,
      createdAt: new Date()
    };
    this.emailFunnels.set(id, funnel);
    return funnel;
  }

  async getEmailFunnels(): Promise<EmailFunnel[]> {
    return Array.from(this.emailFunnels.values());
  }

  async getEmailFunnel(id: number): Promise<EmailFunnel | undefined> {
    return this.emailFunnels.get(id);
  }

  async createAnalyticsEvent(insertEvent: InsertAnalytics): Promise<Analytics> {
    const id = this.currentAnalyticsId++;
    const event: Analytics = {
      ...insertEvent,
      id,
      page: insertEvent.page || null,
      userId: insertEvent.userId || null,
      sessionId: insertEvent.sessionId || null,
      data: insertEvent.data || null,
      createdAt: new Date()
    };
    this.analytics.set(id, event);
    return event;
  }

  async getAnalytics(page?: string): Promise<Analytics[]> {
    const allEvents = Array.from(this.analytics.values());
    if (page) {
      return allEvents.filter(event => event.page === page);
    }
    return allEvents;
  }

  // Upsell Methods
  async createUpsellFlow(flow: InsertUpsellFlow): Promise<UpsellFlow> {
    const id = this.currentUpsellFlowId++;
    const upsellFlow: UpsellFlow = {
      ...flow,
      id,
      createdAt: new Date()
    };
    this.upsellFlows.set(id, upsellFlow);
    return upsellFlow;
  }

  async getUpsellFlows(): Promise<UpsellFlow[]> {
    return Array.from(this.upsellFlows.values());
  }

  async getUpsellFlow(flowId: string): Promise<UpsellFlow | undefined> {
    return Array.from(this.upsellFlows.values()).find(flow => flow.flowId === flowId);
  }

  async createUpsellProduct(product: InsertUpsellProduct): Promise<UpsellProduct> {
    const id = this.currentUpsellProductId++;
    const upsellProduct: UpsellProduct = {
      ...product,
      id,
      createdAt: new Date()
    };
    this.upsellProducts.set(id, upsellProduct);
    return upsellProduct;
  }

  async getUpsellProducts(): Promise<UpsellProduct[]> {
    return Array.from(this.upsellProducts.values());
  }

  async getUpsellProductsByFlow(flowId: string): Promise<UpsellProduct[]> {
    return Array.from(this.upsellProducts.values()).filter(product => product.flowId === flowId);
  }

  async createUpsellEvent(event: InsertUpsellEvent): Promise<UpsellEvent> {
    const id = this.currentUpsellEventId++;
    const upsellEvent: UpsellEvent = {
      ...event,
      id,
      leadId: event.leadId || null,
      sessionId: event.sessionId || null,
      personaType: event.personaType || null,
      amount: event.amount || null,
      commission: event.commission || null,
      customerData: event.customerData || null,
      createdAt: new Date()
    };
    this.upsellEvents.set(id, upsellEvent);
    return upsellEvent;
  }

  async getUpsellEvents(): Promise<UpsellEvent[]> {
    return Array.from(this.upsellEvents.values());
  }

  async getUpsellEventsByFlow(flowId: string): Promise<UpsellEvent[]> {
    return Array.from(this.upsellEvents.values()).filter(event => event.flowId === flowId);
  }

  async createDigistoreSale(sale: InsertDigistoreSale): Promise<DigistoreSale> {
    const id = this.currentDigistoreSaleId++;
    const digistoreSale: DigistoreSale = {
      ...sale,
      id,
      leadId: sale.leadId || null,
      currency: sale.currency || 'eur',
      digistoreTransactionId: sale.digistoreTransactionId || null,
      customerData: sale.customerData || null,
      status: sale.status || 'completed',
      createdAt: new Date()
    };
    this.digistoreSales.set(id, digistoreSale);
    return digistoreSale;
  }

  async getDigistoreSales(): Promise<DigistoreSale[]> {
    return Array.from(this.digistoreSales.values());
  }

  async getAnalyticsEvents(): Promise<Analytics[]> {
    return Array.from(this.analytics.values());
  }
}

export const storage = new MemStorage();
