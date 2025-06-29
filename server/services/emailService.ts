import { storage } from '../storage';
import { leads, emailFunnels } from '../../shared/schema';

export interface EmailTemplate {
  subject: string;
  body: string;
  delay: number; // Stunden nach Quiz-Abschluss
}

export interface PersonaEmailConfig {
  personaType: string;
  funnelName: string;
  templates: EmailTemplate[];
}

export class EmailService {
  private personaConfigs: PersonaEmailConfig[] = [
    {
      personaType: 'student',
      funnelName: 'magic_tool_student',
      templates: [
        {
          subject: '🎓 Dein Studenten-Plan: Erste 500€ in 30 Tagen!',
          body: `Hallo {firstName},

herzlichen Glückwunsch! Du hast den ersten Schritt zu deiner finanziellen Freiheit gemacht.

🎯 DEIN PERSONALISIERTER PLAN:
• Profil: Struggling Student Sarah
• Ziel: 500-800€ im ersten Monat
• Timeline: 30 Tage bis zum ersten Einkommen

📋 DEINE NÄCHSTEN SCHRITTE:
1. Tägliche 30-Minuten-Routine etablieren
2. Social Media Präsenz aufbauen
3. Erste Kunden innerhalb von 7 Tagen gewinnen

🚀 SOFORT STARTEN:
Klicke hier für deinen exklusiven Studenten-Zugang:
{magicToolLink}

Du erhältst:
✅ 30-Tage-Action-Plan speziell für Studenten
✅ Social Media Templates
✅ Kunden-Akquise-Strategien
✅ Community-Zugang mit anderen Studenten

Bis gleich!
Dein Magic Tool Team

P.S. Du hast 24 Stunden exklusiven Zugang zu unserem Studenten-Bonus!`,
          delay: 0
        },
        {
          subject: '⚡ Tag 3: Deine ersten Social Media Posts sind fertig!',
          body: `Hallo {firstName},

heute ist Tag 3 deines Erfolgsplans! 

📱 SOCIAL MEDIA SETUP:
Deine ersten 5 Posts sind vorbereitet und warten darauf, veröffentlicht zu werden.

🎯 HEUTE AUF DEINER AGENDA:
• Instagram-Profil optimieren
• Erste 3 Posts veröffentlichen
• 10 potenzielle Kunden identifizieren

💡 TIPP DES TAGES:
Studenten haben den Vorteil, dass sie flexibel sind. Nutze die Zeit zwischen Vorlesungen für dein Business!

Deine Magic Tool Templates:
{templateLink}

Bleib dran - die ersten 500€ sind näher als du denkst!

Dein Magic Tool Team`,
          delay: 72
        },
        {
          subject: '🎉 Tag 7: Zeit für deine ersten Kunden!',
          body: `Hallo {firstName},

eine Woche ist vergangen - Zeit für deine ersten Kunden!

🎯 WOCHENZIEL:
• 3 potenzielle Kunden kontaktiert
• 1 erste Buchung erhalten
• 50€+ verdient

📞 KUNDEN-AKQUISE STRATEGIE:
1. Schreibe 10 Freunde/Familie an
2. Poste in Facebook-Gruppen
3. Nutze dein Studenten-Netzwerk

💼 DEIN ERSTES ANGEBOT:
"Hey! Ich helfe Studenten dabei, online Geld zu verdienen. 
Interessiert? Kostenloses 15-Min-Gespräch!"

Dein Magic Tool Team

P.S. Die meisten Studenten verdienen ihre ersten 100€ in der zweiten Woche!`,
          delay: 168
        }
      ]
    },
    {
      personaType: 'employee',
      funnelName: 'magic_tool_employee',
      templates: [
        {
          subject: '💼 Dein Angestellten-Plan: 2.000€+ Zusatzeinkommen!',
          body: `Hallo {firstName},

herzlichen Glückwunsch! Du hast den Plan für deine finanzielle Unabhängigkeit gewählt.

🎯 DEIN PERSONALISIERTER PLAN:
• Profil: Burnout-Bernd
• Ziel: 2.000-3.000€ im dritten Monat
• Timeline: 90 Tage bis zur Skalierung

📋 DEINE NÄCHSTEN SCHRITTE:
1. Frühmorgens 1 Stunde investieren
2. Mittagspause für Kundenbetreuung nutzen
3. Abends für Automatisierung arbeiten

🚀 SOFORT STARTEN:
Klicke hier für deinen exklusiven Angestellten-Zugang:
{magicToolLink}

Du erhältst:
✅ 90-Tage-Skalierungsplan
✅ Automatisierungs-Tools
✅ High-Ticket-Strategien
✅ VIP-Community-Zugang

Dein Magic Tool Team

P.S. Als Angestellter hast du den Vorteil der finanziellen Sicherheit - perfekt für risikofreies Wachstum!`,
          delay: 0
        },
        {
          subject: '⚡ Tag 5: Automatisierung starten!',
          body: `Hallo {firstName},

Tag 5 - Zeit für Automatisierung!

🤖 AUTOMATISIERUNG SETUP:
Heute lernst du, wie du dein Business so automatisierst, dass es auch ohne dich läuft.

🎯 HEUTE AUF DEINER AGENDA:
• E-Mail-Automation einrichten
• Social Media Scheduler konfigurieren
• Kunden-Onboarding automatisieren

💡 TIPP DES TAGES:
Als Angestellter solltest du deine Zeit optimal nutzen. Automatisierung ist dein Schlüssel zum Erfolg!

Deine Automatisierungs-Tools:
{automationLink}

Dein Magic Tool Team`,
          delay: 120
        }
      ]
    },
    {
      personaType: 'parent',
      funnelName: 'magic_tool_parent',
      templates: [
        {
          subject: '👨‍👩‍👧‍👦 Dein Eltern-Plan: Flexibles Einkommen neben der Familie!',
          body: `Hallo {firstName},

herzlichen Glückwunsch! Du hast den perfekten Plan für Eltern gewählt.

🎯 DEIN PERSONALISIERTER PLAN:
• Profil: Overwhelmed Mom Maria
• Ziel: 800-1.200€ im ersten Monat
• Timeline: 45 Tage bis zum ersten Einkommen

📋 DEINE NÄCHSTEN SCHRITTE:
1. Morgenroutine vor der Familie etablieren
2. Abendzeit für Kundenbetreuung nutzen
3. Wochenenden für Content-Erstellung

🚀 SOFORT STARTEN:
Klicke hier für deinen exklusiven Eltern-Zugang:
{magicToolLink}

Du erhältst:
✅ Familienfreundlicher Zeitplan
✅ Flexible Arbeitsstrategien
✅ Kinder-freundliche Tools
✅ Eltern-Community

Dein Magic Tool Team

P.S. Viele Eltern verdienen ihre ersten 500€, während die Kinder in der Schule sind!`,
          delay: 0
        }
      ]
    }
  ];

  async sendWelcomeEmail(lead: any, persona: any): Promise<boolean> {
    try {
      // Finde passende E-Mail-Konfiguration
      const config = this.personaConfigs.find(c => c.personaType === persona.type);
      if (!config) {
        console.log(`No email config found for persona type: ${persona.type}`);
        return false;
      }

      // Erstelle E-Mail-Funnel falls nicht vorhanden
      const existingFunnel = await storage.getEmailFunnels().then(funnels => 
        funnels.find(f => f.name === config.funnelName)
      );

      if (!existingFunnel) {
        await storage.createEmailFunnel({
          name: config.funnelName,
          emails: JSON.stringify(config.templates)
        });
      }

      // Sende Willkommens-E-Mail (Template 0)
      const welcomeTemplate = config.templates[0];
      if (welcomeTemplate) {
        const personalizedBody = this.personalizeEmail(welcomeTemplate.body, lead, persona);
        const personalizedSubject = this.personalizeEmail(welcomeTemplate.subject, lead, persona);
        
        console.log(`Sending welcome email to ${lead.email}:`, {
          subject: personalizedSubject,
          personaType: persona.type,
          funnelName: config.funnelName
        });

        // Hier würde normalerweise der E-Mail-Versand stattfinden
        // Für jetzt loggen wir nur
        return true;
      }

      return false;
    } catch (error) {
      console.error('Error sending welcome email:', error);
      return false;
    }
  }

  async scheduleFollowUpEmails(lead: any, persona: any): Promise<void> {
    try {
      const config = this.personaConfigs.find(c => c.personaType === persona.type);
      if (!config) return;

      // Plane Follow-up E-Mails
      for (const template of config.templates.slice(1)) {
        const sendTime = new Date();
        sendTime.setHours(sendTime.getHours() + template.delay);

        console.log(`Scheduling follow-up email for ${lead.email} at ${sendTime}:`, {
          subject: template.subject,
          delay: template.delay,
          personaType: persona.type
        });

        // Hier würde normalerweise ein Job-Scheduler verwendet werden
        // Für jetzt loggen wir nur
      }
    } catch (error) {
      console.error('Error scheduling follow-up emails:', error);
    }
  }

  private personalizeEmail(template: string, lead: any, persona: any): string {
    return template
      .replace(/{firstName}/g, lead.firstName || 'Lieber Interessent')
      .replace(/{magicToolLink}/g, 'https://magictool.com/student-access')
      .replace(/{templateLink}/g, 'https://magictool.com/templates')
      .replace(/{automationLink}/g, 'https://magictool.com/automation')
      .replace(/{personaType}/g, persona.type || 'default');
  }

  async getEmailStats(leadId: number): Promise<any> {
    try {
      const lead = await storage.getLeads().then(leads => leads.find(l => l.id === leadId));
      if (!lead) return null;

      // Hier würden normalerweise E-Mail-Statistiken aus der Datenbank geladen
      return {
        leadId,
        emailsSent: 3,
        emailsOpened: 2,
        emailsClicked: 1,
        lastEmailSent: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error getting email stats:', error);
      return null;
    }
  }
}

export const emailService = new EmailService(); 