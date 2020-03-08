from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from interface.controller.users_controller import UsersController
from interface.models.users import RegisterData
from interface.utils import get_db
from interface.models.users import User

router = APIRouter()


@router.post('/register', response_model=User)
async def register_user(register_data: RegisterData, db: Session = Depends(get_db)):
    return UsersController(db).register(register_data)


@router.post('/token')
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UsersController(db).login(form_data)
