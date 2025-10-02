"""
Database configuration and connection management
"""

import structlog
from supabase import create_client, Client
from app.core.config import settings

logger = structlog.get_logger()

# Global Supabase client
supabase_client: Client = None


async def init_db():
    """Initialize database connection"""
    global supabase_client
    
    try:
        supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )
        
        # Test connection
        result = supabase_client.table('users').select('id').limit(1).execute()
        
        logger.info("Database connection established successfully")
        return True
        
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise e


def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    if supabase_client is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return supabase_client


async def close_db():
    """Close database connections"""
    global supabase_client
    supabase_client = None
    logger.info("Database connections closed")