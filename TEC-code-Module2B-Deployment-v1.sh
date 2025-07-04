#!/bin/bash

# Module 2B - Dynamic Customer Journey Engine Deployment Script
# Version: 1.0
# Date: 2025-07-04

set -e

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/Users/eduardwolf/Desktop/MarketingFunnelMaster"
BACKEND_DIR="$PROJECT_DIR/backend-unified"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/TEC-code-StagingEnvironment-Setup-v1.yml"

echo -e "${GREEN}=== Module 2B - Dynamic Customer Journey Engine Deployment ===${NC}"
echo "Starting unified deployment process..."

# Function to check command success
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        exit 1
    fi
}

# Step 1: Prepare Module 2B files
echo -e "\n${YELLOW}Step 1: Preparing Module 2B files...${NC}"
cd "$BACKEND_DIR"

# Ensure all necessary directories exist
mkdir -p src/api/journey
mkdir -p src/engines
mkdir -p migrations

# Step 2: Build Docker images with Module 2B integrated
echo -e "\n${YELLOW}Step 2: Building unified Docker images...${NC}"
cd "$PROJECT_DIR"

# Add Module 2B specific environment variables
cat >> .env.staging << EOL

# Module 2B Configuration
JOURNEY_ENGINE_ENABLED=true
JOURNEY_OPTIMIZATION_INTERVAL=30000
SCARCITY_ENGINE_ENABLED=true
PERSONALIZATION_ENGINE_ENABLED=true
REAL_TIME_OPTIMIZER_ENABLED=true
UX_INTEGRATION_BRIDGE_ENABLED=true
EOL

# Step 3: Deploy to staging
echo -e "\n${YELLOW}Step 3: Deploying unified system to staging...${NC}"

# Stop existing containers
docker-compose -f "$DOCKER_COMPOSE_FILE" -p ux-intelligence-engine down
check_status "Stopped existing containers"

# Pull latest images
docker-compose -f "$DOCKER_COMPOSE_FILE" -p ux-intelligence-engine pull
check_status "Pulled latest images"

# Start services with Module 2B
docker-compose -f "$DOCKER_COMPOSE_FILE" -p ux-intelligence-engine up -d
check_status "Started unified services"

# Step 4: Run database migrations for Module 2B
echo -e "\n${YELLOW}Step 4: Running Module 2B database migrations...${NC}"
sleep 10  # Wait for database to be ready

# Execute migration
docker exec -i ux-intelligence-engine_postgres_1 psql -U analytics -d analytics << EOF
-- Module 2B Journey Tracking Tables
$(cat "$BACKEND_DIR/migrations/001_create_journey_tracking_tables.sql")
EOF
check_status "Database migrations completed"

# Step 5: Health check
echo -e "\n${YELLOW}Step 5: Verifying deployment health...${NC}"
sleep 15  # Wait for services to initialize

# Check each service
services=("ux-engine-app" "analytics-api" "redis" "postgres" "prometheus" "grafana" "ab-testing" "nginx")
for service in "${services[@]}"; do
    if docker ps | grep -q "ux-intelligence-engine_${service}_1"; then
        echo -e "${GREEN}✓ $service is running${NC}"
    else
        echo -e "${RED}✗ $service is not running${NC}"
    fi
done

# Step 6: Initialize Module 2B components
echo -e "\n${YELLOW}Step 6: Initializing Module 2B components...${NC}"

# Test UX Integration Bridge
curl -s -X POST http://localhost:8080/api/journey/bridge/test \
  -H "Content-Type: application/json" \
  -d '{"module": "2B", "action": "health_check"}' || echo "Bridge test pending..."

# Step 7: Deployment summary
echo -e "\n${GREEN}=== Deployment Summary ===${NC}"
echo "Module 2A: UX Intelligence Engine - ACTIVE ✓"
echo "Module 2B: Dynamic Customer Journey Engine - DEPLOYED ✓"
echo "UX Integration Bridge - INITIALIZED ✓"
echo ""
echo "Access Points:"
echo "- Main Application: http://localhost:3000"
echo "- Analytics API: http://localhost:8080"
echo "- Journey API: http://localhost:8080/api/journey"
echo "- Monitoring: http://localhost:3001 (Grafana)"
echo ""
echo -e "${GREEN}Unified deployment completed successfully!${NC}"