import asyncpg
from config.config import config
from internal.repository.postgres_repo import PostgresRepo

_pg_repo = None

async def init_pg_repo():
    global pg_repo
    pool = await asyncpg.create_pool(
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
        host=config.db_host
    )
    pg_repo = PostgresRepo(pool)
    await pg_repo.init_schema()

def get_pg_repo() -> PostgresRepo:
    if _pg_repo is None:
        raise RuntimeError("pg_repo is not initialized")
    return _pg_repo