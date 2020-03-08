from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from interface.abstracts.balance_client import BalanceClient
from interface.controller.game_controller import GameController
from interface.services.game_service import GameService

router = APIRouter()


@router.websocket('/balance')
async def balance(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f'Balance text was: {data}')
    except WebSocketDisconnect:
        print('disconnected!')


@router.websocket('/click',)
async def click(websocket: WebSocket):
    await websocket.accept()
    balance_client = BalanceClient()
    game_service = GameService()
    game_controller = GameController()
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        print('disconnected!')
