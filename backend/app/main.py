from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .db import get_db

app = FastAPI(title="SmartBase - Phase1 API")

class SQLRequest(BaseModel):
    sql: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": "SmartBase", "phase": "phase-1"}

@app.post("/optimize")
async def optimize_sql(payload: SQLRequest):
    raw_sql = payload.sql.strip()
    if not raw_sql:
        raise HTTPException(status_code=400, detail="Empty SQL provided")

    suggestions = []

    # 1) Detect SELECT *
    if "select *" in raw_sql.lower():
        suggestions.append({
            "issue": "SELECT_STAR",
            "message": "Avoid SELECT * — select only the columns you need.",
            "example": "SELECT id, name, created_at FROM table_name;"
        })

    # 2) Detect simple arithmetic in WHERE like age + 1 > 30
    if "+" in raw_sql and "where" in raw_sql.lower():
        suggestions.append({
            "issue": "FUNCTION_IN_WHERE",
            "message": "Avoid expressions on indexed columns in WHERE (e.g., age + 1 > 30). "
                       "Rewrite to a sargable form to allow index usage.",
            "example": "WHERE age > 29"
        })

    # 3) Placeholder index recommendation 
    if "where" in raw_sql.lower():
        try:
            where_clause = raw_sql.lower().split("where", 1)[1]
            first_token = where_clause.strip().split()[0].strip(",;")

            if first_token.isidentifier():
                suggestions.append({
                    "issue": "MAYBE_ADD_INDEX",
                    "message": f"Consider adding an index on column `{first_token}` if queries filter on it frequently.",
                    "example": f"CREATE INDEX idx_{first_token} ON table_name({first_token});"
                })
        except Exception:
            pass

    response = {
        "original_sql": raw_sql,
        "suggestions": suggestions
    }
    return response

@app.get("/db-test")
async def db_test(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1;"))
    return {"db_connection_test": result.scalar()}
