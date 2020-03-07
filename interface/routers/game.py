from fastapi import APIRouter, WebSocket, Security
from starlette.websockets import WebSocketDisconnect

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


@router.websocket('/click')
async def click(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f'Click text was: {data}')
    except WebSocketDisconnect:
        print('disconnected!')
