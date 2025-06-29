import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const StarterKapital: React.FC = () => {
  const [selectedSkill, setSelectedSkill] = useState('content');
  const [earnings, setEarnings] = useState(500);

  const skills = [
    { id: 'content', name: 'Content Creation', earnings: 800, time: '2-3h/Woche', emoji: '✍️' },
    { id: 'social', name: 'Social Media', earnings: 1200, time: '3-4h/Woche', emoji: '📱' },
    { id: 'design', name: 'Design & Branding', earnings: 1500, time: '4-5h/Woche', emoji: '🎨' },
    { id: 'coding', name: 'Web Development', earnings: 2000, time: '5-6h/Woche', emoji: '💻' }
  ];

  const currentSkill = skills.find(skill => skill.id === selectedSkill);

  return (
    <div className="starter-kapital-page" style={{ backgroundColor: 'var(--starter-primary)', color: 'var(--flow-white)' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo logo-starter">
          <div className="logo-icon">S</div>
          Starter-Kapital
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link" style={{ color: 'var(--flow-white)' }}>Home</a></li>
          <li><a href="#skills" className="nav-link" style={{ color: 'var(--flow-white)' }}>Skills</a></li>
          <li><a href="#success" className="nav-link" style={{ color: 'var(--flow-white)' }}>Erfolge</a></li>
          <li><a href="#contact" className="nav-link" style={{ color: 'var(--flow-white)' }}>Kontakt</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero" style={{ backgroundColor: 'var(--starter-primary)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: 'var(--flow-white)' }}>
                Vergiss den 08/15-Nebenjob
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: 'var(--starter-secondary)' }}>
                Lerne gefragte digitale Skills und baue dir ein echtes Side-Business auf
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--starter-secondary)' }}>
                      {currentSkill?.earnings}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-white)' }}>
                      Monatlich möglich
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-accent)' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--starter-accent)' }}>
                      {currentSkill?.time}
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--flow-white)' }}>
                      Zeitaufwand
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn btn-starter">
                  Kostenlosen Skill-Check starten
                </button>
                <button className="btn btn-outline" style={{ color: 'var(--starter-secondary)', borderColor: 'var(--starter-secondary)' }}>
                  Erfolgsgeschichten ansehen
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section" style={{ backgroundColor: 'rgba(255,255,255,0.05)' }}>
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg" style={{ color: 'var(--flow-white)' }}>Du bist nicht allein mit diesem Problem</h2>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
                <h4 className="mb-sm">💰 Studiengebühren & Kosten</h4>
                <p style={{ color: 'var(--flow-white)' }}>Du brauchst Geld, aber Kellnern ist Zeitverschwendung</p>
              </div>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
                <h4 className="mb-sm">😰 FOMO - Fear of Missing Out</h4>
                <p style={{ color: 'var(--flow-white)' }}>Du siehst auf TikTok, wie andere online Geld verdienen</p>
              </div>
              <div className="card" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
                <h4 className="mb-sm">📚 Fehlende digitale Skills</h4>
                <p style={{ color: 'var(--flow-white)' }}>Dein Studium bereitet dich nicht auf die digitale Wirtschaft vor</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-accent)' }}>
                <h3 className="mb-md" style={{ color: 'var(--flow-white)' }}>Das sagen andere Studenten:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic', color: 'var(--starter-secondary)' }}>
                  "Ich verdiene jetzt mehr mit Content Creation als mit meinem Nebenjob. 
                  Und es macht sogar Spaß!"
                </blockquote>
                <p style={{ color: 'var(--starter-accent)', fontWeight: '600' }}>
                  - Max K., 22, BWL-Student
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: 'var(--flow-white)' }}>Die gefragtesten digitalen Skills 2025</h2>
            <p style={{ fontSize: '1.25rem', color: 'var(--starter-secondary)' }}>
              Wähle deinen Skill und sieh, was möglich ist
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg mb-xl">
            <div>
              <label className="block mb-sm" style={{ fontWeight: '600', color: 'var(--flow-white)' }}>
                Wähle deinen Skill:
              </label>
              <div className="grid grid-2 gap-sm">
                {skills.map((skill) => (
                  <button
                    key={skill.id}
                    onClick={() => setSelectedSkill(skill.id)}
                    className={`card text-center ${selectedSkill === skill.id ? 'border-2' : ''}`}
                    style={{
                      backgroundColor: selectedSkill === skill.id ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.1)',
                      border: selectedSkill === skill.id ? `2px solid ${skill.id === 'content' ? 'var(--starter-secondary)' : skill.id === 'social' ? 'var(--starter-accent)' : 'var(--starter-secondary)'}` : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div className="mb-sm" style={{ fontSize: '2rem' }}>{skill.emoji}</div>
                    <h4 className="mb-0" style={{ color: 'var(--flow-white)' }}>{skill.name}</h4>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="card text-center" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-accent)' }}>
              <h3 className="mb-md" style={{ color: 'var(--flow-white)' }}>Dein Potenzial mit {currentSkill?.name}</h3>
              <div className="mb-lg">
                <div style={{ fontSize: '3rem', fontWeight: '700', color: 'var(--starter-accent)', marginBottom: 'var(--space-sm)' }}>
                  {currentSkill?.earnings}€
                </div>
                <p style={{ color: 'var(--starter-secondary)' }}>Monatlich möglich</p>
              </div>
              <div className="mb-lg">
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--starter-secondary)', marginBottom: 'var(--space-sm)' }}>
                  {currentSkill?.time}
                </div>
                <p style={{ color: 'var(--starter-secondary)' }}>Zeitaufwand</p>
              </div>
              <button className="btn btn-starter">
                Jetzt lernen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="section" style={{ backgroundColor: 'rgba(255,255,255,0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: 'var(--flow-white)' }}>Der Starter-Kapital Weg</h2>
            <p style={{ fontSize: '1.25rem', color: 'var(--starter-secondary)' }}>
              In 4 Wochen vom Anfänger zum Side-Hustle-Profi
            </p>
          </div>
          <div className="grid grid-4">
            <div className="card text-center animate-fade-in-up" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🎯</div>
              <h3 className="mb-sm" style={{ color: 'var(--flow-white)' }}>Woche 1: Skill-Auswahl</h3>
              <p style={{ color: 'var(--flow-white)' }}>Finde deinen perfekten Skill basierend auf deinen Interessen</p>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📚</div>
              <h3 className="mb-sm" style={{ color: 'var(--flow-white)' }}>Woche 2: Lernen</h3>
              <p style={{ color: 'var(--flow-white)' }}>Intensive Praxis mit echten Projekten</p>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s', backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🚀</div>
              <h3 className="mb-sm" style={{ color: 'var(--flow-white)' }}>Woche 3: Start</h3>
              <p style={{ color: 'var(--flow-white)' }}>Erste Kunden gewinnen und Geld verdienen</p>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.6s', backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>💰</div>
              <h3 className="mb-sm" style={{ color: 'var(--flow-white)' }}>Woche 4: Skalieren</h3>
              <p style={{ color: 'var(--flow-white)' }}>Mehr Kunden, höhere Preise, mehr Einkommen</p>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section id="success" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: 'var(--flow-white)' }}>Echte Erfolge von Studenten</h2>
            <p style={{ color: 'var(--starter-secondary)' }}>Sieh dir an, wie andere es geschafft haben</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-secondary)' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--starter-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--starter-primary)', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  MK
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: 'var(--flow-white)' }}>Max K.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--starter-secondary)' }}>
                    22 Jahre, BWL-Student
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: 'var(--flow-white)' }}>
                "Content Creation war die perfekte Lösung. Ich schreibe Artikel für Startups 
                und verdiene 800€ im Monat!"
              </p>
              <div style={{ color: 'var(--starter-accent)', fontWeight: '600' }}>
                Verdienst: 800€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-accent)' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'var(--starter-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--starter-primary)', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  LJ
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: 'var(--flow-white)' }}>Lisa J.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: 'var(--starter-secondary)' }}>
                    20 Jahre, Design-Studentin
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: 'var(--flow-white)' }}>
                "Social Media Management war der Gamechanger. Ich verwalte Accounts 
                für kleine Unternehmen und verdiene 1.200€!"
              </p>
              <div style={{ color: 'var(--starter-accent)', fontWeight: '600' }}>
                Verdienst: 1.200€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(255,255,255,0.1)', border: '1px solid var(--starter-accent)' }}>
            <h2 className="mb-md" style={{ color: 'var(--flow-white)' }}>Bereit für deinen unfairen Vorteil?</h2>
            <p className="mb-lg" style={{ color: 'var(--flow-white)' }}>
              Starte noch heute und baue dir ein Side-Business auf, das deine Karriere beschleunigt
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--starter-accent)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--starter-accent)' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'var(--starter-accent)' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--starter-secondary)' }}>
                Kostenloser Skill-Check + Persönlicher Plan
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn btn-starter">
                Jetzt kostenlos starten
              </button>
              <button className="btn btn-outline" style={{ color: 'var(--starter-secondary)', borderColor: 'var(--starter-secondary)' }}>
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(0,0,0,0.3)', color: 'white' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Starter-Kapital</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Dein Weg zum digitalen Side-Business
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Skills</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Content Creation</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Social Media</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Design & Branding</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Skill-Check</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Webinare</a></li>
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
          <div className="text-center mt-lg" style={{ borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: 'var(--space-lg)' }}>
            <p style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.6)' }}>
              © 2025 Starter-Kapital. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default StarterKapital; 