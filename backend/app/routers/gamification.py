from fastapi import APIRouter
router = APIRouter()
@router.post('/award')
async def award(payload: dict):
    return {'awarded': 10}
