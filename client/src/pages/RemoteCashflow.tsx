import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const RemoteCashflow: React.FC = () => {
  const [selectedMethod, setSelectedMethod] = useState('ai');
  const [monthlyIncome, setMonthlyIncome] = useState(3000);

  const methods = [
    { id: 'ai', name: 'KI-gestützte Automatisierung', income: 5000, time: '2-3h/Woche', emoji: '🤖' },
    { id: 'dropshipping', name: 'Dropshipping Empire', income: 8000, time: '3-4h/Woche', emoji: '📦' },
    { id: 'affiliate', name: 'Affiliate Marketing', income: 12000, time: '4-5h/Woche', emoji: '💸' },
    { id: 'saas', name: 'SaaS Business', income: 25000, time: '5-6h/Woche', emoji: '⚡' }
  ];

  const currentMethod = methods.find(method => method.id === selectedMethod);

  return (
    <div className="remote-cashflow-page" style={{ backgroundColor: '#0f172a', color: 'white' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo" style={{ color: '#10b981' }}>
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #10b981, #3b82f6)' }}>R</div>
          Remote Cashflow
        </Link>
        <ul className="nav-links">
          <li><a href="#home" className="nav-link" style={{ color: 'white' }}>Home</a></li>
          <li><a href="#methods" className="nav-link" style={{ color: 'white' }}>Methoden</a></li>
          <li><a href="#success" className="nav-link" style={{ color: 'white' }}>Erfolge</a></li>
          <li><a href="#contact" className="nav-link" style={{ color: 'white' }}>Kontakt</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero" style={{ backgroundColor: '#0f172a', backgroundImage: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: 'white' }}>
                Der moderne Weg zum passiven Einkommen
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: '#10b981' }}>
                KI-gestützte Business-Methoden für den digitalen Unternehmer von heute
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#10b981' }}>
                      {currentMethod?.income.toLocaleString()}€
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'white' }}>
                      Monatlich möglich
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#3b82f6' }}>
                      {currentMethod?.time}
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'white' }}>
                      Zeitaufwand
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-center gap-md">
                <button className="btn" style={{ background: 'linear-gradient(135deg, #10b981, #3b82f6)', color: 'white' }}>
                  Business-Analyse starten
                </button>
                <button className="btn btn-outline" style={{ color: '#f59e0b', borderColor: '#f59e0b' }}>
                  Case Studies ansehen
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section" style={{ backgroundColor: 'rgba(16, 185, 129, 0.05)' }}>
        <div className="container">
          <div className="grid grid-2 items-center">
            <div className="animate-slide-in-left">
              <h2 className="mb-lg" style={{ color: 'white' }}>Die alten Business-Modelle sind tot</h2>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
                <h4 className="mb-sm">🚫 9-to-5 Hamsterrad</h4>
                <p style={{ color: 'white' }}>Du verkaufst deine Zeit gegen Geld - das ist nicht skalierbar</p>
              </div>
              <div className="card mb-md" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
                <h4 className="mb-sm">😰 Keine Automatisierung</h4>
                <p style={{ color: 'white' }}>Du musst für jeden Euro arbeiten, auch im Urlaub</p>
              </div>
              <div className="card" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
                <h4 className="mb-sm">📉 Verpasste KI-Revolution</h4>
                <p style={{ color: 'white' }}>Du nutzt nicht die Macht der künstlichen Intelligenz</p>
              </div>
            </div>
            <div className="animate-slide-in-right">
              <div className="card text-center" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                <h3 className="mb-md" style={{ color: 'white' }}>Das sagen andere Digital Entrepreneurs:</h3>
                <blockquote className="mb-lg" style={{ fontSize: '1.125rem', fontStyle: 'italic', color: '#10b981' }}>
                  "Mit KI-Automatisierung verdiene ich jetzt 15.000€ passiv im Monat. 
                  Das ist die Zukunft des Business!"
                </blockquote>
                <p style={{ color: '#3b82f6', fontWeight: '600' }}>
                  - Alex M., 29, Digital Entrepreneur
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Methods Section */}
      <section id="methods" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: 'white' }}>Die 4 modernen Business-Methoden</h2>
            <p style={{ fontSize: '1.25rem', color: '#10b981' }}>
              Wähle deine Methode und sieh das Potenzial
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg mb-xl">
            <div>
              <label className="block mb-sm" style={{ fontWeight: '600', color: 'white' }}>
                Wähle deine Business-Methode:
              </label>
              <div className="grid grid-2 gap-sm">
                {methods.map((method) => (
                  <button
                    key={method.id}
                    onClick={() => setSelectedMethod(method.id)}
                    className={`card text-center ${selectedMethod === method.id ? 'border-2' : ''}`}
                    style={{
                      backgroundColor: selectedMethod === method.id ? 'rgba(16, 185, 129, 0.2)' : 'rgba(16, 185, 129, 0.1)',
                      border: selectedMethod === method.id ? '2px solid #10b981' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div className="mb-sm" style={{ fontSize: '2rem' }}>{method.emoji}</div>
                    <h4 className="mb-0" style={{ color: 'white' }}>{method.name}</h4>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="card text-center" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <h3 className="mb-md" style={{ color: 'white' }}>Dein Potenzial mit {currentMethod?.name}</h3>
              <div className="mb-lg">
                <div style={{ fontSize: '3rem', fontWeight: '700', color: '#10b981', marginBottom: 'var(--space-sm)' }}>
                  {currentMethod?.income.toLocaleString()}€
                </div>
                <p style={{ color: '#3b82f6' }}>Monatlich möglich</p>
              </div>
              <div className="mb-lg">
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#f59e0b', marginBottom: 'var(--space-sm)' }}>
                  {currentMethod?.time}
                </div>
                <p style={{ color: '#3b82f6' }}>Zeitaufwand</p>
              </div>
              <button className="btn" style={{ background: 'linear-gradient(135deg, #10b981, #3b82f6)', color: 'white' }}>
                Jetzt starten
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="section" style={{ backgroundColor: 'rgba(59, 130, 246, 0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: 'white' }}>Der Remote Cashflow Weg</h2>
            <p style={{ fontSize: '1.25rem', color: '#10b981' }}>
              In 90 Tagen vom Anfänger zum Digital Entrepreneur
            </p>
          </div>
          <div className="grid grid-4">
            <div className="card text-center animate-fade-in-up" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🎯</div>
              <h3 className="mb-sm" style={{ color: 'white' }}>Phase 1: Setup</h3>
              <p style={{ color: 'white' }}>Business-Modell wählen und technische Grundlagen schaffen</p>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🤖</div>
              <h3 className="mb-sm" style={{ color: 'white' }}>Phase 2: Automatisierung</h3>
              <p style={{ color: 'white' }}>KI-Tools implementieren und Prozesse automatisieren</p>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.4s', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>🚀</div>
              <h3 className="mb-sm" style={{ color: 'white' }}>Phase 3: Skalierung</h3>
              <p style={{ color: 'white' }}>Erste Kunden gewinnen und Systeme optimieren</p>
            </div>
            <div className="card text-center animate-fade-in-up" style={{ animationDelay: '0.6s', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
              <div className="mb-md" style={{ fontSize: '3rem' }}>💰</div>
              <h3 className="mb-sm" style={{ color: 'white' }}>Phase 4: Passiv</h3>
              <p style={{ color: 'white' }}>Passives Einkommen generieren und Business erweitern</p>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section id="success" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: 'white' }}>Echte Erfolge von Digital Entrepreneurs</h2>
            <p style={{ color: '#10b981' }}>Sieh dir an, wie andere es geschafft haben</p>
          </div>
          <div className="grid grid-2">
            <div className="card animate-fade-in-up" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#10b981', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  AM
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: 'white' }}>Alex M.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#10b981' }}>
                    29 Jahre, Digital Entrepreneur
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: 'white' }}>
                "Mit KI-gestützter Automatisierung habe ich mein Dropshipping-Business 
                auf 15.000€ monatlich skaliert!"
              </p>
              <div style={{ color: '#3b82f6', fontWeight: '600' }}>
                Verdienst: 15.000€/Monat
              </div>
            </div>
            <div className="card animate-fade-in-up" style={{ animationDelay: '0.2s', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <div className="flex items-center mb-md">
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600', marginRight: 'var(--space-md)' }}>
                  SJ
                </div>
                <div>
                  <h4 className="mb-0" style={{ color: 'white' }}>Sarah J.</h4>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#3b82f6' }}>
                    31 Jahre, SaaS-Gründerin
                  </p>
                </div>
              </div>
              <p className="mb-md" style={{ color: 'white' }}>
                "Mein SaaS-Tool läuft komplett automatisiert. Ich verdiene 25.000€ 
                passiv im Monat!"
              </p>
              <div style={{ color: '#f59e0b', fontWeight: '600' }}>
                Verdienst: 25.000€/Monat
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981' }}>
            <h2 className="mb-md" style={{ color: 'white' }}>Bereit für die Business-Revolution?</h2>
            <p className="mb-lg" style={{ color: 'white' }}>
              Starte noch heute und baue dir ein automatisiertes Business auf
            </p>
            <div className="mb-lg">
              <div className="flex justify-center gap-sm mb-sm">
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#10b981' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#10b981' }}></div>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#10b981' }}></div>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#10b981' }}>
                Kostenlose Business-Analyse + Automatisierungsplan
              </p>
            </div>
            <div className="flex justify-center gap-md">
              <button className="btn" style={{ background: 'linear-gradient(135deg, #10b981, #3b82f6)', color: 'white' }}>
                Jetzt kostenlos analysieren
              </button>
              <button className="btn btn-outline" style={{ color: '#f59e0b', borderColor: '#f59e0b' }}>
                Webinar ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(0,0,0,0.5)', color: 'white' }}>
        <div className="container">
          <div className="grid grid-4">
            <div>
              <h4 className="mb-md">Remote Cashflow</h4>
              <p style={{ fontSize: '0.875rem' }}>
                Der moderne Weg zum passiven Einkommen
              </p>
            </div>
            <div>
              <h5 className="mb-sm">Methoden</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>KI-Automatisierung</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Dropshipping</a></li>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Affiliate Marketing</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-sm">Ressourcen</h5>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.875rem' }}>
                <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Business-Analyse</a></li>
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
              © 2025 Remote Cashflow. Ein Produkt von Flowtelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default RemoteCashflow; 