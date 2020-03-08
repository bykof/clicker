from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class GeneratorPurchase(Base):
    __tablename__ = 'generator_purchase'
    default_back_populates = 'generator_purchases'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates=default_back_populates)

    generator_id = Column(Integer, ForeignKey('generator.id'))
    generator = relationship('Generator', back_populates=default_back_populates)
    amount = Column(Integer)
