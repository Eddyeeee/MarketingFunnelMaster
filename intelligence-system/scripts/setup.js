#!/usr/bin/env node

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// Create databases directory if it doesn't exist
const dbDir = path.join(__dirname, '..', 'databases');
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

// Database path
const dbPath = path.join(dbDir, 'opportunity.db');

console.log('🚀 Setting up Opportunistic Intelligence System Database...');
console.log(`📁 Database location: ${dbPath}`);

// Create database connection
const db = new sqlite3.Database(dbPath);

// SQL schema
const schema = `
-- Opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    potential_revenue REAL,
    competition_level TEXT,
    time_sensitivity TEXT,
    keywords TEXT,
    metadata JSON,
    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'new',
    score REAL DEFAULT 0
);

-- Affiliate products table
CREATE TABLE IF NOT EXISTS affiliate_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    network TEXT NOT NULL,
    product_id TEXT NOT NULL,
    name TEXT NOT NULL,
    category TEXT,
    commission_rate REAL,
    gravity REAL,
    conversion_rate REAL,
    avg_sale_amount REAL,
    refund_rate REAL,
    url TEXT,
    metadata JSON,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(network, product_id)
);

-- Social trends table
CREATE TABLE IF NOT EXISTS social_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    trend_name TEXT NOT NULL,
    hashtags TEXT,
    engagement_rate REAL,
    growth_rate REAL,
    volume INTEGER,
    sentiment TEXT,
    category TEXT,
    metadata JSON,
    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Keyword opportunities table
CREATE TABLE IF NOT EXISTS keyword_opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    search_volume INTEGER,
    competition REAL,
    cpc REAL,
    trend TEXT,
    related_keywords TEXT,
    metadata JSON,
    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Campaign strategies table
CREATE TABLE IF NOT EXISTS campaign_strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER,
    strategy_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    estimated_roi REAL,
    implementation_steps JSON,
    resources_needed JSON,
    timeline_days INTEGER,
    risk_level TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'draft',
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
);

-- Website projects table
CREATE TABLE IF NOT EXISTS website_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    niche TEXT NOT NULL,
    strategy_id INTEGER,
    status TEXT DEFAULT 'planning',
    traffic_goal INTEGER,
    revenue_goal REAL,
    launch_date DATE,
    metadata JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (strategy_id) REFERENCES campaign_strategies (id)
);

-- Analytics events table
CREATE TABLE IF NOT EXISTS analytics_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    source TEXT,
    data JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_type ON opportunities(type);
CREATE INDEX IF NOT EXISTS idx_affiliate_products_network ON affiliate_products(network);
CREATE INDEX IF NOT EXISTS idx_social_trends_platform ON social_trends(platform);
CREATE INDEX IF NOT EXISTS idx_keyword_opportunities_volume ON keyword_opportunities(search_volume);
CREATE INDEX IF NOT EXISTS idx_campaign_strategies_opportunity ON campaign_strategies(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_website_projects_status ON website_projects(status);
`;

// Execute schema
db.exec(schema, (err) => {
    if (err) {
        console.error('❌ Error creating database schema:', err);
        process.exit(1);
    }
    
    console.log('✅ Database schema created successfully!');
    
    // Insert sample data for testing
    const sampleData = `
    INSERT OR IGNORE INTO opportunities (source, type, title, description, potential_revenue, competition_level)
    VALUES 
    ('manual', 'test', 'Test Opportunity', 'Sample opportunity for testing', 1000, 'low'),
    ('digistore24', 'affiliate', 'High-Converting Fitness Product', 'Fitness product with 50% commission', 5000, 'medium');
    `;
    
    db.exec(sampleData, (err) => {
        if (err) {
            console.error('⚠️  Warning: Could not insert sample data:', err.message);
        } else {
            console.log('📊 Sample data inserted for testing');
        }
        
        // Close database
        db.close((err) => {
            if (err) {
                console.error('Error closing database:', err);
            } else {
                console.log('🎉 Setup complete! Database is ready to use.');
                console.log('\n📝 Next steps:');
                console.log('1. Update .env file with your API keys');
                console.log('2. Run "npm start" to begin scanning');
                console.log('3. Access dashboard at http://localhost:3000');
            }
        });
    });
});