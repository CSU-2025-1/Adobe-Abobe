from concurrent import futures
import grpc
import psycopg2
from auth_service.internal.repository.postgres_repo import PostgresRepo
from auth_service.internal.repository.redis_repo import RedisRepo
from auth_service.internal.delivery.grpc.auth_handler import AuthService
from auth_service.api.auth import auth_pb2_grpc
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_if_not_exists():
    dbname = "authservicedb"
    user = "postgres"
    password = "123"
    host = "localhost"

    # подключение к постгре
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {dbname}")
        print(f"✅ База {dbname} создана.")
    else:
        print(f"📦 База {dbname} уже существует.")
    cursor.close()
    conn.close()


#создание бд
create_database_if_not_exists()


# подключение к бд
conn = psycopg2.connect(dbname="authservicedb", user="postgres", password="123", host="localhost")
pg_repo = PostgresRepo(conn)
pg_repo.init_schema()
redis_repo = RedisRepo()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(pg_repo, redis_repo), server)
server.add_insecure_port("[::]:50001")
server.start()
server.wait_for_termination()