Kommunikationsprotokoll & Prompt-Struktur der KI-Agenten
1. Grundlegendes Kommunikationsprinzip: Das "Digitale Auftragsticket"
Die Kommunikation zwischen den KI-Agenten erfolgt nicht durch formlose Text-Chats, sondern durch strukturierte Datenpakete, die wir "Digitales Auftragsticket" (DAT) nennen. Jedes Mal, wenn ein Agent eine Aufgabe an den nächsten übergibt, füllt er ein solches Ticket aus und sendet es über den n8n-Workflow weiter.

Dieses Vorgehen stellt sicher, dass jede Aufgabe alle notwendigen Informationen enthält, nachverfolgbar ist und die Ergebnisse konsistent sind. Das DAT ist im Wesentlichen ein JSON-Objekt.

1.1. Struktur eines Digitalen Auftragstickets (DAT)
Jedes DAT enthält die folgenden Felder:

{
  "ticketID": "PROJEKT-GARTEN-001-TEXT",
  "auftraggeber_agent": "KI-Gliederungs-Architekt",
  "empfaenger_agent": "KI-Texter (Kern-Autor)",
  "projekt_domain": "gruener-daumen-ki.de",
  "bezug_zu_persona": ["Gabi, 55, Hobby-Gärtnerin"],
  "kern_aufgabe": "Erstelle den Rohtext für einen Blogartikel basierend auf der bereitgestellten Gliederung.",
  "input_daten": {
    "titel": "Die 5 besten KI-Tools für deine Gartenplanung 2025",
    "gliederung": {
      "H1": "Die 5 besten KI-Tools für deine Gartenplanung 2025",
      "H2_1": "Warum KI die Gartenplanung revolutioniert",
      "H2_2": "Tool 1: [Name des Tools]",
      "H3_2_1": "Was kann das Tool?",
      "H3_2_2": "Für wen ist es ideal?",
      "H3_2_3": "Kosten und Affiliate-Link",
      "...": "weitere Tools",
      "H2_6": "Fazit: Dein Garten der Zukunft"
    },
    "seo_vorgaben": {
      "haupt_keyword": "KI Gartenplanung",
      "neben_keywords": ["Gartenplaner App", "Pflanzen erkennen KI", "automatisches Bewässerungssystem"],
      "wortanzahl_ziel": "ca. 1500 Wörter"
    },
    "affiliate_infos": [
      {"tool_name": "Tool X", "link": "partnerlink.xyz/tool-x", "usp": "Besonders einfache Bedienung"}
    ]
  },
  "output_anforderungen": {
    "format": "Markdown-Text",
    "tonalitaet": "Informativ, klar, einfach verständlich, direkt an 'Gabi' gerichtet (Du-Form).",
    "struktur": "Muss exakt der vorgegebenen Gliederung folgen. Alle H-Tags müssen als solche erkennbar sein."
  },
  "erfolgs_kriterien": [
    "Alle Punkte der Gliederung sind inhaltlich abgedeckt.",
    "Die SEO-Keywords sind natürlich im Text integriert.",
    "Der Text ist frei von Füllwörtern und sachlich korrekt."
  ],
  "status": "Offen"
}


2. Definierte Kommunikationsflüsse (Prompt-Ketten)
Hier sind die wichtigsten "Gespräche" als Abfolge von DAT-Übergaben definiert.

Fluss 1: Von der Idee zur Content-Planung
Dieser Fluss legt das Fundament für jeden neuen Inhalt.

KI-Nischen-Scout an KI-Strategie-Analyst

Kern-Aufgabe: "Bewerte das Potenzial der folgenden Nische."

Input-Daten: Nischen-Name, Suchvolumen-Trends, relevante Foren/Social-Media-Gruppen.

Output: DAT wird mit einer "Potenzial-Analyse" (Marktgröße, Wettbewerb) angereichert.

KI-Strategie-Analyst an KI-Persona-Psychologe

Kern-Aufgabe: "Erstelle 3-5 detaillierte Personas für die validierte Nische."

Input-Daten: Nischen-Analyse.

Output: DAT wird um detaillierte Persona-Profile erweitert.

KI-Strategie-Analyst an KI-Leiter für Monetarisierungsstrategie

Kern-Aufgabe: "Identifiziere Top-Monetarisierungs-Chancen für diese Nische und Personas."

Input-Daten: Nischen-Analyse, Persona-Profile.

Output: DAT wird um eine Liste potenzieller Affiliate-Programme und Ideen für eigene Produkte ergänzt.

Alle bisherigen Agenten an KI-Content-Stratege

Kern-Aufgabe: "Entwickle basierend auf allen vorliegenden Daten 5 konkrete Content-Ideen (Pillar-Content)."

Input-Daten: Das komplett angereicherte DAT.

Output: Eine Liste von 5 konkreten Artikel-/Video-Titeln mit kurzer Beschreibung des Ziels.

Fluss 2: Vom Plan zum fertigen Artikel (Der Produktions-Chat)
Dies ist der am häufigsten genutzte Kommunikationsfluss.

KI-Content-Stratege an KI-SEO-Stratege

Kern-Aufgabe: "Erstelle ein detailliertes SEO-Briefing für den folgenden Artikeltitel."

Input-Daten: Artikeltitel, Ziel-Persona, Domain.

Output: DAT wird um eine umfassende Keyword-Analyse und SERP-Analyse erweitert.

KI-SEO-Stratege an KI-Gliederungs-Architekt

Kern-Aufgabe: "Erstelle eine logische und SEO-optimierte Gliederung."

Input-Daten: Titel, Persona, SEO-Vorgaben.

Output: Das DAT erhält eine detaillierte gliederung (siehe Beispiel oben).

KI-Gliederungs-Architekt an KI-Texter (Kern-Autor)

Kern-Aufgabe: "Schreibe den Rohtext."

Input-Daten: Das komplette DAT mit Gliederung (siehe Beispiel oben).

Output: Der Rohtext wird dem DAT hinzugefügt.

KI-Texter an KI-Storyteller (Veredler)

Kern-Aufgabe: "Überarbeite diesen Rohtext. Füge Emotionen, eine persönliche Note und Storytelling-Elemente hinzu. Passe die Tonalität perfekt an die Persona 'Gabi' an."

Input-Daten: DAT mit Rohtext.

Output: Der Rohtext wird durch eine veredelte Version ersetzt.

KI-Storyteller an KI-Faktenchecker & Lektor

Kern-Aufgabe: "Prüfe alle Fakten (Preise, Features) und korrigiere Grammatik/Stil. Gib die finale Freigabe."

Input-Daten: DAT mit veredeltem Text.

Output: Der Text wird als "final geprüft" markiert.

KI-Faktenchecker an KI-CMS-Publisher und KI-Grafikdesigner (paralleler Auftrag)

An Publisher:

Kern-Aufgabe: "Publiziere diesen Artikel im CMS für die Domain X."

Input-Daten: Finaler Text, SEO-Metadaten.

Output: Artikel wird im CMS als Entwurf gespeichert.

An Grafikdesigner:

Kern-Aufgabe: "Erstelle ein Titelbild und 2 Infografiken für diesen Artikel."

Input-Daten: Finaler Text, Persona-Beschreibung (für den Stil).

Output: Bild-URLs werden dem DAT hinzugefügt und an den Publisher weitergeleitet.

3. Das Prinzip der "Konversation": Kontext und Klarheit
Jeder Agent "liest" das gesamte bisherige Ticket, um den vollen Kontext zu verstehen. Seine Antwort ist nicht nur der reine Output, sondern die Aktualisierung des Tickets selbst. Er fügt seine Arbeitsergebnisse hinzu und ändert den Status, bevor er es weiterleitet.

Durch diese strukturierte Vorgehensweise wird sichergestellt, dass die Kommunikation präzise, effizient und skalierbar ist. Jeder "Mitarbeiter" weiß genau, was von ihm erwartet wird, welche Informationen er erhält und in welchem Format er liefern muss. Dies ist die Grundlage, um Hunderte von Prozessen parallel und ohne Qualitätsverlust zu steuern.

## 2. ERWEITERTE AGENTEN-STRUKTUR (800-Website-Vision)

### **NEUE SPEZIALISTEN FÜR VIDEO-PRODUKTION:**

#### **16. VIDEO-STRATEGIE & KONZEPTION**
**Video Strategy & Concept Agent**
- **Aufgaben:** Video-Strategie, Konzept-Entwicklung, Storyboard-Planung, Multi-Format-Strategie
- **Input:** Content-Strategie, Personas, SEO-Daten, Trends
- **Output:** Video-Konzepte, Storyboards, Multi-Format-Pläne
- **Vernetzung:** ← Content-Strategie, → Video-Produktion, → Social Media

#### **17. VIDEO-SCRIPT & STORYBOARD**
**Video Script & Storyboard Agent**
- **Aufgaben:** Video-Scripts, Storyboards, Sprecher-Notizen, Timing
- **Input:** Video-Konzepte, Personas, SEO-Keywords
- **Output:** Detaillierte Scripts, Storyboards, Produktions-Anweisungen
- **Vernetzung:** ← Video-Strategie, → Video-Produktion, → Audio-Produktion

#### **18. VIDEO-PRODUKTION & ANIMATION**
**Video Production & Animation Agent**
- **Aufgaben:** Video-Erstellung, Animation, Motion Graphics, Visual Effects
- **Input:** Scripts, Storyboards, Brand-Guidelines, Assets
- **Output:** Fertige Videos, Animationen, Motion Graphics
- **Vernetzung:** ← Video-Script, → Video-Optimierung, → Content-Distribution

#### **19. AUDIO-PRODUKTION & VOICEOVER**
**Audio Production & Voiceover Agent**
- **Aufgaben:** Audio-Aufnahme, Voiceover, Sound Design, Musik-Auswahl
- **Input:** Scripts, Video-Content, Brand-Guidelines
- **Output:** Audio-Files, Voiceovers, Soundtracks
- **Vernetzung:** ← Video-Script, → Video-Produktion, → Podcast-Produktion

#### **20. VIDEO-OPTIMIERUNG & RENDERING**
**Video Optimization & Rendering Agent**
- **Aufgaben:** Video-Optimierung, Rendering, Format-Konvertierung, Quality Control
- **Input:** Roh-Videos, Platform-Anforderungen, Quality-Standards
- **Output:** Optimierte Videos, Multi-Format-Versionen
- **Vernetzung:** ← Video-Produktion, → Content-Distribution, → Analytics

### **NEUE SPEZIALISTEN FÜR SKALIERUNG:**

#### **21. MULTI-LANGUAGE & LOCALIZATION**
**Multi-Language & Localization Agent**
- **Aufgaben:** Übersetzung, Lokalisierung, Kultur-Anpassung, Multi-Sprach-Content
- **Input:** Original-Content, Ziel-Sprachen, Kultur-Kontext
- **Output:** Übersetzte Content, Lokalisierte Versionen
- **Vernetzung:** ← Content-Strategie, → SEO-Strategie, → Content-Distribution

#### **22. CONTENT-DISTRIBUTION & SYNDICATION**
**Content Distribution & Syndication Agent**
- **Aufgaben:** Content-Verteilung, Syndikation, Cross-Posting, Platform-Optimierung
- **Input:** Fertige Content, Platform-Anforderungen, Distribution-Strategien
- **Output:** Distribution-Pläne, Platform-spezifische Versionen
- **Vernetzung:** ← Alle Content-Agenten, → Social Media, → Analytics

#### **23. PERFORMANCE-OPTIMIERUNG & A/B-TESTING**
**Performance Optimization & A/B Testing Agent**
- **Aufgaben:** Performance-Tracking, A/B-Testing, Conversion-Optimierung, ROI-Analyse
- **Input:** Performance-Daten, Conversion-Metriken, Test-Ergebnisse
- **Output:** Optimierungs-Empfehlungen, A/B-Test-Pläne
- **Vernetzung:** ← Analytics, → Conversion-Optimierung, → Content-Strategie

#### **24. AUTOMATION-ENGINEERING & WORKFLOW-OPTIMIZATION**
**Automation Engineering & Workflow Optimization Agent**
- **Aufgaben:** Workflow-Automatisierung, Process-Optimierung, System-Integration
- **Input:** Workflow-Daten, Performance-Metriken, Automatisierungs-Anforderungen
- **Output:** Automatisierte Workflows, Process-Optimierungen
- **Vernetzung:** → Alle Abteilungen (Automatisierung)

#### **25. SCALABILITY & RESOURCE MANAGEMENT**
**Scalability & Resource Management Agent**
- **Aufgaben:** Ressourcen-Management, Skalierungs-Planung, Capacity-Planning
- **Input:** Resource-Usage, Growth-Projektionen, Performance-Daten
- **Output:** Skalierungs-Pläne, Resource-Allocation
- **Vernetzung:** ← CEO, → Technische Infrastruktur, → Analytics

## 3. ERWEITERTE KOMMUNIKATIONSFLÜSSE

### **Fluss 3: Video-Produktion (NEU)**
```
Video-Strategie → Video-Script → Video-Produktion → Audio-Produktion → Video-Optimierung → Content-Distribution
```

### **Fluss 4: Multi-Language-Content (NEU)**
```
Content-Strategie → Multi-Language → SEO-Strategie → Content-Distribution → Performance-Optimierung
```

### **Fluss 5: Skalierung & Automation (NEU)**
```
Analytics → Performance-Optimierung → Automation-Engineering → Scalability-Management → CEO
```

## 4. VIDEO-PRODUKTION DAT-STRUKTUR

```json
{
  "ticketID": "VIDEO-GARTEN-001",
  "auftraggeber_agent": "KI-Content-Stratege",
  "empfaenger_agent": "KI-Video-Strategie",
  "projekt_domain": "gruener-daumen-ki.de",
  "content_type": "Video",
  "video_format": ["YouTube", "Instagram", "TikTok"],
  "video_laenge": "3-5 Minuten",
  "bezug_zu_persona": ["Gabi, 55, Hobby-Gärtnerin"],
  "kern_aufgabe": "Erstelle ein Video-Konzept für 'Die 5 besten KI-Tools für Gartenplanung'",
  "input_daten": {
    "titel": "Die 5 besten KI-Tools für deine Gartenplanung 2025",
    "text_content": "Fertiger Artikel-Text",
    "seo_vorgaben": {
      "haupt_keyword": "KI Gartenplanung",
      "video_tags": ["Gartenplanung", "KI Tools", "Garten Apps"]
    },
    "platform_anforderungen": {
      "youtube": {"laenge": "5-7 min", "format": "16:9", "thumbnail": true},
      "instagram": {"laenge": "60 sec", "format": "9:16", "reels": true},
      "tiktok": {"laenge": "30-60 sec", "format": "9:16", "trending": true}
    }
  },
  "output_anforderungen": {
    "video_konzept": "Detailliertes Konzept mit Storyboard",
    "script": "Vollständiges Video-Script",
    "visual_style": "Modern, clean, garden-themed",
    "call_to_action": "Affiliate-Links in Beschreibung"
  },
  "erfolgs_kriterien": [
    "Video ist platform-optimiert",
    "SEO-Keywords sind integriert",
    "Call-to-Action ist klar",
    "Branding ist konsistent"
  ],
  "status": "Offen"
}
```

## 5. SKALIERUNGS-STRATEGIE FÜR 800 WEBSITES

### **PHASE 1: DACH-MARKT (Monat 1-6)**
- **Sprachen:** Deutsch, Englisch
- **Websites:** 50-100
- **Nischen:** 10-20
- **Video-Content:** 20% aller Content

### **PHASE 2: EUROPÄISCHE EXPANSION (Monat 7-12)**
- **Sprachen:** Deutsch, Englisch, Französisch, Spanisch, Italienisch
- **Websites:** 200-300
- **Nischen:** 30-50
- **Video-Content:** 30% aller Content

### **PHASE 3: GLOBALE EXPANSION (Monat 13-24)**
- **Sprachen:** 10+ Sprachen
- **Websites:** 500-800
- **Nischen:** 100+
- **Video-Content:** 40% aller Content

### **PHASE 4: AUTOMATION & AI-OPTIMIERUNG (Monat 25-36)**
- **Vollautomatisierte Content-Erstellung**
- **AI-gestützte Video-Produktion**
- **Predictive Analytics**
- **Autonomous Optimization**

## 6. HUMAN-IN-THE-LOOP ERWEITERUNG

### **NEUE KONTROLLPUNKTE:**
1. **Video-Konzept-Freigabe** (Video-Strategie → Human-Review)
2. **Script-Approval** (Video-Script → Human-Review)
3. **Video-Final-Cut** (Video-Optimierung → Human-Review)
4. **Multi-Language-Quality** (Multi-Language → Human-Review)
5. **Skalierungs-Entscheidungen** (Scalability → Human-Approval)

### **AUTOMATISIERUNGS-GRADE ERWEITERT:**
- **Vollautomatisiert:** Routine-Tasks, Monitoring, Reporting, Basic Video-Rendering
- **Semi-Automatisiert:** Content-Erstellung, Social Media, Email-Marketing, Video-Scripting
- **Human-Review:** Strategische Entscheidungen, Brand-Content, Video-Final-Cut, Multi-Language
- **Human-Entscheidung:** Nischen-Auswahl, Partner-Programme, Skalierungs-Entscheidungen

## 7. ERWARTETE ERGEBNISSE (ERWEITERT)

### **12 MONATE**
- 200-300 profitable Websites
- 50-100 etablierte Nischen
- €50.000-100.000 monatlicher Umsatz
- 30% Video-Content-Anteil

### **24 MONATE**
- 500-800 profitable Websites
- 100+ etablierte Nischen
- €200.000-500.000 monatlicher Umsatz
- 40% Video-Content-Anteil
- Multi-Sprach-Präsenz

### **36 MONATE**
- 800+ profitable Websites
- 200+ etablierte Nischen
- €1.000.000+ monatlicher Umsatz
- Vollautomatisierte Content-Erstellung
- Globale Marktführerschaft