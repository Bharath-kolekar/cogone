from fastapi import APIRouter, Request
router = APIRouter()
@router.post('/razorpay')
async def razorpay_webhook(req: Request):
    payload = await req.json()
    return {'ok': True, 'event': payload.get('event')}
