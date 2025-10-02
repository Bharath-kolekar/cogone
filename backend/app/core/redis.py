"""
Redis configuration and connection management
"""

import structlog
import redis
from app.core.config import settings

logger = structlog.get_logger()

# Global Redis client
redis_client = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    
    try:
        redis_client = redis.from_url(
            settings.UPSTASH_REDIS_REST_URL,
            password=settings.UPSTASH_REDIS_REST_TOKEN,
            decode_responses=True
        )
        
        # Test connection
        redis_client.ping()
        
        logger.info("Redis connection established successfully")
        return True
        
    except Exception as e:
        logger.error("Failed to initialize Redis", error=str(e))
        raise e


def get_redis_client():
    """Get Redis client instance"""
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client


async def close_redis():
    """Close Redis connections"""
    global redis_client
    if redis_client:
        redis_client.close()
        redis_client = None
    logger.info("Redis connections closed")