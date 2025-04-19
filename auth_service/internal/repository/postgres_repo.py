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
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO users (login, password_hash) VALUES (%s, %s) RETURNING id", (login, password_hash))
            self.conn.commit()
            return cur.fetchone()[0]

    def get_user_by_login(self, login):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, password_hash FROM users WHERE login=%s", (login,))
            return cur.fetchone()
