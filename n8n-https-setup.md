# n8n HTTPS Setup für Social Media Automation

## 🚀 Schritt 1: SSL-Zertifikat einrichten

### Let's Encrypt Zertifikat generieren
```bash
# Certbot installieren
sudo apt update
sudo apt install certbot

# SSL-Zertifikat für deine Domain generieren
sudo certbot certonly --standalone -d deine-domain.com

# Zertifikate kopieren
sudo cp /etc/letsencrypt/live/deine-domain.com/fullchain.pem /opt/n8n/
sudo cp /etc/letsencrypt/live/deine-domain.com/privkey.pem /opt/n8n/
sudo chown n8n:n8n /opt/n8n/*.pem
```

## 🔧 Schritt 2: n8n mit HTTPS konfigurieren

### n8n Service-Datei erstellen
```bash
sudo nano /etc/systemd/system/n8n.service
```

### Service-Konfiguration
```ini
[Unit]
Description=n8n
After=network.target

[Service]
Type=simple
User=n8n
ExecStart=/usr/bin/n8n start
Restart=always
RestartSec=10
Environment=N8N_HOST=deine-domain.com
Environment=N8N_PORT=5678
Environment=N8N_PROTOCOL=https
Environment=N8N_SSL_KEY=/opt/n8n/privkey.pem
Environment=N8N_SSL_CERT=/opt/n8n/fullchain.pem
Environment=N8N_WEBHOOK_URL=https://deine-domain.com/
Environment=N8N_ENCRYPTION_KEY=dein-encryption-key
Environment=N8N_DATABASE_TYPE=postgresdb
Environment=N8N_DATABASE_POSTGRESDB_HOST=localhost
Environment=N8N_DATABASE_POSTGRESDB_PORT=5432
Environment=N8N_DATABASE_POSTGRESDB_DATABASE=n8n
Environment=N8N_DATABASE_POSTGRESDB_USER=n8n
Environment=N8N_DATABASE_POSTGRESDB_PASSWORD=dein-db-password

[Install]
WantedBy=multi-user.target
```

## 🌐 Schritt 3: Nginx Reverse Proxy

### Nginx-Konfiguration
```bash
sudo nano /etc/nginx/sites-available/n8n
```

### Nginx-Konfiguration
```nginx
server {
    listen 80;
    server_name deine-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name deine-domain.com;

    ssl_certificate /etc/letsencrypt/live/deine-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/deine-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    # Webhook Endpoints
    location /webhook/ {
        proxy_pass http://localhost:5678/webhook/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔄 Schritt 4: Services starten

```bash
# Nginx aktivieren
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# n8n Service starten
sudo systemctl daemon-reload
sudo systemctl enable n8n
sudo systemctl start n8n
sudo systemctl status n8n
```

## 🔐 Schritt 5: Firewall konfigurieren

```bash
# UFW Firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

## 📋 Schritt 6: Webhook-URLs konfigurieren

### Social Media Webhooks
- **Facebook Webhook:** `https://deine-domain.com/webhook/facebook`
- **Instagram Webhook:** `https://deine-domain.com/webhook/instagram`
- **TikTok Webhook:** `https://deine-domain.com/webhook/tiktok`
- **Shopify Webhook:** `https://deine-domain.com/webhook/shopify`

### n8n Webhook-Nodes konfigurieren
```json
{
  "webhookUrl": "https://deine-domain.com/webhook/social-media",
  "httpMethod": "POST",
  "path": "social-media",
  "responseMode": "responseNode",
  "options": {
    "responseHeaders": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    }
  }
}
```

## 🔄 Schritt 7: SSL-Zertifikat erneuern

### Automatische Erneuerung
```bash
# Cron-Job für automatische Erneuerung
sudo crontab -e

# Füge diese Zeile hinzu:
0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx
```

## 🧪 Schritt 8: Testen

### Webhook-Test
```bash
curl -X POST https://deine-domain.com/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### n8n Status prüfen
```bash
curl https://deine-domain.com/healthz
```

## 📊 Schritt 9: Monitoring

### Logs überwachen
```bash
# n8n Logs
sudo journalctl -u n8n -f

# Nginx Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### SSL-Zertifikat Status
```bash
sudo certbot certificates
```

## 🚨 Troubleshooting

### Häufige Probleme
1. **SSL-Zertifikat nicht gefunden**
   ```bash
   sudo certbot certonly --standalone -d deine-domain.com
   ```

2. **n8n startet nicht**
   ```bash
   sudo systemctl status n8n
   sudo journalctl -u n8n -n 50
   ```

3. **Nginx Fehler**
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   ```

4. **Firewall blockiert**
   ```bash
   sudo ufw status
   sudo ufw allow 443/tcp
   ```

## ✅ Checkliste

- [ ] SSL-Zertifikat generiert
- [ ] n8n Service konfiguriert
- [ ] Nginx Reverse Proxy eingerichtet
- [ ] Firewall konfiguriert
- [ ] Webhook-URLs getestet
- [ ] Automatische SSL-Erneuerung eingerichtet
- [ ] Monitoring konfiguriert
- [ ] Backup-Strategie implementiert

## 🔗 Nützliche Links

- [n8n HTTPS Dokumentation](https://docs.n8n.io/hosting/installation/ssl/)
- [Let's Encrypt Dokumentation](https://letsencrypt.org/docs/)
- [Nginx Reverse Proxy Guide](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) 