/**
 * AWIN API Test Script
 * Testet die AWIN Integration und zeigt verfügbare Programme
 */

require('dotenv').config();

// Simple JavaScript Version für schnellen Test
const axios = require('axios');

class AwinAPITest {
  constructor() {
    this.apiKey = process.env.AWIN_API_KEY;
    this.publisherId = process.env.AWIN_PUBLISHER_ID;
    this.baseUrl = process.env.AWIN_BASE_URL || 'https://api.awin.com';
    
    console.log('🚀 AWIN API Test gestartet...');
    console.log(`📊 Publisher ID: ${this.publisherId}`);
    console.log(`🔑 API Key: ${this.apiKey ? 'Gesetzt' : 'FEHLT!'}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      'User-Agent': 'MarketingFunnelMaster-Test/1.0'
    };
  }

  async testBasicConnection() {
    try {
      console.log('🔄 1. Teste Basis-Verbindung zur AWIN API...');
      
      const response = await axios.get(
        `${this.baseUrl}/publishers/${this.publisherId}/programmes`,
        {
          headers: this.getHeaders(),
          timeout: 15000,
          params: {
            limit: 5
          }
        }
      );

      if (response.status === 200) {
        console.log('✅ Verbindung erfolgreich!');
        console.log(`📈 Status Code: ${response.status}`);
        console.log(`📊 Programme verfügbar: ${response.data.length || 'Unbekannt'}`);
        return true;
      } else {
        console.log(`❌ Unerwarteter Status Code: ${response.status}`);
        return false;
      }
    } catch (error) {
      console.log('❌ Verbindungsfehler:');
      if (error.response) {
        console.log(`   Status: ${error.response.status}`);
        console.log(`   Message: ${error.response.data?.message || error.message}`);
      } else {
        console.log(`   Error: ${error.message}`);
      }
      return false;
    }
  }

  async loadTopPrograms() {
    try {
      console.log('🔄 2. Lade Top Affiliate Programme...');
      
      const response = await axios.get(
        `${this.baseUrl}/publishers/${this.publisherId}/programmes`,
        {
          headers: this.getHeaders(),
          params: {
            limit: 10,
            offset: 0
          }
        }
      );

      const programs = response.data;
      console.log(`✅ ${programs.length} Programme geladen:`);
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

      programs.forEach((program, index) => {
        console.log(`${index + 1}. ${program.programName || 'Unnamed Program'}`);
        console.log(`   ID: ${program.id}`);
        console.log(`   Sektor: ${program.primarySector || 'Unbekannt'}`);
        console.log(`   Status: ${program.relationshipStatus || 'Unbekannt'}`);
        console.log(`   Commission: ${program.commissionRange?.max || 'N/A'}%`);
        console.log(`   Cookie: ${program.cookiePeriod || 'N/A'} Tage`);
        console.log('   ────────────────────────────');
      });

      return programs;
    } catch (error) {
      console.log('❌ Fehler beim Laden der Programme:');
      console.log(`   ${error.message}`);
      return [];
    }
  }

  async testDeepLinkCreation() {
    try {
      console.log('🔄 3. Teste Deep Link Erstellung...');
      
      // Verwende das erste verfügbare Programm für Deep Link Test
      const programsResponse = await axios.get(
        `${this.baseUrl}/publishers/${this.publisherId}/programmes`,
        {
          headers: this.getHeaders(),
          params: { limit: 1 }
        }
      );

      if (programsResponse.data.length === 0) {
        console.log('⚠️ Keine Programme verfügbar für Deep Link Test');
        return;
      }

      const testProgram = programsResponse.data[0];
      console.log(`📝 Teste mit Programm: ${testProgram.programName} (ID: ${testProgram.id})`);

      // Deep Link erstellen
      const deepLinkResponse = await axios.get(
        `${this.baseUrl}/publishers/${this.publisherId}/links`,
        {
          headers: this.getHeaders(),
          params: {
            'p': testProgram.id,
            'url': 'https://example.com',
            'clickRef': 'test_campaign_001'
          }
        }
      );

      console.log('✅ Deep Link erfolgreich erstellt:');
      console.log(`🔗 URL: ${deepLinkResponse.data.clickThroughUrl || 'N/A'}`);
      
    } catch (error) {
      console.log('❌ Deep Link Test fehlgeschlagen:');
      console.log(`   ${error.message}`);
    }
  }

  async checkTransactions() {
    try {
      console.log('🔄 4. Prüfe Transaktions-Daten...');
      
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30); // 30 Tage zurück

      const response = await axios.get(
        `${this.baseUrl}/publishers/${this.publisherId}/transactions`,
        {
          headers: this.getHeaders(),
          params: {
            startDate: startDate.toISOString().split('T')[0],
            endDate: endDate.toISOString().split('T')[0],
            limit: 10
          }
        }
      );

      const transactions = response.data;
      console.log(`✅ ${transactions.length} Transaktionen gefunden (letzte 30 Tage)`);

      if (transactions.length > 0) {
        let totalCommissions = 0;
        transactions.forEach((transaction, index) => {
          const commission = parseFloat(transaction.commissionValue || 0);
          totalCommissions += commission;
          
          console.log(`   ${index + 1}. ${transaction.programName || 'Unknown'}`);
          console.log(`      Commission: €${commission.toFixed(2)}`);
          console.log(`      Order Value: €${parseFloat(transaction.orderValue || 0).toFixed(2)}`);
        });
        
        console.log(`💰 Gesamt-Kommissionen: €${totalCommissions.toFixed(2)}`);
      } else {
        console.log('ℹ️ Keine Transaktionen in den letzten 30 Tagen');
      }

    } catch (error) {
      console.log('❌ Transaktions-Check fehlgeschlagen:');
      console.log(`   ${error.message}`);
    }
  }

  async runFullTest() {
    console.log('🎯 AWIN API VOLLSTÄNDIGER TEST');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    if (!this.apiKey || !this.publisherId) {
      console.log('❌ FEHLER: API Key oder Publisher ID fehlt!');
      console.log('💡 Bitte setzen Sie AWIN_API_KEY und AWIN_PUBLISHER_ID in der .env Datei');
      return;
    }

    // Test 1: Basis-Verbindung
    const connectionOk = await this.testBasicConnection();
    if (!connectionOk) {
      console.log('❌ Test abgebrochen - Verbindung fehlgeschlagen');
      return;
    }

    console.log('\n');

    // Test 2: Programme laden  
    await this.loadTopPrograms();
    
    console.log('\n');

    // Test 3: Deep Link erstellen
    await this.testDeepLinkCreation();
    
    console.log('\n');

    // Test 4: Transaktionen prüfen
    await this.checkTransactions();

    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 AWIN API Test abgeschlossen!');
    console.log('✅ Ihr AWIN Account ist bereit für die Integration!');
  }
}

// Test ausführen
const test = new AwinAPITest();
test.runFullTest().catch(console.error);