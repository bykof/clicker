from typing import Any

import redis

from constants import REDIS_URL, REDIS_PASSWORD
from infrastructure.abstracts import BalanceClient
from interface.exceptions.mutex_already_acquired import MutexAlreadyAcquired
from models import User


class RedisBalanceClient(BalanceClient):
    def __init__(self, user: User):
        super().__init__(user)
        self.client = redis.Redis(host=REDIS_URL, port=6379, db=0, password=REDIS_PASSWORD)

    @property
    def click_lock_id(self):
        return f'{self.user.username}_click_lock'

    @property
    def generators_lock_id(self):
        return f'{self.user.username}_generators_lock'

    @property
    def points_id(self):
        return f'{self.user.username}_points'

    def add_points(self, points):
        self.client.incrby(self.points_id, points)

    def subtract_points(self, points):
        self.client.decrby(self.points_id, points)

    def get_points(self):
        return int(self.client.get(self.points_id))

    def acquire_mutex(self, name: str, value: Any):
        lock_value = self.client.get(name)
        if lock_value and lock_value.decode('utf-8', 'replace') == value:
            raise MutexAlreadyAcquired(self.user)

        self.client.set(name, value, nx=True)

    def release_mutex(self, name):
        self.client.delete(name)

    def acquire_click_mutex(self):
        self.acquire_mutex(self.click_lock_id, self.user.username)

    def release_click_mutex(self):
        self.release_mutex(self.click_lock_id)

    def acquire_generators_mutex(self):
        self.acquire_mutex(self.generators_lock_id, self.user.username)

    def release_generators_mutex(self):
        self.release_mutex(self.generators_lock_id)
