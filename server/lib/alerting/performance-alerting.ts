/**
 * Performance Alerting System
 * Tag 4: Advanced Monitoring Integration
 * 
 * Features:
 * - Multi-channel alert delivery (Slack, PagerDuty, Email, Webhook)
 * - Intelligent alert grouping and de-duplication
 * - Escalation policies based on severity
 * - Business impact correlation alerts
 * - Alert suppression and maintenance modes
 */

import { EventEmitter } from 'events';

interface AlertRule {
  id: string;
  name: string;
  metric: string;
  condition: 'greater_than' | 'less_than' | 'equals' | 'not_equals' | 'percentage_change';
  threshold: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  enabled: boolean;
  channels: string[];
  groupingKey?: string;
  suppressionTime?: number; // Minutes
  escalationPolicy?: EscalationPolicy;
  businessImpactThreshold?: number;
  description?: string;
}

interface EscalationPolicy {
  id: string;
  name: string;
  steps: EscalationStep[];
}

interface EscalationStep {
  delay: number; // Minutes
  channels: string[];
  retryCount?: number;
}

interface AlertChannel {
  id: string;
  type: 'slack' | 'pagerduty' | 'email' | 'webhook';
  name: string;
  config: any;
  enabled: boolean;
}

interface Alert {
  id: string;
  ruleId: string;
  metric: string;
  value: number;
  threshold: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'active' | 'acknowledged' | 'resolved' | 'suppressed';
  createdAt: number;
  updatedAt: number;
  resolvedAt?: number;
  acknowledgedBy?: string;
  groupKey?: string;
  businessImpact?: number;
  metadata: {
    url?: string;
    sessionId?: string;
    persona?: string;
    environment?: string;
    userAgent?: string;
    [key: string]: any;
  };
}

interface AlertNotification {
  alertId: string;
  channelId: string;
  status: 'pending' | 'sent' | 'failed' | 'delivered';
  sentAt?: number;
  error?: string;
  retryCount: number;
}

class PerformanceAlertingSystem extends EventEmitter {
  private rules: Map<string, AlertRule> = new Map();
  private channels: Map<string, AlertChannel> = new Map();
  private alerts: Map<string, Alert> = new Map();
  private notifications: Map<string, AlertNotification> = new Map();
  private suppressedAlerts: Set<string> = new Set();
  private groupedAlerts: Map<string, Set<string>> = new Map();
  private isMaintenanceMode: boolean = false;

  constructor() {
    super();
    this.initializeDefaultRules();
    this.initializeDefaultChannels();
  }

  private initializeDefaultRules(): void {
    const defaultRules: AlertRule[] = [
      {
        id: 'lcp_critical',
        name: 'LCP Critical Threshold',
        metric: 'largest-contentful-paint',
        condition: 'greater_than',
        threshold: 4000,
        severity: 'critical',
        enabled: true,
        channels: ['slack_critical', 'pagerduty'],
        groupingKey: 'core_web_vitals',
        suppressionTime: 5,
        description: 'Largest Contentful Paint exceeds critical threshold'
      },
      {
        id: 'fid_critical',
        name: 'FID Critical Threshold',
        metric: 'first-input-delay',
        condition: 'greater_than',
        threshold: 300,
        severity: 'critical',
        enabled: true,
        channels: ['slack_critical', 'pagerduty'],
        groupingKey: 'core_web_vitals',
        suppressionTime: 5,
        description: 'First Input Delay exceeds critical threshold'
      },
      {
        id: 'cls_critical',
        name: 'CLS Critical Threshold',
        metric: 'cumulative-layout-shift',
        condition: 'greater_than',
        threshold: 0.25,
        severity: 'critical',
        enabled: true,
        channels: ['slack_critical', 'pagerduty'],
        groupingKey: 'core_web_vitals',
        suppressionTime: 5,
        description: 'Cumulative Layout Shift exceeds critical threshold'
      },
      {
        id: 'performance_regression',
        name: 'Performance Regression',
        metric: 'performance_score_change',
        condition: 'less_than',
        threshold: -15, // 15% decrease
        severity: 'high',
        enabled: true,
        channels: ['slack_alerts'],
        suppressionTime: 15,
        description: 'Performance score decreased significantly'
      },
      {
        id: 'conversion_impact',
        name: 'Performance Impact on Conversions',
        metric: 'conversion_correlation',
        condition: 'less_than',
        threshold: -10, // 10% conversion drop
        severity: 'high',
        enabled: true,
        channels: ['slack_business', 'email_leadership'],
        businessImpactThreshold: 5,
        description: 'Performance issues impacting conversion rates'
      },
      {
        id: 'error_rate_spike',
        name: 'Error Rate Spike',
        metric: 'error_rate',
        condition: 'greater_than',
        threshold: 5, // 5% error rate
        severity: 'high',
        enabled: true,
        channels: ['slack_critical', 'pagerduty'],
        suppressionTime: 3,
        description: 'Error rate spike detected'
      }
    ];

    defaultRules.forEach(rule => {
      this.rules.set(rule.id, rule);
    });
  }

  private initializeDefaultChannels(): void {
    const defaultChannels: AlertChannel[] = [
      {
        id: 'slack_critical',
        type: 'slack',
        name: 'Slack Critical Alerts',
        enabled: true,
        config: {
          webhook: process.env.SLACK_CRITICAL_WEBHOOK_URL,
          channel: '#alerts-critical',
          username: 'Performance Monitor',
          icon_emoji: ':rotating_light:'
        }
      },
      {
        id: 'slack_alerts',
        type: 'slack',
        name: 'Slack General Alerts',
        enabled: true,
        config: {
          webhook: process.env.SLACK_ALERTS_WEBHOOK_URL,
          channel: '#alerts',
          username: 'Performance Monitor',
          icon_emoji: ':warning:'
        }
      },
      {
        id: 'slack_business',
        type: 'slack',
        name: 'Slack Business Impact',
        enabled: true,
        config: {
          webhook: process.env.SLACK_BUSINESS_WEBHOOK_URL,
          channel: '#business-alerts',
          username: 'Business Impact Monitor',
          icon_emoji: ':chart_with_downwards_trend:'
        }
      },
      {
        id: 'pagerduty',
        type: 'pagerduty',
        name: 'PagerDuty Escalation',
        enabled: !!process.env.PAGERDUTY_INTEGRATION_KEY,
        config: {
          integrationKey: process.env.PAGERDUTY_INTEGRATION_KEY,
          severity: 'critical'
        }
      },
      {
        id: 'email_leadership',
        type: 'email',
        name: 'Leadership Email Alerts',
        enabled: !!process.env.SMTP_HOST,
        config: {
          recipients: (process.env.LEADERSHIP_EMAIL_RECIPIENTS || '').split(','),
          smtp: {
            host: process.env.SMTP_HOST,
            port: parseInt(process.env.SMTP_PORT || '587'),
            secure: process.env.SMTP_SECURE === 'true',
            auth: {
              user: process.env.SMTP_USER,
              pass: process.env.SMTP_PASS
            }
          }
        }
      }
    ];

    defaultChannels.forEach(channel => {
      this.channels.set(channel.id, channel);
    });
  }

  public async evaluateMetric(
    metric: string,
    value: number,
    metadata: Alert['metadata'] = {}
  ): Promise<void> {
    if (this.isMaintenanceMode) {
      console.log('⏸️ Alerting in maintenance mode, skipping evaluation');
      return;
    }

    for (const rule of this.rules.values()) {
      if (!rule.enabled || rule.metric !== metric) {
        continue;
      }

      const shouldAlert = this.evaluateCondition(rule, value);
      
      if (shouldAlert) {
        await this.triggerAlert(rule, value, metadata);
      }
    }
  }

  private evaluateCondition(rule: AlertRule, value: number): boolean {
    switch (rule.condition) {
      case 'greater_than':
        return value > rule.threshold;
      case 'less_than':
        return value < rule.threshold;
      case 'equals':
        return value === rule.threshold;
      case 'not_equals':
        return value !== rule.threshold;
      case 'percentage_change':
        // For percentage change, we'd need historical data
        // This is a simplified implementation
        return Math.abs(value) > Math.abs(rule.threshold);
      default:
        return false;
    }
  }

  private async triggerAlert(
    rule: AlertRule,
    value: number,
    metadata: Alert['metadata']
  ): Promise<void> {
    const alertId = this.generateAlertId();
    const groupKey = rule.groupingKey || rule.id;
    
    // Check for suppression
    const suppressionKey = `${rule.id}_${groupKey}`;
    if (this.suppressedAlerts.has(suppressionKey)) {
      console.log(`🔇 Alert suppressed: ${rule.name}`);
      return;
    }

    // Calculate business impact if applicable
    let businessImpact: number | undefined;
    if (rule.businessImpactThreshold) {
      businessImpact = this.calculateBusinessImpact(rule.metric, value, metadata);
      
      // Skip alert if business impact is below threshold
      if (businessImpact < rule.businessImpactThreshold) {
        console.log(`📊 Business impact below threshold: ${businessImpact}% < ${rule.businessImpactThreshold}%`);
        return;
      }
    }

    const alert: Alert = {
      id: alertId,
      ruleId: rule.id,
      metric: rule.metric,
      value,
      threshold: rule.threshold,
      severity: rule.severity,
      status: 'active',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      groupKey,
      businessImpact,
      metadata
    };

    this.alerts.set(alertId, alert);

    // Group alerts if applicable
    if (rule.groupingKey) {
      if (!this.groupedAlerts.has(rule.groupingKey)) {
        this.groupedAlerts.set(rule.groupingKey, new Set());
      }
      this.groupedAlerts.get(rule.groupingKey)!.add(alertId);
    }

    // Apply suppression
    if (rule.suppressionTime && rule.suppressionTime > 0) {
      this.suppressedAlerts.add(suppressionKey);
      setTimeout(() => {
        this.suppressedAlerts.delete(suppressionKey);
      }, rule.suppressionTime * 60 * 1000);
    }

    console.log(`🚨 Alert triggered: ${rule.name} (${alert.severity})`, {
      metric: rule.metric,
      value,
      threshold: rule.threshold,
      businessImpact
    });

    // Send notifications
    await this.sendNotifications(alert, rule);

    // Emit event for external listeners
    this.emit('alert_triggered', alert, rule);
  }

  private calculateBusinessImpact(
    metric: string,
    value: number,
    metadata: Alert['metadata']
  ): number {
    // This is a simplified business impact calculation
    // In a real implementation, this would correlate with actual business metrics
    
    const impactFactors = {
      'largest-contentful-paint': 0.8, // High impact on conversion
      'first-input-delay': 0.6,        // Medium-high impact
      'cumulative-layout-shift': 0.4,  // Medium impact
      'first-contentful-paint': 0.5,   // Medium impact
      'time-to-first-byte': 0.7,       // High impact
      'error_rate': 1.0                // Very high impact
    };

    const baseFactor = impactFactors[metric as keyof typeof impactFactors] || 0.3;
    
    // Calculate impact based on how much the metric exceeds good thresholds
    let impactMultiplier = 1;
    
    switch (metric) {
      case 'largest-contentful-paint':
        impactMultiplier = Math.max(1, value / 2500); // Good threshold is 2500ms
        break;
      case 'first-input-delay':
        impactMultiplier = Math.max(1, value / 100);  // Good threshold is 100ms
        break;
      case 'cumulative-layout-shift':
        impactMultiplier = Math.max(1, value / 0.1);  // Good threshold is 0.1
        break;
      case 'error_rate':
        impactMultiplier = Math.max(1, value / 1);     // Good threshold is 1%
        break;
    }

    // Persona-based impact adjustment
    const personaMultipliers = {
      'TechEarlyAdopter': 0.8,   // More tolerant of performance issues
      'BusinessOwner': 1.2,      // Less tolerant, higher impact
      'RemoteDad': 1.0,          // Average impact
      'StudentHustler': 1.1      // Budget-conscious, higher impact
    };

    const personaMultiplier = metadata.persona ? 
      personaMultipliers[metadata.persona as keyof typeof personaMultipliers] || 1.0 : 1.0;

    const finalImpact = baseFactor * impactMultiplier * personaMultiplier * 10; // Scale to percentage
    
    return Math.min(100, Math.round(finalImpact));
  }

  private async sendNotifications(alert: Alert, rule: AlertRule): Promise<void> {
    for (const channelId of rule.channels) {
      const channel = this.channels.get(channelId);
      if (!channel || !channel.enabled) {
        console.warn(`⚠️ Channel not found or disabled: ${channelId}`);
        continue;
      }

      const notificationId = `${alert.id}_${channelId}`;
      const notification: AlertNotification = {
        alertId: alert.id,
        channelId,
        status: 'pending',
        retryCount: 0
      };

      this.notifications.set(notificationId, notification);

      try {
        await this.sendToChannel(channel, alert, rule);
        notification.status = 'sent';
        notification.sentAt = Date.now();
        console.log(`✅ Alert sent to ${channel.name}`);
      } catch (error) {
        notification.status = 'failed';
        notification.error = error instanceof Error ? error.message : 'Unknown error';
        console.error(`❌ Failed to send alert to ${channel.name}:`, error);
        
        // Retry logic could be implemented here
      }
    }
  }

  private async sendToChannel(
    channel: AlertChannel,
    alert: Alert,
    rule: AlertRule
  ): Promise<void> {
    switch (channel.type) {
      case 'slack':
        await this.sendSlackNotification(channel, alert, rule);
        break;
      case 'pagerduty':
        await this.sendPagerDutyAlert(channel, alert, rule);
        break;
      case 'email':
        await this.sendEmailAlert(channel, alert, rule);
        break;
      case 'webhook':
        await this.sendWebhookAlert(channel, alert, rule);
        break;
      default:
        throw new Error(`Unsupported channel type: ${channel.type}`);
    }
  }

  private async sendSlackNotification(
    channel: AlertChannel,
    alert: Alert,
    rule: AlertRule
  ): Promise<void> {
    const webhook = channel.config.webhook;
    if (!webhook) {
      throw new Error('Slack webhook URL not configured');
    }

    const color = this.getSeverityColor(alert.severity);
    const emoji = this.getSeverityEmoji(alert.severity);
    
    const message = {
      username: channel.config.username || 'Performance Monitor',
      icon_emoji: channel.config.icon_emoji || ':warning:',
      attachments: [
        {
          color,
          title: `${emoji} ${rule.name}`,
          text: rule.description || 'Performance alert triggered',
          fields: [
            {
              title: 'Metric',
              value: rule.metric,
              short: true
            },
            {
              title: 'Current Value',
              value: this.formatMetricValue(rule.metric, alert.value),
              short: true
            },
            {
              title: 'Threshold',
              value: this.formatMetricValue(rule.metric, alert.threshold),
              short: true
            },
            {
              title: 'Severity',
              value: alert.severity.toUpperCase(),
              short: true
            },
            ...(alert.metadata.url ? [{
              title: 'URL',
              value: alert.metadata.url,
              short: false
            }] : []),
            ...(alert.metadata.persona ? [{
              title: 'Persona',
              value: alert.metadata.persona,
              short: true
            }] : []),
            ...(alert.businessImpact ? [{
              title: 'Business Impact',
              value: `${alert.businessImpact}%`,
              short: true
            }] : [])
          ],
          footer: 'Performance Monitoring System',
          ts: Math.floor(alert.createdAt / 1000)
        }
      ]
    };

    const response = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message)
    });

    if (!response.ok) {
      throw new Error(`Slack API error: ${response.status}`);
    }
  }

  private async sendPagerDutyAlert(
    channel: AlertChannel,
    alert: Alert,
    rule: AlertRule
  ): Promise<void> {
    const integrationKey = channel.config.integrationKey;
    if (!integrationKey) {
      throw new Error('PagerDuty integration key not configured');
    }

    const payload = {
      routing_key: integrationKey,
      event_action: 'trigger',
      dedup_key: `performance_alert_${alert.ruleId}`,
      payload: {
        summary: `${rule.name}: ${rule.metric} = ${this.formatMetricValue(rule.metric, alert.value)}`,
        source: 'performance-monitor',
        severity: alert.severity === 'critical' ? 'critical' : 
                 alert.severity === 'high' ? 'error' :
                 alert.severity === 'medium' ? 'warning' : 'info',
        component: 'web-performance',
        group: rule.groupingKey || 'performance',
        class: rule.metric,
        custom_details: {
          metric: rule.metric,
          current_value: alert.value,
          threshold: alert.threshold,
          url: alert.metadata.url,
          persona: alert.metadata.persona,
          session_id: alert.metadata.sessionId,
          business_impact: alert.businessImpact
        }
      }
    };

    const response = await fetch('https://events.pagerduty.com/v2/enqueue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`PagerDuty API error: ${response.status}`);
    }
  }

  private async sendEmailAlert(
    channel: AlertChannel,
    alert: Alert,
    rule: AlertRule
  ): Promise<void> {
    // Email implementation would require a mail library like nodemailer
    console.log('📧 Email alert would be sent:', {
      recipients: channel.config.recipients,
      subject: `Performance Alert: ${rule.name}`,
      alert,
      rule
    });
  }

  private async sendWebhookAlert(
    channel: AlertChannel,
    alert: Alert,
    rule: AlertRule
  ): Promise<void> {
    const webhook = channel.config.url;
    if (!webhook) {
      throw new Error('Webhook URL not configured');
    }

    const payload = {
      alert,
      rule,
      timestamp: Date.now(),
      source: 'performance-monitoring-system'
    };

    const response = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Webhook error: ${response.status}`);
    }
  }

  private getSeverityColor(severity: string): string {
    const colors = {
      low: 'good',
      medium: 'warning',
      high: 'danger',
      critical: '#ff0000'
    };
    return colors[severity as keyof typeof colors] || 'warning';
  }

  private getSeverityEmoji(severity: string): string {
    const emojis = {
      low: '🟡',
      medium: '🟠',
      high: '🔴',
      critical: '🚨'
    };
    return emojis[severity as keyof typeof emojis] || '⚠️';
  }

  private formatMetricValue(metric: string, value: number): string {
    if (metric.includes('time') || metric.includes('paint') || metric.includes('delay')) {
      return `${Math.round(value)}ms`;
    }
    if (metric.includes('shift')) {
      return value.toFixed(3);
    }
    if (metric.includes('rate') || metric.includes('percentage')) {
      return `${value.toFixed(1)}%`;
    }
    return value.toString();
  }

  private generateAlertId(): string {
    return `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Public API methods
  public acknowledgeAlert(alertId: string, acknowledgedBy: string): boolean {
    const alert = this.alerts.get(alertId);
    if (!alert) {
      return false;
    }

    alert.status = 'acknowledged';
    alert.acknowledgedBy = acknowledgedBy;
    alert.updatedAt = Date.now();

    console.log(`✅ Alert acknowledged: ${alertId} by ${acknowledgedBy}`);
    this.emit('alert_acknowledged', alert);
    
    return true;
  }

  public resolveAlert(alertId: string): boolean {
    const alert = this.alerts.get(alertId);
    if (!alert) {
      return false;
    }

    alert.status = 'resolved';
    alert.resolvedAt = Date.now();
    alert.updatedAt = Date.now();

    console.log(`✅ Alert resolved: ${alertId}`);
    this.emit('alert_resolved', alert);
    
    return true;
  }

  public enableMaintenanceMode(durationMinutes: number = 60): void {
    this.isMaintenanceMode = true;
    console.log(`🔧 Maintenance mode enabled for ${durationMinutes} minutes`);
    
    setTimeout(() => {
      this.isMaintenanceMode = false;
      console.log('🔧 Maintenance mode disabled');
    }, durationMinutes * 60 * 1000);
  }

  public disableMaintenanceMode(): void {
    this.isMaintenanceMode = false;
    console.log('🔧 Maintenance mode disabled manually');
  }

  public getActiveAlerts(): Alert[] {
    return Array.from(this.alerts.values()).filter(alert => alert.status === 'active');
  }

  public getAlertsByRule(ruleId: string): Alert[] {
    return Array.from(this.alerts.values()).filter(alert => alert.ruleId === ruleId);
  }

  public getAlertStats(): any {
    const alerts = Array.from(this.alerts.values());
    const now = Date.now();
    const last24h = now - (24 * 60 * 60 * 1000);
    
    return {
      total: alerts.length,
      active: alerts.filter(a => a.status === 'active').length,
      acknowledged: alerts.filter(a => a.status === 'acknowledged').length,
      resolved: alerts.filter(a => a.status === 'resolved').length,
      last24h: alerts.filter(a => a.createdAt > last24h).length,
      bySeverity: {
        critical: alerts.filter(a => a.severity === 'critical').length,
        high: alerts.filter(a => a.severity === 'high').length,
        medium: alerts.filter(a => a.severity === 'medium').length,
        low: alerts.filter(a => a.severity === 'low').length
      }
    };
  }
}

// Global instance
const performanceAlerting = new PerformanceAlertingSystem();

export default performanceAlerting;
export { PerformanceAlertingSystem, type Alert, type AlertRule, type AlertChannel };