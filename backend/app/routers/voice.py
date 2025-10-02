from fastapi import APIRouter
router = APIRouter()
@router.post('/intent')
async def intent(payload: dict):
    return {'plan': {'steps': [{'id':'scaffold','action':'scaffold'}], 'confidence':0.5}}
