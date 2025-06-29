const https = require('https');
const dns = require('dns').promises;

const domains = [
  // Dachmarke
  'flowtelligence.de',
  'flowtelligence.com',
  
  // Persona-Marken
  'starter-kapital.de',
  'starter-kapital.com',
  'eltern-einkommen.de',
  'eltern-einkommen.com',
  'projekt-profit.de',
  'projekt-profit.com',
  'renten-rendite.de',
  'renten-rendite.com',
  'feierabend-kapital.de',
  'feierabend-kapital.com',
  'remote-cashflow.de',
  'remote-cashflow.com',
  
  // Alternative Schreibweisen
  'starterkapital.de',
  'starterkapital.com',
  'elterneinkommen.de',
  'elterneinkommen.com',
  'projektprofit.de',
  'projektprofit.com',
  'rentenrendite.de',
  'rentenrendite.com',
  'feierabendkapital.de',
  'feierabendkapital.com',
  'remotecashflow.de',
  'remotecashflow.com'
];

async function checkDomain(domain) {
  try {
    // DNS-Lookup versuchen
    await dns.lookup(domain);
    return { domain, available: false, status: 'Registriert' };
  } catch (error) {
    if (error.code === 'ENOTFOUND') {
      return { domain, available: true, status: 'FREI!' };
    } else {
      return { domain, available: false, status: 'Fehler: ' + error.code };
    }
  }
}

async function checkAllDomains() {
  console.log('🔍 Prüfe Domain-Verfügbarkeit...\n');
  
  const results = [];
  
  for (const domain of domains) {
    const result = await checkDomain(domain);
    results.push(result);
    
    // Sofortige Ausgabe
    const status = result.available ? '✅ FREI!' : '❌ Vergeben';
    console.log(`${status} ${domain}`);
    
    // Kleine Pause zwischen den Checks
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  console.log('\n📊 ZUSAMMENFASSUNG:');
  console.log('==================');
  
  const available = results.filter(r => r.available);
  const taken = results.filter(r => !r.available);
  
  console.log(`\n✅ FREIE DOMAINS (${available.length}):`);
  available.forEach(result => {
    console.log(`   • ${result.domain}`);
  });
  
  console.log(`\n❌ VERGEBENE DOMAINS (${taken.length}):`);
  taken.forEach(result => {
    console.log(`   • ${result.domain} - ${result.status}`);
  });
  
  console.log('\n💡 EMPFEHLUNGEN:');
  console.log('================');
  
  if (available.length > 0) {
    console.log('🎯 Priorität 1 (Hauptmarken):');
    available.filter(r => r.domain.includes('flowtelligence')).forEach(result => {
      console.log(`   • ${result.domain} - Dachmarke`);
    });
    
    console.log('\n🎯 Priorität 2 (Persona-Marken):');
    available.filter(r => !r.domain.includes('flowtelligence')).forEach(result => {
      console.log(`   • ${result.domain}`);
    });
  } else {
    console.log('⚠️  Alle Domains sind bereits vergeben!');
    console.log('💡 Alternative Vorschläge:');
    console.log('   • flowtelligence.io');
    console.log('   • flowtelligence.net');
    console.log('   • starter-kapital.io');
    console.log('   • eltern-einkommen.net');
  }
}

// Script ausführen
checkAllDomains().catch(console.error); 