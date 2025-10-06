"""
Predictive Scaling System for Cognomega AI
Anticipates load and scales resources proactively
"""

import asyncio
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import structlog
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json

from app.core.cpu_optimizer import cpu_optimizer
from app.core.performance_monitor import performance_monitor
from app.core.advanced_caching import advanced_cache

logger = structlog.get_logger()


class ScalingAction(str, Enum):
    """Types of scaling actions"""
    SCALE_UP_CPU = "scale_up_cpu"
    SCALE_DOWN_CPU = "scale_down_cpu"
    SCALE_UP_MEMORY = "scale_up_memory"
    SCALE_DOWN_MEMORY = "scale_down_memory"
    SCALE_UP_CACHE = "scale_up_cache"
    SCALE_DOWN_CACHE = "scale_down_cache"
    SCALE_UP_THREADS = "scale_up_threads"
    SCALE_DOWN_THREADS = "scale_down_threads"
    PREEMPTIVE_SCALE = "preemptive_scale"


class LoadPattern(str, Enum):
    """Load patterns"""
    STEADY = "steady"
    INCREASING = "increasing"
    DECREASING = "decreasing"
    SPIKE = "spike"
    CYCLICAL = "cyclical"
    ANOMALOUS = "anomalous"


@dataclass
class ScalingPrediction:
    """Scaling prediction result"""
    action: ScalingAction
    confidence: float
    predicted_load: float
    current_load: float
    time_horizon: int  # minutes
    reasoning: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LoadDataPoint:
    """Load data point"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    throughput: float
    active_users: int
    response_time: float
    error_rate: float
    cache_hit_rate: float
    system_load: float
    predicted_load: Optional[float] = None


class PredictiveScalingEngine:
    """Predictive scaling engine with machine learning"""
    
    def __init__(self):
        self.load_history: List[LoadDataPoint] = []
        self.scaling_predictions: List[ScalingPrediction] = []
        
        # ML models
        self.load_predictor = None
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.pattern_classifier = KMeans(n_clusters=5, random_state=42)
        self.scaler = StandardScaler()
        
        # Configuration
        self.prediction_horizon = 15  # minutes
        self.history_window = 60  # minutes
        self.scaling_threshold = 0.8
        self.cooldown_period = 300  # 5 minutes
        
        # Scaling parameters
        self.cpu_scaling_factor = 0.2
        self.memory_scaling_factor = 0.15
        self.cache_scaling_factor = 0.1
        
        # Track scaling actions
        self.last_scaling_action: Optional[datetime] = None
        self.scaling_cooldown = False
        
        # Initialize with synthetic data
        self._initialize_with_synthetic_data()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _initialize_with_synthetic_data(self):
        """Initialize with synthetic load data"""
        try:
            base_time = datetime.now() - timedelta(hours=2)
            
            for i in range(120):  # 2 hours of data
                # Generate realistic load patterns
                hour_of_day = (base_time + timedelta(minutes=i)).hour
                
                # Simulate daily patterns
                if 9 <= hour_of_day <= 17:  # Business hours
                    base_load = np.random.normal(70, 15)
                elif 18 <= hour_of_day <= 22:  # Evening
                    base_load = np.random.normal(60, 10)
                else:  # Night/weekend
                    base_load = np.random.normal(40, 10)
                
                # Add some spikes
                if np.random.random() < 0.05:  # 5% chance of spike
                    base_load = min(95, base_load + np.random.uniform(20, 40))
                
                data_point = LoadDataPoint(
                    timestamp=base_time + timedelta(minutes=i),
                    cpu_usage=base_load,
                    memory_usage=base_load * 0.8 + np.random.normal(0, 5),
                    throughput=base_load * 10 + np.random.normal(0, 50),
                    active_users=int(base_load * 2 + np.random.normal(0, 10)),
                    response_time=max(50, base_load * 5 + np.random.normal(0, 20)),
                    error_rate=max(0, base_load * 0.05 + np.random.normal(0, 1)),
                    cache_hit_rate=max(0, min(100, 80 - base_load * 0.3 + np.random.normal(0, 5))),
                    system_load=base_load
                )
                
                self.load_history.append(data_point)
            
            # Train initial models
            asyncio.create_task(self._train_predictive_models())
            
            logger.info("Predictive scaling engine initialized with synthetic data")
            
        except Exception as e:
            logger.error("Predictive scaling initialization error", error=str(e))
    
    def _start_background_tasks(self):
        """Start background tasks for predictive scaling"""
        asyncio.create_task(self._load_monitoring_loop())
        asyncio.create_task(self._predictive_scaling_loop())
        asyncio.create_task(self._model_retraining_loop())
    
    async def _load_monitoring_loop(self):
        """Monitor system load continuously"""
        while True:
            try:
                await asyncio.sleep(30)  # Monitor every 30 seconds
                await self._collect_load_data()
                
            except Exception as e:
                logger.error("Load monitoring loop error", error=str(e))
                await asyncio.sleep(60)
    
    async def _predictive_scaling_loop(self):
        """Predict and execute scaling actions"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                if not self.scaling_cooldown:
                    predictions = await self._predict_scaling_needs()
                    
                    for prediction in predictions:
                        if prediction.confidence >= self.scaling_threshold:
                            await self._execute_scaling_action(prediction)
                
            except Exception as e:
                logger.error("Predictive scaling loop error", error=str(e))
                await asyncio.sleep(60)
    
    async def _model_retraining_loop(self):
        """Retrain predictive models periodically"""
        while True:
            try:
                await asyncio.sleep(1800)  # Retrain every 30 minutes
                await self._train_predictive_models()
                
            except Exception as e:
                logger.error("Model retraining loop error", error=str(e))
                await asyncio.sleep(300)
    
    async def _collect_load_data(self):
        """Collect current system load data"""
        try:
            # Get current metrics
            cache_stats = await advanced_cache.get_cache_stats()
            cpu_metrics = await cpu_optimizer.get_cpu_metrics()
            performance_summary = await performance_monitor.get_performance_summary()
            
            # Extract metrics
            cpu_usage = cpu_metrics.get("cpu_stats", {}).get("total_usage", 0)
            memory_usage = cpu_metrics.get("cpu_stats", {}).get("memory_usage", 0)
            throughput = performance_summary.get("throughput", {}).get("total", 0)
            response_time = performance_summary.get("response_times", {}).get("avg", 0)
            error_rate = sum(performance_summary.get("error_counts", {}).values())
            cache_hit_rate = cache_stats.get("metrics", {}).get("hit_rate", 0) * 100
            
            # Estimate active users
            active_users = min(200, throughput / 5)  # Rough estimate
            
            # Calculate system load
            system_load = (cpu_usage + memory_usage + (100 - cache_hit_rate)) / 3
            
            # Create data point
            data_point = LoadDataPoint(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                throughput=throughput,
                active_users=active_users,
                response_time=response_time,
                error_rate=error_rate,
                cache_hit_rate=cache_hit_rate,
                system_load=system_load
            )
            
            self.load_history.append(data_point)
            
            # Keep only recent history
            cutoff_time = datetime.now() - timedelta(minutes=self.history_window)
            self.load_history = [
                dp for dp in self.load_history if dp.timestamp > cutoff_time
            ]
            
        except Exception as e:
            logger.error("Load data collection error", error=str(e))
    
    async def _train_predictive_models(self):
        """Train predictive models"""
        try:
            if len(self.load_history) < 20:
                logger.info("Insufficient data for training", count=len(self.load_history))
                return
            
            # Prepare training data
            df = pd.DataFrame([
                {
                    'cpu_usage': dp.cpu_usage,
                    'memory_usage': dp.memory_usage,
                    'throughput': dp.throughput,
                    'active_users': dp.active_users,
                    'response_time': dp.response_time,
                    'error_rate': dp.error_rate,
                    'cache_hit_rate': dp.cache_hit_rate,
                    'system_load': dp.system_load,
                    'hour': dp.timestamp.hour,
                    'minute': dp.timestamp.minute,
                    'day_of_week': dp.timestamp.weekday()
                }
                for dp in self.load_history
            ])
            
            # Features for prediction
            feature_columns = [
                'cpu_usage', 'memory_usage', 'throughput', 'active_users',
                'response_time', 'error_rate', 'cache_hit_rate', 'system_load',
                'hour', 'minute', 'day_of_week'
            ]
            
            X = df[feature_columns]
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train anomaly detector
            self.anomaly_detector.fit(X_scaled)
            
            # Train pattern classifier
            self.pattern_classifier.fit(X_scaled)
            
            logger.info("Predictive models trained successfully", 
                       samples=len(self.load_history))
            
        except Exception as e:
            logger.error("Model training error", error=str(e))
    
    async def _predict_scaling_needs(self) -> List[ScalingPrediction]:
        """Predict scaling needs based on current and historical data"""
        try:
            if len(self.load_history) < 10:
                return []
            
            # Get recent load pattern
            recent_data = self.load_history[-10:]
            current_data = recent_data[-1]
            
            # Analyze load trend
            trend = self._analyze_load_trend(recent_data)
            
            # Predict future load
            predicted_load = await self._predict_future_load(current_data, trend)
            
            # Generate scaling predictions
            predictions = []
            
            # CPU scaling prediction
            if predicted_load.cpu_usage > 80:
                confidence = min(0.95, (predicted_load.cpu_usage - 70) / 30)
                
                predictions.append(ScalingPrediction(
                    action=ScalingAction.SCALE_UP_CPU,
                    confidence=confidence,
                    predicted_load=predicted_load.cpu_usage,
                    current_load=current_data.cpu_usage,
                    time_horizon=self.prediction_horizon,
                    reasoning=f"CPU usage predicted to reach {predicted_load.cpu_usage:.1f}% in {self.prediction_horizon} minutes",
                    parameters={"target_cpu_usage": 60, "scaling_factor": self.cpu_scaling_factor}
                ))
            elif predicted_load.cpu_usage < 30:
                confidence = min(0.9, (50 - predicted_load.cpu_usage) / 50)
                
                predictions.append(ScalingPrediction(
                    action=ScalingAction.SCALE_DOWN_CPU,
                    confidence=confidence,
                    predicted_load=predicted_load.cpu_usage,
                    current_load=current_data.cpu_usage,
                    time_horizon=self.prediction_horizon,
                    reasoning=f"CPU usage predicted to drop to {predicted_load.cpu_usage:.1f}% in {self.prediction_horizon} minutes",
                    parameters={"target_cpu_usage": 40, "scaling_factor": self.cpu_scaling_factor}
                ))
            
            # Memory scaling prediction
            if predicted_load.memory_usage > 85:
                confidence = min(0.95, (predicted_load.memory_usage - 75) / 25)
                
                predictions.append(ScalingPrediction(
                    action=ScalingAction.SCALE_UP_MEMORY,
                    confidence=confidence,
                    predicted_load=predicted_load.memory_usage,
                    current_load=current_data.memory_usage,
                    time_horizon=self.prediction_horizon,
                    reasoning=f"Memory usage predicted to reach {predicted_load.memory_usage:.1f}% in {self.prediction_horizon} minutes",
                    parameters={"target_memory_usage": 70, "scaling_factor": self.memory_scaling_factor}
                ))
            
            # Thread scaling prediction
            if predicted_load.throughput > current_data.throughput * 1.5:
                confidence = min(0.9, (predicted_load.throughput - current_data.throughput) / current_data.throughput)
                
                predictions.append(ScalingPrediction(
                    action=ScalingAction.SCALE_UP_THREADS,
                    confidence=confidence,
                    predicted_load=predicted_load.throughput,
                    current_load=current_data.throughput,
                    time_horizon=self.prediction_horizon,
                    reasoning=f"Throughput predicted to increase to {predicted_load.throughput:.1f} in {self.prediction_horizon} minutes",
                    parameters={"target_throughput": current_data.throughput * 1.2}
                ))
            
            return predictions
            
        except Exception as e:
            logger.error("Scaling prediction error", error=str(e))
            return []
    
    def _analyze_load_trend(self, recent_data: List[LoadDataPoint]) -> LoadPattern:
        """Analyze load trend from recent data"""
        try:
            if len(recent_data) < 5:
                return LoadPattern.STEADY
            
            # Calculate trend
            cpu_values = [dp.cpu_usage for dp in recent_data]
            memory_values = [dp.memory_usage for dp in recent_data]
            throughput_values = [dp.throughput for dp in recent_data]
            
            # Simple trend analysis
            cpu_trend = np.polyfit(range(len(cpu_values)), cpu_values, 1)[0]
            memory_trend = np.polyfit(range(len(memory_values)), memory_values, 1)[0]
            throughput_trend = np.polyfit(range(len(throughput_values)), throughput_values, 1)[0]
            
            avg_trend = (cpu_trend + memory_trend + throughput_trend) / 3
            
            # Determine pattern
            if avg_trend > 5:
                return LoadPattern.INCREASING
            elif avg_trend < -5:
                return LoadPattern.DECREASING
            elif abs(avg_trend) < 2:
                return LoadPattern.STEADY
            else:
                return LoadPattern.CYCLICAL
                
        except Exception as e:
            logger.error("Load trend analysis error", error=str(e))
            return LoadPattern.STEADY
    
    async def _predict_future_load(self, current_data: LoadDataPoint, trend: LoadPattern) -> LoadDataPoint:
        """Predict future load based on current data and trend"""
        try:
            # Simple prediction based on trend
            if trend == LoadPattern.INCREASING:
                factor = 1.2
            elif trend == LoadPattern.DECREASING:
                factor = 0.8
            else:
                factor = 1.0
            
            # Add some randomness for realistic prediction
            noise_factor = np.random.normal(1.0, 0.1)
            factor *= noise_factor
            
            predicted_data = LoadDataPoint(
                timestamp=datetime.now() + timedelta(minutes=self.prediction_horizon),
                cpu_usage=min(100, current_data.cpu_usage * factor),
                memory_usage=min(100, current_data.memory_usage * factor),
                throughput=max(0, current_data.throughput * factor),
                active_users=max(0, int(current_data.active_users * factor)),
                response_time=max(10, current_data.response_time * factor),
                error_rate=max(0, current_data.error_rate * factor),
                cache_hit_rate=max(0, min(100, current_data.cache_hit_rate * (2 - factor))),
                system_load=min(100, current_data.system_load * factor)
            )
            
            return predicted_data
            
        except Exception as e:
            logger.error("Future load prediction error", error=str(e))
            return current_data
    
    async def _execute_scaling_action(self, prediction: ScalingPrediction):
        """Execute scaling action"""
        try:
            # Check cooldown
            if (self.last_scaling_action and 
                datetime.now() - self.last_scaling_action < timedelta(seconds=self.cooldown_period)):
                logger.info("Scaling action skipped due to cooldown")
                return
            
            logger.info("Executing predictive scaling", 
                       action=prediction.action.value,
                       confidence=prediction.confidence,
                       predicted_load=prediction.predicted_load,
                       current_load=prediction.current_load)
            
            # Execute scaling based on action
            if prediction.action == ScalingAction.SCALE_UP_CPU:
                await self._scale_up_cpu_resources(prediction.parameters)
            elif prediction.action == ScalingAction.SCALE_DOWN_CPU:
                await self._scale_down_cpu_resources(prediction.parameters)
            elif prediction.action == ScalingAction.SCALE_UP_MEMORY:
                await self._scale_up_memory_resources(prediction.parameters)
            elif prediction.action == ScalingAction.SCALE_UP_THREADS:
                await self._scale_up_thread_resources(prediction.parameters)
            elif prediction.action == ScalingAction.SCALE_DOWN_THREADS:
                await self._scale_down_thread_resources(prediction.parameters)
            
            # Record scaling action
            self.last_scaling_action = datetime.now()
            self.scaling_predictions.append(prediction)
            
            # Set cooldown
            self.scaling_cooldown = True
            asyncio.create_task(self._reset_cooldown())
            
            logger.info("Predictive scaling executed successfully", 
                       action=prediction.action.value)
            
        except Exception as e:
            logger.error("Scaling execution error", 
                        action=prediction.action.value, 
                        error=str(e))
    
    async def _scale_up_cpu_resources(self, parameters: Dict[str, Any]):
        """Scale up CPU resources"""
        try:
            scaling_factor = parameters.get("scaling_factor", self.cpu_scaling_factor)
            
            # Increase thread pool sizes
            current_threads = cpu_optimizer.thread_pool._max_workers
            new_size = min(current_threads + int(current_threads * scaling_factor), 
                          cpu_optimizer.cpu_count * 3)
            
            cpu_optimizer._resize_thread_pool(new_size)
            
            logger.info("CPU resources scaled up", 
                       old_size=current_threads, 
                       new_size=new_size)
            
        except Exception as e:
            logger.error("CPU scale up error", error=str(e))
    
    async def _scale_down_cpu_resources(self, parameters: Dict[str, Any]):
        """Scale down CPU resources"""
        try:
            scaling_factor = parameters.get("scaling_factor", self.cpu_scaling_factor)
            
            # Decrease thread pool sizes
            current_threads = cpu_optimizer.thread_pool._max_workers
            new_size = max(int(current_threads * (1 - scaling_factor)), 
                          cpu_optimizer.cpu_count // 2)
            
            cpu_optimizer._resize_thread_pool(new_size)
            
            logger.info("CPU resources scaled down", 
                       old_size=current_threads, 
                       new_size=new_size)
            
        except Exception as e:
            logger.error("CPU scale down error", error=str(e))
    
    async def _scale_up_memory_resources(self, parameters: Dict[str, Any]):
        """Scale up memory resources"""
        try:
            # Trigger memory optimization
            import gc
            gc.collect()
            
            # Clear old cache entries
            await advanced_cache.invalidate_pattern("old_*")
            
            logger.info("Memory resources optimized")
            
        except Exception as e:
            logger.error("Memory scale up error", error=str(e))
    
    async def _scale_up_thread_resources(self, parameters: Dict[str, Any]):
        """Scale up thread resources"""
        try:
            # Increase AI processing pool
            current_ai_threads = cpu_optimizer.ai_pool._max_workers
            new_size = min(current_ai_threads + 2, cpu_optimizer.cpu_count * 2)
            
            cpu_optimizer._resize_ai_pool(new_size)
            
            logger.info("Thread resources scaled up", 
                       old_size=current_ai_threads, 
                       new_size=new_size)
            
        except Exception as e:
            logger.error("Thread scale up error", error=str(e))
    
    async def _scale_down_thread_resources(self, parameters: Dict[str, Any]):
        """Scale down thread resources"""
        try:
            # Decrease AI processing pool
            current_ai_threads = cpu_optimizer.ai_pool._max_workers
            new_size = max(current_ai_threads - 1, cpu_optimizer.cpu_count // 2)
            
            cpu_optimizer._resize_ai_pool(new_size)
            
            logger.info("Thread resources scaled down", 
                       old_size=current_ai_threads, 
                       new_size=new_size)
            
        except Exception as e:
            logger.error("Thread scale down error", error=str(e))
    
    async def _reset_cooldown(self):
        """Reset scaling cooldown"""
        await asyncio.sleep(self.cooldown_period)
        self.scaling_cooldown = False
    
    async def get_scaling_recommendations(self) -> Dict[str, Any]:
        """Get predictive scaling recommendations"""
        try:
            predictions = await self._predict_scaling_needs()
            
            recommendations = []
            for prediction in predictions:
                recommendations.append({
                    "action": prediction.action.value,
                    "confidence": prediction.confidence,
                    "predicted_load": prediction.predicted_load,
                    "current_load": prediction.current_load,
                    "time_horizon": prediction.time_horizon,
                    "reasoning": prediction.reasoning,
                    "parameters": prediction.parameters
                })
            
            return {
                "recommendations": recommendations,
                "scaling_enabled": not self.scaling_cooldown,
                "cooldown_remaining": max(0, self.cooldown_period - 
                                        (datetime.now() - self.last_scaling_action).seconds 
                                        if self.last_scaling_action else 0),
                "recent_predictions": len([
                    p for p in self.scaling_predictions 
                    if p.timestamp > datetime.now() - timedelta(hours=1)
                ]),
                "load_history_size": len(self.load_history)
            }
            
        except Exception as e:
            logger.error("Scaling recommendations error", error=str(e))
            return {}


# Global predictive scaling engine instance
predictive_scaling_engine = PredictiveScalingEngine()


# Convenience functions
async def get_scaling_recommendations() -> Dict[str, Any]:
    """Get predictive scaling recommendations"""
    return await predictive_scaling_engine.get_scaling_recommendations()


async def trigger_predictive_scaling():
    """Trigger predictive scaling analysis"""
    predictions = await predictive_scaling_engine._predict_scaling_needs()
    for prediction in predictions:
        if prediction.confidence >= 0.8:
            await predictive_scaling_engine._execute_scaling_action(prediction)
