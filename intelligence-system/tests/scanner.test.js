const { OpportunityScanner } = require('../core/opportunity-scanner');
const { ProfitabilityAnalyzer } = require('../analyzers/profitability-analyzer');
const { TrendVelocityAnalyzer } = require('../analyzers/trend-velocity-analyzer');

// Mock scanner for testing
class MockScanner {
    constructor(mockData = []) {
        this.mockData = mockData;
        this.scanCount = 0;
    }

    async scan() {
        this.scanCount++;
        return this.mockData;
    }
}

describe('OpportunityScanner', () => {
    let scanner;
    
    beforeEach(() => {
        scanner = new OpportunityScanner({
            scanInterval: 1000,
            minScore: 50,
            maxConcurrentScans: 2
        });
    });

    afterEach(async () => {
        if (scanner.isScanning) {
            await scanner.stopScanning();
        }
    });

    describe('Scanner Registration', () => {
        test('should register a scanner correctly', () => {
            const mockScanner = new MockScanner();
            scanner.registerScanner('test', mockScanner);
            
            expect(scanner.scanners.has('test')).toBe(true);
            expect(scanner.scanners.get('test')).toBe(mockScanner);
        });

        test('should throw error for invalid scanner', () => {
            const invalidScanner = {};
            
            expect(() => {
                scanner.registerScanner('invalid', invalidScanner);
            }).toThrow('Scanner invalid must implement scan() method');
        });

        test('should emit scannerRegistered event', (done) => {
            const mockScanner = new MockScanner();
            
            scanner.on('scannerRegistered', (event) => {
                expect(event.name).toBe('test');
                expect(event.scanner).toBe(mockScanner);
                done();
            });
            
            scanner.registerScanner('test', mockScanner);
        });
    });

    describe('Opportunity Processing', () => {
        test('should process opportunities and calculate scores', async () => {
            const mockOpportunity = {
                id: 'test-opp-1',
                title: 'Test Opportunity',
                source: 'test_scanner',
                type: 'test_type',
                category: 'business',
                metrics: {
                    commission_rate: 0.3,
                    gravity: 75,
                    conversion_rate: 0.05
                }
            };

            const mockScanner = new MockScanner([mockOpportunity]);
            scanner.registerScanner('test', mockScanner);

            const opportunities = await scanner.performScan();
            
            expect(Array.isArray(opportunities)).toBe(true);
            expect(opportunities.length).toBeGreaterThan(0);
            
            const processedOpp = opportunities[0];
            expect(processedOpp.score).toBeGreaterThan(0);
            expect(processedOpp.discoveredAt).toBeDefined();
            expect(processedOpp.id).toBeDefined();
        });

        test('should filter opportunities by minimum score', async () => {
            scanner = new OpportunityScanner({ minScore: 90 });
            
            const lowScoreOpportunity = {
                id: 'low-score',
                title: 'Low Score Opportunity',
                source: 'test_scanner',
                category: 'business',
                metrics: { commission_rate: 0.05 } // Low commission
            };

            const mockScanner = new MockScanner([lowScoreOpportunity]);
            scanner.registerScanner('test', mockScanner);

            const opportunities = await scanner.performScan();
            
            // Should be filtered out due to low score
            expect(opportunities.length).toBe(0);
        });

        test('should handle scanner errors gracefully', async () => {
            const errorScanner = {
                scan: async () => {
                    throw new Error('Scanner failed');
                }
            };

            scanner.registerScanner('error', errorScanner);

            let errorEmitted = false;
            scanner.on('scanError', (event) => {
                expect(event.scanner).toBe('error');
                expect(event.error).toBeInstanceOf(Error);
                errorEmitted = true;
            });

            await scanner.performScan();
            expect(errorEmitted).toBe(true);
        });
    });

    describe('Opportunity Scoring', () => {
        test('should calculate opportunity score correctly', async () => {
            const opportunity = {
                source: 'affiliate_scanner',
                category: 'finance',
                metrics: {
                    commission_rate: 0.4,
                    gravity: 80,
                    conversion_rate: 0.06
                },
                marketConditions: { trend: 'growing' }
            };

            const score = await scanner.scoreOpportunity(opportunity);
            
            expect(score).toBeGreaterThan(0);
            expect(score).toBeLessThanOrEqual(100);
        });

        test('should apply timing factor correctly', () => {
            const opportunity = {
                seasonality: { peakMonths: [new Date().getMonth()] }
            };

            const timingScore = scanner.scoreTimingFactor(opportunity);
            
            expect(timingScore).toBeGreaterThan(50); // Should get seasonal boost
        });

        test('should apply competition factor correctly', () => {
            const highCompetitionOpp = {
                competition: { level: 'high', saturation: 80 }
            };
            
            const lowCompetitionOpp = {
                competition: { level: 'low', saturation: 20 }
            };

            const highCompScore = scanner.scoreCompetitionFactor(highCompetitionOpp);
            const lowCompScore = scanner.scoreCompetitionFactor(lowCompetitionOpp);
            
            expect(lowCompScore).toBeGreaterThan(highCompScore);
        });
    });

    describe('Active Opportunities Management', () => {
        test('should store and retrieve active opportunities', async () => {
            const mockOpportunity = {
                id: 'test-active-1',
                title: 'Active Test Opportunity',
                source: 'test_scanner',
                category: 'business',
                metrics: { commission_rate: 0.25 }
            };

            const mockScanner = new MockScanner([mockOpportunity]);
            scanner.registerScanner('test', mockScanner);

            await scanner.performScan();
            
            const activeOpportunities = scanner.getActiveOpportunities();
            expect(activeOpportunities.length).toBeGreaterThan(0);
            
            const storedOpp = scanner.getOpportunity('test-active-1');
            expect(storedOpp).toBeDefined();
            expect(storedOpp.title).toBe('Active Test Opportunity');
        });

        test('should remove opportunities correctly', async () => {
            const mockOpportunity = {
                id: 'test-remove-1',
                title: 'Remove Test Opportunity',
                source: 'test_scanner',
                category: 'business',
                metrics: { commission_rate: 0.25 }
            };

            const mockScanner = new MockScanner([mockOpportunity]);
            scanner.registerScanner('test', mockScanner);

            await scanner.performScan();
            
            expect(scanner.getOpportunity('test-remove-1')).toBeDefined();
            
            const removed = scanner.removeOpportunity('test-remove-1');
            expect(removed).toBe(true);
            expect(scanner.getOpportunity('test-remove-1')).toBeUndefined();
        });
    });

    describe('Statistics and Monitoring', () => {
        test('should provide accurate statistics', async () => {
            const mockOpportunities = [
                {
                    id: 'stats-test-1',
                    title: 'High Score Opportunity',
                    source: 'test_scanner',
                    category: 'business',
                    metrics: { commission_rate: 0.4 } // High score
                },
                {
                    id: 'stats-test-2',
                    title: 'Medium Score Opportunity',
                    source: 'test_scanner',
                    category: 'business',
                    metrics: { commission_rate: 0.2 } // Medium score
                }
            ];

            const mockScanner = new MockScanner(mockOpportunities);
            scanner.registerScanner('test', mockScanner);

            await scanner.performScan();
            
            const stats = scanner.getStats();
            expect(stats.totalOpportunities).toBeGreaterThan(0);
            expect(stats.averageScore).toBeGreaterThan(0);
            expect(stats.scannerCount).toBe(1);
            expect(stats.isScanning).toBe(false);
        });
    });

    describe('Scanning Lifecycle', () => {
        test('should start and stop scanning correctly', async () => {
            const mockScanner = new MockScanner([]);
            scanner.registerScanner('test', mockScanner);

            expect(scanner.isScanning).toBe(false);
            
            let scanningStarted = false;
            scanner.on('scanningStarted', () => {
                scanningStarted = true;
            });

            await scanner.startScanning();
            expect(scanner.isScanning).toBe(true);
            expect(scanningStarted).toBe(true);

            let scanningStopped = false;
            scanner.on('scanningStopped', () => {
                scanningStopped = true;
            });

            await scanner.stopScanning();
            expect(scanner.isScanning).toBe(false);
            expect(scanningStopped).toBe(true);
        });
    });
});

describe('ProfitabilityAnalyzer', () => {
    let analyzer;

    beforeEach(() => {
        analyzer = new ProfitabilityAnalyzer();
    });

    describe('Revenue Calculation', () => {
        test('should calculate affiliate revenue correctly', () => {
            const opportunity = {
                source: 'affiliate_scanner',
                category: 'finance',
                metrics: {
                    commissionRate: 0.3,
                    price: 200,
                    conversion_rate: 0.04,
                    gravity: 60
                }
            };

            const revenue = analyzer.calculateRevenue(opportunity);
            
            expect(revenue.commissionRate).toBe(0.3);
            expect(revenue.productPrice).toBe(200);
            expect(revenue.monthlyRevenue).toBeGreaterThan(0);
            expect(revenue.annualRevenue).toBe(revenue.monthlyRevenue * 12);
        });

        test('should calculate social trend revenue correctly', () => {
            const opportunity = {
                source: 'social_trend_scanner',
                category: 'business',
                metrics: {
                    total_engagement: 15000,
                    trend_velocity: 0.6
                }
            };

            const revenue = analyzer.calculateRevenue(opportunity);
            
            expect(revenue.monthlyRevenue).toBeGreaterThan(0);
            expect(revenue.revenueConfidence).toBe(0.6);
        });
    });

    describe('Cost Calculation', () => {
        test('should calculate costs for different strategies', () => {
            const opportunity = {
                category: 'business',
                metrics: {}
            };

            const costs = analyzer.calculateCosts(opportunity);
            
            expect(costs.organic).toBeDefined();
            expect(costs.paid).toBeDefined();
            expect(costs.social).toBeDefined();
            expect(costs.recommended).toBeDefined();
            
            expect(costs.organic.totalMonthlyCost).toBeGreaterThan(0);
            expect(costs.paid.totalMonthlyCost).toBeGreaterThan(0);
            expect(costs.social.totalMonthlyCost).toBeGreaterThan(0);
        });
    });

    describe('Risk Assessment', () => {
        test('should assess market risk correctly', () => {
            const opportunity = {
                category: 'finance', // High-risk category
                metrics: {
                    competition_level: 85,
                    market_demand: 30
                }
            };

            const riskAssessment = analyzer.assessRisk(opportunity, {
                metrics: { roi: 150, paybackPeriod: 6, profitMargin: 25 }
            });

            expect(riskAssessment.overall.score).toBeGreaterThan(0);
            expect(riskAssessment.breakdown.market).toBeDefined();
            expect(riskAssessment.breakdown.competition).toBeDefined();
            expect(riskAssessment.mitigationStrategies.length).toBeGreaterThan(0);
        });
    });
});

describe('TrendVelocityAnalyzer', () => {
    let analyzer;

    beforeEach(() => {
        analyzer = new TrendVelocityAnalyzer();
    });

    describe('Velocity Calculation', () => {
        test('should calculate social trend velocity correctly', async () => {
            const opportunity = {
                source: 'social_trend_scanner',
                id: 'test-social-velocity',
                metrics: {
                    trend_velocity: 0.7,
                    total_engagement: 25000,
                    viral_potential: 0.8,
                    platform: 'twitter'
                }
            };

            const analysis = await analyzer.analyze(opportunity);
            
            expect(analysis.score).toBeGreaterThan(0);
            expect(analysis.velocity.overall).toBe(0.7);
            expect(analysis.velocity.direction).toBeDefined();
            expect(analysis.momentum.strength).toBeGreaterThan(0);
        });

        test('should calculate affiliate velocity correctly', async () => {
            const opportunity = {
                source: 'affiliate_scanner',
                id: 'test-affiliate-velocity',
                discovered_at: new Date().toISOString(),
                metrics: {
                    gravity: 75,
                    sales_count: 500,
                    commission_rate: 0.35,
                    network: 'digistore24'
                }
            };

            const analysis = await analyzer.analyze(opportunity);
            
            expect(analysis.score).toBeGreaterThan(0);
            expect(analysis.velocity.consistency).toBe(0.8); // Affiliates are consistent
            expect(analysis.velocity.rawMetrics.gravity).toBe(75);
        });
    });

    describe('Momentum Analysis', () => {
        test('should identify momentum indicators correctly', () => {
            const opportunity = {
                source: 'social_trend_scanner'
            };

            const velocityData = {
                overall: 0.8,
                acceleration: 0.4,
                consistency: 0.9,
                rawMetrics: {
                    viralPotential: 0.7,
                    engagement: 15000
                }
            };

            const momentum = analyzer.analyzeMomentum(opportunity, velocityData);
            
            expect(momentum.strength).toBeGreaterThan(0);
            expect(momentum.indicators).toContain('high_velocity');
            expect(momentum.indicators).toContain('accelerating');
            expect(momentum.indicators).toContain('consistent_growth');
            expect(momentum.indicators).toContain('viral_potential');
        });

        test('should generate appropriate momentum signals', () => {
            const velocityData = {
                overall: 0.8,
                acceleration: 0.3,
                direction: 'up',
                shortTerm: 0.9,
                longTerm: 0.7
            };

            const momentum = {
                strength: 75,
                direction: 'up'
            };

            const signals = analyzer.generateMomentumSignals(velocityData, momentum);
            
            expect(signals.length).toBeGreaterThan(0);
            expect(signals[0].type).toBe('strong_buy');
            expect(signals[0].confidence).toBeGreaterThan(0.5);
        });
    });

    describe('Volatility Calculation', () => {
        test('should calculate volatility metrics correctly', () => {
            const opportunity = {
                source: 'social_trend_scanner'
            };

            const velocityData = {
                shortTerm: 0.9,
                longTerm: 0.5,
                acceleration: 0.3,
                consistency: 0.6
            };

            const volatility = analyzer.calculateVolatility(opportunity, velocityData);
            
            expect(volatility.level).toBeGreaterThan(0);
            expect(volatility.risk).toBeDefined();
            expect(volatility.predictability).toBeGreaterThan(0);
            expect(volatility.factors).toContain('social_media_volatility');
        });
    });

    describe('Predictive Scoring', () => {
        test('should generate realistic predictions', () => {
            const velocityData = {
                shortTerm: 0.8,
                mediumTerm: 0.7,
                longTerm: 0.6,
                acceleration: 0.2,
                consistency: 0.8
            };

            const momentum = {
                strength: 70,
                sustainability: 65,
                direction: 'up'
            };

            const volatility = {
                level: 0.3
            };

            const prediction = analyzer.generatePredictiveScore(velocityData, momentum, volatility);
            
            expect(prediction.overall).toBeGreaterThan(0);
            expect(prediction.shortTerm.confidence).toBeGreaterThan(0);
            expect(prediction.mediumTerm.confidence).toBeGreaterThan(0);
            expect(prediction.longTerm.confidence).toBeGreaterThan(0);
            
            // Short-term should have higher confidence than long-term
            expect(prediction.shortTerm.confidence).toBeGreaterThan(prediction.longTerm.confidence);
        });
    });
});

describe('Integration Tests', () => {
    test('should work with complete opportunity lifecycle', async () => {
        const scanner = new OpportunityScanner({ minScore: 60 });
        
        const mockOpportunity = {
            id: 'integration-test-1',
            title: 'Integration Test Opportunity',
            source: 'affiliate_scanner',
            category: 'finance',
            metrics: {
                commission_rate: 0.35,
                price: 250,
                gravity: 70,
                conversion_rate: 0.05
            }
        };

        const mockScanner = new MockScanner([mockOpportunity]);
        scanner.registerScanner('integration', mockScanner);

        // Perform scan
        await scanner.performScan();
        
        // Check that opportunity was processed
        const opportunities = scanner.getActiveOpportunities();
        expect(opportunities.length).toBeGreaterThan(0);
        
        const processedOpp = opportunities[0];
        expect(processedOpp.score).toBeGreaterThan(60);
        expect(processedOpp.discoveredAt).toBeDefined();
        
        // Test profitability analysis
        const profitabilityAnalyzer = new ProfitabilityAnalyzer();
        const profitabilityData = await profitabilityAnalyzer.analyze(processedOpp);
        
        expect(profitabilityData.score).toBeGreaterThan(0);
        expect(profitabilityData.profitability.revenue.monthlyRevenue).toBeGreaterThan(0);
        
        // Test velocity analysis
        const velocityAnalyzer = new TrendVelocityAnalyzer();
        const velocityData = await velocityAnalyzer.analyze(processedOpp);
        
        expect(velocityData.score).toBeGreaterThan(0);
        expect(velocityData.velocity.overall).toBeGreaterThan(0);
    });
});