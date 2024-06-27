import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
               f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

pool = ConnectionPool(conninfo=DATABASE_URL, open=True)

def get_connection():
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            yield cursor
