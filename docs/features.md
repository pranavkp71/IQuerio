# IQuerio Features Overview

IQuerio is an AI-powered database assistant that simplifies database tasks for developers, running entirely on your local machine for privacy. It combines traditional SQL with AI-driven semantic search, making it easy to query, optimize, and explore data. Below is a brief overview of its key features.

---

## 1. AI-Powered SQL Optimizer

* **What it does:** Automatically fixes and improves your SQL queries to make them faster and error-free.
* **Why it’s useful:** You don’t need to be an SQL expert. It detects issues (like fetching unnecessary data), suggests fixes (like adding indexes), and provides a better query version.
* **Example:** Paste `SELECT * FROM orders WHERE customer_id = 15`, and it suggests `SELECT id, name FROM orders WHERE customer_id = 15` to avoid fetching extra data.
* **Access:** Use via CLI (`db-toolkit optimize --query "SELECT * FROM orders WHERE customer_id = 15"`) or API (`POST /optimize`).

---

## 2. Hybrid Vector + SQL Search

* **What it does:** Lets you search your database using natural language or meanings, not just exact matches.
* **Why it’s useful:** Finds relevant data even if exact words aren’t in the database (e.g., “Tech enthusiast” matches “AI developer”). Combines with SQL for precise filtering.
* **Example:** Search “People who like AI and startups” to find users with similar interests, like “Machine learning developer,” with similarity scores.
* **Access:** Use via CLI (`db-toolkit search --description "Tech enthusiast into AI" --limit 2`) or API (`POST /search-similar`).

---

## 3. Natural Language Queries

* **What it does:** Turns plain English questions into SQL and vector searches automatically.
* **Why it’s useful:** You don’t need to write SQL. Just ask in normal language, and it fetches the right data, combining filters and AI search if needed.
* **Example:** Ask “Show users over 25 into AI,” and it generates a query combining `age > 25` with a semantic search for “AI” interests.
* **Access:** Use via CLI (`db-toolkit nl-query --query "Show users over 25 into AI"`) or API (`POST /nl-query`).

---

## 4. 100% Local & Privacy-Focused

* **What it does:** Runs everything on your computer, with no cloud or internet required.
* **Why it’s useful:** Keeps your data private and secure, with no risk of leaks or vendor lock-in. Works offline and has no subscription costs.
* **Example:** All queries, AI models, and database operations (using PostgreSQL, pgvector, and FastAPI) stay on your machine.
* **Access:** Set up via Docker Compose or local Python environment (`backend/setup_db.py`).

---

## 5. CLI Tool (db-toolkit)

* **What it does:** A simple command-line interface to access all IQuerio features without writing code or SQL.
* **Why it’s useful:** Makes database tasks fast and beginner-friendly. Supports optimization, searches, embedding uploads, and authentication with easy commands.
* **Example:** Run `db-toolkit search --text "AI developer"` to find similar users or `db-toolkit optimize --query "SELECT * FROM orders"` to improve a query.
* **Access:** Install via `pip install .` and use commands like `db-toolkit optimize`, `search`, `nl-query`, or `auth`.

---

## Additional Features

* **User Authentication:** Optional secure login/registration with hashed passwords and JWT tokens for multi-user setups. Access via CLI (`db-toolkit register --username "suername"`) or API (`POST /register`, `/login`).
* **Local Database Setup:** Automated PostgreSQL + pgvector setup with sample data, ensuring quick and private deployment.

For setup instructions, see the README. Visit the GitHub repo for more details.
