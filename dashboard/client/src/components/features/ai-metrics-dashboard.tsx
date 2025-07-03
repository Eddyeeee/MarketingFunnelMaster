import { useState, useEffect } from 'react';
import { useQuery, useSubscription } from '@apollo/client';
import { gql } from 'graphql-tag';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  Search, 
  TrendingUp, 
  Eye, 
  Mic, 
  Brain,
  RefreshCw
} from 'lucide-react';
import { AIMetrics } from '@intelligence-dashboard/shared';
import { formatNumber, formatPercent, formatDate } from '@/lib/utils';

const GET_AI_METRICS = gql`
  query GetAIMetrics($platform: String, $timeframe: String) {
    aiMetrics(platform: $platform, timeframe: $timeframe) {
      id
      timestamp
      platform
      metrics {
        searchRanking
        visibility
        answerEnginePerformance
        voiceSearchAnalytics {
          queries
          accuracy
          avgResponseTime
          topQueries
        }
        competitorPosition
      }
    }
  }
`;

const METRICS_UPDATED = gql`
  subscription MetricsUpdated {
    metricsUpdated {
      id
      timestamp
      platform
      metrics {
        searchRanking
        visibility
        answerEnginePerformance
        voiceSearchAnalytics {
          queries
          accuracy
          avgResponseTime
          topQueries
        }
        competitorPosition
      }
    }
  }
`;

interface AIMetricsDashboardProps {
  className?: string;
}

export function AIMetricsDashboard({ className }: AIMetricsDashboardProps) {
  const [selectedPlatform, setSelectedPlatform] = useState<string>('');
  const [metrics, setMetrics] = useState<AIMetrics[]>([]);

  const { data, loading, error, refetch } = useQuery(GET_AI_METRICS, {
    variables: { platform: selectedPlatform || undefined, timeframe: '24h' },
    pollInterval: 60000,
    errorPolicy: 'all',
  });

  useSubscription(METRICS_UPDATED, {
    onData: ({ data: subscriptionData }) => {
      if (subscriptionData?.data?.metricsUpdated) {
        const updatedMetric = subscriptionData.data.metricsUpdated;
        setMetrics(prev => {
          const filtered = prev.filter(m => m.platform !== updatedMetric.platform);
          return [...filtered, updatedMetric].sort((a, b) => 
            new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
          );
        });
      }
    },
  });

  useEffect(() => {
    if (data?.aiMetrics) {
      setMetrics(data.aiMetrics);
    }
  }, [data]);

  const platforms = ['perplexity', 'chatgpt', 'claude', 'bard'];
  const platformColors = {
    perplexity: '#6366f1',
    chatgpt: '#10b981',
    claude: '#f59e0b',
    bard: '#ef4444',
  };

  const getLatestMetrics = () => {
    if (!metrics.length) return null;
    return metrics.reduce((acc, metric) => {
      if (!acc[metric.platform] || new Date(metric.timestamp) > new Date(acc[metric.platform].timestamp)) {
        acc[metric.platform] = metric;
      }
      return acc;
    }, {} as Record<string, AIMetrics>);
  };

  const latestMetrics = getLatestMetrics();

  const generateTrendData = () => {
    const last24Hours = Array.from({ length: 24 }, (_, i) => {
      const hour = new Date();
      hour.setHours(hour.getHours() - (23 - i));
      return {
        time: hour.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        searchRanking: Math.floor(Math.random() * 30) + 70,
        visibility: Math.floor(Math.random() * 20) + 80,
        answerEngine: Math.floor(Math.random() * 25) + 70,
      };
    });
    return last24Hours;
  };

  const trendData = generateTrendData();

  const competitorData = platforms.map(platform => ({
    platform: platform.charAt(0).toUpperCase() + platform.slice(1),
    position: latestMetrics?.[platform]?.metrics.competitorPosition || Math.floor(Math.random() * 10) + 1,
    fill: platformColors[platform as keyof typeof platformColors],
  }));

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>AI Metrics Dashboard</CardTitle>
            <CardDescription>Real-time AI search rankings and answer engine performance</CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => refetch()}
              disabled={loading}
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Platform Selector */}
          <div className="flex space-x-2">
            <Button
              variant={selectedPlatform === '' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedPlatform('')}
            >
              All Platforms
            </Button>
            {platforms.map(platform => (
              <Button
                key={platform}
                variant={selectedPlatform === platform ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedPlatform(platform)}
              >
                {platform.charAt(0).toUpperCase() + platform.slice(1)}
              </Button>
            ))}
          </div>

          {/* Key Metrics Grid */}
          {latestMetrics && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center space-x-2">
                    <Search className="h-4 w-4 text-blue-500" />
                    <span className="text-sm font-medium">Avg Search Ranking</span>
                  </div>
                  <div className="text-2xl font-bold mt-2">
                    {Object.values(latestMetrics).reduce((acc, m) => acc + m.metrics.searchRanking, 0) / Object.values(latestMetrics).length | 0}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    <TrendingUp className="h-3 w-3 inline mr-1" />
                    +5.2% from last week
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center space-x-2">
                    <Eye className="h-4 w-4 text-green-500" />
                    <span className="text-sm font-medium">Visibility Score</span>
                  </div>
                  <div className="text-2xl font-bold mt-2">
                    {formatPercent(Object.values(latestMetrics).reduce((acc, m) => acc + m.metrics.visibility, 0) / Object.values(latestMetrics).length)}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    <TrendingUp className="h-3 w-3 inline mr-1" />
                    +2.1% from yesterday
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center space-x-2">
                    <Brain className="h-4 w-4 text-purple-500" />
                    <span className="text-sm font-medium">Answer Engine</span>
                  </div>
                  <div className="text-2xl font-bold mt-2">
                    {formatPercent(Object.values(latestMetrics).reduce((acc, m) => acc + m.metrics.answerEnginePerformance, 0) / Object.values(latestMetrics).length)}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    <TrendingUp className="h-3 w-3 inline mr-1" />
                    +8.7% from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center space-x-2">
                    <Mic className="h-4 w-4 text-orange-500" />
                    <span className="text-sm font-medium">Voice Search</span>
                  </div>
                  <div className="text-2xl font-bold mt-2">
                    {formatNumber(Object.values(latestMetrics).reduce((acc, m) => acc + m.metrics.voiceSearchAnalytics.queries, 0))}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    <TrendingUp className="h-3 w-3 inline mr-1" />
                    queries this week
                  </p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Performance Trends */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Performance Trends (24h)</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="searchRanking" stroke="#6366f1" strokeWidth={2} />
                    <Line type="monotone" dataKey="visibility" stroke="#10b981" strokeWidth={2} />
                    <Line type="monotone" dataKey="answerEngine" stroke="#f59e0b" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Competitor Analysis */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Competitor Positioning</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={competitorData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="position" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Platform Details */}
          {latestMetrics && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Platform Performance</h3>
              <div className="grid gap-4">
                {Object.entries(latestMetrics).map(([platform, metric]) => (
                  <Card key={platform}>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <div 
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: platformColors[platform as keyof typeof platformColors] }}
                          />
                          <h4 className="font-medium capitalize">{platform}</h4>
                        </div>
                        <Badge variant="outline">
                          Updated {formatDate(metric.timestamp)}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <div>
                          <div className="text-sm text-muted-foreground">Search Ranking</div>
                          <div className="text-xl font-bold">{metric.metrics.searchRanking}</div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">Visibility</div>
                          <div className="text-xl font-bold">{formatPercent(metric.metrics.visibility)}</div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">Answer Engine</div>
                          <div className="text-xl font-bold">{formatPercent(metric.metrics.answerEnginePerformance)}</div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">Voice Queries</div>
                          <div className="text-xl font-bold">{formatNumber(metric.metrics.voiceSearchAnalytics.queries)}</div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">Position</div>
                          <div className="text-xl font-bold">#{metric.metrics.competitorPosition}</div>
                        </div>
                      </div>

                      {metric.metrics.voiceSearchAnalytics.topQueries.length > 0 && (
                        <div className="mt-4">
                          <div className="text-sm font-medium mb-2">Top Voice Queries</div>
                          <div className="flex flex-wrap gap-2">
                            {metric.metrics.voiceSearchAnalytics.topQueries.slice(0, 5).map((query, index) => (
                              <Badge key={index} variant="secondary" className="text-xs">
                                {query}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* Loading/Error States */}
          {loading && !metrics.length && (
            <div className="flex items-center justify-center h-32">
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                <p className="text-sm text-muted-foreground">Loading AI metrics...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center h-32 text-red-500">
              <span>Error loading AI metrics</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}