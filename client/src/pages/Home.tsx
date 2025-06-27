import { useState, useEffect } from "react";
import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users, Star, Shield, Clock, Play, CheckCircle, Trophy, Lightbulb, Rocket } from "lucide-react";
import QuizForm from "@/components/QuizForm";
import VideoPlayer from "@/components/VideoPlayer";
import CountdownTimer from "@/components/CountdownTimer";
import TestimonialCard from "@/components/TestimonialCard";
import { trackEvent } from "@/lib/analytics";

export default function Home() {
  const [showQuiz, setShowQuiz] = useState(false);

  const handleStartQuiz = () => {
    setShowQuiz(true);
    trackEvent('quiz_started', 'engagement', 'hero_button');
    document.getElementById('quiz')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScrollToVSL = () => {
    trackEvent('vsl_scroll', 'engagement', 'hero_button');
    document.getElementById('vsl')?.scrollIntoView({ behavior: 'smooth' });
  };

  const testimonials = [
    {
      name: "Maria S.",
      role: "Vollzeit-Mama",
      initials: "MS",
      rating: 5,
      text: "In nur 3 Monaten von 0€ auf 1.800€ passives Einkommen. Endlich kann ich für meine Kinder da sein und trotzdem zum Familieneinkommen beitragen.",
      verified: true
    },
    {
      name: "Thomas K.",
      role: "Angestellter",
      initials: "TK",
      rating: 5,
      text: "Das System ist genial! Arbeite nur noch 30 Minuten täglich daran und verdiene 3.200€ nebenbei. Mein Chef weiß nicht mal, was ich in der Mittagspause mache.",
      verified: true
    },
    {
      name: "Julia M.",
      role: "Studentin",
      initials: "JM",
      rating: 5,
      text: "Als Studentin dachte ich, ich hätte kein Geld zum Investieren. Falsch gedacht! Mit 50€ gestartet, jetzt bei 950€ monatlich. BAföG war gestern!",
      verified: true
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
                <span className="text-2xl font-bold text-q-primary">Q-Money</span>
                <span className="text-lg font-medium text-q-neutral-medium ml-2">& Cash Maximus</span>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-6">
              <a href="#quiz" className="text-q-neutral-medium hover:text-q-primary transition-colors">Quiz</a>
              <a href="#vsl" className="text-q-neutral-medium hover:text-q-primary transition-colors">System</a>
              <a href="#testimonials" className="text-q-neutral-medium hover:text-q-primary transition-colors">Erfolge</a>
              <Button onClick={handleStartQuiz} className="bg-q-primary hover:bg-q-primary-dark">
                Jetzt starten
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="gradient-hero text-white py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Von 0€ zu 2.000-5.000€ <br />
              <span className="text-q-accent">passivem Einkommen</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              Das bewährte System für finanzielle Freiheit - auch ohne Vorkenntnisse
            </p>
            
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
                className="gradient-cta hover:bg-q-accent-dark text-white px-8 py-4 text-lg font-semibold transition-all transform hover:scale-105"
              >
                <Play className="mr-2" size={20} />
                Kostenlosen Test starten
              </Button>
              <Button 
                onClick={handleScrollToVSL}
                variant="outline"
                className="bg-white text-q-primary hover:bg-gray-100 px-8 py-4 text-lg font-semibold transition-all"
              >
                System kennenlernen
              </Button>
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
            <p className="text-xl text-q-neutral-medium">
              Beantworte 8 Fragen und erhalte deinen personalisierten Finanzplan
            </p>
          </div>

          <Card className="bg-gray-50 shadow-lg">
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
            <p className="text-xl text-q-neutral-medium">
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
          <Card className="shadow-lg">
            <CardContent className="p-8">
              <h3 className="text-2xl font-bold text-q-neutral-dark text-center mb-8">
                Was du in den Videos lernst:
              </h3>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="bg-q-primary text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    <Lightbulb size={24} />
                  </div>
                  <h4 className="font-semibold text-q-neutral-dark mb-2">Die 3 Säulen</h4>
                  <p className="text-q-neutral-medium text-sm">Passives Einkommen, Automatisierung und Skalierung</p>
                </div>
                <div className="text-center">
                  <div className="bg-q-secondary text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    <Rocket size={24} />
                  </div>
                  <h4 className="font-semibold text-q-neutral-dark mb-2">Schnellstart</h4>
                  <p className="text-q-neutral-medium text-sm">Erste Ergebnisse bereits in den ersten 30 Tagen</p>
                </div>
                <div className="text-center">
                  <div className="bg-q-accent text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    <Shield size={24} />
                  </div>
                  <h4 className="font-semibold text-q-neutral-dark mb-2">Risikofrei</h4>
                  <p className="text-q-neutral-medium text-sm">30 Tage Geld-zurück-Garantie ohne Wenn und Aber</p>
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
            <p className="text-xl text-q-neutral-medium">
              Verschiedene Wege, ein Ziel: Deine finanzielle Unabhängigkeit
            </p>
          </div>

          <div className="text-center">
            <Link href="/bridge">
              <Button 
                className="gradient-cta hover:bg-q-accent-dark text-white px-8 py-4 text-lg font-semibold transition-all transform hover:scale-105"
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
            <p className="text-xl text-q-neutral-medium">
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
          <p className="text-xl mb-8 text-blue-100">
            Schließe dich 10.000+ zufriedenen Kunden an und starte noch heute dein passives Einkommen
          </p>
          
          {/* Urgency Timer */}
          <div className="bg-white bg-opacity-10 rounded-lg p-4 mb-8 inline-block">
            <div className="text-q-accent font-semibold mb-2">
              <Clock className="inline mr-2" size={20} />
              Limitiertes Angebot läuft ab in:
            </div>
            <CountdownTimer />
          </div>

          <div className="space-y-4">
            <Button 
              onClick={handleStartQuiz}
              className="gradient-cta hover:bg-q-accent-dark text-white px-8 py-4 text-xl font-bold transition-all transform hover:scale-105"
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
              <p className="text-gray-300">
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
    </div>
  );
}
