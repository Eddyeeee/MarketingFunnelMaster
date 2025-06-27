import { useState, useEffect } from "react";

interface CountdownTimerProps {
  initialHours?: number;
  initialMinutes?: number;
  initialSeconds?: number;
}

export default function CountdownTimer({ 
  initialHours = 23, 
  initialMinutes = 47, 
  initialSeconds = 32 
}: CountdownTimerProps) {
  const [time, setTime] = useState({
    hours: initialHours,
    minutes: initialMinutes,
    seconds: initialSeconds
  });

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

  const formatNumber = (num: number) => num.toString().padStart(2, '0');

  return (
    <div className="flex justify-center space-x-4 text-2xl font-bold">
      <div className="text-center">
        <div>{formatNumber(time.hours)}</div>
        <div className="text-sm text-current opacity-70">Stunden</div>
      </div>
      <div className="text-center">
        <div>:</div>
        <div className="text-sm opacity-0">-</div>
      </div>
      <div className="text-center">
        <div>{formatNumber(time.minutes)}</div>
        <div className="text-sm text-current opacity-70">Minuten</div>
      </div>
      <div className="text-center">
        <div>:</div>
        <div className="text-sm opacity-0">-</div>
      </div>
      <div className="text-center">
        <div>{formatNumber(time.seconds)}</div>
        <div className="text-sm text-current opacity-70">Sekunden</div>
      </div>
    </div>
  );
}
