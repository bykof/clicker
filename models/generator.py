from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

from models.base import Base


class Generator(Base):
    __tablename__ = 'generator'

    id = Column(Integer, primary_key=True)
    base_cost = Column(Float)
    generator_purchases = relationship('GeneratorPurchase', back_populates='generator')
