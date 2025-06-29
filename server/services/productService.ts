import fs from 'fs';
import path from 'path';

export interface ProductConfig {
  id: string;
  name: string;
  brand: string;
  domain: string;
  description: string;
  targetAudience: string;
  personas: string[];
  pricing: {
    basic: number;
    premium: number;
  };
  commission: number;
  digistoreIds: {
    basic: string;
    premium: string;
  };
  colors: {
    primary: string;
    secondary: string;
    accent: string;
  };
  content: {
    quizTitle: string;
    quizDescription: string;
    vslTitle: string;
    bridgeTitle: string;
  };
}

export interface GlobalConfig {
  defaultLanguage: string;
  supportedLanguages: string[];
  analytics: {
    googleAnalytics: boolean;
    facebookPixel: boolean;
    hotjar: boolean;
  };
  integrations: {
    digistore24: boolean;
    stripe: boolean;
    mailchimp: boolean;
    convertkit: boolean;
  };
}

export interface ProductConfigFile {
  products: Record<string, ProductConfig>;
  global: GlobalConfig;
}

export class ProductService {
  private config: ProductConfigFile;
  private currentProduct: string;

  constructor() {
    this.loadConfig();
    this.currentProduct = process.env.PRODUCT_ID || 'qmoney';
  }

  private loadConfig(): void {
    try {
      const configPath = path.join(process.cwd(), 'config', 'products.json');
      const configData = fs.readFileSync(configPath, 'utf8');
      this.config = JSON.parse(configData);
    } catch (error) {
      console.error('Fehler beim Laden der Produkt-Konfiguration:', error);
      // Fallback-Konfiguration
      this.config = {
        products: {},
        global: {
          defaultLanguage: 'de',
          supportedLanguages: ['de'],
          analytics: {
            googleAnalytics: true,
            facebookPixel: false,
            hotjar: false
          },
          integrations: {
            digistore24: true,
            stripe: true,
            mailchimp: false,
            convertkit: false
          }
        }
      };
    }
  }

  // Aktuelles Produkt abrufen
  getCurrentProduct(): ProductConfig {
    return this.config.products[this.currentProduct];
  }

  // Produkt nach ID abrufen
  getProduct(productId: string): ProductConfig | null {
    return this.config.products[productId] || null;
  }

  // Alle Produkte abrufen
  getAllProducts(): Record<string, ProductConfig> {
    return this.config.products;
  }

  // Global-Konfiguration abrufen
  getGlobalConfig(): GlobalConfig {
    return this.config.global;
  }

  // Produkt-spezifische Quiz-Fragen
  getQuizQuestions(productId: string): any[] {
    const product = this.getProduct(productId);
    if (!product) return [];

    // Basis-Quiz-Fragen für alle Produkte
    const baseQuestions = [
      {
        id: "1",
        question: "Was ist dein aktuelles Einkommen?",
        options: [
          {
            value: "low",
            label: "Unter 2.000€ monatlich",
            description: "Ich verdiene weniger als 2.000€"
          },
          {
            value: "medium",
            label: "2.000€ - 5.000€ monatlich",
            description: "Ich verdiene zwischen 2.000€ und 5.000€"
          },
          {
            value: "high",
            label: "Über 5.000€ monatlich",
            description: "Ich verdiene mehr als 5.000€"
          }
        ]
      },
      {
        id: "2",
        question: "Wie viel Zeit kannst du investieren?",
        options: [
          {
            value: "part_time",
            label: "Nebenbei (5-10 Stunden/Woche)",
            description: "Ich kann nebenbei arbeiten"
          },
          {
            value: "full_time",
            label: "Vollzeit (40+ Stunden/Woche)",
            description: "Ich kann vollzeit arbeiten"
          },
          {
            value: "flexible",
            label: "Flexibel (variabel)",
            description: "Meine Zeit ist flexibel"
          }
        ]
      }
    ];

    // Produkt-spezifische Fragen hinzufügen
    const productQuestions = this.getProductSpecificQuestions(productId);
    
    return [...baseQuestions, ...productQuestions];
  }

  private getProductSpecificQuestions(productId: string): any[] {
    switch (productId) {
      case 'qmoney':
        return [
          {
            id: "3",
            question: "Was ist dein größtes Hindernis?",
            options: [
              {
                value: "no_capital",
                label: "Kein Startkapital",
                description: "Ich habe kein Geld zum Investieren"
              },
              {
                value: "no_skills",
                label: "Keine Fähigkeiten",
                description: "Ich weiß nicht, was ich gut kann"
              },
              {
                value: "no_network",
                label: "Keine Kontakte",
                description: "Ich kenne niemanden in der Branche"
              }
            ]
          }
        ];

      case 'remotecash':
        return [
          {
            id: "3",
            question: "Was ist dein Remote-Ziel?",
            options: [
              {
                value: "location_freedom",
                label: "Ortsunabhängigkeit",
                description: "Ich will von überall arbeiten"
              },
              {
                value: "work_life_balance",
                label: "Work-Life-Balance",
                description: "Ich will mehr Zeit für mich"
              },
              {
                value: "higher_income",
                label: "Höheres Einkommen",
                description: "Ich will mehr verdienen"
              }
            ]
          }
        ];

      case 'cryptoflow':
        return [
          {
            id: "3",
            question: "Was ist deine Crypto-Erfahrung?",
            options: [
              {
                value: "beginner",
                label: "Anfänger",
                description: "Ich kenne mich noch nicht aus"
              },
              {
                value: "intermediate",
                label: "Fortgeschritten",
                description: "Ich habe schon Erfahrung"
              },
              {
                value: "expert",
                label: "Experte",
                description: "Ich bin sehr erfahren"
              }
            ]
          }
        ];

      case 'affiliatepro':
        return [
          {
            id: "3",
            question: "Was ist dein Content-Bereich?",
            options: [
              {
                value: "social_media",
                label: "Social Media",
                description: "Instagram, TikTok, YouTube"
              },
              {
                value: "blog",
                label: "Blog/Website",
                description: "Ich habe eine eigene Website"
              },
              {
                value: "email",
                label: "E-Mail-Marketing",
                description: "Ich nutze E-Mail-Listen"
              }
            ]
          }
        ];

      default:
        return [];
    }
  }

  // Produkt-spezifische Personas
  getPersonas(productId: string): any[] {
    const product = this.getProduct(productId);
    if (!product) return [];

    const personaMap: Record<string, any[]> = {
      qmoney: [
        {
          type: "money_tight",
          name: "Der Sparfüchse",
          profileText: "Du bist der Sparfüchse - du weißt, wie man mit wenig Geld viel erreicht.",
          strategyText: "Deine Strategie: Mikro-Business aufbauen mit minimalem Investment.",
          actionPlan: {
            expectedResults: "500-1.500€ monatlich",
            timeline: "3-6 Monate",
            strategy: "Niedrigschwellige Online-Geschäfte"
          }
        },
        {
          type: "no_time",
          name: "Der Zeitmanager",
          profileText: "Du bist der Zeitmanager - du optimierst jede Minute für maximalen Output.",
          strategyText: "Deine Strategie: Automatisierte Systeme für passives Einkommen.",
          actionPlan: {
            expectedResults: "1.000-3.000€ monatlich",
            timeline: "6-12 Monate",
            strategy: "Automatisierte Online-Systeme"
          }
        },
        {
          type: "no_idea",
          name: "Der Entdecker",
          profileText: "Du bist der Entdecker - du findest immer neue Möglichkeiten.",
          strategyText: "Deine Strategie: Verschiedene Einkommensquellen testen und skalieren.",
          actionPlan: {
            expectedResults: "2.000-5.000€ monatlich",
            timeline: "12-18 Monate",
            strategy: "Multiple Einkommensströme"
          }
        }
      ],
      remotecash: [
        {
          type: "remote_worker",
          name: "Der Remote Worker",
          profileText: "Du bist der Remote Worker - du arbeitest bereits von zu Hause.",
          strategyText: "Deine Strategie: Bestehende Fähigkeiten zu höheren Sätzen vermarkten.",
          actionPlan: {
            expectedResults: "3.000-8.000€ monatlich",
            timeline: "3-6 Monate",
            strategy: "Freelancing & Consulting"
          }
        },
        {
          type: "digital_nomad",
          name: "Der Digital Nomad",
          profileText: "Du bist der Digital Nomad - du willst von überall arbeiten.",
          strategyText: "Deine Strategie: Ortsunabhängige Online-Business aufbauen.",
          actionPlan: {
            expectedResults: "5.000-15.000€ monatlich",
            timeline: "6-12 Monate",
            strategy: "Online-Business & Automatisierung"
          }
        },
        {
          type: "location_freedom",
          name: "Der Freiheitsliebende",
          profileText: "Du bist der Freiheitsliebende - du willst maximale Flexibilität.",
          strategyText: "Deine Strategie: Passive Einkommensströme für echte Freiheit.",
          actionPlan: {
            expectedResults: "10.000€+ monatlich",
            timeline: "12-24 Monate",
            strategy: "Skalierbare Online-Systeme"
          }
        }
      ]
    };

    return personaMap[productId] || [];
  }

  // Produkt-spezifische Upsell-Konfiguration
  getUpsellConfig(productId: string): any {
    const product = this.getProduct(productId);
    if (!product) return null;

    return {
      basic: {
        id: `${productId}_basic`,
        name: `${product.name} Basic`,
        description: product.description,
        price: product.pricing.basic,
        digistoreId: product.digistoreIds.basic,
        commission: product.commission
      },
      premium: {
        id: `${productId}_premium`,
        name: `${product.name} Premium`,
        description: `Erweiterte ${product.name} Strategien`,
        price: product.pricing.premium,
        digistoreId: product.digistoreIds.premium,
        commission: product.commission
      }
    };
  }

  // Produkt-spezifische Farben für CSS
  getProductColors(productId: string): string {
    const product = this.getProduct(productId);
    if (!product) return '';

    return `
      :root {
        --product-primary: ${product.colors.primary};
        --product-secondary: ${product.colors.secondary};
        --product-accent: ${product.colors.accent};
      }
    `;
  }

  // Produkt-spezifische Meta-Tags
  getProductMeta(productId: string): any {
    const product = this.getProduct(productId);
    if (!product) return {};

    return {
      title: product.content.quizTitle,
      description: product.content.quizDescription,
      keywords: `${product.name}, ${product.targetAudience}, online geld verdienen`,
      ogTitle: product.content.quizTitle,
      ogDescription: product.content.quizDescription,
      ogImage: `/images/${productId}/og-image.jpg`
    };
  }
}

export const productService = new ProductService(); 