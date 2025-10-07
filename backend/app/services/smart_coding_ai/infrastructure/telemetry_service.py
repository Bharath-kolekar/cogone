"""
Telemetry Service for Smart Coding AI
Preserves metrics and event tracking capabilities
"""

import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
import structlog

logger = structlog.get_logger()


class TelemetryService:
    """
    Telemetry service for Smart Coding AI metrics and events
    Tracks performance and usage metrics
    """
    
    def __init__(self):
        self.metrics_buffer: List[Dict] = []
        self.events_buffer: List[Dict] = []
        self.telemetry_stats = {
            "metrics_recorded": 0,
            "events_recorded": 0,
            "batches_processed": 0,
            "errors": 0
        }
        self.lock = threading.RLock()
        self.batch_size = 100
        self.flush_interval = 30  # seconds
    
    async def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None,
                          level: str = "info", user_id: Optional[str] = None,
                          session_id: Optional[str] = None) -> bool:
        """
        Record a telemetry metric
        Tracks performance metrics for Six Sigma quality
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
        """
        Record a telemetry event
        Tracks system events and user actions
        """
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
        """
        Record a performance metric
        Supports 65% faster response time tracking
        """
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
                    "metrics_buffer_size": len(self.metrics_buffer),
                    "events_buffer_size": len(self.events_buffer),
                    "created_at": datetime.now()
                }
                
        except Exception as e:
            logger.error(f"Telemetry stats failed: {e}")
            return {}
    
    async def flush(self):
        """Flush all buffers"""
        await self._flush_metrics()
        await self._flush_events()
    
    async def _flush_metrics(self):
        """Flush metrics buffer"""
        try:
            if self.metrics_buffer:
                # In production, send to telemetry backend (DataDog, New Relic, etc.)
                logger.info(f"Flushing {len(self.metrics_buffer)} metrics")
                self.metrics_buffer.clear()
                self.telemetry_stats["batches_processed"] += 1
                
        except Exception as e:
            logger.error(f"Metrics flush failed: {e}")
    
    async def _flush_events(self):
        """Flush events buffer"""
        try:
            if self.events_buffer:
                # In production, send to telemetry backend
                logger.info(f"Flushing {len(self.events_buffer)} events")
                self.events_buffer.clear()
                self.telemetry_stats["batches_processed"] += 1
                
        except Exception as e:
            logger.error(f"Events flush failed: {e}")
