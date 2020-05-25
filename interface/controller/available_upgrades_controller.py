from typing import List

from application.game.generator_points_calculator import GeneratorPointsCalculator
from interface.controller.base.DBController import DBController
from models import Generator, User, Upgrade


class AvailableUpgradesController(DBController):
    def available_upgrades(self, user: User) -> List[Upgrade]:
        points = GeneratorPointsCalculator.calculate_points(user.generator_purchases)
        return self.db.query(Upgrade).filter(
            Upgrade.available_at <= points
        ).filter(
            ~Upgrade.id.in_([upgrade_purchase.upgrade.id for upgrade_purchase in user.upgrade_purchases])
        ).all()
