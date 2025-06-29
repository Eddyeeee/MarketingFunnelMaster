import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { CheckCircle, Clock, Target, TrendingUp, ArrowRight } from 'lucide-react';

interface QuizResultsProps {
  persona: {
    type: string;
    profileText: string;
    strategyText: string;
    recommendedFunnel: string;
    persona: {
      profile: {
        name: string;
        description: string;
        characteristics: string[];
      };
      problem: {
        name: string;
        impact: string;
        solution: string;
      };
      goal: {
        range: string;
        timeline: string;
        strategy: string;
      };
      blocker: {
        name: string;
        solution: string;
        mindset: string;
      };
    };
    actionPlan: {
      nextSteps: string[];
      timeline: string;
      expectedResults: string;
    };
  };
  onContinue?: () => void;
  className?: string;
}

export function QuizResults({ persona, onContinue, className = "" }: QuizResultsProps) {
  const { profile, problem, goal, blocker } = persona.persona;
  const { nextSteps, timeline, expectedResults } = persona.actionPlan;

  return (
    <Card className={`w-full max-w-4xl mx-auto ${className}`}>
      <CardHeader className="text-center bg-gradient-to-r from-blue-50 to-purple-50 rounded-t-lg">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
            <Target className="w-8 h-8 text-white" />
          </div>
        </div>
        <CardTitle className="text-3xl font-bold text-gray-900 mb-2">
          Dein personalisierter Erfolgsplan! 🎯
        </CardTitle>
        <CardDescription className="text-lg text-gray-600">
          Basierend auf deinen Antworten haben wir die perfekte Strategie für dich entwickelt
        </CardDescription>
      </CardHeader>

      <CardContent className="p-8">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Linke Spalte: Persona & Strategie */}
          <div className="space-y-6">
            {/* Dein Profil */}
            <div className="bg-blue-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-3 flex items-center">
                <CheckCircle className="w-5 h-5 text-blue-600 mr-2" />
                Dein Profil: {profile.name}
              </h3>
              <p className="text-gray-700 mb-4">{profile.description}</p>
              <div className="flex flex-wrap gap-2">
                {profile.characteristics.map((char, index) => (
                  <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800">
                    {char}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Dein Problem & Lösung */}
            <div className="bg-orange-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Dein Hauptproblem: {problem.name}
              </h3>
              <p className="text-gray-700 mb-3">
                <strong>Auswirkung:</strong> {problem.impact}
              </p>
              <p className="text-gray-700">
                <strong>Unsere Lösung:</strong> {problem.solution}
              </p>
            </div>

            {/* Deine Ziele */}
            <div className="bg-green-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-3 flex items-center">
                <TrendingUp className="w-5 h-5 text-green-600 mr-2" />
                Deine Ziele: {goal.range}
              </h3>
              <p className="text-gray-700 mb-2">
                <strong>Timeline:</strong> {goal.timeline}
              </p>
              <p className="text-gray-700">
                <strong>Strategie:</strong> {goal.strategy}
              </p>
            </div>
          </div>

          {/* Rechte Spalte: Action Plan */}
          <div className="space-y-6">
            {/* Empfohlene Strategie */}
            <div className="bg-purple-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Deine empfohlene Strategie
              </h3>
              <p className="text-gray-700 mb-4">{persona.strategyText}</p>
              <Badge variant="default" className="bg-purple-600">
                {persona.recommendedFunnel.replace('_', ' ').toUpperCase()}
              </Badge>
            </div>

            {/* Dein Action Plan */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-3 flex items-center">
                <Clock className="w-5 h-5 text-gray-600 mr-2" />
                Dein Action Plan
              </h3>
              
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2">Nächste Schritte:</p>
                <ol className="list-decimal list-inside space-y-2 text-gray-700">
                  {nextSteps.map((step, index) => (
                    <li key={index} className="text-sm">{step}</li>
                  ))}
                </ol>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-white p-3 rounded border">
                  <p className="font-semibold text-gray-900">Timeline</p>
                  <p className="text-gray-600">{timeline}</p>
                </div>
                <div className="bg-white p-3 rounded border">
                  <p className="font-semibold text-gray-900">Erwartete Ergebnisse</p>
                  <p className="text-gray-600">{expectedResults}</p>
                </div>
              </div>
            </div>

            {/* Mindset & Lösung */}
            <div className="bg-yellow-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Dein größter Blocker: {blocker.name}
              </h3>
              <p className="text-gray-700 mb-3">
                <strong>Unsere Lösung:</strong> {blocker.solution}
              </p>
              <p className="text-gray-700">
                <strong>Richtiges Mindset:</strong> {blocker.mindset}
              </p>
            </div>
          </div>
        </div>

        {/* Call-to-Action */}
        <div className="mt-8 text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 rounded-lg text-white">
            <h3 className="text-2xl font-bold mb-2">
              Bereit für deine finanzielle Transformation? 🚀
            </h3>
            <p className="text-blue-100 mb-6">
              Erhalte jetzt deinen personalisierten 30-Tage-Plan und starte noch heute!
            </p>
            <Button
              onClick={onContinue}
              size="lg"
              className="bg-white text-blue-600 hover:bg-gray-100 font-semibold px-8 py-3"
            >
              Jetzt starten
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
          
          <p className="text-xs text-gray-500 mt-4">
            Du erhältst sofort Zugang zu deinem personalisierten Plan und unserem exklusiven Community-Bereich.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

export default QuizResults; 