import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
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
  DollarSign,
  BarChart3,
  Settings,
  Eye,
  MousePointer,
  Sparkles,
  Rocket,
  Crown,
  Trophy,
  Coins
} from 'lucide-react';
import IntelligentVSL from '../components/IntelligentVSL';
import AnimatedVSL from '../components/AnimatedVSL';

interface VSLProps {
  className?: string;
}

export default function VSL({ className = "" }: VSLProps) {
  const [personaType, setPersonaType] = useState<string>('student');
  const [leadId, setLeadId] = useState<number | undefined>();
  const [activeTab, setActiveTab] = useState('vsl');
  const [showAnalytics, setShowAnalytics] = useState(false);

  useEffect(() => {
    // Lade Persona-Daten aus localStorage
    const personaData = localStorage.getItem('personaData');
    if (personaData) {
      const parsed = JSON.parse(personaData);
      setPersonaType(parsed.personaType || 'student');
    }

    // Lade Lead-ID aus localStorage
    const leadIdData = localStorage.getItem('leadId');
    if (leadIdData) {
      setLeadId(parseInt(leadIdData));
    }
  }, []);

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

  const personaTypes = [
    { id: 'student', name: 'Student', icon: '🎓' },
    { id: 'employee', name: 'Angestellter', icon: '💼' },
    { id: 'parent', name: 'Elternteil', icon: '👨‍👩‍👧‍👦' }
  ];

  return (
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 ${className}`}>
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Play className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Intelligente VSL</h1>
                <p className="text-sm text-gray-600">Personabasiert & dynamisch optimiert</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button
                onClick={() => setShowAnalytics(!showAnalytics)}
                variant="outline"
                size="sm"
                className="flex items-center space-x-2"
              >
                <BarChart3 className="w-4 h-4" />
                <span>Analytics</span>
              </Button>
              
              <Badge className={getPersonaColor(personaType)}>
                {getPersonaIcon(personaType)} {personaType.toUpperCase()}
              </Badge>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Persona Selector */}
        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">
                Wähle deine Persona für personalisierte VSL-Inhalte
              </h2>
              <Badge variant="outline" className="text-xs">
                Dynamische Anpassung
              </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {personaTypes.map((persona) => (
                <Button
                  key={persona.id}
                  onClick={() => setPersonaType(persona.id)}
                  variant={personaType === persona.id ? "default" : "outline"}
                  className={`h-auto p-4 flex flex-col items-center space-y-2 ${
                    personaType === persona.id 
                      ? 'bg-blue-600 hover:bg-blue-700' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <span className="text-2xl">{persona.icon}</span>
                  <span className="font-medium">{persona.name}</span>
                  <span className="text-xs opacity-75">
                    {persona.id === 'student' && '500€+ monatlich'}
                    {persona.id === 'employee' && '2.000€+ Zusatzeinkommen'}
                    {persona.id === 'parent' && 'Flexibles Familien-Einkommen'}
                  </span>
                </Button>
              ))}
                  </div>
              </CardContent>
            </Card>

        {/* Analytics Panel */}
        {showAnalytics && (
          <Card className="mb-8">
                <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5" />
                <span>VSL Performance Analytics</span>
                  </CardTitle>
              <CardDescription>
                Echtzeit-Daten für {personaType} Persona
                  </CardDescription>
                </CardHeader>
                <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">1,250</div>
                  <div className="text-sm text-gray-600">VSL Views</div>
                  <div className="text-xs text-green-600">+12% vs. letzter Monat</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">187</div>
                  <div className="text-sm text-gray-600">Conversions</div>
                  <div className="text-xs text-green-600">+8% vs. letzter Monat</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">15.0%</div>
                  <div className="text-sm text-gray-600">Conversion Rate</div>
                  <div className="text-xs text-green-600">+2.3% vs. letzter Monat</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600">320s</div>
                  <div className="text-sm text-gray-600">Avg. Time on VSL</div>
                  <div className="text-xs text-green-600">+45s vs. letzter Monat</div>
                </div>
                  </div>
                </CardContent>
              </Card>
            )}

        {/* Main VSL Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="vsl" className="flex items-center space-x-2">
              <Play className="w-4 h-4" />
              <span>VSL Player</span>
            </TabsTrigger>
            <TabsTrigger value="animated" className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4" />
              <span>Animated VSL</span>
            </TabsTrigger>
            <TabsTrigger value="sections" className="flex items-center space-x-2">
              <Settings className="w-4 h-4" />
              <span>VSL Sections</span>
            </TabsTrigger>
            <TabsTrigger value="optimization" className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4" />
              <span>Optimierung</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="vsl" className="space-y-6">
            <IntelligentVSL 
              personaType={personaType} 
              leadId={leadId}
            />
          </TabsContent>

          <TabsContent value="animated" className="space-y-6">
            <AnimatedVSL 
              personaType={personaType} 
              leadId={leadId}
            />
          </TabsContent>

          <TabsContent value="sections" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Settings className="w-5 h-5" />
                  <span>VSL Section Builder</span>
                </CardTitle>
                <CardDescription>
                  Erstelle und optimiere VSL-Sections für verschiedene Personas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {['hook', 'problem', 'solution', 'proof', 'offer', 'urgency', 'guarantee'].map((sectionType) => (
                    <Card key={sectionType} className="border-dashed">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-sm font-bold text-blue-600">
                              {sectionType.charAt(0).toUpperCase()}
                            </span>
                          </div>
                          <span className="font-medium capitalize">{sectionType}</span>
                    </div>
                        <p className="text-sm text-gray-600 mb-3">
                          {sectionType === 'hook' && 'Fange die Aufmerksamkeit'}
                          {sectionType === 'problem' && 'Identifiziere das Problem'}
                          {sectionType === 'solution' && 'Präsentiere die Lösung'}
                          {sectionType === 'proof' && 'Zeige Social Proof'}
                          {sectionType === 'offer' && 'Mache das Angebot'}
                          {sectionType === 'urgency' && 'Erzeuge Dringlichkeit'}
                          {sectionType === 'guarantee' && 'Gebe Garantien'}
                        </p>
                        <Button variant="outline" size="sm" className="w-full">
                          Bearbeiten
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="optimization" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* A/B Testing */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Eye className="w-5 h-5" />
                    <span>A/B Testing</span>
                </CardTitle>
                  <CardDescription>
                    Teste verschiedene VSL-Varianten
                </CardDescription>
              </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                      <div>
                        <div className="font-medium">Variant A</div>
                        <div className="text-sm text-gray-600">Standard VSL</div>
                      </div>
                      <Badge className="bg-green-100 text-green-800">Gewinner</Badge>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <div className="font-medium">Variant B</div>
                        <div className="text-sm text-gray-600">Kürzere VSL</div>
                      </div>
                      <Badge variant="outline">Test</Badge>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <div className="font-medium">Variant C</div>
                        <div className="text-sm text-gray-600">Video-First</div>
                      </div>
                      <Badge variant="outline">Test</Badge>
                </div>
                </div>
              </CardContent>
            </Card>

              {/* Conversion Optimization */}
              <Card>
              <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <MousePointer className="w-5 h-5" />
                    <span>Conversion Optimization</span>
                </CardTitle>
                  <CardDescription>
                    Optimierung basierend auf User-Verhalten
                  </CardDescription>
              </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Exit-Intent Popup</span>
                      <Badge className="bg-green-100 text-green-800">Aktiv</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Countdown Timer</span>
                      <Badge className="bg-green-100 text-green-800">Aktiv</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Social Proof</span>
                      <Badge className="bg-green-100 text-green-800">Aktiv</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Dynamic Pricing</span>
                      <Badge className="bg-green-100 text-green-800">Aktiv</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Persona-Specific Content</span>
                      <Badge className="bg-green-100 text-green-800">Aktiv</Badge>
                </div>
                </div>
              </CardContent>
            </Card>
          </div>
          </TabsContent>
        </Tabs>
        </div>
    </div>
  );
}
