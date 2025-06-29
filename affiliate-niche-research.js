#!/usr/bin/env node

import dns from 'dns';
import { promisify } from 'util';

const resolve4 = promisify(dns.resolve4);

// Affiliate-Nischen-Analyse mit KPI-Bewertung
const affiliateNiches = {
  // Finanz-Nischen (Ihre Empfehlung)
  finanz: {
    name: "Finanz & Geld",
    subniches: {
      kryptowaehrung: {
        name: "Kryptowährung",
        commission: "5-15%",
        avgOrderValue: 500,
        conversionRate: "2-5%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Binance", "Coinbase", "eToro", "Bitpanda"],
        keywords: ["bitcoin", "krypto", "crypto", "blockchain", "trading"],
        painPoints: ["Verlustangst", "Komplexität", "Sicherheit"],
        targetAudience: "Tech-affine, 25-45, männlich",
        seasonality: "ganzjährig",
        trend: "steigend"
      },
      investieren: {
        name: "Investieren & Trading",
        commission: "3-10%",
        avgOrderValue: 1000,
        conversionRate: "1-3%",
        competition: "sehr hoch",
        difficulty: "hoch",
        programs: ["eToro", "Plus500", "IG", "DEGIRO"],
        keywords: ["investieren", "trading", "aktien", "etf", "portfolio"],
        painPoints: ["Risiko", "Wissen", "Zeit"],
        targetAudience: "30-60, gebildet, finanziell interessiert",
        seasonality: "ganzjährig",
        trend: "stabil"
      },
      passivEinkommen: {
        name: "Passives Einkommen",
        commission: "10-50%",
        avgOrderValue: 200,
        conversionRate: "3-8%",
        competition: "mittel",
        difficulty: "niedrig",
        programs: ["Digistore24", "Clickbank", "Jvzoo"],
        keywords: ["passiv", "einkommen", "automatisch", "online", "geld"],
        painPoints: ["Zeitmangel", "Geldmangel", "Angst"],
        targetAudience: "25-50, alle Geschlechter, Zeitmangel",
        seasonality: "ganzjährig",
        trend: "steigend"
      }
    }
  },

  // Bio-Hacking (Ihre Empfehlung)
  biohacking: {
    name: "Bio-Hacking & Optimierung",
    subniches: {
      nootropics: {
        name: "Nootropics & Gehirnoptimierung",
        commission: "15-30%",
        avgOrderValue: 150,
        conversionRate: "4-10%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["iHerb", "Amazon", "Mind Lab Pro", "Alpha Brain"],
        keywords: ["nootropics", "gehirn", "fokus", "gedächtnis", "leistung"],
        painPoints: ["Konzentrationsschwäche", "Stress", "Müdigkeit"],
        targetAudience: "25-45, Studenten, Berufstätige",
        seasonality: "ganzjährig",
        trend: "steigend"
      },
      fitnessOptimierung: {
        name: "Fitness & Körperoptimierung",
        commission: "10-25%",
        avgOrderValue: 200,
        conversionRate: "3-7%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Myprotein", "Amazon", "Fitness-Programme"],
        keywords: ["fitness", "muskeln", "abnehmen", "gesundheit", "training"],
        painPoints: ["Zeitmangel", "Motivation", "Wissen"],
        targetAudience: "20-50, gesundheitsbewusst",
        seasonality: "Jan-März, Sep-Nov",
        trend: "stabil"
      },
      schlafOptimierung: {
        name: "Schlaf & Regeneration",
        commission: "15-35%",
        avgOrderValue: 100,
        conversionRate: "5-12%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["Amazon", "Sleep-Programme", "Supplements"],
        keywords: ["schlaf", "regeneration", "erholung", "müdigkeit"],
        painPoints: ["Schlafmangel", "Stress", "Müdigkeit"],
        targetAudience: "25-55, gestresst, Schlafprobleme",
        seasonality: "ganzjährig",
        trend: "steigend"
      }
    }
  },

  // KI & Tech (Ihre Empfehlung)
  ki: {
    name: "KI & Technologie",
    subniches: {
      kiTools: {
        name: "KI-Tools & Software",
        commission: "20-40%",
        avgOrderValue: 50,
        conversionRate: "8-15%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["Software-Affiliate", "SaaS", "Digital Products"],
        keywords: ["ki", "ai", "tools", "software", "automatisierung"],
        painPoints: ["Zeitmangel", "Komplexität", "Kosten"],
        targetAudience: "25-45, Tech-affin, Unternehmer",
        seasonality: "ganzjährig",
        trend: "explosiv steigend"
      },
      onlineBusiness: {
        name: "Online Business & Automatisierung",
        commission: "25-50%",
        avgOrderValue: 300,
        conversionRate: "3-8%",
        competition: "mittel",
        difficulty: "mittel",
        programs: ["Clickbank", "Jvzoo", "Digital Products"],
        keywords: ["online", "business", "automatisierung", "passiv"],
        painPoints: ["Zeitmangel", "Geldmangel", "Angst"],
        targetAudience: "25-50, Unternehmer, Angestellte",
        seasonality: "ganzjährig",
        trend: "steigend"
      }
    }
  },

  // Versicherung (Ihre Empfehlung)
  versicherung: {
    name: "Versicherung & Sicherheit",
    subniches: {
      haftpflicht: {
        name: "Haftpflicht & Rechtsschutz",
        commission: "5-15%",
        avgOrderValue: 200,
        conversionRate: "1-3%",
        competition: "hoch",
        difficulty: "hoch",
        programs: ["Check24", "Verivox", "Versicherungen"],
        keywords: ["haftpflicht", "versicherung", "rechtsschutz", "sicherheit"],
        painPoints: ["Angst", "Komplexität", "Kosten"],
        targetAudience: "25-65, alle Geschlechter",
        seasonality: "ganzjährig",
        trend: "stabil"
      },
      lebensversicherung: {
        name: "Lebensversicherung & Vorsorge",
        commission: "10-25%",
        avgOrderValue: 1000,
        conversionRate: "0.5-2%",
        competition: "sehr hoch",
        difficulty: "sehr hoch",
        programs: ["Versicherungsmakler", "Online-Versicherer"],
        keywords: ["lebensversicherung", "vorsorge", "familie", "sicherheit"],
        painPoints: ["Angst", "Komplexität", "Kosten"],
        targetAudience: "30-60, Familien, Verantwortungsbewusst",
        seasonality: "ganzjährig",
        trend: "stabil"
      }
    }
  },

  // Gesundheit (Ihre Empfehlung)
  gesundheit: {
    name: "Gesundheit & Wellness",
    subniches: {
      ernaehrung: {
        name: "Ernährung & Diäten",
        commission: "10-30%",
        avgOrderValue: 150,
        conversionRate: "4-10%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Amazon", "iHerb", "Ernährungsprogramme"],
        keywords: ["ernährung", "diät", "abnehmen", "gesund", "vitamine"],
        painPoints: ["Gewichtsprobleme", "Gesundheit", "Energie"],
        targetAudience: "25-60, gesundheitsbewusst",
        seasonality: "Jan-März, Sep-Nov",
        trend: "steigend"
      },
      mentaleGesundheit: {
        name: "Mentale Gesundheit & Stress",
        commission: "15-40%",
        avgOrderValue: 100,
        conversionRate: "5-12%",
        competition: "niedrig",
        difficulty: "niedrig",
        programs: ["Meditation-Apps", "Coaching", "Bücher"],
        keywords: ["stress", "meditation", "achtsamkeit", "entspannung"],
        painPoints: ["Stress", "Angst", "Burnout"],
        targetAudience: "25-55, gestresst, berufstätig",
        seasonality: "ganzjährig",
        trend: "steigend"
      }
    }
  },

  // Sport & Laufen (Ihre Empfehlung)
  sport: {
    name: "Sport & Laufen",
    subniches: {
      laufen: {
        name: "Laufen & Jogging",
        commission: "8-20%",
        avgOrderValue: 120,
        conversionRate: "3-8%",
        competition: "hoch",
        difficulty: "mittel",
        programs: ["Amazon", "Sportartikel", "Laufprogramme"],
        keywords: ["laufen", "jogging", "marathon", "sport", "fitness"],
        painPoints: ["Motivation", "Zeit", "Verletzungen"],
        targetAudience: "25-55, sportlich, gesundheitsbewusst",
        seasonality: "März-Okt",
        trend: "stabil"
      },
      homeFitness: {
        name: "Home Fitness & Workouts",
        commission: "15-35%",
        avgOrderValue: 200,
        conversionRate: "4-10%",
        competition: "mittel",
        difficulty: "niedrig",
        programs: ["Fitness-Programme", "Equipment", "Online-Kurse"],
        keywords: ["home", "fitness", "workout", "training", "muskeln"],
        painPoints: ["Zeitmangel", "Motivation", "Platz"],
        targetAudience: "25-50, beschäftigt, gesundheitsbewusst",
        seasonality: "Jan-März, Sep-Nov",
        trend: "steigend"
      }
    }
  }
};

// KPI-Berechnung
function calculateNicheScore(niche) {
  const scores = {
    commission: parseFloat(niche.commission.split('-')[1]) / 100,
    avgOrderValue: niche.avgOrderValue / 1000,
    conversionRate: parseFloat(niche.conversionRate.split('-')[1]) / 100,
    competition: getCompetitionScore(niche.competition),
    difficulty: getDifficultyScore(niche.difficulty),
    trend: getTrendScore(niche.trend)
  };

  // Gewichtete Bewertung
  const weights = {
    commission: 0.2,
    avgOrderValue: 0.15,
    conversionRate: 0.2,
    competition: 0.15,
    difficulty: 0.15,
    trend: 0.15
  };

  let totalScore = 0;
  for (const [key, value] of Object.entries(scores)) {
    totalScore += value * weights[key];
  }

  return {
    score: totalScore,
    details: scores,
    roi: (scores.commission * scores.avgOrderValue * scores.conversionRate) / scores.difficulty
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

// Domain-Generierung für Nischen
function generateNicheDomains(niche, keywords) {
  const domains = [];
  const tlds = ['.de', '.com', '.net', '.org', '.io'];
  
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

async function analyzeAffiliateNiches() {
  console.log('🔍 PROFESSIONELLE AFFILIATE-NISCHEN-ANALYSE\n');
  
  const results = [];
  
  // Alle Nischen analysieren
  for (const [category, categoryData] of Object.entries(affiliateNiches)) {
    console.log(`📂 KATEGORIE: ${categoryData.name.toUpperCase()}`);
    
    for (const [subniche, nicheData] of Object.entries(categoryData.subniches)) {
      const analysis = calculateNicheScore(nicheData);
      
      results.push({
        category,
        subniche,
        data: nicheData,
        analysis
      });
      
      console.log(`\n🎯 ${nicheData.name}`);
      console.log(`   Score: ${(analysis.score * 100).toFixed(1)}/100`);
      console.log(`   ROI-Potential: ${(analysis.roi * 100).toFixed(1)}%`);
      console.log(`   Commission: ${nicheData.commission}`);
      console.log(`   Avg. Order: ${nicheData.avgOrderValue}€`);
      console.log(`   Conversion: ${nicheData.conversionRate}`);
      console.log(`   Competition: ${nicheData.competition}`);
      console.log(`   Difficulty: ${nicheData.difficulty}`);
      console.log(`   Trend: ${nicheData.trend}`);
      console.log(`   Programs: ${nicheData.programs.join(', ')}`);
    }
    console.log('\n' + '='.repeat(60) + '\n');
  }
  
  // Top-Nischen sortieren
  results.sort((a, b) => b.analysis.score - a.analysis.score);
  
  console.log('🏆 TOP 10 PROFITABELSTE NISCHEN:\n');
  
  for (let i = 0; i < Math.min(10, results.length); i++) {
    const niche = results[i];
    console.log(`${i + 1}. ${niche.data.name} (${niche.category})`);
    console.log(`   Score: ${(niche.analysis.score * 100).toFixed(1)}/100`);
    console.log(`   ROI: ${(niche.analysis.roi * 100).toFixed(1)}%`);
    console.log(`   Commission: ${niche.data.commission}`);
    console.log(`   Trend: ${niche.data.trend}`);
    console.log('');
  }
  
  // Domain-Check für Top-Nischen
  console.log('🌐 DOMAIN-CHECK FÜR TOP-NISCHEN:\n');
  
  for (let i = 0; i < Math.min(5, results.length); i++) {
    const niche = results[i];
    console.log(`\n📂 ${niche.data.name}:`);
    
    const domains = generateNicheDomains(niche.subniche, niche.data.keywords.slice(0, 3));
    
    for (const domain of domains.slice(0, 5)) {
      const isAvailable = await checkDomain(domain);
      const status = isAvailable ? '✅ FREI' : '❌ VERGEBEN';
      console.log(`   ${status}: ${domain}`);
      
      if (isAvailable) {
        console.log(`      💡 Empfohlen für: ${niche.data.name}`);
        console.log(`      🎯 Target: ${niche.data.targetAudience}`);
        console.log(`      💰 Potential: ${niche.data.avgOrderValue}€ × ${niche.data.conversionRate} = ${(niche.data.avgOrderValue * parseFloat(niche.data.conversionRate.split('-')[1]) / 100).toFixed(0)}€/Conversion`);
      }
      
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  // Strategie-Empfehlungen
  console.log('\n🚀 STRATEGIE-EMPFEHLUNGEN:\n');
  
  const topNiche = results[0];
  console.log(`1. HAUPTNISCHE: ${topNiche.data.name}`);
  console.log(`   - Fokus auf ${topNiche.data.trend} Trend`);
  console.log(`   - Target: ${topNiche.data.targetAudience}`);
  console.log(`   - Pain Points: ${topNiche.data.painPoints.join(', ')}`);
  console.log(`   - Beste Programme: ${topNiche.data.programs.slice(0, 3).join(', ')}`);
  
  console.log('\n2. CONTENT-STRATEGIE:');
  console.log('   - Blog für SEO und Autorität');
  console.log('   - Social Media für Engagement');
  console.log('   - Email-Marketing für Conversions');
  console.log('   - Funnel nur bei direkten Produkt-Empfehlungen');
  
  console.log('\n3. DOMAIN-STRATEGIE:');
  console.log('   - Hauptdomain: Nischen-spezifisch');
  console.log('   - Blog-Domain: Autorität aufbauen');
  console.log('   - Funnel-Domains: Conversion-optimiert');
  
  return results;
}

// Script ausführen
analyzeAffiliateNiches().catch(console.error); 