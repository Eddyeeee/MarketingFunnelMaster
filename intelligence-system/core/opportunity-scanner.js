const EventEmitter = require('events');
const { ProfitabilityAnalyzer } = require('../analyzers/profitability-analyzer');
const { TrendVelocityAnalyzer } = require('../analyzers/trend-velocity-analyzer');

class OpportunityScanner extends EventEmitter {
    constructor(config = {}) {
        super();
        this.config = {
            scanInterval: config.scanInterval || 300000, // 5 minutes
            minScore: config.minScore || 70,
            maxConcurrentScans: config.maxConcurrentScans || 5,
            ...config
        };
        
        this.scanners = new Map();
        this.activeOpportunities = new Map();
        this.profitabilityAnalyzer = new ProfitabilityAnalyzer();
        this.trendVelocityAnalyzer = new TrendVelocityAnalyzer();
        this.isScanning = false;
        this.scanQueue = [];
    }

    registerScanner(name, scannerInstance) {
        if (!scannerInstance.scan || typeof scannerInstance.scan !== 'function') {
            throw new Error(`Scanner ${name} must implement scan() method`);
        }
        
        this.scanners.set(name, scannerInstance);
        this.emit('scannerRegistered', { name, scanner: scannerInstance });
    }

    async startScanning() {
        if (this.isScanning) {
            return;
        }

        this.isScanning = true;
        this.emit('scanningStarted');
        
        // Initial scan
        await this.performScan();
        
        // Schedule periodic scans
        this.scanTimer = setInterval(async () => {
            await this.performScan();
        }, this.config.scanInterval);
    }

    async stopScanning() {
        this.isScanning = false;
        if (this.scanTimer) {
            clearInterval(this.scanTimer);
        }
        this.emit('scanningStopped');
    }

    async performScan() {
        const scanPromises = [];
        const scannerEntries = Array.from(this.scanners.entries());
        
        // Limit concurrent scans
        for (let i = 0; i < Math.min(scannerEntries.length, this.config.maxConcurrentScans); i++) {
            const [name, scanner] = scannerEntries[i];
            scanPromises.push(this.runScannerSafely(name, scanner));
        }

        const results = await Promise.allSettled(scanPromises);
        const opportunities = [];

        results.forEach((result, index) => {
            if (result.status === 'fulfilled' && result.value) {
                opportunities.push(...(Array.isArray(result.value) ? result.value : [result.value]));
            } else if (result.status === 'rejected') {
                const scannerName = scannerEntries[index][0];
                this.emit('scanError', { scanner: scannerName, error: result.reason });
            }
        });

        await this.processOpportunities(opportunities);
    }

    async runScannerSafely(name, scanner) {
        try {
            const startTime = Date.now();
            const result = await scanner.scan();
            const duration = Date.now() - startTime;
            
            this.emit('scanCompleted', { 
                scanner: name, 
                duration, 
                opportunitiesFound: Array.isArray(result) ? result.length : (result ? 1 : 0)
            });
            
            return result;
        } catch (error) {
            this.emit('scanError', { scanner: name, error });
            return null;
        }
    }

    async processOpportunities(opportunities) {
        const scoredOpportunities = [];

        for (const opportunity of opportunities) {
            try {
                const score = await this.scoreOpportunity(opportunity);
                
                if (score >= this.config.minScore) {
                    const enrichedOpportunity = {
                        ...opportunity,
                        score,
                        discoveredAt: new Date().toISOString(),
                        id: this.generateOpportunityId(opportunity)
                    };
                    
                    scoredOpportunities.push(enrichedOpportunity);
                    this.activeOpportunities.set(enrichedOpportunity.id, enrichedOpportunity);
                }
            } catch (error) {
                this.emit('scoringError', { opportunity, error });
            }
        }

        if (scoredOpportunities.length > 0) {
            // Sort by score descending
            scoredOpportunities.sort((a, b) => b.score - a.score);
            this.emit('opportunitiesFound', scoredOpportunities);
        }
    }

    async scoreOpportunity(opportunity) {
        const weights = {
            profitability: 0.4,
            trendVelocity: 0.3,
            timing: 0.2,
            competition: 0.1
        };

        const scores = {};
        
        // Profitability scoring
        scores.profitability = await this.profitabilityAnalyzer.analyze(opportunity);
        
        // Trend velocity scoring
        scores.trendVelocity = await this.trendVelocityAnalyzer.analyze(opportunity);
        
        // Timing scoring (seasonal, market conditions)
        scores.timing = this.scoreTimingFactor(opportunity);
        
        // Competition scoring
        scores.competition = this.scoreCompetitionFactor(opportunity);

        // Calculate weighted score
        const weightedScore = Object.entries(scores).reduce((total, [factor, score]) => {
            return total + (score * weights[factor]);
        }, 0);

        return Math.round(weightedScore);
    }

    scoreTimingFactor(opportunity) {
        const now = new Date();
        const currentMonth = now.getMonth();
        const currentDay = now.getDate();
        
        let timingScore = 50; // Base score
        
        // Seasonal boost
        if (opportunity.seasonality) {
            const seasonalMonths = opportunity.seasonality.peakMonths || [];
            if (seasonalMonths.includes(currentMonth)) {
                timingScore += 30;
            }
        }
        
        // Event-based timing
        if (opportunity.eventTiming) {
            const daysToEvent = this.calculateDaysToEvent(opportunity.eventTiming);
            if (daysToEvent <= 30 && daysToEvent >= 0) {
                timingScore += Math.max(0, 40 - daysToEvent);
            }
        }
        
        // Market condition factor
        if (opportunity.marketConditions) {
            timingScore += this.evaluateMarketConditions(opportunity.marketConditions);
        }
        
        return Math.min(100, timingScore);
    }

    scoreCompetitionFactor(opportunity) {
        let competitionScore = 70; // Base score assuming moderate competition
        
        if (opportunity.competition) {
            const { level, saturation, barriers } = opportunity.competition;
            
            // Competition level impact
            switch (level) {
                case 'low': competitionScore += 20; break;
                case 'medium': competitionScore += 0; break;
                case 'high': competitionScore -= 20; break;
            }
            
            // Market saturation impact
            if (saturation) {
                competitionScore -= Math.min(30, saturation * 0.3);
            }
            
            // Entry barriers (higher barriers = less competition)
            if (barriers && barriers.length > 0) {
                competitionScore += barriers.length * 5;
            }
        }
        
        return Math.max(0, Math.min(100, competitionScore));
    }

    calculateDaysToEvent(eventTiming) {
        const eventDate = new Date(eventTiming);
        const now = new Date();
        const diffTime = eventDate - now;
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    evaluateMarketConditions(conditions) {
        let score = 0;
        
        if (conditions.trend === 'growing') score += 15;
        if (conditions.trend === 'stable') score += 5;
        if (conditions.trend === 'declining') score -= 10;
        
        if (conditions.volatility === 'low') score += 10;
        if (conditions.volatility === 'high') score -= 5;
        
        return score;
    }

    generateOpportunityId(opportunity) {
        const source = opportunity.source || 'unknown';
        const type = opportunity.type || 'general';
        const timestamp = Date.now();
        const hash = this.simpleHash(`${source}-${type}-${JSON.stringify(opportunity)}`);
        return `opp_${source}_${hash}_${timestamp}`;
    }

    simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash).toString(16).substring(0, 8);
    }

    getActiveOpportunities() {
        return Array.from(this.activeOpportunities.values())
            .sort((a, b) => b.score - a.score);
    }

    getOpportunity(id) {
        return this.activeOpportunities.get(id);
    }

    removeOpportunity(id) {
        const removed = this.activeOpportunities.delete(id);
        if (removed) {
            this.emit('opportunityRemoved', { id });
        }
        return removed;
    }

    getStats() {
        const opportunities = this.getActiveOpportunities();
        return {
            totalOpportunities: opportunities.length,
            averageScore: opportunities.length > 0 
                ? opportunities.reduce((sum, opp) => sum + opp.score, 0) / opportunities.length 
                : 0,
            highScoreOpportunities: opportunities.filter(opp => opp.score >= 80).length,
            scannerCount: this.scanners.size,
            isScanning: this.isScanning,
            lastScan: this.lastScanTime
        };
    }
}

module.exports = { OpportunityScanner };