import React from 'react';
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string[];
  canonicalUrl?: string;
  ogImage?: string;
  ogType?: 'website' | 'article' | 'product' | 'course';
  structuredData?: Record<string, any>;
  breadcrumbs?: Array<{ name: string; url: string }>;
  faqData?: Array<{ question: string; answer: string }>;
  productData?: {
    name: string;
    price: string;
    currency: string;
    availability: string;
    rating?: number;
    reviewCount?: number;
  };
  courseData?: {
    name: string;
    description: string;
    provider: string;
    duration?: string;
    difficulty?: string;
  };
}

export function SEOOptimizer({
  title = "Q-Money & Cash Maximus - Finanzielle Freiheit & Passives Einkommen",
  description = "Entdecke bewährte Strategien für 2.000-5.000€ passives Einkommen. Über 10.000 zufriedene Kunden. 30 Tage Geld-zurück-Garantie. Starte jetzt deinen Weg zur finanziellen Freiheit!",
  keywords = [
    "passives einkommen",
    "finanzielle freiheit", 
    "online geld verdienen",
    "cash maximus",
    "q-money",
    "affiliate marketing",
    "digitale produkte",
    "finanzielle unabhängigkeit",
    "nebenberuflich geld verdienen",
    "automatisierte einkommensströme"
  ],
  canonicalUrl = "https://q-money-system.com",
  ogImage = "https://q-money-system.com/og-image-optimized.jpg",
  ogType = "website",
  structuredData,
  breadcrumbs,
  faqData,
  productData,
  courseData
}: SEOProps) {

  // Generate comprehensive structured data
  const generateStructuredData = () => {
    const schemas = [];

    // Organization Schema
    schemas.push({
      "@context": "https://schema.org",
      "@type": "Organization",
      "@id": `${canonicalUrl}/#organization`,
      "name": "Q-Money & Cash Maximus",
      "url": canonicalUrl,
      "logo": {
        "@type": "ImageObject",
        "url": `${canonicalUrl}/logo-structured-data.png`,
        "width": 800,
        "height": 600
      },
      "description": "Führender Anbieter für finanzielle Bildung und passive Einkommensstrategien im deutschsprachigen Raum",
      "foundingDate": "2020",
      "numberOfEmployees": "11-50",
      "slogan": "Dein Weg zur finanziellen Freiheit",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+49-XXX-XXXXXXX",
        "contactType": "customer service",
        "availableLanguage": ["German"],
        "areaServed": ["DE", "AT", "CH"]
      },
      "sameAs": [
        "https://facebook.com/qmoney",
        "https://instagram.com/qmoney",
        "https://youtube.com/qmoney",
        "https://linkedin.com/company/qmoney",
        "https://twitter.com/qmoney"
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": "10000",
        "bestRating": "5",
        "worstRating": "1"
      }
    });

    // Website Schema
    schemas.push({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "@id": `${canonicalUrl}/#website`,
      "url": canonicalUrl,
      "name": "Q-Money System",
      "description": description,
      "publisher": {
        "@id": `${canonicalUrl}/#organization`
      },
      "potentialAction": [
        {
          "@type": "SearchAction",
          "target": {
            "@type": "EntryPoint",
            "urlTemplate": `${canonicalUrl}/search?q={search_term_string}`
          },
          "query-input": "required name=search_term_string"
        }
      ],
      "mainEntity": {
        "@type": "Course",
        "name": "Q-Money & Cash Maximus Komplettkurs",
        "description": "Umfassende Anleitung für den Aufbau passiver Einkommensströme",
        "provider": {
          "@id": `${canonicalUrl}/#organization`
        }
      }
    });

    // Course Schema (if courseData provided)
    if (courseData) {
      schemas.push({
        "@context": "https://schema.org",
        "@type": "Course",
        "name": courseData.name,
        "description": courseData.description,
        "provider": {
          "@type": "Organization",
          "name": courseData.provider,
          "sameAs": canonicalUrl
        },
        "hasCourseInstance": {
          "@type": "CourseInstance",
          "courseMode": "online",
          "courseWorkload": courseData.duration || "P30D",
          "instructor": {
            "@type": "Person",
            "name": "Q-Money Team"
          }
        },
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "EUR",
          "availability": "https://schema.org/InStock",
          "category": "Financial Education"
        },
        "educationalLevel": courseData.difficulty || "Beginner",
        "teaches": [
          "Passive Income Strategies",
          "Affiliate Marketing",
          "Digital Product Creation",
          "Financial Independence"
        ]
      });
    }

    // Product Schema (if productData provided)
    if (productData) {
      schemas.push({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": productData.name,
        "description": description,
        "brand": {
          "@type": "Brand",
          "name": "Q-Money"
        },
        "offers": {
          "@type": "Offer",
          "price": productData.price,
          "priceCurrency": productData.currency,
          "availability": `https://schema.org/${productData.availability}`,
          "seller": {
            "@id": `${canonicalUrl}/#organization`
          }
        },
        "aggregateRating": productData.rating ? {
          "@type": "AggregateRating",
          "ratingValue": productData.rating,
          "reviewCount": productData.reviewCount || 100
        } : undefined
      });
    }

    // FAQ Schema (if faqData provided)
    if (faqData && faqData.length > 0) {
      schemas.push({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqData.map(faq => ({
          "@type": "Question",
          "name": faq.question,
          "acceptedAnswer": {
            "@type": "Answer",
            "text": faq.answer
          }
        }))
      });
    }

    // Breadcrumb Schema (if breadcrumbs provided)
    if (breadcrumbs && breadcrumbs.length > 0) {
      schemas.push({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbs.map((crumb, index) => ({
          "@type": "ListItem",
          "position": index + 1,
          "name": crumb.name,
          "item": crumb.url
        }))
      });
    }

    // Custom structured data
    if (structuredData) {
      schemas.push(structuredData);
    }

    return schemas;
  };

  // Generate AI-optimized meta tags
  const generateAIOptimizedTags = () => {
    return {
      // Core meta tags
      title: title,
      description: description,
      keywords: keywords.join(', '),
      
      // AI-specific tags
      'ai:title': title,
      'ai:description': description,
      'ai:keywords': keywords.join(', '),
      'ai:content_type': 'financial_education',
      'ai:target_audience': 'adults_seeking_financial_freedom',
      'ai:expertise_level': 'beginner_to_advanced',
      'ai:language': 'de',
      'ai:region': 'DACH',
      
      // OpenAI/ChatGPT optimization
      'openai:title': title,
      'openai:description': description,
      'openai:content_category': 'finance,education,business',
      
      // Google AI optimization
      'google:content_type': 'educational',
      'google:audience': 'general',
      'google:content_rating': 'general',
      
      // Semantic web tags
      'semantic:topic': 'financial_education',
      'semantic:intent': 'educational,commercial',
      'semantic:entities': 'passive_income,financial_freedom,affiliate_marketing',
      
      // Content classification for AI
      'content:type': 'educational_course',
      'content:format': 'interactive_web_application',
      'content:difficulty': 'beginner_friendly',
      'content:duration': '30_days',
      'content:language': 'german',
      'content:region': 'germany,austria,switzerland'
    };
  };

  const aiOptimizedTags = generateAIOptimizedTags();
  const structuredDataSchemas = generateStructuredData();

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords.join(', ')} />
      <meta name="author" content="Q-Money & Cash Maximus Team" />
      <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
      <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
      <link rel="canonical" href={canonicalUrl} />

      {/* AI-Optimized Meta Tags */}
      {Object.entries(aiOptimizedTags).map(([key, value]) => (
        <meta key={key} name={key} content={value} />
      ))}

      {/* Open Graph Tags */}
      <meta property="og:type" content={ogType} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:image:alt" content={title} />
      <meta property="og:locale" content="de_DE" />
      <meta property="og:site_name" content="Q-Money System" />

      {/* Twitter Card Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:url" content={canonicalUrl} />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />
      <meta name="twitter:image:alt" content={title} />

      {/* Additional SEO Tags */}
      <meta name="format-detection" content="telephone=no" />
      <meta name="theme-color" content="#3b82f6" />
      <meta name="apple-mobile-web-app-capable" content="yes" />
      <meta name="apple-mobile-web-app-status-bar-style" content="default" />
      <meta name="apple-mobile-web-app-title" content="Q-Money" />

      {/* Structured Data */}
      {structuredDataSchemas.map((schema, index) => (
        <script 
          key={index}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ 
            __html: JSON.stringify(schema, null, 2) 
          }}
        />
      ))}

      {/* Preconnect for Performance */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      <link rel="preconnect" href="https://www.google-analytics.com" />
      <link rel="preconnect" href="https://googletagmanager.com" />

      {/* DNS Prefetch */}
      <link rel="dns-prefetch" href="//www.googletagmanager.com" />
      <link rel="dns-prefetch" href="//fonts.googleapis.com" />
      <link rel="dns-prefetch" href="//cdnjs.cloudflare.com" />

      {/* Additional AI/ML optimization hints */}
      <meta name="content-language" content="de" />
      <meta name="geo.region" content="DE" />
      <meta name="geo.placename" content="Deutschland" />
      <meta name="ICBM" content="51.1657, 10.4515" />
      
      {/* Rich Snippets Support */}
      <meta name="application-name" content="Q-Money System" />
      <meta name="msapplication-TileColor" content="#3b82f6" />
      <meta name="msapplication-config" content="/browserconfig.xml" />
      
      {/* AI Content Classification */}
      <meta name="content-classification" content="educational,financial,business" />
      <meta name="content-target-audience" content="adults" />
      <meta name="content-expertise-level" content="all-levels" />
      <meta name="content-primary-language" content="de" />
      <meta name="content-secondary-languages" content="en" />
    </Helmet>
  );
}

// SEO Hook for easy usage
export function useSEO(seoProps: SEOProps) {
  return <SEOOptimizer {...seoProps} />;
}

export default SEOOptimizer; 