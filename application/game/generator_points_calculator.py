from decimal import Decimal
from typing import List

from models import Generator


class GeneratorPointsCalculator:
    @staticmethod
    def calculate_points(generators: List[Generator]) -> Decimal:
        return sum([generator.income_rate for generator in generators])
