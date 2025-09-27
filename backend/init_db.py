import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
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
