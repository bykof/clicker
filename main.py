import uvicorn
from fastapi import FastAPI

from interface.routers import users, generators

app = FastAPI()
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(generators.router, prefix='/generators', tags=['Generators'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
