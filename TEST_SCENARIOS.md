# Test-Szenarien: Service-Integration & erweiterte Lead-Capture

## 🎯 **Übersicht**

Dieses Dokument beschreibt umfassende Test-Szenarien für die neuen Service-Integrationen und erweiterte Lead-Capture-Features.

## 🧪 **Test-Setup**

### Voraussetzungen
1. **Backend läuft:** `npm run dev` im `server/` Verzeichnis
2. **Frontend läuft:** `npm run dev` im `client/` Verzeichnis
3. **Datenbank:** PostgreSQL läuft und ist konfiguriert
4. **Umgebungsvariablen:** `.env` Datei mit Test-Konfiguration

### Test-Konfiguration
```bash
# .env für Tests
ENABLE_N8N_INTEGRATION=true
ENABLE_INSTAPAGE_INTEGRATION=true
INSTAPAGE_API_KEY=test_key
INSTAPAGE_ACCOUNT_ID=test_account
N8N_WEBHOOK_URL=https://test-n8n.com/webhook
```

## 📋 **Test-Szenarien**

### 1. **Analytics & Tracking Tests**

#### 1.1 UTM-Parameter-Tracking
**Ziel:** Überprüfen der automatischen UTM-Parameter-Extraktion

**Test-Schritte:**
1. Öffne Browser-Entwicklertools (F12)
2. Gehe zu: `http://localhost:3000/?utm_source=google&utm_campaign=test&utm_medium=cpc&gclid=abc123`
3. Fülle LeadCaptureForm aus
4. Überprüfe Network-Tab für `/api/capture-lead` Request
5. Überprüfe Console für Session-Initialisierung

**Erwartetes Ergebnis:**
- UTM-Parameter werden in Request-Body übertragen
- Session-ID wird generiert und gespeichert
- Analytics-Events enthalten UTM-Daten

#### 1.2 Session-Tracking
**Ziel:** Überprüfen der Session-Persistierung

**Test-Schritte:**
1. Öffne neue Browser-Session
2. Gehe zu Homepage
3. Überprüfe `sessionStorage` in Entwicklertools
4. Navigiere zu verschiedenen Seiten
5. Überprüfe Session-Daten-Persistierung

**Erwartetes Ergebnis:**
- `qmoney_session_id` wird erstellt
- `qmoney_session_data` wird gespeichert
- Session-Daten bleiben zwischen Seitenaufrufen erhalten

#### 1.3 Conversion-Tracking
**Ziel:** Überprüfen der erweiterten Conversion-Events

**Test-Schritte:**
1. Öffne Google Analytics Debug-Modus
2. Fülle LeadCaptureForm aus
3. Überprüfe GA-Events in Console
4. Überprüfe `/api/analytics` Requests

**Erwartetes Ergebnis:**
- `form_submission` Event wird getrackt
- `lead_capture_success` Event wird getrackt
- Events enthalten erweiterte Metadaten

### 2. **LeadCaptureForm Tests**

#### 2.1 Standard Lead-Capture
**Ziel:** Überprüfen der Standard-Funktionalität

**Test-Schritte:**
1. Gehe zu Homepage
2. Fülle LeadCaptureForm aus (nur Pflichtfelder)
3. Klicke "Kostenlosen Zugang sichern"
4. Überprüfe Erfolgsmeldung

**Erwartetes Ergebnis:**
- Formular-Validierung funktioniert
- POST `/api/leads` wird gesendet
- Erfolgsmeldung wird angezeigt
- Formular wird zurückgesetzt

#### 2.2 Erweiterte Lead-Capture
**Ziel:** Überprüfen der Service-Integration

**Test-Schritte:**
1. Gehe zu Homepage
2. Fülle LeadCaptureForm mit allen Feldern aus
3. Klicke "Kostenlosen Zugang sichern"
4. Überprüfe erweiterte Erfolgsmeldung

**Erwartetes Ergebnis:**
- POST `/api/capture-lead` wird gesendet
- Erweiterte Erfolgsmeldung mit Integration-Status
- Loading-Messages werden angezeigt
- UTM-Parameter werden übertragen

#### 2.3 Quiz-Integration
**Ziel:** Überprüfen der Quiz-Daten-Integration

**Test-Schritte:**
1. Gehe zu Quiz-Seite
2. Beantworte alle Fragen
3. Fülle Lead-Formular aus
4. Überprüfe Persona-Erstellung

**Erwartetes Ergebnis:**
- Quiz-Antworten werden übertragen
- Persona wird basierend auf Quiz erstellt
- Erweiterte Lead-Daten enthalten Quiz-Kontext

#### 2.4 Error-Handling
**Ziel:** Überprüfen der Fehlerbehandlung

**Test-Schritte:**
1. Deaktiviere Backend-Services
2. Fülle LeadCaptureForm aus
3. Überprüfe Fehlermeldungen
4. Aktiviere Services wieder

**Erwartetes Ergebnis:**
- Graceful Degradation bei Service-Ausfällen
- Benutzerfreundliche Fehlermeldungen
- Fallback zu Standard-Endpunkt

### 3. **QuizForm Tests**

#### 3.1 Quiz-Flow
**Ziel:** Überprüfen des vollständigen Quiz-Flows

**Test-Schritte:**
1. Gehe zu `/quiz`
2. Beantworte alle 4 Fragen
3. Überprüfe Quiz-Ergebnisse
4. Fülle Lead-Formular aus

**Erwartetes Ergebnis:**
- Progress-Indicator funktioniert
- Quiz-Ergebnisse werden korrekt berechnet
- Persona-basierte Empfehlungen
- Erweiterte Lead-Capture mit Quiz-Daten

#### 3.2 Verschiedene Quiz-Pfade
**Ziel:** Überprüfen verschiedener Persona-Pfade

**Test-Szenarien:**
- **Student-Pfad:** student → money_tight → basic → no_capital
- **Employee-Pfad:** employee → no_time → substantial → no_experience
- **Parent-Pfad:** parent → no_time → basic → tried_failed

**Erwartetes Ergebnis:**
- Verschiedene Funnel-Empfehlungen
- Persona-spezifische Strategien
- Angepasste Next-Steps

#### 3.3 Quiz-Tracking
**Ziel:** Überprüfen des Quiz-Trackings

**Test-Schritte:**
1. Öffne GA Debug-Modus
2. Beantworte Quiz-Fragen
3. Überprüfe Tracking-Events
4. Überprüfe Lead-Capture-Tracking

**Erwartetes Ergebnis:**
- `quiz_answer` Events für jede Antwort
- `quiz_completed` Event mit Metadaten
- `quiz_lead_capture_success` Event

### 4. **Service-Integration Tests**

#### 4.1 n8n Integration
**Ziel:** Überprüfen der n8n Webhook-Integration

**Test-Schritte:**
1. Konfiguriere n8n Webhook-URL
2. Fülle LeadCaptureForm aus
3. Überprüfe n8n Webhook-Aufrufe
4. Überprüfe Webhook-Payload

**Erwartetes Ergebnis:**
- Webhook wird mit korrekten Daten aufgerufen
- Lead-Daten werden übertragen
- UTM-Parameter sind enthalten
- Session-Daten sind enthalten

#### 4.2 Instapage Integration
**Ziel:** Überprüfen der Instapage-Seiten-Erstellung

**Test-Schritte:**
1. Konfiguriere Instapage API
2. Fülle LeadCaptureForm mit Persona aus
3. Überprüfe Instapage API-Aufrufe
4. Überprüfe erstellte Seiten

**Erwartetes Ergebnis:**
- Personalisierte Seiten werden erstellt
- Seiten-URL wird zurückgegeben
- Persona-Daten werden übertragen

#### 4.3 Service-Fehler-Handling
**Ziel:** Überprüfen der Service-Fehlerbehandlung

**Test-Szenarien:**
- n8n Service nicht erreichbar
- Instapage API-Fehler
- Beide Services nicht verfügbar

**Erwartetes Ergebnis:**
- Graceful Degradation
- Lead wird trotzdem gespeichert
- Benutzerfreundliche Meldungen

### 5. **Performance Tests**

#### 5.1 Ladezeiten
**Ziel:** Überprüfen der Performance-Impact

**Test-Schritte:**
1. Messen Ladezeit ohne Service-Integration
2. Messen Ladezeit mit Service-Integration
3. Überprüfe Bundle-Größe
4. Überprüfe Network-Requests

**Erwartetes Ergebnis:**
- Keine signifikante Performance-Verschlechterung
- Lazy Loading funktioniert
- Optimale Bundle-Größe

#### 5.2 Memory-Usage
**Ziel:** Überprüfen des Memory-Verbrauchs

**Test-Schritte:**
1. Öffne Memory-Tab in DevTools
2. Navigiere durch verschiedene Seiten
3. Überprüfe Memory-Leaks
4. Überprüfe Session-Storage-Usage

**Erwartetes Ergebnis:**
- Keine Memory-Leaks
- Session-Daten werden korrekt bereinigt
- Optimale Memory-Nutzung

### 6. **Browser-Kompatibilität Tests**

#### 6.1 Moderne Browser
**Ziel:** Überprüfen der Kompatibilität

**Test-Browser:**
- Chrome (neueste Version)
- Firefox (neueste Version)
- Safari (neueste Version)
- Edge (neueste Version)

**Test-Schritte:**
1. Führe alle Haupt-Tests in jedem Browser durch
2. Überprüfe Session-Storage-Funktionalität
3. Überprüfe Analytics-Tracking
4. Überprüfe Service-Integration

#### 6.2 Mobile Browser
**Ziel:** Überprüfen der mobilen Kompatibilität

**Test-Geräte:**
- iOS Safari
- Android Chrome
- Mobile Firefox

**Test-Schritte:**
1. Teste responsive Design
2. Überprüfe Touch-Interaktionen
3. Überprüfe Performance
4. Überprüfe Service-Integration

### 7. **Sicherheits-Tests**

#### 7.1 XSS-Schutz
**Ziel:** Überprüfen der XSS-Sicherheit

**Test-Schritte:**
1. Injiziere Script-Tags in Formular-Felder
2. Überprüfe Output-Sanitization
3. Überprüfe API-Validierung

**Erwartetes Ergebnis:**
- Keine XSS-Vulnerabilities
- Input-Validierung funktioniert
- Output wird korrekt escaped

#### 7.2 CSRF-Schutz
**Ziel:** Überprüfen der CSRF-Sicherheit

**Test-Schritte:**
1. Überprüfe CSRF-Token-Validierung
2. Teste Cross-Origin-Requests
3. Überprüfe Same-Origin-Policy

**Erwartetes Ergebnis:**
- CSRF-Schutz ist implementiert
- Cross-Origin-Requests werden blockiert
- Sichere API-Kommunikation

## 🔍 **Debugging & Monitoring**

### Console-Logs überwachen
```javascript
// Session-Initialisierung
console.log('Session initialized:', sessionData.sessionId);

// Lead-Capture
console.log('Lead captured:', result.data.lead);
console.log('n8n integration:', result.data.integrations.n8n);
console.log('Instapage integration:', result.data.integrations.instapage);
```

### Network-Tab überwachen
- `POST /api/capture-lead` - Erweiterte Lead-Capture
- `POST /api/quiz/results` - Quiz-Ergebnisse
- `POST /api/analytics` - Analytics-Events
- n8n Webhook-Aufrufe
- Instapage API-Aufrufe

### Google Analytics Debug
```javascript
// GA Debug-Modus aktivieren
gtag('config', 'GA_MEASUREMENT_ID', {
  debug_mode: true
});
```

## 📊 **Erfolgs-Metriken**

### Funktionale Metriken
- ✅ Alle Formulare funktionieren korrekt
- ✅ Service-Integration funktioniert
- ✅ Error-Handling funktioniert
- ✅ Tracking funktioniert

### Performance-Metriken
- ⏱️ Ladezeit < 2 Sekunden
- 💾 Memory-Usage < 50MB
- 📦 Bundle-Größe < 500KB

### Sicherheits-Metriken
- 🔒 Keine XSS-Vulnerabilities
- 🛡️ CSRF-Schutz aktiv
- 🔐 Sichere API-Kommunikation

## 🚀 **Nächste Schritte**

Nach erfolgreichen Tests:
1. **Produktions-Deployment** vorbereiten
2. **Monitoring** einrichten
3. **A/B-Tests** planen
4. **Performance-Optimierung** durchführen

Die Tests decken alle wichtigen Aspekte der neuen Service-Integration ab und stellen sicher, dass das System robust und benutzerfreundlich funktioniert. 