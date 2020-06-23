from typing import Union

from fastapi import Depends, Cookie, WebSocket, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker, Session

from infrastructure.database_engine import engine
from interface.controller.users_controller import UsersController
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = UsersController(db).get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def get_current_websocket_user(
    websocket: WebSocket,
    db: Session = Depends(get_db),
) -> [User, None]:
    token = websocket.query_params.get('token', '')

    if token == '':
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user = UsersController(db).get_user_by_token(websocket.query_params.get('token', ''))

    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    else:
        return user
