import { useQuery } from '@apollo/client';
import { GET_RESEARCH_DATASET } from '../../graphql/queries';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp,
  Target,
  Zap,
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Shield,
  Star,
  BarChart3
} from 'lucide-react';
import type { NicheAnalysis } from '@intelligence-dashboard/shared';

interface ResearchOverviewProps {
  className?: string;
}

export function ResearchOverview({ className }: ResearchOverviewProps) {
  const { data, loading, error } = useQuery(GET_RESEARCH_DATASET, {
    pollInterval: 60000, // Refresh every minute
  });

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Research Intelligence Overview</CardTitle>
          <CardDescription>Loading comprehensive market analysis...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Research Intelligence Overview</CardTitle>
          <CardDescription>Error loading research data</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <AlertTriangle className="h-8 w-8 mx-auto mb-2 text-red-500" />
            <p className="text-sm text-muted-foreground">{error.message}</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const summary = data?.researchDataset?.summary;
  const niches = data?.researchDataset?.niches || [];

  // Calculate insights
  const topPerformer = niches.reduce((top: NicheAnalysis | null, niche: NicheAnalysis) => 
    !top || niche.priority_score > top.priority_score ? niche : top, null
  );

  const highROINiches = niches.filter((n: NicheAnalysis) => n.roi_projection.realistic >= 150000);
  const lowRiskNiches = niches.filter((n: NicheAnalysis) => n.risk_assessment_score <= 35);
  const automationReady = niches.filter((n: NicheAnalysis) => n.automation_ready_score >= 9);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatMillions = (amount: number) => {
    return `€${(amount / 1000000).toFixed(1)}M`;
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Market Coverage</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary?.totalNiches || 0}</div>
            <p className="text-xs text-muted-foreground">
              Comprehensive niches analyzed
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total ROI Potential</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {formatMillions(summary?.totalRealisticROI || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Realistic revenue projection
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Automation Ready</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {summary?.highAutomationReadyCount || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Ready for immediate scaling
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Quality Score</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">
              {summary?.averagePriorityScore || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Average priority rating
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Key Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Performer */}
        {topPerformer && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-green-500" />
                Top Priority Niche
              </CardTitle>
              <CardDescription>Highest scoring market opportunity</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-lg">{topPerformer.niche_name}</h3>
                    <Badge className="bg-green-500">
                      {topPerformer.priority_score} Priority
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">
                    {topPerformer.description}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">ROI Potential:</span>
                    <div className="font-semibold text-green-600">
                      {formatCurrency(topPerformer.roi_projection.realistic)}
                    </div>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Automation Score:</span>
                    <div className="font-semibold">
                      {topPerformer.automation_ready_score}/10
                    </div>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Risk Level:</span>
                    <div className="font-semibold">
                      {topPerformer.risk_assessment_score <= 35 ? 'Low' : 
                       topPerformer.risk_assessment_score <= 55 ? 'Medium' : 'High'}
                    </div>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Implementation:</span>
                    <div className="font-semibold">
                      {topPerformer.implementation_difficulty <= 3 ? 'Easy' : 
                       topPerformer.implementation_difficulty <= 6 ? 'Medium' : 'Hard'}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Stats Grid */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="h-5 w-5 mr-2 text-blue-500" />
              Market Intelligence Summary
            </CardTitle>
            <CardDescription>Key performance indicators across all niches</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <DollarSign className="h-4 w-4 mr-2 text-green-500" />
                  <span className="text-sm">High ROI Opportunities</span>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{highROINiches.length}</div>
                  <div className="text-xs text-muted-foreground">≥€150K potential</div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Shield className="h-4 w-4 mr-2 text-blue-500" />
                  <span className="text-sm">Low Risk Markets</span>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{lowRiskNiches.length}</div>
                  <div className="text-xs text-muted-foreground">≤35 risk score</div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Zap className="h-4 w-4 mr-2 text-purple-500" />
                  <span className="text-sm">Automation Champions</span>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{automationReady.length}</div>
                  <div className="text-xs text-muted-foreground">9+ automation score</div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 mr-2 text-green-500" />
                  <span className="text-sm">Prime Investments</span>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{summary?.lowRiskHighRewardCount || 0}</div>
                  <div className="text-xs text-muted-foreground">Low risk + high reward</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top 5 Niches by Priority */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Star className="h-5 w-5 mr-2 text-yellow-500" />
            Top Priority Niches
          </CardTitle>
          <CardDescription>Highest priority market opportunities for immediate action</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...niches]
              .sort((a: NicheAnalysis, b: NicheAnalysis) => b.priority_score - a.priority_score)
              .slice(0, 5)
              .map((niche: NicheAnalysis, index: number) => (
                <div key={niche.niche_id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <h3 className="font-semibold">{niche.niche_name}</h3>
                      <p className="text-sm text-muted-foreground">
                        Priority: {niche.priority_score} • ROI: {formatCurrency(niche.roi_projection.realistic)}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant={niche.automation_ready_score >= 8 ? "default" : "secondary"}>
                      Auto: {niche.automation_ready_score}/10
                    </Badge>
                    <Badge variant={niche.risk_assessment_score <= 35 ? "default" : 
                                  niche.risk_assessment_score <= 55 ? "secondary" : "destructive"}>
                      Risk: {niche.risk_assessment_score <= 35 ? 'Low' : 
                            niche.risk_assessment_score <= 55 ? 'Med' : 'High'}
                    </Badge>
                  </div>
                </div>
              ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}