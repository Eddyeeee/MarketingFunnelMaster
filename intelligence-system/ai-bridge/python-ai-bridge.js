/**
 * Python AI Bridge - Connects Node.js system with Python AI research engine
 * Provides seamless integration between Node.js orchestration and Python ML/AI
 */

const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class PythonAIBridge {
    constructor(config = {}) {
        this.config = {
            pythonApiUrl: config.pythonApiUrl || 'http://localhost:8000',
            pythonPath: config.pythonPath || 'python3',
            aiResearchPath: config.aiResearchPath || path.join(__dirname, '..', 'ai-research'),
            timeout: config.timeout || 60000,
            retries: config.retries || 3,
            ...config
        };
        
        this.isRunning = false;
        this.pythonProcess = null;
        this.logger = console; // Use provided logger or console
    }

    /**
     * Initialize and start the Python AI system
     */
    async initialize() {
        this.logger.info('🐍 Initializing Python AI Research System...');
        
        try {
            // Check if Python AI API is already running
            const isRunning = await this.checkPythonAPIHealth();
            
            if (!isRunning) {
                // Start Python AI API
                await this.startPythonAPI();
            }
            
            // Verify connection
            await this.verifyConnection();
            
            this.isRunning = true;
            this.logger.info('✅ Python AI Research System initialized successfully');
            
            return true;
            
        } catch (error) {
            this.logger.error('❌ Failed to initialize Python AI system:', error.message);
            throw error;
        }
    }

    /**
     * Check if Python AI API is healthy
     */
    async checkPythonAPIHealth() {
        try {
            const response = await axios.get(`${this.config.pythonApiUrl}/`, {
                timeout: 5000
            });
            return response.data.status === 'healthy';
        } catch (error) {
            return false;
        }
    }

    /**
     * Start Python AI API as a subprocess
     */
    async startPythonAPI() {
        return new Promise((resolve, reject) => {
            this.logger.info('🚀 Starting Python AI API server...');
            
            const apiPath = path.join(this.config.aiResearchPath, 'api', 'research_api.py');
            
            // Check if API file exists
            if (!fs.existsSync(apiPath)) {
                reject(new Error(`Python API file not found: ${apiPath}`));
                return;
            }
            
            // Start Python process
            this.pythonProcess = spawn(this.config.pythonPath, [apiPath], {
                cwd: this.config.aiResearchPath,
                env: { ...process.env, PYTHONPATH: this.config.aiResearchPath }
            });
            
            let startupOutput = '';
            
            this.pythonProcess.stdout.on('data', (data) => {
                const output = data.toString();
                startupOutput += output;
                
                // Check for successful startup
                if (output.includes('AI Research Engine API started')) {
                    this.logger.info('✅ Python AI API started successfully');
                    setTimeout(resolve, 2000); // Give it time to fully initialize
                }
            });
            
            this.pythonProcess.stderr.on('data', (data) => {
                this.logger.error('Python AI stderr:', data.toString());
            });
            
            this.pythonProcess.on('close', (code) => {
                this.logger.info(`Python AI process exited with code ${code}`);
                this.isRunning = false;
                this.pythonProcess = null;
            });
            
            this.pythonProcess.on('error', (error) => {
                this.logger.error('Python AI process error:', error);
                reject(error);
            });
            
            // Timeout for startup
            setTimeout(() => {
                if (!this.isRunning) {
                    reject(new Error('Python AI API startup timeout'));
                }
            }, 30000);
        });
    }

    /**
     * Verify connection to Python AI system
     */
    async verifyConnection() {
        const maxRetries = 10;
        
        for (let i = 0; i < maxRetries; i++) {
            try {
                const response = await axios.get(`${this.config.pythonApiUrl}/research/status`, {
                    timeout: 5000
                });
                
                if (response.data.system_status === 'operational') {
                    return true;
                }
            } catch (error) {
                if (i === maxRetries - 1) {
                    throw new Error('Failed to connect to Python AI API after retries');
                }
                
                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }
    }

    /**
     * Conduct comprehensive AI research on a topic
     */
    async conductResearch(topic, options = {}) {
        this.logger.info(`🔍 Starting AI research on: ${topic}`);
        
        try {
            const requestData = {
                topic,
                depth: options.depth || 'deep',
                persona_focus: options.persona_focus,
                competitor_analysis: options.competitor_analysis !== false,
                market_sentiment: options.market_sentiment !== false,
                trend_prediction: options.trend_prediction !== false,
                content_clustering: options.content_clustering !== false,
                ml_enhancement: options.ml_enhancement !== false
            };
            
            const response = await this.makeAPICall('POST', '/research/analyze', requestData);
            
            this.logger.info(`✅ Research completed with confidence: ${response.confidence_score}`);
            return response;
            
        } catch (error) {
            this.logger.error('❌ AI research failed:', error.message);
            throw error;
        }
    }

    /**
     * Analyze crypto education market specifically
     */
    async analyzeCryptoEducation(options = {}) {
        this.logger.info('🪙 Starting crypto education market analysis...');
        
        try {
            const requestData = {
                focus_area: options.focus_area || 'trading_education',
                depth: options.depth || 'comprehensive',
                include_simulations: options.include_simulations !== false
            };
            
            const response = await this.makeAPICall('POST', '/research/crypto-education', requestData);
            
            this.logger.info('✅ Crypto education analysis completed');
            return response;
            
        } catch (error) {
            this.logger.error('❌ Crypto education analysis failed:', error.message);
            throw error;
        }
    }

    /**
     * Get quick AI insights for specific queries
     */
    async getQuickInsight(query, context = null) {
        this.logger.info(`💡 Getting quick insight for: ${query}`);
        
        try {
            const requestData = { query, context };
            const response = await this.makeAPICall('POST', '/research/quick-insight', requestData);
            
            return response;
            
        } catch (error) {
            this.logger.error('❌ Quick insight failed:', error.message);
            throw error;
        }
    }

    /**
     * Analyze competitors using AI
     */
    async analyzeCompetitors(topic, numCompetitors = 10) {
        this.logger.info(`🎯 Analyzing competitors for: ${topic}`);
        
        try {
            const response = await this.makeAPICall('POST', '/research/competitors', null, {
                topic,
                num_competitors: numCompetitors
            });
            
            return response;
            
        } catch (error) {
            this.logger.error('❌ Competitor analysis failed:', error.message);
            throw error;
        }
    }

    /**
     * Generate AI-powered content strategy
     */
    async generateContentStrategy(topic, targetAudience = null) {
        this.logger.info(`📝 Generating content strategy for: ${topic}`);
        
        try {
            const response = await this.makeAPICall('POST', '/research/content-strategy', null, {
                topic,
                target_audience: targetAudience
            });
            
            return response;
            
        } catch (error) {
            this.logger.error('❌ Content strategy generation failed:', error.message);
            throw error;
        }
    }

    /**
     * Analyze trends using AI
     */
    async analyzeTrends(topic, timeframe = '6months') {
        this.logger.info(`📈 Analyzing trends for: ${topic}`);
        
        try {
            const response = await this.makeAPICall('POST', '/research/trends', null, {
                topic,
                timeframe
            });
            
            return response;
            
        } catch (error) {
            this.logger.error('❌ Trend analysis failed:', error.message);
            throw error;
        }
    }

    /**
     * Get knowledge graph data
     */
    async getKnowledgeGraph(topic) {
        this.logger.info(`🕸️ Extracting knowledge graph for: ${topic}`);
        
        try {
            const response = await this.makeAPICall('GET', `/research/knowledge-graph/${encodeURIComponent(topic)}`);
            
            return response;
            
        } catch (error) {
            this.logger.error('❌ Knowledge graph extraction failed:', error.message);
            throw error;
        }
    }

    /**
     * Update learning algorithms with feedback
     */
    async updateLearning(feedbackData) {
        this.logger.info('📚 Updating learning algorithms...');
        
        try {
            const response = await this.makeAPICall('POST', '/research/learn', feedbackData);
            
            return response;
            
        } catch (error) {
            this.logger.error('❌ Learning update failed:', error.message);
            throw error;
        }
    }

    /**
     * Get system status
     */
    async getSystemStatus() {
        try {
            const response = await this.makeAPICall('GET', '/research/status');
            return response;
            
        } catch (error) {
            this.logger.error('❌ Status check failed:', error.message);
            return { system_status: 'offline', error: error.message };
        }
    }

    /**
     * Make API call to Python system with retries
     */
    async makeAPICall(method, endpoint, data = null, params = null) {
        let lastError;
        
        for (let attempt = 1; attempt <= this.config.retries; attempt++) {
            try {
                const config = {
                    method,
                    url: `${this.config.pythonApiUrl}${endpoint}`,
                    timeout: this.config.timeout,
                    headers: { 'Content-Type': 'application/json' }
                };
                
                if (data) config.data = data;
                if (params) config.params = params;
                
                const response = await axios(config);
                return response.data;
                
            } catch (error) {
                lastError = error;
                
                if (attempt < this.config.retries) {
                    this.logger.warn(`API call failed (attempt ${attempt}), retrying...`);
                    await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
                } else {
                    throw new Error(`API call failed after ${this.config.retries} attempts: ${error.message}`);
                }
            }
        }
        
        throw lastError;
    }

    /**
     * Shutdown Python AI system
     */
    async shutdown() {
        this.logger.info('🛑 Shutting down Python AI system...');
        
        if (this.pythonProcess) {
            this.pythonProcess.kill('SIGTERM');
            
            // Wait for graceful shutdown
            await new Promise(resolve => {
                this.pythonProcess.on('close', resolve);
                setTimeout(() => {
                    if (this.pythonProcess) {
                        this.pythonProcess.kill('SIGKILL');
                    }
                    resolve();
                }, 5000);
            });
        }
        
        this.isRunning = false;
        this.pythonProcess = null;
        
        this.logger.info('✅ Python AI system shutdown complete');
    }

    /**
     * Enhanced opportunity analysis combining multiple AI methods
     */
    async enhanceOpportunityWithAI(opportunity) {
        this.logger.info(`🧠 Enhancing opportunity with AI: ${opportunity.title}`);
        
        try {
            const tasks = [];
            
            // Task 1: Comprehensive research
            tasks.push(this.conductResearch(opportunity.title, {
                depth: 'deep',
                competitor_analysis: true,
                market_sentiment: true
            }));
            
            // Task 2: Quick competitor analysis
            tasks.push(this.analyzeCompetitors(opportunity.title, 5));
            
            // Task 3: Content strategy
            tasks.push(this.generateContentStrategy(opportunity.title));
            
            // Task 4: Trend analysis
            tasks.push(this.analyzeTrends(opportunity.title));
            
            // Execute all tasks in parallel
            const [research, competitors, contentStrategy, trends] = await Promise.allSettled(tasks);
            
            // Combine results
            const enhancedOpportunity = {
                ...opportunity,
                ai_analysis: {
                    research: research.status === 'fulfilled' ? research.value : null,
                    competitors: competitors.status === 'fulfilled' ? competitors.value : null,
                    content_strategy: contentStrategy.status === 'fulfilled' ? contentStrategy.value : null,
                    trends: trends.status === 'fulfilled' ? trends.value : null
                },
                ai_confidence_score: this.calculateOverallConfidence([research, competitors, contentStrategy, trends]),
                enhancement_timestamp: new Date().toISOString()
            };
            
            this.logger.info(`✅ Opportunity enhanced with AI analysis`);
            return enhancedOpportunity;
            
        } catch (error) {
            this.logger.error('❌ AI enhancement failed:', error.message);
            return { ...opportunity, ai_enhancement_error: error.message };
        }
    }

    /**
     * Calculate overall confidence from multiple AI analyses
     */
    calculateOverallConfidence(results) {
        const successfulResults = results.filter(r => r.status === 'fulfilled');
        if (successfulResults.length === 0) return 0;
        
        const confidenceScores = successfulResults
            .map(r => r.value?.confidence_score || r.value?.confidence || 0.5)
            .filter(score => score > 0);
        
        if (confidenceScores.length === 0) return 0.5;
        
        return confidenceScores.reduce((sum, score) => sum + score, 0) / confidenceScores.length;
    }
}

module.exports = PythonAIBridge;