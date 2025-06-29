import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  TrendingUp, 
  Star, 
  CheckCircle, 
  ArrowRight,
  Timer,
  Zap,
  Target,
  DollarSign,
  Sparkles,
  Rocket,
  Crown,
  Trophy,
  Coins,
  TrendingDown,
  Eye,
  MousePointer
} from 'lucide-react';

interface AnimatedVSLProps {
  personaType: string;
  leadId?: number;
  className?: string;
}

export function AnimatedVSL({ personaType, leadId, className = "" }: AnimatedVSLProps) {
  const [currentMoney, setCurrentMoney] = useState(0);
  const [targetMoney] = useState(5054);
  const [isCounting, setIsCounting] = useState(false);
  const [pulseState, setPulseState] = useState(0);
  const [floatingElements, setFloatingElements] = useState<Array<{id: number, x: number, y: number, type: string}>>([]);
  const [gradientShift, setGradientShift] = useState(0);
  const [showMoneyRain, setShowMoneyRain] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Geld-Counter Animation
  useEffect(() => {
    if (isCounting && currentMoney < targetMoney) {
      const timer = setTimeout(() => {
        setCurrentMoney(prev => Math.min(prev + Math.floor(Math.random() * 50) + 10, targetMoney));
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [currentMoney, targetMoney, isCounting]);

  // Pulsierende Elemente
  useEffect(() => {
    const pulseInterval = setInterval(() => {
      setPulseState(prev => (prev + 1) % 4);
    }, 800);
    return () => clearInterval(pulseInterval);
  }, []);

  // Floating Animationen
  useEffect(() => {
    const generateFloatingElement = () => {
      const types = ['💎', '💰', '🚀', '⭐', '🎯', '🏆'];
      const newElement = {
        id: Date.now(),
        x: Math.random() * 100,
        y: 100,
        type: types[Math.floor(Math.random() * types.length)]
      };
      setFloatingElements(prev => [...prev, newElement]);
      
      // Element nach 3 Sekunden entfernen
      setTimeout(() => {
        setFloatingElements(prev => prev.filter(el => el.id !== newElement.id));
      }, 3000);
    };

    const floatingInterval = setInterval(generateFloatingElement, 2000);
    return () => clearInterval(floatingInterval);
  }, []);

  // Gradient Shift Animation
  useEffect(() => {
    const gradientInterval = setInterval(() => {
      setGradientShift(prev => (prev + 1) % 360);
    }, 50);
    return () => clearInterval(gradientInterval);
  }, []);

  // Money Rain Effect
  useEffect(() => {
    if (showMoneyRain && canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const moneyDrops: Array<{x: number, y: number, speed: number, symbol: string}> = [];
      
      // Geld-Tropfen erstellen
      for (let i = 0; i < 50; i++) {
        moneyDrops.push({
          x: Math.random() * canvas.width,
          y: -50,
          speed: Math.random() * 3 + 1,
          symbol: Math.random() > 0.5 ? '€' : '💶'
        });
      }

      const animateMoneyRain = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        moneyDrops.forEach(drop => {
          drop.y += drop.speed;
          
          ctx.fillStyle = '#22c55e';
          ctx.font = '20px Arial';
          ctx.fillText(drop.symbol, drop.x, drop.y);
          
          if (drop.y > canvas.height) {
            drop.y = -50;
            drop.x = Math.random() * canvas.width;
          }
        });
        
        requestAnimationFrame(animateMoneyRain);
      };
      
      animateMoneyRain();
    }
  }, [showMoneyRain]);

  const startMoneyCount = () => {
    setIsCounting(true);
    setShowMoneyRain(true);
    setTimeout(() => setShowMoneyRain(false), 3000);
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

  return (
    <div className={`relative w-full max-w-6xl mx-auto ${className}`}>
      {/* Money Rain Canvas */}
      {showMoneyRain && (
        <canvas
          ref={canvasRef}
          className="fixed inset-0 pointer-events-none z-50"
          style={{ background: 'rgba(0,0,0,0.1)' }}
        />
      )}

      {/* Floating Elements */}
      {floatingElements.map(element => (
        <div
          key={element.id}
          className="fixed pointer-events-none z-40 animate-bounce"
          style={{
            left: `${element.x}%`,
            top: `${element.y}%`,
            animationDuration: '3s',
            animationDelay: `${Math.random() * 2}s`
          }}
        >
          <span className="text-2xl">{element.type}</span>
        </div>
      ))}

      {/* Animated Header */}
      <Card className="mb-6 overflow-hidden">
        <CardHeader 
          className="text-white relative overflow-hidden"
          style={{
            background: `linear-gradient(${gradientShift}deg, #3b82f6, #8b5cf6, #06b6d4, #3b82f6)`,
            backgroundSize: '400% 400%',
            animation: 'gradientShift 3s ease infinite'
          }}
        >
          <div className="flex items-center justify-between relative z-10">
            <div className="flex items-center space-x-4">
              <div 
                className={`w-12 h-12 bg-white/20 rounded-full flex items-center justify-center ${
                  pulseState === 0 ? 'animate-pulse' : ''
                }`}
              >
                <Play className="w-6 h-6" />
              </div>
              <div>
                <CardTitle className="text-2xl font-bold flex items-center space-x-2">
                  <span>{getPersonaIcon(personaType)}</span>
                  <span>Personalisierte VSL für {personaType}</span>
                  <Sparkles className="w-5 h-5 animate-spin" />
                </CardTitle>
                <CardDescription className="text-blue-100">
                  Dynamisch generiert mit KI-Optimierung
                </CardDescription>
              </div>
            </div>
            <Badge className={`${getPersonaColor(personaType)} animate-bounce`}>
              {personaType.toUpperCase()}
            </Badge>
          </div>
        </CardHeader>
      </Card>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Money Counter Card */}
          <Card className="border-green-200 bg-gradient-to-r from-green-50 to-emerald-50">
            <CardContent className="p-6">
              <div className="text-center">
                <div className="flex items-center justify-center space-x-2 mb-4">
                  <Coins className="w-8 h-8 text-green-600 animate-bounce" />
                  <h3 className="text-xl font-bold text-green-900">TÄGLICHES EINKOMMEN</h3>
                  <Trophy className="w-8 h-8 text-yellow-600 animate-pulse" />
                </div>
                
                <div className="mb-4">
                  <div className="text-4xl font-bold text-green-600 mb-2">
                    {currentMoney.toLocaleString()}€
                  </div>
                  <div className="text-sm text-gray-600">
                    von {targetMoney.toLocaleString()}€ Ziel
                  </div>
                </div>

                <Button
                  onClick={startMoneyCount}
                  className="bg-green-600 hover:bg-green-700 animate-pulse"
                  disabled={isCounting}
                >
                  <Rocket className="w-4 h-4 mr-2" />
                  {isCounting ? 'Zählt hoch...' : 'Live-Demo starten'}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Animated Success Stories */}
          <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50">
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold text-blue-900 mb-4 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 animate-pulse" />
                Erfolgsgeschichten in Echtzeit
              </h3>
              
              <div className="space-y-4">
                {[
                  { name: 'Sarah M.', amount: '2.847€', time: 'vor 3 Min' },
                  { name: 'Michael K.', amount: '3.156€', time: 'vor 7 Min' },
                  { name: 'Lisa R.', amount: '4.892€', time: 'vor 12 Min' },
                  { name: 'Thomas B.', amount: '5.054€', time: 'vor 15 Min' }
                ].map((story, index) => (
                  <div 
                    key={index}
                    className={`flex items-center justify-between p-3 rounded-lg ${
                      index === 0 ? 'bg-green-100 border-green-200' : 'bg-white border'
                    } ${pulseState === index % 4 ? 'animate-pulse' : ''}`}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        {story.name.charAt(0)}
                      </div>
                      <div>
                        <div className="font-medium">{story.name}</div>
                        <div className="text-sm text-gray-600">{story.time}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-green-600">{story.amount}</div>
                      <div className="text-xs text-gray-500">heute verdient</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Animated Features */}
          <Card className="border-purple-200 bg-gradient-to-r from-purple-50 to-pink-50">
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold text-purple-900 mb-4 flex items-center">
                <Crown className="w-5 h-5 mr-2 animate-bounce" />
                Premium Features
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { icon: '🚀', title: 'Sofortiger Start', desc: 'Heute noch beginnen' },
                  { icon: '⚡', title: 'Automatisierung', desc: 'Läuft von alleine' },
                  { icon: '🎯', title: 'Personalisierung', desc: 'Maßgeschneidert' },
                  { icon: '💰', title: 'Skalierbar', desc: 'Unbegrenztes Wachstum' }
                ].map((feature, index) => (
                  <div 
                    key={index}
                    className={`flex items-center space-x-3 p-3 rounded-lg bg-white border ${
                      pulseState === index % 4 ? 'animate-pulse' : ''
                    }`}
                  >
                    <span className="text-2xl">{feature.icon}</span>
                    <div>
                      <div className="font-medium">{feature.title}</div>
                      <div className="text-sm text-gray-600">{feature.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Animated Sidebar */}
        <div className="space-y-6">
          {/* Urgency Counter */}
          <Card className="border-red-200 bg-gradient-to-r from-red-50 to-orange-50">
            <CardContent className="p-6">
              <div className="text-center">
                <Timer className="w-8 h-8 text-red-600 mx-auto mb-2 animate-pulse" />
                <h3 className="text-lg font-semibold text-red-900 mb-2">
                  Angebot läuft ab!
                </h3>
                <div className="text-2xl font-bold text-red-600 mb-2 animate-bounce">
                  29:47
                </div>
                <p className="text-sm text-red-700">
                  Nur noch heute zum Spezialpreis!
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Animated Pricing */}
          <Card className="border-green-200 bg-gradient-to-r from-green-50 to-emerald-50">
            <CardContent className="p-6">
              <div className="text-center">
                <Target className="w-8 h-8 text-green-600 mx-auto mb-2 animate-bounce" />
                <h3 className="text-lg font-semibold text-green-900 mb-2">
                  Dein personalisierter Preis
                </h3>
                
                <div className="mb-4">
                  <div className="text-3xl font-bold text-green-600 animate-pulse">
                    497€
                  </div>
                  <div className="text-sm text-gray-600 line-through">
                    statt 997€
                  </div>
                </div>

                <div className="space-y-2 mb-4">
                  <Button
                    className="w-full bg-green-600 hover:bg-green-700 animate-pulse"
                  >
                    <DollarSign className="w-4 h-4 mr-2" />
                    497€ / Monat
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full border-green-600 text-green-600 hover:bg-green-50"
                  >
                    <Zap className="w-4 h-4 mr-2" />
                    397€ / Jahr (Spare 20%)
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Animated Bonuses */}
          <Card className="border-yellow-200 bg-gradient-to-r from-yellow-50 to-amber-50">
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold text-yellow-900 mb-4 flex items-center">
                <Star className="w-5 h-5 mr-2 animate-spin" />
                Deine Bonuses
              </h3>
              <div className="space-y-3">
                {[
                  '🎓 Studenten-Bonus: Social Media Templates (Wert: 197€)',
                  '📱 Mobile-First Strategien (Wert: 147€)',
                  '👥 Studenten-Community Zugang (Wert: 97€)',
                  '⏰ 30-Minuten-Routine-Guide (Wert: 77€)'
                ].map((bonus, index) => (
                  <div 
                    key={index}
                    className={`flex items-start space-x-2 ${
                      pulseState === index % 4 ? 'animate-pulse' : ''
                    }`}
                  >
                    <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{bonus}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* CSS für Gradient Animation */}
      <style jsx>{`
        @keyframes gradientShift {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
      `}</style>
    </div>
  );
}

export default AnimatedVSL; 