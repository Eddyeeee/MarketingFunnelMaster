import React, { useEffect, useState } from 'react';
import { Link } from "wouter";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Star, Crown, Download, Play, Mail, FileText, Link as LinkIcon, ChevronRight, CheckCircle, Clock, Target, TrendingUp, ArrowRight } from "lucide-react";
import { trackEvent } from "@/lib/analytics";
import { toast } from "@/hooks/use-toast";
import { useLocation } from 'wouter';
import EmailPreview from '../components/EmailPreview';
import { UpsellModal } from '../components/UpsellModal';
import { useUpsell } from '../hooks/use-upsell';

export default function Bridge() {
  const { data: emailFunnels = [] } = useQuery({
    queryKey: ['/api/email-funnels']
  });

  const [, setLocation] = useLocation();
  const [countdown, setCountdown] = useState(10);
  const [persona, setPersona] = useState<any>(null);
  const [showEmailPreview, setShowEmailPreview] = useState(false);
  const [leadId, setLeadId] = useState<number | null>(null);

  // Upsell System
  const {
    currentProduct,
    isModalOpen,
    openUpsellModal,
    closeUpsellModal,
    purchaseProduct,
    startAutoUpsell,
    loadQMoneyUpsell,
    loadCashMaximusUpsell
  } = useUpsell({
    personaType: persona?.type,
    leadId: leadId || undefined,
    purchaseAmount: 0
  });

  useEffect(() => {
    // Lade Persona-Daten aus localStorage (falls verfügbar)
    const savedPersona = localStorage.getItem('quizPersona');
    if (savedPersona) {
      setPersona(JSON.parse(savedPersona));
    }

    // Lade Lead-ID aus localStorage (falls verfügbar)
    const savedLeadId = localStorage.getItem('leadId');
    if (savedLeadId) {
      setLeadId(parseInt(savedLeadId));
    }

    // Countdown für automatische Weiterleitung
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          // Starte Upsell vor VSL-Weiterleitung
          startAutoUpsell(3);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [setLocation, startAutoUpsell]);

  // Lade Q-Money Upsell nach Persona-Erkennung
  useEffect(() => {
    if (persona?.type) {
      loadQMoneyUpsell();
    }
  }, [persona?.type, loadQMoneyUpsell]);

  const handleImportFunnel = (funnel: string) => {
    trackEvent('funnel_import', 'engagement', funnel);
    toast({
      title: "Funnel wird importiert",
      description: `${funnel === 'magic-profit' ? 'Magic Profit' : 'Money Magnet'} Funnel wird in dein System importiert...`,
    });
  };

  const handleStartQuizFunnel = (funnel: string) => {
    trackEvent('quiz_funnel_start', 'engagement', funnel);
    // Redirect to quiz with funnel parameter
    window.location.href = `/quiz?funnel=${funnel}`;
  };

  const handleOpenEmailFunnel = (id: number) => {
    trackEvent('email_funnel_open', 'engagement', `funnel_${id}`);
    toast({
      title: "E-Mail-Funnel wird geöffnet",
      description: "Der E-Mail-Funnel wird in einem neuen Tab geöffnet...",
    });
  };

  const handleOpenTSL = () => {
    trackEvent('tsl_open', 'engagement', 'bridge_page');
    window.location.href = '/tsl';
  };

  const handleOpenBridgePage = () => {
    trackEvent('bridge_page_open', 'engagement', 'self_reference');
    toast({
      title: "Du bist bereits hier",
      description: "Du befindest dich bereits auf der Bridge Page!",
    });
  };

  const handleContinueNow = () => {
    // Starte Upsell vor VSL-Weiterleitung
    startAutoUpsell(2);
  };

  const handleShowEmailPreview = () => {
    setShowEmailPreview(true);
  };

  const handleUpsellPurchase = (productId: string) => {
    trackEvent('upsell_purchase', 'conversion', productId);
    
    // Wenn Q-Money gekauft wurde, lade Cash Maximus
    if (productId.includes('qmoney')) {
      setTimeout(() => {
        loadCashMaximusUpsell();
        startAutoUpsell(3);
      }, 2000);
    }
  };

  // Zeige E-Mail-Preview an
  if (showEmailPreview && persona) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Navigation */}
          <nav className="bg-white shadow-sm mb-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <Button 
                  variant="ghost" 
                  onClick={() => setShowEmailPreview(false)}
                  className="flex items-center space-x-2"
                >
                  <ArrowLeft size={20} />
                  <span>Zurück zur Bridge</span>
                </Button>
                <div className="flex-shrink-0">
                  <span className="text-2xl font-bold text-blue-600">Magic Tool</span>
                  <span className="text-lg font-medium text-gray-600 ml-2">E-Mail-Preview</span>
                </div>
              </div>
            </div>
          </nav>

          <EmailPreview 
            persona={persona} 
            leadId={leadId || undefined}
            className="shadow-2xl"
          />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
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
                <span className="text-lg font-medium text-q-neutral-medium ml-2">Bridge</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Bridge Content */}
      <section className="py-12">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Perfekt! Dein personalisierter Plan ist bereit! 🎯
            </h1>
            <p className="text-xl text-gray-600">
              Du wirst in {countdown} Sekunden automatisch zu deiner personalisierten Strategie weitergeleitet...
            </p>
          </div>

          {/* Persona Summary */}
          {persona && (
            <Card className="mb-8 shadow-lg">
              <CardHeader className="text-center bg-gradient-to-r from-blue-50 to-purple-50">
                <CardTitle className="text-2xl font-bold text-gray-900">
                  Dein Profil: {persona.profileText}
                </CardTitle>
                <CardDescription className="text-lg text-gray-600">
                  {persona.strategyText}
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6">
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Target className="w-6 h-6 text-blue-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">Dein Ziel</h3>
                    <p className="text-sm text-gray-600">{persona.actionPlan?.expectedResults}</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Clock className="w-6 h-6 text-green-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">Timeline</h3>
                    <p className="text-sm text-gray-600">{persona.actionPlan?.timeline}</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <TrendingUp className="w-6 h-6 text-purple-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">Strategie</h3>
                    <Badge variant="default" className="bg-purple-600">
                      {persona.recommendedFunnel?.replace('_', ' ').toUpperCase()}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* What You'll Get */}
          <Card className="mb-8 shadow-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl font-bold text-gray-900">
                Was du gleich erhältst:
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">30-Tage-Action-Plan</h3>
                      <p className="text-sm text-gray-600">Tägliche Schritte für deinen Erfolg</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Persönliche Strategie</h3>
                      <p className="text-sm text-gray-600">Maßgeschneidert auf deine Situation</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Exklusive Tools</h3>
                      <p className="text-sm text-gray-600">Professionelle Software und Templates</p>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Community-Zugang</h3>
                      <p className="text-sm text-gray-600">Netzwerk mit Gleichgesinnten</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">1:1 Support</h3>
                      <p className="text-sm text-gray-600">Persönliche Beratung und Coaching</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Geld-zurück-Garantie</h3>
                      <p className="text-sm text-gray-600">30 Tage ohne Risiko testen</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Social Proof */}
          <Card className="mb-8 shadow-lg">
            <CardContent className="p-6">
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Über 10.000 Menschen haben bereits Erfolg gehabt
                </h3>
                <div className="flex justify-center space-x-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                  <span className="ml-2 text-sm text-gray-600">4.9/5 Sterne</span>
                </div>
              </div>
              <div className="grid md:grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-600">€2.4M</div>
                  <div className="text-sm text-gray-600">Verdient von Teilnehmern</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">94%</div>
                  <div className="text-sm text-gray-600">Erfolgsrate</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-purple-600">30 Tage</div>
                  <div className="text-sm text-gray-600">Bis zum ersten Erfolg</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Call to Action */}
          <div className="text-center">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-8 rounded-lg text-white mb-6">
              <h2 className="text-3xl font-bold mb-4">
                Bereit für deine finanzielle Transformation? 🚀
              </h2>
              <p className="text-xl text-blue-100 mb-6">
                Klicke jetzt und erhalte sofort Zugang zu deiner personalisierten Strategie!
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  onClick={handleContinueNow}
                  size="lg"
                  className="bg-white text-blue-600 hover:bg-gray-100 font-semibold px-8 py-4 text-lg"
                >
                  Jetzt zu meiner Strategie
                  <ArrowRight className="w-6 h-6 ml-2" />
                </Button>
                <Button
                  onClick={handleShowEmailPreview}
                  size="lg"
                  variant="outline"
                  className="border-white text-white hover:bg-white hover:text-blue-600 font-semibold px-8 py-4 text-lg"
                >
                  E-Mail-Preview anzeigen
                  <Mail className="w-6 h-6 ml-2" />
                </Button>
              </div>
            </div>
            
            <p className="text-sm text-gray-500">
              Du wirst automatisch in {countdown} Sekunden weitergeleitet, oder klicke oben für sofortigen Zugang.
            </p>
          </div>

          {/* Upsell Modal */}
          {currentProduct && (
            <UpsellModal
              isOpen={isModalOpen}
              onClose={closeUpsellModal}
              product={currentProduct}
              personaType={persona?.type}
              leadId={leadId || undefined}
              onPurchase={handleUpsellPurchase}
            />
          )}
        </div>
      </section>
    </div>
  );
}
