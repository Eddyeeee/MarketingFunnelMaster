const fs = require('fs');
const path = require('path');

class ApiConfig {
    constructor(configPath = null) {
        this.configPath = configPath || path.join(__dirname, 'api-credentials.json');
        this.config = {};
        this.networkConfigs = new Map();
        
        this.loadConfig();
        this.initializeNetworkConfigs();
    }

    loadConfig() {
        try {
            // Try to load from file first
            if (fs.existsSync(this.configPath)) {
                const configData = fs.readFileSync(this.configPath, 'utf8');
                this.config = JSON.parse(configData);
            } else {
                // Fallback to environment variables
                this.loadFromEnvironment();
            }
        } catch (error) {
            console.warn('Could not load API config from file, using environment variables');
            this.loadFromEnvironment();
        }
    }

    loadFromEnvironment() {
        this.config = {
            // Affiliate Networks
            digistore24: {
                apiKey: process.env.DIGISTORE24_API_KEY || '',
                baseUrl: process.env.DIGISTORE24_BASE_URL || 'https://www.digistore24.com',
                timeout: parseInt(process.env.DIGISTORE24_TIMEOUT) || 30000,
                rateLimit: parseInt(process.env.DIGISTORE24_RATE_LIMIT) || 60
            },
            
            clickbank: {
                apiKey: process.env.CLICKBANK_API_KEY || '',
                baseUrl: process.env.CLICKBANK_BASE_URL || 'https://api.clickbank.com',
                timeout: parseInt(process.env.CLICKBANK_TIMEOUT) || 25000,
                rateLimit: parseInt(process.env.CLICKBANK_RATE_LIMIT) || 100
            },
            
            shareasale: {
                apiKey: process.env.SHAREASALE_API_KEY || '',
                affiliateId: process.env.SHAREASALE_AFFILIATE_ID || '',
                baseUrl: process.env.SHAREASALE_BASE_URL || 'https://www.shareasale.com',
                timeout: parseInt(process.env.SHAREASALE_TIMEOUT) || 30000,
                rateLimit: parseInt(process.env.SHAREASALE_RATE_LIMIT) || 60
            },
            
            cj_affiliate: {
                apiKey: process.env.CJ_AFFILIATE_API_KEY || '',
                baseUrl: process.env.CJ_AFFILIATE_BASE_URL || 'https://api.cj.com',
                timeout: parseInt(process.env.CJ_AFFILIATE_TIMEOUT) || 30000,
                rateLimit: parseInt(process.env.CJ_AFFILIATE_RATE_LIMIT) || 100
            },
            
            impact: {
                accountSid: process.env.IMPACT_ACCOUNT_SID || '',
                authToken: process.env.IMPACT_AUTH_TOKEN || '',
                baseUrl: process.env.IMPACT_BASE_URL || 'https://api.impact.com',
                timeout: parseInt(process.env.IMPACT_TIMEOUT) || 30000,
                rateLimit: parseInt(process.env.IMPACT_RATE_LIMIT) || 100
            },

            // Social Media Platforms
            twitter: {
                bearerToken: process.env.TWITTER_BEARER_TOKEN || '',
                apiKey: process.env.TWITTER_API_KEY || '',
                apiSecret: process.env.TWITTER_API_SECRET || '',
                accessToken: process.env.TWITTER_ACCESS_TOKEN || '',
                accessTokenSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET || '',
                baseUrl: process.env.TWITTER_BASE_URL || 'https://api.twitter.com',
                timeout: parseInt(process.env.TWITTER_TIMEOUT) || 15000,
                rateLimit: parseInt(process.env.TWITTER_RATE_LIMIT) || 300
            },
            
            instagram: {
                accessToken: process.env.INSTAGRAM_ACCESS_TOKEN || '',
                userId: process.env.INSTAGRAM_USER_ID || '',
                baseUrl: process.env.INSTAGRAM_BASE_URL || 'https://graph.instagram.com',
                timeout: parseInt(process.env.INSTAGRAM_TIMEOUT) || 20000,
                rateLimit: parseInt(process.env.INSTAGRAM_RATE_LIMIT) || 200
            },
            
            tiktok: {
                accessToken: process.env.TIKTOK_ACCESS_TOKEN || '',
                baseUrl: process.env.TIKTOK_BASE_URL || 'https://open-api.tiktok.com',
                timeout: parseInt(process.env.TIKTOK_TIMEOUT) || 20000,
                rateLimit: parseInt(process.env.TIKTOK_RATE_LIMIT) || 100
            },
            
            youtube: {
                apiKey: process.env.YOUTUBE_API_KEY || '',
                baseUrl: process.env.YOUTUBE_BASE_URL || 'https://www.googleapis.com/youtube/v3',
                timeout: parseInt(process.env.YOUTUBE_TIMEOUT) || 20000,
                rateLimit: parseInt(process.env.YOUTUBE_RATE_LIMIT) || 10000
            },
            
            reddit: {
                clientId: process.env.REDDIT_CLIENT_ID || '',
                clientSecret: process.env.REDDIT_CLIENT_SECRET || '',
                userAgent: process.env.REDDIT_USER_AGENT || 'IntelligenceSystem/1.0',
                baseUrl: process.env.REDDIT_BASE_URL || 'https://www.reddit.com',
                timeout: parseInt(process.env.REDDIT_TIMEOUT) || 15000,
                rateLimit: parseInt(process.env.REDDIT_RATE_LIMIT) || 60
            },

            // Additional APIs
            google_trends: {
                apiKey: process.env.GOOGLE_TRENDS_API_KEY || '',
                baseUrl: process.env.GOOGLE_TRENDS_BASE_URL || 'https://trends.googleapis.com',
                timeout: parseInt(process.env.GOOGLE_TRENDS_TIMEOUT) || 15000,
                rateLimit: parseInt(process.env.GOOGLE_TRENDS_RATE_LIMIT) || 100
            },
            
            semrush: {
                apiKey: process.env.SEMRUSH_API_KEY || '',
                baseUrl: process.env.SEMRUSH_BASE_URL || 'https://api.semrush.com',
                timeout: parseInt(process.env.SEMRUSH_TIMEOUT) || 20000,
                rateLimit: parseInt(process.env.SEMRUSH_RATE_LIMIT) || 100
            },

            // Webhook and Automation
            n8n: {
                webhookUrl: process.env.N8N_WEBHOOK_URL || '',
                apiKey: process.env.N8N_API_KEY || '',
                baseUrl: process.env.N8N_BASE_URL || 'https://n8n.yourdomain.com',
                timeout: parseInt(process.env.N8N_TIMEOUT) || 30000
            },
            
            zapier: {
                webhookUrl: process.env.ZAPIER_WEBHOOK_URL || '',
                apiKey: process.env.ZAPIER_API_KEY || '',
                timeout: parseInt(process.env.ZAPIER_TIMEOUT) || 30000
            },

            // Database
            database: {
                path: process.env.DATABASE_PATH || path.join(__dirname, '../databases/intelligence.db'),
                backupPath: process.env.DATABASE_BACKUP_PATH || path.join(__dirname, '../databases/backups/'),
                maxConnections: parseInt(process.env.DATABASE_MAX_CONNECTIONS) || 5
            }
        };
    }

    initializeNetworkConfigs() {
        // Enhanced network configurations with validation and defaults
        Object.entries(this.config).forEach(([networkName, config]) => {
            if (config && typeof config === 'object' && !Array.isArray(config)) {
                this.networkConfigs.set(networkName, {
                    ...config,
                    name: networkName,
                    isValid: this.validateNetworkConfig(networkName, config),
                    lastValidated: new Date().toISOString()
                });
            }
        });
    }

    validateNetworkConfig(networkName, config) {
        const requiredFields = {
            // Affiliate networks
            digistore24: ['apiKey', 'baseUrl'],
            clickbank: ['apiKey', 'baseUrl'],
            shareasale: ['apiKey', 'affiliateId', 'baseUrl'],
            cj_affiliate: ['apiKey', 'baseUrl'],
            impact: ['accountSid', 'authToken', 'baseUrl'],
            
            // Social platforms
            twitter: ['bearerToken', 'baseUrl'],
            instagram: ['accessToken', 'userId', 'baseUrl'],
            tiktok: ['accessToken', 'baseUrl'],
            youtube: ['apiKey', 'baseUrl'],
            reddit: ['userAgent', 'baseUrl'],
            
            // Additional APIs
            google_trends: ['baseUrl'],
            semrush: ['apiKey', 'baseUrl'],
            
            // Automation
            n8n: ['baseUrl'],
            zapier: ['webhookUrl']
        };

        const required = requiredFields[networkName] || [];
        return required.every(field => config[field] && config[field].trim() !== '');
    }

    getNetworkConfig(networkName) {
        const config = this.networkConfigs.get(networkName);
        
        if (!config) {
            console.warn(`No configuration found for network: ${networkName}`);
            return null;
        }

        if (!config.isValid) {
            console.warn(`Invalid configuration for network: ${networkName}`);
            return null;
        }

        return config;
    }

    getAllNetworkConfigs() {
        return Object.fromEntries(this.networkConfigs);
    }

    getValidNetworks() {
        const validNetworks = [];
        this.networkConfigs.forEach((config, name) => {
            if (config.isValid) {
                validNetworks.push(name);
            }
        });
        return validNetworks;
    }

    getInvalidNetworks() {
        const invalidNetworks = [];
        this.networkConfigs.forEach((config, name) => {
            if (!config.isValid) {
                invalidNetworks.push({
                    name,
                    reason: this.getValidationError(name, config)
                });
            }
        });
        return invalidNetworks;
    }

    getValidationError(networkName, config) {
        const requiredFields = {
            digistore24: ['apiKey', 'baseUrl'],
            clickbank: ['apiKey', 'baseUrl'],
            shareasale: ['apiKey', 'affiliateId', 'baseUrl'],
            cj_affiliate: ['apiKey', 'baseUrl'],
            impact: ['accountSid', 'authToken', 'baseUrl'],
            twitter: ['bearerToken', 'baseUrl'],
            instagram: ['accessToken', 'userId', 'baseUrl'],
            tiktok: ['accessToken', 'baseUrl'],
            youtube: ['apiKey', 'baseUrl'],
            reddit: ['userAgent', 'baseUrl']
        };

        const required = requiredFields[networkName] || [];
        const missing = required.filter(field => !config[field] || config[field].trim() === '');
        
        if (missing.length > 0) {
            return `Missing required fields: ${missing.join(', ')}`;
        }
        
        return 'Unknown validation error';
    }

    updateConfig(networkName, updates) {
        if (!this.networkConfigs.has(networkName)) {
            throw new Error(`Network ${networkName} not found`);
        }

        const currentConfig = this.networkConfigs.get(networkName);
        const updatedConfig = { ...currentConfig, ...updates };
        updatedConfig.isValid = this.validateNetworkConfig(networkName, updatedConfig);
        updatedConfig.lastValidated = new Date().toISOString();

        this.networkConfigs.set(networkName, updatedConfig);

        // Update the main config object
        this.config[networkName] = { ...this.config[networkName], ...updates };

        return updatedConfig;
    }

    saveConfig() {
        try {
            const configToSave = { ...this.config };
            
            // Remove sensitive data or create a template
            Object.keys(configToSave).forEach(network => {
                if (configToSave[network] && typeof configToSave[network] === 'object') {
                    Object.keys(configToSave[network]).forEach(key => {
                        if (key.includes('key') || key.includes('token') || key.includes('secret')) {
                            configToSave[network][key] = `<${key.toUpperCase()}>`;
                        }
                    });
                }
            });

            const templatePath = path.join(__dirname, 'api-config-template.json');
            fs.writeFileSync(templatePath, JSON.stringify(configToSave, null, 2));
            
            console.log(`API config template saved to: ${templatePath}`);
            return true;
        } catch (error) {
            console.error('Error saving config:', error);
            return false;
        }
    }

    testConnection(networkName) {
        const config = this.getNetworkConfig(networkName);
        if (!config) {
            return { success: false, error: 'Invalid or missing configuration' };
        }

        // This would implement actual connection testing
        // For now, return success if config is valid
        return {
            success: config.isValid,
            network: networkName,
            baseUrl: config.baseUrl,
            timestamp: new Date().toISOString()
        };
    }

    getNetworkStats() {
        const stats = {
            total: this.networkConfigs.size,
            valid: 0,
            invalid: 0,
            affiliate_networks: 0,
            social_platforms: 0,
            other_apis: 0
        };

        const affiliateNetworks = ['digistore24', 'clickbank', 'shareasale', 'cj_affiliate', 'impact'];
        const socialPlatforms = ['twitter', 'instagram', 'tiktok', 'youtube', 'reddit'];

        this.networkConfigs.forEach((config, name) => {
            if (config.isValid) stats.valid++;
            else stats.invalid++;

            if (affiliateNetworks.includes(name)) stats.affiliate_networks++;
            else if (socialPlatforms.includes(name)) stats.social_platforms++;
            else stats.other_apis++;
        });

        return stats;
    }

    getRateLimitInfo(networkName) {
        const config = this.getNetworkConfig(networkName);
        if (!config) return null;

        return {
            network: networkName,
            rateLimit: config.rateLimit || 100,
            timeout: config.timeout || 30000,
            resetWindow: '1 hour', // Most APIs reset hourly
            recommendations: this.getRateLimitRecommendations(config.rateLimit)
        };
    }

    getRateLimitRecommendations(rateLimit) {
        if (rateLimit >= 1000) {
            return ['High rate limit - suitable for intensive scanning', 'Consider parallel processing'];
        } else if (rateLimit >= 100) {
            return ['Moderate rate limit - good for regular scanning', 'Implement request queuing'];
        } else {
            return ['Low rate limit - use sparingly', 'Implement aggressive caching', 'Consider request batching'];
        }
    }

    exportConfig(format = 'json') {
        const sanitizedConfig = this.sanitizeConfig(this.config);
        
        switch (format.toLowerCase()) {
            case 'json':
                return JSON.stringify(sanitizedConfig, null, 2);
            case 'env':
                return this.convertToEnvFormat(sanitizedConfig);
            case 'yaml':
                return this.convertToYamlFormat(sanitizedConfig);
            default:
                throw new Error(`Unsupported format: ${format}`);
        }
    }

    sanitizeConfig(config) {
        const sanitized = JSON.parse(JSON.stringify(config));
        
        Object.keys(sanitized).forEach(network => {
            if (sanitized[network] && typeof sanitized[network] === 'object') {
                Object.keys(sanitized[network]).forEach(key => {
                    if (key.includes('key') || key.includes('token') || key.includes('secret')) {
                        sanitized[network][key] = `***${sanitized[network][key].slice(-4)}`;
                    }
                });
            }
        });

        return sanitized;
    }

    convertToEnvFormat(config) {
        const envLines = [];
        
        Object.entries(config).forEach(([network, networkConfig]) => {
            if (networkConfig && typeof networkConfig === 'object') {
                Object.entries(networkConfig).forEach(([key, value]) => {
                    const envKey = `${network.toUpperCase()}_${key.toUpperCase()}`;
                    envLines.push(`${envKey}=${value}`);
                });
            }
        });

        return envLines.join('\n');
    }

    convertToYamlFormat(config) {
        // Simple YAML conversion - in production, use a proper YAML library
        let yaml = 'api_config:\n';
        
        Object.entries(config).forEach(([network, networkConfig]) => {
            yaml += `  ${network}:\n`;
            if (networkConfig && typeof networkConfig === 'object') {
                Object.entries(networkConfig).forEach(([key, value]) => {
                    yaml += `    ${key}: ${JSON.stringify(value)}\n`;
                });
            }
        });

        return yaml;
    }

    createConfigTemplate() {
        const template = {
            description: "API Configuration Template for Intelligence System",
            instructions: [
                "1. Copy this file to 'api-credentials.json'",
                "2. Replace placeholder values with your actual API credentials",
                "3. Remove this instructions section",
                "4. Ensure the file is added to .gitignore"
            ],
            required_env_vars: [
                "DIGISTORE24_API_KEY",
                "TWITTER_BEARER_TOKEN",
                "YOUTUBE_API_KEY",
                "N8N_WEBHOOK_URL"
            ],
            config: this.sanitizeConfig(this.config)
        };

        return template;
    }
}

module.exports = { ApiConfig };