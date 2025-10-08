"""
Smart Coding AI Infrastructure - Queue Service  
Extracted from smart_coding_ai_optimized.py
"""

import structlog
import os
import threading
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from queue import PriorityQueue, Empty

logger = structlog.get_logger()


class QueueService:
    """Queue service for Smart Coding AI with async task processing"""
    
    def __init__(self, queue_type: str = "memory"):
        self.queue_type = queue_type
        self.queues: Dict[str, PriorityQueue] = {}
        self.queue_items: Dict[str, Dict] = {}
        self.queue_stats: Dict[str, Dict] = {}
        self.lock = threading.RLock()
        self.processing = False
        
        # Initialize queue based on type
        if queue_type == "memory":
            self._init_memory_queue()
        elif queue_type == "redis":
            self._init_redis_queue()
        elif queue_type == "database":
            self._init_database_queue()
    
    def _init_memory_queue(self):
        """Initialize in-memory queue"""
        pass  # Queues will be created on demand
    
    def _init_redis_queue(self):
        """Initialize Redis queue"""
        try:
            from redis import asyncio as aioredis
            redis_url = os.getenv("REDIS_URL", None) or os.getenv("UPSTASH_REDIS_URL", None) or "redis://localhost:6379"
            self.redis_client = aioredis.from_url(redis_url, decode_responses=True)
            logger.info("Redis queue initialized successfully")
        except ImportError:
            logger.warning("Redis not available, falling back to memory queue")
            self.redis_client = None
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, falling back to memory queue")
            self.redis_client = None
    
    def _init_database_queue(self):
        """Initialize database queue (placeholder)"""
        pass
    
    async def enqueue(self, queue_name: str, data: Dict[str, Any], priority: str = "normal", 
                     delay: Optional[int] = None, max_retries: int = 3) -> str:
        """Add item to queue"""
        try:
            with self.lock:
                item_id = str(uuid.uuid4())
                
                # Create queue if it doesn't exist
                if queue_name not in self.queues:
                    self.queues[queue_name] = PriorityQueue()
                    self.queue_items[queue_name] = {}
                    self.queue_stats[queue_name] = {
                        "total_items": 0,
                        "pending_items": 0,
                        "processing_items": 0,
                        "completed_items": 0,
                        "failed_items": 0,
                        "processing_times": []
                    }
                
                # Create queue item
                item = {
                    "id": item_id,
                    "queue_name": queue_name,
                    "data": data,
                    "priority": priority,
                    "status": "pending",
                    "created_at": datetime.now(),
                    "started_at": None,
                    "completed_at": None,
                    "retry_count": 0,
                    "max_retries": max_retries,
                    "error_message": None
                }
                
                # Store item
                self.queue_items[queue_name][item_id] = item
                
                # Add to priority queue
                priority_value = {"low": 4, "normal": 3, "high": 2, "critical": 1}.get(priority, 3)
                self.queues[queue_name].put((priority_value, item_id))
                
                # Update stats
                self.queue_stats[queue_name]["total_items"] += 1
                self.queue_stats[queue_name]["pending_items"] += 1
                
                return item_id
                
        except Exception as e:
            logger.error(f"Queue enqueue failed: {e}")
            raise
    
    async def dequeue(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """Get next item from queue"""
        try:
            with self.lock:
                if queue_name not in self.queues:
                    return None
                
                try:
                    _, item_id = self.queues[queue_name].get_nowait()
                    
                    if item_id in self.queue_items[queue_name]:
                        item = self.queue_items[queue_name][item_id]
                        item["status"] = "processing"
                        item["started_at"] = datetime.now()
                        
                        # Update stats
                        self.queue_stats[queue_name]["pending_items"] -= 1
                        self.queue_stats[queue_name]["processing_items"] += 1
                        
                        return item
                    else:
                        return None
                        
                except Empty:
                    return None
                    
        except Exception as e:
            logger.error(f"Queue dequeue failed: {e}")
            return None
    
    async def complete(self, queue_name: str, item_id: str, result: Optional[Dict[str, Any]] = None) -> bool:
        """Mark item as completed"""
        try:
            with self.lock:
                if queue_name in self.queue_items and item_id in self.queue_items[queue_name]:
                    item = self.queue_items[queue_name][item_id]
                    item["status"] = "completed"
                    item["completed_at"] = datetime.now()
                    
                    # Calculate processing time
                    if item["started_at"]:
                        processing_time = (item["completed_at"] - item["started_at"]).total_seconds()
                        self.queue_stats[queue_name]["processing_times"].append(processing_time)
                        # Keep only last 100 processing times
                        if len(self.queue_stats[queue_name]["processing_times"]) > 100:
                            self.queue_stats[queue_name]["processing_times"] = self.queue_stats[queue_name]["processing_times"][-100:]
                    
                    # Update stats
                    self.queue_stats[queue_name]["processing_items"] -= 1
                    self.queue_stats[queue_name]["completed_items"] += 1
                    
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Queue complete failed: {e}")
            return False
    
    async def fail(self, queue_name: str, item_id: str, error_message: str) -> bool:
        """Mark item as failed"""
        try:
            with self.lock:
                if queue_name in self.queue_items and item_id in self.queue_items[queue_name]:
                    item = self.queue_items[queue_name][item_id]
                    item["status"] = "failed"
                    item["error_message"] = error_message
                    item["retry_count"] += 1
                    
                    # Retry if under max retries
                    if item["retry_count"] < item["max_retries"]:
                        item["status"] = "retry"
                        priority_value = {"low": 4, "normal": 3, "high": 2, "critical": 1}.get(item["priority"], 3)
                        self.queues[queue_name].put((priority_value, item_id))
                        self.queue_stats[queue_name]["pending_items"] += 1
                    else:
                        self.queue_stats[queue_name]["failed_items"] += 1
                    
                    # Update stats
                    self.queue_stats[queue_name]["processing_items"] -= 1
                    
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Queue fail failed: {e}")
            return False
    
    async def get_stats(self, queue_name: Optional[str] = None) -> Dict[str, Any]:
        """Get queue statistics"""
        try:
            with self.lock:
                if queue_name:
                    if queue_name in self.queue_stats:
                        stats = self.queue_stats[queue_name].copy()
                        # Calculate average processing time
                        if stats["processing_times"]:
                            stats["avg_processing_time"] = sum(stats["processing_times"]) / len(stats["processing_times"])
                        else:
                            stats["avg_processing_time"] = 0.0
                        
                        # Calculate throughput (items per minute)
                        if stats["completed_items"] > 0:
                            # Simple calculation - in production, use time windows
                            stats["throughput_per_minute"] = stats["completed_items"] / 60.0
                        else:
                            stats["throughput_per_minute"] = 0.0
                        
                        stats["queue_name"] = queue_name
                        stats["created_at"] = datetime.now()
                        del stats["processing_times"]  # Remove raw data
                        return stats
                    else:
                        return {}
                else:
                    # Return stats for all queues
                    all_stats = {}
                    for qname in self.queue_stats.keys():
                        stats = self.queue_stats[qname].copy()
                        # Calculate average processing time
                        if stats["processing_times"]:
                            stats["avg_processing_time"] = sum(stats["processing_times"]) / len(stats["processing_times"])
                        else:
                            stats["avg_processing_time"] = 0.0
                        
                        # Calculate throughput (items per minute)
                        if stats["completed_items"] > 0:
                            # Simple calculation - in production, use time windows
                            stats["throughput_per_minute"] = stats["completed_items"] / 60.0
                        else:
                            stats["throughput_per_minute"] = 0.0
                        
                        stats["queue_name"] = qname
                        stats["created_at"] = datetime.now()
                        del stats["processing_times"]  # Remove raw data
                        all_stats[qname] = stats
                    return all_stats
                    
        except Exception as e:
            logger.error(f"Queue stats failed: {e}")
            return {}




__all__ = ['QueueService']
