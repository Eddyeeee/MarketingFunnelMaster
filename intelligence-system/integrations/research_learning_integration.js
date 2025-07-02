/**
 * Research Learning Integration
 * 
 * Integrates manual research data feeding with autonomous learning
 * and specialized "Online Geld Verdienen" analysis
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
const EventEmitter = require('events');

class ResearchLearningIntegration extends EventEmitter {
    constructor() {
        super();
        
        this.pythonPath = process.env.PYTHON_PATH || 'python3';
        this.scriptsPath = path.join(__dirname, '..', 'ai-research');
        
        // Initialize components
        this.dataIngestion = null;
        this.ogvAnalyzer = null;
        
        // Learning statistics
        this.learningStats = {
            totalResearchSessions: 0,
            influencersLearned: 0,
            patternsExtracted: 0,
            strategiesIdentified: 0,
            ogvAnalysesConducted: 0,
            lastUpdate: new Date()
        };
        
        this.initialize();
    }
    
    async initialize() {
        console.log('🧠 Initializing Research Learning Integration...');
        
        try {
            // Verify Python environment
            await this.verifyPythonEnvironment();
            
            // Initialize components
            await this.initializeComponents();
            
            console.log('✅ Research Learning Integration ready');
            this.emit('ready');
            
        } catch (error) {
            console.error('❌ Failed to initialize Research Learning Integration:', error.message);
            this.emit('error', error);
        }
    }
    
    async verifyPythonEnvironment() {
        return new Promise((resolve, reject) => {
            const pythonCheck = spawn(this.pythonPath, ['-c', 'import asyncio, json, sqlite3; print("OK")']);
            
            let output = '';
            pythonCheck.stdout.on('data', (data) => {
                output += data.toString();
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
    
    async initializeComponents() {
        // Components will be initialized when first used
        console.log('📚 Components ready for lazy initialization');
    }
    
    /**
     * Submit research data from Gemini/ChatGPT research
     */
    async submitResearchData(researchData) {
        console.log(`📊 Submitting research data: ${researchData.sessionName || 'Unnamed Session'}`);
        
        try {
            const result = await this.executeDataIngestion('submit_research_session', researchData);
            
            // Update statistics
            this.learningStats.totalResearchSessions++;
            this.learningStats.influencersLearned += result.influencersProcessed || 0;
            this.learningStats.patternsExtracted += result.patternsDiscovered || 0;
            this.learningStats.lastUpdate = new Date();
            
            console.log(`✅ Research data submitted successfully: ${result.sessionId}`);
            
            // Emit event for further processing
            this.emit('researchSubmitted', {
                sessionId: result.sessionId,
                data: researchData,
                result: result
            });
            
            return result;
            
        } catch (error) {
            console.error('❌ Failed to submit research data:', error.message);
            throw error;
        }
    }
    
    /**
     * Submit research data specifically from Gemini
     */
    async submitGeminiResearch(geminiData) {
        console.log('🤖 Submitting Gemini research data...');
        
        const formattedData = {
            sessionName: geminiData.sessionName || `Gemini Research ${new Date().toISOString().split('T')[0]}`,
            researchSource: 'manual_gemini',
            researcherName: 'Gemini AI Assistant',
            data: geminiData
        };
        
        return await this.submitResearchData(formattedData);
    }
    
    /**
     * Submit research data specifically from ChatGPT
     */
    async submitChatGPTResearch(chatgptData) {
        console.log('🤖 Submitting ChatGPT research data...');
        
        const formattedData = {
            sessionName: chatgptData.sessionName || `ChatGPT Research ${new Date().toISOString().split('T')[0]}`,
            researchSource: 'manual_chatgpt',
            researcherName: 'ChatGPT Assistant',
            data: chatgptData
        };
        
        return await this.submitResearchData(formattedData);
    }
    
    /**
     * Run specialized Online Geld Verdienen analysis
     */
    async runOGVAnalysis(analysisType = 'comprehensive') {
        console.log(`💰 Running Online Geld Verdienen analysis: ${analysisType}`);
        
        try {
            const result = await this.executeOGVAnalysis(analysisType);
            
            // Update statistics
            this.learningStats.ogvAnalysesConducted++;
            this.learningStats.lastUpdate = new Date();
            
            console.log(`✅ OGV analysis completed: ${result.sessionId}`);
            
            // Emit event
            this.emit('ogvAnalysisComplete', {
                analysisType: analysisType,
                result: result
            });
            
            return result;
            
        } catch (error) {
            console.error('❌ OGV analysis failed:', error.message);
            throw error;
        }
    }
    
    /**
     * Get learned patterns for autonomous research
     */
    async getLearnedPatterns(patternType = null) {
        console.log(`🧠 Retrieving learned patterns${patternType ? ` of type: ${patternType}` : ''}`);
        
        try {
            const patterns = await this.executeDataIngestion('export_learned_patterns', { patternType });
            
            console.log(`📊 Retrieved ${Object.keys(patterns).length} pattern categories`);
            
            return patterns;
            
        } catch (error) {
            console.error('❌ Failed to retrieve learned patterns:', error.message);
            throw error;
        }
    }
    
    /**
     * Train autonomous research from manual data
     */
    async trainAutonomousResearch() {
        console.log('🤖 Training autonomous research from manual data...');
        
        try {
            // Get all learned patterns
            const patterns = await this.getLearnedPatterns();
            
            // Extract training data
            const trainingData = this.extractTrainingData(patterns);
            
            // Apply learning to universal analyzers
            await this.applyLearningToAnalyzers(trainingData);
            
            console.log('✅ Autonomous research training completed');
            
            this.emit('autonomousTrainingComplete', {
                patternsUsed: Object.keys(patterns).length,
                trainingData: trainingData
            });
            
            return {
                success: true,
                patternsUsed: Object.keys(patterns).length,
                trainingData: trainingData
            };
            
        } catch (error) {
            console.error('❌ Autonomous research training failed:', error.message);
            throw error;
        }
    }
    
    /**
     * Create data templates for easy input
     */
    createDataTemplates() {
        return {
            germanInfluencerTemplate: {
                name: '',                    // Required: Full name
                handle: '',                  // Social media handle
                platforms: [],               // ['Instagram', 'YouTube', 'TikTok']
                primaryPlatform: '',         // Main platform
                followers: {},               // {instagram: 0, youtube: 0}
                niche: 'online_marketing',   // Main niche
                subNiches: [],               // Additional niches
                contentThemes: [],           // Main content themes
                funnelType: '',              // course, coaching, product
                pricingStrategy: {},         // price points
                currentHooks: [],            // hook examples
                trendingStrategies: [],      // current strategies
                engagementRate: 0.0,         // average engagement %
                estimatedRevenue: '',        // revenue estimate
                confidenceScore: 0.8         // data confidence
            },
            
            hookTemplate: {
                hookText: '',                // The actual hook
                hookCategory: '',            // curiosity, fear, desire
                germanSpecific: true,        // German market hook
                effectivenessScore: 0.0,     // 0-1 effectiveness
                usageExamples: [],           // where seen used
                sourceInfluencer: '',        // who uses it
                platformOptimized: '',       // best platform
                trendPeriod: '2024'          // when trending
            },
            
            strategyTemplate: {
                strategyName: '',            // Strategy name
                category: '',                // affiliate, dropshipping, etc.
                description: '',             // What it is
                germanSuitability: 0.0,      // 0-1 German market fit
                startupCost: 0.0,            // Initial investment
                timeToFirstEuro: '',         // Time to first earnings
                difficultyLevel: '',         // Anfänger, Mittel, Fortgeschritten
                successRate: 0.0,            // 0-1 success rate
                marketSaturation: 0.0,       // 0-1 market saturation
                trendStatus: 'emerging'      // emerging, established, declining
            }
        };
    }
    
    /**
     * Validate research data before submission
     */
    validateResearchData(data) {
        const errors = [];
        
        // Check required fields
        if (!data.sessionName) {
            errors.push('sessionName is required');
        }
        
        if (!data.data) {
            errors.push('data object is required');
        }
        
        // Validate influencers
        if (data.data.influencers) {
            data.data.influencers.forEach((influencer, index) => {
                if (!influencer.name) {
                    errors.push(`Influencer ${index + 1}: name is required`);
                }
                if (!influencer.primaryPlatform) {
                    errors.push(`Influencer ${index + 1}: primaryPlatform is required`);
                }
            });
        }
        
        // Validate hooks
        if (data.data.hooks) {
            data.data.hooks.forEach((hook, index) => {
                if (!hook.hookText) {
                    errors.push(`Hook ${index + 1}: hookText is required`);
                }
                if (!hook.hookCategory) {
                    errors.push(`Hook ${index + 1}: hookCategory is required`);
                }
            });
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }
    
    /**
     * Execute Python data ingestion script
     */
    async executeDataIngestion(action, data) {
        return new Promise((resolve, reject) => {
            const scriptPath = path.join(this.scriptsPath, 'training', 'research_data_ingestion.py');
            const args = [scriptPath, '--action', action, '--data', JSON.stringify(data)];
            
            const pythonProcess = spawn(this.pythonPath, args);
            
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
                        const result = JSON.parse(stdout.trim());
                        resolve(result);
                    } catch (parseError) {
                        resolve({ success: true, message: stdout.trim() });
                    }
                } else {
                    reject(new Error(`Data ingestion failed: ${stderr}`));
                }
            });
            
            pythonProcess.on('error', (error) => {
                reject(new Error(`Failed to start data ingestion: ${error.message}`));
            });
        });
    }
    
    /**
     * Execute Python OGV analysis script
     */
    async executeOGVAnalysis(analysisType) {
        return new Promise((resolve, reject) => {
            const scriptPath = path.join(this.scriptsPath, 'specialized', 'online_geld_verdienen_analyzer.py');
            const args = [scriptPath, '--analysis-type', analysisType];
            
            const pythonProcess = spawn(this.pythonPath, args);
            
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
                        const result = JSON.parse(stdout.trim());
                        resolve(result);
                    } catch (parseError) {
                        resolve({ success: true, message: stdout.trim() });
                    }
                } else {
                    reject(new Error(`OGV analysis failed: ${stderr}`));
                }
            });
            
            pythonProcess.on('error', (error) => {
                reject(new Error(`Failed to start OGV analysis: ${error.message}`));
            });
        });
    }
    
    /**
     * Extract training data from learned patterns
     */
    extractTrainingData(patterns) {
        const trainingData = {
            germanHooks: [],
            funnelStructures: [],
            pricingPatterns: [],
            contentStrategies: [],
            platformOptimizations: []
        };
        
        // Extract German-specific hooks
        if (patterns.hook_formulas) {
            trainingData.germanHooks = Object.values(patterns.hook_formulas)
                .filter(hook => hook.data.german_specific)
                .map(hook => ({
                    structure: hook.data.structure,
                    effectiveness: hook.effectiveness_score,
                    trigger: hook.data.trigger,
                    examples: hook.data.examples
                }));
        }
        
        // Extract funnel structures
        if (patterns.funnel_structures) {
            trainingData.funnelStructures = Object.values(patterns.funnel_structures)
                .map(funnel => ({
                    type: funnel.data.funnel_type,
                    stages: funnel.data.common_stages,
                    pricing: funnel.data.pricing_patterns,
                    effectiveness: funnel.effectiveness_score
                }));
        }
        
        // Extract pricing patterns
        if (patterns.pricing_psychology) {
            trainingData.pricingPatterns = Object.values(patterns.pricing_psychology)
                .map(pricing => ({
                    pricePoints: pricing.data.preferred_price_points,
                    paymentMethods: pricing.data.payment_preferences,
                    trustSignals: pricing.data.trust_signals,
                    effectiveness: pricing.effectiveness_score
                }));
        }
        
        return trainingData;
    }
    
    /**
     * Apply learning to universal analyzers
     */
    async applyLearningToAnalyzers(trainingData) {
        // This would enhance the universal analyzers with learned patterns
        console.log('🔄 Applying learned patterns to universal analyzers...');
        
        // Save training data for analyzers to use
        const trainingDataPath = path.join(this.scriptsPath, 'training', 'learned_patterns.json');
        await fs.writeFile(trainingDataPath, JSON.stringify(trainingData, null, 2));
        
        console.log(`📁 Training data saved to: ${trainingDataPath}`);
        
        // The analyzers can now load and use this data for improved accuracy
        return true;
    }
    
    /**
     * Get current learning statistics
     */
    getLearningStats() {
        return {
            ...this.learningStats,
            systemStatus: 'operational',
            lastUpdate: this.learningStats.lastUpdate.toISOString(),
            uptime: Date.now() - this.learningStats.lastUpdate.getTime()
        };
    }
    
    /**
     * Save research data to file for later submission
     */
    async saveResearchToFile(data, filename) {
        const exportPath = path.join(__dirname, '..', 'exports');
        await fs.mkdir(exportPath, { recursive: true });
        
        const filepath = path.join(exportPath, `${filename}.json`);
        await fs.writeFile(filepath, JSON.stringify(data, null, 2, 'utf8'));
        
        console.log(`💾 Research data saved to: ${filepath}`);
        return filepath;
    }
    
    /**
     * Load research data from file
     */
    async loadResearchFromFile(filename) {
        const exportPath = path.join(__dirname, '..', 'exports');
        const filepath = path.join(exportPath, `${filename}.json`);
        
        const data = JSON.parse(await fs.readFile(filepath, 'utf8'));
        
        console.log(`📂 Research data loaded from: ${filepath}`);
        return data;
    }
    
    /**
     * Generate research session template
     */
    generateResearchSessionTemplate(sessionName = 'German Marketing Research') {
        return {
            sessionName: sessionName,
            researchDate: new Date().toISOString(),
            researchSource: 'manual_human',
            researcherName: 'Manual Research',
            focusAreas: [
                'Top 20 German online marketing influencers',
                'Funnel structures and pricing strategies',
                'Current hooks and strategies 2024/2025',
                'Platform-specific adaptations',
                'German market compliance and cultural fit'
            ],
            data: {
                influencers: [],  // Fill with influencer data
                hooks: [],        // Fill with hook data
                funnels: [],      // Fill with funnel data
                strategies: []    // Fill with strategy data
            },
            metadata: {
                totalInfluencers: 0,
                targetCount: 20,
                completionStatus: 'in_progress',
                dataQuality: 'high',
                verificationStatus: 'manual_verified'
            }
        };
    }
}

module.exports = ResearchLearningIntegration;