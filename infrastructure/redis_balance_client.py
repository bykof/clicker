import redis

from constants import REDIS_URL
from interface.abstracts.balance_client import BalanceClient
from interface.exceptions.mutex_already_acquired import MutexAlreadyAcquired
from models import User


class RedisBalanceClient(BalanceClient):
    def __init__(self, user: User):
        super().__init__(user)
        self.client = redis.Redis(host=REDIS_URL, port=6379, db=0)

    @property
    def lock_id(self):
        return f'{self.user.username}_lock'

    @property
    def points_id(self):
        return f'{self.user.username}_points'

    def add_points(self, points):
        self.client.incrby(self.points_id, points)

    def get_points(self):
        return int(self.client.get(self.points_id))

    def acquire_mutex(self):
        lock_value = self.client.get(self.lock_id)
        if lock_value and lock_value.decode('utf-8', 'replace') == self.user.username:
            raise MutexAlreadyAcquired(self.user)

        self.client.set(self.lock_id, self.user.username, nx=True)

    def release_mutex(self):
        self.client.delete(self.lock_id)
