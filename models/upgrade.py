from decimal import Decimal

from sqlalchemy import Column, Numeric, Integer
from sqlalchemy.orm import relationship

from models.base import Base


class Upgrade(Base):
    __tablename__ = 'upgrade'
    id: int = Column(Integer, primary_key=True)
    cost: Decimal = Column(Numeric)
    available_at: Decimal = Column(Numeric)
    multiplier: Decimal = Column(Numeric)
    upgrade_purchases = relationship('UpgradePurchase', back_populates='upgrade')
    order: int = Column(Integer)
