from fastapi import FastAPI
from pydantic import BaseModel
from .optimizer import optimize_query
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
import re
from sentence_transformers import SentenceTransformer

load_dotenv()
app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")


class OptimizeRequest(BaseModel):
    query: str


class UploadEmbeddingRequest(BaseModel):
    user_id: int
    description: str


class SearchSimilarRequest(BaseModel):
    description: str
    limit: int = 3


class NLQueryRequest(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"message": "IQuerio MVP is alive."}


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


@app.post("/nl-query")
def nl_query(request: NLQueryRequest):
    try:
        query = request.query.lower()
        age_match = re.search(r"users (?:over|older than) (\d+)", query)
        desc_match = re.search(r'similar to ["\']?([^"\']+)["\']?', query)
        sql = "SELECT id, name, description, embedding <-> %s::vector AS distance FROM users"
        params = []
        conditions = []
        if desc_match:
            desc = desc_match.group(1)
            embedding = model.encode([desc], convert_to_tensor=False)[0].tolist()
            params.append(embedding)
        else:
            return {
                "status": "Failed",
                "error": "No 'similar to' clause found in query",
            }
        if age_match:
            age = int(age_match.group(1))
            conditions.append(f"age > {age}")
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY distance LIMIT 3"
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()
        cursor.execute(sql, params)
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
            ],
            "sql": sql,
            "params": params,
        }
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
