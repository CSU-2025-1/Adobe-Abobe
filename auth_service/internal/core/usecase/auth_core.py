import bcrypt
import jwt
from config.config import config

SECRET = config.jwt_secret


class AuthCore:
    def __init__(self, pg_repo, redis_repo):
        self.pg = pg_repo
        self.redis = redis_repo

    def register_user(self, login: str, password: str):
        if self.pg.get_user_by_login(login):
            raise ValueError("User already exists")

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_id = self.pg.create_user(login, hashed)
        return self._generate_tokens(user_id)

    def login(self, login: str, password: str):
        user = self.pg.get_user_by_login(login)
        if not user or not bcrypt.checkpw(password.encode(), user[1].encode()):
            raise ValueError("Invalid credentials")
        return self._generate_tokens(user[0])

    def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_id = int(payload["user_id"])
            return True, user_id
        except jwt.ExpiredSignatureError:
            return False, -1
        except jwt.InvalidTokenError:
            return False, -2

    def _generate_tokens(self, user_id):
        access_token = jwt.encode({"user_id": user_id}, SECRET, algorithm="HS256")
        refresh_token = jwt.encode({"user_id": user_id, "type": "refresh"}, SECRET, algorithm="HS256")
        self.redis.set_refresh_token(user_id, refresh_token)
        return access_token, refresh_token

    def refresh_tokens(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, SECRET, algorithms=["HS256"])
            if payload.get("type") != "refresh":
                raise jwt.InvalidTokenError()

            user_id = payload["user_id"]
            stored_token = self.redis.get_refresh_token(user_id)
            if stored_token != refresh_token:
                raise jwt.InvalidTokenError()

            return self._generate_tokens(user_id)
        except Exception:
            raise ValueError("Invalid refresh token")