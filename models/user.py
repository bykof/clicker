from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    created = Column(DateTime)
    inventories = relationship('GeneratorPurchase', back_populates='user')
