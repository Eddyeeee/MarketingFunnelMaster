import express from 'express';
import { upsellService } from '../services/upsellService.js';
import { analyticsService } from '../services/analyticsService.js';

const router = express.Router();

// Alle Upsell Flows abrufen
router.get('/flows', async (req, res) => {
  try {
    const flows = await upsellService.getAllUpsellFlows();
    res.json({
      success: true,
      flows
    });
  } catch (error) {
    console.error('Fehler beim Abrufen der Upsell Flows:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Abrufen der Upsell Flows'
    });
  }
});

// Upsell Flow für Persona abrufen
router.get('/flows/:personaType', async (req, res) => {
  try {
    const { personaType } = req.params;
    const { purchaseAmount = 0 } = req.query;
    
    const flows = await upsellService.getUpsellFlowForPersona(
      personaType, 
      Number(purchaseAmount)
    );
    
    res.json({
      success: true,
      flows
    });
  } catch (error) {
    console.error('Fehler beim Abrufen der Upsell Flows für Persona:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Abrufen der Upsell Flows'
    });
  }
});

// Spezifischen Upsell Flow abrufen
router.get('/flows/detail/:flowId', async (req, res) => {
  try {
    const { flowId } = req.params;
    const flow = await upsellService.getUpsellFlow(flowId);
    
    if (!flow) {
      return res.status(404).json({
        success: false,
        error: 'Upsell Flow nicht gefunden'
      });
    }
    
    res.json({
      success: true,
      flow
    });
  } catch (error) {
    console.error('Fehler beim Abrufen des Upsell Flows:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Abrufen des Upsell Flows'
    });
  }
});

// Upsell-Statistiken abrufen
router.get('/stats', async (req, res) => {
  try {
    const stats = await upsellService.getUpsellStats();
    res.json({
      success: true,
      stats
    });
  } catch (error) {
    console.error('Fehler beim Abrufen der Upsell-Statistiken:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Abrufen der Statistiken'
    });
  }
});

// Upsell Event tracken
router.post('/track', async (req, res) => {
  try {
    const { eventType, flowId, productId, customerData } = req.body;
    
    // Event tracken
    await upsellService.trackUpsellEvent(eventType, flowId, productId, customerData);
    
    // Analytics Event senden
    await analyticsService.trackEvent('upsell_event', {
      eventType,
      flowId,
      productId,
      customerData
    });
    
    res.json({
      success: true,
      message: 'Event erfolgreich getrackt'
    });
  } catch (error) {
    console.error('Fehler beim Tracken des Upsell Events:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Tracken des Events'
    });
  }
});

// Digistore24 Produkt erstellen
router.post('/digistore/create-product', async (req, res) => {
  try {
    const productData = req.body;
    const result = await upsellService.createDigistoreProduct(productData);
    
    res.json({
      success: true,
      result
    });
  } catch (error) {
    console.error('Fehler beim Erstellen des Digistore24 Produkts:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Erstellen des Produkts'
    });
  }
});

// Digistore24 Verkauf registrieren
router.post('/digistore/register-sale', async (req, res) => {
  try {
    const { productId, customerData } = req.body;
    const result = await upsellService.registerDigistoreSale(productId, customerData);
    
    // Analytics Event senden
    await analyticsService.trackEvent('digistore_sale', {
      productId,
      customerData,
      result
    });
    
    res.json({
      success: true,
      result
    });
  } catch (error) {
    console.error('Fehler beim Registrieren des Digistore24 Verkaufs:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Registrieren des Verkaufs'
    });
  }
});

// Q-Money spezifische Route
router.get('/qmoney', async (req, res) => {
  try {
    const qmoneyFlow = await upsellService.getUpsellFlow('qmoney_upsell');
    
    if (!qmoneyFlow) {
      return res.status(404).json({
        success: false,
        error: 'Q-Money Flow nicht gefunden'
      });
    }
    
    res.json({
      success: true,
      flow: qmoneyFlow
    });
  } catch (error) {
    console.error('Fehler beim Abrufen des Q-Money Flows:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Abrufen des Q-Money Flows'
    });
  }
});

// Cash Maximus spezifische Route
router.get('/cashmaximus', async (req, res) => {
  try {
    const cashMaximusFlow = await upsellService.getUpsellFlow('cashmaximus_upsell');
    
    if (!cashMaximusFlow) {
      return res.status(404).json({
        success: false,
        error: 'Cash Maximus Flow nicht gefunden'
      });
    }
    
    res.json({
      success: true,
      flow: cashMaximusFlow
    });
  } catch (error) {
    console.error('Fehler beim Abrufen des Cash Maximus Flows:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Abrufen des Cash Maximus Flows'
    });
  }
});

// Upsell Conversion Tracking
router.post('/conversion', async (req, res) => {
  try {
    const { flowId, productId, customerData, conversionType } = req.body;
    
    // Conversion Event tracken
    await upsellService.trackUpsellEvent('conversion', flowId, productId, customerData);
    
    // Analytics Conversion Event
    await analyticsService.trackEvent('upsell_conversion', {
      flowId,
      productId,
      customerData,
      conversionType
    });
    
    res.json({
      success: true,
      message: 'Conversion erfolgreich getrackt'
    });
  } catch (error) {
    console.error('Fehler beim Tracken der Conversion:', error);
    res.status(500).json({
      success: false,
      error: 'Fehler beim Tracken der Conversion'
    });
  }
});

export default router; 