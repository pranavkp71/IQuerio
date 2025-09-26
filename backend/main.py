from fastapi import FastAPI
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
from .optimizer import optimize_query
from pydantic import BaseModel

class OptimizeRequest(BaseModel):
    query: str

load_dotenv()

app = FastAPI()

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
            database=os.getenv("DB_NAME")
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
        "explain_plan": result["explain_plan"]
    }