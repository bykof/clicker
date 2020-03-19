import unittest

from application.game.upgrade_points_calculator import UpgradePointsCalculator
from models import UpgradePurchase, Upgrade


class TestUpgradePointsCalculator(unittest.TestCase):
    def test_calculate_points(self):
        self.assertEqual(
            1,
            UpgradePointsCalculator.calculate_points([]),
        )
        self.assertEqual(
            1.5,
            UpgradePointsCalculator.calculate_points([UpgradePurchase(upgrade=Upgrade(multiplier=1.5))])
        )
        self.assertEqual(
            3.75,
            UpgradePointsCalculator.calculate_points(
                [
                    UpgradePurchase(upgrade=Upgrade(multiplier=1.5)),
                    UpgradePurchase(upgrade=Upgrade(multiplier=2.5)),
                ],
            )
        )
