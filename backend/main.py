from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .optimizer import optimize_query
import psycopg2
from psycopg2 import Error as PsycopgError
from dotenv import load_dotenv
import os
import re
from sentence_transformers import SentenceTransformer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", "your-secret-key"
)  # Replace with secure key in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db_connection():
    return psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT creation
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/register")
def register_user(request: RegisterRequest):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        password_hash = hash_password(request.password)
        cursor.execute(
            """
            INSERT INTO auth_users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, username, email
            """,
            (request.username, request.email, password_hash),
        )
        user = cursor.fetchone()
        connection.commit()
        return {
            "status": "User registered successfully",
            "user_id": user[0],
            "username": user[1],
            "email": user[2],
        }
    except PsycopgError as e:
        if "unique_violation" in str(e):
            raise HTTPException(
                status_code=400, detail="Username or email already exists"
            )
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.post("/login", response_model=Token)
def login_user(request: LoginRequest):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash FROM auth_users WHERE email = %s",
            (request.email,),
        )
        user = cursor.fetchone()
        if not user or not verify_password(request.password, user[3]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        access_token = create_access_token(data={"sub": user[2], "user_id": user[0]})
        return {"access_token": access_token, "token_type": "bearer"}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()


@app.get("/")
def read_root():
    return {"message": "IQuerio MVP is alive."}


@app.get("/db-test")
def test_db_connection():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        return {"status": "Connected", "version": version}
    except PsycopgError as e:
        return {"status": "Failed", "error": str(e)}
    finally:
        cursor.close()
        connection.close()


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
        connection = get_db_connection()
        cursor = connection.cursor()
        embedding = model.encode([request.description], convert_to_tensor=False)[
            0
        ].tolist()
        cursor.execute(
            "UPDATE users SET description = %s, embedding = %s WHERE id = %s;",
            (request.description, embedding, request.user_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"User ID {request.user_id} not found"
            )
        connection.commit()
        return {"status": "Embedding uploaded successfully", "user_id": request.user_id}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()


@app.post("/search-similar")
def search_similar(request: SearchSimilarRequest):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        embedding = model.encode([request.description], convert_to_tensor=False)[
            0
        ].tolist()
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
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()


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
            raise HTTPException(
                status_code=400, detail="No 'similar to' clause found in query"
            )
        if age_match:
            age = int(age_match.group(1))
            conditions.append(f"age > {age}")
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY distance LIMIT 3"
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchall()
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
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()
