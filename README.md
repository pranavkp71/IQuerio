# IQuerio: AI-Powered SQL Optimizer & Vector Playground

**IQuerio** is a next-gen database assistant (Phase 1 MVP) for devs and AI builders. It optimizes SQL queries, performs vector-based similarity searches, and supports natural language queries using Postgres with `pgvector` and a FastAPI backend.

## Features
Discover IQuerio’s AI-powered tools in the [Features Overview](./docs/features.md).

## Setup
1. Clone repo: `git clone https://github.com/pranavkp71/IQuerio`
2. Install PostgreSQL dev libraries: `sudo apt install libpq-dev python3-dev`
3. Create a virtual env: `python3 -m venv .venv` and activate it using `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start Postgres with pgvector: `docker-compose up -d`
6. Set up DB: `python backend/setup_db.py`
7. Install CLI: `pip install .`
8. Run server: `uvicorn backend.main:app --reload`

## Usage
- **SQL Optimizer**:
  - CLI: `db-toolkit optimize --query "SELECT * FROM users WHERE age + 1 > 30"`
  - API: `curl -X POST "http://127.0.0.1:8000/optimize" -H "Content-Type: application/json" -d '{"query": "SELECT * FROM users WHERE age + 1 > 30"}'`
  - Output: `{"query": "...", "optimized_query": "SELECT id, name FROM users WHERE age > 29", "issues": [...], "suggestions": [...], "explain_plan": [...]}`

- **Vector Playground**:
  - Upload: `db-toolkit upload --user-id 1 --description "AI researcher"`
  - API: `curl -X POST "http://127.0.0.1:8000/upload-embedding" -H "Content-Type: application/json" -d '{"user_id": 1, "description": "AI researcher"}'`
  - Output: `{"status": "Embedding uploaded successfully", "user_id": 1}`
  
  - Search: `db-toolkit search --description "Tech enthusiast into AI" --limit 2`
  - API: `curl -X POST "http://127.0.0.1:8000/search-similar" -H "Content-Type: application/json" -d '{"description": "Tech enthusiast into AI", "limit": 2}'`
  - Output: `{"results": [{"id": 1, "name": "Soman", "description": "...", "distance": 0.66}, ...]}`

  - NL Query: `db-toolkit nl-query --query "Show users over 30 similar to Tech enthusiast into AI"`
  - API: `curl -X POST "http://127.0.0.1:8000/nl-query" -H "Content-Type: application/json" -d '{"query": "Show users over 30 similar to Tech enthusiast into AI"}'`
  - Output: `{"results": [{"id": 3, "name": "Chandran", "description": "...", "distance": 0.98}, ...], "sql": "...", "params": [...]}`

- **Test DB**: `curl http://127.0.0.1:8000/db-test`
  - Output: `{"status": "Connected", "version": "..."}` or `{"status": "Failed", "error": "..."}`

## Testing
- Run tests: `pytest backend/`
- CI/CD: GitHub Actions runs tests and linting on push/PR.

## API Specs for Frontend
- **GET `/`**: Returns `{"message": "IQuerio MVP is alive."}`
- **GET `/db-test`**: Returns `{"status": "Connected", "version": "..."}` or `{"status": "Failed", "error": "..."}`
- **POST `/optimize`**:
  - Input: `{"query": "<SQL>"}`
  - Output: `{"query": "...", "optimized_query": "...", "issues": [...], "suggestions": [...], "explain_plan": [...]}`
- **POST `/upload-embedding`**:
  - Input: `{"user_id": int, "description": string}`
  - Output: `{"status": "...", "user_id": int}`
- **POST `/search-similar`**:
  - Input: `{"description": string, "limit": int}`
  - Output: `{"results": [{"id": int, "name": string, "description": string, "distance": float}, ...]}`
- **POST `/nl-query`**:
  - Input: `{"query": string}`
  - Output: `{"results": [{"id": int, "name": string, "description": string, "distance": float}, ...], "sql": string, "params": [...]}`

## Development
- Backend: FastAPI, `psycopg2`, `sentence-transformers`
- Database: Postgres with `pgvector`
- CLI: `db-toolkit` (installed via `pip install .`)
- Testing: `pytest` with GitHub Actions CI