/**
 * AWIN Affiliate Network Service
 * Integriert das weltweit größte Affiliate-Netzwerk für massive Revenue-Generierung
 */

import axios from 'axios';
import { config } from 'dotenv';

// Load environment variables
config();

interface AwinConfig {
  apiKey: string;
  publisherId: string;
  baseUrl: string;
}

interface AwinProgram {
  id: number;
  name: string;
  description: string;
  sector: string;
  commissionRate: number;
  cookiePeriod: number;
  applicationStatus: string;
  deepLinkUrl?: string;
}

interface AwinTransaction {
  id: string;
  clickTime: string;
  transactionTime: string;
  commissionValue: number;
  orderValue: number;
  programId: number;
  programName: string;
}

interface AwinDeepLink {
  clickThroughUrl: string;
  shortenedUrl?: string;
  trackingCode: string;
}

class AwinService {
  private config: AwinConfig;

  constructor() {
    this.config = {
      apiKey: process.env.AWIN_API_KEY || '',
      publisherId: process.env.AWIN_PUBLISHER_ID || '',
      baseUrl: process.env.AWIN_BASE_URL || 'https://api.awin.com'
    };

    if (!this.config.apiKey || !this.config.publisherId) {
      throw new Error('AWIN API credentials sind nicht konfiguriert!');
    }
  }

  private getHeaders() {
    return {
      'Authorization': `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
      'User-Agent': 'MarketingFunnelMaster/1.0'
    };
  }

  /**
   * Testet die AWIN API Verbindung
   */
  async testConnection(): Promise<boolean> {
    try {
      console.log('🔄 Teste AWIN API Verbindung...');
      
      const response = await axios.get(
        `${this.config.baseUrl}/publishers/${this.config.publisherId}/programmes`,
        {
          headers: this.getHeaders(),
          timeout: 10000,
          params: {
            limit: 1
          }
        }
      );

      if (response.status === 200) {
        console.log('✅ AWIN API Verbindung erfolgreich!');
        console.log(`📊 Publisher ID: ${this.config.publisherId}`);
        return true;
      } else {
        console.log('❌ AWIN API Verbindung fehlgeschlagen:', response.status);
        return false;
      }
    } catch (error: any) {
      console.error('❌ AWIN API Fehler:', error.message);
      if (error.response) {
        console.error('Response Status:', error.response.status);
        console.error('Response Data:', error.response.data);
      }
      return false;
    }
  }

  /**
   * Holt alle verfügbaren Affiliate Programme
   */
  async getPrograms(sector?: string, limit: number = 100): Promise<AwinProgram[]> {
    try {
      console.log(`🔍 Lade AWIN Programme... ${sector ? `(Sektor: ${sector})` : ''}`);
      
      const params: any = {
        limit,
        offset: 0
      };

      if (sector) {
        params.sector = sector;
      }

      const response = await axios.get(
        `${this.config.baseUrl}/publishers/${this.config.publisherId}/programmes`,
        {
          headers: this.getHeaders(),
          params
        }
      );

      const programs: AwinProgram[] = response.data.map((program: any) => ({
        id: program.id,
        name: program.programName,
        description: program.description || 'Keine Beschreibung verfügbar',
        sector: program.primarySector || 'Unbekannt',
        commissionRate: program.commissionRange?.max || 0,
        cookiePeriod: program.cookiePeriod || 30,
        applicationStatus: program.relationshipStatus
      }));

      console.log(`✅ ${programs.length} AWIN Programme geladen`);
      return programs;

    } catch (error: any) {
      console.error('❌ Fehler beim Laden der AWIN Programme:', error.message);
      return [];
    }
  }

  /**
   * Erstellt Deep Links für Affiliate Marketing
   */
  async createDeepLink(
    programId: number, 
    targetUrl: string, 
    clickRef?: string
  ): Promise<AwinDeepLink | null> {
    try {
      console.log(`🔗 Erstelle Deep Link für Programm ${programId}`);
      
      const params: any = {
        'p': programId,
        'url': targetUrl
      };

      if (clickRef) {
        params.clickRef = clickRef;
      }

      const response = await axios.get(
        `${this.config.baseUrl}/publishers/${this.config.publisherId}/links`,
        {
          headers: this.getHeaders(),
          params
        }
      );

      const deepLink: AwinDeepLink = {
        clickThroughUrl: response.data.clickThroughUrl || targetUrl,
        trackingCode: `awin_${programId}_${Date.now()}`,
        shortenedUrl: response.data.shortenedUrl
      };

      console.log('✅ Deep Link erstellt:', deepLink.clickThroughUrl);
      return deepLink;

    } catch (error: any) {
      console.error('❌ Fehler beim Erstellen des Deep Links:', error.message);
      return null;
    }
  }

  /**
   * Holt Transaktions-/Commission-Daten
   */
  async getTransactions(
    startDate?: Date, 
    endDate?: Date, 
    limit: number = 100
  ): Promise<AwinTransaction[]> {
    try {
      const start = startDate || new Date(Date.now() - 30 * 24 * 60 * 60 * 1000); // 30 Tage zurück
      const end = endDate || new Date();

      console.log(`📊 Lade AWIN Transaktionen von ${start.toISOString().split('T')[0]} bis ${end.toISOString().split('T')[0]}`);

      const response = await axios.get(
        `${this.config.baseUrl}/publishers/${this.config.publisherId}/transactions`,
        {
          headers: this.getHeaders(),
          params: {
            startDate: start.toISOString().split('T')[0],
            endDate: end.toISOString().split('T')[0],
            limit
          }
        }
      );

      const transactions: AwinTransaction[] = response.data.map((transaction: any) => ({
        id: transaction.id,
        clickTime: transaction.clickTime,
        transactionTime: transaction.transactionTime,
        commissionValue: parseFloat(transaction.commissionValue || '0'),
        orderValue: parseFloat(transaction.orderValue || '0'),
        programId: transaction.programId,
        programName: transaction.programName || 'Unbekannt'
      }));

      console.log(`✅ ${transactions.length} Transaktionen geladen`);
      return transactions;

    } catch (error: any) {
      console.error('❌ Fehler beim Laden der Transaktionen:', error.message);
      return [];
    }
  }

  /**
   * Sucht nach profitablen Programmen in spezifischen Nischen
   */
  async findProfitablePrograms(niche: string): Promise<AwinProgram[]> {
    try {
      console.log(`🎯 Suche profitable Programme für Nische: ${niche}`);
      
      // Lade alle Programme
      const allPrograms = await this.getPrograms();
      
      // Filtere nach Nische (einfache Keyword-Suche)
      const nicheKeywords = niche.toLowerCase().split(' ');
      const relevantPrograms = allPrograms.filter(program => {
        const searchText = `${program.name} ${program.description} ${program.sector}`.toLowerCase();
        return nicheKeywords.some(keyword => searchText.includes(keyword));
      });

      // Sortiere nach Commission Rate
      relevantPrograms.sort((a, b) => b.commissionRate - a.commissionRate);

      console.log(`✅ ${relevantPrograms.length} relevante Programme für '${niche}' gefunden`);
      return relevantPrograms.slice(0, 10); // Top 10

    } catch (error: any) {
      console.error('❌ Fehler bei der Programmsuche:', error.message);
      return [];
    }
  }

  /**
   * Generiert einen kompletten Affiliate-Report
   */
  async generateAffiliateReport(): Promise<any> {
    try {
      console.log('📈 Generiere AWIN Affiliate Report...');

      const [programs, transactions] = await Promise.all([
        this.getPrograms(undefined, 50),
        this.getTransactions()
      ]);

      const totalCommissions = transactions.reduce(
        (sum, transaction) => sum + transaction.commissionValue, 
        0
      );

      const totalOrderValue = transactions.reduce(
        (sum, transaction) => sum + transaction.orderValue, 
        0
      );

      const topPrograms = programs
        .filter(p => p.commissionRate > 0)
        .sort((a, b) => b.commissionRate - a.commissionRate)
        .slice(0, 10);

      const report = {
        summary: {
          totalPrograms: programs.length,
          totalTransactions: transactions.length,
          totalCommissions: totalCommissions,
          totalOrderValue: totalOrderValue,
          averageCommissionRate: totalCommissions / totalOrderValue * 100 || 0
        },
        topPrograms,
        recentTransactions: transactions.slice(0, 10),
        generatedAt: new Date().toISOString()
      };

      console.log('✅ AWIN Report generiert');
      console.log(`💰 Total Commissions: €${totalCommissions.toFixed(2)}`);
      console.log(`📊 Total Order Value: €${totalOrderValue.toFixed(2)}`);

      return report;

    } catch (error: any) {
      console.error('❌ Fehler beim Generieren des Reports:', error.message);
      return null;
    }
  }
}

export default AwinService;