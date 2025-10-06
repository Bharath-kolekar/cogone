"""
Multi-Region Optimization System for Cognomega AI
Global performance optimization with intelligent routing and load distribution
"""

import asyncio
import aiohttp
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import structlog
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor

logger = structlog.get_logger()


class Region(str, Enum):
    """Available regions"""
    US_EAST = "us-east-1"
    US_WEST = "us-west-2"
    EU_WEST = "eu-west-1"
    EU_CENTRAL = "eu-central-1"
    ASIA_SOUTHEAST = "ap-southeast-1"
    ASIA_NORTHEAST = "ap-northeast-1"
    AUSTRALIA = "ap-southeast-2"
    SOUTH_AMERICA = "sa-east-1"


class OptimizationStrategy(str, Enum):
    """Optimization strategies"""
    LATENCY_FIRST = "latency_first"
    COST_FIRST = "cost_first"
    PERFORMANCE_FIRST = "performance_first"
    RELIABILITY_FIRST = "reliability_first"
    HYBRID = "hybrid"


class LoadBalanceMode(str, Enum):
    """Load balancing modes"""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    LEAST_RESPONSE_TIME = "least_response_time"
    GEOGRAPHIC = "geographic"
    INTELLIGENT = "intelligent"


@dataclass
class RegionMetrics:
    """Region performance metrics"""
    region: Region
    latency_ms: float
    throughput_rps: float
    error_rate: float
    cpu_usage: float
    memory_usage: float
    cost_per_request: float
    availability: float
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class RouteDecision:
    """Routing decision result"""
    primary_region: Region
    fallback_regions: List[Region]
    routing_strategy: str
    confidence: float
    expected_latency: float
    expected_cost: float
    reasoning: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class GlobalOptimizationConfig:
    """Global optimization configuration"""
    preferred_strategy: OptimizationStrategy
    load_balance_mode: LoadBalanceMode
    max_latency_threshold: float = 500.0  # ms
    min_availability_threshold: float = 0.99
    cost_optimization_enabled: bool = True
    failover_enabled: bool = True
    auto_scaling_enabled: bool = True


class MultiRegionOptimizer:
    """Multi-region optimization engine"""
    
    def __init__(self, config: Optional[GlobalOptimizationConfig] = None):
        self.config = config or GlobalOptimizationConfig(
            preferred_strategy=OptimizationStrategy.HYBRID,
            load_balance_mode=LoadBalanceMode.INTELLIGENT
        )
        
        # Region registry
        self.regions: Dict[Region, Dict[str, Any]] = {
            region: {
                "endpoint": self._get_region_endpoint(region),
                "metrics": RegionMetrics(
                    region=region,
                    latency_ms=100.0,  # Default values
                    throughput_rps=1000.0,
                    error_rate=0.01,
                    cpu_usage=50.0,
                    memory_usage=60.0,
                    cost_per_request=0.001,
                    availability=0.999
                ),
                "status": "healthy",
                "last_check": datetime.now()
            }
            for region in Region
        }
        
        # Load balancing state
        self.region_weights: Dict[Region, float] = {
            region: 1.0 for region in Region
        }
        self.region_connections: Dict[Region, int] = {
            region: 0 for region in Region
        }
        self.region_response_times: Dict[Region, List[float]] = {
            region: [] for region in Region
        }
        
        # Optimization history
        self.routing_history: List[RouteDecision] = []
        self.optimization_stats: Dict[str, Any] = {
            "total_requests": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "average_latency": 0.0,
            "cost_savings": 0.0
        }
        
        # Background tasks
        self._monitoring_task = None
        self._optimization_task = None
        
        # Initialize
        self._start_background_tasks()
    
    def _get_region_endpoint(self, region: Region) -> str:
        """Get region endpoint URL"""
        base_url = "https://api.cognomega.ai"
        region_mapping = {
            Region.US_EAST: f"{base_url}/us-east",
            Region.US_WEST: f"{base_url}/us-west",
            Region.EU_WEST: f"{base_url}/eu-west",
            Region.EU_CENTRAL: f"{base_url}/eu-central",
            Region.ASIA_SOUTHEAST: f"{base_url}/ap-southeast",
            Region.ASIA_NORTHEAST: f"{base_url}/ap-northeast",
            Region.AUSTRALIA: f"{base_url}/ap-australia",
            Region.SOUTH_AMERICA: f"{base_url}/sa-east"
        }
        return region_mapping.get(region, base_url)
    
    def _start_background_tasks(self):
        """Start background monitoring and optimization tasks"""
        self._monitoring_task = asyncio.create_task(self._monitor_regions())
        self._optimization_task = asyncio.create_task(self._optimize_globally())
    
    async def _monitor_regions(self):
        """Monitor all regions for health and performance"""
        while True:
            try:
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
                # Check all regions in parallel
                monitoring_tasks = [
                    self._check_region_health(region) 
                    for region in Region
                ]
                await asyncio.gather(*monitoring_tasks, return_exceptions=True)
                
                # Update region weights based on performance
                await self._update_region_weights()
                
            except Exception as e:
                logger.error("Region monitoring error", error=str(e))
                await asyncio.sleep(60)
    
    async def _check_region_health(self, region: Region):
        """Check health and performance of a specific region"""
        try:
            region_data = self.regions[region]
            endpoint = region_data["endpoint"]
            
            # Perform health check
            start_time = datetime.now()
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(f"{endpoint}/health") as response:
                    response_time = (datetime.now() - start_time).total_seconds() * 1000
                    
                    # Update metrics
                    region_data["metrics"].latency_ms = response_time
                    region_data["metrics"].availability = 1.0 if response.status == 200 else 0.0
                    region_data["status"] = "healthy" if response.status == 200 else "unhealthy"
                    region_data["last_check"] = datetime.now()
                    
                    # Update response time history
                    self.region_response_times[region].append(response_time)
                    if len(self.region_response_times[region]) > 100:
                        self.region_response_times[region].pop(0)
                    
                    logger.debug("Region health check completed", 
                               region=region.value, 
                               latency=response_time,
                               status=region_data["status"])
            
        except Exception as e:
            # Mark region as unhealthy
            self.regions[region]["status"] = "unhealthy"
            self.regions[region]["metrics"].availability = 0.0
            logger.warning("Region health check failed", 
                         region=region.value, 
                         error=str(e))
    
    async def _update_region_weights(self):
        """Update region weights based on performance metrics"""
        try:
            for region in Region:
                region_data = self.regions[region]
                metrics = region_data["metrics"]
                
                # Calculate weight based on multiple factors
                latency_weight = max(0.1, 1.0 - (metrics.latency_ms / 1000.0))
                availability_weight = metrics.availability
                performance_weight = 1.0 - metrics.error_rate
                
                # Combined weight
                combined_weight = (latency_weight * 0.4 + 
                                 availability_weight * 0.4 + 
                                 performance_weight * 0.2)
                
                self.region_weights[region] = max(0.1, combined_weight)
            
            # Normalize weights
            total_weight = sum(self.region_weights.values())
            if total_weight > 0:
                for region in Region:
                    self.region_weights[region] /= total_weight
            
        except Exception as e:
            logger.error("Region weight update error", error=str(e))
    
    async def _optimize_globally(self):
        """Global optimization process"""
        while True:
            try:
                await asyncio.sleep(300)  # Optimize every 5 minutes
                
                # Analyze global performance patterns
                await self._analyze_global_patterns()
                
                # Optimize routing strategies
                await self._optimize_routing_strategies()
                
                # Update optimization statistics
                await self._update_optimization_stats()
                
            except Exception as e:
                logger.error("Global optimization error", error=str(e))
                await asyncio.sleep(300)
    
    async def _analyze_global_patterns(self):
        """Analyze global performance patterns"""
        try:
            # Analyze latency patterns by region
            for region in Region:
                response_times = self.region_response_times[region]
                if response_times:
                    avg_response_time = np.mean(response_times)
                    std_response_time = np.std(response_times)
                    
                    # Update region metrics
                    self.regions[region]["metrics"].latency_ms = avg_response_time
                    
                    # Detect anomalies
                    if std_response_time > avg_response_time * 0.5:
                        logger.warning("High latency variance detected", 
                                     region=region.value,
                                     avg_latency=avg_response_time,
                                     std_latency=std_response_time)
            
            # Analyze global trends
            healthy_regions = [
                region for region, data in self.regions.items()
                if data["status"] == "healthy"
            ]
            
            if len(healthy_regions) < len(Region) * 0.5:
                logger.error("Less than 50% of regions are healthy", 
                           healthy_count=len(healthy_regions),
                           total_regions=len(Region))
            
        except Exception as e:
            logger.error("Global pattern analysis error", error=str(e))
    
    async def _optimize_routing_strategies(self):
        """Optimize routing strategies based on current conditions"""
        try:
            # Analyze current strategy effectiveness
            strategy_performance = await self._analyze_strategy_performance()
            
            # Update strategy if needed
            best_strategy = max(strategy_performance.items(), key=lambda x: x[1])
            if best_strategy[1] > 0.8 and best_strategy[0] != self.config.preferred_strategy:
                logger.info("Switching optimization strategy", 
                          from_strategy=self.config.preferred_strategy.value,
                          to_strategy=best_strategy[0].value,
                          performance=best_strategy[1])
                
                self.config.preferred_strategy = best_strategy[0]
            
        except Exception as e:
            logger.error("Routing strategy optimization error", error=str(e))
    
    async def _analyze_strategy_performance(self) -> Dict[OptimizationStrategy, float]:
        """Analyze performance of different strategies"""
        try:
            performance_scores = {}
            
            # Simulate different strategies
            for strategy in OptimizationStrategy:
                score = await self._simulate_strategy_performance(strategy)
                performance_scores[strategy] = score
            
            return performance_scores
            
        except Exception as e:
            logger.error("Strategy performance analysis error", error=str(e))
            return {strategy: 0.5 for strategy in OptimizationStrategy}
    
    async def _simulate_strategy_performance(self, strategy: OptimizationStrategy) -> float:
        """Simulate performance of a specific strategy"""
        try:
            # Get healthy regions
            healthy_regions = [
                region for region, data in self.regions.items()
                if data["status"] == "healthy"
            ]
            
            if not healthy_regions:
                return 0.0
            
            # Simulate routing decisions
            total_score = 0.0
            test_requests = 100
            
            for _ in range(test_requests):
                route_decision = await self._make_routing_decision(
                    strategy=strategy,
                    test_mode=True
                )
                
                # Calculate score based on strategy goals
                if strategy == OptimizationStrategy.LATENCY_FIRST:
                    score = max(0, 1.0 - (route_decision.expected_latency / 1000.0))
                elif strategy == OptimizationStrategy.COST_FIRST:
                    score = max(0, 1.0 - (route_decision.expected_cost * 1000))
                elif strategy == OptimizationStrategy.PERFORMANCE_FIRST:
                    primary_metrics = self.regions[route_decision.primary_region]["metrics"]
                    score = (primary_metrics.availability * 0.5 + 
                            (1.0 - primary_metrics.error_rate) * 0.5)
                else:  # HYBRID or RELIABILITY_FIRST
                    primary_metrics = self.regions[route_decision.primary_region]["metrics"]
                    score = (primary_metrics.availability * 0.4 +
                            (1.0 - primary_metrics.error_rate) * 0.3 +
                            max(0, 1.0 - route_decision.expected_latency / 1000.0) * 0.3)
                
                total_score += score
            
            return total_score / test_requests
            
        except Exception as e:
            logger.error("Strategy simulation error", error=str(e))
            return 0.5
    
    async def _update_optimization_stats(self):
        """Update optimization statistics"""
        try:
            # Calculate success rate
            total_routes = len(self.routing_history)
            successful_routes = len([
                route for route in self.routing_history
                if route.primary_region and self.regions[route.primary_region]["status"] == "healthy"
            ])
            
            success_rate = successful_routes / total_routes if total_routes > 0 else 0.0
            
            # Calculate average latency
            if self.routing_history:
                avg_latency = np.mean([route.expected_latency for route in self.routing_history[-100:]])
            else:
                avg_latency = 0.0
            
            # Update stats
            self.optimization_stats.update({
                "total_requests": total_routes,
                "successful_routes": successful_routes,
                "failed_routes": total_routes - successful_routes,
                "success_rate": success_rate,
                "average_latency": avg_latency,
                "last_updated": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error("Optimization stats update error", error=str(e))
    
    async def make_routing_decision(
        self, 
        user_location: Optional[Tuple[float, float]] = None,
        request_type: str = "general",
        priority: str = "normal"
    ) -> RouteDecision:
        """Make intelligent routing decision"""
        try:
            # Get healthy regions
            healthy_regions = [
                region for region, data in self.regions.items()
                if data["status"] == "healthy"
            ]
            
            if not healthy_regions:
                raise Exception("No healthy regions available")
            
            # Apply optimization strategy
            if self.config.preferred_strategy == OptimizationStrategy.LATENCY_FIRST:
                decision = await self._latency_first_routing(healthy_regions, user_location)
            elif self.config.preferred_strategy == OptimizationStrategy.COST_FIRST:
                decision = await self._cost_first_routing(healthy_regions)
            elif self.config.preferred_strategy == OptimizationStrategy.PERFORMANCE_FIRST:
                decision = await self._performance_first_routing(healthy_regions)
            elif self.config.preferred_strategy == OptimizationStrategy.RELIABILITY_FIRST:
                decision = await self._reliability_first_routing(healthy_regions)
            else:  # HYBRID
                decision = await self._hybrid_routing(healthy_regions, user_location, request_type)
            
            # Store routing decision
            self.routing_history.append(decision)
            
            # Keep only recent history
            if len(self.routing_history) > 1000:
                self.routing_history = self.routing_history[-1000:]
            
            return decision
            
        except Exception as e:
            logger.error("Routing decision error", error=str(e))
            # Fallback to first healthy region
            healthy_regions = [
                region for region, data in self.regions.items()
                if data["status"] == "healthy"
            ]
            if healthy_regions:
                return RouteDecision(
                    primary_region=healthy_regions[0],
                    fallback_regions=healthy_regions[1:],
                    routing_strategy="fallback",
                    confidence=0.1,
                    expected_latency=1000.0,
                    expected_cost=0.01,
                    reasoning="Fallback routing due to error"
                )
            else:
                raise Exception("No regions available for routing")
    
    async def _latency_first_routing(
        self, 
        healthy_regions: List[Region], 
        user_location: Optional[Tuple[float, float]] = None
    ) -> RouteDecision:
        """Latency-first routing strategy"""
        try:
            # Sort regions by latency
            region_latencies = [
                (region, self.regions[region]["metrics"].latency_ms)
                for region in healthy_regions
            ]
            region_latencies.sort(key=lambda x: x[1])
            
            primary_region = region_latencies[0][0]
            fallback_regions = [region for region, _ in region_latencies[1:3]]
            
            return RouteDecision(
                primary_region=primary_region,
                fallback_regions=fallback_regions,
                routing_strategy="latency_first",
                confidence=0.9,
                expected_latency=region_latencies[0][1],
                expected_cost=self.regions[primary_region]["metrics"].cost_per_request,
                reasoning=f"Selected {primary_region.value} for lowest latency ({region_latencies[0][1]:.1f}ms)"
            )
            
        except Exception as e:
            logger.error("Latency-first routing error", error=str(e))
            raise
    
    async def _cost_first_routing(self, healthy_regions: List[Region]) -> RouteDecision:
        """Cost-first routing strategy"""
        try:
            # Sort regions by cost
            region_costs = [
                (region, self.regions[region]["metrics"].cost_per_request)
                for region in healthy_regions
            ]
            region_costs.sort(key=lambda x: x[1])
            
            primary_region = region_costs[0][0]
            fallback_regions = [region for region, _ in region_costs[1:3]]
            
            return RouteDecision(
                primary_region=primary_region,
                fallback_regions=fallback_regions,
                routing_strategy="cost_first",
                confidence=0.8,
                expected_latency=self.regions[primary_region]["metrics"].latency_ms,
                expected_cost=region_costs[0][1],
                reasoning=f"Selected {primary_region.value} for lowest cost (${region_costs[0][1]:.4f}/request)"
            )
            
        except Exception as e:
            logger.error("Cost-first routing error", error=str(e))
            raise
    
    async def _performance_first_routing(self, healthy_regions: List[Region]) -> RouteDecision:
        """Performance-first routing strategy"""
        try:
            # Calculate performance score for each region
            region_scores = []
            for region in healthy_regions:
                metrics = self.regions[region]["metrics"]
                # Performance score based on availability and error rate
                score = metrics.availability * (1.0 - metrics.error_rate)
                region_scores.append((region, score))
            
            region_scores.sort(key=lambda x: x[1], reverse=True)
            
            primary_region = region_scores[0][0]
            fallback_regions = [region for region, _ in region_scores[1:3]]
            
            return RouteDecision(
                primary_region=primary_region,
                fallback_regions=fallback_regions,
                routing_strategy="performance_first",
                confidence=0.85,
                expected_latency=self.regions[primary_region]["metrics"].latency_ms,
                expected_cost=self.regions[primary_region]["metrics"].cost_per_request,
                reasoning=f"Selected {primary_region.value} for best performance (score: {region_scores[0][1]:.3f})"
            )
            
        except Exception as e:
            logger.error("Performance-first routing error", error=str(e))
            raise
    
    async def _reliability_first_routing(self, healthy_regions: List[Region]) -> RouteDecision:
        """Reliability-first routing strategy"""
        try:
            # Sort regions by availability
            region_availability = [
                (region, self.regions[region]["metrics"].availability)
                for region in healthy_regions
            ]
            region_availability.sort(key=lambda x: x[1], reverse=True)
            
            primary_region = region_availability[0][0]
            fallback_regions = [region for region, _ in region_availability[1:3]]
            
            return RouteDecision(
                primary_region=primary_region,
                fallback_regions=fallback_regions,
                routing_strategy="reliability_first",
                confidence=0.9,
                expected_latency=self.regions[primary_region]["metrics"].latency_ms,
                expected_cost=self.regions[primary_region]["metrics"].cost_per_request,
                reasoning=f"Selected {primary_region.value} for highest availability ({region_availability[0][1]:.3f})"
            )
            
        except Exception as e:
            logger.error("Reliability-first routing error", error=str(e))
            raise
    
    async def _hybrid_routing(
        self, 
        healthy_regions: List[Region], 
        user_location: Optional[Tuple[float, float]] = None,
        request_type: str = "general"
    ) -> RouteDecision:
        """Hybrid routing strategy combining multiple factors"""
        try:
            # Calculate composite score for each region
            region_scores = []
            for region in healthy_regions:
                metrics = self.regions[region]["metrics"]
                
                # Weighted score combining multiple factors
                latency_score = max(0, 1.0 - (metrics.latency_ms / 1000.0))
                availability_score = metrics.availability
                cost_score = max(0, 1.0 - (metrics.cost_per_request * 1000))
                performance_score = 1.0 - metrics.error_rate
                
                # Adjust weights based on request type
                if request_type == "critical":
                    # Prioritize availability and performance
                    composite_score = (availability_score * 0.4 + 
                                     performance_score * 0.4 + 
                                     latency_score * 0.2)
                elif request_type == "cost_sensitive":
                    # Prioritize cost and availability
                    composite_score = (cost_score * 0.4 + 
                                     availability_score * 0.3 + 
                                     latency_score * 0.2 + 
                                     performance_score * 0.1)
                else:
                    # Balanced approach
                    composite_score = (latency_score * 0.3 + 
                                     availability_score * 0.3 + 
                                     performance_score * 0.2 + 
                                     cost_score * 0.2)
                
                region_scores.append((region, composite_score))
            
            region_scores.sort(key=lambda x: x[1], reverse=True)
            
            primary_region = region_scores[0][0]
            fallback_regions = [region for region, _ in region_scores[1:3]]
            
            return RouteDecision(
                primary_region=primary_region,
                fallback_regions=fallback_regions,
                routing_strategy="hybrid",
                confidence=0.8,
                expected_latency=self.regions[primary_region]["metrics"].latency_ms,
                expected_cost=self.regions[primary_region]["metrics"].cost_per_request,
                reasoning=f"Selected {primary_region.value} using hybrid strategy (score: {region_scores[0][1]:.3f})"
            )
            
        except Exception as e:
            logger.error("Hybrid routing error", error=str(e))
            raise
    
    async def _make_routing_decision(
        self, 
        strategy: OptimizationStrategy,
        test_mode: bool = False
    ) -> RouteDecision:
        """Make routing decision for testing/simulation"""
        healthy_regions = [
            region for region, data in self.regions.items()
            if data["status"] == "healthy"
        ]
        
        if strategy == OptimizationStrategy.LATENCY_FIRST:
            return await self._latency_first_routing(healthy_regions)
        elif strategy == OptimizationStrategy.COST_FIRST:
            return await self._cost_first_routing(healthy_regions)
        elif strategy == OptimizationStrategy.PERFORMANCE_FIRST:
            return await self._performance_first_routing(healthy_regions)
        elif strategy == OptimizationStrategy.RELIABILITY_FIRST:
            return await self._reliability_first_routing(healthy_regions)
        else:
            return await self._hybrid_routing(healthy_regions)
    
    async def get_global_metrics(self) -> Dict[str, Any]:
        """Get global optimization metrics"""
        try:
            healthy_regions = [
                region for region, data in self.regions.items()
                if data["status"] == "healthy"
            ]
            
            region_metrics = {}
            for region in Region:
                region_data = self.regions[region]
                region_metrics[region.value] = {
                    "status": region_data["status"],
                    "latency_ms": region_data["metrics"].latency_ms,
                    "availability": region_data["metrics"].availability,
                    "error_rate": region_data["metrics"].error_rate,
                    "cost_per_request": region_data["metrics"].cost_per_request,
                    "weight": self.region_weights[region],
                    "last_check": region_data["last_check"].isoformat()
                }
            
            return {
                "global_config": {
                    "strategy": self.config.preferred_strategy.value,
                    "load_balance_mode": self.config.load_balance_mode.value,
                    "max_latency_threshold": self.config.max_latency_threshold,
                    "min_availability_threshold": self.config.min_availability_threshold
                },
                "region_metrics": region_metrics,
                "optimization_stats": self.optimization_stats,
                "healthy_regions_count": len(healthy_regions),
                "total_regions_count": len(Region),
                "global_health_score": len(healthy_regions) / len(Region),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Global metrics error", error=str(e))
            return {}
    
    async def optimize_region_selection(
        self, 
        user_context: Dict[str, Any]
    ) -> RouteDecision:
        """Optimize region selection based on user context"""
        try:
            user_location = user_context.get("location")
            request_type = user_context.get("request_type", "general")
            priority = user_context.get("priority", "normal")
            
            decision = await self.make_routing_decision(
                user_location=user_location,
                request_type=request_type,
                priority=priority
            )
            
            logger.info("Region selection optimized", 
                       primary_region=decision.primary_region.value,
                       strategy=decision.routing_strategy,
                       confidence=decision.confidence,
                       expected_latency=decision.expected_latency)
            
            return decision
            
        except Exception as e:
            logger.error("Region selection optimization error", error=str(e))
            raise


# Global multi-region optimizer instance
multi_region_optimizer = MultiRegionOptimizer()


# Convenience functions
async def get_global_metrics() -> Dict[str, Any]:
    """Get global optimization metrics"""
    return await multi_region_optimizer.get_global_metrics()


async def optimize_region_selection(user_context: Dict[str, Any]) -> RouteDecision:
    """Optimize region selection based on user context"""
    return await multi_region_optimizer.optimize_region_selection(user_context)


async def make_routing_decision(
    user_location: Optional[Tuple[float, float]] = None,
    request_type: str = "general",
    priority: str = "normal"
) -> RouteDecision:
    """Make intelligent routing decision"""
    return await multi_region_optimizer.make_routing_decision(
        user_location=user_location,
        request_type=request_type,
        priority=priority
    )
