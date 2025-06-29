import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { useToast } from '../hooks/use-toast';
import { trackLeadCapture } from '../lib/analytics';
import QuizResults from './QuizResults';

interface QuizQuestion {
  id: string;
  question: string;
  options: {
    value: string;
    label: string;
    description?: string;
  }[];
}

interface QuizFormProps {
  questions?: QuizQuestion[];
  quizId?: string;
  title?: string;
  description?: string;
  onComplete?: (results: any) => void;
  className?: string;
}

export function QuizForm({
  questions: propQuestions,
  quizId = "magic_tool",
  title = "Finde heraus, welcher Geld-Typ du bist!",
  description = "Beantworte 4 kurze Fragen und erhalte deine personalisierte Strategie für finanziellen Erfolg.",
  onComplete,
  className = ""
}: QuizFormProps) {
  // ALLE HOOKS AM ANFANG!
  const [questions, setQuestions] = useState<QuizQuestion[]>(propQuestions || []);
  const [isLoading, setIsLoading] = useState(!propQuestions);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [quizPersona, setQuizPersona] = useState<any>(null);
  const { toast } = useToast();

  useEffect(() => {
    if (propQuestions) {
      setQuestions(propQuestions);
      setIsLoading(false);
      return;
    }
    const fetchQuizQuestions = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await fetch(`/api/quizzes/${quizId}`);
        const data = await response.json();
        if (data.success && data.quiz) {
          setQuestions(data.quiz.questions);
          // Verwende Titel und Beschreibung von der API, falls verfügbar
          if (data.quiz.title) title = data.quiz.title;
          if (data.quiz.description) description = data.quiz.description;
        } else {
          throw new Error(data.error || 'Fehler beim Laden der Quiz-Fragen');
        }
      } catch (err) {
        console.error('Error fetching quiz questions:', err);
        setError(err instanceof Error ? err.message : 'Unbekannter Fehler');
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuizQuestions();
  }, [quizId, propQuestions]);

  // AB HIER: Bedingungen und Rückgaben!
  if (isLoading) {
    return (
      <Card className={`w-full max-w-2xl mx-auto ${className}`}>
        <CardContent className="p-8">
          <div className="flex items-center justify-center space-x-2">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="text-gray-600">Lade Quiz-Fragen...</span>
          </div>
        </CardContent>
      </Card>
    );
  }
  if (error) {
    return (
      <Card className={`w-full max-w-2xl mx-auto ${className}`}>
        <CardContent className="p-8">
          <div className="text-center">
            <div className="text-red-600 mb-4">
              <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Fehler beim Laden</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button 
              onClick={() => window.location.reload()} 
              className="bg-blue-600 hover:bg-blue-700"
            >
              Erneut versuchen
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }
  if (!questions || questions.length === 0) {
    return (
      <Card className={`w-full max-w-2xl mx-auto ${className}`}>
        <CardContent className="p-8">
          <div className="text-center">
            <p className="text-gray-600">Keine Quiz-Fragen verfügbar.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const handleAnswer = (questionId: string, answer: string) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const generatePersona = (answers: Record<string, string>) => {
    const profile = answers['1'];
    const problem = answers['2'];
    const goal = answers['3'];
    const blocker = answers['4'];

    // Erweiterte Profile mapping
    const profiles: Record<string, { name: string; description: string; characteristics: string[] }> = {
      'student': {
        name: 'Struggling Student Sarah',
        description: 'Studentin mit begrenztem Budget, sucht nach flexiblen Einkommensmöglichkeiten',
        characteristics: ['Flexible Zeitplanung', 'Technik-affin', 'Lernbereit', 'Budget-bewusst']
      },
      'employee': {
        name: 'Burnout-Bernd',
        description: 'Vollzeit-Angestellter, der nach finanzieller Unabhängigkeit strebt',
        characteristics: ['Zeitlich eingeschränkt', 'Erfahrung im Business', 'Strukturiert', 'Zielorientiert']
      },
      'parent': {
        name: 'Overwhelmed Mom Maria',
        description: 'Elternteil, das Familie und Einkommen unter einen Hut bringen muss',
        characteristics: ['Flexible Arbeitszeiten', 'Familienorientiert', 'Multitasking', 'Geduldig']
      }
    };

    const problems: Record<string, { name: string; impact: string; solution: string }> = {
      'money_tight': {
        name: 'Monatliche Geldknappheit',
        impact: 'Stress durch finanzielle Unsicherheit',
        solution: 'Sofortige Einkommensgenerierung mit minimalem Risiko'
      },
      'no_time': {
        name: 'Zeitmangel durch Vollzeitarbeit',
        impact: 'Keine Zeit für traditionelle Nebenjobs',
        solution: 'Automatisierte Systeme mit flexibler Zeiteinteilung'
      },
      'no_idea': {
        name: 'Orientierungslosigkeit beim Start',
        impact: 'Überforderung durch zu viele Optionen',
        solution: 'Strukturierter Einstieg mit klarem Fahrplan'
      }
    };

    const goals: Record<string, { range: string; timeline: string; strategy: string }> = {
      'basic': {
        range: '500-1.500€ monatlich',
        timeline: '30-60 Tage',
        strategy: 'Konsistente Grundlagen mit skalierbarem Potenzial'
      },
      'substantial': {
        range: '2.000-5.000€ monatlich',
        timeline: '3-6 Monate',
        strategy: 'Multiple Einkommensströme mit Automatisierung'
      },
      'freedom': {
        range: '5.000€+ monatlich',
        timeline: '6-12 Monate',
        strategy: 'Vollständige Automatisierung und Team-Aufbau'
      }
    };

    const blockers: Record<string, { name: string; solution: string; mindset: string }> = {
      'no_capital': {
        name: 'Kein Startkapital',
        solution: '0€-Start-Strategien mit vorhandenen Ressourcen',
        mindset: 'Kreativität über Kapital'
      },
      'no_skills': {
        name: 'Fehlende Fähigkeiten',
        solution: 'Schritt-für-Schritt-Training und Mentoring',
        mindset: 'Lernen durch Tun'
      },
      'no_network': {
        name: 'Keine Kontakte',
        solution: 'Online-Netzwerk-Aufbau und Community-Integration',
        mindset: 'Digitale Verbindungen schaffen'
      }
    };

    // Persona-Text generieren
    const profileData = profiles[profile] || profiles['student'];
    const problemData = problems[problem] || problems['money_tight'];
    const goalData = goals[goal] || goals['basic'];
    const blockerData = blockers[blocker] || blockers['no_capital'];

    const profileText = `${profileData.name} • ${problemData.name} • ${goalData.range}`;

    // Erweiterte Strategie-Empfehlung basierend auf Kombination
    let strategyText = '';
    let recommendedFunnel = '';
    let nextSteps: string[] = [];
    let timeline = '';
    let expectedResults = '';

    // Kombinations-basierte Strategie
    if (profile === 'student' && goal === 'basic') {
      strategyText = 'Magic Tool System - Perfekt für Studenten mit 0€ Startkapital. Erste 500€ in 30 Tagen möglich.';
      recommendedFunnel = 'magic_tool_student';
      nextSteps = [
        'Tägliche 30-Minuten-Routine etablieren',
        'Social Media Präsenz aufbauen',
        'Erste Kunden innerhalb von 7 Tagen gewinnen'
      ];
      timeline = '30 Tage bis zum ersten Einkommen';
      expectedResults = '500-800€ im ersten Monat';
    } else if (profile === 'parent' && problem === 'no_time') {
      strategyText = 'Magic Tool System - Ideal für flexible Arbeitszeiten zwischen Familie und Job. 15-30 Min täglich reichen.';
      recommendedFunnel = 'magic_tool_parent';
      nextSteps = [
        'Morgenroutine vor der Familie etablieren',
        'Abendzeit für Kundenbetreuung nutzen',
        'Wochenenden für Content-Erstellung'
      ];
      timeline = '45 Tage bis zum ersten Einkommen';
      expectedResults = '800-1.200€ im ersten Monat';
    } else if (profile === 'employee' && goal === 'substantial') {
      strategyText = 'Magic Tool System - Für ambitionierte Ziele und Skalierung auf 5.000€+. Multiple Einkommensströme aufbauen.';
      recommendedFunnel = 'magic_tool_employee';
      nextSteps = [
        'Frühmorgens 1 Stunde investieren',
        'Mittagspause für Kundenbetreuung nutzen',
        'Abends für Automatisierung arbeiten'
      ];
      timeline = '90 Tage bis zur Skalierung';
      expectedResults = '2.000-3.000€ im dritten Monat';
    } else if (goal === 'freedom') {
      strategyText = 'Magic Tool System - Der Weg zur finanziellen Freiheit. Vollständige Automatisierung und Team-Aufbau.';
      recommendedFunnel = 'magic_tool_freedom';
      nextSteps = [
        'System vollständig automatisieren',
        'Team von 3-5 Personen aufbauen',
        'Multiple Einkommensströme etablieren'
      ];
      timeline = '180 Tage bis zur finanziellen Freiheit';
      expectedResults = '5.000€+ ab dem sechsten Monat';
    } else {
      strategyText = 'Magic Tool System - Der bewährte Einstieg für alle, die ohne Risiko starten wollen.';
      recommendedFunnel = 'magic_tool';
      nextSteps = [
        'Grundlagen in 7 Tagen erlernen',
        'Erste Ergebnisse in 14 Tagen sehen',
        'Konsistente Steigerung über 30 Tage'
      ];
      timeline = '30 Tage bis zum ersten Einkommen';
      expectedResults = '500-1.500€ im ersten Monat';
    }

    return {
      type: profile || 'default',
      profileText,
      strategyText,
      recommendedFunnel,
      preferences: answers,
      persona: {
        profile: profileData,
        problem: problemData,
        goal: goalData,
        blocker: blockerData
      },
      actionPlan: {
        nextSteps,
        timeline,
        expectedResults
      }
    };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      toast({
        title: "E-Mail erforderlich",
        description: "Bitte gib deine E-Mail-Adresse ein, um deine Ergebnisse zu erhalten.",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      const persona = generatePersona(answers);

      // Sende Quiz-Ergebnisse an Backend
      const response = await fetch('/api/quiz/results', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          name: name || undefined,
          answers,
          persona,
          utmParams: {
            utm_source: 'quiz',
            utm_campaign: 'magic_tool',
            utm_medium: 'organic'
          },
          sessionId: undefined,
          pageUrl: window.location.href,
          referrer: document.referrer
        }),
      });

      const result = await response.json();

      if (result.success) {
        // Track Lead Capture
        await trackLeadCapture({
          email,
          name: name || undefined,
          source: 'quiz',
          funnel: 'magic_tool',
          quizAnswers: answers,
          persona
        });

        // Setze Quiz-Ergebnisse für Anzeige
        setQuizPersona(persona);
        setShowResults(true);

        // Speichere Persona-Daten im localStorage für Bridge-Seite
        localStorage.setItem('quizPersona', JSON.stringify(persona));

        // Speichere Lead-ID im localStorage für E-Mail-Preview
        if (result.lead?.id) {
          localStorage.setItem('leadId', result.lead.id.toString());
        }

        toast({
          title: "Quiz erfolgreich abgeschlossen!",
          description: "Du erhältst gleich eine E-Mail mit deiner personalisierten Strategie.",
        });

        // Call completion callback
        if (onComplete) {
          onComplete({
            answers,
            persona,
            lead: result.lead
          });
        }

        // Weiterleitung zur Bridge-Seite nach 3 Sekunden
        setTimeout(() => {
          window.location.href = '/bridge';
        }, 3000);
      } else {
        throw new Error(result.error || 'Unbekannter Fehler');
      }
    } catch (error) {
      console.error('Quiz submission error:', error);
      toast({
        title: "Fehler beim Absenden",
        description: "Bitte versuche es noch einmal oder kontaktiere uns direkt.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const currentQ = questions[currentQuestion];
  const isLastQuestion = currentQuestion === questions.length - 1;
  const canProceed = answers[currentQ?.id];

  // Zeige Quiz-Ergebnisse an
  if (showResults && quizPersona) {
    return (
      <QuizResults
        persona={quizPersona}
        onContinue={() => setShowResults(false)}
        className={className}
      />
    );
  }

  if (currentQuestion >= questions.length) {
    // Show results form
    return (
      <Card className={`w-full max-w-2xl mx-auto ${className}`}>
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-gray-900">
            Fast geschafft! 🎉
          </CardTitle>
          <CardDescription className="text-gray-600">
            Gib deine E-Mail-Adresse ein und erhalte sofort deine personalisierte Strategie.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Name (optional)</Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Dein Name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">E-Mail-Adresse *</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="deine@email.de"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full"
                  required
                />
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2">Deine Antworten:</h4>
              <div className="space-y-2 text-sm text-gray-600">
                {questions.map((q, index) => (
                  <div key={q.id} className="flex justify-between">
                    <span>Frage {index + 1}:</span>
                    <span className="font-medium">
                      {q.options.find(opt => opt.value === answers[q.id])?.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Wird verarbeitet...</span>
                </div>
              ) : (
                "Jetzt meine Strategie erhalten"
              )}
            </Button>

            <p className="text-xs text-gray-500 text-center">
              Du erhältst sofort Zugang zu deiner personalisierten Strategie und unserem kostenlosen Guide.
            </p>
          </form>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={`w-full max-w-2xl mx-auto ${className}`}>
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-bold text-gray-900">
          {title}
        </CardTitle>
        <CardDescription className="text-gray-600">
          {description}
        </CardDescription>
        <div className="flex justify-center space-x-2 mt-4">
          {questions.map((_, index) => (
            <div
              key={index}
              className={`w-3 h-3 rounded-full ${
                index === currentQuestion
                  ? 'bg-blue-600'
                  : index < currentQuestion
                  ? 'bg-green-500'
                  : 'bg-gray-300'
              }`}
            />
          ))}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {currentQ.question}
            </h3>
          </div>

          <RadioGroup
            value={answers[currentQ.id] || ''}
            onValueChange={(value) => handleAnswer(currentQ.id, value)}
            className="space-y-4"
          >
            {currentQ.options.map((option) => (
              <div key={option.value} className="flex items-center space-x-3">
                <RadioGroupItem value={option.value} id={option.value} />
                <Label htmlFor={option.value} className="flex-1 cursor-pointer">
                  <div className="font-medium text-gray-900">{option.label}</div>
                  {option.description && (
                    <div className="text-sm text-gray-600 mt-1">
                      {option.description}
                    </div>
                  )}
                </Label>
              </div>
            ))}
          </RadioGroup>

          <div className="flex justify-between pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={handlePrevious}
              disabled={currentQuestion === 0}
            >
              Zurück
            </Button>

            {isLastQuestion ? (
              <Button
                onClick={() => setCurrentQuestion(prev => prev + 1)}
                disabled={!canProceed}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Ergebnisse anzeigen
              </Button>
            ) : (
              <Button
                onClick={handleNext}
                disabled={!canProceed}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Weiter
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default QuizForm;
