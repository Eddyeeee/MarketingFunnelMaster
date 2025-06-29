import nodemailer from 'nodemailer';
import { storage } from '../storage';

export interface EmailConfig {
  provider: 'gmail' | 'sendgrid' | 'mailgun' | 'custom';
  host?: string;
  port?: number;
  secure?: boolean;
  auth: {
    user: string;
    pass: string;
  };
  from: string;
  fromName: string;
}

export interface EmailTemplate {
  subject: string;
  html: string;
  text: string;
  variables: string[];
}

export interface EmailData {
  to: string;
  subject: string;
  html: string;
  text: string;
  personaType: string;
  leadId?: number;
  templateId?: string;
}

export class SMTPService {
  private transporter: nodemailer.Transporter | null = null;
  private config: EmailConfig | null = null;

  async initialize(config: EmailConfig): Promise<boolean> {
    try {
      this.config = config;
      
      // Konfiguriere Transporter basierend auf Provider
      switch (config.provider) {
        case 'gmail':
          this.transporter = nodemailer.createTransporter({
            service: 'gmail',
            auth: config.auth
          });
          break;
          
        case 'sendgrid':
          this.transporter = nodemailer.createTransporter({
            host: 'smtp.sendgrid.net',
            port: 587,
            secure: false,
            auth: config.auth
          });
          break;
          
        case 'mailgun':
          this.transporter = nodemailer.createTransporter({
            host: 'smtp.mailgun.org',
            port: 587,
            secure: false,
            auth: config.auth
          });
          break;
          
        case 'custom':
          this.transporter = nodemailer.createTransporter({
            host: config.host,
            port: config.port,
            secure: config.secure,
            auth: config.auth
          });
          break;
      }

      // Teste Verbindung
      await this.transporter.verify();
      console.log('SMTP-Verbindung erfolgreich hergestellt');
      return true;
    } catch (error) {
      console.error('SMTP-Verbindung fehlgeschlagen:', error);
      return false;
    }
  }

  async sendEmail(emailData: EmailData): Promise<boolean> {
    if (!this.transporter || !this.config) {
      console.error('SMTP nicht initialisiert');
      return false;
    }

    try {
      const mailOptions = {
        from: `"${this.config.fromName}" <${this.config.from}>`,
        to: emailData.to,
        subject: emailData.subject,
        html: emailData.html,
        text: emailData.text,
        headers: {
          'X-Persona-Type': emailData.personaType,
          'X-Lead-ID': emailData.leadId?.toString() || '',
          'X-Template-ID': emailData.templateId || ''
        }
      };

      const result = await this.transporter.sendMail(mailOptions);
      
      // Track E-Mail-Versendung
      await this.trackEmailSent(emailData, result.messageId);
      
      console.log(`E-Mail erfolgreich gesendet: ${result.messageId}`);
      return true;
    } catch (error) {
      console.error('E-Mail-Versendung fehlgeschlagen:', error);
      await this.trackEmailError(emailData, error);
      return false;
    }
  }

  async sendBulkEmails(emails: EmailData[]): Promise<{ success: number; failed: number }> {
    let success = 0;
    let failed = 0;

    for (const email of emails) {
      const result = await this.sendEmail(email);
      if (result) {
        success++;
      } else {
        failed++;
      }
      
      // Rate Limiting für Bulk-Versendung
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    return { success, failed };
  }

  async sendPersonaEmail(personaType: string, leadData: any, templateId: string): Promise<boolean> {
    const template = await this.getPersonaTemplate(personaType, templateId);
    if (!template) {
      console.error(`Template nicht gefunden: ${templateId}`);
      return false;
    }

    const personalizedHtml = this.personalizeTemplate(template.html, leadData, personaType);
    const personalizedText = this.personalizeTemplate(template.text, leadData, personaType);
    const personalizedSubject = this.personalizeTemplate(template.subject, leadData, personaType);

    const emailData: EmailData = {
      to: leadData.email,
      subject: personalizedSubject,
      html: personalizedHtml,
      text: personalizedText,
      personaType,
      leadId: leadData.id,
      templateId
    };

    return await this.sendEmail(emailData);
  }

  private async getPersonaTemplate(personaType: string, templateId: string): Promise<EmailTemplate | null> {
    // Hier würden normalerweise Templates aus der Datenbank geladen
    const templates = {
      // STUDENT TEMPLATES
      'student_welcome': {
        subject: '🎓 Willkommen im Studenten-Programm, {firstName}!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #3b82f6;">🎓 Willkommen im Studenten-Programm!</h1>
            <p>Hallo {firstName},</p>
            <p>herzlich willkommen im Magic Tool System für Studenten!</p>
            <p>Du hast den ersten Schritt gemacht und bist jetzt Teil einer exklusiven Community von Studenten, die bereits 500€+ monatlich verdienen.</p>
            
            <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #1e40af;">Dein nächster Schritt:</h3>
              <ol>
                <li>Schau dir die VSL an: <a href="{vslUrl}">Hier klicken</a></li>
                <li>Lade deine Bonus-Materialien herunter</li>
                <li>Trete der Studenten-Community bei</li>
              </ol>
            </div>
            
            <p>Viel Erfolg auf deinem Weg zu 500€+ monatlich!</p>
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Willkommen im Studenten-Programm!
          
          Hallo {firstName},
          
          herzlich willkommen im Magic Tool System für Studenten!
          
          Dein nächster Schritt:
          1. Schau dir die VSL an: {vslUrl}
          2. Lade deine Bonus-Materialien herunter
          3. Trete der Studenten-Community bei
          
          Viel Erfolg!
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'student_followup_1': {
        subject: '📚 Dein Studenten-Erfolgsplan wartet auf dich!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #3b82f6;">📚 Dein Studenten-Erfolgsplan</h1>
            <p>Hallo {firstName},</p>
            <p>ich hoffe, du hast die VSL bereits angeschaut! Falls nicht, hier ist dein direkter Link:</p>
            <p><a href="{vslUrl}" style="background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">🎯 VSL jetzt ansehen</a></p>
            
            <div style="background: #fef3c7; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #92400e;">🔥 Exklusives Studenten-Angebot:</h3>
              <p><strong>Nur noch 24 Stunden: 50% Rabatt auf das Premium-Paket!</strong></p>
              <p>Statt 197€ nur 97€ - inklusive 1:1 Coaching Session!</p>
            </div>
            
            <p>Viele Studenten haben bereits mit dem Magic Tool System begonnen. Wirst du der nächste Erfolgsfall?</p>
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Dein Studenten-Erfolgsplan
          
          Hallo {firstName},
          
          ich hoffe, du hast die VSL bereits angeschaut! Falls nicht, hier ist dein direkter Link: {vslUrl}
          
          🔥 Exklusives Studenten-Angebot:
          Nur noch 24 Stunden: 50% Rabatt auf das Premium-Paket!
          Statt 197€ nur 97€ - inklusive 1:1 Coaching Session!
          
          Viele Studenten haben bereits mit dem Magic Tool System begonnen. Wirst du der nächste Erfolgsfall?
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'student_followup_2': {
        subject: '⚡ Letzte Chance: Studenten-Rabatt läuft ab!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #dc2626;">⚡ Letzte Chance: Studenten-Rabatt läuft ab!</h1>
            <p>Hallo {firstName},</p>
            <p>dein exklusiver Studenten-Rabatt läuft in wenigen Stunden ab!</p>
            
            <div style="background: #fee2e2; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #dc2626;">
              <h3 style="color: #dc2626;">⏰ Nur noch 6 Stunden:</h3>
              <p><strong>Magic Tool Premium für Studenten</strong></p>
              <p>Statt 197€ nur 97€</p>
              <p>✅ 1:1 Coaching Session (30 Min)</p>
              <p>✅ Exklusive Studenten-Strategien</p>
              <p>✅ Community-Zugang</p>
              <p>✅ Prioritäts-Support</p>
            </div>
            
            <p><a href="{vslUrl}" style="background: #dc2626; color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 18px;">🚀 JETZT KAUFEN & SPAREN</a></p>
            
            <p>Nach Ablauf des Rabatts kostet das Premium-Paket wieder 197€.</p>
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Letzte Chance: Studenten-Rabatt läuft ab!
          
          Hallo {firstName},
          
          dein exklusiver Studenten-Rabatt läuft in wenigen Stunden ab!
          
          ⏰ Nur noch 6 Stunden:
          Magic Tool Premium für Studenten
          Statt 197€ nur 97€
          ✅ 1:1 Coaching Session (30 Min)
          ✅ Exklusive Studenten-Strategien
          ✅ Community-Zugang
          ✅ Prioritäts-Support
          
          JETZT KAUFEN: {vslUrl}
          
          Nach Ablauf des Rabatts kostet das Premium-Paket wieder 197€.
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'student_reminder': {
        subject: '🎯 {firstName}, dein Magic Tool wartet auf dich!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #059669;">🎯 Dein Magic Tool wartet auf dich!</h1>
            <p>Hallo {firstName},</p>
            <p>ich habe bemerkt, dass du noch nicht mit dem Magic Tool System gestartet bist. Vielleicht hast du Fragen oder brauchst mehr Informationen?</p>
            
            <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #059669;">💡 Häufige Fragen von Studenten:</h3>
              <p><strong>Q: Wie viel Zeit brauche ich täglich?</strong><br>
              A: Nur 30-60 Minuten am Tag reichen aus!</p>
              
              <p><strong>Q: Brauche ich Vorkenntnisse?</strong><br>
              A: Nein, alles wird Schritt für Schritt erklärt!</p>
              
              <p><strong>Q: Wann sehe ich erste Ergebnisse?</strong><br>
              A: Viele Studenten sehen erste Erfolge in 2-4 Wochen!</p>
            </div>
            
            <p><a href="{vslUrl}" style="background: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">🎯 Jetzt mehr erfahren</a></p>
            
            <p>Falls du Fragen hast, antworte einfach auf diese E-Mail!</p>
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Dein Magic Tool wartet auf dich!
          
          Hallo {firstName},
          
          ich habe bemerkt, dass du noch nicht mit dem Magic Tool System gestartet bist. Vielleicht hast du Fragen oder brauchst mehr Informationen?
          
          💡 Häufige Fragen von Studenten:
          Q: Wie viel Zeit brauche ich täglich?
          A: Nur 30-60 Minuten am Tag reichen aus!
          
          Q: Brauche ich Vorkenntnisse?
          A: Nein, alles wird Schritt für Schritt erklärt!
          
          Q: Wann sehe ich erste Ergebnisse?
          A: Viele Studenten sehen erste Erfolge in 2-4 Wochen!
          
          Jetzt mehr erfahren: {vslUrl}
          
          Falls du Fragen hast, antworte einfach auf diese E-Mail!
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },

      // EMPLOYEE TEMPLATES
      'employee_welcome': {
        subject: '💼 Willkommen im Business-Programm, {firstName}!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #059669;">💼 Willkommen im Business-Programm!</h1>
            <p>Hallo {firstName},</p>
            <p>herzlich willkommen im Magic Tool System für Angestellte!</p>
            <p>Du bist jetzt Teil einer exklusiven Community von Vollzeit-Angestellten, die bereits 2.000€+ Zusatzeinkommen generieren.</p>
            
            <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #166534;">Dein Skalierungsplan:</h3>
              <ol>
                <li>Schau dir die VSL an: <a href="{vslUrl}">Hier klicken</a></li>
                <li>Lade deine Business-Automatisierung herunter</li>
                <li>Trete der VIP-Community bei</li>
              </ol>
            </div>
            
            <p>Viel Erfolg auf deinem Weg zu 5.000€+ monatlich!</p>
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Willkommen im Business-Programm!
          
          Hallo {firstName},
          
          herzlich willkommen im Magic Tool System für Angestellte!
          
          Dein Skalierungsplan:
          1. Schau dir die VSL an: {vslUrl}
          2. Lade deine Business-Automatisierung herunter
          3. Trete der VIP-Community bei
          
          Viel Erfolg!
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'employee_followup_1': {
        subject: '🚀 Dein Business-Skalierungsplan wartet!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #059669;">🚀 Dein Business-Skalierungsplan</h1>
            <p>Hallo {firstName},</p>
            <p>als Vollzeit-Angestellter weißt du, wie wichtig ein stabiles Zusatzeinkommen ist. Das Magic Tool System ist speziell für Menschen wie dich entwickelt!</p>
            
            <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #166534;">💼 Business-Vorteile:</h3>
              <ul>
                <li>Flexible Arbeitszeiten (nach der Arbeit)</li>
                <li>Skalierbares System</li>
                <li>Business-Automatisierung</li>
                <li>VIP-Community für Angestellte</li>
              </ul>
            </div>
            
            <p><a href="{vslUrl}" style="background: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">💼 Business-VSL ansehen</a></p>
            
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Dein Business-Skalierungsplan
          
          Hallo {firstName},
          
          als Vollzeit-Angestellter weißt du, wie wichtig ein stabiles Zusatzeinkommen ist. Das Magic Tool System ist speziell für Menschen wie dich entwickelt!
          
          💼 Business-Vorteile:
          • Flexible Arbeitszeiten (nach der Arbeit)
          • Skalierbares System
          • Business-Automatisierung
          • VIP-Community für Angestellte
          
          Business-VSL ansehen: {vslUrl}
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'employee_followup_2': {
        subject: '🔥 VIP-Business-Strategien - Nur für Angestellte!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #dc2626;">🔥 VIP-Business-Strategien</h1>
            <p>Hallo {firstName},</p>
            <p>als Angestellter hast du Zugang zu exklusiven Business-Strategien, die andere nicht kennen!</p>
            
            <div style="background: #fef2f2; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #dc2626;">⚡ Exklusive Business-Boni:</h3>
              <p><strong>Magic Tool Premium Business</strong></p>
              <p>✅ 1:1 Business-Coaching (60 Min)</p>
              <p>✅ Skalierungs-Strategien</p>
              <p>✅ Exklusive Business-Tools</p>
              <p>✅ VIP-Community</p>
              <p>✅ Prioritäts-Support</p>
            </div>
            
            <p><a href="{vslUrl}" style="background: #dc2626; color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 18px;">🚀 VIP-BUSINESS-PAKET</a></p>
            
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          VIP-Business-Strategien
          
          Hallo {firstName},
          
          als Angestellter hast du Zugang zu exklusiven Business-Strategien, die andere nicht kennen!
          
          ⚡ Exklusive Business-Boni:
          Magic Tool Premium Business
          ✅ 1:1 Business-Coaching (60 Min)
          ✅ Skalierungs-Strategien
          ✅ Exklusive Business-Tools
          ✅ VIP-Community
          ✅ Prioritäts-Support
          
          VIP-BUSINESS-PAKET: {vslUrl}
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'employee_reminder': {
        subject: '💼 {firstName}, dein Business wartet auf dich!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #059669;">💼 Dein Business wartet auf dich!</h1>
            <p>Hallo {firstName},</p>
            <p>ich weiß, dass du als Angestellter wenig Zeit hast. Deshalb habe ich das Magic Tool System so entwickelt, dass es perfekt in deinen Alltag passt.</p>
            
            <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #059669;">⏰ Zeitmanagement für Angestellte:</h3>
              <p><strong>Nur 1-2 Stunden pro Woche</strong> reichen aus, um 2.000€+ Zusatzeinkommen aufzubauen!</p>
              <p>• Nach der Arbeit oder am Wochenende</p>
              <p>• Vollständig automatisiert</p>
              <p>• Skalierbar nach deinen Wünschen</p>
            </div>
            
            <p><a href="{vslUrl}" style="background: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">💼 Business-Plan ansehen</a></p>
            
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Dein Business wartet auf dich!
          
          Hallo {firstName},
          
          ich weiß, dass du als Angestellter wenig Zeit hast. Deshalb habe ich das Magic Tool System so entwickelt, dass es perfekt in deinen Alltag passt.
          
          ⏰ Zeitmanagement für Angestellte:
          Nur 1-2 Stunden pro Woche reichen aus, um 2.000€+ Zusatzeinkommen aufzubauen!
          • Nach der Arbeit oder am Wochenende
          • Vollständig automatisiert
          • Skalierbar nach deinen Wünschen
          
          Business-Plan ansehen: {vslUrl}
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },

      // PARENT TEMPLATES
      'parent_welcome': {
        subject: '👨‍👩‍👧‍👦 Willkommen im Familien-Programm, {firstName}!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #7c3aed;">👨‍👩‍👧‍👦 Willkommen im Familien-Programm!</h1>
            <p>Hallo {firstName},</p>
            <p>herzlich willkommen im Magic Tool System für Eltern!</p>
            <p>Du bist jetzt Teil einer exklusiven Community von Eltern, die bereits 800-1.200€ flexibles Einkommen neben der Familie aufbauen.</p>
            
            <div style="background: #faf5ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #5b21b6;">Dein Familien-Plan:</h3>
              <ol>
                <li>Schau dir die VSL an: <a href="{vslUrl}">Hier klicken</a></li>
                <li>Lade deine Familien-Strategien herunter</li>
                <li>Trete der Eltern-Community bei</li>
              </ol>
            </div>
            
            <p>Viel Erfolg auf deinem Weg zu flexiblem Familien-Einkommen!</p>
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Willkommen im Familien-Programm!
          
          Hallo {firstName},
          
          herzlich willkommen im Magic Tool System für Eltern!
          
          Dein Familien-Plan:
          1. Schau dir die VSL an: {vslUrl}
          2. Lade deine Familien-Strategien herunter
          3. Trete der Eltern-Community bei
          
          Viel Erfolg!
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'parent_followup_1': {
        subject: '👨‍👩‍👧‍👦 Dein flexibles Familien-Einkommen wartet!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #7c3aed;">👨‍👩‍👧‍👦 Dein flexibles Familien-Einkommen</h1>
            <p>Hallo {firstName},</p>
            <p>als Elternteil weißt du, wie wichtig es ist, Zeit für die Familie zu haben und trotzdem ein gutes Einkommen zu generieren.</p>
            
            <div style="background: #faf5ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #5b21b6;">👨‍👩‍👧‍👦 Familien-Vorteile:</h3>
              <ul>
                <li>Flexible Arbeitszeiten (wenn die Kinder schlafen)</li>
                <li>Work-Life-Balance</li>
                <li>Familien-freundliche Strategien</li>
                <li>Eltern-Community</li>
              </ul>
            </div>
            
            <p><a href="{vslUrl}" style="background: #7c3aed; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">👨‍👩‍👧‍👦 Familien-VSL ansehen</a></p>
            
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Dein flexibles Familien-Einkommen
          
          Hallo {firstName},
          
          als Elternteil weißt du, wie wichtig es ist, Zeit für die Familie zu haben und trotzdem ein gutes Einkommen zu generieren.
          
          👨‍👩‍👧‍👦 Familien-Vorteile:
          • Flexible Arbeitszeiten (wenn die Kinder schlafen)
          • Work-Life-Balance
          • Familien-freundliche Strategien
          • Eltern-Community
          
          Familien-VSL ansehen: {vslUrl}
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'parent_followup_2': {
        subject: '🎁 Familien-freundliche Strategien - Exklusiv für Eltern!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #dc2626;">🎁 Familien-freundliche Strategien</h1>
            <p>Hallo {firstName},</p>
            <p>als Elternteil hast du Zugang zu speziellen Strategien, die perfekt in deinen Familienalltag passen!</p>
            
            <div style="background: #fef2f2; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #dc2626;">👨‍👩‍👧‍👦 Exklusive Familien-Boni:</h3>
              <p><strong>Magic Tool Premium Familien</strong></p>
              <p>✅ 1:1 Familien-Coaching (45 Min)</p>
              <p>✅ Exklusive Familien-Tools</p>
              <p>✅ Work-Life-Balance Guide</p>
              <p>✅ Eltern-Community</p>
              <p>✅ Flexible Arbeitszeiten</p>
            </div>
            
            <p><a href="{vslUrl}" style="background: #dc2626; color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 18px;">👨‍👩‍👧‍👦 FAMILIEN-PREMIUM</a></p>
            
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Familien-freundliche Strategien
          
          Hallo {firstName},
          
          als Elternteil hast du Zugang zu speziellen Strategien, die perfekt in deinen Familienalltag passen!
          
          👨‍👩‍👧‍👦 Exklusive Familien-Boni:
          Magic Tool Premium Familien
          ✅ 1:1 Familien-Coaching (45 Min)
          ✅ Exklusive Familien-Tools
          ✅ Work-Life-Balance Guide
          ✅ Eltern-Community
          ✅ Flexible Arbeitszeiten
          
          FAMILIEN-PREMIUM: {vslUrl}
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      },
      'parent_reminder': {
        subject: '👨‍👩‍👧‍👦 {firstName}, deine Familie wartet auf mehr Zeit!',
        html: `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #7c3aed;">👨‍👩‍👧‍👦 Deine Familie wartet auf mehr Zeit!</h1>
            <p>Hallo {firstName},</p>
            <p>ich verstehe, dass du als Elternteil wenig Zeit hast. Das Magic Tool System ist speziell für Eltern entwickelt, die mehr Zeit mit der Familie verbringen möchten.</p>
            
            <div style="background: #faf5ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #5b21b6;">⏰ Familien-Zeitmanagement:</h3>
              <p><strong>Nur 30-60 Minuten pro Tag</strong> reichen aus, um 800-1.200€ flexibles Einkommen aufzubauen!</p>
              <p>• Wenn die Kinder schlafen</p>
              <p>• Am Wochenende</p>
              <p>• Vollständig flexibel</p>
            </div>
            
            <p><a href="{vslUrl}" style="background: #7c3aed; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">👨‍👩‍👧‍👦 Familien-Plan ansehen</a></p>
            
            <p>Dein Magic Tool Team</p>
          </div>
        `,
        text: `
          Deine Familie wartet auf mehr Zeit!
          
          Hallo {firstName},
          
          ich verstehe, dass du als Elternteil wenig Zeit hast. Das Magic Tool System ist speziell für Eltern entwickelt, die mehr Zeit mit der Familie verbringen möchten.
          
          ⏰ Familien-Zeitmanagement:
          Nur 30-60 Minuten pro Tag reichen aus, um 800-1.200€ flexibles Einkommen aufzubauen!
          • Wenn die Kinder schlafen
          • Am Wochenende
          • Vollständig flexibel
          
          Familien-Plan ansehen: {vslUrl}
          
          Dein Magic Tool Team
        `,
        variables: ['firstName', 'vslUrl']
      }
    };

    return templates[`${personaType}_${templateId}`] || null;
  }

  private personalizeTemplate(template: string, leadData: any, personaType: string): string {
    return template
      .replace(/{firstName}/g, leadData?.firstName || 'Lieber Interessent')
      .replace(/{email}/g, leadData?.email || '')
      .replace(/{personaType}/g, personaType)
      .replace(/{vslUrl}/g, `http://localhost:3000/vsl?persona=${personaType}&leadId=${leadData?.id || ''}`)
      .replace(/{quizAnswers}/g, JSON.stringify(leadData?.quizAnswers || {}));
  }

  private async trackEmailSent(emailData: EmailData, messageId: string): Promise<void> {
    await storage.createAnalyticsEvent({
      event: 'email_sent',
      page: '/email',
      userId: emailData.leadId?.toString(),
      data: JSON.stringify({
        to: emailData.to,
        subject: emailData.subject,
        personaType: emailData.personaType,
        templateId: emailData.templateId,
        messageId,
        timestamp: new Date().toISOString()
      })
    });
  }

  private async trackEmailError(emailData: EmailData, error: any): Promise<void> {
    await storage.createAnalyticsEvent({
      event: 'email_error',
      page: '/email',
      userId: emailData.leadId?.toString(),
      data: JSON.stringify({
        to: emailData.to,
        subject: emailData.subject,
        personaType: emailData.personaType,
        templateId: emailData.templateId,
        error: error.message,
        timestamp: new Date().toISOString()
      })
    });
  }

  async getEmailStats(personaType?: string): Promise<any> {
    // Hier würden normalerweise E-Mail-Statistiken aus der Datenbank geladen
    const baseStats = {
      sent: 0,
      delivered: 0,
      opened: 0,
      clicked: 0,
      bounced: 0,
      unsubscribed: 0
    };

    // Simuliere Persona-spezifische Statistiken
    if (personaType) {
      switch (personaType) {
        case 'student':
          return {
            ...baseStats,
            sent: 1250,
            delivered: 1187,
            opened: 892,
            clicked: 445,
            bounced: 63,
            unsubscribed: 12,
            openRate: 75.1,
            clickRate: 37.5
          };
        case 'employee':
          return {
            ...baseStats,
            sent: 890,
            delivered: 845,
            opened: 676,
            clicked: 338,
            bounced: 45,
            unsubscribed: 8,
            openRate: 80.0,
            clickRate: 40.0
          };
        case 'parent':
          return {
            ...baseStats,
            sent: 1100,
            delivered: 1045,
            opened: 836,
            clicked: 418,
            bounced: 55,
            unsubscribed: 10,
            openRate: 80.0,
            clickRate: 40.0
          };
      }
    }

    return baseStats;
  }
}

export const smtpService = new SMTPService(); 