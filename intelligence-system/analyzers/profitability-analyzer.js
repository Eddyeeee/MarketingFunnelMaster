class ProfitabilityAnalyzer {
    constructor(config = {}) {
        this.config = {
            minCommissionRate: config.minCommissionRate || 0.05, // 5%
            maxPaybackPeriod: config.maxPaybackPeriod || 30, // days
            minROI: config.minROI || 1.5, // 150% return
            defaultConversionRate: config.defaultConversionRate || 0.02, // 2%
            defaultTrafficCost: config.defaultTrafficCost || 0.5, // $0.50 per click
            ...config
        };

        // Industry benchmark data
        this.industryBenchmarks = {
            finance: {
                conversionRate: 0.025,
                avgCommission: 0.15,
                trafficCost: 0.8,
                competitionMultiplier: 1.3
            },
            business: {
                conversionRate: 0.03,
                avgCommission: 0.25,
                trafficCost: 0.6,
                competitionMultiplier: 1.1
            },
            education: {
                conversionRate: 0.045,
                avgCommission: 0.35,
                trafficCost: 0.4,
                competitionMultiplier: 0.9
            },
            lifestyle: {
                conversionRate: 0.02,
                avgCommission: 0.12,
                trafficCost: 0.3,
                competitionMultiplier: 1.0
            }
        };

        this.marketingCosts = {
            organic: {
                contentCreation: 50, // per piece
                timeInvestment: 20, // hours
                hourlyRate: 25 // $/hour
            },
            paid: {
                adSpend: 100, // minimum test budget
                managementCost: 25, // $/hour
                setupTime: 5 // hours
            },
            social: {
                postCreation: 15, // per post
                engagementTime: 2, // hours per day
                toolsCost: 50 // monthly tools
            }
        };
    }

    async analyze(opportunity) {
        try {
            const profitabilityData = await this.calculateProfitability(opportunity);
            const riskAssessment = this.assessRisk(opportunity, profitabilityData);
            const marketPosition = this.analyzeMarketPosition(opportunity);
            const scalabilityScore = this.assessScalability(opportunity);
            
            const finalScore = this.calculateFinalScore(
                profitabilityData,
                riskAssessment,
                marketPosition,
                scalabilityScore
            );

            return {
                score: Math.round(finalScore),
                profitability: profitabilityData,
                risk: riskAssessment,
                market: marketPosition,
                scalability: scalabilityScore,
                recommendations: this.generateRecommendations(opportunity, profitabilityData, riskAssessment)
            };

        } catch (error) {
            console.error('Profitability analysis error:', error);
            return {
                score: 0,
                error: error.message,
                fallbackScore: this.calculateFallbackScore(opportunity)
            };
        }
    }

    async calculateProfitability(opportunity) {
        const revenue = this.calculateRevenue(opportunity);
        const costs = this.calculateCosts(opportunity);
        const metrics = this.calculateMetrics(revenue, costs);
        
        return {
            revenue,
            costs,
            metrics,
            projections: this.calculateProjections(revenue, costs, opportunity)
        };
    }

    calculateRevenue(opportunity) {
        let revenueData = {
            commissionRate: 0,
            productPrice: 0,
            estimatedConversions: 0,
            monthlyRevenue: 0,
            annualRevenue: 0
        };

        // Extract revenue data based on opportunity type
        switch (opportunity.source) {
            case 'affiliate_scanner':
                revenueData = this.calculateAffiliateRevenue(opportunity);
                break;
            case 'social_trend_scanner':
                revenueData = this.calculateSocialTrendRevenue(opportunity);
                break;
            case 'seasonal_scanner':
                revenueData = this.calculateSeasonalRevenue(opportunity);
                break;
            case 'timing_optimizer':
                revenueData = this.calculateTimingRevenue(opportunity);
                break;
            default:
                revenueData = this.calculateGenericRevenue(opportunity);
        }

        return revenueData;
    }

    calculateAffiliateRevenue(opportunity) {
        const metrics = opportunity.metrics || {};
        const commissionRate = metrics.commissionRate || this.config.defaultCommissionRate;
        const productPrice = metrics.price || 100; // Default $100
        const conversionRate = metrics.conversion_rate || this.getIndustryBenchmark(opportunity.category, 'conversionRate');
        
        // Estimate traffic based on gravity/popularity
        const gravity = metrics.gravity || 10;
        const estimatedMonthlyTraffic = Math.min(gravity * 100, 10000); // Cap at 10k
        
        const monthlyConversions = estimatedMonthlyTraffic * conversionRate;
        const commissionPerSale = productPrice * commissionRate;
        const monthlyRevenue = monthlyConversions * commissionPerSale;
        
        return {
            commissionRate,
            productPrice,
            commissionPerSale,
            estimatedMonthlyTraffic,
            conversionRate,
            monthlyConversions,
            monthlyRevenue,
            annualRevenue: monthlyRevenue * 12,
            revenueConfidence: this.calculateRevenueConfidence(metrics)
        };
    }

    calculateSocialTrendRevenue(opportunity) {
        const metrics = opportunity.metrics || {};
        const engagement = metrics.total_engagement || 1000;
        const trendVelocity = metrics.trend_velocity || 0.1;
        
        // Estimate monetization potential from social trends
        const estimatedReach = engagement * (1 + trendVelocity);
        const conversionRate = this.getIndustryBenchmark(opportunity.category, 'conversionRate') * 0.5; // Lower for social
        const avgProductPrice = 50; // Typical info product price
        const avgCommission = this.getIndustryBenchmark(opportunity.category, 'avgCommission');
        
        const monthlyConversions = (estimatedReach * 0.1) * conversionRate; // 10% of reach clicks through
        const commissionPerSale = avgProductPrice * avgCommission;
        const monthlyRevenue = monthlyConversions * commissionPerSale;
        
        return {
            commissionRate: avgCommission,
            productPrice: avgProductPrice,
            commissionPerSale,
            estimatedReach,
            conversionRate,
            monthlyConversions,
            monthlyRevenue,
            annualRevenue: monthlyRevenue * 12,
            revenueConfidence: 0.6 // Lower confidence for social trends
        };
    }

    calculateSeasonalRevenue(opportunity) {
        const metrics = opportunity.metrics || {};
        const historicalPerformance = (metrics.historical_performance || 70) / 100;
        const marketDemand = (metrics.market_demand || 50) / 100;
        
        // Seasonal opportunities often have higher but time-limited revenue
        const seasonalMultiplier = 1 + (historicalPerformance * marketDemand);
        const baseBenchmark = this.getIndustryBenchmark(opportunity.category, 'avgCommission');
        
        const productPrice = 150; // Seasonal products often premium priced
        const commissionRate = baseBenchmark * seasonalMultiplier;
        const conversionRate = this.getIndustryBenchmark(opportunity.category, 'conversionRate') * seasonalMultiplier;
        
        // Estimate seasonal traffic spike
        const baseMonthlyTraffic = 2000;
        const seasonalTraffic = baseMonthlyTraffic * seasonalMultiplier;
        
        const monthlyConversions = seasonalTraffic * conversionRate;
        const commissionPerSale = productPrice * Math.min(commissionRate, 0.5); // Cap at 50%
        const monthlyRevenue = monthlyConversions * commissionPerSale;
        
        return {
            commissionRate: Math.min(commissionRate, 0.5),
            productPrice,
            commissionPerSale,
            estimatedMonthlyTraffic: seasonalTraffic,
            conversionRate,
            monthlyConversions,
            monthlyRevenue,
            annualRevenue: monthlyRevenue * 4, // Seasonal opportunities are limited time
            revenueConfidence: historicalPerformance,
            seasonalMultiplier
        };
    }

    calculateTimingRevenue(opportunity) {
        const metrics = opportunity.metrics || {};
        const marketActivity = (metrics.global_market_activity || 50) / 100;
        
        // Timing opportunities provide short-term boosts
        const timingMultiplier = 1 + (marketActivity * 0.5);
        const baseBenchmark = this.getIndustryBenchmark(opportunity.category, 'conversionRate');
        
        const productPrice = 100;
        const commissionRate = this.getIndustryBenchmark(opportunity.category, 'avgCommission');
        const conversionRate = baseBenchmark * timingMultiplier;
        
        const estimatedTraffic = 1000 * timingMultiplier;
        const monthlyConversions = estimatedTraffic * conversionRate;
        const commissionPerSale = productPrice * commissionRate;
        const monthlyRevenue = monthlyConversions * commissionPerSale;
        
        return {
            commissionRate,
            productPrice,
            commissionPerSale,
            estimatedMonthlyTraffic: estimatedTraffic,
            conversionRate,
            monthlyConversions,
            monthlyRevenue,
            annualRevenue: monthlyRevenue * 12,
            revenueConfidence: 0.7,
            timingMultiplier
        };
    }

    calculateGenericRevenue(opportunity) {
        // Fallback calculation for unknown opportunity types
        const category = opportunity.category || 'business';
        const score = opportunity.score || 50;
        const scoreMultiplier = score / 100;
        
        const conversionRate = this.getIndustryBenchmark(category, 'conversionRate') * scoreMultiplier;
        const commissionRate = this.getIndustryBenchmark(category, 'avgCommission');
        const productPrice = 75;
        
        const estimatedTraffic = 1500 * scoreMultiplier;
        const monthlyConversions = estimatedTraffic * conversionRate;
        const commissionPerSale = productPrice * commissionRate;
        const monthlyRevenue = monthlyConversions * commissionPerSale;
        
        return {
            commissionRate,
            productPrice,
            commissionPerSale,
            estimatedMonthlyTraffic: estimatedTraffic,
            conversionRate,
            monthlyConversions,
            monthlyRevenue,
            annualRevenue: monthlyRevenue * 12,
            revenueConfidence: 0.5
        };
    }

    calculateCosts(opportunity) {
        const category = opportunity.category || 'business';
        const trafficCost = this.getIndustryBenchmark(category, 'trafficCost');
        
        // Calculate different cost scenarios
        const organicCosts = this.calculateOrganicCosts(opportunity);
        const paidCosts = this.calculatePaidCosts(opportunity, trafficCost);
        const socialCosts = this.calculateSocialCosts(opportunity);
        
        return {
            organic: organicCosts,
            paid: paidCosts,
            social: socialCosts,
            recommended: this.selectOptimalCostStrategy(organicCosts, paidCosts, socialCosts)
        };
    }

    calculateOrganicCosts(opportunity) {
        const costs = this.marketingCosts.organic;
        const monthlyContentPieces = 8; // 2 per week
        const monthlyTimeInvestment = costs.timeInvestment * 4; // 4 weeks
        
        const contentCost = monthlyContentPieces * costs.contentCreation;
        const timeCost = monthlyTimeInvestment * costs.hourlyRate;
        const totalMonthlyCost = contentCost + timeCost;
        
        return {
            contentCreation: contentCost,
            timeInvestment: timeCost,
            totalMonthlyCost,
            annualCost: totalMonthlyCost * 12,
            costPerLead: totalMonthlyCost / Math.max(50, 1), // Assume 50 leads/month organic
            strategy: 'organic'
        };
    }

    calculatePaidCosts(opportunity, trafficCost) {
        const costs = this.marketingCosts.paid;
        const revenue = this.calculateRevenue(opportunity);
        const estimatedClicks = revenue.estimatedMonthlyTraffic || 1000;
        
        const adSpend = estimatedClicks * trafficCost;
        const managementTime = 10; // hours per month
        const managementCost = managementTime * costs.managementCost;
        const totalMonthlyCost = adSpend + managementCost;
        
        return {
            adSpend,
            managementCost,
            totalMonthlyCost,
            annualCost: totalMonthlyCost * 12,
            costPerClick: trafficCost,
            costPerLead: totalMonthlyCost / Math.max(revenue.monthlyConversions, 1),
            strategy: 'paid'
        };
    }

    calculateSocialCosts(opportunity) {
        const costs = this.marketingCosts.social;
        const postsPerMonth = 20; // Daily posting
        const engagementHours = costs.engagementTime * 30; // Daily engagement
        
        const postCreationCost = postsPerMonth * costs.postCreation;
        const engagementCost = engagementHours * 25; // $25/hour
        const toolsCost = costs.toolsCost;
        const totalMonthlyCost = postCreationCost + engagementCost + toolsCost;
        
        return {
            postCreation: postCreationCost,
            engagement: engagementCost,
            tools: toolsCost,
            totalMonthlyCost,
            annualCost: totalMonthlyCost * 12,
            costPerLead: totalMonthlyCost / Math.max(30, 1), // Assume 30 leads/month social
            strategy: 'social'
        };
    }

    calculateMetrics(revenue, costs) {
        const recommendedCosts = costs.recommended;
        const monthlyRevenue = revenue.monthlyRevenue;
        const monthlyCost = recommendedCosts.totalMonthlyCost;
        
        const monthlyProfit = monthlyRevenue - monthlyCost;
        const roi = monthlyCost > 0 ? (monthlyProfit / monthlyCost) * 100 : 0;
        const profitMargin = monthlyRevenue > 0 ? (monthlyProfit / monthlyRevenue) * 100 : 0;
        const paybackPeriod = monthlyProfit > 0 ? monthlyCost / monthlyProfit : Infinity;
        
        return {
            monthlyRevenue,
            monthlyCost,
            monthlyProfit,
            roi,
            profitMargin,
            paybackPeriod,
            breakEvenPoint: monthlyCost / (revenue.commissionPerSale || 1),
            ltv: this.calculateLTV(revenue),
            cac: this.calculateCAC(costs, revenue)
        };
    }

    calculateLTV(revenue) {
        // Simplified LTV calculation
        const monthlyValue = revenue.commissionPerSale || 25;
        const averageLifespan = 12; // months
        const retentionRate = 0.8; // 80% of customers make repeat purchases
        
        return monthlyValue * averageLifespan * retentionRate;
    }

    calculateCAC(costs, revenue) {
        // Customer Acquisition Cost
        const monthlyCost = costs.recommended.totalMonthlyCost;
        const monthlyCustomers = revenue.monthlyConversions || 1;
        
        return monthlyCost / monthlyCustomers;
    }

    calculateProjections(revenue, costs, opportunity) {
        const baseMetrics = this.calculateMetrics(revenue, costs);
        const projections = [];
        
        // Project 12 months with growth assumptions
        for (let month = 1; month <= 12; month++) {
            const growthRate = this.calculateGrowthRate(opportunity, month);
            const monthlyRev = revenue.monthlyRevenue * growthRate;
            const monthlyCost = costs.recommended.totalMonthlyCost * Math.sqrt(growthRate); // Costs scale slower
            const monthlyProfit = monthlyRev - monthlyCost;
            
            projections.push({
                month,
                revenue: monthlyRev,
                costs: monthlyCost,
                profit: monthlyProfit,
                roi: monthlyCost > 0 ? (monthlyProfit / monthlyCost) * 100 : 0,
                cumulativeProfit: projections.reduce((sum, p) => sum + p.profit, 0) + monthlyProfit
            });
        }
        
        return {
            monthly: projections,
            totalRevenue: projections.reduce((sum, p) => sum + p.revenue, 0),
            totalCosts: projections.reduce((sum, p) => sum + p.costs, 0),
            totalProfit: projections.reduce((sum, p) => sum + p.profit, 0),
            averageROI: projections.reduce((sum, p) => sum + p.roi, 0) / 12
        };
    }

    calculateGrowthRate(opportunity, month) {
        // Different growth patterns based on opportunity type
        switch (opportunity.source) {
            case 'affiliate_scanner':
                return 1 + (month * 0.05); // Steady 5% monthly growth
            case 'social_trend_scanner':
                return Math.max(1 - (month * 0.1), 0.3); // Declining trend
            case 'seasonal_scanner':
                // Seasonal spike and decline
                if (month <= 3) return 1 + (month * 0.3);
                return Math.max(1 - ((month - 3) * 0.2), 0.2);
            case 'timing_optimizer':
                return 1 + (month * 0.02); // Modest steady growth
            default:
                return 1 + (month * 0.03); // Default 3% monthly growth
        }
    }

    assessRisk(opportunity, profitabilityData) {
        const risks = {
            market: this.assessMarketRisk(opportunity),
            competition: this.assessCompetitionRisk(opportunity),
            execution: this.assessExecutionRisk(opportunity),
            financial: this.assessFinancialRisk(profitabilityData),
            timing: this.assessTimingRisk(opportunity)
        };
        
        const overallRiskScore = Object.values(risks).reduce((sum, risk) => sum + risk.score, 0) / Object.keys(risks).length;
        
        return {
            overall: {
                score: overallRiskScore,
                level: this.getRiskLevel(overallRiskScore)
            },
            breakdown: risks,
            mitigationStrategies: this.generateRiskMitigation(risks)
        };
    }

    assessMarketRisk(opportunity) {
        let riskScore = 30; // Base risk
        
        // Category risk assessment
        const categoryRisk = {
            finance: 40, // Regulated, competitive
            business: 30, // Moderate risk
            education: 20, // Lower risk
            lifestyle: 25 // Moderate-low risk
        };
        
        riskScore += categoryRisk[opportunity.category] || 30;
        
        // Market saturation risk
        if (opportunity.metrics?.competition_level > 80) riskScore += 20;
        if (opportunity.metrics?.market_demand < 40) riskScore += 15;
        
        return {
            score: Math.min(100, riskScore),
            factors: ['market_saturation', 'regulatory_risk', 'demand_volatility'],
            mitigation: 'Diversify across multiple markets and products'
        };
    }

    assessCompetitionRisk(opportunity) {
        let riskScore = 25; // Base risk
        
        // High competition indicators
        if (opportunity.metrics?.gravity > 50) riskScore += 15;
        if (opportunity.source === 'affiliate_scanner' && opportunity.metrics?.commission_rate > 0.4) riskScore += 10;
        
        // Social trend competition
        if (opportunity.source === 'social_trend_scanner' && opportunity.metrics?.trend_velocity < 0.3) riskScore += 20;
        
        return {
            score: Math.min(100, riskScore),
            factors: ['market_saturation', 'price_competition', 'entry_barriers'],
            mitigation: 'Focus on unique value proposition and niche positioning'
        };
    }

    assessExecutionRisk(opportunity) {
        let riskScore = 20; // Base risk
        
        // Complexity factors
        if (opportunity.type === 'seasonal_timing' && opportunity.metrics?.preparation_days < 7) riskScore += 25;
        if (opportunity.source === 'social_trend_scanner') riskScore += 15; // Social trends are harder to execute
        
        // Resource requirements
        const revenue = this.calculateRevenue(opportunity);
        if (revenue.revenueConfidence < 0.6) riskScore += 20;
        
        return {
            score: Math.min(100, riskScore),
            factors: ['complexity', 'resource_requirements', 'timeline_pressure'],
            mitigation: 'Start with MVP and iterate based on results'
        };
    }

    assessFinancialRisk(profitabilityData) {
        let riskScore = 15; // Base risk
        
        const metrics = profitabilityData.metrics;
        
        // Payback period risk
        if (metrics.paybackPeriod > this.config.maxPaybackPeriod) riskScore += 30;
        if (metrics.roi < this.config.minROI * 100) riskScore += 25;
        if (metrics.profitMargin < 20) riskScore += 20;
        
        return {
            score: Math.min(100, riskScore),
            factors: ['cash_flow', 'roi_uncertainty', 'cost_volatility'],
            mitigation: 'Start with smaller investment and scale based on performance'
        };
    }

    assessTimingRisk(opportunity) {
        let riskScore = 20; // Base risk
        
        // Time-sensitive opportunities have higher risk
        if (opportunity.expires_at) {
            const timeUntilExpiry = new Date(opportunity.expires_at) - new Date();
            const daysUntilExpiry = timeUntilExpiry / (1000 * 60 * 60 * 24);
            
            if (daysUntilExpiry < 7) riskScore += 30;
            else if (daysUntilExpiry < 30) riskScore += 15;
        }
        
        // Seasonal timing risk
        if (opportunity.source === 'seasonal_scanner') {
            if (opportunity.metrics?.days_until_event < 14) riskScore += 20;
        }
        
        return {
            score: Math.min(100, riskScore),
            factors: ['time_pressure', 'seasonality', 'market_timing'],
            mitigation: 'Have contingency plans and flexible execution timeline'
        };
    }

    analyzeMarketPosition(opportunity) {
        const category = opportunity.category || 'business';
        const benchmark = this.industryBenchmarks[category];
        
        let marketScore = 50; // Base score
        
        // Compare against industry benchmarks
        if (opportunity.metrics?.commission_rate > benchmark.avgCommission) marketScore += 15;
        if (opportunity.metrics?.conversion_rate > benchmark.conversionRate) marketScore += 15;
        
        // Competition analysis
        const competitionLevel = opportunity.metrics?.competition_level || 50;
        if (competitionLevel < 40) marketScore += 20; // Low competition is good
        else if (competitionLevel > 70) marketScore -= 15; // High competition is bad
        
        // Market demand
        const marketDemand = opportunity.metrics?.market_demand || 50;
        marketScore += (marketDemand - 50) * 0.3;
        
        return {
            score: Math.max(0, Math.min(100, marketScore)),
            position: this.getMarketPosition(marketScore),
            competitionLevel,
            marketDemand,
            opportunities: this.identifyMarketOpportunities(opportunity, marketScore),
            threats: this.identifyMarketThreats(opportunity, competitionLevel)
        };
    }

    assessScalability(opportunity) {
        let scalabilityScore = 50; // Base score
        
        // Scalability factors by source
        switch (opportunity.source) {
            case 'affiliate_scanner':
                scalabilityScore += 20; // Affiliate products are highly scalable
                if (opportunity.metrics?.network === 'digistore24') scalabilityScore += 5;
                break;
            case 'social_trend_scanner':
                scalabilityScore -= 10; // Social trends are less scalable
                if (opportunity.metrics?.viral_potential > 0.7) scalabilityScore += 15;
                break;
            case 'seasonal_scanner':
                scalabilityScore += 10; // Seasonal opportunities can be planned and scaled
                break;
            case 'timing_optimizer':
                scalabilityScore += 5; // Timing opportunities have moderate scalability
                break;
        }
        
        // Category scalability
        const categoryScalability = {
            finance: 15, // High scalability
            business: 20, // Very high scalability
            education: 25, // Highest scalability
            lifestyle: 10 // Moderate scalability
        };
        
        scalabilityScore += categoryScalability[opportunity.category] || 10;
        
        // Resource requirements
        const estimatedInvestment = this.calculateCosts(opportunity).recommended.totalMonthlyCost;
        if (estimatedInvestment < 500) scalabilityScore += 15; // Low barrier to entry
        
        return {
            score: Math.max(0, Math.min(100, scalabilityScore)),
            level: this.getScalabilityLevel(scalabilityScore),
            factors: this.getScalabilityFactors(opportunity),
            timeline: this.getScalabilityTimeline(opportunity),
            investmentRequired: this.getScalabilityInvestment(opportunity)
        };
    }

    calculateFinalScore(profitability, risk, market, scalability) {
        const weights = {
            profitability: 0.35,
            risk: 0.25, // Lower risk = higher score
            market: 0.25,
            scalability: 0.15
        };
        
        const profitabilityScore = this.normalizeProfitabilityScore(profitability);
        const riskScore = 100 - risk.overall.score; // Invert risk (lower risk = higher score)
        const marketScore = market.score;
        const scalabilityScore = scalability.score;
        
        const weightedScore = 
            (profitabilityScore * weights.profitability) +
            (riskScore * weights.risk) +
            (marketScore * weights.market) +
            (scalabilityScore * weights.scalability);
        
        return Math.max(0, Math.min(100, weightedScore));
    }

    normalizeProfitabilityScore(profitability) {
        const metrics = profitability.metrics;
        
        let score = 0;
        
        // ROI scoring (0-40 points)
        if (metrics.roi >= 300) score += 40;
        else if (metrics.roi >= 200) score += 35;
        else if (metrics.roi >= 150) score += 30;
        else if (metrics.roi >= 100) score += 25;
        else if (metrics.roi >= 50) score += 15;
        else score += Math.max(0, metrics.roi * 0.3);
        
        // Profit margin scoring (0-30 points)
        if (metrics.profitMargin >= 70) score += 30;
        else if (metrics.profitMargin >= 50) score += 25;
        else if (metrics.profitMargin >= 30) score += 20;
        else if (metrics.profitMargin >= 15) score += 15;
        else score += Math.max(0, metrics.profitMargin * 0.5);
        
        // Payback period scoring (0-20 points)
        if (metrics.paybackPeriod <= 1) score += 20;
        else if (metrics.paybackPeriod <= 3) score += 15;
        else if (metrics.paybackPeriod <= 6) score += 10;
        else if (metrics.paybackPeriod <= 12) score += 5;
        
        // Revenue potential scoring (0-10 points)
        if (metrics.monthlyRevenue >= 5000) score += 10;
        else if (metrics.monthlyRevenue >= 2000) score += 8;
        else if (metrics.monthlyRevenue >= 1000) score += 6;
        else if (metrics.monthlyRevenue >= 500) score += 4;
        else score += Math.max(0, metrics.monthlyRevenue * 0.008);
        
        return Math.min(100, score);
    }

    // Helper methods
    getIndustryBenchmark(category, metric) {
        const benchmark = this.industryBenchmarks[category] || this.industryBenchmarks.business;
        return benchmark[metric] || 0;
    }

    calculateRevenueConfidence(metrics) {
        let confidence = 0.5; // Base confidence
        
        if (metrics.conversion_rate) confidence += 0.2;
        if (metrics.sales_count > 100) confidence += 0.2;
        if (metrics.gravity > 20) confidence += 0.1;
        
        return Math.min(1, confidence);
    }

    selectOptimalCostStrategy(organic, paid, social) {
        const strategies = [
            { ...organic, roi: organic.totalMonthlyCost > 0 ? 1000 / organic.totalMonthlyCost : 0 },
            { ...paid, roi: paid.totalMonthlyCost > 0 ? 1000 / paid.totalMonthlyCost : 0 },
            { ...social, roi: social.totalMonthlyCost > 0 ? 1000 / social.totalMonthlyCost : 0 }
        ];
        
        return strategies.reduce((best, current) => current.roi > best.roi ? current : best);
    }

    getRiskLevel(score) {
        if (score <= 25) return 'low';
        if (score <= 50) return 'medium';
        if (score <= 75) return 'high';
        return 'very_high';
    }

    getMarketPosition(score) {
        if (score >= 80) return 'market_leader';
        if (score >= 60) return 'strong_position';
        if (score >= 40) return 'competitive';
        return 'challenging';
    }

    getScalabilityLevel(score) {
        if (score >= 80) return 'highly_scalable';
        if (score >= 60) return 'scalable';
        if (score >= 40) return 'moderately_scalable';
        return 'limited_scalability';
    }

    getScalabilityFactors(opportunity) {
        const factors = ['automation_potential', 'resource_requirements'];
        
        if (opportunity.source === 'affiliate_scanner') {
            factors.push('product_availability', 'commission_structure');
        }
        
        if (opportunity.category === 'education') {
            factors.push('content_reusability', 'evergreen_potential');
        }
        
        return factors;
    }

    getScalabilityTimeline(opportunity) {
        switch (opportunity.source) {
            case 'affiliate_scanner': return '3-6 months';
            case 'social_trend_scanner': return '1-3 months';
            case 'seasonal_scanner': return '6-12 months';
            default: return '3-9 months';
        }
    }

    getScalabilityInvestment(opportunity) {
        const costs = this.calculateCosts(opportunity);
        const monthlyCost = costs.recommended.totalMonthlyCost;
        
        return {
            initial: monthlyCost * 3,
            scaling: monthlyCost * 10,
            enterprise: monthlyCost * 50
        };
    }

    identifyMarketOpportunities(opportunity, marketScore) {
        const opportunities = [];
        
        if (marketScore > 60) {
            opportunities.push('Market expansion potential');
        }
        
        if (opportunity.metrics?.competition_level < 50) {
            opportunities.push('Low competition advantage');
        }
        
        if (opportunity.category === 'education') {
            opportunities.push('Evergreen content potential');
        }
        
        return opportunities;
    }

    identifyMarketThreats(opportunity, competitionLevel) {
        const threats = [];
        
        if (competitionLevel > 70) {
            threats.push('High market saturation');
        }
        
        if (opportunity.source === 'social_trend_scanner') {
            threats.push('Trend volatility');
        }
        
        if (opportunity.category === 'finance') {
            threats.push('Regulatory changes');
        }
        
        return threats;
    }

    generateRiskMitigation(risks) {
        const strategies = [];
        
        if (risks.market.score > 60) {
            strategies.push('Diversify across multiple markets and products');
        }
        
        if (risks.competition.score > 60) {
            strategies.push('Focus on unique value proposition and differentiation');
        }
        
        if (risks.financial.score > 60) {
            strategies.push('Start with lower investment and scale gradually');
        }
        
        if (risks.timing.score > 60) {
            strategies.push('Develop flexible timeline and contingency plans');
        }
        
        return strategies;
    }

    generateRecommendations(opportunity, profitability, risk) {
        const recommendations = [];
        
        // Investment recommendation
        if (profitability.metrics.roi > 200 && risk.overall.score < 50) {
            recommendations.push({
                type: 'investment',
                priority: 'high',
                action: 'Proceed with full investment',
                reasoning: 'High ROI with manageable risk'
            });
        } else if (profitability.metrics.roi > 100) {
            recommendations.push({
                type: 'investment',
                priority: 'medium',
                action: 'Start with test budget',
                reasoning: 'Positive ROI justifies testing'
            });
        }
        
        // Strategy recommendation
        const optimalStrategy = profitability.costs.recommended.strategy;
        recommendations.push({
            type: 'strategy',
            priority: 'high',
            action: `Use ${optimalStrategy} marketing approach`,
            reasoning: `${optimalStrategy} offers best cost-efficiency for this opportunity`
        });
        
        // Timing recommendation
        if (opportunity.source === 'seasonal_scanner' && opportunity.metrics?.days_until_event < 30) {
            recommendations.push({
                type: 'timing',
                priority: 'urgent',
                action: 'Execute immediately',
                reasoning: 'Limited time window for seasonal opportunity'
            });
        }
        
        return recommendations;
    }

    calculateFallbackScore(opportunity) {
        // Simple scoring when full analysis fails
        let score = 50; // Base score
        
        if (opportunity.score) score += (opportunity.score - 50) * 0.3;
        if (opportunity.category === 'finance' || opportunity.category === 'business') score += 10;
        if (opportunity.source === 'affiliate_scanner') score += 5;
        
        return Math.max(0, Math.min(100, score));
    }
}

module.exports = { ProfitabilityAnalyzer };