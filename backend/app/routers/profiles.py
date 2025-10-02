from fastapi import APIRouter
router = APIRouter()
@router.get('/me')
async def me():
    return {'user_id':'demo','email':'demo@example.com','role':'user'}
