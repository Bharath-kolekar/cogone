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
    
    # Temporarily skip Supabase initialization to get the backend running
    # This allows all other features (WebSocket, APIs, etc.) to work
    # TODO: Re-enable when Supabase credentials are configured
    try:
        if not settings.SUPABASE_URL or settings.SUPABASE_URL == "your-project-url.supabase.co":
            logger.info("Supabase not configured, skipping database initialization (development mode)")
            return False
            
        # Create synchronous client
        supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )
        
        logger.info("Database connection established successfully")
        return True
        
    except Exception as e:
        logger.warning("Failed to initialize database, continuing in development mode", error=str(e))
        # Don't raise - allow app to start without database
        return False


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