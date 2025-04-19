import redis

class RedisRepo:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def set_refresh_token(self, user_id, token, ttl=86400):
        self.client.setex(f"refresh:{user_id}", ttl, token)

    def get_refresh_token(self, user_id):
        return self.client.get(f"refresh:{user_id}")