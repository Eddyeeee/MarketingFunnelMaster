#!/usr/bin/env node

require('dotenv').config();
const express = require('express');
const cron = require('node-cron');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Core modules
const OpportunityScanner = require('./core/OpportunityScanner');
const N8nIntegration = require('./n8n-integration/opportunity-webhook');

// Initialize Express app
const app = express();
app.use(express.json());

// Database connection
const db = new sqlite3.Database(path.join(__dirname, 'databases', 'opportunity.db'));

// Initialize scanner and N8n integration
const scanner = new OpportunityScanner(db);
const n8nIntegration = new N8nIntegration(app, db);

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

// Trigger manual scan
app.post('/api/scan', async (req, res) => {
    try {
        console.log('🔍 Manual scan triggered...');
        const results = await scanner.scanAll();
        res.json({
            success: true,
            message: 'Scan completed',
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
║       OPPORTUNISTIC INTELLIGENCE SYSTEM v1.0.0        ║
╠═══════════════════════════════════════════════════════╣
║  🚀 System started successfully!                      ║
║  🌐 API running on: http://localhost:${PORT}            ║
║  📊 Dashboard: http://localhost:${PORT}/dashboard       ║
║  🔍 Scanning: Every 30 minutes (quick), 6 hours (full)║
╚═══════════════════════════════════════════════════════╝
    `);
    
    // Run initial scan
    console.log('\n🎯 Running initial opportunity scan...');
    try {
        const results = await scanner.quickScan();
        console.log('✅ Initial scan complete!');
    } catch (error) {
        console.error('❌ Initial scan failed:', error.message);
    }
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down gracefully...');
    db.close();
    process.exit(0);
});