from decimal import Decimal

from application.game.generator_costs_calculator import GeneratorCostsCalculator
from infrastructure.redis_balance_client import RedisBalanceClient
from interface.controller.base.DBController import DBController
from interface.exceptions.not_sufficient_points import NotSufficientPoints
from interface.exceptions.upgrade_already_bought_error import UpgradeAlreadyBoughtError
from interface.services.game_service import GameService
from models import User, Generator, GeneratorPurchase, Upgrade, UpgradePurchase


class PurchaseController(DBController):
    def buy_generator(self, user: User, generator: Generator) -> GeneratorPurchase:
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

        game_service.subtract_points(costs=int(costs))
        if amount == 0:
            user_generator_purchase = GeneratorPurchase(user=user, generator=generator, amount=1)
            self.db.add(user_generator_purchase)
        else:
            user_generator_purchase.amount += 1

        self.db.commit()
        return user_generator_purchase

    def buy_upgrade(self, user: User, upgrade: Upgrade) -> UpgradePurchase:

        for upgrade_purchase in user.upgrade_purchases:
            if upgrade_purchase.upgrade.id == upgrade.id:
                raise UpgradeAlreadyBoughtError(user, upgrade)

        game_service = GameService(user, RedisBalanceClient(user))
        points = game_service.get_current_points()

        if points < upgrade.cost:
            raise NotSufficientPoints()

        game_service.subtract_points(costs=int(upgrade.cost))
        user_upgrade_purchase = UpgradePurchase(user=user, upgrade=upgrade)
        self.db.add(user_upgrade_purchase)
        self.db.commit()
        return user_upgrade_purchase
