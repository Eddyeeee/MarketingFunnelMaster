import { storage } from '../storage';

export interface VSLSection {
  id: string;
  title: string;
  content: string;
  type: 'hook' | 'problem' | 'solution' | 'proof' | 'offer' | 'urgency' | 'guarantee';
  personaSpecific: boolean;
  variants?: {
    [personaType: string]: string;
  };
}

export interface VSLConfig {
  personaType: string;
  sections: VSLSection[];
  pricing: {
    basePrice: number;
    discountPrice: number;
    currency: string;
    paymentPlans: {
      monthly: number;
      yearly: number;
    };
  };
  bonuses: string[];
  guarantees: string[];
  urgencyElements: {
    countdown: boolean;
    limitedSpots: boolean;
    expiringOffer: boolean;
  };
}

export class VSLService {
  private vslConfigs: { [personaType: string]: VSLConfig } = {
    student: {
      personaType: 'student',
      sections: [
        {
          id: 'hook',
          title: '🎓 Studenten, die 500€+ im Monat verdienen - während sie studieren!',
          content: 'Entdecke, wie Studenten wie du bereits 500-800€ monatlich verdienen, ohne ihren Studienalltag zu opfern. Die Zeit zwischen Vorlesungen wird zu deinem Vorteil!',
          type: 'hook',
          personaSpecific: true,
          variants: {
            student: '🎓 Studenten, die 500€+ im Monat verdienen - während sie studieren!',
            employee: '💼 Angestellte, die 2.000€+ Zusatzeinkommen generieren!',
            parent: '👨‍👩‍👧‍👦 Eltern, die flexibles Einkommen neben der Familie aufbauen!'
          }
        },
        {
          id: 'problem',
          title: 'Das Studenten-Dilemma: Zeit vs. Geld',
          content: 'Als Student hast du zwei Probleme: Du brauchst Geld, aber du hast keine Zeit für einen traditionellen Nebenjob. Die meisten Studenten-Jobs zahlen schlecht und rauben dir wertvolle Studienzeit.',
          type: 'problem',
          personaSpecific: true
        },
        {
          id: 'solution',
          title: 'Magic Tool System: Der Studenten-Weg zu 500€+',
          content: 'Das Magic Tool System wurde speziell für Studenten entwickelt. Du investierst nur 30 Minuten täglich und baust ein automatisiertes Online-Business auf, das auch ohne dich läuft.',
          type: 'solution',
          personaSpecific: true
        },
        {
          id: 'proof',
          title: 'Studenten-Erfolgsgeschichten',
          content: 'Sarah, 22, Studentin: "Ich verdiene jetzt 650€ monatlich und kann mir mein Studium selbst finanzieren. Das Beste: Ich arbeite nur 30 Minuten täglich!"',
          type: 'proof',
          personaSpecific: true
        },
        {
          id: 'offer',
          title: 'Dein Studenten-Paket: Alles für 500€+ im ersten Monat',
          content: 'Du erhältst: 30-Tage-Studenten-Plan, Social Media Templates, Kunden-Akquise-Strategien, Community-Zugang, 1:1 Support',
          type: 'offer',
          personaSpecific: true
        }
      ],
      pricing: {
        basePrice: 997,
        discountPrice: 497,
        currency: 'EUR',
        paymentPlans: {
          monthly: 497,
          yearly: 397
        }
      },
      bonuses: [
        '🎓 Studenten-Bonus: Social Media Templates (Wert: 197€)',
        '📱 Mobile-First Strategien (Wert: 147€)',
        '👥 Studenten-Community Zugang (Wert: 97€)',
        '⏰ 30-Minuten-Routine-Guide (Wert: 77€)'
      ],
      guarantees: [
        '✅ 30 Tage Geld-zurück-Garantie',
        '✅ Erste 100€ in 14 Tagen oder Geld zurück',
        '✅ Persönlicher Studenten-Support'
      ],
      urgencyElements: {
        countdown: true,
        limitedSpots: true,
        expiringOffer: true
      }
    },
    employee: {
      personaType: 'employee',
      sections: [
        {
          id: 'hook',
          title: '💼 Angestellte, die 2.000€+ Zusatzeinkommen generieren!',
          content: 'Entdecke, wie Vollzeit-Angestellte wie du bereits 2.000-5.000€ monatlich zusätzlich verdienen, ohne ihren sicheren Job zu riskieren.',
          type: 'hook',
          personaSpecific: true
        },
        {
          id: 'problem',
          title: 'Das Angestellten-Problem: Sicherheit vs. Wachstum',
          content: 'Du hast einen sicheren Job, aber du siehst keine Möglichkeit für signifikantes Einkommenswachstum. Beförderungen sind selten und Gehaltserhöhungen minimal.',
          type: 'problem',
          personaSpecific: true
        },
        {
          id: 'solution',
          title: 'Magic Tool System: Skalierung für Angestellte',
          content: 'Das Magic Tool System nutzt deine Business-Erfahrung und zeigt dir, wie du automatisierte Einkommensströme aufbaust, die parallel zu deinem Job laufen.',
          type: 'solution',
          personaSpecific: true
        },
        {
          id: 'proof',
          title: 'Angestellten-Erfolgsgeschichten',
          content: 'Michael, 32, Projektmanager: "Ich verdiene jetzt 3.200€ zusätzlich monatlich. Das System läuft automatisch und ich investiere nur 1 Stunde täglich."',
          type: 'proof',
          personaSpecific: true
        },
        {
          id: 'offer',
          title: 'Dein Angestellten-Paket: Skalierung auf 5.000€+',
          content: 'Du erhältst: 90-Tage-Skalierungsplan, Automatisierungs-Tools, High-Ticket-Strategien, VIP-Community, Business-Coaching',
          type: 'offer',
          personaSpecific: true
        }
      ],
      pricing: {
        basePrice: 1997,
        discountPrice: 997,
        currency: 'EUR',
        paymentPlans: {
          monthly: 997,
          yearly: 797
        }
      },
      bonuses: [
        '💼 Business-Automatisierung Toolkit (Wert: 397€)',
        '📈 Skalierungs-Strategien (Wert: 297€)',
        '🤖 AI-Tools für Automatisierung (Wert: 197€)',
        '👑 VIP-Community Zugang (Wert: 147€)'
      ],
      guarantees: [
        '✅ 30 Tage Geld-zurück-Garantie',
        '✅ Erste 1.000€ in 30 Tagen oder Geld zurück',
        '✅ Persönliches Business-Coaching'
      ],
      urgencyElements: {
        countdown: true,
        limitedSpots: true,
        expiringOffer: true
      }
    },
    parent: {
      personaType: 'parent',
      sections: [
        {
          id: 'hook',
          title: '👨‍👩‍👧‍👦 Eltern, die flexibles Einkommen neben der Familie aufbauen!',
          content: 'Entdecke, wie Eltern wie du bereits 800-1.200€ monatlich verdienen, ohne die Familie zu vernachlässigen. Flexible Arbeitszeiten, die zu deinem Leben passen.',
          type: 'hook',
          personaSpecific: true
        },
        {
          id: 'problem',
          title: 'Das Eltern-Problem: Familie vs. Einkommen',
          content: 'Du möchtest für deine Familie da sein, aber du brauchst auch ein Einkommen. Traditionelle Jobs sind zu unflexibel und nehmen dir wertvolle Familienzeit.',
          type: 'problem',
          personaSpecific: true
        },
        {
          id: 'solution',
          title: 'Magic Tool System: Familienfreundliches Business',
          content: 'Das Magic Tool System wurde für Eltern entwickelt. Du arbeitest, wann es dir passt: morgens vor der Familie, abends oder am Wochenende.',
          type: 'solution',
          personaSpecific: true
        },
        {
          id: 'proof',
          title: 'Eltern-Erfolgsgeschichten',
          content: 'Maria, 35, Mutter von 2 Kindern: "Ich verdiene jetzt 950€ monatlich und kann immer für meine Kinder da sein. Das Beste: Ich arbeite nur, wenn es mir passt!"',
          type: 'proof',
          personaSpecific: true
        },
        {
          id: 'offer',
          title: 'Dein Eltern-Paket: Flexibles Einkommen für die Familie',
          content: 'Du erhältst: Familienfreundlicher Zeitplan, Flexible Arbeitsstrategien, Kinder-freundliche Tools, Eltern-Community, Familien-Coaching',
          type: 'offer',
          personaSpecific: true
        }
      ],
      pricing: {
        basePrice: 1497,
        discountPrice: 747,
        currency: 'EUR',
        paymentPlans: {
          monthly: 747,
          yearly: 597
        }
      },
      bonuses: [
        '👨‍👩‍👧‍👦 Familienfreundlicher Zeitplan (Wert: 247€)',
        '📅 Flexible Arbeitsstrategien (Wert: 197€)',
        '🧸 Kinder-freundliche Tools (Wert: 147€)',
        '👥 Eltern-Community (Wert: 97€)'
      ],
      guarantees: [
        '✅ 30 Tage Geld-zurück-Garantie',
        '✅ Erste 500€ in 45 Tagen oder Geld zurück',
        '✅ Familien-Coaching'
      ],
      urgencyElements: {
        countdown: true,
        limitedSpots: true,
        expiringOffer: true
      }
    }
  };

  async generateVSL(personaType: string, leadData?: any): Promise<VSLConfig> {
    const config = this.vslConfigs[personaType] || this.vslConfigs['student'];
    
    // Personalisiere VSL basierend auf Lead-Daten
    if (leadData) {
      config.sections = config.sections.map(section => ({
        ...section,
        content: this.personalizeContent(section.content, leadData, personaType)
      }));
    }

    // Dynamische Preisanpassung basierend auf Persona
    config.pricing = this.calculateDynamicPricing(personaType, leadData);

    return config;
  }

  private personalizeContent(content: string, leadData: any, personaType: string): string {
    return content
      .replace(/{firstName}/g, leadData?.firstName || 'Lieber Interessent')
      .replace(/{personaType}/g, personaType)
      .replace(/{email}/g, leadData?.email || '')
      .replace(/{quizAnswers}/g, JSON.stringify(leadData?.quizAnswers || {}));
  }

  private calculateDynamicPricing(personaType: string, leadData?: any): any {
    const baseConfig = this.vslConfigs[personaType] || this.vslConfigs['student'];
    
    // Dynamische Preisanpassung basierend auf verschiedenen Faktoren
    let priceMultiplier = 1.0;

    // Faktor 1: Quiz-Antworten (Ziele)
    if (leadData?.quizAnswers) {
      const goal = leadData.quizAnswers['3'];
      if (goal === 'freedom') {
        priceMultiplier *= 1.2; // 20% höher für Freiheits-Ziele
      } else if (goal === 'basic') {
        priceMultiplier *= 0.9; // 10% niedriger für Basis-Ziele
      }
    }

    // Faktor 2: Problem-Typ
    if (leadData?.quizAnswers) {
      const problem = leadData.quizAnswers['2'];
      if (problem === 'no_time') {
        priceMultiplier *= 1.1; // 10% höher für Zeit-Probleme
      }
    }

    // Faktor 3: Blocker
    if (leadData?.quizAnswers) {
      const blocker = leadData.quizAnswers['4'];
      if (blocker === 'no_capital') {
        priceMultiplier *= 0.95; // 5% niedriger für Kapital-Probleme
      }
    }

    return {
      basePrice: Math.round(baseConfig.pricing.basePrice * priceMultiplier),
      discountPrice: Math.round(baseConfig.pricing.discountPrice * priceMultiplier),
      currency: baseConfig.pricing.currency,
      paymentPlans: {
        monthly: Math.round(baseConfig.pricing.paymentPlans.monthly * priceMultiplier),
        yearly: Math.round(baseConfig.pricing.paymentPlans.yearly * priceMultiplier)
      }
    };
  }

  async getVSLStats(personaType: string): Promise<any> {
    // Hier würden normalerweise VSL-Statistiken aus der Datenbank geladen
    const baseStats = {
      views: 0,
      conversions: 0,
      revenue: 0,
      avgTimeOnPage: 0
    };

    // Simuliere Persona-spezifische Statistiken
    switch (personaType) {
      case 'student':
        return {
          ...baseStats,
          views: 1250,
          conversions: 187,
          revenue: 92839,
          avgTimeOnPage: 320,
          conversionRate: 15.0
        };
      case 'employee':
        return {
          ...baseStats,
          views: 890,
          conversions: 156,
          revenue: 155532,
          avgTimeOnPage: 420,
          conversionRate: 17.5
        };
      case 'parent':
        return {
          ...baseStats,
          views: 1100,
          conversions: 165,
          revenue: 123255,
          avgTimeOnPage: 380,
          conversionRate: 15.0
        };
      default:
        return baseStats;
    }
  }

  async trackVSLView(personaType: string, leadId?: number): Promise<void> {
    // Track VSL-View für Analytics
    await storage.createAnalyticsEvent({
      event: 'vsl_viewed',
      page: '/vsl',
      userId: leadId?.toString(),
      data: JSON.stringify({
        personaType,
        leadId,
        timestamp: new Date().toISOString()
      })
    });
  }

  async trackVSLConversion(personaType: string, leadId?: number, amount?: number): Promise<void> {
    // Track VSL-Conversion für Analytics
    await storage.createAnalyticsEvent({
      event: 'vsl_conversion',
      page: '/vsl',
      userId: leadId?.toString(),
      data: JSON.stringify({
        personaType,
        leadId,
        amount,
        timestamp: new Date().toISOString()
      })
    });
  }
}

export const vslService = new VSLService(); 