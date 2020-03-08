from application.game.generator_points_calculator import GeneratorPointsCalculator
from interface.abstracts.balance_client import BalanceClient
from models import User


class GameService:
    def __int__(self, user: User, balance_client: BalanceClient):
        self.user = user
        self.balance_client = balance_client

    def add_click_to_balance(self):
        # TODO: correct points
        points = 1
        self.balance_client.add_points(points=points)

    def add_generator_points_to_balance(self):
        points = GeneratorPointsCalculator.calculate_points(self.user.generator_purchases.all())
        self.balance_client.add_points(points=points)
