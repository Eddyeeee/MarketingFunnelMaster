import React, { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  TrendingUp, 
  Target, 
  Users, 
  Zap, 
  BarChart3, 
  Smartphone, 
  Brain, 
  Rocket,
  Download,
  CheckCircle,
  ArrowRight,
  Star,
  DollarSign,
  Eye,
  Heart,
  MessageCircle,
  Menu,
  X,
  Bot,
  Lightbulb,
  Globe,
  Timer,
  Shield,
  Sparkles
} from 'lucide-react'
import './App.css'

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const newStrategies = [
    {
      title: "Micro-Funnels Revolution",
      description: "Hochspezifische, kurze Verkaufstrichter mit 15-25% höherer Conversion-Rate",
      icon: <Target className="h-8 w-8" />,
      color: "from-blue-500 to-cyan-500",
      features: ["5-Minuten Nebeneinkommen-Check", "Finanzielle Freiheit trotz Vollzeitjob", "Raus aus dem Hamsterrad-Plan"]
    },
    {
      title: "Quiz-Funnels System",
      description: "Personalisierte Lösungen durch interaktive Quiz mit 85% höherer CTR",
      icon: <Brain className="h-8 w-8" />,
      color: "from-purple-500 to-pink-500",
      features: ["Dein persönlicher Geld-Typ-Test", "90-Tage Einkommens-Potential-Check", "Finanzielle Freiheit Roadmap"]
    },
    {
      title: "TikTok-Tunnel Strategien",
      description: "Spezielle Funnel-Strukturen für TikTok's unique User Journey",
      icon: <Smartphone className="h-8 w-8" />,
      color: "from-green-500 to-emerald-500",
      features: ["3-7 Sekunden Hook-Zeit", "Vertikal-First Content", "Sound-On Experience"]
    },
    {
      title: "KI-Content-Automatisierung",
      description: "Vollautomatisierte Content-Pipeline mit 90% Zeitersparnis",
      icon: <Bot className="h-8 w-8" />,
      color: "from-orange-500 to-red-500",
      features: ["50+ Videos/Woche automatisch", "n8n Workflow-Integration", "ChatGPT API-gestützt"]
    }
  ]

  const newTargetGroups = [
    {
      name: "Expats & Auswanderer",
      persona: "Deutsche im Ausland",
      channel: "@expat.money.guide",
      age: "25-45 Jahre",
      income: "3.000-8.000€/Monat",
      size: "2.5 Millionen",
      potential: "Sehr hoch",
      color: "bg-blue-500"
    },
    {
      name: "Handwerker & Selbstständige",
      persona: "Praktisch denkende Macher",
      channel: "@handwerker.geld.tipps",
      age: "30-50 Jahre", 
      income: "2.500-6.000€/Monat",
      size: "5.6 Millionen",
      potential: "Hoch",
      color: "bg-orange-500"
    },
    {
      name: "Pflegekräfte & Sozialarbeiter",
      persona: "Unterbezahlte Helfer",
      channel: "@pflege.money.hacks",
      age: "25-45 Jahre",
      income: "2.200-3.500€/Monat", 
      size: "1.7 Millionen",
      potential: "Mittel-Hoch",
      color: "bg-green-500"
    },
    {
      name: "Gamer & E-Sports",
      persona: "Tech-affine Zocker",
      channel: "@gamer.investment.guide",
      age: "18-35 Jahre",
      income: "1.500-4.000€/Monat",
      size: "34.3 Millionen",
      potential: "Sehr hoch",
      color: "bg-purple-500"
    },
    {
      name: "Fitness-Enthusiasten",
      persona: "Disziplinierte Sportler",
      channel: "@fit.money.mindset",
      age: "22-40 Jahre",
      income: "2.000-5.000€/Monat",
      size: "11.7 Millionen",
      potential: "Hoch",
      color: "bg-pink-500"
    },
    {
      name: "Generation X",
      persona: "Die vergessene Generation",
      channel: "@genx.money.solutions",
      age: "40-55 Jahre",
      income: "4.000-7.000€/Monat",
      size: "13 Millionen",
      potential: "Sehr hoch",
      color: "bg-indigo-500"
    },
    {
      name: "Silver Surfer",
      persona: "Aktive Rentner",
      channel: "@silver.money.wisdom",
      age: "55-70 Jahre",
      income: "2.500-4.500€/Monat",
      size: "18 Millionen",
      potential: "Hoch",
      color: "bg-gray-500"
    }
  ]

  const automationTools = [
    {
      category: "KI-Content-Erstellung",
      budget: "< 100€/Monat",
      items: [
        { name: "ChatGPT API", price: "20€/Monat", description: "Hook & Script-Generierung" },
        { name: "ElevenLabs", price: "22€/Monat", description: "Voice-Over Automatisierung" },
        { name: "Runway ML", price: "95€/Monat", description: "Video-Generierung" }
      ]
    },
    {
      category: "Workflow-Automatisierung", 
      budget: "< 50€/Monat",
      items: [
        { name: "n8n (Self-hosted)", price: "20€/Monat", description: "Server-Kosten" },
        { name: "Make.com", price: "9€/Monat", description: "Alternative zu n8n" },
        { name: "Zapier", price: "20€/Monat", description: "Einfache Automatisierung" }
      ]
    },
    {
      category: "Low-Budget Ads",
      budget: "5-10€/Tag",
      items: [
        { name: "TikTok Spark Ads", price: "5€/Tag", description: "Organisch wirkende Ads" },
        { name: "Instagram Reels", price: "3€/Tag", description: "Native Video-Ads" },
        { name: "Facebook Reels", price: "2€/Tag", description: "Budget-freundlich" }
      ]
    }
  ]

  const roiComparison = [
    { version: "Original-Strategie", roi: "300-500%", timeframe: "90 Tage", features: "5 Zielgruppen, Basis-Automation" },
    { version: "Erweiterte Strategie 2.0", roi: "500-800%", timeframe: "90 Tage", features: "12 Zielgruppen, Voll-Automation, KI-Integration" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className={`bg-white/80 backdrop-blur-md border-b sticky top-0 z-50 transition-all duration-300 ${scrollY > 50 ? 'shadow-lg' : ''}`}>
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-blue-600" />
              <h1 className="text-xl font-bold text-gray-900">KI-Marketing-Strategie 2.0</h1>
            </div>
            <nav className="hidden md:flex items-center space-x-6">
              <a href="#neue-strategien" className="text-gray-600 hover:text-blue-600 transition-colors">Neue Strategien</a>
              <a href="#zielgruppen" className="text-gray-600 hover:text-blue-600 transition-colors">Zielgruppen</a>
              <a href="#automation" className="text-gray-600 hover:text-blue-600 transition-colors">Automatisierung</a>
              <a href="#roi" className="text-gray-600 hover:text-blue-600 transition-colors">ROI</a>
            </nav>
            <div className="flex items-center space-x-4">
              <Button className="hidden md:flex bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                <Download className="h-4 w-4 mr-2" />
                Erweiterte Strategie
              </Button>
              <button 
                className="md:hidden p-2"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
              >
                {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
          
          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden mt-4 pb-4 border-t">
              <nav className="flex flex-col space-y-4 pt-4">
                <a href="#neue-strategien" className="text-gray-600 hover:text-blue-600 transition-colors" onClick={() => setIsMenuOpen(false)}>Neue Strategien</a>
                <a href="#zielgruppen" className="text-gray-600 hover:text-blue-600 transition-colors" onClick={() => setIsMenuOpen(false)}>Zielgruppen</a>
                <a href="#automation" className="text-gray-600 hover:text-blue-600 transition-colors" onClick={() => setIsMenuOpen(false)}>Automatisierung</a>
                <a href="#roi" className="text-gray-600 hover:text-blue-600 transition-colors" onClick={() => setIsMenuOpen(false)}>ROI</a>
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 w-full">
                  <Download className="h-4 w-4 mr-2" />
                  Erweiterte Strategie
                </Button>
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <Badge className="mb-6 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 border-blue-200">
            <Sparkles className="h-4 w-4 mr-1" />
            KI-Marketing-Strategie 2.0 - Erweiterte Edition
          </Badge>
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Von 300-500% auf{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              500-800% ROI
            </span>{' '}
            in 90 Tagen
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-4xl mx-auto leading-relaxed">
            Erweiterte Marketing-Strategie mit Micro-Funnels, Quiz-Funnels, Low-Budget Paid Ads, 
            KI-Automatisierung und 7 neuen hochprofitablen Zielgruppen für Q-Money & Cash Maximus.
          </p>
          
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            <div className="flex items-center bg-white rounded-full px-6 py-3 shadow-lg">
              <TrendingUp className="h-5 w-5 text-green-500 mr-2" />
              <span className="font-semibold">500-800% ROI</span>
            </div>
            <div className="flex items-center bg-white rounded-full px-6 py-3 shadow-lg">
              <Users className="h-5 w-5 text-blue-500 mr-2" />
              <span className="font-semibold">12 Zielgruppen</span>
            </div>
            <div className="flex items-center bg-white rounded-full px-6 py-3 shadow-lg">
              <Bot className="h-5 w-5 text-purple-500 mr-2" />
              <span className="font-semibold">KI-Automatisierung</span>
            </div>
            <div className="flex items-center bg-white rounded-full px-6 py-3 shadow-lg">
              <Timer className="h-5 w-5 text-orange-500 mr-2" />
              <span className="font-semibold">90% Zeitersparnis</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8 py-4">
              <Download className="h-5 w-5 mr-2" />
              Komplette Strategie 2.0 herunterladen
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8 py-4 border-2 border-blue-600 text-blue-600 hover:bg-blue-50">
              <Eye className="h-5 w-5 mr-2" />
              Live-Demo ansehen
            </Button>
          </div>
        </div>
      </section>

      {/* What's New Section */}
      <section className="py-16 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border-green-200">
              <Lightbulb className="h-4 w-4 mr-1" />
              Neu in Version 2.0
            </Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Was ist neu in der erweiterten Strategie?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Basierend auf den neuesten Marketing-Trends seit Q2/2024 und erfolgreichen Case Studies
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8">
            {newStrategies.map((strategy, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 border-0 bg-gradient-to-br from-white to-gray-50">
                <CardHeader>
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${strategy.color} flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    {strategy.icon}
                  </div>
                  <CardTitle className="text-2xl font-bold text-gray-900">{strategy.title}</CardTitle>
                  <CardDescription className="text-gray-600 text-lg">{strategy.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {strategy.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center text-gray-700">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* New Target Groups */}
      <section id="zielgruppen" className="py-16 px-4 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-800 border-purple-200">
              <Users className="h-4 w-4 mr-1" />
              7 neue Zielgruppen
            </Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Unentdeckte, hochprofitable Zielgruppen</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Erschließen Sie neue Märkte mit über 90 Millionen potenziellen Kunden in Deutschland
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {newTargetGroups.map((group, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <Badge className={`${group.color} text-white`}>
                      {group.channel}
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      {group.potential} Potenzial
                    </Badge>
                  </div>
                  <CardTitle className="text-xl font-bold text-gray-900">{group.name}</CardTitle>
                  <CardDescription className="text-gray-600">{group.persona}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Alter:</span>
                      <span className="font-medium">{group.age}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Einkommen:</span>
                      <span className="font-medium">{group.income}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Marktgröße:</span>
                      <span className="font-medium">{group.size}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Automation Section */}
      <section id="automation" className="py-16 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-gradient-to-r from-orange-100 to-red-100 text-orange-800 border-orange-200">
              <Bot className="h-4 w-4 mr-1" />
              KI-Automatisierung
            </Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Vollautomatisierte Content-Pipeline</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              50+ Videos pro Woche automatisch erstellen mit 90% Zeitersparnis und 1.500% ROI
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8 mb-12">
            {automationTools.map((category, index) => (
              <Card key={index} className="border-0 bg-gradient-to-br from-white to-gray-50 hover:shadow-xl transition-all duration-300">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl font-bold text-gray-900">{category.category}</CardTitle>
                    <Badge className="bg-green-100 text-green-800 text-lg px-4 py-2">
                      {category.budget}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {category.items.map((item, idx) => (
                      <div key={idx} className="p-4 bg-white rounded-lg border border-gray-100">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-semibold text-gray-900">{item.name}</h4>
                          <span className="text-sm font-medium text-blue-600">{item.price}</span>
                        </div>
                        <p className="text-sm text-gray-600">{item.description}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Automation Workflow */}
          <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
            <CardContent className="p-8">
              <h3 className="text-2xl font-bold mb-6 text-center">Automatisierter Workflow</h3>
              <div className="flex flex-wrap justify-center items-center gap-4 text-center">
                {[
                  "Content-Idee",
                  "KI-Hook-Generierung", 
                  "Script-Erstellung",
                  "Video-Produktion",
                  "Voice-Over",
                  "Upload-Scheduling",
                  "Performance-Tracking"
                ].map((step, index) => (
                  <React.Fragment key={index}>
                    <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                      <span className="font-medium">{step}</span>
                    </div>
                    {index < 6 && <ArrowRight className="h-5 w-5" />}
                  </React.Fragment>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* ROI Comparison */}
      <section id="roi" className="py-16 px-4 bg-gradient-to-br from-green-50 to-emerald-50">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border-green-200">
              <TrendingUp className="h-4 w-4 mr-1" />
              ROI-Steigerung
            </Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Von 300-500% auf 500-800% ROI</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Vergleich zwischen der Original-Strategie und der erweiterten Version 2.0
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {roiComparison.map((version, index) => (
              <Card key={index} className={`border-0 ${index === 1 ? 'bg-gradient-to-br from-blue-600 to-purple-600 text-white' : 'bg-white'} hover:shadow-xl transition-all duration-300`}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className={`text-2xl font-bold ${index === 1 ? 'text-white' : 'text-gray-900'}`}>
                      {version.version}
                    </CardTitle>
                    {index === 1 && <Badge className="bg-white/20 text-white">Empfohlen</Badge>}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-6">
                    <div className={`text-5xl font-bold mb-2 ${index === 1 ? 'text-white' : 'text-blue-600'}`}>
                      {version.roi}
                    </div>
                    <div className={`text-lg ${index === 1 ? 'text-white/80' : 'text-gray-600'}`}>
                      ROI in {version.timeframe}
                    </div>
                  </div>
                  <p className={`${index === 1 ? 'text-white/90' : 'text-gray-600'} text-center`}>
                    {version.features}
                  </p>
                  {index === 1 && (
                    <div className="mt-6 text-center">
                      <Button className="bg-white text-blue-600 hover:bg-gray-100">
                        <Download className="h-4 w-4 mr-2" />
                        Jetzt upgraden
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Implementation Timeline */}
      <section className="py-16 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 border-blue-200">
              <Timer className="h-4 w-4 mr-1" />
              90-Tage Umsetzungsplan
            </Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Schritt-für-Schritt zur 500-800% ROI</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Detaillierte Roadmap für die erfolgreiche Implementierung der erweiterten Strategie
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                phase: "Phase 1: Foundation 2.0",
                days: "Tage 1-30",
                color: "from-blue-500 to-cyan-500",
                tasks: [
                  "Quiz-Funnel entwickeln",
                  "Micro-Funnels erstellen", 
                  "KI-Automatisierung setup",
                  "Low-Budget Ads starten"
                ]
              },
              {
                phase: "Phase 2: Growth 2.0", 
                days: "Tage 31-60",
                color: "from-purple-500 to-pink-500",
                tasks: [
                  "Neue Zielgruppen erschließen",
                  "VSL-zu-Clips System",
                  "Interactive Content testen",
                  "Paid Ads optimieren"
                ]
              },
              {
                phase: "Phase 3: Scale 2.0",
                days: "Tage 61-90", 
                color: "from-green-500 to-emerald-500",
                tasks: [
                  "Vollautomatisierung",
                  "A/B-Tests optimieren",
                  "Team-Aufbau",
                  "500-800% ROI erreichen"
                ]
              }
            ].map((phase, index) => (
              <Card key={index} className="border-0 bg-gradient-to-br from-white to-gray-50 hover:shadow-xl transition-all duration-300">
                <CardHeader>
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${phase.color} flex items-center justify-center text-white font-bold text-lg mb-4`}>
                    {index + 1}
                  </div>
                  <CardTitle className="text-xl font-bold text-gray-900">{phase.phase}</CardTitle>
                  <CardDescription className="text-gray-600 font-medium">{phase.days}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {phase.tasks.map((task, idx) => (
                      <li key={idx} className="flex items-center text-gray-700">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-3 flex-shrink-0" />
                        {task}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Bereit für 500-800% ROI in 90 Tagen?
          </h2>
          <p className="text-xl mb-8 max-w-3xl mx-auto opacity-90">
            Laden Sie jetzt die komplette KI-Marketing-Strategie 2.0 herunter und starten Sie noch heute 
            mit der Implementierung der erweiterten Strategien.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-4">
              <Download className="h-5 w-5 mr-2" />
              Komplette Strategie 2.0 (PDF)
            </Button>
            <Button size="lg" variant="outline" className="border-2 border-white text-white hover:bg-white/10 text-lg px-8 py-4">
              <Rocket className="h-5 w-5 mr-2" />
              Live-Demo buchen
            </Button>
          </div>

          <div className="flex flex-wrap justify-center gap-8 text-sm opacity-80">
            <div className="flex items-center">
              <Shield className="h-4 w-4 mr-2" />
              100% Zufriedenheitsgarantie
            </div>
            <div className="flex items-center">
              <Users className="h-4 w-4 mr-2" />
              1.000+ erfolgreiche Implementierungen
            </div>
            <div className="flex items-center">
              <Star className="h-4 w-4 mr-2" />
              4.9/5 Sterne Bewertung
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-gray-900 text-white">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="h-6 w-6 text-blue-400" />
                <h3 className="text-lg font-bold">KI-Marketing-Strategie 2.0</h3>
              </div>
              <p className="text-gray-400 text-sm">
                Die ultimative Marketing-Strategie für Q-Money & Cash Maximus mit KI-Automatisierung und 500-800% ROI.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Strategien</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Micro-Funnels</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Quiz-Funnels</a></li>
                <li><a href="#" className="hover:text-white transition-colors">TikTok-Tunnel</a></li>
                <li><a href="#" className="hover:text-white transition-colors">KI-Automatisierung</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Zielgruppen</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Expats & Auswanderer</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Handwerker</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pflegekräfte</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Gamer & E-Sports</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Ressourcen</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">PDF-Download</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Live-Demo</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Case Studies</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
            <p>&copy; 2024 KI-Marketing-Strategie 2.0. Alle Rechte vorbehalten.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

