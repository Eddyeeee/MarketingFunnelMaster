import Stripe from 'stripe';
import { storage } from '../storage';

export interface PaymentConfig {
  secretKey: string;
  webhookSecret: string;
  currency: string;
  successUrl: string;
  cancelUrl: string;
}

export interface ProductConfig {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  personaType: string;
  features: string[];
  bonusItems: string[];
  paymentPlan: 'one-time' | 'subscription';
  subscriptionInterval?: 'month' | 'year';
}

export interface PaymentIntent {
  id: string;
  amount: number;
  currency: string;
  status: string;
  clientSecret: string;
  personaType: string;
  leadId?: number;
}

export interface PaymentData {
  amount: number;
  currency: string;
  personaType: string;
  leadId?: number;
  email: string;
  firstName?: string;
  lastName?: string;
  paymentMethod: 'card' | 'sepa' | 'sofort';
  metadata?: Record<string, string>;
}

export class PaymentService {
  private stripe: Stripe | null = null;
  private config: PaymentConfig | null = null;
  private products: Map<string, ProductConfig> = new Map();

  async initialize(config: PaymentConfig): Promise<boolean> {
    try {
      this.config = config;
      this.stripe = new Stripe(config.secretKey, {
        apiVersion: '2024-12-18.acacia',
      });

      // Initialisiere Produkte
      await this.initializeProducts();
      
      console.log('Payment-Service erfolgreich initialisiert');
      return true;
    } catch (error) {
      console.error('Payment-Service Initialisierung fehlgeschlagen:', error);
      return false;
    }
  }

  private async initializeProducts(): Promise<void> {
    const productConfigs: ProductConfig[] = [
      // STUDENT PRODUCTS
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        description: 'Perfekt für Studenten - 500€+ monatlich',
        price: 97,
        currency: 'eur',
        personaType: 'student',
        features: [
          'Magic Tool Zugang (Lifetime)',
          'Studenten-Strategien & Templates',
          'Community-Zugang (Studenten-Bereich)',
          'E-Mail-Support (24h)',
          'Mobile App Zugang',
          'Wöchentliche Updates'
        ],
        bonusItems: [
          'Studenten-Bonus-Guide (PDF)',
          'Zeitmanagement-Template (Excel)',
          '500€-Challenge (30 Tage)',
          'Study-Schedule Optimizer',
          'Studenten-Checkliste',
          'Exklusive Studenten-Strategien'
        ],
        paymentPlan: 'one-time'
      },
      {
        id: 'student_premium',
        name: 'Student Magic Tool Premium',
        description: 'Erweiterte Studenten-Version mit Coaching',
        price: 197,
        currency: 'eur',
        personaType: 'student',
        features: [
          'Magic Tool Zugang (Lifetime)',
          'Studenten-Strategien & Templates',
          'Community-Zugang (Studenten-Bereich)',
          '1:1 Coaching Session (30 Min)',
          'Prioritäts-Support (12h)',
          'Mobile App Zugang',
          'Wöchentliche Updates',
          'Exklusive Studenten-Tools'
        ],
        bonusItems: [
          'Studenten-Bonus-Guide (PDF)',
          'Zeitmanagement-Template (Excel)',
          '500€-Challenge (30 Tage)',
          'Study-Schedule Optimizer',
          'Studenten-Checkliste',
          'Exklusive Studenten-Strategien',
          'Coaching-Call (30 Min)',
          'Premium Studenten-Templates',
          '1:1 Erfolgsplanung',
          'Exklusive Studenten-Community'
        ],
        paymentPlan: 'one-time'
      },

      // EMPLOYEE PRODUCTS
      {
        id: 'employee_basic',
        name: 'Employee Magic Tool Basic',
        description: 'Für Angestellte - 2.000€+ Zusatzeinkommen',
        price: 197,
        currency: 'eur',
        personaType: 'employee',
        features: [
          'Magic Tool Zugang (Lifetime)',
          'Business-Automatisierung',
          'VIP-Community (Angestellte)',
          'E-Mail-Support (24h)',
          'Mobile App Zugang',
          'Wöchentliche Updates',
          'Business-Templates'
        ],
        bonusItems: [
          'Business-Automatisierung Guide (PDF)',
          'Zeitmanagement-System (Excel)',
          '2.000€-Challenge (60 Tage)',
          'Business-Strategien',
          'Angestellten-Checkliste',
          'Work-Life-Balance Guide'
        ],
        paymentPlan: 'one-time'
      },
      {
        id: 'employee_premium',
        name: 'Employee Magic Tool Premium',
        description: 'Erweiterte Business-Version mit Skalierung',
        price: 397,
        currency: 'eur',
        personaType: 'employee',
        features: [
          'Magic Tool Zugang (Lifetime)',
          'Business-Automatisierung',
          'VIP-Community (Angestellte)',
          '1:1 Business-Coaching (60 Min)',
          'Prioritäts-Support (12h)',
          'Skalierungs-Strategien',
          'Mobile App Zugang',
          'Wöchentliche Updates',
          'Exklusive Business-Tools'
        ],
        bonusItems: [
          'Business-Automatisierung Guide (PDF)',
          'Zeitmanagement-System (Excel)',
          '2.000€-Challenge (60 Tage)',
          'Business-Strategien',
          'Angestellten-Checkliste',
          'Work-Life-Balance Guide',
          'Business-Coaching-Call (60 Min)',
          'Skalierungs-Strategien',
          'Exklusive Business-Tools',
          '1:1 Business-Planung',
          'VIP Business-Community',
          'Exklusive Business-Templates'
        ],
        paymentPlan: 'one-time'
      },

      // PARENT PRODUCTS
      {
        id: 'parent_basic',
        name: 'Parent Magic Tool Basic',
        description: 'Für Eltern - 800-1.200€ flexibles Einkommen',
        price: 147,
        currency: 'eur',
        personaType: 'parent',
        features: [
          'Magic Tool Zugang (Lifetime)',
          'Familien-Strategien',
          'Eltern-Community',
          'E-Mail-Support (24h)',
          'Mobile App Zugang',
          'Wöchentliche Updates',
          'Familien-Templates'
        ],
        bonusItems: [
          'Familien-Strategien Guide (PDF)',
          'Flexibles Zeitmanagement (Excel)',
          '1.000€-Challenge (45 Tage)',
          'Familien-Checkliste',
          'Work-Life-Balance Guide',
          'Eltern-Strategien'
        ],
        paymentPlan: 'one-time'
      },
      {
        id: 'parent_premium',
        name: 'Parent Magic Tool Premium',
        description: 'Erweiterte Familien-Version mit Support',
        price: 297,
        currency: 'eur',
        personaType: 'parent',
        features: [
          'Magic Tool Zugang (Lifetime)',
          'Familien-Strategien',
          'Eltern-Community',
          '1:1 Familien-Coaching (45 Min)',
          'Prioritäts-Support (12h)',
          'Flexible Arbeitszeiten',
          'Mobile App Zugang',
          'Wöchentliche Updates',
          'Exklusive Familien-Tools'
        ],
        bonusItems: [
          'Familien-Strategien Guide (PDF)',
          'Flexibles Zeitmanagement (Excel)',
          '1.000€-Challenge (45 Tage)',
          'Familien-Checkliste',
          'Work-Life-Balance Guide',
          'Eltern-Strategien',
          'Familien-Coaching-Call (45 Min)',
          'Exklusive Familien-Tools',
          '1:1 Familien-Planung',
          'Premium Eltern-Community',
          'Exklusive Familien-Templates',
          'Work-Life-Balance Optimizer'
        ],
        paymentPlan: 'one-time'
      }
    ];

    for (const product of productConfigs) {
      this.products.set(product.id, product);
    }
  }

  async createPaymentIntent(paymentData: PaymentData): Promise<PaymentIntent | null> {
    if (!this.stripe || !this.config) {
      console.error('Payment-Service nicht initialisiert');
      return null;
    }

    try {
      const product = this.getProductForPersona(paymentData.personaType, paymentData.amount);
      if (!product) {
        console.error(`Kein Produkt gefunden für Persona: ${paymentData.personaType}`);
        return null;
      }

      const paymentIntent = await this.stripe.paymentIntents.create({
        amount: paymentData.amount * 100, // Stripe erwartet Cents
        currency: paymentData.currency,
        automatic_payment_methods: {
          enabled: true,
        },
        metadata: {
          personaType: paymentData.personaType,
          leadId: paymentData.leadId?.toString() || '',
          productId: product.id,
          email: paymentData.email,
          firstName: paymentData.firstName || '',
          lastName: paymentData.lastName || '',
          ...paymentData.metadata
        },
        receipt_email: paymentData.email,
        description: `${product.name} - ${product.description}`,
        statement_descriptor: 'Magic Tool',
        application_fee_amount: Math.round(paymentData.amount * 0.05 * 100), // 5% Gebühr
      });

      // Track Payment Intent
      await this.trackPaymentIntent(paymentIntent, paymentData);

      return {
        id: paymentIntent.id,
        amount: paymentData.amount,
        currency: paymentData.currency,
        status: paymentIntent.status,
        clientSecret: paymentIntent.client_secret!,
        personaType: paymentData.personaType,
        leadId: paymentData.leadId
      };
    } catch (error) {
      console.error('Payment Intent Erstellung fehlgeschlagen:', error);
      await this.trackPaymentError(paymentData, error);
      return null;
    }
  }

  async createCheckoutSession(paymentData: PaymentData): Promise<string | null> {
    if (!this.stripe || !this.config) {
      console.error('Payment-Service nicht initialisiert');
      return null;
    }

    try {
      const product = this.getProductForPersona(paymentData.personaType, paymentData.amount);
      if (!product) {
        console.error(`Kein Produkt gefunden für Persona: ${paymentData.personaType}`);
        return null;
      }

      const session = await this.stripe.checkout.sessions.create({
        payment_method_types: ['card', 'sepa_debit', 'sofort'],
        line_items: [
          {
            price_data: {
              currency: paymentData.currency,
              product_data: {
                name: product.name,
                description: product.description,
                images: ['https://example.com/magic-tool-logo.png'],
              },
              unit_amount: paymentData.amount * 100,
            },
            quantity: 1,
          },
        ],
        mode: 'payment',
        success_url: `${this.config.successUrl}?session_id={CHECKOUT_SESSION_ID}&persona=${paymentData.personaType}`,
        cancel_url: `${this.config.cancelUrl}?persona=${paymentData.personaType}`,
        customer_email: paymentData.email,
        metadata: {
          personaType: paymentData.personaType,
          leadId: paymentData.leadId?.toString() || '',
          productId: product.id,
          firstName: paymentData.firstName || '',
          lastName: paymentData.lastName || '',
          ...paymentData.metadata
        },
        payment_intent_data: {
          application_fee_amount: Math.round(paymentData.amount * 0.05 * 100),
          metadata: {
            personaType: paymentData.personaType,
            leadId: paymentData.leadId?.toString() || '',
            productId: product.id,
          },
        },
      });

      // Track Checkout Session
      await this.trackCheckoutSession(session, paymentData);

      return session.url;
    } catch (error) {
      console.error('Checkout Session Erstellung fehlgeschlagen:', error);
      await this.trackPaymentError(paymentData, error);
      return null;
    }
  }

  async handleWebhook(payload: string, signature: string): Promise<boolean> {
    if (!this.stripe || !this.config) {
      console.error('Payment-Service nicht initialisiert');
      return false;
    }

    try {
      const event = this.stripe.webhooks.constructEvent(
        payload,
        signature,
        this.config.webhookSecret
      );

      switch (event.type) {
        case 'payment_intent.succeeded':
          await this.handlePaymentSuccess(event.data.object as Stripe.PaymentIntent);
          break;
        case 'payment_intent.payment_failed':
          await this.handlePaymentFailure(event.data.object as Stripe.PaymentIntent);
          break;
        case 'checkout.session.completed':
          await this.handleCheckoutSuccess(event.data.object as Stripe.Checkout.Session);
          break;
        case 'invoice.payment_succeeded':
          await this.handleSubscriptionPayment(event.data.object as Stripe.Invoice);
          break;
        case 'customer.subscription.deleted':
          await this.handleSubscriptionCancelled(event.data.object as Stripe.Subscription);
          break;
      }

      return true;
    } catch (error) {
      console.error('Webhook-Verarbeitung fehlgeschlagen:', error);
      return false;
    }
  }

  private async handlePaymentSuccess(paymentIntent: Stripe.PaymentIntent): Promise<void> {
    const metadata = paymentIntent.metadata;
    const personaType = metadata.personaType;
    const leadId = parseInt(metadata.leadId || '0');

    // Update Lead Status
    if (leadId) {
      await storage.updateLead(leadId, {
        status: 'paid',
        paymentAmount: paymentIntent.amount / 100,
        paymentDate: new Date().toISOString(),
        paymentMethod: paymentIntent.payment_method_types?.[0] || 'unknown'
      });
    }

    // Track Payment Success
    await storage.createAnalyticsEvent({
      event: 'payment_success',
      page: '/payment',
      userId: leadId.toString(),
      data: JSON.stringify({
        paymentIntentId: paymentIntent.id,
        amount: paymentIntent.amount / 100,
        currency: paymentIntent.currency,
        personaType,
        leadId,
        timestamp: new Date().toISOString()
      })
    });

    console.log(`Zahlung erfolgreich: ${paymentIntent.id} für Persona: ${personaType}`);
  }

  private async handlePaymentFailure(paymentIntent: Stripe.PaymentIntent): Promise<void> {
    const metadata = paymentIntent.metadata;
    const personaType = metadata.personaType;
    const leadId = parseInt(metadata.leadId || '0');

    // Track Payment Failure
    await storage.createAnalyticsEvent({
      event: 'payment_failed',
      page: '/payment',
      userId: leadId.toString(),
      data: JSON.stringify({
        paymentIntentId: paymentIntent.id,
        amount: paymentIntent.amount / 100,
        currency: paymentIntent.currency,
        personaType,
        leadId,
        lastPaymentError: paymentIntent.last_payment_error?.message,
        timestamp: new Date().toISOString()
      })
    });

    console.log(`Zahlung fehlgeschlagen: ${paymentIntent.id} für Persona: ${personaType}`);
  }

  private async handleCheckoutSuccess(session: Stripe.Checkout.Session): Promise<void> {
    const metadata = session.metadata;
    const personaType = metadata?.personaType;
    const leadId = parseInt(metadata?.leadId || '0');

    // Update Lead Status
    if (leadId) {
      await storage.updateLead(leadId, {
        status: 'paid',
        paymentAmount: session.amount_total ? session.amount_total / 100 : 0,
        paymentDate: new Date().toISOString(),
        paymentMethod: 'checkout_session'
      });
    }

    // Track Checkout Success
    await storage.createAnalyticsEvent({
      event: 'checkout_success',
      page: '/checkout',
      userId: leadId.toString(),
      data: JSON.stringify({
        sessionId: session.id,
        amount: session.amount_total ? session.amount_total / 100 : 0,
        currency: session.currency,
        personaType,
        leadId,
        timestamp: new Date().toISOString()
      })
    });

    console.log(`Checkout erfolgreich: ${session.id} für Persona: ${personaType}`);
  }

  private async handleSubscriptionPayment(invoice: Stripe.Invoice): Promise<void> {
    // Handle subscription payments
    console.log(`Subscription-Zahlung: ${invoice.id}`);
  }

  private async handleSubscriptionCancelled(subscription: Stripe.Subscription): Promise<void> {
    // Handle subscription cancellations
    console.log(`Subscription gekündigt: ${subscription.id}`);
  }

  private getProductForPersona(personaType: string, amount: number): ProductConfig | null {
    for (const [id, product] of this.products) {
      if (product.personaType === personaType && product.price === amount) {
        return product;
      }
    }
    return null;
  }

  async getProductsForPersona(personaType: string): Promise<ProductConfig[]> {
    const products: ProductConfig[] = [];
    for (const [id, product] of this.products) {
      if (product.personaType === personaType) {
        products.push(product);
      }
    }
    return products.sort((a, b) => a.price - b.price);
  }

  async getPaymentStats(personaType?: string): Promise<any> {
    // Hier würden normalerweise Zahlungsstatistiken aus der Datenbank geladen
    const baseStats = {
      totalRevenue: 0,
      totalPayments: 0,
      averageOrderValue: 0,
      conversionRate: 0,
      refundRate: 0
    };

    // Simuliere Persona-spezifische Statistiken
    if (personaType) {
      switch (personaType) {
        case 'student':
          return {
            ...baseStats,
            totalRevenue: 125000,
            totalPayments: 1289,
            averageOrderValue: 97,
            conversionRate: 12.5,
            refundRate: 2.1
          };
        case 'employee':
          return {
            ...baseStats,
            totalRevenue: 175000,
            totalPayments: 890,
            averageOrderValue: 197,
            conversionRate: 15.2,
            refundRate: 1.8
          };
        case 'parent':
          return {
            ...baseStats,
            totalRevenue: 165000,
            totalPayments: 1120,
            averageOrderValue: 147,
            conversionRate: 13.8,
            refundRate: 2.3
          };
      }
    }

    return baseStats;
  }

  private async trackPaymentIntent(paymentIntent: Stripe.PaymentIntent, paymentData: PaymentData): Promise<void> {
    await storage.createAnalyticsEvent({
      event: 'payment_intent_created',
      page: '/payment',
      userId: paymentData.leadId?.toString(),
      data: JSON.stringify({
        paymentIntentId: paymentIntent.id,
        amount: paymentData.amount,
        currency: paymentData.currency,
        personaType: paymentData.personaType,
        leadId: paymentData.leadId,
        timestamp: new Date().toISOString()
      })
    });
  }

  private async trackCheckoutSession(session: Stripe.Checkout.Session, paymentData: PaymentData): Promise<void> {
    await storage.createAnalyticsEvent({
      event: 'checkout_session_created',
      page: '/checkout',
      userId: paymentData.leadId?.toString(),
      data: JSON.stringify({
        sessionId: session.id,
        amount: paymentData.amount,
        currency: paymentData.currency,
        personaType: paymentData.personaType,
        leadId: paymentData.leadId,
        timestamp: new Date().toISOString()
      })
    });
  }

  private async trackPaymentError(paymentData: PaymentData, error: any): Promise<void> {
    await storage.createAnalyticsEvent({
      event: 'payment_error',
      page: '/payment',
      userId: paymentData.leadId?.toString(),
      data: JSON.stringify({
        amount: paymentData.amount,
        currency: paymentData.currency,
        personaType: paymentData.personaType,
        leadId: paymentData.leadId,
        error: error.message,
        timestamp: new Date().toISOString()
      })
    });
  }
}

export const paymentService = new PaymentService(); 