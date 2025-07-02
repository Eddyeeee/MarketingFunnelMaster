/**
 * Creator Intelligence Bridge
 * 
 * Bridges the Node.js intelligence system with the Python Universal Creator Analyzer
 * Automatically triggers creator analysis for every opportunity found
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
const EventEmitter = require('events');

class CreatorIntelligenceBridge extends EventEmitter {
    constructor(config = {}) {
        super();
        
        this.config = {
            pythonPath: config.pythonPath || 'python3',
            analysisTimeout: config.analysisTimeout || 300000, // 5 minutes
            maxConcurrentAnalyses: config.maxConcurrentAnalyses || 3,
            retryFailedAnalyses: config.retryFailedAnalyses || true,
            maxRetries: config.maxRetries || 2,
            ...config
        };
        
        this.activeAnalyses = new Map();
        this.analysisQueue = [];
        this.stats = {
            totalOpportunities: 0,
            successfulAnalyses: 0,
            failedAnalyses: 0,
            averageProcessingTime: 0,
            nichesCovered: new Set(),
            creatorsDiscovered: 0
        };
        
        this.pythonScriptPath = path.join(__dirname, '..', 'ai-research', 'opportunity_driven_pipeline.py');
        
        // Initialize
        this.initialize();
    }
    
    async initialize() {
        try {
            // Verify Python script exists
            await fs.access(this.pythonScriptPath);
            
            // Verify Python environment
            await this.verifyPythonEnvironment();
            
            console.log('✅ Creator Intelligence Bridge initialized successfully');
            this.emit('ready');
            
        } catch (error) {
            console.error('❌ Failed to initialize Creator Intelligence Bridge:', error.message);
            this.emit('error', error);
        }
    }
    
    async verifyPythonEnvironment() {
        return new Promise((resolve, reject) => {
            const pythonCheck = spawn(this.config.pythonPath, ['-c', 'import asyncio, sqlite3, spacy, langchain; print("OK")']);
            
            let output = '';
            pythonCheck.stdout.on('data', (data) => {
                output += data.toString();
            });
            
            pythonCheck.stderr.on('data', (data) => {
                console.warn('Python environment warning:', data.toString());
            });
            
            pythonCheck.on('close', (code) => {
                if (code === 0 && output.includes('OK')) {
                    resolve();
                } else {
                    reject(new Error('Python environment verification failed'));
                }
            });
        });
    }
    
    /**
     * Analyze opportunity - main entry point from intelligence system
     */
    async analyzeOpportunity(opportunityData) {
        const analysisId = `analysis_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        console.log(`🔍 Starting creator analysis for opportunity: ${opportunityData.title || opportunityData.product_name || 'Unknown'}`);
        
        // Add to queue if at capacity
        if (this.activeAnalyses.size >= this.config.maxConcurrentAnalyses) {
            this.analysisQueue.push({ analysisId, opportunityData });
            console.log(`📋 Queued analysis ${analysisId} (queue size: ${this.analysisQueue.length})`);
            return analysisId;
        }
        
        // Start analysis
        return this.startAnalysis(analysisId, opportunityData);
    }
    
    async startAnalysis(analysisId, opportunityData) {
        const startTime = Date.now();
        
        try {
            // Mark as active
            this.activeAnalyses.set(analysisId, {
                startTime,
                opportunityData,
                status: 'running'
            });
            
            // Prepare data for Python script
            const analysisData = this.prepareAnalysisData(opportunityData);
            
            // Execute Python analysis
            const result = await this.executePythonAnalysis(analysisData);
            
            // Process results
            const processedResult = await this.processAnalysisResult(result, opportunityData);
            
            // Update statistics
            const processingTime = Date.now() - startTime;
            this.updateStats(true, processingTime, processedResult);
            
            // Remove from active analyses
            this.activeAnalyses.delete(analysisId);
            
            // Process next in queue
            this.processNextInQueue();
            
            console.log(`✅ Completed creator analysis ${analysisId} in ${processingTime}ms`);
            
            // Emit success event
            this.emit('analysisComplete', {
                analysisId,
                opportunityData,
                result: processedResult,
                processingTime
            });
            
            return processedResult;
            
        } catch (error) {
            console.error(`❌ Creator analysis ${analysisId} failed:`, error.message);
            
            // Update statistics
            const processingTime = Date.now() - startTime;
            this.updateStats(false, processingTime);
            
            // Remove from active analyses
            this.activeAnalyses.delete(analysisId);
            
            // Process next in queue
            this.processNextInQueue();
            
            // Emit error event
            this.emit('analysisError', {
                analysisId,
                opportunityData,
                error: error.message,
                processingTime
            });
            
            throw error;
        }
    }
    
    prepareAnalysisData(opportunityData) {
        // Convert intelligence system data format to Python pipeline format
        return {
            opportunity_id: opportunityData.id || `opp_${Date.now()}`,
            opportunity_type: this.determineOpportunityType(opportunityData),
            title: opportunityData.title || opportunityData.product_name || 'Unknown Opportunity',
            description: opportunityData.description || opportunityData.niche || '',
            platform: opportunityData.platform || 'unknown',
            source: opportunityData.source || 'intelligence_system',
            metadata: {
                ...opportunityData,
                commission_rate: opportunityData.commission_rate || opportunityData.commission,
                price: opportunityData.price,
                gravity: opportunityData.gravity,
                category: opportunityData.category || opportunityData.niche,
                vendor: opportunityData.vendor,
                marketplace: opportunityData.marketplace,
                trending_score: opportunityData.trending_score,
                social_mentions: opportunityData.social_mentions,
                seasonal_factor: opportunityData.seasonal_factor
            },
            priority_score: opportunityData.opportunity_score || 0.5,
            created_at: new Date().toISOString(),
            raw_data: opportunityData
        };
    }
    
    determineOpportunityType(opportunityData) {
        // Determine opportunity type based on data structure
        if (opportunityData.product_name || opportunityData.marketplace) {
            return 'affiliate_product';
        } else if (opportunityData.trending_score || opportunityData.social_mentions) {
            return 'social_trend';
        } else if (opportunityData.seasonal_factor) {
            return 'seasonal_opportunity';
        } else if (opportunityData.niche) {
            return 'content_opportunity';
        } else {
            return 'market_gap';
        }
    }
    
    async executePythonAnalysis(analysisData) {
        return new Promise((resolve, reject) => {
            const pythonProcess = spawn(this.config.pythonPath, [
                this.pythonScriptPath,
                '--analyze-single',
                JSON.stringify(analysisData)
            ]);
            
            let stdout = '';
            let stderr = '';
            
            pythonProcess.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            
            pythonProcess.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                    try {
                        // Parse JSON result from Python
                        const result = JSON.parse(stdout.trim());
                        resolve(result);
                    } catch (parseError) {
                        reject(new Error(`Failed to parse Python output: ${parseError.message}`));
                    }
                } else {
                    reject(new Error(`Python analysis failed with code ${code}: ${stderr}`));
                }
            });
            
            pythonProcess.on('error', (error) => {
                reject(new Error(`Failed to start Python analysis: ${error.message}`));
            });
            
            // Set timeout
            setTimeout(() => {
                pythonProcess.kill();
                reject(new Error('Python analysis timed out'));
            }, this.config.analysisTimeout);
        });
    }
    
    async processAnalysisResult(rawResult, originalOpportunity) {
        // Process and enhance the Python analysis result
        const processedResult = {
            analysis_id: rawResult.analysis_id || `analysis_${Date.now()}`,
            opportunity_id: originalOpportunity.id,
            
            // Niche Analysis
            niche: {
                primary_niche: rawResult.niche_analysis?.primary_niche,
                secondary_niches: rawResult.niche_analysis?.secondary_niches || [],
                confidence_score: rawResult.niche_analysis?.confidence_score || 0,
                keywords: rawResult.niche_analysis?.keywords || [],
                language: rawResult.niche_analysis?.language || 'en',
                market_size: rawResult.niche_analysis?.market_size || 'unknown',
                competition_level: rawResult.niche_analysis?.competition_level || 'unknown'
            },
            
            // Creator Intelligence
            creators: {
                total_found: rawResult.creator_insights?.top_creators?.length || 0,
                top_creators: (rawResult.creator_insights?.top_creators || []).slice(0, 10).map(creator => ({
                    name: creator.name,
                    platform: creator.platform,
                    followers: creator.followers,
                    engagement_rate: creator.engagement_rate,
                    influence_score: creator.influence_score,
                    niche: creator.niche,
                    url: creator.url
                })),
                platform_distribution: rawResult.creator_insights?.platform_distribution || {},
                common_strategies: rawResult.creator_insights?.common_strategies || [],
                trending_formats: rawResult.creator_insights?.trending_formats || []
            },
            
            // Pattern Analysis
            patterns: {
                universal_hooks: (rawResult.pattern_analysis?.universal_hooks || []).slice(0, 5).map(hook => ({
                    name: hook.name,
                    structure: hook.structure,
                    effectiveness_score: hook.effectiveness_score,
                    examples: hook.examples?.slice(0, 3) || []
                })),
                viral_triggers: (rawResult.pattern_analysis?.viral_triggers || []).slice(0, 5).map(trigger => ({
                    name: trigger.name,
                    description: trigger.description,
                    effectiveness_score: trigger.effectiveness_score
                })),
                engagement_tactics: (rawResult.pattern_analysis?.engagement_patterns || []).slice(0, 5).map(tactic => ({
                    name: tactic.name,
                    description: tactic.description
                }))
            },
            
            // Strategy Recommendations
            strategy: {
                recommended_approach: rawResult.recommended_strategy?.approach || 'creator_inspired_content',
                primary_platform: rawResult.recommended_strategy?.primary_platform || 'youtube',
                content_strategy: rawResult.recommended_strategy?.content_strategy || {},
                monetization_strategy: rawResult.recommended_strategy?.monetization_strategy || {}
            },
            
            // Implementation Plan
            implementation: {
                phases: rawResult.implementation_plan || [],
                estimated_timeline: rawResult.timeline_estimate || '2-4 weeks',
                investment_required: rawResult.investment_required || 'medium',
                next_actions: rawResult.next_actions || []
            },
            
            // Success Metrics
            success_probability: rawResult.success_probability || 0.5,
            key_insights: rawResult.key_insights || [],
            competitive_advantages: rawResult.competitive_advantages || [],
            potential_risks: rawResult.potential_risks || [],
            
            // Metadata
            analysis_timestamp: new Date().toISOString(),
            processing_version: '1.0.0',
            data_sources: ['youtube', 'social_media', 'pattern_analysis']
        };
        
        return processedResult;
    }
    
    processNextInQueue() {
        if (this.analysisQueue.length > 0 && this.activeAnalyses.size < this.config.maxConcurrentAnalyses) {
            const { analysisId, opportunityData } = this.analysisQueue.shift();
            this.startAnalysis(analysisId, opportunityData);
        }
    }
    
    updateStats(success, processingTime, result = null) {
        this.stats.totalOpportunities++;
        
        if (success) {
            this.stats.successfulAnalyses++;
            
            if (result) {
                // Update niche tracking
                if (result.niche?.primary_niche) {
                    this.stats.nichesCovered.add(result.niche.primary_niche);
                }
                
                // Update creator count
                if (result.creators?.total_found) {
                    this.stats.creatorsDiscovered += result.creators.total_found;
                }
            }
        } else {
            this.stats.failedAnalyses++;
        }
        
        // Update average processing time
        const totalSuccessful = this.stats.successfulAnalyses;
        if (totalSuccessful > 0) {
            this.stats.averageProcessingTime = 
                ((this.stats.averageProcessingTime * (totalSuccessful - 1)) + processingTime) / totalSuccessful;
        }
    }
    
    /**
     * Get current statistics
     */
    getStats() {
        return {
            ...this.stats,
            nichesCovered: Array.from(this.stats.nichesCovered),
            activeAnalyses: this.activeAnalyses.size,
            queuedAnalyses: this.analysisQueue.length,
            successRate: this.stats.totalOpportunities > 0 ? 
                (this.stats.successfulAnalyses / this.stats.totalOpportunities) * 100 : 0
        };
    }
    
    /**
     * Get status of specific analysis
     */
    getAnalysisStatus(analysisId) {
        if (this.activeAnalyses.has(analysisId)) {
            const analysis = this.activeAnalyses.get(analysisId);
            return {
                analysisId,
                status: analysis.status,
                startTime: analysis.startTime,
                runningTime: Date.now() - analysis.startTime,
                opportunityTitle: analysis.opportunityData.title || analysis.opportunityData.product_name
            };
        }
        
        const queuedAnalysis = this.analysisQueue.find(item => item.analysisId === analysisId);
        if (queuedAnalysis) {
            return {
                analysisId,
                status: 'queued',
                queuePosition: this.analysisQueue.indexOf(queuedAnalysis) + 1
            };
        }
        
        return null;
    }
    
    /**
     * Cancel analysis
     */
    cancelAnalysis(analysisId) {
        // Remove from active analyses
        if (this.activeAnalyses.has(analysisId)) {
            this.activeAnalyses.delete(analysisId);
            console.log(`🚫 Cancelled active analysis ${analysisId}`);
            return true;
        }
        
        // Remove from queue
        const queueIndex = this.analysisQueue.findIndex(item => item.analysisId === analysisId);
        if (queueIndex > -1) {
            this.analysisQueue.splice(queueIndex, 1);
            console.log(`🚫 Cancelled queued analysis ${analysisId}`);
            return true;
        }
        
        return false;
    }
    
    /**
     * Integration point for intelligence system scanners
     */
    async integrateWithScanner(scannerName, opportunityHandler) {
        console.log(`🔗 Integrating Creator Intelligence with ${scannerName} scanner`);
        
        // Wrap the original opportunity handler
        const wrappedHandler = async (opportunity) => {
            try {
                // First, run the original handler
                const originalResult = await opportunityHandler(opportunity);
                
                // Then, trigger creator analysis
                const analysisId = await this.analyzeOpportunity(opportunity);
                
                // Return enhanced result
                return {
                    ...originalResult,
                    creator_analysis_id: analysisId,
                    creator_analysis_status: 'initiated'
                };
                
            } catch (error) {
                console.error(`❌ Failed to integrate creator analysis with ${scannerName}:`, error.message);
                
                // Return original result without creator analysis
                return await opportunityHandler(opportunity);
            }
        };
        
        return wrappedHandler;
    }
}

module.exports = CreatorIntelligenceBridge;