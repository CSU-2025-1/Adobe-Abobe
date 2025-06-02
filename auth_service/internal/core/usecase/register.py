import asyncio
from internal.repository.postgres_repo import PostgresRepo
from utils.generate_token import generate_tokens
from utils.hash_function import hash_sync


async def register_user(pg_repo: PostgresRepo, login: str, password: str):
        if await pg_repo.get_user_by_login(login):
            raise ValueError("User already exists")
        hashed = await asyncio.to_thread(hash_sync, password)
        user_id = await pg_repo.create_user(login, hashed)
        return generate_tokens(user_id)