# Performance Analytics API Controller for Dynamic Customer Journey Engine
# Module: 2B - Dynamic Customer Journey Engine
# Created: 2024-07-04

import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .performance_analytics import PerformanceAnalyticsEngine
from ...database import get_db
from ...utils.auth import get_current_user
from ...utils.rate_limiting import rate_limit
from ...utils.monitoring import track_api_call, track_performance

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/journey/analytics", tags=["analytics"])

# =============================================================================
# ANALYTICS MODELS
# =============================================================================

class AnalyticsRequest(BaseModel):
    """Base analytics request model"""
    time_range: str = Field(default="24h", description="Time range: 1h, 24h, 7d, 30d, 90d")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Additional filters")

class FunnelAnalyticsRequest(AnalyticsRequest):
    """Request model for funnel analytics"""
    persona_filter: Optional[str] = Field(None, description="Filter by persona type")
    device_filter: Optional[str] = Field(None, description="Filter by device type")
    journey_path_filter: Optional[str] = Field(None, description="Filter by journey path")

class PerformanceReportRequest(BaseModel):
    """Request model for performance reports"""
    report_type: str = Field(default="comprehensive", description="Report type: comprehensive, executive, technical")
    time_range: str = Field(default="7d", description="Time range for report")
    include_sections: List[str] = Field(default=["all"], description="Sections to include")
    format: str = Field(default="json", description="Report format: json, pdf, excel")

class RealTimeMetricsResponse(BaseModel):
    """Response model for real-time metrics"""
    timestamp: str = Field(..., description="Metrics timestamp")
    time_window_minutes: int = Field(..., description="Time window in minutes")
    session_metrics: Dict[str, Any] = Field(..., description="Session metrics")
    conversion_metrics: Dict[str, Any] = Field(..., description="Conversion metrics")
    optimization_metrics: Dict[str, Any] = Field(..., description="Optimization metrics")
    personalization_metrics: Dict[str, Any] = Field(..., description="Personalization metrics")
    system_health: Dict[str, Any] = Field(..., description="System health scores")
    alerts: List[Dict[str, Any]] = Field(default_factory=list, description="Real-time alerts")

class FunnelAnalyticsResponse(BaseModel):
    """Response model for funnel analytics"""
    time_range: str = Field(..., description="Time range analyzed")
    persona_filter: Optional[str] = Field(None, description="Applied persona filter")
    funnel_data: Dict[str, Any] = Field(..., description="Funnel conversion data")
    stage_performance: Dict[str, Any] = Field(..., description="Stage performance metrics")
    journey_path_analytics: Dict[str, Any] = Field(..., description="Journey path analytics")
    dropoff_analysis: Dict[str, Any] = Field(..., description="Drop-off analysis")
    persona_performance: Dict[str, Any] = Field(..., description="Persona performance comparison")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Optimization recommendations")

class OptimizationAnalyticsResponse(BaseModel):
    """Response model for optimization analytics"""
    time_range: str = Field(..., description="Time range analyzed")
    optimization_performance: Dict[str, Any] = Field(..., description="Optimization performance by type")
    ab_test_results: Dict[str, Any] = Field(..., description="A/B test results")
    personalization_effectiveness: Dict[str, Any] = Field(..., description="Personalization effectiveness")
    scarcity_effectiveness: Dict[str, Any] = Field(..., description="Scarcity trigger effectiveness")
    roi_analysis: Dict[str, Any] = Field(..., description="ROI analysis")
    trend_analysis: Dict[str, Any] = Field(..., description="Trend analysis")
    optimization_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Optimization recommendations")

class CrossDeviceAnalyticsResponse(BaseModel):
    """Response model for cross-device analytics"""
    time_range: str = Field(..., description="Time range analyzed")
    cross_device_stats: Dict[str, Any] = Field(..., description="Cross-device statistics")
    device_switching: Dict[str, Any] = Field(..., description="Device switching patterns")
    cross_device_conversions: Dict[str, Any] = Field(..., description="Cross-device conversion analysis")
    continuity_effectiveness: Dict[str, Any] = Field(..., description="Journey continuity effectiveness")
    cross_device_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Cross-device recommendations")

class PerformanceReportResponse(BaseModel):
    """Response model for performance reports"""
    report_type: str = Field(..., description="Type of report generated")
    time_range: str = Field(..., description="Time range covered")
    generated_at: str = Field(..., description="Report generation timestamp")
    executive_summary: Dict[str, Any] = Field(..., description="Executive summary")
    real_time_metrics: Dict[str, Any] = Field(default_factory=dict, description="Real-time metrics")
    funnel_analytics: Dict[str, Any] = Field(default_factory=dict, description="Funnel analytics")
    optimization_analytics: Dict[str, Any] = Field(default_factory=dict, description="Optimization analytics")
    cross_device_analytics: Dict[str, Any] = Field(default_factory=dict, description="Cross-device analytics")
    strategic_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Strategic recommendations")
    next_review_date: str = Field(..., description="Next recommended review date")

# =============================================================================
# ANALYTICS ENDPOINTS
# =============================================================================

@router.get("/real-time", response_model=RealTimeMetricsResponse)
@track_api_call("analytics_real_time")
@rate_limit(requests_per_minute=200)
async def get_real_time_metrics(
    time_window: int = Query(5, description="Time window in minutes", ge=1, le=60),
    db: AsyncSession = Depends(get_db)
) -> RealTimeMetricsResponse:
    """
    Get real-time performance metrics
    
    Returns live performance metrics for sessions, conversions,
    optimizations, and system health status.
    """
    try:
        logger.debug(f"Getting real-time metrics for {time_window} minute window")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Get real-time metrics
        with track_performance("real_time_metrics_generation"):
            metrics = await analytics_engine.get_real_time_performance_metrics(time_window)
        
        # Handle errors from analytics engine
        if "error" in metrics:
            raise HTTPException(status_code=500, detail=metrics["error"])
        
        return RealTimeMetricsResponse(**metrics)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting real-time metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Real-time metrics failed: {str(e)}")

@router.post("/funnel", response_model=FunnelAnalyticsResponse)
@track_api_call("analytics_funnel")
@rate_limit(requests_per_minute=100)
async def get_funnel_analytics(
    funnel_request: FunnelAnalyticsRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> FunnelAnalyticsResponse:
    """
    Get journey funnel analytics
    
    Returns comprehensive funnel conversion rates, stage performance,
    journey path analysis, and drop-off insights.
    """
    try:
        logger.debug(f"Getting funnel analytics for {funnel_request.time_range}")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Get funnel analytics
        with track_performance("funnel_analytics_generation"):
            analytics = await analytics_engine.get_journey_funnel_analytics(
                funnel_request.time_range, 
                funnel_request.persona_filter
            )
        
        # Handle errors from analytics engine
        if "error" in analytics:
            raise HTTPException(status_code=500, detail=analytics["error"])
        
        # Background task for analytics tracking
        background_tasks.add_task(
            track_funnel_analytics_request,
            funnel_request.time_range,
            funnel_request.persona_filter,
            analytics.get("funnel_data", {}).get("overall", {}).get("overall_conversion_rate", 0)
        )
        
        return FunnelAnalyticsResponse(**analytics)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting funnel analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Funnel analytics failed: {str(e)}")

@router.get("/optimization", response_model=OptimizationAnalyticsResponse)
@track_api_call("analytics_optimization")
@rate_limit(requests_per_minute=50)
async def get_optimization_analytics(
    time_range: str = Query("7d", description="Time range: 1h, 24h, 7d, 30d, 90d"),
    optimization_type: Optional[str] = Query(None, description="Filter by optimization type"),
    db: AsyncSession = Depends(get_db)
) -> OptimizationAnalyticsResponse:
    """
    Get optimization effectiveness analytics
    
    Returns comprehensive analysis of optimization performance,
    A/B test results, ROI analysis, and trend insights.
    """
    try:
        logger.debug(f"Getting optimization analytics for {time_range}")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Get optimization analytics
        with track_performance("optimization_analytics_generation"):
            analytics = await analytics_engine.get_optimization_effectiveness_analytics(time_range)
        
        # Handle errors from analytics engine
        if "error" in analytics:
            raise HTTPException(status_code=500, detail=analytics["error"])
        
        return OptimizationAnalyticsResponse(**analytics)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting optimization analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization analytics failed: {str(e)}")

@router.get("/cross-device", response_model=CrossDeviceAnalyticsResponse)
@track_api_call("analytics_cross_device")
@rate_limit(requests_per_minute=50)
async def get_cross_device_analytics(
    time_range: str = Query("7d", description="Time range: 1h, 24h, 7d, 30d, 90d"),
    device_type: Optional[str] = Query(None, description="Filter by device type"),
    db: AsyncSession = Depends(get_db)
) -> CrossDeviceAnalyticsResponse:
    """
    Get cross-device journey analytics
    
    Returns analysis of cross-device sessions, device switching patterns,
    and journey continuity effectiveness.
    """
    try:
        logger.debug(f"Getting cross-device analytics for {time_range}")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Get cross-device analytics
        with track_performance("cross_device_analytics_generation"):
            analytics = await analytics_engine.get_cross_device_analytics(time_range)
        
        # Handle errors from analytics engine
        if "error" in analytics:
            raise HTTPException(status_code=500, detail=analytics["error"])
        
        return CrossDeviceAnalyticsResponse(**analytics)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting cross-device analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cross-device analytics failed: {str(e)}")

@router.post("/report", response_model=PerformanceReportResponse)
@track_api_call("analytics_performance_report")
@rate_limit(requests_per_minute=20)
async def generate_performance_report(
    report_request: PerformanceReportRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> PerformanceReportResponse:
    """
    Generate comprehensive performance report
    
    Creates detailed performance report with executive summary,
    analytics across all systems, and strategic recommendations.
    """
    try:
        logger.info(f"Generating {report_request.report_type} performance report for {report_request.time_range}")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Generate performance report
        with track_performance("performance_report_generation"):
            report = await analytics_engine.generate_performance_report(
                report_request.report_type,
                report_request.time_range
            )
        
        # Handle errors from analytics engine
        if "error" in report:
            raise HTTPException(status_code=500, detail=report["error"])
        
        # Background tasks for report tracking and processing
        background_tasks.add_task(
            track_performance_report_generation,
            report_request.report_type,
            report_request.time_range,
            len(report.get("strategic_recommendations", []))
        )
        
        background_tasks.add_task(
            process_performance_report,
            report,
            report_request.format
        )
        
        logger.info(f"Performance report generated successfully: {report_request.report_type}")
        return PerformanceReportResponse(**report)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating performance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Performance report generation failed: {str(e)}")

@router.get("/dashboard")
@track_api_call("analytics_dashboard")
@rate_limit(requests_per_minute=100)
async def get_analytics_dashboard(
    time_range: str = Query("24h", description="Time range for dashboard metrics"),
    refresh_interval: int = Query(60, description="Dashboard refresh interval in seconds"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get analytics dashboard data
    
    Returns optimized data for analytics dashboard with key metrics,
    charts, and real-time indicators.
    """
    try:
        logger.debug(f"Getting analytics dashboard data for {time_range}")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Get dashboard data
        with track_performance("analytics_dashboard_generation"):
            # Get key metrics concurrently
            tasks = [
                analytics_engine.get_real_time_performance_metrics(5),
                analytics_engine.get_journey_funnel_analytics(time_range),
                analytics_engine.get_optimization_effectiveness_analytics(time_range)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            real_time_metrics = results[0] if not isinstance(results[0], Exception) else {}
            funnel_analytics = results[1] if not isinstance(results[1], Exception) else {}
            optimization_analytics = results[2] if not isinstance(results[2], Exception) else {}
        
        # Build dashboard response
        dashboard_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "time_range": time_range,
            "refresh_interval": refresh_interval,
            "key_metrics": {
                "active_sessions": real_time_metrics.get("session_metrics", {}).get("active_sessions", 0),
                "conversion_rate": real_time_metrics.get("conversion_metrics", {}).get("conversion_rate", 0),
                "total_revenue": real_time_metrics.get("conversion_metrics", {}).get("total_revenue", 0),
                "system_health": real_time_metrics.get("system_health", {}).get("overall_system_health", 0)
            },
            "charts": {
                "funnel_conversion": funnel_analytics.get("funnel_data", {}),
                "optimization_performance": optimization_analytics.get("optimization_performance", {}),
                "real_time_trends": {
                    "sessions_per_minute": real_time_metrics.get("session_metrics", {}).get("sessions_per_minute", 0),
                    "conversions_per_minute": real_time_metrics.get("conversion_metrics", {}).get("conversions_per_minute", 0)
                }
            },
            "alerts": real_time_metrics.get("alerts", []),
            "recommendations": funnel_analytics.get("recommendations", [])[:3]  # Top 3 recommendations
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting analytics dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics dashboard failed: {str(e)}")

@router.get("/export/{report_type}")
@track_api_call("analytics_export")
@rate_limit(requests_per_minute=10)
async def export_analytics_data(
    report_type: str = Path(..., description="Report type to export"),
    time_range: str = Query("7d", description="Time range for export"),
    format: str = Query("csv", description="Export format: csv, json, xlsx"),
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Export analytics data
    
    Exports analytics data in various formats for external analysis
    and reporting systems.
    """
    try:
        logger.info(f"Exporting {report_type} analytics data in {format} format")
        
        # Validate export parameters
        valid_report_types = ["funnel", "optimization", "cross_device", "performance"]
        if report_type not in valid_report_types:
            raise HTTPException(status_code=400, detail=f"Invalid report type. Must be one of: {valid_report_types}")
        
        valid_formats = ["csv", "json", "xlsx"]
        if format not in valid_formats:
            raise HTTPException(status_code=400, detail=f"Invalid format. Must be one of: {valid_formats}")
        
        # Initialize analytics engine
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        # Get data based on report type
        if report_type == "funnel":
            data = await analytics_engine.get_journey_funnel_analytics(time_range)
        elif report_type == "optimization":
            data = await analytics_engine.get_optimization_effectiveness_analytics(time_range)
        elif report_type == "cross_device":
            data = await analytics_engine.get_cross_device_analytics(time_range)
        elif report_type == "performance":
            data = await analytics_engine.generate_performance_report("comprehensive", time_range)
        
        # Generate export
        export_id = str(uuid4())
        
        # Background task for export processing
        background_tasks.add_task(
            process_analytics_export,
            export_id,
            report_type,
            data,
            format,
            time_range
        )
        
        return {
            "export_id": export_id,
            "report_type": report_type,
            "format": format,
            "time_range": time_range,
            "status": "processing",
            "estimated_completion": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting analytics data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics export failed: {str(e)}")

@router.get("/health")
async def analytics_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Health check endpoint for analytics service"""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        
        # Test analytics engine initialization
        analytics_engine = PerformanceAnalyticsEngine(db)
        
        return {
            "status": "healthy",
            "service": "performance_analytics_engine",
            "module": "2b_dynamic_customer_journey",
            "capabilities": "real_time,funnel,optimization,cross_device,reporting",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Analytics health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Analytics service unhealthy")

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

import asyncio
from uuid import uuid4

async def track_funnel_analytics_request(time_range: str, persona_filter: Optional[str], conversion_rate: float):
    """Background task to track funnel analytics requests"""
    logger.info(f"Tracking funnel analytics: {time_range}, persona: {persona_filter}, conv_rate: {conversion_rate}")

async def track_performance_report_generation(report_type: str, time_range: str, recommendations_count: int):
    """Background task to track performance report generation"""
    logger.info(f"Tracking performance report: {report_type}, {time_range}, {recommendations_count} recommendations")

async def process_performance_report(report: Dict[str, Any], format: str):
    """Background task to process performance report"""
    logger.debug(f"Processing performance report in {format} format")

async def process_analytics_export(export_id: str, report_type: str, data: Dict[str, Any], format: str, time_range: str):
    """Background task to process analytics export"""
    logger.info(f"Processing analytics export: {export_id}, {report_type}, {format}")
    # Implementation would handle actual file generation and storage