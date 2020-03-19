from decimal import Decimal

from application.game.generator_points_calculator import GeneratorPointsCalculator
from application.game.upgrade_points_calculator import UpgradePointsCalculator
from infrastructure.abstracts import BalanceClient
from models import User


class GameService:
    def __init__(self, user: User, balance_client: BalanceClient):
        self.user = user
        self.balance_client = balance_client

    def acquire_click_mutex(self):
        self.balance_client.acquire_click_mutex()

    def release_click_mutex(self):
        self.balance_client.release_click_mutex()

    def acquire_generators_mutex(self):
        self.balance_client.acquire_generators_mutex()

    def release_generators_mutex(self):
        self.balance_client.release_generators_mutex()

    def get_current_points(self):
        return self.balance_client.get_points()

    def add_click_to_balance(self):
        points = UpgradePointsCalculator.calculate_points(self.user.upgrade_purchases)
        self.balance_client.add_points(points=points)

    def add_generator_points_to_balance(self) -> Decimal:
        points = GeneratorPointsCalculator.calculate_points(self.user.generator_purchases)
        self.balance_client.add_points(points=int(points))
        return points

    def subtract_points(self, costs: int):
        self.balance_client.subtract_points(costs)
