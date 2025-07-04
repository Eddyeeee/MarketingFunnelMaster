#!/usr/bin/env node

/**
 * Performance Budget Manager with Context-aware Flexibility
 * Phase 2: Performance Budget Hardening
 * 
 * Features:
 * - Dynamic budget adjustment based on context
 * - Marketing campaign mode with relaxed budgets
 * - Critical bug fix mode with performance validation bypass
 * - Feature flag integration for selective budget enforcement
 * - Emergency deployment handling
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const CONFIG_FILE = path.join(__dirname, '..', 'performance-budget-config.json');
const LIGHTHOUSE_CONFIG_FILE = path.join(__dirname, '..', 'lighthouse-budgets.config.js');

// Default configuration
const DEFAULT_CONFIG = {
  contextualBudgets: {
    // Marketing campaign mode - relaxed budgets for traffic spikes
    marketing: {
      description: 'Marketing campaign mode - optimized for traffic handling',
      budgetMultiplier: 1.3, // 30% more lenient
      duration: 7200000, // 2 hours in milliseconds
      triggers: ['campaign-launch', 'traffic-spike', 'viral-content'],
      notifications: ['slack', 'email']
    },
    
    // Critical bug fix mode - bypass performance validation
    hotfix: {
      description: 'Critical bug fix mode - performance validation bypassed',
      budgetMultiplier: 2.0, // Very lenient
      duration: 3600000, // 1 hour in milliseconds
      triggers: ['security-patch', 'critical-bug', 'payment-issue'],
      notifications: ['slack', 'pagerduty', 'email'],
      requiresApproval: true
    },
    
    // Feature rollout mode - gradual budget tightening
    rollout: {
      description: 'Feature rollout mode - gradual budget enforcement',
      budgetMultiplier: 1.5, // 50% more lenient initially
      duration: 86400000, // 24 hours in milliseconds
      triggers: ['feature-flag', 'a-b-test', 'gradual-rollout'],
      notifications: ['slack']
    },
    
    // Load testing mode - very strict budgets
    load_test: {
      description: 'Load testing mode - strict performance validation',
      budgetMultiplier: 0.8, // 20% stricter
      duration: 1800000, // 30 minutes in milliseconds
      triggers: ['load-test', 'performance-test', 'stress-test'],
      notifications: ['slack']
    }
  },
  
  // Feature flag integration
  featureFlags: {
    enableContextualBudgets: true,
    enableEmergencyBypass: true,
    enableAutomaticAdjustment: true,
    enableBusinessImpactTracking: true
  },
  
  // Alert thresholds
  alertThresholds: {
    budgetViolationRate: 0.1, // 10%
    regressionThreshold: 0.15, // 15%
    criticalMetricsCount: 2
  },
  
  // Integration endpoints
  integrations: {
    slack: {
      enabled: true,
      webhook: process.env.SLACK_WEBHOOK_URL
    },
    pagerduty: {
      enabled: false,
      apiKey: process.env.PAGERDUTY_API_KEY
    },
    email: {
      enabled: false,
      smtp: process.env.SMTP_CONFIG
    }
  }
};

// Load configuration
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      const configData = fs.readFileSync(CONFIG_FILE, 'utf8');
      return { ...DEFAULT_CONFIG, ...JSON.parse(configData) };
    }
  } catch (error) {
    console.warn('Warning: Could not load configuration file, using defaults');
  }
  return DEFAULT_CONFIG;
}

// Save configuration
function saveConfig(config) {
  try {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
    console.log('Configuration saved successfully');
  } catch (error) {
    console.error('Error saving configuration:', error.message);
  }
}

// Detect current context
function detectContext() {
  const context = {
    mode: 'normal',
    triggers: [],
    confidence: 0,
    metadata: {}
  };
  
  // Check environment variables for context hints
  const gitMessage = process.env.GIT_COMMIT_MESSAGE || '';
  const branchName = process.env.GITHUB_REF_NAME || process.env.BRANCH || '';
  const prTitle = process.env.PR_TITLE || '';
  const labels = process.env.PR_LABELS || '';
  
  // Marketing context detection
  const marketingKeywords = ['campaign', 'marketing', 'traffic', 'viral', 'promotion'];
  if (marketingKeywords.some(keyword => 
    gitMessage.toLowerCase().includes(keyword) || 
    branchName.toLowerCase().includes(keyword) ||
    prTitle.toLowerCase().includes(keyword)
  )) {
    context.mode = 'marketing';
    context.triggers.push('marketing-detected');
    context.confidence += 0.7;
  }
  
  // Hotfix context detection
  const hotfixKeywords = ['hotfix', 'urgent', 'critical', 'security', 'patch', 'emergency'];
  if (hotfixKeywords.some(keyword => 
    gitMessage.toLowerCase().includes(keyword) || 
    branchName.toLowerCase().includes(keyword) ||
    labels.toLowerCase().includes(keyword)
  )) {
    context.mode = 'hotfix';
    context.triggers.push('hotfix-detected');
    context.confidence += 0.9;
  }
  
  // Feature rollout context detection
  const rolloutKeywords = ['rollout', 'feature', 'experiment', 'test', 'gradual'];
  if (rolloutKeywords.some(keyword => 
    gitMessage.toLowerCase().includes(keyword) || 
    branchName.toLowerCase().includes(keyword)
  )) {
    context.mode = 'rollout';
    context.triggers.push('rollout-detected');
    context.confidence += 0.6;
  }
  
  // Load test context detection
  const loadTestKeywords = ['load-test', 'performance-test', 'stress-test', 'benchmark'];
  if (loadTestKeywords.some(keyword => 
    gitMessage.toLowerCase().includes(keyword) || 
    branchName.toLowerCase().includes(keyword)
  )) {
    context.mode = 'load_test';
    context.triggers.push('load-test-detected');
    context.confidence += 0.8;
  }
  
  // Add metadata
  context.metadata = {
    gitMessage,
    branchName,
    prTitle,
    labels,
    timestamp: new Date().toISOString()
  };
  
  return context;
}

// Adjust budget based on context
function adjustBudgetForContext(baseBudget, context, config) {
  if (context.mode === 'normal' || context.confidence < 0.5) {
    return baseBudget;
  }
  
  const contextConfig = config.contextualBudgets[context.mode];
  if (!contextConfig) {
    console.warn(`Warning: No configuration found for context mode: ${context.mode}`);
    return baseBudget;
  }
  
  console.log(`🎯 Adjusting budget for context: ${context.mode}`);
  console.log(`   Description: ${contextConfig.description}`);
  console.log(`   Multiplier: ${contextConfig.budgetMultiplier}`);
  console.log(`   Duration: ${contextConfig.duration / 1000}s`);
  
  // Apply multiplier to numeric budget values
  const adjustedBudget = { ...baseBudget };
  
  Object.keys(adjustedBudget).forEach(key => {
    if (Array.isArray(adjustedBudget[key]) && adjustedBudget[key].length === 2) {
      const [severity, config] = adjustedBudget[key];
      
      if (config && typeof config === 'object' && config.maxNumericValue) {
        // Adjust maxNumericValue (higher is more lenient for performance metrics)
        adjustedBudget[key] = [
          severity,
          {
            ...config,
            maxNumericValue: Math.round(config.maxNumericValue * contextConfig.budgetMultiplier)
          }
        ];
      } else if (config && typeof config === 'object' && config.minScore) {
        // Adjust minScore (lower is more lenient for score-based metrics)
        adjustedBudget[key] = [
          severity,
          {
            ...config,
            minScore: Math.max(0, config.minScore / contextConfig.budgetMultiplier)
          }
        ];
      }
    }
  });
  
  return adjustedBudget;
}

// Send notifications
async function sendNotifications(context, config, message) {
  const contextConfig = config.contextualBudgets[context.mode];
  if (!contextConfig || !contextConfig.notifications) {
    return;
  }
  
  for (const notificationType of contextConfig.notifications) {
    switch (notificationType) {
      case 'slack':
        await sendSlackNotification(message, config);
        break;
      case 'pagerduty':
        await sendPagerDutyAlert(message, config);
        break;
      case 'email':
        await sendEmailNotification(message, config);
        break;
    }
  }
}

// Slack notification
async function sendSlackNotification(message, config) {
  if (!config.integrations.slack.enabled || !config.integrations.slack.webhook) {
    return;
  }
  
  try {
    const { spawn } = require('child_process');
    const curl = spawn('curl', [
      '-X', 'POST',
      '-H', 'Content-type: application/json',
      '--data', JSON.stringify({
        text: message,
        username: 'Performance Budget Manager',
        icon_emoji: ':chart_with_upwards_trend:'
      }),
      config.integrations.slack.webhook
    ]);
    
    curl.on('close', (code) => {
      if (code === 0) {
        console.log('✅ Slack notification sent');
      } else {
        console.error('❌ Failed to send Slack notification');
      }
    });
  } catch (error) {
    console.error('Error sending Slack notification:', error.message);
  }
}

// PagerDuty alert (placeholder)
async function sendPagerDutyAlert(message, config) {
  if (!config.integrations.pagerduty.enabled) {
    return;
  }
  
  console.log('📟 PagerDuty alert would be sent:', message);
  // Implement PagerDuty integration if needed
}

// Email notification (placeholder)
async function sendEmailNotification(message, config) {
  if (!config.integrations.email.enabled) {
    return;
  }
  
  console.log('📧 Email notification would be sent:', message);
  // Implement email integration if needed
}

// Generate context-aware Lighthouse configuration
function generateLighthouseConfig(context, config) {
  const baseLighthouseConfig = require(LIGHTHOUSE_CONFIG_FILE);
  
  // Get base budget assertions
  const baseAssertions = baseLighthouseConfig.ci.assert.assertions;
  
  // Apply context-based adjustments
  const adjustedAssertions = adjustBudgetForContext(baseAssertions, context, config);
  
  // Create new configuration
  const contextualConfig = {
    ...baseLighthouseConfig,
    ci: {
      ...baseLighthouseConfig.ci,
      assert: {
        assertions: adjustedAssertions
      }
    },
    _contextualMetadata: {
      context: context.mode,
      confidence: context.confidence,
      triggers: context.triggers,
      adjustmentApplied: context.mode !== 'normal',
      timestamp: new Date().toISOString()
    }
  };
  
  return contextualConfig;
}

// Main command handlers
const commands = {
  detect: () => {
    const context = detectContext();
    console.log('🔍 Context Detection Results:');
    console.log(`   Mode: ${context.mode}`);
    console.log(`   Confidence: ${(context.confidence * 100).toFixed(1)}%`);
    console.log(`   Triggers: ${context.triggers.join(', ') || 'none'}`);
    console.log(`   Metadata: ${JSON.stringify(context.metadata, null, 2)}`);
  },
  
  adjust: () => {
    const config = loadConfig();
    const context = detectContext();
    
    console.log('🎯 Generating context-aware Lighthouse configuration...');
    
    const contextualConfig = generateLighthouseConfig(context, config);
    
    // Save the contextual configuration
    const contextualConfigPath = path.join(__dirname, '..', 'lighthouse-contextual.config.js');
    const configContent = `module.exports = ${JSON.stringify(contextualConfig, null, 2)};`;
    
    fs.writeFileSync(contextualConfigPath, configContent);
    
    console.log(`✅ Contextual configuration saved to: ${contextualConfigPath}`);
    
    // Send notifications if context is detected
    if (context.mode !== 'normal') {
      const message = `🎯 Performance Budget Context Detected\\n` +
                     `Mode: ${context.mode}\\n` +
                     `Confidence: ${(context.confidence * 100).toFixed(1)}%\\n` +
                     `Triggers: ${context.triggers.join(', ')}\\n` +
                     `Budget adjustments applied for deployment.`;
      
      sendNotifications(context, config, message);
    }
  },
  
  config: () => {
    const config = loadConfig();
    console.log('📋 Current Configuration:');
    console.log(JSON.stringify(config, null, 2));
  },
  
  'set-context': (mode) => {
    const validModes = ['normal', 'marketing', 'hotfix', 'rollout', 'load_test'];
    if (!validModes.includes(mode)) {
      console.error(`Error: Invalid context mode. Valid modes: ${validModes.join(', ')}`);
      process.exit(1);
    }
    
    // Set environment variable to force context
    process.env.FORCE_CONTEXT_MODE = mode;
    console.log(`🎯 Context mode set to: ${mode}`);
    
    // Run adjustment with forced context
    const config = loadConfig();
    const context = {
      mode,
      triggers: ['manually-set'],
      confidence: 1.0,
      metadata: {
        manuallySet: true,
        timestamp: new Date().toISOString()
      }
    };
    
    const contextualConfig = generateLighthouseConfig(context, config);
    const contextualConfigPath = path.join(__dirname, '..', 'lighthouse-contextual.config.js');
    const configContent = `module.exports = ${JSON.stringify(contextualConfig, null, 2)};`;
    
    fs.writeFileSync(contextualConfigPath, configContent);
    console.log(`✅ Contextual configuration updated for mode: ${mode}`);
  },
  
  reset: () => {
    const contextualConfigPath = path.join(__dirname, '..', 'lighthouse-contextual.config.js');
    if (fs.existsSync(contextualConfigPath)) {
      fs.unlinkSync(contextualConfigPath);
      console.log('✅ Contextual configuration reset');
    } else {
      console.log('ℹ️  No contextual configuration found');
    }
  },
  
  help: () => {
    console.log(`
Performance Budget Manager

Usage: node performance-budget-manager.js <command> [options]

Commands:
  detect              Detect current deployment context
  adjust              Generate context-aware Lighthouse configuration
  config              Show current configuration
  set-context <mode>  Manually set context mode
  reset               Reset contextual configuration
  help                Show this help message

Context Modes:
  normal              Standard performance budgets
  marketing           Relaxed budgets for traffic spikes
  hotfix              Bypass performance validation for critical fixes
  rollout             Gradual budget enforcement for feature rollouts
  load_test           Strict budgets for performance testing

Examples:
  node performance-budget-manager.js detect
  node performance-budget-manager.js adjust
  node performance-budget-manager.js set-context marketing
  node performance-budget-manager.js reset
`);
  }
};

// Main execution
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  const options = args.slice(1);
  
  if (commands[command]) {
    commands[command](...options);
  } else {
    console.error(`Error: Unknown command '${command}'`);
    commands.help();
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = {
  detectContext,
  adjustBudgetForContext,
  generateLighthouseConfig,
  loadConfig,
  saveConfig
};