import redis


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
        self.client.incr()