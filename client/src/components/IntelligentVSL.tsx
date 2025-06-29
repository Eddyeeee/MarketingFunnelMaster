import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  Clock, 
  Users, 
  TrendingUp, 
  Star, 
  CheckCircle, 
  ArrowRight,
  Timer,
  AlertTriangle,
  Zap,
  Target,
  DollarSign
} from 'lucide-react';

interface VSLSection {
  id: string;
  title: string;
  content: string;
  type: 'hook' | 'problem' | 'solution' | 'proof' | 'offer' | 'urgency' | 'guarantee';
  personaSpecific: boolean;
}

interface VSLConfig {
  personaType: string;
  sections: VSLSection[];
  pricing: {
    basePrice: number;
    discountPrice: number;
    currency: string;
    paymentPlans: {
      monthly: number;
      yearly: number;
    };
  };
  bonuses: string[];
  guarantees: string[];
  urgencyElements: {
    countdown: boolean;
    limitedSpots: boolean;
    expiringOffer: boolean;
  };
}

interface IntelligentVSLProps {
  personaType: string;
  leadId?: number;
  className?: string;
}

export function IntelligentVSL({ personaType, leadId, className = "" }: IntelligentVSLProps) {
  const [vslConfig, setVslConfig] = useState<VSLConfig | null>(null);
  const [currentSection, setCurrentSection] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(0);
  const [timeSpent, setTimeSpent] = useState(0);
  const [showOffer, setShowOffer] = useState(false);
  const [countdown, setCountdown] = useState(1800); // 30 Minuten
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetchVSL();
    fetchStats();
  }, [personaType, leadId]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isPlaying) {
      interval = setInterval(() => {
        setTimeSpent(prev => prev + 1);
        setProgress(prev => Math.min(prev + 0.1, 100));
        
        // Zeige Offer nach 60% Progress
        if (progress >= 60 && !showOffer) {
          setShowOffer(true);
        }
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isPlaying, progress, showOffer]);

  useEffect(() => {
    let countdownInterval: NodeJS.Timeout;
    
    if (countdown > 0) {
      countdownInterval = setInterval(() => {
        setCountdown(prev => prev - 1);
      }, 1000);
    }

    return () => clearInterval(countdownInterval);
  }, [countdown]);

  const fetchVSL = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (leadId) params.append('leadId', leadId.toString());
      
      const response = await fetch(`/api/vsl/${personaType}?${params}`);
      const data = await response.json();
      
      if (data.success) {
        setVslConfig(data.vsl);
      }
    } catch (error) {
      console.error('Error fetching VSL:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`/api/vsl/stats/${personaType}`);
      const data = await response.json();
      
      if (data.success) {
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Error fetching VSL stats:', error);
    }
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleMuteToggle = () => {
    setIsMuted(!isMuted);
  };

  const handleSectionChange = (index: number) => {
    setCurrentSection(index);
    setProgress((index / (vslConfig?.sections.length || 1)) * 100);
  };

  const handlePurchase = async (plan: 'monthly' | 'yearly') => {
    try {
      const amount = plan === 'monthly' 
        ? vslConfig?.pricing.paymentPlans.monthly 
        : vslConfig?.pricing.paymentPlans.yearly;

      // Track Conversion
      await fetch('/api/vsl/conversion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personaType,
          leadId,
          amount
        })
      });

      // Hier würde normalerweise zur Zahlungsseite weitergeleitet
      alert(`Weiterleitung zur Zahlung: ${amount}€`);
    } catch (error) {
      console.error('Error tracking conversion:', error);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getPersonaIcon = (type: string) => {
    switch (type) {
      case 'student': return '🎓';
      case 'employee': return '💼';
      case 'parent': return '👨‍👩‍👧‍👦';
      default: return '👤';
    }
  };

  const getPersonaColor = (type: string) => {
    switch (type) {
      case 'student': return 'bg-blue-100 text-blue-800';
      case 'employee': return 'bg-green-100 text-green-800';
      case 'parent': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <Card className={`w-full max-w-6xl mx-auto ${className}`}>
        <CardContent className="p-8">
          <div className="flex items-center justify-center space-x-2">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="text-gray-600">Lade personalisierte VSL...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!vslConfig) {
    return (
      <Card className={`w-full max-w-6xl mx-auto ${className}`}>
        <CardContent className="p-8">
          <div className="text-center">
            <p className="text-gray-600">VSL konnte nicht geladen werden.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const currentSectionData = vslConfig.sections[currentSection];

  return (
    <div className={`w-full max-w-6xl mx-auto ${className}`}>
      {/* VSL Header */}
      <Card className="mb-6">
        <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <Play className="w-6 h-6" />
              </div>
              <div>
                <CardTitle className="text-2xl font-bold">
                  {getPersonaIcon(personaType)} Personalisierte VSL für {personaType}
                </CardTitle>
                <CardDescription className="text-blue-100">
                  Dynamisch generiert basierend auf deiner Persona
                </CardDescription>
              </div>
            </div>
            <Badge className={getPersonaColor(personaType)}>
              {personaType.toUpperCase()}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="p-6">
          {/* Progress Bar */}
          <div className="mb-4">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Fortschritt: {Math.round(progress)}%</span>
              <span>Zeit: {formatTime(timeSpent)}</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {/* Controls */}
          <div className="flex items-center space-x-4">
            <Button
              onClick={handlePlayPause}
              variant="outline"
              size="sm"
              className="flex items-center space-x-2"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              <span>{isPlaying ? 'Pause' : 'Play'}</span>
            </Button>
            <Button
              onClick={handleMuteToggle}
              variant="outline"
              size="sm"
              className="flex items-center space-x-2"
            >
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              <span>{isMuted ? 'Unmute' : 'Mute'}</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main VSL Content */}
        <div className="lg:col-span-2">
          <Card className="mb-6">
            <CardContent className="p-8">
              {/* Current Section */}
              <div className="mb-8">
                <div className="flex items-center space-x-2 mb-4">
                  <Badge variant="outline">
                    {currentSection + 1} von {vslConfig.sections.length}
                  </Badge>
                  <Badge variant="secondary">
                    {currentSectionData.type.toUpperCase()}
                  </Badge>
                </div>
                
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  {currentSectionData.title}
                </h2>
                
                <div className="prose prose-lg max-w-none">
                  <p className="text-gray-700 leading-relaxed">
                    {currentSectionData.content}
                  </p>
                </div>
              </div>

              {/* Section Navigation */}
              <div className="flex justify-between">
                <Button
                  onClick={() => handleSectionChange(Math.max(0, currentSection - 1))}
                  disabled={currentSection === 0}
                  variant="outline"
                >
                  Zurück
                </Button>
                
                <Button
                  onClick={() => handleSectionChange(Math.min(vslConfig.sections.length - 1, currentSection + 1))}
                  disabled={currentSection === vslConfig.sections.length - 1}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Weiter
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Social Proof */}
          {stats && (
            <Card className="mb-6">
              <CardContent className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2" />
                  VSL-Performance für {personaType}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{stats.views}</div>
                    <div className="text-sm text-gray-600">Views</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{stats.conversions}</div>
                    <div className="text-sm text-gray-600">Conversions</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{stats.conversionRate}%</div>
                    <div className="text-sm text-gray-600">Conversion Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">{stats.avgTimeOnPage}s</div>
                    <div className="text-sm text-gray-600">Avg. Time</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Urgency Elements */}
          {vslConfig.urgencyElements.countdown && (
            <Card className="border-red-200 bg-red-50">
              <CardContent className="p-6">
                <div className="text-center">
                  <Timer className="w-8 h-8 text-red-600 mx-auto mb-2" />
                  <h3 className="text-lg font-semibold text-red-900 mb-2">
                    Angebot läuft ab!
                  </h3>
                  <div className="text-2xl font-bold text-red-600 mb-2">
                    {formatTime(countdown)}
                  </div>
                  <p className="text-sm text-red-700">
                    Nur noch heute zum Spezialpreis!
                  </p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Pricing */}
          <Card className="border-green-200 bg-green-50">
            <CardContent className="p-6">
              <div className="text-center">
                <Target className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <h3 className="text-lg font-semibold text-green-900 mb-2">
                  Dein personalisierter Preis
                </h3>
                
                <div className="mb-4">
                  <div className="text-3xl font-bold text-green-600">
                    {vslConfig.pricing.discountPrice}€
                  </div>
                  <div className="text-sm text-gray-600 line-through">
                    statt {vslConfig.pricing.basePrice}€
                  </div>
                </div>

                <div className="space-y-2 mb-4">
                  <Button
                    onClick={() => handlePurchase('monthly')}
                    className="w-full bg-green-600 hover:bg-green-700"
                  >
                    <DollarSign className="w-4 h-4 mr-2" />
                    {vslConfig.pricing.paymentPlans.monthly}€ / Monat
                  </Button>
                  <Button
                    onClick={() => handlePurchase('yearly')}
                    variant="outline"
                    className="w-full border-green-600 text-green-600 hover:bg-green-50"
                  >
                    <Zap className="w-4 h-4 mr-2" />
                    {vslConfig.pricing.paymentPlans.yearly}€ / Jahr (Spare 20%)
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Bonuses */}
          <Card>
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Star className="w-5 h-5 mr-2" />
                Deine Bonuses
              </h3>
              <div className="space-y-3">
                {vslConfig.bonuses.map((bonus, index) => (
                  <div key={index} className="flex items-start space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{bonus}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Guarantees */}
          <Card>
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2" />
                Deine Garantien
              </h3>
              <div className="space-y-3">
                {vslConfig.guarantees.map((guarantee, index) => (
                  <div key={index} className="flex items-start space-x-2">
                    <CheckCircle className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{guarantee}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default IntelligentVSL; 