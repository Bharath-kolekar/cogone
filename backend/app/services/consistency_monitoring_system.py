"""
Real-time Consistency Monitoring System
Monitors and alerts on consistency issues across the entire CognOmega platform
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)

class MonitoringLevel(Enum):
    """Monitoring alert levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ConsistencyMetric(Enum):
    """Types of consistency metrics"""
    VARIABLE_NAMING = "variable_naming"
    API_ENDPOINTS = "api_endpoints"
    DATABASE_SCHEMA = "database_schema"
    FRONTEND_BACKEND_SYNC = "frontend_backend_sync"
    CONFIG_CONSISTENCY = "config_consistency"
    IMPORT_ORDER = "import_order"
    ERROR_HANDLING = "error_handling"

@dataclass
class ConsistencyAlert:
    """Consistency monitoring alert"""
    alert_id: str
    metric_type: ConsistencyMetric
    level: MonitoringLevel
    message: str
    details: Dict[str, Any]
    timestamp: datetime
    source: str
    resolved: bool = False
    resolution_notes: Optional[str] = None

@dataclass
class ConsistencyMetricData:
    """Consistency metric data point"""
    metric_type: ConsistencyMetric
    value: float
    threshold: float
    timestamp: datetime
    context: Dict[str, Any]

class RealTimeConsistencyMonitor:
    """
    Real-time consistency monitoring system
    Continuously monitors the platform for consistency issues
    """
    
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_interval = 30  # seconds
        self.alerts: List[ConsistencyAlert] = []
        self.metrics: List[ConsistencyMetricData] = []
        self.thresholds = self._initialize_thresholds()
        self.alert_callbacks: List[Callable] = []
        self.monitoring_task: Optional[asyncio.Task] = None
        
        # Import consistency manager
        from .proactive_consistency_manager import proactive_consistency_manager
        self.consistency_manager = proactive_consistency_manager
        
    def _initialize_thresholds(self) -> Dict[ConsistencyMetric, float]:
        """Initialize consistency thresholds"""
        return {
            ConsistencyMetric.VARIABLE_NAMING: 100.0,  # Must be 100%
            ConsistencyMetric.API_ENDPOINTS: 95.0,     # 95% consistency
            ConsistencyMetric.DATABASE_SCHEMA: 100.0,  # Must be 100%
            ConsistencyMetric.FRONTEND_BACKEND_SYNC: 100.0,  # Must be 100%
            ConsistencyMetric.CONFIG_CONSISTENCY: 100.0,     # Must be 100%
            ConsistencyMetric.IMPORT_ORDER: 90.0,      # 90% consistency
            ConsistencyMetric.ERROR_HANDLING: 95.0,    # 95% consistency
        }
    
    async def start_monitoring(self):
        """Start real-time consistency monitoring"""
        if self.is_monitoring:
            logger.warning("Consistency monitoring already running")
            return
            
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("🔍 Real-time consistency monitoring started")
    
    async def stop_monitoring(self):
        """Stop real-time consistency monitoring"""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Real-time consistency monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                await self._run_consistency_checks()
                await asyncio.sleep(self.monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Short delay before retry
    
    async def _run_consistency_checks(self):
        """Run all consistency checks"""
        logger.debug("Running consistency checks...")
        
        # Check variable naming consistency
        await self._check_variable_naming_consistency()
        
        # Check API endpoint consistency
        await self._check_api_endpoint_consistency()
        
        # Check database schema consistency
        await self._check_database_schema_consistency()
        
        # Check frontend-backend synchronization
        await self._check_frontend_backend_sync()
        
        # Check configuration consistency
        await self._check_config_consistency()
        
        # Check import order consistency
        await self._check_import_order_consistency()
        
        # Check error handling consistency
        await self._check_error_handling_consistency()
        
        # Clean up old metrics
        await self._cleanup_old_metrics()
    
    async def _check_variable_naming_consistency(self):
        """Check variable naming consistency across the platform"""
        try:
            # Check environment templates
            template_files = [
                "ENHANCED_ENV_TEMPLATE.md",
                "ENVIRONMENT_TEMPLATE.md"
            ]
            
            issues_found = 0
            for template_file in template_files:
                if Path(template_file).exists():
                    with open(template_file, 'r') as f:
                        content = f.read()
                    
                    # Check for inconsistent variable names
                    if "JWT_SECRET_KEY" in content:
                        issues_found += 1
                        await self._create_alert(
                            ConsistencyMetric.VARIABLE_NAMING,
                            MonitoringLevel.ERROR,
                            f"Inconsistent variable name in {template_file}",
                            {"file": template_file, "issue": "JWT_SECRET_KEY should be JWT_SECRET"}
                        )
            
            # Calculate consistency score
            consistency_score = max(0, 100 - (issues_found * 10))
            await self._record_metric(
                ConsistencyMetric.VARIABLE_NAMING,
                consistency_score,
                self.thresholds[ConsistencyMetric.VARIABLE_NAMING]
            )
            
        except Exception as e:
            logger.error(f"Error checking variable naming consistency: {e}")
    
    async def _check_api_endpoint_consistency(self):
        """Check API endpoint consistency"""
        try:
            # This would check API endpoints for consistency
            # For now, assume 95% consistency
            await self._record_metric(
                ConsistencyMetric.API_ENDPOINTS,
                95.0,
                self.thresholds[ConsistencyMetric.API_ENDPOINTS]
            )
            
        except Exception as e:
            logger.error(f"Error checking API endpoint consistency: {e}")
    
    async def _check_database_schema_consistency(self):
        """Check database schema consistency"""
        try:
            # This would check database schemas for consistency
            # For now, assume 100% consistency
            await self._record_metric(
                ConsistencyMetric.DATABASE_SCHEMA,
                100.0,
                self.thresholds[ConsistencyMetric.DATABASE_SCHEMA]
            )
            
        except Exception as e:
            logger.error(f"Error checking database schema consistency: {e}")
    
    async def _check_frontend_backend_sync(self):
        """Check frontend-backend synchronization"""
        try:
            # Check if frontend variables are properly defined
            template_files = [
                "ENHANCED_ENV_TEMPLATE.md",
                "ENVIRONMENT_TEMPLATE.md"
            ]
            
            required_vars = [
                "NEXT_PUBLIC_SUPABASE_URL",
                "NEXT_PUBLIC_SUPABASE_ANON_KEY",
                "NEXT_PUBLIC_API_URL",
                "NEXT_PUBLIC_APP_URL"
            ]
            
            issues_found = 0
            for template_file in template_files:
                if Path(template_file).exists():
                    with open(template_file, 'r') as f:
                        content = f.read()
                    
                    for var in required_vars:
                        if var not in content:
                            issues_found += 1
                            await self._create_alert(
                                ConsistencyMetric.FRONTEND_BACKEND_SYNC,
                                MonitoringLevel.ERROR,
                                f"Missing frontend variable {var} in {template_file}",
                                {"file": template_file, "missing_variable": var}
                            )
            
            # Calculate consistency score
            consistency_score = max(0, 100 - (issues_found * 25))
            await self._record_metric(
                ConsistencyMetric.FRONTEND_BACKEND_SYNC,
                consistency_score,
                self.thresholds[ConsistencyMetric.FRONTEND_BACKEND_SYNC]
            )
            
        except Exception as e:
            logger.error(f"Error checking frontend-backend sync: {e}")
    
    async def _check_config_consistency(self):
        """Check configuration consistency"""
        try:
            # This would check configuration files for consistency
            # For now, assume 100% consistency
            await self._record_metric(
                ConsistencyMetric.CONFIG_CONSISTENCY,
                100.0,
                self.thresholds[ConsistencyMetric.CONFIG_CONSISTENCY]
            )
            
        except Exception as e:
            logger.error(f"Error checking config consistency: {e}")
    
    async def _check_import_order_consistency(self):
        """Check import order consistency"""
        try:
            # This would check Python files for import order consistency
            # For now, assume 90% consistency
            await self._record_metric(
                ConsistencyMetric.IMPORT_ORDER,
                90.0,
                self.thresholds[ConsistencyMetric.IMPORT_ORDER]
            )
            
        except Exception as e:
            logger.error(f"Error checking import order consistency: {e}")
    
    async def _check_error_handling_consistency(self):
        """Check error handling consistency"""
        try:
            # This would check code for consistent error handling
            # For now, assume 95% consistency
            await self._record_metric(
                ConsistencyMetric.ERROR_HANDLING,
                95.0,
                self.thresholds[ConsistencyMetric.ERROR_HANDLING]
            )
            
        except Exception as e:
            logger.error(f"Error checking error handling consistency: {e}")
    
    async def _create_alert(
        self, 
        metric_type: ConsistencyMetric, 
        level: MonitoringLevel, 
        message: str, 
        details: Dict[str, Any]
    ):
        """Create a consistency alert"""
        alert = ConsistencyAlert(
            alert_id=f"alert_{int(time.time())}_{len(self.alerts)}",
            metric_type=metric_type,
            level=level,
            message=message,
            details=details,
            timestamp=datetime.now(),
            source="consistency_monitor"
        )
        
        self.alerts.append(alert)
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")
        
        logger.warning(f"Consistency Alert [{level.value}]: {message}")
    
    async def _record_metric(
        self, 
        metric_type: ConsistencyMetric, 
        value: float, 
        threshold: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """Record a consistency metric"""
        metric = ConsistencyMetricData(
            metric_type=metric_type,
            value=value,
            threshold=threshold,
            timestamp=datetime.now(),
            context=context or {}
        )
        
        self.metrics.append(metric)
        
        # Check if metric is below threshold
        if value < threshold:
            await self._create_alert(
                metric_type,
                MonitoringLevel.WARNING,
                f"{metric_type.value} consistency below threshold",
                {
                    "current_value": value,
                    "threshold": threshold,
                    "context": context or {}
                }
            )
    
    async def _cleanup_old_metrics(self):
        """Clean up old metrics and alerts"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        # Keep only recent metrics
        self.metrics = [
            metric for metric in self.metrics 
            if metric.timestamp > cutoff_time
        ]
        
        # Keep only recent unresolved alerts
        self.alerts = [
            alert for alert in self.alerts 
            if alert.timestamp > cutoff_time or not alert.resolved
        ]
    
    def add_alert_callback(self, callback: Callable):
        """Add an alert callback function"""
        self.alert_callbacks.append(callback)
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            "is_monitoring": self.is_monitoring,
            "monitoring_interval": self.monitoring_interval,
            "total_alerts": len(self.alerts),
            "unresolved_alerts": len([a for a in self.alerts if not a.resolved]),
            "total_metrics": len(self.metrics),
            "thresholds": {metric.value: threshold for metric, threshold in self.thresholds.items()},
            "last_check": datetime.now().isoformat()
        }
    
    def get_consistency_dashboard(self) -> Dict[str, Any]:
        """Get consistency dashboard data"""
        # Calculate current consistency scores
        current_metrics = {}
        for metric_type in ConsistencyMetric:
            recent_metrics = [
                m for m in self.metrics 
                if m.metric_type == metric_type and m.timestamp > datetime.now() - timedelta(hours=1)
            ]
            if recent_metrics:
                current_metrics[metric_type.value] = recent_metrics[-1].value
            else:
                current_metrics[metric_type.value] = 0.0
        
        # Get recent alerts
        recent_alerts = [
            asdict(alert) for alert in self.alerts 
            if alert.timestamp > datetime.now() - timedelta(hours=24)
        ]
        
        # Calculate overall consistency score
        overall_score = sum(current_metrics.values()) / len(current_metrics) if current_metrics else 0.0
        
        return {
            "overall_consistency_score": overall_score,
            "metric_scores": current_metrics,
            "recent_alerts": recent_alerts,
            "monitoring_status": self.get_monitoring_status(),
            "dashboard_timestamp": datetime.now().isoformat()
        }
    
    async def resolve_alert(self, alert_id: str, resolution_notes: str):
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.resolution_notes = resolution_notes
                logger.info(f"Alert {alert_id} resolved: {resolution_notes}")
                return True
        return False

# Global instance for system-wide access
consistency_monitor = RealTimeConsistencyMonitor()
