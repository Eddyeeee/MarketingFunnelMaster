import React, { useState, useMemo } from 'react';
import { useQuery } from '@apollo/client';
import { GET_RESEARCH_DATASET } from '../../graphql/queries';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { 
  BarChart3,
  TrendingUp,
  Target,
  Zap,
  AlertTriangle,
  DollarSign,
  Users,
  Brain,
  Search,
  Filter,
  ArrowUp,
  ArrowDown,
  Star,
  Clock,
  Shield
} from 'lucide-react';


interface ResearchIntelligenceProps {
  className?: string;
}

export function ResearchIntelligence({ className }: ResearchIntelligenceProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState<number | null>(null);
  const [riskFilter, setRiskFilter] = useState<number | null>(null);
  const [selectedNiche, setSelectedNiche] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'analysis'>('grid');

  const { data, loading, error } = useQuery(GET_RESEARCH_DATASET, {
    pollInterval: 30000, // Refresh every 30 seconds
  });

  const filteredNiches = useMemo(() => {
    if (!data?.researchDataset?.niches) return [];
    
    let filtered = data.researchDataset.niches;
    
    if (searchQuery) {
      filtered = filtered.filter((niche: any) =>
        niche.niche_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        niche.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    if (priorityFilter !== null) {
      filtered = filtered.filter((niche: any) => niche.priority_score >= priorityFilter);
    }
    
    if (riskFilter !== null) {
      filtered = filtered.filter((niche: any) => niche.risk_assessment_score <= riskFilter);
    }
    
    return filtered.sort((a: any, b: any) => b.priority_score - a.priority_score);
  }, [data, searchQuery, priorityFilter, riskFilter]);

  const selectedNicheData = useMemo(() => {
    if (!selectedNiche || !data?.researchDataset?.niches) return null;
    return data.researchDataset.niches.find((n: any) => n.niche_id === selectedNiche);
  }, [selectedNiche, data]);

  const selectedPersona = useMemo(() => {
    if (!selectedNiche || !data?.researchDataset?.personas) return null;
    return data.researchDataset.personas.find((p: any) => p.niche_id === selectedNiche);
  }, [selectedNiche, data]);

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Research Intelligence</CardTitle>
          <CardDescription>Loading research data...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12">
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
          <CardTitle>Research Intelligence</CardTitle>
          <CardDescription>Error loading research data</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-red-500" />
            <p className="text-muted-foreground">{error.message}</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const summary = data?.researchDataset?.summary;

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getPriorityColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getRiskColor = (score: number) => {
    if (score <= 30) return 'text-green-600 bg-green-100';
    if (score <= 50) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Summary Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Niches</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary?.totalNiches || 0}</div>
            <p className="text-xs text-muted-foreground">
              Avg Priority: {summary?.averagePriorityScore || 0}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total ROI Potential</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(summary?.totalRealisticROI || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Conservative: {formatCurrency(summary?.totalConservativeROI || 0)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Automation Ready</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary?.highAutomationReadyCount || 0}</div>
            <p className="text-xs text-muted-foreground">
              Ready for immediate automation
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Low Risk High Reward</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary?.lowRiskHighRewardCount || 0}</div>
            <p className="text-xs text-muted-foreground">
              Prime investment opportunities
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Controls */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-4 sm:space-y-0">
            <div>
              <CardTitle>Market Niches Analysis</CardTitle>
              <CardDescription>
                AI-powered niche analysis with ROI projections and automation readiness scores
              </CardDescription>
            </div>
            <div className="flex space-x-2">
              <Button
                variant={viewMode === 'grid' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('grid')}
              >
                Grid
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('list')}
              >
                List
              </Button>
              <Button
                variant={viewMode === 'analysis' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('analysis')}
              >
                Analysis
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2 mb-4">
            <div className="relative flex-1">
              <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search niches..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8"
              />
            </div>
            <div className="flex space-x-2">
              <Input
                type="number"
                placeholder="Min Priority"
                value={priorityFilter || ''}
                onChange={(e) => setPriorityFilter(e.target.value ? Number(e.target.value) : null)}
                className="w-32"
              />
              <Input
                type="number"
                placeholder="Max Risk"
                value={riskFilter || ''}
                onChange={(e) => setRiskFilter(e.target.value ? Number(e.target.value) : null)}
                className="w-32"
              />
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setSearchQuery('');
                  setPriorityFilter(null);
                  setRiskFilter(null);
                }}
              >
                <Filter className="h-4 w-4" />
                Clear
              </Button>
            </div>
          </div>

          {/* Niche Grid/List View */}
          {viewMode === 'grid' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredNiches.map((niche: any) => (
                <Card
                  key={niche.niche_id}
                  className={`cursor-pointer transition-all hover:shadow-md ${
                    selectedNiche === niche.niche_id ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => setSelectedNiche(niche.niche_id)}
                >
                  <CardHeader className="pb-2">
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-base">{niche.niche_name}</CardTitle>
                      <Badge className={getPriorityColor(niche.priority_score)}>
                        {niche.priority_score}
                      </Badge>
                    </div>
                    <CardDescription className="text-sm line-clamp-2">
                      {niche.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">ROI (Realistic)</span>
                      <span className="font-semibold text-green-600">
                        {formatCurrency(niche.roi_projection.realistic)}
                      </span>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Automation Ready</span>
                        <span>{niche.automation_ready_score}/10</span>
                      </div>
                      <Progress value={niche.automation_ready_score * 10} className="h-2" />
                    </div>

                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Risk Level</span>
                      <Badge className={getRiskColor(niche.risk_assessment_score)}>
                        {niche.risk_assessment_score <= 30 ? 'Low' : 
                         niche.risk_assessment_score <= 50 ? 'Medium' : 'High'}
                      </Badge>
                    </div>

                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Difficulty</span>
                      <div className="flex">
                        {Array.from({ length: Math.ceil(niche.implementation_difficulty / 2) }).map((_, i) => (
                          <Star key={i} className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {viewMode === 'list' && (
            <div className="space-y-2">
              {filteredNiches.map((niche: any) => (
                <Card
                  key={niche.niche_id}
                  className={`cursor-pointer transition-all hover:shadow-sm ${
                    selectedNiche === niche.niche_id ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => setSelectedNiche(niche.niche_id)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <h3 className="font-semibold">{niche.niche_name}</h3>
                          <Badge className={getPriorityColor(niche.priority_score)}>
                            {niche.priority_score}
                          </Badge>
                          <Badge className={getRiskColor(niche.risk_assessment_score)}>
                            Risk: {niche.risk_assessment_score}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground mt-1 line-clamp-1">
                          {niche.description}
                        </p>
                      </div>
                      <div className="flex items-center space-x-4 text-sm">
                        <div className="text-center">
                          <div className="font-semibold text-green-600">
                            {formatCurrency(niche.roi_projection.realistic)}
                          </div>
                          <div className="text-muted-foreground">ROI</div>
                        </div>
                        <div className="text-center">
                          <div className="font-semibold">{niche.automation_ready_score}/10</div>
                          <div className="text-muted-foreground">Automation</div>
                        </div>
                        <div className="text-center">
                          <div className="font-semibold">{niche.virality_potential_score}</div>
                          <div className="text-muted-foreground">Virality</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {viewMode === 'analysis' && selectedNicheData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Detailed Niche Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle>{selectedNicheData.niche_name}</CardTitle>
                  <CardDescription>{selectedNicheData.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-sm text-muted-foreground">Priority Score</div>
                      <div className="text-2xl font-bold">{selectedNicheData.priority_score}</div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">Implementation Difficulty</div>
                      <div className="text-2xl font-bold">{selectedNicheData.implementation_difficulty}/10</div>
                    </div>
                  </div>

                  <div>
                    <div className="text-sm text-muted-foreground mb-2">ROI Projections</div>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Conservative</span>
                        <span className="font-semibold text-green-600">
                          {formatCurrency(selectedNicheData.roi_projection.conservative)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Realistic</span>
                        <span className="font-semibold text-green-600">
                          {formatCurrency(selectedNicheData.roi_projection.realistic)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Optimistic</span>
                        <span className="font-semibold text-green-600">
                          {formatCurrency(selectedNicheData.roi_projection.optimistic)}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <div className="text-sm text-muted-foreground mb-2">Quick Win Opportunities</div>
                    <div className="space-y-1">
                      {selectedNicheData.quick_win_opportunities.map((opportunity: string, index: number) => (
                        <div key={index} className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-green-500 rounded-full" />
                          <span className="text-sm">{opportunity}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Persona Analysis */}
              {selectedPersona && (
                <Card>
                  <CardHeader>
                    <CardTitle>Target Persona</CardTitle>
                    <CardDescription>{selectedPersona.persona_name}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Demographics</div>
                      <div className="flex items-center space-x-2">
                        <Users className="h-4 w-4 text-muted-foreground" />
                        <span>Age Range: {selectedPersona.age_range}</span>
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Device Usage</div>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Mobile</span>
                          <span>{Math.round(selectedPersona.device_usage.mobile * 100)}%</span>
                        </div>
                        <Progress value={selectedPersona.device_usage.mobile * 100} className="h-2" />
                        
                        <div className="flex justify-between">
                          <span>Desktop</span>
                          <span>{Math.round(selectedPersona.device_usage.desktop * 100)}%</span>
                        </div>
                        <Progress value={selectedPersona.device_usage.desktop * 100} className="h-2" />
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Core Values</div>
                      <div className="flex flex-wrap gap-1">
                        {selectedPersona.psychographics.values.map((value: string, index: number) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {value}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Behavioral Triggers</div>
                      <div className="space-y-1">
                        {selectedPersona.behavioral_triggers.slice(0, 3).map((trigger: string, index: number) => (
                          <div key={index} className="flex items-center space-x-2">
                            <Target className="h-3 w-3 text-blue-500" />
                            <span className="text-sm">{trigger}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {filteredNiches.length === 0 && (
            <div className="text-center py-12">
              <Search className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground">No niches match your current filters</p>
              <Button
                variant="outline"
                className="mt-4"
                onClick={() => {
                  setSearchQuery('');
                  setPriorityFilter(null);
                  setRiskFilter(null);
                }}
              >
                Clear Filters
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}