/**
 * RUM Metrics Collection API Endpoints
 * Tag 4: Advanced Monitoring Integration
 * 
 * Features:
 * - RUM data ingestion and storage
 * - Performance alert processing
 * - Business metrics correlation
 * - Real-time performance analysis
 */

import express from 'express';
import { z } from 'zod';
import rateLimit from 'express-rate-limit';

const router = express.Router();

// Rate limiting for metrics endpoints
const metricsRateLimit = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute per IP
  message: 'Too many metric submissions, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

// Validation schemas
const PerformanceMetricSchema = z.object({
  name: z.string(),
  value: z.number(),
  rating: z.enum(['good', 'needs-improvement', 'poor']),
  timestamp: z.number(),
  url: z.string().url(),
  userAgent: z.string(),
  connection: z.string().optional(),
  device: z.string().optional(),
  persona: z.string().optional(),
});

const BusinessMetricSchema = z.object({
  type: z.enum(['conversion', 'engagement', 'bounce', 'revenue']),
  value: z.number(),
  timestamp: z.number(),
  correlatedPerformance: z.array(PerformanceMetricSchema).optional(),
});

const RUMPayloadSchema = z.object({
  sessionId: z.string(),
  userId: z.string().optional(),
  persona: z.string().optional(),
  timestamp: z.number(),
  performanceMetrics: z.array(PerformanceMetricSchema),
  businessMetrics: z.array(BusinessMetricSchema),
  environment: z.string(),
  version: z.string().optional(),
  url: z.string().url(),
});

const PerformanceAlertSchema = z.object({
  type: z.string(),
  metric: z.string(),
  value: z.number(),
  threshold: z.number().optional(),
  url: z.string().url(),
  sessionId: z.string(),
  persona: z.string().optional(),
});

// In-memory storage for demonstration (replace with proper database)
interface StoredRUMData {
  id: string;
  sessionId: string;
  userId?: string;
  persona?: string;
  timestamp: number;
  performanceMetrics: any[];
  businessMetrics: any[];
  environment: string;
  version?: string;
  url: string;
  processedAt: number;
}

interface PerformanceAlert {
  id: string;
  type: string;
  metric: string;
  value: number;
  threshold?: number;
  url: string;
  sessionId: string;
  persona?: string;
  timestamp: number;
  acknowledged: boolean;
}

// In-memory stores (replace with database)
const rumDataStore: StoredRUMData[] = [];
const alertsStore: PerformanceAlert[] = [];
const metricsAggregation: Map<string, any> = new Map();

// Performance Budget Thresholds
const PERFORMANCE_BUDGETS = {
  'largest-contentful-paint': { good: 2500, poor: 4000 },
  'first-input-delay': { good: 100, poor: 300 },
  'cumulative-layout-shift': { good: 0.1, poor: 0.25 },
  'first-contentful-paint': { good: 1800, poor: 3000 },
  'time-to-first-byte': { good: 800, poor: 1800 },
};

// Utility functions
function generateId(): string {
  return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function calculatePerformanceScore(metrics: any[]): number {
  const weights = {
    'largest-contentful-paint': 0.25,
    'first-input-delay': 0.25,
    'cumulative-layout-shift': 0.15,
    'first-contentful-paint': 0.15,
    'time-to-first-byte': 0.20,
  };

  let totalScore = 0;
  let totalWeight = 0;

  metrics.forEach(metric => {
    const weight = weights[metric.name as keyof typeof weights];
    if (weight) {
      const budget = PERFORMANCE_BUDGETS[metric.name as keyof typeof PERFORMANCE_BUDGETS];
      if (budget) {
        // Convert metric value to score (0-100)
        let score = 100;
        if (metric.value > budget.good) {
          score = Math.max(0, 100 - ((metric.value - budget.good) / (budget.poor - budget.good)) * 50);
        }
        totalScore += score * weight;
        totalWeight += weight;
      }
    }
  });

  return totalWeight > 0 ? Math.round(totalScore / totalWeight) : 0;
}

function updateMetricsAggregation(data: StoredRUMData): void {
  const key = `${data.url}_${data.environment}_${data.persona || 'unknown'}`;
  
  if (!metricsAggregation.has(key)) {
    metricsAggregation.set(key, {
      url: data.url,
      environment: data.environment,
      persona: data.persona,
      sessions: 0,
      totalPerformanceScore: 0,
      avgPerformanceScore: 0,
      conversions: 0,
      bounces: 0,
      totalEngagementTime: 0,
      avgEngagementTime: 0,
      lastUpdated: Date.now(),
      coreWebVitals: {
        lcp: { values: [], avg: 0, p95: 0 },
        fid: { values: [], avg: 0, p95: 0 },
        cls: { values: [], avg: 0, p95: 0 },
        fcp: { values: [], avg: 0, p95: 0 },
        ttfb: { values: [], avg: 0, p95: 0 },
      }
    });
  }

  const aggregation = metricsAggregation.get(key)!;
  aggregation.sessions++;
  
  // Update performance metrics
  const performanceScore = calculatePerformanceScore(data.performanceMetrics);
  aggregation.totalPerformanceScore += performanceScore;
  aggregation.avgPerformanceScore = aggregation.totalPerformanceScore / aggregation.sessions;

  // Update Core Web Vitals
  data.performanceMetrics.forEach(metric => {
    if (aggregation.coreWebVitals[metric.name as keyof typeof aggregation.coreWebVitals]) {
      const vitals = aggregation.coreWebVitals[metric.name as keyof typeof aggregation.coreWebVitals];
      vitals.values.push(metric.value);
      vitals.avg = vitals.values.reduce((sum, val) => sum + val, 0) / vitals.values.length;
      vitals.p95 = calculatePercentile(vitals.values, 95);
    }
  });

  // Update business metrics
  data.businessMetrics.forEach(metric => {
    switch (metric.type) {
      case 'conversion':
        aggregation.conversions++;
        break;
      case 'bounce':
        aggregation.bounces++;
        break;
      case 'engagement':
        aggregation.totalEngagementTime += metric.value;
        aggregation.avgEngagementTime = aggregation.totalEngagementTime / aggregation.sessions;
        break;
    }
  });

  aggregation.lastUpdated = Date.now();
}

function calculatePercentile(values: number[], percentile: number): number {
  const sorted = values.slice().sort((a, b) => a - b);
  const index = Math.ceil((percentile / 100) * sorted.length) - 1;
  return sorted[index] || 0;
}

async function sendSlackAlert(alert: PerformanceAlert): Promise<void> {
  const webhookUrl = process.env.SLACK_WEBHOOK_URL;
  if (!webhookUrl) return;

  const message = {
    text: `🚨 Performance Alert: ${alert.metric}`,
    attachments: [
      {
        color: 'danger',
        fields: [
          { title: 'Metric', value: alert.metric, short: true },
          { title: 'Value', value: `${alert.value.toFixed(2)}ms`, short: true },
          { title: 'Threshold', value: `${alert.threshold}ms`, short: true },
          { title: 'URL', value: alert.url, short: false },
          { title: 'Persona', value: alert.persona || 'Unknown', short: true },
          { title: 'Session', value: alert.sessionId, short: true },
        ],
        footer: 'RUM Performance Monitor',
        ts: Math.floor(alert.timestamp / 1000)
      }
    ]
  };

  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message)
    });

    if (!response.ok) {
      console.error('Failed to send Slack alert:', response.status);
    }
  } catch (error) {
    console.error('Error sending Slack alert:', error);
  }
}

// Routes

/**
 * POST /api/metrics/rum
 * Collect RUM data from client applications
 */
router.post('/rum', metricsRateLimit, async (req, res) => {
  try {
    const validatedData = RUMPayloadSchema.parse(req.body);
    
    const storedData: StoredRUMData = {
      id: generateId(),
      ...validatedData,
      processedAt: Date.now()
    };

    // Store the data
    rumDataStore.push(storedData);

    // Update aggregations
    updateMetricsAggregation(storedData);

    // Check for performance budget violations
    validatedData.performanceMetrics.forEach(metric => {
      if (metric.rating === 'poor') {
        const alert: PerformanceAlert = {
          id: generateId(),
          type: 'budget_violation',
          metric: metric.name,
          value: metric.value,
          threshold: PERFORMANCE_BUDGETS[metric.name as keyof typeof PERFORMANCE_BUDGETS]?.poor,
          url: validatedData.url,
          sessionId: validatedData.sessionId,
          persona: validatedData.persona,
          timestamp: Date.now(),
          acknowledged: false
        };

        alertsStore.push(alert);
        
        // Send immediate notification
        sendSlackAlert(alert);
      }
    });

    console.log('📊 RUM data processed:', {
      sessionId: validatedData.sessionId,
      performanceMetrics: validatedData.performanceMetrics.length,
      businessMetrics: validatedData.businessMetrics.length,
      persona: validatedData.persona
    });

    res.status(200).json({
      success: true,
      id: storedData.id,
      processed: true
    });

  } catch (error) {
    console.error('Error processing RUM data:', error);
    
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: 'Invalid data format',
        details: error.errors
      });
    } else {
      res.status(500).json({
        success: false,
        error: 'Internal server error'
      });
    }
  }
});

/**
 * POST /api/alerts/performance
 * Handle immediate performance alerts
 */
router.post('/alerts/performance', async (req, res) => {
  try {
    const validatedAlert = PerformanceAlertSchema.parse(req.body);
    
    const alert: PerformanceAlert = {
      id: generateId(),
      ...validatedAlert,
      timestamp: Date.now(),
      acknowledged: false
    };

    alertsStore.push(alert);
    
    // Send notifications
    await sendSlackAlert(alert);

    console.log('🚨 Performance alert processed:', alert);

    res.status(200).json({
      success: true,
      alertId: alert.id
    });

  } catch (error) {
    console.error('Error processing performance alert:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to process alert'
    });
  }
});

/**
 * GET /api/metrics/dashboard
 * Get aggregated metrics for dashboard
 */
router.get('/dashboard', async (req, res) => {
  try {
    const { timeRange = '24h', environment, persona } = req.query;
    
    // Calculate time range filter
    const now = Date.now();
    const timeRangeMs = timeRange === '1h' ? 60 * 60 * 1000 :
                       timeRange === '24h' ? 24 * 60 * 60 * 1000 :
                       timeRange === '7d' ? 7 * 24 * 60 * 60 * 1000 :
                       24 * 60 * 60 * 1000;
    
    const startTime = now - timeRangeMs;

    // Filter data
    const filteredData = rumDataStore.filter(data => {
      if (data.timestamp < startTime) return false;
      if (environment && data.environment !== environment) return false;
      if (persona && data.persona !== persona) return false;
      return true;
    });

    // Calculate dashboard metrics
    const totalSessions = new Set(filteredData.map(d => d.sessionId)).size;
    const totalPageViews = filteredData.length;
    
    // Core Web Vitals aggregation
    const coreWebVitals = {
      lcp: { values: [] as number[], avg: 0, p95: 0 },
      fid: { values: [] as number[], avg: 0, p95: 0 },
      cls: { values: [] as number[], avg: 0, p95: 0 },
      fcp: { values: [] as number[], avg: 0, p95: 0 },
      ttfb: { values: [] as number[], avg: 0, p95: 0 },
    };

    filteredData.forEach(data => {
      data.performanceMetrics.forEach(metric => {
        if (coreWebVitals[metric.name as keyof typeof coreWebVitals]) {
          coreWebVitals[metric.name as keyof typeof coreWebVitals].values.push(metric.value);
        }
      });
    });

    // Calculate averages and percentiles
    Object.keys(coreWebVitals).forEach(key => {
      const values = coreWebVitals[key as keyof typeof coreWebVitals].values;
      if (values.length > 0) {
        coreWebVitals[key as keyof typeof coreWebVitals].avg = values.reduce((sum, val) => sum + val, 0) / values.length;
        coreWebVitals[key as keyof typeof coreWebVitals].p95 = calculatePercentile(values, 95);
      }
    });

    // Business metrics
    let conversions = 0;
    let bounces = 0;
    let totalEngagementTime = 0;

    filteredData.forEach(data => {
      data.businessMetrics.forEach(metric => {
        switch (metric.type) {
          case 'conversion':
            conversions++;
            break;
          case 'bounce':
            bounces++;
            break;
          case 'engagement':
            totalEngagementTime += metric.value;
            break;
        }
      });
    });

    const conversionRate = totalSessions > 0 ? (conversions / totalSessions) * 100 : 0;
    const bounceRate = totalSessions > 0 ? (bounces / totalSessions) * 100 : 0;
    const avgEngagementTime = totalSessions > 0 ? totalEngagementTime / totalSessions : 0;

    // Recent alerts
    const recentAlerts = alertsStore
      .filter(alert => alert.timestamp > startTime)
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 10);

    const dashboard = {
      summary: {
        totalSessions,
        totalPageViews,
        conversionRate: Math.round(conversionRate * 100) / 100,
        bounceRate: Math.round(bounceRate * 100) / 100,
        avgEngagementTime: Math.round(avgEngagementTime / 1000), // Convert to seconds
      },
      coreWebVitals: {
        lcp: {
          avg: Math.round(coreWebVitals.lcp.avg),
          p95: Math.round(coreWebVitals.lcp.p95),
          rating: coreWebVitals.lcp.avg <= PERFORMANCE_BUDGETS['largest-contentful-paint'].good ? 'good' :
                  coreWebVitals.lcp.avg <= PERFORMANCE_BUDGETS['largest-contentful-paint'].poor ? 'needs-improvement' : 'poor'
        },
        fid: {
          avg: Math.round(coreWebVitals.fid.avg),
          p95: Math.round(coreWebVitals.fid.p95),
          rating: coreWebVitals.fid.avg <= PERFORMANCE_BUDGETS['first-input-delay'].good ? 'good' :
                  coreWebVitals.fid.avg <= PERFORMANCE_BUDGETS['first-input-delay'].poor ? 'needs-improvement' : 'poor'
        },
        cls: {
          avg: Math.round(coreWebVitals.cls.avg * 1000) / 1000,
          p95: Math.round(coreWebVitals.cls.p95 * 1000) / 1000,
          rating: coreWebVitals.cls.avg <= PERFORMANCE_BUDGETS['cumulative-layout-shift'].good ? 'good' :
                  coreWebVitals.cls.avg <= PERFORMANCE_BUDGETS['cumulative-layout-shift'].poor ? 'needs-improvement' : 'poor'
        },
        fcp: {
          avg: Math.round(coreWebVitals.fcp.avg),
          p95: Math.round(coreWebVitals.fcp.p95),
          rating: coreWebVitals.fcp.avg <= PERFORMANCE_BUDGETS['first-contentful-paint'].good ? 'good' :
                  coreWebVitals.fcp.avg <= PERFORMANCE_BUDGETS['first-contentful-paint'].poor ? 'needs-improvement' : 'poor'
        },
        ttfb: {
          avg: Math.round(coreWebVitals.ttfb.avg),
          p95: Math.round(coreWebVitals.ttfb.p95),
          rating: coreWebVitals.ttfb.avg <= PERFORMANCE_BUDGETS['time-to-first-byte'].good ? 'good' :
                  coreWebVitals.ttfb.avg <= PERFORMANCE_BUDGETS['time-to-first-byte'].poor ? 'needs-improvement' : 'poor'
        }
      },
      alerts: {
        recent: recentAlerts,
        total: alertsStore.filter(alert => alert.timestamp > startTime).length,
        unacknowledged: alertsStore.filter(alert => alert.timestamp > startTime && !alert.acknowledged).length
      },
      timeRange,
      generatedAt: Date.now()
    };

    res.json(dashboard);

  } catch (error) {
    console.error('Error generating dashboard data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate dashboard data'
    });
  }
});

/**
 * GET /api/metrics/health
 * Health check endpoint for monitoring
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: Date.now(),
    metrics: {
      rumDataPoints: rumDataStore.length,
      alerts: alertsStore.length,
      aggregations: metricsAggregation.size
    }
  });
});

export default router;