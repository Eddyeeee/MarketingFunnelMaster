class TrendVelocityAnalyzer {
    constructor(config = {}) {
        this.config = {
            timeWindows: config.timeWindows || [1, 6, 24, 168], // 1h, 6h, 24h, 1week in hours
            momentumThreshold: config.momentumThreshold || 0.3,
            volatilityThreshold: config.volatilityThreshold || 0.5,
            minDataPoints: config.minDataPoints || 5,
            ...config
        };

        this.trendHistory = new Map(); // Store historical trend data
        this.velocityCache = new Map(); // Cache velocity calculations
        this.momentumIndicators = new Set(['engagement_growth', 'volume_growth', 'sentiment_shift']);
    }

    async analyze(opportunity) {
        try {
            const velocityData = await this.calculateVelocity(opportunity);
            const momentumAnalysis = this.analyzeMomentum(opportunity, velocityData);
            const volatilityMetrics = this.calculateVolatility(opportunity, velocityData);
            const trendStrength = this.assessTrendStrength(velocityData, momentumAnalysis);
            const predictiveScore = this.generatePredictiveScore(velocityData, momentumAnalysis, volatilityMetrics);
            
            const finalScore = this.calculateFinalVelocityScore(
                velocityData,
                momentumAnalysis,
                volatilityMetrics,
                trendStrength,
                predictiveScore
            );

            return {
                score: Math.round(finalScore),
                velocity: velocityData,
                momentum: momentumAnalysis,
                volatility: volatilityMetrics,
                strength: trendStrength,
                prediction: predictiveScore,
                recommendations: this.generateVelocityRecommendations(velocityData, momentumAnalysis)
            };

        } catch (error) {
            console.error('Trend velocity analysis error:', error);
            return {
                score: 0,
                error: error.message,
                fallbackScore: this.calculateFallbackVelocityScore(opportunity)
            };
        }
    }

    async calculateVelocity(opportunity) {
        const velocityMetrics = {
            overall: 0,
            shortTerm: 0,    // 1-6 hours
            mediumTerm: 0,   // 6-24 hours
            longTerm: 0,     // 24+ hours
            acceleration: 0,
            direction: 'neutral',
            consistency: 0
        };

        // Calculate velocity based on opportunity source
        switch (opportunity.source) {
            case 'social_trend_scanner':
                velocityMetrics = await this.calculateSocialVelocity(opportunity);
                break;
            case 'affiliate_scanner':
                velocityMetrics = await this.calculateAffiliateVelocity(opportunity);
                break;
            case 'seasonal_scanner':
                velocityMetrics = await this.calculateSeasonalVelocity(opportunity);
                break;
            case 'timing_optimizer':
                velocityMetrics = await this.calculateTimingVelocity(opportunity);
                break;
            default:
                velocityMetrics = await this.calculateGenericVelocity(opportunity);
        }

        // Store in history for future analysis
        this.updateTrendHistory(opportunity.id, velocityMetrics);

        return velocityMetrics;
    }

    async calculateSocialVelocity(opportunity) {
        const metrics = opportunity.metrics || {};
        const trendVelocity = metrics.trend_velocity || 0;
        const totalEngagement = metrics.total_engagement || 0;
        const averageEngagement = metrics.average_engagement || 0;
        const viralPotential = metrics.viral_potential || 0;

        // Calculate different time window velocities
        const shortTermVelocity = this.calculateTimeWindowVelocity(opportunity, 1); // 1 hour
        const mediumTermVelocity = this.calculateTimeWindowVelocity(opportunity, 6); // 6 hours
        const longTermVelocity = this.calculateTimeWindowVelocity(opportunity, 24); // 24 hours

        // Calculate acceleration (change in velocity)
        const historicalVelocity = this.getHistoricalVelocity(opportunity.id);
        const acceleration = historicalVelocity ? trendVelocity - historicalVelocity.overall : 0;

        // Determine trend direction
        const direction = this.determineTrendDirection(trendVelocity, acceleration, viralPotential);

        // Calculate consistency score
        const consistency = this.calculateConsistency([shortTermVelocity, mediumTermVelocity, longTermVelocity]);

        return {
            overall: trendVelocity,
            shortTerm: shortTermVelocity,
            mediumTerm: mediumTermVelocity,
            longTerm: longTermVelocity,
            acceleration,
            direction,
            consistency,
            rawMetrics: {
                engagement: totalEngagement,
                averageEngagement,
                viralPotential,
                platform: metrics.platform || 'unknown'
            }
        };
    }

    async calculateAffiliateVelocity(opportunity) {
        const metrics = opportunity.metrics || {};
        const gravity = metrics.gravity || 0;
        const salesCount = metrics.sales_count || 0;
        const commissionRate = metrics.commission_rate || 0;

        // Estimate velocity based on gravity changes and sales momentum
        const gravityVelocity = Math.min(gravity / 100, 1); // Normalize gravity to 0-1
        const salesVelocity = this.estimateSalesVelocity(salesCount, opportunity.discovered_at);
        const commissionVelocity = Math.min(commissionRate * 2, 1); // High commission = high velocity

        const overall = (gravityVelocity + salesVelocity + commissionVelocity) / 3;

        // Affiliate opportunities typically have slower but steadier velocity
        const shortTerm = overall * 0.7;
        const mediumTerm = overall * 0.9;
        const longTerm = overall * 1.1;

        const historicalVelocity = this.getHistoricalVelocity(opportunity.id);
        const acceleration = historicalVelocity ? overall - historicalVelocity.overall : 0;

        return {
            overall,
            shortTerm,
            mediumTerm,
            longTerm,
            acceleration,
            direction: acceleration > 0.1 ? 'up' : acceleration < -0.1 ? 'down' : 'stable',
            consistency: 0.8, // Affiliate opportunities are generally consistent
            rawMetrics: {
                gravity,
                salesCount,
                commissionRate,
                network: metrics.network || 'unknown'
            }
        };
    }

    async calculateSeasonalVelocity(opportunity) {
        const metrics = opportunity.metrics || {};
        const daysUntilEvent = metrics.days_until_event || metrics.days_until_peak || 0;
        const historicalPerformance = (metrics.historical_performance || 50) / 100;
        const marketDemand = (metrics.market_demand || 50) / 100;

        // Seasonal velocity increases as the event approaches
        const timeFactorVelocity = daysUntilEvent > 0 ? Math.max(0, (60 - daysUntilEvent) / 60) : 0;
        const demandVelocity = marketDemand * historicalPerformance;
        
        const overall = (timeFactorVelocity + demandVelocity) / 2;

        // Seasonal opportunities have predictable velocity patterns
        const seasonalPattern = this.getSeasonalPattern(opportunity);
        const shortTerm = overall * seasonalPattern.shortTermMultiplier;
        const mediumTerm = overall * seasonalPattern.mediumTermMultiplier;
        const longTerm = overall * seasonalPattern.longTermMultiplier;

        const acceleration = this.calculateSeasonalAcceleration(daysUntilEvent, historicalPerformance);

        return {
            overall,
            shortTerm,
            mediumTerm,
            longTerm,
            acceleration,
            direction: daysUntilEvent < 30 && daysUntilEvent > 0 ? 'up' : 'stable',
            consistency: historicalPerformance, // Historical performance indicates consistency
            rawMetrics: {
                daysUntilEvent,
                historicalPerformance: metrics.historical_performance,
                marketDemand: metrics.market_demand,
                seasonType: metrics.season_type || 'unknown'
            }
        };
    }

    async calculateTimingVelocity(opportunity) {
        const metrics = opportunity.metrics || {};
        const globalActivity = (metrics.global_market_activity || 50) / 100;
        const marketActivity = metrics.market_activity || {};
        
        // Calculate velocity based on current market conditions
        const activityVelocity = globalActivity;
        const timingVelocity = this.calculateOptimalTimingVelocity(opportunity);
        
        const overall = (activityVelocity + timingVelocity) / 2;

        // Timing opportunities have rapid but short-lived velocity
        const shortTerm = overall;
        const mediumTerm = overall * 0.7; // Decreases over time
        const longTerm = overall * 0.4; // Further decreases

        const acceleration = this.calculateTimingAcceleration(globalActivity);

        return {
            overall,
            shortTerm,
            mediumTerm,
            longTerm,
            acceleration,
            direction: globalActivity > 0.7 ? 'up' : globalActivity < 0.3 ? 'down' : 'stable',
            consistency: 0.5, // Timing opportunities are inherently inconsistent
            rawMetrics: {
                globalActivity: metrics.global_market_activity,
                marketActivity,
                timingType: metrics.timing_type || 'unknown'
            }
        };
    }

    async calculateGenericVelocity(opportunity) {
        const score = opportunity.score || 50;
        const scoreVelocity = Math.min(score / 100, 1);
        
        // Generic opportunities have moderate, stable velocity
        const overall = scoreVelocity * 0.6; // Conservative estimate
        
        return {
            overall,
            shortTerm: overall * 0.9,
            mediumTerm: overall,
            longTerm: overall * 1.1,
            acceleration: 0,
            direction: 'stable',
            consistency: 0.7,
            rawMetrics: {
                score,
                type: opportunity.type || 'unknown'
            }
        };
    }

    calculateTimeWindowVelocity(opportunity, timeWindowHours) {
        const baseVelocity = opportunity.metrics?.trend_velocity || 0;
        
        // Adjust velocity based on time window
        const timeMultipliers = {
            1: 1.2,    // 1 hour - higher volatility
            6: 1.0,    // 6 hours - baseline
            24: 0.8,   // 24 hours - smoother trend
            168: 0.6   // 1 week - long-term trend
        };
        
        return baseVelocity * (timeMultipliers[timeWindowHours] || 1.0);
    }

    analyzeMomentum(opportunity, velocityData) {
        const momentum = {
            strength: 0,
            direction: velocityData.direction,
            sustainability: 0,
            indicators: [],
            signals: []
        };

        // Calculate momentum strength
        momentum.strength = this.calculateMomentumStrength(velocityData);
        
        // Assess sustainability
        momentum.sustainability = this.assessMomentumSustainability(opportunity, velocityData);
        
        // Identify momentum indicators
        momentum.indicators = this.identifyMomentumIndicators(opportunity, velocityData);
        
        // Generate momentum signals
        momentum.signals = this.generateMomentumSignals(velocityData, momentum);

        return momentum;
    }

    calculateMomentumStrength(velocityData) {
        const { overall, acceleration, consistency } = velocityData;
        
        // Combine velocity, acceleration, and consistency
        const velocityScore = overall * 40; // 0-40 points
        const accelerationScore = Math.min(Math.abs(acceleration) * 30, 30); // 0-30 points
        const consistencyScore = consistency * 30; // 0-30 points
        
        return Math.min(100, velocityScore + accelerationScore + consistencyScore);
    }

    assessMomentumSustainability(opportunity, velocityData) {
        let sustainabilityScore = 50; // Base score
        
        // Source-based sustainability
        switch (opportunity.source) {
            case 'affiliate_scanner':
                sustainabilityScore += 20; // Generally sustainable
                break;
            case 'social_trend_scanner':
                sustainabilityScore -= 20; // Less sustainable
                if (velocityData.rawMetrics.viralPotential > 0.7) sustainabilityScore += 15;
                break;
            case 'seasonal_scanner':
                sustainabilityScore += 15; // Predictable sustainability
                break;
            case 'timing_optimizer':
                sustainabilityScore -= 30; // Short-term sustainability
                break;
        }
        
        // Consistency impact
        sustainabilityScore += (velocityData.consistency - 0.5) * 40;
        
        // Acceleration impact
        if (velocityData.acceleration > 0.2) sustainabilityScore += 10;
        else if (velocityData.acceleration < -0.2) sustainabilityScore -= 15;
        
        return Math.max(0, Math.min(100, sustainabilityScore));
    }

    identifyMomentumIndicators(opportunity, velocityData) {
        const indicators = [];
        
        // Velocity-based indicators
        if (velocityData.overall > 0.6) indicators.push('high_velocity');
        if (velocityData.acceleration > 0.3) indicators.push('accelerating');
        if (velocityData.consistency > 0.7) indicators.push('consistent_growth');
        
        // Source-specific indicators
        if (opportunity.source === 'social_trend_scanner') {
            const metrics = velocityData.rawMetrics;
            if (metrics.viralPotential > 0.6) indicators.push('viral_potential');
            if (metrics.engagement > 10000) indicators.push('high_engagement');
        }
        
        if (opportunity.source === 'affiliate_scanner') {
            const metrics = velocityData.rawMetrics;
            if (metrics.gravity > 50) indicators.push('high_gravity');
            if (metrics.commissionRate > 0.3) indicators.push('high_commission');
        }
        
        return indicators;
    }

    generateMomentumSignals(velocityData, momentum) {
        const signals = [];
        
        // Buy/sell signals based on momentum
        if (momentum.strength > 70 && velocityData.direction === 'up') {
            signals.push({
                type: 'strong_buy',
                confidence: 0.8,
                reason: 'High momentum with upward trend'
            });
        } else if (momentum.strength > 50 && velocityData.acceleration > 0.2) {
            signals.push({
                type: 'buy',
                confidence: 0.6,
                reason: 'Positive momentum building'
            });
        } else if (momentum.strength < 30 || velocityData.direction === 'down') {
            signals.push({
                type: 'wait',
                confidence: 0.7,
                reason: 'Low momentum or downward trend'
            });
        }
        
        // Timing signals
        if (velocityData.shortTerm > velocityData.longTerm * 1.2) {
            signals.push({
                type: 'immediate_action',
                confidence: 0.8,
                reason: 'Short-term velocity exceeds long-term trend'
            });
        }
        
        return signals;
    }

    calculateVolatility(opportunity, velocityData) {
        const volatilityMetrics = {
            level: 0,
            risk: 'medium',
            predictability: 0,
            factors: []
        };

        // Calculate volatility based on velocity consistency
        const velocityRange = Math.abs(velocityData.shortTerm - velocityData.longTerm);
        const accelerationVolatility = Math.abs(velocityData.acceleration);
        
        volatilityMetrics.level = (velocityRange + accelerationVolatility) / 2;
        
        // Risk assessment
        if (volatilityMetrics.level > this.config.volatilityThreshold) {
            volatilityMetrics.risk = 'high';
        } else if (volatilityMetrics.level < 0.2) {
            volatilityMetrics.risk = 'low';
        }
        
        // Predictability (inverse of volatility, adjusted by consistency)
        volatilityMetrics.predictability = (1 - volatilityMetrics.level) * velocityData.consistency;
        
        // Identify volatility factors
        volatilityMetrics.factors = this.identifyVolatilityFactors(opportunity, velocityData);
        
        return volatilityMetrics;
    }

    identifyVolatilityFactors(opportunity, velocityData) {
        const factors = [];
        
        // Source-based factors
        if (opportunity.source === 'social_trend_scanner') {
            factors.push('social_media_volatility');
            if (velocityData.rawMetrics.platform === 'tiktok') factors.push('high_platform_volatility');
        }
        
        if (opportunity.source === 'timing_optimizer') {
            factors.push('market_timing_volatility');
        }
        
        // Velocity-based factors
        if (Math.abs(velocityData.acceleration) > 0.3) {
            factors.push('acceleration_volatility');
        }
        
        if (velocityData.consistency < 0.4) {
            factors.push('trend_inconsistency');
        }
        
        return factors;
    }

    assessTrendStrength(velocityData, momentumAnalysis) {
        const strength = {
            overall: 0,
            components: {
                velocity: 0,
                momentum: 0,
                consistency: 0,
                direction: 0
            },
            level: 'weak'
        };

        // Component scores
        strength.components.velocity = Math.min(velocityData.overall * 100, 100);
        strength.components.momentum = momentumAnalysis.strength;
        strength.components.consistency = velocityData.consistency * 100;
        strength.components.direction = this.scoreDirection(velocityData.direction);

        // Overall strength calculation
        strength.overall = (
            strength.components.velocity * 0.3 +
            strength.components.momentum * 0.3 +
            strength.components.consistency * 0.2 +
            strength.components.direction * 0.2
        );

        // Strength level classification
        if (strength.overall >= 80) strength.level = 'very_strong';
        else if (strength.overall >= 60) strength.level = 'strong';
        else if (strength.overall >= 40) strength.level = 'moderate';
        else if (strength.overall >= 20) strength.level = 'weak';
        else strength.level = 'very_weak';

        return strength;
    }

    generatePredictiveScore(velocityData, momentumAnalysis, volatilityMetrics) {
        const prediction = {
            shortTerm: { score: 0, confidence: 0, direction: 'neutral' },
            mediumTerm: { score: 0, confidence: 0, direction: 'neutral' },
            longTerm: { score: 0, confidence: 0, direction: 'neutral' },
            overall: 0
        };

        // Short-term prediction (1-7 days)
        prediction.shortTerm = this.predictShortTerm(velocityData, momentumAnalysis, volatilityMetrics);
        
        // Medium-term prediction (1-4 weeks)
        prediction.mediumTerm = this.predictMediumTerm(velocityData, momentumAnalysis);
        
        // Long-term prediction (1-6 months)
        prediction.longTerm = this.predictLongTerm(velocityData, momentumAnalysis);
        
        // Overall predictive score
        prediction.overall = (
            prediction.shortTerm.score * 0.5 +
            prediction.mediumTerm.score * 0.3 +
            prediction.longTerm.score * 0.2
        );

        return prediction;
    }

    predictShortTerm(velocityData, momentumAnalysis, volatilityMetrics) {
        let score = velocityData.shortTerm * 100;
        let confidence = 0.7; // Base confidence
        
        // Adjust based on momentum
        if (momentumAnalysis.strength > 70) {
            score += 15;
            confidence += 0.15;
        }
        
        // Adjust based on volatility
        if (volatilityMetrics.level > 0.5) {
            confidence -= 0.2;
        } else {
            confidence += 0.1;
        }
        
        // Direction prediction
        const direction = momentumAnalysis.direction;
        
        return {
            score: Math.min(100, score),
            confidence: Math.max(0, Math.min(1, confidence)),
            direction
        };
    }

    predictMediumTerm(velocityData, momentumAnalysis) {
        let score = velocityData.mediumTerm * 100;
        let confidence = 0.6; // Base confidence
        
        // Sustainability impact
        if (momentumAnalysis.sustainability > 60) {
            score += 10;
            confidence += 0.1;
        } else if (momentumAnalysis.sustainability < 40) {
            score -= 10;
            confidence -= 0.1;
        }
        
        const direction = velocityData.acceleration > 0 ? 'up' : 
                         velocityData.acceleration < 0 ? 'down' : 'stable';
        
        return {
            score: Math.min(100, Math.max(0, score)),
            confidence: Math.max(0, Math.min(1, confidence)),
            direction
        };
    }

    predictLongTerm(velocityData, momentumAnalysis) {
        let score = velocityData.longTerm * 100;
        let confidence = 0.4; // Lower confidence for long-term
        
        // Consistency is key for long-term prediction
        score += velocityData.consistency * 20;
        confidence += velocityData.consistency * 0.3;
        
        const direction = momentumAnalysis.sustainability > 50 ? 'stable' : 'declining';
        
        return {
            score: Math.min(100, Math.max(0, score)),
            confidence: Math.max(0, Math.min(1, confidence)),
            direction
        };
    }

    calculateFinalVelocityScore(velocityData, momentumAnalysis, volatilityMetrics, trendStrength, predictiveScore) {
        const weights = {
            velocity: 0.25,
            momentum: 0.25,
            stability: 0.2, // Inverse of volatility
            strength: 0.15,
            prediction: 0.15
        };

        const velocityScore = velocityData.overall * 100;
        const momentumScore = momentumAnalysis.strength;
        const stabilityScore = (1 - volatilityMetrics.level) * 100;
        const strengthScore = trendStrength.overall;
        const predictionScore = predictiveScore.overall;

        const weightedScore = 
            (velocityScore * weights.velocity) +
            (momentumScore * weights.momentum) +
            (stabilityScore * weights.stability) +
            (strengthScore * weights.strength) +
            (predictionScore * weights.prediction);

        return Math.max(0, Math.min(100, weightedScore));
    }

    // Helper methods
    updateTrendHistory(opportunityId, velocityData) {
        if (!this.trendHistory.has(opportunityId)) {
            this.trendHistory.set(opportunityId, []);
        }
        
        const history = this.trendHistory.get(opportunityId);
        history.push({
            timestamp: Date.now(),
            velocity: velocityData.overall,
            acceleration: velocityData.acceleration
        });
        
        // Keep only last 24 data points
        if (history.length > 24) {
            history.shift();
        }
    }

    getHistoricalVelocity(opportunityId) {
        const history = this.trendHistory.get(opportunityId);
        if (!history || history.length === 0) return null;
        
        return history[history.length - 2]; // Previous velocity
    }

    determineTrendDirection(velocity, acceleration, viralPotential = 0) {
        if (acceleration > 0.1 || (velocity > 0.6 && viralPotential > 0.6)) return 'up';
        if (acceleration < -0.1 || velocity < 0.2) return 'down';
        return 'stable';
    }

    calculateConsistency(velocities) {
        if (velocities.length < 2) return 0.5;
        
        const mean = velocities.reduce((sum, v) => sum + v, 0) / velocities.length;
        const variance = velocities.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / velocities.length;
        const standardDeviation = Math.sqrt(variance);
        
        // Consistency is inverse of coefficient of variation
        const coefficientOfVariation = mean > 0 ? standardDeviation / mean : 1;
        return Math.max(0, 1 - coefficientOfVariation);
    }

    estimateSalesVelocity(salesCount, discoveredAt) {
        if (!discoveredAt) return 0.5; // Default
        
        const daysSinceDiscovery = (Date.now() - new Date(discoveredAt).getTime()) / (1000 * 60 * 60 * 24);
        if (daysSinceDiscovery <= 0) return 0.5;
        
        const salesPerDay = salesCount / daysSinceDiscovery;
        return Math.min(salesPerDay / 100, 1); // Normalize to 0-1
    }

    getSeasonalPattern(opportunity) {
        const daysUntil = opportunity.metrics?.days_until_event || 30;
        
        if (daysUntil <= 7) {
            return { shortTermMultiplier: 1.5, mediumTermMultiplier: 1.2, longTermMultiplier: 0.8 };
        } else if (daysUntil <= 30) {
            return { shortTermMultiplier: 1.2, mediumTermMultiplier: 1.3, longTermMultiplier: 1.0 };
        } else {
            return { shortTermMultiplier: 1.0, mediumTermMultiplier: 1.1, longTermMultiplier: 1.2 };
        }
    }

    calculateSeasonalAcceleration(daysUntilEvent, historicalPerformance) {
        if (daysUntilEvent <= 0) return -0.5; // Event passed
        if (daysUntilEvent <= 7) return 0.8; // High acceleration near event
        if (daysUntilEvent <= 30) return 0.4; // Moderate acceleration
        return 0.1; // Low acceleration
    }

    calculateOptimalTimingVelocity(opportunity) {
        const timingType = opportunity.metrics?.timing_type;
        
        switch (timingType) {
            case 'market_timing': return 0.8;
            case 'event_timing': return 0.9;
            case 'cycle_timing': return 0.6;
            default: return 0.5;
        }
    }

    calculateTimingAcceleration(globalActivity) {
        if (globalActivity > 0.8) return 0.6;
        if (globalActivity > 0.6) return 0.3;
        if (globalActivity < 0.3) return -0.3;
        return 0;
    }

    scoreDirection(direction) {
        switch (direction) {
            case 'up': return 100;
            case 'stable': return 70;
            case 'down': return 20;
            default: return 50;
        }
    }

    generateVelocityRecommendations(velocityData, momentumAnalysis) {
        const recommendations = [];
        
        // High velocity recommendations
        if (velocityData.overall > 0.7) {
            recommendations.push({
                type: 'timing',
                priority: 'high',
                action: 'Act immediately',
                reasoning: 'High velocity trend - optimal entry point'
            });
        }
        
        // Momentum-based recommendations
        if (momentumAnalysis.strength > 70 && momentumAnalysis.sustainability > 60) {
            recommendations.push({
                type: 'investment',
                priority: 'high',
                action: 'Increase investment',
                reasoning: 'Strong sustainable momentum detected'
            });
        }
        
        // Low velocity recommendations
        if (velocityData.overall < 0.3) {
            recommendations.push({
                type: 'strategy',
                priority: 'medium',
                action: 'Wait for better velocity',
                reasoning: 'Current velocity too low for optimal results'
            });
        }
        
        // Acceleration recommendations
        if (velocityData.acceleration > 0.3) {
            recommendations.push({
                type: 'scaling',
                priority: 'high',
                action: 'Scale quickly',
                reasoning: 'Positive acceleration indicates growing opportunity'
            });
        }
        
        return recommendations;
    }

    calculateFallbackVelocityScore(opportunity) {
        // Simple scoring when full analysis fails
        let score = 40; // Conservative base score
        
        if (opportunity.score > 70) score += 20;
        if (opportunity.source === 'social_trend_scanner') score += 15;
        if (opportunity.metrics?.trend_velocity) score += opportunity.metrics.trend_velocity * 30;
        
        return Math.max(0, Math.min(100, score));
    }

    getStats() {
        return {
            trendHistorySize: this.trendHistory.size,
            cacheSize: this.velocityCache.size,
            timeWindows: this.config.timeWindows,
            momentumIndicators: Array.from(this.momentumIndicators)
        };
    }
}

module.exports = { TrendVelocityAnalyzer };