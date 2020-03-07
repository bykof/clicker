from fastapi import APIRouter

router = APIRouter()


@router.post('/register')
async def register_user():
    return {'message': 'Hello World'}


@router.post('/login')
async def login_user():
    return {'message': 'Hello World'}
