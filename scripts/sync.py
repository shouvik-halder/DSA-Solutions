import json
import os
from pathlib import Path

import requests

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRFTOKEN = os.getenv("CSRFTOKEN")
USERNAME = os.getenv("LEETCODE_USERNAME")

GRAPHQL_URL = "https://leetcode.com/graphql"

HEADERS = {
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRFTOKEN}",
    "x-csrftoken": CSRFTOKEN,
    "Referer": "https://leetcode.com",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}


def graphql_request(query: str, variables: dict = None):
    response = requests.post(
        GRAPHQL_URL,
        json={
            "query": query,
            "variables": variables or {},
        },
        headers=HEADERS,
    )

    print(f"Status Code: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL Errors: {data['errors']}")

    return data["data"]


def get_recent_submissions():
    query = """
    query recentAcSubmissions($username: String!) {
      recentAcSubmissionList(username: $username) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """

    data = graphql_request(
        query,
        {"username": USERNAME},
    )

    return data["recentAcSubmissionList"]


def save_json(filename: str, data):
    problems_dir = Path("problems")
    problems_dir.mkdir(exist_ok=True)

    filepath = problems_dir / filename

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved: {filepath}")


def validate_environment():
    missing = []

    if not LEETCODE_SESSION:
        missing.append("LEETCODE_SESSION")

    if not CSRFTOKEN:
        missing.append("CSRFTOKEN")

    if not USERNAME:
        missing.append("LEETCODE_USERNAME")

    if missing:
        raise Exception(
            f"Missing environment variables: {', '.join(missing)}"
        )


def main():
    validate_environment()

    submissions = get_recent_submissions()

    print(f"Found {len(submissions)} recent accepted submissions")

    save_json("recent_submissions.json", submissions)

    print(json.dumps(submissions, indent=2))


if __name__ == "__main__":
    main()