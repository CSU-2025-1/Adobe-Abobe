import psycopg2

class PostgresRepo:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def init_schema(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()
        print("Таблица users проверена/создана.")

    def create_user(self, login, password_hash):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (login, password_hash) VALUES (%s, %s) RETURNING id",
                (login, password_hash)
            )
            user_id = cursor.fetchone()[0]
            self.conn.commit()
            return user_id
        except Exception as e:
            self.conn.rollback()
            raise e


    def get_user_by_login(self, login):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, password_hash FROM users WHERE login=%s", (login,))
            return cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            raise e