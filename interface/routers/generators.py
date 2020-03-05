from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def list_generators():
    return {'message': 'Hello World'}


@router.get('/buy')
async def buy_generator():
    return {'message': 'Hello World'}
