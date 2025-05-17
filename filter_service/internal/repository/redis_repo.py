import redis.asyncio as redis
from config.config import config


class RedisRepo:
    def __init__(self, redis_url: str = config.redis_url):
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    async def get_current_version_url(self, image_id: str) -> str:
        index_key = f"image_current:{image_id}"
        list_key = f"image_versions:{image_id}"

        index = await self.client.get(index_key)
        if index is None:
            index = 0
        index = int(index)

        url = await self.client.lindex(list_key, index)
        if url is None:
            raise ValueError(f"Version not found for image {image_id} at index {index}")
        return url

    async def push_new_version(self, image_id: str, version_url: str):
        list_key = f"image_versions:{image_id}"
        index_key = f"image_current:{image_id}"

        await self.client.rpush(list_key, version_url)
        length = await self.client.llen(list_key)
        await self.client.set(index_key, length - 1)  # обновляем current индекс

