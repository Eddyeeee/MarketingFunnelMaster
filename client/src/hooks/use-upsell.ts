import { useState, useEffect, useCallback } from 'react';
import { useToast } from './use-toast';

interface UpsellProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  digistoreId: string;
  digistoreUrl: string;
  commission: number;
  features: string[];
  bonusItems: string[];
}

interface UpsellFlow {
  id: string;
  name: string;
  products: UpsellProduct[];
  sequence: number;
  conditions: {
    personaType?: string;
    minPurchaseAmount?: number;
    timeDelay?: number;
  };
}

interface UseUpsellProps {
  personaType?: string;
  leadId?: number;
  purchaseAmount?: number;
}

export const useUpsell = ({ personaType, leadId, purchaseAmount = 0 }: UseUpsellProps) => {
  const [upsellFlows, setUpsellFlows] = useState<UpsellFlow[]>([]);
  const [currentFlow, setCurrentFlow] = useState<UpsellFlow | null>(null);
  const [currentProduct, setCurrentProduct] = useState<UpsellProduct | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [purchasedProducts, setPurchasedProducts] = useState<string[]>([]);
  const { toast } = useToast();

  // Upsell Flows laden
  const loadUpsellFlows = useCallback(async () => {
    if (!personaType) return;

    setIsLoading(true);
    try {
      const response = await fetch(`/api/upsell/flows/${personaType}?purchaseAmount=${purchaseAmount}`);
      const data = await response.json();

      if (data.success) {
        setUpsellFlows(data.flows);
        
        // Ersten verfügbaren Flow setzen
        if (data.flows.length > 0) {
          setCurrentFlow(data.flows[0]);
          setCurrentProduct(data.flows[0].products[0]);
        }
      }
    } catch (error) {
      console.error('Fehler beim Laden der Upsell Flows:', error);
      toast({
        title: "Fehler",
        description: "Upsell-Angebote konnten nicht geladen werden.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  }, [personaType, purchaseAmount, toast]);

  // Nächsten Upsell Flow anzeigen
  const showNextUpsell = useCallback(() => {
    if (!currentFlow || !upsellFlows.length) return;

    const currentIndex = upsellFlows.findIndex(flow => flow.id === currentFlow.id);
    const nextIndex = currentIndex + 1;

    if (nextIndex < upsellFlows.length) {
      const nextFlow = upsellFlows[nextIndex];
      setCurrentFlow(nextFlow);
      setCurrentProduct(nextFlow.products[0]);
      return true;
    }

    return false; // Keine weiteren Flows verfügbar
  }, [currentFlow, upsellFlows]);

  // Upsell Modal öffnen
  const openUpsellModal = useCallback((flowId?: string, productId?: string) => {
    if (flowId && productId) {
      const flow = upsellFlows.find(f => f.id === flowId);
      const product = flow?.products.find(p => p.id === productId);
      
      if (flow && product) {
        setCurrentFlow(flow);
        setCurrentProduct(product);
      }
    }

    setIsModalOpen(true);
  }, [upsellFlows]);

  // Upsell Modal schließen
  const closeUpsellModal = useCallback(() => {
    setIsModalOpen(false);
  }, []);

  // Produkt kaufen
  const purchaseProduct = useCallback(async (productId: string) => {
    if (!currentProduct || currentProduct.id !== productId) return;

    try {
      // Produkt als gekauft markieren
      setPurchasedProducts(prev => [...prev, productId]);

      // Event tracken
      await fetch('/api/upsell/track', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          eventType: 'purchase',
          flowId: currentFlow?.id,
          productId,
          customerData: {
            personaType,
            leadId,
            purchaseAmount: currentProduct.price,
            timestamp: new Date().toISOString()
          }
        })
      });

      toast({
        title: "Kauf erfolgreich!",
        description: "Du wirst zu Digistore24 weitergeleitet.",
      });

      // Nächsten Upsell Flow anzeigen
      const hasNextFlow = showNextUpsell();
      
      if (hasNextFlow) {
        // Kurze Verzögerung vor nächstem Upsell
        setTimeout(() => {
          openUpsellModal();
        }, 2000);
      }

    } catch (error) {
      console.error('Fehler beim Kauf:', error);
      toast({
        title: "Fehler beim Kauf",
        description: "Bitte versuche es erneut.",
        variant: "destructive"
      });
    }
  }, [currentProduct, currentFlow, personaType, leadId, showNextUpsell, openUpsellModal, toast]);

  // Upsell ablehnen
  const declineUpsell = useCallback(async () => {
    if (!currentProduct || !currentFlow) return;

    try {
      // Event tracken
      await fetch('/api/upsell/track', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          eventType: 'decline',
          flowId: currentFlow.id,
          productId: currentProduct.id,
          customerData: {
            personaType,
            leadId,
            timestamp: new Date().toISOString()
          }
        })
      });

      // Nächsten Upsell Flow anzeigen
      const hasNextFlow = showNextUpsell();
      
      if (hasNextFlow) {
        // Kurze Verzögerung vor nächstem Upsell
        setTimeout(() => {
          openUpsellModal();
        }, 1000);
      } else {
        closeUpsellModal();
      }

    } catch (error) {
      console.error('Fehler beim Ablehnen:', error);
    }
  }, [currentProduct, currentFlow, personaType, leadId, showNextUpsell, openUpsellModal, closeUpsellModal]);

  // Automatischen Upsell nach Zeitverzögerung starten
  const startAutoUpsell = useCallback((delaySeconds: number = 5) => {
    if (!currentFlow || !currentProduct) return;

    setTimeout(() => {
      openUpsellModal();
    }, delaySeconds * 1000);
  }, [currentFlow, currentProduct, openUpsellModal]);

  // Q-Money spezifischen Upsell laden
  const loadQMoneyUpsell = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/upsell/qmoney');
      const data = await response.json();

      if (data.success) {
        setCurrentFlow(data.flow);
        setCurrentProduct(data.flow.products[0]);
      }
    } catch (error) {
      console.error('Fehler beim Laden des Q-Money Upsells:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Cash Maximus spezifischen Upsell laden
  const loadCashMaximusUpsell = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/upsell/cashmaximus');
      const data = await response.json();

      if (data.success) {
        setCurrentFlow(data.flow);
        setCurrentProduct(data.flow.products[0]);
      }
    } catch (error) {
      console.error('Fehler beim Laden des Cash Maximus Upsells:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Upsell-Statistiken abrufen
  const getUpsellStats = useCallback(async () => {
    try {
      const response = await fetch('/api/upsell/stats');
      const data = await response.json();

      if (data.success) {
        return data.stats;
      }
    } catch (error) {
      console.error('Fehler beim Abrufen der Upsell-Statistiken:', error);
    }
    return null;
  }, []);

  // Initial laden
  useEffect(() => {
    loadUpsellFlows();
  }, [loadUpsellFlows]);

  return {
    // State
    upsellFlows,
    currentFlow,
    currentProduct,
    isModalOpen,
    isLoading,
    purchasedProducts,
    
    // Actions
    loadUpsellFlows,
    openUpsellModal,
    closeUpsellModal,
    purchaseProduct,
    declineUpsell,
    startAutoUpsell,
    showNextUpsell,
    loadQMoneyUpsell,
    loadCashMaximusUpsell,
    getUpsellStats
  };
}; 