export interface Process {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error' | 'pending';
  type: 'research' | 'content' | 'automation' | 'analysis';
  startTime: Date;
  lastUpdate: Date;
  progress: number;
  metrics: ProcessMetrics;
  logs: LogEntry[];
}

export interface ProcessMetrics {
  cpu: number;
  memory: number;
  requestsPerMinute: number;
  errorRate: number;
  avgResponseTime: number;
}

export interface LogEntry {
  id: string;
  timestamp: Date;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  metadata?: Record<string, any>;
}

export interface ResearchData {
  id: string;
  query: string;
  results: ResearchResult[];
  timestamp: Date;
  source: string;
  metadata: ResearchMetadata;
}

export interface ResearchResult {
  id: string;
  title: string;
  content: string;
  url?: string;
  relevanceScore: number;
  entities: Entity[];
  sentiment: SentimentAnalysis;
  children?: ResearchResult[];
}

export interface Entity {
  name: string;
  type: 'person' | 'organization' | 'location' | 'product' | 'other';
  confidence: number;
}

export interface SentimentAnalysis {
  score: number;
  label: 'positive' | 'negative' | 'neutral';
}

export interface ResearchMetadata {
  duration: number;
  sources: string[];
  filters: Record<string, any>;
}

export interface AIMetrics {
  id: string;
  timestamp: Date;
  platform: 'perplexity' | 'chatgpt' | 'claude' | 'bard' | 'other';
  metrics: PlatformMetrics;
}

export interface PlatformMetrics {
  searchRanking: number;
  visibility: number;
  answerEnginePerformance: number;
  voiceSearchAnalytics: VoiceSearchMetrics;
  competitorPosition: number;
}

export interface VoiceSearchMetrics {
  queries: number;
  accuracy: number;
  avgResponseTime: number;
  topQueries: string[];
}

export interface PredictiveIntelligence {
  id: string;
  timestamp: Date;
  predictions: Prediction[];
  trends: TrendAnalysis[];
  opportunities: MarketOpportunity[];
}

export interface Prediction {
  id: string;
  type: 'trend' | 'viral' | 'market' | 'competition';
  title: string;
  probability: number;
  timeframe: string;
  impact: 'low' | 'medium' | 'high';
  recommendations: string[];
}

export interface TrendAnalysis {
  topic: string;
  momentum: number;
  sentiment: number;
  volume: number;
  projectedGrowth: number;
  relatedTopics: string[];
}

export interface MarketOpportunity {
  id: string;
  title: string;
  description: string;
  potentialRevenue: number;
  difficulty: 'easy' | 'medium' | 'hard';
  timeToImplement: string;
  requiredResources: string[];
}

export interface ChannelPerformance {
  channelId: string;
  channelName: string;
  platform: 'youtube' | 'tiktok' | 'instagram' | 'twitter' | 'linkedin' | 'other';
  metrics: ChannelMetrics;
  content: ContentItem[];
}

export interface ChannelMetrics {
  followers: number;
  engagement: number;
  reach: number;
  impressions: number;
  conversions: number;
  revenue: number;
  roi: number;
}

export interface ContentItem {
  id: string;
  title: string;
  type: 'video' | 'post' | 'story' | 'article' | 'other';
  publishedAt: Date;
  performance: ContentPerformance;
  adaptations: ContentAdaptation[];
}

export interface ContentPerformance {
  views: number;
  likes: number;
  shares: number;
  comments: number;
  saves: number;
  clickThrough: number;
  conversionRate: number;
}

export interface ContentAdaptation {
  platform: string;
  format: string;
  changes: string[];
  performance: ContentPerformance;
}

export interface RevenueData {
  id: string;
  timestamp: Date;
  actual: number;
  projected: number;
  byChannel: ChannelRevenue[];
  byProduct: ProductRevenue[];
  ltv: CustomerLTV;
}

export interface ChannelRevenue {
  channelId: string;
  channelName: string;
  revenue: number;
  transactions: number;
  avgOrderValue: number;
  attribution: Attribution[];
}

export interface Attribution {
  touchpoint: string;
  timestamp: Date;
  influence: number;
}

export interface ProductRevenue {
  productId: string;
  productName: string;
  revenue: number;
  units: number;
  refunds: number;
  netRevenue: number;
}

export interface CustomerLTV {
  average: number;
  bySegment: SegmentLTV[];
  projections: LTVProjection[];
}

export interface SegmentLTV {
  segment: string;
  value: number;
  customers: number;
  churnRate: number;
}

export interface LTVProjection {
  period: string;
  value: number;
  confidence: number;
}

export interface AutomationHealth {
  workflowId: string;
  workflowName: string;
  status: 'healthy' | 'degraded' | 'failed';
  uptime: number;
  lastRun: Date;
  nextRun: Date;
  metrics: AutomationMetrics;
  errors: AutomationError[];
}

export interface AutomationMetrics {
  executionTime: number;
  successRate: number;
  itemsProcessed: number;
  apiUsage: APIUsage[];
  resourceUsage: ResourceUsage;
}

export interface APIUsage {
  service: string;
  calls: number;
  limit: number;
  remaining: number;
  resetAt: Date;
}

export interface ResourceUsage {
  cpu: number;
  memory: number;
  storage: number;
  bandwidth: number;
}

export interface AutomationError {
  id: string;
  timestamp: Date;
  type: string;
  message: string;
  stackTrace?: string;
  resolved: boolean;
  resolution?: string;
}

export interface ScalingRecommendation {
  id: string;
  timestamp: Date;
  type: 'opportunity' | 'bottleneck' | 'resource' | 'expansion';
  priority: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  impact: ScalingImpact;
  actions: ScalingAction[];
}

export interface ScalingImpact {
  revenue: number;
  efficiency: number;
  risk: number;
  timeframe: string;
}

export interface ScalingAction {
  id: string;
  action: string;
  effort: 'low' | 'medium' | 'high';
  cost: number;
  expectedResult: string;
  dependencies: string[];
}

export interface DashboardConfig {
  refreshInterval: number;
  theme: 'light' | 'dark' | 'auto';
  layout: LayoutConfig;
  widgets: WidgetConfig[];
}

export interface LayoutConfig {
  type: 'grid' | 'flex' | 'custom';
  columns: number;
  gap: number;
}

export interface WidgetConfig {
  id: string;
  type: string;
  position: WidgetPosition;
  settings: Record<string, any>;
  dataSource: string;
}

export interface WidgetPosition {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface WebSocketMessage {
  type: 'process_update' | 'metric_update' | 'alert' | 'research_result' | 'revenue_update';
  data: any;
  timestamp: Date;
}

// Research Intelligence System Types
export interface NicheAnalysis {
  niche_id: string;
  niche_name: string;
  description: string;
  priority_score: number;
  implementation_difficulty: number;
  roi_projection: {
    conservative: number;
    realistic: number;
    optimistic: number;
  };
  quick_win_opportunities: string[];
  automation_ready_score: number;
  market_saturation_index: number;
  competition_intensity_score: number;
  virality_potential_score: number;
  scalability_score: number;
  risk_assessment_score: number;
}

export interface ResearchPersona {
  persona_id: string;
  persona_name: string;
  niche_id: string;
  age_range: string;
  psychographics: {
    personality_types: string[];
    values: string[];
    interests: string[];
  };
  behavioral_triggers: string[];
  emotional_states: string[];
  device_usage: {
    mobile: number;
    desktop: number;
    tablet: number;
  };
}

export interface NicheMetrics {
  [niche_id: string]: {
    health_score: number;
    alert_thresholds: {
      conversion_rate_min: number;
      bounce_rate_max: number;
    };
    performance_triggers: {
      [trigger_name: string]: string;
    };
    optimization_priorities: string[];
    investment_priority_rank: number;
  };
}

export interface ImplementationRoadmap {
  phase: string;
  [key: string]: any; // Dynamic milestone properties
}

export interface ResearchDataset {
  niches: NicheAnalysis[];
  personas: ResearchPersona[];
  metrics: NicheMetrics;
  roadmaps: ImplementationRoadmap[];
  summary: {
    totalNiches: number;
    averagePriorityScore: number;
    totalConservativeROI: number;
    totalRealisticROI: number;
    totalOptimisticROI: number;
    highAutomationReadyCount: number;
    lowRiskHighRewardCount: number;
  };
}