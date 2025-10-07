import sys
import requests
import json
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="IQuerio CLI: SQL Optimizer & Vector Playground"
    )
    parser.add_argument(
        "command",
        choices=["optimize", "search", "upload", "nl-query", "register", "login"],
        help="Command to run",
    )
    parser.add_argument(
        "--query", help="SQL query for optimize or NL query for nl-query"
    )
    parser.add_argument("--description", help="Description for search/upload")
    parser.add_argument("--user-id", type=int, help="User ID for upload")
    parser.add_argument("--limit", type=int, default=5, help="Limit for search results")
    parser.add_argument("--username", help="Username for register")
    parser.add_argument("--email", help="Email for register/login")
    parser.add_argument("--password", help="Password for register/login")
    args = parser.parse_args()

    import os
    BASE_URL = os.getenv("IQUERIO_BASE_URL", "http://127.0.0.1:8000")
    headers = {"Content-Type": "application/json"}

    try:
        if args.command == "optimize":
            if not args.query:
                print("Error: --query required for optimize")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/optimize", json={"query": args.query}, headers=headers
            )
        elif args.command == "search":
            if not args.description:
                print("Error: --description required for search")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/search-similar",
                json={"description": args.description, "limit": args.limit},
                headers=headers,
            )
        elif args.command == "upload":
            if not args.user_id or not args.description:
                print("Error: --user-id and --description required for upload")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/upload-embedding",
                json={"user_id": args.user_id, "description": args.description},
                headers=headers,
            )
        elif args.command == "nl-query":
            if not args.query:
                print("Error: --query required for nl-query")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/nl-query", json={"query": args.query}, headers=headers
            )
        elif args.command == "register":
            if not args.username or not args.email or not args.password:
                print(
                    "Error: --username, --email, and --password required for register"
                )
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/register",
                json={
                    "username": args.username,
                    "email": args.email,
                    "password": args.password,
                },
                headers=headers,
            )
        elif args.command == "login":
            if not args.email or not args.password:
                print("Error: --email and --password required for login")
                sys.exit(1)
            response = requests.post(
                f"{BASE_URL}/login",
                json={"email": args.email, "password": args.password},
                headers=headers,
            )
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
