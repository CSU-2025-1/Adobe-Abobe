import redis.asyncio as redis
from config.config import config


class RedisRepo:
    def __init__(self, redis_url: str = config.redis_url):
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    async def get_image_url(self, image_id: str) -> str:
        key = f"image:{image_id}"
        value = await self.client.get(key)

        if value is None:
            raise ValueError(f"Image URL not found in Redis for id: {image_id}")

        return value
