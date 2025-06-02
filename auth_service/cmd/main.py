import asyncio
from concurrent import futures
#import grpc
#import psycopg2
import concurrent.futures

from config.config import config
# from internal.core.usecase.auth_core import AuthCore
from internal.repository.pg_instances import init_pg_repo, get_pg_repo
from internal.repository.postgres_repo import PostgresRepo
from internal.repository.redis_repo import RedisRepo
#from internal.delivery.grpc.auth_handler import AuthService
#from api.auth import auth_pb2_grpc
from utils.db_init import DBInit
from internal.broker.rabbitclient.workers import wrap_consumer, consume_token_refresh, consume_authorization, check_authorization

import asyncpg

async def main():
    # создание бд
    DBInit.create_database_if_not_exists()

    # await init_pg_repo()
    # redis_repo = RedisRepo()

    pool = await asyncpg.create_pool(
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
        host=config.db_host
    )
    # redis_repo = RedisRepo()
    await init_pg_repo()
    # pg_repo = get_pg_repo()
    pg_repo = PostgresRepo(pool)
    await pg_repo.init_schema()
    #
    #
    #
    # auth_core = AuthCore(pg_repo, redis_repo)



    # CONSUMER_COUNT = 10
    # await asyncio.gather(
    #     # wrap_consumer(auth_core, check_authorization, "check_authorization"),
    #     # wrap_consumer(auth_core, consume_authorization, "authorization"),
    #     # wrap_consumer(consume_token_refresh, "refresh_token")
    # )
    # await asyncio.gather(
    #     *(wrap_consumer(auth_core, check_authorization, f"check_authorization_{i}") for i in range(10)),
    #     *(wrap_consumer(auth_core, consume_authorization, f"authorization_{i}") for i in range(10))
    # )

    await asyncio.gather(
        *(wrap_consumer(pg_repo, check_authorization, f"check_authorization_{i}") for i in range(10)),
        *(wrap_consumer(pg_repo, consume_authorization, f"authorization_{i}") for i in range(10))
    )





if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=64)
    loop.set_default_executor(executor)
    loop.run_until_complete(main())
