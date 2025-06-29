import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/ci-system.css';

const Personas: React.FC = () => {
  const personas = [
    {
      id: 'starter-kapital',
      name: 'Starter-Kapital',
      target: 'Studenten & Berufsanfänger (18-25)',
      description: 'Digital-nativ, energetisch, Fokus auf Side-Hustle und Skills',
      colors: ['#10b981', '#059669', '#047857'],
      emoji: '🚀',
      monthlyGoal: '1500€',
      timeInvestment: '1-2h/Tag',
      path: '/starter-kapital'
    },
    {
      id: 'eltern-einkommen',
      name: 'Eltern-Einkommen',
      target: 'Eltern in Elternzeit (25-40)',
      description: 'Warm, empathisch, Fokus auf flexible Jobs und Kinderbetreuung',
      colors: ['#f59e0b', '#f97316', '#ea580c'],
      emoji: '👨‍👩‍👧‍👦',
      monthlyGoal: '2000€',
      timeInvestment: '2-3h/Tag',
      path: '/eltern-einkommen'
    },
    {
      id: 'projekt-profit',
      name: 'Projekt-Profit',
      target: 'Freelancer (25-45)',
      description: 'Professionell, wachstumsorientiert, Fokus auf Skalierung',
      colors: ['#3b82f6', '#1d4ed8', '#1e40af'],
      emoji: '💼',
      monthlyGoal: '8000€',
      timeInvestment: '20-30h/Woche',
      path: '/projekt-profit'
    },
    {
      id: 'renten-rendite',
      name: 'Renten-Rendite',
      target: 'Best Ager (50+)',
      description: 'Seriös, vertrauensvoll, Fokus auf sichere Anlagen',
      colors: ['#0ea5e9', '#0369a1', '#075985'],
      emoji: '💰',
      monthlyGoal: '3000€',
      timeInvestment: 'Flexibel',
      path: '/renten-rendite'
    },
    {
      id: 'feierabend-kapital',
      name: 'Feierabend-Kapital',
      target: 'Unzufriedene Angestellte (28-45)',
      description: 'Hoffnungsvoll, realistisch, Fokus auf Nebenjobs',
      colors: ['#a855f7', '#7c3aed', '#6d28d9'],
      emoji: '🌅',
      monthlyGoal: '4000€',
      timeInvestment: '2-3h/Tag',
      path: '/feierabend-kapital'
    },
    {
      id: 'remote-cashflow',
      name: 'Remote Cashflow',
      target: 'Hippe Business-KI-Typ (25-35)',
      description: 'Modern, cool, Fokus auf KI-Automatisierung',
      colors: ['#10b981', '#3b82f6', '#f59e0b'],
      emoji: '🤖',
      monthlyGoal: '5000€',
      timeInvestment: '2-3h/Woche',
      path: '/remote-cashflow'
    }
  ];

  return (
    <div className="personas-page" style={{ backgroundColor: '#f8fafc', color: '#1e293b' }}>
      {/* Navigation */}
      <nav className="nav container">
        <Link to="/" className="logo" style={{ color: '#3b82f6' }}>
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)' }}>D</div>
          Digitaler Kompass
        </Link>
        <ul className="nav-links">
          <li><a href="#overview" className="nav-link" style={{ color: '#1e293b' }}>Übersicht</a></li>
          <li><a href="#personas" className="nav-link" style={{ color: '#1e293b' }}>Personas</a></li>
          <li><a href="#strategy" className="nav-link" style={{ color: '#1e293b' }}>Strategie</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section id="overview" className="hero" style={{ backgroundColor: '#f8fafc', backgroundImage: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)' }}>
        <div className="container">
          <div className="hero-content animate-fade-in-up">
            <div className="text-center mb-lg">
              <h1 className="mb-md" style={{ color: '#1e293b' }}>
                Ihr Wegweiser zur finanziellen Freiheit
              </h1>
              <p className="mb-xl" style={{ fontSize: '1.25rem', color: '#3b82f6' }}>
                Entdecken Sie Ihre personalisierte Strategie - unabhängig von Ihrer Lebenssituation
              </p>
              <div className="mb-xl">
                <div className="flex justify-center gap-md mb-md">
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#3b82f6' }}>
                      6
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#1e293b' }}>
                      Personas
                    </div>
                  </div>
                  <div className="card" style={{ padding: 'var(--space-md)', minWidth: '120px', backgroundColor: 'rgba(29, 78, 216, 0.1)', border: '1px solid #1d4ed8' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '700', color: '#1d4ed8' }}>
                      100%
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#1e293b' }}>
                      Abgedeckt
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Personas Grid */}
      <section id="personas" className="section">
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Unsere Personas</h2>
            <p style={{ fontSize: '1.25rem', color: '#3b82f6' }}>
              Klicke auf eine Persona, um ihre Landingpage zu besuchen
            </p>
          </div>
          
          <div className="grid grid-3 gap-lg">
            {personas.map((persona, index) => (
              <Link 
                key={persona.id} 
                to={persona.path}
                className="card animate-fade-in-up" 
                style={{ 
                  backgroundColor: 'white',
                  border: `2px solid ${persona.colors[0]}`,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  textDecoration: 'none',
                  animationDelay: `${index * 0.1}s`
                }}
              >
                <div className="text-center mb-md">
                  <div style={{ fontSize: '4rem', marginBottom: 'var(--space-sm)' }}>
                    {persona.emoji}
                  </div>
                  <h3 className="mb-sm" style={{ color: persona.colors[0] }}>
                    {persona.name}
                  </h3>
                  <p style={{ color: '#64748b', fontSize: '0.875rem', fontWeight: '600' }}>
                    {persona.target}
                  </p>
                </div>
                
                <div className="mb-md">
                  <p style={{ color: '#374151', fontSize: '0.875rem' }}>
                    {persona.description}
                  </p>
                </div>
                
                <div className="grid grid-2 gap-sm mb-md">
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.25rem', fontWeight: '700', color: persona.colors[0] }}>
                      {persona.monthlyGoal}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                      Ziel
                    </div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.25rem', fontWeight: '700', color: persona.colors[1] }}>
                      {persona.timeInvestment}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                      Zeitaufwand
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-1 justify-center">
                  {persona.colors.map((color, colorIndex) => (
                    <div 
                      key={colorIndex}
                      style={{ 
                        width: '20px', 
                        height: '20px', 
                        borderRadius: '50%', 
                        backgroundColor: color 
                      }}
                    />
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Strategy Section */}
      <section id="strategy" className="section" style={{ backgroundColor: 'rgba(59, 130, 246, 0.05)' }}>
        <div className="container">
          <div className="text-center mb-xl">
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Die Markenstrategie</h2>
            <p style={{ fontSize: '1.25rem', color: '#3b82f6' }}>
              Jede Persona hat ihre eigene Identität und Ansprache
            </p>
          </div>
          
          <div className="grid grid-2 gap-lg">
            <div className="card" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
              <h3 className="mb-md" style={{ color: '#1e293b' }}>Dachmarke: Flowtelligence</h3>
              <p style={{ color: '#374151' }}>
                Die übergeordnete Marke, die alle Personas verbindet. Steht für intelligente 
                Finanzlösungen und persönliche Entwicklung.
              </p>
              <div className="mt-md">
                <div style={{ color: '#3b82f6', fontWeight: '600' }}>
                  Farben: Blau, Grün, Weiß
                </div>
                <div style={{ color: '#3b82f6', fontWeight: '600' }}>
                  Positionierung: Der intelligente Weg zum Erfolg
                </div>
              </div>
            </div>
            
            <div className="card" style={{ backgroundColor: 'rgba(29, 78, 216, 0.1)', border: '1px solid #1d4ed8' }}>
              <h3 className="mb-md" style={{ color: '#1e293b' }}>Persona-Marken</h3>
              <p style={{ color: '#374151' }}>
                Jede Persona hat ihre eigene Marke mit eigenem Design, Farben und 
                Ansprache. Das schafft Vertrauen und Identifikation.
              </p>
              <div className="mt-md">
                <div style={{ color: '#1d4ed8', fontWeight: '600' }}>
                  Individuelle Farbpaletten
                </div>
                <div style={{ color: '#1d4ed8', fontWeight: '600' }}>
                  Persona-spezifische Content-Strategien
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container-sm">
          <div className="card text-center" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6' }}>
            <h2 className="mb-md" style={{ color: '#1e293b' }}>Welche Persona interessiert dich?</h2>
            <p className="mb-lg" style={{ color: '#374151' }}>
              Besuche die Landingpages und sieh dir die verschiedenen Ansätze an
            </p>
            <div className="flex justify-center gap-md flex-wrap">
              {personas.slice(0, 3).map((persona) => (
                <Link 
                  key={persona.id}
                  to={persona.path}
                  className="btn" 
                  style={{ 
                    background: `linear-gradient(135deg, ${persona.colors[0]}, ${persona.colors[1]})`, 
                    color: 'white',
                    textDecoration: 'none'
                  }}
                >
                  {persona.name}
                </Link>
              ))}
            </div>
            <div className="flex justify-center gap-md flex-wrap mt-md">
              {personas.slice(3).map((persona) => (
                <Link 
                  key={persona.id}
                  to={persona.path}
                  className="btn btn-outline" 
                  style={{ 
                    color: persona.colors[0], 
                    borderColor: persona.colors[0],
                    textDecoration: 'none'
                  }}
                >
                  {persona.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-sm" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#1e293b' }}>
        <div className="container">
          <div className="text-center">
            <h4 className="mb-md">Flowtelligence</h4>
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
              Intelligente Finanzlösungen für jede Lebensphase
            </p>
            <div className="mt-lg" style={{ borderTop: '1px solid rgba(59, 130, 246, 0.3)', paddingTop: 'var(--space-lg)' }}>
              <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
                © 2025 Flowtelligence. Alle Rechte vorbehalten.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Personas; 