#!/usr/bin/env node

import dns from 'dns';
import { promisify } from 'util';

const resolve4 = promisify(dns.resolve4);

// KI-Tools Domain-Strategie
const kiDomains = {
  // Hauptdomains
  main: [
    'ai-tools-guru',
    'ki-automatisierung', 
    'ai-productivity',
    'ki-business',
    'ai-optimierung',
    'ki-tools-deutschland',
    'ai-automation',
    'ki-produktivitaet',
    'ai-business-tools',
    'ki-optimierung-tools'
  ],
  
  // Blog-Domains
  blog: [
    'ai-insights',
    'ki-trends',
    'ai-tipps',
    'ki-blog',
    'ai-news',
    'ki-updates',
    'ai-guide',
    'ki-ratgeber',
    'ai-magazin',
    'ki-journal'
  ],
  
  // Funnel-Domains
  funnel: [
    'ai-tools-test',
    'ki-vergleich',
    'ai-empfehlung',
    'ki-beste',
    'ai-top',
    'ki-reviews',
    'ai-vergleich',
    'ki-tests',
    'ai-empfehlungen',
    'ki-bewertungen'
  ],
  
  // Spezifische KI-Tools
  specific: [
    'chatgpt-tools',
    'midjourney-guide',
    'notion-ki',
    'zapier-automation',
    'grammarly-ki',
    'canva-ai',
    'copy-ai',
    'jasper-ai',
    'surfer-seo',
    'ahrefs-ki'
  ],
  
  // Nischen-spezifisch
  niche: [
    'ki-marketing',
    'ai-content',
    'ki-seo',
    'ai-design',
    'ki-writing',
    'ai-coding',
    'ki-research',
    'ai-analysis',
    'ki-automation',
    'ai-workflow'
  ]
};

// TLDs für verschiedene Strategien
const tlds = [
  '.de',    // Hauptmarkt Deutschland
  '.com',   // International
  '.net',   // Technisch
  '.org',   // Vertrauensvoll
  '.io',    // Tech/Modern
  '.co',    // Business
  '.me',    // Persönlich
  '.pro',   // Professionell
  '.biz'    // Business
];

async function checkDomain(domain) {
  try {
    await resolve4(domain);
    return false; // Domain ist vergeben
  } catch (error) {
    if (error.code === 'ENOTFOUND') {
      return true; // Domain ist frei
    }
    return false; // Anderer Fehler, vorsichtshalber als vergeben betrachten
  }
}

async function checkDomainWithTLD(baseDomain, tld) {
  const fullDomain = baseDomain + tld;
  const isAvailable = await checkDomain(fullDomain);
  return {
    domain: fullDomain,
    available: isAvailable,
    tld: tld
  };
}

async function checkKIDomains() {
  console.log('🤖 KI-TOOLS DOMAIN-CHECKER GESTARTET\n');
  
  const results = {
    available: [],
    taken: [],
    byCategory: {}
  };
  
  let totalChecked = 0;
  let availableCount = 0;
  
  for (const [category, domains] of Object.entries(kiDomains)) {
    console.log(`📂 Prüfe Kategorie: ${category.toUpperCase()}`);
    results.byCategory[category] = { available: [], taken: [] };
    
    for (const domain of domains) {
      for (const tld of tlds) {
        totalChecked++;
        const result = await checkDomainWithTLD(domain, tld);
        
        if (result.available) {
          availableCount++;
          results.available.push(result);
          results.byCategory[category].available.push(result);
          console.log(`✅ FREI: ${result.domain}`);
        } else {
          results.taken.push(result);
          results.byCategory[category].taken.push(result);
        }
        
        // Kurze Pause zwischen Checks
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    console.log('');
  }
  
  // Ergebnisse zusammenfassen
  console.log('📊 ERGEBNISSE:');
  console.log(`Gesamt geprüft: ${totalChecked} Domains`);
  console.log(`Verfügbar: ${availableCount} Domains`);
  console.log(`Vergeben: ${totalChecked - availableCount} Domains`);
  console.log('');
  
  // Top-Empfehlungen pro Kategorie
  console.log('🏆 TOP EMPFEHLUNGEN (verfügbare Domains):');
  console.log('');
  
  for (const [category, data] of Object.entries(results.byCategory)) {
    if (data.available.length > 0) {
      console.log(`${category.toUpperCase()}:`);
      data.available.slice(0, 5).forEach(domain => {
        console.log(`  ✅ ${domain.domain}`);
      });
      console.log('');
    }
  }
  
  // Spezielle Empfehlungen für KI-Tools
  console.log('🎯 KI-TOOLS SPEZIAL-EMPFEHLUNGEN:');
  const kiRecommendations = results.available.filter(domain => 
    domain.domain.includes('ai') || 
    domain.domain.includes('ki') || 
    domain.domain.includes('tools') ||
    domain.domain.includes('automation')
  ).slice(0, 15);
  
  kiRecommendations.forEach(domain => {
    console.log(`  🎯 ${domain.domain}`);
  });
  
  // Provider-Empfehlungen
  console.log('\n🚀 PROVIDER-EMPFEHLUNGEN FÜR KI-TOOLS:');
  console.log('1. Hetzner (ab 0,99€/Jahr) - Hauptprovider');
  console.log('2. INWX (ab 1,99€/Jahr) - Backup/Performance');
  console.log('3. Cloudflare (kostenlos) - DDoS-Schutz');
  console.log('4. All-Inkl (bereits vorhanden) - Hosting');
  console.log('5. Strato (bereits vorhanden) - Backup');
  
  // Strategie-Empfehlungen
  console.log('\n📈 STRATEGIE-EMPFEHLUNGEN:');
  console.log('1. Hauptdomains: Für Autorität und SEO');
  console.log('2. Blog-Domains: Für Content-Marketing');
  console.log('3. Funnel-Domains: Für Conversion-Optimierung');
  console.log('4. Spezifische Domains: Für Tool-spezifische Landingpages');
  console.log('5. Nischen-Domains: Für spezielle Zielgruppen');
  
  return results;
}

// Script ausführen
checkKIDomains().catch(console.error); 