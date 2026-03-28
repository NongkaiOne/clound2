import psycopg2
import os

def get_connection():
    try:
        conn = psycopg2.connect(
            os.environ.get('DATABASE_URL'),
            sslmode='require'
        )
        return conn
    except Exception as err:
        raise RuntimeError(f"Could not connect to database: {err}") from err