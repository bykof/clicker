from models import User, Upgrade


class UpgradeAlreadyBoughtError(Exception):
    def __init__(self, user: User, upgrade: Upgrade):
        self.user = user
        self.upgrade = upgrade

    def __str__(self):
        return f'The user {self.user.username} has already bought the upgrade {self.upgrade.id}'