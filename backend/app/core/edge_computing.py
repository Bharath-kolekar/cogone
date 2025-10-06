"""
Edge Computing System for Cognomega AI
Reduced latency through intelligent edge deployment and content delivery
"""

import asyncio
import aiohttp
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import structlog
import numpy as np
from concurrent.futures import ThreadPoolExecutor

logger = structlog.get_logger()


class EdgeNodeType(str, Enum):
    """Types of edge nodes"""
    CDN = "cdn"
    COMPUTE = "compute"
    CACHE = "cache"
    STORAGE = "storage"
    AI_PROCESSING = "ai_processing"
    HYBRID = "hybrid"


class EdgeStrategy(str, Enum):
    """Edge computing strategies"""
    LATENCY_OPTIMIZED = "latency_optimized"
    BANDWIDTH_OPTIMIZED = "bandwidth_optimized"
    COST_OPTIMIZED = "cost_optimized"
    RELIABILITY_OPTIMIZED = "reliability_optimized"
    HYBRID = "hybrid"


class ContentType(str, Enum):
    """Content types for edge optimization"""
    STATIC_ASSETS = "static_assets"
    API_RESPONSES = "api_responses"
    AI_MODELS = "ai_models"
    USER_DATA = "user_data"
    DYNAMIC_CONTENT = "dynamic_content"
    REAL_TIME = "real_time"


@dataclass
class EdgeNode:
    """Edge node definition"""
    node_id: str
    name: str
    node_type: EdgeNodeType
    location: Tuple[float, float]  # (latitude, longitude)
    endpoint: str
    capacity: int  # requests per second
    current_load: float = 0.0
    latency_ms: float = 0.0
    availability: float = 1.0
    cost_per_request: float = 0.001
    last_updated: datetime = field(default_factory=datetime.now)
    status: str = "healthy"


@dataclass
class EdgeRequest:
    """Edge request definition"""
    request_id: str
    content_type: ContentType
    user_location: Tuple[float, float]
    priority: str
    size_bytes: int
    ttl_seconds: int
    cacheable: bool = True
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EdgeOptimization:
    """Edge optimization result"""
    optimal_node: EdgeNode
    fallback_nodes: List[EdgeNode]
    expected_latency: float
    cache_hit_probability: float
    cost_estimate: float
    optimization_strategy: str
    reasoning: str
    timestamp: datetime = field(default_factory=datetime.now)


class EdgeComputingEngine:
    """Edge computing optimization engine"""
    
    def __init__(self):
        # Edge nodes registry
        self.edge_nodes: Dict[str, EdgeNode] = {}
        self._initialize_edge_nodes()
        
        # Content cache
        self.edge_cache: Dict[str, Dict[str, Any]] = {}
        
        # Request routing
        self.routing_history: List[EdgeOptimization] = []
        
        # Performance metrics
        self.edge_metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_latency": 0.0,
            "cost_savings": 0.0,
            "edge_utilization": 0.0
        }
        
        # Configuration
        self.max_cache_size = 10000  # items
        self.cache_ttl_default = 3600  # 1 hour
        self.load_balancing_enabled = True
        self.auto_scaling_enabled = True
        
        # Background tasks
        self._monitoring_task = None
        self._optimization_task = None
        
        # Initialize
        self._start_background_tasks()
    
    def _initialize_edge_nodes(self):
        """Initialize edge nodes"""
        edge_nodes_config = [
            {
                "node_id": "us-east-cdn",
                "name": "US East CDN",
                "node_type": EdgeNodeType.CDN,
                "location": (40.7128, -74.0060),  # New York
                "endpoint": "https://cdn-us-east.cognomega.ai",
                "capacity": 10000
            },
            {
                "node_id": "us-west-cdn",
                "name": "US West CDN",
                "node_type": EdgeNodeType.CDN,
                "location": (37.7749, -122.4194),  # San Francisco
                "endpoint": "https://cdn-us-west.cognomega.ai",
                "capacity": 10000
            },
            {
                "node_id": "eu-west-cdn",
                "name": "EU West CDN",
                "node_type": EdgeNodeType.CDN,
                "location": (51.5074, -0.1278),  # London
                "endpoint": "https://cdn-eu-west.cognomega.ai",
                "capacity": 8000
            },
            {
                "node_id": "asia-cdn",
                "name": "Asia CDN",
                "node_type": EdgeNodeType.CDN,
                "location": (1.3521, 103.8198),  # Singapore
                "endpoint": "https://cdn-asia.cognomega.ai",
                "capacity": 8000
            },
            {
                "node_id": "us-east-compute",
                "name": "US East Compute",
                "node_type": EdgeNodeType.COMPUTE,
                "location": (40.7128, -74.0060),
                "endpoint": "https://compute-us-east.cognomega.ai",
                "capacity": 5000
            },
            {
                "node_id": "eu-west-compute",
                "name": "EU West Compute",
                "node_type": EdgeNodeType.COMPUTE,
                "location": (51.5074, -0.1278),
                "endpoint": "https://compute-eu-west.cognomega.ai",
                "capacity": 5000
            },
            {
                "node_id": "global-ai",
                "name": "Global AI Processing",
                "node_type": EdgeNodeType.AI_PROCESSING,
                "location": (0.0, 0.0),  # Global
                "endpoint": "https://ai-global.cognomega.ai",
                "capacity": 2000
            }
        ]
        
        for config in edge_nodes_config:
            node = EdgeNode(
                node_id=config["node_id"],
                name=config["name"],
                node_type=config["node_type"],
                location=config["location"],
                endpoint=config["endpoint"],
                capacity=config["capacity"]
            )
            self.edge_nodes[node.node_id] = node
    
    def _start_background_tasks(self):
        """Start background edge monitoring tasks"""
        self._monitoring_task = asyncio.create_task(self._monitor_edge_nodes())
        self._optimization_task = asyncio.create_task(self._optimize_edge_performance())
    
    async def _monitor_edge_nodes(self):
        """Monitor edge nodes for health and performance"""
        while True:
            try:
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
                # Check all edge nodes in parallel
                monitoring_tasks = [
                    self._check_edge_node_health(node_id, node)
                    for node_id, node in self.edge_nodes.items()
                ]
                await asyncio.gather(*monitoring_tasks, return_exceptions=True)
                
                # Update edge metrics
                await self._update_edge_metrics()
                
            except Exception as e:
                logger.error("Edge node monitoring error", error=str(e))
                await asyncio.sleep(60)
    
    async def _check_edge_node_health(self, node_id: str, node: EdgeNode):
        """Check health and performance of an edge node"""
        try:
            start_time = datetime.now()
            
            # Perform health check
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f"{node.endpoint}/health") as response:
                    response_time = (datetime.now() - start_time).total_seconds() * 1000
                    
                    # Update node metrics
                    node.latency_ms = response_time
                    node.availability = 1.0 if response.status == 200 else 0.0
                    node.status = "healthy" if response.status == 200 else "unhealthy"
                    node.last_updated = datetime.now()
                    
                    # Estimate current load (simplified)
                    node.current_load = min(1.0, np.random.uniform(0.1, 0.8))
                    
                    logger.debug("Edge node health check completed",
                               node_id=node_id,
                               latency=response_time,
                               status=node.status,
                               load=node.current_load)
            
        except Exception as e:
            # Mark node as unhealthy
            node.status = "unhealthy"
            node.availability = 0.0
            logger.warning("Edge node health check failed",
                         node_id=node_id,
                         error=str(e))
    
    async def _update_edge_metrics(self):
        """Update edge computing metrics"""
        try:
            healthy_nodes = [
                node for node in self.edge_nodes.values()
                if node.status == "healthy"
            ]
            
            if healthy_nodes:
                avg_latency = np.mean([node.latency_ms for node in healthy_nodes])
                total_capacity = sum(node.capacity for node in healthy_nodes)
                total_load = sum(node.current_load * node.capacity for node in healthy_nodes)
                utilization = total_load / total_capacity if total_capacity > 0 else 0.0
                
                self.edge_metrics.update({
                    "average_latency": avg_latency,
                    "edge_utilization": utilization,
                    "healthy_nodes": len(healthy_nodes),
                    "total_nodes": len(self.edge_nodes),
                    "last_updated": datetime.now().isoformat()
                })
            
        except Exception as e:
            logger.error("Edge metrics update error", error=str(e))
    
    async def _optimize_edge_performance(self):
        """Optimize edge performance continuously"""
        while True:
            try:
                await asyncio.sleep(300)  # Optimize every 5 minutes
                
                # Analyze edge performance patterns
                await self._analyze_edge_patterns()
                
                # Optimize cache strategies
                await self._optimize_cache_strategies()
                
                # Update routing algorithms
                await self._optimize_routing_algorithms()
                
            except Exception as e:
                logger.error("Edge performance optimization error", error=str(e))
                await asyncio.sleep(300)
    
    async def _analyze_edge_patterns(self):
        """Analyze edge performance patterns"""
        try:
            # Analyze latency patterns
            for node_id, node in self.edge_nodes.items():
                if node.status == "healthy":
                    # Simple pattern analysis
                    if node.latency_ms > 500:
                        logger.warning("High latency detected on edge node",
                                     node_id=node_id,
                                     latency=node.latency_ms)
                    
                    if node.current_load > 0.9:
                        logger.warning("High load detected on edge node",
                                     node_id=node_id,
                                     load=node.current_load)
            
            # Analyze cache performance
            cache_hit_rate = self.edge_metrics["cache_hits"] / max(1, self.edge_metrics["total_requests"])
            if cache_hit_rate < 0.6:
                logger.info("Low cache hit rate detected", hit_rate=cache_hit_rate)
            
        except Exception as e:
            logger.error("Edge pattern analysis error", error=str(e))
    
    async def _optimize_cache_strategies(self):
        """Optimize cache strategies"""
        try:
            # Clean up expired cache entries
            current_time = datetime.now()
            expired_keys = []
            
            for key, cache_entry in self.edge_cache.items():
                if current_time > cache_entry.get("expires_at", datetime.min):
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.edge_cache[key]
            
            if expired_keys:
                logger.info("Cleaned up expired cache entries", count=len(expired_keys))
            
            # Optimize cache size
            if len(self.edge_cache) > self.max_cache_size:
                # Remove oldest entries
                sorted_entries = sorted(
                    self.edge_cache.items(),
                    key=lambda x: x[1].get("created_at", datetime.min)
                )
                
                entries_to_remove = len(self.edge_cache) - self.max_cache_size
                for key, _ in sorted_entries[:entries_to_remove]:
                    del self.edge_cache[key]
                
                logger.info("Optimized cache size", removed_entries=entries_to_remove)
            
        except Exception as e:
            logger.error("Cache strategy optimization error", error=str(e))
    
    async def _optimize_routing_algorithms(self):
        """Optimize routing algorithms"""
        try:
            # Analyze routing history for optimization opportunities
            if len(self.routing_history) > 100:
                recent_routes = self.routing_history[-100:]
                
                # Calculate average latency by node
                node_latencies = {}
                for route in recent_routes:
                    node_id = route.optimal_node.node_id
                    if node_id not in node_latencies:
                        node_latencies[node_id] = []
                    node_latencies[node_id].append(route.expected_latency)
                
                # Update node latency estimates
                for node_id, latencies in node_latencies.items():
                    if node_id in self.edge_nodes:
                        avg_latency = np.mean(latencies)
                        self.edge_nodes[node_id].latency_ms = avg_latency
                
                logger.info("Updated node latency estimates", nodes_updated=len(node_latencies))
            
        except Exception as e:
            logger.error("Routing algorithm optimization error", error=str(e))
    
    async def optimize_edge_routing(
        self,
        request: EdgeRequest,
        strategy: EdgeStrategy = EdgeStrategy.HYBRID
    ) -> EdgeOptimization:
        """Optimize edge routing for a request"""
        try:
            # Filter available nodes by type and health
            available_nodes = [
                node for node in self.edge_nodes.values()
                if (node.status == "healthy" and 
                    node.node_type in self._get_suitable_node_types(request.content_type))
            ]
            
            if not available_nodes:
                raise Exception("No available edge nodes")
            
            # Apply optimization strategy
            if strategy == EdgeStrategy.LATENCY_OPTIMIZED:
                optimal_node = await self._select_latency_optimized_node(available_nodes, request)
            elif strategy == EdgeStrategy.BANDWIDTH_OPTIMIZED:
                optimal_node = await self._select_bandwidth_optimized_node(available_nodes, request)
            elif strategy == EdgeStrategy.COST_OPTIMIZED:
                optimal_node = await self._select_cost_optimized_node(available_nodes, request)
            elif strategy == EdgeStrategy.RELIABILITY_OPTIMIZED:
                optimal_node = await self._select_reliability_optimized_node(available_nodes, request)
            else:  # HYBRID
                optimal_node = await self._select_hybrid_optimized_node(available_nodes, request)
            
            # Select fallback nodes
            fallback_nodes = [
                node for node in available_nodes
                if node.node_id != optimal_node.node_id
            ][:3]
            
            # Calculate cache hit probability
            cache_hit_prob = await self._calculate_cache_hit_probability(request)
            
            # Create optimization result
            optimization = EdgeOptimization(
                optimal_node=optimal_node,
                fallback_nodes=fallback_nodes,
                expected_latency=optimal_node.latency_ms,
                cache_hit_probability=cache_hit_prob,
                cost_estimate=optimal_node.cost_per_request,
                optimization_strategy=strategy.value,
                reasoning=f"Selected {optimal_node.name} based on {strategy.value} strategy"
            )
            
            # Store routing decision
            self.routing_history.append(optimization)
            
            # Keep only recent history
            if len(self.routing_history) > 1000:
                self.routing_history = self.routing_history[-1000:]
            
            # Update metrics
            self.edge_metrics["total_requests"] += 1
            
            return optimization
            
        except Exception as e:
            logger.error("Edge routing optimization error", error=str(e))
            raise
    
    def _get_suitable_node_types(self, content_type: ContentType) -> List[EdgeNodeType]:
        """Get suitable node types for content type"""
        mapping = {
            ContentType.STATIC_ASSETS: [EdgeNodeType.CDN, EdgeNodeType.CACHE],
            ContentType.API_RESPONSES: [EdgeNodeType.COMPUTE, EdgeNodeType.CACHE],
            ContentType.AI_MODELS: [EdgeNodeType.AI_PROCESSING, EdgeNodeType.COMPUTE],
            ContentType.USER_DATA: [EdgeNodeType.STORAGE, EdgeNodeType.CACHE],
            ContentType.DYNAMIC_CONTENT: [EdgeNodeType.COMPUTE, EdgeNodeType.HYBRID],
            ContentType.REAL_TIME: [EdgeNodeType.COMPUTE, EdgeNodeType.AI_PROCESSING]
        }
        return mapping.get(content_type, [EdgeNodeType.HYBRID])
    
    async def _select_latency_optimized_node(
        self, 
        available_nodes: List[EdgeNode], 
        request: EdgeRequest
    ) -> EdgeNode:
        """Select node optimized for latency"""
        try:
            # Calculate distance-based latency
            user_lat, user_lon = request.user_location
            
            best_node = None
            best_score = float('inf')
            
            for node in available_nodes:
                node_lat, node_lon = node.location
                
                # Calculate approximate distance
                distance = self._calculate_distance(user_lat, user_lon, node_lat, node_lon)
                
                # Estimate network latency based on distance
                estimated_latency = distance * 0.1  # Rough estimate: 0.1ms per km
                total_latency = node.latency_ms + estimated_latency
                
                # Consider node load
                load_factor = 1.0 + (node.current_load * 0.5)
                score = total_latency * load_factor
                
                if score < best_score:
                    best_score = score
                    best_node = node
            
            return best_node or available_nodes[0]
            
        except Exception as e:
            logger.error("Latency-optimized node selection error", error=str(e))
            return available_nodes[0]
    
    async def _select_bandwidth_optimized_node(
        self, 
        available_nodes: List[EdgeNode], 
        request: EdgeRequest
    ) -> EdgeNode:
        """Select node optimized for bandwidth"""
        try:
            # Prefer nodes with lower load for bandwidth optimization
            best_node = min(available_nodes, key=lambda node: node.current_load)
            return best_node
            
        except Exception as e:
            logger.error("Bandwidth-optimized node selection error", error=str(e))
            return available_nodes[0]
    
    async def _select_cost_optimized_node(
        self, 
        available_nodes: List[EdgeNode], 
        request: EdgeRequest
    ) -> EdgeNode:
        """Select node optimized for cost"""
        try:
            # Prefer nodes with lower cost per request
            best_node = min(available_nodes, key=lambda node: node.cost_per_request)
            return best_node
            
        except Exception as e:
            logger.error("Cost-optimized node selection error", error=str(e))
            return available_nodes[0]
    
    async def _select_reliability_optimized_node(
        self, 
        available_nodes: List[EdgeNode], 
        request: EdgeRequest
    ) -> EdgeNode:
        """Select node optimized for reliability"""
        try:
            # Prefer nodes with higher availability
            best_node = max(available_nodes, key=lambda node: node.availability)
            return best_node
            
        except Exception as e:
            logger.error("Reliability-optimized node selection error", error=str(e))
            return available_nodes[0]
    
    async def _select_hybrid_optimized_node(
        self, 
        available_nodes: List[EdgeNode], 
        request: EdgeRequest
    ) -> EdgeNode:
        """Select node using hybrid optimization"""
        try:
            user_lat, user_lon = request.user_location
            
            best_node = None
            best_score = 0.0
            
            for node in available_nodes:
                node_lat, node_lon = node.location
                distance = self._calculate_distance(user_lat, user_lon, node_lat, node_lon)
                
                # Calculate composite score
                latency_score = max(0, 1.0 - (node.latency_ms / 1000.0))
                availability_score = node.availability
                cost_score = max(0, 1.0 - (node.cost_per_request * 1000))
                load_score = 1.0 - node.current_load
                distance_score = max(0, 1.0 - (distance / 20000))  # Normalize to ~20,000 km max
                
                # Weighted composite score
                composite_score = (
                    latency_score * 0.3 +
                    availability_score * 0.25 +
                    cost_score * 0.2 +
                    load_score * 0.15 +
                    distance_score * 0.1
                )
                
                if composite_score > best_score:
                    best_score = composite_score
                    best_node = node
            
            return best_node or available_nodes[0]
            
        except Exception as e:
            logger.error("Hybrid-optimized node selection error", error=str(e))
            return available_nodes[0]
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in kilometers"""
        try:
            # Haversine formula
            R = 6371  # Earth's radius in kilometers
            
            dlat = np.radians(lat2 - lat1)
            dlon = np.radians(lon2 - lon1)
            
            a = (np.sin(dlat/2) * np.sin(dlat/2) + 
                 np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * 
                 np.sin(dlon/2) * np.sin(dlon/2))
            
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
            distance = R * c
            
            return distance
            
        except Exception as e:
            logger.error("Distance calculation error", error=str(e))
            return 1000.0  # Default distance
    
    async def _calculate_cache_hit_probability(self, request: EdgeRequest) -> float:
        """Calculate cache hit probability for request"""
        try:
            # Generate cache key
            cache_key = self._generate_cache_key(request)
            
            # Check if content is in cache
            if cache_key in self.edge_cache:
                cache_entry = self.edge_cache[cache_key]
                if datetime.now() < cache_entry.get("expires_at", datetime.min):
                    return 1.0  # Cache hit
                else:
                    # Cache expired
                    del self.edge_cache[cache_key]
            
            # Estimate cache hit probability based on content type and request patterns
            base_probability = {
                ContentType.STATIC_ASSETS: 0.9,
                ContentType.API_RESPONSES: 0.6,
                ContentType.AI_MODELS: 0.8,
                ContentType.USER_DATA: 0.7,
                ContentType.DYNAMIC_CONTENT: 0.3,
                ContentType.REAL_TIME: 0.1
            }
            
            return base_probability.get(request.content_type, 0.5)
            
        except Exception as e:
            logger.error("Cache hit probability calculation error", error=str(e))
            return 0.5
    
    def _generate_cache_key(self, request: EdgeRequest) -> str:
        """Generate cache key for request"""
        try:
            key_data = f"{request.content_type.value}_{request.user_location}_{request.size_bytes}"
            return hashlib.md5(key_data.encode()).hexdigest()
            
        except Exception as e:
            logger.error("Cache key generation error", error=str(e))
            return "default"
    
    async def cache_content(self, request: EdgeRequest, content: Any, ttl_seconds: int = None):
        """Cache content at edge nodes"""
        try:
            if not request.cacheable:
                return
            
            cache_key = self._generate_cache_key(request)
            
            if ttl_seconds is None:
                ttl_seconds = request.ttl_seconds
            
            cache_entry = {
                "content": content,
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(seconds=ttl_seconds),
                "request_id": request.request_id,
                "content_type": request.content_type.value,
                "size_bytes": request.size_bytes
            }
            
            self.edge_cache[cache_key] = cache_entry
            self.edge_metrics["cache_hits"] += 1
            
            logger.debug("Content cached at edge", 
                        cache_key=cache_key,
                        ttl_seconds=ttl_seconds,
                        size_bytes=request.size_bytes)
            
        except Exception as e:
            logger.error("Content caching error", error=str(e))
    
    async def get_cached_content(self, request: EdgeRequest) -> Optional[Any]:
        """Get cached content from edge nodes"""
        try:
            cache_key = self._generate_cache_key(request)
            
            if cache_key in self.edge_cache:
                cache_entry = self.edge_cache[cache_key]
                
                if datetime.now() < cache_entry.get("expires_at", datetime.min):
                    self.edge_metrics["cache_hits"] += 1
                    return cache_entry["content"]
                else:
                    # Cache expired
                    del self.edge_cache[cache_key]
            
            self.edge_metrics["cache_misses"] += 1
            return None
            
        except Exception as e:
            logger.error("Cached content retrieval error", error=str(e))
            return None
    
    async def get_edge_metrics(self) -> Dict[str, Any]:
        """Get edge computing metrics"""
        try:
            healthy_nodes = [
                node for node in self.edge_nodes.values()
                if node.status == "healthy"
            ]
            
            node_metrics = {}
            for node_id, node in self.edge_nodes.items():
                node_metrics[node_id] = {
                    "name": node.name,
                    "type": node.node_type.value,
                    "status": node.status,
                    "latency_ms": node.latency_ms,
                    "availability": node.availability,
                    "current_load": node.current_load,
                    "capacity": node.capacity,
                    "cost_per_request": node.cost_per_request,
                    "last_updated": node.last_updated.isoformat()
                }
            
            return {
                "edge_metrics": self.edge_metrics,
                "node_metrics": node_metrics,
                "healthy_nodes_count": len(healthy_nodes),
                "total_nodes_count": len(self.edge_nodes),
                "cache_stats": {
                    "total_entries": len(self.edge_cache),
                    "cache_hit_rate": self.edge_metrics["cache_hits"] / max(1, self.edge_metrics["total_requests"]),
                    "max_cache_size": self.max_cache_size
                },
                "routing_history_size": len(self.routing_history),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Edge metrics retrieval error", error=str(e))
            return {}


# Global edge computing engine instance
edge_computing_engine = EdgeComputingEngine()


# Convenience functions
async def optimize_edge_routing(
    request: EdgeRequest,
    strategy: EdgeStrategy = EdgeStrategy.HYBRID
) -> EdgeOptimization:
    """Optimize edge routing for a request"""
    return await edge_computing_engine.optimize_edge_routing(request, strategy)


async def get_edge_metrics() -> Dict[str, Any]:
    """Get edge computing metrics"""
    return await edge_computing_engine.get_edge_metrics()


async def cache_edge_content(
    request: EdgeRequest, 
    content: Any, 
    ttl_seconds: int = None
):
    """Cache content at edge nodes"""
    await edge_computing_engine.cache_content(request, content, ttl_seconds)


async def get_cached_edge_content(request: EdgeRequest) -> Optional[Any]:
    """Get cached content from edge nodes"""
    return await edge_computing_engine.get_cached_content(request)
