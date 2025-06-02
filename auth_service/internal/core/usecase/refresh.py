import jwt
from config.config import config
from internal.repository.redis_repo import redis_repo
from utils.generate_token import generate_tokens

SECRET = config.jwt_secret

def refresh_tokens(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError()

        user_id = payload["user_id"]
        stored_token = redis_repo.get_refresh_token(user_id)
        if stored_token != refresh_token:
            raise jwt.InvalidTokenError()

        return generate_tokens(user_id)
    except Exception:
        raise ValueError("Invalid refresh token")