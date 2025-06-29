#!/bin/bash

# ========================================
# MULTI-PRODUCT DEPLOYMENT SCRIPT
# ========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PRODUCT_ID=${1:-qmoney}
DEPLOYMENT_TYPE=${2:-vercel}
ENVIRONMENT=${3:-production}

# Product configurations
declare -A PRODUCTS=(
    ["qmoney"]="Q-Money"
    ["remotecash"]="Remote Cash Flow"
    ["cryptoflow"]="Crypto Flow Master"
    ["affiliatepro"]="Affiliate Pro"
)

# Validate product
if [[ ! ${PRODUCTS[$PRODUCT_ID]} ]]; then
    echo -e "${RED}❌ Invalid product ID: $PRODUCT_ID${NC}"
    echo -e "${YELLOW}Available products:${NC}"
    for key in "${!PRODUCTS[@]}"; do
        echo -e "  - $key: ${PRODUCTS[$key]}"
    done
    exit 1
fi

echo -e "${BLUE}🚀 Starting deployment for ${PRODUCTS[$PRODUCT_ID]} ($PRODUCT_ID)${NC}"
echo -e "${BLUE}📦 Deployment type: $DEPLOYMENT_TYPE${NC}"
echo -e "${BLUE}🌍 Environment: $ENVIRONMENT${NC}"

# ========================================
# PRE-DEPLOYMENT CHECKS
# ========================================

echo -e "${YELLOW}🔍 Running pre-deployment checks...${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

# Check if .env.production exists
if [[ ! -f ".env.production" ]]; then
    echo -e "${YELLOW}⚠️  .env.production not found, creating from template...${NC}"
    cp env.production.example .env.production
    echo -e "${YELLOW}⚠️  Please update .env.production with your actual keys${NC}"
fi

# ========================================
# BUILD PROCESS
# ========================================

echo -e "${YELLOW}🔨 Building application...${NC}"

# Set product environment variable
export PRODUCT_ID=$PRODUCT_ID

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
npm ci --production=false

# Run tests
echo -e "${BLUE}🧪 Running tests...${NC}"
npm test

# Build application
echo -e "${BLUE}🔨 Building for production...${NC}"
npm run build

# ========================================
# DEPLOYMENT STRATEGIES
# ========================================

case $DEPLOYMENT_TYPE in
    "vercel")
        deploy_vercel
        ;;
    "netlify")
        deploy_netlify
        ;;
    "docker")
        deploy_docker
        ;;
    "manual")
        deploy_manual
        ;;
    *)
        echo -e "${RED}❌ Unknown deployment type: $DEPLOYMENT_TYPE${NC}"
        echo -e "${YELLOW}Available types: vercel, netlify, docker, manual${NC}"
        exit 1
        ;;
esac

# ========================================
# DEPLOYMENT FUNCTIONS
# ========================================

deploy_vercel() {
    echo -e "${BLUE}🚀 Deploying to Vercel...${NC}"
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo -e "${YELLOW}📦 Installing Vercel CLI...${NC}"
        npm install -g vercel
    fi
    
    # Create vercel.json if it doesn't exist
    if [[ ! -f "vercel.json" ]]; then
        cat > vercel.json << EOF
{
  "version": 2,
  "builds": [
    {
      "src": "server/index.ts",
      "use": "@vercel/node"
    },
    {
      "src": "client/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "client/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "server/index.ts"
    },
    {
      "src": "/(.*)",
      "dest": "client/dist/\$1"
    }
  ],
  "env": {
    "PRODUCT_ID": "$PRODUCT_ID",
    "NODE_ENV": "production"
  }
}
EOF
    fi
    
    # Deploy to Vercel
    vercel --prod --confirm
}

deploy_netlify() {
    echo -e "${BLUE}🚀 Deploying to Netlify...${NC}"
    
    # Check if Netlify CLI is installed
    if ! command -v netlify &> /dev/null; then
        echo -e "${YELLOW}📦 Installing Netlify CLI...${NC}"
        npm install -g netlify-cli
    fi
    
    # Create netlify.toml if it doesn't exist
    if [[ ! -f "netlify.toml" ]]; then
        cat > netlify.toml << EOF
[build]
  publish = "client/dist"
  command = "npm run build:client"

[build.environment]
  PRODUCT_ID = "$PRODUCT_ID"
  NODE_ENV = "production"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
    fi
    
    # Deploy to Netlify
    netlify deploy --prod --dir=client/dist
}

deploy_docker() {
    echo -e "${BLUE}🐳 Deploying with Docker...${NC}"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        exit 1
    fi
    
    # Build Docker image
    echo -e "${BLUE}🔨 Building Docker image...${NC}"
    docker build -t marketing-funnel-$PRODUCT_ID .
    
    # Run Docker container
    echo -e "${BLUE}🚀 Starting Docker container...${NC}"
    docker run -d \
        --name marketing-funnel-$PRODUCT_ID \
        -p 3000:3000 \
        -e PRODUCT_ID=$PRODUCT_ID \
        -e NODE_ENV=production \
        --env-file .env.production \
        marketing-funnel-$PRODUCT_ID
}

deploy_manual() {
    echo -e "${BLUE}📁 Manual deployment preparation...${NC}"
    
    # Create deployment package
    echo -e "${BLUE}📦 Creating deployment package...${NC}"
    mkdir -p deployment/$PRODUCT_ID
    
    # Copy necessary files
    cp -r client/dist deployment/$PRODUCT_ID/
    cp -r server deployment/$PRODUCT_ID/
    cp package.json deployment/$PRODUCT_ID/
    cp .env.production deployment/$PRODUCT_ID/.env
    cp config/products.json deployment/$PRODUCT_ID/
    
    # Create startup script
    cat > deployment/$PRODUCT_ID/start.sh << EOF
#!/bin/bash
export PRODUCT_ID=$PRODUCT_ID
export NODE_ENV=production
npm install --production
npm run start:prod
EOF
    chmod +x deployment/$PRODUCT_ID/start.sh
    
    echo -e "${GREEN}✅ Deployment package created in deployment/$PRODUCT_ID/${NC}"
    echo -e "${YELLOW}📋 Manual deployment steps:${NC}"
    echo -e "  1. Upload deployment/$PRODUCT_ID/ to your server"
    echo -e "  2. Run: cd deployment/$PRODUCT_ID && ./start.sh"
    echo -e "  3. Configure your domain to point to the server"
}

# ========================================
# POST-DEPLOYMENT
# ========================================

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${BLUE}🎉 ${PRODUCTS[$PRODUCT_ID]} is now live!${NC}"

# Display deployment info
case $DEPLOYMENT_TYPE in
    "vercel")
        echo -e "${YELLOW}🌐 Your app should be available at: https://your-project.vercel.app${NC}"
        ;;
    "netlify")
        echo -e "${YELLOW}🌐 Your app should be available at: https://your-site.netlify.app${NC}"
        ;;
    "docker")
        echo -e "${YELLOW}🌐 Your app should be available at: http://localhost:3000${NC}"
        ;;
    "manual")
        echo -e "${YELLOW}🌐 Upload the deployment package to your server${NC}"
        ;;
esac

echo -e "${BLUE}📊 Next steps:${NC}"
echo -e "  1. Configure your domain"
echo -e "  2. Set up SSL certificate"
echo -e "  3. Configure analytics tracking"
echo -e "  4. Test the complete funnel"
echo -e "  5. Start your marketing campaigns"

echo -e "${GREEN}🎯 Ready to scale with ${PRODUCTS[$PRODUCT_ID]}!${NC}" 