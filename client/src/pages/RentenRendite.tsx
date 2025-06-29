import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const RentenRendite: React.FC = () => {
  const [selectedConcern, setSelectedConcern] = useState('pension');
  const [monthlyIncome, setMonthlyIncome] = useState(3000);

  const concerns = [
    { id: 'pension', name: 'Rentenlücke', description: 'Die gesetzliche Rente reicht nicht aus', emoji: '💰' },
    { id: 'security', name: 'Sicherheit', description: 'Ich will mein Geld sicher anlegen', emoji: '🛡️' },
    { id: 'knowledge', name: 'Wissen', description: 'Ich verstehe die Finanzmärkte nicht', emoji: '📚' },
    { id: 'time', name: 'Zeit', description: 'Ich habe nicht viel Zeit zum Lernen', emoji: '⏰' }
  ];

  const currentConcern = concerns.find(concern => concern.id === selectedConcern);

  return (
    <div className="renten-rendite-page" style={{ backgroundColor: '#f0f9ff', color: '#0f172a' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo" style={{ color: '#0ea5e9' }}>
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #0ea5e9, #0369a1)' }}>R</div>
          Renten-Rendite
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link" style={{ color: '#0f172a' }}>Home</a></li>
          <li><a href="#concerns" className="nav-link" style={{ color: '#0f172a' }}>Sorgen</a></li>
          <li><a href="#solutions" className="nav-link" style={{ color: '#0f172a' }}>Lösungen</a></li>
          <li><a href="#testimonials" className="nav-link" style={{ color: '#0f172a' }}>Erfahrungen</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero" style={{ backgroundColor: '#f0f9ff', backgroundImage: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: '#0f172a' }}>
                Sichere deine finanzielle Zukunft - auch mit 50+
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: '#0ea5e9' }}>
                Bewährte Anlagestrategien für ein sorgenfreies Leben im Ruhestand
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#0ea5e9' }}>
                      {monthlyIncome.toLocaleString()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#0f172a' }}>
                      Monatlich möglich
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(3, 105, 161, 0.1)', border: '1px solid #0369a1' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#0369a1' }}>
                      7-12% p.a.
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#0f172a' }}>
                      Sichere Rendite
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn" style={{ background: 'linear-gradient(135deg, #0ea5e9, #0369a1)', color: 'white' }}>
                  Kostenlose Beratung
                </button>
                <button className="btn btn-outline" style={{ color: '#0ea5e9', borderColor: '#0ea5e9' }}>
                  Erfahrungsberichte
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section" style={{ backgroundColor: 'rgba(14, 165, 233, 0.05)' }}>
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg" style={{ color: '#0f172a' }}>Die Realität der Altersvorsorge</h2>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
                <h4 className="mb-sm">💰 Rentenlücke wächst</h4>
                <p style={{ color: '#0f172a' }}>Die gesetzliche Rente wird immer weniger - du brauchst eine private Vorsorge</p>
              </div>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
                <h4 className="mb-sm">😰 Angst vor Verlusten</h4>
                <p style={{ color: '#0f172a' }}>Du willst dein hart verdientes Geld nicht riskieren</p>
              </div>
              <div className="card" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
                <h4 className="mb-sm">📉 Niedrige Zinsen</h4>
                <p style={{ color: '#0f172a' }}>Sparbuch und Lebensversicherung bringen kaum noch Rendite</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center" style={{ backgroundColor: 'rgba(3, 105, 161, 0.1)', border: '1px solid #0369a1' }}>
                <h3 className="mb-md" style={{ color: '#0f172a' }}>Das sagen andere Best Ager:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic', color: '#0ea5e9' }}>
                  "Mit der richtigen Strategie verdiene ich jetzt 3.500€ im Monat passiv. 
                  Endlich kann ich ruhig schlafen!"
                </blockquote>
                <p style={{ color: '#0369a1', fontWeight: '600' }}>
                  - Hans M., 58, ehemaliger Ingenieur
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Concerns Section */}
      <section id="concerns" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#0f172a' }}>Was beschäftigt dich am meisten?</h2>
            <p style={{ fontSize: '1.25rem', color: '#0ea5e9' }}>
              Wähle deine größte Sorge und finde die passende Lösung
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg mb-xl">
            <div>
              <label className="block mb-sm" style={{ fontWeight: '600', color: '#0f172a' }}>
                Deine größte Sorge:
              </label>
              <div className="grid grid-2 gap-sm">
                {concerns.map((concern) => (
                  <button
                    key={concern.id}
                    onClick={() => setSelectedConcern(concern.id)}
                    className={`card text-center ${selectedConcern === concern.id ? 'border-2' : ''}`}
                    style={{
                      backgroundColor: selectedConcern === concern.id ? 'rgba(14, 165, 233, 0.2)' : 'rgba(14, 165, 233, 0.1)',
                      border: selectedConcern === concern.id ? '2px solid #0ea5e9' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div className="mb-sm" style={{ fontSize: '2rem' }}>{concern.emoji}</div>
                    <h4 className="mb-sm" style={{ color: '#0f172a' }}>{concern.name}</h4>
                    <p className="mb-0" style={{ fontSize: '0.875rem', color: '#475569' }}>{concern.description}</p>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="card text-center" style={{ backgroundColor: 'rgba(3, 105, 161, 0.1)', border: '1px solid #0369a1' }}>
              <h3 className="mb-md" style={{ color: '#0f172a' }}>Lösung für {currentConcern?.name}</h3>
              <div className="mb-lg">
                <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#0ea5e9', marginBottom: 'var(--space-sm)' }}>
                  {currentConcern?.emoji}
                </div>
                <p style={{ color: '#0369a1', fontWeight: '600' }}>{currentConcern?.name}</p>
              </div>
              <div className="mb-lg">
                <p style={{ color: '#0f172a' }}>{currentConcern?.description}</p>
              </div>
              <button className="btn" style={{ background: 'linear-gradient(135deg, #0ea5e9, #0369a1)', color: 'white' }}>
                Lösung ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Solutions Section */}
      <section id="solutions" className="section" style={{ backgroundColor: 'rgba(3, 105, 161, 0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#0f172a' }}>Bewährte Anlagestrategien für Best Ager</h2>
            <p style={{ fontSize: '1.25rem', color: '#0ea5e9' }}>
              Sichere und profitable Wege zur Altersvorsorge
            </p>
          </div>
          <div className="grid grid-4">
            <div className="card text-center animate-fade-in-up" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🏠</div>
              <h3 className="mb-sm" style={{ color: '#0f172a' }}>Immobilien</h3>
              <p style={{ color: '#0f172a' }}>Sichere Mieteinnahmen und Wertsteigerung</p>
              <div style={{ color: '#0ea5e9', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                4-6% Rendite
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📊</div>
              <h3 className="mb-sm" style={{ color: '#0f172a' }}>Dividenden</h3>
              <p style={{ color: '#0f172a' }}>Regelmäßige Ausschüttungen von Top-Unternehmen</p>
              <div style={{ color: '#0ea5e9', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                5-8% Rendite
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s', backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>💼</div>
              <h3 className="mb-sm" style={{ color: '#0f172a' }}>Rentenfonds</h3>
              <p style={{ color: '#0f172a' }}>Professionell gemanagte Anleihen-Portfolios</p>
              <div style={{ color: '#0ea5e9', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                3-5% Rendite
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.6s', backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>⚡</div>
              <h3 className="mb-sm" style={{ color: '#0f172a' }}>KI-Trading</h3>
              <p style={{ color: '#0f172a' }}>Automatisierte Handelssysteme</p>
              <div style={{ color: '#0ea5e9', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                8-12% Rendite
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#0f172a' }}>Erfahrungsberichte von Best Agern</h2>
            <p style={{ color: '#0ea5e9' }}>So haben es andere geschafft</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#0ea5e9', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  HM
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#0f172a' }}>Hans M.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#0ea5e9' }}>
                    58 Jahre, ehemaliger Ingenieur
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#0f172a' }}>
                "Mit der richtigen Anlagestrategie verdiene ich jetzt 3.500€ im Monat passiv. 
                Endlich kann ich ruhig schlafen!"
              </p>
              <div style={{ color: '#0369a1', fontWeight: '600' }}>
                Verdienst: 3.500€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(3, 105, 161, 0.1)', border: '1px solid #0369a1' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#0369a1', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  EW
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#0f172a' }}>Erika W.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#0369a1' }}>
                    62 Jahre, ehemalige Lehrerin
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#0f172a' }}>
                "Ich habe nie verstanden, wie man Geld anlegt. Jetzt habe ich ein sicheres 
                System und verdiene 2.800€ im Monat!"
              </p>
              <div style={{ color: '#0ea5e9', fontWeight: '600' }}>
                Verdienst: 2.800€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', border: '1px solid #0ea5e9' }}>
            <h2 className="mb-md" style={{ color: '#0f172a' }}>Bereit für deine finanzielle Sicherheit?</h2>
            <p className="mb-lg" style={{ color: '#0f172a' }}>
              Starte noch heute und sichere dir ein sorgenfreies Leben im Ruhestand
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#0ea5e9' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#0ea5e9' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#0ea5e9' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#0ea5e9' }}>
                Kostenlose Beratung + Anlagestrategie
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn" style={{ background: 'linear-gradient(135deg, #0ea5e9, #0369a1)', color: 'white' }}>
                Jetzt kostenlos beraten lassen
              </button>
              <button className="btn btn-outline" style={{ color: '#0ea5e9', borderColor: '#0ea5e9' }}>
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(14, 165, 233, 0.1)', color: '#0f172a' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Renten-Rendite</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Sichere Altersvorsorge für Best Ager
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Anlagen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Immobilien</a></li>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Dividenden</a></li>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Rentenfonds</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Beratung</a></li>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Webinare</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Rechtliches</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Impressum</a></li>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>Datenschutz</a></li>
                <li><a href="#" style={{ color: '#0f172a', textDecoration: 'none' }}>AGB</a></li>
              </ul>
            </div>
          </div>
          <div className="text-center mt-lg" style={{ borderTop: '1px solid rgba(14, 165, 233, 0.3)', paddingTop: 'var(--space-lg)' }}>
            <p style={{ fontSize: '0.875rem', color: '#475569' }}>
              © 2025 Renten-Rendite. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default RentenRendite; 