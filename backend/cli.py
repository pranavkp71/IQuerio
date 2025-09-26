from optimizer import optimize_query
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli.py 'YOUR SQL QUERY'")
        sys.exit(1)
    query = sys.argv[1]
    result = optimize_query(query)
    print("Original:", result["original_query"])
    print("Optimized:", result["optimized_query"])
    print("Issues:", result["issues"])
    print("Suggestions:", result["suggestions"])