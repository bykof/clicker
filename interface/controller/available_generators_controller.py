from typing import List

from application.game.generator_points_calculator import GeneratorPointsCalculator
from interface.controller.base.DBController import DBController
from models import Generator, User


class AvailableGeneratorsController(DBController):
    def available_generators(self, user: User) -> List[Generator]:
        points = GeneratorPointsCalculator.calculate_points(user.generator_purchases)
        return self.db.query(Generator).filter(Generator.available_at_points_per_second <= points).all()
