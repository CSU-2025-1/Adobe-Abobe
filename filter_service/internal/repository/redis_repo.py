import json

import redis.asyncio as redis
from config.config import config


class RedisRepo:
    def __init__(self, redis_url: str = config.redis_url):
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    def _key(self, user_id: str) -> str:
        return f"image:history:{user_id}"

    async def save_filter_history(self, user_id: str, image_url: str, filters: list[dict], timestamp: str):
        entry = {
            "url": image_url,
            "filters": filters,
            "timestamp": timestamp
        }
        await self.client.lpush(self._key(user_id), json.dumps(entry))
        await self.client.ltrim(self._key(user_id), 0, 19)
