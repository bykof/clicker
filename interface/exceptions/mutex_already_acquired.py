from models import User


class MutexAlreadyAcquired(Exception):
    def __init__(self, user: User):
        self.user = user

    def __str__(self):
        return f'The mutex for user ({self.user.username}) was already acquired'
