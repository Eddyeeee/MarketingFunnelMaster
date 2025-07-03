#!/bin/bash

# 🚀 Multi-Site Vercel Deployment Script
# Marketing Funnel Master - Automated Deployment Pipeline

set -e  # Exit on any error

# ===== CONFIGURATION =====
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="$PROJECT_ROOT/logs/deployment"
LOG_FILE="$LOG_DIR/deploy_${TIMESTAMP}.log"

# Products to deploy
PRODUCTS=(qmoney remotecash cryptoflow affiliatepro)
ENVIRONMENTS=(staging production)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ===== UTILITY FUNCTIONS =====
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# ===== SETUP FUNCTIONS =====
setup_environment() {
    log "Setting up deployment environment..."
    
    # Create log directory
    mkdir -p "$LOG_DIR"
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        error "Vercel CLI is not installed. Please install it with: npm install -g vercel"
        exit 1
    fi
    
    # Check if logged in to Vercel
    if ! vercel whoami &> /dev/null; then
        error "Not logged in to Vercel. Please run: vercel login"
        exit 1
    fi
    
    # Check if all required environment variables are set
    if [[ -z "$VERCEL_TOKEN" ]]; then
        warning "VERCEL_TOKEN not set. Using interactive login."
    fi
    
    success "Environment setup complete"
}

# ===== VALIDATION FUNCTIONS =====
validate_build() {
    local product=$1
    log "Validating build for $product..."
    
    # Check if build directory exists
    if [[ ! -d "$PROJECT_ROOT/dist" ]]; then
        error "Build directory not found for $product"
        return 1
    fi
    
    # Check if index.html exists
    if [[ ! -f "$PROJECT_ROOT/dist/index.html" ]]; then
        error "index.html not found in build directory for $product"
        return 1
    fi
    
    # Check build size
    local build_size=$(du -sh "$PROJECT_ROOT/dist" | cut -f1)
    log "Build size for $product: $build_size"
    
    # Basic validation - ensure build is not empty
    local file_count=$(find "$PROJECT_ROOT/dist" -type f | wc -l)
    if [[ $file_count -lt 5 ]]; then
        error "Build appears to be incomplete for $product (only $file_count files)"
        return 1
    fi
    
    success "Build validation passed for $product"
    return 0
}

# ===== BUILD FUNCTIONS =====
build_product() {
    local product=$1
    log "Building $product..."
    
    cd "$PROJECT_ROOT"
    
    # Set environment variables for the build
    export PRODUCT_ID="$product"
    export NODE_ENV="production"
    
    # Clean previous build
    rm -rf dist/
    
    # Build the product
    if npm run build:$product; then
        success "Build completed for $product"
        return 0
    else
        error "Build failed for $product"
        return 1
    fi
}

# ===== DEPLOYMENT FUNCTIONS =====
deploy_to_vercel() {
    local product=$1
    local environment=$2
    local config_file="$PROJECT_ROOT/vercel-configs/$product.json"
    
    log "Deploying $product to $environment..."
    
    # Check if config file exists
    if [[ ! -f "$config_file" ]]; then
        error "Configuration file not found: $config_file"
        return 1
    fi
    
    # Set deployment flags based on environment
    local deploy_flags=""
    if [[ "$environment" == "production" ]]; then
        deploy_flags="--prod"
    fi
    
    # Deploy to Vercel
    cd "$PROJECT_ROOT"
    
    # Use specific configuration file
    cp "$config_file" vercel.json
    
    # Deploy
    local deployment_url
    if deployment_url=$(vercel --confirm $deploy_flags --token "$VERCEL_TOKEN" 2>&1); then
        success "Deployment successful for $product to $environment"
        log "Deployment URL: $deployment_url"
        
        # Store deployment info
        echo "{
            \"product\": \"$product\",
            \"environment\": \"$environment\",
            \"url\": \"$deployment_url\",
            \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
            \"commit\": \"$(git rev-parse HEAD)\"
        }" > "$LOG_DIR/deployment_${product}_${environment}_${TIMESTAMP}.json"
        
        return 0
    else
        error "Deployment failed for $product to $environment"
        error "Vercel output: $deployment_url"
        return 1
    fi
}

# ===== HEALTH CHECK FUNCTIONS =====
health_check() {
    local url=$1
    local product=$2
    local max_attempts=30
    local attempt=0
    
    log "Performing health check for $product at $url..."
    
    while [[ $attempt -lt $max_attempts ]]; do
        if curl -s -f "$url" > /dev/null; then
            success "Health check passed for $product"
            return 0
        fi
        
        attempt=$((attempt + 1))
        log "Health check attempt $attempt/$max_attempts failed. Retrying in 10 seconds..."
        sleep 10
    done
    
    error "Health check failed for $product after $max_attempts attempts"
    return 1
}

performance_check() {
    local url=$1
    local product=$2
    
    log "Performing performance check for $product..."
    
    # Check load time
    local load_time
    if load_time=$(curl -s -w "%{time_total}" -o /dev/null "$url"); then
        log "Load time for $product: ${load_time}s"
        
        # Check if load time is acceptable (< 3 seconds)
        if (( $(echo "$load_time < 3.0" | bc -l) )); then
            success "Performance check passed for $product"
            return 0
        else
            warning "Performance check warning: Load time ${load_time}s exceeds 3s threshold"
            return 1
        fi
    else
        error "Performance check failed for $product"
        return 1
    fi
}

# ===== ROLLBACK FUNCTIONS =====
rollback_deployment() {
    local product=$1
    local environment=$2
    
    error "Rolling back deployment for $product in $environment..."
    
    # This would typically involve:
    # 1. Finding the previous successful deployment
    # 2. Promoting it to current
    # 3. Updating any necessary configurations
    
    # For now, we'll create a rollback record
    echo "{
        \"product\": \"$product\",
        \"environment\": \"$environment\",
        \"rollback_timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
        \"reason\": \"Health check failed\"
    }" > "$LOG_DIR/rollback_${product}_${environment}_${TIMESTAMP}.json"
    
    # TODO: Implement actual rollback logic with Vercel API
    warning "Rollback initiated for $product. Manual intervention may be required."
}

# ===== NOTIFICATION FUNCTIONS =====
send_notification() {
    local message=$1
    local status=$2
    
    log "Sending notification: $message"
    
    # Webhook notification (if configured)
    if [[ -n "$SLACK_WEBHOOK_URL" ]]; then
        local color="good"
        if [[ "$status" == "error" ]]; then
            color="danger"
        elif [[ "$status" == "warning" ]]; then
            color="warning"
        fi
        
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"$message\", \"color\":\"$color\"}" \
            "$SLACK_WEBHOOK_URL" || true
    fi
    
    # Email notification could be added here
    # Discord notification could be added here
}

# ===== MAIN DEPLOYMENT LOGIC =====
deploy_single_product() {
    local product=$1
    local environment=$2
    
    log "Starting deployment process for $product to $environment..."
    
    # Build the product
    if ! build_product "$product"; then
        error "Build failed for $product"
        return 1
    fi
    
    # Validate the build
    if ! validate_build "$product"; then
        error "Build validation failed for $product"
        return 1
    fi
    
    # Deploy to Vercel
    if ! deploy_to_vercel "$product" "$environment"; then
        error "Deployment failed for $product to $environment"
        return 1
    fi
    
    # Determine the URL for health checks
    local url
    if [[ "$environment" == "production" ]]; then
        url="https://$product.com"
    else
        url="https://$product-staging.vercel.app"
    fi
    
    # Health check
    if ! health_check "$url" "$product"; then
        error "Health check failed for $product"
        rollback_deployment "$product" "$environment"
        return 1
    fi
    
    # Performance check
    if ! performance_check "$url" "$product"; then
        warning "Performance check failed for $product, but deployment continues"
    fi
    
    success "Deployment completed successfully for $product to $environment"
    return 0
}

deploy_all_products() {
    local environment=$1
    local failed_deployments=()
    
    log "Starting mass deployment to $environment..."
    
    for product in "${PRODUCTS[@]}"; do
        if deploy_single_product "$product" "$environment"; then
            success "✅ $product deployed successfully to $environment"
        else
            error "❌ $product deployment failed to $environment"
            failed_deployments+=("$product")
        fi
    done
    
    # Summary
    if [[ ${#failed_deployments[@]} -eq 0 ]]; then
        success "🎉 All products deployed successfully to $environment"
        send_notification "🚀 All products deployed successfully to $environment" "success"
    else
        error "❌ Some deployments failed to $environment: ${failed_deployments[*]}"
        send_notification "🚨 Failed deployments to $environment: ${failed_deployments[*]}" "error"
        return 1
    fi
}

# ===== MAIN EXECUTION =====
main() {
    local product=""
    local environment="staging"
    local action="deploy"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--product)
                product="$2"
                shift 2
                ;;
            -e|--environment)
                environment="$2"
                shift 2
                ;;
            -a|--action)
                action="$2"
                shift 2
                ;;
            -h|--help)
                echo "Usage: $0 [-p product] [-e environment] [-a action]"
                echo "  -p, --product      Product to deploy (qmoney, remotecash, cryptoflow, affiliatepro, or 'all')"
                echo "  -e, --environment  Environment to deploy to (staging, production)"
                echo "  -a, --action       Action to perform (deploy, rollback, health-check)"
                echo "  -h, --help         Show this help message"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Setup environment
    setup_environment
    
    log "🚀 Starting deployment process..."
    log "Product: ${product:-all}"
    log "Environment: $environment"
    log "Action: $action"
    
    # Execute based on parameters
    case $action in
        deploy)
            if [[ -n "$product" && "$product" != "all" ]]; then
                deploy_single_product "$product" "$environment"
            else
                deploy_all_products "$environment"
            fi
            ;;
        rollback)
            if [[ -n "$product" && "$product" != "all" ]]; then
                rollback_deployment "$product" "$environment"
            else
                error "Rollback requires a specific product"
                exit 1
            fi
            ;;
        health-check)
            if [[ -n "$product" && "$product" != "all" ]]; then
                local url="https://$product.com"
                health_check "$url" "$product"
            else
                error "Health check requires a specific product"
                exit 1
            fi
            ;;
        *)
            error "Unknown action: $action"
            exit 1
            ;;
    esac
    
    log "🎉 Deployment process completed!"
}

# Execute main function with all arguments
main "$@"