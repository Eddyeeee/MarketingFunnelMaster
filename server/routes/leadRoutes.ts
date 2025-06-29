import { Router } from 'express';
import { storage } from '../storage';

const router = Router();

// Lead erstellen
router.post('/', async (req, res) => {
  try {
    const leadData = req.body;
    const lead = await storage.createLead(leadData);
    
    if (lead) {
      res.json({ success: true, lead });
    } else {
      res.status(500).json({ success: false, message: 'Lead-Erstellung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Lead-Erstellung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Lead abrufen
router.get('/:leadId', async (req, res) => {
  try {
    const { leadId } = req.params;
    const lead = await storage.getLead(parseInt(leadId));
    
    if (lead) {
      res.json({ success: true, lead });
    } else {
      res.status(404).json({ success: false, message: 'Lead nicht gefunden' });
    }
  } catch (error) {
    console.error('Lead-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Lead aktualisieren
router.put('/:leadId', async (req, res) => {
  try {
    const { leadId } = req.params;
    const updateData = req.body;
    const lead = await storage.updateLead(parseInt(leadId), updateData);
    
    if (lead) {
      res.json({ success: true, lead });
    } else {
      res.status(404).json({ success: false, message: 'Lead nicht gefunden' });
    }
  } catch (error) {
    console.error('Lead-Aktualisierung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Alle Leads abrufen
router.get('/', async (req, res) => {
  try {
    const { personaType, status, limit, offset } = req.query;
    const leads = await storage.getLeads({
      personaType: personaType as string,
      status: status as string,
      limit: limit ? parseInt(limit as string) : undefined,
      offset: offset ? parseInt(offset as string) : undefined
    });
    
    res.json({ success: true, leads });
  } catch (error) {
    console.error('Leads-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

export default router; 