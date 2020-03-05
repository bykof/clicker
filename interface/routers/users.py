from fastapi import APIRouter

router = APIRouter()


@router.get('/register')
async def register_user():
    return {'message': 'Hello World'}


@router.get('/login')
async def login_user():
    return {'message': 'Hello World'}
