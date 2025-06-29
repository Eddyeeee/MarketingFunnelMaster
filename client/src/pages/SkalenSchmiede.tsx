import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const SkalenSchmiede: React.FC = () => {
  const [showCalculator, setShowCalculator] = useState(false);
  const [revenue, setRevenue] = useState(5000);
  const [hours, setHours] = useState(40);

  const calculateHourlyRate = () => {
    return (revenue / hours).toFixed(0);
  };

  const calculateScaledRevenue = () => {
    const currentRate = revenue / hours;
    return (currentRate * 20).toFixed(0); // 20 Stunden bei gleichem Stundensatz
  };

  return (
    <div className="skalen-schmiede-page">
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo logo-skalen">
          <div className="logo-icon">S</div>
          Skalen-Schmiede
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link">Home</a></li>
          <li><a href="#calculator" className="nav-link">Skalierbarkeits-Score</a></li>
          <li><a href="#case-studies" className="nav-link">Case Studies</a></li>
          <li><a href="#contact" className="nav-link">Kontakt</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md">
                Du bist der Engpass in deinem Business
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: 'var(--skalen-primary)' }}>
                Entdecke die 3 Systeme, um der Zeit-gegen-Geld-Falle zu entkommen
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--skalen-primary)' }}>
                      {calculateHourlyRate()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                      Aktueller Stundensatz
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--skalen-accent)' }}>
                      {calculateScaledRevenue()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                      Skaliert (20h)
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button 
                  className="btn btn-skalen"
                  onClick={() => setShowCalculator(true)}
                >
                  Skalierbarkeits-Score berechnen
                </button>
                <button className="btn btn-outline">
                  Case Studies ansehen
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
              <h2 className="mb-lg">Die Zeit-gegen-Geld-Falle</h2>
              <div className="card mb-md" style={{ borderLeft: '4px solid var(--skalen-secondary)' }}>
                <h4 className="mb-sm">🚫 Keine Skalierung</h4>
                <p>Du musst für jeden Euro arbeiten. Urlaub = kein Einkommen</p>
              </div>
              <div className="card mb-md" style={{ borderLeft: '4px solid var(--skalen-secondary)' }}>
                <h4 className="mb-sm">⏰ Zeit-Engpass</h4>
                <p>Du lehnst lukrative Projekte ab, weil die Zeit fehlt</p>
              </div>
              <div className="card" style={{ borderLeft: '4px solid var(--skalen-secondary)' }}>
                <h4 className="mb-sm">😰 Burnout-Risiko</h4>
                <p>60+ Stunden pro Woche sind keine nachhaltige Lösung</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center">
                <h3 className="mb-md">Das sagen andere Freelancer:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic' }}>
                  "Ich war der Flaschenhals in meinem eigenen Business. 
                  Jetzt verdiene ich das 3-fache bei halber Arbeitszeit!"
                </blockquote>
                <p style={{ color: 'var(--skalen-primary)', fontWeight: '600' }}>
                  - Michael K., 35, ehemaliger Freelancer
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
              <h2 className="mb-md">Skalierbarkeits-Score Rechner</h2>
              <p>Finde heraus, wie skalierbar dein Business ist</p>
            </div>
            
            <div className="grid grid-2 gap-lg">
              <div>
                <label className="block mb-sm" style={{ fontWeight: '600' }}>
                  Monatlicher Umsatz (€)
                </label>
                <input
                  type="range"
                  min="1000"
                  max="50000"
                  step="1000"
                  value={revenue}
                  onChange={(e) => setRevenue(Number(e.target.value))}
                  style={{ width: '100%', marginBottom: 'var(--space-sm)' }}
                />
                <div className="text-center" style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--skalen-primary)' }}>
                  {revenue.toLocaleString()}€
                </div>
              </div>
              
              <div>
                <label className="block mb-sm" style={{ fontWeight: '600' }}>
                  Arbeitsstunden pro Monat
                </label>
                <input
                  type="range"
                  min="20"
                  max="80"
                  step="5"
                  value={hours}
                  onChange={(e) => setHours(Number(e.target.value))}
                  style={{ width: '100%', marginBottom: 'var(--space-sm)' }}
                />
                <div className="text-center" style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--skalen-accent)' }}>
                  {hours}h
                </div>
              </div>
            </div>

            <div className="text-center mt-xl">
              <div className="card" style={{ backgroundColor: 'var(--skalen-primary)', color: 'white' }}>
                <h3 className="mb-sm">Dein Skalierbarkeits-Score</h3>
                <div style={{ fontSize: '3rem', fontWeight: '700', marginBottom: 'var(--space-sm)' }}>
                  {Math.round((revenue / hours) * 10)}
                </div>
                <p className="mb-0">
                  {revenue / hours > 100 ? 'Hoch skalierbar' : revenue / hours > 50 ? 'Mittel skalierbar' : 'Niedrig skalierbar'}
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
            <h2 className="mb-md">Die 3 Systeme zur Skalierung</h2>
            <p style={{ fontSize: '1.25rem' }}>
              Bewährte Methoden, um dein Business zu skalieren
            </p>
          </div>
          <div className="grid grid-3">
            <div className="card text-center animate-fade-in-up">
              <div className="mb-md" style={{ fontSize: '3rem' }}>🤖</div>
              <h3 className="mb-sm">System 1: Automatisierung</h3>
              <p>Automatisiere repetitive Aufgaben und spare 20+ Stunden pro Woche</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--skalen-accent)', fontWeight: '600' }}>
                  ROI: 300% in 3 Monaten
                </span>
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>👥</div>
              <h3 className="mb-sm">System 2: Delegation</h3>
              <p>Baue ein Team auf und delegiere Aufgaben an Experten</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--skalen-accent)', fontWeight: '600' }}>
                  Skalierung: 5x Umsatz
                </span>
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📦</div>
              <h3 className="mb-sm">System 3: Produktisierung</h3>
              <p>Verwandle deine Dienstleistung in skalierbare Produkte</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--skalen-accent)', fontWeight: '600' }}>
                  Passive Einnahmen: 10.000€+
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Case Studies */}
      <section id="case-studies" className="section" style={{ backgroundColor: 'var(--flow-light)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md">Bewiesene Erfolge</h2>
            <p>Echte Freelancer, echte Ergebnisse</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up">
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--skalen-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  TK
                </div>
                <div>
                  <h4 className="mb-0">Thomas Klein</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                    Webdesigner → Agentur-CEO
                  </p>
                </div>
              </div>
              <div className="mb-md">
                <div className="grid grid-2 gap-sm">
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--skalen-secondary)' }}>Vorher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>5.000€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>40h/Woche</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--skalen-accent)' }}>Nachher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>25.000€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>20h/Woche</div>
                  </div>
                </div>
              </div>
              <p className="mb-0">
                "Durch Automatisierung und ein 5-köpfiges Team habe ich mein Business 
                in 8 Monaten verfünffacht!"
              </p>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--skalen-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  AS
                </div>
                <div>
                  <h4 className="mb-0">Anna Schmidt</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                    Copywriter → Online-Kurs-Expertin
                  </p>
                </div>
              </div>
              <div className="mb-md">
                <div className="grid grid-2 gap-sm">
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--skalen-secondary)' }}>Vorher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>3.500€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>50h/Woche</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--skalen-accent)' }}>Nachher</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>15.000€</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>15h/Woche</div>
                  </div>
                </div>
              </div>
              <p className="mb-0">
                "Mein Online-Kurs verkauft sich automatisch. Ich verdiene jetzt 
                passiv, während ich schlafe!"
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center">
            <h2 className="mb-md">Bereit, dein Business zu skalieren?</h2>
            <p className="mb-lg">
              Entdecke die bewährten Systeme, die andere Freelancer erfolgreich gemacht haben
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--skalen-primary)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--skalen-primary)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--skalen-primary)' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                Kostenlose Analyse + Skalierungsplan
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn btn-skalen">
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
              <h4 className="mb-md">Skalen-Schmiede</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Dein Weg vom Freelancer zum Unternehmer
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Systeme</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Automatisierung</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Delegation</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Produktisierung</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Case Studies</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Tools</a></li>
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
              © 2025 Skalen-Schmiede. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default SkalenSchmiede; 