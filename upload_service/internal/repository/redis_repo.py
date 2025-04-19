import redis
from config.config import REDIS_HOST, REDIS_PORT, REDIS_DB

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def save_image_mapping(user_id: str, image_id: str, image_url: str):
    key = f"image:{user_id}:{image_id}"
    r.set(key, image_url)
