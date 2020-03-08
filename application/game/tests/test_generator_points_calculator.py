import unittest
from decimal import Decimal

from application.game.generator_points_calculator import GeneratorPointsCalculator
from models import Generator


class TestGeneratorPointsCalculator(unittest.TestCase):
    def test_calculate_points(self):
        self.assertEqual(
            Decimal(0),
            GeneratorPointsCalculator.calculate_points([]),
        )

        self.assertEqual(
            Decimal("1.3"),
            GeneratorPointsCalculator.calculate_points(
                [
                    Generator(income_rate=Decimal("1.0")),
                    Generator(income_rate=Decimal("0.3")),
                ]
            ),
        )

        self.assertEqual(
            Decimal("1"),
            GeneratorPointsCalculator.calculate_points(
                [
                    Generator(income_rate=Decimal("1.0")),
                ]
            ),
        )

        self.assertEqual(
            Decimal("1.93"),
            GeneratorPointsCalculator.calculate_points(
                [
                    Generator(income_rate=Decimal("1")),
                    Generator(income_rate=Decimal("0.3")),
                    Generator(income_rate=Decimal("0.3")),
                    Generator(income_rate=Decimal("0.33")),
                ]
            ),
        )
