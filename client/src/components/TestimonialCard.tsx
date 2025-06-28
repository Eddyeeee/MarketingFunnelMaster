import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Star, CheckCircle, TrendingUp, Clock, DollarSign } from "lucide-react";

interface TestimonialCardProps {
  name: string;
  role: string;
  initials: string;
  rating: number;
  text: string;
  verified?: boolean;
  avatarColor?: string;
  earnings?: string;
  timeframe?: string;
  isRecent?: boolean;
  isTopPerformer?: boolean;
}

export default function TestimonialCard({
  name,
  role,
  initials,
  rating,
  text,
  verified = false,
  avatarColor = "bg-q-primary",
  earnings,
  timeframe,
  isRecent = false,
  isTopPerformer = false
}: TestimonialCardProps) {
  return (
    <Card className="card-psychological hover-lift h-full relative overflow-hidden">
      {/* Top Performer Badge */}
      {isTopPerformer && (
        <div className="absolute top-0 right-0 bg-gradient-to-l from-q-accent to-q-primary text-white px-3 py-1 text-xs font-bold rounded-bl-lg">
          <TrendingUp size={12} className="inline mr-1" />
          Top Performer
        </div>
      )}
      
      {/* Recent Badge */}
      {isRecent && (
        <div className="absolute top-0 left-0 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-3 py-1 text-xs font-bold rounded-br-lg">
          <Clock size={12} className="inline mr-1" />
          Neu
        </div>
      )}
      
      <CardContent className="p-6">
        {/* Header with Avatar and Info */}
        <div className="flex items-center mb-4">
          <div className={`${avatarColor} text-white rounded-full w-12 h-12 flex items-center justify-center mr-4 font-bold shadow-lg`}>
            {initials}
          </div>
          <div className="flex-1">
            <div className="font-semibold text-q-neutral-dark">{name}</div>
            <div className="text-sm text-q-neutral-medium">{role}</div>
            
            {/* Earnings Display */}
            {earnings && (
              <div className="flex items-center space-x-1 mt-1">
                <DollarSign size={14} className="text-success-green" />
                <span className="text-sm font-semibold text-success-green">
                  {earnings}
                </span>
                {timeframe && (
                  <span className="text-xs text-q-neutral-medium">
                    / {timeframe}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
        
        {/* Rating Stars */}
        <div className="text-q-accent mb-4">
          {[...Array(rating)].map((_, i) => (
            <Star key={i} size={16} className="inline fill-current" />
          ))}
          <span className="text-sm text-q-neutral-medium ml-2">
            {rating}/5
          </span>
        </div>
        
        {/* Testimonial Text */}
        <blockquote className="text-q-neutral-medium mb-4 flex-grow text-scannable">
          <span className="text-2xl text-q-accent mr-1">"</span>
          {text}
          <span className="text-2xl text-q-accent ml-1">"</span>
        </blockquote>
        
        {/* Trust Indicators */}
        <div className="flex items-center justify-between">
          {verified && (
            <div className="text-sm text-q-neutral-medium">
              <CheckCircle className="inline text-q-secondary mr-1" size={16} />
              Verifizierter Erfolg
            </div>
          )}
          
          {/* Social Proof */}
          <div className="text-xs text-q-neutral-medium">
            <span className="text-q-accent font-semibold">✓</span> Echte Person
          </div>
        </div>
        
        {/* Psychological Trigger */}
        <div className="mt-3 p-2 bg-gradient-to-r from-q-accent/10 to-q-primary/10 rounded-lg">
          <div className="text-xs text-q-neutral-medium text-center">
            <span className="font-semibold text-q-accent">Erfolgsgarantie:</span> 
            {" "}Diese Ergebnisse sind typisch für unsere Kunden
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
