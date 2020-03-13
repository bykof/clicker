from application.game.generator_costs_calculator import GeneratorCostsCalculator
from infrastructure.redis_balance_client import RedisBalanceClient
from interface.controller.base.DBController import DBController
from interface.exceptions.not_sufficient_points import NotSufficientPoints
from interface.services.game_service import GameService
from models import User, Generator, GeneratorPurchase


class PurchaseController(DBController):
    def buy_generator(self, user: User, generator: Generator):
        game_service = GameService(user, RedisBalanceClient(user))
        points = game_service.get_current_points()
        user_generator_purchase = self.db.query(GeneratorPurchase).filter(
            GeneratorPurchase.user == user,
            GeneratorPurchase.generator == generator,
        ).first()

        amount = user_generator_purchase.amount if user_generator_purchase else 0
        costs = GeneratorCostsCalculator.calculate(generator_to_buy=generator, purchased_generators=amount)
        if points < costs:
            raise NotSufficientPoints()

        if amount == 0:
            user_generator_purchase = GeneratorPurchase(user=user, generator=generator, amount=1)
            self.db.add(user_generator_purchase)
        else:
            user_generator_purchase.amount += 1

        self.db.commit()
        game_service.subtract_points(costs=costs)
        return user_generator_purchase
