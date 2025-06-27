import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertLeadSchema, insertEmailFunnelSchema, insertAnalyticsSchema } from "@shared/schema";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Lead capture endpoint
  app.post("/api/leads", async (req, res) => {
    try {
      const leadData = insertLeadSchema.parse(req.body);
      const lead = await storage.createLead(leadData);
      res.json(lead);
    } catch (error) {
      res.status(400).json({ message: "Invalid lead data", error });
    }
  });

  // Get leads endpoint
  app.get("/api/leads", async (req, res) => {
    try {
      const funnel = req.query.funnel as string;
      const leads = funnel 
        ? await storage.getLeadsByFunnel(funnel)
        : await storage.getLeads();
      res.json(leads);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch leads", error });
    }
  });

  // Email funnels endpoint
  app.get("/api/email-funnels", async (req, res) => {
    try {
      const funnels = await storage.getEmailFunnels();
      res.json(funnels);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch email funnels", error });
    }
  });

  app.get("/api/email-funnels/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const funnel = await storage.getEmailFunnel(id);
      if (!funnel) {
        res.status(404).json({ message: "Email funnel not found" });
        return;
      }
      res.json(funnel);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch email funnel", error });
    }
  });

  app.post("/api/email-funnels", async (req, res) => {
    try {
      const funnelData = insertEmailFunnelSchema.parse(req.body);
      const funnel = await storage.createEmailFunnel(funnelData);
      res.json(funnel);
    } catch (error) {
      res.status(400).json({ message: "Invalid email funnel data", error });
    }
  });

  // Analytics endpoint
  app.post("/api/analytics", async (req, res) => {
    try {
      const eventData = insertAnalyticsSchema.parse(req.body);
      const event = await storage.createAnalyticsEvent(eventData);
      res.json(event);
    } catch (error) {
      res.status(400).json({ message: "Invalid analytics data", error });
    }
  });

  app.get("/api/analytics", async (req, res) => {
    try {
      const page = req.query.page as string;
      const analytics = await storage.getAnalytics(page);
      res.json(analytics);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch analytics", error });
    }
  });

  // Quiz results endpoint
  app.post("/api/quiz/results", async (req, res) => {
    try {
      const { answers, email } = req.body;
      
      // Generate personalized results based on quiz answers
      const results = generateQuizResults(answers);
      
      // If email is provided, create a lead
      if (email) {
        const leadData = {
          email,
          quizAnswers: JSON.stringify(answers),
          funnel: results.recommendedFunnel,
          source: 'quiz'
        };
        await storage.createLead(leadData);
      }
      
      res.json(results);
    } catch (error) {
      res.status(400).json({ message: "Failed to process quiz results", error });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}

function generateQuizResults(answers: Record<string, string>) {
  const profile = answers['1'];
  const time = answers['2'];
  const goal = answers['3'];
  
  // Profile mapping
  const profiles: Record<string, string> = {
    'student': 'Student/Azubi mit begrenztem Budget',
    'employee': 'Angestellte/r mit festem Einkommen',
    'parent': 'Vollzeit-Elternteil mit Familienfokus'
  };
  
  const times: Record<string, string> = {
    '15min': '15-30 Minuten täglich',
    '1hour': '1-2 Stunden täglich',
    'flexible': 'Flexible Zeiteinteilung'
  };
  
  const goals: Record<string, string> = {
    'passive': 'Passives Einkommen aufbauen',
    'freedom': 'Finanzielle Freiheit erreichen',
    'security': 'Finanzielle Sicherheit schaffen'
  };
  
  const profileText = `${profiles[profile] || 'Individueller Typ'} • ${times[time] || 'Flexible Zeit'} • ${goals[goal] || 'Finanzielle Ziele'}`;
  
  // Strategy recommendation
  let strategyText = '';
  let recommendedFunnel = '';
  
  if (profile === 'student') {
    strategyText = 'Magic Profit System - Perfekt für den Einstieg mit 0€ Startkapital';
    recommendedFunnel = 'magic-profit';
  } else if (profile === 'parent') {
    strategyText = 'Magic Profit System - Ideal für Eltern mit flexiblen Arbeitszeiten';
    recommendedFunnel = 'magic-profit';
  } else {
    strategyText = 'Money Magnet System - Optimal für Skalierung und höhere Ziele';
    recommendedFunnel = 'money-magnet';
  }
  
  return {
    profileText,
    strategyText,
    recommendedFunnel,
    nextSteps: [
      'Kostenlosen personalisierten Plan herunterladen',
      'VSL zum empfohlenen System ansehen',
      'E-Mail-Funnel mit wertvollen Tipps erhalten'
    ]
  };
}
