import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { useToast } from '../hooks/use-toast';
import { useAnalytics } from '../hooks/use-analytics';

interface PaymentFormProps {
  personaType: string;
  leadId?: number;
  leadData?: any;
  onSuccess?: (paymentData: any) => void;
  onError?: (error: any) => void;
}

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  features: string[];
  bonusItems: string[];
}

interface PaymentMethod {
  id: string;
  name: string;
  description: string;
  icon: string;
  enabled: boolean;
}

export const PaymentForm: React.FC<PaymentFormProps> = ({
  personaType,
  leadId,
  leadData,
  onSuccess,
  onError
}) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [selectedMethod, setSelectedMethod] = useState<string>('card');
  const [loading, setLoading] = useState(false);
  const [paymentIntent, setPaymentIntent] = useState<any>(null);
  const [showSpecialOffer, setShowSpecialOffer] = useState(false);
  const [timeLeft, setTimeLeft] = useState(3600); // 1 Stunde in Sekunden
  const [cardData, setCardData] = useState({
    number: '',
    expiry: '',
    cvc: '',
    name: ''
  });

  const { toast } = useToast();
  const { trackEvent } = useAnalytics();

  useEffect(() => {
    loadProducts();
    loadPaymentMethods();
    
    // Countdown Timer
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [personaType]);

  // Zeige spezielles Angebot nach 30 Sekunden
  useEffect(() => {
    const offerTimer = setTimeout(() => {
      setShowSpecialOffer(true);
    }, 30000);

    return () => clearTimeout(offerTimer);
  }, []);

  const loadProducts = async () => {
    try {
      const response = await fetch(`/api/payment/products/${personaType}`);
      const data = await response.json();
      
      if (data.success) {
        setProducts(data.products);
        if (data.products.length > 0) {
          setSelectedProduct(data.products[0]);
        }
      }
    } catch (error) {
      console.error('Produkte laden fehlgeschlagen:', error);
    }
  };

  const loadPaymentMethods = async () => {
    try {
      const response = await fetch('/api/payment/payment-methods');
      const data = await response.json();
      
      if (data.success) {
        setPaymentMethods(data.paymentMethods);
      }
    } catch (error) {
      console.error('Zahlungsmethoden laden fehlgeschlagen:', error);
    }
  };

  const createPaymentIntent = async () => {
    if (!selectedProduct || !leadData?.email) {
      toast({
        title: "Fehler",
        description: "Bitte wähle ein Produkt und gib deine E-Mail-Adresse ein.",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    
    try {
      const paymentData = {
        amount: selectedProduct.price,
        currency: selectedProduct.currency,
        personaType,
        leadId,
        email: leadData.email,
        firstName: leadData.firstName,
        lastName: leadData.lastName,
        paymentMethod: selectedMethod,
        metadata: {
          productId: selectedProduct.id,
          personaType
        }
      };

      const response = await fetch('/api/payment/create-payment-intent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(paymentData)
      });

      const data = await response.json();

      if (data.success) {
        setPaymentIntent(data.paymentIntent);
        trackEvent('payment_intent_created', {
          productId: selectedProduct.id,
          amount: selectedProduct.price,
          personaType
        });
      } else {
        throw new Error(data.message);
      }
    } catch (error) {
      console.error('Payment Intent Erstellung fehlgeschlagen:', error);
      toast({
        title: "Zahlungsfehler",
        description: "Die Zahlung konnte nicht initialisiert werden. Bitte versuche es erneut.",
        variant: "destructive"
      });
      onError?.(error);
    } finally {
      setLoading(false);
    }
  };

  const createCheckoutSession = async () => {
    if (!selectedProduct || !leadData?.email) {
      toast({
        title: "Fehler",
        description: "Bitte wähle ein Produkt und gib deine E-Mail-Adresse ein.",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    
    try {
      const paymentData = {
        amount: selectedProduct.price,
        currency: selectedProduct.currency,
        personaType,
        leadId,
        email: leadData.email,
        firstName: leadData.firstName,
        lastName: leadData.lastName,
        paymentMethod: selectedMethod,
        metadata: {
          productId: selectedProduct.id,
          personaType
        }
      };

      const response = await fetch('/api/payment/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(paymentData)
      });

      const data = await response.json();

      if (data.success) {
        // Weiterleitung zur Stripe Checkout-Seite
        window.location.href = data.checkoutUrl;
        trackEvent('checkout_session_created', {
          productId: selectedProduct.id,
          amount: selectedProduct.price,
          personaType
        });
      } else {
        throw new Error(data.message);
      }
    } catch (error) {
      console.error('Checkout Session Erstellung fehlgeschlagen:', error);
      toast({
        title: "Zahlungsfehler",
        description: "Die Zahlung konnte nicht initialisiert werden. Bitte versuche es erneut.",
        variant: "destructive"
      });
      onError?.(error);
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async () => {
    if (selectedMethod === 'card') {
      await createPaymentIntent();
    } else {
      await createCheckoutSession();
    }
  };

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: currency.toUpperCase()
    }).format(price);
  };

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getSpecialOffer = () => {
    switch (personaType) {
      case 'student':
        return {
          title: '🎓 Exklusiver Studenten-Rabatt!',
          description: 'Nur noch 24 Stunden: 50% Rabatt auf Premium!',
          originalPrice: 197,
          discountedPrice: 97,
          savings: 100
        };
      case 'employee':
        return {
          title: '💼 Business-Frühbucher-Rabatt!',
          description: 'Nur noch 12 Stunden: 30% Rabatt auf Premium!',
          originalPrice: 397,
          discountedPrice: 277,
          savings: 120
        };
      case 'parent':
        return {
          title: '👨‍👩‍👧‍👦 Familien-Frühbucher-Rabatt!',
          description: 'Nur noch 18 Stunden: 25% Rabatt auf Premium!',
          originalPrice: 297,
          discountedPrice: 222,
          savings: 75
        };
      default:
        return null;
    }
  };

  const specialOffer = getSpecialOffer();

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Countdown Timer */}
      {timeLeft > 0 && (
        <Card className="bg-gradient-to-r from-red-500 to-orange-500 text-white">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold mb-2">⏰ Angebot läuft ab!</div>
            <div className="text-4xl font-mono font-bold mb-2">
              {formatTime(timeLeft)}
            </div>
            <div className="text-sm opacity-90">
              Sichere dir jetzt dein exklusives Angebot!
            </div>
          </CardContent>
        </Card>
      )}

      {/* Spezielles Angebot */}
      {showSpecialOffer && specialOffer && (
        <Card className="bg-gradient-to-r from-yellow-400 to-orange-500 border-4 border-yellow-300 animate-pulse">
          <CardContent className="p-6 text-center">
            <h2 className="text-2xl font-bold text-white mb-2">
              {specialOffer.title}
            </h2>
            <p className="text-white mb-4">{specialOffer.description}</p>
            <div className="flex justify-center items-center space-x-4 mb-4">
              <span className="text-3xl font-bold text-white line-through">
                {formatPrice(specialOffer.originalPrice, 'eur')}
              </span>
              <span className="text-4xl font-bold text-white">
                {formatPrice(specialOffer.discountedPrice, 'eur')}
              </span>
            </div>
            <div className="text-white font-semibold">
              Du sparst {formatPrice(specialOffer.savings, 'eur')}!
            </div>
          </CardContent>
        </Card>
      )}

      {/* Produktauswahl */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            🎯 Wähle dein Magic Tool Paket
          </CardTitle>
          <CardDescription className="text-center">
            Personalisiert für {personaType === 'student' ? 'Studenten' : 
                              personaType === 'employee' ? 'Angestellte' : 'Eltern'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            {products.map((product) => (
              <Card
                key={product.id}
                className={`cursor-pointer transition-all ${
                  selectedProduct?.id === product.id
                    ? 'ring-2 ring-blue-500 bg-blue-50'
                    : 'hover:shadow-lg'
                }`}
                onClick={() => setSelectedProduct(product)}
              >
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg">{product.name}</CardTitle>
                      <CardDescription>{product.description}</CardDescription>
                    </div>
                    <Badge variant="secondary" className="text-lg font-bold">
                      {formatPrice(product.price, product.currency)}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-semibold text-sm text-gray-700 mb-2">
                        ✅ Was du bekommst:
                      </h4>
                      <ul className="space-y-1">
                        {product.features.map((feature, index) => (
                          <li key={index} className="text-sm text-gray-600">
                            • {feature}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold text-sm text-green-700 mb-2">
                        🎁 Bonus-Materialien:
                      </h4>
                      <ul className="space-y-1">
                        {product.bonusItems.map((bonus, index) => (
                          <li key={index} className="text-sm text-green-600">
                            • {bonus}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Garantie-Box */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <CardContent className="p-6">
          <div className="flex items-center space-x-4">
            <div className="text-4xl">🛡️</div>
            <div>
              <h3 className="text-lg font-bold text-green-800">30-Tage Geld-zurück-Garantie</h3>
              <p className="text-green-700">
                Du bist nicht zufrieden? Du bekommst dein Geld zurück - ohne Fragen!
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Zahlungsmethoden */}
      <Card>
        <CardHeader>
          <CardTitle>💳 Zahlungsmethode wählen</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-4">
            {paymentMethods.map((method) => (
              <Card
                key={method.id}
                className={`cursor-pointer transition-all ${
                  selectedMethod === method.id
                    ? 'ring-2 ring-blue-500 bg-blue-50'
                    : 'hover:shadow-md'
                } ${!method.enabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                onClick={() => method.enabled && setSelectedMethod(method.id)}
              >
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{method.icon}</span>
                    <div>
                      <h4 className="font-semibold">{method.name}</h4>
                      <p className="text-sm text-gray-600">{method.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Kreditkarten-Formular */}
      {selectedMethod === 'card' && (
        <Card>
          <CardHeader>
            <CardTitle>💳 Kreditkarten-Daten</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <Label htmlFor="cardName">Name auf der Karte</Label>
                <Input
                  id="cardName"
                  value={cardData.name}
                  onChange={(e) => setCardData({ ...cardData, name: e.target.value })}
                  placeholder="Max Mustermann"
                />
              </div>
              <div className="md:col-span-2">
                <Label htmlFor="cardNumber">Kartennummer</Label>
                <Input
                  id="cardNumber"
                  value={cardData.number}
                  onChange={(e) => setCardData({ ...cardData, number: e.target.value })}
                  placeholder="1234 5678 9012 3456"
                />
              </div>
              <div>
                <Label htmlFor="cardExpiry">Ablaufdatum</Label>
                <Input
                  id="cardExpiry"
                  value={cardData.expiry}
                  onChange={(e) => setCardData({ ...cardData, expiry: e.target.value })}
                  placeholder="MM/YY"
                />
              </div>
              <div>
                <Label htmlFor="cardCvc">CVC</Label>
                <Input
                  id="cardCvc"
                  value={cardData.cvc}
                  onChange={(e) => setCardData({ ...cardData, cvc: e.target.value })}
                  placeholder="123"
                />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Zusammenfassung */}
      {selectedProduct && (
        <Card className="bg-gradient-to-r from-blue-50 to-green-50">
          <CardHeader>
            <CardTitle className="text-center">📋 Bestellübersicht</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="font-semibold">{selectedProduct.name}</span>
                <span className="font-bold text-lg">
                  {formatPrice(selectedProduct.price, selectedProduct.currency)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span>Zahlungsmethode</span>
                <span className="flex items-center space-x-2">
                  <span>{paymentMethods.find(m => m.id === selectedMethod)?.icon}</span>
                  <span>{paymentMethods.find(m => m.id === selectedMethod)?.name}</span>
                </span>
              </div>
              <hr />
              <div className="flex justify-between items-center text-lg font-bold">
                <span>Gesamtbetrag</span>
                <span className="text-green-600">
                  {formatPrice(selectedProduct.price, selectedProduct.currency)}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Zahlungsbutton */}
      <div className="text-center">
        <Button
          onClick={handlePayment}
          disabled={!selectedProduct || loading}
          size="lg"
          className="bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white font-bold py-4 px-8 text-lg"
        >
          {loading ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Zahlung wird verarbeitet...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <span>🚀 Jetzt kaufen & sofort starten!</span>
            </div>
          )}
        </Button>
        
        <p className="text-sm text-gray-600 mt-4">
          🔒 Sichere Zahlung über Stripe • 30-Tage Geld-zurück-Garantie
        </p>
      </div>

      {/* Payment Intent Status */}
      {paymentIntent && (
        <Card className="bg-green-50 border-green-200">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="text-green-800">
                Zahlung initialisiert! Client Secret: {paymentIntent.clientSecret.substring(0, 20)}...
              </span>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}; 