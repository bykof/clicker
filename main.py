import os

import uvicorn

import sentry_sdk
from sentry_sdk.integrations.excepthook import ExcepthookIntegration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from interface.routers import users, generators, game, upgrades, dashboard, ws_docs
from constants import SENTRY_URL

if SENTRY_URL:
    sentry_sdk.init(SENTRY_URL, integrations=[ExcepthookIntegration(always_run=True)])

app = FastAPI(title='Clicker', description='The generic clicker games platform')
app.mount(
    '/static',
    StaticFiles(directory=os.path.join('interface', 'static')),
    name='static',
)
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(generators.router, prefix='/generators', tags=['Generators'])
app.include_router(upgrades.router, prefix='/upgrades', tags=['Upgrades'])
app.include_router(game.router, prefix='/game', tags=['Game'])
app.include_router(dashboard.router, prefix='/dashboard')
app.include_router(ws_docs.router, prefix='/ws-docs')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
