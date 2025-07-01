const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

class DatabaseConfig {
    constructor(config = {}) {
        this.config = {
            dbPath: config.dbPath || path.join(__dirname, '../databases/intelligence.db'),
            backupPath: config.backupPath || path.join(__dirname, '../databases/backups/'),
            schemaPath: config.schemaPath || path.join(__dirname, '../databases/schemas.sql'),
            seedDataPath: config.seedDataPath || path.join(__dirname, '../databases/seed-data.json'),
            maxConnections: config.maxConnections || 5,
            timeout: config.timeout || 30000,
            enableWAL: config.enableWAL !== false, // WAL mode enabled by default
            backupInterval: config.backupInterval || 24 * 60 * 60 * 1000, // 24 hours
            maxBackups: config.maxBackups || 7,
            ...config
        };

        this.db = null;
        this.isConnected = false;
        this.connectionPool = [];
        this.backupTimer = null;
        
        this.initializeDatabase();
    }

    async initializeDatabase() {
        try {
            // Ensure directories exist
            this.ensureDirectoriesExist();
            
            // Initialize database connection
            await this.connect();
            
            // Setup database schema
            await this.setupSchema();
            
            // Load seed data if database is empty
            await this.loadSeedDataIfNeeded();
            
            // Configure database settings
            await this.configureDatabase();
            
            // Start backup scheduler
            this.startBackupScheduler();
            
            console.log('Database initialized successfully');
        } catch (error) {
            console.error('Database initialization failed:', error);
            throw error;
        }
    }

    ensureDirectoriesExist() {
        const dirs = [
            path.dirname(this.config.dbPath),
            this.config.backupPath
        ];

        dirs.forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
                console.log(`Created directory: ${dir}`);
            }
        });
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(this.config.dbPath, (err) => {
                if (err) {
                    console.error('Database connection error:', err);
                    reject(err);
                } else {
                    this.isConnected = true;
                    console.log(`Connected to SQLite database: ${this.config.dbPath}`);
                    resolve();
                }
            });
        });
    }

    async setupSchema() {
        try {
            if (fs.existsSync(this.config.schemaPath)) {
                const schema = fs.readFileSync(this.config.schemaPath, 'utf8');
                await this.executeSQLScript(schema);
                console.log('Database schema setup completed');
            } else {
                console.warn('Schema file not found, creating basic tables');
                await this.createBasicSchema();
            }
        } catch (error) {
            console.error('Schema setup failed:', error);
            throw error;
        }
    }

    async executeSQLScript(script) {
        return new Promise((resolve, reject) => {
            this.db.exec(script, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });
    }

    async createBasicSchema() {
        const basicSchema = `
            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT,
                score INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                metrics TEXT,
                tags TEXT
            );

            CREATE TABLE IF NOT EXISTS scanner_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scanner_name TEXT NOT NULL,
                scan_started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                scan_completed_at DATETIME,
                opportunities_found INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running'
            );

            CREATE INDEX IF NOT EXISTS idx_opportunities_score ON opportunities(score DESC);
            CREATE INDEX IF NOT EXISTS idx_opportunities_source ON opportunities(source);
        `;

        await this.executeSQLScript(basicSchema);
    }

    async loadSeedDataIfNeeded() {
        try {
            // Check if database has any data
            const hasData = await this.hasExistingData();
            
            if (!hasData && fs.existsSync(this.config.seedDataPath)) {
                console.log('Loading seed data...');
                const seedData = JSON.parse(fs.readFileSync(this.config.seedDataPath, 'utf8'));
                await this.loadSeedData(seedData);
                console.log('Seed data loaded successfully');
            }
        } catch (error) {
            console.warn('Failed to load seed data:', error.message);
        }
    }

    async hasExistingData() {
        return new Promise((resolve, reject) => {
            this.db.get("SELECT COUNT(*) as count FROM opportunities", (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row.count > 0);
                }
            });
        });
    }

    async loadSeedData(seedData) {
        const tables = ['tracked_keywords', 'n8n_workflows'];
        
        for (const tableName of tables) {
            if (seedData[tableName]) {
                await this.insertSeedDataForTable(tableName, seedData[tableName]);
            }
        }

        // Load sample opportunities
        if (seedData.sample_opportunities) {
            await this.insertSampleOpportunities(seedData.sample_opportunities);
        }

        // Load market conditions
        if (seedData.sample_market_conditions) {
            await this.insertMarketConditions(seedData.sample_market_conditions);
        }
    }

    async insertSeedDataForTable(tableName, data) {
        for (const item of data) {
            const columns = Object.keys(item);
            const placeholders = columns.map(() => '?').join(',');
            const values = Object.values(item);

            // Convert arrays/objects to JSON strings
            const processedValues = values.map(value => 
                typeof value === 'object' ? JSON.stringify(value) : value
            );

            const sql = `INSERT OR IGNORE INTO ${tableName} (${columns.join(',')}) VALUES (${placeholders})`;
            
            await new Promise((resolve, reject) => {
                this.db.run(sql, processedValues, function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(this.lastID);
                    }
                });
            });
        }
        
        console.log(`Loaded ${data.length} records into ${tableName}`);
    }

    async insertSampleOpportunities(opportunities) {
        for (const opportunity of opportunities) {
            const sql = `
                INSERT OR IGNORE INTO opportunities 
                (id, title, description, source, type, category, score, status, metadata, metrics, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;
            
            const values = [
                opportunity.id,
                opportunity.title,
                opportunity.description,
                opportunity.source,
                opportunity.type,
                opportunity.category,
                opportunity.score,
                opportunity.status,
                JSON.stringify(opportunity.metadata || {}),
                JSON.stringify(opportunity.metrics || {}),
                JSON.stringify(opportunity.tags || [])
            ];

            await new Promise((resolve, reject) => {
                this.db.run(sql, values, function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(this.lastID);
                    }
                });
            });
        }
        
        console.log(`Loaded ${opportunities.length} sample opportunities`);
    }

    async insertMarketConditions(conditions) {
        for (const condition of conditions) {
            const sql = `
                INSERT OR IGNORE INTO market_conditions 
                (condition_date, market_sentiment, volatility_index, consumer_confidence, 
                 social_media_activity, trending_topics, viral_content_count, 
                 seasonal_multiplier, holiday_factor, weekend_factor, 
                 global_market_activity, optimal_posting_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;
            
            const values = [
                condition.condition_date,
                condition.market_sentiment,
                condition.volatility_index,
                condition.consumer_confidence,
                condition.social_media_activity,
                JSON.stringify(condition.trending_topics || []),
                condition.viral_content_count,
                condition.seasonal_multiplier,
                condition.holiday_factor,
                condition.weekend_factor,
                condition.global_market_activity,
                JSON.stringify(condition.optimal_posting_hours || {})
            ];

            await new Promise((resolve, reject) => {
                this.db.run(sql, values, function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(this.lastID);
                    }
                });
            });
        }
        
        console.log(`Loaded ${conditions.length} market condition records`);
    }

    async configureDatabase() {
        const settings = [
            'PRAGMA foreign_keys = ON',
            'PRAGMA journal_mode = WAL',
            'PRAGMA synchronous = NORMAL',
            'PRAGMA cache_size = 10000',
            'PRAGMA temp_store = MEMORY',
            'PRAGMA mmap_size = 268435456' // 256MB
        ];

        for (const setting of settings) {
            await this.executeSQLScript(setting);
        }

        console.log('Database configuration applied');
    }

    startBackupScheduler() {
        if (this.backupTimer) {
            clearInterval(this.backupTimer);
        }

        this.backupTimer = setInterval(() => {
            this.createBackup().catch(error => {
                console.error('Scheduled backup failed:', error);
            });
        }, this.config.backupInterval);

        console.log(`Backup scheduler started (interval: ${this.config.backupInterval}ms)`);
    }

    async createBackup() {
        try {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupFileName = `intelligence_backup_${timestamp}.db`;
            const backupPath = path.join(this.config.backupPath, backupFileName);

            // Copy database file
            fs.copyFileSync(this.config.dbPath, backupPath);

            // Cleanup old backups
            await this.cleanupOldBackups();

            console.log(`Database backup created: ${backupPath}`);
            return backupPath;
        } catch (error) {
            console.error('Backup creation failed:', error);
            throw error;
        }
    }

    async cleanupOldBackups() {
        try {
            const backupFiles = fs.readdirSync(this.config.backupPath)
                .filter(file => file.startsWith('intelligence_backup_') && file.endsWith('.db'))
                .map(file => ({
                    name: file,
                    path: path.join(this.config.backupPath, file),
                    stats: fs.statSync(path.join(this.config.backupPath, file))
                }))
                .sort((a, b) => b.stats.mtime - a.stats.mtime); // Sort by modification time, newest first

            // Remove excess backups
            if (backupFiles.length > this.config.maxBackups) {
                const filesToDelete = backupFiles.slice(this.config.maxBackups);
                for (const file of filesToDelete) {
                    fs.unlinkSync(file.path);
                    console.log(`Deleted old backup: ${file.name}`);
                }
            }
        } catch (error) {
            console.warn('Backup cleanup failed:', error);
        }
    }

    async query(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    async get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    async run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ lastID: this.lastID, changes: this.changes });
                }
            });
        });
    }

    async insert(tableName, data) {
        const columns = Object.keys(data);
        const placeholders = columns.map(() => '?').join(',');
        const values = columns.map(col => {
            const value = data[col];
            return typeof value === 'object' ? JSON.stringify(value) : value;
        });

        const sql = `INSERT INTO ${tableName} (${columns.join(',')}) VALUES (${placeholders})`;
        return await this.run(sql, values);
    }

    async update(tableName, data, whereClause, whereParams = []) {
        const columns = Object.keys(data);
        const setClause = columns.map(col => `${col} = ?`).join(', ');
        const values = columns.map(col => {
            const value = data[col];
            return typeof value === 'object' ? JSON.stringify(value) : value;
        });

        const sql = `UPDATE ${tableName} SET ${setClause} WHERE ${whereClause}`;
        return await this.run(sql, [...values, ...whereParams]);
    }

    async delete(tableName, whereClause, whereParams = []) {
        const sql = `DELETE FROM ${tableName} WHERE ${whereClause}`;
        return await this.run(sql, whereParams);
    }

    async getStats() {
        const stats = {};

        try {
            // Table counts
            const tables = ['opportunities', 'scanner_performance', 'tracked_keywords', 'n8n_workflows'];
            for (const table of tables) {
                try {
                    const result = await this.get(`SELECT COUNT(*) as count FROM ${table}`);
                    stats[`${table}_count`] = result.count;
                } catch (error) {
                    stats[`${table}_count`] = 0;
                }
            }

            // Database file size
            if (fs.existsSync(this.config.dbPath)) {
                const fileStats = fs.statSync(this.config.dbPath);
                stats.database_size_mb = (fileStats.size / 1024 / 1024).toFixed(2);
            }

            // Recent activity
            try {
                const recentOpportunities = await this.get(`
                    SELECT COUNT(*) as count 
                    FROM opportunities 
                    WHERE discovered_at >= datetime('now', '-24 hours')
                `);
                stats.opportunities_last_24h = recentOpportunities.count;
            } catch (error) {
                stats.opportunities_last_24h = 0;
            }

            // Backup info
            if (fs.existsSync(this.config.backupPath)) {
                const backupFiles = fs.readdirSync(this.config.backupPath)
                    .filter(file => file.startsWith('intelligence_backup_') && file.endsWith('.db'));
                stats.backup_count = backupFiles.length;
                
                if (backupFiles.length > 0) {
                    const latestBackup = backupFiles
                        .map(file => path.join(this.config.backupPath, file))
                        .map(filePath => ({ path: filePath, stats: fs.statSync(filePath) }))
                        .sort((a, b) => b.stats.mtime - a.stats.mtime)[0];
                    
                    stats.latest_backup = latestBackup.stats.mtime.toISOString();
                }
            }

            stats.status = 'healthy';
        } catch (error) {
            stats.status = 'error';
            stats.error = error.message;
        }

        return stats;
    }

    async vacuum() {
        try {
            await this.executeSQLScript('VACUUM');
            console.log('Database VACUUM completed');
            return true;
        } catch (error) {
            console.error('VACUUM failed:', error);
            return false;
        }
    }

    async analyze() {
        try {
            await this.executeSQLScript('ANALYZE');
            console.log('Database ANALYZE completed');
            return true;
        } catch (error) {
            console.error('ANALYZE failed:', error);
            return false;
        }
    }

    async checkIntegrity() {
        try {
            const result = await this.get('PRAGMA integrity_check');
            return {
                isValid: result.integrity_check === 'ok',
                message: result.integrity_check
            };
        } catch (error) {
            return {
                isValid: false,
                message: error.message
            };
        }
    }

    async close() {
        if (this.backupTimer) {
            clearInterval(this.backupTimer);
        }

        if (this.db && this.isConnected) {
            return new Promise((resolve) => {
                this.db.close((err) => {
                    if (err) {
                        console.error('Database close error:', err);
                    } else {
                        console.log('Database connection closed');
                    }
                    this.isConnected = false;
                    resolve();
                });
            });
        }
    }

    // Connection management for potential future connection pooling
    getConnection() {
        return this.db;
    }

    isHealthy() {
        return this.isConnected && this.db;
    }

    getConfig() {
        return { ...this.config };
    }
}

module.exports = { DatabaseConfig };