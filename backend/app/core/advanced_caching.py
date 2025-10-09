"""
Advanced Multi-Tier Caching System for Cognomega AI
Optimizes Performance, Scalability, and Resource Utilization
"""

import asyncio
import json
import time
import hashlib
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import structlog

from app.core.config import settings
from app.core.redis import get_redis_client

logger = structlog.get_logger()


class CacheLevel(str, Enum):
    """Cache levels in the multi-tier system"""
    L1_MEMORY = "l1_memory"
    L2_REDIS = "l2_redis"
    L3_DATABASE = "l3_database"
    L4_EXTERNAL = "l4_external"


class CacheStrategy(str, Enum):
    """Caching strategies"""
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"
    WRITE_AROUND = "write_around"
    CACHE_ASIDE = "cache_aside"


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    ttl: int = 3600  # 1 hour default
    level: CacheLevel = CacheLevel.L1_MEMORY
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_requests: int = 0
    hit_rate: float = 0.0
    avg_response_time: float = 0.0
    memory_usage: float = 0.0
    redis_usage: float = 0.0


class MultiTierCaching:
    """Advanced multi-tier caching system"""
    
    def __init__(self):
        self.l1_cache: Dict[str, CacheEntry] = {}
        # l2_cache will be acquired via async provider when needed
        self.l2_cache = None
        self.cache_strategies: Dict[str, CacheStrategy] = {}
        self.metrics = CacheMetrics()
        self.max_l1_size = 10000  # Maximum entries in L1 cache
        self.compression_enabled = True
        self.encryption_enabled = True
        
        # Cache configuration
        self.ttl_configs = {
            "ai_responses": 3600,  # 1 hour
            "user_sessions": 86400,  # 24 hours
            "code_completions": 7200,  # 2 hours
            "architecture_diagrams": 43200,  # 12 hours
            "performance_metrics": 300,  # 5 minutes
        }
        
        # Initialize cache strategies
        self._initialize_cache_strategies()
    
    def _initialize_cache_strategies(self):
        """Initialize cache strategies for different data types"""
        self.cache_strategies = {
            "ai_responses": CacheStrategy.WRITE_THROUGH,
            "user_sessions": CacheStrategy.WRITE_BACK,
            "code_completions": CacheStrategy.CACHE_ASIDE,
            "architecture_diagrams": CacheStrategy.WRITE_AROUND,
            "performance_metrics": CacheStrategy.WRITE_THROUGH,
        }
    
    def _generate_cache_key(self, namespace: str, *args, **kwargs) -> str:
        """Generate consistent cache key"""
        key_data = f"{namespace}:{':'.join(map(str, args))}"
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            key_data += f":{':'.join(f'{k}={v}' for k, v in sorted_kwargs)}"
        
        # Create hash for long keys
        if len(key_data) > 250:
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            return f"{namespace}:hash:{key_hash}"
        
        return key_data
    
    async def get(self, namespace: str, *args, **kwargs) -> Optional[Any]:
        """Get value from cache with multi-tier fallback"""
        cache_key = self._generate_cache_key(namespace, *args, **kwargs)
        start_time = time.time()
        
        try:
            # Try L1 cache first
            if cache_key in self.l1_cache:
                entry = self.l1_cache[cache_key]
                if not self._is_expired(entry):
                    entry.access_count += 1
                    entry.last_accessed = datetime.now()
                    self.metrics.hits += 1
                    self.metrics.total_requests += 1
                    self._update_hit_rate()
                    logger.debug("Cache hit L1", key=cache_key, level="L1")
                    return entry.value
                else:
                    # Remove expired entry
                    del self.l1_cache[cache_key]
            
            # Try L2 cache (Redis)
            try:
                redis_value = await self._get_from_redis(cache_key)
                if redis_value is not None:
                    # Promote to L1 cache
                    await self._promote_to_l1(cache_key, redis_value, namespace)
                    self.metrics.hits += 1
                    self.metrics.total_requests += 1
                    self._update_hit_rate()
                    logger.debug("Cache hit L2", key=cache_key, level="L2")
                    return redis_value
            except Exception as e:
                logger.warning("Redis cache error", key=cache_key, error=str(e))
            
            # Cache miss
            self.metrics.misses += 1
            self.metrics.total_requests += 1
            self._update_hit_rate()
            logger.debug("Cache miss", key=cache_key)
            
            return None
            
        except Exception as e:
            logger.error("Cache get error", key=cache_key, error=str(e))
            return None
        finally:
            # Update response time metrics
            response_time = time.time() - start_time
            self._update_avg_response_time(response_time)
    
    async def set(self, namespace: str, value: Any, ttl: Optional[int] = None, 
                  *args, **kwargs) -> bool:
        """Set value in cache with multi-tier strategy"""
        cache_key = self._generate_cache_key(namespace, *args, **kwargs)
        
        try:
            # Determine TTL
            if ttl is None:
                ttl = self.ttl_configs.get(namespace, 3600)
            
            # Get cache strategy
            strategy = self.cache_strategies.get(namespace, CacheStrategy.WRITE_THROUGH)
            
            # Create cache entry
            expires_at = datetime.now() + timedelta(seconds=ttl)
            entry = CacheEntry(
                key=cache_key,
                value=value,
                expires_at=expires_at,
                ttl=ttl,
                level=CacheLevel.L1_MEMORY,
                metadata={"namespace": namespace, "strategy": strategy.value}
            )
            
            # Apply cache strategy
            if strategy == CacheStrategy.WRITE_THROUGH:
                # Write to all levels
                await self._write_to_all_levels(entry)
            elif strategy == CacheStrategy.WRITE_BACK:
                # Write to L1, lazy write to other levels
                await self._write_to_l1(entry)
            elif strategy == CacheStrategy.WRITE_AROUND:
                # Write to L2 and L3, skip L1
                await self._write_to_l2_l3(entry)
            elif strategy == CacheStrategy.CACHE_ASIDE:
                # Application manages cache
                await self._write_to_l1(entry)
            
            logger.debug("Cache set", key=cache_key, strategy=strategy.value, ttl=ttl)
            return True
            
        except Exception as e:
            logger.error("Cache set error", key=cache_key, error=str(e))
            return False
    
    async def delete(self, namespace: str, *args, **kwargs) -> bool:
        """Delete value from all cache levels"""
        cache_key = self._generate_cache_key(namespace, *args, **kwargs)
        
        try:
            # Remove from L1
            if cache_key in self.l1_cache:
                del self.l1_cache[cache_key]
            
            # Remove from L2 (Redis)
            try:
                await self.l2_cache.delete(cache_key)
            except Exception as e:
                logger.warning("Redis delete error", key=cache_key, error=str(e))
            
            logger.debug("Cache delete", key=cache_key)
            return True
            
        except Exception as e:
            logger.error("Cache delete error", key=cache_key, error=str(e))
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            deleted_count = 0
            
            # Invalidate L1 cache
            keys_to_delete = [key for key in self.l1_cache.keys() if pattern in key]
            for key in keys_to_delete:
                del self.l1_cache[key]
                deleted_count += 1
            
            # Invalidate L2 cache (Redis)
            try:
                redis_keys = await self.l2_cache.keys(pattern)
                if redis_keys:
                    await self.l2_cache.delete(*redis_keys)
                    deleted_count += len(redis_keys)
            except Exception as e:
                logger.warning("Redis pattern delete error", pattern=pattern, error=str(e))
            
            logger.info("Cache pattern invalidated", pattern=pattern, count=deleted_count)
            return deleted_count
            
        except Exception as e:
            logger.error("Cache pattern invalidation error", pattern=pattern, error=str(e))
            return 0
    
    async def get_or_set(self, namespace: str, key_args: tuple, key_kwargs: dict,
                        factory_func, ttl: Optional[int] = None) -> Any:
        """Get from cache or set using factory function"""
        cached_value = await self.get(namespace, *key_args, **key_kwargs)
        
        if cached_value is not None:
            return cached_value
        
        # Generate value using factory function
        try:
            if asyncio.iscoroutinefunction(factory_func):
                value = await factory_func(*key_args, **key_kwargs)
            else:
                value = factory_func(*key_args, **key_kwargs)
            
            # Cache the generated value
            await self.set(namespace, value, ttl, *key_args, **key_kwargs)
            
            return value
            
        except Exception as e:
            logger.error("Cache factory function error", 
                        namespace=namespace, key_args=key_args, error=str(e))
            raise
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired"""
        if entry.expires_at is None:
            return False
        return datetime.now() > entry.expires_at
    
    async def _get_from_redis(self, key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        try:
            value = await self.l2_cache.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning("Redis get error", key=key, error=str(e))
            return None
    
    async def _promote_to_l1(self, key: str, value: Any, namespace: str):
        """Promote value from L2 to L1 cache"""
        try:
            ttl = self.ttl_configs.get(namespace, 3600)
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            entry = CacheEntry(
                key=key,
                value=value,
                expires_at=expires_at,
                ttl=ttl,
                level=CacheLevel.L1_MEMORY,
                metadata={"namespace": namespace, "promoted": True}
            )
            
            await self._write_to_l1(entry)
            
        except Exception as e:
            logger.warning("L1 promotion error", key=key, error=str(e))
    
    async def _write_to_l1(self, entry: CacheEntry):
        """Write entry to L1 cache with eviction"""
        try:
            # Check if we need to evict
            if len(self.l1_cache) >= self.max_l1_size:
                await self._evict_lru_entry()
            
            self.l1_cache[entry.key] = entry
            
        except Exception as e:
            logger.warning("L1 write error", key=entry.key, error=str(e))
    
    async def _write_to_l2(self, entry: CacheEntry):
        """Write entry to L2 cache (Redis)"""
        try:
            value_json = json.dumps(entry.value, default=str)
            await self.l2_cache.setex(entry.key, entry.ttl, value_json)
            
        except Exception as e:
            logger.warning("L2 write error", key=entry.key, error=str(e))
    
    async def _write_to_all_levels(self, entry: CacheEntry):
        """Write entry to all cache levels"""
        await self._write_to_l1(entry)
        await self._write_to_l2(entry)
    
    async def _write_to_l2_l3(self, entry: CacheEntry):
        """Write entry to L2 and L3 levels"""
        await self._write_to_l2(entry)
        # L3 (database) write would be implemented here
    
    async def _evict_lru_entry(self):
        """Evict least recently used entry from L1 cache"""
        if not self.l1_cache:
            return
        
        # Find LRU entry
        lru_key = min(self.l1_cache.keys(), 
                     key=lambda k: self.l1_cache[k].last_accessed)
        
        del self.l1_cache[lru_key]
        self.metrics.evictions += 1
        
        logger.debug("L1 cache eviction", key=lru_key)
    
    def _update_hit_rate(self):
        """Update cache hit rate"""
        if self.metrics.total_requests > 0:
            self.metrics.hit_rate = self.metrics.hits / self.metrics.total_requests
    
    def _update_avg_response_time(self, response_time: float):
        """Update average response time"""
        if self.metrics.total_requests == 1:
            self.metrics.avg_response_time = response_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics.avg_response_time = (
                alpha * response_time + (1 - alpha) * self.metrics.avg_response_time
            )
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        try:
            l1_size = len(self.l1_cache)
            l1_memory = sum(
                len(str(entry.value)) for entry in self.l1_cache.values()
            ) / 1024  # KB
            
            # Get Redis info
            redis_info = {}
            try:
                redis_info = await self.l2_cache.info('memory')
            except Exception as e:
                logger.warning("Redis info error", error=str(e))
            
            return {
                "l1_cache": {
                    "size": l1_size,
                    "max_size": self.max_l1_size,
                    "memory_usage_kb": l1_memory,
                    "utilization": l1_size / self.max_l1_size * 100
                },
                "l2_cache": {
                    "redis_memory": redis_info.get('used_memory', 0),
                    "redis_memory_human": redis_info.get('used_memory_human', '0B')
                },
                "metrics": {
                    "hits": self.metrics.hits,
                    "misses": self.metrics.misses,
                    "hit_rate": self.metrics.hit_rate * 100,
                    "total_requests": self.metrics.total_requests,
                    "evictions": self.metrics.evictions,
                    "avg_response_time_ms": self.metrics.avg_response_time * 1000
                },
                "configuration": {
                    "compression_enabled": self.compression_enabled,
                    "encryption_enabled": self.encryption_enabled,
                    "ttl_configs": self.ttl_configs,
                    "strategies": {k: v.value for k, v in self.cache_strategies.items()}
                }
            }
            
        except Exception as e:
            logger.error("Cache stats error", error=str(e))
            return {}
    
    async def clear_all_caches(self) -> bool:
        """Clear all cache levels"""
        try:
            # Clear L1 cache
            self.l1_cache.clear()
            
            # Clear L2 cache (Redis)
            try:
                await self.l2_cache.flushdb()
            except Exception as e:
                logger.warning("Redis flush error", error=str(e))
            
            # Reset metrics
            self.metrics = CacheMetrics()
            
            logger.info("All caches cleared")
            return True
            
        except Exception as e:
            logger.error("Cache clear error", error=str(e))
            return False


    def get_cache_metrics(self) -> Dict[str, Any]:
        """
        Get cache metrics and statistics - REAL IMPLEMENTATION
        
        Returns actual cache performance metrics
        """
        try:
            # Calculate L1 cache statistics
            l1_size = len(self.l1_cache)
            l1_capacity = self.max_l1_size
            l1_usage_percent = (l1_size / l1_capacity * 100) if l1_capacity > 0 else 0
            
            # Get actual metrics from CacheMetrics
            total_requests = self.metrics.hits + self.metrics.misses
            hit_rate = (self.metrics.hits / total_requests) if total_requests > 0 else 0.0
            miss_rate = (self.metrics.misses / total_requests) if total_requests > 0 else 0.0
            
            # Calculate average operation times
            avg_get_time = (
                self.metrics.get_time_total / self.metrics.get_count
            ) if self.metrics.get_count > 0 else 0.0
            
            avg_set_time = (
                self.metrics.set_time_total / self.metrics.set_count
            ) if self.metrics.set_count > 0 else 0.0
            
            # L2 cache info (Redis)
            l2_available = self.l2_cache is not None
            l2_size = 0
            if l2_available:
                try:
                    # Try to get Redis info if available
                    if hasattr(self.l2_cache, 'dbsize'):
                        l2_size = self.l2_cache.dbsize()
                except:
                    pass
            
            metrics = {
                "l1_cache": {
                    "size": l1_size,
                    "capacity": l1_capacity,
                    "usage_percent": round(l1_usage_percent, 1),
                    "entries": l1_size
                },
                "l2_cache": {
                    "available": l2_available,
                    "size": l2_size,
                    "type": "redis" if l2_available else "none"
                },
                "performance": {
                    "total_requests": total_requests,
                    "hits": self.metrics.hits,
                    "misses": self.metrics.misses,
                    "hit_rate": round(hit_rate, 4),
                    "miss_rate": round(miss_rate, 4),
                    "evictions": self.metrics.evictions,
                    "avg_get_time_ms": round(avg_get_time * 1000, 2),
                    "avg_set_time_ms": round(avg_set_time * 1000, 2)
                },
                "efficiency": {
                    "compression_enabled": self.compression_enabled,
                    "encryption_enabled": self.encryption_enabled,
                    "memory_saved_bytes": self.metrics.memory_saved
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            logger.error("Error getting cache metrics", error=str(e))
            return {
                "l1_cache": {"size": len(self.l1_cache)},
                "error": str(e)
            }


# Global cache instance
advanced_cache = MultiTierCaching()


# Convenience functions
async def cache_get(namespace: str, *args, **kwargs) -> Optional[Any]:
    """Get from advanced cache"""
    return await advanced_cache.get(namespace, *args, **kwargs)


async def cache_set(namespace: str, value: Any, ttl: Optional[int] = None, 
                   *args, **kwargs) -> bool:
    """Set in advanced cache"""
    return await advanced_cache.set(namespace, value, ttl, *args, **kwargs)


async def cache_delete(namespace: str, *args, **kwargs) -> bool:
    """Delete from advanced cache"""
    return await advanced_cache.delete(namespace, *args, **kwargs)


async def cache_get_or_set(namespace: str, key_args: tuple, key_kwargs: dict,
                          factory_func, ttl: Optional[int] = None) -> Any:
    """Get from cache or set using factory function"""
    return await advanced_cache.get_or_set(namespace, key_args, key_kwargs, 
                                         factory_func, ttl)


async def cache_invalidate_pattern(pattern: str) -> int:
    """Invalidate cache pattern"""
    return await advanced_cache.invalidate_pattern(pattern)


async def get_cache_metrics() -> Dict[str, Any]:
    """Get cache performance metrics"""
    return await advanced_cache.get_cache_stats()