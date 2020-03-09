from decimal import Decimal
from typing import List

from models import GeneratorPurchase


class GeneratorPointsCalculator:
    @staticmethod
    def calculate_points(generator_purchases: List[GeneratorPurchase]) -> Decimal:
        return sum([
            generator_purchase.generator.income_rate * generator_purchase.amount
            for generator_purchase in generator_purchases
        ])
