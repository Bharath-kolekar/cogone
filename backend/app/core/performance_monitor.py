"""
Advanced Performance Monitoring System for Cognomega AI
Real-time monitoring and optimization of system performance
"""

import asyncio
import time
import psutil
import threading
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import structlog

from app.core.cpu_optimizer import cpu_optimizer
from app.core.advanced_caching import advanced_cache

logger = structlog.get_logger()


class MetricType(str, Enum):
    """Types of performance metrics"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    CACHE_HIT_RATE = "cache_hit_rate"
    DATABASE_QUERIES = "database_queries"
    AI_PROCESSING_TIME = "ai_processing_time"


class AlertLevel(str, Enum):
    """Alert levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class PerformanceMetric:
    """Performance metric data"""
    metric_type: MetricType
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    component: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceAlert:
    """Performance alert"""
    alert_id: str
    level: AlertLevel
    metric_type: MetricType
    current_value: float
    threshold: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    component: str = ""


@dataclass
class PerformanceThreshold:
    """Performance threshold configuration"""
    metric_type: MetricType
    warning_threshold: float
    critical_threshold: float
    emergency_threshold: float
    component: str = ""


class PerformanceMonitor:
    """Advanced performance monitoring system"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetric] = []
        self.active_alerts: List[PerformanceAlert] = []
        self.thresholds: Dict[str, PerformanceThreshold] = {}
        
        # Monitoring configuration
        self.monitoring_interval = 1.0  # seconds
        self.history_retention = 3600  # seconds (1 hour)
        self.alert_cooldown = 300  # seconds (5 minutes)
        
        # Performance tracking
        self.response_times: List[float] = []
        self.error_counts: Dict[str, int] = {}
        self.throughput_counter = 0
        self.last_throughput_reset = time.time()
        
        # Callbacks for alerts
        self.alert_callbacks: List[Callable] = []
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
        
        # Start monitoring
        self._monitoring_task = None
        self._start_monitoring()
    
    def _initialize_default_thresholds(self):
        """Initialize default performance thresholds"""
        default_thresholds = {
            "response_time": PerformanceThreshold(
                metric_type=MetricType.RESPONSE_TIME,
                warning_threshold=1000.0,  # 1 second
                critical_threshold=3000.0,  # 3 seconds
                emergency_threshold=10000.0  # 10 seconds
            ),
            "error_rate": PerformanceThreshold(
                metric_type=MetricType.ERROR_RATE,
                warning_threshold=5.0,  # 5%
                critical_threshold=10.0,  # 10%
                emergency_threshold=25.0  # 25%
            ),
            "cpu_usage": PerformanceThreshold(
                metric_type=MetricType.CPU_USAGE,
                warning_threshold=70.0,  # 70%
                critical_threshold=85.0,  # 85%
                emergency_threshold=95.0  # 95%
            ),
            "memory_usage": PerformanceThreshold(
                metric_type=MetricType.MEMORY_USAGE,
                warning_threshold=80.0,  # 80%
                critical_threshold=90.0,  # 90%
                emergency_threshold=95.0  # 95%
            ),
            "cache_hit_rate": PerformanceThreshold(
                metric_type=MetricType.CACHE_HIT_RATE,
                warning_threshold=60.0,  # 60%
                critical_threshold=40.0,  # 40%
                emergency_threshold=20.0  # 20%
            )
        }
        
        self.thresholds.update(default_thresholds)
    
    def _start_monitoring(self):
        """Start performance monitoring"""
        self._monitoring_task = asyncio.create_task(self._monitor_performance())
    
    async def _monitor_performance(self):
        """Main performance monitoring loop"""
        while True:
            try:
                await self._collect_system_metrics()
                await self._collect_application_metrics()
                await self._check_thresholds()
                await self._cleanup_old_data()
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error("Performance monitoring error", error=str(e))
                await asyncio.sleep(self.monitoring_interval)
    
    async def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            await self._record_metric(MetricType.CPU_USAGE, cpu_percent, "system")
            
            # Memory usage
            memory = psutil.virtual_memory()
            await self._record_metric(MetricType.MEMORY_USAGE, memory.percent, "system")
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            await self._record_metric("disk_usage", disk_percent, "system")
            
            # Network I/O
            network = psutil.net_io_counters()
            await self._record_metric("network_bytes_sent", network.bytes_sent, "system")
            await self._record_metric("network_bytes_recv", network.bytes_recv, "system")
            
        except Exception as e:
            logger.error("System metrics collection error", error=str(e))
    
    async def _collect_application_metrics(self):
        """Collect application-level performance metrics"""
        try:
            # Cache performance
            cache_stats = await advanced_cache.get_cache_stats()
            if cache_stats and "metrics" in cache_stats:
                cache_metrics = cache_stats["metrics"]
                hit_rate = cache_metrics.get("hit_rate", 0) * 100
                await self._record_metric(MetricType.CACHE_HIT_RATE, hit_rate, "cache")
            
            # CPU optimizer metrics
            cpu_metrics = await cpu_optimizer.get_cpu_metrics()
            if cpu_metrics and "task_metrics" in cpu_metrics:
                task_metrics = cpu_metrics["task_metrics"]
                avg_execution_time = task_metrics.get("avg_execution_time", 0) * 1000  # Convert to ms
                await self._record_metric(MetricType.AI_PROCESSING_TIME, avg_execution_time, "ai_processing")
            
            # Throughput
            current_time = time.time()
            if current_time - self.last_throughput_reset >= 60:  # Reset every minute
                throughput = self.throughput_counter / 60  # requests per second
                await self._record_metric(MetricType.THROUGHPUT, throughput, "application")
                self.throughput_counter = 0
                self.last_throughput_reset = current_time
            
        except Exception as e:
            logger.error("Application metrics collection error", error=str(e))
    
    async def _record_metric(self, metric_type: Union[MetricType, str], value: float, 
                           component: str = "", metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        try:
            metric = PerformanceMetric(
                metric_type=metric_type if isinstance(metric_type, MetricType) else MetricType.RESPONSE_TIME,
                value=value,
                component=component,
                metadata=metadata or {}
            )
            
            self.metrics_history.append(metric)
            
            # Keep only recent metrics
            cutoff_time = datetime.now() - timedelta(seconds=self.history_retention)
            self.metrics_history = [
                m for m in self.metrics_history if m.timestamp > cutoff_time
            ]
            
        except Exception as e:
            logger.error("Metric recording error", metric_type=metric_type, error=str(e))
    
    async def _check_thresholds(self):
        """Check performance metrics against thresholds"""
        try:
            # Get recent metrics
            recent_metrics = self._get_recent_metrics(60)  # Last minute
            
            # Group metrics by type and component
            grouped_metrics = {}
            for metric in recent_metrics:
                key = f"{metric.metric_type.value}_{metric.component}"
                if key not in grouped_metrics:
                    grouped_metrics[key] = []
                grouped_metrics[key].append(metric)
            
            # Check thresholds
            for key, metrics in grouped_metrics.items():
                if not metrics:
                    continue
                
                # Calculate average value
                avg_value = sum(m.value for m in metrics) / len(metrics)
                
                # Find matching threshold
                threshold_key = metrics[0].metric_type.value
                if threshold_key in self.thresholds:
                    threshold = self.thresholds[threshold_key]
                    await self._check_metric_threshold(
                        metrics[0].metric_type, avg_value, threshold, metrics[0].component
                    )
            
        except Exception as e:
            logger.error("Threshold checking error", error=str(e))
    
    async def _check_metric_threshold(self, metric_type: MetricType, value: float,
                                    threshold: PerformanceThreshold, component: str):
        """Check a single metric against its threshold"""
        try:
            alert_level = None
            
            # Determine alert level
            if value >= threshold.emergency_threshold:
                alert_level = AlertLevel.EMERGENCY
            elif value >= threshold.critical_threshold:
                alert_level = AlertLevel.CRITICAL
            elif value >= threshold.warning_threshold:
                alert_level = AlertLevel.WARNING
            
            if alert_level:
                # Check if alert already exists and is not resolved
                existing_alert = None
                for alert in self.active_alerts:
                    if (alert.metric_type == metric_type and 
                        alert.component == component and 
                        not alert.resolved):
                        existing_alert = alert
                        break
                
                if not existing_alert:
                    # Create new alert
                    alert = PerformanceAlert(
                        alert_id=f"alert_{int(time.time() * 1000)}",
                        level=alert_level,
                        metric_type=metric_type,
                        current_value=value,
                        threshold=getattr(threshold, f"{alert_level.value}_threshold"),
                        message=f"{metric_type.value} exceeded {alert_level.value} threshold",
                        component=component
                    )
                    
                    self.active_alerts.append(alert)
                    await self._trigger_alert(alert)
                    
        except Exception as e:
            logger.error("Metric threshold check error", metric_type=metric_type.value, error=str(e))
    
    async def _trigger_alert(self, alert: PerformanceAlert):
        """Trigger performance alert"""
        try:
            logger.warning("Performance alert triggered",
                          level=alert.level.value,
                          metric=alert.metric_type.value,
                          value=alert.current_value,
                          threshold=alert.threshold,
                          component=alert.component)
            
            # Call registered alert callbacks
            for callback in self.alert_callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(alert)
                    else:
                        callback(alert)
                except Exception as e:
                    logger.error("Alert callback error", error=str(e))
            
        except Exception as e:
            logger.error("Alert trigger error", error=str(e))
    
    def _get_recent_metrics(self, seconds: int) -> List[PerformanceMetric]:
        """Get metrics from the last N seconds"""
        cutoff_time = datetime.now() - timedelta(seconds=seconds)
        return [m for m in self.metrics_history if m.timestamp > cutoff_time]
    
    async def _cleanup_old_data(self):
        """Clean up old metrics and resolved alerts"""
        try:
            # Clean up old metrics (already done in _record_metric)
            
            # Clean up old resolved alerts
            cutoff_time = datetime.now() - timedelta(seconds=self.alert_cooldown)
            self.active_alerts = [
                alert for alert in self.active_alerts
                if not alert.resolved or alert.timestamp > cutoff_time
            ]
            
        except Exception as e:
            logger.error("Data cleanup error", error=str(e))
    
    def record_response_time(self, response_time: float, component: str = ""):
        """Record API response time"""
        self.response_times.append(response_time)
        
        # Keep only recent response times (last 1000)
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        # Record as metric
        asyncio.create_task(self._record_metric(
            MetricType.RESPONSE_TIME, response_time, component
        ))
    
    def record_error(self, error_type: str, component: str = ""):
        """Record an error occurrence"""
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Calculate error rate
        total_requests = sum(self.error_counts.values()) + self.throughput_counter
        if total_requests > 0:
            error_rate = (sum(self.error_counts.values()) / total_requests) * 100
            asyncio.create_task(self._record_metric(
                MetricType.ERROR_RATE, error_rate, component
            ))
    
    def record_throughput(self):
        """Record throughput (successful request)"""
        self.throughput_counter += 1
    
    def add_alert_callback(self, callback: Callable):
        """Add alert callback function"""
        self.alert_callbacks.append(callback)
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        try:
            recent_metrics = self._get_recent_metrics(300)  # Last 5 minutes
            
            # Calculate summary statistics
            summary = {
                "timestamp": datetime.now().isoformat(),
                "active_alerts": len([a for a in self.active_alerts if not a.resolved]),
                "total_alerts": len(self.active_alerts),
                "metrics_count": len(self.metrics_history),
                "response_times": {
                    "count": len(self.response_times),
                    "avg": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
                    "min": min(self.response_times) if self.response_times else 0,
                    "max": max(self.response_times) if self.response_times else 0
                },
                "error_counts": self.error_counts.copy(),
                "throughput": {
                    "total": self.throughput_counter,
                    "period": time.time() - self.last_throughput_reset
                },
                "recent_metrics": {}
            }
            
            # Group recent metrics by type
            for metric in recent_metrics:
                metric_type = metric.metric_type.value
                if metric_type not in summary["recent_metrics"]:
                    summary["recent_metrics"][metric_type] = {
                        "count": 0,
                        "avg": 0,
                        "min": float('inf'),
                        "max": 0,
                        "components": {}
                    }
                
                metric_summary = summary["recent_metrics"][metric_type]
                metric_summary["count"] += 1
                metric_summary["min"] = min(metric_summary["min"], metric.value)
                metric_summary["max"] = max(metric_summary["max"], metric.value)
                
                # Component breakdown
                component = metric.component or "unknown"
                if component not in metric_summary["components"]:
                    metric_summary["components"][component] = []
                metric_summary["components"][component].append(metric.value)
            
            # Calculate averages
            for metric_type, data in summary["recent_metrics"].items():
                if data["count"] > 0:
                    total = sum(
                        sum(component_values) for component_values in data["components"].values()
                    )
                    data["avg"] = total / data["count"]
                else:
                    data["min"] = 0
            
            return summary
            
        except Exception as e:
            logger.error("Performance summary error", error=str(e))
            return {}
    
    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active performance alerts"""
        return [
            {
                "alert_id": alert.alert_id,
                "level": alert.level.value,
                "metric_type": alert.metric_type.value,
                "current_value": alert.current_value,
                "threshold": alert.threshold,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "component": alert.component
            }
            for alert in self.active_alerts if not alert.resolved
        ]
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve a performance alert"""
        try:
            for alert in self.active_alerts:
                if alert.alert_id == alert_id:
                    alert.resolved = True
                    logger.info("Alert resolved", alert_id=alert_id)
                    return True
            return False
        except Exception as e:
            logger.error("Alert resolution error", alert_id=alert_id, error=str(e))
            return False
    
    async def shutdown(self):
        """Shutdown performance monitor"""
        try:
            if self._monitoring_task:
                self._monitoring_task.cancel()
            logger.info("Performance monitor shutdown complete")
        except Exception as e:
            logger.error("Performance monitor shutdown error", error=str(e))


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


# Convenience functions
def record_response_time(response_time: float, component: str = ""):
    """Record API response time"""
    performance_monitor.record_response_time(response_time, component)


def record_error(error_type: str, component: str = ""):
    """Record an error"""
    performance_monitor.record_error(error_type, component)


def record_throughput():
    """Record successful request"""
    performance_monitor.record_throughput()


async def get_performance_summary() -> Dict[str, Any]:
    """Get performance summary"""
    return await performance_monitor.get_performance_summary()


async def get_active_alerts() -> List[Dict[str, Any]]:
    """Get active alerts"""
    return await performance_monitor.get_active_alerts()
