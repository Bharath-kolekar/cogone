from fastapi import APIRouter, UploadFile, File
router = APIRouter()
@router.post('/transcribe')
async def transcribe(file: UploadFile = File(...)):
    return {'transcript':'demo transcript'}


@router.get("/health")
async def health_check():
    """
    Health check endpoint for transcribe service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "transcribe",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )
