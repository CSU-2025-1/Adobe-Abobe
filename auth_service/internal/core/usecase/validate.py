import jwt
from config.config import config

SECRET = config.jwt_secret


def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = int(payload["user_id"])
        return True, user_id
    except jwt.ExpiredSignatureError:
        return False, -1
    except jwt.InvalidTokenError:
        return False, -2