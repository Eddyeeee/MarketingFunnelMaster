import { Router } from 'express';
import { z } from 'zod';
import { getInstapageService, duplicatePage, createPersonalizedPage } from '../services/instapageService';

const router = Router();

// Schema für Validierung
const duplicatePageSchema = z.object({
  templateId: z.string().min(1),
  newName: z.string().min(1)
});

const createPersonalizedPageSchema = z.object({
  templateId: z.string().min(1),
  persona: z.object({
    name: z.string().min(1),
    type: z.string().min(1),
    preferences: z.record(z.any())
  })
});

/**
 * GET /api/instapage/pages
 * Holt alle Instapage-Seiten
 */
router.get('/pages', async (req, res) => {
  try {
    const service = getInstapageService();
    const pages = await service.getPages();
    res.json({ success: true, data: pages });
  } catch (error) {
    console.error('Failed to fetch Instapage pages:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to fetch pages',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

/**
 * GET /api/instapage/pages/:id
 * Holt eine spezifische Instapage-Seite
 */
router.get('/pages/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const service = getInstapageService();
    const page = await service.getPage(id);
    res.json({ success: true, data: page });
  } catch (error) {
    console.error(`Failed to fetch Instapage page ${req.params.id}:`, error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to fetch page',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

/**
 * POST /api/instapage/pages/duplicate
 * Dupliziert eine Instapage-Seite
 */
router.post('/pages/duplicate', async (req, res) => {
  try {
    const { templateId, newName } = duplicatePageSchema.parse(req.body);
    
    const duplicatedPage = await duplicatePage(templateId, newName);
    
    res.json({ 
      success: true, 
      data: duplicatedPage,
      message: 'Page duplicated successfully'
    });
  } catch (error) {
    console.error('Failed to duplicate Instapage page:', error);
    
    if (error instanceof z.ZodError) {
      res.status(400).json({ 
        success: false, 
        error: 'Invalid request data',
        details: error.errors
      });
    } else {
      res.status(500).json({ 
        success: false, 
        error: 'Failed to duplicate page',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }
});

/**
 * POST /api/instapage/pages/personalized
 * Erstellt eine personalisierte Landing Page
 */
router.post('/pages/personalized', async (req, res) => {
  try {
    const { templateId, persona } = createPersonalizedPageSchema.parse(req.body);
    
    const personalizedPage = await createPersonalizedPage(templateId, persona);
    
    res.json({ 
      success: true, 
      data: personalizedPage,
      message: 'Personalized page created successfully'
    });
  } catch (error) {
    console.error('Failed to create personalized page:', error);
    
    if (error instanceof z.ZodError) {
      res.status(400).json({ 
        success: false, 
        error: 'Invalid request data',
        details: error.errors
      });
    } else {
      res.status(500).json({ 
        success: false, 
        error: 'Failed to create personalized page',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }
});

/**
 * POST /api/instapage/test-connection
 * Testet die Instapage API-Verbindung
 */
router.post('/test-connection', async (req, res) => {
  try {
    const service = getInstapageService();
    const isConnected = await service.testConnection();
    
    res.json({ 
      success: true, 
      connected: isConnected,
      message: isConnected ? 'Connection successful' : 'Connection failed'
    });
  } catch (error) {
    console.error('Instapage connection test failed:', error);
    res.status(500).json({ 
      success: false, 
      connected: false,
      error: 'Connection test failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

export default router; 