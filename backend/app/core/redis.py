"""
Redis configuration and connection management
"""

import structlog
from redis import asyncio as aioredis
from app.core.config import settings

logger = structlog.get_logger()

# Global Redis client (async)
redis_client = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    
    try:
        # Prefer a standard Redis URL if available; fallback to configured URL
        redis_url = getattr(settings, 'REDIS_URL', None) or getattr(settings, 'UPSTASH_REDIS_URL', None) or 'redis://localhost:6379'
        redis_client = aioredis.from_url(redis_url, decode_responses=True)
        
        # Test connection (async)
        pong = await redis_client.ping()
        if pong is not True and pong != 'PONG':
            raise RuntimeError("Redis ping failed")
        
        logger.info("Redis connection established successfully")
        return True
        
    except Exception as e:
        logger.error("Failed to initialize Redis", error=str(e))
        raise e


async def get_redis_client():
    """Async getter for Redis client; ensures initialized."""
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client


async def close_redis():
    """Close Redis connections"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
    logger.info("Redis connections closed")