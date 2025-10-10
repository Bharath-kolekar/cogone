"""
Enhanced Monitoring Analytics Manager

⚠️ HONEST STATUS: Provides monitoring structure and interfaces
Some methods return placeholder data - these are marked with warnings
Real integrations needed for full functionality

This module provides monitoring and analytics capabilities including
real-time monitoring structure, performance analytics interfaces,
and reporting frameworks.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import statistics
from collections import defaultdict, deque
import time

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core
from app.core.enhanced_context_sharing import enhanced_context_sharing, ContextType

logger = structlog.get_logger(__name__)

class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    CUSTOM = "custom"

class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ComponentStatus(Enum):
    """Component status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class MetricData:
    """Metric data structure"""
    metric_id: str
    metric_type: MetricType
    component_id: str
    name: str
    value: Union[int, float, str]
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AlertRule:
    """Alert rule configuration"""
    rule_id: str
    name: str
    metric_name: str
    condition: str  # e.g., "value > 100"
    severity: AlertSeverity
    enabled: bool = True
    cooldown_minutes: int = 5
    last_triggered: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Alert:
    """Alert instance"""
    alert_id: str
    rule_id: str
    component_id: str
    severity: AlertSeverity
    message: str
    metric_value: Union[int, float, str]
    triggered_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceReport:
    """Performance analysis report"""
    report_id: str
    component_id: str
    period_start: datetime
    period_end: datetime
    total_requests: int
    success_rate: float
    average_response_time: float
    error_rate: float
    throughput: float
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemHealth:
    """System health status"""
    overall_status: ComponentStatus
    component_statuses: Dict[str, ComponentStatus]
    critical_alerts: int
    warnings: int
    uptime_percentage: float
    last_updated: datetime = field(default_factory=datetime.now)
    recommendations: List[str] = field(default_factory=list)

class EnhancedMonitoringAnalytics:
    """Enhanced monitoring and analytics manager"""
    
    def __init__(self):
        self.redis_client = None
        self.metrics_buffer: deque = deque(maxlen=10000)
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.component_health: Dict[str, ComponentStatus] = {}
        self.performance_history: Dict[str, List[float]] = defaultdict(list)
        self.metric_aggregates: Dict[str, Dict[str, Any]] = {}
        
        # Initialize monitoring system
        self._initialize_monitoring_system()
        self._initialize_alert_system()
        self._background_tasks_started = False
    
    def _initialize_monitoring_system(self):
        """Initialize the monitoring system"""
        self.metric_prefixes = {
            "performance": "metrics:perf:",
            "security": "metrics:sec:",
            "quality": "metrics:qual:",
            "consistency": "metrics:cons:",
            "error": "metrics:err:",
            "custom": "metrics:custom:"
        }
        
        # Initialize default alert rules
        self._initialize_default_alert_rules()
        
        logger.info("Enhanced monitoring system initialized")
    
    def _initialize_alert_system(self):
        """Initialize the alert system"""
        self.alert_channels = {
            "critical": "alerts:critical",
            "high": "alerts:high",
            "medium": "alerts:medium",
            "low": "alerts:low",
            "info": "alerts:info"
        }
        
        logger.info("Alert system initialized")
    
    def _initialize_default_alert_rules(self):
        """Initialize default alert rules"""
        default_rules = [
            AlertRule(
                rule_id="high_error_rate",
                name="High Error Rate",
                metric_name="error_rate",
                condition="value > 5",
                severity=AlertSeverity.HIGH,
                cooldown_minutes=10
            ),
            AlertRule(
                rule_id="slow_response_time",
                name="Slow Response Time",
                metric_name="response_time",
                condition="value > 5000",
                severity=AlertSeverity.MEDIUM,
                cooldown_minutes=5
            ),
            AlertRule(
                rule_id="low_success_rate",
                name="Low Success Rate",
                metric_name="success_rate",
                condition="value < 95",
                severity=AlertSeverity.HIGH,
                cooldown_minutes=15
            ),
            AlertRule(
                rule_id="high_memory_usage",
                name="High Memory Usage",
                metric_name="memory_usage",
                condition="value > 80",
                severity=AlertSeverity.MEDIUM,
                cooldown_minutes=5
            ),
            AlertRule(
                rule_id="security_violation",
                name="Security Violation Detected",
                metric_name="security_violations",
                condition="value > 0",
                severity=AlertSeverity.CRITICAL,
                cooldown_minutes=1
            )
        ]
        
        for rule in default_rules:
            self.alert_rules[rule.rule_id] = rule
        
        logger.info("Default alert rules initialized", count=len(default_rules))
    
    def _start_background_tasks(self):
        """Start background monitoring tasks"""
        asyncio.create_task(self._metrics_processor())
        asyncio.create_task(self._alert_processor())
        asyncio.create_task(self._health_checker())
        asyncio.create_task(self._performance_analyzer())
        
        logger.info("Background monitoring tasks started")
    
    async def _ensure_background_tasks_started(self):
        """Ensure background tasks are started"""
        if not self._background_tasks_started:
            try:
                self._start_background_tasks()
                self._background_tasks_started = True
            except RuntimeError:
                # No event loop running, will start later
                pass
    
    async def record_metric(self, metric_data: MetricData) -> bool:
        """Record a metric with buffering and aggregation"""
        try:
            # Ensure background tasks are started
            await self._ensure_background_tasks_started()
            # Add to buffer
            self.metrics_buffer.append(metric_data)
            
            # Update real-time aggregates
            await self._update_metric_aggregates(metric_data)
            
            # Check alert rules
            await self._check_alert_rules(metric_data)
            
            # Store in Redis for persistence
            await self._store_metric_in_redis(metric_data)
            
            logger.debug("Metric recorded", 
                        metric_id=metric_data.metric_id,
                        component_id=metric_data.component_id,
                        name=metric_data.name,
                        value=metric_data.value)
            
            return True
            
        except Exception as e:
            logger.error("Failed to record metric", 
                        metric_id=metric_data.metric_id,
                        error=str(e))
            return False
    
    async def get_component_metrics(self, component_id: str, 
                                  metric_names: List[str] = None,
                                  time_range_minutes: int = 60) -> Dict[str, List[MetricData]]:
        """Get metrics for a specific component"""
        try:
            component_metrics = defaultdict(list)
            
            # Filter metrics from buffer
            cutoff_time = datetime.now() - timedelta(minutes=time_range_minutes)
            
            for metric in self.metrics_buffer:
                if (metric.component_id == component_id and 
                    metric.timestamp >= cutoff_time):
                    
                    if metric_names is None or metric.name in metric_names:
                        component_metrics[metric.name].append(metric)
            
            # Sort by timestamp
            for metric_list in component_metrics.values():
                metric_list.sort(key=lambda m: m.timestamp)
            
            logger.info("Component metrics retrieved", 
                       component_id=component_id,
                       metric_count=sum(len(metrics) for metrics in component_metrics.values()))
            
            return dict(component_metrics)
            
        except Exception as e:
            logger.error("Failed to get component metrics", 
                        component_id=component_id,
                        error=str(e))
            return {}
    
    async def get_system_health(self) -> SystemHealth:
        """Get overall system health status"""
        try:
            # Analyze component statuses
            component_statuses = {}
            critical_alerts = 0
            warnings = 0
            
            for component_id, status in self.component_health.items():
                component_statuses[component_id] = status
                
                if status == ComponentStatus.CRITICAL:
                    critical_alerts += 1
                elif status == ComponentStatus.WARNING:
                    warnings += 1
            
            # Count active alerts
            for alert in self.active_alerts.values():
                if alert.severity == AlertSeverity.CRITICAL:
                    critical_alerts += 1
                elif alert.severity in [AlertSeverity.HIGH, AlertSeverity.MEDIUM]:
                    warnings += 1
            
            # Determine overall status
            if critical_alerts > 0:
                overall_status = ComponentStatus.CRITICAL
            elif warnings > 0:
                overall_status = ComponentStatus.WARNING
            elif all(status == ComponentStatus.HEALTHY for status in component_statuses.values()):
                overall_status = ComponentStatus.HEALTHY
            else:
                overall_status = ComponentStatus.WARNING
            
            # Calculate uptime percentage (simplified)
            uptime_percentage = await self._calculate_uptime_percentage()
            
            # Generate recommendations
            recommendations = await self._generate_health_recommendations(
                component_statuses, critical_alerts, warnings)
            
            system_health = SystemHealth(
                overall_status=overall_status,
                component_statuses=component_statuses,
                critical_alerts=critical_alerts,
                warnings=warnings,
                uptime_percentage=uptime_percentage,
                recommendations=recommendations
            )
            
            logger.info("System health retrieved", 
                       overall_status=overall_status.value,
                       critical_alerts=critical_alerts,
                       warnings=warnings)
            
            return system_health
            
        except Exception as e:
            logger.error("Failed to get system health", error=str(e))
            return SystemHealth(
                overall_status=ComponentStatus.UNKNOWN,
                component_statuses={},
                critical_alerts=0,
                warnings=0,
                uptime_percentage=0.0
            )
    
    async def generate_performance_report(self, component_id: str,
                                        period_hours: int = 24) -> PerformanceReport:
        """Generate comprehensive performance report"""
        try:
            period_end = datetime.now()
            period_start = period_end - timedelta(hours=period_hours)
            
            # Get metrics for the period
            metrics = await self.get_component_metrics(
                component_id=component_id,
                time_range_minutes=period_hours * 60
            )
            
            # Calculate performance metrics
            total_requests = 0
            successful_requests = 0
            response_times = []
            errors = 0
            
            for metric_name, metric_list in metrics.items():
                if metric_name == "requests_total":
                    total_requests = sum(m.value for m in metric_list if isinstance(m.value, (int, float)))
                elif metric_name == "requests_successful":
                    successful_requests = sum(m.value for m in metric_list if isinstance(m.value, (int, float)))
                elif metric_name == "response_time":
                    response_times.extend([m.value for m in metric_list if isinstance(m.value, (int, float))])
                elif metric_name == "errors_total":
                    errors = sum(m.value for m in metric_list if isinstance(m.value, (int, float)))
            
            # Calculate derived metrics
            success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
            error_rate = (errors / total_requests * 100) if total_requests > 0 else 0
            average_response_time = statistics.mean(response_times) if response_times else 0
            throughput = total_requests / period_hours if period_hours > 0 else 0
            
            # Generate recommendations
            recommendations = await self._generate_performance_recommendations(
                success_rate, error_rate, average_response_time, throughput)
            
            report = PerformanceReport(
                report_id=str(uuid.uuid4()),
                component_id=component_id,
                period_start=period_start,
                period_end=period_end,
                total_requests=total_requests,
                success_rate=success_rate,
                average_response_time=average_response_time,
                error_rate=error_rate,
                throughput=throughput,
                recommendations=recommendations,
                metadata={
                    "generated_at": datetime.now().isoformat(),
                    "period_hours": period_hours
                }
            )
            
            logger.info("Performance report generated", 
                       component_id=component_id,
                       period_hours=period_hours,
                       total_requests=total_requests,
                       success_rate=success_rate)
            
            return report
            
        except Exception as e:
            logger.error("Failed to generate performance report", 
                        component_id=component_id,
                        error=str(e))
            raise
    
    async def create_alert_rule(self, alert_rule: AlertRule) -> bool:
        """Create a new alert rule"""
        try:
            self.alert_rules[alert_rule.rule_id] = alert_rule
            
            # Store in Redis for persistence
            rule_key = f"alert_rule:{alert_rule.rule_id}"
            rule_data = {
                "rule_id": alert_rule.rule_id,
                "name": alert_rule.name,
                "metric_name": alert_rule.metric_name,
                "condition": alert_rule.condition,
                "severity": alert_rule.severity.value,
                "enabled": alert_rule.enabled,
                "cooldown_minutes": alert_rule.cooldown_minutes,
                "last_triggered": alert_rule.last_triggered.isoformat() if alert_rule.last_triggered else None,
                "metadata": alert_rule.metadata
            }
            
            await self.redis_client.set(
                rule_key,
                json.dumps(rule_data, default=str),
                ex=86400  # 24 hours
            )
            
            logger.info("Alert rule created", 
                       rule_id=alert_rule.rule_id,
                       name=alert_rule.name,
                       severity=alert_rule.severity.value)
            
            return True
            
        except Exception as e:
            logger.error("Failed to create alert rule", 
                        rule_id=alert_rule.rule_id,
                        error=str(e))
            return False
    
    async def get_active_alerts(self, severity: AlertSeverity = None) -> List[Alert]:
        """Get active alerts, optionally filtered by severity"""
        try:
            alerts = list(self.active_alerts.values())
            
            if severity:
                alerts = [alert for alert in alerts if alert.severity == severity]
            
            # Sort by triggered time (most recent first)
            alerts.sort(key=lambda a: a.triggered_at, reverse=True)
            
            return alerts
            
        except Exception as e:
            logger.error("Failed to get active alerts", error=str(e))
            return []
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an active alert"""
        try:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.resolved_at = datetime.now()
                
                # Remove from active alerts
                del self.active_alerts[alert_id]
                
                # Store resolved alert in Redis
                resolved_key = f"resolved_alert:{alert_id}"
                alert_data = {
                    "alert_id": alert.alert_id,
                    "rule_id": alert.rule_id,
                    "component_id": alert.component_id,
                    "severity": alert.severity.value,
                    "message": alert.message,
                    "metric_value": alert.metric_value,
                    "triggered_at": alert.triggered_at.isoformat(),
                    "resolved_at": alert.resolved_at.isoformat(),
                    "metadata": alert.metadata
                }
                
                await self.redis_client.set(
                    resolved_key,
                    json.dumps(alert_data, default=str),
                    ex=604800  # 7 days
                )
                
                logger.info("Alert resolved", alert_id=alert_id)
                return True
            else:
                logger.warning("Alert not found for resolution", alert_id=alert_id)
                return False
                
        except Exception as e:
            logger.error("Failed to resolve alert", alert_id=alert_id, error=str(e))
            return False
    
    async def get_monitoring_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        try:
            # Get system health
            system_health = await self.get_system_health()
            
            # Get active alerts
            active_alerts = await self.get_active_alerts()
            
            # Get performance metrics for key components
            performance_metrics = {}
            key_components = ["ethical_ai_core", "security_validator", "code_quality_analyzer"]
            
            for component_id in key_components:
                metrics = await self.get_component_metrics(
                    component_id=component_id,
                    time_range_minutes=60
                )
                performance_metrics[component_id] = metrics
            
            # Get metric aggregates
            metric_summary = await self._get_metric_summary()
            
            dashboard_data = {
                "system_health": {
                    "overall_status": system_health.overall_status.value,
                    "component_statuses": {
                        comp: status.value for comp, status in system_health.component_statuses.items()
                    },
                    "critical_alerts": system_health.critical_alerts,
                    "warnings": system_health.warnings,
                    "uptime_percentage": system_health.uptime_percentage,
                    "recommendations": system_health.recommendations
                },
                "active_alerts": [
                    {
                        "alert_id": alert.alert_id,
                        "rule_id": alert.rule_id,
                        "component_id": alert.component_id,
                        "severity": alert.severity.value,
                        "message": alert.message,
                        "triggered_at": alert.triggered_at.isoformat()
                    }
                    for alert in active_alerts[:10]  # Limit to 10 most recent
                ],
                "performance_metrics": {
                    component_id: {
                        metric_name: [
                            {
                                "value": metric.value,
                                "timestamp": metric.timestamp.isoformat()
                            }
                            for metric in metric_list[-20:]  # Last 20 data points
                        ]
                        for metric_name, metric_list in metrics.items()
                    }
                    for component_id, metrics in performance_metrics.items()
                },
                "metric_summary": metric_summary,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info("Dashboard data generated", 
                       active_alerts=len(active_alerts),
                       components_monitored=len(key_components))
            
            return dashboard_data
            
        except Exception as e:
            logger.error("Failed to generate dashboard data", error=str(e))
            return {}
    
    # Background tasks
    
    async def _metrics_processor(self):
        """Background task to process metrics"""
        while True:
            try:
                # Process metrics from buffer
                if self.metrics_buffer:
                    # Aggregate metrics by component and name
                    await self._aggregate_metrics()
                
                # Sleep for processing interval
                await asyncio.sleep(30)  # Process every 30 seconds
                
            except Exception as e:
                logger.error("Metrics processor error", error=str(e))
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _alert_processor(self):
        """Background task to process alerts"""
        while True:
            try:
                # Check for expired alerts
                await self._cleanup_expired_alerts()
                
                # Send alert notifications
                await self._send_alert_notifications()
                
                # Sleep for processing interval
                await asyncio.sleep(60)  # Process every minute
                
            except Exception as e:
                logger.error("Alert processor error", error=str(e))
                await asyncio.sleep(120)  # Wait longer on error
    
    async def _health_checker(self):
        """Background task to check component health"""
        while True:
            try:
                # Check health of all components
                await self._check_component_health()
                
                # Sleep for health check interval
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error("Health checker error", error=str(e))
                await asyncio.sleep(600)  # Wait longer on error
    
    async def _performance_analyzer(self):
        """Background task to analyze performance"""
        while True:
            try:
                # Analyze performance trends
                await self._analyze_performance_trends()
                
                # Generate performance insights
                await self._generate_performance_insights()
                
                # Sleep for analysis interval
                await asyncio.sleep(1800)  # Analyze every 30 minutes
                
            except Exception as e:
                logger.error("Performance analyzer error", error=str(e))
                await asyncio.sleep(3600)  # Wait longer on error
    
    # Helper methods
    
    async def _update_metric_aggregates(self, metric_data: MetricData):
        """Update real-time metric aggregates"""
        try:
            aggregate_key = f"{metric_data.component_id}:{metric_data.name}"
            
            if aggregate_key not in self.metric_aggregates:
                self.metric_aggregates[aggregate_key] = {
                    "count": 0,
                    "sum": 0,
                    "min": float('inf'),
                    "max": float('-inf'),
                    "last_value": 0,
                    "last_updated": datetime.now()
                }
            
            aggregate = self.metric_aggregates[aggregate_key]
            
            if isinstance(metric_data.value, (int, float)):
                aggregate["count"] += 1
                aggregate["sum"] += metric_data.value
                aggregate["min"] = min(aggregate["min"], metric_data.value)
                aggregate["max"] = max(aggregate["max"], metric_data.value)
                aggregate["last_value"] = metric_data.value
            
            aggregate["last_updated"] = datetime.now()
            
        except Exception as e:
            logger.error("Failed to update metric aggregates", error=str(e))
    
    async def _check_alert_rules(self, metric_data: MetricData):
        """Check if metric data triggers any alert rules"""
        try:
            for rule_id, rule in self.alert_rules.items():
                if not rule.enabled:
                    continue
                
                # Check if rule applies to this metric
                if rule.metric_name != metric_data.name:
                    continue
                
                # Check cooldown period
                if (rule.last_triggered and 
                    datetime.now() - rule.last_triggered < timedelta(minutes=rule.cooldown_minutes)):
                    continue
                
                # Evaluate condition
                if await self._evaluate_alert_condition(rule.condition, metric_data.value):
                    await self._trigger_alert(rule, metric_data)
                    rule.last_triggered = datetime.now()
                    
        except Exception as e:
            logger.error("Failed to check alert rules", error=str(e))
    
    async def _evaluate_alert_condition(self, condition: str, value: Union[int, float, str]) -> bool:
        """Evaluate alert condition (simplified implementation)"""
        try:
            # Simple condition evaluation - in production, use a proper expression evaluator
            if ">" in condition:
                threshold = float(condition.split(">")[1].strip())
                return float(value) > threshold
            elif "<" in condition:
                threshold = float(condition.split("<")[1].strip())
                return float(value) < threshold
            elif "==" in condition:
                expected = condition.split("==")[1].strip().strip('"')
                return str(value) == expected
            else:
                return False
                
        except Exception as e:
            logger.error("Failed to evaluate alert condition", 
                        condition=condition, 
                        value=value, 
                        error=str(e))
            return False
    
    async def _trigger_alert(self, rule: AlertRule, metric_data: MetricData):
        """Trigger an alert"""
        try:
            alert_id = str(uuid.uuid4())
            
            alert = Alert(
                alert_id=alert_id,
                rule_id=rule.rule_id,
                component_id=metric_data.component_id,
                severity=rule.severity,
                message=f"{rule.name}: {metric_data.name} = {metric_data.value}",
                metric_value=metric_data.value,
                metadata={
                    "condition": rule.condition,
                    "metric_id": metric_data.metric_id,
                    "tags": metric_data.tags
                }
            )
            
            self.active_alerts[alert_id] = alert
            
            # Publish alert to Redis channel
            alert_data = {
                "alert_id": alert.alert_id,
                "rule_id": alert.rule_id,
                "component_id": alert.component_id,
                "severity": alert.severity.value,
                "message": alert.message,
                "metric_value": alert.metric_value,
                "triggered_at": alert.triggered_at.isoformat(),
                "metadata": alert.metadata
            }
            
            await self.redis_client.publish(
                self.alert_channels[rule.severity.value],
                json.dumps(alert_data, default=str)
            )
            
            logger.warning("Alert triggered", 
                          alert_id=alert_id,
                          rule_name=rule.name,
                          severity=rule.severity.value,
                          component_id=metric_data.component_id)
            
        except Exception as e:
            logger.error("Failed to trigger alert", 
                        rule_id=rule.rule_id,
                        error=str(e))
    
    async def _store_metric_in_redis(self, metric_data: MetricData):
        """Store metric in Redis for persistence"""
        try:
            metric_key = f"{self.metric_prefixes.get('custom', 'metrics:custom:')}{metric_data.metric_id}"
            
            metric_dict = {
                "metric_id": metric_data.metric_id,
                "metric_type": metric_data.metric_type.value,
                "component_id": metric_data.component_id,
                "name": metric_data.name,
                "value": metric_data.value,
                "timestamp": metric_data.timestamp.isoformat(),
                "tags": metric_data.tags,
                "metadata": metric_data.metadata
            }
            
            await self.redis_client.set(
                metric_key,
                json.dumps(metric_dict, default=str),
                ex=86400  # 24 hours
            )
            
        except Exception as e:
            logger.error("Failed to store metric in Redis", error=str(e))
    
    async def _calculate_uptime_percentage(self) -> float:
        """Calculate system uptime percentage"""
        try:
            # Simplified uptime calculation
            # In production, this would analyze actual uptime data
            return 99.9  # Placeholder
            
        except Exception as e:
            logger.error("Failed to calculate uptime percentage", error=str(e))
            return 0.0
    
    async def _generate_health_recommendations(self, component_statuses: Dict[str, ComponentStatus],
                                            critical_alerts: int, warnings: int) -> List[str]:
        """Generate health recommendations"""
        recommendations = []
        
        if critical_alerts > 0:
            recommendations.append("Address critical alerts immediately")
        
        if warnings > 5:
            recommendations.append("Review and resolve warning conditions")
        
        unhealthy_components = [
            comp for comp, status in component_statuses.items() 
            if status in [ComponentStatus.ERROR, ComponentStatus.CRITICAL]
        ]
        
        if unhealthy_components:
            recommendations.append(f"Check health of components: {', '.join(unhealthy_components)}")
        
        if not recommendations:
            recommendations.append("System is operating normally")
        
        return recommendations
    
    async def _generate_performance_recommendations(self, success_rate: float, error_rate: float,
                                                  average_response_time: float, throughput: float) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if success_rate < 95:
            recommendations.append("Improve error handling to increase success rate")
        
        if error_rate > 5:
            recommendations.append("Investigate and fix error sources")
        
        if average_response_time > 2000:
            recommendations.append("Optimize response times through caching or code optimization")
        
        if throughput < 100:
            recommendations.append("Consider scaling resources to improve throughput")
        
        if not recommendations:
            recommendations.append("Performance metrics are within acceptable ranges")
        
        return recommendations
    
    async def _aggregate_metrics(self):
        """Aggregate metrics from buffer"""
        try:
            # Group metrics by component and name
            grouped_metrics = defaultdict(list)
            
            for metric in self.metrics_buffer:
                key = f"{metric.component_id}:{metric.name}"
                grouped_metrics[key].append(metric)
            
            # Calculate aggregates for each group
            for key, metrics in grouped_metrics.items():
                if metrics:
                    values = [m.value for m in metrics if isinstance(m.value, (int, float))]
                    if values:
                        # Store performance history
                        self.performance_history[key].extend(values)
                        
                        # Keep only recent history (last 1000 values)
                        if len(self.performance_history[key]) > 1000:
                            self.performance_history[key] = self.performance_history[key][-1000:]
            
        except Exception as e:
            logger.error("Failed to aggregate metrics", error=str(e))
    
    async def _cleanup_expired_alerts(self):
        """Clean up expired alerts"""
        try:
            current_time = datetime.now()
            expired_alerts = []
            
            for alert_id, alert in self.active_alerts.items():
                # Consider alerts older than 24 hours as expired
                if current_time - alert.triggered_at > timedelta(hours=24):
                    expired_alerts.append(alert_id)
            
            for alert_id in expired_alerts:
                await self.resolve_alert(alert_id)
            
            if expired_alerts:
                logger.info("Expired alerts cleaned up", count=len(expired_alerts))
                
        except Exception as e:
            logger.error("Failed to cleanup expired alerts", error=str(e))
    
    async def _send_alert_notifications(self):
        """Send alert notifications"""
        try:
            # In production, this would integrate with notification services
            # (email, Slack, PagerDuty, etc.)
            pass
            
        except Exception as e:
            logger.error("Failed to send alert notifications", error=str(e))
    
    async def _check_component_health(self):
        """Check health of all components"""
        try:
            # Check health of key components
            components_to_check = [
                "ethical_ai_core",
                "security_validator", 
                "code_quality_analyzer",
                "error_recovery_manager",
                "factual_accuracy_validator",
                "consistency_enforcer"
            ]
            
            for component_id in components_to_check:
                # Get recent metrics for the component
                metrics = await self.get_component_metrics(
                    component_id=component_id,
                    time_range_minutes=5
                )
                
                # Determine health based on metrics
                health_status = await self._determine_component_health(component_id, metrics)
                self.component_health[component_id] = health_status
            
            logger.debug("Component health checked", 
                        components=len(components_to_check))
            
        except Exception as e:
            logger.error("Failed to check component health", error=str(e))
    
    async def _determine_component_health(self, component_id: str, 
                                        metrics: Dict[str, List[MetricData]]) -> ComponentStatus:
        """Determine component health based on metrics"""
        try:
            # Check for error metrics
            if "errors_total" in metrics:
                error_metrics = metrics["errors_total"]
                if error_metrics and error_metrics[-1].value > 0:
                    return ComponentStatus.ERROR
            
            # Check for performance metrics
            if "response_time" in metrics:
                response_metrics = metrics["response_time"]
                if response_metrics:
                    avg_response_time = statistics.mean([m.value for m in response_metrics if isinstance(m.value, (int, float))])
                    if avg_response_time > 10000:  # 10 seconds
                        return ComponentStatus.WARNING
            
            # Check for success rate
            if "success_rate" in metrics:
                success_metrics = metrics["success_rate"]
                if success_metrics:
                    latest_success_rate = success_metrics[-1].value
                    if isinstance(latest_success_rate, (int, float)) and latest_success_rate < 90:
                        return ComponentStatus.WARNING
            
            return ComponentStatus.HEALTHY
            
        except Exception as e:
            logger.error("Failed to determine component health", 
                        component_id=component_id,
                        error=str(e))
            return ComponentStatus.UNKNOWN
    
    async def _analyze_performance_trends(self):
        """Analyze performance trends"""
        try:
            # Analyze trends in performance history
            for key, values in self.performance_history.items():
                if len(values) > 10:
                    # Calculate trend (simple linear regression)
                    recent_values = values[-10:]
                    if all(isinstance(v, (int, float)) for v in recent_values):
                        # Simple trend calculation
                        trend = (recent_values[-1] - recent_values[0]) / len(recent_values)
                        
                        # Store trend analysis
                        trend_key = f"trend:{key}"
                        trend_data = {
                            "trend": trend,
                            "last_value": recent_values[-1],
                            "analyzed_at": datetime.now().isoformat()
                        }
                        
                        await self.redis_client.set(
                            trend_key,
                            json.dumps(trend_data, default=str),
                            ex=3600  # 1 hour
                        )
            
        except Exception as e:
            logger.error("Failed to analyze performance trends", error=str(e))
    
    async def _generate_performance_insights(self):
        """Generate performance insights"""
        try:
            # Generate insights based on performance data
            insights = []
            
            # Analyze metric aggregates
            for key, aggregate in self.metric_aggregates.items():
                if aggregate["count"] > 0:
                    avg_value = aggregate["sum"] / aggregate["count"]
                    
                    # Generate insight based on average value
                    if "response_time" in key and avg_value > 5000:
                        insights.append(f"High response time detected for {key}: {avg_value}ms")
                    
                    if "error_rate" in key and avg_value > 5:
                        insights.append(f"High error rate detected for {key}: {avg_value}%")
            
            # Store insights
            if insights:
                insights_key = "performance_insights"
                await self.redis_client.set(
                    insights_key,
                    json.dumps({
                        "insights": insights,
                        "generated_at": datetime.now().isoformat()
                    }, default=str),
                    ex=3600  # 1 hour
                )
            
        except Exception as e:
            logger.error("Failed to generate performance insights", error=str(e))
    
    async def _get_metric_summary(self) -> Dict[str, Any]:
        """Get summary of metrics"""
        try:
            summary = {
                "total_metrics": len(self.metrics_buffer),
                "components_monitored": len(set(m.component_id for m in self.metrics_buffer)),
                "metric_types": {},
                "recent_activity": {}
            }
            
            # Count metrics by type
            for metric in self.metrics_buffer:
                metric_type = metric.metric_type.value
                summary["metric_types"][metric_type] = summary["metric_types"].get(metric_type, 0) + 1
            
            # Recent activity (last hour)
            cutoff_time = datetime.now() - timedelta(hours=1)
            recent_metrics = [m for m in self.metrics_buffer if m.timestamp >= cutoff_time]
            
            summary["recent_activity"] = {
                "metrics_count": len(recent_metrics),
                "components_active": len(set(m.component_id for m in recent_metrics))
            }
            
            return summary
            
        except Exception as e:
            logger.error("Failed to get metric summary", error=str(e))
            return {}

# Global instance
enhanced_monitoring_analytics = EnhancedMonitoringAnalytics()
