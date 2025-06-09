import json

import redis.asyncio as redis
from config.config import config


class RedisRepo:
    def __init__(self, redis_url: str = config.redis_url):
        self.pool = redis.ConnectionPool.from_url(redis_url, max_connections=100)
        self.client = redis.Redis(connection_pool=self.pool)

    def _key(self, user_id: str) -> str:
        return f"image:history:{user_id}"

    async def save_filter_history(self, user_id: str, image_url: str, filters: list[dict], timestamp: str):
        entry = {
            "url": image_url,
            "filters": filters,
            "timestamp": timestamp
        }
        key = self._key(user_id)
        async with self.client.pipeline() as pipe:
            await pipe.lpush(key, json.dumps(entry))
            await pipe.ltrim(key, 0, 19)
            await pipe.execute()

    async def save_filter_result(self, task_id: str, image_url: str, timestamp: str):
        key = f"image:result:{task_id}"
        entry = {
            "status": "done",
            "filtered_url": image_url,
            "timestamp": timestamp
        }
        await self.client.set(key, json.dumps(entry), ex=60 * 60)

    async def get_filter_result(self, task_id: str):
        key = f"image:result:{task_id}"
        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None


redis_repo = RedisRepo()
