"""
Performance Architecture Core Module

This module implements advanced performance architecture optimizations
following standard architecture principles and performance best practices.
"""

import asyncio
import time
import psutil
import gc
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import structlog
from functools import wraps
import weakref
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
from queue import Queue, Empty
import resource
import sys

logger = structlog.get_logger(__name__)

class PerformanceLevel(Enum):
    """Performance optimization levels"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"

class ResourceType(Enum):
    """Resource types for monitoring"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    DATABASE = "database"

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: float = field(default_factory=time.time)
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_io: float = 0.0
    network_io: float = 0.0
    response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    active_connections: int = 0
    queue_size: int = 0

@dataclass
class ResourceLimit:
    """Resource limit configuration"""
    resource_type: ResourceType
    warning_threshold: float
    critical_threshold: float
    max_limit: float
    auto_scaling_enabled: bool = True

class PerformanceMonitor:
    """Advanced performance monitoring system"""
    
    def __init__(self, performance_level: PerformanceLevel = PerformanceLevel.ADVANCED):
        self.performance_level = performance_level
        self.metrics_history: List[PerformanceMetrics] = []
        self.resource_limits: Dict[ResourceType, ResourceLimit] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.monitoring_active = False
        self._setup_resource_limits()
        
    def _setup_resource_limits(self):
        """Setup resource limits based on performance level"""
        if self.performance_level == PerformanceLevel.BASIC:
            self.resource_limits = {
                ResourceType.CPU: ResourceLimit(ResourceType.CPU, 70.0, 85.0, 95.0),
                ResourceType.MEMORY: ResourceLimit(ResourceType.MEMORY, 80.0, 90.0, 95.0),
            }
        elif self.performance_level == PerformanceLevel.INTERMEDIATE:
            self.resource_limits = {
                ResourceType.CPU: ResourceLimit(ResourceType.CPU, 60.0, 75.0, 90.0),
                ResourceType.MEMORY: ResourceLimit(ResourceType.MEMORY, 70.0, 85.0, 95.0),
                ResourceType.DISK: ResourceLimit(ResourceType.DISK, 80.0, 90.0, 95.0),
            }
        elif self.performance_level == PerformanceLevel.ADVANCED:
            self.resource_limits = {
                ResourceType.CPU: ResourceLimit(ResourceType.CPU, 50.0, 70.0, 85.0),
                ResourceType.MEMORY: ResourceLimit(ResourceType.MEMORY, 60.0, 80.0, 90.0),
                ResourceType.DISK: ResourceLimit(ResourceType.DISK, 70.0, 85.0, 95.0),
                ResourceType.NETWORK: ResourceLimit(ResourceType.NETWORK, 80.0, 90.0, 95.0),
            }
        else:  # ENTERPRISE
            self.resource_limits = {
                ResourceType.CPU: ResourceLimit(ResourceType.CPU, 40.0, 60.0, 80.0),
                ResourceType.MEMORY: ResourceLimit(ResourceType.MEMORY, 50.0, 70.0, 85.0),
                ResourceType.DISK: ResourceLimit(ResourceType.DISK, 60.0, 80.0, 90.0),
                ResourceType.NETWORK: ResourceLimit(ResourceType.NETWORK, 70.0, 85.0, 95.0),
                ResourceType.DATABASE: ResourceLimit(ResourceType.DATABASE, 80.0, 90.0, 95.0),
            }
    
    async def start_monitoring(self, interval: float = 1.0):
        """Start performance monitoring"""
        self.monitoring_active = True
        logger.info("Starting performance monitoring", level=self.performance_level.value)
        
        while self.monitoring_active:
            try:
                metrics = await self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                await self._check_resource_limits(metrics)
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error("Error in performance monitoring", error=str(e))
                await asyncio.sleep(interval)
    
    async def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        logger.info("Performance monitoring stopped")
    
    async def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        metrics = PerformanceMetrics()
        
        try:
            # CPU usage
            metrics.cpu_usage = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            metrics.memory_usage = memory.percent
            
            # Disk I/O
            disk = psutil.disk_io_counters()
            if disk:
                metrics.disk_io = (disk.read_bytes + disk.write_bytes) / 1024 / 1024  # MB
            
            # Network I/O
            network = psutil.net_io_counters()
            if network:
                metrics.network_io = (network.bytes_sent + network.bytes_recv) / 1024 / 1024  # MB
            
            # Active connections
            metrics.active_connections = len(psutil.net_connections())
            
        except Exception as e:
            logger.error("Error collecting metrics", error=str(e))
        
        return metrics
    
    async def _check_resource_limits(self, metrics: PerformanceMetrics):
        """Check resource limits and generate alerts"""
        for resource_type, limit in self.resource_limits.items():
            current_usage = getattr(metrics, f"{resource_type.value}_usage", 0)
            
            if current_usage >= limit.critical_threshold:
                alert = {
                    "type": "critical",
                    "resource": resource_type.value,
                    "usage": current_usage,
                    "threshold": limit.critical_threshold,
                    "timestamp": metrics.timestamp
                }
                self.alerts.append(alert)
                logger.critical("Critical resource usage", **alert)
                
            elif current_usage >= limit.warning_threshold:
                alert = {
                    "type": "warning",
                    "resource": resource_type.value,
                    "usage": current_usage,
                    "threshold": limit.warning_threshold,
                    "timestamp": metrics.timestamp
                }
                self.alerts.append(alert)
                logger.warning("Resource usage warning", **alert)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {"status": "no_data"}
        
        latest = self.metrics_history[-1]
        avg_cpu = sum(m.cpu_usage for m in self.metrics_history[-10:]) / min(10, len(self.metrics_history))
        avg_memory = sum(m.memory_usage for m in self.metrics_history[-10:]) / min(10, len(self.metrics_history))
        
        return {
            "status": "monitoring",
            "latest_metrics": {
                "cpu_usage": latest.cpu_usage,
                "memory_usage": latest.memory_usage,
                "active_connections": latest.active_connections,
            },
            "average_metrics": {
                "cpu_usage": avg_cpu,
                "memory_usage": avg_memory,
            },
            "alerts_count": len([a for a in self.alerts if a["type"] == "critical"]),
            "warnings_count": len([a for a in self.alerts if a["type"] == "warning"]),
        }

class MemoryOptimizer:
    """Advanced memory optimization system"""
    
    def __init__(self):
        self.memory_pools: Dict[str, Queue] = {}
        self.object_registry: Dict[str, weakref.ref] = {}
        self.gc_threshold = 1000
        self.last_gc_count = 0
        
    def create_memory_pool(self, name: str, size: int = 100):
        """Create a memory pool for object reuse"""
        self.memory_pools[name] = Queue(maxsize=size)
        logger.info("Created memory pool", name=name, size=size)
    
    def get_from_pool(self, pool_name: str) -> Optional[Any]:
        """Get object from memory pool"""
        if pool_name in self.memory_pools:
            try:
                return self.memory_pools[pool_name].get_nowait()
            except Empty:
                pass
        return None
    
    def return_to_pool(self, pool_name: str, obj: Any):
        """Return object to memory pool"""
        if pool_name in self.memory_pools:
            try:
                self.memory_pools[pool_name].put_nowait(obj)
            except:
                pass  # Pool full, object will be garbage collected
    
    def register_object(self, name: str, obj: Any):
        """Register object for tracking"""
        self.object_registry[name] = weakref.ref(obj)
    
    def cleanup_dead_objects(self):
        """Clean up dead object references"""
        dead_refs = []
        for name, ref in self.object_registry.items():
            if ref() is None:
                dead_refs.append(name)
        
        for name in dead_refs:
            del self.object_registry[name]
        
        if dead_refs:
            logger.info("Cleaned up dead object references", count=len(dead_refs))
    
    def optimize_memory(self):
        """Perform memory optimization"""
        # Force garbage collection
        collected = gc.collect()
        
        # Clean up dead references
        self.cleanup_dead_objects()
        
        # Set memory limits
        try:
            # Set memory limit to 80% of available memory
            available_memory = psutil.virtual_memory().available
            memory_limit = int(available_memory * 0.8)
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
        except Exception as e:
            logger.error("Failed to set memory limit", error=str(e))
        
        logger.info("Memory optimization completed", collected=collected)

class CPUOptimizer:
    """Advanced CPU optimization system"""
    
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=psutil.cpu_count() * 2)
        self.process_pool = ProcessPoolExecutor(max_workers=psutil.cpu_count())
        self.cpu_affinity_set = False
        
    def set_cpu_affinity(self, cpu_cores: List[int]):
        """Set CPU affinity for the process"""
        try:
            process = psutil.Process()
            process.cpu_affinity(cpu_cores)
            self.cpu_affinity_set = True
            logger.info("CPU affinity set", cores=cpu_cores)
        except Exception as e:
            logger.error("Failed to set CPU affinity", error=str(e))
    
    def optimize_cpu_scheduling(self):
        """Optimize CPU scheduling"""
        try:
            # Set high priority for the process
            process = psutil.Process()
            if hasattr(process, 'nice'):
                process.nice(-10)  # Higher priority
        except Exception as e:
            logger.error("Failed to optimize CPU scheduling", error=str(e))
    
    def submit_cpu_intensive_task(self, func: Callable, *args, **kwargs):
        """Submit CPU intensive task to process pool"""
        return self.process_pool.submit(func, *args, **kwargs)
    
    def submit_io_bound_task(self, func: Callable, *args, **kwargs):
        """Submit I/O bound task to thread pool"""
        return self.thread_pool.submit(func, *args, **kwargs)
    
    def shutdown(self):
        """Shutdown CPU optimizer"""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)
        logger.info("CPU optimizer shutdown")

class PerformanceProfiler:
    """Performance profiling and optimization system"""
    
    def __init__(self):
        self.profiles: Dict[str, List[float]] = {}
        self.active_profiles: Dict[str, float] = {}
        
    def start_profile(self, name: str):
        """Start profiling a function or operation"""
        self.active_profiles[name] = time.perf_counter()
    
    def end_profile(self, name: str) -> float:
        """End profiling and return duration"""
        if name in self.active_profiles:
            duration = time.perf_counter() - self.active_profiles[name]
            del self.active_profiles[name]
            
            if name not in self.profiles:
                self.profiles[name] = []
            self.profiles[name].append(duration)
            
            return duration
        return 0.0
    
    def profile_function(self, name: Optional[str] = None):
        """Decorator for profiling functions"""
        def decorator(func):
            profile_name = name or f"{func.__module__}.{func.__name__}"
            
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                self.start_profile(profile_name)
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = self.end_profile(profile_name)
                    if duration > 1.0:  # Log slow operations
                        logger.warning("Slow operation detected", function=profile_name, duration=duration)
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                self.start_profile(profile_name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = self.end_profile(profile_name)
                    if duration > 1.0:  # Log slow operations
                        logger.warning("Slow operation detected", function=profile_name, duration=duration)
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        
        return decorator
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get profiling summary"""
        summary = {}
        for name, durations in self.profiles.items():
            if durations:
                summary[name] = {
                    "count": len(durations),
                    "total": sum(durations),
                    "average": sum(durations) / len(durations),
                    "min": min(durations),
                    "max": max(durations),
                }
        return summary

class PerformanceArchitecture:
    """Main performance architecture orchestrator"""
    
    def __init__(self, performance_level: PerformanceLevel = PerformanceLevel.ADVANCED):
        self.performance_level = performance_level
        self.monitor = PerformanceMonitor(performance_level)
        self.memory_optimizer = MemoryOptimizer()
        self.cpu_optimizer = CPUOptimizer()
        self.profiler = PerformanceProfiler()
        self.optimization_active = False
        
    async def initialize(self):
        """Initialize performance architecture"""
        logger.info("Initializing performance architecture", level=self.performance_level.value)
        
        # Setup memory pools
        self.memory_optimizer.create_memory_pool("database_connections", 20)
        self.memory_optimizer.create_memory_pool("http_connections", 50)
        self.memory_optimizer.create_memory_pool("ai_models", 5)
        
        # Optimize CPU
        self.cpu_optimizer.optimize_cpu_scheduling()
        
        # Set CPU affinity if available
        cpu_count = psutil.cpu_count()
        if cpu_count > 4:
            # Use half the cores for the main process
            cores = list(range(cpu_count // 2))
            self.cpu_optimizer.set_cpu_affinity(cores)
        
        # Start monitoring
        asyncio.create_task(self.monitor.start_monitoring())
        
        self.optimization_active = True
        logger.info("Performance architecture initialized")
    
    async def shutdown(self):
        """Shutdown performance architecture"""
        self.optimization_active = False
        
        # Stop monitoring
        await self.monitor.stop_monitoring()
        
        # Shutdown CPU optimizer
        self.cpu_optimizer.shutdown()
        
        logger.info("Performance architecture shutdown")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            "monitoring": self.monitor.get_performance_summary(),
            "profiling": self.profiler.get_profile_summary(),
            "memory_pools": {name: pool.qsize() for name, pool in self.memory_optimizer.memory_pools.items()},
            "object_registry": len(self.memory_optimizer.object_registry),
            "performance_level": self.performance_level.value,
            "optimization_active": self.optimization_active,
        }
    
    async def optimize_performance(self):
        """Perform comprehensive performance optimization"""
        logger.info("Starting performance optimization")
        
        # Memory optimization
        self.memory_optimizer.optimize_memory()
        
        # CPU optimization
        self.cpu_optimizer.optimize_cpu_scheduling()
        
        # Cleanup resources
        self.memory_optimizer.cleanup_dead_objects()
        
        logger.info("Performance optimization completed")

# Global performance architecture instance
performance_architecture = PerformanceArchitecture()

# Performance decorators
def profile_performance(name: Optional[str] = None):
    """Decorator for profiling function performance"""
    return performance_architecture.profiler.profile_function(name)

def optimize_memory(pool_name: Optional[str] = None):
    """Decorator for memory optimization"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get object from pool if available
            if pool_name:
                obj = performance_architecture.memory_optimizer.get_from_pool(pool_name)
                if obj:
                    kwargs['pooled_object'] = obj
            
            result = await func(*args, **kwargs)
            
            # Return object to pool if applicable
            if pool_name and 'pooled_object' in kwargs:
                performance_architecture.memory_optimizer.return_to_pool(
                    pool_name, kwargs['pooled_object']
                )
            
            return result
        return wrapper
    return decorator

def cpu_intensive_task(func):
    """Decorator for CPU intensive tasks"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return performance_architecture.cpu_optimizer.submit_cpu_intensive_task(func, *args, **kwargs)
    return wrapper

def io_bound_task(func):
    """Decorator for I/O bound tasks"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return performance_architecture.cpu_optimizer.submit_io_bound_task(func, *args, **kwargs)
    return wrapper
