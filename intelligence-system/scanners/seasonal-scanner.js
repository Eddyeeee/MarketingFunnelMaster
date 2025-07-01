class SeasonalScanner {
    constructor(config = {}) {
        this.config = {
            lookAheadDays: config.lookAheadDays || 90,
            minSeasonalScore: config.minSeasonalScore || 60,
            regions: config.regions || ['US', 'EU', 'DE'],
            categories: config.categories || ['finance', 'business', 'education', 'lifestyle'],
            ...config
        };
        
        this.seasonalData = new Map();
        this.holidayCalendar = new Map();
        this.marketingCalendar = new Map();
        this.weatherPatterns = new Map();
        
        this.initializeSeasonalData();
        this.initializeHolidayCalendar();
        this.initializeMarketingCalendar();
    }

    async scan() {
        const opportunities = [];
        
        try {
            const now = new Date();
            const endDate = new Date(now.getTime() + (this.config.lookAheadDays * 24 * 60 * 60 * 1000));
            
            // Scan upcoming seasonal opportunities
            const seasonalOpportunities = this.scanSeasonalPatterns(now, endDate);
            
            // Scan holiday-based opportunities
            const holidayOpportunities = this.scanHolidayOpportunities(now, endDate);
            
            // Scan marketing calendar events
            const marketingOpportunities = this.scanMarketingCalendar(now, endDate);
            
            // Scan weather-related opportunities
            const weatherOpportunities = await this.scanWeatherOpportunities(now, endDate);
            
            // Cultural and regional events
            const culturalOpportunities = this.scanCulturalEvents(now, endDate);

            opportunities.push(
                ...seasonalOpportunities,
                ...holidayOpportunities,
                ...marketingOpportunities,
                ...weatherOpportunities,
                ...culturalOpportunities
            );

            // Filter by minimum score and remove duplicates
            const filteredOpportunities = opportunities
                .filter(opp => opp.score >= this.config.minSeasonalScore)
                .filter((opp, index, self) => 
                    index === self.findIndex(o => o.title === opp.title && o.startDate === opp.startDate)
                )
                .sort((a, b) => b.score - a.score);

            return filteredOpportunities;

        } catch (error) {
            console.error('Seasonal scanning error:', error);
            throw error;
        }
    }

    scanSeasonalPatterns(startDate, endDate) {
        const opportunities = [];
        const currentDate = new Date(startDate);
        
        while (currentDate <= endDate) {
            const month = currentDate.getMonth();
            const patterns = this.seasonalData.get(month);
            
            if (patterns) {
                for (const pattern of patterns) {
                    if (this.isPatternActive(pattern, currentDate)) {
                        const opportunity = this.createSeasonalOpportunity(pattern, currentDate);
                        if (opportunity) {
                            opportunities.push(opportunity);
                        }
                    }
                }
            }
            
            currentDate.setDate(currentDate.getDate() + 7); // Check weekly
        }
        
        return opportunities;
    }

    scanHolidayOpportunities(startDate, endDate) {
        const opportunities = [];
        
        for (const [region, holidays] of this.holidayCalendar.entries()) {
            if (!this.config.regions.includes(region)) continue;
            
            for (const holiday of holidays) {
                const holidayDate = this.getHolidayDate(holiday, startDate.getFullYear());
                
                if (holidayDate >= startDate && holidayDate <= endDate) {
                    const opportunity = this.createHolidayOpportunity(holiday, holidayDate, region);
                    if (opportunity) {
                        opportunities.push(opportunity);
                    }
                }
                
                // Check next year for holidays at year boundary
                if (endDate.getFullYear() > startDate.getFullYear()) {
                    const nextYearHolidayDate = this.getHolidayDate(holiday, endDate.getFullYear());
                    if (nextYearHolidayDate >= startDate && nextYearHolidayDate <= endDate) {
                        const opportunity = this.createHolidayOpportunity(holiday, nextYearHolidayDate, region);
                        if (opportunity) {
                            opportunities.push(opportunity);
                        }
                    }
                }
            }
        }
        
        return opportunities;
    }

    scanMarketingCalendar(startDate, endDate) {
        const opportunities = [];
        
        for (const [category, events] of this.marketingCalendar.entries()) {
            if (!this.config.categories.includes(category)) continue;
            
            for (const event of events) {
                const eventDate = this.getEventDate(event, startDate.getFullYear());
                
                if (eventDate >= startDate && eventDate <= endDate) {
                    const opportunity = this.createMarketingOpportunity(event, eventDate, category);
                    if (opportunity) {
                        opportunities.push(opportunity);
                    }
                }
            }
        }
        
        return opportunities;
    }

    async scanWeatherOpportunities(startDate, endDate) {
        const opportunities = [];
        
        // Simulate weather-based opportunities
        const weatherEvents = [
            {
                name: 'Summer Heat Wave',
                months: [6, 7, 8],
                impact: 'high',
                categories: ['lifestyle', 'health'],
                description: 'Hot weather increases interest in indoor activities, cooling products, and remote work'
            },
            {
                name: 'Winter Storm Season',
                months: [11, 0, 1, 2],
                impact: 'medium',
                categories: ['lifestyle', 'business'],
                description: 'Winter weather increases indoor time and online activity'
            },
            {
                name: 'Spring Renewal',
                months: [2, 3, 4],
                impact: 'high',
                categories: ['lifestyle', 'business', 'education'],
                description: 'Spring season associated with new beginnings and fresh starts'
            },
            {
                name: 'Fall Preparation',
                months: [8, 9, 10],
                impact: 'medium',
                categories: ['business', 'education', 'finance'],
                description: 'Fall season associated with planning and preparation'
            }
        ];

        const currentDate = new Date(startDate);
        
        while (currentDate <= endDate) {
            const month = currentDate.getMonth();
            
            for (const weatherEvent of weatherEvents) {
                if (weatherEvent.months.includes(month)) {
                    const hasRelevantCategory = weatherEvent.categories.some(cat => 
                        this.config.categories.includes(cat)
                    );
                    
                    if (hasRelevantCategory) {
                        opportunities.push({
                            id: `weather_${weatherEvent.name.replace(/\s+/g, '_').toLowerCase()}_${currentDate.getTime()}`,
                            title: `${weatherEvent.name} Marketing Opportunity`,
                            description: weatherEvent.description,
                            source: 'seasonal_scanner',
                            type: 'weather_seasonal',
                            category: weatherEvent.categories[0],
                            startDate: new Date(currentDate).toISOString(),
                            endDate: new Date(currentDate.getFullYear(), month + 1, 0).toISOString(),
                            score: this.calculateWeatherScore(weatherEvent, currentDate),
                            weatherEvent: weatherEvent.name,
                            impact: weatherEvent.impact,
                            lastUpdated: new Date().toISOString()
                        });
                    }
                }
            }
            
            currentDate.setMonth(currentDate.getMonth() + 1);
        }
        
        return opportunities;
    }

    scanCulturalEvents(startDate, endDate) {
        const opportunities = [];
        
        const culturalEvents = [
            {
                name: 'German Oktoberfest Season',
                region: 'DE',
                startMonth: 8, // September
                endMonth: 9,   // October
                categories: ['lifestyle', 'business'],
                description: 'Cultural celebration period with increased social activity'
            },
            {
                name: 'US Tax Season',
                region: 'US',
                startMonth: 0, // January
                endMonth: 3,   // April
                categories: ['finance', 'business'],
                description: 'Annual tax preparation period with high financial activity'
            },
            {
                name: 'European Summer Holiday',
                region: 'EU',
                startMonth: 6, // July
                endMonth: 7,   // August
                categories: ['lifestyle', 'education'],
                description: 'Summer vacation period with different consumption patterns'
            },
            {
                name: 'Back to School Global',
                region: 'GLOBAL',
                startMonth: 7, // August
                endMonth: 8,   // September
                categories: ['education', 'business'],
                description: 'Global back-to-school period with focus on learning and productivity'
            }
        ];

        for (const event of culturalEvents) {
            if (event.region !== 'GLOBAL' && !this.config.regions.includes(event.region)) {
                continue;
            }

            const hasRelevantCategory = event.categories.some(cat => 
                this.config.categories.includes(cat)
            );

            if (hasRelevantCategory) {
                const eventStart = new Date(startDate.getFullYear(), event.startMonth, 1);
                const eventEnd = new Date(startDate.getFullYear(), event.endMonth + 1, 0);

                // Check if event overlaps with our scan period
                if (eventEnd >= startDate && eventStart <= endDate) {
                    opportunities.push({
                        id: `cultural_${event.name.replace(/\s+/g, '_').toLowerCase()}_${eventStart.getTime()}`,
                        title: `Cultural Event: ${event.name}`,
                        description: event.description,
                        source: 'seasonal_scanner',
                        type: 'cultural_seasonal',
                        category: event.categories[0],
                        region: event.region,
                        startDate: eventStart.toISOString(),
                        endDate: eventEnd.toISOString(),
                        score: this.calculateCulturalScore(event, eventStart),
                        culturalEvent: event.name,
                        lastUpdated: new Date().toISOString()
                    });
                }

                // Check next year if scan period crosses year boundary
                if (endDate.getFullYear() > startDate.getFullYear()) {
                    const nextYearStart = new Date(endDate.getFullYear(), event.startMonth, 1);
                    const nextYearEnd = new Date(endDate.getFullYear(), event.endMonth + 1, 0);

                    if (nextYearEnd >= startDate && nextYearStart <= endDate) {
                        opportunities.push({
                            id: `cultural_${event.name.replace(/\s+/g, '_').toLowerCase()}_${nextYearStart.getTime()}`,
                            title: `Cultural Event: ${event.name}`,
                            description: event.description,
                            source: 'seasonal_scanner',
                            type: 'cultural_seasonal',
                            category: event.categories[0],
                            region: event.region,
                            startDate: nextYearStart.toISOString(),
                            endDate: nextYearEnd.toISOString(),
                            score: this.calculateCulturalScore(event, nextYearStart),
                            culturalEvent: event.name,
                            lastUpdated: new Date().toISOString()
                        });
                    }
                }
            }
        }

        return opportunities;
    }

    createSeasonalOpportunity(pattern, date) {
        const score = this.calculateSeasonalScore(pattern, date);
        
        if (score < this.config.minSeasonalScore) {
            return null;
        }

        return {
            id: `seasonal_${pattern.name.replace(/\s+/g, '_').toLowerCase()}_${date.getTime()}`,
            title: `Seasonal Opportunity: ${pattern.name}`,
            description: pattern.description,
            source: 'seasonal_scanner',
            type: 'seasonal_pattern',
            category: pattern.category,
            startDate: date.toISOString(),
            endDate: new Date(date.getTime() + (pattern.duration * 24 * 60 * 60 * 1000)).toISOString(),
            score: score,
            seasonality: {
                pattern: pattern.name,
                strength: pattern.strength,
                historicalPerformance: pattern.historicalPerformance,
                competitionLevel: pattern.competitionLevel
            },
            lastUpdated: new Date().toISOString()
        };
    }

    createHolidayOpportunity(holiday, date, region) {
        const score = this.calculateHolidayScore(holiday, date);
        
        if (score < this.config.minSeasonalScore) {
            return null;
        }

        // Pre-holiday opportunity (preparation phase)
        const preHolidayDate = new Date(date);
        preHolidayDate.setDate(preHolidayDate.getDate() - (holiday.preparationDays || 7));

        return {
            id: `holiday_${holiday.name.replace(/\s+/g, '_').toLowerCase()}_${date.getTime()}`,
            title: `Holiday Opportunity: ${holiday.name}`,
            description: holiday.marketingOpportunity || `Marketing opportunity around ${holiday.name}`,
            source: 'seasonal_scanner',
            type: 'holiday_seasonal',
            category: holiday.category || 'lifestyle',
            region: region,
            startDate: preHolidayDate.toISOString(),
            endDate: date.toISOString(),
            score: score,
            holiday: {
                name: holiday.name,
                date: date.toISOString(),
                impact: holiday.impact,
                commercialPotential: holiday.commercialPotential
            },
            lastUpdated: new Date().toISOString()
        };
    }

    createMarketingOpportunity(event, date, category) {
        const score = this.calculateMarketingScore(event, date);
        
        if (score < this.config.minSeasonalScore) {
            return null;
        }

        return {
            id: `marketing_${event.name.replace(/\s+/g, '_').toLowerCase()}_${date.getTime()}`,
            title: `Marketing Calendar: ${event.name}`,
            description: event.description,
            source: 'seasonal_scanner',
            type: 'marketing_seasonal',
            category: category,
            startDate: date.toISOString(),
            endDate: new Date(date.getTime() + (event.duration * 24 * 60 * 60 * 1000)).toISOString(),
            score: score,
            marketingEvent: {
                name: event.name,
                focus: event.focus,
                targetAudience: event.targetAudience,
                keyMessages: event.keyMessages
            },
            lastUpdated: new Date().toISOString()
        };
    }

    isPatternActive(pattern, date) {
        const month = date.getMonth();
        const day = date.getDate();
        
        // Check if current date falls within pattern's active period
        if (pattern.months && !pattern.months.includes(month)) {
            return false;
        }
        
        if (pattern.dateRange) {
            const startDate = new Date(date.getFullYear(), pattern.dateRange.startMonth, pattern.dateRange.startDay);
            const endDate = new Date(date.getFullYear(), pattern.dateRange.endMonth, pattern.dateRange.endDay);
            
            return date >= startDate && date <= endDate;
        }
        
        return true;
    }

    calculateSeasonalScore(pattern, date) {
        let score = pattern.baseScore || 70;
        
        // Historical performance bonus
        if (pattern.historicalPerformance >= 80) {
            score += 15;
        } else if (pattern.historicalPerformance >= 60) {
            score += 10;
        }
        
        // Competition penalty
        if (pattern.competitionLevel >= 80) {
            score -= 15;
        } else if (pattern.competitionLevel >= 60) {
            score -= 10;
        }
        
        // Strength bonus
        score += (pattern.strength || 5) * 2;
        
        // Timing bonus (peak season)
        if (pattern.peakMonths && pattern.peakMonths.includes(date.getMonth())) {
            score += 20;
        }
        
        return Math.max(0, Math.min(100, score));
    }

    calculateHolidayScore(holiday, date) {
        let score = 60; // Base score
        
        // Impact multiplier
        const impactMultiplier = {
            'high': 1.5,
            'medium': 1.2,
            'low': 1.0
        };
        
        score *= impactMultiplier[holiday.impact] || 1.0;
        
        // Commercial potential bonus
        if (holiday.commercialPotential >= 80) {
            score += 20;
        } else if (holiday.commercialPotential >= 60) {
            score += 10;
        }
        
        // Days until holiday (optimal window is 7-14 days before)
        const daysUntil = Math.ceil((date - new Date()) / (1000 * 60 * 60 * 24));
        if (daysUntil >= 7 && daysUntil <= 14) {
            score += 15;
        } else if (daysUntil >= 1 && daysUntil <= 30) {
            score += 5;
        }
        
        return Math.max(0, Math.min(100, score));
    }

    calculateMarketingScore(event, date) {
        let score = event.baseScore || 70;
        
        // Relevance to configured categories
        const relevantCategories = event.categories?.filter(cat => 
            this.config.categories.includes(cat)
        ) || [];
        
        score += relevantCategories.length * 5;
        
        // Target audience alignment
        if (event.targetAudience?.includes('business_owners') || 
            event.targetAudience?.includes('entrepreneurs')) {
            score += 10;
        }
        
        return Math.max(0, Math.min(100, score));
    }

    calculateWeatherScore(weatherEvent, date) {
        let score = 60; // Base score
        
        // Impact multiplier
        const impactMultiplier = {
            'high': 1.4,
            'medium': 1.2,
            'low': 1.0
        };
        
        score *= impactMultiplier[weatherEvent.impact] || 1.0;
        
        // Category relevance
        const relevantCategories = weatherEvent.categories.filter(cat => 
            this.config.categories.includes(cat)
        );
        
        score += relevantCategories.length * 8;
        
        return Math.max(0, Math.min(100, score));
    }

    calculateCulturalScore(event, date) {
        let score = 65; // Base score
        
        // Regional relevance
        if (this.config.regions.includes(event.region) || event.region === 'GLOBAL') {
            score += 10;
        }
        
        // Category alignment
        const relevantCategories = event.categories.filter(cat => 
            this.config.categories.includes(cat)
        );
        
        score += relevantCategories.length * 10;
        
        return Math.max(0, Math.min(100, score));
    }

    getHolidayDate(holiday, year) {
        if (holiday.fixedDate) {
            return new Date(year, holiday.fixedDate.month, holiday.fixedDate.day);
        }
        
        if (holiday.dynamicDate) {
            // Handle dynamic dates like "First Monday in September"
            return this.calculateDynamicDate(holiday.dynamicDate, year);
        }
        
        return new Date(year, 0, 1); // Default to January 1st
    }

    getEventDate(event, year) {
        if (event.fixedDate) {
            return new Date(year, event.fixedDate.month, event.fixedDate.day);
        }
        
        if (event.dateRange) {
            return new Date(year, event.dateRange.month, event.dateRange.startDay);
        }
        
        return new Date(year, 0, 1); // Default to January 1st
    }

    calculateDynamicDate(dynamicDate, year) {
        // Simplified dynamic date calculation
        // In production, implement full dynamic date logic
        const { month, week, day } = dynamicDate;
        const firstDayOfMonth = new Date(year, month, 1);
        const firstDayOfWeek = firstDayOfMonth.getDay();
        
        let targetDate = new Date(year, month, 1);
        targetDate.setDate(1 + (day - firstDayOfWeek + 7) % 7 + (week - 1) * 7);
        
        return targetDate;
    }

    initializeSeasonalData() {
        // January patterns
        this.seasonalData.set(0, [
            {
                name: 'New Year Resolution Peak',
                category: 'self_improvement',
                description: 'Peak time for personal development and financial goal setting',
                months: [0, 1],
                strength: 9,
                baseScore: 85,
                duration: 30,
                historicalPerformance: 90,
                competitionLevel: 75,
                peakMonths: [0]
            }
        ]);

        // March patterns
        this.seasonalData.set(2, [
            {
                name: 'Tax Season Preparation',
                category: 'finance',
                description: 'High demand for financial planning and tax preparation services',
                months: [2, 3],
                strength: 8,
                baseScore: 80,
                duration: 60,
                historicalPerformance: 85,
                competitionLevel: 70,
                peakMonths: [2, 3]
            }
        ]);

        // April patterns
        this.seasonalData.set(3, [
            {
                name: 'Spring Renewal',
                category: 'business',
                description: 'Spring season drives new business initiatives and fresh starts',
                months: [3, 4],
                strength: 7,
                baseScore: 75,
                duration: 45,
                historicalPerformance: 80,
                competitionLevel: 60,
                peakMonths: [3, 4]
            }
        ]);

        // September patterns
        this.seasonalData.set(8, [
            {
                name: 'Back to School Learning',
                category: 'education',
                description: 'High interest in skill development and learning opportunities',
                months: [8, 9],
                strength: 8,
                baseScore: 82,
                duration: 45,
                historicalPerformance: 85,
                competitionLevel: 65,
                peakMonths: [8]
            }
        ]);

        // November patterns
        this.seasonalData.set(10, [
            {
                name: 'Holiday Shopping Preparation',
                category: 'business',
                description: 'Pre-holiday period with high consumer activity and spending',
                months: [10, 11],
                strength: 9,
                baseScore: 88,
                duration: 60,
                historicalPerformance: 95,
                competitionLevel: 85,
                peakMonths: [10, 11]
            }
        ]);
    }

    initializeHolidayCalendar() {
        // US holidays
        this.holidayCalendar.set('US', [
            {
                name: 'New Year\'s Day',
                fixedDate: { month: 0, day: 1 },
                impact: 'high',
                commercialPotential: 70,
                category: 'lifestyle',
                preparationDays: 14,
                marketingOpportunity: 'New year, new opportunities messaging'
            },
            {
                name: 'Valentine\'s Day',
                fixedDate: { month: 1, day: 14 },
                impact: 'medium',
                commercialPotential: 85,
                category: 'lifestyle',
                preparationDays: 10
            },
            {
                name: 'Independence Day',
                fixedDate: { month: 6, day: 4 },
                impact: 'high',
                commercialPotential: 75,
                category: 'lifestyle',
                preparationDays: 7
            },
            {
                name: 'Black Friday',
                dynamicDate: { month: 10, week: 4, day: 5 }, // 4th Friday of November
                impact: 'high',
                commercialPotential: 95,
                category: 'business',
                preparationDays: 30
            },
            {
                name: 'Christmas',
                fixedDate: { month: 11, day: 25 },
                impact: 'high',
                commercialPotential: 90,
                category: 'lifestyle',
                preparationDays: 45
            }
        ]);

        // German holidays
        this.holidayCalendar.set('DE', [
            {
                name: 'Neujahr',
                fixedDate: { month: 0, day: 1 },
                impact: 'high',
                commercialPotential: 70,
                category: 'lifestyle',
                preparationDays: 14
            },
            {
                name: 'Oktoberfest',
                fixedDate: { month: 8, day: 21 }, // Simplified
                impact: 'high',
                commercialPotential: 80,
                category: 'lifestyle',
                preparationDays: 14
            },
            {
                name: 'Weihnachten',
                fixedDate: { month: 11, day: 25 },
                impact: 'high',
                commercialPotential: 90,
                category: 'lifestyle',
                preparationDays: 45
            }
        ]);

        // EU-wide holidays
        this.holidayCalendar.set('EU', [
            {
                name: 'New Year\'s Day',
                fixedDate: { month: 0, day: 1 },
                impact: 'high',
                commercialPotential: 70,
                category: 'lifestyle',
                preparationDays: 14
            },
            {
                name: 'Christmas',
                fixedDate: { month: 11, day: 25 },
                impact: 'high',
                commercialPotential: 90,
                category: 'lifestyle',
                preparationDays: 45
            }
        ]);
    }

    initializeMarketingCalendar() {
        // Finance category events
        this.marketingCalendar.set('finance', [
            {
                name: 'Tax Season Peak',
                fixedDate: { month: 3, day: 15 },
                duration: 30,
                focus: 'Financial planning and tax optimization',
                targetAudience: ['business_owners', 'high_earners'],
                keyMessages: ['Tax savings', 'Financial planning', 'Business deductions'],
                baseScore: 85,
                categories: ['finance', 'business']
            },
            {
                name: 'Year-End Financial Planning',
                fixedDate: { month: 10, day: 1 },
                duration: 60,
                focus: 'End-of-year financial strategies',
                targetAudience: ['investors', 'business_owners'],
                keyMessages: ['Year-end planning', 'Tax strategies', 'Investment review'],
                baseScore: 80,
                categories: ['finance', 'business']
            }
        ]);

        // Business category events
        this.marketingCalendar.set('business', [
            {
                name: 'New Year Business Goals',
                fixedDate: { month: 0, day: 1 },
                duration: 45,
                focus: 'Business planning and goal setting',
                targetAudience: ['entrepreneurs', 'business_owners'],
                keyMessages: ['New year goals', 'Business growth', 'Strategic planning'],
                baseScore: 85,
                categories: ['business']
            },
            {
                name: 'Q4 Business Preparation',
                fixedDate: { month: 9, day: 1 },
                duration: 30,
                focus: 'Fourth quarter business strategies',
                targetAudience: ['business_owners', 'managers'],
                keyMessages: ['Q4 planning', 'Year-end push', 'Goal achievement'],
                baseScore: 75,
                categories: ['business']
            }
        ]);

        // Education category events
        this.marketingCalendar.set('education', [
            {
                name: 'Back to School Learning',
                fixedDate: { month: 8, day: 1 },
                duration: 45,
                focus: 'Skill development and learning',
                targetAudience: ['students', 'professionals', 'career_changers'],
                keyMessages: ['New skills', 'Career advancement', 'Personal development'],
                baseScore: 82,
                categories: ['education', 'business']
            },
            {
                name: 'New Year Learning Resolutions',
                fixedDate: { month: 0, day: 1 },
                duration: 30,
                focus: 'Personal development and skill building',
                targetAudience: ['professionals', 'entrepreneurs'],
                keyMessages: ['Skill upgrade', 'Career growth', 'Learning goals'],
                baseScore: 80,
                categories: ['education']
            }
        ]);
    }

    getStats() {
        return {
            seasonalPatterns: this.seasonalData.size,
            holidayRegions: this.holidayCalendar.size,
            marketingCategories: this.marketingCalendar.size,
            lookAheadDays: this.config.lookAheadDays,
            regions: this.config.regions,
            categories: this.config.categories
        };
    }
}

module.exports = { SeasonalScanner };