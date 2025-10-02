from fastapi import APIRouter
router = APIRouter()
@router.post('/request-otp')
async def request_otp(payload: dict):
    return {'ok': True}
@router.post('/verify-otp')
async def verify_otp(payload: dict):
    return {'ok': True, 'user_id':'demo'}
