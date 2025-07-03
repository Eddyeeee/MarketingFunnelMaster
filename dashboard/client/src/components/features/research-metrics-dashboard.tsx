import { useMemo } from 'react';
import { useQuery } from '@apollo/client';
import { GET_RESEARCH_DATASET } from '../../graphql/queries';
import type { NicheAnalysis } from '@intelligence-dashboard/shared';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
// import { Progress } from '@/components/ui/progress'; // Removed as not used
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  TrendingUp, 
  Target,
  BarChart3,
  Award,
  Zap,
  Brain,
  DollarSign,
  // Activity, // Removed as not used
  // Gauge // Removed as not used
} from 'lucide-react';

interface ResearchMetricsDashboardProps {
  className?: string;
}

export function ResearchMetricsDashboard({ className }: ResearchMetricsDashboardProps) {
  const { data, loading, error } = useQuery(GET_RESEARCH_DATASET, {
    pollInterval: 60000, // Refresh every minute
  });

  const chartData = useMemo(() => {
    if (!data?.researchDataset?.niches) return { priorityData: [], riskVsROI: [] };
    
    const niches = data.researchDataset.niches;
    
    // Create chart data for different visualizations
    const priorityData = niches
      .sort((a: NicheAnalysis, b: NicheAnalysis) => b.priority_score - a.priority_score)
      .slice(0, 8)
      .map((niche: NicheAnalysis) => ({
        name: niche.niche_name.length > 15 ? 
              niche.niche_name.substring(0, 15) + '...' : 
              niche.niche_name,
        priority: niche.priority_score,
        automation: niche.automation_ready_score * 10,
        roi: niche.roi_projection.realistic / 1000, // Convert to thousands
        risk: niche.risk_assessment_score,
      }));

    const riskVsROI = niches.map((niche: NicheAnalysis) => ({
      name: niche.niche_name.length > 12 ? 
            niche.niche_name.substring(0, 12) + '...' : 
            niche.niche_name,
      risk: niche.risk_assessment_score,
      roi: niche.roi_projection.realistic / 1000,
      priority: niche.priority_score,
      automation: niche.automation_ready_score,
    }));

    return { priorityData, riskVsROI };
  }, [data]);

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Research Metrics</CardTitle>
          <CardDescription>Loading market intelligence...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error || !data?.researchDataset) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Research Metrics</CardTitle>
          <CardDescription>Real-time intelligence analytics</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-sm text-muted-foreground">No data available</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const summary = data.researchDataset.summary;
  const niches = data.researchDataset.niches;

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Key Performance Indicators */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Avg. Priority</p>
                <p className="text-2xl font-bold">{summary.averagePriorityScore}</p>
              </div>
              <Target className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Auto Ready</p>
                <p className="text-2xl font-bold text-green-600">{summary.highAutomationReadyCount}</p>
              </div>
              <Zap className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total ROI</p>
                <p className="text-2xl font-bold text-purple-600">
                  €{(summary.totalRealisticROI / 1000000).toFixed(1)}M
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Low Risk</p>
                <p className="text-2xl font-bold text-emerald-600">{summary.lowRiskHighRewardCount}</p>
              </div>
              <Award className="h-8 w-8 text-emerald-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Priority vs Automation Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="h-5 w-5 mr-2" />
              Priority vs Automation
            </CardTitle>
            <CardDescription>Top niches by priority and automation readiness</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData.priorityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="name" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip />
                <Bar dataKey="priority" fill="#3b82f6" name="Priority Score" />
                <Bar dataKey="automation" fill="#10b981" name="Automation %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Risk vs ROI Scatter */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Risk vs ROI Analysis
            </CardTitle>
            <CardDescription>Investment opportunity matrix</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData.riskVsROI.slice(0, 10)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="risk" name="Risk Score" />
                <YAxis dataKey="roi" name="ROI (K€)" />
                <Tooltip 
                  formatter={(value, name) => [
                    name === 'roi' ? `€${value}K` : value,
                    name === 'roi' ? 'ROI' : 'Risk'
                  ]}
                  labelFormatter={(label) => `Risk Score: ${label}`}
                />
                <Line 
                  type="monotone" 
                  dataKey="roi" 
                  stroke="#8b5cf6" 
                  strokeWidth={3}
                  dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Quick Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Brain className="h-5 w-5 mr-2" />
            AI-Powered Insights
          </CardTitle>
          <CardDescription>Real-time intelligence recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border rounded-lg">
              <div className="flex items-center mb-2">
                <Badge className="bg-green-500">Recommendation</Badge>
              </div>
              <h4 className="font-semibold mb-1">Immediate Action</h4>
              <p className="text-sm text-muted-foreground">
                Focus on {niches.filter((n: NicheAnalysis) => n.priority_score >= 90).length} high-priority niches 
                with {Math.round((summary.highAutomationReadyCount / summary.totalNiches) * 100)}% automation ready.
              </p>
            </div>

            <div className="p-4 border rounded-lg">
              <div className="flex items-center mb-2">
                <Badge variant="secondary">Risk Analysis</Badge>
              </div>
              <h4 className="font-semibold mb-1">Investment Safety</h4>
              <p className="text-sm text-muted-foreground">
                {niches.filter((n: NicheAnalysis) => n.risk_assessment_score <= 35).length} low-risk opportunities 
                with combined ROI of €{(niches.filter((n: NicheAnalysis) => n.risk_assessment_score <= 35).reduce((sum: number, n: NicheAnalysis) => sum + n.roi_projection.realistic, 0) / 1000).toFixed(0)}K.
              </p>
            </div>

            <div className="p-4 border rounded-lg">
              <div className="flex items-center mb-2">
                <Badge variant="outline">Scaling</Badge>
              </div>
              <h4 className="font-semibold mb-1">Growth Potential</h4>
              <p className="text-sm text-muted-foreground">
                Top performer: {niches.reduce((top: NicheAnalysis | null, n: NicheAnalysis) => 
                  !top || n.priority_score > top.priority_score ? n : top, null)?.niche_name} 
                with {niches.reduce((top: NicheAnalysis | null, n: NicheAnalysis) => 
                  !top || n.priority_score > top.priority_score ? n : top, null)?.priority_score} priority.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}