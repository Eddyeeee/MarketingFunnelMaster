#!/bin/bash

# 📊 Monitoring Setup Script
# Marketing Funnel Master - Prometheus & Grafana Setup

set -e

# ===== CONFIGURATION =====
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MONITORING_DIR="$PROJECT_ROOT/monitoring"
DOCKER_COMPOSE_FILE="$PROJECT_ROOT/docker-compose.monitoring.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ===== UTILITY FUNCTIONS =====
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# ===== SETUP FUNCTIONS =====
setup_monitoring_directories() {
    log "Setting up monitoring directories..."
    
    mkdir -p "$MONITORING_DIR"
    mkdir -p "$MONITORING_DIR/grafana/dashboards"
    mkdir -p "$MONITORING_DIR/grafana/provisioning/dashboards"
    mkdir -p "$MONITORING_DIR/grafana/provisioning/datasources"
    mkdir -p "$MONITORING_DIR/alertmanager"
    mkdir -p "$MONITORING_DIR/blackbox"
    
    success "Monitoring directories created"
}

create_docker_compose_monitoring() {
    log "Creating monitoring Docker Compose configuration..."
    
    cat > "$DOCKER_COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  # ===== PROMETHEUS =====
  prometheus:
    image: prom/prometheus:latest
    container_name: mfm-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/alert_rules.yml:/etc/prometheus/alert_rules.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    networks:
      - monitoring
    restart: unless-stopped

  # ===== GRAFANA =====
  grafana:
    image: grafana/grafana:latest
    container_name: mfm-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-piechart-panel,grafana-worldmap-panel
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
    networks:
      - monitoring
    restart: unless-stopped
    depends_on:
      - prometheus

  # ===== ALERTMANAGER =====
  alertmanager:
    image: prom/alertmanager:latest
    container_name: mfm-alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
      - '--web.external-url=http://localhost:9093'
    networks:
      - monitoring
    restart: unless-stopped

  # ===== BLACKBOX EXPORTER =====
  blackbox-exporter:
    image: prom/blackbox-exporter:latest
    container_name: mfm-blackbox-exporter
    ports:
      - "9115:9115"
    volumes:
      - ./monitoring/blackbox/blackbox.yml:/etc/blackbox_exporter/config.yml:ro
    command:
      - '--config.file=/etc/blackbox_exporter/config.yml'
    networks:
      - monitoring
    restart: unless-stopped

  # ===== NODE EXPORTER =====
  node-exporter:
    image: prom/node-exporter:latest
    container_name: mfm-node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring
    restart: unless-stopped

networks:
  monitoring:
    driver: bridge
    name: mfm-monitoring

volumes:
  prometheus_data:
    name: mfm-prometheus-data
  grafana_data:
    name: mfm-grafana-data
  alertmanager_data:
    name: mfm-alertmanager-data
EOF

    success "Monitoring Docker Compose configuration created"
}

create_alertmanager_config() {
    log "Creating Alertmanager configuration..."
    
    cat > "$MONITORING_DIR/alertmanager/alertmanager.yml" << 'EOF'
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@marketingfunnelmaster.com'
  smtp_auth_username: 'alerts@marketingfunnelmaster.com'
  smtp_auth_password: 'your-email-password'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
    - match:
        severity: warning
      receiver: 'warning-alerts'

receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://localhost:5001/webhook'

  - name: 'critical-alerts'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts-critical'
        title: '🚨 Critical Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        color: 'danger'
    email_configs:
      - to: 'admin@marketingfunnelmaster.com'
        subject: '🚨 Critical Alert: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}

  - name: 'warning-alerts'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts-warning'
        title: '⚠️ Warning Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        color: 'warning'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
EOF

    success "Alertmanager configuration created"
}

create_blackbox_config() {
    log "Creating Blackbox Exporter configuration..."
    
    cat > "$MONITORING_DIR/blackbox/blackbox.yml" << 'EOF'
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
      valid_status_codes: [200, 201, 202, 204, 206, 301, 302, 307, 308]
      method: GET
      headers:
        Host: example.com
        Accept-Language: en-US
      no_follow_redirects: false
      fail_if_ssl: false
      fail_if_not_ssl: false
      
  http_post_2xx:
    prober: http
    timeout: 5s
    http:
      method: POST
      headers:
        Content-Type: application/json
      body: '{"test": "data"}'
      valid_status_codes: [200, 201, 202, 204]
      
  tcp_connect:
    prober: tcp
    timeout: 5s
    
  pop3s_banner:
    prober: tcp
    timeout: 5s
    tcp:
      query_response:
        - expect: "^+OK"
      tls: true
      tls_config:
        insecure_skip_verify: false
        
  ssh_banner:
    prober: tcp
    timeout: 5s
    tcp:
      query_response:
        - expect: "^SSH-2.0-"
        
  irc_banner:
    prober: tcp
    timeout: 5s
    tcp:
      query_response:
        - send: "NICK prober"
        - send: "USER prober prober prober :prober"
        - expect: "PING :([^ ]+)"
          send: "PONG :${1}"
        - expect: "^:[^ ]+ 001"
EOF

    success "Blackbox Exporter configuration created"
}

create_grafana_provisioning() {
    log "Creating Grafana provisioning configuration..."
    
    # Datasource configuration
    cat > "$MONITORING_DIR/grafana/provisioning/datasources/prometheus.yml" << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    basicAuth: false
    isDefault: true
    editable: true
EOF

    # Dashboard configuration
    cat > "$MONITORING_DIR/grafana/provisioning/dashboards/dashboard.yml" << 'EOF'
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
EOF

    success "Grafana provisioning configuration created"
}

create_grafana_dashboards() {
    log "Creating Grafana dashboards..."
    
    # Business Metrics Dashboard
    cat > "$MONITORING_DIR/grafana/dashboards/business-metrics.json" << 'EOF'
{
  "dashboard": {
    "id": null,
    "title": "Marketing Funnel Master - Business Metrics",
    "tags": ["business", "conversion", "revenue"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Total Revenue",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(revenue_total)",
            "legendFormat": "Total Revenue"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "currencyEUR",
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 5000},
                {"color": "green", "value": 10000}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Conversion Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "(sum(conversions_total) / sum(visitors_total)) * 100",
            "legendFormat": "Conversion Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 5},
                {"color": "green", "value": 10}
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Website Traffic",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(visitors_total[5m])) by (instance)",
            "legendFormat": "{{instance}}"
          }
        ]
      }
    ],
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
EOF

    # Technical Metrics Dashboard
    cat > "$MONITORING_DIR/grafana/dashboards/technical-metrics.json" << 'EOF'
{
  "dashboard": {
    "id": null,
    "title": "Marketing Funnel Master - Technical Metrics",
    "tags": ["technical", "performance", "uptime"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Website Uptime",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(probe_success)",
            "legendFormat": "Uptime"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 0.95},
                {"color": "green", "value": 0.99}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "probe_duration_seconds",
            "legendFormat": "{{instance}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s"
          }
        }
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{instance}}"
          }
        ]
      }
    ],
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
EOF

    success "Grafana dashboards created"
}

start_monitoring_stack() {
    log "Starting monitoring stack..."
    
    cd "$PROJECT_ROOT"
    
    # Start the monitoring stack
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Check if services are running
    if docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "Up"; then
        success "Monitoring stack started successfully"
        
        log "Access points:"
        log "  - Prometheus: http://localhost:9090"
        log "  - Grafana: http://localhost:3001 (admin/admin123)"
        log "  - Alertmanager: http://localhost:9093"
        log "  - Blackbox Exporter: http://localhost:9115"
        log "  - Node Exporter: http://localhost:9100"
        
        return 0
    else
        error "Failed to start monitoring stack"
        return 1
    fi
}

stop_monitoring_stack() {
    log "Stopping monitoring stack..."
    
    cd "$PROJECT_ROOT"
    docker-compose -f "$DOCKER_COMPOSE_FILE" down
    
    success "Monitoring stack stopped"
}

# ===== MAIN FUNCTION =====
main() {
    local action="setup"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            setup)
                action="setup"
                shift
                ;;
            start)
                action="start"
                shift
                ;;
            stop)
                action="stop"
                shift
                ;;
            restart)
                action="restart"
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [setup|start|stop|restart]"
                echo "  setup   - Set up monitoring configuration (default)"
                echo "  start   - Start monitoring stack"
                echo "  stop    - Stop monitoring stack"
                echo "  restart - Restart monitoring stack"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    case $action in
        setup)
            log "🔧 Setting up monitoring system..."
            setup_monitoring_directories
            create_docker_compose_monitoring
            create_alertmanager_config
            create_blackbox_config
            create_grafana_provisioning
            create_grafana_dashboards
            success "✅ Monitoring setup completed!"
            log "Run '$0 start' to start the monitoring stack"
            ;;
        start)
            log "🚀 Starting monitoring stack..."
            start_monitoring_stack
            ;;
        stop)
            log "🛑 Stopping monitoring stack..."
            stop_monitoring_stack
            ;;
        restart)
            log "🔄 Restarting monitoring stack..."
            stop_monitoring_stack
            sleep 5
            start_monitoring_stack
            ;;
        *)
            error "Unknown action: $action"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"