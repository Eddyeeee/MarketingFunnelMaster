import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const KapitalKlar: React.FC = () => {
  const [age, setAge] = useState(55);
  const [savings, setSavings] = useState(100000);
  const [monthlyIncome, setMonthlyIncome] = useState(3000);

  const calculateRetirementGap = () => {
    const targetAge = 67;
    const yearsToRetirement = targetAge - age;
    const targetMonthlyIncome = 4000; // Ziel-Rente
    const monthlyGap = targetMonthlyIncome - (savings * 0.04 / 12); // 4% Regel
    return Math.max(0, monthlyGap);
  };

  const calculateYearsToTarget = () => {
    const gap = calculateRetirementGap();
    if (gap <= 0) return 0;
    const additionalSavings = gap * 12;
    const years = additionalSavings / (monthlyIncome * 0.2); // 20% sparen
    return Math.ceil(years);
  };

  return (
    <div className="kapital-klar-page">
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo logo-kapital">
          <div className="logo-icon">K</div>
          Kapital-Klar
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link">Home</a></li>
          <li><a href="#calculator" className="nav-link">Rentenlücken-Rechner</a></li>
          <li><a href="#strategies" className="nav-link">Strategien</a></li>
          <li><a href="#contact" className="nav-link">Kontakt</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md">
                Sichere deine finanzielle Zukunft
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: 'var(--kapital-primary)' }}>
                Entdecke bewährte Strategien für ein sorgenfreies Leben im Ruhestand
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--kapital-primary)' }}>
                      {calculateRetirementGap().toFixed(0)}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                      Monatliche Rentenlücke
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--kapital-accent)' }}>
                      {calculateYearsToTarget()}
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                      Jahre bis zum Ziel
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn btn-kapital">
                  Rentenlücken-Rechner starten
                </button>
                <button className="btn btn-outline">
                  Strategien ansehen
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section">
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg">Die Realität der Altersvorsorge</h2>
              <div className="card mb-md" style={{ borderLeft: '4px solid var(--kapital-secondary)' }}>
                <h4 className="mb-sm">📉 Niedrige Renten</h4>
                <p>Die gesetzliche Rente reicht oft nicht aus für den gewohnten Lebensstandard</p>
              </div>
              <div className="card mb-md" style={{ borderLeft: '4px solid var(--kapital-secondary)' }}>
                <h4 className="mb-sm">⏰ Zeitdruck</h4>
                <p>Je später du startest, desto mehr musst du monatlich sparen</p>
              </div>
              <div className="card" style={{ borderLeft: '4px solid var(--kapital-secondary)' }}>
                <h4 className="mb-sm">😰 Unsicherheit</h4>
                <p>Du weißt nicht, ob deine Ersparnisse für den Ruhestand reichen</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center">
                <h3 className="mb-md">Das sagen andere Best Ager:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic' }}>
                  "Ich hatte Angst vor der Rente. Jetzt habe ich einen klaren Plan 
                  und schlafe wieder ruhig!"
                </blockquote>
                <p style={{ color: 'var(--kapital-primary)', fontWeight: '600' }}>
                  - Hans M., 58, Angestellter
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Calculator Section */}
      <section id="calculator" className="section" style={{ backgroundColor: 'var(--flow-light)' }}>
        <div className="container-sm">
          <div className="card">
            <div className="text-center mb-xl">
              <h2 className="mb-md">Rentenlücken-Rechner</h2>
              <p>Finde heraus, wie groß deine Rentenlücke ist</p>
            </div>
            
            <div className="grid grid-3 gap-lg">
              <div>
                <label className="block mb-sm" style={{ fontWeight: '600' }}>
                  Alter
                </label>
                <input
                  type="range"
                  min="40"
                  max="65"
                  step="1"
                  value={age}
                  onChange={(e) => setAge(Number(e.target.value))}
                  style={{ width: '100%', marginBottom: 'var(--space-sm)' }}
                />
                <div className="text-center" style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-primary)' }}>
                  {age} Jahre
                </div>
              </div>
              
              <div>
                <label className="block mb-sm" style={{ fontWeight: '600' }}>
                  Ersparnisse (€)
                </label>
                <input
                  type="range"
                  min="0"
                  max="500000"
                  step="10000"
                  value={savings}
                  onChange={(e) => setSavings(Number(e.target.value))}
                  style={{ width: '100%', marginBottom: 'var(--space-sm)' }}
                />
                <div className="text-center" style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-accent)' }}>
                  {savings.toLocaleString()}€
                </div>
              </div>

              <div>
                <label className="block mb-sm" style={{ fontWeight: '600' }}>
                  Monatliches Einkommen (€)
                </label>
                <input
                  type="range"
                  min="1000"
                  max="10000"
                  step="500"
                  value={monthlyIncome}
                  onChange={(e) => setMonthlyIncome(Number(e.target.value))}
                  style={{ width: '100%', marginBottom: 'var(--space-sm)' }}
                />
                <div className="text-center" style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-secondary)' }}>
                  {monthlyIncome.toLocaleString()}€
                </div>
              </div>
            </div>

            <div className="text-center mt-xl">
              <div className="card" style={{ backgroundColor: 'var(--kapital-primary)', color: 'white' }}>
                <h3 className="mb-sm">Deine Rentenlücke</h3>
                <div style={{ fontSize: '3rem', fontWeight: '700', marginBottom: 'var(--space-sm)' }}>
                  {calculateRetirementGap().toFixed(0)}€
                </div>
                <p className="mb-0">
                  Monatlich fehlende Rente
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md">Die 3 Säulen der Altersvorsorge</h2>
            <p style={{ fontSize: '1.25rem' }}>
              Bewährte Strategien für ein sorgenfreies Leben
            </p>
          </div>
          <div className="grid grid-3">
            <div className="card text-center animate-fade-in-up">
              <div className="mb-md" style={{ fontSize: '3rem' }}>🏦</div>
              <h3 className="mb-sm">Säule 1: Kapitalaufbau</h3>
              <p>Systematisch Vermögen aufbauen mit bewährten Anlagestrategien</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--kapital-accent)', fontWeight: '600' }}>
                  Rendite: 6-8% p.a.
                </span>
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🛡️</div>
              <h3 className="mb-sm">Säule 2: Risikomanagement</h3>
              <p>Diversifikation und Absicherung gegen Marktrisiken</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--kapital-accent)', fontWeight: '600' }}>
                  Sicherheit: 95%+
                </span>
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📈</div>
              <h3 className="mb-sm">Säule 3: Passive Einnahmen</h3>
              <p>Zusätzliche Einkommensquellen für mehr finanzielle Freiheit</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--kapital-accent)', fontWeight: '600' }}>
                  Zusatzeinkommen: 1.000€+
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Strategies Section */}
      <section id="strategies" className="section" style={{ backgroundColor: 'var(--flow-light)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md">Bewährte Strategien</h2>
            <p>Erprobte Methoden für deine finanzielle Zukunft</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up">
              <h3 className="mb-md">ETF-Sparplan</h3>
              <p className="mb-md">
                Monatlich in breit gestreute ETFs investieren. Einfach, kostengünstig 
                und langfristig profitabel.
              </p>
              <div className="mb-md">
                <div className="flex justify-between mb-sm">
                  <span>Risiko:</span>
                  <span style={{ color: 'var(--kapital-accent)' }}>Niedrig-Mittel</span>
                </div>
                <div className="flex justify-between mb-sm">
                  <span>Rendite:</span>
                  <span style={{ color: 'var(--kapital-accent)' }}>6-8% p.a.</span>
                </div>
                <div className="flex justify-between">
                  <span>Zeitaufwand:</span>
                  <span style={{ color: 'var(--kapital-accent)' }}>1h/Monat</span>
                </div>
              </div>
              <button className="btn btn-kapital">
                Mehr erfahren
              </button>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <h3 className="mb-md">Dividenden-Strategie</h3>
              <p className="mb-md">
                In dividendenstarke Aktien investieren für regelmäßige Einnahmen. 
                Perfekt für den Ruhestand.
              </p>
              <div className="mb-md">
                <div className="flex justify-between mb-sm">
                  <span>Risiko:</span>
                  <span style={{ color: 'var(--kapital-accent)' }}>Mittel</span>
                </div>
                <div className="flex justify-between mb-sm">
                  <span>Dividendenrendite:</span>
                  <span style={{ color: 'var(--kapital-accent)' }}>3-5% p.a.</span>
                </div>
                <div className="flex justify-between">
                  <span>Zeitaufwand:</span>
                  <span style={{ color: 'var(--kapital-accent)' }}>2h/Monat</span>
                </div>
              </div>
              <button className="btn btn-kapital">
                Mehr erfahren
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md">Erfolgsgeschichten</h2>
            <p>Echte Menschen, echte Ergebnisse</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up">
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--kapital-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  WM
                </div>
                <div>
                  <h4 className="mb-0">Wolfgang Müller</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                    58 Jahre, Angestellter
                  </p>
                </div>
              </div>
              <div className="mb-md">
                <div className="grid grid-2 gap-sm">
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-secondary)' }}>Vorher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>50.000€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>Ersparnisse</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-accent)' }}>Nachher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>180.000€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>Vermögen</div>
                  </div>
                </div>
              </div>
              <p className="mb-0">
                "In 5 Jahren habe ich mein Vermögen verdreifacht. 
                Jetzt kann ich beruhigt in die Rente gehen!"
              </p>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--kapital-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  IB
                </div>
                <div>
                  <h4 className="mb-0">Ingrid Bauer</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                    62 Jahre, Lehrerin
                  </p>
                </div>
              </div>
              <div className="mb-md">
                <div className="grid grid-2 gap-sm">
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-secondary)' }}>Vorher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>1.200€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>Monatliche Rente</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--kapital-accent)' }}>Nachher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>2.800€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>Gesamteinkommen</div>
                  </div>
                </div>
              </div>
              <p className="mb-0">
                "Durch Dividenden-Strategie habe ich 1.600€ zusätzlich im Monat. 
                Das macht den Unterschied!"
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center">
            <h2 className="mb-md">Bereit für deine finanzielle Zukunft?</h2>
            <p className="mb-lg">
              Starte noch heute und sichere dir ein sorgenfreies Leben im Ruhestand
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--kapital-primary)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--kapital-primary)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--kapital-primary)' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                Kostenlose Analyse + Persönlicher Plan
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn btn-kapital">
                Jetzt kostenlos analysieren
              </button>
              <button className="btn btn-outline">
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'var(--flow-neutral)', color: 'white' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Kapital-Klar</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Dein Weg zur finanziellen Sicherheit
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Strategien</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>ETF-Sparplan</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Dividenden-Strategie</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Risikomanagement</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Rechner</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Beratung</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Rechtliches</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Impressum</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Datenschutz</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>AGB</a></li>
              </ul>
            </div>
          </div>
          <div className="text-center mt-lg" style={{ borderTop: '1px solid #374151', paddingTop: 'var(--space-lg)' }}>
            <p style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
              © 2025 Kapital-Klar. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default KapitalKlar; 