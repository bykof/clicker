import unittest

from application.game.generator_costs_calculator import GeneratorCostsCalculator
from models import Generator


class TestGeneratorCostsCalculator(unittest.TestCase):
    def test_calculate_costs(self):
        self.assertEqual(1, GeneratorCostsCalculator.calculate(Generator(base_cost=1), 1))
        self.assertEqual(2, GeneratorCostsCalculator.calculate(Generator(base_cost=1), 5))
        self.assertEqual(1174313, GeneratorCostsCalculator.calculate(Generator(base_cost=1), 100))
