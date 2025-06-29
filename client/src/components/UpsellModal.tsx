import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Check, X, Star, Clock, Users, Zap } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

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

interface UpsellModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: UpsellProduct;
  personaType?: string;
  leadId?: number;
  onPurchase?: (productId: string) => void;
}

export const UpsellModal: React.FC<UpsellModalProps> = ({
  isOpen,
  onClose,
  product,
  personaType,
  leadId,
  onPurchase
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [timeLeft, setTimeLeft] = useState(300); // 5 Minuten Countdown
  const { toast } = useToast();

  useEffect(() => {
    if (!isOpen) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          onClose();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isOpen, onClose]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handlePurchase = async () => {
    setIsLoading(true);
    
    try {
      // Track Conversion Event
      await fetch('/api/upsell/conversion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          flowId: product.id.includes('qmoney') ? 'qmoney_upsell' : 'cashmaximus_upsell',
          productId: product.id,
          customerData: {
            personaType,
            leadId,
            timestamp: new Date().toISOString()
          },
          conversionType: 'purchase'
        })
      });

      // Weiterleitung zu Digistore24
      window.open(product.digistoreUrl, '_blank');
      
      // Callback aufrufen
      onPurchase?.(product.id);
      
      toast({
        title: "Erfolgreich weitergeleitet!",
        description: "Du wirst jetzt zu Digistore24 weitergeleitet.",
      });
      
      onClose();
    } catch (error) {
      console.error('Fehler beim Kauf:', error);
      toast({
        title: "Fehler beim Kauf",
        description: "Bitte versuche es erneut.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDecline = async () => {
    try {
      // Track Decline Event
      await fetch('/api/upsell/conversion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          flowId: product.id.includes('qmoney') ? 'qmoney_upsell' : 'cashmaximus_upsell',
          productId: product.id,
          customerData: {
            personaType,
            leadId,
            timestamp: new Date().toISOString()
          },
          conversionType: 'decline'
        })
      });
    } catch (error) {
      console.error('Fehler beim Tracken des Ablehnens:', error);
    }
    
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header mit Countdown */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-lg">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold">Exklusives Angebot!</h2>
              <p className="text-blue-100">Nur für dich - begrenzte Zeit</p>
            </div>
            <div className="text-center">
              <div className="text-sm text-blue-100">Verbleibende Zeit</div>
              <div className="text-3xl font-bold text-red-300">
                {formatTime(timeLeft)}
              </div>
            </div>
          </div>
        </div>

        {/* Produkt-Content */}
        <div className="p-6">
          <div className="text-center mb-6">
            <h3 className="text-3xl font-bold text-gray-900 mb-2">
              {product.name}
            </h3>
            <p className="text-lg text-gray-600 mb-4">
              {product.description}
            </p>
            
            {/* Preis */}
            <div className="mb-6">
              <div className="text-4xl font-bold text-green-600">
                {product.price}€
              </div>
              <div className="text-sm text-gray-500">
                Einmalzahlung - Keine versteckten Kosten
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="mb-6">
            <h4 className="text-xl font-semibold mb-4 flex items-center">
              <Zap className="w-5 h-5 mr-2 text-yellow-500" />
              Was du bekommst:
            </h4>
            <div className="space-y-3">
              {product.features.map((feature, index) => (
                <div key={index} className="flex items-start">
                  <Check className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{feature}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Bonus Items */}
          <div className="mb-6">
            <h4 className="text-xl font-semibold mb-4 flex items-center">
              <Star className="w-5 h-5 mr-2 text-yellow-500" />
              Bonus-Materialien (Wert: 297€):
            </h4>
            <div className="space-y-3">
              {product.bonusItems.map((bonus, index) => (
                <div key={index} className="flex items-start">
                  <Check className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{bonus}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Garantie */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mr-3">
                <Check className="w-6 h-6 text-white" />
              </div>
              <div>
                <h5 className="font-semibold text-green-800">30-Tage Geld-zurück-Garantie</h5>
                <p className="text-green-700 text-sm">
                  Du bist zu 100% geschützt. Falls du nicht zufrieden bist, bekommst du dein Geld zurück.
                </p>
              </div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="space-y-3">
            <Button
              onClick={handlePurchase}
              disabled={isLoading}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-4 text-lg font-semibold"
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Weiterleitung...
                </div>
              ) : (
                `Jetzt für ${product.price}€ kaufen`
              )}
            </Button>
            
            <Button
              onClick={handleDecline}
              variant="outline"
              className="w-full py-4 text-lg"
            >
              Nein, danke - Ich verpasse diese Chance
            </Button>
          </div>

          {/* Footer */}
          <div className="text-center mt-6 text-sm text-gray-500">
            <p>Dieses Angebot ist nur für kurze Zeit verfügbar</p>
            <p>Klicke auf "Kaufen" um zu Digistore24 weitergeleitet zu werden</p>
          </div>
        </div>
      </div>
    </div>
  );
}; 