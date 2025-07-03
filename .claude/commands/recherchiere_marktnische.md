# 🔍 RECHERCHIERE_MARKTNISCHE Command
## Vollautomatische Nischen-Analyse für digitales Imperium

---

## 📋 COMMAND STRUCTURE
```bash
claude research:niche [topic] [depth_level] [target_websites]
```

### **PARAMETER:**
- `topic`: Nischen-Thema (z.B. "nachhaltige Kaffeemaschinen")
- `depth_level`: basic|advanced|comprehensive
- `target_websites`: Anzahl geplanter Websites (1-50)

---

## 🎯 WORKFLOW SCHRITTE

### **SCHRITT 1: MARKET-INTELLIGENCE**
```python
# Google Gemini Agent Integration
market_data = GeminiAgent.analyze_market({
    'topic': input_topic,
    'search_volume': True,
    'competition_analysis': True, 
    'trend_analysis': True,
    'seasonal_patterns': True,
    'geographic_distribution': True
})
```

**Output:** Structured Market Report
- Suchvolumen (monatlich)
- Konkurrenz-Level (0-100)
- Trend-Direction (+/-/%)
- Seasonality-Patterns
- Top-Keywords (50+)

### **SCHRITT 2: AFFILIATE-OPPORTUNITY-SCAN**
```python
# Spezialisierte Affiliate-Research
affiliate_programs = AffiliateResearchAgent.scan_programs({
    'niche': market_data.niche,
    'min_commission': 20,
    'platforms': ['digistore24', 'clickbank', 'amazon', 'custom'],
    'product_types': ['digital', 'physical', 'software', 'courses']
})
```

**Output:** Top-10 Affiliate-Programs
- Kommission (%)
- EPC (Earnings per Click)
- Conversion-Rate
- Konkurrenzniveau
- Vendor-Reputation

### **SCHRITT 3: CONTENT-OPPORTUNITY-ANALYSIS**
```python
# Content-Gap-Analyse
content_gaps = ContentAnalysisAgent.find_gaps({
    'niche': market_data.niche,
    'competitor_content': True,
    'viral_potential': True,
    'seo_difficulty': True,
    'content_types': ['articles', 'videos', 'infographics', 'tools']
})
```

**Output:** Content-Opportunity-Matrix
- High-Impact-Keywords (Difficulty < 30)
- Viral-Content-Angles
- Underserved-Topics
- Content-Format-Recommendations

### **SCHRITT 4: DIGITAL-PRODUCT-POTENTIAL**
```python
# Produkt-Generierungs-Analyse
product_opportunities = ProductGeneratorAgent.analyze_potential({
    'niche': market_data.niche,
    'audience_pain_points': True,
    'existing_solutions': True,
    'price_sensitivity': True,
    'development_complexity': True
})
```

**Output:** Digital-Product-Roadmap
- Software-Tool-Ideen (MVPs)
- SaaS-Opportunities
- Template/Asset-Potential
- Estimated Development-Cost

### **SCHRITT 5: SCALING-PROJECTION**
```python
# Multi-Website-Strategie
scaling_plan = ScalingAgent.project_expansion({
    'base_niche': market_data.niche,
    'sub_niches': True,
    'geographic_expansion': True,
    'audience_segments': True,
    'target_websites': input_target_websites
})
```

**Output:** Skalierungs-Blueprint
- Sub-Nischen-Aufschlüsselung
- Domain-Strategien
- Content-Syndication-Plan
- Revenue-Projektion

---

## 📊 NISCHEN-BEWERTUNGS-ALGORITHMUS

### **SCORING-MATRIX (1-10 Scale):**
```python
def calculate_niche_score(market_data, affiliate_data, content_data, product_data):
    score = {
        'market_size': (search_volume / 100000) * 2,  # Max 2 points
        'competition': 2 - (competition_level / 50),   # Max 2 points (inverse)
        'monetization': (avg_commission * conversion_rate) / 10,  # Max 2 points
        'content_potential': content_gaps_count / 20,   # Max 2 points
        'scaling_potential': sub_niches_count / 10,     # Max 2 points
    }
    return min(sum(score.values()), 10)
```

### **BEWERTUNGS-KATEGORIEN:**
- **9-10**: 🚀 GOLDMINE - Sofort starten!
- **7-8**: 💰 PROFITABLE - Hohe Priorität
- **5-6**: ⚡ POTENTIAL - Überwachen
- **3-4**: ⚠️ RISIKO - Vorsichtig bewerten
- **1-2**: ❌ SKIP - Nicht verfolgen

---

## 📋 OUTPUT-FORMAT

### **EXECUTIVE SUMMARY:**
```json
{
  "niche": "nachhaltige-kaffeemaschinen",
  "overall_score": 8.7,
  "recommendation": "GOLDMINE",
  "estimated_revenue_potential": "€50k-100k/year per website",
  "competition_level": "medium",
  "time_to_profitability": "3-6 months",
  "scaling_potential": "high"
}
```

### **DETAILED ANALYSIS:**
```json
{
  "market_intelligence": {
    "monthly_searches": 45000,
    "trend_direction": "+23%",
    "seasonality": "Q4 peak",
    "top_keywords": [...],
    "competition_analysis": {...}
  },
  "monetization_opportunities": {
    "affiliate_programs": [...],
    "product_ideas": [...],
    "revenue_streams": [...]
  },
  "content_strategy": {
    "high_impact_topics": [...],
    "content_calendar": {...},
    "viral_angles": [...]
  },
  "scaling_blueprint": {
    "sub_niches": [...],
    "expansion_timeline": {...},
    "website_targets": {...}
  }
}
```

---

## 🚀 INTEGRATION MIT AGENT-NETZWERK

### **TRIGGER-EVENTS:**
- **Score > 8**: Automatischer Trigger für WebsiteGeneratorAgent
- **Score 6-8**: Hinzufügung zur Monitoring-Pipeline
- **Score < 6**: Archivierung mit Trend-Monitoring

### **FOLLOW-UP-ACTIONS:**
```python
if niche_score >= 8:
    DomainManagerAgent.register_domains(recommended_domains)
    WebsiteGeneratorAgent.queue_creation(niche_data)
    ContentWriterAgent.prepare_content_calendar(content_strategy)
    SEOOptimizationAgent.setup_tracking(keywords)
```

---

## ⚡ PERFORMANCE-TARGETS

### **SPEED-REQUIREMENTS:**
- **Basic Analysis**: < 5 Minuten
- **Advanced Analysis**: < 15 Minuten
- **Comprehensive Analysis**: < 30 Minuten

### **ACCURACY-TARGETS:**
- **Revenue-Prediction**: ±20% Accuracy
- **Competition-Assessment**: ±15% Accuracy
- **Trend-Prediction**: 80%+ Accuracy

---

**USAGE EXAMPLE:**
```bash
claude research:niche "Horoskop-Software" comprehensive 5
# → Vollständige Analyse für Horoskop-Software-Nische
# → Planung für 5 zusammenhängende Websites
# → Comprehensive Report mit allen Daten
```