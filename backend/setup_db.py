import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

load_dotenv()

def setup_users_table():
    """Create users table, enable pgvector, and insert sample data with embeddings."""
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

        # Enable pgvector extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # Create users table with embedding column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                description TEXT,
                embedding vector(384)
            );
        """)

        # Load embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Sample data with descriptions
        sample_data = [
            ('Soman', 25, 'Young tech enthusiast who loves AI and startups'),
            ('Babu', 30, 'Experienced software engineer interested in cloud computing'),
            ('Chandran', 35, 'Data scientist passionate about machine learning'),
            ('Dasappan', 28, 'Product manager focused on user experience and design')
        ]

        # Generate embeddings
        descriptions = [row[2] for row in sample_data]
        embeddings = model.encode(descriptions, convert_to_tensor=False).tolist()

        # Insert data with embeddings
        for (name, age, description), embedding in zip(sample_data, embeddings):
            cursor.execute("""
                INSERT INTO users (name, age, description, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (name, age, description, embedding))

        connection.commit()
        print("Users table created, pgvector enabled, and populated with embeddings successfully.")
    except (OperationalError, Exception) as e:
        print(f"Error setting up users table: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    setup_users_table()