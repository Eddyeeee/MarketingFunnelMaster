"""
Health Monitoring System for Agentic RAG Infrastructure
Monitors PostgreSQL, Neo4j, and application performance
Version: 1.0.0
Created: 2025-07-03
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import psutil
import os

from database.database_config import db_manager
from database.neo4j_manager import graph_manager
from database.sync_manager import sync_manager

logger = logging.getLogger(__name__)

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class ComponentHealth:
    """Health status for a system component"""
    name: str
    status: HealthStatus
    response_time_ms: float
    last_check: datetime
    details: Dict[str, Any]
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['last_check'] = self.last_check.isoformat()
        data['status'] = self.status.value
        return data

@dataclass
class SystemMetrics:
    """System-wide performance metrics"""
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_io_mb: float
    active_connections: int
    queries_per_second: float
    error_rate: float
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

class HealthMonitor:
    """Comprehensive health monitoring for the Agentic RAG system"""
    
    def __init__(self):
        self.check_interval_seconds = 30
        self.warning_thresholds = {
            'response_time_ms': 1000,
            'cpu_usage_percent': 80,
            'memory_usage_percent': 85,
            'disk_usage_percent': 90,
            'error_rate': 0.05
        }
        self.critical_thresholds = {
            'response_time_ms': 5000,
            'cpu_usage_percent': 95,
            'memory_usage_percent': 95,
            'disk_usage_percent': 95,
            'error_rate': 0.15
        }
        self.health_history: List[Dict[str, Any]] = []
        self.max_history_entries = 1000
        self.is_monitoring = False
        
    async def check_postgresql_health(self) -> ComponentHealth:
        """Check PostgreSQL database health"""
        start_time = time.time()
        
        try:
            health_data = await db_manager.health_check()
            response_time = (time.time() - start_time) * 1000
            
            if health_data['status'] == 'healthy':
                status = self._determine_status(response_time, 'response_time_ms')
                
                # Additional checks
                pool_usage = health_data['pool_info']['size'] / health_data['pool_info']['max_size']
                if pool_usage > 0.9:
                    status = HealthStatus.WARNING
                
                return ComponentHealth(
                    name="PostgreSQL",
                    status=status,
                    response_time_ms=response_time,
                    last_check=datetime.now(),
                    details={
                        'pool_info': health_data['pool_info'],
                        'table_sizes': health_data['table_sizes'][:5],  # Top 5 tables
                        'top_indexes': health_data['top_indexes'][:5],  # Top 5 indexes
                        'pool_usage_percent': pool_usage * 100
                    }
                )
            else:
                return ComponentHealth(
                    name="PostgreSQL",
                    status=HealthStatus.CRITICAL,
                    response_time_ms=response_time,
                    last_check=datetime.now(),
                    details=health_data,
                    error_message=health_data.get('error', 'Unknown error')
                )
                
        except Exception as e:
            return ComponentHealth(
                name="PostgreSQL",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                last_check=datetime.now(),
                details={},
                error_message=str(e)
            )
    
    async def check_neo4j_health(self) -> ComponentHealth:
        """Check Neo4j database health"""
        start_time = time.time()
        
        try:
            health_data = await graph_manager.get_system_health()
            response_time = (time.time() - start_time) * 1000
            
            # Determine status based on response time and entity counts
            status = self._determine_status(response_time, 'response_time_ms')
            
            # Check for data consistency
            if health_data['total_entities'] == 0 and health_data['total_relationships'] == 0:
                status = HealthStatus.WARNING
            
            return ComponentHealth(
                name="Neo4j",
                status=status,
                response_time_ms=response_time,
                last_check=datetime.now(),
                details={
                    'total_entities': health_data['total_entities'],
                    'total_relationships': health_data['total_relationships'],
                    'total_snapshots': health_data['total_snapshots'],
                    'avg_performance': health_data['avg_performance'],
                    'avg_confidence': health_data['avg_confidence'],
                    'high_performers': health_data['high_performers']
                }
            )
            
        except Exception as e:
            return ComponentHealth(
                name="Neo4j",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                last_check=datetime.now(),
                details={},
                error_message=str(e)
            )
    
    async def check_sync_health(self) -> ComponentHealth:
        """Check database synchronization health"""
        start_time = time.time()
        
        try:
            sync_status = await sync_manager.get_sync_status()
            response_time = (time.time() - start_time) * 1000
            
            # Determine status based on sync metrics
            status = HealthStatus.HEALTHY
            
            if sync_status['errors_encountered'] > 0:
                status = HealthStatus.WARNING
            
            if sync_status['conflicts_detected'] > sync_status['conflicts_resolved']:
                status = HealthStatus.WARNING
            
            # Check if sync is severely behind
            if sync_status['last_sync']:
                last_sync = datetime.fromisoformat(sync_status['last_sync'])
                time_since_sync = datetime.now() - last_sync
                if time_since_sync > timedelta(hours=1):
                    status = HealthStatus.CRITICAL
            
            return ComponentHealth(
                name="Database Sync",
                status=status,
                response_time_ms=response_time,
                last_check=datetime.now(),
                details=sync_status
            )
            
        except Exception as e:
            return ComponentHealth(
                name="Database Sync",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                last_check=datetime.now(),
                details={},
                error_message=str(e)
            )
    
    def check_system_resources(self) -> ComponentHealth:
        """Check system resource utilization"""
        start_time = time.time()
        
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io_mb = (network.bytes_sent + network.bytes_recv) / (1024 * 1024)
            
            # Determine overall status
            status = HealthStatus.HEALTHY
            
            if (cpu_usage > self.warning_thresholds['cpu_usage_percent'] or
                memory_usage > self.warning_thresholds['memory_usage_percent'] or
                disk_usage > self.warning_thresholds['disk_usage_percent']):
                status = HealthStatus.WARNING
            
            if (cpu_usage > self.critical_thresholds['cpu_usage_percent'] or
                memory_usage > self.critical_thresholds['memory_usage_percent'] or
                disk_usage > self.critical_thresholds['disk_usage_percent']):
                status = HealthStatus.CRITICAL
            
            response_time = (time.time() - start_time) * 1000
            
            return ComponentHealth(
                name="System Resources",
                status=status,
                response_time_ms=response_time,
                last_check=datetime.now(),
                details={
                    'cpu_usage_percent': cpu_usage,
                    'memory_usage_percent': memory_usage,
                    'memory_available_gb': memory.available / (1024**3),
                    'disk_usage_percent': disk_usage,
                    'disk_free_gb': disk.free / (1024**3),
                    'network_io_mb': network_io_mb,
                    'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
                }
            )
            
        except Exception as e:
            return ComponentHealth(
                name="System Resources",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                last_check=datetime.now(),
                details={},
                error_message=str(e)
            )
    
    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of all components"""
        start_time = time.time()
        
        # Run all health checks concurrently
        postgresql_task = asyncio.create_task(self.check_postgresql_health())
        neo4j_task = asyncio.create_task(self.check_neo4j_health())
        sync_task = asyncio.create_task(self.check_sync_health())
        
        # System resources check (synchronous)
        system_health = self.check_system_resources()
        
        # Wait for async checks to complete
        postgresql_health = await postgresql_task
        neo4j_health = await neo4j_task
        sync_health = await sync_task
        
        # Collect all component healths
        components = {
            'postgresql': postgresql_health.to_dict(),
            'neo4j': neo4j_health.to_dict(),
            'database_sync': sync_health.to_dict(),
            'system_resources': system_health.to_dict()
        }
        
        # Determine overall system status
        component_statuses = [
            postgresql_health.status,
            neo4j_health.status,
            sync_health.status,
            system_health.status
        ]
        
        overall_status = self._determine_overall_status(component_statuses)
        
        # Calculate total response time
        total_response_time = (time.time() - start_time) * 1000
        
        health_report = {
            'overall_status': overall_status.value,
            'total_response_time_ms': total_response_time,
            'timestamp': datetime.now().isoformat(),
            'components': components,
            'summary': {
                'healthy_components': sum(1 for c in component_statuses if c == HealthStatus.HEALTHY),
                'warning_components': sum(1 for c in component_statuses if c == HealthStatus.WARNING),
                'critical_components': sum(1 for c in component_statuses if c == HealthStatus.CRITICAL),
                'total_components': len(component_statuses)
            }
        }
        
        # Store in history
        self._store_health_history(health_report)
        
        return health_report
    
    def _determine_status(self, value: float, metric_type: str) -> HealthStatus:
        """Determine health status based on metric value and thresholds"""
        if value > self.critical_thresholds.get(metric_type, float('inf')):
            return HealthStatus.CRITICAL
        elif value > self.warning_thresholds.get(metric_type, float('inf')):
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _determine_overall_status(self, statuses: List[HealthStatus]) -> HealthStatus:
        """Determine overall status from component statuses"""
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.WARNING in statuses:
            return HealthStatus.WARNING
        elif HealthStatus.UNKNOWN in statuses:
            return HealthStatus.UNKNOWN
        else:
            return HealthStatus.HEALTHY
    
    def _store_health_history(self, health_report: Dict[str, Any]) -> None:
        """Store health report in history"""
        self.health_history.append(health_report)
        
        # Trim history if it exceeds max entries
        if len(self.health_history) > self.max_history_entries:
            self.health_history = self.health_history[-self.max_history_entries:]
    
    async def get_health_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get health trends over specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter history by time period
        recent_history = [
            report for report in self.health_history
            if datetime.fromisoformat(report['timestamp']) > cutoff_time
        ]
        
        if not recent_history:
            return {'error': 'No health data available for the specified period'}
        
        # Calculate trends
        trends = {
            'total_checks': len(recent_history),
            'avg_response_time_ms': sum(r['total_response_time_ms'] for r in recent_history) / len(recent_history),
            'status_distribution': {
                'healthy': sum(1 for r in recent_history if r['overall_status'] == 'healthy'),
                'warning': sum(1 for r in recent_history if r['overall_status'] == 'warning'),
                'critical': sum(1 for r in recent_history if r['overall_status'] == 'critical')
            },
            'component_availability': {},
            'performance_trends': {}
        }
        
        # Calculate component availability
        for component in ['postgresql', 'neo4j', 'database_sync', 'system_resources']:
            component_statuses = [r['components'][component]['status'] for r in recent_history]
            trends['component_availability'][component] = {
                'uptime_percentage': (sum(1 for s in component_statuses if s in ['healthy', 'warning']) / len(component_statuses)) * 100,
                'avg_response_time_ms': sum(r['components'][component]['response_time_ms'] for r in recent_history) / len(recent_history)
            }
        
        return trends
    
    async def start_monitoring(self) -> None:
        """Start continuous health monitoring"""
        if self.is_monitoring:
            logger.warning("Health monitoring already running")
            return
        
        self.is_monitoring = True
        logger.info(f"Starting health monitoring with {self.check_interval_seconds}s intervals")
        
        while self.is_monitoring:
            try:
                health_report = await self.comprehensive_health_check()
                
                # Log critical issues
                if health_report['overall_status'] == 'critical':
                    logger.error(f"CRITICAL: System health issues detected: {health_report['summary']}")
                elif health_report['overall_status'] == 'warning':
                    logger.warning(f"WARNING: System health degraded: {health_report['summary']}")
                
                # Wait for next check
                await asyncio.sleep(self.check_interval_seconds)
                
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(self.check_interval_seconds)
    
    def stop_monitoring(self) -> None:
        """Stop health monitoring"""
        self.is_monitoring = False
        logger.info("Health monitoring stopped")
    
    async def get_current_health(self) -> Dict[str, Any]:
        """Get current system health status"""
        return await self.comprehensive_health_check()
    
    def get_health_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent health history"""
        return self.health_history[-limit:]
    
    async def run_performance_diagnostics(self) -> Dict[str, Any]:
        """Run detailed performance diagnostics"""
        diagnostics = {
            'timestamp': datetime.now().isoformat(),
            'database_performance': {},
            'system_performance': {},
            'recommendations': []
        }
        
        # PostgreSQL diagnostics
        try:
            pg_metrics = await db_manager.get_performance_metrics()
            diagnostics['database_performance']['postgresql'] = pg_metrics
            
            # Check for performance issues
            if pg_metrics.get('system_metrics', {}).get('avg_response_time', 0) > 1000:
                diagnostics['recommendations'].append(
                    "PostgreSQL response times are high. Consider query optimization or connection pool tuning."
                )
                
        except Exception as e:
            diagnostics['database_performance']['postgresql'] = {'error': str(e)}
        
        # Neo4j diagnostics
        try:
            neo4j_patterns = await graph_manager.analyze_relationship_patterns()
            diagnostics['database_performance']['neo4j'] = neo4j_patterns
            
            # Check for graph issues
            if neo4j_patterns['total_relationships'] == 0:
                diagnostics['recommendations'].append(
                    "Neo4j has no relationships. Check entity extraction and relationship creation processes."
                )
                
        except Exception as e:
            diagnostics['database_performance']['neo4j'] = {'error': str(e)}
        
        # System diagnostics
        system_info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'disk_total_gb': psutil.disk_usage('/').total / (1024**3),
            'python_version': f"{psutil.PROCFS_PATH}",  # Simplified
            'process_count': len(psutil.pids())
        }
        diagnostics['system_performance'] = system_info
        
        return diagnostics

# Global health monitor instance
health_monitor = HealthMonitor()

# Helper functions
async def get_system_health() -> Dict[str, Any]:
    """Get current system health"""
    return await health_monitor.get_current_health()

async def start_health_monitoring():
    """Start background health monitoring"""
    asyncio.create_task(health_monitor.start_monitoring())

def stop_health_monitoring():
    """Stop health monitoring"""
    health_monitor.stop_monitoring()

async def get_health_trends(hours: int = 24) -> Dict[str, Any]:
    """Get health trends"""
    return await health_monitor.get_health_trends(hours)

if __name__ == "__main__":
    # Test the health monitor
    async def test_health_monitor():
        try:
            # Initialize database managers
            await db_manager.initialize()
            await graph_manager.initialize()
            await sync_manager.initialize()
            
            # Run health check
            health = await get_system_health()
            print(f"System Health: {health['overall_status']}")
            print(f"Response Time: {health['total_response_time_ms']:.2f}ms")
            
            # Run diagnostics
            diagnostics = await health_monitor.run_performance_diagnostics()
            print(f"Diagnostics completed with {len(diagnostics['recommendations'])} recommendations")
            
        except Exception as e:
            print(f"Health monitor test failed: {e}")
    
    asyncio.run(test_health_monitor())