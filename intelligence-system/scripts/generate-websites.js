#!/usr/bin/env node

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const WebsiteGenerator = require('../strategies/website-generator');

// Database connection
const db = new sqlite3.Database(path.join(__dirname, '..', 'databases', 'opportunity.db'));

async function generateWebsites() {
    console.log('🌐 Starting website generation...\n');
    
    const generator = new WebsiteGenerator(db);
    
    // Get top opportunities
    db.all(
        'SELECT * FROM opportunities WHERE status = "new" ORDER BY potential_revenue DESC LIMIT 5',
        async (err, opportunities) => {
            if (err) {
                console.error('Error fetching opportunities:', err);
                return;
            }
            
            console.log(`Found ${opportunities.length} opportunities to convert into websites\n`);
            
            for (const opp of opportunities) {
                try {
                    console.log(`📦 Generating website for: ${opp.title}`);
                    console.log(`   💰 Potential Revenue: $${opp.potential_revenue}`);
                    console.log(`   🎯 Competition: ${opp.competition_level}`);
                    
                    const website = await generator.generateWebsiteFromOpportunity(opp.id);
                    
                    console.log(`   ✅ Website created: ${website.domain}`);
                    console.log(`   📁 Location: ${website.projectPath}`);
                    console.log(`   🎨 Theme: ${website.design.name} (${website.design.primaryColor})`);
                    console.log(`   💵 Monetization: ${website.monetization.map(m => m.type).join(', ')}`);
                    console.log('');
                    
                    // Update opportunity status
                    db.run(
                        'UPDATE opportunities SET status = "processed" WHERE id = ?',
                        [opp.id]
                    );
                    
                } catch (error) {
                    console.error(`   ❌ Error generating website:`, error.message);
                }
            }
            
            console.log('\n🎉 Website generation complete!');
            console.log('\n📝 Next steps:');
            console.log('1. Review generated websites in ./generated-websites/');
            console.log('2. Update content and design as needed');
            console.log('3. Configure real API keys for monetization');
            console.log('4. Deploy using the provided deployment scripts');
            
            // Show summary
            db.get(
                'SELECT COUNT(*) as count FROM website_projects WHERE status = "ready"',
                (err, row) => {
                    if (!err && row) {
                        console.log(`\n📊 Total websites ready for deployment: ${row.count}`);
                    }
                    db.close();
                }
            );
        }
    );
}

// Run the generator
generateWebsites();