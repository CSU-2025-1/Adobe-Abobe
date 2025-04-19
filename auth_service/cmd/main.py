from concurrent import futures
import grpc
import psycopg2

from config.config import config
from internal.repository.postgres_repo import PostgresRepo
from internal.repository.redis_repo import RedisRepo
from internal.delivery.grpc.auth_handler import AuthService
from api.auth import auth_pb2_grpc
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dbname = config.db_name
user = config.db_user
password = config.db_password
host = config.db_host

#временно внутри сервиса инициализации потом проcто в докере отделельно
def create_database_if_not_exists():
    # подключение к постгре
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {dbname}")
        print(f"База {dbname} создана.")
    else:
        print(f"База {dbname} уже существует.")
    cursor.close()
    conn.close()


#создание бд
create_database_if_not_exists()


# подключение к бд
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
pg_repo = PostgresRepo(conn)
pg_repo.init_schema()
redis_repo = RedisRepo()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(pg_repo, redis_repo), server)
server.add_insecure_port(f"[::]:{config.grpc_port}")
server.start()
server.wait_for_termination()