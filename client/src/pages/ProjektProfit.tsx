import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const ProjektProfit: React.FC = () => {
  const [selectedGoal, setSelectedGoal] = useState('scale');
  const [monthlyRevenue, setMonthlyRevenue] = useState(8000);

  const goals = [
    { id: 'scale', name: 'Skalierung', description: 'Mehr Projekte und höhere Preise', emoji: '📈' },
    { id: 'automation', name: 'Automatisierung', description: 'Weniger Arbeit, mehr Einkommen', emoji: '⚡' },
    { id: 'clients', name: 'Premium-Kunden', description: 'Bessere Kunden mit höheren Budgets', emoji: '👑' },
    { id: 'systems', name: 'Systeme', description: 'Wiederholbare Prozesse aufbauen', emoji: '🔧' }
  ];

  const currentGoal = goals.find(goal => goal.id === selectedGoal);

  return (
    <div className="projekt-profit-page" style={{ backgroundColor: '#f8fafc', color: '#1e293b' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo" style={{ color: '#3b82f6' }}>
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)' }}>P</div>
          Projekt-Profit
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link" style={{ color: '#1e293b' }}>Home</a></li>
          <li><a href="#goals" className="nav-link" style={{ color: '#1e293b' }}>Ziele</a></li>
          <li><a href="#strategies" className="nav-link" style={{ color: '#1e293b' }}>Strategien</a></li>
          <li><a href="#success" className="nav-link" style={{ color: '#1e293b' }}>Erfolge</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero" style={{ backgroundColor: '#f8fafc', backgroundImage: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: '#1e293b' }}>
                Skaliere dein Freelance-Business systematisch
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: '#3b82f6' }}>
                Von Einzelkämpfer zu profitablen Systemen - so baust du ein skalierbares Business
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#3b82f6' }}>
                      {monthlyRevenue.toLocaleString()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#1e293b' }}>
                      Monatlich möglich
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(29, 78, 216, 0.1)', border: '1px solid #1d4ed8' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#1d4ed8' }}>
                      20-30h/Woche
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#1e293b' }}>
                      Flexibel einteilbar
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn" style={{ background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)', color: 'white' }}>
                  Business-Analyse starten
                </button>
                <button className="btn btn-outline" style={{ color: '#3b82f6', borderColor: '#3b82f6' }}>
                  Case Studies ansehen
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section" style={{ backgroundColor: 'rgba(59, 130, 246, 0.05)' }}>
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg" style={{ color: '#1e293b' }}>Die typischen Freelancer-Probleme</h2>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                <h4 className="mb-sm">⏰ Zeit gegen Geld</h4>
                <p style={{ color: '#1e293b' }}>Du musst für jeden Euro arbeiten - das ist nicht skalierbar</p>
              </div>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                <h4 className="mb-sm">😰 Feast or Famine</h4>
                <p style={{ color: '#1e293b' }}>Entweder zu viel oder zu wenig Arbeit - nie konstant</p>
              </div>
              <div className="card" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                <h4 className="mb-sm">📉 Keine Systeme</h4>
                <p style={{ color: '#1e293b' }}>Jedes Projekt ist ein Einzelstück - keine Wiederholbarkeit</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center" style={{ backgroundColor: 'rgba(29, 78, 216, 0.1)', border: '1px solid #1d4ed8' }}>
                <h3 className="mb-md" style={{ color: '#1e293b' }}>Das sagen erfolgreiche Freelancer:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic', color: '#3b82f6' }}>
                  "Mit systematischer Skalierung verdiene ich jetzt 15.000€ im Monat. 
                  Und das bei weniger Arbeitszeit!"
                </blockquote>
                <p style={{ color: '#1d4ed8', fontWeight: '600' }}>
                  - Thomas M., 35, Web-Entwickler
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Goals Section */}
      <section id="goals" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Was ist dein wichtigstes Ziel?</h2>
            <p style={{ fontSize: '1.25rem', color: '#3b82f6' }}>
              Wähle dein Hauptziel und finde die passende Strategie
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg mb-xl">
            <div>
              <label className="block mb-sm" style={{ fontWeight: '600', color: '#1e293b' }}>
                Dein wichtigstes Ziel:
              </label>
              <div className="grid grid-2 gap-sm">
                {goals.map((goal) => (
                  <button
                    key={goal.id}
                    onClick={() => setSelectedGoal(goal.id)}
                    className={`card text-center ${selectedGoal === goal.id ? 'border-2' : ''}`}
                    style={{
                      backgroundColor: selectedGoal === goal.id ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)',
                      border: selectedGoal === goal.id ? '2px solid #3b82f6' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div className="mb-sm" style={{ fontSize: '2rem' }}>{goal.emoji}</div>
                    <h4 className="mb-sm" style={{ color: '#1e293b' }}>{goal.name}</h4>
                    <p className="mb-0" style={{ fontSize: '0.875rem', color: '#64748b' }}>{goal.description}</p>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="card text-center" style={{ backgroundColor: 'rgba(29, 78, 216, 0.1)', border: '1px solid #1d4ed8' }}>
              <h3 className="mb-md" style={{ color: '#1e293b' }}>Strategie für {currentGoal?.name}</h3>
              <div className="mb-lg">
                <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#3b82f6', marginBottom: 'var(--space-sm)' }}>
                  {currentGoal?.emoji}
                </div>
                <p style={{ color: '#1d4ed8', fontWeight: '600' }}>{currentGoal?.name}</p>
              </div>
              <div className="mb-lg">
                <p style={{ color: '#1e293b' }}>{currentGoal?.description}</p>
              </div>
              <button className="btn" style={{ background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)', color: 'white' }}>
                Strategie ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Strategies Section */}
      <section id="strategies" className="section" style={{ backgroundColor: 'rgba(29, 78, 216, 0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Die 4 Säulen der Freelancer-Skalierung</h2>
            <p style={{ fontSize: '1.25rem', color: '#3b82f6' }}>
              Systematischer Aufbau deines profitablen Business
            </p>
          </div>
          <div className="grid grid-4">
            <div className="card text-center animate-fade-in-up" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🎯</div>
              <h3 className="mb-sm" style={{ color: '#1e293b' }}>Positionierung</h3>
              <p style={{ color: '#1e293b' }}>Finde deine Nische und werde zum Experten</p>
              <div style={{ color: '#3b82f6', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                +50% Preise
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🔧</div>
              <h3 className="mb-sm" style={{ color: '#1e293b' }}>Systeme</h3>
              <p style={{ color: '#1e293b' }}>Baue wiederholbare Prozesse auf</p>
              <div style={{ color: '#3b82f6', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                -70% Zeitaufwand
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🚀</div>
              <h3 className="mb-sm" style={{ color: '#1e293b' }}>Skalierung</h3>
              <p style={{ color: '#1e293b' }}>Erweitere dein Team und Angebot</p>
              <div style={{ color: '#3b82f6', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                +200% Umsatz
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.6s', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>💰</div>
              <h3 className="mb-sm" style={{ color: '#1e293b' }}>Automatisierung</h3>
              <p style={{ color: '#1e293b' }}>Geld verdienen im Schlaf</p>
              <div style={{ color: '#3b82f6', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                Passives Einkommen
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section id="success" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Erfolgsgeschichten von Freelancern</h2>
            <p style={{ color: '#3b82f6' }}>So haben es andere geschafft</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  TM
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#1e293b' }}>Thomas M.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#3b82f6' }}>
                    35 Jahre, Web-Entwickler
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#1e293b' }}>
                "Mit systematischer Skalierung habe ich mein Team auf 5 Mitarbeiter erweitert. 
                Jetzt verdiene ich 15.000€ im Monat!"
              </p>
              <div style={{ color: '#1d4ed8', fontWeight: '600' }}>
                Verdienst: 15.000€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(29, 78, 216, 0.1)', border: '1px solid #1d4ed8' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#1d4ed8', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  SL
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#1e293b' }}>Sarah L.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#1d4ed8' }}>
                    29 Jahre, Grafik-Designerin
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#1e293b' }}>
                "Durch Automatisierung und Systeme kann ich jetzt 3x so viele Projekte 
                in der gleichen Zeit bearbeiten!"
              </p>
              <div style={{ color: '#3b82f6', fontWeight: '600' }}>
                Verdienst: 12.000€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Bereit für die nächste Stufe?</h2>
            <p className="mb-lg" style={{ color: '#1e293b' }}>
              Starte noch heute und baue dir ein skalierbares Freelance-Business
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#3b82f6' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#3b82f6' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#3b82f6' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#3b82f6' }}>
                Kostenlose Business-Analyse + Skalierungsplan
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn" style={{ background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)', color: 'white' }}>
                Jetzt kostenlos analysieren
              </button>
              <button className="btn btn-outline" style={{ color: '#3b82f6', borderColor: '#3b82f6' }}>
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#1e293b' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Projekt-Profit</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Systematische Skalierung für Freelancer
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Strategien</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Positionierung</a></li>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Systeme</a></li>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Skalierung</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Business-Analyse</a></li>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Webinare</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Rechtliches</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Impressum</a></li>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>Datenschutz</a></li>
                <li><a href="#" style={{ color: '#1e293b', textDecoration: 'none' }}>AGB</a></li>
              </ul>
            </div>
          </div>
          <div className="text-center mt-lg" style={{ borderTop: '1px solid rgba(59, 130, 246, 0.3)', paddingTop: 'var(--space-lg)' }}>
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
              © 2025 Projekt-Profit. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ProjektProfit; 