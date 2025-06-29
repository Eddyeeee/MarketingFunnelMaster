#!/usr/bin/env node

import dns from 'dns';
import { promisify } from 'util';

const resolve4 = promisify(dns.resolve4);

// Erweiterte Nischen-Analyse basierend auf persönlichen Interessen
const extendedNiches = {
  // KI & Coding (Ihre Hauptinteressen)
  kiCoding: {
    name: "KI & Coding",
    subniches: {
      multiAIWorkflow: {
        name: "Multi-AI Workflow & Automatisierung",
        commission: "25-50%",
        avgOrderValue: 200,
        conversionRate: "5-12%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["GitHub Copilot", "Cursor AI", "Replit", "CodeWhisperer"],
        keywords: ["multi-ai", "workflow", "coding", "automation", "developer"],
        painPoints: ["Zeitmangel", "Komplexität", "Lernkurve"],
        targetAudience: "Entwickler, 20-40, Tech-affin",
        seasonality: "ganzjährig",
        trend: "explosiv steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      codingCourses: {
        name: "Coding-Kurse & Bootcamps",
        commission: "30-60%",
        avgOrderValue: 500,
        conversionRate: "3-8%",
        competition: "mittel",
        difficulty: "mittel",
        programs: ["Udemy", "Coursera", "Codecademy", "freeCodeCamp"],
        keywords: ["coding", "programmierung", "kurs", "bootcamp", "lernen"],
        painPoints: ["Karrierewechsel", "Skills-Upgrade", "Zeitmangel"],
        targetAudience: "Berufswechsler, Studenten, 18-35",
        seasonality: "Jan-März, Sep-Nov",
        trend: "steigend",
        googleTrends: "stabil",
        personalInterest: "hoch"
      },
      appleDev: {
        name: "Apple Development & iOS",
        commission: "20-40%",
        avgOrderValue: 300,
        conversionRate: "4-10%",
        competition: "mittel",
        difficulty: "mittel",
        programs: ["Apple Developer", "MacStories", "iOS-Apps"],
        keywords: ["apple", "ios", "swift", "mac", "development"],
        painPoints: ["App Store", "Entwicklungskosten", "Zulassung"],
        targetAudience: "iOS-Entwickler, Apple-Fans, 25-45",
        seasonality: "ganzjährig",
        trend: "stabil",
        googleTrends: "stabil",
        personalInterest: "hoch"
      }
    }
  },

  // Tanzen & Sport (Ihre Hobbys)
  tanzenSport: {
    name: "Tanzen & Sport",
    subniches: {
      tanzen: {
        name: "Tanzen & Dance Moves",
        commission: "15-35%",
        avgOrderValue: 150,
        conversionRate: "4-10%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["Amazon", "Dance-Studios", "Online-Kurse"],
        keywords: ["tanzen", "dance", "moves", "choreografie", "tutorial"],
        painPoints: ["Koordination", "Rhythmus", "Selbstvertrauen"],
        targetAudience: "Tänzer, Fitness-Interessierte, 15-40",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      nikeSneakers: {
        name: "Nike Sneakers & Sportswear",
        commission: "5-15%",
        avgOrderValue: 120,
        conversionRate: "3-8%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Nike Affiliate", "Amazon", "Sportartikel"],
        keywords: ["nike", "sneakers", "schuhe", "sport", "fashion"],
        painPoints: ["Styling", "Komfort", "Trends"],
        targetAudience: "Sneaker-Collector, Sportler, 15-35",
        seasonality: "ganzjährig",
        trend: "stabil",
        googleTrends: "stabil",
        personalInterest: "hoch"
      },
      fitnessWorkout: {
        name: "Fitness & Workout",
        commission: "10-30%",
        avgOrderValue: 200,
        conversionRate: "3-7%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Myprotein", "Amazon", "Fitness-Programme"],
        keywords: ["fitness", "workout", "training", "muskeln", "abnehmen"],
        painPoints: ["Motivation", "Zeitmangel", "Wissen"],
        targetAudience: "Fitness-Interessierte, 20-50",
        seasonality: "Jan-März, Sep-Nov",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "mittel"
      }
    }
  },

  // Business & Finanzen (Ihre Interessen)
  businessFinance: {
    name: "Business & Finanzen",
    subniches: {
      businessCoaching: {
        name: "Business Coaching & Kurse",
        commission: "40-70%",
        avgOrderValue: 500,
        conversionRate: "2-6%",
        competition: "mittel",
        difficulty: "mittel",
        programs: ["Clickbank", "Jvzoo", "Digistore24"],
        keywords: ["business", "coaching", "kurs", "unternehmer", "erfolg"],
        painPoints: ["Geschäftserfolg", "Zeitmanagement", "Strategie"],
        targetAudience: "Unternehmer, Selbstständige, 25-55",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      steuern: {
        name: "Steuern & Buchhaltung",
        commission: "10-25%",
        avgOrderValue: 300,
        conversionRate: "2-5%",
        competition: "hoch",
        difficulty: "hoch",
        programs: ["Steuer-Software", "Buchhaltungs-Tools"],
        keywords: ["steuern", "buchhaltung", "finanzen", "software"],
        painPoints: ["Komplexität", "Zeitmangel", "Angst vor Fehlern"],
        targetAudience: "Unternehmer, Freelancer, 25-60",
        seasonality: "Jan-Apr, Nov-Dez",
        trend: "stabil",
        googleTrends: "saisonal",
        personalInterest: "mittel"
      },
      cryptoLight: {
        name: "Crypto & Blockchain (Light)",
        commission: "5-20%",
        avgOrderValue: 100,
        conversionRate: "3-8%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Binance", "Coinbase", "Crypto-Exchanges"],
        keywords: ["crypto", "bitcoin", "blockchain", "trading", "investment"],
        painPoints: ["Risiko", "Komplexität", "Volatilität"],
        targetAudience: "Crypto-Interessierte, 20-45",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "volatil",
        personalInterest: "mittel"
      }
    }
  },

  // Biohacking & Gesundheit
  biohacking: {
    name: "Biohacking & Gesundheit",
    subniches: {
      nootropics: {
        name: "Nootropics & Gehirnoptimierung",
        commission: "15-30%",
        avgOrderValue: 150,
        conversionRate: "4-10%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["iHerb", "Amazon", "Mind Lab Pro"],
        keywords: ["nootropics", "gehirn", "fokus", "leistung", "optimierung"],
        painPoints: ["Konzentration", "Stress", "Müdigkeit"],
        targetAudience: "Biohacker, Studenten, 20-45",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      sleepOptimization: {
        name: "Schlaf & Regeneration",
        commission: "15-35%",
        avgOrderValue: 100,
        conversionRate: "5-12%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["Amazon", "Sleep-Programme", "Supplements"],
        keywords: ["schlaf", "regeneration", "erholung", "müdigkeit"],
        painPoints: ["Schlafmangel", "Stress", "Müdigkeit"],
        targetAudience: "Gestresste, 25-55",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      fitnessBiohacking: {
        name: "Fitness Biohacking",
        commission: "10-25%",
        avgOrderValue: 200,
        conversionRate: "3-7%",
        competition: "mittel",
        difficulty: "mittel",
        programs: ["Myprotein", "Amazon", "Fitness-Programme"],
        keywords: ["biohacking", "fitness", "leistung", "optimierung"],
        painPoints: ["Zeitmangel", "Motivation", "Wissen"],
        targetAudience: "Fitness-Interessierte, 20-50",
        seasonality: "Jan-März, Sep-Nov",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      }
    }
  },

  // Digitale Produkte & Kurse
  digitalProducts: {
    name: "Digitale Produkte & Kurse",
    subniches: {
      onlineKurse: {
        name: "Online-Kurse & E-Learning",
        commission: "30-70%",
        avgOrderValue: 200,
        conversionRate: "3-10%",
        competition: "mittel",
        difficulty: "niedrig",
        programs: ["Udemy", "Coursera", "Skillshare", "Teachable"],
        keywords: ["online-kurs", "e-learning", "lernen", "skill"],
        painPoints: ["Zeitmangel", "Kosten", "Motivation"],
        targetAudience: "Lernende, 18-50",
        seasonality: "Jan-März, Sep-Nov",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      softwareTools: {
        name: "Software & Tools",
        commission: "20-40%",
        avgOrderValue: 100,
        conversionRate: "5-15%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["Software-Affiliate", "SaaS", "Digital Products"],
        keywords: ["software", "tools", "produktivität", "automatisierung"],
        painPoints: ["Zeitmangel", "Komplexität", "Kosten"],
        targetAudience: "Professionals, 25-45",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      },
      coachingProgramme: {
        name: "Coaching & Mentoring",
        commission: "40-80%",
        avgOrderValue: 1000,
        conversionRate: "1-5%",
        competition: "mittel",
        difficulty: "hoch",
        programs: ["Clickbank", "Jvzoo", "Digistore24"],
        keywords: ["coaching", "mentoring", "beratung", "entwicklung"],
        painPoints: ["Entwicklung", "Ziele", "Blockaden"],
        targetAudience: "Entwicklungsorientierte, 25-55",
        seasonality: "ganzjährig",
        trend: "steigend",
        googleTrends: "steigend",
        personalInterest: "hoch"
      }
    }
  }
};

// Erweiterte KPI-Berechnung mit persönlichen Interessen
function calculateExtendedNicheScore(niche) {
  const scores = {
    commission: parseFloat(niche.commission.split('-')[1]) / 100,
    avgOrderValue: niche.avgOrderValue / 1000,
    conversionRate: parseFloat(niche.conversionRate.split('-')[1]) / 100,
    competition: getCompetitionScore(niche.competition),
    difficulty: getDifficultyScore(niche.difficulty),
    trend: getTrendScore(niche.trend),
    googleTrends: getGoogleTrendsScore(niche.googleTrends),
    personalInterest: getPersonalInterestScore(niche.personalInterest)
  };

  // Gewichtete Bewertung mit persönlichen Interessen
  const weights = {
    commission: 0.15,
    avgOrderValue: 0.10,
    conversionRate: 0.15,
    competition: 0.10,
    difficulty: 0.10,
    trend: 0.15,
    googleTrends: 0.10,
    personalInterest: 0.15  // Höhere Gewichtung für persönliche Interessen
  };

  let totalScore = 0;
  for (const [key, value] of Object.entries(scores)) {
    totalScore += value * weights[key];
  }

  return {
    score: totalScore,
    details: scores,
    roi: (scores.commission * scores.avgOrderValue * scores.conversionRate) / scores.difficulty,
    personalFit: scores.personalInterest * scores.trend * scores.googleTrends
  };
}

function getCompetitionScore(competition) {
  const scores = {
    "sehr hoch": 0.2,
    "hoch": 0.4,
    "mittel": 0.7,
    "niedrig": 0.9
  };
  return scores[competition] || 0.5;
}

function getDifficultyScore(difficulty) {
  const scores = {
    "sehr hoch": 0.2,
    "hoch": 0.4,
    "mittel": 0.7,
    "niedrig": 0.9
  };
  return scores[difficulty] || 0.5;
}

function getTrendScore(trend) {
  const scores = {
    "explosiv steigend": 1.0,
    "steigend": 0.8,
    "stabil": 0.6,
    "fallend": 0.3
  };
  return scores[trend] || 0.5;
}

function getGoogleTrendsScore(trends) {
  const scores = {
    "steigend": 0.9,
    "stabil": 0.7,
    "volatil": 0.6,
    "fallend": 0.3,
    "saisonal": 0.5
  };
  return scores[trends] || 0.5;
}

function getPersonalInterestScore(interest) {
  const scores = {
    "hoch": 1.0,
    "mittel": 0.6,
    "niedrig": 0.3
  };
  return scores[interest] || 0.5;
}

// Domain-Generierung für erweiterte Nischen
function generateExtendedDomains(niche, keywords) {
  const domains = [];
  const tlds = ['.de', '.com', '.net', '.org', '.io', '.co'];
  
  for (const keyword of keywords) {
    for (const tld of tlds) {
      domains.push(keyword + tld);
    }
  }
  
  return domains;
}

async function checkDomain(domain) {
  try {
    await resolve4(domain);
    return false; // Vergeben
  } catch (error) {
    if (error.code === 'ENOTFOUND') {
      return true; // Frei
    }
    return false;
  }
}

async function analyzeExtendedNiches() {
  console.log('🔍 ERWEITERTE NISCHEN-ANALYSE MIT PERSÖNLICHEN INTERESSEN\n');
  
  const results = [];
  
  // Alle Nischen analysieren
  for (const [category, categoryData] of Object.entries(extendedNiches)) {
    console.log(`📂 KATEGORIE: ${categoryData.name.toUpperCase()}`);
    
    for (const [subniche, nicheData] of Object.entries(categoryData.subniches)) {
      const analysis = calculateExtendedNicheScore(nicheData);
      
      results.push({
        category,
        subniche,
        data: nicheData,
        analysis
      });
      
      console.log(`\n🎯 ${nicheData.name}`);
      console.log(`   Score: ${(analysis.score * 100).toFixed(1)}/100`);
      console.log(`   ROI-Potential: ${(analysis.roi * 100).toFixed(1)}%`);
      console.log(`   Persönliche Passung: ${(analysis.personalFit * 100).toFixed(1)}%`);
      console.log(`   Commission: ${nicheData.commission}`);
      console.log(`   Avg. Order: ${nicheData.avgOrderValue}€`);
      console.log(`   Conversion: ${nicheData.conversionRate}`);
      console.log(`   Competition: ${nicheData.competition}`);
      console.log(`   Difficulty: ${nicheData.difficulty}`);
      console.log(`   Trend: ${nicheData.trend}`);
      console.log(`   Google Trends: ${nicheData.googleTrends}`);
      console.log(`   Persönliches Interesse: ${nicheData.personalInterest}`);
      console.log(`   Programs: ${nicheData.programs.join(', ')}`);
    }
    console.log('\n' + '='.repeat(80) + '\n');
  }
  
  // Top-Nischen sortieren nach persönlicher Passung
  results.sort((a, b) => b.analysis.personalFit - a.analysis.personalFit);
  
  console.log('🏆 TOP 15 NISCHEN NACH PERSÖNLICHER PASSUNG:\n');
  
  for (let i = 0; i < Math.min(15, results.length); i++) {
    const niche = results[i];
    console.log(`${i + 1}. ${niche.data.name} (${niche.category})`);
    console.log(`   Score: ${(niche.analysis.score * 100).toFixed(1)}/100`);
    console.log(`   Persönliche Passung: ${(niche.analysis.personalFit * 100).toFixed(1)}%`);
    console.log(`   ROI: ${(niche.analysis.roi * 100).toFixed(1)}%`);
    console.log(`   Commission: ${niche.data.commission}`);
    console.log(`   Trend: ${niche.data.trend}`);
    console.log(`   Google Trends: ${niche.data.googleTrends}`);
    console.log('');
  }
  
  // Content-Recycling-Strategie
  console.log('♻️ CONTENT-RECYCLING-STRATEGIE:\n');
  
  const recyclingGroups = {
    "KI & Tech": ["kiCoding", "digitalProducts"],
    "Fitness & Lifestyle": ["tanzenSport", "biohacking"],
    "Business & Finance": ["businessFinance", "digitalProducts"]
  };
  
  for (const [group, categories] of Object.entries(recyclingGroups)) {
    console.log(`${group}:`);
    categories.forEach(cat => {
      const niches = results.filter(r => r.category === cat);
      niches.forEach(niche => {
        console.log(`  - ${niche.data.name}: ${niche.data.keywords.join(', ')}`);
      });
    });
    console.log('');
  }
  
  // Domain-Check für Top-Nischen
  console.log('🌐 DOMAIN-CHECK FÜR TOP-NISCHEN:\n');
  
  for (let i = 0; i < Math.min(5, results.length); i++) {
    const niche = results[i];
    console.log(`\n📂 ${niche.data.name}:`);
    
    const domains = generateExtendedDomains(niche.subniche, niche.data.keywords.slice(0, 3));
    
    for (const domain of domains.slice(0, 5)) {
      const isAvailable = await checkDomain(domain);
      const status = isAvailable ? '✅ FREI' : '❌ VERGEBEN';
      console.log(`   ${status}: ${domain}`);
      
      if (isAvailable) {
        console.log(`      💡 Perfekt für: ${niche.data.name}`);
        console.log(`      🎯 Target: ${niche.data.targetAudience}`);
        console.log(`      💰 Potential: ${niche.data.avgOrderValue}€ × ${niche.data.conversionRate} = ${(niche.data.avgOrderValue * parseFloat(niche.data.conversionRate.split('-')[1]) / 100).toFixed(0)}€/Conversion`);
        console.log(`      🎭 Persönliche Passung: ${niche.data.personalInterest}`);
      }
      
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  // Strategie-Empfehlungen
  console.log('\n🚀 PERSONALISIERTE STRATEGIE-EMPFEHLUNGEN:\n');
  
  const topNiche = results[0];
  console.log(`1. HAUPTNISCHE: ${topNiche.data.name}`);
  console.log(`   - Perfekt für Ihre Interessen: ${topNiche.data.personalInterest}`);
  console.log(`   - Trend: ${topNiche.data.trend} (Google Trends: ${topNiche.data.googleTrends})`);
  console.log(`   - Target: ${topNiche.data.targetAudience}`);
  console.log(`   - Pain Points: ${topNiche.data.painPoints.join(', ')}`);
  console.log(`   - Beste Programme: ${topNiche.data.programs.slice(0, 3).join(', ')}`);
  
  console.log('\n2. CONTENT-RECYCLING-STRATEGIE:');
  console.log('   - KI-Content für Coding-Nische wiederverwenden');
  console.log('   - Fitness-Content für Tanzen-Nische anpassen');
  console.log('   - Business-Content für Coaching-Nische erweitern');
  console.log('   - Biohacking-Content für Gesundheit-Nische nutzen');
  
  console.log('\n3. MULTI-NISCHEN-APPROACH:');
  console.log('   - Hauptfokus: KI & Coding (höchste persönliche Passung)');
  console.log('   - Sekundär: Tanzen & Sport (Hobby-basiert)');
  console.log('   - Tertiär: Business & Coaching (Erfahrung)');
  console.log('   - Ergänzend: Biohacking (Trend)');
  
  return results;
}

// Script ausführen
analyzeExtendedNiches().catch(console.error); 