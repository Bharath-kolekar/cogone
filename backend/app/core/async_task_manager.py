"""
Global Async Task Manager for CognOmega Platform

This module provides centralized management of async tasks to prevent
RuntimeError: no running event loop issues during module import.
"""

import asyncio
import structlog
from typing import Dict, List, Callable, Any
from datetime import datetime
import threading

logger = structlog.get_logger(__name__)

class AsyncTaskManager:
    """Centralized manager for async task initialization"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._tasks: Dict[str, asyncio.Task] = {}
            self._deferred_initializers: List[Callable] = []
            self._event_loop_started = False
            self._background_tasks_started = False
            logger.info("Async Task Manager initialized")
    
    def register_deferred_initializer(self, name: str, initializer: Callable):
        """Register a deferred initializer to be called when event loop is available"""
        self._deferred_initializers.append((name, initializer))
        logger.info(f"Registered deferred initializer: {name}")
    
    async def start_all_tasks(self):
        """Start all registered async tasks when event loop is available"""
        if self._background_tasks_started:
            return
        
        try:
            logger.info("Starting all async tasks...")
            
            # Start all deferred initializers
            for name, initializer in self._deferred_initializers:
                try:
                    if asyncio.iscoroutinefunction(initializer):
                        task = asyncio.create_task(initializer())
                        self._tasks[name] = task
                        logger.info(f"Started async task: {name}")
                    else:
                        # For non-async initializers, call them directly
                        initializer()
                        logger.info(f"Executed initializer: {name}")
                except Exception as e:
                    logger.error(f"Failed to start task {name}", error=str(e))
            
            self._background_tasks_started = True
            self._event_loop_started = True
            logger.info("All async tasks started successfully")
            
        except Exception as e:
            logger.error("Failed to start async tasks", error=str(e))
    
    async def stop_all_tasks(self):
        """Stop all running async tasks"""
        try:
            for name, task in self._tasks.items():
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                    logger.info(f"Stopped task: {name}")
            
            self._tasks.clear()
            self._background_tasks_started = False
            logger.info("All async tasks stopped")
            
        except Exception as e:
            logger.error("Error stopping tasks", error=str(e))
    
    def is_event_loop_running(self) -> bool:
        """Check if event loop is running"""
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False
    
    async def ensure_tasks_started(self):
        """Ensure all tasks are started (safe to call multiple times)"""
        if not self._background_tasks_started and self.is_event_loop_running():
            await self.start_all_tasks()
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get status of all tasks"""
        return {
            "total_tasks": len(self._tasks),
            "running_tasks": len([t for t in self._tasks.values() if not t.done()]),
            "completed_tasks": len([t for t in self._tasks.values() if t.done()]),
            "background_tasks_started": self._background_tasks_started,
            "event_loop_running": self.is_event_loop_running(),
            "tasks": {
                name: {
                    "done": task.done(),
                    "cancelled": task.cancelled(),
                    "exception": str(task.exception()) if task.done() and task.exception() else None
                }
                for name, task in self._tasks.items()
            }
        }

# Global instance
async_task_manager = AsyncTaskManager()

def register_async_initializer(name: str, initializer: Callable):
    """Convenience function to register async initializers"""
    async_task_manager.register_deferred_initializer(name, initializer)

async def ensure_all_tasks_started():
    """Convenience function to ensure all tasks are started"""
    await async_task_manager.ensure_tasks_started()
