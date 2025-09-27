import pytest
from backend.optimizer import optimize_query

def test_invalid_query():
    result = optimize_query("")
    assert result["optimized_query"] == ""
    assert "Invalid SQL query" in result["issues"]

def test_select_star_replacement():
    result = optimize_query("SELECT * FROM users WHERE age + 1 > 30")
    assert result["original_query"] == "SELECT * FROM users WHERE age + 1 > 30"
    assert "SELECT id, name" in result["optimized_query"] 
    assert any("SELECT * fetches unnecessary columns" in issue for issue in result["issues"])

def test_where_expression_optimization():
    result = optimize_query("SELECT name FROM users WHERE age + 1 > 30")
    assert any("Expressions in WHERE" in issue for issue in result["issues"])
    assert "age > 29" in result["optimized_query"]

def test_add_where_suggestion():
    result = optimize_query("SELECT name FROM users")
    assert "Consider adding a WHERE clause" in "\n".join(result["suggestions"])
