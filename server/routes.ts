import express from "express";
import { z } from "zod";
import { storage } from "./storage";
import { leads, emailFunnels, analytics } from "../shared/schema";
import { emailService } from "./services/emailService";
import { vslService } from "./services/vslService";
import quizRoutes from './routes/quizRoutes';
import leadRoutes from './routes/leadRoutes';
import analyticsRoutes from './routes/analyticsRoutes';
import vslRoutes from './routes/vslRoutes';
import emailRoutes from './routes/emailRoutes';
import paymentRoutes from './routes/paymentRoutes';
import upsellRoutes from './routes/upsellRoutes';

const router = express.Router();

// Lead capture schema
const leadSchema = z.object({
  email: z.string().email(),
  name: z.string().optional(),
  phone: z.string().optional(),
  source: z.string().default('capture-lead'),
  funnel: z.string().optional(),
  quizAnswers: z.record(z.string()).optional(),
  persona: z.record(z.any()).optional(),
  utmSource: z.string().optional(),
  utmMedium: z.string().optional(),
  utmCampaign: z.string().optional(),
  utmTerm: z.string().optional(),
  utmContent: z.string().optional(),
  gclid: z.string().optional(),
  fbclid: z.string().optional(),
  sessionId: z.string().optional(),
  pageUrl: z.string().optional(),
  referrer: z.string().optional(),
  customFields: z.record(z.any()).optional()
});

// Standard lead capture endpoint
router.post("/api/leads", async (req, res) => {
  try {
    const leadData = leadSchema.parse(req.body);
    
    const lead = await storage.createLead({
      email: leadData.email,
      firstName: leadData.name || null,
      phone: leadData.phone || null,
      source: leadData.source,
      funnel: leadData.funnel || null,
      quizAnswers: leadData.quizAnswers ? JSON.stringify(leadData.quizAnswers) : null
    });

    res.json({
      success: true,
      lead: { id: lead.id, email: lead.email },
      message: 'Lead erfolgreich erfasst'
    });

  } catch (error) {
    console.error('Error capturing lead:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to capture lead'
    });
  }
});

// NEUER Endpunkt: /api/capture-lead - Speziell für Service-Integration optimiert
router.post("/api/capture-lead", async (req, res) => {
  try {
    const captureData = leadSchema.parse(req.body);
    
    // 1. Speichere Lead in Datenbank
    const lead = await storage.createLead({
      email: captureData.email,
      firstName: captureData.name || null,
      phone: captureData.phone || null,
      source: captureData.source,
      funnel: captureData.funnel || null,
      quizAnswers: captureData.quizAnswers ? JSON.stringify(captureData.quizAnswers) : null
    });

    // 2. Erfolgreiche Antwort ohne externe Services
    res.json({
      success: true,
      lead: { id: lead.id, email: lead.email },
      integrations: {
        n8n: false,
        instapage: false
      },
      message: 'Lead erfolgreich erfasst. Du erhältst gleich eine E-Mail von uns.'
    });

  } catch (error) {
    console.error('Error capturing lead:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to capture lead',
      integrations: {
        n8n: false,
        instapage: false
      }
    });
  }
});

// Get all leads
router.get("/api/leads", async (req, res) => {
  try {
    const allLeads = await storage.getLeads();
    res.json(allLeads);
  } catch (error) {
    console.error('Error fetching leads:', error);
    res.status(500).json({ error: 'Failed to fetch leads' });
  }
});

// Email funnels endpoints
router.get("/api/email-funnels", async (req, res) => {
  try {
    const funnels = await storage.getEmailFunnels();
    res.json(funnels);
  } catch (error) {
    console.error('Error fetching email funnels:', error);
    res.status(500).json({ error: 'Failed to fetch email funnels' });
  }
});

// E-Mail-Statistiken für einen Lead
router.get("/api/email-stats/:leadId", async (req, res) => {
  try {
    const { leadId } = req.params;
    const stats = await emailService.getEmailStats(parseInt(leadId));
    
    if (!stats) {
      return res.status(404).json({ error: 'Lead not found' });
    }
    
    res.json({
      success: true,
      stats
    });
  } catch (error) {
    console.error('Error fetching email stats:', error);
    res.status(500).json({ error: 'Failed to fetch email stats' });
  }
});

// E-Mail-Funnel für eine Persona
router.get("/api/email-funnels/persona/:personaType", async (req, res) => {
  try {
    const { personaType } = req.params;
    const funnels = await storage.getEmailFunnels();
    const personaFunnel = funnels.find(f => f.name.includes(personaType));
    
    if (!personaFunnel) {
      return res.status(404).json({ error: 'Email funnel not found for persona type' });
    }
    
    res.json({
      success: true,
      funnel: personaFunnel
    });
  } catch (error) {
    console.error('Error fetching persona email funnel:', error);
    res.status(500).json({ error: 'Failed to fetch persona email funnel' });
  }
});

router.get("/api/email-funnels/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const funnel = await storage.getEmailFunnel(parseInt(id));
    
    if (!funnel) {
      return res.status(404).json({ error: 'Email funnel not found' });
    }
    
    res.json(funnel);
  } catch (error) {
    console.error('Error fetching email funnel:', error);
    res.status(500).json({ error: 'Failed to fetch email funnel' });
  }
});

router.post("/api/email-funnels", async (req, res) => {
  try {
    const { name, description, steps } = req.body;
    const funnel = await storage.createEmailFunnel({
      name,
      emails: JSON.stringify(steps)
    });
    
    res.json(funnel);
  } catch (error) {
    console.error('Error creating email funnel:', error);
    res.status(500).json({ error: 'Failed to create email funnel' });
  }
});

// Analytics endpoint
router.post("/api/analytics", async (req, res) => {
  try {
    const { page, event, data } = req.body;
    
    await storage.createAnalyticsEvent({
      event,
      page,
      data: JSON.stringify(data)
    });
    
    res.json({ success: true });
  } catch (error) {
    console.error('Error saving analytics:', error);
    res.status(500).json({ error: 'Failed to save analytics' });
  }
});

router.get("/api/analytics", async (req, res) => {
  try {
    const analyticsData = await storage.getAnalytics();
    res.json(analyticsData);
  } catch (error) {
    console.error('Error fetching analytics:', error);
    res.status(500).json({ error: 'Failed to fetch analytics' });
  }
});

// Quiz results endpoint - ERWEITERT um n8n-Integration
router.post("/api/quiz/results", async (req, res) => {
  try {
    const { email, name, answers, persona, utmParams, sessionId, pageUrl, referrer } = req.body;
    
    // 1. Erstelle Lead aus Quiz-Ergebnissen mit erweiterten Daten
    const lead = await storage.createLead({
      email,
      firstName: name || null,
      source: 'quiz',
      funnel: persona?.recommendedFunnel || 'magic_tool',
      quizAnswers: JSON.stringify({
        answers,
        persona: {
          type: persona?.type,
          profileText: persona?.profileText,
          strategyText: persona?.strategyText,
          recommendedFunnel: persona?.recommendedFunnel,
          actionPlan: persona?.actionPlan
        },
        timestamp: new Date().toISOString()
      })
    });

    // 2. Track Quiz Completion Analytics
    await storage.createAnalyticsEvent({
      event: 'quiz_completed',
      page: pageUrl || '/quiz',
      sessionId: sessionId || undefined,
      data: JSON.stringify({
        quizId: 'magic_tool',
        personaType: persona?.type,
        recommendedFunnel: persona?.recommendedFunnel,
        answers: answers,
        leadId: lead.id
      })
    });

    // 3. Track Lead Capture Analytics
    await storage.createAnalyticsEvent({
      event: 'lead_captured',
      page: pageUrl || '/quiz',
      sessionId: sessionId || undefined,
      data: JSON.stringify({
        source: 'quiz',
        funnel: persona?.recommendedFunnel || 'magic_tool',
        personaType: persona?.type,
        leadId: lead.id
      })
    });

    // 4. Sende personalisierte Willkommens-E-Mail
    let emailSent = false;
    try {
      emailSent = await emailService.sendWelcomeEmail(lead, persona);
      
      if (emailSent) {
        // Plane Follow-up E-Mails
        await emailService.scheduleFollowUpEmails(lead, persona);
        
        // Track E-Mail-Versand
        await storage.createAnalyticsEvent({
          event: 'email_sent',
          page: pageUrl || '/quiz',
          sessionId: sessionId || undefined,
          data: JSON.stringify({
            leadId: lead.id,
            emailType: 'welcome',
            personaType: persona?.type,
            funnelName: persona?.recommendedFunnel
          })
        });
      }
    } catch (emailError) {
      console.error('Error sending welcome email:', emailError);
      // E-Mail-Fehler sollte den Quiz-Abschluss nicht blockieren
    }

    // 5. Erfolgreiche Antwort mit erweiterten Daten
    res.json({
      success: true,
      lead: { 
        id: lead.id, 
        email: lead.email,
        persona: persona?.type,
        recommendedFunnel: persona?.recommendedFunnel
      },
      persona: {
        type: persona?.type,
        profileText: persona?.profileText,
        strategyText: persona?.strategyText,
        actionPlan: persona?.actionPlan
      },
      email: {
        sent: emailSent,
        type: 'welcome',
        personaType: persona?.type
      },
      integrations: {
        n8n: false,
        instapage: false
      },
      message: 'Quiz-Ergebnisse erfolgreich gespeichert. Du erhältst gleich eine E-Mail mit deiner personalisierten Strategie.'
    });

  } catch (error) {
    console.error('Error saving quiz results:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to save quiz results',
      integrations: {
        n8n: false,
        instapage: false
      }
    });
  }
});

// Quiz questions endpoint
router.get("/api/quizzes/:id", async (req, res) => {
  try {
    const { id } = req.params;
    
    // Für jetzt geben wir immer die gleichen Fragen zurück
    // In Zukunft können wir verschiedene Quiz-Typen basierend auf der ID unterstützen
    const quizQuestions = [
      {
        id: "1",
        question: "Welches Profil beschreibt dich am besten?",
        options: [
          {
            value: "student",
            label: "Student/Studentin",
            description: "Ich studiere noch und suche nach einem Nebenverdienst"
          },
          {
            value: "employee",
            label: "Angestellter/Angestellte",
            description: "Ich arbeite Vollzeit und möchte mein Einkommen aufstocken"
          },
          {
            value: "parent",
            label: "Elternteil",
            description: "Ich kümmere mich um die Familie und suche flexible Einkommensmöglichkeiten"
          }
        ]
      },
      {
        id: "2",
        question: "Was ist dein größtes finanzielles Problem?",
        options: [
          {
            value: "money_tight",
            label: "Geld ist jeden Monat knapp",
            description: "Ich komme kaum über die Runden"
          },
          {
            value: "no_time",
            label: "Ich habe keine Zeit für einen Nebenjob",
            description: "Mein Hauptjob nimmt mich voll in Anspruch"
          },
          {
            value: "no_idea",
            label: "Ich weiß nicht, wo ich anfangen soll",
            description: "Es gibt so viele Möglichkeiten, dass ich überfordert bin"
          }
        ]
      },
      {
        id: "3",
        question: "Wie viel zusätzliches Einkommen möchtest du erreichen?",
        options: [
          {
            value: "basic",
            label: "500-1.500€ monatlich",
            description: "Für ein bisschen mehr finanziellen Spielraum"
          },
          {
            value: "substantial",
            label: "2.000-5.000€ monatlich",
            description: "Für finanzielle Unabhängigkeit"
          },
          {
            value: "freedom",
            label: "5.000€+ monatlich",
            description: "Für komplette finanzielle Freiheit"
          }
        ]
      },
      {
        id: "4",
        question: "Was hält dich am meisten zurück?",
        options: [
          {
            value: "no_capital",
            label: "Ich habe kein Startkapital",
            description: "Ich kann nicht viel investieren"
          },
          {
            value: "no_skills",
            label: "Ich habe nicht die richtigen Fähigkeiten",
            description: "Ich weiß nicht, was ich gut kann"
          },
          {
            value: "no_network",
            label: "Ich habe keine Kontakte",
            description: "Ich kenne niemanden in der Branche"
          }
        ]
      }
    ];

    res.json({
      success: true,
      quiz: {
        id: id,
        title: "Finde heraus, welcher Geld-Typ du bist!",
        description: "Beantworte 4 kurze Fragen und erhalte deine personalisierte Strategie für finanziellen Erfolg.",
        questions: quizQuestions
      }
    });

  } catch (error) {
    console.error('Error fetching quiz questions:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch quiz questions'
    });
  }
});

// VSL-API-Routen
router.get("/api/vsl/:personaType", async (req, res) => {
  try {
    const { personaType } = req.params;
    const { leadId } = req.query;
    
    // Lade Lead-Daten falls Lead-ID vorhanden
    let leadData = null;
    if (leadId) {
      const leads = await storage.getLeads();
      leadData = leads.find(l => l.id === parseInt(leadId as string));
    }
    
    // Generiere personabasiert VSL
    const vslConfig = await vslService.generateVSL(personaType, leadData);
    
    // Track VSL-View
    await vslService.trackVSLView(personaType, leadId ? parseInt(leadId as string) : undefined);
    
    res.json({
      success: true,
      vsl: vslConfig
    });
  } catch (error) {
    console.error('Error generating VSL:', error);
    res.status(500).json({ error: 'Failed to generate VSL' });
  }
});

// VSL-Statistiken
router.get("/api/vsl/stats/:personaType", async (req, res) => {
  try {
    const { personaType } = req.params;
    const stats = await vslService.getVSLStats(personaType);
    
    res.json({
      success: true,
      stats
    });
  } catch (error) {
    console.error('Error fetching VSL stats:', error);
    res.status(500).json({ error: 'Failed to fetch VSL stats' });
  }
});

// VSL-Conversion tracken
router.post("/api/vsl/conversion", async (req, res) => {
  try {
    const { personaType, leadId, amount } = req.body;
    
    // Track Conversion
    await vslService.trackVSLConversion(personaType, leadId, amount);
    
    res.json({
      success: true,
      message: 'Conversion tracked successfully'
    });
  } catch (error) {
    console.error('Error tracking VSL conversion:', error);
    res.status(500).json({ error: 'Failed to track conversion' });
  }
});

// A/B-Testing für VSL-Varianten
router.get("/api/vsl/ab-test/:personaType", async (req, res) => {
  try {
    const { personaType } = req.params;
    const { variant } = req.query;
    
    // Generiere VSL mit A/B-Test-Variante
    const vslConfig = await vslService.generateVSL(personaType);
    
    // Hier würde normalerweise A/B-Test-Logik implementiert
    const testVariant = variant || 'A';
    
    res.json({
      success: true,
      vsl: vslConfig,
      variant: testVariant,
      testId: `vsl_${personaType}_${testVariant}`
    });
  } catch (error) {
    console.error('Error generating A/B test VSL:', error);
    res.status(500).json({ error: 'Failed to generate A/B test VSL' });
  }
});

// API-Routen
router.use('/api/quizzes', quizRoutes);
router.use('/api/leads', leadRoutes);
router.use('/api/analytics', analyticsRoutes);
router.use('/api/vsl', vslRoutes);
router.use('/api/email', emailRoutes);
router.use('/api/payment', paymentRoutes);
router.use('/api/upsell', upsellRoutes);

// Health Check
router.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    services: {
      quiz: 'active',
      lead: 'active',
      analytics: 'active',
      vsl: 'active',
      email: 'active',
      payment: 'active',
      upsell: 'active'
    }
  });
});

export default router;

// Funktion für index.ts
export function registerRoutes(app: express.Application) {
  app.use(router);
  return app;
}
