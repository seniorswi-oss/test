import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DATABASE_URL = os.getenv("DATABASE_URL")


class PostgresDB:
    def __init__(self, **kwargs):
        self.conn = None
        self.kwargs = kwargs

    def connect(self):
        if self.db_url:
            self.conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        else:
            self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None, fetch=False, many=False):
        if not self.conn:
            self.connect()

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            if many:
                cur.executemany(query, params)
            else:
                cur.execute(query, params)

            if fetch:
                return cur.fetchall()

            self.conn.commit()
            return {"status": "success"}

    def fetch_all(self, query, params=None):
        return self.execute(query, params, fetch=True)

    def fetch_one(self, query, params=None):
        results = self.execute(query, params, fetch=True)
        return results[0] if results else None

    def insert(self, query, params=None):
        return self.execute(query, params)

    def update(self, query, params=None):
        return self.execute(query, params)

    def delete(self, query, params=None):
        return self.execute(query, params)