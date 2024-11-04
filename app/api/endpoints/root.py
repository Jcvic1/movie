from fastapi import APIRouter

router = APIRouter()


@router.get('/status/')
async def health_check():
    return {'status': 200, 'state': 'ready'}
