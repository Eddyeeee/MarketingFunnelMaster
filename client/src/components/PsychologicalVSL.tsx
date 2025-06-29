import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Pause, Volume2, VolumeX, Clock, Users, Star, Zap } from 'lucide-react';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { useToast } from '../hooks/use-toast';

interface PsychologicalVSLProps {
  productId: string;
  personaType: string;
  onComplete: () => void;
}

interface VSLSegment {
  id: string;
  title: string;
  content: string;
  duration: number;
  showUrgency?: boolean;
  showScarcity?: boolean;
  revealSecret?: boolean;
}

export const PsychologicalVSL: React.FC<PsychologicalVSLProps> = ({
  productId,
  personaType,
  onComplete
}) => {
  const [currentSegment, setCurrentSegment] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(0);
  const [timeLeft, setTimeLeft] = useState(0);
  const [viewerCount, setViewerCount] = useState(0);
  const [spotsLeft, setSpotsLeft] = useState(0);
  const [showSecret, setShowSecret] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const intervalRef = useRef<NodeJS.Timeout>();
  const { toast } = useToast();

  // Psychologische VSL-Segmente
  const vslSegments: VSLSegment[] = [
    {
      id: 'hook',
      title: 'Die geheime Methode, die 97% der Menschen nicht kennen',
      content: 'Was wäre, wenn ich dir eine Methode zeigen würde, die dir 2000€+ monatlich bringt, ohne dass du deinen Job kündigen musst? Eine Methode, die so einfach ist, dass du sie in 30 Minuten lernen kannst?',
      duration: 45,
      showUrgency: true
    },
    {
      id: 'problem',
      title: 'Warum 99% der Menschen nie finanziell frei werden',
      content: 'Das Problem ist nicht, dass du nicht genug verdienst. Das Problem ist, dass du dein Geld falsch investierst. Die meisten Menschen arbeiten 40 Jahre für ein Gehalt, das nie steigt.',
      duration: 60
    },
    {
      id: 'agitation',
      title: 'Die 3 tödlichen Fehler beim Geldverdienen',
      content: 'Fehler 1: Du denkst, du brauchst viel Startkapital. Fehler 2: Du glaubst, du brauchst besondere Fähigkeiten. Fehler 3: Du wartest auf den perfekten Moment. Diese Fehler kosten dich Millionen!',
      duration: 75
    },
    {
      id: 'solution',
      title: 'Die Lösung: Eine bewährte Methode von einem Millionär',
      content: 'Ich habe eine Methode entwickelt, die bereits über 10.000 Menschen geholfen hat. Sie funktioniert von überall, braucht kein Startkapital und du kannst sofort anfangen.',
      duration: 90,
      showScarcity: true
    },
    {
      id: 'proof',
      title: 'Beweise: Echte Ergebnisse von echten Menschen',
      content: 'Sarah: "Ich verdiene jetzt 3.200€ monatlich von Bali aus." Markus: "Ich habe meinen Job gekündigt und verdiene das Doppelte." Lisa: "Ich arbeite nur noch 2 Stunden am Tag."',
      duration: 60
    },
    {
      id: 'bonus',
      title: 'Bonus: Du bekommst 3 zusätzliche Methoden GRATIS',
      content: 'Neben der Hauptmethode bekommst du: 1. Die "Schnellstart-Formel" (Wert: 297€), 2. Die "Skalierungs-Strategie" (Wert: 497€), 3. Die "Automatisierungs-Methode" (Wert: 397€).',
      duration: 45
    },
    {
      id: 'urgency',
      title: 'WARNUNG: Diese Methode wird nur noch 47 Menschen gezeigt!',
      content: 'Ich kann nur 100 Menschen persönlich betreuen. 53 Plätze sind bereits vergeben. Wenn du jetzt nicht handelst, verpasst du diese einmalige Gelegenheit für immer.',
      duration: 30,
      showUrgency: true,
      showScarcity: true
    },
    {
      id: 'secret',
      title: 'Das Geheimnis: Q-Money von Andreas Lang',
      content: 'Das ist Q-Money - die bewährte Methode von Andreas Lang. Über 50.000 Menschen haben damit bereits ihr Einkommen vervielfacht. Jetzt ist es deine Chance!',
      duration: 30,
      revealSecret: true
    }
  ];

  // Live-Viewer-Simulation
  useEffect(() => {
    const updateViewers = () => {
      const baseViewers = 127;
      const randomChange = Math.floor(Math.random() * 11) - 5; // -5 bis +5
      setViewerCount(Math.max(100, baseViewers + randomChange));
    };

    const updateSpots = () => {
      const baseSpots = 47;
      const randomChange = Math.floor(Math.random() * 3); // 0 bis 2
      setSpotsLeft(Math.max(1, baseSpots - randomChange));
    };

    updateViewers();
    updateSpots();

    const viewerInterval = setInterval(updateViewers, 5000);
    const spotsInterval = setInterval(updateSpots, 8000);

    return () => {
      clearInterval(viewerInterval);
      clearInterval(spotsInterval);
    };
  }, []);

  // Progress und Segment-Management
  useEffect(() => {
    if (!isPlaying) return;

    const totalDuration = vslSegments.reduce((sum, segment) => sum + segment.duration, 0);
    const currentTime = vslSegments
      .slice(0, currentSegment)
      .reduce((sum, segment) => sum + segment.duration, 0);

    const updateProgress = () => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min((elapsed / (totalDuration * 1000)) * 100, 100);
      setProgress(newProgress);

      // Segment-Wechsel
      let accumulatedTime = 0;
      for (let i = 0; i < vslSegments.length; i++) {
        accumulatedTime += vslSegments[i].duration * 1000;
        if (elapsed < accumulatedTime) {
          if (i !== currentSegment) {
            setCurrentSegment(i);
            if (vslSegments[i].revealSecret) {
              setShowSecret(true);
              toast({
                title: "🎯 Das Geheimnis wird enthüllt!",
                description: "Du erfährst jetzt, was hinter dieser Methode steckt!",
                duration: 5000
              });
            }
          }
          break;
        }
      }

      // VSL beendet
      if (elapsed >= totalDuration * 1000) {
        setIsPlaying(false);
        onComplete();
      }
    };

    const startTime = Date.now();
    intervalRef.current = setInterval(updateProgress, 100);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isPlaying, currentSegment, onComplete, toast]);

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  const currentSegmentData = vslSegments[currentSegment];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white">
      {/* Header mit Live-Indikatoren */}
      <div className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">LIVE</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="w-4 h-4" />
                <span className="text-sm">{viewerCount} Zuschauer</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {currentSegmentData.showUrgency && (
                <Badge variant="destructive" className="animate-pulse">
                  <Clock className="w-3 h-3 mr-1" />
                  Nur noch {spotsLeft} Plätze!
                </Badge>
              )}
              {currentSegmentData.showScarcity && (
                <Badge variant="secondary" className="bg-orange-600">
                  <Star className="w-3 h-3 mr-1" />
                  Begrenzt verfügbar!
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Haupt-Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Video-Player */}
          <div className="relative bg-black rounded-lg overflow-hidden mb-8">
            <video
              ref={videoRef}
              className="w-full h-96 object-cover"
              poster="/images/video-poster.jpg"
            />
            
            {/* Video-Controls */}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Button
                    onClick={togglePlay}
                    variant="ghost"
                    size="sm"
                    className="text-white hover:bg-white/20"
                  >
                    {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                  </Button>
                  
                  <Button
                    onClick={toggleMute}
                    variant="ghost"
                    size="sm"
                    className="text-white hover:bg-white/20"
                  >
                    {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                  </Button>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Clock className="w-4 h-4" />
                  <span className="text-sm">
                    {Math.floor(progress)}% abgeschlossen
                  </span>
                </div>
              </div>
              
              <Progress value={progress} className="mt-2" />
            </div>
          </div>

          {/* Aktuelles Segment */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSegment}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <span className="text-white font-bold text-lg">
                          {currentSegment + 1}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold mb-4 text-white">
                        {currentSegmentData.title}
                      </h2>
                      
                      <p className="text-lg leading-relaxed text-gray-200 mb-6">
                        {currentSegmentData.content}
                      </p>
                      
                      {/* Psychologische Elemente */}
                      {currentSegmentData.showUrgency && (
                        <div className="bg-red-600/20 border border-red-500/30 rounded-lg p-4 mb-4">
                          <div className="flex items-center space-x-2">
                            <Zap className="w-5 h-5 text-red-400" />
                            <span className="font-semibold text-red-300">
                              ⚡ Dringend: Nur noch {spotsLeft} Plätze verfügbar!
                            </span>
                          </div>
                        </div>
                      )}
                      
                      {currentSegmentData.showScarcity && (
                        <div className="bg-orange-600/20 border border-orange-500/30 rounded-lg p-4 mb-4">
                          <div className="flex items-center space-x-2">
                            <Star className="w-5 h-5 text-orange-400" />
                            <span className="font-semibold text-orange-300">
                              ⭐ Diese Methode wird nur 100 Menschen gezeigt!
                            </span>
                          </div>
                        </div>
                      )}
                      
                      {showSecret && currentSegmentData.revealSecret && (
                        <div className="bg-gradient-to-r from-green-600/20 to-blue-600/20 border border-green-500/30 rounded-lg p-6">
                          <div className="text-center">
                            <h3 className="text-2xl font-bold text-green-300 mb-2">
                              🎯 Das Geheimnis wird enthüllt!
                            </h3>
                            <p className="text-lg text-green-200">
                              {currentSegmentData.content}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </AnimatePresence>

          {/* Segment-Navigation */}
          <div className="mt-8">
            <div className="flex flex-wrap gap-2">
              {vslSegments.map((segment, index) => (
                <button
                  key={segment.id}
                  onClick={() => setCurrentSegment(index)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    index === currentSegment
                      ? 'bg-blue-600 text-white'
                      : index < currentSegment
                      ? 'bg-green-600/20 text-green-300 border border-green-500/30'
                      : 'bg-gray-700/50 text-gray-400 hover:bg-gray-600/50'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}; 