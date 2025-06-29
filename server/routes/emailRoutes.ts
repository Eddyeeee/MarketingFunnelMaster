import { Router } from 'express';
import { smtpService, EmailConfig, EmailData } from '../services/smtpService';
import { storage } from '../storage';

const router = Router();

// SMTP-Konfiguration initialisieren
router.post('/smtp/initialize', async (req, res) => {
  try {
    const config: EmailConfig = req.body;
    const success = await smtpService.initialize(config);
    
    if (success) {
      res.json({ success: true, message: 'SMTP erfolgreich konfiguriert' });
    } else {
      res.status(500).json({ success: false, message: 'SMTP-Konfiguration fehlgeschlagen' });
    }
  } catch (error) {
    console.error('SMTP-Initialisierung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Einzelne E-Mail senden
router.post('/send', async (req, res) => {
  try {
    const emailData: EmailData = req.body;
    const success = await smtpService.sendEmail(emailData);
    
    if (success) {
      res.json({ success: true, message: 'E-Mail erfolgreich gesendet' });
    } else {
      res.status(500).json({ success: false, message: 'E-Mail-Versendung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('E-Mail-Versendung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Bulk-E-Mails senden
router.post('/send/bulk', async (req, res) => {
  try {
    const { emails }: { emails: EmailData[] } = req.body;
    const result = await smtpService.sendBulkEmails(emails);
    
    res.json({
      success: true,
      message: `Bulk-Versendung abgeschlossen`,
      result
    });
  } catch (error) {
    console.error('Bulk-E-Mail-Versendung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Persona-spezifische E-Mail senden
router.post('/send/persona', async (req, res) => {
  try {
    const { personaType, leadId, templateId } = req.body;
    
    // Lead-Daten abrufen
    const lead = await storage.getLead(leadId);
    if (!lead) {
      return res.status(404).json({ success: false, message: 'Lead nicht gefunden' });
    }
    
    const success = await smtpService.sendPersonaEmail(personaType, lead, templateId);
    
    if (success) {
      res.json({ success: true, message: 'Persona-E-Mail erfolgreich gesendet' });
    } else {
      res.status(500).json({ success: false, message: 'Persona-E-Mail-Versendung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Persona-E-Mail-Versendung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Automatische Follow-up E-Mails
router.post('/send/followup', async (req, res) => {
  try {
    const { personaType, leadId, followupType } = req.body;
    
    // Lead-Daten abrufen
    const lead = await storage.getLead(leadId);
    if (!lead) {
      return res.status(404).json({ success: false, message: 'Lead nicht gefunden' });
    }
    
    // Follow-up Template basierend auf Typ und Persona
    const templateId = `${followupType}_${personaType}`;
    const success = await smtpService.sendPersonaEmail(personaType, lead, templateId);
    
    if (success) {
      res.json({ success: true, message: 'Follow-up E-Mail erfolgreich gesendet' });
    } else {
      res.status(500).json({ success: false, message: 'Follow-up E-Mail-Versendung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Follow-up E-Mail-Versendung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// E-Mail-Statistiken abrufen
router.get('/stats/:personaType?', async (req, res) => {
  try {
    const { personaType } = req.params;
    const stats = await smtpService.getEmailStats(personaType);
    
    res.json({ success: true, stats });
  } catch (error) {
    console.error('E-Mail-Statistiken Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// E-Mail-Templates abrufen
router.get('/templates/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    
    // Hier würden normalerweise Templates aus der Datenbank geladen
    const templates = {
      student: [
        { id: 'welcome', name: 'Willkommens-E-Mail', subject: '🎓 Willkommen im Studenten-Programm!' },
        { id: 'followup_1', name: 'Follow-up 1', subject: 'Dein nächster Schritt zum Erfolg' },
        { id: 'followup_2', name: 'Follow-up 2', subject: 'Exklusive Studenten-Boni' },
        { id: 'reminder', name: 'Erinnerung', subject: 'Verpasse nicht deine Chance!' }
      ],
      employee: [
        { id: 'welcome', name: 'Willkommens-E-Mail', subject: '💼 Willkommen im Business-Programm!' },
        { id: 'followup_1', name: 'Follow-up 1', subject: 'Dein Business-Skalierungsplan' },
        { id: 'followup_2', name: 'Follow-up 2', subject: 'VIP-Business-Strategien' },
        { id: 'reminder', name: 'Erinnerung', subject: 'Dein Business wartet auf dich!' }
      ],
      parent: [
        { id: 'welcome', name: 'Willkommens-E-Mail', subject: '👨‍👩‍👧‍👦 Willkommen im Familien-Programm!' },
        { id: 'followup_1', name: 'Follow-up 1', subject: 'Dein flexibles Familien-Einkommen' },
        { id: 'followup_2', name: 'Follow-up 2', subject: 'Familien-freundliche Strategien' },
        { id: 'reminder', name: 'Erinnerung', subject: 'Deine Familie wartet auf mehr Zeit!' }
      ]
    };
    
    const personaTemplates = templates[personaType] || [];
    res.json({ success: true, templates: personaTemplates });
  } catch (error) {
    console.error('Template-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// E-Mail-Template erstellen/bearbeiten
router.post('/templates', async (req, res) => {
  try {
    const { personaType, templateId, template } = req.body;
    
    // Hier würde normalerweise das Template in der Datenbank gespeichert
    console.log(`Template ${templateId} für Persona ${personaType} gespeichert`);
    
    res.json({ success: true, message: 'Template erfolgreich gespeichert' });
  } catch (error) {
    console.error('Template-Speicherung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// E-Mail-Automation starten
router.post('/automation/start', async (req, res) => {
  try {
    const { personaType, automationType, leadIds } = req.body;
    
    let successCount = 0;
    let errorCount = 0;
    
    for (const leadId of leadIds) {
      try {
        const lead = await storage.getLead(leadId);
        if (lead) {
          const success = await smtpService.sendPersonaEmail(personaType, lead, automationType);
          if (success) {
            successCount++;
          } else {
            errorCount++;
          }
        }
      } catch (error) {
        errorCount++;
        console.error(`Automation Fehler für Lead ${leadId}:`, error);
      }
    }
    
    res.json({
      success: true,
      message: 'E-Mail-Automation abgeschlossen',
      result: { successCount, errorCount }
    });
  } catch (error) {
    console.error('E-Mail-Automation Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// E-Mail-Tracking Webhook
router.post('/webhook/tracking', async (req, res) => {
  try {
    const { event, email, messageId, timestamp } = req.body;
    
    // E-Mail-Tracking-Event speichern
    await storage.createAnalyticsEvent({
      event: `email_${event}`,
      page: '/email',
      userId: messageId,
      data: JSON.stringify({
        email,
        messageId,
        event,
        timestamp
      })
    });
    
    res.json({ success: true });
  } catch (error) {
    console.error('E-Mail-Tracking Webhook Fehler:', error);
    res.status(500).json({ success: false });
  }
});

export default router; 