from fastapi import APIRouter

router = APIRouter()


@router.get('/available')
async def available_upgrades():
    return {'message': 'Hello World'}


@router.post('/buy')
async def buy_upgrade():
    return {'message': 'Hello World'}
