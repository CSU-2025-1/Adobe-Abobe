from config.config import config
import jwt
from internal.repository.redis_repo import redis_repo

SECRET = config.jwt_secret


def generate_tokens(user_id):
    access_token = jwt.encode({"user_id": user_id}, SECRET, algorithm="HS256")
    refresh_token = jwt.encode({"user_id": user_id, "type": "refresh"}, SECRET, algorithm="HS256")
    redis_repo.set_refresh_token(user_id, refresh_token)
    return access_token, refresh_token
