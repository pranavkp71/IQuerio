from fastapi import FastAPI
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SmartBase MVP is alive."}

@app.get("/db-test")
def test_db_connection():
    try:
        connection = psycopg2.connect(
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            database = os.getenv("DB_NAME")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        connection.close()
        return {"status": "Connected", "version": db_version[0]}
    except OperationalError as e:
        return {"status": "Failed", "error": str(e)}
