# 🎯 Intelligence System

An advanced **AI-Powered Intelligence System** that automatically discovers profitable marketing opportunities and analyzes successful creators across any niche. Features universal creator intelligence, viral pattern extraction, and automated opportunity assessment.

## 🚀 System Architecture

### **Core Components**
- **Basic Intelligence System** (`index.js`) - Core opportunity scanning and AI research
- **Enhanced Creator Intelligence** (`main_with_creator_intelligence.js`) - Advanced creator analysis and pattern extraction
- **Production Launcher** (`start_enhanced_system.js`) - Full system orchestration and monitoring

### **Key Features**
- ✨ **Universal Creator Intelligence** - Niche-agnostic creator discovery
- 🎯 **Automatic Opportunity Scanning** - Multi-platform opportunity detection
- 📊 **Viral Pattern Extraction** - AI-powered content strategy analysis
- 🔄 **Real-time Integration** - N8N workflow automation
- 💰 **Success Probability Scoring** - AI-driven opportunity assessment
- 🌐 **RESTful API** - Complete programmatic access
- 🧠 **AI Research Integration** - Python-based AI analysis pipeline

## 📁 Project Structure

```
intelligence-system/
├── core/
│   └── opportunity-scanner.js         # Central orchestration engine
├── scanners/
│   ├── affiliate-scanner.js           # Multi-network affiliate API scanner
│   ├── social-trend-scanner.js        # Social media trend analysis
│   ├── timing-optimizer.js            # Market timing optimization
│   └── seasonal-scanner.js            # Seasonal opportunity detection
├── analyzers/
│   ├── profitability-analyzer.js      # ROI and profitability analysis
│   └── trend-velocity-analyzer.js     # Trend momentum and velocity
├── strategies/
│   └── campaign-strategies.js         # Automated campaign strategy generation
├── databases/
│   ├── schemas.sql                    # Complete database schema
│   └── seed-data.json                 # Initial configuration data
├── config/
│   ├── api-config.js                  # API configuration management
│   └── database-config.js             # Database setup and management
└── tests/
    └── scanner.test.js                # Test suite
```

## 🛠️ Quick Start

### Prerequisites
Before starting the system, ensure you have:

- **Node.js 16+** - Check with `node --version`
- **Python 3.8+** - For AI analysis components
- **SQLite3** - Database access
- **API Keys** (optional but recommended):
  - `OPENAI_API_KEY` - For enhanced AI analysis
  - `YOUTUBE_API_KEY` - For YouTube creator analysis
  - `CLAUDE_API_KEY` - Alternative AI provider

### Installation
```bash
# Install dependencies
npm install

# Optional: Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 🚀 **STARTUP PROCEDURES**

### **Option 1: Enhanced System (Recommended)**
```bash
# Start the full enhanced system with creator intelligence
npm start
```
or
```bash
node start_enhanced_system.js
```

**What this starts:**
- Full creator intelligence pipeline
- All opportunity scanners integrated
- Health monitoring and auto-recovery
- Production-ready configuration
- Runs on port **3001** by default

### **Option 2: Basic System (Development/Testing)**
```bash
# Start basic intelligence system only
npm run start:basic
```
or
```bash
node index.js
```

**What this starts:**
- Core opportunity scanning
- Basic AI research integration
- Simplified API endpoints
- Runs on port **3000** by default

### **Option 3: Manual Enhanced Launch**
```bash
# Launch the enhanced system with full initialization
node main_with_creator_intelligence.js
```

**Important:** Update your package.json scripts:
```json
{
  "scripts": {
    "start": "node start_enhanced_system.js",
    "start:basic": "node index.js",
    "start:enhanced": "node start_enhanced_system.js"
  }
}
```

## ⚙️ Configuration

## 🔧 Enhanced System Startup Sequence

When you run `npm start`, the system performs these steps:

### 1. **Prerequisites Check**
- Node.js version validation
- Python environment verification
- Required packages verification
- Database access confirmation
- API key validation (with warnings for missing keys)

### 2. **Environment Initialization**
- Creates necessary directories (`databases/`, `logs/`, `exports/`, `temp/`)
- Sets default environment variables
- Initializes database schemas

### 3. **System Components Launch**
- Starts Enhanced Intelligence System
- Initializes Creator Intelligence Bridge
- Sets up opportunity scanning schedules
- Connects to Python AI analysis services

### 4. **Health Monitoring**
- Starts system health checks (every 30 seconds)
- Begins statistics logging (every 5 minutes)
- Sets up graceful shutdown handlers

### Expected Console Output
```
🚀 Launching Enhanced Intelligence System with Universal Creator Intelligence...

🔍 Checking prerequisites...
  ✅ Node.js
  ✅ Python Environment
  ✅ Required Packages
  ✅ Database Access
  ✅ API Keys
✅ All prerequisites met

╔══════════════════════════════════════════════════════════════╗
║        🚀 ENHANCED INTELLIGENCE SYSTEM v2.0                  ║
║                                                              ║
║  ✨ Universal Creator Intelligence - NICHE AGNOSTIC         ║
║  🎯 Automatic Creator Discovery for ANY Opportunity         ║
║  📊 Real-time Pattern Extraction & Analysis                 ║
║  🔄 Fully Integrated with Existing Scanners                ║
║                                                              ║
║  💰 Finding €3.4M+ in opportunities with AI creators!        ║
╚══════════════════════════════════════════════════════════════╝

✅ Enhanced Intelligence System is fully operational!
```

## ⚙️ Configuration

### Environment Variables
```bash
# Core Configuration
NODE_ENV=production
PORT=3001

# AI Services (Optional but recommended)
OPENAI_API_KEY=your_openai_key_here
CLAUDE_API_KEY=your_claude_key_here
YOUTUBE_API_KEY=your_youtube_key_here

# Python Environment
PYTHON_PATH=python3
PYTHON_AI_URL=http://localhost:8000

# Database
DATABASE_PATH=./databases/
```

### API Configuration

The system automatically loads configuration from:
1. Environment variables (recommended for production)
2. `config/api-credentials.json` file
3. Default fallback values

Generate a configuration template:

```javascript
const { ApiConfig } = require('./config/api-config');
const config = new ApiConfig();
console.log(config.createConfigTemplate());
```

## 🎯 Usage Examples

### Basic Usage

```javascript
const { OpportunityScanner } = require('./core/opportunity-scanner');
const { AffiliateScanner } = require('./scanners/affiliate-scanner');
const { SocialTrendScanner } = require('./scanners/social-trend-scanner');

// Initialize the system
const scanner = new OpportunityScanner({
    scanInterval: 300000, // 5 minutes
    minScore: 70
});

// Register scanners
scanner.registerScanner('affiliate', new AffiliateScanner());
scanner.registerScanner('social', new SocialTrendScanner());

// Start scanning
await scanner.startScanning();

// Listen for opportunities
scanner.on('opportunitiesFound', (opportunities) => {
    console.log(`Found ${opportunities.length} new opportunities`);
    opportunities.forEach(opp => {
        console.log(`${opp.title} - Score: ${opp.score}`);
    });
});
```

### Advanced Analysis

```javascript
const { ProfitabilityAnalyzer } = require('./analyzers/profitability-analyzer');
const { TrendVelocityAnalyzer } = require('./analyzers/trend-velocity-analyzer');
const { CampaignStrategies } = require('./strategies/campaign-strategies');

// Analyze opportunity profitability
const profitabilityAnalyzer = new ProfitabilityAnalyzer();
const profitabilityData = await profitabilityAnalyzer.analyze(opportunity);

// Analyze trend velocity
const velocityAnalyzer = new TrendVelocityAnalyzer();
const velocityData = await velocityAnalyzer.analyze(opportunity);

// Generate campaign strategy
const strategist = new CampaignStrategies();
const strategy = await strategist.generateStrategy(
    opportunity, 
    profitabilityData, 
    velocityData,
    { budget: 5000 }
);

console.log('Campaign Strategy:', strategy);
```

### Database Operations

```javascript
const { DatabaseConfig } = require('./config/database-config');

// Initialize database
const db = new DatabaseConfig();

// Query opportunities
const highScoreOpportunities = await db.query(
    'SELECT * FROM opportunities WHERE score >= ? ORDER BY score DESC',
    [80]
);

// Get system statistics
const stats = await db.getStats();
console.log('System Stats:', stats);
```

## 📡 API Reference

### Enhanced System Endpoints (Port 3001)

#### Core Opportunities
```bash
# Get enhanced opportunities with creator analysis
GET /api/opportunities/enhanced
Query params: ?limit=50&niche=crypto&platform=youtube&min_success_probability=0.7

# Get creator analysis for specific opportunity
GET /api/opportunities/{id}/creators

# Trigger manual creator analysis
POST /api/opportunities/{id}/analyze-creators
```

#### Creator Intelligence
```bash
# Get top creators across all niches
GET /api/creators/top
Query params: ?limit=100&platform=youtube&niche=fitness&min_followers=1000

# Get discovered niches
GET /api/niches

# Get viral patterns
GET /api/patterns/viral
Query params: ?pattern_type=hook&min_effectiveness=0.7
```

#### System Management
```bash
# Enhanced system statistics
GET /api/stats/enhanced

# Integration status
GET /api/integration/status

# Health check
GET /health
```

### Basic System Endpoints (Port 3000)
```bash
# Basic opportunities
GET /api/opportunities

# System statistics
GET /api/stats

# Manual scan trigger
POST /api/scan

# AI research
POST /api/ai/research
```

## ⚠️ Troubleshooting

### Common Issues

#### 1. "Python environment check failed"
```bash
# Ensure Python 3.8+ is installed and accessible
python3 --version

# Install required Python packages
pip3 install asyncio sqlite3
```

#### 2. "Port already in use"
```bash
# Check what's running on the ports
lsof -i :3000
lsof -i :3001

# Kill existing processes or change port
export PORT=3002
npm start
```

#### 3. "Missing required package"
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### 4. "Database access failed"
```bash
# Ensure write permissions
chmod 755 ./databases/

# Or let the system create the directory
mkdir -p ./databases
```

#### 5. "AI enhancement failed"
- System will continue without AI features
- Check your `OPENAI_API_KEY` environment variable
- Verify internet connectivity for API calls

### System Recovery
The enhanced system includes automatic recovery mechanisms:
- **Health Monitoring**: Detects and reports system issues
- **Graceful Shutdown**: Handles SIGINT/SIGTERM properly
- **Error Handling**: Continues operation despite component failures
- **Process Management**: Restarts failed components automatically

### System Behavior
- **Automatic Scanning**: Every 30 minutes (quick) and 6 hours (full)
- **Creator Analysis**: Triggered automatically for new opportunities
- **Data Retention**: 30 days for pipeline executions, permanent for opportunities
- **Concurrent Processing**: Up to 3 simultaneous creator analyses

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Test Structure

```javascript
// Example test
const { OpportunityScanner } = require('../core/opportunity-scanner');

describe('OpportunityScanner', () => {
    test('should register scanners correctly', () => {
        const scanner = new OpportunityScanner();
        const mockScanner = { scan: jest.fn() };
        
        scanner.registerScanner('test', mockScanner);
        expect(scanner.scanners.has('test')).toBe(true);
    });
});
```

## 🔧 API Endpoints

When running as a service, the system exposes REST endpoints:

```bash
# Get all opportunities
GET /api/opportunities

# Get high-score opportunities
GET /api/opportunities?min_score=80

# Get opportunities by source
GET /api/opportunities?source=affiliate_scanner

# Trigger manual scan
POST /api/scan

# Get system stats
GET /api/stats

# Health check
GET /api/health
```

## 🚀 System Status Indicators

### Health Check
```bash
# Check system status
curl http://localhost:3001/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-07-02T...",
  "uptime": 1234.567,
  "creator_intelligence": "active",
  "database_status": "connected"
}
```

### Quick Start Guide (Displayed on Startup)
After successful startup, the system displays:

```
🎯 QUICK START GUIDE:
📡 API Endpoints:
   • All opportunities: http://localhost:3001/api/opportunities/enhanced
   • Creator analysis:  http://localhost:3001/api/opportunities/{id}/creators
   • Top creators:      http://localhost:3001/api/creators/top
   • Viral patterns:    http://localhost:3001/api/patterns/viral
   • System stats:      http://localhost:3001/api/stats/enhanced

💡 Example Usage:
   curl http://localhost:3001/api/opportunities/enhanced?limit=10&min_success_probability=0.7

📊 The system is now automatically:
   ✅ Finding opportunities across all scanners
   ✅ Detecting niches automatically (German + International)
   ✅ Discovering creators in ANY niche
   ✅ Extracting viral patterns and strategies
   ✅ Generating success probability scores
   ✅ Creating implementation plans

🚀 NO MANUAL CONFIGURATION NEEDED - Everything is automatic!
```

## 📈 Performance Optimization

### Rate Limiting
- Automatic rate limiting per API provider
- Configurable request throttling
- Smart caching with TTL

### Database Optimization
- Indexed queries for fast lookups
- WAL mode for concurrent access
- Automatic VACUUM and ANALYZE

### Memory Management
- Connection pooling
- Garbage collection optimization
- Memory usage monitoring

## 🔐 Security

### API Security
- API key validation
- Request signing (where supported)
- Rate limiting protection

### Data Security
- No sensitive data in logs
- Encrypted credential storage option
- Database backup encryption

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Run linting before commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Important Notes

### Getting Help
1. Check this README for common issues
2. Review the console output for specific error messages
3. Ensure all prerequisites are met
4. Check the `/health` endpoint for system status

### System Status
- **Healthy**: All components operational
- **Degraded**: Some AI features unavailable
- **Error**: Core functionality affected

### File Structure Issues (Fixed in v2.0)
⚠️ **Important**: If you encounter import errors, ensure:
1. Use `npm start` (points to `start_enhanced_system.js`)
2. Update package.json scripts as shown above
3. The enhanced system properly imports from `index.js` not `main.js`

### Key Benefits
- **Automatic Operation**: No manual configuration required
- **Graceful Degradation**: Continues working even if AI services are unavailable  
- **Multi-Platform**: Works with any affiliate network or social platform
- **Universal Intelligence**: Discovers creators in ANY niche automatically
- **Production Ready**: Built-in monitoring, health checks, and recovery

---

**🚀 Enhanced Intelligence System v2.0 - AI-Powered Creator Discovery**

*The system is designed to gracefully degrade when external services are unavailable while maintaining core opportunity scanning functionality.*