import asyncio
from typing import Union

from fastapi import APIRouter, WebSocket, Depends, status
from fastapi.websockets import WebSocketDisconnect
from websockets import ConnectionClosedOK

from infrastructure.redis_balance_client import RedisBalanceClient
from interface.exceptions.mutex_already_acquired import MutexAlreadyAcquired
from interface.services.game_service import GameService
from interface.utils import get_current_websocket_user
from models import User

router = APIRouter()


@router.websocket('/balance')
async def balance(websocket: WebSocket, user: Union[User, None] = Depends(get_current_websocket_user)):
    if user is None:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()
    balance_client = RedisBalanceClient(user)
    game_service = GameService(user, balance_client)
    try:
        while True:
            await websocket.send_json({
                'points': game_service.get_current_points(),
            })
            await asyncio.sleep(1)
    except (WebSocketDisconnect, ConnectionClosedOK):
        pass


@router.websocket('/generators')
async def generators(websocket: WebSocket, user: Union[User, None] = Depends(get_current_websocket_user)):
    if user is None:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    balance_client = RedisBalanceClient(user)
    game_service = GameService(user, balance_client)

    try:
        game_service.acquire_generators_mutex()
        await websocket.accept()

        while True:
            points = game_service.add_generator_points_to_balance()
            await websocket.send_json({
                'points': int(points),
            })
            await asyncio.sleep(1)
    except (WebSocketDisconnect, ConnectionClosedOK):
        pass
    except MutexAlreadyAcquired:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        game_service.release_generators_mutex()


@router.websocket('/click')
async def click(websocket: WebSocket, user: Union[User, None] = Depends(get_current_websocket_user)):
    if user is None:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    balance_client = RedisBalanceClient(user)
    game_service = GameService(user, balance_client)

    try:
        game_service.acquire_click_mutex()
        await websocket.accept()

        while True:
            await websocket.receive_text()
            game_service.add_click_to_balance()
    except (WebSocketDisconnect, ConnectionClosedOK):
        pass
    except MutexAlreadyAcquired:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        game_service.release_click_mutex()
