import asyncio

from fastapi import APIRouter, WebSocket, Depends, status
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session
from websockets import ConnectionClosed

from infrastructure.redis_balance_client import RedisBalanceClient
from interface.exceptions.mutex_already_acquired import MutexAlreadyAcquired
from interface.services.game_service import GameService
from interface.utils import get_current_websocket_user, get_db
from models import User

router = APIRouter()


@router.websocket('/balance')
async def balance(
    websocket: WebSocket,
    user: User = Depends(get_current_websocket_user),
    db: Session = Depends(get_db),
):
    await websocket.accept()
    balance_client = RedisBalanceClient(user)
    game_service = GameService(user, balance_client)
    try:
        while True:
            db.refresh(user)
            await websocket.send_json({
                'points': game_service.get_current_points(),
            })
            await asyncio.sleep(1)
    except (WebSocketDisconnect, ConnectionClosedOK):
        pass


@router.websocket('/generators')
async def generators(
    websocket: WebSocket,
    user: User = Depends(get_current_websocket_user),
    db: Session = Depends(get_db),
):
    balance_client = RedisBalanceClient(user)
    game_service = GameService(user, balance_client)

    try:
        game_service.acquire_generators_mutex()
        await websocket.accept()

        while True:
            db.refresh(user)
            points = game_service.add_generator_points_to_balance()
            await websocket.send_json({
                'points': int(points),
            })
            await asyncio.sleep(1)
    except MutexAlreadyAcquired:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except (WebSocketDisconnect, ConnectionClosed):
        game_service.release_generators_mutex()


@router.websocket('/click')
async def click(websocket: WebSocket, user: User = Depends(get_current_websocket_user)):
    balance_client = RedisBalanceClient(user)
    game_service = GameService(user, balance_client)

    try:
        game_service.acquire_click_mutex()
        await websocket.accept()

        while True:
            await websocket.receive_text()
            points = game_service.add_click_to_balance()
            await websocket.send_json({
                'points': int(points),
            })
    except MutexAlreadyAcquired:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except (WebSocketDisconnect, ConnectionClosed):
        game_service.release_click_mutex()
