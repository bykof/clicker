from datetime import datetime

from pydantic import BaseModel


class RegisterData(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: str
    username: str
    created: datetime

    class Config:
        orm_mode = True
