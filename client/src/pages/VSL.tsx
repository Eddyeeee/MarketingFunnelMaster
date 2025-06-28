import React, { useState, useEffect } from 'react';
import { useParams, Link } from "wouter";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import VideoPlayer from "@/components/VideoPlayer";
import { LeadCaptureForm } from "@/components/LeadCaptureForm";
import { 
  ArrowLeft, 
  Play, 
  CheckCircle, 
  Star, 
  Crown, 
  DollarSign,
  Zap,
  Clock,
  AlertTriangle,
  Shield,
  TrendingUp
} from "lucide-react";
import { trackEvent, trackConversion } from "@/lib/analytics";
import CountdownTimer from '../components/CountdownTimer';
import LiveVisitorCounter from '../components/LiveVisitorCounter';
import FloatingCTA from '../components/FloatingCTA';
import ExitIntentPopup from '../components/ExitIntentPopup';
import TestimonialCard from '../components/TestimonialCard';
import { useToast } from '../hooks/use-toast';

interface VSLProps {
  product?: 'cash_maximus' | 'q_money';
  videoUrl?: string;
  affiliateUrl?: string;
}

export default function VSL({ 
  product = 'cash_maximus', 
  // HIER DIE ECHTE VIDEO-URL EINFÜGEN:
  // Cash Maximus: https://www.youtube.com/embed/DEINE_VIDEO_ID
  // Q-Money: https://www.youtube.com/embed/DEINE_VIDEO_ID
  videoUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ', // ⚠️ PLACEHOLDER - Ersetze mit echtem Video!
  affiliateUrl = 'https://E-Wolf-Media.short.gy/vsl-cash-maximus'
}: VSLProps) {
  const params = useParams();
  const system = params.system || 'magic-profit';
  const [showVideo, setShowVideo] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [hasWatchedVideo, setHasWatchedVideo] = useState(false);
  const [currentViewers, setCurrentViewers] = useState(47);
  const { toast } = useToast();
  
  const systemData = {
    'magic-profit': {
      title: "Magic Profit System",
      subtitle: "Das bewährte System für 500-1.500€ monatlich",
      description: "Lerne das bewährte System kennen, mit dem bereits über 10.000 Menschen erfolgreich online Geld verdienen.",
      duration: "45 Min",
      views: "127.432",
      badge: "Bestseller",
      badgeColor: "bg-q-secondary",
      benefits: [
        "Sofortiger Start ohne Vorkenntnisse",
        "Bewährtes System mit 97% Erfolgsrate",
        "Vollständige Schritt-für-Schritt Anleitung",
        "Live-Support und Community-Zugang",
        "30-Tage Geld-zurück-Garantie"
      ],
      color: "q-secondary",
      price: "97€",
      originalPrice: "297€",
      savings: "200€",
      testimonials: [
        {
          name: "Sarah M.",
          text: "Ich verdiene jetzt 650€ täglich mit Magic Profit! Unglaublich einfach umzusetzen.",
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
    'money-magnet': {
      title: "Money Magnet System",
      subtitle: "Für ambitionierte Ziele: 2.000-5.000€ monatlich",
      description: "Das erweiterte System für alle, die mehr wollen. Skaliere auf 5.000€+ und baue multiple Einkommensströme auf.",
      duration: "52 Min",
      views: "89.156",
      badge: "Premium",
      badgeColor: "bg-q-primary",
      benefits: [
        "Erweiterte Strategien für höhere Einnahmen",
        "Multiple Einkommensströme aufbauen",
        "Automatisierung und Skalierung",
        "Exklusive Community und Coaching",
        "60-Tage Geld-zurück-Garantie"
      ],
      color: "q-primary",
      price: "147€",
      originalPrice: "347€",
      savings: "200€",
      testimonials: [
        {
          name: "Lisa R.",
          text: "Money Magnet hat mein Leben verändert! Ich verdiene jetzt 2.800€ pro Monat.",
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

  const currentSystem = systemData[system as keyof typeof systemData];

  useEffect(() => {
    // Track VSL page view
    trackEvent('vsl_page_view', 'conversion', product);
    
    // Simulate live viewers
    const interval = setInterval(() => {
      setCurrentViewers(prev => prev + Math.floor(Math.random() * 3) - 1);
    }, 30000);
    
    return () => clearInterval(interval);
  }, [product]);

  const handleVideoStart = () => {
    setShowVideo(true);
    trackEvent('video_started', 'engagement', product);
  };

  const handleVideoEnd = () => {
    setHasWatchedVideo(true);
    setShowLeadForm(true);
    trackEvent('video_completed', 'conversion', product);
  };

  const handleLeadCapture = (data: any) => {
    trackConversion('lead_captured', 1, 'EUR', {
      product,
      source: 'vsl',
      has_watched_video: hasWatchedVideo
    });
    
    toast({
      title: "Perfekt! Du erhältst gleich eine E-Mail.",
      description: "Schau in dein Postfach für deine exklusiven Bonus-Materialien.",
    });
  };

  const handleAffiliateClick = () => {
    trackConversion('affiliate_click', 1, 'EUR', {
      product,
      source: 'vsl',
      has_watched_video: hasWatchedVideo,
      has_lead: showLeadForm
    });
    
    // Öffne Affiliate-Link in neuem Tab
    window.open(affiliateUrl, '_blank');
  };

  const [showExitIntent, setShowExitIntent] = useState(false);
  const [isVideoPlaying, setIsVideoPlaying] = useState(false);
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
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Hauptinhalt - Video & Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Hero Section */}
            <div className="text-center space-y-4">
              <Badge variant="secondary" className="mb-4">
                <AlertTriangle className="h-4 w-4 mr-1" />
                WICHTIG: Nur noch 97 Plätze verfügbar!
              </Badge>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                {currentSystem.title}
              </h1>
              
              <p className="text-xl lg:text-2xl text-blue-600 font-semibold">
                {currentSystem.subtitle}
              </p>
              
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                {currentSystem.description}
              </p>
            </div>

            {/* Video Section */}
            <Card className="overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                <CardTitle className="flex items-center justify-center space-x-2">
                  <Play className="h-6 w-6" />
                  <span>SCHAU DIESES VIDEO BIS ZUM ENDE</span>
                </CardTitle>
                <CardDescription className="text-blue-100 text-center">
                  In diesem Video erfährst du das komplette System - Klicke auf Play!
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                {showVideo ? (
                  <div className="relative aspect-video">
                    <iframe
                      src={videoUrls[currentVideo as 'cashMaximus' | 'qMoney']}
                      className="w-full h-full"
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      onEnded={handleVideoEnd}
                    />
                  </div>
                ) : (
                  <div className="aspect-video bg-gray-900 flex items-center justify-center cursor-pointer" onClick={handleVideoStart}>
                    <div className="text-center text-white">
                      <Play className="h-16 w-16 mx-auto mb-4" />
                      <p className="text-xl font-semibold">Video starten</p>
                      <p className="text-gray-300">Klicke hier um das Video zu sehen</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Lead Capture Section */}
            {showLeadForm && (
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
                    source="vsl"
                    funnel={product}
                    onSuccess={handleLeadCapture}
                    className="max-w-md mx-auto"
                  />
                  <div className="mt-4 text-center text-sm text-green-600">
                    ✓ Sofortiger Download • ✓ Keine Verpflichtungen • ✓ 100% kostenlos
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Features Section */}
            <Card>
              <CardHeader>
                <CardTitle className="text-center text-2xl">
                  Was du mit {currentSystem.title} erhältst:
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  {currentSystem.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                      <span className="text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Testimonials */}
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-center text-gray-900">
                Das sagen unsere Kunden:
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {currentSystem.testimonials.map((testimonial, index) => (
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

          {/* Sidebar - CTA & Pricing */}
          <div className="space-y-6">
            {/* Pricing Card */}
            <Card className="bg-gradient-to-br from-blue-600 to-purple-600 text-white border-0">
              <CardHeader className="text-center">
                <CardTitle className="text-3xl font-bold">
                  {currentSystem.price}
                </CardTitle>
                <CardDescription className="text-blue-100">
                  <span className="line-through text-lg">{currentSystem.originalPrice}</span>
                  <span className="ml-2 text-2xl font-bold text-yellow-300">
                    {currentSystem.savings} gespart!
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
                  onClick={handleAffiliateClick}
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

            {/* Scarcity Card */}
            <Card className="bg-red-50 border-red-200">
              <CardHeader>
                <CardTitle className="text-red-800 text-center">
                  ⚠️ WICHTIG: Nur noch 97 Plätze!
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <div className="bg-red-100 rounded-lg p-4 mb-4">
                  <p className="text-red-800 font-semibold">
                    Bereits {Math.floor(Math.random() * 50) + 150} Menschen haben heute zugegriffen!
                  </p>
                </div>
                <p className="text-sm text-red-700">
                  Das Angebot ist zeitlich begrenzt. Sichere dir jetzt deinen Platz!
                </p>
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
      <FloatingCTA onAction={handleAffiliateClick} />

      {/* Exit Intent Popup */}
      <ExitIntentPopup 
        onClose={() => setShowLeadForm(true)}
        onAccept={handleAffiliateClick}
        isVisible={false}
      />
    </div>
  );
}
