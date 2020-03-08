import os

MULTIPLIER = 1.07
SECRET_KEY = os.environ.get('SECRET_KEY', '123')
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_HOURS = 24
REDIS_URL = os.environ.get('REDIS_URL', 'localhost')