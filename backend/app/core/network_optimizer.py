"""
Network Optimization Engine for CognOmega System

This module implements advanced network optimization techniques including
API response caching, data compression, CDN integration, and intelligent
connection pooling.
"""

import structlog
import asyncio
import aiohttp
import gzip
import json
import time
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import hashlib
from redis import asyncio as aioredis
from collections import defaultdict, deque

logger = structlog.get_logger(__name__)

class CacheStrategy(Enum):
    """Cache strategy types"""
    NO_CACHE = "no_cache"
    SHORT_TERM = "short_term"      # 5 minutes
    MEDIUM_TERM = "medium_term"    # 1 hour
    LONG_TERM = "long_term"        # 24 hours
    PERSISTENT = "persistent"      # Until manually invalidated

class CompressionLevel(Enum):
    """Compression level types"""
    NONE = 0
    FAST = 1
    BALANCED = 6
    MAXIMUM = 9

@dataclass
class NetworkRequest:
    """Network request definition"""
    request_id: str
    url: str
    method: str
    headers: Dict[str, str]
    data: Any
    cache_strategy: CacheStrategy
    compression_level: CompressionLevel
    timeout: int
    created_at: datetime

@dataclass
class NetworkResponse:
    """Network response definition"""
    request_id: str
    status_code: int
    headers: Dict[str, str]
    data: Any
    compressed_data: bytes
    response_time: float
    cache_hit: bool
    compressed_size: int
    original_size: int
    timestamp: datetime

@dataclass
class NetworkMetrics:
    """Network performance metrics"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    cache_hit_rate: float
    compression_ratio: float
    bandwidth_saved: int
    timestamp: datetime

class NetworkOptimizer:
    """Advanced network optimization engine"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = aioredis.from_url(redis_url, decode_responses=False)
        
        # Connection pools
        self.connector = aiohttp.TCPConnector(
            limit=100,  # Total connection pool size
            limit_per_host=30,  # Per-host connection limit
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        self.session = None
        
        # Cache configuration
        self.cache_ttl = {
            CacheStrategy.NO_CACHE: 0,
            CacheStrategy.SHORT_TERM: 300,  # 5 minutes
            CacheStrategy.MEDIUM_TERM: 3600,  # 1 hour
            CacheStrategy.LONG_TERM: 86400,  # 24 hours
            CacheStrategy.PERSISTENT: -1  # Never expire
        }
        
        # Network metrics
        self.network_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_response_time": 0.0,
            "cache_hits": 0,
            "total_original_size": 0,
            "total_compressed_size": 0
        }
        
        # Request history for analytics
        self.request_history: deque = deque(maxlen=1000)
        
        # CDN configuration
        self.cdn_endpoints = {
            "static_assets": "https://cdn.cognomega.com/static",
            "api_responses": "https://cdn.cognomega.com/api",
            "user_uploads": "https://cdn.cognomega.com/uploads"
        }
        
        logger.info("Network Optimizer initialized")

    async def initialize_session(self):
        """Initialize aiohttp session with optimized settings"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            
            self.session = aiohttp.ClientSession(
                connector=self.connector,
                timeout=timeout,
                headers={
                    'User-Agent': 'CognOmega-NetworkOptimizer/1.0',
                    'Accept-Encoding': 'gzip, deflate, br'
                }
            )
            logger.info("Network session initialized")

    async def optimize_api_request(self, request: NetworkRequest) -> NetworkResponse:
        """Optimize API request with caching and compression"""
        try:
            await self.initialize_session()
            
            logger.info(f"Optimizing API request: {request.method} {request.url}")
            
            # Check cache first
            cached_response = await self._check_cache(request)
            if cached_response:
                self.network_metrics["cache_hits"] += 1
                logger.info(f"Cache hit for request: {request.request_id}")
                return cached_response
            
            # Make optimized request
            response = await self._make_optimized_request(request)
            
            # Cache response if applicable
            if request.cache_strategy != CacheStrategy.NO_CACHE:
                await self._cache_response(request, response)
            
            # Update metrics
            self._update_network_metrics(response)
            
            # Store in history
            self.request_history.append(response)
            
            logger.info(f"API request completed: {request.request_id} in {response.response_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"API request optimization failed for {request.request_id}", error=str(e))
            self.network_metrics["failed_requests"] += 1
            raise

    async def _check_cache(self, request: NetworkRequest) -> Optional[NetworkResponse]:
        """Check cache for existing response"""
        try:
            cache_key = self._generate_cache_key(request)
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                # Deserialize cached response
                response_data = json.loads(gzip.decompress(cached_data).decode('utf-8'))
                
                # Reconstruct response object
                response = NetworkResponse(
                    request_id=response_data["request_id"],
                    status_code=response_data["status_code"],
                    headers=response_data["headers"],
                    data=response_data["data"],
                    compressed_data=cached_data,
                    response_time=response_data["response_time"],
                    cache_hit=True,
                    compressed_size=len(cached_data),
                    original_size=response_data["original_size"],
                    timestamp=datetime.fromisoformat(response_data["timestamp"])
                )
                
                return response
            
            return None
            
        except Exception as e:
            logger.error(f"Cache check failed for {request.request_id}", error=str(e))
            return None

    def _generate_cache_key(self, request: NetworkRequest) -> str:
        """Generate cache key for request"""
        key_data = f"{request.method}:{request.url}:{json.dumps(request.headers, sort_keys=True)}"
        if request.data:
            key_data += f":{json.dumps(request.data, sort_keys=True)}"
        
        return f"network_cache:{hashlib.md5(key_data.encode()).hexdigest()}"

    async def _make_optimized_request(self, request: NetworkRequest) -> NetworkResponse:
        """Make optimized HTTP request"""
        try:
            start_time = time.time()
            
            # Prepare request data with compression (only if > 16KB); set header when compressing
            compressed_data, used_compression = await self._compress_request_data(request.data, request.compression_level)
            headers = request.headers.copy() if request.headers else {}
            if used_compression:
                headers['Content-Encoding'] = 'gzip'
            
            # Make request
            async with self.session.request(
                method=request.method,
                url=request.url,
                headers=headers,
                data=compressed_data if compressed_data else request.data,
                timeout=request.timeout
            ) as response:
                
                # Read response data
                response_data = await response.read()
                
                # Decompress response if needed
                if response.headers.get('Content-Encoding') == 'gzip':
                    response_data = gzip.decompress(response_data)
                
                # Parse response data
                try:
                    parsed_data = json.loads(response_data.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    parsed_data = response_data
                
                response_time = time.time() - start_time
                
                # Create response object
                network_response = NetworkResponse(
                    request_id=request.request_id,
                    status_code=response.status,
                    headers=dict(response.headers),
                    data=parsed_data,
                    compressed_data=compressed_data,
                    response_time=response_time,
                    cache_hit=False,
                    compressed_size=len(compressed_data) if compressed_data else 0,
                    original_size=len(str(request.data)) if request.data else 0,
                    timestamp=datetime.now()
                )
                
                return network_response
                
        except Exception as e:
            logger.error(f"Optimized request failed for {request.request_id}", error=str(e))
            raise

    async def _compress_request_data(self, data: Any, compression_level: CompressionLevel) -> Tuple[Optional[bytes], bool]:
        """Compress request data; returns (bytes or None, used_compression: bool)"""
        try:
            if not data or compression_level == CompressionLevel.NONE:
                return None, False
            
            # Serialize data
            if isinstance(data, (dict, list)):
                serialized_data = json.dumps(data).encode('utf-8')
            elif isinstance(data, str):
                serialized_data = data.encode('utf-8')
            elif isinstance(data, bytes):
                serialized_data = data
            else:
                serialized_data = str(data).encode('utf-8')
            
            # Only compress if payload > 16KB
            if len(serialized_data) < 16 * 1024:
                return None, False

            # Compress data
            if compression_level == CompressionLevel.FAST:
                compressed_data = gzip.compress(serialized_data, compresslevel=1)
            elif compression_level == CompressionLevel.BALANCED:
                compressed_data = gzip.compress(serialized_data, compresslevel=6)
            elif compression_level == CompressionLevel.MAXIMUM:
                compressed_data = gzip.compress(serialized_data, compresslevel=9)
            else:
                return None, False
            
            return compressed_data, True
            
        except Exception as e:
            logger.error(f"Request data compression failed", error=str(e))
            return None, False

    async def _cache_response(self, request: NetworkRequest, response: NetworkResponse):
        """Cache response for future requests"""
        try:
            cache_key = self._generate_cache_key(request)
            ttl = self.cache_ttl[request.cache_strategy]
            
            # Prepare response data for caching
            response_data = {
                "request_id": response.request_id,
                "status_code": response.status_code,
                "headers": response.headers,
                "data": response.data,
                "response_time": response.response_time,
                "original_size": response.original_size,
                "timestamp": response.timestamp.isoformat()
            }
            
            # Compress and store
            serialized_data = json.dumps(response_data).encode('utf-8')
            compressed_data = gzip.compress(serialized_data)
            
            if ttl > 0:
                await self.redis_client.setex(cache_key, ttl, compressed_data)
            else:
                await self.redis_client.set(cache_key, compressed_data)
            
            logger.info(f"Response cached: {request.request_id} with TTL {ttl}")
            
        except Exception as e:
            logger.error(f"Response caching failed for {request.request_id}", error=str(e))

    def _update_network_metrics(self, response: NetworkResponse):
        """Update network performance metrics"""
        self.network_metrics["total_requests"] += 1
        
        if 200 <= response.status_code < 300:
            self.network_metrics["successful_requests"] += 1
        else:
            self.network_metrics["failed_requests"] += 1
        
        self.network_metrics["total_response_time"] += response.response_time
        self.network_metrics["total_original_size"] += response.original_size
        self.network_metrics["total_compressed_size"] += response.compressed_size

    async def optimize_service_network_usage(self, service_name: str, requests: List[NetworkRequest]) -> Dict[str, Any]:
        """Optimize network usage for specific service"""
        try:
            logger.info(f"Optimizing network usage for service: {service_name}")
            
            # Analyze service network patterns
            network_analysis = self._analyze_service_network_patterns(service_name, requests)
            
            # Apply network optimizations
            optimization_results = await self._apply_network_optimizations(service_name, requests, network_analysis)
            
            # Calculate network efficiency
            network_efficiency = self._calculate_network_efficiency(optimization_results)
            
            return {
                "service_name": service_name,
                "original_requests": len(requests),
                "optimized_requests": len(optimization_results["responses"]),
                "network_efficiency": network_efficiency,
                "network_analysis": network_analysis,
                "optimization_results": optimization_results
            }
            
        except Exception as e:
            logger.error(f"Service network optimization failed for {service_name}", error=str(e))
            raise

    def _analyze_service_network_patterns(self, service_name: str, requests: List[NetworkRequest]) -> Dict[str, Any]:
        """Analyze network patterns for specific service"""
        analysis = {
            "service_name": service_name,
            "total_requests": len(requests),
            "unique_urls": len(set(req.url for req in requests)),
            "average_request_size": 0,
            "cacheable_requests": 0,
            "compression_opportunities": 0,
            "recommendations": []
        }
        
        if requests:
            total_size = sum(len(str(req.data)) if req.data else 0 for req in requests)
            analysis["average_request_size"] = total_size / len(requests)
            analysis["cacheable_requests"] = len([req for req in requests if req.cache_strategy != CacheStrategy.NO_CACHE])
            analysis["compression_opportunities"] = len([req for req in requests if req.data and len(str(req.data)) > 1024])
        
        # Generate recommendations
        if analysis["unique_urls"] / len(requests) < 0.1:
            analysis["recommendations"].append("High URL reuse detected, consider aggressive caching")
        
        if analysis["average_request_size"] > 10240:  # 10KB
            analysis["recommendations"].append("Large request sizes detected, consider compression")
        
        if analysis["cacheable_requests"] / len(requests) < 0.5:
            analysis["recommendations"].append("Low cache utilization, consider enabling more caching")
        
        return analysis

    async def _apply_network_optimizations(self, service_name: str, requests: List[NetworkRequest], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply network optimizations to service requests"""
        optimization_results = {
            "responses": [],
            "cache_hits": 0,
            "compression_savings": 0,
            "total_response_time": 0.0
        }
        
        for request in requests:
            # Apply service-specific optimizations
            optimized_request = self._optimize_request_for_service(request, analysis)
            
            # Execute optimized request
            response = await self.optimize_api_request(optimized_request)
            optimization_results["responses"].append(response)
            
            # Track optimization metrics
            if response.cache_hit:
                optimization_results["cache_hits"] += 1
            
            optimization_results["compression_savings"] += (response.original_size - response.compressed_size)
            optimization_results["total_response_time"] += response.response_time
        
        return optimization_results

    def _optimize_request_for_service(self, request: NetworkRequest, analysis: Dict[str, Any]) -> NetworkRequest:
        """Optimize request for specific service"""
        # Create optimized copy of request
        optimized_request = NetworkRequest(
            request_id=request.request_id,
            url=request.url,
            method=request.method,
            headers=request.headers.copy(),
            data=request.data,
            cache_strategy=request.cache_strategy,
            compression_level=request.compression_level,
            timeout=request.timeout,
            created_at=request.created_at
        )
        
        # Apply service-specific optimizations
        if analysis["average_request_size"] > 10240:  # Large requests
            optimized_request.compression_level = CompressionLevel.BALANCED
        
        if analysis["unique_urls"] / analysis["total_requests"] < 0.1:  # High URL reuse
            optimized_request.cache_strategy = CacheStrategy.LONG_TERM
        
        # Add optimized headers
        optimized_request.headers.update({
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br'
        })
        
        return optimized_request

    def _calculate_network_efficiency(self, optimization_results: Dict[str, Any]) -> float:
        """Calculate network efficiency score"""
        total_requests = len(optimization_results["responses"])
        cache_hits = optimization_results["cache_hits"]
        compression_savings = optimization_results["compression_savings"]
        
        if total_requests == 0:
            return 0.0
        
        cache_efficiency = (cache_hits / total_requests) * 100
        compression_efficiency = min(100, (compression_savings / (total_requests * 1024)) * 100)  # Normalize to 100%
        
        return (cache_efficiency + compression_efficiency) / 2

    async def get_network_metrics(self) -> NetworkMetrics:
        """Get comprehensive network performance metrics"""
        try:
            total_requests = self.network_metrics["total_requests"]
            successful_requests = self.network_metrics["successful_requests"]
            failed_requests = self.network_metrics["failed_requests"]
            
            average_response_time = 0.0
            if total_requests > 0:
                average_response_time = self.network_metrics["total_response_time"] / total_requests
            
            cache_hit_rate = 0.0
            if total_requests > 0:
                cache_hit_rate = (self.network_metrics["cache_hits"] / total_requests) * 100
            
            compression_ratio = 0.0
            if self.network_metrics["total_original_size"] > 0:
                compression_ratio = (1 - self.network_metrics["total_compressed_size"] / self.network_metrics["total_original_size"]) * 100
            
            bandwidth_saved = self.network_metrics["total_original_size"] - self.network_metrics["total_compressed_size"]
            
            return NetworkMetrics(
                total_requests=total_requests,
                successful_requests=successful_requests,
                failed_requests=failed_requests,
                average_response_time=average_response_time,
                cache_hit_rate=cache_hit_rate,
                compression_ratio=compression_ratio,
                bandwidth_saved=bandwidth_saved,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Network metrics retrieval failed", error=str(e))
            raise

    async def optimize_connection_pooling(self):
        """Optimize connection pooling settings"""
        try:
            logger.info("Optimizing connection pooling")
            
            # Analyze current connection usage
            connection_analysis = await self._analyze_connection_usage()
            
            # Adjust connection pool settings
            optimized_settings = self._calculate_optimal_pool_settings(connection_analysis)
            
            # Apply optimized settings
            await self._apply_optimized_pool_settings(optimized_settings)
            
            logger.info("Connection pooling optimization completed")
            return optimized_settings
            
        except Exception as e:
            logger.error(f"Connection pooling optimization failed", error=str(e))
            raise

    async def _analyze_connection_usage(self) -> Dict[str, Any]:
        """Analyze current connection usage patterns"""
        # This would analyze actual connection usage in a real implementation
        return {
            "concurrent_connections": 50,
            "average_connection_time": 2.5,
            "connection_failures": 5,
            "idle_connections": 10
        }

    def _calculate_optimal_pool_settings(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal connection pool settings"""
        return {
            "total_limit": min(100, analysis["concurrent_connections"] * 2),
            "per_host_limit": min(30, analysis["concurrent_connections"] // 2),
            "keepalive_timeout": 30,
            "enable_cleanup_closed": True
        }

    async def _apply_optimized_pool_settings(self, settings: Dict[str, Any]):
        """Apply optimized connection pool settings"""
        try:
            # Close existing session
            if self.session:
                await self.session.close()
            
            # Create new connector with optimized settings
            self.connector = aiohttp.TCPConnector(
                limit=settings["total_limit"],
                limit_per_host=settings["per_host_limit"],
                keepalive_timeout=settings["keepalive_timeout"],
                enable_cleanup_closed=settings["enable_cleanup_closed"]
            )
            
            # Reinitialize session
            self.session = None
            await self.initialize_session()
            
            logger.info("Optimized connection pool settings applied")
            
        except Exception as e:
            logger.error(f"Connection pool settings application failed", error=str(e))
            raise

    async def get_network_optimization_metrics(self) -> Dict[str, Any]:
        """Get comprehensive network optimization metrics"""
        try:
            network_metrics = await self.get_network_metrics()
            
            return {
                "network_metrics": {
                    "total_requests": network_metrics.total_requests,
                    "successful_requests": network_metrics.successful_requests,
                    "failed_requests": network_metrics.failed_requests,
                    "average_response_time": network_metrics.average_response_time,
                    "cache_hit_rate": network_metrics.cache_hit_rate,
                    "compression_ratio": network_metrics.compression_ratio,
                    "bandwidth_saved_mb": network_metrics.bandwidth_saved / (1024 * 1024)
                },
                "optimization_metrics": self.network_metrics,
                "connection_pool": {
                    "total_limit": self.connector.limit,
                    "per_host_limit": self.connector.limit_per_host,
                    "keepalive_timeout": self.connector.keepalive_timeout
                },
                "cache_configuration": {
                    "cache_strategies": {strategy.value: ttl for strategy, ttl in self.cache_ttl.items()},
                    "redis_connected": await self._check_redis_connection()
                },
                "recent_requests": list(self.request_history)[-10:]  # Last 10 requests
            }
            
        except Exception as e:
            logger.error(f"Network optimization metrics retrieval failed", error=str(e))
            raise

    async def _check_redis_connection(self) -> bool:
        """Check Redis connection status"""
        try:
            pong = await self.redis_client.ping()
            return pong is True or pong == b'PONG'
        except Exception:
            return False

    async def cleanup(self):
        """Cleanup network optimizer resources"""
        try:
            if self.session:
                await self.session.close()
            
            if self.connector:
                await self.connector.close()
            
            logger.info("Network Optimizer cleanup completed")
        except Exception as e:
            logger.error(f"Network Optimizer cleanup failed", error=str(e))

# Global network optimizer instance
network_optimizer = NetworkOptimizer()
