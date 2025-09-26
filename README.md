# SmartBase

**SmartBase** — Next-Gen Database Assistant (Phase 1 MVP)

This repository contains the Phase 1 skeleton for SmartBase:
- AI-Powered SQL Optimizer (backend skeleton)
- Vector + SQL Hybrid Playground (backlog; backend + pgvector-ready)
- Local dev via Docker Compose (Postgres with pgvector + FastAPI backend)

## Setup
- Clone repo: `git clone https://github.com/pranavkp71/Smart-Base.git`
- Create virtual env: `python -m venv venv`
- Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
- Install dependencies: `pip install -r requirements.txt`
- Start Postgres: `docker-compose up -d`
- Setup users table: `python backend/setup_db.py`

## Run
- Start API: `uvicorn backend.main:app --reload`
- Test DB: `http://127.0.0.1:8000/db-test`
- Optimize query (CLI): `python backend/cli.py "SELECT * FROM users"`
- Optimize query (API): `curl -X POST "http://127.0.0.1:8000/optimize" -H "Content-Type: application/json" -d '{"query": "SELECT * FROM users"}'`

## Features
- **SQL Optimizer**: Detects issues (SELECT *, arithmetic in WHERE, sequential scans) and suggests fixes with EXPLAIN-based performance analysis.
