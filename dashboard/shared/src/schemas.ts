import { z } from 'zod';

export const ProcessStatusSchema = z.enum(['running', 'stopped', 'error', 'pending']);
export const ProcessTypeSchema = z.enum(['research', 'content', 'automation', 'analysis']);
export const LogLevelSchema = z.enum(['info', 'warn', 'error', 'debug']);

export const ProcessMetricsSchema = z.object({
  cpu: z.number().min(0).max(100),
  memory: z.number().min(0),
  requestsPerMinute: z.number().min(0),
  errorRate: z.number().min(0).max(100),
  avgResponseTime: z.number().min(0),
});

export const LogEntrySchema = z.object({
  id: z.string(),
  timestamp: z.coerce.date(),
  level: LogLevelSchema,
  message: z.string(),
  metadata: z.record(z.any()).optional(),
});

export const ProcessSchema = z.object({
  id: z.string(),
  name: z.string(),
  status: ProcessStatusSchema,
  type: ProcessTypeSchema,
  startTime: z.coerce.date(),
  lastUpdate: z.coerce.date(),
  progress: z.number().min(0).max(100),
  metrics: ProcessMetricsSchema,
  logs: z.array(LogEntrySchema),
});

export const EntityTypeSchema = z.enum(['person', 'organization', 'location', 'product', 'other']);
export const SentimentLabelSchema = z.enum(['positive', 'negative', 'neutral']);

export const EntitySchema = z.object({
  name: z.string(),
  type: EntityTypeSchema,
  confidence: z.number().min(0).max(1),
});

export const SentimentAnalysisSchema = z.object({
  score: z.number().min(-1).max(1),
  label: SentimentLabelSchema,
});

export const ResearchResultSchema: z.ZodType<any> = z.lazy(() =>
  z.object({
    id: z.string(),
    title: z.string(),
    content: z.string(),
    url: z.string().url().optional(),
    relevanceScore: z.number().min(0).max(1),
    entities: z.array(EntitySchema),
    sentiment: SentimentAnalysisSchema,
    children: z.array(ResearchResultSchema).optional(),
  })
);

export const ResearchMetadataSchema = z.object({
  duration: z.number().min(0),
  sources: z.array(z.string()),
  filters: z.record(z.any()),
});

export const ResearchDataSchema = z.object({
  id: z.string(),
  query: z.string(),
  results: z.array(ResearchResultSchema),
  timestamp: z.coerce.date(),
  source: z.string(),
  metadata: ResearchMetadataSchema,
});

export const PlatformSchema = z.enum(['perplexity', 'chatgpt', 'claude', 'bard', 'other']);

export const VoiceSearchMetricsSchema = z.object({
  queries: z.number().min(0),
  accuracy: z.number().min(0).max(100),
  avgResponseTime: z.number().min(0),
  topQueries: z.array(z.string()),
});

export const PlatformMetricsSchema = z.object({
  searchRanking: z.number().min(0),
  visibility: z.number().min(0).max(100),
  answerEnginePerformance: z.number().min(0).max(100),
  voiceSearchAnalytics: VoiceSearchMetricsSchema,
  competitorPosition: z.number().min(0),
});

export const AIMetricsSchema = z.object({
  id: z.string(),
  timestamp: z.coerce.date(),
  platform: PlatformSchema,
  metrics: PlatformMetricsSchema,
});

export const PredictionTypeSchema = z.enum(['trend', 'viral', 'market', 'competition']);
export const ImpactLevelSchema = z.enum(['low', 'medium', 'high']);

export const PredictionSchema = z.object({
  id: z.string(),
  type: PredictionTypeSchema,
  title: z.string(),
  probability: z.number().min(0).max(100),
  timeframe: z.string(),
  impact: ImpactLevelSchema,
  recommendations: z.array(z.string()),
});

export const TrendAnalysisSchema = z.object({
  topic: z.string(),
  momentum: z.number(),
  sentiment: z.number().min(-1).max(1),
  volume: z.number().min(0),
  projectedGrowth: z.number(),
  relatedTopics: z.array(z.string()),
});

export const DifficultySchema = z.enum(['easy', 'medium', 'hard']);

export const MarketOpportunitySchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  potentialRevenue: z.number().min(0),
  difficulty: DifficultySchema,
  timeToImplement: z.string(),
  requiredResources: z.array(z.string()),
});

export const ChannelPlatformSchema = z.enum(['youtube', 'tiktok', 'instagram', 'twitter', 'linkedin', 'other']);

export const ChannelMetricsSchema = z.object({
  followers: z.number().min(0),
  engagement: z.number().min(0).max(100),
  reach: z.number().min(0),
  impressions: z.number().min(0),
  conversions: z.number().min(0),
  revenue: z.number().min(0),
  roi: z.number(),
});

export const ContentTypeSchema = z.enum(['video', 'post', 'story', 'article', 'other']);

export const ContentPerformanceSchema = z.object({
  views: z.number().min(0),
  likes: z.number().min(0),
  shares: z.number().min(0),
  comments: z.number().min(0),
  saves: z.number().min(0),
  clickThrough: z.number().min(0).max(100),
  conversionRate: z.number().min(0).max(100),
});

export const ContentAdaptationSchema = z.object({
  platform: z.string(),
  format: z.string(),
  changes: z.array(z.string()),
  performance: ContentPerformanceSchema,
});

export const ContentItemSchema = z.object({
  id: z.string(),
  title: z.string(),
  type: ContentTypeSchema,
  publishedAt: z.coerce.date(),
  performance: ContentPerformanceSchema,
  adaptations: z.array(ContentAdaptationSchema),
});

export const ChannelPerformanceSchema = z.object({
  channelId: z.string(),
  channelName: z.string(),
  platform: ChannelPlatformSchema,
  metrics: ChannelMetricsSchema,
  content: z.array(ContentItemSchema),
});

export const AttributionSchema = z.object({
  touchpoint: z.string(),
  timestamp: z.coerce.date(),
  influence: z.number().min(0).max(100),
});

export const ChannelRevenueSchema = z.object({
  channelId: z.string(),
  channelName: z.string(),
  revenue: z.number().min(0),
  transactions: z.number().min(0),
  avgOrderValue: z.number().min(0),
  attribution: z.array(AttributionSchema),
});

export const ProductRevenueSchema = z.object({
  productId: z.string(),
  productName: z.string(),
  revenue: z.number().min(0),
  units: z.number().min(0),
  refunds: z.number().min(0),
  netRevenue: z.number(),
});

export const SegmentLTVSchema = z.object({
  segment: z.string(),
  value: z.number().min(0),
  customers: z.number().min(0),
  churnRate: z.number().min(0).max(100),
});

export const LTVProjectionSchema = z.object({
  period: z.string(),
  value: z.number().min(0),
  confidence: z.number().min(0).max(100),
});

export const CustomerLTVSchema = z.object({
  average: z.number().min(0),
  bySegment: z.array(SegmentLTVSchema),
  projections: z.array(LTVProjectionSchema),
});

export const RevenueDataSchema = z.object({
  id: z.string(),
  timestamp: z.coerce.date(),
  actual: z.number().min(0),
  projected: z.number().min(0),
  byChannel: z.array(ChannelRevenueSchema),
  byProduct: z.array(ProductRevenueSchema),
  ltv: CustomerLTVSchema,
});

export const AutomationStatusSchema = z.enum(['healthy', 'degraded', 'failed']);

export const APIUsageSchema = z.object({
  service: z.string(),
  calls: z.number().min(0),
  limit: z.number().min(0),
  remaining: z.number().min(0),
  resetAt: z.coerce.date(),
});

export const ResourceUsageSchema = z.object({
  cpu: z.number().min(0).max(100),
  memory: z.number().min(0).max(100),
  storage: z.number().min(0).max(100),
  bandwidth: z.number().min(0).max(100),
});

export const AutomationMetricsSchema = z.object({
  executionTime: z.number().min(0),
  successRate: z.number().min(0).max(100),
  itemsProcessed: z.number().min(0),
  apiUsage: z.array(APIUsageSchema),
  resourceUsage: ResourceUsageSchema,
});

export const AutomationErrorSchema = z.object({
  id: z.string(),
  timestamp: z.coerce.date(),
  type: z.string(),
  message: z.string(),
  stackTrace: z.string().optional(),
  resolved: z.boolean(),
  resolution: z.string().optional(),
});

export const AutomationHealthSchema = z.object({
  workflowId: z.string(),
  workflowName: z.string(),
  status: AutomationStatusSchema,
  uptime: z.number().min(0).max(100),
  lastRun: z.coerce.date(),
  nextRun: z.coerce.date(),
  metrics: AutomationMetricsSchema,
  errors: z.array(AutomationErrorSchema),
});

export const ScalingTypeSchema = z.enum(['opportunity', 'bottleneck', 'resource', 'expansion']);
export const PrioritySchema = z.enum(['low', 'medium', 'high', 'critical']);
export const EffortSchema = z.enum(['low', 'medium', 'high']);

export const ScalingImpactSchema = z.object({
  revenue: z.number(),
  efficiency: z.number(),
  risk: z.number(),
  timeframe: z.string(),
});

export const ScalingActionSchema = z.object({
  id: z.string(),
  action: z.string(),
  effort: EffortSchema,
  cost: z.number().min(0),
  expectedResult: z.string(),
  dependencies: z.array(z.string()),
});

export const ScalingRecommendationSchema = z.object({
  id: z.string(),
  timestamp: z.coerce.date(),
  type: ScalingTypeSchema,
  priority: PrioritySchema,
  title: z.string(),
  description: z.string(),
  impact: ScalingImpactSchema,
  actions: z.array(ScalingActionSchema),
});

export const ThemeSchema = z.enum(['light', 'dark', 'auto']);
export const LayoutTypeSchema = z.enum(['grid', 'flex', 'custom']);

export const LayoutConfigSchema = z.object({
  type: LayoutTypeSchema,
  columns: z.number().min(1).max(24),
  gap: z.number().min(0),
});

export const WidgetPositionSchema = z.object({
  x: z.number().min(0),
  y: z.number().min(0),
  width: z.number().min(1),
  height: z.number().min(1),
});

export const WidgetConfigSchema = z.object({
  id: z.string(),
  type: z.string(),
  position: WidgetPositionSchema,
  settings: z.record(z.any()),
  dataSource: z.string(),
});

export const DashboardConfigSchema = z.object({
  refreshInterval: z.number().min(1000),
  theme: ThemeSchema,
  layout: LayoutConfigSchema,
  widgets: z.array(WidgetConfigSchema),
});

export const WebSocketMessageTypeSchema = z.enum([
  'process_update',
  'metric_update',
  'alert',
  'research_result',
  'revenue_update',
]);

export const WebSocketMessageSchema = z.object({
  type: WebSocketMessageTypeSchema,
  data: z.any(),
  timestamp: z.coerce.date(),
});