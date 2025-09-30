import sys
import requests
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="SmartBase CLI: SQL Optimizer & Vector Playground")
    parser.add_argument("command", choices=["optimize", "search", "upload"], help="Command to run")
    parser.add_argument("--query", help="SQL query for optimize")
    parser.add_argument("--description", help="Description for search/upload")
    parser.add_argument("--user-id", type=int, help="User ID for upload")
    parser.add_argument("--limit", type=int, default=5, help="Limit for search results")
    args = parser.parse_args()

    BASE_URL = "http://127.0.0.1:8000"
    headers = {"Content-Type": "application/json"}

    try:
        if args.command == "optimize":
            if not args.query:
                print("Error: --query required for optimize")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/optimize",
                json={"query": args.query},
                headers=headers
            )
        elif args.command == "search":
            if not args.description:
                print("Error: --description required for search")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/search-similar",
                json={"description": args.description, "limit": args.limit},
                headers=headers
            )
        elif args.command == "upload":
            if not args.user_id or not args.description:
                print("Error: --user-id and --description required for upload")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/upload-embedding",
                json={"user_id": args.user_id, "description": args.description},
                headers=headers
            )
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()