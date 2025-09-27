from fastapi import FastAPI
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
from .optimizer import optimize_query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

load_dotenv()

app = FastAPI()


class OptimizeRequest(BaseModel):
    query: str


class UploadEmbeddingRequest(BaseModel):
    user_id: int
    description: str


class SearchSimilarRequest(BaseModel):
    description: str
    limit: int = 3


@app.get("/")
def read_root():
    return {"message": "SmartBase MVP is alive."}


@app.get("/db-test")
def test_db_connection():
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        connection.close()
        return {"status": "Connected", "version": db_version[0]}
    except OperationalError as e:
        return {"status": "Failed", "error": str(e)}


@app.post("/optimize")
def optimize_endpoint(request: OptimizeRequest):
    result = optimize_query(request.query)
    return {
        "query": request.query,
        "optimized_query": result["optimized_query"],
        "issues": result["issues"],
        "suggestions": result["suggestions"],
        "explain_plan": result["explain_plan"],
    }


@app.post("/upload-embedding")
def upload_embedding(request: UploadEmbeddingRequest):
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode([request.description], convert_to_tensor=False)[
            0
        ].tolist()

        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET description = %s, embedding = %s WHERE id = %s;",
            (request.description, embedding, request.user_id),
        )
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "Embedding uploaded successfully", "user_id": request.user_id}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}


@app.post("/search-similar")
def search_similar(request: SearchSimilarRequest):
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode([request.description], convert_to_tensor=False)[
            0
        ].tolist()

        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, name, description, embedding <-> %s::vector AS distance
            FROM users
            ORDER BY distance
            LIMIT %s;
        """,
            (embedding, request.limit),
        )
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        return {
            "results": [
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "distance": row[3],
                }
                for row in results
            ]
        }
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
