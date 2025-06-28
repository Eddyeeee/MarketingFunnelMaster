import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { LeadCaptureForm } from '../components/LeadCaptureForm';
import CountdownTimer from '../components/CountdownTimer';
import LiveVisitorCounter from '../components/LiveVisitorCounter';
import FloatingCTA from '../components/FloatingCTA';
import ExitIntentPopup from '../components/ExitIntentPopup';
import TestimonialCard from '../components/TestimonialCard';
import { trackEvent, trackConversion } from '../lib/analytics';
import { useToast } from '../hooks/use-toast';
import { 
  Play, 
  Clock, 
  Users, 
  Star, 
  CheckCircle, 
  ArrowRight, 
  Zap,
  Shield,
  TrendingUp,
  DollarSign,
  AlertTriangle,
  Video
} from 'lucide-react';

interface LandingProps {
  product?: 'cash_maximus' | 'q_money';
  affiliateUrl?: string;
}

export default function Landing({ 
  product = 'cash_maximus', 
  affiliateUrl = 'https://E-Wolf-Media.short.gy/vsl-cash-maximus'
}: LandingProps) {
  const [showExitIntent, setShowExitIntent] = useState(false);
  const [isVideoPlaying, setIsVideoPlaying] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [remainingAccess, setRemainingAccess] = useState(97);
  const [timeLeft, setTimeLeft] = useState({
    hours: 3,
    minutes: 3,
    seconds: 3
  });

  // Echte Video-URLs von den Affiliate-Links
  const videoUrls = {
    cashMaximus: "https://video.funnelcockpit.com/video/user/YmvEcadc9R9xLFzPC/video-player/dD8YEqg4htWNMwaYC/1080p.mp4",
    qMoney: "https://video.funnelcockpit.com/video/user/jqb5HDNGJbYRDydhK/video-player/krq7y8o4WREHtoJpN/1080p.mp4"
  };

  const [currentVideo, setCurrentVideo] = useState<'cashMaximus' | 'qMoney'>('cashMaximus');
  const { toast } = useToast();

  // Produkt-spezifische Daten
  const productData = {
    cash_maximus: {
      title: "Cash Maximus 2.0",
      subtitle: "Das legale System für 500-750€ täglich",
      description: "Entdecke das einzigartige Verfahren, mit dem du legal und seriös online Geld verdienen kannst.",
      price: "97€",
      originalPrice: "297€",
      savings: "200€",
      features: [
        "Sofortiger Zugang zum kompletten System",
        "Schritt-für-Schritt Anleitung",
        "Live-Support und Community",
        "30-Tage Geld-zurück-Garantie",
        "Exklusive Bonus-Materialien"
      ],
      testimonials: [
        {
          name: "Sarah M.",
          text: "Ich verdiene jetzt 650€ täglich mit Cash Maximus! Unglaublich einfach umzusetzen.",
          rating: 5,
          role: "Studentin",
          initials: "SM"
        },
        {
          name: "Michael K.",
          text: "Endlich finanzielle Freiheit! Das System funktioniert wirklich wie beschrieben.",
          rating: 5,
          role: "Angestellter",
          initials: "MK"
        }
      ]
    },
    q_money: {
      title: "Q-Money System",
      subtitle: "Das einzigartige Bild bringt täglich 550€+",
      description: "Lerne das Geheimnis hinter dem aktuellen Internet-Hype kennen.",
      price: "147€",
      originalPrice: "347€",
      savings: "200€",
      features: [
        "Das exklusive Bild-System",
        "Vollständige Anleitung",
        "Live-Coaching-Sessions",
        "60-Tage Geld-zurück-Garantie",
        "Premium-Bonus-Paket"
      ],
      testimonials: [
        {
          name: "Lisa R.",
          text: "Q-Money hat mein Leben verändert! Ich verdiene jetzt 580€ pro Tag.",
          rating: 5,
          role: "Selbstständige",
          initials: "LR"
        },
        {
          name: "Thomas B.",
          text: "Einfach genial! Das System ist so einfach und bringt sofort Ergebnisse.",
          rating: 5,
          role: "Vater",
          initials: "TB"
        }
      ]
    }
  };

  const currentProduct = productData[product];

  const handleLeadCapture = (data: any) => {
    setShowLeadForm(true);
    trackConversion('lead_captured', 1, 'EUR', {
      product,
      source: 'landing',
      has_lead: true
    });
    
    toast({
      title: "Perfekt! Du erhältst gleich eine E-Mail.",
      description: "Schau in dein Postfach für deine exklusiven Bonus-Materialien.",
    });
  };

  const handleVideoClick = () => {
    trackConversion('video_click', 1, 'EUR', {
      product,
      source: 'landing',
      has_lead: showLeadForm
    });
    
    // Öffne Affiliate-Link in neuem Tab
    window.open(affiliateUrl, '_blank');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Zap className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">E-Wolf Media</span>
            </div>
            <div className="flex items-center space-x-4">
              <LiveVisitorCounter />
              <Badge variant="destructive" className="animate-pulse">
                <Clock className="h-4 w-4 mr-1" />
                <CountdownTimer />
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Linke Seite - Content */}
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="space-y-6">
              <Badge variant="secondary" className="mb-4">
                <AlertTriangle className="h-4 w-4 mr-1" />
                WICHTIG: Nur noch 97 Plätze verfügbar!
              </Badge>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                {currentProduct.title}
              </h1>
              
              <p className="text-xl lg:text-2xl text-blue-600 font-semibold">
                {currentProduct.subtitle}
              </p>
              
              <p className="text-lg text-gray-600">
                {currentProduct.description}
              </p>
            </div>

            {/* Features */}
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">
                Was du erhältst:
              </h2>
              <div className="space-y-3">
                {currentProduct.features.map((feature, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{feature}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Testimonials */}
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">
                Das sagen unsere Kunden:
              </h2>
              <div className="space-y-4">
                {currentProduct.testimonials.map((testimonial, index) => (
                  <TestimonialCard
                    key={index}
                    name={testimonial.name}
                    text={testimonial.text}
                    rating={testimonial.rating}
                    role={testimonial.role}
                    initials={testimonial.initials}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Rechte Seite - CTA & Video */}
          <div className="space-y-6">
            {/* Video Preview */}
            <Card className="overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                <CardTitle className="flex items-center justify-center space-x-2">
                  <Video className="h-6 w-6" />
                  <span>EXKLUSIVES VIDEO</span>
                </CardTitle>
                <CardDescription className="text-blue-100 text-center">
                  Schau dir das komplette System im Detail an
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="aspect-video bg-gray-900 flex items-center justify-center cursor-pointer" onClick={handleVideoClick}>
                  <div className="text-center text-white">
                    <Play className="h-16 w-16 mx-auto mb-4" />
                    <p className="text-xl font-semibold">Video ansehen</p>
                    <p className="text-gray-300">Klicke hier um das Video zu starten</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Lead Capture */}
            <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
              <CardHeader>
                <CardTitle className="text-center text-green-800">
                  🎉 GRATIS BONUS: Sichere dir jetzt deine exklusiven Materialien!
                </CardTitle>
                <CardDescription className="text-center text-green-700">
                  Du erhältst sofort Zugang zu unserem kostenlosen Starter-Guide und exklusiven Tipps.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <LeadCaptureForm
                  title="Kostenlose Bonus-Materialien sichern"
                  description="Gib deine E-Mail-Adresse ein und erhalte sofort:"
                  buttonText="Jetzt kostenlos sichern"
                  source="landing"
                  funnel={product}
                  onSuccess={handleLeadCapture}
                  className="max-w-md mx-auto"
                />
                <div className="mt-4 text-center text-sm text-green-600">
                  ✓ Sofortiger Download • ✓ Keine Verpflichtungen • ✓ 100% kostenlos
                </div>
              </CardContent>
            </Card>

            {/* Pricing Card */}
            <Card className="bg-gradient-to-br from-blue-600 to-purple-600 text-white border-0">
              <CardHeader className="text-center">
                <CardTitle className="text-3xl font-bold">
                  {currentProduct.price}
                </CardTitle>
                <CardDescription className="text-blue-100">
                  <span className="line-through text-lg">{currentProduct.originalPrice}</span>
                  <span className="ml-2 text-2xl font-bold text-yellow-300">
                    {currentProduct.savings} gespart!
                  </span>
                </CardDescription>
              </CardHeader>
              <CardContent className="text-center space-y-4">
                <div className="bg-white/10 rounded-lg p-4">
                  <p className="text-sm text-blue-100">
                    ⏰ Angebot läuft ab in:
                  </p>
                  <CountdownTimer />
                </div>
                
                <Button 
                  onClick={handleVideoClick}
                  className="w-full bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-4 text-lg"
                  size="lg"
                >
                  <DollarSign className="h-5 w-5 mr-2" />
                  JETZT ZUGANG SICHERN
                </Button>
                
                <div className="text-xs text-blue-100 space-y-1">
                  <p>✓ 30-Tage Geld-zurück-Garantie</p>
                  <p>✓ Sofortiger Zugang</p>
                  <p>✓ Live-Support inklusive</p>
                </div>
              </CardContent>
            </Card>

            {/* Trust Badges */}
            <Card>
              <CardContent className="text-center space-y-4 pt-6">
                <div className="flex justify-center space-x-4">
                  <Shield className="h-8 w-8 text-green-500" />
                  <TrendingUp className="h-8 w-8 text-blue-500" />
                  <Star className="h-8 w-8 text-yellow-500" />
                </div>
                <p className="text-sm text-gray-600">
                  ✓ 100% seriös und legal<br/>
                  ✓ Über 10.000 zufriedene Kunden<br/>
                  ✓ 30-Tage Geld-zurück-Garantie
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Floating CTA */}
      <FloatingCTA onAction={handleVideoClick} />

      {/* Exit Intent Popup */}
      <ExitIntentPopup 
        onClose={() => setShowLeadForm(true)}
        onAccept={handleVideoClick}
        isVisible={false}
      />
    </div>
  );
} 