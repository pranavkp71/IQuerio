import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

def setup_users_table():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER
            );
        """)

        cursor.execute("""
            INSERT INTO users (name, age) VALUES
            ('Alice', 25),
            ('Bob', 30),
            ('Charlie', 35),
            ('Diana', 28)
            ON CONFLICT DO NOTHING;
        """)

        connection.commit()
        print("Users table created and populated successfully.")
    except OperationalError as e:
        print(f"Error setting up users table: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    setup_users_table()