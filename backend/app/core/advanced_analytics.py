"""
Advanced Analytics System for Cognomega AI
Deep performance insights, trend analysis, and intelligent recommendations
"""

import asyncio
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import structlog
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import json
import math

from app.core.cpu_optimizer import cpu_optimizer
from app.core.performance_monitor import performance_monitor
from app.core.advanced_caching import advanced_cache
from app.core.ai_optimization_engine import ai_optimization_engine
from app.core.predictive_scaling import predictive_scaling_engine

logger = structlog.get_logger()


class InsightType(str, Enum):
    """Types of performance insights"""
    PERFORMANCE_BOTTLENECK = "performance_bottleneck"
    RESOURCE_UTILIZATION = "resource_utilization"
    TREND_ANALYSIS = "trend_analysis"
    ANOMALY_DETECTION = "anomaly_detection"
    OPTIMIZATION_OPPORTUNITY = "optimization_opportunity"
    CAPACITY_PLANNING = "capacity_planning"
    COST_OPTIMIZATION = "cost_optimization"
    USER_BEHAVIOR = "user_behavior"


class InsightSeverity(str, Enum):
    """Insight severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationType(str, Enum):
    """Types of recommendations"""
    IMMEDIATE_ACTION = "immediate_action"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    STRATEGIC = "strategic"


@dataclass
class PerformanceInsight:
    """Performance insight result"""
    insight_type: InsightType
    severity: InsightSeverity
    title: str
    description: str
    impact_score: float  # 0-100
    confidence: float  # 0-1
    metrics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    metric_name: str
    trend_direction: str  # increasing, decreasing, stable, cyclical
    trend_strength: float  # 0-1
    predicted_value: float
    confidence_interval: Tuple[float, float]
    time_horizon: int  # hours
    seasonal_pattern: Optional[Dict[str, Any]] = None


@dataclass
class AnomalyDetection:
    """Anomaly detection result"""
    anomaly_type: str
    severity: InsightSeverity
    affected_metrics: List[str]
    anomaly_score: float  # 0-1
    normal_range: Tuple[float, float]
    current_value: float
    explanation: str


@dataclass
class OptimizationOpportunity:
    """Optimization opportunity"""
    opportunity_type: str
    potential_improvement: float  # percentage
    effort_required: str  # low, medium, high
    cost_benefit_ratio: float
    implementation_complexity: str
    expected_impact: Dict[str, float]


class AdvancedAnalyticsEngine:
    """Advanced analytics engine for deep performance insights"""
    
    def __init__(self):
        self.performance_data: List[Dict[str, Any]] = []
        self.insights_history: List[PerformanceInsight] = []
        self.trend_models: Dict[str, Any] = {}
        self.anomaly_detectors: Dict[str, IsolationForest] = {}
        self.clustering_models: Dict[str, KMeans] = {}
        
        # Analytics configuration
        self.data_retention_hours = 168  # 7 days
        self.analysis_interval = 300  # 5 minutes
        self.trend_window_hours = 24
        self.anomaly_threshold = 0.1
        
        # Performance thresholds
        self.performance_thresholds = {
            "cpu_usage": {"warning": 70, "critical": 85},
            "memory_usage": {"warning": 75, "critical": 90},
            "response_time": {"warning": 500, "critical": 1000},
            "error_rate": {"warning": 5, "critical": 10},
            "cache_hit_rate": {"warning": 60, "critical": 40},
            "throughput": {"warning": 100, "critical": 50}
        }
        
        # Start background tasks
        self._start_background_tasks()
    
    def _start_background_tasks(self):
        """Start background analytics tasks"""
        asyncio.create_task(self._data_collection_loop())
        asyncio.create_task(self._analytics_processing_loop())
        asyncio.create_task(self._insight_generation_loop())
    
    async def _data_collection_loop(self):
        """Collect performance data continuously"""
        while True:
            try:
                await asyncio.sleep(30)  # Collect every 30 seconds
                await self._collect_performance_data()
                
            except Exception as e:
                logger.error("Data collection loop error", error=str(e))
                await asyncio.sleep(60)
    
    async def _analytics_processing_loop(self):
        """Process analytics continuously"""
        while True:
            try:
                await asyncio.sleep(self.analysis_interval)
                await self._process_analytics()
                
            except Exception as e:
                logger.error("Analytics processing loop error", error=str(e))
                await asyncio.sleep(300)
    
    async def _insight_generation_loop(self):
        """Generate insights continuously"""
        while True:
            try:
                await asyncio.sleep(600)  # Generate insights every 10 minutes
                await self._generate_insights()
                
            except Exception as e:
                logger.error("Insight generation loop error", error=str(e))
                await asyncio.sleep(300)
    
    async def _collect_performance_data(self):
        """Collect comprehensive performance data"""
        try:
            # Get data from all monitoring systems
            cache_stats = await advanced_cache.get_cache_metrics()
            cpu_metrics = await cpu_optimizer.get_cpu_metrics()
            performance_metrics = await performance_monitor.get_current_metrics()
            ai_metrics = await ai_optimization_engine.get_optimization_recommendations()
            scaling_metrics = await predictive_scaling_engine.get_scaling_recommendations()
            
            # Compile comprehensive data point
            data_point = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "usage": cpu_metrics.get("average_cpu_usage", 0),
                    "workers": cpu_metrics.get("current_workers", 0),
                    "max_workers": cpu_metrics.get("max_workers", 0),
                    "monitoring_active": cpu_metrics.get("monitoring_active", False)
                },
                "memory": {
                    "usage": cpu_metrics.get("memory_usage", 0),
                    "available": cpu_metrics.get("memory_available", 0)
                },
                "cache": {
                    "hit_rate": cache_stats.get("hit_rate", 0),
                    "total_requests": cache_stats.get("total_requests", 0),
                    "l1_size": cache_stats.get("l1_current_size", 0),
                    "l2_status": cache_stats.get("l2_status", "unknown")
                },
                "performance": {
                    "response_time": performance_metrics.get("response_time_ms", 0),
                    "throughput": performance_metrics.get("throughput", 0),
                    "error_rate": performance_metrics.get("error_rate", 0),
                    "active_users": performance_metrics.get("active_users", 0)
                },
                "ai_optimization": {
                    "recommendations_count": len(ai_metrics.get("recommendations", [])),
                    "model_accuracy": ai_metrics.get("model_accuracy", {}),
                    "training_samples": ai_metrics.get("training_samples", 0)
                },
                "predictive_scaling": {
                    "recommendations_count": len(scaling_metrics.get("recommendations", [])),
                    "scaling_enabled": scaling_metrics.get("scaling_enabled", False),
                    "cooldown_remaining": scaling_metrics.get("cooldown_remaining", 0)
                }
            }
            
            self.performance_data.append(data_point)
            
            # Clean old data
            cutoff_time = datetime.now() - timedelta(hours=self.data_retention_hours)
            self.performance_data = [
                dp for dp in self.performance_data 
                if datetime.fromisoformat(dp["timestamp"]) > cutoff_time
            ]
            
        except Exception as e:
            logger.error("Performance data collection error", error=str(e))
    
    async def _process_analytics(self):
        """Process collected data for analytics"""
        try:
            if len(self.performance_data) < 10:
                return
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(self.performance_data)
            
            # Extract metrics for analysis
            metrics_df = pd.DataFrame([
                {
                    'timestamp': pd.to_datetime(dp['timestamp']),
                    'cpu_usage': dp['cpu']['usage'],
                    'memory_usage': dp['memory']['usage'],
                    'cache_hit_rate': dp['cache']['hit_rate'],
                    'response_time': dp['performance']['response_time'],
                    'throughput': dp['performance']['throughput'],
                    'error_rate': dp['performance']['error_rate'],
                    'active_users': dp['performance']['active_users']
                }
                for dp in self.performance_data
            ])
            
            # Train anomaly detectors
            await self._train_anomaly_detectors(metrics_df)
            
            # Train clustering models
            await self._train_clustering_models(metrics_df)
            
            # Update trend models
            await self._update_trend_models(metrics_df)
            
        except Exception as e:
            logger.error("Analytics processing error", error=str(e))
    
    async def _train_anomaly_detectors(self, df: pd.DataFrame):
        """Train anomaly detection models"""
        try:
            metric_columns = ['cpu_usage', 'memory_usage', 'cache_hit_rate', 
                            'response_time', 'throughput', 'error_rate']
            
            for metric in metric_columns:
                if metric in df.columns:
                    values = df[metric].values.reshape(-1, 1)
                    
                    # Train isolation forest for anomaly detection
                    detector = IsolationForest(
                        contamination=self.anomaly_threshold,
                        random_state=42
                    )
                    detector.fit(values)
                    
                    self.anomaly_detectors[metric] = detector
            
        except Exception as e:
            logger.error("Anomaly detector training error", error=str(e))
    
    async def _train_clustering_models(self, df: pd.DataFrame):
        """Train clustering models for pattern recognition"""
        try:
            metric_columns = ['cpu_usage', 'memory_usage', 'cache_hit_rate', 
                            'response_time', 'throughput', 'error_rate']
            
            # Prepare data for clustering
            clustering_data = df[metric_columns].fillna(0)
            
            # Normalize data
            scaler = StandardScaler()
            normalized_data = scaler.fit_transform(clustering_data)
            
            # Train K-means clustering
            for n_clusters in [3, 5, 7]:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                kmeans.fit(normalized_data)
                
                # Calculate silhouette score
                silhouette_avg = silhouette_score(normalized_data, kmeans.labels_)
                
                if silhouette_avg > 0.3:  # Good clustering
                    self.clustering_models[f"kmeans_{n_clusters}"] = kmeans
            
        except Exception as e:
            logger.error("Clustering model training error", error=str(e))
    
    async def _update_trend_models(self, df: pd.DataFrame):
        """Update trend analysis models"""
        try:
            metric_columns = ['cpu_usage', 'memory_usage', 'cache_hit_rate', 
                            'response_time', 'throughput', 'error_rate']
            
            for metric in metric_columns:
                if metric in df.columns:
                    values = df[metric].values
                    
                    # Simple trend analysis using linear regression
                    x = np.arange(len(values))
                    coeffs = np.polyfit(x, values, 1)
                    trend_slope = coeffs[0]
                    
                    # Calculate trend strength
                    trend_strength = abs(trend_slope) / np.std(values) if np.std(values) > 0 else 0
                    
                    self.trend_models[metric] = {
                        "slope": trend_slope,
                        "strength": min(1.0, trend_strength),
                        "direction": "increasing" if trend_slope > 0 else "decreasing" if trend_slope < 0 else "stable",
                        "last_updated": datetime.now()
                    }
            
        except Exception as e:
            logger.error("Trend model update error", error=str(e))
    
    async def _generate_insights(self):
        """Generate performance insights"""
        try:
            if len(self.performance_data) < 5:
                return
            
            insights = []
            
            # Get latest data
            latest_data = self.performance_data[-1]
            
            # Generate performance bottleneck insights
            bottleneck_insights = await self._analyze_performance_bottlenecks(latest_data)
            insights.extend(bottleneck_insights)
            
            # Generate resource utilization insights
            resource_insights = await self._analyze_resource_utilization(latest_data)
            insights.extend(resource_insights)
            
            # Generate trend analysis insights
            trend_insights = await self._analyze_trends()
            insights.extend(trend_insights)
            
            # Generate anomaly detection insights
            anomaly_insights = await self._detect_anomalies(latest_data)
            insights.extend(anomaly_insights)
            
            # Generate optimization opportunities
            optimization_insights = await self._identify_optimization_opportunities(latest_data)
            insights.extend(optimization_insights)
            
            # Store insights
            self.insights_history.extend(insights)
            
            # Keep only recent insights
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.insights_history = [
                insight for insight in self.insights_history 
                if insight.timestamp > cutoff_time
            ]
            
            logger.info("Generated performance insights", count=len(insights))
            
        except Exception as e:
            logger.error("Insight generation error", error=str(e))
    
    async def _analyze_performance_bottlenecks(self, data: Dict[str, Any]) -> List[PerformanceInsight]:
        """Analyze performance bottlenecks"""
        insights = []
        
        try:
            # CPU bottleneck analysis
            cpu_usage = data["cpu"]["usage"]
            if cpu_usage > self.performance_thresholds["cpu_usage"]["critical"]:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.PERFORMANCE_BOTTLENECK,
                    severity=InsightSeverity.CRITICAL,
                    title="Critical CPU Bottleneck",
                    description=f"CPU usage is critically high at {cpu_usage:.1f}%, causing performance degradation",
                    impact_score=95,
                    confidence=0.95,
                    metrics={"cpu_usage": cpu_usage},
                    recommendations=[
                        "Scale up CPU resources immediately",
                        "Optimize CPU-intensive operations",
                        "Implement CPU load balancing"
                    ]
                ))
            elif cpu_usage > self.performance_thresholds["cpu_usage"]["warning"]:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.PERFORMANCE_BOTTLENECK,
                    severity=InsightSeverity.HIGH,
                    title="High CPU Usage",
                    description=f"CPU usage is high at {cpu_usage:.1f}%, monitor for potential bottlenecks",
                    impact_score=75,
                    confidence=0.8,
                    metrics={"cpu_usage": cpu_usage},
                    recommendations=[
                        "Monitor CPU usage trends",
                        "Consider proactive scaling",
                        "Optimize resource allocation"
                    ]
                ))
            
            # Memory bottleneck analysis
            memory_usage = data["memory"]["usage"]
            if memory_usage > self.performance_thresholds["memory_usage"]["critical"]:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.PERFORMANCE_BOTTLENECK,
                    severity=InsightSeverity.CRITICAL,
                    title="Critical Memory Bottleneck",
                    description=f"Memory usage is critically high at {memory_usage:.1f}%, risking system stability",
                    impact_score=90,
                    confidence=0.9,
                    metrics={"memory_usage": memory_usage},
                    recommendations=[
                        "Increase memory allocation immediately",
                        "Identify memory leaks",
                        "Implement memory optimization"
                    ]
                ))
            
            # Response time bottleneck analysis
            response_time = data["performance"]["response_time"]
            if response_time > self.performance_thresholds["response_time"]["critical"]:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.PERFORMANCE_BOTTLENECK,
                    severity=InsightSeverity.CRITICAL,
                    title="Critical Response Time",
                    description=f"Response time is critically high at {response_time:.1f}ms, severely impacting user experience",
                    impact_score=98,
                    confidence=0.95,
                    metrics={"response_time": response_time},
                    recommendations=[
                        "Optimize database queries",
                        "Implement response caching",
                        "Scale up application servers"
                    ]
                ))
            
            # Cache performance analysis
            cache_hit_rate = data["cache"]["hit_rate"]
            if cache_hit_rate < self.performance_thresholds["cache_hit_rate"]["critical"]:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.PERFORMANCE_BOTTLENECK,
                    severity=InsightSeverity.HIGH,
                    title="Low Cache Hit Rate",
                    description=f"Cache hit rate is low at {cache_hit_rate:.1f}%, causing unnecessary database load",
                    impact_score=70,
                    confidence=0.85,
                    metrics={"cache_hit_rate": cache_hit_rate},
                    recommendations=[
                        "Optimize cache strategies",
                        "Implement cache warming",
                        "Review cache eviction policies"
                    ]
                ))
            
        except Exception as e:
            logger.error("Performance bottleneck analysis error", error=str(e))
        
        return insights
    
    async def _analyze_resource_utilization(self, data: Dict[str, Any]) -> List[PerformanceInsight]:
        """Analyze resource utilization patterns"""
        insights = []
        
        try:
            # CPU utilization analysis
            cpu_usage = data["cpu"]["usage"]
            cpu_workers = data["cpu"]["workers"]
            max_workers = data["cpu"]["max_workers"]
            
            utilization_ratio = cpu_workers / max_workers if max_workers > 0 else 0
            
            if utilization_ratio > 0.9:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.RESOURCE_UTILIZATION,
                    severity=InsightSeverity.HIGH,
                    title="High CPU Resource Utilization",
                    description=f"CPU resources are {utilization_ratio:.1%} utilized ({cpu_workers}/{max_workers} workers)",
                    impact_score=80,
                    confidence=0.9,
                    metrics={
                        "utilization_ratio": utilization_ratio,
                        "active_workers": cpu_workers,
                        "max_workers": max_workers
                    },
                    recommendations=[
                        "Consider scaling up CPU resources",
                        "Optimize thread pool management",
                        "Implement intelligent load distribution"
                    ]
                ))
            
            # Memory utilization analysis
            memory_usage = data["memory"]["usage"]
            memory_available = data["memory"]["available"]
            
            if memory_usage > 80 and memory_available < 1000:  # Less than 1GB available
                insights.append(PerformanceInsight(
                    insight_type=InsightType.RESOURCE_UTILIZATION,
                    severity=InsightSeverity.MEDIUM,
                    title="High Memory Utilization",
                    description=f"Memory usage is {memory_usage:.1f}% with only {memory_available}MB available",
                    impact_score=65,
                    confidence=0.8,
                    metrics={
                        "memory_usage": memory_usage,
                        "memory_available": memory_available
                    },
                    recommendations=[
                        "Monitor memory usage trends",
                        "Implement memory cleanup routines",
                        "Consider memory optimization"
                    ]
                ))
            
        except Exception as e:
            logger.error("Resource utilization analysis error", error=str(e))
        
        return insights
    
    async def _analyze_trends(self) -> List[PerformanceInsight]:
        """Analyze performance trends"""
        insights = []
        
        try:
            for metric, trend_data in self.trend_models.items():
                trend_strength = trend_data["strength"]
                trend_direction = trend_data["direction"]
                
                if trend_strength > 0.5:  # Strong trend
                    severity = InsightSeverity.HIGH if trend_strength > 0.8 else InsightSeverity.MEDIUM
                    
                    if trend_direction == "increasing":
                        if metric in ["cpu_usage", "memory_usage", "response_time", "error_rate"]:
                            insights.append(PerformanceInsight(
                                insight_type=InsightType.TREND_ANALYSIS,
                                severity=severity,
                                title=f"Worrying {metric.replace('_', ' ').title()} Trend",
                                description=f"{metric.replace('_', ' ').title()} is trending upward with {trend_strength:.1%} strength",
                                impact_score=int(trend_strength * 100),
                                confidence=trend_strength,
                                metrics={"trend_strength": trend_strength, "trend_direction": trend_direction},
                                recommendations=[
                                    "Monitor trend closely",
                                    "Consider proactive optimization",
                                    "Plan for capacity scaling"
                                ]
                            ))
                    elif trend_direction == "decreasing":
                        if metric in ["cache_hit_rate", "throughput"]:
                            insights.append(PerformanceInsight(
                                insight_type=InsightType.TREND_ANALYSIS,
                                severity=severity,
                                title=f"Concerning {metric.replace('_', ' ').title()} Trend",
                                description=f"{metric.replace('_', ' ').title()} is trending downward with {trend_strength:.1%} strength",
                                impact_score=int(trend_strength * 100),
                                confidence=trend_strength,
                                metrics={"trend_strength": trend_strength, "trend_direction": trend_direction},
                                recommendations=[
                                    "Investigate performance degradation",
                                    "Implement corrective measures",
                                    "Review optimization strategies"
                                ]
                            ))
            
        except Exception as e:
            logger.error("Trend analysis error", error=str(e))
        
        return insights
    
    async def _detect_anomalies(self, data: Dict[str, Any]) -> List[PerformanceInsight]:
        """Detect performance anomalies"""
        insights = []
        
        try:
            metric_mapping = {
                "cpu_usage": data["cpu"]["usage"],
                "memory_usage": data["memory"]["usage"],
                "cache_hit_rate": data["cache"]["hit_rate"],
                "response_time": data["performance"]["response_time"],
                "throughput": data["performance"]["throughput"],
                "error_rate": data["performance"]["error_rate"]
            }
            
            for metric, detector in self.anomaly_detectors.items():
                if metric in metric_mapping:
                    value = metric_mapping[metric]
                    anomaly_score = detector.decision_function([[value]])[0]
                    is_anomaly = detector.predict([[value]])[0] == -1
                    
                    if is_anomaly:
                        severity = InsightSeverity.CRITICAL if abs(anomaly_score) > 2 else InsightSeverity.HIGH
                        
                        insights.append(PerformanceInsight(
                            insight_type=InsightType.ANOMALY_DETECTION,
                            severity=severity,
                            title=f"Anomaly Detected in {metric.replace('_', ' ').title()}",
                            description=f"Unusual {metric.replace('_', ' ')} detected with value {value:.2f} (anomaly score: {anomaly_score:.2f})",
                            impact_score=min(100, abs(anomaly_score) * 25),
                            confidence=min(0.95, abs(anomaly_score) / 3),
                            metrics={
                                "anomaly_score": anomaly_score,
                                "current_value": value,
                                "metric": metric
                            },
                            recommendations=[
                                "Investigate root cause immediately",
                                "Monitor for similar anomalies",
                                "Review recent system changes"
                            ]
                        ))
            
        except Exception as e:
            logger.error("Anomaly detection error", error=str(e))
        
        return insights
    
    async def _identify_optimization_opportunities(self, data: Dict[str, Any]) -> List[PerformanceInsight]:
        """Identify optimization opportunities"""
        insights = []
        
        try:
            # Cache optimization opportunity
            cache_hit_rate = data["cache"]["hit_rate"]
            if 60 <= cache_hit_rate < 80:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.OPTIMIZATION_OPPORTUNITY,
                    severity=InsightSeverity.MEDIUM,
                    title="Cache Optimization Opportunity",
                    description=f"Cache hit rate is {cache_hit_rate:.1f}%, there's room for improvement",
                    impact_score=60,
                    confidence=0.75,
                    metrics={"cache_hit_rate": cache_hit_rate},
                    recommendations=[
                        "Implement cache warming strategies",
                        "Optimize cache key patterns",
                        "Review cache eviction policies"
                    ]
                ))
            
            # CPU optimization opportunity
            cpu_usage = data["cpu"]["usage"]
            if 50 <= cpu_usage < 70:
                insights.append(PerformanceInsight(
                    insight_type=InsightType.OPTIMIZATION_OPPORTUNITY,
                    severity=InsightSeverity.LOW,
                    title="CPU Optimization Opportunity",
                    description=f"CPU usage is {cpu_usage:.1f}%, consider proactive optimization",
                    impact_score=40,
                    confidence=0.7,
                    metrics={"cpu_usage": cpu_usage},
                    recommendations=[
                        "Implement CPU optimization algorithms",
                        "Review thread pool configurations",
                        "Consider predictive scaling"
                    ]
                ))
            
            # Throughput optimization opportunity
            throughput = data["performance"]["throughput"]
            if throughput > 0:
                # Compare with historical average (simplified)
                historical_avg = np.mean([dp["performance"]["throughput"] for dp in self.performance_data[-10:]])
                if throughput < historical_avg * 0.8:
                    insights.append(PerformanceInsight(
                        insight_type=InsightType.OPTIMIZATION_OPPORTUNITY,
                        severity=InsightSeverity.MEDIUM,
                        title="Throughput Optimization Opportunity",
                        description=f"Current throughput ({throughput:.1f}) is below recent average ({historical_avg:.1f})",
                        impact_score=55,
                        confidence=0.8,
                        metrics={"current_throughput": throughput, "historical_average": historical_avg},
                        recommendations=[
                            "Optimize application performance",
                            "Review resource allocation",
                            "Implement throughput monitoring"
                        ]
                    ))
            
        except Exception as e:
            logger.error("Optimization opportunity identification error", error=str(e))
        
        return insights
    
    async def get_comprehensive_analytics(self) -> Dict[str, Any]:
        """Get comprehensive analytics report"""
        try:
            # Get recent insights
            recent_insights = [
                insight for insight in self.insights_history 
                if insight.timestamp > datetime.now() - timedelta(hours=6)
            ]
            
            # Categorize insights
            insights_by_type = {}
            insights_by_severity = {}
            
            for insight in recent_insights:
                # By type
                if insight.insight_type not in insights_by_type:
                    insights_by_type[insight.insight_type] = []
                insights_by_type[insight.insight_type].append(insight)
                
                # By severity
                if insight.severity not in insights_by_severity:
                    insights_by_severity[insight.severity] = []
                insights_by_severity[insight.severity].append(insight)
            
            # Calculate system health score
            health_score = self._calculate_system_health_score(recent_insights)
            
            # Get performance summary
            performance_summary = await self._get_performance_summary()
            
            # Get optimization recommendations
            optimization_recommendations = await self._get_optimization_recommendations()
            
            return {
                "system_health_score": health_score,
                "insights_summary": {
                    "total_insights": len(recent_insights),
                    "by_type": {k.value: len(v) for k, v in insights_by_type.items()},
                    "by_severity": {k.value: len(v) for k, v in insights_by_severity.items()}
                },
                "performance_summary": performance_summary,
                "optimization_recommendations": optimization_recommendations,
                "trend_analysis": self.trend_models,
                "data_points_analyzed": len(self.performance_data),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Comprehensive analytics error", error=str(e))
            return {}
    
    def _calculate_system_health_score(self, insights: List[PerformanceInsight]) -> float:
        """Calculate overall system health score"""
        try:
            if not insights:
                return 100.0
            
            # Weight insights by severity
            severity_weights = {
                InsightSeverity.LOW: 0.1,
                InsightSeverity.MEDIUM: 0.3,
                InsightSeverity.HIGH: 0.6,
                InsightSeverity.CRITICAL: 1.0
            }
            
            total_impact = sum(
                insight.impact_score * severity_weights.get(insight.severity, 0.5)
                for insight in insights
            )
            
            # Normalize to 0-100 scale
            max_possible_impact = len(insights) * 100 * 1.0  # All critical insights
            health_score = max(0, 100 - (total_impact / max_possible_impact * 100))
            
            return round(health_score, 1)
            
        except Exception as e:
            logger.error("Health score calculation error", error=str(e))
            return 50.0
    
    async def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            if not self.performance_data:
                return {}
            
            latest_data = self.performance_data[-1]
            
            return {
                "cpu_usage": latest_data["cpu"]["usage"],
                "memory_usage": latest_data["memory"]["usage"],
                "cache_hit_rate": latest_data["cache"]["hit_rate"],
                "response_time": latest_data["performance"]["response_time"],
                "throughput": latest_data["performance"]["throughput"],
                "error_rate": latest_data["performance"]["error_rate"],
                "active_users": latest_data["performance"]["active_users"]
            }
            
        except Exception as e:
            logger.error("Performance summary error", error=str(e))
            return {}
    
    async def _get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get optimization recommendations"""
        try:
            recommendations = []
            
            # Get recent high-priority insights
            recent_critical_insights = [
                insight for insight in self.insights_history 
                if (insight.severity in [InsightSeverity.CRITICAL, InsightSeverity.HIGH] and
                    insight.timestamp > datetime.now() - timedelta(hours=2))
            ]
            
            for insight in recent_critical_insights:
                recommendations.append({
                    "priority": insight.severity.value,
                    "type": insight.insight_type.value,
                    "title": insight.title,
                    "description": insight.description,
                    "impact_score": insight.impact_score,
                    "confidence": insight.confidence,
                    "recommendations": insight.recommendations
                })
            
            return recommendations
            
        except Exception as e:
            logger.error("Optimization recommendations error", error=str(e))
            return []


# Global advanced analytics engine instance
advanced_analytics_engine = AdvancedAnalyticsEngine()


# Convenience functions
async def get_comprehensive_analytics() -> Dict[str, Any]:
    """Get comprehensive analytics report"""
    return await advanced_analytics_engine.get_comprehensive_analytics()


async def get_performance_insights() -> List[Dict[str, Any]]:
    """Get recent performance insights"""
    recent_insights = [
        insight for insight in advanced_analytics_engine.insights_history 
        if insight.timestamp > datetime.now() - timedelta(hours=6)
    ]
    
    return [
        {
            "type": insight.insight_type.value,
            "severity": insight.severity.value,
            "title": insight.title,
            "description": insight.description,
            "impact_score": insight.impact_score,
            "confidence": insight.confidence,
            "recommendations": insight.recommendations,
            "timestamp": insight.timestamp.isoformat()
        }
        for insight in recent_insights
    ]