from decimal import Decimal

from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.orm import relationship

from models.base import Base


class Generator(Base):
    __tablename__ = 'generator'

    id = Column(Integer, primary_key=True)
    base_cost: Decimal = Column(Numeric)
    income_rate: Decimal = Column(Numeric)
    generator_purchases = relationship('GeneratorPurchase', back_populates='generator')