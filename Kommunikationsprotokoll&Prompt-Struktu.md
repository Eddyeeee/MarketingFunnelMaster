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