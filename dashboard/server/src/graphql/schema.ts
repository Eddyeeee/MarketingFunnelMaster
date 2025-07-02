import { gql } from 'graphql-tag';

export const typeDefs = gql`
  scalar Date
  scalar JSON

  type Query {
    processes: [Process!]!
    process(id: ID!): Process
    searchResearch(query: String!, filters: JSON): [ResearchData!]!
    aiMetrics(platform: String, timeframe: String): [AIMetrics!]!
    revenueData(timeframe: String): RevenueData
    channelPerformance(channelId: String): [ChannelPerformance!]!
    automationHealth: [AutomationHealth!]!
    scalingRecommendations(priority: String): [ScalingRecommendation!]!
    predictiveIntelligence(type: String): PredictiveIntelligence
    dashboardConfig: DashboardConfig!
    
    # Research Intelligence System
    researchDataset: ResearchDataset!
    niches(filters: NicheFilters): [NicheAnalysis!]!
    niche(nicheId: String!): NicheAnalysis
    persona(nicheId: String!): ResearchPersona
    nicheMetrics(nicheId: String!): NicheMetricsData
    implementationRoadmaps: [ImplementationRoadmap!]!
  }

  type Mutation {
    startProcess(input: StartProcessInput!): Process!
    stopProcess(id: ID!): Process!
    updateProcessStatus(id: ID!, status: ProcessStatus!): Process!
    createResearchQuery(input: ResearchQueryInput!): ResearchData!
    updateDashboardConfig(input: DashboardConfigInput!): DashboardConfig!
    acknowledgeAlert(id: ID!): Boolean!
    executeScalingAction(recommendationId: ID!, actionId: ID!): Boolean!
    restartAutomation(workflowId: ID!): AutomationHealth!
  }

  type Subscription {
    processUpdated: Process!
    metricsUpdated: AIMetrics!
    revenueUpdated: RevenueData!
    alertReceived: Alert!
    researchCompleted: ResearchData!
  }

  enum ProcessStatus {
    RUNNING
    STOPPED
    ERROR
    PENDING
  }

  enum ProcessType {
    RESEARCH
    CONTENT
    AUTOMATION
    ANALYSIS
  }

  enum LogLevel {
    INFO
    WARN
    ERROR
    DEBUG
  }

  type Process {
    id: ID!
    name: String!
    status: ProcessStatus!
    type: ProcessType!
    startTime: Date!
    lastUpdate: Date!
    progress: Float!
    metrics: ProcessMetrics!
    logs: [LogEntry!]!
  }

  type ProcessMetrics {
    cpu: Float!
    memory: Float!
    requestsPerMinute: Float!
    errorRate: Float!
    avgResponseTime: Float!
  }

  type LogEntry {
    id: ID!
    timestamp: Date!
    level: LogLevel!
    message: String!
    metadata: JSON
  }

  type ResearchData {
    id: ID!
    query: String!
    results: [ResearchResult!]!
    timestamp: Date!
    source: String!
    metadata: ResearchMetadata!
  }

  type ResearchResult {
    id: ID!
    title: String!
    content: String!
    url: String
    relevanceScore: Float!
    entities: [Entity!]!
    sentiment: SentimentAnalysis!
    children: [ResearchResult!]
  }

  type Entity {
    name: String!
    type: EntityType!
    confidence: Float!
  }

  enum EntityType {
    PERSON
    ORGANIZATION
    LOCATION
    PRODUCT
    OTHER
  }

  type SentimentAnalysis {
    score: Float!
    label: SentimentLabel!
  }

  enum SentimentLabel {
    POSITIVE
    NEGATIVE
    NEUTRAL
  }

  type ResearchMetadata {
    duration: Float!
    sources: [String!]!
    filters: JSON!
  }

  type AIMetrics {
    id: ID!
    timestamp: Date!
    platform: Platform!
    metrics: PlatformMetrics!
  }

  enum Platform {
    PERPLEXITY
    CHATGPT
    CLAUDE
    BARD
    OTHER
  }

  type PlatformMetrics {
    searchRanking: Float!
    visibility: Float!
    answerEnginePerformance: Float!
    voiceSearchAnalytics: VoiceSearchMetrics!
    competitorPosition: Float!
  }

  type VoiceSearchMetrics {
    queries: Int!
    accuracy: Float!
    avgResponseTime: Float!
    topQueries: [String!]!
  }

  type PredictiveIntelligence {
    id: ID!
    timestamp: Date!
    predictions: [Prediction!]!
    trends: [TrendAnalysis!]!
    opportunities: [MarketOpportunity!]!
  }

  type Prediction {
    id: ID!
    type: PredictionType!
    title: String!
    probability: Float!
    timeframe: String!
    impact: ImpactLevel!
    recommendations: [String!]!
  }

  enum PredictionType {
    TREND
    VIRAL
    MARKET
    COMPETITION
  }

  enum ImpactLevel {
    LOW
    MEDIUM
    HIGH
  }

  type TrendAnalysis {
    topic: String!
    momentum: Float!
    sentiment: Float!
    volume: Float!
    projectedGrowth: Float!
    relatedTopics: [String!]!
  }

  type MarketOpportunity {
    id: ID!
    title: String!
    description: String!
    potentialRevenue: Float!
    difficulty: Difficulty!
    timeToImplement: String!
    requiredResources: [String!]!
  }

  enum Difficulty {
    EASY
    MEDIUM
    HARD
  }

  type ChannelPerformance {
    channelId: ID!
    channelName: String!
    platform: ChannelPlatform!
    metrics: ChannelMetrics!
    content: [ContentItem!]!
  }

  enum ChannelPlatform {
    YOUTUBE
    TIKTOK
    INSTAGRAM
    TWITTER
    LINKEDIN
    OTHER
  }

  type ChannelMetrics {
    followers: Int!
    engagement: Float!
    reach: Int!
    impressions: Int!
    conversions: Int!
    revenue: Float!
    roi: Float!
  }

  type ContentItem {
    id: ID!
    title: String!
    type: ContentType!
    publishedAt: Date!
    performance: ContentPerformance!
    adaptations: [ContentAdaptation!]!
  }

  enum ContentType {
    VIDEO
    POST
    STORY
    ARTICLE
    OTHER
  }

  type ContentPerformance {
    views: Int!
    likes: Int!
    shares: Int!
    comments: Int!
    saves: Int!
    clickThrough: Float!
    conversionRate: Float!
  }

  type ContentAdaptation {
    platform: String!
    format: String!
    changes: [String!]!
    performance: ContentPerformance!
  }

  type RevenueData {
    id: ID!
    timestamp: Date!
    actual: Float!
    projected: Float!
    byChannel: [ChannelRevenue!]!
    byProduct: [ProductRevenue!]!
    ltv: CustomerLTV!
  }

  type ChannelRevenue {
    channelId: ID!
    channelName: String!
    revenue: Float!
    transactions: Int!
    avgOrderValue: Float!
    attribution: [Attribution!]!
  }

  type Attribution {
    touchpoint: String!
    timestamp: Date!
    influence: Float!
  }

  type ProductRevenue {
    productId: ID!
    productName: String!
    revenue: Float!
    units: Int!
    refunds: Int!
    netRevenue: Float!
  }

  type CustomerLTV {
    average: Float!
    bySegment: [SegmentLTV!]!
    projections: [LTVProjection!]!
  }

  type SegmentLTV {
    segment: String!
    value: Float!
    customers: Int!
    churnRate: Float!
  }

  type LTVProjection {
    period: String!
    value: Float!
    confidence: Float!
  }

  type AutomationHealth {
    workflowId: ID!
    workflowName: String!
    status: AutomationStatus!
    uptime: Float!
    lastRun: Date!
    nextRun: Date!
    metrics: AutomationMetrics!
    errors: [AutomationError!]!
  }

  enum AutomationStatus {
    HEALTHY
    DEGRADED
    FAILED
  }

  type AutomationMetrics {
    executionTime: Float!
    successRate: Float!
    itemsProcessed: Int!
    apiUsage: [APIUsage!]!
    resourceUsage: ResourceUsage!
  }

  type APIUsage {
    service: String!
    calls: Int!
    limit: Int!
    remaining: Int!
    resetAt: Date!
  }

  type ResourceUsage {
    cpu: Float!
    memory: Float!
    storage: Float!
    bandwidth: Float!
  }

  type AutomationError {
    id: ID!
    timestamp: Date!
    type: String!
    message: String!
    stackTrace: String
    resolved: Boolean!
    resolution: String
  }

  type ScalingRecommendation {
    id: ID!
    timestamp: Date!
    type: ScalingType!
    priority: Priority!
    title: String!
    description: String!
    impact: ScalingImpact!
    actions: [ScalingAction!]!
  }

  enum ScalingType {
    OPPORTUNITY
    BOTTLENECK
    RESOURCE
    EXPANSION
  }

  enum Priority {
    LOW
    MEDIUM
    HIGH
    CRITICAL
  }

  type ScalingImpact {
    revenue: Float!
    efficiency: Float!
    risk: Float!
    timeframe: String!
  }

  type ScalingAction {
    id: ID!
    action: String!
    effort: Effort!
    cost: Float!
    expectedResult: String!
    dependencies: [String!]!
  }

  enum Effort {
    LOW
    MEDIUM
    HIGH
  }

  type DashboardConfig {
    refreshInterval: Int!
    theme: Theme!
    layout: LayoutConfig!
    widgets: [WidgetConfig!]!
  }

  enum Theme {
    LIGHT
    DARK
    AUTO
  }

  type LayoutConfig {
    type: LayoutType!
    columns: Int!
    gap: Int!
  }

  enum LayoutType {
    GRID
    FLEX
    CUSTOM
  }

  type WidgetConfig {
    id: ID!
    type: String!
    position: WidgetPosition!
    settings: JSON!
    dataSource: String!
  }

  type WidgetPosition {
    x: Int!
    y: Int!
    width: Int!
    height: Int!
  }

  type Alert {
    id: ID!
    timestamp: Date!
    level: AlertLevel!
    title: String!
    message: String!
    data: JSON
    acknowledged: Boolean!
  }

  enum AlertLevel {
    INFO
    WARNING
    ERROR
    CRITICAL
  }

  input StartProcessInput {
    name: String!
    type: ProcessType!
    config: JSON
  }

  input ResearchQueryInput {
    query: String!
    sources: [String!]
    filters: JSON
  }

  input DashboardConfigInput {
    refreshInterval: Int
    theme: Theme
    layout: LayoutConfigInput
    widgets: [WidgetConfigInput!]
  }

  input LayoutConfigInput {
    type: LayoutType
    columns: Int
    gap: Int
  }

  input WidgetConfigInput {
    id: ID!
    type: String!
    position: WidgetPositionInput!
    settings: JSON!
    dataSource: String!
  }

  input WidgetPositionInput {
    x: Int!
    y: Int!
    width: Int!
    height: Int!
  }

  # Research Intelligence System Types
  type ResearchDataset {
    niches: [NicheAnalysis!]!
    personas: [ResearchPersona!]!
    metrics: JSON!
    roadmaps: [ImplementationRoadmap!]!
    summary: ResearchSummary!
  }

  type NicheAnalysis {
    niche_id: ID!
    niche_name: String!
    description: String!
    priority_score: Float!
    implementation_difficulty: Float!
    roi_projection: ROIProjection!
    quick_win_opportunities: [String!]!
    automation_ready_score: Float!
    market_saturation_index: Float!
    competition_intensity_score: Float!
    virality_potential_score: Float!
    scalability_score: Float!
    risk_assessment_score: Float!
  }

  type ROIProjection {
    conservative: Float!
    realistic: Float!
    optimistic: Float!
  }

  type ResearchPersona {
    persona_id: ID!
    persona_name: String!
    niche_id: String!
    age_range: String!
    psychographics: Psychographics!
    behavioral_triggers: [String!]!
    emotional_states: [String!]!
    device_usage: DeviceUsage!
  }

  type Psychographics {
    personality_types: [String!]!
    values: [String!]!
    interests: [String!]!
  }

  type DeviceUsage {
    mobile: Float!
    desktop: Float!
    tablet: Float!
  }

  type NicheMetricsData {
    health_score: Float!
    alert_thresholds: AlertThresholds!
    performance_triggers: JSON!
    optimization_priorities: [String!]!
    investment_priority_rank: Int!
  }

  type AlertThresholds {
    conversion_rate_min: Float!
    bounce_rate_max: Float!
  }

  type ImplementationRoadmap {
    phase: String!
    data: JSON!
  }

  type ResearchSummary {
    totalNiches: Int!
    averagePriorityScore: Float!
    totalConservativeROI: Float!
    totalRealisticROI: Float!
    totalOptimisticROI: Float!
    highAutomationReadyCount: Int!
    lowRiskHighRewardCount: Int!
  }

  input NicheFilters {
    minPriorityScore: Float
    maxRisk: Float
    minROI: Float
    minAutomationScore: Float
  }
`;