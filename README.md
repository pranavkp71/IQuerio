# IQuerio

**IQuerio** — Next-Gen Database Assistant (Phase 1 MVP)

This repository contains the Phase 1 skeleton for IQuerio:
- AI-Powered SQL Optimizer (backend skeleton)
- Vector + SQL Hybrid Playground (backlog; backend + pgvector-ready)
- Local dev via Docker Compose (Postgres with pgvector + FastAPI backend)

## Setup
1. Clone repo: `git clone https://github.com/pranavkp71/IQuerio.git`
2. Start Postgres: `docker-compose up -d`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up DB: `python backend/setup_db.py`
5. Run server: `uvicorn backend.main:app --reload`

## Usage
- **SQL Optimizer**:
  - API: `curl -X POST "http://127.0.0.1:8000/optimize" -d '{"query": "SELECT * FROM users WHERE age + 1 > 30"}'`
  - CLI: `python backend/cli.py "SELECT name FROM users WHERE age > 30"`
- **Vector Playground**:
  - Upload: `curl -X POST "http://127.0.0.1:8000/upload-embedding" -d '{"user_id": 1, "description": "AI researcher"}'`
  - Search: `curl -X POST "http://127.0.0.1:8000/search-similar" -d '{"description": "Tech enthusiast into AI", "limit": 2}'`
- Test DB: `curl http://127.0.0.1:8000/db-test`
