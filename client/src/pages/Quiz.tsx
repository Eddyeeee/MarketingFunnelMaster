import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import QuizForm from "@/components/QuizForm";
import { Link } from "wouter";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Quiz() {
  return (
    <div className="min-h-screen bg-gray-50">
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
                <span className="text-lg font-medium text-q-neutral-medium ml-2">Quiz</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Quiz Content */}
      <section className="py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-q-neutral-dark mb-4">
              Finanzielle Freiheit Quiz
            </h1>
            <p className="text-xl text-q-neutral-medium">
              Finde deinen personalisierten Weg zum passiven Einkommen
            </p>
          </div>

          <Card className="shadow-lg">
            <CardContent className="p-8">
              <QuizForm />
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}
