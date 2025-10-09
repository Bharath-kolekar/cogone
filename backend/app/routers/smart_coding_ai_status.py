from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.smart_coding_ai_validation import get_event_queue, ValidationStatusEvent, demo_emit_validation_events
import asyncio
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.websocket("/ws/smart-coding-ai/status/{session_id}")
async def websocket_status_stream(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for streaming validation events"""
    import structlog
    logger = structlog.get_logger()
    
    await websocket.accept()
    logger.info("WebSocket connected", session_id=session_id)
    
    queue = get_event_queue(session_id)
    logger.info("Got event queue", session_id=session_id, queue_size=queue.qsize())
    
    try:
        while True:
            event: ValidationStatusEvent = await queue.get()
            logger.info("Sending event", session_id=session_id, step=event.step, status=event.status)
            await websocket.send_json(event.model_dump())  # Use model_dump() for Pydantic v2
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected", session_id=session_id)
    except Exception as e:
        logger.error("WebSocket error", session_id=session_id, error=str(e))

@router.post("/test/smart-coding-ai/emit-events/{session_id}")
async def test_emit_events(session_id: str):
    """Trigger demo validation events for testing"""
    logger.info("API endpoint hit - starting demo events", session_id=session_id)
    
    # Get the current event loop
    loop = asyncio.get_event_loop()
    
    # Schedule the demo task on the event loop
    task = loop.create_task(demo_emit_validation_events(session_id))
    logger.info("Demo task created", session_id=session_id, task_id=id(task))
    
    return {"status": "started", "session_id": session_id, "message": "Events task created"}


@router.get("/health")
async def health_check():
    """
    Health check endpoint for smart-coding-ai-status service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "smart-coding-ai-status",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )
