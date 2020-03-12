import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from interface.routers import users, generators, game, upgrades

app = FastAPI()
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(generators.router, prefix='/generators', tags=['Generators'])
app.include_router(upgrades.router, prefix='/upgrades', tags=['Upgrades'])
app.include_router(game.router, prefix='/game', tags=['Game'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
