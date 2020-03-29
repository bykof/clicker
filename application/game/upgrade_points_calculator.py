import math
from typing import List

from models import UpgradePurchase


class UpgradePointsCalculator:
    @staticmethod
    def calculate_points(upgrade_purchases: List[UpgradePurchase]) -> float:
        return float(
            math.prod([
                upgrade_purchase.upgrade.multiplier
                for upgrade_purchase in upgrade_purchases
            ])
        )
