# 📝 ERSTELLE_ARTIKEL Command
## KI-gestützte Content-Erstellung für Maximum-Impact

---

## 📋 COMMAND STRUCTURE
```bash
claude content:create [keyword] [audience] [content_type] [optimization_level]
```

### **PARAMETER:**
- `keyword`: Haupt-Keyword (z.B. "beste Kaffeemaschine 2025")
- `audience`: Zielgruppe (z.B. "FeierabendKapital", "StarterKapital")
- `content_type`: article|vsl|landing|review|comparison
- `optimization_level`: seo|conversion|viral

---

## 🎯 MULTI-AGENT WORKFLOW

### **PHASE 1: INTELLIGENT RESEARCH**
```python
# Schritt 1: Blitz-Nischen-Analyse
niche_context = NicheResearchAgent.quick_analysis({
    'keyword': input_keyword,
    'audience': input_audience,
    'depth': 'contextual',
    'competitor_content': True,
    'trending_angles': True
})
```

**Output:** Content-Context-Brief
- Keyword-Difficulty & Volume
- Top-3 Competitor-Analysis
- Trending-Content-Angles
- Audience-Pain-Points
- Monetization-Opportunities

### **PHASE 2: STRATEGIC OUTLINE**
```python
# Schritt 2: Content-Architektur
outline = ContentOutlineAgent.create_structure({
    'keyword': input_keyword,
    'audience_persona': niche_context.audience,
    'content_type': input_content_type,
    'optimization_target': input_optimization_level,
    'competitor_gaps': niche_context.content_gaps,
    'viral_elements': True
})
```

**Output:** Strategic Content-Outline
- Hook-optimierte Überschrift
- Emotional-Story-Arc
- Trust-Building-Elemente
- Call-to-Action-Placement
- SEO-optimierte Struktur

### **PHASE 3: APPROVAL GATE**
```python
# Business Manager Approval
approval = BusinessManagerAgent.review_outline({
    'outline': outline,
    'strategic_fit': True,
    'roi_potential': True,
    'brand_alignment': True,
    'scaling_potential': True
})

if not approval.approved:
    return optimization_suggestions
```

### **PHASE 4: CONTENT CREATION**
```python
# Schritt 3: Multi-Layer Content Generation
content = ContentWriterAgent.generate_content({
    'outline': approved_outline,
    'writing_style': audience_persona.voice,
    'optimization_target': input_optimization_level,
    'sales_psychology': True,
    'storytelling_elements': True,
    'proof_elements': True
})
```

**Output:** High-Converting Content
- Emotional-Hook-Intro
- Value-Packed-Content
- Trust-Signals integriert
- Natural-CTA-Integration
- Scannable-Format

### **PHASE 5: SEO SUPERCHARGING**
```python
# Schritt 4: Technical SEO Optimization  
seo_optimized = SEOOptimizationAgent.enhance_content({
    'content': content,
    'target_keyword': input_keyword,
    'related_keywords': niche_context.keywords,
    'internal_linking': True,
    'schema_markup': True,
    'featured_snippet_optimization': True
})
```

**Output:** SEO-Powerhouse Content
- Perfect-Keyword-Density
- Related-Keywords integriert
- Meta-Tags optimiert
- Internal-Linking-Strategy
- Featured-Snippet-ready

### **PHASE 6: VISUAL ENHANCEMENT**
```python
# Schritt 5: Visual Content Creation
visuals = VisualContentAgent.create_assets({
    'content': seo_optimized_content,
    'brand_style': audience_persona.visual_style,
    'social_media_variants': True,
    'infographic_elements': True,
    'video_thumbnails': True
})
```

**Output:** Complete Visual Package
- Hero-Image (optimiert)
- Social-Media-Variants
- Infographic-Elements
- Pinterest-optimized Graphics
- Video-Thumbnail (falls VSL)

---

## 📊 CONTENT-TYPES & SPECIALIZATIONS

### **ARTICLE (Standard Blog Content):**
```python
article_config = {
    'length': '2000-3500 words',
    'structure': 'Problem-Agitate-Solve',
    'cta_placement': 'multiple_natural',
    'trust_signals': 'testimonials_stats',
    'optimization': 'seo_first'
}
```

### **VSL (Video Sales Letter Content):**
```python
vsl_config = {
    'format': 'script_with_visuals',
    'length': '15-25 minutes',
    'structure': 'attention_interest_desire_action',
    'psychological_triggers': 'scarcity_authority_social_proof',
    'optimization': 'conversion_first'
}
```

### **LANDING (Landing Page Content):**
```python
landing_config = {
    'format': 'conversion_optimized',
    'structure': 'hero_benefits_proof_cta',
    'length': '1000-2000 words',
    'trust_elements': 'guarantees_testimonials',
    'optimization': 'conversion_maximum'
}
```

### **REVIEW (Product Review Content):**
```python
review_config = {
    'format': 'honest_comprehensive',
    'structure': 'overview_pros_cons_verdict',
    'affiliate_integration': 'natural_contextual',
    'trust_building': 'personal_experience',
    'optimization': 'trust_conversion_balance'
}
```

---

## 🎆 OPTIMIZATION-LEVELS

### **SEO-OPTIMIZATION:**
- **Focus**: Organic Traffic Maximum
- **Keyword-Density**: 1-2% (natural)
- **Structure**: H1-H6 Hierarchy perfekt
- **Internal-Links**: 3-5 pro 1000 Wörter
- **External-Authority**: 2-3 High-DA Links

### **CONVERSION-OPTIMIZATION:**
- **Focus**: Revenue Maximum
- **Psychology-Triggers**: Scarcity, Authority, Social Proof
- **CTA-Density**: Every 300-500 words
- **Trust-Signals**: Testimonials, Guarantees, Stats
- **Urgency-Elements**: Limited-Time, Bonus-Offers

### **VIRAL-OPTIMIZATION:**
- **Focus**: Social-Sharing Maximum
- **Emotional-Hooks**: Surprise, Anger, Joy, Fear
- **Share-Triggers**: Quotable-Moments, Statistics
- **Social-Proof**: "People like you" Elements
- **Platform-Specific**: Twitter, Instagram, Pinterest variants

---

## 📦 OUTPUT-PACKAGE

### **COMPLETE CONTENT PACKAGE:**
```json
{
  "main_content": {
    "title": "optimized_headline",
    "content": "full_article_html",
    "word_count": 2847,
    "reading_time": "12 minutes",
    "seo_score": 94
  },
  "meta_data": {
    "meta_title": "seo_optimized_title",
    "meta_description": "compelling_description",
    "focus_keyword": "primary_keyword",
    "secondary_keywords": [...]
  },
  "visual_assets": {
    "hero_image": "path/to/hero.jpg",
    "social_variants": {...},
    "infographics": [...]
  },
  "promotion_ready": {
    "social_posts": {...},
    "email_subject_lines": [...],
    "pinterest_descriptions": [...]
  },
  "monetization": {
    "affiliate_links": [...],
    "cta_buttons": [...],
    "upsell_opportunities": [...]
  }
}
```

---

## 🚀 AUTOMATION & SCALING

### **BATCH-PROCESSING:**
```bash
# Multiple Articles gleichzeitig
claude content:batch [
  {"keyword": "beste Kaffeemaschine", "audience": "FeierabendKapital"},
  {"keyword": "Kaffeemaschine Test", "audience": "StarterKapital"},
  {"keyword": "Espressomaschine kaufen", "audience": "RemoteCashflow"}
]
```

### **TEMPLATE-LEARNING:**
- **Pattern-Recognition**: Lernt aus erfolgreichen Contents
- **Style-Adaptation**: Passt sich an Audience-Preferences an
- **Performance-Optimization**: Optimiert basierend auf Conversion-Data

### **QUALITY-ASSURANCE:**
```python
quality_gates = {
    'plagiarism_check': '< 5% similarity',
    'readability_score': '> 60 Flesch',
    'seo_score': '> 80',
    'conversion_elements': '> 5 CTAs',
    'trust_signals': '> 3 elements'
}
```

---

## ⚡ PERFORMANCE TARGETS

### **SPEED-BENCHMARKS:**
- **Research + Outline**: < 3 Minuten
- **Content Creation**: < 8 Minuten
- **SEO Optimization**: < 2 Minuten
- **Visual Creation**: < 5 Minuten
- **Total Time**: < 20 Minuten pro Artikel

### **QUALITY-BENCHMARKS:**
- **SEO-Score**: > 85/100
- **Readability**: 60-80 Flesch Score
- **Conversion-Rate**: > 3% (Industrie-Standard: 1-2%)
- **Social-Shares**: > 50 Shares pro 1000 Views

---

**USAGE EXAMPLES:**
```bash
# Standard SEO Article
claude content:create "beste Kaffeemaschine 2025" "FeierabendKapital" article seo

# High-Converting Landing Page
claude content:create "Q-Money Kurs" "StarterKapital" landing conversion

# Viral Social Content
claude content:create "Kaffee Mythen" "RemoteCashflow" article viral
```