import aioredis
import json
from config.config import REDIS_URL



class RedisRepo:
    def __init__(self):
        self.client = aioredis.from_url(REDIS_URL, decode_responses=True)

    def _key(self, user_id: str) -> str:
        return f"image:history:{user_id}"

    async def get_filter_history(self, user_id: str) -> list[dict]:
        entries = await self.client.lrange(self._key(user_id), 0, -1)
        parsed = [json.loads(entry) for entry in entries]

        return [
            {
                "url": item.get("url"),
                "filters": item.get("filters"),
                "timestamp": item.get("timestamp")
            } for item in parsed
        ]

    async def close(self):
        await self.client.close()
