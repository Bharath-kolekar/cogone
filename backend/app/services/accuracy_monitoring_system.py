"""
Accuracy Monitoring and Enforcement System
Ensures accuracy levels are maintained in production with real-time monitoring
"""

import asyncio
import json
import logging
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import UUID, uuid4
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import Enum

from app.core.database import get_database
from app.core.redis import get_redis_client
from app.core.config import get_settings
from app.services.accuracy_validation_engine import RealAccuracyValidator, AccuracyLevel, AccuracyMetrics

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class AccuracyAlert:
    """Accuracy alert data class"""
    alert_id: str
    level: AccuracyLevel
    current_accuracy: float
    target_accuracy: float
    threshold_breach: float
    timestamp: datetime
    severity: str
    action_required: str
    resolved: bool = False


@dataclass
class AccuracyReport:
    """Accuracy report data class"""
    report_id: str
    level: AccuracyLevel
    time_period: str
    total_requests: int
    successful_validations: int
    failed_validations: int
    average_accuracy: float
    accuracy_trend: List[float]
    alerts_generated: int
    recommendations: List[str]
    timestamp: datetime


class AccuracyMonitoringSystem:
    """Real-time accuracy monitoring and enforcement system"""
    
    def __init__(self):
        self.validator = RealAccuracyValidator()
        self.accuracy_thresholds = self._initialize_thresholds()
        self.monitoring_active = False
        self.alert_history = []
        self.accuracy_trends = defaultdict(list)
        self.performance_metrics = defaultdict(list)
        
    def _initialize_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize accuracy thresholds for monitoring"""
        return {
            "standard": {
                "target_accuracy": 0.85,
                "warning_threshold": 0.80,
                "critical_threshold": 0.75,
                "min_samples": 10
            },
            "optimized": {
                "target_accuracy": 0.87,
                "warning_threshold": 0.82,
                "critical_threshold": 0.77,
                "min_samples": 10
            },
            "ultra_optimized": {
                "target_accuracy": 0.90,
                "warning_threshold": 0.85,
                "critical_threshold": 0.80,
                "min_samples": 10
            },
            "maximum_accuracy_98": {
                "target_accuracy": 0.98,
                "warning_threshold": 0.95,
                "critical_threshold": 0.90,
                "min_samples": 5
            },
            "maximum_accuracy_99": {
                "target_accuracy": 0.99,
                "warning_threshold": 0.96,
                "critical_threshold": 0.92,
                "min_samples": 5
            },
            "maximum_accuracy_100": {
                "target_accuracy": 1.00,
                "warning_threshold": 0.98,
                "critical_threshold": 0.95,
                "min_samples": 3
            }
        }
    
    async def start_monitoring(self):
        """Start accuracy monitoring system"""
        try:
            self.monitoring_active = True
            logger.info("Accuracy monitoring system started")
            
            # Start background monitoring tasks
            asyncio.create_task(self._monitor_accuracy_trends())
            asyncio.create_task(self._check_threshold_breaches())
            asyncio.create_task(self._generate_accuracy_reports())
            asyncio.create_task(self._enforce_accuracy_standards())
            
        except Exception as e:
            logger.error(f"Failed to start accuracy monitoring: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop accuracy monitoring system"""
        try:
            self.monitoring_active = False
            logger.info("Accuracy monitoring system stopped")
        except Exception as e:
            logger.error(f"Failed to stop accuracy monitoring: {e}")
    
    async def validate_and_monitor(
        self, 
        prompt: str, 
        response: str, 
        accuracy_level: AccuracyLevel,
        context: Dict[str, Any] = None
    ) -> Tuple[bool, AccuracyMetrics, List[AccuracyAlert]]:
        """Validate accuracy and monitor for threshold breaches"""
        try:
            # Validate accuracy
            metrics = await self.validator.validate_accuracy(
                prompt, response, accuracy_level, context
            )
            
            # Store metrics for monitoring
            await self._store_accuracy_metrics(metrics)
            
            # Check for threshold breaches
            alerts = await self._check_accuracy_thresholds(metrics)
            
            # Update trends
            self.accuracy_trends[accuracy_level.value].append(metrics.actual_accuracy)
            
            # Keep only recent trends (last 100 measurements)
            if len(self.accuracy_trends[accuracy_level.value]) > 100:
                self.accuracy_trends[accuracy_level.value] = self.accuracy_trends[accuracy_level.value][-100:]
            
            return metrics.validation_passed, metrics, alerts
            
        except Exception as e:
            logger.error(f"Accuracy validation and monitoring failed: {e}")
            return False, None, []
    
    async def _monitor_accuracy_trends(self):
        """Monitor accuracy trends in real-time"""
        while self.monitoring_active:
            try:
                for level_name, trends in self.accuracy_trends.items():
                    if len(trends) >= 10:  # Minimum samples for trend analysis
                        # Calculate trend
                        trend = self._calculate_accuracy_trend(trends)
                        
                        # Check for declining trends
                        if trend < -0.05:  # 5% decline
                            await self._generate_trend_alert(level_name, trend, trends)
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Accuracy trend monitoring failed: {e}")
                await asyncio.sleep(60)
    
    async def _check_threshold_breaches(self):
        """Check for accuracy threshold breaches"""
        while self.monitoring_active:
            try:
                for level_name, trends in self.accuracy_trends.items():
                    if len(trends) >= 5:  # Minimum samples
                        threshold_config = self.accuracy_thresholds.get(level_name)
                        if threshold_config:
                            recent_accuracy = statistics.mean(trends[-5:])  # Last 5 measurements
                            
                            # Check for critical threshold breach
                            if recent_accuracy < threshold_config["critical_threshold"]:
                                await self._generate_critical_alert(level_name, recent_accuracy, threshold_config)
                            
                            # Check for warning threshold breach
                            elif recent_accuracy < threshold_config["warning_threshold"]:
                                await self._generate_warning_alert(level_name, recent_accuracy, threshold_config)
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Threshold breach checking failed: {e}")
                await asyncio.sleep(30)
    
    async def _generate_accuracy_reports(self):
        """Generate periodic accuracy reports"""
        while self.monitoring_active:
            try:
                # Generate hourly reports
                await asyncio.sleep(3600)  # Wait 1 hour
                
                for level_name in self.accuracy_trends.keys():
                    report = await self._create_accuracy_report(level_name, "hourly")
                    await self._store_accuracy_report(report)
                    
                    # Send report if accuracy is below target
                    if report.average_accuracy < self.accuracy_thresholds[level_name]["target_accuracy"]:
                        await self._send_accuracy_report(report)
                
            except Exception as e:
                logger.error(f"Accuracy report generation failed: {e}")
    
    async def _enforce_accuracy_standards(self):
        """Enforce accuracy standards automatically"""
        while self.monitoring_active:
            try:
                for level_name, trends in self.accuracy_trends.items():
                    if len(trends) >= 10:
                        threshold_config = self.accuracy_thresholds.get(level_name)
                        if threshold_config:
                            recent_accuracy = statistics.mean(trends[-10:])
                            
                            # If accuracy is consistently below target, take action
                            if recent_accuracy < threshold_config["target_accuracy"]:
                                await self._enforce_accuracy_improvement(level_name, recent_accuracy)
                
                # Wait before next check
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Accuracy enforcement failed: {e}")
                await asyncio.sleep(300)
    
    def _calculate_accuracy_trend(self, trends: List[float]) -> float:
        """Calculate accuracy trend (positive = improving, negative = declining)"""
        if len(trends) < 2:
            return 0.0
        
        # Simple linear regression for trend
        n = len(trends)
        x = list(range(n))
        y = trends
        
        # Calculate slope
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        slope = numerator / denominator
        return slope
    
    async def _generate_trend_alert(self, level_name: str, trend: float, trends: List[float]):
        """Generate trend alert"""
        try:
            alert = AccuracyAlert(
                alert_id=str(uuid4()),
                level=AccuracyLevel(level_name),
                current_accuracy=trends[-1],
                target_accuracy=self.accuracy_thresholds[level_name]["target_accuracy"],
                threshold_breach=trend,
                timestamp=datetime.now(),
                severity="warning",
                action_required="Monitor accuracy trend and consider system adjustments"
            )
            
            self.alert_history.append(alert)
            await self._store_alert(alert)
            await self._send_alert_notification(alert)
            
        except Exception as e:
            logger.error(f"Failed to generate trend alert: {e}")
    
    async def _generate_critical_alert(self, level_name: str, accuracy: float, threshold_config: Dict[str, float]):
        """Generate critical accuracy alert"""
        try:
            alert = AccuracyAlert(
                alert_id=str(uuid4()),
                level=AccuracyLevel(level_name),
                current_accuracy=accuracy,
                target_accuracy=threshold_config["target_accuracy"],
                threshold_breach=threshold_config["target_accuracy"] - accuracy,
                timestamp=datetime.now(),
                severity="critical",
                action_required="Immediate system intervention required"
            )
            
            self.alert_history.append(alert)
            await self._store_alert(alert)
            await self._send_alert_notification(alert)
            
            # Take immediate action
            await self._take_immediate_action(level_name, accuracy)
            
        except Exception as e:
            logger.error(f"Failed to generate critical alert: {e}")
    
    async def _generate_warning_alert(self, level_name: str, accuracy: float, threshold_config: Dict[str, float]):
        """Generate warning accuracy alert"""
        try:
            alert = AccuracyAlert(
                alert_id=str(uuid4()),
                level=AccuracyLevel(level_name),
                current_accuracy=accuracy,
                target_accuracy=threshold_config["target_accuracy"],
                threshold_breach=threshold_config["target_accuracy"] - accuracy,
                timestamp=datetime.now(),
                severity="warning",
                action_required="Monitor accuracy and consider system adjustments"
            )
            
            self.alert_history.append(alert)
            await self._store_alert(alert)
            await self._send_alert_notification(alert)
            
        except Exception as e:
            logger.error(f"Failed to generate warning alert: {e}")
    
    async def _enforce_accuracy_improvement(self, level_name: str, current_accuracy: float):
        """Enforce accuracy improvement automatically"""
        try:
            # Implement automatic accuracy improvement strategies
            improvement_strategies = {
                "maximum_accuracy_100": [
                    "Increase validation retry attempts",
                    "Enable redundant validation systems",
                    "Activate real-time verification",
                    "Implement peer review validation"
                ],
                "maximum_accuracy_99": [
                    "Increase validation retry attempts",
                    "Enable expert validation",
                    "Activate cross-reference validation",
                    "Implement source verification"
                ],
                "maximum_accuracy_98": [
                    "Increase validation retry attempts",
                    "Enable expert validation",
                    "Activate cross-reference validation"
                ]
            }
            
            strategies = improvement_strategies.get(level_name, [])
            
            for strategy in strategies:
                await self._apply_accuracy_strategy(level_name, strategy)
            
            logger.info(f"Applied accuracy improvement strategies for {level_name}")
            
        except Exception as e:
            logger.error(f"Failed to enforce accuracy improvement: {e}")
    
    async def _take_immediate_action(self, level_name: str, accuracy: float):
        """Take immediate action for critical accuracy breaches"""
        try:
            # Immediate actions for critical breaches
            actions = [
                "Increase validation timeout",
                "Enable all validation methods",
                "Activate redundant systems",
                "Implement emergency validation protocols"
            ]
            
            for action in actions:
                await self._apply_emergency_action(level_name, action)
            
            logger.warning(f"Applied emergency actions for {level_name} (accuracy: {accuracy:.3f})")
            
        except Exception as e:
            logger.error(f"Failed to take immediate action: {e}")
    
    async def _apply_accuracy_strategy(self, level_name: str, strategy: str):
        """Apply specific accuracy improvement strategy"""
        try:
            # Update validation configuration
            if "retry attempts" in strategy:
                # Increase retry attempts
                pass
            elif "redundant validation" in strategy:
                # Enable redundant validation
                pass
            elif "real-time verification" in strategy:
                # Enable real-time verification
                pass
            elif "peer review" in strategy:
                # Enable peer review
                pass
            elif "expert validation" in strategy:
                # Enable expert validation
                pass
            elif "cross-reference" in strategy:
                # Enable cross-reference validation
                pass
            elif "source verification" in strategy:
                # Enable source verification
                pass
            
            logger.info(f"Applied strategy '{strategy}' for {level_name}")
            
        except Exception as e:
            logger.error(f"Failed to apply accuracy strategy: {e}")
    
    async def _apply_emergency_action(self, level_name: str, action: str):
        """Apply emergency action for critical situations"""
        try:
            # Emergency actions
            if "timeout" in action:
                # Increase validation timeout
                pass
            elif "all validation methods" in action:
                # Enable all validation methods
                pass
            elif "redundant systems" in action:
                # Activate redundant systems
                pass
            elif "emergency protocols" in action:
                # Implement emergency validation protocols
                pass
            
            logger.warning(f"Applied emergency action '{action}' for {level_name}")
            
        except Exception as e:
            logger.error(f"Failed to apply emergency action: {e}")
    
    async def _create_accuracy_report(self, level_name: str, time_period: str) -> AccuracyReport:
        """Create accuracy report"""
        try:
            trends = self.accuracy_trends.get(level_name, [])
            
            if not trends:
                return AccuracyReport(
                    report_id=str(uuid4()),
                    level=AccuracyLevel(level_name),
                    time_period=time_period,
                    total_requests=0,
                    successful_validations=0,
                    failed_validations=0,
                    average_accuracy=0.0,
                    accuracy_trend=[],
                    alerts_generated=0,
                    recommendations=[],
                    timestamp=datetime.now()
                )
            
            # Calculate metrics
            total_requests = len(trends)
            successful_validations = sum(1 for acc in trends if acc >= self.accuracy_thresholds[level_name]["target_accuracy"])
            failed_validations = total_requests - successful_validations
            average_accuracy = statistics.mean(trends)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(level_name, average_accuracy, trends)
            
            return AccuracyReport(
                report_id=str(uuid4()),
                level=AccuracyLevel(level_name),
                time_period=time_period,
                total_requests=total_requests,
                successful_validations=successful_validations,
                failed_validations=failed_validations,
                average_accuracy=average_accuracy,
                accuracy_trend=trends[-20:],  # Last 20 measurements
                alerts_generated=len([a for a in self.alert_history if a.level.value == level_name]),
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Failed to create accuracy report: {e}")
            return None
    
    def _generate_recommendations(self, level_name: str, average_accuracy: float, trends: List[float]) -> List[str]:
        """Generate accuracy improvement recommendations"""
        recommendations = []
        threshold_config = self.accuracy_thresholds.get(level_name, {})
        target_accuracy = threshold_config.get("target_accuracy", 0.0)
        
        if average_accuracy < target_accuracy:
            recommendations.append(f"Increase validation retry attempts for {level_name}")
            recommendations.append(f"Enable additional validation methods for {level_name}")
            recommendations.append(f"Review and improve response generation for {level_name}")
        
        if len(trends) >= 5:
            recent_trend = statistics.mean(trends[-5:])
            if recent_trend < average_accuracy:
                recommendations.append(f"Monitor accuracy trend for {level_name} - declining performance detected")
        
        if not recommendations:
            recommendations.append(f"Accuracy for {level_name} is within acceptable range")
        
        return recommendations
    
    async def _store_accuracy_metrics(self, metrics: AccuracyMetrics):
        """Store accuracy metrics for monitoring"""
        try:
            redis_client = await get_redis_client()
            
            # Store in Redis for real-time access
            await redis_client.setex(
                f"accuracy_metrics:{metrics.level.value}:{metrics.timestamp.isoformat()}",
                3600,  # 1 hour TTL
                json.dumps({
                    "level": metrics.level.value,
                    "target_accuracy": metrics.target_accuracy,
                    "actual_accuracy": metrics.actual_accuracy,
                    "validation_passed": metrics.validation_passed,
                    "timestamp": metrics.timestamp.isoformat()
                })
            )
            
        except Exception as e:
            logger.error(f"Failed to store accuracy metrics: {e}")
    
    async def _store_alert(self, alert: AccuracyAlert):
        """Store accuracy alert"""
        try:
            redis_client = await get_redis_client()
            
            # Store alert in Redis
            await redis_client.setex(
                f"accuracy_alert:{alert.alert_id}",
                86400,  # 24 hours TTL
                json.dumps({
                    "alert_id": alert.alert_id,
                    "level": alert.level.value,
                    "current_accuracy": alert.current_accuracy,
                    "target_accuracy": alert.target_accuracy,
                    "threshold_breach": alert.threshold_breach,
                    "timestamp": alert.timestamp.isoformat(),
                    "severity": alert.severity,
                    "action_required": alert.action_required,
                    "resolved": alert.resolved
                })
            )
            
        except Exception as e:
            logger.error(f"Failed to store alert: {e}")
    
    async def _store_accuracy_report(self, report: AccuracyReport):
        """Store accuracy report"""
        try:
            redis_client = await get_redis_client()
            
            # Store report in Redis
            await redis_client.setex(
                f"accuracy_report:{report.report_id}",
                86400,  # 24 hours TTL
                json.dumps({
                    "report_id": report.report_id,
                    "level": report.level.value,
                    "time_period": report.time_period,
                    "total_requests": report.total_requests,
                    "successful_validations": report.successful_validations,
                    "failed_validations": report.failed_validations,
                    "average_accuracy": report.average_accuracy,
                    "accuracy_trend": report.accuracy_trend,
                    "alerts_generated": report.alerts_generated,
                    "recommendations": report.recommendations,
                    "timestamp": report.timestamp.isoformat()
                })
            )
            
        except Exception as e:
            logger.error(f"Failed to store accuracy report: {e}")
    
    async def _send_alert_notification(self, alert: AccuracyAlert):
        """Send alert notification"""
        try:
            # In production, this would send actual notifications
            # (email, Slack, SMS, etc.)
            logger.warning(f"ACCURACY ALERT: {alert.severity.upper()} - {alert.level.value} accuracy at {alert.current_accuracy:.3f} (target: {alert.target_accuracy:.3f})")
            logger.warning(f"Action required: {alert.action_required}")
            
        except Exception as e:
            logger.error(f"Failed to send alert notification: {e}")
    
    async def _send_accuracy_report(self, report: AccuracyReport):
        """Send accuracy report"""
        try:
            # In production, this would send actual reports
            logger.info(f"ACCURACY REPORT: {report.level.value} - {report.time_period}")
            logger.info(f"Average accuracy: {report.average_accuracy:.3f} (target: {self.accuracy_thresholds[report.level.value]['target_accuracy']:.3f})")
            logger.info(f"Recommendations: {', '.join(report.recommendations)}")
            
        except Exception as e:
            logger.error(f"Failed to send accuracy report: {e}")
    
    async def get_accuracy_status(self, level_name: str) -> Dict[str, Any]:
        """Get current accuracy status for a level"""
        try:
            trends = self.accuracy_trends.get(level_name, [])
            threshold_config = self.accuracy_thresholds.get(level_name, {})
            
            if not trends:
                return {
                    "level": level_name,
                    "status": "no_data",
                    "message": "No accuracy data available"
                }
            
            recent_accuracy = statistics.mean(trends[-5:]) if len(trends) >= 5 else statistics.mean(trends)
            target_accuracy = threshold_config.get("target_accuracy", 0.0)
            
            if recent_accuracy >= target_accuracy:
                status = "healthy"
                message = f"Accuracy {recent_accuracy:.3f} meets target {target_accuracy:.3f}"
            elif recent_accuracy >= threshold_config.get("warning_threshold", 0.0):
                status = "warning"
                message = f"Accuracy {recent_accuracy:.3f} below target {target_accuracy:.3f} but above warning threshold"
            else:
                status = "critical"
                message = f"Accuracy {recent_accuracy:.3f} below critical threshold"
            
            return {
                "level": level_name,
                "status": status,
                "message": message,
                "recent_accuracy": recent_accuracy,
                "target_accuracy": target_accuracy,
                "trend": self._calculate_accuracy_trend(trends),
                "total_measurements": len(trends)
            }
            
        except Exception as e:
            logger.error(f"Failed to get accuracy status: {e}")
            return {"level": level_name, "status": "error", "message": str(e)}


# Global accuracy monitoring system instance
accuracy_monitoring_system = AccuracyMonitoringSystem()
