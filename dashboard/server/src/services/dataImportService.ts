import fs from 'fs/promises';
import path from 'path';
import { logger } from '../utils/logger';
import { cacheSet, cacheGet } from '../redis/client';

// Type definitions for research data
export interface NicheAnalysis {
  niche_id: string;
  niche_name: string;
  description: string;
  priority_score: number;
  implementation_difficulty: number;
  roi_projection: {
    conservative: number;
    realistic: number;
    optimistic: number;
  };
  quick_win_opportunities: string[];
  automation_ready_score: number;
  market_saturation_index: number;
  competition_intensity_score: number;
  virality_potential_score: number;
  scalability_score: number;
  risk_assessment_score: number;
}

export interface Persona {
  persona_id: string;
  persona_name: string;
  niche_id: string;
  age_range: string;
  psychographics: {
    personality_types: string[];
    values: string[];
    interests: string[];
  };
  behavioral_triggers: string[];
  emotional_states: string[];
  device_usage: {
    mobile: number;
    desktop: number;
    tablet: number;
  };
}

export interface MetricsDashboard {
  [niche_id: string]: {
    health_score: number;
    alert_thresholds: {
      conversion_rate_min: number;
      bounce_rate_max: number;
    };
    performance_triggers: {
      [trigger_name: string]: string;
    };
    optimization_priorities: string[];
    investment_priority_rank: number;
  };
}

export interface ImplementationRoadmap {
  phase: string;
  [key: string]: any; // Dynamic milestone properties
}

export interface ResearchDataset {
  niches: NicheAnalysis[];
  personas: Persona[];
  metrics: MetricsDashboard;
  roadmaps: ImplementationRoadmap[];
  summary: {
    totalNiches: number;
    averagePriorityScore: number;
    totalConservativeROI: number;
    totalRealisticROI: number;
    totalOptimisticROI: number;
    highAutomationReadyCount: number;
    lowRiskHighRewardCount: number;
  };
}

class DataImportService {
  private researchDataPath: string;
  private cacheKey = 'research:dataset:all';
  private cacheTTL = 3600; // 1 hour

  constructor() {
    // Path to intelligence-system research data relative to dashboard
    this.researchDataPath = path.resolve(__dirname, '../../../../intelligence-system/research-data');
  }

  /**
   * Import and merge all research data from intelligence system
   */
  async importResearchData(): Promise<ResearchDataset> {
    try {
      logger.info(`Starting research data import from path: ${this.researchDataPath}`);

      // Check cache first
      const cached = await cacheGet<ResearchDataset>(this.cacheKey);
      if (cached) {
        logger.info('Returning cached research data');
        return cached;
      }

      // Import all data types
      const [niches, personas, metrics, roadmaps] = await Promise.all([
        this.importNicheAnalysis(),
        this.importPersonas(),
        this.importMetrics(),
        this.importRoadmaps()
      ]);

      logger.info(`Data imported: ${niches.length} niches, ${personas.length} personas, ${Object.keys(metrics).length} metrics, ${roadmaps.length} roadmaps`);

      // Generate summary statistics
      const summary = this.generateSummary(niches, metrics);

      const dataset: ResearchDataset = {
        niches,
        personas,
        metrics,
        roadmaps,
        summary
      };

      // Cache the merged dataset
      await cacheSet(this.cacheKey, dataset, this.cacheTTL);

      logger.info(`Research data import completed successfully`);
      return dataset;

    } catch (error) {
      logger.error('Failed to import research data:', error);
      throw new Error(`Research data import failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Import and merge all niche analysis files (4 batches)
   */
  private async importNicheAnalysis(): Promise<NicheAnalysis[]> {
    const files = [
      'niche-analysis-2025-01.json',
      'niche-analysis-2025-batch-2.json',
      'niche-analysis-2025-batch-3.json',
      'niche-analysis-2025-batch-4.json'
    ];

    const allNiches: NicheAnalysis[] = [];

    for (const file of files) {
      try {
        const filePath = path.join(this.researchDataPath, file);
        logger.info(`Attempting to read file: ${filePath}`);
        
        // Check if file exists first
        await fs.access(filePath);
        
        const data = await fs.readFile(filePath, 'utf-8');
        const niches = JSON.parse(data) as NicheAnalysis[];
        logger.info(`Successfully loaded ${niches.length} niches from ${file}`);
        allNiches.push(...niches);
      } catch (error) {
        logger.warn(`Failed to read niche analysis file ${file}:`, error instanceof Error ? error.message : String(error));
      }
    }

    logger.info(`Total niches loaded: ${allNiches.length}`);
    return allNiches;
  }

  /**
   * Import and merge all persona files (4 batches)
   */
  private async importPersonas(): Promise<Persona[]> {
    const files = [
      'personas-detailed.json',
      'personas-detailed-batch-2.json',
      'personas-detailed-batch-3.json',
      'personas-detailed-batch-4.json'
    ];

    const allPersonas: Persona[] = [];

    for (const file of files) {
      try {
        const filePath = path.join(this.researchDataPath, file);
        const data = await fs.readFile(filePath, 'utf-8');
        const personas = JSON.parse(data) as Persona[];
        allPersonas.push(...personas);
      } catch (error) {
        logger.warn(`Failed to read personas file ${file}:`, error);
      }
    }

    return allPersonas;
  }

  /**
   * Import and merge all metrics dashboard files (4 batches)
   */
  private async importMetrics(): Promise<MetricsDashboard> {
    const files = [
      'metrics-dashboard.json',
      'metrics-dashboard-batch-2.json',
      'metrics-dashboard-batch-3.json',
      'metrics-dashboard-batch-4.json'
    ];

    const mergedMetrics: MetricsDashboard = {};

    for (const file of files) {
      try {
        const filePath = path.join(this.researchDataPath, file);
        const data = await fs.readFile(filePath, 'utf-8');
        const metrics = JSON.parse(data) as MetricsDashboard;
        Object.assign(mergedMetrics, metrics);
      } catch (error) {
        logger.warn(`Failed to read metrics file ${file}:`, error);
      }
    }

    return mergedMetrics;
  }

  /**
   * Import and merge all implementation roadmap files (4 batches)
   */
  private async importRoadmaps(): Promise<ImplementationRoadmap[]> {
    const files = [
      'implementation-roadmap.json',
      'implementation-roadmap-batch-2.json',
      'implementation-roadmap-batch-3.json',
      'implementation-roadmap-batch-4.json'
    ];

    const allRoadmaps: ImplementationRoadmap[] = [];

    for (const file of files) {
      try {
        const filePath = path.join(this.researchDataPath, file);
        const data = await fs.readFile(filePath, 'utf-8');
        const roadmapData = JSON.parse(data);
        
        // Convert the roadmap data to our expected format
        const roadmap: ImplementationRoadmap = {
          phase: file.includes('batch-2') ? 'Phase 2' :
                 file.includes('batch-3') ? 'Phase 3' :
                 file.includes('batch-4') ? 'Phase 4' : 'Phase 1',
          ...roadmapData
        };
        
        allRoadmaps.push(roadmap);
      } catch (error) {
        logger.warn(`Failed to read roadmap file ${file}:`, error instanceof Error ? error.message : String(error));
      }
    }

    logger.info(`Total roadmaps loaded: ${allRoadmaps.length}`);
    return allRoadmaps;
  }

  /**
   * Generate summary statistics from imported data
   */
  private generateSummary(niches: NicheAnalysis[], _metrics: MetricsDashboard): ResearchDataset['summary'] {
    const totalNiches = niches.length;
    const averagePriorityScore = totalNiches > 0 ? 
      Math.round(niches.reduce((sum, n) => sum + (n.priority_score || 0), 0) / totalNiches) : 0;

    const totalConservativeROI = niches.reduce((sum, n) => sum + (n.roi_projection?.conservative || 0), 0);
    const totalRealisticROI = niches.reduce((sum, n) => sum + (n.roi_projection?.realistic || 0), 0);
    const totalOptimisticROI = niches.reduce((sum, n) => sum + (n.roi_projection?.optimistic || 0), 0);

    const highAutomationReadyCount = niches.filter(n => (n.automation_ready_score || 0) >= 8).length;
    const lowRiskHighRewardCount = niches.filter(n => 
      (n.risk_assessment_score || 100) <= 30 && (n.roi_projection?.realistic || 0) >= 100000
    ).length;

    return {
      totalNiches,
      averagePriorityScore,
      totalConservativeROI,
      totalRealisticROI,
      totalOptimisticROI,
      highAutomationReadyCount,
      lowRiskHighRewardCount
    };
  }

  /**
   * Get niches filtered by criteria
   */
  async getFilteredNiches(filters: {
    minPriorityScore?: number;
    maxRisk?: number;
    minROI?: number;
    minAutomationScore?: number;
  }): Promise<NicheAnalysis[]> {
    const dataset = await this.importResearchData();
    let filtered = dataset.niches;

    if (filters.minPriorityScore !== undefined) {
      filtered = filtered.filter(n => n.priority_score >= filters.minPriorityScore!);
    }

    if (filters.maxRisk !== undefined) {
      filtered = filtered.filter(n => n.risk_assessment_score <= filters.maxRisk!);
    }

    if (filters.minROI !== undefined) {
      filtered = filtered.filter(n => n.roi_projection.realistic >= filters.minROI!);
    }

    if (filters.minAutomationScore !== undefined) {
      filtered = filtered.filter(n => n.automation_ready_score >= filters.minAutomationScore!);
    }

    return filtered;
  }

  /**
   * Get persona data for specific niche
   */
  async getPersonaForNiche(nicheId: string): Promise<Persona | null> {
    const dataset = await this.importResearchData();
    return dataset.personas.find(p => p.niche_id === nicheId) || null;
  }

  /**
   * Get metrics for specific niche
   */
  async getMetricsForNiche(nicheId: string): Promise<MetricsDashboard[string] | null> {
    const dataset = await this.importResearchData();
    return dataset.metrics[nicheId] || null;
  }

  /**
   * Force refresh cache by reimporting data
   */
  async refreshData(): Promise<ResearchDataset> {
    await cacheSet(this.cacheKey, null, 0); // Clear cache
    return this.importResearchData();
  }
}

// Export singleton instance
export const dataImportService = new DataImportService();