const Digistore24Scanner = require('../scanners/digistore24-real');
const ClickBankScanner = require('../scanners/clickbank-real');

class OpportunityScanner {
    constructor(db) {
        this.db = db;
        this.scanners = [];
        this.loadScanners();
    }

    loadScanners() {
        console.log('📦 Loading REAL scanners...');
        
        try {
            // Load environment variables
            const digistore24Key = process.env.DIGISTORE24_API_KEY;
            const clickbankKey = process.env.CLICKBANK_API_KEY;
            
            // Initialize real scanners with API keys
            if (digistore24Key && digistore24Key !== 'your_digistore24_api_key_here') {
                this.scanners.push(new Digistore24Scanner(digistore24Key));
                console.log('✅ Digistore24 scanner loaded with API key');
            } else {
                console.log('⚠️  Digistore24 scanner skipped - no valid API key');
            }
            
            if (clickbankKey && clickbankKey !== 'your_clickbank_api_key_here') {
                this.scanners.push(new ClickBankScanner(clickbankKey));
                console.log('✅ ClickBank scanner loaded with API key');
            } else {
                console.log('⚠️  ClickBank scanner skipped - no valid API key');
            }
            
            // Load additional scanners if available
            this.loadAdditionalScanners();
            
            console.log(`✅ Loaded ${this.scanners.length} real scanners`);
            
        } catch (error) {
            console.error('❌ Error loading scanners:', error);
            // Continue with any successfully loaded scanners
        }
    }

    loadAdditionalScanners() {
        // Future: Load social media scanners, trend scanners, etc.
        // Only if API keys are available
    }

    async quickScan() {
        console.log('⚡ Starting quick scan with REAL data...');
        const results = {
            total: 0,
            new: 0,
            errors: [],
            sources: {}
        };

        // Run first 2 scanners only for quick scan
        const quickScanners = this.scanners.slice(0, 2);
        
        for (const scanner of quickScanners) {
            try {
                console.log(`🔍 Running ${scanner.name} scanner...`);
                const startTime = Date.now();
                
                const opportunities = await scanner.scan();
                const scanTime = Date.now() - startTime;
                
                console.log(`⏱️  ${scanner.name} scan completed in ${scanTime}ms`);
                
                // Track results by source
                results.sources[scanner.name] = {
                    found: opportunities.length,
                    new: 0,
                    errors: 0
                };
                
                for (const opp of opportunities) {
                    try {
                        const exists = await this.opportunityExists(opp);
                        if (!exists) {
                            await this.saveOpportunity(opp);
                            results.new++;
                            results.sources[scanner.name].new++;
                        }
                        results.total++;
                    } catch (error) {
                        console.error(`❌ Error saving opportunity:`, error.message);
                        results.sources[scanner.name].errors++;
                    }
                }
                
            } catch (error) {
                console.error(`❌ Error in ${scanner.name}:`, error.message);
                results.errors.push({
                    scanner: scanner.name,
                    error: error.message
                });
            }
        }

        console.log(`✅ Quick scan complete: ${results.new} new opportunities from ${results.total} total`);
        return results;
    }

    async scanAll() {
        console.log('🔍 Starting full scan with ALL real scanners...');
        const results = {
            total: 0,
            new: 0,
            errors: [],
            sources: {}
        };

        for (const scanner of this.scanners) {
            try {
                console.log(`🔍 Running ${scanner.name} scanner...`);
                const startTime = Date.now();
                
                const opportunities = await scanner.scan();
                const scanTime = Date.now() - startTime;
                
                console.log(`⏱️  ${scanner.name} scan completed in ${scanTime}ms`);
                
                // Track results by source
                results.sources[scanner.name] = {
                    found: opportunities.length,
                    new: 0,
                    errors: 0
                };
                
                for (const opp of opportunities) {
                    try {
                        const exists = await this.opportunityExists(opp);
                        if (!exists) {
                            await this.saveOpportunity(opp);
                            results.new++;
                            results.sources[scanner.name].new++;
                        }
                        results.total++;
                    } catch (error) {
                        console.error(`❌ Error saving opportunity:`, error.message);
                        results.sources[scanner.name].errors++;
                    }
                }
                
            } catch (error) {
                console.error(`❌ Error in ${scanner.name}:`, error.message);
                results.errors.push({
                    scanner: scanner.name,
                    error: error.message
                });
            }
        }

        console.log(`✅ Full scan complete: ${results.new} new opportunities from ${results.total} total`);
        this.logScanSummary(results);
        return results;
    }

    async opportunityExists(opportunity) {
        return new Promise((resolve, reject) => {
            // Check if opportunity already exists based on source and title
            this.db.get(
                'SELECT id FROM opportunities WHERE source = ? AND title = ?',
                [opportunity.source, opportunity.title],
                (err, row) => {
                    if (err) reject(err);
                    else resolve(!!row);
                }
            );
        });
    }

    async saveOpportunity(opportunity) {
        return new Promise((resolve, reject) => {
            const query = `
                INSERT INTO opportunities (
                    source, type, title, description, url, 
                    potential_revenue, competition_level, keywords, metadata,
                    score, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;
            
            // Calculate initial score
            const score = this.calculateOpportunityScore(opportunity);
            
            const params = [
                opportunity.source,
                opportunity.type,
                opportunity.title,
                opportunity.description || null,
                opportunity.url || null,
                opportunity.potential_revenue || 0,
                opportunity.competition_level || 'unknown',
                opportunity.keywords || null,
                JSON.stringify(opportunity.metadata || {}),
                score,
                'new'
            ];
            
            this.db.run(query, params, function(err) {
                if (err) {
                    reject(err);
                } else {
                    console.log(`💾 Saved: ${opportunity.title} (Score: ${score})`);
                    resolve(this.lastID);
                }
            });
        });
    }

    calculateOpportunityScore(opportunity) {
        let score = 50; // Base score
        
        // Revenue potential factor (0-30 points)
        const revenue = opportunity.potential_revenue || 0;
        if (revenue > 10000) score += 30;
        else if (revenue > 5000) score += 20;
        else if (revenue > 1000) score += 10;
        
        // Competition factor (0-20 points)
        const competition = opportunity.competition_level || 'unknown';
        if (competition === 'low') score += 20;
        else if (competition === 'medium') score += 10;
        else if (competition === 'high') score += 5;
        
        // Metadata factors (0-50 points)
        const metadata = opportunity.metadata || {};
        
        // Gravity/popularity factor
        const gravity = parseFloat(metadata.gravity) || 0;
        if (gravity > 200) score += 20;
        else if (gravity > 100) score += 15;
        else if (gravity > 50) score += 10;
        
        // Commission factor
        const commission = parseFloat(metadata.commission_rate || metadata.commission) || 0;
        if (commission > 60) score += 15;
        else if (commission > 40) score += 10;
        else if (commission > 20) score += 5;
        
        // Recurring revenue bonus
        if (metadata.recurring) score += 15;
        
        return Math.min(100, Math.max(0, score));
    }

    logScanSummary(results) {
        console.log('\n📊 Scan Summary:');
        console.log('================');
        
        Object.entries(results.sources).forEach(([source, data]) => {
            console.log(`\n${source}:`);
            console.log(`  - Found: ${data.found} opportunities`);
            console.log(`  - New: ${data.new} saved`);
            if (data.errors > 0) {
                console.log(`  - Errors: ${data.errors}`);
            }
        });
        
        if (results.errors.length > 0) {
            console.log('\n⚠️  Errors encountered:');
            results.errors.forEach(err => {
                console.log(`  - ${err.scanner}: ${err.error}`);
            });
        }
        
        console.log('\n================');
    }
}

module.exports = OpportunityScanner;