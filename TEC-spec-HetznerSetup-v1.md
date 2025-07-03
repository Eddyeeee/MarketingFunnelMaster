# HETZNER CLOUD INFRASTRUCTURE SETUP - TECHNISCHE SPEZIFIKATION

**Dokument ID:** TEC-spec-HetznerSetup-v1  
**Executor:** Claude Code (HTD-Executor-Ebene)  
**Erstellt:** 2025-07-03  
**Ziel:** Phase 1 Server-Infrastructure für 25 Websites  
**Budget:** €19/Monat (Hetzner-Anteil des €55 Gesamt-Budgets)  

---

## 🎯 INFRASTRUCTURE-ZIELE

### **PERFORMANCE-REQUIREMENTS:**
- **Load Time**: <2s (5x schneller als WordPress)
- **Uptime**: 99.9% SLA
- **Concurrent Users**: 1,000+ pro Website
- **Scalability**: Bereit für Phase 2 (100 Websites)

### **KOSTEN-ZIELE:**
- **Phase 1**: €19/Monat (2x CX32 + Load Balancer)
- **Vergleich**: 20x günstiger als €500 WordPress-Lösung
- **ROI**: Sofortige Kostenersparnis ab Tag 1

---

## 🏗️ SERVER-ARCHITEKTUR PHASE 1

### **KERN-KONFIGURATION:**
```
SETUP: High-Availability Multi-Server
├── 2x CX32 Application Servers (€6.80 × 2 = €13.60)
├── 1x Load Balancer (€5.39)
├── Geographic: Nuremberg (EU-Central)
└── Network: 10 Gbit backbone
```

### **SERVER-SPEZIFIKATIONEN:**

#### **CX32 Application Servers (2x):**
```
vCPUs:           4 (Intel Shared)
RAM:             8GB
Storage:         80GB NVMe SSD
Network:         20TB Traffic/Monat
Performance:     Shared vCPU (burst capability)
Cost:            €6.80/Monat pro Server
```

#### **Load Balancer Configuration:**
```
Type:            Hetzner Cloud Load Balancer
Algorithm:       Round Robin (default)
Health Checks:   HTTP/HTTPS endpoint monitoring
SSL Termination: Automatic Let's Encrypt
Scaling:         Auto-scaling based on demand
Cost:            €5.39/Monat
```

---

## 🔧 TECHNISCHE IMPLEMENTIERUNG

### **DOCKER-CONTAINERIZATION:**
```yaml
# docker-compose.yml für FastAPI + Next.js Stack
version: '3.8'
services:
  fastapi-backend:
    image: tiangolo/uvicorn-gunicorn-fastapi:python3.11
    ports:
      - "8000:80"
    environment:
      - MODULE_NAME=main
      - VARIABLE_NAME=app
    volumes:
      - ./backend:/app
    
  nextjs-frontend:
    image: node:18-alpine
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    command: npm run start
    
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
```

### **AUTOMATISIERTE SERVER-PROVISIONING:**
```python
# Hetzner Cloud API Integration
import requests
import json

class HetznerCloudManager:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.hetzner.cloud/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def create_server(self, name, server_type="cx32", image="ubuntu-22.04"):
        """Create new server instance"""
        data = {
            "name": name,
            "server_type": server_type,
            "image": image,
            "location": "nbg1",  # Nuremberg
            "start_after_create": True,
            "user_data": self.get_cloud_init_script()
        }
        
        response = requests.post(
            f"{self.base_url}/servers",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def create_load_balancer(self, name, targets):
        """Create load balancer with target servers"""
        data = {
            "name": name,
            "load_balancer_type": "lb11",
            "location": "nbg1",
            "targets": targets,
            "services": [
                {
                    "protocol": "http",
                    "listen_port": 80,
                    "destination_port": 80,
                    "health_check": {
                        "protocol": "http",
                        "port": 80,
                        "interval": 15,
                        "timeout": 10,
                        "retries": 3,
                        "http": {"path": "/health"}
                    }
                },
                {
                    "protocol": "https",
                    "listen_port": 443,
                    "destination_port": 443
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/load_balancers",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_cloud_init_script(self):
        """Cloud-init script for automated server setup"""
        return """#cloud-config
packages:
  - docker.io
  - docker-compose
  - nginx
  - certbot
  - python3-certbot-nginx

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ubuntu
  - curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  - chmod +x /usr/local/bin/docker-compose
  - mkdir -p /opt/fastapi-nextjs
  - git clone https://github.com/yourusername/marketing-funnel-master.git /opt/fastapi-nextjs
  - cd /opt/fastapi-nextjs && docker-compose up -d
"""
```

---

## 🌐 NETWORK & SECURITY KONFIGURATION

### **LOAD BALANCER SETUP:**
```
HEALTH CHECK CONFIGURATION:
├── Protocol: HTTP/HTTPS
├── Path: /health
├── Interval: 15 seconds
├── Timeout: 10 seconds
├── Retries: 3
└── Healthy Threshold: 2

SSL/TLS CONFIGURATION:
├── Certificate: Let's Encrypt (Auto-Renewal)
├── TLS Version: 1.2+ only
├── HSTS: Enabled
└── Redirect HTTP → HTTPS: Automatic
```

### **FIREWALL-REGELN:**
```
INBOUND RULES:
├── Port 22 (SSH): Source 0.0.0.0/0 (Management)
├── Port 80 (HTTP): Source Load Balancer only
├── Port 443 (HTTPS): Source Load Balancer only
├── Port 8000 (FastAPI): Source Load Balancer only
└── Port 3000 (Next.js): Source Load Balancer only

OUTBOUND RULES:
├── All traffic allowed (Updates, API calls)
└── DNS: Port 53 UDP/TCP
```

### **MONITORING & LOGGING:**
```python
# Monitoring Integration Setup
import psutil
import requests
from datetime import datetime

class ServerMonitoring:
    def __init__(self, server_id, webhook_url):
        self.server_id = server_id
        self.webhook_url = webhook_url
    
    def collect_metrics(self):
        """Collect server performance metrics"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "server_id": self.server_id,
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict(),
            "load_average": psutil.getloadavg()
        }
    
    def send_metrics(self):
        """Send metrics to monitoring system"""
        metrics = self.collect_metrics()
        response = requests.post(self.webhook_url, json=metrics)
        return response.status_code == 200
```

---

## 📊 DEPLOYMENT STRATEGY

### **BLUE-GREEN DEPLOYMENT:**
```
PRODUCTION SETUP:
├── Blue Environment: CX32-Server-01 (Active)
├── Green Environment: CX32-Server-02 (Standby)
├── Load Balancer: Traffic routing control
└── Deployment: Zero-downtime switches

DEPLOYMENT PROCESS:
1. Deploy new version to Green environment
2. Run health checks and tests
3. Switch load balancer to Green
4. Blue becomes new standby
5. Monitor and rollback if issues
```

### **BACKUP & DISASTER RECOVERY:**
```
BACKUP STRATEGY:
├── Automated Snapshots: Daily (€0.011/GB)
├── Application Data: Real-time sync
├── Configuration: Git-based versioning
└── Database: Continuous replication

RECOVERY OBJECTIVES:
├── RTO (Recovery Time): <15 minutes
├── RPO (Recovery Point): <5 minutes
├── Failover: Automatic with health checks
└── Geographic: EU-Central primary
```

---

## 💰 KOSTENOPTIMIERUNG

### **PHASE 1 KOSTEN-BREAKDOWN:**
```
CX32 Server 1:          €6.80/Monat
CX32 Server 2:          €6.80/Monat
Load Balancer:          €5.39/Monat
Snapshots (160GB):      €1.76/Monat (€0.011 × 160GB)
TOTAL HETZNER:          €20.75/Monat

BUDGETIERTE KOSTEN:     €19.00/Monat
DIFFERENZ:              +€1.75/Monat (3.7% über Budget)
```

### **KOSTENOPTIMIERUNGS-MASSNAHMEN:**
1. **Snapshot-Optimierung**: Nur kritische Daten sichern
2. **Traffic-Monitoring**: 20TB Limit überwachen
3. **Resource-Scaling**: Bei Bedarf auf kleinere Server wechseln
4. **Volume-Discounts**: Bei Phase 2 Verhandlungen

---

## 🔄 SKALIERUNGS-ROADMAP

### **PHASE 2 EXPANSION (100 Websites):**
```
SCALE-UP STRATEGY:
├── 4x CCX33 Dedicated vCPU (€28 × 4 = €112)
├── 2x Load Balancers (Geographic distribution)
├── Block Storage Volumes (für Daten-Persistierung)
└── Multi-Region Setup (EU + US)

ESTIMATED COSTS PHASE 2:
├── Servers: €112/Monat
├── Load Balancers: €10.78/Monat
├── Storage: €44/Monat (1TB)
└── Total: €166.78/Monat
```

### **AUTOMATION-ERWEITERUNGEN:**
- **Auto-Scaling**: Hetzner API-based server provisioning
- **Container Orchestration**: Kubernetes für advanced management
- **CI/CD Integration**: Automated deployment pipelines
- **Performance Optimization**: CDN integration mit Cloudflare

---

## 📋 IMPLEMENTATION CHECKLIST

### **SOFORT AUSFÜHREN:**
- [ ] Hetzner Cloud Account erstellen
- [ ] API-Token generieren
- [ ] SSH-Key-Pair erstellen
- [ ] 2x CX32 Server provisionieren
- [ ] Load Balancer konfigurieren
- [ ] Cloud-init Scripts deployen
- [ ] Health-Checks einrichten
- [ ] Monitoring-Dashboard setup

### **WOCHE 1 ZIELE:**
- [ ] Alle Server operational
- [ ] Load Balancer aktiv mit Health-Checks
- [ ] SSL-Certificates automatisch erneuert
- [ ] Monitoring-Alerts konfiguriert
- [ ] Backup-Strategie implementiert

---

**🎯 EXECUTOR-STATUS:** Server-Spezifikation abgeschlossen. Hetzner-Infrastructure bereit für Provisioning.

**🚀 NÄCHSTER SCHRITT:** Cloudflare-Integration für DNS & CDN Setup.