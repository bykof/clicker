from pydantic import BaseModel


class Upgrade(BaseModel):
    id: str
    multiplier: float
    cost: float
    order: int

    class Config:
        orm_mode = True


class UpgradePurchase(BaseModel):
    upgrade: Upgrade

    class Config:
        orm_mode = True
