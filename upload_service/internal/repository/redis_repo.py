import aioredis
from config.config import REDIS_HOST, REDIS_PORT, REDIS_DB

r = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")


async def save_image_mapping(user_id: str, image_id: str, image_url: str):
    await r.set(f"image:{user_id}:{image_id}", image_url)

    list_key = f"image_versions:{image_id}"
    index_key = f"image_current:{image_id}"
    await r.rpush(list_key, image_url)
    await r.set(index_key, 0)
