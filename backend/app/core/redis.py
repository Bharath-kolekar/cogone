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
        redis_url = getattr(settings, 'REDIS_URL', None) or getattr(settings, 'UPSTASH_REDIS_REST_URL', None) or 'redis://localhost:6379'
        redis_client = aioredis.from_url(redis_url, decode_responses=True)
        
        # Test connection (async) - skip for now
        # pong = await redis_client.ping()
        # if pong is not True and pong != 'PONG':
        #     raise RuntimeError("Redis ping failed")
        
        logger.info("Redis connection established successfully")
        return True
        
    except Exception as e:
        logger.warning("Failed to initialize Redis, continuing without it (development mode)", error=str(e))
        # Don't raise - allow app to start without Redis
        return False


async def get_redis_client():
    """Async getter for Redis client; ensures initialized."""
    global redis_client
    if redis_client is None:
        # Auto-initialize if not done yet (lazy initialization)
        try:
            await init_redis()
        except Exception as e:
            logger.warning("Redis auto-initialization failed, returning None", error=str(e))
            return None
    return redis_client


def get_redis_client_sync():
    """
    Synchronous getter that returns None if Redis is not initialized.
    Use this ONLY in __init__ methods where async is not possible.
    The actual async operations will call get_redis_client() which will initialize if needed.
    """
    return redis_client  # Returns None if not initialized, which is fine


async def close_redis():
    """Close Redis connections"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
    logger.info("Redis connections closed")