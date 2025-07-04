#!/bin/bash
# Staging Environment Deployment Script for UX Intelligence Engine
# Version: 1.0
# Purpose: Automated setup and deployment of staging environment

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
STAGING_ENV="staging"
UX_ENGINE_VERSION="v1.0"
DOCKER_COMPOSE_FILE="TEC-code-StagingEnvironment-Setup-v1.yml"
PROJECT_NAME="ux-intelligence-engine"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running. Please start Docker first."
    fi
    
    success "All prerequisites satisfied"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    
    mkdir -p config
    mkdir -p logs
    mkdir -p monitoring/{prometheus,grafana/{dashboards,datasources}}
    mkdir -p sql
    mkdir -p nginx
    mkdir -p ssl
    mkdir -p ab-testing
    mkdir -p analytics
    
    success "Directories created"
}

# Generate configuration files
generate_configs() {
    log "Generating configuration files..."
    
    # A/B Testing Configuration
    cat > config/ab-test-config.json << EOF
{
  "experiment": {
    "name": "ux_intelligence_rollout_v1",
    "version": "1.0",
    "enabled": true,
    "startDate": "$(date -d '+1 day' '+%Y-%m-%d')",
    "endDate": "$(date -d '+28 days' '+%Y-%m-%d')",
    "trafficAllocation": {
      "control": 0.50,
      "testGroupA": 0.25,
      "testGroupB": 0.20,
      "testGroupC": 0.05
    },
    "features": {
      "control": ["baseline_ux"],
      "testGroupA": ["persona_detection", "device_optimization", "intent_recognition", "realtime_adaptation"],
      "testGroupB": ["persona_detection", "device_optimization"],
      "testGroupC": ["device_optimization"]
    }
  },
  "metrics": {
    "primary": ["conversion_rate", "engagement_score", "bounce_rate"],
    "secondary": ["time_to_conversion", "revenue_per_session", "page_depth"]
  },
  "safety": {
    "autoRollback": true,
    "conversionDropThreshold": -15,
    "performanceThreshold": 5000,
    "errorRateThreshold": 2
  }
}
EOF

    # Prometheus Configuration
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "/etc/prometheus/rules/*.yml"

scrape_configs:
  - job_name: 'ux-engine-app'
    static_configs:
      - targets: ['ux-engine-app:3000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'analytics-service'
    static_configs:
      - targets: ['analytics:8080']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'ab-testing-service'
    static_configs:
      - targets: ['ab-testing:8080']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

    # Grafana Datasource Configuration
    cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF

    # Database Initialization Script
    cat > sql/init.sql << EOF
-- UX Analytics Database Schema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table for experiment tracking
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    experiment_group VARCHAR(50),
    persona_type VARCHAR(50),
    device_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metrics table for performance tracking
CREATE TABLE IF NOT EXISTS metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    metric_type VARCHAR(100) NOT NULL,
    metric_value NUMERIC NOT NULL,
    metadata JSONB,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Experiments table for A/B test tracking
CREATE TABLE IF NOT EXISTS experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    config JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_session_id ON users(session_id);
CREATE INDEX IF NOT EXISTS idx_users_experiment_group ON users(experiment_group);
CREATE INDEX IF NOT EXISTS idx_metrics_user_id ON metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_metrics_type_recorded ON metrics(metric_type, recorded_at);

-- Insert initial experiment configuration
INSERT INTO experiments (name, version, config) VALUES 
('ux_intelligence_rollout_v1', '1.0', '{
  "description": "UX Intelligence Engine rollout experiment",
  "traffic_allocation": {
    "control": 0.50,
    "testGroupA": 0.25,
    "testGroupB": 0.20,
    "testGroupC": 0.05
  },
  "success_metrics": ["conversion_rate", "engagement_score", "bounce_rate"],
  "safety_thresholds": {
    "conversion_drop": -15,
    "performance_max": 5000,
    "error_rate_max": 2
  }
}') ON CONFLICT DO NOTHING;
EOF

    # Nginx Configuration
    cat > nginx/staging.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream ux_engine_app {
        server ux-engine-app:3000;
    }

    upstream analytics_service {
        server analytics:8080;
    }

    upstream ab_testing_service {
        server ab-testing:8080;
    }

    server {
        listen 80;
        server_name staging.ux-engine.local;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;

        # Main application
        location / {
            proxy_pass http://ux_engine_app;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # Analytics API
        location /api/analytics/ {
            proxy_pass http://analytics_service/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
        }

        # A/B Testing API
        location /api/experiments/ {
            proxy_pass http://ab_testing_service/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

    # Redis Configuration
    cat > config/redis.conf << EOF
# Redis configuration for staging environment
port 6379
bind 0.0.0.0
protected-mode no
timeout 300
keepalive 60
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
dbfilename staging-dump.rdb
dir /data
EOF

    success "Configuration files generated"
}

# Build and deploy services
deploy_services() {
    log "Building and deploying services..."
    
    # Pull latest images
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME pull --quiet
    
    # Build custom images
    log "Building custom images..."
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME build --no-cache
    
    # Start services
    log "Starting services..."
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME up -d
    
    success "Services deployed"
}

# Wait for services to be ready
wait_for_services() {
    log "Waiting for services to be ready..."
    
    # Wait for main application
    log "Waiting for UX Engine application..."
    for i in {1..30}; do
        if curl -f http://localhost:3000/health &> /dev/null; then
            success "UX Engine application is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            error "UX Engine application failed to start"
        fi
        sleep 5
    done
    
    # Wait for analytics service
    log "Waiting for analytics service..."
    for i in {1..20}; do
        if curl -f http://localhost:8080/health &> /dev/null; then
            success "Analytics service is ready"
            break
        fi
        if [ $i -eq 20 ]; then
            warning "Analytics service may not be ready"
        fi
        sleep 3
    done
    
    # Wait for Prometheus
    log "Waiting for Prometheus..."
    for i in {1..20}; do
        if curl -f http://localhost:9090/-/healthy &> /dev/null; then
            success "Prometheus is ready"
            break
        fi
        if [ $i -eq 20 ]; then
            warning "Prometheus may not be ready"
        fi
        sleep 3
    done
    
    # Wait for Grafana
    log "Waiting for Grafana..."
    for i in {1..20}; do
        if curl -f http://localhost:3001/api/health &> /dev/null; then
            success "Grafana is ready"
            break
        fi
        if [ $i -eq 20 ]; then
            warning "Grafana may not be ready"
        fi
        sleep 3
    done
}

# Run health checks
run_health_checks() {
    log "Running health checks..."
    
    # Check service status
    local services=(
        "ux-engine-app:3000:/health"
        "analytics:8080:/health"
        "ab-testing:8081:/health"
        "prometheus:9090/-/healthy"
        "grafana:3001:/api/health"
    )
    
    for service in "${services[@]}"; do
        IFS=':' read -r name port path <<< "$service"
        if curl -f "http://localhost:$port$path" &> /dev/null; then
            success "$name health check passed"
        else
            warning "$name health check failed"
        fi
    done
    
    # Check database connectivity
    if docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME exec -T postgres pg_isready -U analytics &> /dev/null; then
        success "PostgreSQL connectivity check passed"
    else
        warning "PostgreSQL connectivity check failed"
    fi
    
    # Check Redis connectivity
    if docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME exec -T redis redis-cli ping | grep -q PONG; then
        success "Redis connectivity check passed"
    else
        warning "Redis connectivity check failed"
    fi
}

# Display deployment summary
display_summary() {
    log "Deployment Summary"
    echo
    echo -e "${GREEN}=== UX Intelligence Engine Staging Environment ===${NC}"
    echo
    echo -e "${BLUE}Services:${NC}"
    echo "  • Main Application:  http://localhost:3000"
    echo "  • Analytics API:     http://localhost:8080"
    echo "  • A/B Testing API:   http://localhost:8081"
    echo "  • Prometheus:        http://localhost:9090"
    echo "  • Grafana:           http://localhost:3001 (admin/admin123)"
    echo "  • Load Balancer:     http://localhost:80"
    echo
    echo -e "${BLUE}Database:${NC}"
    echo "  • PostgreSQL:        localhost:5432 (analytics/password)"
    echo "  • Redis:             localhost:6379"
    echo
    echo -e "${BLUE}Monitoring:${NC}"
    echo "  • Logs:              docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME logs -f"
    echo "  • Status:            docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME ps"
    echo
    echo -e "${BLUE}Management:${NC}"
    echo "  • Stop:              docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME down"
    echo "  • Restart:           docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME restart"
    echo "  • Update:            ./$(basename $0) --update"
    echo
    echo -e "${GREEN}Staging environment is ready for testing!${NC}"
}

# Cleanup function
cleanup() {
    log "Cleaning up staging environment..."
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME down -v
    docker system prune -f
    success "Cleanup completed"
}

# Update function
update_deployment() {
    log "Updating staging deployment..."
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME pull
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME build --no-cache
    docker-compose -f $DOCKER_COMPOSE_FILE -p $PROJECT_NAME up -d
    success "Update completed"
}

# Main execution
main() {
    case "${1:-deploy}" in
        "deploy")
            log "Starting UX Intelligence Engine staging deployment..."
            check_prerequisites
            create_directories
            generate_configs
            deploy_services
            wait_for_services
            run_health_checks
            display_summary
            ;;
        "--cleanup")
            cleanup
            ;;
        "--update")
            update_deployment
            ;;
        "--health")
            run_health_checks
            ;;
        "--help")
            echo "Usage: $0 [deploy|--cleanup|--update|--health|--help]"
            echo "  deploy    - Deploy staging environment (default)"
            echo "  --cleanup - Remove staging environment and volumes"
            echo "  --update  - Update deployment with latest changes"
            echo "  --health  - Run health checks on existing deployment"
            echo "  --help    - Show this help message"
            ;;
        *)
            error "Unknown option: $1. Use --help for usage information."
            ;;
    esac
}

# Execute main function with all arguments
main "$@"