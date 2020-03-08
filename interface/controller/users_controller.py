from datetime import timedelta, datetime
from typing import Union

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from application.user.user_password_hasher import UserPasswordHasher
from constants import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS
from interface.models.users import RegisterData
from models import User
from models.factories.user_factory import UserFactory


class UsersController:
    def __init__(self, db):
        self.db = db

    def get_user(self, username: str) -> Union[User, None]:
        return self.db.query(User).filter(User.username == username).first()

    def authenticate_user(self, username: str, password: str) -> Union[User, None]:
        user = self.get_user(username)
        if not user:
            return None
        if not UserPasswordHasher.verify(user.password, password):
            return None
        return user

    @staticmethod
    def create_access_token(*, data: dict, expires_delta: timedelta = None) -> bytes:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def login(self, form_data: OAuth2PasswordRequestForm):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = UsersController.create_access_token(
            data={'sub': user.username},
            expires_delta=access_token_expires,
        )
        return {'access_token': access_token, 'token_type': 'bearer'}

    def register(self, register_data: RegisterData):
        if self.get_user(register_data.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
        user = UserFactory.create(
            username=register_data.username,
            password=register_data.password,
        )
        self.db.add(user)
        self.db.commit()
        return user
