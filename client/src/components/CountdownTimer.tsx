import { useState, useEffect } from "react";
import { Clock, AlertTriangle, Zap } from "lucide-react";

interface CountdownTimerProps {
  initialHours?: number;
  initialMinutes?: number;
  initialSeconds?: number;
  showUrgency?: boolean;
  urgencyThreshold?: number; // minutes before showing urgency
}

export default function CountdownTimer({ 
  initialHours = 23, 
  initialMinutes = 47, 
  initialSeconds = 32,
  showUrgency = true,
  urgencyThreshold = 30
}: CountdownTimerProps) {
  const [time, setTime] = useState({
    hours: initialHours,
    minutes: initialMinutes,
    seconds: initialSeconds
  });

  const [isUrgent, setIsUrgent] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(prevTime => {
        let { hours, minutes, seconds } = prevTime;
        
        seconds--;
        
        if (seconds < 0) {
          seconds = 59;
          minutes--;
          
          if (minutes < 0) {
            minutes = 59;
            hours--;
            
            if (hours < 0) {
              // Reset timer when it reaches zero
              hours = 23;
              minutes = 59;
              seconds = 59;
            }
          }
        }
        
        return { hours, minutes, seconds };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Check for urgency threshold
  useEffect(() => {
    const totalMinutes = time.hours * 60 + time.minutes;
    if (showUrgency && totalMinutes <= urgencyThreshold && !isUrgent) {
      setIsUrgent(true);
    }
  }, [time, showUrgency, urgencyThreshold, isUrgent]);

  const formatNumber = (num: number) => num.toString().padStart(2, '0');

  const totalMinutes = time.hours * 60 + time.minutes;
  const isCritical = totalMinutes <= 5;

  return (
    <div className="text-center">
      {/* Urgency Indicator */}
      {isUrgent && (
        <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg">
          <div className="flex items-center justify-center space-x-2 text-red-400">
            <AlertTriangle size={20} />
            <span className="font-semibold text-sm">
              {isCritical ? 'KRITISCH: Nur noch wenige Minuten!' : 'Zeit läuft ab!'}
            </span>
          </div>
        </div>
      )}

      {/* Timer Display */}
      <div className={`flex justify-center space-x-2 text-2xl font-bold ${
        isCritical ? 'text-red-500 animate-pulse' : 
        isUrgent ? 'text-orange-500' : 'text-q-accent'
      }`}>
        <div className="text-center">
          <div className={`bg-white/10 rounded-lg p-3 min-w-[60px] ${
            isCritical ? 'bg-red-500/20 border border-red-500/50' : 
            isUrgent ? 'bg-orange-500/20 border border-orange-500/50' : 
            'bg-q-accent/20 border border-q-accent/50'
          }`}>
            {formatNumber(time.hours)}
          </div>
          <div className="text-xs text-current opacity-70 mt-1">Stunden</div>
        </div>
        
        <div className="text-center flex items-center">
          <div className="text-3xl font-bold">:</div>
        </div>
        
        <div className="text-center">
          <div className={`bg-white/10 rounded-lg p-3 min-w-[60px] ${
            isCritical ? 'bg-red-500/20 border border-red-500/50' : 
            isUrgent ? 'bg-orange-500/20 border border-orange-500/50' : 
            'bg-q-accent/20 border border-q-accent/50'
          }`}>
            {formatNumber(time.minutes)}
          </div>
          <div className="text-xs text-current opacity-70 mt-1">Minuten</div>
        </div>
        
        <div className="text-center flex items-center">
          <div className="text-3xl font-bold">:</div>
        </div>
        
        <div className="text-center">
          <div className={`bg-white/10 rounded-lg p-3 min-w-[60px] ${
            isCritical ? 'bg-red-500/20 border border-red-500/50' : 
            isUrgent ? 'bg-orange-500/20 border border-orange-500/50' : 
            'bg-q-accent/20 border border-q-accent/50'
          }`}>
            {formatNumber(time.seconds)}
          </div>
          <div className="text-xs text-current opacity-70 mt-1">Sekunden</div>
        </div>
      </div>

      {/* Urgency Message */}
      {isUrgent && (
        <div className="mt-4 text-sm text-white/90">
          <div className="flex items-center justify-center space-x-2">
            <Zap size={16} className="text-q-accent" />
            <span>
              {isCritical 
                ? 'Nur noch wenige Plätze verfügbar!' 
                : 'Angebot läuft bald ab - Jetzt handeln!'
              }
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
