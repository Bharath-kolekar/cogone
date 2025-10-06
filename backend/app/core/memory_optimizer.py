"""
Memory Optimization Engine for CognOmega System

This module implements advanced memory optimization techniques including
memory pooling, shared memory management, garbage collection optimization,
and intelligent caching strategies.
"""

import structlog
import asyncio
import gc
import psutil
import threading
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import weakref
from dataclasses import dataclass
import sys
import os
from collections import defaultdict, deque

logger = structlog.get_logger(__name__)

class MemoryType(Enum):
    """Memory allocation types"""
    SHARED = "shared"
    POOLED = "pooled"
    CACHED = "cached"
    TEMPORARY = "temporary"
    PERSISTENT = "persistent"

@dataclass
class MemoryBlock:
    """Memory block definition"""
    block_id: str
    memory_type: MemoryType
    size_bytes: int
    allocated_at: datetime
    last_accessed: datetime
    access_count: int
    data: Any
    weak_ref: Optional[weakref.ref] = None

@dataclass
class MemoryUsage:
    """Memory usage metrics"""
    total_memory: int
    available_memory: int
    used_memory: int
    cached_memory: int
    shared_memory: int
    memory_percent: float
    swap_memory: int
    timestamp: datetime

class MemoryPool:
    """Memory pool for efficient memory management"""
    
    def __init__(self, pool_size: int, block_size: int):
        self.pool_size = pool_size
        self.block_size = block_size
        self.available_blocks = deque()
        self.allocated_blocks = {}
        self.pool_lock = threading.Lock()
        
        # Initialize pool with pre-allocated blocks
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize memory pool with pre-allocated blocks"""
        for i in range(self.pool_size):
            block_id = f"pool_block_{i}"
            block = MemoryBlock(
                block_id=block_id,
                memory_type=MemoryType.POOLED,
                size_bytes=self.block_size,
                allocated_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=0,
                data=None
            )
            self.available_blocks.append(block)
    
    def allocate_block(self, data: Any) -> Optional[MemoryBlock]:
        """Allocate a memory block from the pool"""
        with self.pool_lock:
            if self.available_blocks:
                block = self.available_blocks.popleft()
                block.data = data
                block.last_accessed = datetime.now()
                block.access_count += 1
                self.allocated_blocks[block.block_id] = block
                return block
        return None
    
    def deallocate_block(self, block_id: str):
        """Deallocate a memory block back to the pool"""
        with self.pool_lock:
            if block_id in self.allocated_blocks:
                block = self.allocated_blocks.pop(block_id)
                block.data = None
                self.available_blocks.append(block)

class MemoryOptimizer:
    """Advanced memory optimization engine"""
    
    def __init__(self):
        self.memory_pools = {}
        self.shared_memory_cache = {}
        self.memory_usage_history: List[MemoryUsage] = []
        self.optimization_metrics = {
            "total_allocations": 0,
            "pool_hits": 0,
            "cache_hits": 0,
            "gc_collections": 0,
            "memory_efficiency": 0.0
        }
        
        # Memory monitoring
        self.memory_monitor_thread = None
        self.monitoring_active = False
        
        # Garbage collection optimization
        self.gc_thresholds = {
            "generation_0": 700,
            "generation_1": 10,
            "generation_2": 10
        }
        
        # Initialize memory pools for different services
        self._initialize_memory_pools()
        
        logger.info("Memory Optimizer initialized")

    def _initialize_memory_pools(self):
        """Initialize memory pools for different services (optimized for zero-cost)"""
        from app.core.config import settings
        
        if getattr(settings, 'ZERO_COST_MODE', False):
            # Smaller pools for zero-cost deployment
            self.memory_pools["ai_models"] = MemoryPool(pool_size=5, block_size=512 * 1024)  # 512KB blocks
            self.memory_pools["code_generation"] = MemoryPool(pool_size=10, block_size=256 * 1024)  # 256KB blocks
            self.memory_pools["voice_processing"] = MemoryPool(pool_size=8, block_size=128 * 1024)  # 128KB blocks
            self.memory_pools["payment_processing"] = MemoryPool(pool_size=3, block_size=32 * 1024)  # 32KB blocks
            self.memory_pools["general"] = MemoryPool(pool_size=20, block_size=64 * 1024)  # 64KB blocks
        else:
            # Standard pools for normal deployment
            self.memory_pools["ai_models"] = MemoryPool(pool_size=10, block_size=1024 * 1024)  # 1MB blocks
            self.memory_pools["code_generation"] = MemoryPool(pool_size=20, block_size=512 * 1024)  # 512KB blocks
            self.memory_pools["voice_processing"] = MemoryPool(pool_size=15, block_size=256 * 1024)  # 256KB blocks
            self.memory_pools["payment_processing"] = MemoryPool(pool_size=5, block_size=64 * 1024)  # 64KB blocks
            self.memory_pools["general"] = MemoryPool(pool_size=50, block_size=128 * 1024)  # 128KB blocks

    async def optimize_memory_allocation(self, service_name: str, data: Any, memory_type: MemoryType = MemoryType.TEMPORARY) -> str:
        """Optimize memory allocation for specific service"""
        try:
            logger.info(f"Optimizing memory allocation for service: {service_name}")
            
            # Get appropriate memory pool
            pool_name = self._get_pool_for_service(service_name)
            pool = self.memory_pools[pool_name]
            
            # Try to allocate from pool first
            block = pool.allocate_block(data)
            
            if block:
                # Pool allocation successful
                self.optimization_metrics["pool_hits"] += 1
                self.optimization_metrics["total_allocations"] += 1
                
                logger.info(f"Memory allocated from pool for {service_name}: {block.block_id}")
                return block.block_id
            else:
                # Pool full, use shared memory cache
                cache_key = self._create_cache_key(service_name, data)
                
                if cache_key in self.shared_memory_cache:
                    # Cache hit
                    self.optimization_metrics["cache_hits"] += 1
                    self.shared_memory_cache[cache_key]["access_count"] += 1
                    self.shared_memory_cache[cache_key]["last_accessed"] = datetime.now()
                    
                    logger.info(f"Memory retrieved from cache for {service_name}: {cache_key}")
                    return cache_key
                else:
                    # Cache miss, create new entry
                    self.shared_memory_cache[cache_key] = {
                        "data": data,
                        "memory_type": memory_type,
                        "allocated_at": datetime.now(),
                        "last_accessed": datetime.now(),
                        "access_count": 1,
                        "size_bytes": sys.getsizeof(data)
                    }
                    
                    self.optimization_metrics["total_allocations"] += 1
                    
                    logger.info(f"Memory allocated in cache for {service_name}: {cache_key}")
                    return cache_key
            
        except Exception as e:
            logger.error(f"Memory allocation optimization failed for {service_name}", error=str(e))
            raise

    def _get_pool_for_service(self, service_name: str) -> str:
        """Get appropriate memory pool for service"""
        pool_mapping = {
            "smart_coding_ai": "ai_models",
            "voice_to_app": "voice_processing",
            "payment_service": "payment_processing",
            "ai_orchestrator": "code_generation",
            "agent_system": "ai_models"
        }
        return pool_mapping.get(service_name, "general")

    def _create_cache_key(self, service_name: str, data: Any) -> str:
        """Create cache key for data"""
        data_hash = hash(str(data))
        return f"{service_name}_{data_hash}_{datetime.now().timestamp()}"

    async def deallocate_memory(self, allocation_id: str, service_name: str):
        """Deallocate memory with optimization"""
        try:
            logger.info(f"Deallocating memory for {service_name}: {allocation_id}")
            
            # Try pool deallocation first
            pool_name = self._get_pool_for_service(service_name)
            pool = self.memory_pools[pool_name]
            
            if allocation_id.startswith("pool_block_"):
                pool.deallocate_block(allocation_id)
                logger.info(f"Memory deallocated from pool: {allocation_id}")
            elif allocation_id in self.shared_memory_cache:
                # Check if memory should be kept in cache
                cache_entry = self.shared_memory_cache[allocation_id]
                if cache_entry["access_count"] > 1:
                    # Keep in cache, just mark as less frequently used
                    cache_entry["access_count"] -= 1
                    logger.info(f"Memory kept in cache (reduced access count): {allocation_id}")
                else:
                    # Remove from cache
                    del self.shared_memory_cache[allocation_id]
                    logger.info(f"Memory removed from cache: {allocation_id}")
            
        except Exception as e:
            logger.error(f"Memory deallocation failed for {allocation_id}", error=str(e))

    async def optimize_garbage_collection(self):
        """Optimize garbage collection for better memory management"""
        try:
            logger.info("Optimizing garbage collection")
            
            # Get current memory usage
            memory_info = await self.get_memory_usage()
            
            # Adjust GC thresholds based on memory usage
            if memory_info.memory_percent > 80:
                # High memory usage, be more aggressive
                self.gc_thresholds["generation_0"] = 500
                self.gc_thresholds["generation_1"] = 5
                self.gc_thresholds["generation_2"] = 5
            elif memory_info.memory_percent < 50:
                # Low memory usage, be less aggressive
                self.gc_thresholds["generation_0"] = 1000
                self.gc_thresholds["generation_1"] = 20
                self.gc_thresholds["generation_2"] = 20
            
            # Set GC thresholds
            gc.set_threshold(
                self.gc_thresholds["generation_0"],
                self.gc_thresholds["generation_1"],
                self.gc_thresholds["generation_2"]
            )
            
            # Run garbage collection
            collected = gc.collect()
            self.optimization_metrics["gc_collections"] += 1
            
            logger.info(f"Garbage collection completed, collected {collected} objects")
            
            return {
                "objects_collected": collected,
                "gc_thresholds": self.gc_thresholds,
                "memory_usage_before": memory_info.memory_percent
            }
            
        except Exception as e:
            logger.error(f"Garbage collection optimization failed", error=str(e))
            raise

    async def get_memory_usage(self) -> MemoryUsage:
        """Get current memory usage with optimization insights"""
        try:
            # Get system memory info
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Calculate shared memory usage
            shared_memory = sum(entry["size_bytes"] for entry in self.shared_memory_cache.values())
            
            # Calculate cached memory usage
            cached_memory = 0
            for pool in self.memory_pools.values():
                cached_memory += len(pool.allocated_blocks) * pool.block_size
            
            memory_usage = MemoryUsage(
                total_memory=memory.total,
                available_memory=memory.available,
                used_memory=memory.used,
                cached_memory=cached_memory,
                shared_memory=shared_memory,
                memory_percent=memory.percent,
                swap_memory=swap.used,
                timestamp=datetime.now()
            )
            
            # Store in history
            self.memory_usage_history.append(memory_usage)
            
            # Keep only recent history
            if len(self.memory_usage_history) > 100:
                self.memory_usage_history = self.memory_usage_history[-100:]
            
            return memory_usage
            
        except Exception as e:
            logger.error(f"Memory usage retrieval failed", error=str(e))
            raise

    async def optimize_service_memory_usage(self, service_name: str, data_objects: List[Any]) -> Dict[str, Any]:
        """Optimize memory usage for specific service"""
        try:
            logger.info(f"Optimizing memory usage for service: {service_name}")
            
            # Analyze service memory patterns
            memory_analysis = self._analyze_service_memory_patterns(service_name, data_objects)
            
            # Apply memory optimizations
            optimization_results = await self._apply_memory_optimizations(service_name, data_objects, memory_analysis)
            
            # Calculate memory efficiency
            memory_efficiency = self._calculate_memory_efficiency(optimization_results)
            
            return {
                "service_name": service_name,
                "original_objects": len(data_objects),
                "optimized_objects": len(optimization_results["allocated_objects"]),
                "memory_efficiency": memory_efficiency,
                "memory_analysis": memory_analysis,
                "optimization_results": optimization_results
            }
            
        except Exception as e:
            logger.error(f"Service memory optimization failed for {service_name}", error=str(e))
            raise

    def _analyze_service_memory_patterns(self, service_name: str, data_objects: List[Any]) -> Dict[str, Any]:
        """Analyze memory usage patterns for specific service"""
        analysis = {
            "service_name": service_name,
            "total_objects": len(data_objects),
            "total_size_bytes": sum(sys.getsizeof(obj) for obj in data_objects),
            "average_object_size": 0,
            "memory_intensive_objects": 0,
            "recommendations": []
        }
        
        # Calculate average object size
        if data_objects:
            analysis["average_object_size"] = analysis["total_size_bytes"] / len(data_objects)
        
        # Identify memory-intensive objects
        for obj in data_objects:
            if sys.getsizeof(obj) > 1024 * 1024:  # Objects larger than 1MB
                analysis["memory_intensive_objects"] += 1
        
        # Generate recommendations
        if analysis["average_object_size"] > 512 * 1024:  # Average size > 512KB
            analysis["recommendations"].append("Consider using memory pools for large objects")
        
        if analysis["memory_intensive_objects"] > len(data_objects) * 0.3:
            analysis["recommendations"].append("High proportion of memory-intensive objects detected")
        
        return analysis

    async def _apply_memory_optimizations(self, service_name: str, data_objects: List[Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply memory optimizations to service data"""
        optimization_results = {
            "allocated_objects": [],
            "pool_allocations": 0,
            "cache_allocations": 0,
            "memory_savings": 0
        }
        
        for obj in data_objects:
            # Optimize memory allocation
            allocation_id = await self.optimize_memory_allocation(service_name, obj)
            optimization_results["allocated_objects"].append(allocation_id)
            
            # Track allocation type
            if allocation_id.startswith("pool_block_"):
                optimization_results["pool_allocations"] += 1
            else:
                optimization_results["cache_allocations"] += 1
        
        return optimization_results

    def _calculate_memory_efficiency(self, optimization_results: Dict[str, Any]) -> float:
        """Calculate memory efficiency score"""
        total_allocations = len(optimization_results["allocated_objects"])
        pool_allocations = optimization_results["pool_allocations"]
        
        if total_allocations > 0:
            efficiency = (pool_allocations / total_allocations) * 100
        else:
            efficiency = 0.0
        
        return efficiency

    async def cleanup_unused_memory(self):
        """Cleanup unused memory from cache and pools"""
        try:
            logger.info("Cleaning up unused memory")
            
            current_time = datetime.now()
            cleanup_threshold = timedelta(hours=1)  # Clean up memory not accessed for 1 hour
            
            # Cleanup cache
            cache_keys_to_remove = []
            for key, entry in self.shared_memory_cache.items():
                if current_time - entry["last_accessed"] > cleanup_threshold:
                    cache_keys_to_remove.append(key)
            
            for key in cache_keys_to_remove:
                del self.shared_memory_cache[key]
            
            # Cleanup pools (this would be more sophisticated in a real implementation)
            for pool_name, pool in self.memory_pools.items():
                # Reset access counts for long-unused blocks
                for block in pool.available_blocks:
                    if current_time - block.last_accessed > cleanup_threshold:
                        block.access_count = 0
            
            logger.info(f"Memory cleanup completed, removed {len(cache_keys_to_remove)} cache entries")
            
            return {
                "cache_entries_removed": len(cache_keys_to_remove),
                "cleanup_threshold": cleanup_threshold,
                "remaining_cache_entries": len(self.shared_memory_cache)
            }
            
        except Exception as e:
            logger.error(f"Memory cleanup failed", error=str(e))
            raise

    async def get_memory_optimization_metrics(self) -> Dict[str, Any]:
        """Get comprehensive memory optimization metrics"""
        try:
            current_usage = await self.get_memory_usage()
            
            # Calculate optimization metrics
            total_allocations = self.optimization_metrics["total_allocations"]
            pool_hits = self.optimization_metrics["pool_hits"]
            cache_hits = self.optimization_metrics["cache_hits"]
            
            pool_hit_rate = (pool_hits / total_allocations * 100) if total_allocations > 0 else 0
            cache_hit_rate = (cache_hits / total_allocations * 100) if total_allocations > 0 else 0
            
            return {
                "current_usage": {
                    "total_memory_gb": current_usage.total_memory / (1024**3),
                    "used_memory_gb": current_usage.used_memory / (1024**3),
                    "available_memory_gb": current_usage.available_memory / (1024**3),
                    "memory_percent": current_usage.memory_percent,
                    "shared_memory_mb": current_usage.shared_memory / (1024**2),
                    "cached_memory_mb": current_usage.cached_memory / (1024**2)
                },
                "optimization_metrics": {
                    **self.optimization_metrics,
                    "pool_hit_rate": pool_hit_rate,
                    "cache_hit_rate": cache_hit_rate,
                    "memory_efficiency": (pool_hit_rate + cache_hit_rate) / 2
                },
                "pool_status": {
                    pool_name: {
                        "total_blocks": pool.pool_size,
                        "available_blocks": len(pool.available_blocks),
                        "allocated_blocks": len(pool.allocated_blocks)
                    }
                    for pool_name, pool in self.memory_pools.items()
                },
                "cache_status": {
                    "total_entries": len(self.shared_memory_cache),
                    "total_size_mb": sum(entry["size_bytes"] for entry in self.shared_memory_cache.values()) / (1024**2)
                }
            }
            
        except Exception as e:
            logger.error(f"Memory optimization metrics retrieval failed", error=str(e))
            raise

    async def start_memory_monitoring(self):
        """Start continuous memory monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.memory_monitor_thread = threading.Thread(target=self._memory_monitoring_loop)
            self.memory_monitor_thread.start()
            logger.info("Memory monitoring started")

    def _memory_monitoring_loop(self):
        """Memory monitoring loop"""
        while self.monitoring_active:
            try:
                # Monitor memory usage
                asyncio.create_task(self.get_memory_usage())
                
                # Cleanup unused memory periodically
                asyncio.create_task(self.cleanup_unused_memory())
                
                # Sleep for monitoring interval
                threading.Event().wait(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logger.error(f"Memory monitoring loop error", error=str(e))
                threading.Event().wait(60)  # Wait longer on error

    async def stop_memory_monitoring(self):
        """Stop memory monitoring"""
        self.monitoring_active = False
        if self.memory_monitor_thread:
            self.memory_monitor_thread.join()
        logger.info("Memory monitoring stopped")

    async def cleanup(self):
        """Cleanup memory optimizer resources"""
        try:
            await self.stop_memory_monitoring()
            await self.cleanup_unused_memory()
            logger.info("Memory Optimizer cleanup completed")
        except Exception as e:
            logger.error(f"Memory Optimizer cleanup failed", error=str(e))

# Global memory optimizer instance
memory_optimizer = MemoryOptimizer()
