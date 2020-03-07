from datetime import datetime

from application.user.user_password_hasher import UserPasswordHasher
from models import User


class UserFactory:
    @classmethod
    def create(cls, username: str, password: str) -> User:
        return User(
            username=username,
            password=UserPasswordHasher.hash(password),
            created=datetime.now(),
        )
