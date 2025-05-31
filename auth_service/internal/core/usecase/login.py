import asyncio

from internal.repository.postgres_repo import PostgresRepo
from utils.generate_token import generate_tokens
from utils.hash_function import check_password


async def login_user(pg_repo: PostgresRepo, login: str, password: str):
        user = await pg_repo.get_user_by_login(login)
        if not user:
            raise ValueError("Invalid credentials")
        valid = await asyncio.to_thread(check_password, password, user[1])
        if not valid:
            raise ValueError("Invalid credentials")
        return generate_tokens(user[0])