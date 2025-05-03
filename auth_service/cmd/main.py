import asyncio
from concurrent import futures
import grpc
import psycopg2

from config.config import config
from internal.repository.postgres_repo import PostgresRepo
from internal.repository.redis_repo import RedisRepo
from internal.delivery.grpc.auth_handler import AuthService
from api.auth import auth_pb2_grpc
from utils.db_init import DBInit
from internal.broker.rabbitclient.workers import wrap_consumer
from internal.broker.rabbitclient.workers import check_authorization, give_token


async def main():
    dbname = config.db_name
    user = config.db_user
    password = config.db_password
    host = config.db_host

    # создание бд
    DBInit.create_database_if_not_exists()

    # подключение к бд
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    pg_repo = PostgresRepo(conn)
    pg_repo.init_schema()
    redis_repo = RedisRepo()

    # Здесь крутятся воркеры для приёма сообщений
    await asyncio.gather(
        wrap_consumer(check_authorization, "check_authorization"),
        wrap_consumer(give_token, "give_token"),
    )

    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(pg_repo, redis_repo), server)
    # server.add_insecure_port(f"[::]:{config.grpc_port}")
    # server.start()
    # server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(main())
