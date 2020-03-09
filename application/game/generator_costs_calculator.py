import math

from constants import GENERATOR_MULTIPLIER
from models import Generator


class GeneratorCostsCalculator:

    @staticmethod
    def calculate(generator_to_buy: Generator, purchased_generators: int) -> float:
        return math.floor(generator_to_buy.base_cost * math.pow(GENERATOR_MULTIPLIER, purchased_generators))
