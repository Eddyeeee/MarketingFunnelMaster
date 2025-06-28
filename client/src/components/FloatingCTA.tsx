import { useState, useEffect } from "react";
import { Rocket, X, ArrowUp, Users, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";

interface FloatingCTAProps {
  onAction: () => void;
  variant?: 'default' | 'urgent' | 'success';
}

export default function FloatingCTA({ onAction, variant = 'default' }: FloatingCTAProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [showClose, setShowClose] = useState(false);

  useEffect(() => {
    // Show after 3 seconds
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    // Show close button after 10 seconds
    const timer = setTimeout(() => {
      setShowClose(true);
    }, 10000);

    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsVisible(false);
  };

  if (!isVisible) return null;

  const getVariantStyles = () => {
    switch (variant) {
      case 'urgent':
        return {
          bg: 'bg-gradient-to-r from-red-500 to-orange-500',
          text: 'text-white',
          border: 'border-red-400'
        };
      case 'success':
        return {
          bg: 'bg-gradient-to-r from-green-500 to-emerald-500',
          text: 'text-white',
          border: 'border-green-400'
        };
      default:
        return {
          bg: 'bg-gradient-to-r from-q-primary to-q-accent',
          text: 'text-white',
          border: 'border-q-accent'
        };
    }
  };

  const styles = getVariantStyles();

  return (
    <div className={`fixed bottom-4 right-4 z-40 transform transition-all duration-500 ${
      isVisible ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'
    }`}>
      <div className={`${styles.bg} ${styles.text} rounded-lg shadow-2xl border ${styles.border} p-4 max-w-sm`}>
        {/* Close Button */}
        {showClose && (
          <button
            onClick={handleClose}
            className="absolute top-2 right-2 text-white/70 hover:text-white transition-colors"
          >
            <X size={16} />
          </button>
        )}

        {/* Content */}
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <Rocket size={24} className="text-white" />
            </div>
          </div>
          
          <div className="flex-1 min-w-0">
            <h4 className="font-bold text-sm mb-1">
              {variant === 'urgent' ? 'Zeit läuft ab!' : 
               variant === 'success' ? 'Erfolg garantiert!' : 
               'Finanzielle Freiheit wartet!'}
            </h4>
            
            <p className="text-xs opacity-90 mb-2">
              {variant === 'urgent' ? 'Nur noch wenige Plätze verfügbar' :
               variant === 'success' ? 'Über 10.000 Erfolgsgeschichten' :
               'Starte jetzt dein passives Einkommen'}
            </p>

            {/* Social Proof */}
            <div className="flex items-center space-x-3 text-xs opacity-75">
              <div className="flex items-center space-x-1">
                <Users size={12} />
                <span>1.247 online</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock size={12} />
                <span>23:47</span>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Button */}
        <Button
          onClick={onAction}
          className={`w-full mt-3 ${styles.text} bg-white/20 hover:bg-white/30 border border-white/30 transition-all transform hover:scale-105`}
          size="sm"
        >
          <ArrowUp size={16} className="mr-2" />
          Jetzt starten
        </Button>
      </div>
    </div>
  );
} 