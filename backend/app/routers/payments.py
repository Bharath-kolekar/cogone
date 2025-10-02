from fastapi import APIRouter
router = APIRouter()
@router.post('/create-order')
async def create_order(payload: dict):
    return {'order_id':'demo'}
@router.get('/verify/{payment_id}')
async def verify(payment_id: str):
    return {'ok': True}
