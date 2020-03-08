from fastapi import APIRouter, Depends

from interface.utils import oauth2_scheme

router = APIRouter()


@router.get('/available')
async def available_generators(token: str = Depends(oauth2_scheme)):
    return {'message': 'token'}


@router.post('/buy')
async def buy_generator():
    return {'message': 'Hello World'}
