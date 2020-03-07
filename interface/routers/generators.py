from fastapi import APIRouter

router = APIRouter()


@router.get('/available')
async def available_generators():
    return {'message': 'Hello World'}


@router.post('/buy')
async def buy_generator():
    return {'message': 'Hello World'}
