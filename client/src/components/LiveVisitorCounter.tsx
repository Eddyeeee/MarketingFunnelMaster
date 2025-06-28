import { useState, useEffect } from "react";
import { Users, Eye, TrendingUp } from "lucide-react";

interface LiveVisitorCounterProps {
  baseCount?: number;
  updateInterval?: number;
  showTrending?: boolean;
}

export default function LiveVisitorCounter({ 
  baseCount = 1247, 
  updateInterval = 3000,
  showTrending = true 
}: LiveVisitorCounterProps) {
  const [visitorCount, setVisitorCount] = useState<number>(baseCount);
  const [recentSignups, setRecentSignups] = useState<number>(0);

  useEffect(() => {
    const visitorTimer = setInterval(() => {
      // Simulate live visitor updates
      const increment = Math.floor(Math.random() * 3) + 1;
      setVisitorCount((prev: number) => prev + increment);
    }, updateInterval);

    const signupTimer = setInterval(() => {
      // Simulate recent signups
      if (Math.random() < 0.3) { // 30% chance every 3 seconds
        setRecentSignups((prev: number) => prev + 1);
      }
    }, updateInterval);

    return () => {
      clearInterval(visitorTimer);
      clearInterval(signupTimer);
    };
  }, [updateInterval]);

  return (
    <div className="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-6 bg-white/10 rounded-lg p-4 backdrop-blur-sm">
      <div className="flex items-center space-x-2">
        <Eye className="text-q-accent" size={20} />
        <span className="text-sm font-medium text-white">
          <span className="font-bold">{visitorCount.toLocaleString()}</span> Menschen online
        </span>
        {showTrending && (
          <span className="inline-flex items-center rounded-full bg-q-accent text-white text-xs px-2 py-1 font-semibold">
            <TrendingUp size={12} className="mr-1" />
            Live
          </span>
        )}
      </div>
      
      {recentSignups > 0 && (
        <div className="flex items-center space-x-2 text-q-accent">
          <Users size={16} />
          <span className="text-sm font-medium">
            <span className="font-bold">{recentSignups}</span> haben sich gerade angemeldet
          </span>
        </div>
      )}
    </div>
  );
} 