import psycopg2

import asyncpg


from config.config import config


class PostgresRepo:
    def __init__(self, pool):
        self.pool = pool

    async def init_schema(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        print("Таблица users проверена/создана.")

    async def create_user(self, login, password_hash):
        async with self.pool.acquire() as conn:
            try:
                user_id = await conn.fetchval(
                    "INSERT INTO users (login, password_hash) VALUES ($1, $2) RETURNING id",
                    login, password_hash
                )
                return user_id
            except Exception as e:
                raise e

    async def get_user_by_login(self, login):
        async with self.pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    "SELECT id, password_hash FROM users WHERE login = $1", login
                )
                return (row["id"], row["password_hash"]) if row else None
            except Exception as e:
                raise e