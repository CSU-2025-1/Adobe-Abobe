import aioredis
from config.config import REDIS_HOST, REDIS_PORT, REDIS_DB

r = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

async def save_image_mapping(user_id: str, image_id: str, image_url: str):
    key = f"image:{user_id}:{image_id}"
    await r.set(key, image_url)
