import { leads, emailFunnels, analytics, type Lead, type InsertLead, type EmailFunnel, type InsertEmailFunnel, type Analytics, type InsertAnalytics, users, type User, type InsertUser } from "@shared/schema";

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
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private leads: Map<number, Lead>;
  private emailFunnels: Map<number, EmailFunnel>;
  private analytics: Map<number, Analytics>;
  private currentUserId: number;
  private currentLeadId: number;
  private currentFunnelId: number;
  private currentAnalyticsId: number;

  constructor() {
    this.users = new Map();
    this.leads = new Map();
    this.emailFunnels = new Map();
    this.analytics = new Map();
    this.currentUserId = 1;
    this.currentLeadId = 1;
    this.currentFunnelId = 1;
    this.currentAnalyticsId = 1;

    // Initialize with sample email funnels
    this.initializeEmailFunnels();
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
}

export const storage = new MemStorage();
