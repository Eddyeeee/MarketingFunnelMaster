#!/bin/bash
# Vercel Foundation Setup Script - Meilenstein 1D, Woche 1
# Automatisiert das Vercel Account Setup und API Integration

set -e

echo "🚀 MarketingFunnelMaster - Vercel Foundation Setup"
echo "=================================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI nicht installiert. Installiere mit: npm i -g vercel"
    exit 1
fi

# Step 1: Vercel Login
echo "📝 Step 1: Vercel Login"
echo "Bitte logge dich mit deinem Vercel Account ein..."
vercel login

# Step 2: Team Setup
echo "📝 Step 2: Team Setup"
read -p "Möchtest du ein neues Team erstellen? (y/n): " create_team
if [ "$create_team" = "y" ]; then
    vercel team add
fi

# Step 3: Environment Variables
echo "📝 Step 3: Environment Setup"
echo "Erstelle .env.vercel für API Integration..."

cat > .env.vercel << EOL
# Vercel API Configuration
VERCEL_TOKEN=your_token_here
VERCEL_TEAM_ID=your_team_id_here
VERCEL_PROJECT_ID=your_project_id_here

# Deployment Configuration
DEPLOYMENT_MODE=production
PARALLEL_DEPLOYMENTS=50
MAX_RETRY_ATTEMPTS=3

# Domain Configuration
PRIMARY_DOMAIN=marketingfunnelmaster.de
DOMAIN_WILDCARDS=*.qmoney.de,*.remotecash.de,*.cryptoflow.de,*.affiliatepro.de

# Cost Management
MONTHLY_BUDGET_LIMIT=25
ALERT_THRESHOLD=20
EOL

echo "✅ .env.vercel erstellt - Bitte Token eintragen!"

# Step 4: Project Setup
echo "📝 Step 4: Project Initialization"
read -p "Projekt Name (default: marketing-funnel-master): " project_name
project_name=${project_name:-marketing-funnel-master}

vercel link --yes

# Step 5: Vercel Configuration
echo "📝 Step 5: Erweiterte Vercel Konfiguration"
echo "Erstelle vercel-multi-site.json..."

cat > vercel-multi-site.json << 'EOL'
{
  "version": 2,
  "name": "marketing-funnel-master",
  "scope": "MarketingFunnelEmpire",
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    },
    {
      "src": "client/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1",
      "headers": {
        "x-deployment-id": "$VERCEL_DEPLOYMENT_ID"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/client/$1"
    }
  ],
  "env": {
    "DEPLOYMENT_MODE": "@deployment_mode",
    "NEON_DATABASE_URL": "@neon_database_url",
    "NEO4J_URI": "@neo4j_uri"
  },
  "functions": {
    "api/deploy/orchestrate.py": {
      "maxDuration": 300,
      "memory": 1024
    },
    "api/deploy/bulk.py": {
      "maxDuration": 600,
      "memory": 2048
    }
  }
}
EOL

# Step 6: API Integration Test
echo "📝 Step 6: API Integration Test Script"
cat > deployment/test-vercel-api.py << 'EOL'
#!/usr/bin/env python3
"""Test Vercel API Integration"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.vercel')

VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')
VERCEL_TEAM_ID = os.getenv('VERCEL_TEAM_ID')

def test_vercel_connection():
    """Test Vercel API Verbindung"""
    headers = {
        'Authorization': f'Bearer {VERCEL_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: User Info
    print("🔍 Test 1: Vercel User Info...")
    response = requests.get('https://api.vercel.com/v2/user', headers=headers)
    if response.status_code == 200:
        print("✅ User authenticated:", response.json()['user']['username'])
    else:
        print("❌ Authentication failed:", response.status_code)
        return False
    
    # Test 2: Team Info
    if VERCEL_TEAM_ID:
        print("\n🔍 Test 2: Team Info...")
        response = requests.get(
            f'https://api.vercel.com/v1/teams/{VERCEL_TEAM_ID}', 
            headers=headers
        )
        if response.status_code == 200:
            print("✅ Team found:", response.json()['name'])
        else:
            print("❌ Team not found:", response.status_code)
    
    # Test 3: Projects List
    print("\n🔍 Test 3: Projects List...")
    response = requests.get(
        'https://api.vercel.com/v8/projects',
        headers=headers,
        params={'teamId': VERCEL_TEAM_ID} if VERCEL_TEAM_ID else {}
    )
    if response.status_code == 200:
        projects = response.json()['projects']
        print(f"✅ Found {len(projects)} projects")
        for project in projects[:3]:
            print(f"  - {project['name']}")
    
    return True

if __name__ == "__main__":
    print("🚀 Vercel API Integration Test")
    print("=" * 40)
    
    if not VERCEL_TOKEN:
        print("❌ VERCEL_TOKEN nicht gesetzt in .env.vercel")
        exit(1)
    
    if test_vercel_connection():
        print("\n✅ Vercel API Integration erfolgreich!")
    else:
        print("\n❌ Vercel API Integration fehlgeschlagen!")
EOL

chmod +x deployment/test-vercel-api.py

# Step 7: Domain Wildcard Setup Helper
echo "📝 Step 7: Domain Wildcard Helper"
cat > deployment/setup-domain-wildcards.sh << 'EOL'
#!/bin/bash
# Domain Wildcard Setup für Multi-Site Deployment

source .env.vercel

echo "🌐 Domain Wildcard Konfiguration"
echo "================================"

domains=(
    "*.qmoney.de"
    "*.remotecash.de"
    "*.cryptoflow.de"
    "*.affiliatepro.de"
)

for domain in "${domains[@]}"; do
    echo "Adding wildcard domain: $domain"
    vercel domains add "$domain" --team "$VERCEL_TEAM_ID"
done

echo "✅ Domain Wildcards konfiguriert!"
echo ""
echo "⚠️  WICHTIG: DNS Konfiguration erforderlich!"
echo "Füge folgende DNS Records bei deinem Provider hinzu:"
echo ""
echo "*.qmoney.de        CNAME   cname.vercel-dns.com"
echo "*.remotecash.de    CNAME   cname.vercel-dns.com"
echo "*.cryptoflow.de    CNAME   cname.vercel-dns.com"
echo "*.affiliatepro.de  CNAME   cname.vercel-dns.com"
EOL

chmod +x deployment/setup-domain-wildcards.sh

echo ""
echo "✅ Vercel Foundation Setup abgeschlossen!"
echo ""
echo "📋 Nächste Schritte:"
echo "1. Trage VERCEL_TOKEN in .env.vercel ein"
echo "2. Führe deployment/test-vercel-api.py aus"
echo "3. Konfiguriere Domain Wildcards mit deployment/setup-domain-wildcards.sh"
echo "4. Erstelle HITL Entscheidungsvorlage für Account Upgrade"