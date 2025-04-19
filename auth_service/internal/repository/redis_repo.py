import redis

from config.config import config


class RedisRepo:
    def __init__(self, host=config.redis_host, port=config.redis_port):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def set_refresh_token(self, user_id, token, ttl=86400):
        self.client.setex(f"refresh:{user_id}", ttl, token)

    def get_refresh_token(self, user_id):
        return self.client.get(f"refresh:{user_id}")