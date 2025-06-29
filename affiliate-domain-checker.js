#!/usr/bin/env node

import dns from 'dns';
import { promisify } from 'util';

const resolve4 = promisify(dns.resolve4);
const resolve6 = promisify(dns.resolve6);

// Affiliate-Marketing Domain-Kategorien
const domainCategories = {
  // Hauptkategorien
  finanz: [
    'geld-verdienen', 'passiv-einkommen', 'online-geld', 'finanz-freiheit',
    'geld-online', 'einkommen-passiv', 'finanz-strategie', 'geld-strategie',
    'online-einkommen', 'finanz-tipps', 'geld-tipps', 'einkommen-online'
  ],
  
  // Spezifische Affiliate-Nischen
  krypto: [
    'krypto-geld', 'bitcoin-geld', 'crypto-einkommen', 'krypto-strategie',
    'bitcoin-strategie', 'crypto-tipps', 'krypto-tipps', 'blockchain-geld'
  ],
  
  investieren: [
    'investieren-geld', 'anlage-strategie', 'investment-tipps', 'geld-anlegen',
    'anlage-geld', 'investment-strategie', 'geld-investieren', 'anlage-tipps'
  ],
  
  business: [
    'business-geld', 'unternehmer-geld', 'startup-geld', 'business-strategie',
    'unternehmer-strategie', 'startup-strategie', 'business-tipps'
  ],
  
  online: [
    'online-business', 'internet-geld', 'web-geld', 'digital-geld',
    'online-strategie', 'internet-strategie', 'web-strategie', 'digital-strategie'
  ],
  
  // Persona-spezifisch
  studenten: [
    'student-geld', 'student-einkommen', 'student-strategie', 'student-tipps',
    'studium-geld', 'studium-einkommen', 'student-online', 'student-business'
  ],
  
  eltern: [
    'eltern-geld', 'eltern-einkommen', 'familie-geld', 'familie-einkommen',
    'eltern-strategie', 'familie-strategie', 'eltern-online', 'familie-online'
  ],
  
  freelancer: [
    'freelancer-geld', 'freelancer-einkommen', 'freelancer-strategie',
    'freelancer-tipps', 'freelancer-online', 'freelancer-business'
  ],
  
  bestager: [
    'bestager-geld', 'bestager-einkommen', 'bestager-strategie', 'bestager-tipps',
    '50plus-geld', '50plus-einkommen', 'bestager-online', '50plus-online'
  ],
  
  angestellte: [
    'angestellter-geld', 'angestellter-einkommen', 'angestellter-strategie',
    'angestellter-tipps', 'angestellter-online', 'angestellter-business'
  ],
  
  // Action-Wörter
  action: [
    'geld-machen', 'geld-verdienen', 'geld-generieren', 'geld-schaffen',
    'einkommen-machen', 'einkommen-verdienen', 'einkommen-generieren',
    'freiheit-schaffen', 'freiheit-erreichen', 'freiheit-verdienen'
  ],
  
  // Moderne Begriffe
  modern: [
    'side-hustle', 'side-income', 'passive-income', 'financial-freedom',
    'money-making', 'income-generation', 'wealth-building', 'freedom-creating'
  ]
};

// TLDs für verschiedene Strategien
const tlds = [
  '.de',    // Hauptmarkt Deutschland
  '.com',   // International
  '.net',   // Technisch
  '.org',   // Vertrauensvoll
  '.info',  // Informativ
  '.co',    // Business
  '.io',    // Tech/Modern
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

async function checkAllDomains() {
  console.log('🔍 Affiliate-Marketing Domain-Checker gestartet...\n');
  
  const results = {
    available: [],
    taken: [],
    byCategory: {}
  };
  
  let totalChecked = 0;
  let availableCount = 0;
  
  for (const [category, domains] of Object.entries(domainCategories)) {
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
  
  // Top-Empfehlungen
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
  
  // Spezielle Empfehlungen für Affiliate-Marketing
  console.log('🎯 AFFILIATE-MARKETING SPEZIAL-EMPFEHLUNGEN:');
  const affiliateRecommendations = results.available.filter(domain => 
    domain.domain.includes('geld') || 
    domain.domain.includes('einkommen') || 
    domain.domain.includes('freiheit') ||
    domain.domain.includes('strategie')
  ).slice(0, 10);
  
  affiliateRecommendations.forEach(domain => {
    console.log(`  🎯 ${domain.domain}`);
  });
  
  // Provider-Empfehlungen
  console.log('\n🚀 PROVIDER-EMPFEHLUNGEN FÜR AFFILIATE-MARKETING:');
  console.log('1. Hetzner (ab 0,99€/Jahr) - Hauptprovider');
  console.log('2. INWX (ab 1,99€/Jahr) - Backup/Performance');
  console.log('3. Cloudflare (kostenlos) - DDoS-Schutz');
  console.log('4. All-Inkl (bereits vorhanden) - Hosting');
  console.log('5. Strato (bereits vorhanden) - Backup');
  
  return results;
}

// Script ausführen
checkAllDomains().catch(console.error); 