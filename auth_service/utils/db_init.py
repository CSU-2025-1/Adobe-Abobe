import psycopg2

from config.config import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dbname = config.db_name
user = config.db_user
password = config.db_password
host = config.db_host

class DBInit:

    def create_database_if_not_exists():
        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
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
