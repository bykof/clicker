from pydantic import BaseModel


class Generator(BaseModel):
    id: str
    income_rate: float
    order: int

    class Config:
        orm_mode = True


class GeneratorPurchase(BaseModel):
    generator: Generator
    amount: int

    class Config:
        orm_mode = True
