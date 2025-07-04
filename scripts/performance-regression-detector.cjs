#!/usr/bin/env node

/**
 * Performance Regression Detection System
 * Phase 2: Performance Budget Hardening
 * 
 * Features:
 * - Compares performance metrics between baseline and current builds
 * - Detects regressions above configurable thresholds
 * - Generates detailed regression reports
 * - Provides optimization recommendations
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Command line argument parsing
const args = process.argv.slice(2);
const config = {
  baselineDir: null,
  currentDir: null,
  threshold: 10, // Default 10% regression threshold
  device: 'desktop',
  environment: 'production',
  outputFormat: 'console' // console, json, markdown
};

// Parse arguments
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--baseline':
      config.baselineDir = args[++i];
      break;
    case '--current':
      config.currentDir = args[++i];
      break;
    case '--threshold':
      config.threshold = parseFloat(args[++i]);
      break;
    case '--device':
      config.device = args[++i];
      break;
    case '--environment':
      config.environment = args[++i];
      break;
    case '--output':
      config.outputFormat = args[++i];
      break;
    case '--help':
      console.log(`
Performance Regression Detector

Usage: node performance-regression-detector.js [options]

Options:
  --baseline <dir>     Directory containing baseline Lighthouse reports
  --current <dir>      Directory containing current Lighthouse reports
  --threshold <num>    Regression threshold percentage (default: 10)
  --device <type>      Device type: mobile, desktop, tablet (default: desktop)
  --environment <env>  Environment: production, staging, development (default: production)
  --output <format>    Output format: console, json, markdown (default: console)
  --help              Show this help message
`);
      process.exit(0);
  }
}

// Validate required arguments
if (!config.baselineDir || !config.currentDir) {
  console.error('Error: --baseline and --current directories are required');
  process.exit(1);
}

// Performance metrics configuration
const METRICS_CONFIG = {
  'largest-contentful-paint': {
    name: 'Largest Contentful Paint (LCP)',
    unit: 'ms',
    lowerIsBetter: true,
    critical: true,
    thresholds: {
      good: 2500,
      needsImprovement: 4000
    }
  },
  'first-contentful-paint': {
    name: 'First Contentful Paint (FCP)',
    unit: 'ms',
    lowerIsBetter: true,
    critical: true,
    thresholds: {
      good: 1800,
      needsImprovement: 3000
    }
  },
  'total-blocking-time': {
    name: 'Total Blocking Time (TBT)',
    unit: 'ms',
    lowerIsBetter: true,
    critical: true,
    thresholds: {
      good: 200,
      needsImprovement: 600
    }
  },
  'cumulative-layout-shift': {
    name: 'Cumulative Layout Shift (CLS)',
    unit: '',
    lowerIsBetter: true,
    critical: true,
    thresholds: {
      good: 0.1,
      needsImprovement: 0.25
    }
  },
  'first-input-delay': {
    name: 'First Input Delay (FID)',
    unit: 'ms',
    lowerIsBetter: true,
    critical: true,
    thresholds: {
      good: 100,
      needsImprovement: 300
    }
  },
  'speed-index': {
    name: 'Speed Index',
    unit: 'ms',
    lowerIsBetter: true,
    critical: false,
    thresholds: {
      good: 3400,
      needsImprovement: 5800
    }
  },
  'interactive': {
    name: 'Time to Interactive (TTI)',
    unit: 'ms',
    lowerIsBetter: true,
    critical: false,
    thresholds: {
      good: 3800,
      needsImprovement: 7300
    }
  },
  'performance-score': {
    name: 'Performance Score',
    unit: '%',
    lowerIsBetter: false,
    critical: true,
    thresholds: {
      good: 90,
      needsImprovement: 50
    }
  }
};

// Load Lighthouse reports from directory
function loadReports(directory) {
  try {
    const files = fs.readdirSync(directory)
      .filter(file => file.endsWith('.json'))
      .map(file => path.join(directory, file));
    
    const reports = files.map(file => {
      const content = fs.readFileSync(file, 'utf8');
      return JSON.parse(content);
    });
    
    return reports;
  } catch (error) {
    console.error(`Error loading reports from ${directory}:`, error.message);
    return [];
  }
}

// Extract metrics from Lighthouse report
function extractMetrics(report) {
  const metrics = {};
  
  // Extract audit metrics
  Object.keys(METRICS_CONFIG).forEach(key => {
    if (key === 'performance-score') {
      metrics[key] = (report.categories?.performance?.score || 0) * 100;
    } else {
      metrics[key] = report.audits?.[key]?.numericValue || 0;
    }
  });
  
  // Extract additional metadata
  metrics.url = report.finalUrl || report.requestedUrl;
  metrics.timestamp = report.fetchTime;
  metrics.userAgent = report.userAgent;
  
  return metrics;
}

// Calculate regression percentage
function calculateRegression(baseline, current, lowerIsBetter = true) {
  if (baseline === 0) return current === 0 ? 0 : 100;
  
  const change = current - baseline;
  const percentage = (change / baseline) * 100;
  
  // For metrics where lower is better, positive change is bad (regression)
  // For metrics where higher is better, negative change is bad (regression)
  return lowerIsBetter ? percentage : -percentage;
}

// Analyze performance regression
function analyzeRegression(baselineReports, currentReports) {
  const analysis = {
    summary: {
      totalUrls: 0,
      regressedUrls: 0,
      improvedUrls: 0,
      criticalRegressions: 0,
      averageRegression: 0
    },
    urlAnalysis: [],
    recommendations: []
  };
  
  // Group reports by URL
  const baselineByUrl = {};
  const currentByUrl = {};
  
  baselineReports.forEach(report => {
    const metrics = extractMetrics(report);
    baselineByUrl[metrics.url] = metrics;
  });
  
  currentReports.forEach(report => {
    const metrics = extractMetrics(report);
    currentByUrl[metrics.url] = metrics;
  });
  
  // Compare metrics for each URL
  Object.keys(baselineByUrl).forEach(url => {
    if (!currentByUrl[url]) {
      console.warn(`Warning: No current report found for URL: ${url}`);
      return;
    }
    
    const baselineMetrics = baselineByUrl[url];
    const currentMetrics = currentByUrl[url];
    
    const urlAnalysis = {
      url,
      metrics: {},
      hasRegression: false,
      hasCriticalRegression: false,
      overallRegression: 0
    };
    
    let totalRegression = 0;
    let criticalRegressions = 0;
    
    // Analyze each metric
    Object.keys(METRICS_CONFIG).forEach(metricKey => {
      const metricConfig = METRICS_CONFIG[metricKey];
      const baselineValue = baselineMetrics[metricKey];
      const currentValue = currentMetrics[metricKey];
      
      const regression = calculateRegression(
        baselineValue,
        currentValue,
        metricConfig.lowerIsBetter
      );
      
      const hasRegression = regression > config.threshold;
      const isCriticalRegression = hasRegression && metricConfig.critical;
      
      urlAnalysis.metrics[metricKey] = {
        baseline: baselineValue,
        current: currentValue,
        regression: regression,
        hasRegression: hasRegression,
        isCritical: isCriticalRegression,
        threshold: metricConfig.thresholds,
        unit: metricConfig.unit
      };
      
      totalRegression += regression;
      
      if (isCriticalRegression) {
        criticalRegressions++;
      }
    });
    
    urlAnalysis.overallRegression = totalRegression / Object.keys(METRICS_CONFIG).length;
    urlAnalysis.hasRegression = Object.values(urlAnalysis.metrics).some(m => m.hasRegression);
    urlAnalysis.hasCriticalRegression = criticalRegressions > 0;
    
    analysis.urlAnalysis.push(urlAnalysis);
    analysis.summary.totalUrls++;
    
    if (urlAnalysis.hasRegression) {
      analysis.summary.regressedUrls++;
    }
    
    if (urlAnalysis.overallRegression < 0) {
      analysis.summary.improvedUrls++;
    }
    
    analysis.summary.criticalRegressions += criticalRegressions;
    analysis.summary.averageRegression += urlAnalysis.overallRegression;
  });
  
  analysis.summary.averageRegression /= analysis.summary.totalUrls;
  
  // Generate recommendations
  analysis.recommendations = generateRecommendations(analysis);
  
  return analysis;
}

// Generate optimization recommendations
function generateRecommendations(analysis) {
  const recommendations = [];
  
  // Analyze common regression patterns
  const commonIssues = {
    lcp: [],
    fcp: [],
    tbt: [],
    cls: []
  };
  
  analysis.urlAnalysis.forEach(urlAnalysis => {
    Object.keys(urlAnalysis.metrics).forEach(metricKey => {
      const metric = urlAnalysis.metrics[metricKey];
      
      if (metric.hasRegression && metric.isCritical) {
        switch (metricKey) {
          case 'largest-contentful-paint':
            commonIssues.lcp.push(urlAnalysis.url);
            break;
          case 'first-contentful-paint':
            commonIssues.fcp.push(urlAnalysis.url);
            break;
          case 'total-blocking-time':
            commonIssues.tbt.push(urlAnalysis.url);
            break;
          case 'cumulative-layout-shift':
            commonIssues.cls.push(urlAnalysis.url);
            break;
        }
      }
    });
  });
  
  // Generate specific recommendations
  if (commonIssues.lcp.length > 0) {
    recommendations.push({
      priority: 'HIGH',
      category: 'Largest Contentful Paint',
      description: 'LCP regression detected. Consider optimizing images, reducing server response time, or implementing preloading.',
      affectedUrls: commonIssues.lcp,
      actions: [
        'Optimize hero images with WebP format',
        'Implement critical resource preloading',
        'Reduce server response time (TTFB)',
        'Use CDN for static assets'
      ]
    });
  }
  
  if (commonIssues.fcp.length > 0) {
    recommendations.push({
      priority: 'HIGH',
      category: 'First Contentful Paint',
      description: 'FCP regression detected. Focus on critical rendering path optimization.',
      affectedUrls: commonIssues.fcp,
      actions: [
        'Inline critical CSS',
        'Reduce render-blocking resources',
        'Optimize web fonts loading',
        'Minimize HTML document size'
      ]
    });
  }
  
  if (commonIssues.tbt.length > 0) {
    recommendations.push({
      priority: 'HIGH',
      category: 'Total Blocking Time',
      description: 'TBT regression detected. JavaScript execution is blocking the main thread.',
      affectedUrls: commonIssues.tbt,
      actions: [
        'Split long tasks into smaller chunks',
        'Defer non-critical JavaScript',
        'Use Web Workers for heavy computations',
        'Optimize third-party scripts'
      ]
    });
  }
  
  if (commonIssues.cls.length > 0) {
    recommendations.push({
      priority: 'MEDIUM',
      category: 'Cumulative Layout Shift',
      description: 'CLS regression detected. Layout shifts are occurring during page load.',
      affectedUrls: commonIssues.cls,
      actions: [
        'Add size attributes to images and videos',
        'Reserve space for dynamic content',
        'Avoid inserting content above existing content',
        'Use CSS aspect-ratio for responsive media'
      ]
    });
  }
  
  return recommendations;
}

// Output formatters
function formatConsoleOutput(analysis) {
  console.log('\\n🎯 Performance Regression Analysis Report');
  console.log('=' .repeat(50));
  
  // Summary
  console.log('\\n📊 Summary:');
  console.log(`- Total URLs analyzed: ${analysis.summary.totalUrls}`);
  console.log(`- URLs with regressions: ${analysis.summary.regressedUrls}`);
  console.log(`- URLs with improvements: ${analysis.summary.improvedUrls}`);
  console.log(`- Critical regressions: ${analysis.summary.criticalRegressions}`);
  console.log(`- Average regression: ${analysis.summary.averageRegression.toFixed(2)}%`);
  
  // Detailed analysis
  console.log('\\n📋 Detailed Analysis:');
  analysis.urlAnalysis.forEach(urlAnalysis => {
    console.log(`\\n🔍 ${urlAnalysis.url}`);
    console.log(`   Overall regression: ${urlAnalysis.overallRegression.toFixed(2)}%`);
    
    Object.keys(urlAnalysis.metrics).forEach(metricKey => {
      const metric = urlAnalysis.metrics[metricKey];
      const metricConfig = METRICS_CONFIG[metricKey];
      
      if (metric.hasRegression) {
        const status = metric.isCritical ? '❌ CRITICAL' : '⚠️  WARNING';
        console.log(`   ${status} ${metricConfig.name}: ${metric.baseline.toFixed(1)}${metric.unit} → ${metric.current.toFixed(1)}${metric.unit} (+${metric.regression.toFixed(1)}%)`);
      }
    });
  });
  
  // Recommendations
  if (analysis.recommendations.length > 0) {
    console.log('\\n💡 Recommendations:');
    analysis.recommendations.forEach(rec => {
      console.log(`\\n🔧 ${rec.priority} - ${rec.category}`);
      console.log(`   ${rec.description}`);
      console.log(`   Affected URLs: ${rec.affectedUrls.length}`);
      console.log('   Actions:');
      rec.actions.forEach(action => {
        console.log(`     • ${action}`);
      });
    });
  }
}

function formatJsonOutput(analysis) {
  console.log(JSON.stringify(analysis, null, 2));
}

function formatMarkdownOutput(analysis) {
  let output = '# Performance Regression Analysis Report\\n\\n';
  
  // Summary
  output += '## 📊 Summary\\n\\n';
  output += `- **Total URLs analyzed:** ${analysis.summary.totalUrls}\\n`;
  output += `- **URLs with regressions:** ${analysis.summary.regressedUrls}\\n`;
  output += `- **URLs with improvements:** ${analysis.summary.improvedUrls}\\n`;
  output += `- **Critical regressions:** ${analysis.summary.criticalRegressions}\\n`;
  output += `- **Average regression:** ${analysis.summary.averageRegression.toFixed(2)}%\\n\\n`;
  
  // Detailed analysis
  output += '## 📋 Detailed Analysis\\n\\n';
  analysis.urlAnalysis.forEach(urlAnalysis => {
    output += `### ${urlAnalysis.url}\\n\\n`;
    output += `**Overall regression:** ${urlAnalysis.overallRegression.toFixed(2)}%\\n\\n`;
    
    output += '| Metric | Baseline | Current | Regression | Status |\\n';
    output += '|--------|----------|---------|------------|--------|\\n';
    
    Object.keys(urlAnalysis.metrics).forEach(metricKey => {
      const metric = urlAnalysis.metrics[metricKey];
      const metricConfig = METRICS_CONFIG[metricKey];
      
      const status = metric.hasRegression ? 
        (metric.isCritical ? '❌ CRITICAL' : '⚠️ WARNING') : 
        '✅ OK';
      
      output += `| ${metricConfig.name} | ${metric.baseline.toFixed(1)}${metric.unit} | ${metric.current.toFixed(1)}${metric.unit} | ${metric.regression.toFixed(1)}% | ${status} |\\n`;
    });
    
    output += '\\n';
  });
  
  // Recommendations
  if (analysis.recommendations.length > 0) {
    output += '## 💡 Recommendations\\n\\n';
    analysis.recommendations.forEach(rec => {
      output += `### ${rec.priority} - ${rec.category}\\n\\n`;
      output += `${rec.description}\\n\\n`;
      output += `**Affected URLs:** ${rec.affectedUrls.length}\\n\\n`;
      output += '**Actions:**\\n';
      rec.actions.forEach(action => {
        output += `- ${action}\\n`;
      });
      output += '\\n';
    });
  }
  
  console.log(output);
}

// Main execution
function main() {
  console.log('🔍 Loading performance reports...');
  
  const baselineReports = loadReports(config.baselineDir);
  const currentReports = loadReports(config.currentDir);
  
  if (baselineReports.length === 0) {
    console.error('Error: No baseline reports found');
    process.exit(1);
  }
  
  if (currentReports.length === 0) {
    console.error('Error: No current reports found');
    process.exit(1);
  }
  
  console.log(`📊 Analyzing ${baselineReports.length} baseline reports vs ${currentReports.length} current reports...`);
  
  const analysis = analyzeRegression(baselineReports, currentReports);
  
  // Output results
  switch (config.outputFormat) {
    case 'json':
      formatJsonOutput(analysis);
      break;
    case 'markdown':
      formatMarkdownOutput(analysis);
      break;
    default:
      formatConsoleOutput(analysis);
  }
  
  // Exit with error code if critical regressions found
  if (analysis.summary.criticalRegressions > 0) {
    console.error(`\\n❌ ${analysis.summary.criticalRegressions} critical performance regressions detected!`);
    process.exit(1);
  }
  
  console.log('\\n✅ Performance regression analysis completed successfully');
}

// Run the script
if (require.main === module) {
  main();
}

module.exports = {
  analyzeRegression,
  extractMetrics,
  calculateRegression,
  generateRecommendations
};