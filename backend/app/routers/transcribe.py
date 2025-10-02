from fastapi import APIRouter, UploadFile, File
router = APIRouter()
@router.post('/transcribe')
async def transcribe(file: UploadFile = File(...)):
    return {'transcript':'demo transcript'}
