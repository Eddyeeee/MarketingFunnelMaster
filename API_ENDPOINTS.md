# Q-Money Funnel API Dokumentation

## Übersicht

Die Q-Money Funnel API bietet umfassende Endpunkte für Lead-Capture, Quiz-Integration, Analytics und Service-Integrationen mit Instapage und n8n.

## Base URL
```
http://localhost:3000/api
```

## Authentifizierung
Aktuell ist keine Authentifizierung erforderlich. Für Produktionsumgebungen wird JWT-Token-Authentifizierung empfohlen.

## Endpunkte

### 1. Lead Capture

#### POST `/api/leads`
**Standard Lead-Capture Endpunkt**

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "Max Mustermann",
  "phone": "+49123456789",
  "source": "homepage",
  "funnel": "magic-profit",
  "quizAnswers": "{\"1\":\"student\",\"2\":\"money_tight\"}",
  "persona": "{\"type\":\"student\",\"preferences\":{}}"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "Max Mustermann",
    "phone": "+49123456789",
    "source": "homepage",
    "funnel": "magic-profit",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "message": "Lead captured successfully"
}
```

#### POST `/api/capture-lead`
**Erweiterter Lead-Capture Endpunkt mit Service-Integration**

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "Max Mustermann",
  "phone": "+49123456789",
  "source": "capture-lead",
  "funnel": "magic-profit",
  "quizAnswers": "{\"1\":\"student\",\"2\":\"money_tight\"}",
  "persona": "{\"type\":\"student\",\"preferences\":{}}",
  "utmSource": "google",
  "utmMedium": "cpc",
  "utmCampaign": "qmoney_winter_2024",
  "utmTerm": "online geld verdienen",
  "utmContent": "banner_ad_1",
  "gclid": "abc123",
  "fbclid": "def456",
  "sessionId": "session_789",
  "pageUrl": "https://qmoney.de/quiz",
  "referrer": "https://google.com",
  "customFields": {
    "age": "25",
    "interests": ["finance", "entrepreneurship"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "lead": {
      "id": 1,
      "email": "user@example.com",
      "name": "Max Mustermann",
      "phone": "+49123456789",
      "source": "capture-lead",
      "funnel": "magic-profit",
      "created_at": "2024-01-15T10:30:00Z"
    },
    "integrations": {
      "n8n": true,
      "instapage": {
        "success": true,
        "pageUrl": "https://instapage.com/p/abc123",
        "pageId": "page_456"
      }
    }
  },
  "message": "Lead captured and processed successfully"
}
```

### 2. Lead Abfrage

#### GET `/api/leads`
**Alle Leads abrufen**

**Query Parameters:**
- `funnel` (optional): Filter nach Funnel-Typ

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "Max Mustermann",
      "source": "homepage",
      "funnel": "magic-profit",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 3. Quiz Integration

#### POST `/api/quiz/results`
**Quiz-Ergebnisse verarbeiten und Lead erstellen**

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "Max Mustermann",
  "answers": {
    "1": "student",
    "2": "money_tight",
    "3": "basic",
    "4": "no_capital"
  },
  "persona": {
    "type": "student",
    "profileText": "Struggling Student Sarah • Monatliche Geldknappheit • 500-1.500€ Zusatzeinkommen",
    "strategyText": "Magic Tool System - Perfekt für den Einstieg mit 0€ Startkapital.",
    "recommendedFunnel": "magic_tool"
  },
  "utmParams": {
    "utm_source": "quiz",
    "utm_campaign": "magic_tool",
    "utm_medium": "organic"
  },
  "sessionId": "abc123",
  "pageUrl": "https://example.com/quiz",
  "referrer": "https://google.com"
}
```

**Response:**
```json
{
  "success": true,
  "lead": {
    "id": 1,
    "email": "user@example.com"
  },
  "integrations": {
    "n8n": false,
    "instapage": false
  },
  "message": "Quiz-Ergebnisse erfolgreich gespeichert. Du erhältst gleich eine E-Mail von uns."
}
```

### 4. Email Funnels

#### GET `/api/email-funnels`
**Alle Email-Funnels abrufen**

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Magic Profit Welcome Series",
      "description": "Willkommens-Serie für Magic Profit Interessenten",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### GET `/api/email-funnels/:id`
**Spezifischen Email-Funnel abrufen**

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Magic Profit Welcome Series",
    "description": "Willkommens-Serie für Magic Profit Interessenten",
    "emails": [
      {
        "id": 1,
        "subject": "Willkommen bei Q-Money!",
        "content": "Hallo {{name}}, willkommen bei Q-Money...",
        "delay_hours": 0
      }
    ],
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### POST `/api/email-funnels`
**Neuen Email-Funnel erstellen**

**Request Body:**
```json
{
  "name": "Money Magnet Advanced Series",
  "description": "Erweiterte Serie für Money Magnet Kunden"
}
```

### 5. Analytics

#### POST `/api/analytics`
**Analytics-Event erstellen**

**Request Body:**
```json
{
  "page": "/quiz",
  "event": "quiz_started",
  "data": {
    "quizType": "personality",
    "sessionId": "session_789"
  }
}
```

#### GET `/api/analytics`
**Analytics-Events abrufen**

**Query Parameters:**
- `page` (optional): Filter nach Seite

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "page": "/quiz",
      "event": "quiz_started",
      "data": {
        "quizType": "personality",
        "sessionId": "session_789"
      },
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Instapage Integration

### Verfügbare Endpunkte
- `GET /api/instapage/pages` - Alle Seiten abrufen
- `GET /api/instapage/pages/:id` - Spezifische Seite abrufen
- `POST /api/instapage/pages` - Neue Seite erstellen
- `POST /api/instapage/pages/:id/duplicate` - Seite duplizieren
- `PUT /api/instapage/pages/:id` - Seite aktualisieren
- `DELETE /api/instapage/pages/:id` - Seite löschen

### Beispiel: Seite duplizieren
```bash
curl -X POST http://localhost:3000/api/instapage/pages/template_123/duplicate \
  -H "Content-Type: application/json" \
  -d '{
    "new_name": "Q-Money Student Sarah - 2024-01-15",
    "account_id": "account_456"
  }'
```

## Fehlerbehandlung

Alle Endpunkte geben strukturierte Fehlerantworten zurück:

```json
{
  "success": false,
  "message": "Beschreibung des Fehlers",
  "error": "Detaillierte Fehlermeldung"
}
```

### HTTP Status Codes
- `200` - Erfolgreich
- `400` - Ungültige Anfrage
- `404` - Nicht gefunden
- `500` - Server-Fehler

## Rate Limiting

Standardmäßig sind 100 Anfragen pro 15 Minuten erlaubt. Überschreitungen führen zu HTTP 429.

## Umgebungsvariablen

Stelle sicher, dass folgende Umgebungsvariablen gesetzt sind:

```bash
# Service Integration
ENABLE_N8N_INTEGRATION=true
ENABLE_INSTAPAGE_INTEGRATION=true

# Instapage
INSTAPAGE_API_KEY=your_api_key
INSTAPAGE_ACCOUNT_ID=your_account_id
INSTAPAGE_TEMPLATE_ID=your_template_id

# n8n
N8N_WEBHOOK_URL=your_webhook_url
N8N_API_KEY=your_api_key
```

## Beispiele

### Frontend Integration (JavaScript)
```javascript
// Lead capture
const response = await fetch('/api/capture-lead', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    name: 'Max Mustermann',
    source: 'homepage',
    utmSource: 'google',
    utmCampaign: 'winter_2024'
  })
});

const result = await response.json();
console.log('Lead captured:', result.data.lead);
console.log('n8n integration:', result.data.integrations.n8n);
```

### Quiz Integration
```javascript
// Quiz results
const quizResponse = await fetch('/api/quiz/results', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    answers: {
      '1': 'student',
      '2': 'money_tight',
      '3': 'basic',
      '4': 'no_capital'
    }
  })
});

const quizResult = await quizResponse.json();
console.log('Recommended funnel:', quizResult.data.recommendedFunnel);
```

## Quiz Endpoints

### GET /api/quizzes/:id
Lädt Quiz-Fragen für ein spezifisches Quiz.

**Parameter:**
- `id` (string): Die ID des Quiz (z.B. "magic_tool")

**Response:**
```json
{
  "success": true,
  "quiz": {
    "id": "magic_tool",
    "title": "Finde heraus, welcher Geld-Typ du bist!",
    "description": "Beantworte 4 kurze Fragen und erhalte deine personalisierte Strategie für finanziellen Erfolg.",
    "questions": [
      {
        "id": "1",
        "question": "Welches Profil beschreibt dich am besten?",
        "options": [
          {
            "value": "student",
            "label": "Student/Studentin",
            "description": "Ich studiere noch und suche nach einem Nebenverdienst"
          },
          {
            "value": "employee",
            "label": "Angestellter/Angestellte",
            "description": "Ich arbeite Vollzeit und möchte mein Einkommen aufstocken"
          },
          {
            "value": "parent",
            "label": "Elternteil",
            "description": "Ich kümmere mich um die Familie und suche flexible Einkommensmöglichkeiten"
          }
        ]
      }
    ]
  }
}
```

**Beispiel:**
```bash
curl -X GET http://localhost:3000/api/quizzes/magic_tool
``` 