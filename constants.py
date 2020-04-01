import os

GENERATOR_MULTIPLIER = float(os.environ.get('GENERATOR_MULTIPLIER', 1.15))
SECRET_KEY = os.environ.get('SECRET_KEY', '123')
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_HOURS = int(os.environ.get('ACCESS_TOKEN_EXPIRE_HOURS', 24))
REDIS_URL = os.environ.get('REDIS_URL', 'localhost')
POSTGRES_URL = os.environ.get('POSTGRES_URL', 'postgres://localhost/clicker')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
SENTRY_URL = os.environ.get('SENTRY_URL')
