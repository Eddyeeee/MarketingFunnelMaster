import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GraduationCap, Briefcase, Heart, Clock, HourglassIcon, Infinity, TrendingUp, Bird, Shield, Trophy, Download } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { trackEvent } from "@/lib/analytics";
import { toast } from "@/hooks/use-toast";

const quizSchema = z.object({
  answers: z.record(z.string()),
  email: z.string().email("Bitte gib eine gültige E-Mail-Adresse ein").optional(),
  firstName: z.string().min(2, "Bitte gib deinen Vornamen ein").optional(),
});

type QuizFormData = z.infer<typeof quizSchema>;

const questions = [
  {
    id: '1',
    question: 'Welcher Typ beschreibt dich am besten?',
    options: [
      {
        value: 'student',
        icon: GraduationCap,
        title: 'Struggling Student',
        description: 'Student/Azubi mit wenig Budget, will nebenbei verdienen'
      },
      {
        value: 'employee',
        icon: Briefcase,
        title: 'Burnout-Bernd',
        description: 'Angestellte/r, frustriert vom Hamsterrad'
      },
      {
        value: 'parent',
        icon: Heart,
        title: 'Overwhelmed Mom',
        description: 'Alleinerziehend oder Vollzeit-Mama, braucht Extra-Einkommen'
      }
    ]
  },
  {
    id: '2',
    question: 'Was ist dein größtes Problem gerade?',
    options: [
      {
        value: 'money_tight',
        icon: Clock,
        title: 'Geld ist knapp',
        description: 'Jeden Monat kämpfe ich, über die Runden zu kommen'
      },
      {
        value: 'no_time',
        icon: HourglassIcon,
        title: 'Keine Zeit',
        description: 'Ich arbeite schon viel, habe kaum Zeit für was Neues'
      },
      {
        value: 'no_idea',
        icon: Infinity,
        title: 'Keine Ahnung wo anfangen',
        description: 'Will was ändern, weiß aber nicht wie'
      }
    ]
  },
  {
    id: '3',
    question: 'Wie viel möchtest du zusätzlich verdienen?',
    options: [
      {
        value: 'basic',
        icon: TrendingUp,
        title: '500-1.500€ monatlich',
        description: 'Würde meine Sorgen deutlich reduzieren'
      },
      {
        value: 'substantial',
        icon: Bird,
        title: '2.000-5.000€ monatlich',
        description: 'Will finanziell unabhängig werden'
      },
      {
        value: 'freedom',
        icon: Shield,
        title: '5.000€+ monatlich',
        description: 'Träume von kompletter finanzieller Freiheit'
      }
    ]
  },
  {
    id: '4',
    question: 'Was hält dich zurück?',
    options: [
      {
        value: 'no_capital',
        icon: TrendingUp,
        title: 'Kein Startkapital',
        description: 'Habe kein Geld zum Investieren'
      },
      {
        value: 'no_experience',
        icon: Bird,
        title: 'Keine Erfahrung',
        description: 'Weiß nicht, wo ich anfangen soll'
      },
      {
        value: 'tried_failed',
        icon: Shield,
        title: 'Schon mal versucht',
        description: 'Hatte schon mal Hoffnung, wurde enttäuscht'
      }
    ]
  }
];

export default function QuizForm() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState<any>(null);

  const form = useForm<QuizFormData>({
    resolver: zodResolver(quizSchema)
  });

  const quizMutation = useMutation({
    mutationFn: async (data: { answers: Record<string, string>; email?: string }) => {
      const response = await apiRequest('POST', '/api/quiz/results', data);
      return response.json();
    },
    onSuccess: (data) => {
      setResults(data);
      setShowResults(true);
      trackEvent('quiz_completed', 'conversion', 'quiz_form');
    },
    onError: (error) => {
      toast({
        title: "Fehler",
        description: "Beim Verarbeiten der Quiz-Ergebnisse ist ein Fehler aufgetreten.",
        variant: "destructive"
      });
    }
  });

  const leadMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await apiRequest('POST', '/api/leads', data);
      return response.json();
    },
    onSuccess: () => {
      toast({
        title: "Erfolgreich!",
        description: "Deine Daten wurden gespeichert. Du erhältst gleich eine E-Mail von uns.",
      });
      trackEvent('quiz_lead_capture', 'conversion', 'quiz_results');
    }
  });

  const handleOptionSelect = (value: string) => {
    const newAnswers = { ...answers, [questions[currentQuestion].id]: value };
    setAnswers(newAnswers);
    
    trackEvent('quiz_answer', 'engagement', `question_${questions[currentQuestion].id}_${value}`);
    
    if (currentQuestion < questions.length - 1) {
      setTimeout(() => {
        setCurrentQuestion(currentQuestion + 1);
      }, 500);
    } else {
      // Quiz completed, process results
      setTimeout(() => {
        quizMutation.mutate({ answers: newAnswers });
      }, 500);
    }
  };

  const handleEmailSubmit = (data: QuizFormData) => {
    if (data.email && data.firstName) {
      leadMutation.mutate({
        email: data.email,
        firstName: data.firstName,
        quizAnswers: JSON.stringify(answers),
        funnel: results?.recommendedFunnel,
        source: 'quiz'
      });
    }
  };

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  if (showResults && results) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="bg-q-secondary text-white rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
            <Trophy size={32} />
          </div>
          <h3 className="text-2xl font-bold text-q-neutral-dark mb-4">
            Perfekt! Dein personalisierter Plan ist bereit
          </h3>
          <p className="text-q-neutral-medium mb-8">
            Basierend auf deinen Antworten haben wir die ideale Strategie für dich zusammengestellt.
          </p>
        </div>
        
        <Card className="shadow-sm">
          <CardContent className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-q-neutral-dark mb-2">Dein Profil:</h4>
                <p className="text-q-neutral-medium text-sm">{results.profileText}</p>
              </div>
              <div>
                <h4 className="font-semibold text-q-neutral-dark mb-2">Empfohlene Strategie:</h4>
                <p className="text-q-neutral-medium text-sm">{results.strategyText}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-sm">
          <CardContent className="p-6">
            <h4 className="font-semibold text-q-neutral-dark mb-4 text-center">
              Nächste Schritte:
            </h4>
            <div className="space-y-3">
              {results.nextSteps?.map((step: string, index: number) => (
                <div key={index} className="flex items-center space-x-3">
                  <div className="bg-q-secondary text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">
                    {index + 1}
                  </div>
                  <span className="text-q-neutral-dark">{step}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleEmailSubmit)} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="firstName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Vorname</FormLabel>
                    <FormControl>
                      <Input placeholder="Dein Vorname" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>E-Mail-Adresse</FormLabel>
                    <FormControl>
                      <Input type="email" placeholder="deine@email.de" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            
            <Button 
              type="submit" 
              className="w-full gradient-cta hover:bg-q-accent-dark text-white py-4 text-lg font-semibold"
              disabled={leadMutation.isPending}
            >
              <Download className="mr-2" size={20} />
              {leadMutation.isPending ? 'Wird verarbeitet...' : 'Kostenlosen personalisierten Plan sichern'}
            </Button>
            
            <p className="text-sm text-q-neutral-medium text-center">
              🔒 100% kostenlos • Keine Verpflichtungen • Sofortiger Zugang
            </p>
          </form>
        </Form>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <div className="flex justify-between text-sm text-q-neutral-medium mb-2">
          <span>Fortschritt</span>
          <span>{currentQuestion + 1} von {questions.length}</span>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {questions.map((question, index) => (
        <div 
          key={question.id} 
          className={`quiz-question ${index === currentQuestion ? 'active' : ''}`}
          style={{ display: index === currentQuestion ? 'block' : 'none' }}
        >
          <h3 className="text-2xl font-semibold text-q-neutral-dark mb-6">
            {question.question}
          </h3>
          <div className="space-y-4">
            {question.options.map((option) => {
              const IconComponent = option.icon;
              return (
                <Button
                  key={option.value}
                  onClick={() => handleOptionSelect(option.value)}
                  variant="outline"
                  className="quiz-option w-full text-left p-4 h-auto border-2 hover:border-q-primary hover:bg-blue-50 transition-all"
                >
                  <div className="flex items-center">
                    <IconComponent className="text-q-primary mr-4" size={24} />
                    <div>
                      <div className="font-semibold text-q-neutral-dark">{option.title}</div>
                      <div className="text-sm text-q-neutral-medium">{option.description}</div>
                    </div>
                  </div>
                </Button>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
