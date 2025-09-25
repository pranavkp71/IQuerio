import psycopg2
from psycopg2 import OperationalError

try:
    connection = psycopg2.connect(
            user = "smartbase_user",
            password = "smartbase_pass",
            host = "localhost",
            port = "5432",
            database = "smartbase_db"
        )
    cursor = connection.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
    version = cursor.fetchone()
    print(f"pgvector enabled, version: {version[0]}")
    cursor.close()
    connection.close()
except OperationalError as e:
    print(f"Error: {e}")

