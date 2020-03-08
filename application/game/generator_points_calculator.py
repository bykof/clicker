import functools
from decimal import Decimal, Context
from typing import List

from models import Generator


class GeneratorPointsCalculator:
    @staticmethod
    def add(value: Decimal, income_rate: Decimal) -> Decimal:
        return Context(prec=6).add(income_rate, value)

    @staticmethod
    def calculate_points(generators: List[Generator]) -> Decimal:
        return functools.reduce(GeneratorPointsCalculator.add, [generator.income_rate for generator in generators])
