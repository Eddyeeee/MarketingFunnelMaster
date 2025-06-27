import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Star, Crown, Download, Play, Mail, FileText, Link as LinkIcon, ChevronRight } from "lucide-react";
import { trackEvent } from "@/lib/analytics";
import { toast } from "@/hooks/use-toast";

export default function Bridge() {
  const { data: emailFunnels = [] } = useQuery({
    queryKey: ['/api/email-funnels']
  });

  const handleImportFunnel = (funnel: string) => {
    trackEvent('funnel_import', 'engagement', funnel);
    toast({
      title: "Funnel wird importiert",
      description: `${funnel === 'magic-profit' ? 'Magic Profit' : 'Money Magnet'} Funnel wird in dein System importiert...`,
    });
  };

  const handleStartQuizFunnel = (funnel: string) => {
    trackEvent('quiz_funnel_start', 'engagement', funnel);
    // Redirect to quiz with funnel parameter
    window.location.href = `/quiz?funnel=${funnel}`;
  };

  const handleOpenEmailFunnel = (id: number) => {
    trackEvent('email_funnel_open', 'engagement', `funnel_${id}`);
    toast({
      title: "E-Mail-Funnel wird geöffnet",
      description: "Der E-Mail-Funnel wird in einem neuen Tab geöffnet...",
    });
  };

  const handleOpenTSL = () => {
    trackEvent('tsl_open', 'engagement', 'bridge_page');
    window.location.href = '/tsl';
  };

  const handleOpenBridgePage = () => {
    trackEvent('bridge_page_open', 'engagement', 'self_reference');
    toast({
      title: "Du bist bereits hier",
      description: "Du befindest dich bereits auf der Bridge Page!",
    });
  };

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
                <span className="text-lg font-medium text-q-neutral-medium ml-2">Bridge</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Bridge Content */}
      <section className="py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-3xl md:text-4xl font-bold text-q-neutral-dark mb-4">
              Wähle deinen Weg zur finanziellen Freiheit
            </h1>
            <p className="text-xl text-q-neutral-medium">
              Verschiedene Wege, ein Ziel: Deine finanzielle Unabhängigkeit
            </p>
          </div>

          {/* Funnel Options */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Magic Profit Funnel */}
            <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200 shadow-lg">
              <CardContent className="p-8">
                <div className="text-center mb-6">
                  <div className="bg-q-primary text-white rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                    <Star size={24} />
                  </div>
                  <h3 className="text-2xl font-bold text-q-neutral-dark mb-2">Magic Profit</h3>
                  <p className="text-q-neutral-medium">Perfekt für Einsteiger</p>
                  <Badge className="bg-q-accent text-white mt-2">
                    BESTSELLER
                  </Badge>
                </div>
                
                <div className="space-y-4 mb-8">
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Schritt-für-Schritt Anleitung</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">0€ Startkapital erforderlich</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Erste Ergebnisse in 30 Tagen</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Bonus: E-Mail-Funnel-Templates</span>
                  </div>
                </div>

                <div className="space-y-4">
                  <Button 
                    onClick={() => handleImportFunnel('magic-profit')}
                    className="w-full bg-q-primary hover:bg-q-primary-dark text-white"
                  >
                    <Download className="mr-2" size={20} />
                    Magic Profit importieren
                  </Button>
                  <Button 
                    onClick={() => handleStartQuizFunnel('magic-profit')}
                    variant="outline"
                    className="w-full border-q-primary text-q-primary hover:bg-q-primary hover:text-white"
                  >
                    <Play className="mr-2" size={20} />
                    Quiz-Funnel starten
                  </Button>
                  <Link href="/vsl/magic-profit">
                    <Button variant="ghost" className="w-full text-q-primary">
                      VSL ansehen
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>

            {/* Money Magnet Funnel */}
            <Card className="bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200 shadow-lg">
              <CardContent className="p-8">
                <div className="text-center mb-6">
                  <div className="bg-q-secondary text-white rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                    <Crown size={24} />
                  </div>
                  <h3 className="text-2xl font-bold text-q-neutral-dark mb-2">Money Magnet</h3>
                  <p className="text-q-neutral-medium">Für Fortgeschrittene</p>
                  <Badge className="bg-q-secondary text-white mt-2">
                    PREMIUM
                  </Badge>
                </div>
                
                <div className="space-y-4 mb-8">
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Skalierung auf 5.000€+</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Automatisierte Systeme</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Multiple Einkommensquellen</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-q-secondary rounded-full mr-3"></div>
                    <span className="text-q-neutral-dark">Bonus: KI-Automatisierung</span>
                  </div>
                </div>

                <div className="space-y-4">
                  <Button 
                    onClick={() => handleImportFunnel('money-magnet')}
                    className="w-full bg-q-secondary hover:bg-q-secondary-dark text-white"
                  >
                    <Download className="mr-2" size={20} />
                    Money Magnet importieren
                  </Button>
                  <Button 
                    onClick={() => handleStartQuizFunnel('money-magnet')}
                    variant="outline"
                    className="w-full border-q-secondary text-q-secondary hover:bg-q-secondary hover:text-white"
                  >
                    <Play className="mr-2" size={20} />
                    Quiz-Funnel starten
                  </Button>
                  <Link href="/vsl/money-magnet">
                    <Button variant="ghost" className="w-full text-q-secondary">
                      VSL ansehen
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Additional Resources */}
          <Card className="shadow-lg">
            <CardContent className="p-8">
              <h3 className="text-xl font-bold text-q-neutral-dark text-center mb-6">
                Zusätzliche Ressourcen
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                {emailFunnels.slice(0, 2).map((funnel: any, index: number) => (
                  <Button
                    key={funnel.id}
                    onClick={() => handleOpenEmailFunnel(funnel.id)}
                    variant="outline"
                    className="flex items-center justify-between p-4 h-auto hover:shadow-md transition-all"
                  >
                    <div className="flex items-center">
                      <Mail className="text-q-primary mr-3" size={20} />
                      <span className="font-semibold text-q-neutral-dark">{funnel.name}</span>
                    </div>
                    <ChevronRight className="text-q-neutral-medium" size={20} />
                  </Button>
                ))}
                
                <Button
                  onClick={handleOpenTSL}
                  variant="outline"
                  className="flex items-center justify-between p-4 h-auto hover:shadow-md transition-all"
                >
                  <div className="flex items-center">
                    <FileText className="text-q-primary mr-3" size={20} />
                    <span className="font-semibold text-q-neutral-dark">Text Sales Letter</span>
                  </div>
                  <ChevronRight className="text-q-neutral-medium" size={20} />
                </Button>
                
                <Button
                  onClick={handleOpenBridgePage}
                  variant="outline"
                  className="flex items-center justify-between p-4 h-auto hover:shadow-md transition-all"
                >
                  <div className="flex items-center">
                    <LinkIcon className="text-q-primary mr-3" size={20} />
                    <span className="font-semibold text-q-neutral-dark">Bridge Page</span>
                  </div>
                  <ChevronRight className="text-q-neutral-medium" size={20} />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}
