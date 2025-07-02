/**
 * Auto-Integrate Scanners with Creator Intelligence
 * 
 * Automatically enhances all existing scanners with creator intelligence capabilities
 * No manual configuration needed - works with any scanner automatically!
 */

const fs = require('fs').promises;
const path = require('path');
const CreatorIntelligenceBridge = require('./creator_intelligence_bridge');

class ScannerAutoIntegrator {
    constructor() {
        this.bridge = new CreatorIntelligenceBridge();
        this.integratedScanners = new Map();
        this.scannersPath = path.join(__dirname, '..', 'scanners');
        
        // Initialize after bridge is ready
        this.bridge.on('ready', () => {
            this.autoIntegrateAllScanners();
        });
        
        this.bridge.on('analysisComplete', (result) => {
            this.handleCreatorAnalysisComplete(result);
        });
    }
    
    async autoIntegrateAllScanners() {
        console.log('🚀 Auto-integrating all scanners with Creator Intelligence...');
        
        try {
            // Find all scanner files
            const scannerFiles = await this.findScannerFiles();
            
            console.log(`📁 Found ${scannerFiles.length} scanner files to integrate`);
            
            // Integrate each scanner
            for (const scannerFile of scannerFiles) {
                await this.integrateScannerFile(scannerFile);
            }
            
            console.log(`✅ Successfully integrated ${this.integratedScanners.size} scanners with Creator Intelligence`);
            
        } catch (error) {
            console.error('❌ Failed to auto-integrate scanners:', error.message);
        }
    }
    
    async findScannerFiles() {
        const scannerFiles = [];
        
        try {
            const files = await fs.readdir(this.scannersPath);
            
            for (const file of files) {
                if (file.endsWith('.js') && !file.includes('test')) {
                    const filePath = path.join(this.scannersPath, file);
                    const stats = await fs.stat(filePath);
                    
                    if (stats.isFile()) {
                        scannerFiles.push({
                            name: file.replace('.js', ''),
                            path: filePath,
                            file: file
                        });
                    }
                }
            }
        } catch (error) {
            console.warn('Warning: Could not read scanners directory:', error.message);
        }
        
        return scannerFiles;
    }
    
    async integrateScannerFile(scannerInfo) {
        try {
            console.log(`🔧 Integrating ${scannerInfo.name} scanner...`);
            
            // Read scanner file
            const scannerContent = await fs.readFile(scannerInfo.path, 'utf8');
            
            // Check if already integrated
            if (scannerContent.includes('CreatorIntelligenceBridge') || 
                scannerContent.includes('creator_intelligence_enhanced')) {
                console.log(`⏭️  ${scannerInfo.name} already integrated, skipping`);
                return;
            }
            
            // Detect scanner pattern and integrate
            const integratedContent = await this.enhanceScannerContent(scannerContent, scannerInfo.name);
            
            if (integratedContent !== scannerContent) {
                // Create backup
                await fs.writeFile(`${scannerInfo.path}.backup`, scannerContent);
                
                // Write enhanced version
                await fs.writeFile(scannerInfo.path, integratedContent);
                
                this.integratedScanners.set(scannerInfo.name, {
                    file: scannerInfo.file,
                    integratedAt: new Date(),
                    backupCreated: true
                });
                
                console.log(`✅ Successfully integrated ${scannerInfo.name}`);
            } else {
                console.log(`⚠️  Could not integrate ${scannerInfo.name} - no recognized pattern`);
            }
            
        } catch (error) {
            console.error(`❌ Failed to integrate ${scannerInfo.name}:`, error.message);
        }
    }
    
    async enhanceScannerContent(content, scannerName) {
        // Add creator intelligence import at the top
        let enhancedContent = content;
        
        // Pattern 1: Standard module pattern
        if (content.includes('module.exports') && content.includes('class ')) {
            enhancedContent = this.enhanceStandardClassScanner(content, scannerName);
        }
        
        // Pattern 2: Function-based scanner
        else if (content.includes('async function') && content.includes('scan')) {
            enhancedContent = this.enhanceFunctionBasedScanner(content, scannerName);
        }
        
        // Pattern 3: Object-based scanner
        else if (content.includes('const scanner = {') || content.includes('module.exports = {')) {
            enhancedContent = this.enhanceObjectBasedScanner(content, scannerName);
        }
        
        // Pattern 4: Express route scanner
        else if (content.includes('app.') && content.includes('router')) {
            enhancedContent = this.enhanceRouteBasedScanner(content, scannerName);
        }
        
        return enhancedContent;
    }
    
    enhanceStandardClassScanner(content, scannerName) {
        const creatorBridgeImport = `const CreatorIntelligenceBridge = require('../integrations/creator_intelligence_bridge');\n`;
        
        // Add import after other requires
        let enhancedContent = content;
        
        // Find the last require statement
        const requireMatches = content.match(/const .* = require\\([^)]+\\);/g);
        if (requireMatches && requireMatches.length > 0) {
            const lastRequire = requireMatches[requireMatches.length - 1];
            enhancedContent = content.replace(lastRequire, lastRequire + '\n' + creatorBridgeImport);
        } else {
            // Add at the beginning
            enhancedContent = creatorBridgeImport + '\n' + content;
        }
        
        // Find class constructor and add creator bridge
        const constructorMatch = enhancedContent.match(/constructor\\s*\\([^)]*\\)\\s*{/);
        if (constructorMatch) {
            const constructorEnd = enhancedContent.indexOf('}', constructorMatch.index);
            const beforeClosing = enhancedContent.substring(0, constructorEnd);
            const afterClosing = enhancedContent.substring(constructorEnd);
            
            const bridgeInit = `\n        // Creator Intelligence Integration\n        this.creatorBridge = new CreatorIntelligenceBridge();\n        this.creator_intelligence_enhanced = true;\n    `;
            
            enhancedContent = beforeClosing + bridgeInit + afterClosing;
        }
        
        // Enhance scan method to trigger creator analysis
        enhancedContent = this.addCreatorAnalysisToScanMethod(enhancedContent, scannerName);
        
        return enhancedContent;
    }
    
    enhanceFunctionBasedScanner(content, scannerName) {
        const creatorBridgeImport = `const CreatorIntelligenceBridge = require('../integrations/creator_intelligence_bridge');\nconst creatorBridge = new CreatorIntelligenceBridge();\n`;
        
        // Add import at the top
        let enhancedContent = creatorBridgeImport + '\n' + content;
        
        // Find main scan function and enhance it
        enhancedContent = this.addCreatorAnalysisToScanMethod(enhancedContent, scannerName);
        
        return enhancedContent;
    }
    
    enhanceObjectBasedScanner(content, scannerName) {
        const creatorBridgeImport = `const CreatorIntelligenceBridge = require('../integrations/creator_intelligence_bridge');\nconst creatorBridge = new CreatorIntelligenceBridge();\n`;
        
        // Add import at the top
        let enhancedContent = creatorBridgeImport + '\n' + content;
        
        // Find scan methods and enhance them
        enhancedContent = this.addCreatorAnalysisToScanMethod(enhancedContent, scannerName);
        
        return enhancedContent;
    }
    
    enhanceRouteBasedScanner(content, scannerName) {
        // For Express route scanners, we need a different approach
        const creatorBridgeImport = `const CreatorIntelligenceBridge = require('../integrations/creator_intelligence_bridge');\nconst creatorBridge = new CreatorIntelligenceBridge();\n`;
        
        let enhancedContent = creatorBridgeImport + '\n' + content;
        
        // Find route handlers that return opportunities
        const routePattern = /(app\\.(get|post|put)\\([^{]+{[^}]+}[^}]*})/g;
        enhancedContent = enhancedContent.replace(routePattern, (match) => {
            return this.enhanceRouteHandler(match, scannerName);
        });
        
        return enhancedContent;
    }
    
    addCreatorAnalysisToScanMethod(content, scannerName) {
        // Find patterns where opportunities are processed or returned
        let enhancedContent = content;
        
        // Pattern 1: opportunities.push(opportunity)
        enhancedContent = enhancedContent.replace(
            /opportunities\\.push\\(([^)]+)\\);/g,
            (match, opportunity) => {
                return `opportunities.push(${opportunity});\n            // Trigger creator analysis\n            this.triggerCreatorAnalysis && this.triggerCreatorAnalysis(${opportunity}, '${scannerName}');`;
            }
        );
        
        // Pattern 2: return opportunities
        enhancedContent = enhancedContent.replace(
            /(return\\s+opportunities;)/g,
            (match) => {
                return `// Trigger creator analysis for all opportunities\n        this.triggerCreatorAnalysisForAll && this.triggerCreatorAnalysisForAll(opportunities, '${scannerName}');\n        ${match}`;
            }
        );
        
        // Pattern 3: Database inserts
        enhancedContent = enhancedContent.replace(
            /(await\\s+db\\.run\\([^)]+\\);)/g,
            (match) => {
                return `${match}\n            // Trigger creator analysis after DB insert\n            this.triggerCreatorAnalysisAfterInsert && this.triggerCreatorAnalysisAfterInsert(opportunity, '${scannerName}');`;
            }
        );
        
        // Add helper methods to class
        if (enhancedContent.includes('class ') && !enhancedContent.includes('triggerCreatorAnalysis(')) {
            const classEndMatch = enhancedContent.match(/}\\s*module\\.exports/);
            if (classEndMatch) {
                const insertPoint = classEndMatch.index;
                const helperMethods = this.generateCreatorAnalysisHelperMethods(scannerName);
                enhancedContent = enhancedContent.substring(0, insertPoint) + helperMethods + enhancedContent.substring(insertPoint);
            }
        }
        
        return enhancedContent;
    }
    
    generateCreatorAnalysisHelperMethods(scannerName) {
        return `
    /**
     * Creator Intelligence Integration Methods
     * Auto-generated by ScannerAutoIntegrator
     */
    
    async triggerCreatorAnalysis(opportunity, scannerName = '${scannerName}') {
        try {
            if (this.creatorBridge) {
                const analysisId = await this.creatorBridge.analyzeOpportunity({
                    ...opportunity,
                    scanner_source: scannerName,
                    discovered_at: new Date().toISOString()
                });
                
                console.log(\`🎯 Triggered creator analysis \${analysisId} for opportunity: \${opportunity.title || opportunity.product_name}\`);
                return analysisId;
            }
        } catch (error) {
            console.error(\`❌ Failed to trigger creator analysis from \${scannerName}:\`, error.message);
        }
        return null;
    }
    
    async triggerCreatorAnalysisForAll(opportunities, scannerName = '${scannerName}') {
        const analysisPromises = opportunities.map(opportunity => 
            this.triggerCreatorAnalysis(opportunity, scannerName)
        );
        
        try {
            const analysisIds = await Promise.all(analysisPromises);
            console.log(\`🎯 Triggered \${analysisIds.filter(id => id).length} creator analyses from \${scannerName}\`);
            return analysisIds;
        } catch (error) {
            console.error(\`❌ Failed to trigger batch creator analysis from \${scannerName}:\`, error.message);
            return [];
        }
    }
    
    async triggerCreatorAnalysisAfterInsert(opportunity, scannerName = '${scannerName}') {
        // Delay slightly to ensure DB transaction is complete
        setTimeout(() => {
            this.triggerCreatorAnalysis(opportunity, scannerName);
        }, 1000);
    }
    
    getCreatorAnalysisStats() {
        return this.creatorBridge ? this.creatorBridge.getStats() : null;
    }

`;
    }
    
    enhanceRouteHandler(routeMatch, scannerName) {
        // Enhance route handlers to trigger creator analysis
        if (routeMatch.includes('opportunities') || routeMatch.includes('scan')) {
            return routeMatch.replace(
                /(res\\.json\\([^)]+\\);)/g,
                (match, jsonResponse) => {
                    return `// Trigger creator analysis\n    if (creatorBridge && opportunities) {\n        opportunities.forEach(opp => creatorBridge.analyzeOpportunity({...opp, scanner_source: '${scannerName}'}));\n    }\n    ${match}`;
                }
            );
        }
        
        return routeMatch;
    }
    
    handleCreatorAnalysisComplete(result) {
        const { analysisId, opportunityData, result: analysisResult } = result;
        
        console.log(`🎉 Creator analysis completed for "${opportunityData.title || opportunityData.product_name}"`);
        console.log(`📊 Found ${analysisResult.creators?.total_found || 0} creators in ${analysisResult.niche?.primary_niche || 'unknown'} niche`);
        console.log(`💡 Success probability: ${Math.round((analysisResult.success_probability || 0) * 100)}%`);
        
        // You could emit events here for the main system to handle
        // For example, updating the database with enhanced opportunity data
    }
    
    async restoreScanner(scannerName) {
        const scannerInfo = this.integratedScanners.get(scannerName);
        if (!scannerInfo) {
            throw new Error(`Scanner ${scannerName} not found in integrated scanners`);
        }
        
        const backupPath = path.join(this.scannersPath, scannerInfo.file + '.backup');
        const originalPath = path.join(this.scannersPath, scannerInfo.file);
        
        try {
            const backupContent = await fs.readFile(backupPath, 'utf8');
            await fs.writeFile(originalPath, backupContent);
            
            this.integratedScanners.delete(scannerName);
            
            console.log(`✅ Restored ${scannerName} scanner from backup`);
            return true;
        } catch (error) {
            console.error(`❌ Failed to restore ${scannerName}:`, error.message);
            return false;
        }
    }
    
    getIntegrationStatus() {
        return {
            integratedScanners: Array.from(this.integratedScanners.keys()),
            totalIntegrated: this.integratedScanners.size,
            bridgeStats: this.bridge.getStats(),
            integrationDetails: Array.from(this.integratedScanners.entries()).map(([name, info]) => ({
                name,
                file: info.file,
                integratedAt: info.integratedAt,
                backupCreated: info.backupCreated
            }))
        };
    }
}

// Auto-start integration when this module is loaded
const autoIntegrator = new ScannerAutoIntegrator();

module.exports = {
    ScannerAutoIntegrator,
    autoIntegrator
};