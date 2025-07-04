/**
 * Performance Dashboard Component
 * Tag 4: Advanced Monitoring Integration
 * 
 * Features:
 * - Real-time Core Web Vitals visualization
 * - Business impact correlation charts
 * - Performance budget compliance tracking
 * - Alert management interface
 * - Persona-based performance analytics
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

interface CoreWebVital {
  name: string;
  avg: number;
  p95: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  threshold: {
    good: number;
    poor: number;
  };
}

interface DashboardData {
  summary: {
    totalSessions: number;
    totalPageViews: number;
    conversionRate: number;
    bounceRate: number;
    avgEngagementTime: number;
  };
  coreWebVitals: {
    lcp: CoreWebVital;
    fid: CoreWebVital;
    cls: CoreWebVital;
    fcp: CoreWebVital;
    ttfb: CoreWebVital;
  };
  alerts: {
    recent: any[];
    total: number;
    unacknowledged: number;
  };
  timeRange: string;
  generatedAt: number;
}

interface TimeSeriesData {
  timestamp: number;
  lcp: number;
  fid: number;
  cls: number;
  fcp: number;
  ttfb: number;
  conversions: number;
  sessions: number;
}

interface PersonaPerformance {
  persona: string;
  sessions: number;
  avgLCP: number;
  avgFID: number;
  avgCLS: number;
  conversionRate: number;
  businessImpact: number;
}

const PerformanceDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>([]);
  const [personaData, setPersonaData] = useState<PersonaPerformance[]>([]);
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
  const [selectedEnvironment, setSelectedEnvironment] = useState('production');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      
      const [dashboardResponse, timeSeriesResponse, personaResponse] = await Promise.all([
        fetch(`/api/metrics/dashboard?timeRange=${selectedTimeRange}&environment=${selectedEnvironment}`),
        fetch(`/api/metrics/timeseries?timeRange=${selectedTimeRange}&environment=${selectedEnvironment}`),
        fetch(`/api/metrics/persona-performance?timeRange=${selectedTimeRange}&environment=${selectedEnvironment}`)
      ]);

      if (!dashboardResponse.ok) {
        throw new Error('Failed to fetch dashboard data');
      }

      const dashboard = await dashboardResponse.json();
      const timeSeries = timeSeriesResponse.ok ? await timeSeriesResponse.json() : [];
      const persona = personaResponse.ok ? await personaResponse.json() : [];

      setDashboardData(dashboard);
      setTimeSeriesData(timeSeries);
      setPersonaData(persona);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Auto-refresh data
  useEffect(() => {
    fetchDashboardData();
    
    const interval = setInterval(fetchDashboardData, refreshInterval);
    return () => clearInterval(interval);
  }, [selectedTimeRange, selectedEnvironment, refreshInterval]);

  // Performance rating colors
  const getRatingColor = (rating: string): string => {
    switch (rating) {
      case 'good': return '#10b981'; // green-500
      case 'needs-improvement': return '#f59e0b'; // amber-500
      case 'poor': return '#ef4444'; // red-500
      default: return '#6b7280'; // gray-500
    }
  };

  // Format metric values
  const formatMetricValue = (metric: string, value: number): string => {
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
  };

  // Summary metrics cards
  const SummaryCard: React.FC<{
    title: string;
    value: string | number;
    trend?: string;
    icon: string;
    color: string;
  }> = ({ title, value, trend, icon, color }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4" style={{ borderLeftColor: color }}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {trend && (
            <p className={`text-sm ${trend.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
              {trend}
            </p>
          )}
        </div>
        <div className="text-3xl">{icon}</div>
      </div>
    </div>
  );

  // Core Web Vitals card
  const CoreWebVitalCard: React.FC<{
    name: string;
    vital: CoreWebVital;
    unit: string;
  }> = ({ name, vital, unit }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
        <div 
          className="px-3 py-1 rounded-full text-sm font-medium text-white"
          style={{ backgroundColor: getRatingColor(vital.rating) }}
        >
          {vital.rating.replace('-', ' ')}
        </div>
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Average:</span>
          <span className="font-medium">{formatMetricValue(name.toLowerCase(), vital.avg)}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-600">95th Percentile:</span>
          <span className="font-medium">{formatMetricValue(name.toLowerCase(), vital.p95)}</span>
        </div>
        
        {/* Progress bar showing performance relative to thresholds */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all duration-300"
            style={{
              width: `${Math.min(100, (vital.threshold.poor - vital.avg) / vital.threshold.poor * 100)}%`,
              backgroundColor: getRatingColor(vital.rating)
            }}
          />
        </div>
        
        <div className="flex justify-between text-xs text-gray-500">
          <span>Good: &lt;{vital.threshold.good}{unit}</span>
          <span>Poor: &gt;{vital.threshold.poor}{unit}</span>
        </div>
      </div>
    </div>
  );

  // Alert severity pie chart data
  const alertSeverityData = useMemo(() => {
    if (!dashboardData?.alerts.recent) return [];
    
    const severityCounts = dashboardData.alerts.recent.reduce((acc, alert) => {
      acc[alert.severity] = (acc[alert.severity] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return Object.entries(severityCounts).map(([severity, count]) => ({
      name: severity,
      value: count,
      color: getRatingColor(severity === 'critical' ? 'poor' : 
                          severity === 'high' ? 'needs-improvement' : 'good')
    }));
  }, [dashboardData]);

  if (isLoading && !dashboardData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 className="text-red-800 font-medium">Error loading dashboard</h3>
        <p className="text-red-600">{error}</p>
        <button 
          onClick={fetchDashboardData}
          className="mt-2 px-4 py-2 bg-red-100 text-red-800 rounded hover:bg-red-200"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!dashboardData) {
    return <div>No data available</div>;
  }

  return (
    <div className="space-y-6 p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Performance Dashboard</h1>
          <p className="text-gray-600">Real-time performance monitoring and analytics</p>
        </div>
        
        <div className="flex gap-4">
          {/* Time Range Selector */}
          <select
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg bg-white"
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>

          {/* Environment Selector */}
          <select
            value={selectedEnvironment}
            onChange={(e) => setSelectedEnvironment(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg bg-white"
          >
            <option value="production">Production</option>
            <option value="staging">Staging</option>
            <option value="development">Development</option>
          </select>

          {/* Refresh Button */}
          <button
            onClick={fetchDashboardData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <SummaryCard
          title="Total Sessions"
          value={dashboardData.summary.totalSessions.toLocaleString()}
          icon="👥"
          color="#3b82f6"
        />
        <SummaryCard
          title="Page Views"
          value={dashboardData.summary.totalPageViews.toLocaleString()}
          icon="📄"
          color="#10b981"
        />
        <SummaryCard
          title="Conversion Rate"
          value={`${dashboardData.summary.conversionRate}%`}
          icon="💰"
          color="#f59e0b"
        />
        <SummaryCard
          title="Bounce Rate"
          value={`${dashboardData.summary.bounceRate}%`}
          icon="↩️"
          color="#ef4444"
        />
        <SummaryCard
          title="Avg. Engagement"
          value={`${dashboardData.summary.avgEngagementTime}s`}
          icon="⏱️"
          color="#8b5cf6"
        />
      </div>

      {/* Core Web Vitals */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <CoreWebVitalCard
          name="LCP"
          vital={dashboardData.coreWebVitals.lcp}
          unit="ms"
        />
        <CoreWebVitalCard
          name="FID"
          vital={dashboardData.coreWebVitals.fid}
          unit="ms"
        />
        <CoreWebVitalCard
          name="CLS"
          vital={dashboardData.coreWebVitals.cls}
          unit=""
        />
        <CoreWebVitalCard
          name="FCP"
          vital={dashboardData.coreWebVitals.fcp}
          unit="ms"
        />
        <CoreWebVitalCard
          name="TTFB"
          vital={dashboardData.coreWebVitals.ttfb}
          unit="ms"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Trends */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timeSeriesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timestamp" 
                tickFormatter={(value) => new Date(value).toLocaleTimeString()}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleString()}
                formatter={(value: number, name: string) => [
                  formatMetricValue(name, value), 
                  name.toUpperCase()
                ]}
              />
              <Legend />
              <Line type="monotone" dataKey="lcp" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="fid" stroke="#f59e0b" strokeWidth={2} />
              <Line type="monotone" dataKey="cls" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Alert Distribution */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Alert Distribution ({dashboardData.alerts.total} total, {dashboardData.alerts.unacknowledged} unacknowledged)
          </h3>
          {alertSeverityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={alertSeverityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {alertSeverityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              No alerts in selected time range
            </div>
          )}
        </div>
      </div>

      {/* Persona Performance */}
      {personaData.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance by Persona</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={personaData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="persona" />
              <YAxis />
              <Tooltip 
                formatter={(value: number, name: string) => [
                  name === 'avgLCP' || name === 'avgFID' ? `${Math.round(value)}ms` :
                  name === 'avgCLS' ? value.toFixed(3) :
                  name === 'conversionRate' ? `${value.toFixed(1)}%` :
                  value.toString(),
                  name
                ]}
              />
              <Legend />
              <Bar dataKey="avgLCP" fill="#ef4444" name="Avg LCP" />
              <Bar dataKey="avgFID" fill="#f59e0b" name="Avg FID" />
              <Bar dataKey="conversionRate" fill="#10b981" name="Conversion Rate" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Recent Alerts */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h3>
        {dashboardData.alerts.recent.length > 0 ? (
          <div className="space-y-3">
            {dashboardData.alerts.recent.slice(0, 10).map((alert, index) => (
              <div 
                key={index}
                className={`p-4 rounded-lg border-l-4 ${
                  alert.severity === 'critical' ? 'bg-red-50 border-red-500' :
                  alert.severity === 'high' ? 'bg-orange-50 border-orange-500' :
                  alert.severity === 'medium' ? 'bg-yellow-50 border-yellow-500' :
                  'bg-blue-50 border-blue-500'
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium text-gray-900">{alert.metric}</h4>
                    <p className="text-sm text-gray-600">
                      Value: {formatMetricValue(alert.metric, alert.value)} 
                      (Threshold: {formatMetricValue(alert.metric, alert.threshold)})
                    </p>
                    {alert.url && (
                      <p className="text-sm text-gray-500">URL: {alert.url}</p>
                    )}
                  </div>
                  <div className="text-right">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      alert.severity === 'critical' ? 'bg-red-100 text-red-800' :
                      alert.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                      alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {alert.severity}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(alert.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No recent alerts 🎉
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="text-center text-sm text-gray-500">
        Last updated: {new Date(dashboardData.generatedAt).toLocaleString()}
        {isLoading && <span className="ml-2">🔄 Refreshing...</span>}
      </div>
    </div>
  );
};

export default PerformanceDashboard;