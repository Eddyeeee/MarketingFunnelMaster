import { useState, useEffect } from "react";
import { X, Gift, Clock, Shield, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface ExitIntentPopupProps {
  onClose: () => void;
  onAccept: () => void;
  isVisible: boolean;
}

export default function ExitIntentPopup({ onClose, onAccept, isVisible }: ExitIntentPopupProps) {
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    if (isVisible) {
      setShowPopup(true);
    }
  }, [isVisible]);

  const handleClose = () => {
    setShowPopup(false);
    setTimeout(onClose, 300); // Allow animation to complete
  };

  const handleAccept = () => {
    setShowPopup(false);
    setTimeout(onAccept, 300);
  };

  if (!isVisible) return null;

  return (
    <div className={`fixed inset-0 z-50 flex items-center justify-center transition-opacity duration-300 ${
      showPopup ? 'opacity-100' : 'opacity-0'
    }`}>
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={handleClose}
      />
      
      {/* Popup Content */}
      <Card className="relative max-w-md w-full mx-4 transform transition-transform duration-300 ${
        showPopup ? 'scale-100' : 'scale-95'
      }">
        <CardContent className="p-6 text-center">
          {/* Close Button */}
          <button
            onClick={handleClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={20} />
          </button>

          {/* Icon */}
          <div className="mx-auto w-16 h-16 bg-q-accent rounded-full flex items-center justify-center mb-4">
            <Gift size={32} className="text-white" />
          </div>

          {/* Headline */}
          <h3 className="text-2xl font-bold text-q-neutral-dark mb-2">
            Warte! 🎁
          </h3>
          
          <p className="text-lg text-q-neutral-medium mb-4">
            Du bekommst ein <span className="font-bold text-q-accent">kostenloses Geschenk</span>!
          </p>

          {/* Offer Details */}
          <div className="bg-gradient-to-r from-q-accent/10 to-q-primary/10 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <Clock size={16} className="text-q-accent" />
              <span className="text-sm font-semibold text-q-neutral-dark">
                Nur für die nächsten 5 Minuten
              </span>
            </div>
            <p className="text-sm text-q-neutral-medium">
              "Die 7 Geheimnisse der finanziellen Freiheit" - 
              <span className="font-semibold text-q-accent"> Kostenlos für dich!</span>
            </p>
          </div>

          {/* Trust Indicators */}
          <div className="flex items-center justify-center space-x-4 mb-6 text-sm text-q-neutral-medium">
            <div className="flex items-center space-x-1">
              <Shield size={14} className="text-q-secondary" />
              <span>100% kostenlos</span>
            </div>
            <div className="flex items-center space-x-1">
              <Star size={14} className="text-q-accent" />
              <span>4.8/5 Sterne</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="space-y-3">
            <Button 
              onClick={handleAccept}
              className="w-full gradient-cta hover:bg-q-accent-dark text-white py-3 text-lg font-semibold transition-all transform hover:scale-105"
            >
              Ja, ich will das kostenlose Geschenk!
            </Button>
            
            <button
              onClick={handleClose}
              className="w-full text-q-neutral-medium hover:text-q-neutral-dark transition-colors text-sm"
            >
              Nein danke, ich verzichte auf das Geschenk
            </button>
          </div>

          {/* Urgency */}
          <p className="text-xs text-q-neutral-medium mt-4">
            ⚡ Nur noch 3 Plätze verfügbar für das kostenlose Geschenk
          </p>
        </CardContent>
      </Card>
    </div>
  );
} 