const axios = require('axios');

class TimingOptimizer {
    constructor(config = {}) {
        this.config = {
            timeZones: config.timeZones || ['Europe/Berlin', 'America/New_York', 'America/Los_Angeles'],
            marketHours: config.marketHours || {
                'Europe/Berlin': { start: 9, end: 17 },
                'America/New_York': { start: 9, end: 17 },
                'America/Los_Angeles': { start: 9, end: 17 }
            },
            weekendFactor: config.weekendFactor || 0.3, // 30% less activity on weekends
            holidayFactor: config.holidayFactor || 0.2, // 20% less activity on holidays
            ...config
        };
        
        this.economicCalendar = [];
        this.marketEvents = new Map();
        this.seasonalPatterns = new Map();
        this.loadSeasonalPatterns();
    }

    async scan() {
        const opportunities = [];
        
        try {
            // Get current timing analysis
            const currentTiming = await this.analyzeCurrentTiming();
            
            // Get upcoming high-impact events
            const upcomingEvents = await this.getUpcomingEvents();
            
            // Analyze seasonal opportunities
            const seasonalOpportunities = this.getSeasonalOpportunities();
            
            // Market cycle analysis
            const marketCycles = await this.analyzeMarketCycles();

            // Combine all timing-based opportunities
            opportunities.push(
                ...this.createTimingOpportunities(currentTiming),
                ...this.createEventOpportunities(upcomingEvents),
                ...seasonalOpportunities,
                ...this.createCycleOpportunities(marketCycles)
            );

            return opportunities.filter(opp => opp.score >= 60);

        } catch (error) {
            console.error('Timing optimization error:', error);
            throw error;
        }
    }

    async analyzeCurrentTiming() {
        const now = new Date();
        const analysis = {
            timestamp: now.toISOString(),
            dayOfWeek: now.getDay(),
            hour: now.getHours(),
            month: now.getMonth(),
            isWeekend: now.getDay() === 0 || now.getDay() === 6,
            isHoliday: await this.checkIfHoliday(now),
            marketActivity: {},
            globalActivity: 0
        };

        // Analyze activity across time zones
        let totalActivity = 0;
        let activeMarkets = 0;

        for (const [timezone, hours] of Object.entries(this.config.marketHours)) {
            const marketTime = new Date(now.toLocaleString("en-US", {timeZone: timezone}));
            const marketHour = marketTime.getHours();
            
            const isActive = marketHour >= hours.start && marketHour <= hours.end;
            const activityLevel = this.calculateMarketActivity(marketTime, timezone);
            
            analysis.marketActivity[timezone] = {
                time: marketTime.toISOString(),
                hour: marketHour,
                isActive,
                activityLevel
            };

            if (isActive) {
                totalActivity += activityLevel;
                activeMarkets++;
            }
        }

        analysis.globalActivity = activeMarkets > 0 ? totalActivity / activeMarkets : 0;
        
        // Apply weekend and holiday factors
        if (analysis.isWeekend) {
            analysis.globalActivity *= this.config.weekendFactor;
        }
        
        if (analysis.isHoliday) {
            analysis.globalActivity *= this.config.holidayFactor;
        }

        return analysis;
    }

    calculateMarketActivity(marketTime, timezone) {
        const hour = marketTime.getHours();
        const dayOfWeek = marketTime.getDay();
        
        // Base activity patterns (0-100)
        const hourlyActivity = {
            0: 10, 1: 5, 2: 5, 3: 5, 4: 10, 5: 20, 6: 40, 7: 60, 8: 80,
            9: 90, 10: 95, 11: 100, 12: 85, 13: 90, 14: 95, 15: 100, 16: 90,
            17: 80, 18: 70, 19: 60, 20: 50, 21: 40, 22: 30, 23: 20
        };

        const weeklyActivity = {
            0: 30, // Sunday
            1: 100, // Monday
            2: 95, // Tuesday
            3: 90, // Wednesday
            4: 85, // Thursday
            5: 80, // Friday
            6: 40  // Saturday
        };

        const baseActivity = hourlyActivity[hour] || 50;
        const weeklyMultiplier = (weeklyActivity[dayOfWeek] || 50) / 100;
        
        return Math.round(baseActivity * weeklyMultiplier);
    }

    async getUpcomingEvents() {
        const events = [];
        
        try {
            // Economic calendar events (simulate API call)
            const economicEvents = await this.fetchEconomicCalendar();
            
            // Earnings calendar
            const earningsEvents = await this.fetchEarningsCalendar();
            
            // Social media events and trends
            const socialEvents = await this.fetchSocialCalendar();
            
            // Seasonal marketing events
            const marketingEvents = this.getMarketingCalendar();

            events.push(...economicEvents, ...earningsEvents, ...socialEvents, ...marketingEvents);

            // Filter for next 30 days and high impact
            const thirtyDaysFromNow = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);
            
            return events
                .filter(event => {
                    const eventDate = new Date(event.date);
                    return eventDate <= thirtyDaysFromNow && event.impact >= 7; // High impact events
                })
                .sort((a, b) => new Date(a.date) - new Date(b.date));

        } catch (error) {
            console.error('Error fetching upcoming events:', error);
            return [];
        }
    }

    async fetchEconomicCalendar() {
        // Simulate economic calendar API
        const events = [
            {
                id: 'fed_meeting_' + Date.now(),
                title: 'Federal Reserve Interest Rate Decision',
                date: this.getNextBusinessDay(7),
                impact: 9,
                type: 'economic',
                category: 'monetary_policy',
                description: 'Federal Reserve announces interest rate decision'
            },
            {
                id: 'nfp_' + Date.now(),
                title: 'Non-Farm Payrolls Report',
                date: this.getFirstFridayOfMonth(),
                impact: 8,
                type: 'economic',
                category: 'employment',
                description: 'Monthly employment statistics release'
            },
            {
                id: 'cpi_' + Date.now(),
                title: 'Consumer Price Index (CPI)',
                date: this.getNextBusinessDay(14),
                impact: 8,
                type: 'economic',
                category: 'inflation',
                description: 'Monthly inflation data release'
            }
        ];

        return events;
    }

    async fetchEarningsCalendar() {
        // Simulate earnings calendar
        const events = [
            {
                id: 'aapl_earnings_' + Date.now(),
                title: 'Apple Inc. Earnings Report',
                date: this.getNextBusinessDay(5),
                impact: 7,
                type: 'earnings',
                category: 'technology',
                symbol: 'AAPL',
                description: 'Apple quarterly earnings announcement'
            },
            {
                id: 'msft_earnings_' + Date.now(),
                title: 'Microsoft Corp. Earnings Report',
                date: this.getNextBusinessDay(8),
                impact: 7,
                type: 'earnings',
                category: 'technology',
                symbol: 'MSFT',
                description: 'Microsoft quarterly earnings announcement'
            }
        ];

        return events;
    }

    async fetchSocialCalendar() {
        // Simulate social media events
        const events = [
            {
                id: 'black_friday_' + Date.now(),
                title: 'Black Friday Shopping Event',
                date: this.getNextBlackFriday(),
                impact: 9,
                type: 'social',
                category: 'shopping',
                description: 'Major shopping event with high consumer activity'
            },
            {
                id: 'cyber_monday_' + Date.now(),
                title: 'Cyber Monday Online Sales',
                date: this.getNextCyberMonday(),
                impact: 8,
                type: 'social',
                category: 'shopping',
                description: 'Online shopping event following Black Friday'
            }
        ];

        return events;
    }

    getMarketingCalendar() {
        const events = [];
        const now = new Date();
        const currentMonth = now.getMonth();
        const currentYear = now.getFullYear();

        // Tax season (March-April)
        if (currentMonth <= 3) {
            events.push({
                id: 'tax_season_' + currentYear,
                title: 'Tax Season Peak',
                date: new Date(currentYear, 3, 15), // April 15
                impact: 8,
                type: 'seasonal',
                category: 'finance',
                description: 'Peak tax filing period with high financial product interest'
            });
        }

        // Back to school (August-September)
        if (currentMonth >= 7 && currentMonth <= 8) {
            events.push({
                id: 'back_to_school_' + currentYear,
                title: 'Back to School Season',
                date: new Date(currentYear, 8, 1), // September 1
                impact: 7,
                type: 'seasonal',
                category: 'education',
                description: 'Back to school period with education and skill-building focus'
            });
        }

        // New Year resolution period (January)
        if (currentMonth === 0 || currentMonth === 11) {
            events.push({
                id: 'new_year_resolutions_' + (currentMonth === 11 ? currentYear + 1 : currentYear),
                title: 'New Year Resolution Period',
                date: new Date(currentMonth === 11 ? currentYear + 1 : currentYear, 0, 1),
                impact: 8,
                type: 'seasonal',
                category: 'self_improvement',
                description: 'New Year period with high motivation for change and improvement'
            });
        }

        return events;
    }

    getSeasonalOpportunities() {
        const opportunities = [];
        const now = new Date();
        const currentMonth = now.getMonth();
        const patterns = this.seasonalPatterns.get(currentMonth);

        if (patterns) {
            for (const pattern of patterns) {
                if (pattern.isActive) {
                    opportunities.push({
                        id: `seasonal_${pattern.category}_${currentMonth}_${Date.now()}`,
                        title: `Seasonal Opportunity: ${pattern.title}`,
                        description: pattern.description,
                        category: pattern.category,
                        source: 'timing_optimizer',
                        type: 'seasonal_timing',
                        seasonality: {
                            month: currentMonth,
                            peakMonths: pattern.peakMonths,
                            intensity: pattern.intensity
                        },
                        score: this.calculateSeasonalScore(pattern),
                        lastUpdated: new Date().toISOString(),
                        metrics: {
                            historicalPerformance: pattern.historicalPerformance,
                            competitionLevel: pattern.competitionLevel,
                            marketDemand: pattern.marketDemand
                        }
                    });
                }
            }
        }

        return opportunities;
    }

    async analyzeMarketCycles() {
        const cycles = {
            stockMarket: await this.analyzeStockMarketCycle(),
            cryptocurrency: await this.analyzeCryptoCycle(),
            businessCycle: this.analyzeBusinessCycle(),
            consumerSpending: this.analyzeConsumerSpendingCycle()
        };

        return cycles;
    }

    async analyzeStockMarketCycle() {
        // Simulate market cycle analysis
        const now = new Date();
        const dayOfYear = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
        
        // Historical patterns: January effect, summer doldrums, year-end rally
        let phase = 'neutral';
        let strength = 50;

        if (dayOfYear <= 31) { // January
            phase = 'january_effect';
            strength = 75;
        } else if (dayOfYear >= 152 && dayOfYear <= 243) { // Summer months
            phase = 'summer_doldrums';
            strength = 30;
        } else if (dayOfYear >= 305) { // November-December
            phase = 'year_end_rally';
            strength = 80;
        }

        return {
            phase,
            strength,
            nextPhaseDate: this.calculateNextPhaseDate(phase),
            confidence: 70
        };
    }

    async analyzeCryptoCycle() {
        // Simulate crypto cycle analysis
        const phases = ['accumulation', 'markup', 'distribution', 'markdown'];
        const currentPhase = phases[Math.floor(Math.random() * phases.length)];
        
        return {
            phase: currentPhase,
            strength: Math.floor(Math.random() * 100),
            halving: {
                nextDate: new Date('2028-04-01'),
                daysUntil: Math.floor((new Date('2028-04-01') - new Date()) / (1000 * 60 * 60 * 24))
            },
            confidence: 60
        };
    }

    analyzeBusinessCycle() {
        // Simulate business cycle analysis
        const now = new Date();
        const quarter = Math.floor(now.getMonth() / 3) + 1;
        
        return {
            quarter,
            phase: quarter <= 2 ? 'expansion' : 'peak',
            strength: 65,
            nextEarningsSeason: this.getNextEarningsSeason(),
            confidence: 75
        };
    }

    analyzeConsumerSpendingCycle() {
        const now = new Date();
        const month = now.getMonth();
        
        // Higher spending in November-December, tax refund season, back-to-school
        let phase = 'normal';
        let strength = 50;

        if (month >= 10 || month <= 0) { // Holiday season
            phase = 'high_spending';
            strength = 90;
        } else if (month >= 2 && month <= 4) { // Tax refund season
            phase = 'tax_refund_boost';
            strength = 70;
        } else if (month >= 7 && month <= 8) { // Back to school
            phase = 'back_to_school';
            strength = 65;
        }

        return {
            phase,
            strength,
            confidence: 80
        };
    }

    createTimingOpportunities(timing) {
        const opportunities = [];
        
        if (timing.globalActivity >= 80) {
            opportunities.push({
                id: `high_activity_${Date.now()}`,
                title: 'High Global Market Activity',
                description: 'Current timing shows high global market activity across multiple time zones',
                source: 'timing_optimizer',
                type: 'market_timing',
                score: Math.min(100, timing.globalActivity + 10),
                timing: {
                    immediate: true,
                    duration: '2-4 hours',
                    bestAction: 'launch_campaigns'
                },
                lastUpdated: timing.timestamp
            });
        }

        // Weekend opportunity for different content types
        if (timing.isWeekend && timing.globalActivity >= 30) {
            opportunities.push({
                id: `weekend_opportunity_${Date.now()}`,
                title: 'Weekend Engagement Opportunity',
                description: 'Weekend timing optimal for lifestyle and entertainment content',
                source: 'timing_optimizer',
                type: 'weekend_timing',
                score: 70,
                timing: {
                    immediate: true,
                    duration: 'weekend',
                    bestAction: 'lifestyle_content'
                },
                lastUpdated: timing.timestamp
            });
        }

        return opportunities;
    }

    createEventOpportunities(events) {
        return events.map(event => ({
            id: `event_${event.id}`,
            title: `Timing Opportunity: ${event.title}`,
            description: `Prepare campaigns around ${event.title} for maximum impact`,
            source: 'timing_optimizer',
            type: 'event_timing',
            eventTiming: event.date,
            score: this.calculateEventScore(event),
            event: {
                ...event,
                daysUntil: Math.ceil((new Date(event.date) - new Date()) / (1000 * 60 * 60 * 24))
            },
            lastUpdated: new Date().toISOString()
        }));
    }

    createCycleOpportunities(cycles) {
        const opportunities = [];

        Object.entries(cycles).forEach(([cycleType, cycleData]) => {
            if (cycleData.strength >= 70) {
                opportunities.push({
                    id: `cycle_${cycleType}_${Date.now()}`,
                    title: `${cycleType.charAt(0).toUpperCase() + cycleType.slice(1)} Cycle Opportunity`,
                    description: `${cycleType} is in ${cycleData.phase} phase with ${cycleData.strength}% strength`,
                    source: 'timing_optimizer',
                    type: 'cycle_timing',
                    score: cycleData.strength,
                    cycle: {
                        type: cycleType,
                        ...cycleData
                    },
                    lastUpdated: new Date().toISOString()
                });
            }
        });

        return opportunities;
    }

    calculateSeasonalScore(pattern) {
        const baseScore = pattern.intensity * 10; // 0-100 base score
        const demandBonus = pattern.marketDemand * 0.2; // 0-20 bonus
        const competitionPenalty = pattern.competitionLevel * 0.1; // 0-10 penalty
        
        return Math.max(0, Math.min(100, baseScore + demandBonus - competitionPenalty));
    }

    calculateEventScore(event) {
        const impactScore = event.impact * 10; // 0-100 base score
        const daysUntil = Math.ceil((new Date(event.date) - new Date()) / (1000 * 60 * 60 * 24));
        
        // Optimal preparation window is 7-21 days before event
        let timingBonus = 0;
        if (daysUntil >= 7 && daysUntil <= 21) {
            timingBonus = 20;
        } else if (daysUntil >= 3 && daysUntil <= 30) {
            timingBonus = 10;
        }

        return Math.min(100, impactScore + timingBonus);
    }

    loadSeasonalPatterns() {
        // Load seasonal patterns for each month
        this.seasonalPatterns.set(0, [ // January
            {
                title: 'New Year Resolutions',
                category: 'self_improvement',
                description: 'High motivation for personal and financial improvement',
                peakMonths: [0, 1],
                intensity: 9,
                isActive: true,
                historicalPerformance: 85,
                competitionLevel: 70,
                marketDemand: 90
            }
        ]);

        this.seasonalPatterns.set(2, [ // March
            {
                title: 'Tax Preparation Season',
                category: 'finance',
                description: 'High demand for financial advice and tax-related services',
                peakMonths: [2, 3],
                intensity: 8,
                isActive: true,
                historicalPerformance: 80,
                competitionLevel: 75,
                marketDemand: 85
            }
        ]);

        this.seasonalPatterns.set(8, [ // September
            {
                title: 'Back to School / Skill Building',
                category: 'education',
                description: 'High interest in learning and skill development',
                peakMonths: [8, 9],
                intensity: 7,
                isActive: true,
                historicalPerformance: 75,
                competitionLevel: 60,
                marketDemand: 80
            }
        ]);

        this.seasonalPatterns.set(10, [ // November
            {
                title: 'Holiday Shopping Season',
                category: 'commerce',
                description: 'Peak consumer spending and promotional opportunities',
                peakMonths: [10, 11],
                intensity: 9,
                isActive: true,
                historicalPerformance: 90,
                competitionLevel: 85,
                marketDemand: 95
            }
        ]);
    }

    // Helper methods
    getNextBusinessDay(daysFromNow) {
        const date = new Date();
        date.setDate(date.getDate() + daysFromNow);
        
        // Adjust for weekends
        while (date.getDay() === 0 || date.getDay() === 6) {
            date.setDate(date.getDate() + 1);
        }
        
        return date.toISOString();
    }

    getFirstFridayOfMonth() {
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), now.getMonth() + 1, 1);
        const firstFriday = new Date(firstDay);
        
        // Find first Friday
        while (firstFriday.getDay() !== 5) {
            firstFriday.setDate(firstFriday.getDate() + 1);
        }
        
        return firstFriday.toISOString();
    }

    getNextBlackFriday() {
        const now = new Date();
        const year = now.getMonth() >= 10 ? now.getFullYear() + 1 : now.getFullYear();
        
        // Black Friday is the Friday after the fourth Thursday in November
        const thanksgiving = new Date(year, 10, 1); // November 1st
        thanksgiving.setDate(thanksgiving.getDate() + (4 - thanksgiving.getDay()) % 7); // First Thursday
        thanksgiving.setDate(thanksgiving.getDate() + 21); // Fourth Thursday
        
        const blackFriday = new Date(thanksgiving);
        blackFriday.setDate(blackFriday.getDate() + 1); // Friday after
        
        return blackFriday.toISOString();
    }

    getNextCyberMonday() {
        const blackFriday = new Date(this.getNextBlackFriday());
        const cyberMonday = new Date(blackFriday);
        cyberMonday.setDate(cyberMonday.getDate() + 3); // Monday after Black Friday
        
        return cyberMonday.toISOString();
    }

    calculateNextPhaseDate(currentPhase) {
        const now = new Date();
        const year = now.getFullYear();
        
        switch (currentPhase) {
            case 'january_effect':
                return new Date(year, 5, 1); // June (summer doldrums)
            case 'summer_doldrums':
                return new Date(year, 10, 1); // November (year-end rally)
            case 'year_end_rally':
                return new Date(year + 1, 0, 1); // Next January
            default:
                return new Date(year, 0, 1); // January
        }
    }

    getNextEarningsSeason() {
        const now = new Date();
        const month = now.getMonth();
        
        // Earnings seasons: Jan, Apr, Jul, Oct
        const seasons = [0, 3, 6, 9]; // January, April, July, October
        const nextSeason = seasons.find(season => season > month) || seasons[0];
        const year = nextSeason > month ? now.getFullYear() : now.getFullYear() + 1;
        
        return new Date(year, nextSeason, 15);
    }

    async checkIfHoliday(date) {
        // Simplified holiday check - in production, use a holiday API
        const holidays = [
            '01-01', '12-25', '12-31', // New Year, Christmas, New Year's Eve
            '07-04', '11-11', '02-14'  // Independence Day, Veterans Day, Valentine's Day
        ];
        
        const dateStr = `${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
        return holidays.includes(dateStr);
    }

    getStats() {
        return {
            timeZones: this.config.timeZones,
            seasonalPatterns: this.seasonalPatterns.size,
            marketEvents: this.marketEvents.size
        };
    }
}

module.exports = { TimingOptimizer };