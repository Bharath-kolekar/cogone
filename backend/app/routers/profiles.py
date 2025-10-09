from fastapi import APIRouter
router = APIRouter()
@router.get('/me')
async def me():
    return {'user_id':'demo','email':'demo@example.com','role':'user'}


@router.get("/health")
async def health_check():
    """
    Health check endpoint for profiles service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "profiles",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )
