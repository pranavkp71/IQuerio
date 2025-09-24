from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="SmartBase - Phase1 API")

class SQLRequest(BaseModel):
    sql: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": "SmartBase", "Phase": "Phase-1"}

@app.post("/optimize")
async def optimize(payload: SQLRequest):
    raw_sql = payload.sql.strip()
    if not raw_sql:
        raise HTTPException(status_code=400, detail="Empty SQL provided")
    
    suggestion = []

    # Dectect SELECT *
    if "select *" in raw_sql.lower():
        suggestion.append({
            "issue": "SELECT_STAR",
            "message": "Avoid SELECT * - select only the columns you need.",
            "example": "SELECT id, name, created_at FROM table_name;"
        })

    # Dectect simple arithmatic in WHERE like age + 1 > 30
    if "+" in raw_sql and "where" in raw_sql.lower():
        suggestion.append({
            "issue": "FUNCTION_IN_WHERE",
            "message": "Avoid expressions on indexed columns in WHERE (eg. age + 1 > 30)."
            "Rewrite to a sargable form to allow index usage.",
            "example": "WHERE age > 29"
        })

    # Placeholder index recommendations
    if "where" in raw_sql.lower():
        try:
            where_clause = raw_sql.lower().split("where", 1)[i]
            first_token = where_clause.strip().split()[0].strip(",;")

            if first_token.isidentifier():
                suggestion.append({
                    "issue": "MAYBE_ADD_INDEX",
                    "message": f"Consider adding an index on column `{first_token}` if queries filter on it frequently.",
                    "example": f"CREATED INDEX idx_{first_token} ON table_name({first_token});"
                })
        except Exception:
            pass

    response = {
        "original_sql": raw_sql,
        "suggestions": suggestion
    }

    return response
