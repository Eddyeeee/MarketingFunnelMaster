/**
 * AWIN API Test Script (ES Module Version)
 * Testet die AWIN Integration und zeigt verfügbare Programme
 */

import { config } from 'dotenv';
import axios from 'axios';

// Load environment variables
config();

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
        console.log('   ────────────────────────────────');
      });

      return programs;
    } catch (error) {
      console.log('❌ Fehler beim Laden der Programme:');
      console.log(`   ${error.message}`);
      return [];
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

    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 AWIN API Test abgeschlossen!');
    console.log('✅ Ihr AWIN Account ist bereit für die Integration!');
    console.log('💡 Nächster Schritt: Tragen Sie Ihren echten API Key ein und testen Sie erneut');
  }
}

// Test ausführen
const test = new AwinAPITest();
test.runFullTest().catch(console.error);