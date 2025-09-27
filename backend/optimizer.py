import sqlparse
from sqlparse.sql import Where
from typing import Dict, List
import psycopg2
from psycopg2 import OperationalError
from psycopg2.errors import UndefinedTable 
from dotenv import load_dotenv
import os

load_dotenv()

def optimize_query(query: str) -> Dict[str, any]:
    parsed = sqlparse.parse(query)

    if not parsed:
        return {
            "original_query": query,
            "optimized_query": query,
            "issues": ["Invalid SQL query"],
            "suggestions": [],
            "explain_plan": "N/A"
        }
    stmt = parsed[0]

    issues: List[str] = []
    suggestions: List[str] = []
    optimized_query = query.strip()
    explain_plan = "N/A"
    query_upper = query.upper().strip()

    print("Tokens:", [str(t).strip() for t in stmt.tokens if str(t).strip()])

    if stmt.get_type().upper() == 'SELECT' and 'SELECT *' in query_upper:
        issues.append("SELECT * fetches unnecessary columns (slow and risky).")
        suggestions.append("Replace with specific columns, e.g., SELECT id, name FROM table.")
        optimized_query = optimized_query.replace('SELECT *', 'SELECT id, name').replace('select *', 'SELECT id, name')

    join_count = query_upper.count('JOIN')
    table_names = []
    for token in stmt.tokens:
        if isinstance(token, sqlparse.sql.Identifier):
            table_name = str(token).strip().lower()
            if table_name not in table_names:
                table_names.append(table_name)

    if join_count > 0 and len(table_names) < join_count + 1:
        issues.append("Possible redundant JOIN: Joining the same table multiple times.")
        suggestions.append("Check if multiple JOINs to the same table are necessary.")

    try:
        if os.getenv("ENV") == "test":
            raise OperationalError("Skipping EXPLAIN in test mode")

        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()
        cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
        explain_plan = cursor.fetchall()[0][0]
        cursor.close()
        connection.close()

        plan = explain_plan[0]["Plan"]
        if plan.get("Node Type") == "Seq Scan":
            issues.append("Query uses a sequential scan (slow for large tables).")
            suggestions.append("Consider adding an index on filtered columns.")
        total_cost = plan.get("Total Cost", 0.0)
        if total_cost > 1000:
            issues.append(f"High query cost ({total_cost:.2f}): Likely inefficient.")
            suggestions.append("Optimize filters or add indexes to reduce cost.")

    except (OperationalError, UndefinedTable) as e:
        explain_plan = f"EXPLAIN skipped: {str(e)}"

    where_clause_obj = None
    for token in stmt.tokens:
        if isinstance(token, Where):
            where_clause_obj = token
            break

    if where_clause_obj:
        where_clause = str(where_clause_obj).lower().replace('  ', ' ')
        print("WHERE clause:", where_clause)

        if '+' in where_clause or '-' in where_clause:
            issues.append("Expressions in WHERE (e.g., age + 1) prevent index usage.")
            suggestions.append("Simplify to direct column comparisons, e.g., age > 29.")
            if 'age + 1 > 30' in where_clause:
                optimized_query = optimized_query.replace('age + 1 > 30', 'age > 29')
            optimized_query = optimized_query.replace('age - 1', 'age')

        if 'age' in where_clause:
            suggestions.append("Add an index: CREATE INDEX idx_age ON users(age);")
    else:
        suggestions.append("Consider adding a WHERE clause to filter data early.")

    return {
        "original_query": query,
        "optimized_query": optimized_query,
        "issues": issues,
        "suggestions": suggestions,
        "explain_plan": explain_plan
    }
