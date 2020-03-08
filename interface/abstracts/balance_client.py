from abc import ABCMeta, abstractmethod

from models import User


class BalanceClient(metaclass=ABCMeta):
    def __init__(self, user: User):
        self.user = user

    @abstractmethod
    def add_points(self, points):
        pass

    @abstractmethod
    def subtract_points(self, points):
        pass

    @abstractmethod
    def get_points(self):
        pass

    @abstractmethod
    def acquire_click_mutex(self):
        pass

    @abstractmethod
    def release_click_mutex(self):
        pass

    @abstractmethod
    def acquire_generators_mutex(self):
        pass

    @abstractmethod
    def release_generators_mutex(self):
        pass
