import { Router } from 'express';
import { paymentService, PaymentConfig, PaymentData } from '../services/paymentService';
import { storage } from '../storage';

const router = Router();

// Payment-Service initialisieren
router.post('/initialize', async (req, res) => {
  try {
    const config: PaymentConfig = req.body;
    const success = await paymentService.initialize(config);
    
    if (success) {
      res.json({ success: true, message: 'Payment-Service erfolgreich konfiguriert' });
    } else {
      res.status(500).json({ success: false, message: 'Payment-Service-Konfiguration fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Payment-Service-Initialisierung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Payment Intent erstellen
router.post('/create-payment-intent', async (req, res) => {
  try {
    const paymentData: PaymentData = req.body;
    const paymentIntent = await paymentService.createPaymentIntent(paymentData);
    
    if (paymentIntent) {
      res.json({ success: true, paymentIntent });
    } else {
      res.status(500).json({ success: false, message: 'Payment Intent Erstellung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Payment Intent Erstellung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Checkout Session erstellen
router.post('/create-checkout-session', async (req, res) => {
  try {
    const paymentData: PaymentData = req.body;
    const checkoutUrl = await paymentService.createCheckoutSession(paymentData);
    
    if (checkoutUrl) {
      res.json({ success: true, checkoutUrl });
    } else {
      res.status(500).json({ success: false, message: 'Checkout Session Erstellung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Checkout Session Erstellung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Produkte für Persona abrufen
router.get('/products/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    const products = await paymentService.getProductsForPersona(personaType);
    
    res.json({ success: true, products });
  } catch (error) {
    console.error('Produkt-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Zahlungsstatistiken abrufen
router.get('/stats/:personaType?', async (req, res) => {
  try {
    const { personaType } = req.params;
    const stats = await paymentService.getPaymentStats(personaType);
    
    res.json({ success: true, stats });
  } catch (error) {
    console.error('Zahlungsstatistiken Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Stripe Webhook verarbeiten
router.post('/webhook', async (req, res) => {
  try {
    const signature = req.headers['stripe-signature'] as string;
    const payload = req.body;
    
    const success = await paymentService.handleWebhook(payload, signature);
    
    if (success) {
      res.json({ success: true });
    } else {
      res.status(400).json({ success: false, message: 'Webhook-Verarbeitung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Webhook-Verarbeitung Fehler:', error);
    res.status(400).json({ success: false, message: 'Webhook-Fehler' });
  }
});

// Zahlungsstatus abrufen
router.get('/status/:paymentIntentId', async (req, res) => {
  try {
    const { paymentIntentId } = req.params;
    
    // Hier würde normalerweise der Zahlungsstatus von Stripe abgerufen
    const status = {
      id: paymentIntentId,
      status: 'succeeded',
      amount: 19700,
      currency: 'eur',
      created: new Date().toISOString(),
      metadata: {
        personaType: 'student',
        leadId: '123'
      }
    };
    
    res.json({ success: true, status });
  } catch (error) {
    console.error('Zahlungsstatus-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Refund erstellen
router.post('/refund', async (req, res) => {
  try {
    const { paymentIntentId, amount, reason } = req.body;
    
    // Hier würde normalerweise ein Refund über Stripe erstellt
    console.log(`Refund für ${paymentIntentId}: ${amount} - Grund: ${reason}`);
    
    res.json({ success: true, message: 'Refund erfolgreich erstellt' });
  } catch (error) {
    console.error('Refund-Erstellung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Zahlungsmethoden abrufen
router.get('/payment-methods', async (req, res) => {
  try {
    const paymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      },
      {
        id: 'sepa',
        name: 'SEPA-Lastschrift',
        description: 'Direkte Abbuchung vom Konto',
        icon: '🏦',
        enabled: true
      },
      {
        id: 'sofort',
        name: 'Sofortüberweisung',
        description: 'Sofortige Überweisung',
        icon: '⚡',
        enabled: true
      }
    ];
    
    res.json({ success: true, paymentMethods });
  } catch (error) {
    console.error('Zahlungsmethoden-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Zahlungsplan erstellen
router.post('/create-payment-plan', async (req, res) => {
  try {
    const { personaType, leadId, planType } = req.body;
    
    // Lead-Daten abrufen
    const lead = await storage.getLead(leadId);
    if (!lead) {
      return res.status(404).json({ success: false, message: 'Lead nicht gefunden' });
    }
    
    // Zahlungsplan basierend auf Persona und Plan-Typ
    const plans = {
      student: {
        basic: { amount: 97, installments: 1, interval: 'month' },
        premium: { amount: 197, installments: 1, interval: 'month' }
      },
      employee: {
        basic: { amount: 197, installments: 1, interval: 'month' },
        premium: { amount: 397, installments: 1, interval: 'month' }
      },
      parent: {
        basic: { amount: 147, installments: 1, interval: 'month' },
        premium: { amount: 297, installments: 1, interval: 'month' }
      }
    };
    
    const plan = plans[personaType]?.[planType];
    if (!plan) {
      return res.status(400).json({ success: false, message: 'Ungültiger Plan-Typ' });
    }
    
    // Payment Intent für Plan erstellen
    const paymentData: PaymentData = {
      amount: plan.amount,
      currency: 'eur',
      personaType,
      leadId,
      email: lead.email,
      firstName: lead.firstName,
      lastName: lead.lastName,
      paymentMethod: 'card',
      metadata: {
        planType,
        installments: plan.installments.toString(),
        interval: plan.interval
      }
    };
    
    const paymentIntent = await paymentService.createPaymentIntent(paymentData);
    
    if (paymentIntent) {
      res.json({ success: true, paymentIntent, plan });
    } else {
      res.status(500).json({ success: false, message: 'Zahlungsplan-Erstellung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Zahlungsplan-Erstellung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Zahlungshistorie abrufen
router.get('/history/:leadId', async (req, res) => {
  try {
    const { leadId } = req.params;
    
    // Hier würde normalerweise die Zahlungshistorie aus der Datenbank geladen
    const history = [
      {
        id: 'pi_1234567890',
        amount: 19700,
        currency: 'eur',
        status: 'succeeded',
        date: new Date().toISOString(),
        method: 'card',
        description: 'Student Magic Tool Premium'
      }
    ];
    
    res.json({ success: true, history });
  } catch (error) {
    console.error('Zahlungshistorie-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Zahlungsabschluss bestätigen
router.post('/confirm', async (req, res) => {
  try {
    const { paymentIntentId, leadId } = req.body;
    
    // Lead-Status auf "paid" setzen
    if (leadId) {
      await storage.updateLead(leadId, {
        status: 'paid',
        paymentDate: new Date().toISOString(),
        paymentMethod: 'stripe'
      });
    }
    
    // Erfolgs-Event tracken
    await storage.createAnalyticsEvent({
      event: 'payment_confirmed',
      page: '/payment',
      userId: leadId?.toString(),
      data: JSON.stringify({
        paymentIntentId,
        leadId,
        timestamp: new Date().toISOString()
      })
    });
    
    res.json({ success: true, message: 'Zahlung erfolgreich bestätigt' });
  } catch (error) {
    console.error('Zahlungsbestätigung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Zahlungsfehler behandeln
router.post('/error', async (req, res) => {
  try {
    const { paymentIntentId, leadId, error } = req.body;
    
    // Fehler-Event tracken
    await storage.createAnalyticsEvent({
      event: 'payment_error',
      page: '/payment',
      userId: leadId?.toString(),
      data: JSON.stringify({
        paymentIntentId,
        leadId,
        error,
        timestamp: new Date().toISOString()
      })
    });
    
    res.json({ success: true, message: 'Zahlungsfehler protokolliert' });
  } catch (error) {
    console.error('Zahlungsfehler-Behandlung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

export default router; 