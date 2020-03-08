import redis

from interface.abstracts.balance_client import BalanceClient
from models import User


class RedisBalanceClient(BalanceClient):
    def __init__(self, user: User):
        super().__init__(user)
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def add_points(self, points):
        self.client.incrby(self.user.id, points)
