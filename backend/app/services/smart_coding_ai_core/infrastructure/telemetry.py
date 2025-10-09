"""
🧠 Intelligent Telemetry Service - Enhanced
Moved from smart_coding_ai_telemetry.py with intelligence enhancements

PRESERVES: All functionality from smart_coding_ai_telemetry.py (163 lines)
ENHANCES: Adds intelligent metric aggregation and anomaly detection

Version: 1.0.0 - Enhanced
Created: October 9, 2025
"""

import structlog
import threading
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class IntelligentTelemetryService:
    """
    Enhanced telemetry service with intelligent metric analysis
    
    PRESERVES: All original functionality
    ENHANCES: Adds anomaly detection and intelligent aggregation
    """
    
    def __init__(self):
        self.metrics_buffer: List[Dict] = []
        self.events_buffer: List[Dict] = []
        self.telemetry_stats = {
            "metrics_recorded": 0,
            "events_recorded": 0,
            "batches_processed": 0,
            "errors": 0,
            "anomalies_detected": 0  # ENHANCEMENT
        }
        self.lock = threading.RLock()
        self.batch_size = 100
        self.flush_interval = 30
        
        # ENHANCEMENT: Metric baselines for anomaly detection
        self.metric_baselines: Dict[str, Dict[str, float]] = {}
        
        logger.info("Intelligent telemetry service initialized", anomaly_detection=True)
    
    async def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None,
                          level: str = "info", user_id: Optional[str] = None,
                          session_id: Optional[str] = None) -> bool:
        """
        Record a telemetry metric
        ENHANCED: Detect anomalies
        """
        try:
            with self.lock:
                metric = {
                    "name": name,
                    "value": value,
                    "type": "metric",
                    "level": level,
                    "tags": tags or {},
                    "timestamp": datetime.now(),
                    "source": "smart_coding_ai",
                    "user_id": user_id,
                    "session_id": session_id
                }
                
                # ENHANCEMENT: Check for anomalies
                is_anomaly = await self._detect_anomaly(name, value)
                if is_anomaly:
                    metric["anomaly"] = True
                    self.telemetry_stats["anomalies_detected"] += 1
                    logger.warning(f"Anomaly detected in metric {name}", value=value)
                
                self.metrics_buffer.append(metric)
                self.telemetry_stats["metrics_recorded"] += 1
                
                # Flush if buffer is full
                if len(self.metrics_buffer) >= self.batch_size:
                    await self._flush_metrics()
                
                return True
                
        except Exception as e:
            logger.error(f"Telemetry metric recording failed: {e}")
            self.telemetry_stats["errors"] += 1
            return False
    
    async def record_event(self, event_name: str, event_data: Dict[str, Any],
                         tags: Optional[Dict[str, str]] = None, level: str = "info",
                         user_id: Optional[str] = None, session_id: Optional[str] = None) -> bool:
        """Record a telemetry event"""
        try:
            with self.lock:
                event = {
                    "event_name": event_name,
                    "event_data": event_data,
                    "type": "event",
                    "level": level,
                    "tags": tags or {},
                    "timestamp": datetime.now(),
                    "source": "smart_coding_ai",
                    "user_id": user_id,
                    "session_id": session_id
                }
                
                self.events_buffer.append(event)
                self.telemetry_stats["events_recorded"] += 1
                
                # Flush if buffer is full
                if len(self.events_buffer) >= self.batch_size:
                    await self._flush_events()
                
                return True
                
        except Exception as e:
            logger.error(f"Telemetry event recording failed: {e}")
            self.telemetry_stats["errors"] += 1
            return False
    
    async def record_performance_metric(self, operation: str, duration: float,
                                      success: bool, user_id: Optional[str] = None) -> bool:
        """Record a performance metric"""
        return await self.record_metric(
            name=f"performance.{operation}",
            value=duration,
            tags={"operation": operation, "success": str(success)},
            level="info",
            user_id=user_id
        )
    
    async def record_error(self, error_type: str, error_message: str,
                          user_id: Optional[str] = None, session_id: Optional[str] = None) -> bool:
        """Record an error event"""
        return await self.record_event(
            event_name="error_occurred",
            event_data={"error_type": error_type, "error_message": error_message},
            tags={"error_type": error_type},
            level="error",
            user_id=user_id,
            session_id=session_id
        )
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        try:
            with self.lock:
                return {
                    "metrics_recorded": self.telemetry_stats["metrics_recorded"],
                    "events_recorded": self.telemetry_stats["events_recorded"],
                    "batches_processed": self.telemetry_stats["batches_processed"],
                    "errors": self.telemetry_stats["errors"],
                    "anomalies_detected": self.telemetry_stats["anomalies_detected"],  # ENHANCED
                    "metrics_buffer_size": len(self.metrics_buffer),
                    "events_buffer_size": len(self.events_buffer),
                    "baselines_tracked": len(self.metric_baselines),  # ENHANCED
                    "created_at": datetime.now()
                }
                
        except Exception as e:
            logger.error(f"Telemetry stats failed: {e}")
            return {}
    
    async def _detect_anomaly(self, metric_name: str, value: float) -> bool:
        """
        ENHANCEMENT: Detect anomalies in metrics
        Simple statistical approach - can be enhanced with ML
        """
        try:
            if metric_name not in self.metric_baselines:
                # Initialize baseline
                self.metric_baselines[metric_name] = {
                    "values": [value],
                    "mean": value,
                    "std_dev": 0.0,
                    "count": 1
                }
                return False
            
            baseline = self.metric_baselines[metric_name]
            
            # Update baseline
            baseline["values"].append(value)
            if len(baseline["values"]) > 100:
                baseline["values"] = baseline["values"][-100:]
            
            # Calculate stats
            values = baseline["values"]
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5
            
            baseline["mean"] = mean
            baseline["std_dev"] = std_dev
            baseline["count"] = len(values)
            
            # Check for anomaly (3 standard deviations)
            if std_dev > 0:
                z_score = abs((value - mean) / std_dev)
                return z_score > 3.0
            
            return False
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return False
    
    async def _flush_metrics(self):
        """Flush metrics buffer"""
        try:
            if self.metrics_buffer:
                logger.info(f"Flushing {len(self.metrics_buffer)} metrics")
                self.metrics_buffer.clear()
                self.telemetry_stats["batches_processed"] += 1
                
        except Exception as e:
            logger.error(f"Metrics flush failed: {e}")
    
    async def _flush_events(self):
        """Flush events buffer"""
        try:
            if self.events_buffer:
                logger.info(f"Flushing {len(self.events_buffer)} events")
                self.events_buffer.clear()
                self.telemetry_stats["batches_processed"] += 1
                
        except Exception as e:
            logger.error(f"Events flush failed: {e}")


# Backward compatibility alias
TelemetryService = IntelligentTelemetryService

__all__ = ['IntelligentTelemetryService', 'TelemetryService']

logger.info("✅ Telemetry module enhanced", intelligence_added="anomaly_detection")

