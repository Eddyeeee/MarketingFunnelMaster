import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import LeadCaptureForm from "@/components/LeadCaptureForm";
import CountdownTimer from "@/components/CountdownTimer";
import { ArrowLeft, CheckCircle, Star, Trophy, Clock, Shield, Zap } from "lucide-react";
import { trackEvent } from "@/lib/analytics";

export default function TSL() {
  const handleLeadCapture = (leadData: any) => {
    trackEvent('tsl_lead_capture', 'conversion', 'tsl_page');
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
                <span className="text-lg font-medium text-q-neutral-medium ml-2">Text Sales Letter</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* TSL Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Headline */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-q-neutral-dark mb-4 leading-tight">
            Warum 90% der Menschen niemals finanziell frei werden
            <span className="text-q-primary"> (und wie du zu den 10% gehörst)</span>
          </h1>
          <p className="text-xl text-q-neutral-medium mb-6">
            Die schockierende Wahrheit über finanzielle Freiheit, die dir niemand verraten will
          </p>
          
          {/* Urgency Timer */}
          <Card className="bg-q-accent text-white inline-block mb-8">
            <CardContent className="p-4">
              <div className="text-sm font-semibold mb-2">
                <Clock className="inline mr-2" size={16} />
                Limitiertes Angebot läuft ab in:
              </div>
              <CountdownTimer />
            </CardContent>
          </Card>
        </div>

        {/* Lead Magnet */}
        <Card className="shadow-lg mb-12 bg-gradient-to-r from-q-primary to-q-primary-dark text-white">
          <CardContent className="p-8 text-center">
            <Trophy className="mx-auto mb-4" size={48} />
            <h2 className="text-2xl font-bold mb-4">
              Sichere dir JETZT den kostenlosen "Finanzielle Freiheit Blueprint"
            </h2>
            <p className="text-lg mb-6 text-blue-100">
              Der 47-seitige Leitfaden, der bereits über 10.000 Menschen zu 2.000-5.000€ passivem Einkommen verholfen hat
            </p>
            <div className="max-w-md mx-auto">
              <LeadCaptureForm 
                funnel="tsl"
                source="tsl"
                onSubmit={handleLeadCapture}
                buttonText="Blueprint kostenlos sichern"
              />
            </div>
          </CardContent>
        </Card>

        {/* Main Content */}
        <div className="prose prose-lg max-w-none">
          <Card className="shadow-lg mb-8">
            <CardContent className="p-8">
              <h2 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Liebe/r Freund/in der finanziellen Freiheit,
              </h2>
              
              <p className="text-lg mb-6">
                wenn du bis hierher gelesen hast, dann gehörst du zu den wenigen Menschen, die <strong>wirklich bereit</strong> sind, 
                etwas an ihrer finanziellen Situation zu ändern.
              </p>

              <p className="text-lg mb-6">
                Die meisten Menschen träumen ihr Leben lang von finanzieller Freiheit, aber nur 10% schaffen es tatsächlich. 
                Warum? Weil sie die <span className="text-q-primary font-semibold">3 kritischen Fehler</span> machen, 
                die ich dir gleich verrate.
              </p>

              <div className="bg-red-50 border-l-4 border-red-500 p-6 my-8">
                <h3 className="text-xl font-bold text-red-800 mb-4">⚠️ WARNUNG: Das ist nicht für jeden!</h3>
                <p className="text-red-700">
                  Falls du zu den Menschen gehörst, die bei der ersten Schwierigkeit aufgeben oder nicht bereit sind, 
                  15-30 Minuten täglich zu investieren, dann schließe diese Seite JETZT. Dieses System funktioniert nur 
                  für Menschen, die <strong>wirklich</strong> etwas ändern wollen.
                </p>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Der Grund, warum 90% der Menschen arm bleiben (und es nicht einmal merken)
              </h3>

              <p className="text-lg mb-6">
                Lass mich dir eine Geschichte erzählen, die dein Leben verändern wird...
              </p>

              <p className="text-lg mb-6">
                Vor 3 Jahren war ich genau wie du. Gefangen im Hamsterrad. Jeden Monat das gleiche Spiel: 
                Gehalt rein, Rechnungen raus, und am Ende des Monats war wieder nichts übrig.
              </p>

              <p className="text-lg mb-6">
                Ich dachte, ich müsste härter arbeiten. Länger arbeiten. Einen besseren Job finden. 
                <span className="text-q-primary font-semibold"> Ich lag völlig falsch.</span>
              </p>

              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-6 my-8">
                <h4 className="text-lg font-bold text-yellow-800 mb-3">Die brutale Wahrheit:</h4>
                <p className="text-yellow-700">
                  Reiche Menschen arbeiten NICHT härter als du. Sie arbeiten NICHT länger als du. 
                  Sie haben nur EIN SYSTEM, das für sie arbeitet, während sie schlafen.
                </p>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Die 3 kritischen Fehler, die 90% der Menschen arm halten
              </h3>

              <div className="space-y-6 mb-8">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-xl font-bold text-q-primary mb-3">
                    <span className="bg-q-primary text-white px-3 py-1 rounded-full mr-3">1</span>
                    Sie verkaufen Zeit gegen Geld
                  </h4>
                  <p className="text-lg">
                    Der größte Fehler überhaupt. Solange du deine Zeit verkaufst, wirst du niemals reich. 
                    Reiche Menschen haben verstanden: Du musst ein System aufbauen, das auch ohne dich läuft.
                  </p>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-xl font-bold text-q-primary mb-3">
                    <span className="bg-q-primary text-white px-3 py-1 rounded-full mr-3">2</span>
                    Sie warten auf den "perfekten Moment"
                  </h4>
                  <p className="text-lg">
                    "Wenn ich mehr Geld habe...", "Wenn ich mehr Zeit habe...", "Wenn die Kinder größer sind...". 
                    Der perfekte Moment kommt nie. Erfolgreiche Menschen starten mit dem, was sie haben.
                  </p>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-xl font-bold text-q-primary mb-3">
                    <span className="bg-q-primary text-white px-3 py-1 rounded-full mr-3">3</span>
                    Sie denken, sie brauchen viel Startkapital
                  </h4>
                  <p className="text-lg">
                    Das ist der größte Mythos. Die erfolgreichsten Menschen haben oft mit NICHTS angefangen. 
                    Was du brauchst, ist das richtige System - nicht das große Geld.
                  </p>
                </div>
              </div>

              <div className="bg-green-50 border-l-4 border-green-500 p-6 my-8">
                <h4 className="text-lg font-bold text-green-800 mb-3">Hier ist die gute Nachricht:</h4>
                <p className="text-green-700">
                  Diese 3 Fehler kannst du ab HEUTE vermeiden. Und ich zeige dir genau wie. 
                  Mit dem gleichen System, das bereits über 10.000 Menschen zu 2.000-5.000€ passivem Einkommen verholfen hat.
                </p>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Wie ich von 0€ auf 4.200€ passives Einkommen kam (und warum es auch bei dir funktioniert)
              </h3>

              <p className="text-lg mb-6">
                Es war ein Dienstagabend im Oktober 2021. Ich saß in meiner kleinen Küche, starrte auf mein Bankkonto 
                und wusste nicht, wie ich die Miete bezahlen sollte.
              </p>

              <p className="text-lg mb-6">
                Damals arbeitete ich 50 Stunden die Woche in einem Job, den ich hasste. Jeden Morgen das gleiche: 
                Wecker um 6:30 Uhr, schnell einen Kaffee, dann ins Büro hetzen.
              </p>

              <p className="text-lg mb-6">
                <span className="text-q-primary font-semibold">Heute, knapp 3 Jahre später, verdiene ich 4.200€ im Monat. Vollautomatisch.</span> 
                Ich stehe auf, wann ich will. Arbeite von wo ich will. Und das Beste: Das System läuft auch, wenn ich schlafe.
              </p>

              <div className="bg-blue-50 border-l-4 border-blue-500 p-6 my-8">
                <h4 className="text-lg font-bold text-blue-800 mb-3">Das Geheimnis:</h4>
                <p className="text-blue-700">
                  Ich habe aufgehört, meine Zeit zu verkaufen. Stattdessen habe ich ein System aufgebaut, 
                  das 24/7 für mich arbeitet. Dieses System nennt sich "Magic Profit System".
                </p>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Was macht das Magic Profit System so besonders?
              </h3>

              <p className="text-lg mb-6">
                Das Magic Profit System basiert auf 3 simplen Säulen, die jeder umsetzen kann - 
                auch ohne Vorkenntnisse und ohne Startkapital:
              </p>

              <div className="space-y-6 mb-8">
                <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-500">
                  <h4 className="text-xl font-bold text-green-800 mb-3">
                    <span className="bg-green-500 text-white px-3 py-1 rounded-full mr-3">1</span>
                    Automatisierung statt Zeitverkauf
                  </h4>
                  <p className="text-lg text-green-700">
                    Du baust einmal ein System auf, das dann 24/7 für dich arbeitet. Keine Tauschgeschäfte mehr: 
                    Zeit gegen Geld. Das System verdient auch, wenn du schläfst.
                  </p>
                </div>

                <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-500">
                  <h4 className="text-xl font-bold text-blue-800 mb-3">
                    <span className="bg-blue-500 text-white px-3 py-1 rounded-full mr-3">2</span>
                    Skalierbarkeit ohne Grenzen
                  </h4>
                  <p className="text-lg text-blue-700">
                    Während traditionelle Jobs ein Gehaltslimit haben, ist beim Magic Profit System der Himmel die Grenze. 
                    Von 500€ zu 2.000€ zu 5.000€+ - alles ist möglich.
                  </p>
                </div>

                <div className="bg-purple-50 p-6 rounded-lg border-l-4 border-purple-500">
                  <h4 className="text-xl font-bold text-purple-800 mb-3">
                    <span className="bg-purple-500 text-white px-3 py-1 rounded-full mr-3">3</span>
                    Einfache Umsetzung für jeden
                  </h4>
                  <p className="text-lg text-purple-700">
                    Kein Informatikstudium nötig. Keine komplizierten Technologien. Das System ist so simpel, 
                    dass es auch deine Oma verstehen würde.
                  </p>
                </div>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-6 my-8">
                <h4 className="text-lg font-bold text-yellow-800 mb-3">Echte Ergebnisse von echten Menschen:</h4>
                <div className="space-y-4">
                  <p className="text-yellow-700">
                    <strong>Maria S., Alleinerziehende Mutter:</strong> "Nach 90 Tagen hatte ich konstant 1.800€ im Monat. 
                    Heute sind es über 3.200€ - komplett automatisch!"
                  </p>
                  <p className="text-yellow-700">
                    <strong>Thomas K., Angestellter:</strong> "Das System läuft jetzt seit 6 Monaten und bringt mir 4.200€ 
                    passives Einkommen. Mein Chef ahnt nicht, dass ich bald kündige."
                  </p>
                </div>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Die 3 fatalen Fehler, die 90% der Menschen arm halten:
              </h3>

              <div className="space-y-6 mb-8">
                <div className="flex items-start space-x-4">
                  <div className="bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">1</div>
                  <div>
                    <h4 className="text-xl font-bold text-q-neutral-dark mb-2">Sie warten auf den "perfekten" Moment</h4>
                    <p className="text-q-neutral-medium">
                      "Ich fange an, wenn ich mehr Geld habe", "Ich warte bis nächstes Jahr", "Ich muss erst mehr lernen" - 
                      kennst du diese Ausreden? Der perfekte Moment kommt nie. Erfolgreiche Menschen starten mit dem, was sie haben.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">2</div>
                  <div>
                    <h4 className="text-xl font-bold text-q-neutral-dark mb-2">Sie versuchen alles gleichzeitig</h4>
                    <p className="text-q-neutral-medium">
                      Aktien, Krypto, Immobilien, Online-Business - sie verzetteln sich und werden in nichts richtig gut. 
                      Erfolgreiche Menschen fokussieren sich auf EIN System und meistern es perfekt.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">3</div>
                  <div>
                    <h4 className="text-xl font-bold text-q-neutral-dark mb-2">Sie geben zu früh auf</h4>
                    <p className="text-q-neutral-medium">
                      Nach 2-3 Wochen ohne Ergebnisse werfen sie das Handtuch. Dabei braucht jedes System Zeit zum Wachsen. 
                      Die erfolgreichsten Menschen sind nicht die klügsten - sondern die hartnäckigsten.
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-green-50 border-l-4 border-green-500 p-6 my-8">
                <h3 className="text-xl font-bold text-green-800 mb-4">✅ Die gute Nachricht:</h3>
                <p className="text-green-700">
                  Wenn du diese 3 Fehler vermeidest, stehen deine Chancen auf finanzielle Freiheit bei über 80%. 
                  Und genau dabei hilft dir das Q-Money & Cash Maximus System.
                </p>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Wie Maria S. in 90 Tagen von 0€ auf 1.800€ passives Einkommen kam:
              </h3>

              <p className="text-lg mb-6">
                Maria ist Vollzeit-Mama von zwei Kindern. Ihr Mann arbeitet Vollzeit, aber das Geld reicht trotzdem nie. 
                Besonders frustrierend: Sie wollte schon immer zum Familieneinkommen beitragen, aber hatte weder Zeit noch 
                Erfahrung mit Geldanlagen.
              </p>

              <p className="text-lg mb-6">
                Dann stieß sie auf unser System. Was sie besonders überzeugte: Sie brauchte kein Startkapital und 
                konnte flexibel arbeiten, wenn die Kinder schliefen.
              </p>

              <div className="bg-blue-50 p-6 rounded-lg mb-6">
                <p className="text-lg italic text-blue-800">
                  "Am Anfang war ich skeptisch. Aber bereits nach 30 Tagen hatte ich meine ersten 180€ verdient. 
                  Nach 90 Tagen waren es konstant 1.800€ im Monat. Heute, 6 Monate später, sind es über 3.200€. 
                  Das Beste: Es läuft komplett automatisch!"
                </p>
                <p className="text-right text-blue-600 font-semibold mt-4">- Maria S., Vollzeit-Mama</p>
              </div>

              <h3 className="text-2xl font-bold text-q-neutral-dark mb-6">
                Das Q-Money & Cash Maximus System im Überblick:
              </h3>

              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>Schritt-für-Schritt Anleitung</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>0€ Startkapital erforderlich</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>Erste Ergebnisse in 30 Tagen</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>Funktioniert neben Vollzeitjob</span>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>Automatisierte Systeme</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>Multiple Einkommensquellen</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>Skalierbar auf 5.000€+</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="text-q-secondary" size={20} />
                    <span>30 Tage Geld-zurück-Garantie</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* CTA Section */}
          <Card className="shadow-lg bg-gradient-to-r from-q-accent to-q-accent-dark text-white">
            <CardContent className="p-8 text-center">
              <h2 className="text-3xl font-bold mb-4">
                Deine Entscheidung bestimmt deine Zukunft
              </h2>
              <p className="text-xl mb-6">
                Du hast jetzt zwei Möglichkeiten:
              </p>
              
              <div className="grid md:grid-cols-2 gap-6 mb-8 text-left">
                <div className="bg-red-500 bg-opacity-20 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Option 1: Nichts tun</h3>
                  <ul className="space-y-2">
                    <li>• In 1 Jahr bist du finanziell genauso da wie heute</li>
                    <li>• Du ärgerst dich, dass du nicht gehandelt hast</li>
                    <li>• Andere um dich herum werden erfolgreich</li>
                    <li>• Du bleibst in der finanziellen Unsicherheit</li>
                  </ul>
                </div>
                
                <div className="bg-green-500 bg-opacity-20 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Option 2: JETZT starten</h3>
                  <ul className="space-y-2">
                    <li>• In 90 Tagen dein erstes passives Einkommen</li>
                    <li>• In 1 Jahr finanzielle Sicherheit</li>
                    <li>• Du bist stolz auf deinen Mut und Erfolg</li>
                    <li>• Du inspirierst andere mit deiner Geschichte</li>
                  </ul>
                </div>
              </div>

              <div className="max-w-md mx-auto mb-6">
                <LeadCaptureForm 
                  funnel="tsl"
                  source="tsl_bottom"
                  onSubmit={handleLeadCapture}
                  buttonText="JA, ich will finanzielle Freiheit!"
                />
              </div>

              <div className="flex justify-center items-center space-x-6 text-sm">
                <div className="flex items-center space-x-2">
                  <Shield size={16} />
                  <span>30 Tage Garantie</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Zap size={16} />
                  <span>Sofortiger Zugang</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Star size={16} />
                  <span>10.000+ Erfolge</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Final Testimonials */}
          <Card className="shadow-lg mt-8">
            <CardContent className="p-8">
              <h3 className="text-2xl font-bold text-q-neutral-dark text-center mb-8">
                Das sagen unsere erfolgreichsten Kunden:
              </h3>
              
              <div className="space-y-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <p className="text-lg italic mb-4">
                    "Ich war am Anfang skeptisch. Aber die Ergebnisse sprechen für sich: 
                    Von 0€ auf 4.200€ passives Einkommen in nur 6 Monaten. Das System funktioniert wirklich!"
                  </p>
                  <p className="font-semibold text-q-primary">- Thomas K., Angestellter</p>
                </div>
                
                <div className="bg-gray-50 p-6 rounded-lg">
                  <p className="text-lg italic mb-4">
                    "Als Studentin dachte ich, finanzielle Freiheit wäre nur was für Reiche. 
                    Mit diesem System verdiene ich jetzt mehr als meine Eltern - und das neben dem Studium!"
                  </p>
                  <p className="font-semibold text-q-primary">- Julia M., Studentin</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
