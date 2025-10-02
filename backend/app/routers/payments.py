from fastapi import APIRouter, Request
router = APIRouter()

@router.post('/create-order')
async def create_order(payload: dict):
    return {'order_id':'demo'}

@router.get('/verify/{payment_id}')
async def verify(payment_id: str):
    return {'ok': True}

@router.get('/payment-methods')
async def get_payment_methods(request: Request):
    # Access currency from request query parameters or headers
    currency = request.query_params.get('currency', 'INR')
    return {'payment_methods': [], 'currency': currency}
