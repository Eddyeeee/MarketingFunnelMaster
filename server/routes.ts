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
  const problem = answers['2'];
  const goal = answers['3'];
  const blocker = answers['4'];
  
  // Profile mapping based on new quiz structure
  const profiles: Record<string, string> = {
    'student': 'Struggling Student Sarah - Knapper Budgetrahmen, hohe Motivation',
    'employee': 'Burnout-Bernd - Frustriert vom Hamsterrad, will ausbrechen',
    'parent': 'Overwhelmed Mom Maria - Zeitnot, familienfokussiert'
  };
  
  const problems: Record<string, string> = {
    'money_tight': 'Monatliche Geldknappheit',
    'no_time': 'Zeitmangel durch Vollzeitarbeit',
    'no_idea': 'Orientierungslosigkeit beim Start'
  };
  
  const goals: Record<string, string> = {
    'basic': '500-1.500€ Zusatzeinkommen angestrebt',
    'substantial': '2.000-5.000€ für finanzielle Unabhängigkeit',
    'freedom': '5.000€+ für komplette Freiheit'
  };
  
  const profileText = `${profiles[profile] || 'Individueller Typ'} • ${problems[problem] || 'Spezifisches Problem'} • ${goals[goal] || 'Finanzielle Ziele'}`;
  
  // Advanced strategy recommendation based on multiple factors
  let strategyText = '';
  let recommendedFunnel = '';
  
  // Students and people with no capital -> Magic Profit
  if (profile === 'student' || blocker === 'no_capital' || goal === 'basic') {
    strategyText = 'Magic Profit System - Perfekt für den Einstieg mit 0€ Startkapital. Erste Ergebnisse in 30 Tagen möglich.';
    recommendedFunnel = 'magic-profit';
  } 
  // Parents needing flexible time -> Magic Profit  
  else if (profile === 'parent' || problem === 'no_time') {
    strategyText = 'Magic Profit System - Ideal für flexible Arbeitszeiten zwischen Familie und Job. 15-30 Min täglich reichen.';
    recommendedFunnel = 'magic-profit';
  }
  // Higher earners and ambitious goals -> Money Magnet
  else if (goal === 'substantial' || goal === 'freedom' || profile === 'employee') {
    strategyText = 'Money Magnet System - Für ambitionierte Ziele und Skalierung auf 5.000€+. Multiple Einkommensströme aufbauen.';
    recommendedFunnel = 'money-magnet';
  }
  else {
    strategyText = 'Magic Profit System - Der bewährte Einstieg für alle, die ohne Risiko starten wollen.';
    recommendedFunnel = 'magic-profit';
  }
  
  // Personalized next steps based on profile
  let nextSteps = [];
  if (recommendedFunnel === 'magic-profit') {
    nextSteps = [
      'Magic Profit VSL ansehen (45 Min Investment)',
      'Kostenlosen Starter-Guide herunterladen',
      'E-Mail-Serie mit Schritt-für-Schritt Anleitung erhalten',
      'Bei Fragen: Kostenloses Beratungsgespräch buchen'
    ];
  } else {
    nextSteps = [
      'Money Magnet VSL ansehen (52 Min Investment)', 
      'Premium-Guide für Fortgeschrittene sichern',
      'Erweiterte E-Mail-Serie mit Skalierungs-Strategien',
      'Zugang zur exklusiven Money Magnet Community'
    ];
  }
  
  return {
    profileText,
    strategyText,
    recommendedFunnel,
    nextSteps
  };
}
