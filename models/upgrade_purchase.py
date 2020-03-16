from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class UpgradePurchase(Base):
    __tablename__ = 'upgrade_purchase'
    default_back_populates = 'upgrade_purchases'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates=default_back_populates)

    upgrade_id = Column(Integer, ForeignKey('upgrade.id'))
    upgrade = relationship('Upgrade', back_populates=default_back_populates)
