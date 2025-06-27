import { useParams, Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import VideoPlayer from "@/components/VideoPlayer";
import LeadCaptureForm from "@/components/LeadCaptureForm";
import { ArrowLeft, Play, CheckCircle, Star, Crown } from "lucide-react";
import { trackEvent } from "@/lib/analytics";

export default function VSL() {
  const params = useParams();
  const system = params.system || 'magic-profit';
  
  const systemData = {
    'magic-profit': {
      title: 'Magic Profit System',
      subtitle: 'Für Einsteiger: Von 0€ zu 2.000€ passivem Einkommen',
      description: 'Das perfekte System für alle, die ohne Vorkenntnisse und ohne Startkapital ihr erstes passives Einkommen aufbauen möchten.',
      duration: '45 Minuten',
      views: '150.000+ Aufrufe',
      badge: 'BESTSELLER',
      badgeColor: 'bg-q-accent',
      benefits: [
        'Schritt-für-Schritt Anleitung',
        '0€ Startkapital erforderlich',
        'Erste Ergebnisse in 30 Tagen',
        'Bonus: E-Mail-Funnel-Templates'
      ],
      color: 'q-primary'
    },
    'money-magnet': {
      title: 'Money Magnet System',
      subtitle: 'Für Fortgeschrittene: Skalierung auf 5.000€+',
      description: 'Das erweiterte System für alle, die bereits erste Erfahrungen gesammelt haben und ihr Einkommen auf das nächste Level bringen möchten.',
      duration: '52 Minuten',
      views: '95.000+ Aufrufe',
      badge: 'PREMIUM',
      badgeColor: 'bg-q-secondary',
      benefits: [
        'Skalierung auf 5.000€+',
        'Automatisierte Systeme',
        'Multiple Einkommensquellen',
        'Bonus: KI-Automatisierung'
      ],
      color: 'q-secondary'
    }
  };

  const currentSystem = systemData[system as keyof typeof systemData];

  const handleVideoPlay = () => {
    trackEvent('vsl_video_play', 'engagement', `${system}_page`);
  };

  const handleLeadCapture = (leadData: any) => {
    trackEvent('vsl_lead_capture', 'conversion', `${system}_page`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <Link href="/">
                <Button variant="ghost" className="flex items-center space-x-2">
                  <ArrowLeft size={20} />
                  <span>Zurück</span>
                </Button>
              </Link>
              <div className="flex-shrink-0">
                <span className="text-2xl font-bold text-q-primary">Q-Money</span>
                <span className="text-lg font-medium text-q-neutral-medium ml-2">VSL</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* VSL Content */}
      <section className="py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex justify-center items-center space-x-3 mb-4">
              <h1 className="text-3xl md:text-4xl font-bold text-q-neutral-dark">
                {currentSystem.title}
              </h1>
              <Badge className={`${currentSystem.badgeColor} text-white`}>
                {currentSystem.badge}
              </Badge>
            </div>
            <p className="text-xl text-q-neutral-medium mb-2">
              {currentSystem.subtitle}
            </p>
            <p className="text-lg text-q-neutral-medium max-w-3xl mx-auto">
              {currentSystem.description}
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Video Player */}
            <div className="lg:col-span-2">
              <Card className="shadow-lg mb-8">
                <CardContent className="p-6">
                  <VideoPlayer
                    title={currentSystem.title}
                    description={currentSystem.subtitle}
                    duration={currentSystem.duration}
                    views={currentSystem.views}
                    videoId={system}
                    onPlay={handleVideoPlay}
                    size="large"
                  />
                </CardContent>
              </Card>

              {/* Benefits */}
              <Card className="shadow-lg">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-q-neutral-dark mb-4">
                    Was du in diesem Video lernst:
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {currentSystem.benefits.map((benefit, index) => (
                      <div key={index} className="flex items-center space-x-3">
                        <CheckCircle className="text-q-secondary flex-shrink-0" size={20} />
                        <span className="text-q-neutral-dark">{benefit}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Lead Capture Sidebar */}
            <div className="lg:col-span-1">
              <Card className="shadow-lg sticky top-8">
                <CardContent className="p-6">
                  <div className="text-center mb-6">
                    <div className={`bg-${currentSystem.color} text-white rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4`}>
                      {system === 'magic-profit' ? <Star size={24} /> : <Crown size={24} />}
                    </div>
                    <h3 className="text-xl font-bold text-q-neutral-dark mb-2">
                      Kostenlosen Zugang sichern
                    </h3>
                    <p className="text-q-neutral-medium text-sm">
                      Erhalte sofortigen Zugriff auf das komplette System + Bonus-Material
                    </p>
                  </div>

                  <LeadCaptureForm 
                    funnel={system}
                    source="vsl"
                    onSubmit={handleLeadCapture}
                  />

                  <div className="mt-6 space-y-3 text-sm text-q-neutral-medium">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="text-q-secondary" size={16} />
                      <span>100% kostenlos</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="text-q-secondary" size={16} />
                      <span>Keine Verpflichtungen</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="text-q-secondary" size={16} />
                      <span>Sofortiger Zugang</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Additional Resources */}
              <Card className="shadow-lg mt-6">
                <CardContent className="p-6">
                  <h4 className="font-semibold text-q-neutral-dark mb-4">
                    Weitere Ressourcen
                  </h4>
                  <div className="space-y-3">
                    <Link href="/bridge">
                      <Button variant="outline" className="w-full justify-start">
                        Alle Funnels ansehen
                      </Button>
                    </Link>
                    <Link href="/tsl">
                      <Button variant="outline" className="w-full justify-start">
                        Text Sales Letter
                      </Button>
                    </Link>
                    <Link href="/quiz">
                      <Button variant="outline" className="w-full justify-start">
                        Persönlichen Test machen
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
