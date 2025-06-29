import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const ElternEinkommen: React.FC = () => {
  const [selectedChallenge, setSelectedChallenge] = useState('time');
  const [monthlyGoal, setMonthlyGoal] = useState(2000);

  const challenges = [
    { id: 'time', name: 'Zeitmangel', description: 'Zwischen Kind und Haushalt bleibt kaum Zeit für Arbeit', emoji: '⏰' },
    { id: 'money', name: 'Finanzielle Sorgen', description: 'Ein Gehalt weniger macht sich stark bemerkbar', emoji: '💰' },
    { id: 'skills', name: 'Fehlende Skills', description: 'Ich weiß nicht, wie ich online Geld verdienen kann', emoji: '📚' },
    { id: 'confidence', name: 'Sicherheit', description: 'Ich traue mich nicht, etwas Neues zu starten', emoji: '🤗' }
  ];

  const currentChallenge = challenges.find(challenge => challenge.id === selectedChallenge);

  return (
    <div className="eltern-einkommen-page" style={{ backgroundColor: '#fef7f0', color: '#374151' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo" style={{ color: '#f59e0b' }}>
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #f97316)' }}>E</div>
          Eltern-Einkommen
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link" style={{ color: '#374151' }}>Home</a></li>
          <li><a href="#challenges" className="nav-link" style={{ color: '#374151' }}>Herausforderungen</a></li>
          <li><a href="#solutions" className="nav-link" style={{ color: '#374151' }}>Lösungen</a></li>
          <li><a href="#stories" className="nav-link" style={{ color: '#374151' }}>Erfolge</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero" style={{ backgroundColor: '#fef7f0', backgroundImage: 'linear-gradient(135deg, #fef7f0 0%, #fed7aa 100%)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: '#374151' }}>
                Verdiene Geld von zu Hause - auch mit Kind
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: '#f59e0b' }}>
                Flexible Online-Jobs, die sich perfekt mit der Elternzeit vereinbaren lassen
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#f59e0b' }}>
                      {monthlyGoal.toLocaleString()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#374151' }}>
                      Monatlich möglich
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(249, 115, 22, 0.1)', border: '1px solid #f97316' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#f97316' }}>
                      2-3h/Tag
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#374151' }}>
                      Flexibel einteilbar
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn" style={{ background: 'linear-gradient(135deg, #f59e0b, #f97316)', color: 'white' }}>
                  Kostenlose Beratung
                </button>
                <button className="btn btn-outline" style={{ color: '#f59e0b', borderColor: '#f59e0b' }}>
                  Erfolgsgeschichten
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section" style={{ backgroundColor: 'rgba(245, 158, 11, 0.05)' }}>
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg" style={{ color: '#374151' }}>Du bist nicht allein mit diesen Herausforderungen</h2>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
                <h4 className="mb-sm">⏰ Keine Zeit für Vollzeitjob</h4>
                <p style={{ color: '#374151' }}>Zwischen Kind, Haushalt und Schlafmangel bleibt kaum Zeit für Arbeit</p>
              </div>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
                <h4 className="mb-sm">💰 Finanzielle Sorgen</h4>
                <p style={{ color: '#374151' }}>Ein Gehalt weniger macht sich stark im Haushaltsbudget bemerkbar</p>
              </div>
              <div className="card" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
                <h4 className="mb-sm">😰 Angst vor dem Wiedereinstieg</h4>
                <p style={{ color: '#374151' }}>Du hast das Gefühl, den Anschluss zu verlieren</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center" style={{ backgroundColor: 'rgba(249, 115, 22, 0.1)', border: '1px solid #f97316' }}>
                <h3 className="mb-md" style={{ color: '#374151' }}>Das sagen andere Eltern:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic', color: '#f59e0b' }}>
                  "Ich verdiene jetzt 2.500€ im Monat von zu Hause aus. 
                  Perfekt neben der Kinderbetreuung!"
                </blockquote>
                <p style={{ color: '#f97316', fontWeight: '600' }}>
                  - Maria S., 32, Mutter von 2 Kindern
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Challenges Section */}
      <section id="challenges" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#374151' }}>Welche Herausforderung beschäftigt dich am meisten?</h2>
            <p style={{ fontSize: '1.25rem', color: '#f59e0b' }}>
              Wähle deine größte Sorge und finde die passende Lösung
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg mb-xl">
            <div>
              <label className="block mb-sm" style={{ fontWeight: '600', color: '#374151' }}>
                Deine größte Herausforderung:
              </label>
              <div className="grid grid-2 gap-sm">
                {challenges.map((challenge) => (
                  <button
                    key={challenge.id}
                    onClick={() => setSelectedChallenge(challenge.id)}
                    className={`card text-center ${selectedChallenge === challenge.id ? 'border-2' : ''}`}
                    style={{
                      backgroundColor: selectedChallenge === challenge.id ? 'rgba(245, 158, 11, 0.2)' : 'rgba(245, 158, 11, 0.1)',
                      border: selectedChallenge === challenge.id ? '2px solid #f59e0b' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div className="mb-sm" style={{ fontSize: '2rem' }}>{challenge.emoji}</div>
                    <h4 className="mb-sm" style={{ color: '#374151' }}>{challenge.name}</h4>
                    <p className="mb-0" style={{ fontSize: '0.875rem', color: '#6b7280' }}>{challenge.description}</p>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="card text-center" style={{ backgroundColor: 'rgba(249, 115, 22, 0.1)', border: '1px solid #f97316' }}>
              <h3 className="mb-md" style={{ color: '#374151' }}>Deine Lösung für {currentChallenge?.name}</h3>
              <div className="mb-lg">
                <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#f59e0b', marginBottom: 'var(--space-sm)' }}>
                  {currentChallenge?.emoji}
                </div>
                <p style={{ color: '#f97316', fontWeight: '600' }}>{currentChallenge?.name}</p>
              </div>
              <div className="mb-lg">
                <p style={{ color: '#374151' }}>{currentChallenge?.description}</p>
              </div>
              <button className="btn" style={{ background: 'linear-gradient(135deg, #f59e0b, #f97316)', color: 'white' }}>
                Lösung ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Solutions Section */}
      <section id="solutions" className="section" style={{ backgroundColor: 'rgba(249, 115, 22, 0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#374151' }}>Flexible Jobs für Eltern</h2>
            <p style={{ fontSize: '1.25rem', color: '#f59e0b' }}>
              Diese Jobs lassen sich perfekt mit der Kinderbetreuung vereinbaren
            </p>
          </div>
          <div className="grid grid-4">
            <div className="card text-center animate-fade-in-up" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>✍️</div>
              <h3 className="mb-sm" style={{ color: '#374151' }}>Content Writing</h3>
              <p style={{ color: '#374151' }}>Artikel schreiben, wann du Zeit hast</p>
              <div style={{ color: '#f59e0b', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                15-25€/Artikel
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🎨</div>
              <h3 className="mb-sm" style={{ color: '#374151' }}>Social Media</h3>
              <p style={{ color: '#374151' }}>Posts erstellen und verwalten</p>
              <div style={{ color: '#f59e0b', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                300-800€/Monat
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>📞</div>
              <h3 className="mb-sm" style={{ color: '#374151' }}>Online Support</h3>
              <p style={{ color: '#374151' }}>Kundenservice von zu Hause</p>
              <div style={{ color: '#f59e0b', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                12-18€/Stunde
              </div>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.6s', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🛒</div>
              <h3 className="mb-sm" style={{ color: '#374151' }}>Online Shop</h3>
              <p style={{ color: '#374151' }}>Eigene Produkte verkaufen</p>
              <div style={{ color: '#f59e0b', fontWeight: '600', marginTop: 'var(--space-md)' }}>
                500-2000€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section id="stories" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#374151' }}>Erfolgsgeschichten von Eltern</h2>
            <p style={{ color: '#f59e0b' }}>So haben es andere geschafft</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#f59e0b', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  MS
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#374151' }}>Maria S.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#f59e0b' }}>
                    32 Jahre, Mutter von 2 Kindern
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#374151' }}>
                "Ich schreibe Artikel für verschiedene Websites. Das kann ich machen, 
                wenn die Kinder schlafen. Perfekt für mich!"
              </p>
              <div style={{ color: '#f97316', fontWeight: '600' }}>
                Verdienst: 2.500€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(249, 115, 22, 0.1)', border: '1px solid #f97316' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#f97316', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  AK
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: '#374151' }}>Anna K.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#f97316' }}>
                    28 Jahre, Mutter von 1 Kind
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: '#374151' }}>
                "Ich betreue Social Media Accounts für kleine Unternehmen. 
                Das macht mir Spaß und bringt gutes Geld!"
              </p>
              <div style={{ color: '#f59e0b', fontWeight: '600' }}>
                Verdienst: 1.800€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid #f59e0b' }}>
            <h2 className="mb-md" style={{ color: '#374151' }}>Bereit für dein Eltern-Einkommen?</h2>
            <p className="mb-lg" style={{ color: '#374151' }}>
              Starte noch heute und finde den perfekten Job für dich
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#f59e0b' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#f59e0b' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#f59e0b' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#f59e0b' }}>
                Kostenlose Beratung + Job-Matching
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn" style={{ background: 'linear-gradient(135deg, #f59e0b, #f97316)', color: 'white' }}>
                Jetzt kostenlos beraten lassen
              </button>
              <button className="btn btn-outline" style={{ color: '#f59e0b', borderColor: '#f59e0b' }}>
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#374151' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Eltern-Einkommen</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Flexible Jobs für Eltern in Elternzeit
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Jobs</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Content Writing</a></li>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Social Media</a></li>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Online Support</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Beratung</a></li>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Community</a></li>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Webinare</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Rechtliches</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Impressum</a></li>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>Datenschutz</a></li>
                <li><a href="#" style={{ color: '#374151', textDecoration: 'none' }}>AGB</a></li>
              </ul>
            </div>
          </div>
          <div className="text-center mt-lg" style={{ borderTop: '1px solid rgba(245, 158, 11, 0.3)', paddingTop: 'var(--space-lg)' }}>
            <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
              © 2025 Eltern-Einkommen. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ElternEinkommen; 