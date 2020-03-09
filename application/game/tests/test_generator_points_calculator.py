import unittest
from decimal import Decimal

from application.game.generator_points_calculator import GeneratorPointsCalculator
from models import Generator, GeneratorPurchase


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
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("1.0")),
                        amount=1,
                    ),
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("0.3")),
                        amount=1,
                    ),
                ]
            ),
        )

        self.assertEqual(
            Decimal("1"),
            GeneratorPointsCalculator.calculate_points(
                [
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("1.0")),
                        amount=1,
                    )
                ]
            ),
        )

        self.assertEqual(
            Decimal("2"),
            GeneratorPointsCalculator.calculate_points(
                [
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("1.0")),
                        amount=2,
                    )
                ]
            ),
        )

        self.assertEqual(
            Decimal("9.5"),
            GeneratorPointsCalculator.calculate_points(
                [
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("1.0")),
                        amount=2,
                    ),
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("2.5")),
                        amount=3,
                    )
                ]
            ),
        )

        self.assertEqual(
            Decimal("1.93"),
            GeneratorPointsCalculator.calculate_points(
                [
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("1")),
                        amount=1,
                    ),
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("0.3")),
                        amount=1,
                    ),
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("0.3")),
                        amount=1,
                    ),
                    GeneratorPurchase(
                        generator=Generator(income_rate=Decimal("0.33")),
                        amount=1,
                    ),
                ]
            ),
        )
