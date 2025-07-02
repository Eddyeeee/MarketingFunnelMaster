import { gql } from '@apollo/client';

export const GET_PROCESSES = gql`
  query GetProcesses {
    processes {
      id
      name
      status
      type
      startTime
      lastUpdate
      progress
      metrics {
        cpu
        memory
        requestsPerMinute
        errorRate
        avgResponseTime
      }
      logs {
        id
        timestamp
        level
        message
        metadata
      }
    }
  }
`;

export const GET_AI_METRICS = gql`
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

export const SEARCH_RESEARCH = gql`
  query SearchResearch($query: String!, $filters: JSON) {
    searchResearch(query: $query, filters: $filters) {
      id
      query
      results {
        id
        title
        content
        url
        relevanceScore
        entities {
          name
          type
          confidence
        }
        sentiment {
          score
          label
        }
        children {
          id
          title
          content
          relevanceScore
          entities {
            name
            type
            confidence
          }
          sentiment {
            score
            label
          }
        }
      }
      timestamp
      source
      metadata {
        duration
        sources
        filters
      }
    }
  }
`;

// New Research Intelligence Queries
export const GET_RESEARCH_DATASET = gql`
  query GetResearchDataset {
    researchDataset {
      niches {
        niche_id
        niche_name
        description
        priority_score
        implementation_difficulty
        roi_projection {
          conservative
          realistic
          optimistic
        }
        quick_win_opportunities
        automation_ready_score
        market_saturation_index
        competition_intensity_score
        virality_potential_score
        scalability_score
        risk_assessment_score
      }
      personas {
        persona_id
        persona_name
        niche_id
        age_range
        psychographics {
          personality_types
          values
          interests
        }
        behavioral_triggers
        emotional_states
        device_usage {
          mobile
          desktop
          tablet
        }
      }
      summary {
        totalNiches
        averagePriorityScore
        totalConservativeROI
        totalRealisticROI
        totalOptimisticROI
        highAutomationReadyCount
        lowRiskHighRewardCount
      }
    }
  }
`;

export const GET_NICHES = gql`
  query GetNiches($filters: NicheFilters) {
    niches(filters: $filters) {
      niche_id
      niche_name
      description
      priority_score
      implementation_difficulty
      roi_projection {
        conservative
        realistic
        optimistic
      }
      quick_win_opportunities
      automation_ready_score
      market_saturation_index
      competition_intensity_score
      virality_potential_score
      scalability_score
      risk_assessment_score
    }
  }
`;

export const GET_NICHE = gql`
  query GetNiche($nicheId: String!) {
    niche(nicheId: $nicheId) {
      niche_id
      niche_name
      description
      priority_score
      implementation_difficulty
      roi_projection {
        conservative
        realistic
        optimistic
      }
      quick_win_opportunities
      automation_ready_score
      market_saturation_index
      competition_intensity_score
      virality_potential_score
      scalability_score
      risk_assessment_score
    }
  }
`;

export const GET_PERSONA = gql`
  query GetPersona($nicheId: String!) {
    persona(nicheId: $nicheId) {
      persona_id
      persona_name
      niche_id
      age_range
      psychographics {
        personality_types
        values
        interests
      }
      behavioral_triggers
      emotional_states
      device_usage {
        mobile
        desktop
        tablet
      }
    }
  }
`;

export const GET_NICHE_METRICS = gql`
  query GetNicheMetrics($nicheId: String!) {
    nicheMetrics(nicheId: $nicheId) {
      health_score
      alert_thresholds {
        conversion_rate_min
        bounce_rate_max
      }
      performance_triggers
      optimization_priorities
      investment_priority_rank
    }
  }
`;

export const GET_IMPLEMENTATION_ROADMAPS = gql`
  query GetImplementationRoadmaps {
    implementationRoadmaps {
      phase
      data
    }
  }
`;

// Subscriptions
export const PROCESS_UPDATED = gql`
  subscription ProcessUpdated {
    processUpdated {
      id
      name
      status
      type
      startTime
      lastUpdate
      progress
      metrics {
        cpu
        memory
        requestsPerMinute
        errorRate
        avgResponseTime
      }
      logs {
        id
        timestamp
        level
        message
        metadata
      }
    }
  }
`;

export const METRICS_UPDATED = gql`
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

export const RESEARCH_COMPLETED = gql`
  subscription ResearchCompleted {
    researchCompleted {
      id
      query
      results {
        id
        title
        content
        url
        relevanceScore
        entities {
          name
          type
          confidence
        }
        sentiment {
          score
          label
        }
        children {
          id
          title
          content
          relevanceScore
          entities {
            name
            type
            confidence
          }
          sentiment {
            score
            label
          }
        }
      }
      timestamp
      source
      metadata {
        duration
        sources
        filters
      }
    }
  }
`;

// Mutations
export const START_PROCESS = gql`
  mutation StartProcess($input: StartProcessInput!) {
    startProcess(input: $input) {
      id
      name
      status
      type
      startTime
      lastUpdate
      progress
      metrics {
        cpu
        memory
        requestsPerMinute
        errorRate
        avgResponseTime
      }
      logs {
        id
        timestamp
        level
        message
        metadata
      }
    }
  }
`;

export const STOP_PROCESS = gql`
  mutation StopProcess($id: ID!) {
    stopProcess(id: $id) {
      id
      name
      status
      lastUpdate
    }
  }
`;

export const CREATE_RESEARCH_QUERY = gql`
  mutation CreateResearchQuery($input: ResearchQueryInput!) {
    createResearchQuery(input: $input) {
      id
      query
      results {
        id
        title
        content
        url
        relevanceScore
        entities {
          name
          type
          confidence
        }
        sentiment {
          score
          label
        }
      }
      timestamp
      source
      metadata {
        duration
        sources
        filters
      }
    }
  }
`;