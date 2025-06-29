import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const FeierabendKapital: React.FC = () => {
  const [selectedPain, setSelectedPain] = useState('boredom');
  const [monthlyGoal, setMonthlyGoal] = useState(4000);

  const pains = [
    { id: 'boredom', name: 'Langeweile', description: 'Mein Job ist eintönig und nicht erfüllend', emoji: '😴' },
    { id: 'stress', name: 'Stress', description: 'Zu viel Druck und Überstunden', emoji: '😰' },
    { id: 'money', name: 'Geld', description: 'Ich verdiene nicht genug für meine Arbeit', emoji: '💰' },
    { id: 'freedom', name: 'Freiheit', description: 'Ich will mehr Zeit für mich und Familie', emoji: '🕊️' }
  ];

  const currentPain = pains.find(pain => pain.id === selectedPain);

  return (
    <div className="feierabend-kapital-page" style={{ backgroundColor: '#fdf4ff', color: '#581c87' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo" style={{ color: '#a855f7' }}>
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #a855f7, #7c3aed)' }}>F</div>
          Feierabend-Kapital
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link" style={{ color: '#581c87' }}>Home</a></li>
          <li><a href="#pains" className="nav-link" style={{ color: '#581c87' }}>Probleme</a></li>
          <li><a href="#solutions" className="nav-link" style={{ color: '#581c87' }}>Lösungen</a></li>
          <li><a href="#stories" className="nav-link" style={{ color: '#581c87' }}>Erfolge</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero" style={{ backgroundColor: '#fdf4ff', backgroundImage: 'linear-gradient(135deg, #fdf4ff 0%, #f3e8ff 100%)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: '#581c87' }}>
                Verdiene Geld im Feierabend - ohne Jobwechsel
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: '#a855f7' }}>
                Flexible Nebenjobs, die sich perfekt mit deinem Hauptjob vereinbaren lassen
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#a855f7' }}>
                      {monthlyGoal.toLocaleString()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#581c87' }}>
                      Monatlich möglich
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(124, 58, 237, 0.1)', border: '1px solid #7c3aed' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#7c3aed' }}>
                      2-3h/Tag
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#581c87' }}>
                      Nach Feierabend
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn" style={{ background: 'linear-gradient(135deg, #a855f7, #7c3aed)', color: 'white' }}>
                  Kostenlose Beratung
                </button>
                <button className="btn btn-outline" style={{ color: '#a855f7', borderColor: '#a855f7' }}>
                  Erfolgsgeschichten
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section" style={{ backgroundColor: 'rgba(168, 85, 247, 0.05)' }}>
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg" style={{ color: '#581c87' }}>Du bist nicht allein mit diesen Gefühlen</h2>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
                <h4 className="mb-sm">😴 Eintöniger Alltag</h4>
                <p style={{ color: '#581c87' }}>Jeden Tag das Gleiche - keine Herausforderung, keine Erfüllung</p>
              </div>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
                <h4 className="mb-sm">😰 Zu viel Stress</h4>
                <p style={{ color: '#581c87' }}>Überstunden, Druck, keine Wertschätzung für deine Arbeit</p>
              </div>
              <div className="card" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
                <h4 className="mb-sm">💰 Zu wenig Geld</h4>
                <p style={{ color: '#581c87' }}>Du arbeitest hart, aber das Gehalt reicht nicht für deine Träume</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center" style={{ backgroundColor: 'rgba(124, 58, 237, 0.1)', border: '1px solid #7c3aed' }}>
                <h3 className="mb-md" style={{ color: '#581c87' }}>Das sagen andere Angestellte:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic', color: '#a855f7' }}>
                  "Ich verdiene jetzt 4.500€ im Monat nebenbei. Endlich kann ich 
                  mir meine Träume erfüllen!"
                </blockquote>
                <p style={{ color: '#7c3aed', fontWeight: '600' }}>
                  - Lisa K., 34, Bürokauffrau
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pains Section */}
      <section id="pains" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#581c87' }}>Was belastet dich am meisten?</h2>
            <p style={{ fontSize: '1.25rem', color: '#a855f7' }}>
              Wähle dein größtes Problem und finde die passende Lösung
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg mb-xl">
            <div>
              <label className="block mb-sm" style={{ fontWeight: '600', color: '#581c87' }}>
                Dein größtes Problem:
              </label>
              <div className="grid grid-2 gap-sm">
                {pains.map((pain) => (
                  <button
                    key={pain.id}
                    onClick={() => setSelectedPain(pain.id)}
                    className={`card text-center ${selectedPain === pain.id ? 'border-2' : ''}`}
                    style={{
                      backgroundColor: selectedPain === pain.id ? 'rgba(168, 85, 247, 0.2)' : 'rgba(168, 85, 247, 0.1)',
                      border: selectedPain === pain.id ? '2px solid #a855f7' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div className="mb-sm" style={{ fontSize: '2rem' }}>{pain.emoji}</div>
                    <h4 className="mb-sm" style={{ color: '#581c87' }}>{pain.name}</h4>
                    <p className="mb-0" style={{ fontSize: '0.875rem', color: '#7c3aed' }}>{pain.description}</p>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="card text-center" style={{ backgroundColor: 'rgba(124, 58, 237, 0.1)', border: '1px solid #7c3aed' }}>
              <h3 className="mb-md" style={{ color: '#581c87' }}>Lösung für {currentPain?.name}</h3>
              <div className="mb-lg">
                <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#a855f7', marginBottom: 'var(--space-sm)' }}>
                  {currentPain?.emoji}
                </div>
                <p style={{ color: '#7c3aed', fontWeight: '600' }}>{currentPain?.name}</p>
              </div>
              <div className="mb-lg">
                <p style={{ color: '#581c87' }}>{currentPain?.description}</p>
              </div>
              <button className="btn" style={{ background: 'linear-gradient(135deg, #a855f7, #7c3aed)', color: 'white' }}>
                Lösung ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Solutions Section */}
      <section id="solutions" className="section" style={{ backgroundColor: 'rgba(124, 58, 237, 0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#581c87' }}>Perfekte Nebenjobs für Angestellte</h2>
            <p style={{ fontSize: '1.25rem', color: '#a855f7' }}>
              Diese Jobs lassen sich perfekt mit deinem Hauptjob vereinbaren
            </p>
          </div>
          <div className="grid grid-4">
            <div className="card text-center animate-fade-in-up" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>✍️</div>
              <h3 className="mb-sm" style={{ color: '#581c87' }}>Content Writing</h3>
              <p style={{ color: '#581c87' }}>Artikel schreiben nach Feierabend</p>
              <div style={{ color: '#a855f7', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                20-40€/Artikel
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🎨</div>
              <h3 className="mb-sm" style={{ color: '#581c87' }}>Social Media</h3>
              <p style={{ color: '#581c87' }}>Posts erstellen und verwalten</p>
              <div style={{ color: '#a855f7', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                500-1000€/Monat
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s', backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📞</div>
              <h3 className="mb-sm" style={{ color: '#581c87' }}>Online Support</h3>
              <p style={{ color: '#581c87' }}>Kundenservice von zu Hause</p>
              <div style={{ color: '#a855f7', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                15-20€/Stunde
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.6s', backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🛒</div>
              <h3 className="mb-sm" style={{ color: '#581c87' }}>Online Shop</h3>
              <p style={{ color: '#581c87' }}>Eigene Produkte verkaufen</p>
              <div style={{ color: '#a855f7', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                800-2000€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section id="stories" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#581c87' }}>Erfolgsgeschichten von Angestellten</h2>
            <p style={{ color: '#a855f7' }}>So haben es andere geschafft</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#a855f7', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  LK
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#581c87' }}>Lisa K.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#a855f7' }}>
                    34 Jahre, Bürokauffrau
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#581c87' }}>
                "Ich schreibe Artikel nach Feierabend und betreue Social Media Accounts. 
                Jetzt verdiene ich 4.500€ im Monat!"
              </p>
              <div style={{ color: '#7c3aed', fontWeight: '600' }}>
                Verdienst: 4.500€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(124, 58, 237, 0.1)', border: '1px solid #7c3aed' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#7c3aed', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  MJ
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#581c87' }}>Michael J.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#7c3aed' }}>
                    38 Jahre, IT-Systemadministrator
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#581c87' }}>
                "Ich verkaufe digitale Produkte online. Das läuft komplett automatisiert 
                und bringt 3.200€ im Monat!"
              </p>
              <div style={{ color: '#a855f7', fontWeight: '600' }}>
                Verdienst: 3.200€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', border: '1px solid #a855f7' }}>
            <h2 className="mb-md" style={{ color: '#581c87' }}>Bereit für dein Feierabend-Kapital?</h2>
            <p className="mb-lg" style={{ color: '#581c87' }}>
              Starte noch heute und verdiene Geld neben deinem Hauptjob
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#a855f7' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#a855f7' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#a855f7' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#a855f7' }}>
                Kostenlose Beratung + Job-Matching
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn" style={{ background: 'linear-gradient(135deg, #a855f7, #7c3aed)', color: 'white' }}>
                Jetzt kostenlos beraten lassen
              </button>
              <button className="btn btn-outline" style={{ color: '#a855f7', borderColor: '#a855f7' }}>
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(168, 85, 247, 0.1)', color: '#581c87' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Feierabend-Kapital</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Flexible Nebenjobs für Angestellte
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Jobs</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Content Writing</a></li>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Social Media</a></li>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Online Support</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Beratung</a></li>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Webinare</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Rechtliches</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Impressum</a></li>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>Datenschutz</a></li>
                <li><a href="#" style={{ color: '#581c87', textDecoration: 'none' }}>AGB</a></li>
              </ul>
            </div>
          </div>
          <div className="text-center mt-lg" style={{ borderTop: '1px solid rgba(168, 85, 247, 0.3)', paddingTop: 'var(--space-lg)' }}>
            <p style={{ fontSize: '0.875rem', color: '#7c3aed' }}>
              © 2025 Feierabend-Kapital. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default FeierabendKapital; 