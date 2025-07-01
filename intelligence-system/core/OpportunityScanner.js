class OpportunityScanner {
    constructor(db) {
        this.db = db;
        this.scanners = [];
        this.loadScanners();
    }

    loadScanners() {
        // Load available scanners
        try {
            // For now, we'll add scanners manually
            // In production, dynamically load from scanners directory
            console.log('📦 Loading scanners...');
            
            // Mock scanners for testing
            this.scanners = [
                {
                    name: 'Digistore24',
                    scan: async () => this.mockScan('digistore24')
                },
                {
                    name: 'TrendScanner',
                    scan: async () => this.mockScan('trends')
                }
            ];
            
            console.log(`✅ Loaded ${this.scanners.length} scanners`);
        } catch (error) {
            console.error('Error loading scanners:', error);
        }
    }

    async mockScan(source) {
        // Mock scan for testing
        const opportunities = [
            {
                source: source,
                type: 'affiliate',
                title: `High-Converting ${source} Product - ${Date.now()}`,
                description: 'Mock opportunity for testing',
                potential_revenue: Math.floor(Math.random() * 10000),
                competition_level: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)]
            }
        ];
        
        return opportunities;
    }

    async quickScan() {
        console.log('⚡ Starting quick scan...');
        const results = {
            total: 0,
            new: 0,
            errors: []
        };

        // Run first 2 scanners only for quick scan
        const quickScanners = this.scanners.slice(0, 2);
        
        for (const scanner of quickScanners) {
            try {
                console.log(`🔍 Running ${scanner.name} scanner...`);
                const opportunities = await scanner.scan();
                
                for (const opp of opportunities) {
                    await this.saveOpportunity(opp);
                    results.total++;
                    results.new++;
                }
            } catch (error) {
                console.error(`❌ Error in ${scanner.name}:`, error.message);
                results.errors.push({
                    scanner: scanner.name,
                    error: error.message
                });
            }
        }

        console.log(`✅ Quick scan complete: ${results.new} new opportunities found`);
        return results;
    }

    async scanAll() {
        console.log('🔍 Starting full scan...');
        const results = {
            total: 0,
            new: 0,
            errors: []
        };

        for (const scanner of this.scanners) {
            try {
                console.log(`🔍 Running ${scanner.name} scanner...`);
                const opportunities = await scanner.scan();
                
                for (const opp of opportunities) {
                    await this.saveOpportunity(opp);
                    results.total++;
                    results.new++;
                }
            } catch (error) {
                console.error(`❌ Error in ${scanner.name}:`, error.message);
                results.errors.push({
                    scanner: scanner.name,
                    error: error.message
                });
            }
        }

        console.log(`✅ Full scan complete: ${results.new} new opportunities found`);
        return results;
    }

    async saveOpportunity(opportunity) {
        return new Promise((resolve, reject) => {
            const query = `
                INSERT INTO opportunities (source, type, title, description, potential_revenue, competition_level, url, keywords, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;
            
            const params = [
                opportunity.source,
                opportunity.type,
                opportunity.title,
                opportunity.description || null,
                opportunity.potential_revenue || null,
                opportunity.competition_level || null,
                opportunity.url || null,
                opportunity.keywords || null,
                JSON.stringify(opportunity.metadata || {})
            ];
            
            this.db.run(query, params, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.lastID);
                }
            });
        });
    }
}

module.exports = OpportunityScanner;