const fs = require('fs').promises;
const path = require('path');

class WebsiteGenerator {
    constructor(db) {
        this.db = db;
        this.templates = {
            affiliate: this.getAffiliateTemplate(),
            blog: this.getBlogTemplate(),
            landing: this.getLandingTemplate()
        };
    }

    async generateWebsiteFromOpportunity(opportunityId) {
        // Get opportunity from database
        const opportunity = await this.getOpportunity(opportunityId);
        if (!opportunity) throw new Error('Opportunity not found');

        // Determine best website type
        const websiteType = this.determineWebsiteType(opportunity);
        
        // Generate niche-specific content
        const websiteConfig = {
            domain: this.generateDomainName(opportunity),
            niche: opportunity.title.toLowerCase().replace(/[^a-z0-9]/g, '-'),
            title: opportunity.title,
            description: opportunity.description,
            keywords: opportunity.keywords || this.extractKeywords(opportunity.title),
            monetization: this.getMonetizationStrategy(opportunity),
            content: await this.generateInitialContent(opportunity),
            design: this.getDesignTheme(opportunity)
        };

        // Create project structure
        const projectPath = await this.createProjectStructure(websiteConfig);
        
        // Save to database
        await this.saveWebsiteProject(websiteConfig, opportunity.id);
        
        return {
            ...websiteConfig,
            projectPath,
            deploymentReady: true
        };
    }

    determineWebsiteType(opportunity) {
        if (opportunity.type === 'affiliate') return 'affiliate';
        if (opportunity.potential_revenue > 5000) return 'landing';
        return 'blog';
    }

    generateDomainName(opportunity) {
        const base = opportunity.title.toLowerCase()
            .replace(/[^a-z0-9]/g, '')
            .substring(0, 20);
        const suffixes = ['pro', 'hub', 'central', 'guide', 'master'];
        const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
        return `${base}${suffix}.com`;
    }

    extractKeywords(title) {
        return title.toLowerCase().split(' ')
            .filter(word => word.length > 3)
            .join(',');
    }

    getMonetizationStrategy(opportunity) {
        const strategies = [];
        
        if (opportunity.type === 'affiliate') {
            strategies.push({
                type: 'affiliate',
                network: opportunity.source,
                productId: opportunity.metadata?.productId || 'default',
                commission: opportunity.metadata?.commission || '50%'
            });
        }
        
        strategies.push({
            type: 'adsense',
            placement: 'automatic'
        });
        
        if (opportunity.potential_revenue > 3000) {
            strategies.push({
                type: 'email',
                provider: 'convertkit',
                leadMagnet: 'free-guide'
            });
        }
        
        return strategies;
    }

    async generateInitialContent(opportunity) {
        return {
            homepage: {
                hero: {
                    headline: `Master ${opportunity.title} Today`,
                    subheadline: opportunity.description || 'Discover the secrets to success',
                    cta: 'Get Started Now'
                },
                sections: [
                    {
                        type: 'benefits',
                        title: 'Why Choose Us',
                        items: [
                            'Expert guidance and support',
                            'Proven strategies that work',
                            'Money-back guarantee'
                        ]
                    },
                    {
                        type: 'testimonials',
                        title: 'Success Stories',
                        items: this.generateTestimonials(3)
                    },
                    {
                        type: 'cta',
                        title: 'Ready to Start?',
                        button: 'Click Here to Begin'
                    }
                ]
            },
            pages: [
                {
                    slug: 'about',
                    title: 'About Us',
                    content: 'Leading experts in ' + opportunity.title
                },
                {
                    slug: 'guide',
                    title: 'Complete Guide',
                    content: this.generateGuideContent(opportunity)
                }
            ]
        };
    }

    generateTestimonials(count) {
        const names = ['Sarah M.', 'John D.', 'Lisa K.', 'Mike R.', 'Emma T.'];
        const testimonials = [];
        
        for (let i = 0; i < count; i++) {
            testimonials.push({
                name: names[i % names.length],
                text: 'This changed my life! Highly recommended.',
                rating: 5
            });
        }
        
        return testimonials;
    }

    generateGuideContent(opportunity) {
        return `
# The Ultimate Guide to ${opportunity.title}

## Introduction
Welcome to your comprehensive guide on ${opportunity.title}.

## Chapter 1: Getting Started
Learn the fundamentals...

## Chapter 2: Advanced Strategies
Take your skills to the next level...

## Chapter 3: Success Tips
Insider secrets for maximum results...

## Conclusion
Start your journey today!
        `.trim();
    }

    getDesignTheme(opportunity) {
        const themes = [
            { name: 'modern', primaryColor: '#3B82F6', style: 'clean' },
            { name: 'professional', primaryColor: '#10B981', style: 'corporate' },
            { name: 'bold', primaryColor: '#EF4444', style: 'energetic' },
            { name: 'elegant', primaryColor: '#8B5CF6', style: 'sophisticated' }
        ];
        
        return themes[Math.floor(Math.random() * themes.length)];
    }

    async createProjectStructure(config) {
        const projectName = config.domain.replace('.com', '');
        const projectPath = path.join(__dirname, '..', 'generated-websites', projectName);
        
        // Create directories
        await fs.mkdir(projectPath, { recursive: true });
        await fs.mkdir(path.join(projectPath, 'public'), { recursive: true });
        await fs.mkdir(path.join(projectPath, 'src'), { recursive: true });
        
        // Create index.html
        const indexHtml = this.generateIndexHtml(config);
        await fs.writeFile(path.join(projectPath, 'public', 'index.html'), indexHtml);
        
        // Create config file
        await fs.writeFile(
            path.join(projectPath, 'config.json'),
            JSON.stringify(config, null, 2)
        );
        
        // Create deployment script
        const deployScript = this.generateDeployScript(config);
        await fs.writeFile(path.join(projectPath, 'deploy.sh'), deployScript);
        await fs.chmod(path.join(projectPath, 'deploy.sh'), '755');
        
        return projectPath;
    }

    generateIndexHtml(config) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${config.title}</title>
    <meta name="description" content="${config.description}">
    <meta name="keywords" content="${config.keywords}">
    <style>
        :root {
            --primary-color: ${config.design.primaryColor};
        }
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
        }
        .hero {
            background: var(--primary-color);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
        }
        .hero h1 {
            margin: 0 0 1rem;
            font-size: 3rem;
        }
        .hero p {
            font-size: 1.25rem;
            margin-bottom: 2rem;
        }
        .btn {
            display: inline-block;
            background: white;
            color: var(--primary-color);
            padding: 1rem 2rem;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: scale(1.05);
        }
        .section {
            padding: 3rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .benefits {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        .benefit {
            text-align: center;
            padding: 2rem;
            background: #f5f5f5;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>${config.content.homepage.hero.headline}</h1>
        <p>${config.content.homepage.hero.subheadline}</p>
        <a href="#" class="btn">${config.content.homepage.hero.cta}</a>
    </div>
    
    ${config.content.homepage.sections.map(section => {
        if (section.type === 'benefits') {
            return `
            <div class="section">
                <h2>${section.title}</h2>
                <div class="benefits">
                    ${section.items.map(item => `
                        <div class="benefit">
                            <p>${item}</p>
                        </div>
                    `).join('')}
                </div>
            </div>`;
        }
        return '';
    }).join('')}
    
    <!-- Monetization Scripts -->
    ${config.monetization.map(strategy => {
        if (strategy.type === 'adsense') {
            return '<!-- Google AdSense placeholder -->';
        }
        return '';
    }).join('')}
</body>
</html>`;
    }

    generateDeployScript(config) {
        return `#!/bin/bash
# Auto-generated deployment script for ${config.domain}

echo "🚀 Deploying ${config.domain}..."

# Option 1: Deploy to Netlify
# netlify deploy --prod --dir=public

# Option 2: Deploy to Vercel
# vercel --prod

# Option 3: Deploy to GitHub Pages
# git init
# git add .
# git commit -m "Initial commit"
# git push origin main

echo "✅ Deployment complete!"
`;
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

    async saveWebsiteProject(config, strategyId) {
        return new Promise((resolve, reject) => {
            const query = `
                INSERT INTO website_projects 
                (domain, niche, strategy_id, status, traffic_goal, revenue_goal, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            `;
            
            this.db.run(query, [
                config.domain,
                config.niche,
                strategyId,
                'ready',
                1000, // Initial traffic goal
                config.monetization[0]?.commission || 1000,
                JSON.stringify(config)
            ], function(err) {
                if (err) reject(err);
                else resolve(this.lastID);
            });
        });
    }

    getAffiliateTemplate() {
        return 'affiliate-template';
    }

    getBlogTemplate() {
        return 'blog-template';
    }

    getLandingTemplate() {
        return 'landing-template';
    }
}

module.exports = WebsiteGenerator;