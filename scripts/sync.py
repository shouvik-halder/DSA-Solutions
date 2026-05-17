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

LANGUAGE_EXTENSIONS = {
    "Python3": "py",
    "C++": "cpp",
    "Java": "java",
    "JavaScript": "js",
    "TypeScript": "ts",
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


def get_submission_details(submission_id: str):
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        runtime
        memory
        code
        timestamp
        lang {
          name
        }
        question {
          title
          titleSlug
          difficulty
        }
      }
    }
    """

    data = graphql_request(
        query,
        {
            "submissionId": int(submission_id)
        }
    )

    return data["submissionDetails"]


def save_problem(details):
    question = details["question"]

    title_slug = question["titleSlug"]

    lang_name = details["lang"]["name"]

    extension = LANGUAGE_EXTENSIONS.get(lang_name, "txt")

    problem_dir = Path("problems") / title_slug

    problem_dir.mkdir(parents=True, exist_ok=True)

    solution_path = problem_dir / f"solution.{extension}"

    metadata_path = problem_dir / "metadata.json"

    with open(solution_path, "w") as f:
        f.write(details["code"])

    metadata = {
        "title": question["title"],
        "titleSlug": question["titleSlug"],
        "difficulty": question["difficulty"],
        "runtime": details["runtime"],
        "memory": details["memory"],
        "language": lang_name,
        "timestamp": details["timestamp"],
    }

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved: {problem_dir}")


def load_synced_submissions():
    synced_file = Path("synced_submissions.json")

    if not synced_file.exists():
        return set()

    with open(synced_file, "r") as f:
        data = json.load(f)

    return set(data)


def save_synced_submissions(submission_ids):
    with open("synced_submissions.json", "w") as f:
        json.dump(sorted(list(submission_ids)), f, indent=2)


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

    synced_submissions = load_synced_submissions()

    submissions = get_recent_submissions()

    print(f"Found {len(submissions)} recent accepted submissions")

    new_synced = set(synced_submissions)

    processed_count = 0

    for submission in submissions:
        submission_id = submission["id"]

        if submission_id in synced_submissions:
            print(f"Skipping already synced: {submission['title']}")
            continue

        print(f"Processing: {submission['title']}")

        details = get_submission_details(submission_id)

        save_problem(details)

        new_synced.add(submission_id)

        processed_count += 1

    save_synced_submissions(new_synced)

    print(f"Processed {processed_count} new submissions")


if __name__ == "__main__":
    main()