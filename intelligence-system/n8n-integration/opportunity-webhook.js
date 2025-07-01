// N8n Webhook Integration for Opportunity Scanner
// This creates a webhook endpoint that n8n can call to trigger actions

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class N8nIntegration {
    constructor(app, db) {
        this.app = app;
        this.db = db;
        this.setupWebhooks();
    }

    setupWebhooks() {
        // Webhook for new opportunities
        this.app.post('/webhook/new-opportunity', (req, res) => {
            this.handleNewOpportunity(req, res);
        });

        // Webhook for website deployment
        this.app.post('/webhook/deploy-website', (req, res) => {
            this.handleWebsiteDeployment(req, res);
        });

        // Webhook for content generation
        this.app.post('/webhook/generate-content', (req, res) => {
            this.handleContentGeneration(req, res);
        });

        // Webhook for social media distribution
        this.app.post('/webhook/distribute-social', (req, res) => {
            this.handleSocialDistribution(req, res);
        });
    }

    async handleNewOpportunity(req, res) {
        const { opportunity } = req.body;
        
        console.log('🎯 N8n triggered: New opportunity received');
        
        try {
            // Save opportunity to database
            const opportunityId = await this.saveOpportunity(opportunity);
            
            // Trigger automated workflow
            const actions = await this.getAutomatedActions(opportunity);
            
            res.json({
                success: true,
                opportunityId,
                automatedActions: actions,
                webhookTriggered: {
                    contentGeneration: `/webhook/generate-content`,
                    websiteCreation: `/webhook/deploy-website`,
                    socialDistribution: `/webhook/distribute-social`
                }
            });
            
        } catch (error) {
            console.error('Webhook error:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleWebsiteDeployment(req, res) {
        const { opportunityId, domain } = req.body;
        
        console.log('🚀 N8n triggered: Website deployment');
        
        try {
            // Update website status
            await this.updateWebsiteStatus(opportunityId, 'deploying');
            
            // Return deployment instructions for n8n
            res.json({
                success: true,
                deploymentSteps: [
                    {
                        action: 'build',
                        command: 'npm run build',
                        directory: `./generated-websites/${domain.replace('.com', '')}`
                    },
                    {
                        action: 'deploy-netlify',
                        command: 'netlify deploy --prod --dir=public',
                        environment: {
                            NETLIFY_SITE_ID: process.env.NETLIFY_SITE_ID,
                            NETLIFY_AUTH_TOKEN: process.env.NETLIFY_AUTH_TOKEN
                        }
                    },
                    {
                        action: 'update-status',
                        webhook: '/webhook/deployment-complete'
                    }
                ]
            });
            
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleContentGeneration(req, res) {
        const { opportunityId, contentType = 'blog' } = req.body;
        
        console.log('📝 N8n triggered: Content generation');
        
        try {
            const opportunity = await this.getOpportunity(opportunityId);
            
            const contentPlan = {
                mainArticle: {
                    title: `Ultimate Guide to ${opportunity.title}`,
                    wordCount: 2500,
                    sections: [
                        'Introduction',
                        'Key Benefits',
                        'How to Get Started',
                        'Expert Tips',
                        'Conclusion'
                    ]
                },
                socialMedia: {
                    twitter: [
                        `🔥 Discovered: ${opportunity.title}`,
                        `💰 Potential: $${opportunity.potential_revenue}`,
                        `Get started: [link]`
                    ],
                    linkedin: `Professional insight into ${opportunity.title}...`,
                    instagram: {
                        caption: `Transform your business with ${opportunity.title}`,
                        hashtags: this.generateHashtags(opportunity)
                    }
                },
                email: {
                    subject: `🚀 New Opportunity: ${opportunity.title}`,
                    template: 'opportunity-announcement'
                }
            };
            
            res.json({
                success: true,
                contentPlan,
                nextSteps: [
                    'Generate main article content',
                    'Create social media posts',
                    'Design email campaign',
                    'Schedule content distribution'
                ]
            });
            
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleSocialDistribution(req, res) {
        const { content, platforms } = req.body;
        
        console.log('📱 N8n triggered: Social media distribution');
        
        try {
            const distributionPlan = {
                twitter: {
                    post: content.twitter,
                    schedule: 'immediate',
                    engagement: 'auto-reply enabled'
                },
                linkedin: {
                    post: content.linkedin,
                    schedule: '+2 hours',
                    targeting: 'business professionals'
                },
                instagram: {
                    post: content.instagram,
                    schedule: '+4 hours',
                    format: 'carousel'
                }
            };
            
            res.json({
                success: true,
                distributionPlan,
                estimatedReach: 10000,
                expectedEngagement: '3-5%'
            });
            
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    generateHashtags(opportunity) {
        const base = opportunity.title.toLowerCase().split(' ');
        const hashtags = base
            .filter(word => word.length > 4)
            .map(word => `#${word}`)
            .slice(0, 5);
        
        hashtags.push('#business', '#opportunity', '#success');
        return hashtags.join(' ');
    }

    async getAutomatedActions(opportunity) {
        const actions = [];
        
        if (opportunity.potential_revenue > 5000) {
            actions.push('priority-content-creation');
            actions.push('immediate-website-generation');
        }
        
        if (opportunity.competition_level === 'low') {
            actions.push('aggressive-marketing-campaign');
        }
        
        actions.push('social-media-announcement');
        actions.push('email-notification');
        
        return actions;
    }

    async saveOpportunity(opportunity) {
        return new Promise((resolve, reject) => {
            const query = `
                INSERT INTO opportunities (source, type, title, description, potential_revenue, competition_level, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            `;
            
            this.db.run(query, [
                opportunity.source || 'n8n',
                opportunity.type || 'manual',
                opportunity.title,
                opportunity.description,
                opportunity.potential_revenue,
                opportunity.competition_level,
                JSON.stringify(opportunity.metadata || {})
            ], function(err) {
                if (err) reject(err);
                else resolve(this.lastID);
            });
        });
    }

    async getOpportunity(id) {
        return new Promise((resolve, reject) => {
            this.db.get(
                'SELECT * FROM opportunities WHERE id = ?',
                [id],
                (err, row) => {
                    if (err) reject(err);
                    else resolve(row);
                }
            );
        });
    }

    async updateWebsiteStatus(opportunityId, status) {
        return new Promise((resolve, reject) => {
            this.db.run(
                'UPDATE website_projects SET status = ? WHERE strategy_id = ?',
                [status, opportunityId],
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    }
}

module.exports = N8nIntegration;