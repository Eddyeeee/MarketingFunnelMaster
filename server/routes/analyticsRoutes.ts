import { Router } from 'express';
import { storage } from '../storage';

const router = Router();

// Analytics-Event erstellen
router.post('/events', async (req, res) => {
  try {
    const { event, page, userId, data } = req.body;
    const analyticsEvent = await storage.createAnalyticsEvent({
      event,
      page,
      userId,
      data
    });
    
    if (analyticsEvent) {
      res.json({ success: true, event: analyticsEvent });
    } else {
      res.status(500).json({ success: false, message: 'Event-Erstellung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Analytics-Event Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Analytics-Statistiken abrufen
router.get('/stats', async (req, res) => {
  try {
    const { startDate, endDate, event, page, personaType } = req.query;
    
    const stats = await storage.getAnalyticsStats({
      startDate: startDate as string,
      endDate: endDate as string,
      event: event as string,
      page: page as string,
      personaType: personaType as string
    });
    
    res.json({ success: true, stats });
  } catch (error) {
    console.error('Analytics-Statistiken Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Events für Lead abrufen
router.get('/events/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const { limit, offset } = req.query;
    
    const events = await storage.getUserEvents(userId, {
      limit: limit ? parseInt(limit as string) : undefined,
      offset: offset ? parseInt(offset as string) : undefined
    });
    
    res.json({ success: true, events });
  } catch (error) {
    console.error('User-Events Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Conversion-Funnel abrufen
router.get('/funnel', async (req, res) => {
  try {
    const { startDate, endDate, personaType } = req.query;
    
    const funnel = await storage.getConversionFunnel({
      startDate: startDate as string,
      endDate: endDate as string,
      personaType: personaType as string
    });
    
    res.json({ success: true, funnel });
  } catch (error) {
    console.error('Conversion-Funnel Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

export default router; 