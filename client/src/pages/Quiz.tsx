import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import QuizForm from "@/components/QuizForm";
import { Link } from "wouter";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from '../hooks/use-toast';

export default function Quiz() {
  const { toast } = useToast();

  const handleQuizComplete = (results: any) => {
    console.log('Quiz completed:', results);
    
    // Optional: Weiterleitung zu VSL oder Bridge-Seite
    // setTimeout(() => {
    //   window.location.href = '/vsl';
    // }, 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Finde heraus, welcher Geld-Typ du bist! 💰
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Beantworte 4 kurze Fragen und erhalte deine personalisierte Strategie für finanziellen Erfolg.
            Basierend auf deinen Antworten entwickeln wir einen maßgeschneiderten Plan für dich.
          </p>
        </div>

        {/* Quiz Container */}
        <div className="flex justify-center">
          <QuizForm
            quizId="magic_tool"
            onComplete={handleQuizComplete}
            className="shadow-2xl"
          />
        </div>

        {/* Trust Indicators */}
        <div className="mt-16 text-center">
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">✅</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Personalisiert
              </h3>
              <p className="text-gray-600">
                Jede Strategie wird individuell auf deine Situation angepasst
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Sofort verfügbar
              </h3>
              <p className="text-gray-600">
                Du erhältst deine Strategie sofort nach dem Quiz
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Bewährt
              </h3>
              <p className="text-gray-600">
                Über 10.000 Menschen haben bereits mit dieser Methode Erfolg gehabt
              </p>
            </div>
          </div>
        </div>

        {/* Social Proof */}
        <div className="mt-16 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">
            Was andere über unser Quiz sagen:
          </h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-lg text-left">
              <p className="text-gray-700 mb-4">
                "Das Quiz hat mir geholfen, meine finanzielle Situation zu verstehen. 
                Die Strategie war genau das, was ich brauchte!"
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gray-300 rounded-full mr-3"></div>
                <div>
                  <p className="font-semibold text-gray-900">Sarah M.</p>
                  <p className="text-sm text-gray-600">Studentin, 24</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-lg text-left">
              <p className="text-gray-700 mb-4">
                "Endlich eine Strategie, die zu meinem Zeitplan passt. 
                Ich verdiene jetzt 2.000€ zusätzlich im Monat!"
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gray-300 rounded-full mr-3"></div>
                <div>
                  <p className="font-semibold text-gray-900">Michael K.</p>
                  <p className="text-sm text-gray-600">Angestellter, 32</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
