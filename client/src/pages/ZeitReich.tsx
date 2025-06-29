import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const ZeitReich: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showCountdown, setShowCountdown] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('de-DE', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="zeit-reich-page">
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo logo-zeit">
          <div className="logo-icon">Z</div>
          Zeit-Reich
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link">Home</a></li>
          <li><a href="#about" className="nav-link">Über uns</a></li>
          <li><a href="#testimonials" className="nav-link">Erfolge</a></li>
          <li><a href="#contact" className="nav-link">Kontakt</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md">
                Verdiene Geld, während dein Baby schläft
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: 'var(--zeit-primary)' }}>
                Entdecke flexible Nebenjobs, die sich perfekt in deine Elternzeit einfügen
              </p>
              <div className="mb-xl">
                <span style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                  Aktuelle Zeit: {formatTime(currentTime)}
                </span>
              </div>
              <div className="flex justify-center gap-md">
                <button 
                  className="btn btn-zeit"
                  onClick={() => setShowCountdown(true)}
                >
                  Kostenloses Quiz starten
                </button>
                <button className="btn btn-outline">
                  Erfolgsgeschichten ansehen
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
              <h2 className="mb-lg">Du bist nicht allein mit diesem Problem</h2>
              <div className="card mb-md">
                <h4 className="mb-sm">⏰ Zeitmangel</h4>
                <p>Zwischen Windelwechseln und Schlafenszeiten bleibt kaum Zeit für dich selbst</p>
              </div>
              <div className="card mb-md">
                <h4 className="mb-sm">💰 Finanzielle Sorgen</h4>
                <p>Das Elterngeld reicht oft nicht aus, um den gewohnten Lebensstandard zu halten</p>
              </div>
              <div className="card">
                <h4 className="mb-sm">😰 Berufliche Unsicherheit</h4>
                <p>Du hast Angst, den Anschluss zu verlieren und deine Fähigkeiten zu verlieren</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center">
                <h3 className="mb-md">Das sagen andere Mütter:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic' }}>
                  "Ich dachte, ich müsste mich zwischen Familie und Karriere entscheiden. 
                  Zeit-Reich hat mir gezeigt, dass beides möglich ist!"
                </blockquote>
                <p style={{ color: 'var(--zeit-primary)', fontWeight: '600' }}>
                  - Sarah M., 32, Mutter von 2 Kindern
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="section" style={{ backgroundColor: 'var(--flow-light)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md">Die Lösung: Flexible Nebenjobs für Eltern</h2>
            <p style={{ fontSize: '1.25rem' }}>
              Entdecke Möglichkeiten, die sich an deinen Zeitplan anpassen
            </p>
          </div>
          <div className="grid grid-3">
            <div className="card text-center animate-fade-in-up">
              <div className="mb-md" style={{ fontSize: '3rem' }}>✍️</div>
              <h3 className="mb-sm">Content Writing</h3>
              <p>Schreibe Artikel, Blog-Posts oder Produktbeschreibungen - wann immer du Zeit hast</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--zeit-accent)', fontWeight: '600' }}>
                  Verdienst: 15-50€ pro Artikel
                </span>
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📱</div>
              <h3 className="mb-sm">Social Media</h3>
              <p>Verwalte Social Media Accounts für kleine Unternehmen - perfekt für Social Media Affine</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--zeit-accent)', fontWeight: '600' }}>
                  Verdienst: 300-800€ pro Monat
                </span>
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🎨</div>
              <h3 className="mb-sm">Design & Kreativität</h3>
              <p>Erstelle Logos, Grafiken oder Videos - nutze deine kreativen Fähigkeiten</p>
              <div className="mt-lg">
                <span style={{ color: 'var(--zeit-accent)', fontWeight: '600' }}>
                  Verdienst: 50-200€ pro Projekt
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Quiz Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center">
            <h2 className="mb-md">Finde deinen perfekten Nebenjob in 60 Sekunden</h2>
            <p className="mb-lg">
              Unser Quiz zeigt dir basierend auf deinen Fähigkeiten und deinem Zeitplan 
              die besten Möglichkeiten auf
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--zeit-primary)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--zeit-primary)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--zeit-primary)' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                Nur 3 einfache Fragen
              </p>
            </div>
            <button className="btn btn-zeit">
              Quiz jetzt starten
            </button>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="section" style={{ backgroundColor: 'var(--flow-light)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md">Erfolgsgeschichten von echten Müttern</h2>
            <p>Sieh dir an, wie andere es geschafft haben</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up">
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--zeit-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  LM
                </div>
                <div>
                  <h4 className="mb-0">Lisa Müller</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                    Mutter von 2 Kindern, 29 Jahre
                  </p>
                </div>
              </div>
              <p className="mb-md">
                "Ich verdiene jetzt 450€ im Monat mit Content Writing. 
                Das Beste: Ich kann arbeiten, wann mein Baby schläft!"
              </p>
              <div style={{ color: 'var(--zeit-accent)', fontWeight: '600' }}>
                Verdienst: 450€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--zeit-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  AK
                </div>
                <div>
                  <h4 className="mb-0">Anna Klein</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--flow-neutral)' }}>
                    Mutter von 1 Kind, 31 Jahre
                  </p>
                </div>
              </div>
              <p className="mb-md">
                "Social Media Management war die perfekte Lösung für mich. 
                Ich nutze meine Marketing-Erfahrung und bin flexibel!"
              </p>
              <div style={{ color: 'var(--zeit-accent)', fontWeight: '600' }}>
                Verdienst: 650€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center">
            <h2 className="mb-md">Bereit für deine finanzielle Freiheit?</h2>
            <p className="mb-lg">
              Starte noch heute und entdecke, wie du deine Elternzeit 
              zur Chance für deine Karriere machst
            </p>
            {showCountdown && (
              <div className="mb-lg p-md" style={{ backgroundColor: 'var(--zeit-primary)', color: 'white', borderRadius: 'var(--radius-lg)' }}>
                <h4 className="mb-sm">⏰ Angebot läuft in: 23:47:12</h4>
                <p className="mb-0">Nur heute: Kostenloser Guide + Community-Zugang</p>
              </div>
            )}
            <div className="flex justify-center gap-md">
              <button className="btn btn-zeit">
                Jetzt kostenlos starten
              </button>
              <button className="btn btn-outline">
                Mehr erfahren
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
              <h4 className="mb-md">Zeit-Reich</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Dein Weg zur finanziellen Freiheit in der Elternzeit
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Nebenjobs</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Content Writing</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Social Media</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Design</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Support</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>FAQ</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Kontakt</a></li>
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
              © 2025 Zeit-Reich. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ZeitReich; 