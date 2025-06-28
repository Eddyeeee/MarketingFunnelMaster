import express from "express";
import { z } from "zod";
import { storage } from "./storage";
import { leads, emailFunnels, analytics } from "../shared/schema";

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
    
    // 1. Erstelle Lead aus Quiz-Ergebnissen
    const lead = await storage.createLead({
      email,
      firstName: name || null,
      source: 'quiz',
      funnel: 'magic_tool',
      quizAnswers: JSON.stringify(answers)
    });

    // 2. Erfolgreiche Antwort ohne externe Services
    res.json({
      success: true,
      lead: { id: lead.id, email: lead.email },
      integrations: {
        n8n: false,
        instapage: false
      },
      message: 'Quiz-Ergebnisse erfolgreich gespeichert. Du erhältst gleich eine E-Mail von uns.'
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

export default router;

// Funktion für index.ts
export function registerRoutes(app: express.Application) {
  app.use(router);
  return app;
}
