import { Router } from 'express';
import { vslService } from '../services/vslService';

const router = Router();

// VSL-Inhalt für Persona abrufen
router.get('/content/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    const { leadId } = req.query;
    
    const vslContent = await vslService.generatePersonaContent(personaType, {
      leadId: leadId ? parseInt(leadId as string) : undefined
    });
    
    if (vslContent) {
      res.json({ success: true, content: vslContent });
    } else {
      res.status(404).json({ success: false, message: 'VSL-Inhalt nicht gefunden' });
    }
  } catch (error) {
    console.error('VSL-Inhalt Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// VSL-Preise für Persona abrufen
router.get('/pricing/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    const pricing = await vslService.getPersonaPricing(personaType);
    
    res.json({ success: true, pricing });
  } catch (error) {
    console.error('VSL-Pricing Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// VSL-Strategien für Persona abrufen
router.get('/strategies/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    const strategies = await vslService.getPersonaStrategies(personaType);
    
    res.json({ success: true, strategies });
  } catch (error) {
    console.error('VSL-Strategien Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// VSL-Tracking Event
router.post('/track', async (req, res) => {
  try {
    const { event, personaType, leadId, data } = req.body;
    
    await vslService.trackEvent(event, {
      personaType,
      leadId,
      data
    });
    
    res.json({ success: true });
  } catch (error) {
    console.error('VSL-Tracking Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// VSL-A/B-Test Variante abrufen
router.get('/ab-test/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    const { leadId } = req.query;
    
    const variant = await vslService.getABTestVariant(personaType, {
      leadId: leadId ? parseInt(leadId as string) : undefined
    });
    
    res.json({ success: true, variant });
  } catch (error) {
    console.error('VSL-A/B-Test Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

export default router; 