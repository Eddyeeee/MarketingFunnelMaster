# 🎯 Marketing Funnel Intelligence System

An advanced **Opportunistic Intelligence System** that automatically hunts profitable marketing opportunities from affiliate APIs, social trends, and seasonal events. Built for the MarketingFunnelMaster ecosystem.

## 🚀 Features

### **Real-Time Opportunity Detection**
- **Affiliate Scanner** - Multi-network API integration (Digistore24, ClickBank, ShareASale, CJ Affiliate, Impact)
- **Social Trend Scanner** - Real-time analysis across Twitter, Instagram, TikTok, YouTube, Reddit
- **Seasonal Scanner** - Holiday, cultural, and marketing calendar opportunities
- **Timing Optimizer** - Market timing and global activity analysis

### **Advanced Analytics**
- **Profitability Analyzer** - ROI calculation, risk assessment, market positioning
- **Trend Velocity Analyzer** - Momentum analysis, volatility metrics, predictive scoring
- **Campaign Strategies** - Automated strategy generation based on opportunity profiles

### **Intelligence & Automation**
- **Intelligent Scoring** - Multi-factor scoring based on commission rates, trend velocity, timing
- **N8n Integration** - Ready-to-use workflow automation
- **Real-time Monitoring** - Continuous scanning with configurable intervals
- **Database Management** - Complete SQLite schema with automated backups

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

## 🛠️ Installation

### Prerequisites
- Node.js >= 16.0.0
- npm >= 8.0.0
- SQLite3

### Quick Setup

```bash
# Clone or copy the intelligence-system folder
cd intelligence-system

# Install dependencies
npm install

# Initialize database and configuration
npm run setup

# Start the system
npm start
```

### Manual Setup

```bash
# Install dependencies
npm install

# Initialize database
npm run init-db

# Validate configuration
npm run validate-config

# Run health check
npm run health-check
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Affiliate Networks
DIGISTORE24_API_KEY=your_digistore24_key
CLICKBANK_API_KEY=your_clickbank_key
SHAREASALE_API_KEY=your_shareasale_key

# Social Media APIs
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
YOUTUBE_API_KEY=your_youtube_api_key
INSTAGRAM_ACCESS_TOKEN=your_instagram_token

# N8n Automation
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/intelligence

# Database
DATABASE_PATH=./databases/intelligence.db
DATABASE_BACKUP_PATH=./databases/backups/
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

## 🔗 N8n Integration

The system includes pre-configured N8n workflows for automation:

### Workflow Types
- **High Score Opportunity Alert** - Triggers on opportunities scoring 85+
- **Affiliate Product Notification** - New affiliate products with high commissions
- **Social Trend Alert** - Viral trends with high engagement
- **Seasonal Opportunity Prep** - Upcoming seasonal events

### Webhook Configuration

```json
{
  "workflow_name": "High Score Opportunity Alert",
  "trigger_type": "high_score",
  "min_score": 85,
  "webhook_url": "https://your-n8n.com/webhook/high-score-alert",
  "trigger_conditions": {
    "score_threshold": 85,
    "max_age_hours": 2,
    "exclude_expired": true
  }
}
```

## 📊 Monitoring & Analytics

### Built-in Dashboards

```bash
# View system health
npm run health-check

# Export opportunities data
npm run export-data

# Create database backup
npm run backup-db
```

### Key Metrics

The system tracks:
- **Opportunity Discovery Rate** - New opportunities per hour
- **Scanner Performance** - Success rate and response times
- **Profitability Metrics** - Average ROI, profit margins
- **Trend Analysis** - Velocity scores, momentum indicators

### Database Views

Pre-built views for common queries:
- `high_score_opportunities` - Opportunities scoring 80+
- `recent_opportunities` - Last 7 days of discoveries
- `scanner_summary` - Performance summary by scanner

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

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production
```bash
# Install production dependencies only
npm ci --only=production

# Start with PM2 (recommended)
pm2 start ecosystem.config.js

# Or use npm
npm start
```

### Docker Deployment

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
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

## 🆘 Support

- **Documentation**: [Full API Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/marketing-funnel-intelligence/issues)
- **Discord**: [Join our community](https://discord.gg/your-invite)

## 🎉 Acknowledgments

- Built for the MarketingFunnelMaster ecosystem
- Inspired by modern business intelligence practices
- Thanks to all API providers for their excellent documentation

---

**Made with ❤️ for profitable marketing automation**

*Transform your marketing with intelligent opportunity detection*