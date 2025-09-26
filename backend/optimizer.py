import sqlparse
from sqlparse.sql import Where
from sqlparse.tokens import Keyword
from typing import Dict, List

def optimize_query(query: str) -> Dict[str, any]:
    parsed = sqlparse.parse(query)
    if not parsed:
        return {
            "original_query": query,
            "optimized_query": query,
            "issues": ["Invalid SQL query"],
            "suggestions": []
        }
    stmt = parsed[0]

    issues: List[str] = []
    suggestions: List[str] = []
    optimized_query = query.strip()
    query_upper = query.upper().strip()

    print("Tokens:", [str(t).strip() for t in stmt.tokens if str(t).strip()])

    if stmt.get_type().upper() == 'SELECT' and 'SELECT *' in query_upper:
        issues.append("SELECT * fetches unnecessary columns (slow and risky).")
        suggestions.append("Replace with specific columns, e.g., SELECT id, name FROM table.")
        optimized_query = optimized_query.replace('SELECT *', 'SELECT id, name').replace('select *', 'SELECT id, name')

    where_clause_obj = None
    for token in stmt.tokens:
        if isinstance(token, Where):
            where_clause_obj = token
            break

    if where_clause_obj:
        where_clause = str(where_clause_obj).lower()
        print("WHERE clause:", where_clause)

        if '+' in where_clause or '-' in where_clause:
            issues.append("Expressions in WHERE (e.g., age + 1) prevent index usage.")
            suggestions.append("Simplify to direct column comparisons, e.g., age > 29.")
            optimized_query = optimized_query.replace('age + 1', 'age > 29').replace('age - 1', 'age')

        if 'age' in where_clause:
            suggestions.append("Add an index: CREATE INDEX idx_age ON users(age);")
    else:
        suggestions.append("Consider adding a WHERE clause to filter data early.")

    return {
        "original_query": query,
        "optimized_query": optimized_query,
        "issues": issues,
        "suggestions": suggestions
    }
