import { useState, useEffect } from "react";
import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users, Star, Shield, Clock, Play, CheckCircle, Trophy, Lightbulb, Rocket, TrendingUp, Zap, Gift } from "lucide-react";
import QuizForm from "@/components/QuizForm";
import VideoPlayer from "@/components/VideoPlayer";
import CountdownTimer from "@/components/CountdownTimer";
import TestimonialCard from "@/components/TestimonialCard";
import LiveVisitorCounter from "@/components/LiveVisitorCounter";
import ExitIntentPopup from "@/components/ExitIntentPopup";
import FloatingCTA from "@/components/FloatingCTA";
import { trackEvent } from "@/lib/analytics";

export default function Home() {
  const [showQuiz, setShowQuiz] = useState(false);
  const [showExitPopup, setShowExitPopup] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);

  // Exit intent detection
  useEffect(() => {
    const handleMouseLeave = (e: MouseEvent) => {
      if (e.clientY <= 0 && !hasInteracted && !showExitPopup) {
        setShowExitPopup(true);
        trackEvent('exit_intent_triggered', 'engagement', 'exit_popup');
      }
    };

    const handleInteraction = () => {
      setHasInteracted(true);
    };

    document.addEventListener('mouseleave', handleMouseLeave);
    document.addEventListener('click', handleInteraction);
    document.addEventListener('scroll', handleInteraction);

    return () => {
      document.removeEventListener('mouseleave', handleMouseLeave);
      document.removeEventListener('click', handleInteraction);
      document.removeEventListener('scroll', handleInteraction);
    };
  }, [hasInteracted, showExitPopup]);

  const handleStartQuiz = () => {
    setShowQuiz(true);
    trackEvent('quiz_started', 'engagement', 'hero_button');
    document.getElementById('quiz')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScrollToVSL = () => {
    trackEvent('vsl_scroll', 'engagement', 'hero_button');
    document.getElementById('vsl')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleExitPopupAccept = () => {
    trackEvent('exit_popup_accepted', 'conversion', 'exit_popup');
    // Handle the free gift offer
    console.log('User accepted free gift');
  };

  const handleExitPopupClose = () => {
    setShowExitPopup(false);
    trackEvent('exit_popup_closed', 'engagement', 'exit_popup');
  };

  const testimonials = [
    {
      name: "Maria S.",
      role: "Alleinerziehende Mama",
      initials: "MS",
      rating: 5,
      text: "Am Anfang war ich skeptisch. Aber bereits nach 30 Tagen hatte ich meine ersten 180€ verdient. Nach 90 Tagen waren es konstant 1.800€ im Monat. Heute, 6 Monate später, sind es über 3.200€. Das Beste: Es läuft komplett automatisch!",
      verified: true,
      avatarColor: "bg-pink-500",
      earnings: "3.200€",
      timeframe: "Monat",
      isTopPerformer: true
    },
    {
      name: "Thomas K.",
      role: "Frustrierter Angestellter",
      initials: "TK",
      rating: 5,
      text: "Ich war am Anfang skeptisch. Aber die Ergebnisse sprechen für sich: Von 0€ auf 4.200€ passives Einkommen in nur 6 Monaten. Das System funktioniert wirklich! Mein Chef ahnt nicht, dass ich bald kündige.",
      verified: true,
      avatarColor: "bg-blue-600",
      earnings: "4.200€",
      timeframe: "Monat",
      isRecent: true
    },
    {
      name: "Julia M.",
      role: "Studentin",
      initials: "JM",
      rating: 5,
      text: "Als Studentin dachte ich, finanzielle Freiheit wäre nur was für Reiche. Mit diesem System verdiene ich jetzt mehr als meine Eltern - und das neben dem Studium! BAföG? Brauche ich nicht mehr.",
      verified: true,
      avatarColor: "bg-green-500",
      earnings: "2.800€",
      timeframe: "Monat"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <div className="flex-shrink-0">
                <span className="text-2xl font-bold text-q-primary">Digitaler Kompass</span>
                <span className="text-lg font-medium text-q-neutral-medium ml-2">Ihr Wegweiser zur finanziellen Freiheit</span>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-6">
              <a href="#quiz" className="text-q-neutral-medium hover:text-q-primary transition-colors">Quiz</a>
              <a href="#vsl" className="text-q-neutral-medium hover:text-q-primary transition-colors">System</a>
              <a href="#testimonials" className="text-q-neutral-medium hover:text-q-primary transition-colors">Erfolge</a>
              <Link href="/personas" className="text-q-neutral-medium hover:text-q-primary transition-colors">Personas</Link>
              <Button onClick={handleStartQuiz} className="gradient-cta hover:bg-q-accent-dark text-white touch-target">
                Jetzt starten
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="gradient-hero text-white py-20 relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-20 h-20 bg-q-accent rounded-full animate-pulse"></div>
          <div className="absolute top-32 right-20 w-16 h-16 bg-q-secondary rounded-full animate-pulse delay-1000"></div>
          <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-q-primary rounded-full animate-pulse delay-2000"></div>
        </div>
        
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight animate-fade-in-up">
              Ihr persönlicher <br />
              <span className="text-q-accent">Wegweiser zur finanziellen Freiheit</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 text-scannable">
              Entdecken Sie Ihre personalisierte Strategie - unabhängig von Ihrer Lebenssituation
            </p>
            
            {/* Live Visitor Counter */}
            <div className="mb-8">
              <LiveVisitorCounter baseCount={1247} updateInterval={3000} />
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-8 mb-8">
              <div className="flex items-center space-x-2">
                <Users className="text-q-accent" size={20} />
                <span className="text-sm">Über 10.000 zufriedene Kunden</span>
              </div>
              <div className="flex items-center space-x-2">
                <Star className="text-q-accent" size={20} />
                <span className="text-sm">4.8/5 Sterne Bewertung</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="text-q-accent" size={20} />
                <span className="text-sm">30 Tage Geld-zurück-Garantie</span>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Button 
                onClick={handleStartQuiz} 
                className="gradient-cta hover:bg-q-accent-dark text-white px-8 py-4 text-lg font-semibold transition-all transform hover:scale-105 touch-target hover-glow"
              >
                <Play className="mr-2" size={20} />
                Kostenlosen Finanz-Test starten
              </Button>
              <Button 
                onClick={handleScrollToVSL}
                variant="outline"
                className="bg-white text-q-primary hover:bg-gray-100 px-8 py-4 text-lg font-semibold transition-all touch-target"
              >
                System kennenlernen
              </Button>
            </div>
            
            {/* Urgency Indicator */}
            <div className="mt-6 p-3 bg-red-500/20 border border-red-500/30 rounded-lg max-w-md mx-auto">
              <div className="flex items-center justify-center space-x-2 text-red-400">
                <Zap size={16} />
                <span className="text-sm font-semibold">
                  ⚡ Nur noch 47 Plätze verfügbar für das kostenlose Geschenk!
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Quiz Section */}
      <section id="quiz" className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-q-neutral-dark mb-4">
              Finde deinen perfekten Weg zur finanziellen Freiheit
            </h2>
            <p className="text-xl text-q-neutral-medium text-scannable">
              Beantworte 8 Fragen und erhalte deinen personalisierten Finanzplan
            </p>
          </div>

          <Card className="card-psychological hover-lift">
            <CardContent className="p-8">
              <QuizForm />
            </CardContent>
          </Card>
        </div>
      </section>

      {/* VSL Section */}
      <section id="vsl" className="py-20 bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-q-neutral-dark mb-4">
              Entdecke das System, das bereits 10.000+ Menschen geholfen hat
            </h2>
            <p className="text-xl text-q-neutral-medium text-scannable">
              In diesem Video erfährst du die bewährte Strategie für 2.000-5.000€ passives Einkommen
            </p>
          </div>

          {/* Video Players */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <VideoPlayer
              title="Magic Profit System"
              description="Für Einsteiger: Von 0€ zu 2.000€ passivem Einkommen"
              duration="45 Minuten"
              views="150.000+ Aufrufe"
              videoId="magic-profit"
              onPlay={() => trackEvent('video_play', 'engagement', 'magic_profit_vsl')}
            />
            
            <VideoPlayer
              title="Money Magnet System"
              description="Für Fortgeschrittene: Skalierung auf 5.000€+"
              duration="52 Minuten"
              views="95.000+ Aufrufe"
              videoId="money-magnet"
              onPlay={() => trackEvent('video_play', 'engagement', 'money_magnet_vsl')}
            />
          </div>

          {/* Benefits */}
          <Card className="card-psychological shadow-lg">
            <CardContent className="p-8">
              <h3 className="text-2xl font-bold text-q-neutral-dark text-center mb-8">
                Was du in den Videos lernst:
              </h3>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="bg-q-primary text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 hover-scale">
                    <Lightbulb size={24} />
                  </div>
                  <h4 className="font-semibold text-q-neutral-dark mb-2">Die 3 Säulen</h4>
                  <p className="text-q-neutral-medium text-sm text-scannable">Passives Einkommen, Automatisierung und Skalierung</p>
                </div>
                <div className="text-center">
                  <div className="bg-q-secondary text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 hover-scale">
                    <Rocket size={24} />
                  </div>
                  <h4 className="font-semibold text-q-neutral-dark mb-2">Schnellstart</h4>
                  <p className="text-q-neutral-medium text-sm text-scannable">Erste Ergebnisse bereits in den ersten 30 Tagen</p>
                </div>
                <div className="text-center">
                  <div className="bg-q-accent text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 hover-scale">
                    <Shield size={24} />
                  </div>
                  <h4 className="font-semibold text-q-neutral-dark mb-2">Risikofrei</h4>
                  <p className="text-q-neutral-medium text-sm text-scannable">30 Tage Geld-zurück-Garantie ohne Wenn und Aber</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Bridge Page Section */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-q-neutral-dark mb-4">
              Wähle deinen Weg zur finanziellen Freiheit
            </h2>
            <p className="text-xl text-q-neutral-medium text-scannable">
              Verschiedene Wege, ein Ziel: Deine finanzielle Unabhängigkeit
            </p>
          </div>

          <div className="text-center">
            <Link href="/bridge">
              <Button 
                className="gradient-cta hover:bg-q-accent-dark text-white px-8 py-4 text-lg font-semibold transition-all transform hover:scale-105 touch-target hover-glow"
                onClick={() => trackEvent('bridge_page_click', 'navigation', 'home_cta')}
              >
                <Trophy className="mr-2" size={20} />
                Alle Funnel-Optionen ansehen
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-q-neutral-dark mb-4">
              Über 10.000 Menschen haben es bereits geschafft
            </h2>
            <p className="text-xl text-q-neutral-medium text-scannable">
              Echte Erfolgsgeschichten von echten Menschen
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <TestimonialCard key={index} {...testimonial} />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 gradient-hero text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Deine finanzielle Freiheit wartet nicht
          </h2>
          <p className="text-xl mb-8 text-blue-100 text-scannable">
            Schließe dich 10.000+ zufriedenen Kunden an und starte noch heute dein passives Einkommen
          </p>
          
          {/* Urgency Timer */}
          <div className="bg-white bg-opacity-10 rounded-lg p-4 mb-8 inline-block">
            <div className="text-q-accent font-semibold mb-2">
              <Clock className="inline mr-2" size={20} />
              Limitiertes Angebot läuft ab in:
            </div>
            <CountdownTimer showUrgency={true} urgencyThreshold={30} />
          </div>

          <div className="space-y-4">
            <Button 
              onClick={handleStartQuiz}
              className="gradient-cta hover:bg-q-accent-dark text-white px-8 py-4 text-xl font-bold transition-all transform hover:scale-105 touch-target hover-glow"
            >
              <Rocket className="mr-2" size={20} />
              Jetzt kostenlosen Zugang sichern
            </Button>
            <p className="text-sm text-blue-100">
              <Shield className="inline mr-1" size={16} />
              30 Tage Geld-zurück-Garantie • Kein Risiko • Sofortiger Zugang
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-q-neutral-dark text-white py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="text-2xl font-bold mb-4">Q-Money</div>
              <p className="text-gray-300 text-scannable">
                Dein Partner für finanzielle Freiheit und passives Einkommen.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Produkte</h4>
              <ul className="space-y-2 text-gray-300">
                <li><Link href="/vsl/magic-profit" className="hover:text-white transition-colors">Magic Profit</Link></li>
                <li><Link href="/vsl/money-magnet" className="hover:text-white transition-colors">Money Magnet</Link></li>
                <li><Link href="/bridge" className="hover:text-white transition-colors">Cash Maximus</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Kontakt</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Live Chat</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Rechtliches</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">Datenschutz</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Impressum</a></li>
                <li><a href="#" className="hover:text-white transition-colors">AGB</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300">
            <p>&copy; 2024 Q-Money & Cash Maximus. Alle Rechte vorbehalten.</p>
          </div>
        </div>
      </footer>

      {/* Floating CTA */}
      <FloatingCTA 
        onAction={handleStartQuiz}
        variant="urgent"
      />

      {/* Exit Intent Popup */}
      <ExitIntentPopup
        isVisible={showExitPopup}
        onClose={handleExitPopupClose}
        onAccept={handleExitPopupAccept}
      />
    </div>
  );
}
