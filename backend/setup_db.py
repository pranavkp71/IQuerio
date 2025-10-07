import psycopg2
from psycopg2 import Error as PsycopgError
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

load_dotenv()


def setup_database():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()

        # Create auth_users table for login/registration
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS auth_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
        """
        )

        # Creating users table for vector playgroung
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                description TEXT,
                embedding vector(384)
            );
        """
        )

        # Insert sample daa with embeddings
        model = SentenceTransformer("all-MiniLM-L6-v2")

        sample_data = [
            ("Soman", 25, "Young tech enthusiast who loves AI and startups"),
            ("Babu", 30, "Experienced software engineer interested in cloud computing"),
            ("Chandran", 35, "Data scientist passionate about machine learning"),
            ("Dasappan", 28, "Product manager focused on user experience and design"),
        ]

        descriptions = [row[2] for row in sample_data]
        embeddings = model.encode(descriptions, convert_to_tensor=False).tolist()

        inserted = 0

        for (name, age, description), embedding in zip(sample_data, embeddings):
            cursor.execute(
                """
                INSERT INTO users (name, age, description, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                RETURNING id;
            """,
                (name, age, description, embedding),
            )
            if cursor.fetchone():
                inserted += 1

        connection.commit()
        print(
            f"Databse setup complete: auth users and users tables created, pgvector enabled, {inserted}/{len(sample_data)} sample users inserted."
        )
    except PsycopgError as e:
        print(f"Database error during setup: {e}")
    except Exception as e:
        print(f"Unexpected error during setup: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    setup_database()
