from abc import ABCMeta, abstractmethod

from models import User


class BalanceClient(metaclass=ABCMeta):
    def __init__(self, user: User):
        self.user = user

    @abstractmethod
    def add_points(self, points):
        pass

    @abstractmethod
    def get_points(self):
        pass

    @abstractmethod
    def acquire_mutex(self):
        pass

    @abstractmethod
    def release_mutex(self):
        pass
