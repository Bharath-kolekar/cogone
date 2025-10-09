"""
CPU Optimization Engine for CognOmega System

This module implements advanced CPU optimization techniques including
async processing, CPU pooling, load balancing, and intelligent task scheduling.
"""

import structlog
import asyncio
import multiprocessing
import os
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
import time

logger = structlog.get_logger(__name__)

class CPUPriority(Enum):
    """CPU task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class CPUTask:
    """CPU task definition"""
    task_id: str
    function: Callable
    args: tuple
    kwargs: dict
    priority: CPUPriority
    cpu_cores_required: int
    estimated_duration: float
    created_at: datetime

@dataclass
class CPUUsage:
    """CPU usage metrics"""
    total_usage: float
    per_core_usage: List[float]
    load_average: float
    temperature: Optional[float]
    frequency: float
    timestamp: datetime

class CPUOptimizer:
    """Advanced CPU optimization engine"""
    
    def __init__(self, max_workers: Optional[int] = None):
        # Zero-cost mode: limit workers based on settings
        from app.core.config import settings
        if getattr(settings, 'ZERO_COST_MODE', False):
            default_workers = min(4, multiprocessing.cpu_count())
        else:
            default_workers = min(32, multiprocessing.cpu_count())
        
        self.max_workers = max_workers or default_workers
        self.total_cores = multiprocessing.cpu_count()
        
        # Task queues by priority
        self.task_queues = {
            priority: asyncio.Queue() for priority in CPUPriority
        }
        
        # CPU pools (ensure at least one worker per pool)
        half = max(1, self.max_workers // 2)
        self.io_pool = ThreadPoolExecutor(max_workers=half)
        self.cpu_pool = ProcessPoolExecutor(max_workers=half)
        self.background_pool = ThreadPoolExecutor(max_workers=2)
        
        # CPU monitoring
        self.cpu_usage_history: List[CPUUsage] = []
        self.optimization_metrics = {
            "tasks_processed": 0,
            "average_task_time": 0.0,
            "cpu_efficiency": 0.0,
            "load_balance_score": 0.0
        }
        
        # Intelligent scheduling
        self.cpu_affinity_map: Dict[str, List[int]] = {}
        self.task_scheduler = None
        
        logger.info(f"CPU Optimizer initialized with {self.total_cores} cores, {self.max_workers} workers")

    async def optimize_async_processing(self, tasks: List[CPUTask]) -> List[Any]:
        """Optimize async processing with intelligent task scheduling"""
        try:
            logger.info(f"Optimizing async processing for {len(tasks)} tasks")
            
            # Sort tasks by priority and CPU requirements
            sorted_tasks = self._sort_tasks_by_priority(tasks)
            
            # Group tasks for optimal CPU utilization
            task_groups = self._group_tasks_for_cpu_optimization(sorted_tasks)
            
            # Execute tasks with optimized scheduling
            results = []
            for group in task_groups:
                group_results = await self._execute_task_group_optimized(group)
                results.extend(group_results)
            
            # Update optimization metrics
            self._update_cpu_optimization_metrics(tasks, results)
            
            logger.info(f"Async processing optimization completed, {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Async processing optimization failed", error=str(e))
            raise

    def _sort_tasks_by_priority(self, tasks: List[CPUTask]) -> List[CPUTask]:
        """Sort tasks by priority and CPU efficiency"""
        def priority_key(task: CPUTask) -> tuple:
            # Sort by priority (lower number = higher priority)
            # Then by CPU efficiency (fewer cores = higher efficiency)
            efficiency_score = 1.0 / max(1, task.cpu_cores_required)
            return (task.priority.value, -efficiency_score)
        
        return sorted(tasks, key=priority_key)

    def _group_tasks_for_cpu_optimization(self, tasks: List[CPUTask]) -> List[List[CPUTask]]:
        """Group tasks for optimal CPU utilization"""
        groups = []
        current_group = []
        current_cpu_usage = 0
        
        for task in tasks:
            # Check if task fits in current group
            if current_cpu_usage + task.cpu_cores_required <= self.total_cores:
                current_group.append(task)
                current_cpu_usage += task.cpu_cores_required
            else:
                # Start new group
                if current_group:
                    groups.append(current_group)
                current_group = [task]
                current_cpu_usage = task.cpu_cores_required
        
        # Add remaining group
        if current_group:
            groups.append(current_group)
        
        return groups

    async def _execute_task_group_optimized(self, task_group: List[CPUTask]) -> List[Any]:
        """Execute task group with optimized CPU utilization"""
        try:
            # Create coroutines for parallel execution
            coroutines = []
            for task in task_group:
                coroutine = self._execute_single_task_optimized(task)
                coroutines.append(coroutine)
            
            # Execute all tasks in parallel
            results = await asyncio.gather(*coroutines, return_exceptions=True)
            
            # Handle exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Task {task_group[i].task_id} failed", error=str(result))
                    processed_results.append(None)
                else:
                    processed_results.append(result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Task group execution failed", error=str(e))
            raise

    async def _execute_single_task_optimized(self, task: CPUTask) -> Any:
        """Execute single task with CPU optimization"""
        try:
            start_time = time.time()
            
            # Set CPU affinity if available
            if hasattr(os, 'sched_setaffinity'):
                try:
                    # Use specific cores for this task
                    cores = self._get_optimal_cores_for_task(task)
                    os.sched_setaffinity(0, cores)
                except Exception:
                    pass  # Continue without affinity if not possible
            
            # Execute task in appropriate pool
            if task.priority == CPUPriority.BACKGROUND:
                # Use background pool for non-critical tasks
                result = await asyncio.get_event_loop().run_in_executor(
                    self.background_pool, task.function, *task.args, **task.kwargs
                )
            elif task.cpu_cores_required > 2:
                # Use process pool for CPU-intensive tasks
                result = await asyncio.get_event_loop().run_in_executor(
                    self.cpu_pool, task.function, *task.args, **task.kwargs
                )
            else:
                # Use thread pool for I/O-bound tasks
                result = await asyncio.get_event_loop().run_in_executor(
                    self.io_pool, task.function, *task.args, **task.kwargs
                )
            
            # Record execution time
            execution_time = time.time() - start_time
            self._record_task_execution(task, execution_time)
            
            return result
            
        except Exception as e:
            logger.error(f"Single task execution failed", error=str(e))
            raise

    def _get_optimal_cores_for_task(self, task: CPUTask) -> List[int]:
        """Get optimal CPU cores for task execution"""
        # Simple round-robin assignment
        # In a real implementation, this would be more sophisticated
        start_core = hash(task.task_id) % self.total_cores
        cores = list(range(start_core, min(start_core + task.cpu_cores_required, self.total_cores)))
        return cores

    def _record_task_execution(self, task: CPUTask, execution_time: float):
        """Record task execution metrics"""
        # Update metrics
        self.optimization_metrics["tasks_processed"] += 1
        
        # Update average task time
        total_tasks = self.optimization_metrics["tasks_processed"]
        current_avg = self.optimization_metrics["average_task_time"]
        new_avg = ((current_avg * (total_tasks - 1)) + execution_time) / total_tasks
        self.optimization_metrics["average_task_time"] = new_avg

    async def monitor_cpu_usage(self) -> CPUUsage:
        """Monitor current CPU usage with optimization insights"""
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            # Windows-safe load average
            load_avg = 0.0
            getloadavg = getattr(os, 'getloadavg', None)
            if callable(getloadavg):
                try:
                    load_avg = getloadavg()[0]
                except Exception:
                    load_avg = 0.0
            
            # Get CPU frequency
            cpu_freq = psutil.cpu_freq()
            frequency = cpu_freq.current if cpu_freq else 0.0
            
            # Get CPU temperature if available
            temperature = None
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            temperature = entries[0].current
                            break
            except Exception:
                pass
            
            cpu_usage = CPUUsage(
                total_usage=sum(cpu_percent) / len(cpu_percent),
                per_core_usage=cpu_percent,
                load_average=load_avg,
                temperature=temperature,
                frequency=frequency,
                timestamp=datetime.now()
            )
            
            # Store in history
            self.cpu_usage_history.append(cpu_usage)
            
            # Keep only recent history
            if len(self.cpu_usage_history) > 100:
                self.cpu_usage_history = self.cpu_usage_history[-100:]
            
            return cpu_usage
            
        except Exception as e:
            logger.error(f"CPU monitoring failed", error=str(e))
            raise

    def _update_cpu_optimization_metrics(self, tasks: List[CPUTask], results: List[Any]):
        """Update CPU optimization metrics"""
        try:
            # Calculate CPU efficiency
            total_cpu_required = sum(task.cpu_cores_required for task in tasks)
            actual_cpu_used = min(total_cpu_required, self.total_cores)
            cpu_efficiency = (actual_cpu_used / self.total_cores) * 100
            self.optimization_metrics["cpu_efficiency"] = cpu_efficiency
            
            # Calculate load balance score
            if self.cpu_usage_history:
                recent_usage = self.cpu_usage_history[-5:]  # Last 5 measurements
                avg_per_core = [sum(usage.per_core_usage[i] for usage in recent_usage) / len(recent_usage) 
                              for i in range(self.total_cores)]
                
                # Calculate variance (lower variance = better balance)
                mean_usage = sum(avg_per_core) / len(avg_per_core)
                variance = sum((usage - mean_usage) ** 2 for usage in avg_per_core) / len(avg_per_core)
                load_balance_score = max(0, 100 - (variance / 10))  # Convert to 0-100 scale
                self.optimization_metrics["load_balance_score"] = load_balance_score
            
        except Exception as e:
            logger.error(f"CPU optimization metrics update failed", error=str(e))

    async def get_optimization_recommendations(self) -> Dict[str, Any]:
        """Get CPU optimization recommendations"""
        try:
            current_usage = await self.monitor_cpu_usage()
            
            recommendations = {
                "current_status": {
                    "total_usage": current_usage.total_usage,
                    "load_average": current_usage.load_average,
                    "temperature": current_usage.temperature,
                    "frequency": current_usage.frequency
                },
                "optimization_metrics": self.optimization_metrics,
                "recommendations": []
            }
            
            # Generate recommendations based on current state
            if current_usage.total_usage > 80:
                recommendations["recommendations"].append({
                    "type": "cpu_scaling",
                    "message": "High CPU usage detected. Consider scaling up or optimizing tasks.",
                    "priority": "high"
                })
            
            if current_usage.load_average > self.total_cores * 0.8:
                recommendations["recommendations"].append({
                    "type": "load_balancing",
                    "message": "High load average. Consider better task distribution.",
                    "priority": "medium"
                })
            
            if current_usage.temperature and current_usage.temperature > 80:
                recommendations["recommendations"].append({
                    "type": "thermal_management",
                    "message": "High CPU temperature. Consider thermal throttling or cooling.",
                    "priority": "critical"
                })
            
            if self.optimization_metrics["cpu_efficiency"] < 70:
                recommendations["recommendations"].append({
                    "type": "efficiency_improvement",
                    "message": "Low CPU efficiency. Consider task optimization or resource allocation.",
                    "priority": "medium"
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"CPU optimization recommendations failed", error=str(e))
            raise

    async def optimize_service_cpu_usage(self, service_name: str, tasks: List[CPUTask]) -> Dict[str, Any]:
        """Optimize CPU usage for specific service"""
        try:
            logger.info(f"Optimizing CPU usage for service: {service_name}")
            
            # Analyze service-specific CPU patterns
            service_analysis = self._analyze_service_cpu_patterns(service_name, tasks)
            
            # Apply service-specific optimizations
            optimized_tasks = await self._apply_service_optimizations(service_name, tasks, service_analysis)
            
            # Execute optimized tasks
            results = await self.optimize_async_processing(optimized_tasks)
            
            # Calculate optimization impact
            optimization_impact = self._calculate_optimization_impact(tasks, optimized_tasks, results)
            
            return {
                "service_name": service_name,
                "original_tasks": len(tasks),
                "optimized_tasks": len(optimized_tasks),
                "results_count": len(results),
                "optimization_impact": optimization_impact,
                "recommendations": service_analysis.get("recommendations", [])
            }
            
        except Exception as e:
            logger.error(f"Service CPU optimization failed for {service_name}", error=str(e))
            raise

    def _analyze_service_cpu_patterns(self, service_name: str, tasks: List[CPUTask]) -> Dict[str, Any]:
        """Analyze CPU usage patterns for specific service"""
        analysis = {
            "service_name": service_name,
            "total_tasks": len(tasks),
            "total_cpu_required": sum(task.cpu_cores_required for task in tasks),
            "priority_distribution": {},
            "cpu_intensive_tasks": 0,
            "io_intensive_tasks": 0,
            "recommendations": []
        }
        
        # Analyze priority distribution
        for task in tasks:
            priority = task.priority.value
            analysis["priority_distribution"][priority] = analysis["priority_distribution"].get(priority, 0) + 1
        
        # Analyze task types
        for task in tasks:
            if task.cpu_cores_required > 2:
                analysis["cpu_intensive_tasks"] += 1
            else:
                analysis["io_intensive_tasks"] += 1
        
        # Generate recommendations
        if analysis["cpu_intensive_tasks"] > analysis["io_intensive_tasks"]:
            analysis["recommendations"].append("Consider using process pool for CPU-intensive tasks")
        
        if analysis["total_cpu_required"] > self.total_cores:
            analysis["recommendations"].append("Consider task batching or priority optimization")
        
        return analysis

    async def _apply_service_optimizations(self, service_name: str, tasks: List[CPUTask], analysis: Dict[str, Any]) -> List[CPUTask]:
        """Apply service-specific optimizations"""
        optimized_tasks = []
        
        for task in tasks:
            # Create optimized version of task
            optimized_task = CPUTask(
                task_id=task.task_id,
                function=task.function,
                args=task.args,
                kwargs=task.kwargs,
                priority=self._optimize_task_priority(task, analysis),
                cpu_cores_required=self._optimize_cpu_requirements(task, analysis),
                estimated_duration=task.estimated_duration,
                created_at=task.created_at
            )
            optimized_tasks.append(optimized_task)
        
        return optimized_tasks

    def _optimize_task_priority(self, task: CPUTask, analysis: Dict[str, Any]) -> CPUPriority:
        """Optimize task priority based on service analysis"""
        # Implement priority optimization logic
        if task.cpu_cores_required > 4:
            return CPUPriority.HIGH  # CPU-intensive tasks get higher priority
        elif task.estimated_duration > 10:
            return CPUPriority.BACKGROUND  # Long-running tasks go to background
        else:
            return task.priority  # Keep original priority

    def _optimize_cpu_requirements(self, task: CPUTask, analysis: Dict[str, Any]) -> int:
        """Optimize CPU requirements based on service analysis"""
        # Implement CPU requirement optimization
        if task.cpu_cores_required > 4 and analysis["total_cpu_required"] > self.total_cores:
            return min(task.cpu_cores_required, 4)  # Cap CPU requirements
        else:
            return task.cpu_cores_required

    def _calculate_optimization_impact(self, original_tasks: List[CPUTask], optimized_tasks: List[CPUTask], results: List[Any]) -> Dict[str, Any]:
        """Calculate optimization impact"""
        original_cpu = sum(task.cpu_cores_required for task in original_tasks)
        optimized_cpu = sum(task.cpu_cores_required for task in optimized_tasks)
        
        cpu_reduction = ((original_cpu - optimized_cpu) / original_cpu) * 100 if original_cpu > 0 else 0
        
        return {
            "cpu_reduction_percentage": cpu_reduction,
            "original_cpu_required": original_cpu,
            "optimized_cpu_required": optimized_cpu,
            "tasks_completed": len([r for r in results if r is not None]),
            "optimization_success": True
        }

    async def get_cpu_optimization_metrics(self) -> Dict[str, Any]:
        """Get comprehensive CPU optimization metrics"""
        try:
            current_usage = await self.monitor_cpu_usage()
            
            return {
                "current_usage": {
                    "total_usage": current_usage.total_usage,
                    "per_core_usage": current_usage.per_core_usage,
                    "load_average": current_usage.load_average,
                    "temperature": current_usage.temperature,
                    "frequency": current_usage.frequency
                },
                "optimization_metrics": self.optimization_metrics,
                "system_info": {
                    "total_cores": self.total_cores,
                    "max_workers": self.max_workers,
                    "monitoring_history_length": len(self.cpu_usage_history)
                },
                "recommendations": await self.get_optimization_recommendations()
            }
            
        except Exception as e:
            logger.error(f"CPU optimization metrics retrieval failed", error=str(e))
            raise

    def get_cpu_metrics(self) -> Dict[str, Any]:
        """
        Get current CPU metrics - REAL IMPLEMENTATION
        
        Returns actual CPU usage, worker count, and optimization metrics
        """
        try:
            import psutil
            
            # Get real CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1, percpu=False)
            cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
            cpu_count = psutil.cpu_count(logical=True)
            cpu_count_physical = psutil.cpu_count(logical=False)
            
            # Get load average (Unix-like systems)
            try:
                load_avg = psutil.getloadavg()
                load_1min, load_5min, load_15min = load_avg
            except (AttributeError, OSError):
                # Windows doesn't have getloadavg
                load_1min = load_5min = load_15min = cpu_percent / 100.0
            
            # Get CPU frequency
            try:
                freq = psutil.cpu_freq()
                current_freq = freq.current if freq else 0
                max_freq = freq.max if freq else 0
            except:
                current_freq = max_freq = 0
            
            metrics = {
                "cpu_usage_percent": round(cpu_percent, 1),
                "cpu_per_core": [round(c, 1) for c in cpu_per_core] if cpu_per_core else [],
                "cpu_count_logical": cpu_count,
                "cpu_count_physical": cpu_count_physical,
                "load_average_1min": round(load_1min, 2),
                "load_average_5min": round(load_5min, 2),
                "load_average_15min": round(load_15min, 2),
                "frequency_mhz": round(current_freq, 0) if current_freq else 0,
                "frequency_max_mhz": round(max_freq, 0) if max_freq else 0,
                "worker_count": self.max_workers,
                "total_cores": self.total_cores,
                "tasks_processed": self.optimization_metrics.get("tasks_processed", 0),
                "cpu_efficiency": round(self.optimization_metrics.get("cpu_efficiency", 0.0), 2),
                "timestamp": datetime.now().isoformat()
            }
            
            return metrics
            
        except ImportError:
            logger.warning("psutil not installed for get_cpu_metrics")
            return {
                "worker_count": self.max_workers,
                "total_cores": self.total_cores,
                "note": "Install psutil for detailed CPU metrics: pip install psutil"
            }
        except Exception as e:
            logger.error("Error getting CPU metrics", error=str(e))
            return {
                "worker_count": self.max_workers,
                "total_cores": self.total_cores,
                "error": str(e)
            }

    def _resize_thread_pool(self, new_size: int):
        """
        Resize thread pool for dynamic scaling
        Note: ThreadPoolExecutor doesn't support dynamic resizing,
        so we log the request for monitoring purposes
        """
        logger.info("Thread pool resize requested", 
                   current_size=self.max_workers, 
                   requested_size=new_size,
                   note="ThreadPoolExecutor does not support dynamic resizing")
        # In production, you would need to implement pool recreation
        # or use a custom thread pool implementation that supports resizing

    async def cleanup(self):
        """Cleanup resources"""
        try:
            self.io_pool.shutdown(wait=True)
            self.cpu_pool.shutdown(wait=True)
            self.background_pool.shutdown(wait=True)
            logger.info("CPU Optimizer cleanup completed")
        except Exception as e:
            logger.error(f"CPU Optimizer cleanup failed", error=str(e))

# Global CPU optimizer instance
cpu_optimizer = CPUOptimizer()

async def get_cpu_performance() -> Dict[str, Any]:
    """Get current CPU performance metrics"""
    try:
        cpu_usage = await cpu_optimizer.monitor_cpu_usage()
        optimization_metrics = await cpu_optimizer.get_cpu_optimization_metrics()
        
        return {
            "cpu_usage": {
                "total_usage": cpu_usage.total_usage,
                "per_core_usage": cpu_usage.per_core_usage,
                "load_average": cpu_usage.load_average,
                "temperature": cpu_usage.temperature,
                "frequency": cpu_usage.frequency
            },
            "optimization_metrics": optimization_metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get CPU performance metrics", error=str(e))
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }