#!/usr/bin/env node

require('dotenv').config();
const express = require('express');
const cron = require('node-cron');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Core modules
const OpportunityScanner = require('./core/OpportunityScanner');
const N8nIntegration = require('./n8n-integration/opportunity-webhook');
const PythonAIBridge = require('./ai-bridge/python-ai-bridge');

// Initialize Express app
const app = express();
app.use(express.json());

// Database connection
const db = new sqlite3.Database(path.join(__dirname, 'databases', 'opportunity.db'));

// Initialize scanner, N8n integration, and AI bridge
const scanner = new OpportunityScanner(db);
const n8nIntegration = new N8nIntegration(app, db);
const aiBridge = new PythonAIBridge({
    pythonApiUrl: process.env.PYTHON_AI_URL || 'http://localhost:8000',
    timeout: 120000 // 2 minutes for AI operations
});

// API Routes
app.get('/', (req, res) => {
    res.json({
        status: 'running',
        message: 'Opportunistic Intelligence System is active',
        version: '1.0.0'
    });
});

// Get all opportunities
app.get('/api/opportunities', (req, res) => {
    const { status, type, limit = 50 } = req.query;
    let query = 'SELECT * FROM opportunities WHERE 1=1';
    const params = [];
    
    if (status) {
        query += ' AND status = ?';
        params.push(status);
    }
    
    if (type) {
        query += ' AND type = ?';
        params.push(type);
    }
    
    query += ' ORDER BY discovered_at DESC LIMIT ?';
    params.push(parseInt(limit));
    
    db.all(query, params, (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(rows);
        }
    });
});

// Trigger manual scan with AI enhancement
app.post('/api/scan', async (req, res) => {
    try {
        console.log('🔍 Manual scan triggered with AI enhancement...');
        const results = await scanner.scanAll();
        
        // Enhance top opportunities with AI if available
        if (aiBridge.isRunning && results.new > 0) {
            console.log('🧠 Enhancing opportunities with AI...');
            try {
                // Get latest opportunities
                const latestOpportunities = await getLatestOpportunities(3);
                
                // Enhance each with AI
                for (const opp of latestOpportunities) {
                    const enhanced = await aiBridge.enhanceOpportunityWithAI(opp);
                    await saveEnhancedOpportunity(enhanced);
                }
                
                results.ai_enhanced = latestOpportunities.length;
            } catch (aiError) {
                console.error('⚠️ AI enhancement failed:', aiError.message);
                results.ai_enhancement_error = aiError.message;
            }
        }
        
        res.json({
            success: true,
            message: 'Scan completed with AI enhancement',
            results: results
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get scan statistics
app.get('/api/stats', (req, res) => {
    const queries = {
        total_opportunities: 'SELECT COUNT(*) as count FROM opportunities',
        new_opportunities: 'SELECT COUNT(*) as count FROM opportunities WHERE status = "new"',
        total_products: 'SELECT COUNT(*) as count FROM affiliate_products',
        total_trends: 'SELECT COUNT(*) as count FROM social_trends',
        total_keywords: 'SELECT COUNT(*) as count FROM keyword_opportunities'
    };
    
    const stats = {};
    let completed = 0;
    
    Object.entries(queries).forEach(([key, query]) => {
        db.get(query, (err, row) => {
            stats[key] = err ? 0 : row.count;
            completed++;
            
            if (completed === Object.keys(queries).length) {
                res.json(stats);
            }
        });
    });
});

// AI-powered research endpoint
app.post('/api/ai/research', async (req, res) => {
    try {
        const { topic, options = {} } = req.body;
        
        if (!topic) {
            return res.status(400).json({ error: 'Topic is required' });
        }
        
        console.log(`🧠 AI research requested for: ${topic}`);
        
        if (!aiBridge.isRunning) {
            return res.status(503).json({ error: 'AI system not available' });
        }
        
        const result = await aiBridge.conductResearch(topic, options);
        
        res.json({
            success: true,
            topic: topic,
            result: result
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Crypto education analysis endpoint
app.post('/api/ai/crypto-analysis', async (req, res) => {
    try {
        console.log('🪙 Crypto education analysis requested');
        
        if (!aiBridge.isRunning) {
            return res.status(503).json({ error: 'AI system not available' });
        }
        
        const result = await aiBridge.analyzeCryptoEducation(req.body);
        
        res.json({
            success: true,
            result: result
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// AI system status endpoint
app.get('/api/ai/status', async (req, res) => {
    try {
        const status = await aiBridge.getSystemStatus();
        res.json(status);
    } catch (error) {
        res.json({
            system_status: 'offline',
            error: error.message
        });
    }
});

// Helper functions
async function getLatestOpportunities(limit = 5) {
    return new Promise((resolve, reject) => {
        db.all(
            'SELECT * FROM opportunities ORDER BY discovered_at DESC LIMIT ?',
            [limit],
            (err, rows) => {
                if (err) reject(err);
                else resolve(rows);
            }
        );
    });
}

async function saveEnhancedOpportunity(enhanced) {
    return new Promise((resolve, reject) => {
        const metadata = enhanced.metadata ? JSON.parse(enhanced.metadata) : {};
        metadata.ai_analysis = enhanced.ai_analysis;
        metadata.ai_confidence_score = enhanced.ai_confidence_score;
        metadata.enhancement_timestamp = enhanced.enhancement_timestamp;
        
        db.run(
            'UPDATE opportunities SET metadata = ? WHERE id = ?',
            [JSON.stringify(metadata), enhanced.id],
            (err) => {
                if (err) reject(err);
                else resolve();
            }
        );
    });
}

// Schedule automatic scans
console.log('📅 Setting up scheduled scans...');

// Every 30 minutes - Quick opportunity scan
cron.schedule('*/30 * * * *', async () => {
    console.log('⚡ Running quick opportunity scan...');
    try {
        await scanner.quickScan();
    } catch (error) {
        console.error('Error in quick scan:', error);
    }
});

// Every 6 hours - Full scan
cron.schedule('0 */6 * * *', async () => {
    console.log('🔍 Running full opportunity scan...');
    try {
        await scanner.scanAll();
    } catch (error) {
        console.error('Error in full scan:', error);
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, async () => {
    console.log(`
╔═══════════════════════════════════════════════════════╗
║       OPPORTUNISTIC INTELLIGENCE SYSTEM v2.0.0        ║
║              🧠 AI-POWERED VERSION 🧠                 ║
╠═══════════════════════════════════════════════════════╣
║  🚀 System started successfully!                      ║
║  🌐 API running on: http://localhost:${PORT}            ║
║  📊 Dashboard: http://localhost:${PORT}/dashboard       ║
║  🔍 Scanning: Every 30 minutes (quick), 6 hours (full)║
║  🧠 AI Research: http://localhost:${PORT}/api/ai/       ║
╚═══════════════════════════════════════════════════════╝
    `);
    
    // Initialize AI system
    console.log('\n🧠 Initializing AI Research System...');
    try {
        await aiBridge.initialize();
        console.log('✅ AI Research System online!');
    } catch (error) {
        console.error('⚠️ AI Research System failed to start:', error.message);
        console.log('💡 System will continue without AI enhancement');
    }
    
    // Run initial scan
    console.log('\n🎯 Running initial opportunity scan...');
    try {
        const results = await scanner.quickScan();
        console.log('✅ Initial scan complete!');
        
        // Try AI enhancement if available
        if (aiBridge.isRunning && results.new > 0) {
            console.log('🧠 Starting AI enhancement of opportunities...');
            try {
                const latestOpportunities = await getLatestOpportunities(2);
                for (const opp of latestOpportunities) {
                    const enhanced = await aiBridge.enhanceOpportunityWithAI(opp);
                    await saveEnhancedOpportunity(enhanced);
                }
                console.log(`✅ AI enhanced ${latestOpportunities.length} opportunities!`);
            } catch (aiError) {
                console.error('⚠️ AI enhancement failed:', aiError.message);
            }
        }
        
    } catch (error) {
        console.error('❌ Initial scan failed:', error.message);
    }
});

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n🛑 Shutting down gracefully...');
    
    try {
        // Shutdown AI system
        if (aiBridge.isRunning) {
            await aiBridge.shutdown();
        }
        
        // Close database
        db.close();
        
        console.log('✅ Shutdown complete');
        process.exit(0);
    } catch (error) {
        console.error('Error during shutdown:', error);
        process.exit(1);
    }
});