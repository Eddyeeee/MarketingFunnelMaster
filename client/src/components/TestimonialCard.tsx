import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Star, CheckCircle } from "lucide-react";

interface TestimonialCardProps {
  name: string;
  role: string;
  initials: string;
  rating: number;
  text: string;
  verified?: boolean;
  avatarColor?: string;
}

export default function TestimonialCard({
  name,
  role,
  initials,
  rating,
  text,
  verified = false,
  avatarColor = "bg-q-primary"
}: TestimonialCardProps) {
  return (
    <Card className="shadow-lg h-full">
      <CardContent className="p-6">
        <div className="flex items-center mb-4">
          <div className={`${avatarColor} text-white rounded-full w-12 h-12 flex items-center justify-center mr-4 font-bold`}>
            {initials}
          </div>
          <div>
            <div className="font-semibold text-q-neutral-dark">{name}</div>
            <div className="text-sm text-q-neutral-medium">{role}</div>
          </div>
        </div>
        
        <div className="text-q-accent mb-4">
          {[...Array(rating)].map((_, i) => (
            <Star key={i} size={16} className="inline fill-current" />
          ))}
        </div>
        
        <p className="text-q-neutral-medium mb-4 flex-grow">
          "{text}"
        </p>
        
        {verified && (
          <div className="text-sm text-q-neutral-medium">
            <CheckCircle className="inline text-q-secondary mr-1" size={16} />
            Verifizierter Erfolg
          </div>
        )}
      </CardContent>
    </Card>
  );
}
