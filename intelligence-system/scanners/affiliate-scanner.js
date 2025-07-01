const axios = require('axios');
const { ApiConfig } = require('../config/api-config');

class AffiliateScanner {
    constructor(config = {}) {
        this.config = {
            minCommissionRate: config.minCommissionRate || 0.1, // 10%
            maxRequestsPerMinute: config.maxRequestsPerMinute || 60,
            timeout: config.timeout || 30000,
            ...config
        };
        
        this.apiConfig = new ApiConfig();
        this.requestCount = 0;
        this.lastResetTime = Date.now();
        this.cache = new Map();
        this.cacheExpiry = 15 * 60 * 1000; // 15 minutes
    }

    async scan() {
        const opportunities = [];
        
        try {
            // Scan multiple affiliate networks
            const networks = [
                'digistore24',
                'clickbank',
                'shareasale',
                'cj_affiliate',
                'impact'
            ];

            const scanPromises = networks.map(network => 
                this.scanNetwork(network).catch(error => {
                    console.error(`Error scanning ${network}:`, error.message);
                    return [];
                })
            );

            const results = await Promise.all(scanPromises);
            results.forEach(networkOpportunities => {
                opportunities.push(...networkOpportunities);
            });

            // Remove duplicates and sort by commission rate
            const uniqueOpportunities = this.deduplicateOpportunities(opportunities);
            return uniqueOpportunities.sort((a, b) => b.commissionRate - a.commissionRate);

        } catch (error) {
            console.error('Affiliate scanning error:', error);
            throw error;
        }
    }

    async scanNetwork(networkName) {
        const cacheKey = `${networkName}_scan_${Math.floor(Date.now() / this.cacheExpiry)}`;
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        await this.rateLimitCheck();

        const config = this.apiConfig.getNetworkConfig(networkName);
        if (!config) {
            console.warn(`No configuration found for network: ${networkName}`);
            return [];
        }

        let opportunities = [];

        try {
            switch (networkName) {
                case 'digistore24':
                    opportunities = await this.scanDigistore24(config);
                    break;
                case 'clickbank':
                    opportunities = await this.scanClickBank(config);
                    break;
                case 'shareasale':
                    opportunities = await this.scanShareASale(config);
                    break;
                case 'cj_affiliate':
                    opportunities = await this.scanCJAffiliate(config);
                    break;
                case 'impact':
                    opportunities = await this.scanImpact(config);
                    break;
                default:
                    console.warn(`Unknown network: ${networkName}`);
            }

            this.cache.set(cacheKey, opportunities);
            return opportunities;

        } catch (error) {
            console.error(`Error scanning ${networkName}:`, error.message);
            return [];
        }
    }

    async scanDigistore24(config) {
        const opportunities = [];
        
        try {
            const response = await axios.get(`${config.baseUrl}/api/products`, {
                headers: {
                    'Authorization': `Bearer ${config.apiKey}`,
                    'Content-Type': 'application/json'
                },
                params: {
                    limit: 100,
                    sort: 'commission_desc',
                    category: 'business,marketing,finance'
                },
                timeout: this.config.timeout
            });

            if (response.data && response.data.products) {
                for (const product of response.data.products) {
                    if (product.commission_rate >= this.config.minCommissionRate) {
                        opportunities.push({
                            id: `ds24_${product.id}`,
                            title: product.title,
                            description: product.description,
                            commissionRate: product.commission_rate,
                            price: product.price,
                            currency: product.currency || 'EUR',
                            category: product.category,
                            vendor: product.vendor_name,
                            gravity: product.popularity_score || 0,
                            conversionRate: product.conversion_rate || 0,
                            source: 'digistore24',
                            type: 'affiliate_product',
                            url: product.affiliate_url,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                salesCount: product.sales_count || 0,
                                refundRate: product.refund_rate || 0,
                                averageOrderValue: product.avg_order_value || product.price
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('Digistore24 API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanClickBank(config) {
        const opportunities = [];
        
        try {
            const response = await axios.get(`${config.baseUrl}/marketplace/products`, {
                headers: {
                    'Authorization': `Bearer ${config.apiKey}`
                },
                params: {
                    category: 'business-investing,employment-jobs,money-making',
                    limit: 100,
                    sort_by: 'commission'
                },
                timeout: this.config.timeout
            });

            if (response.data && response.data.results) {
                for (const product of response.data.results) {
                    const commissionRate = product.commission_percentage / 100;
                    
                    if (commissionRate >= this.config.minCommissionRate) {
                        opportunities.push({
                            id: `cb_${product.id}`,
                            title: product.title,
                            description: product.description,
                            commissionRate: commissionRate,
                            price: product.price,
                            currency: 'USD',
                            category: product.category,
                            vendor: product.vendor,
                            gravity: product.gravity || 0,
                            conversionRate: product.conversion_rate || 0,
                            source: 'clickbank',
                            type: 'affiliate_product',
                            url: product.hop_link,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                salesCount: product.sales_count || 0,
                                refundRate: product.refund_rate || 0,
                                averageOrderValue: product.price
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('ClickBank API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanShareASale(config) {
        const opportunities = [];
        
        try {
            const response = await axios.get(`${config.baseUrl}/api/merchants`, {
                headers: {
                    'Authorization': `Bearer ${config.apiKey}`,
                    'Content-Type': 'application/json'
                },
                params: {
                    category: 'business,finance,marketing',
                    status: 'active',
                    limit: 50
                },
                timeout: this.config.timeout
            });

            if (response.data && response.data.merchants) {
                for (const merchant of response.data.merchants) {
                    if (merchant.commission_rate >= this.config.minCommissionRate) {
                        opportunities.push({
                            id: `sas_${merchant.merchant_id}`,
                            title: merchant.merchant_name,
                            description: merchant.description || '',
                            commissionRate: merchant.commission_rate,
                            price: 0, // Merchant-based, not product-based
                            currency: 'USD',
                            category: merchant.category,
                            vendor: merchant.merchant_name,
                            gravity: merchant.performance_score || 0,
                            conversionRate: merchant.conversion_rate || 0,
                            source: 'shareasale',
                            type: 'affiliate_merchant',
                            url: merchant.join_url,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                salesCount: merchant.sales_count || 0,
                                refundRate: merchant.refund_rate || 0,
                                averageOrderValue: merchant.avg_order_value || 0
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('ShareASale API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanCJAffiliate(config) {
        const opportunities = [];
        
        try {
            const response = await axios.get(`${config.baseUrl}/advertiser-lookup`, {
                headers: {
                    'Authorization': `Bearer ${config.apiKey}`,
                    'Content-Type': 'application/json'
                },
                params: {
                    'advertiser-ids': 'joined',
                    'categories': 'business-to-business,financial-services,education'
                },
                timeout: this.config.timeout
            });

            if (response.data && response.data.advertisers) {
                for (const advertiser of response.data.advertisers) {
                    if (advertiser.network_rank <= 100) { // Top performers
                        opportunities.push({
                            id: `cj_${advertiser.advertiser_id}`,
                            title: advertiser.advertiser_name,
                            description: advertiser.program_description || '',
                            commissionRate: advertiser.commission_rate || 0.05, // Default 5%
                            price: 0,
                            currency: 'USD',
                            category: advertiser.primary_category,
                            vendor: advertiser.advertiser_name,
                            gravity: (100 - advertiser.network_rank) || 0,
                            conversionRate: advertiser.conversion_rate || 0,
                            source: 'cj_affiliate',
                            type: 'affiliate_advertiser',
                            url: advertiser.program_url,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                salesCount: advertiser.sales_count || 0,
                                refundRate: advertiser.refund_rate || 0,
                                averageOrderValue: advertiser.avg_order_value || 0
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('CJ Affiliate API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanImpact(config) {
        const opportunities = [];
        
        try {
            const response = await axios.get(`${config.baseUrl}/Advertisers`, {
                headers: {
                    'Authorization': `Basic ${Buffer.from(`${config.accountSid}:${config.authToken}`).toString('base64')}`,
                    'Content-Type': 'application/json'
                },
                params: {
                    PageSize: 100,
                    Status: 'ACTIVE'
                },
                timeout: this.config.timeout
            });

            if (response.data && response.data.Advertisers) {
                for (const advertiser of response.data.Advertisers) {
                    if (advertiser.DefaultPayout && advertiser.DefaultPayout.Amount >= this.config.minCommissionRate * 100) {
                        opportunities.push({
                            id: `impact_${advertiser.Id}`,
                            title: advertiser.Name,
                            description: advertiser.Description || '',
                            commissionRate: advertiser.DefaultPayout.Amount / 100,
                            price: 0,
                            currency: advertiser.DefaultPayout.Currency || 'USD',
                            category: advertiser.Category || 'general',
                            vendor: advertiser.Name,
                            gravity: advertiser.Rank || 0,
                            conversionRate: advertiser.ConversionRate || 0,
                            source: 'impact',
                            type: 'affiliate_advertiser',
                            url: advertiser.TrackingUrl,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                salesCount: advertiser.SalesCount || 0,
                                refundRate: advertiser.RefundRate || 0,
                                averageOrderValue: advertiser.AverageOrderValue || 0
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('Impact API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    deduplicateOpportunities(opportunities) {
        const seen = new Set();
        return opportunities.filter(opportunity => {
            const key = `${opportunity.title}_${opportunity.vendor}_${opportunity.commissionRate}`;
            if (seen.has(key)) {
                return false;
            }
            seen.add(key);
            return true;
        });
    }

    async rateLimitCheck() {
        const now = Date.now();
        
        if (now - this.lastResetTime >= 60000) { // Reset every minute
            this.requestCount = 0;
            this.lastResetTime = now;
        }
        
        if (this.requestCount >= this.config.maxRequestsPerMinute) {
            const waitTime = 60000 - (now - this.lastResetTime);
            await new Promise(resolve => setTimeout(resolve, waitTime));
            this.requestCount = 0;
            this.lastResetTime = Date.now();
        }
        
        this.requestCount++;
    }

    clearCache() {
        this.cache.clear();
    }

    getStats() {
        return {
            cacheSize: this.cache.size,
            requestCount: this.requestCount,
            lastResetTime: this.lastResetTime
        };
    }
}

module.exports = { AffiliateScanner };