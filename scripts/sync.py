import json
import os
import time
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
    # C# — LeetCode returns "csharp" for lang.name
    "csharp": "cs",
    "C#": "cs",
    "golang": "go",
    "Go": "go",
    "Rust": "rs",
    "Ruby": "rb",
    "Swift": "swift",
    "Kotlin": "kt",
    "Scala": "scala",
}

SYNCED_FILE = Path("synced_submissions.json")
RECENT_SUBMISSIONS_FILE = Path("problems/recent_submissions.json")

# Seconds to wait between API calls to avoid rate limiting
RATE_LIMIT_DELAY = 1.0


# ---------------------------------------------------------------------------
# GraphQL helpers
# ---------------------------------------------------------------------------

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
    data = graphql_request(query, {"username": USERNAME})
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
    data = graphql_request(query, {"submissionId": int(submission_id)})
    return data["submissionDetails"]


def get_problem_tags(title_slug: str) -> list[str]:
    """Fetch topic tags for a problem by its titleSlug."""
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        topicTags {
          name
          slug
        }
      }
    }
    """
    try:
        data = graphql_request(query, {"titleSlug": title_slug})
        return [tag["name"] for tag in data["question"]["topicTags"]]
    except Exception as e:
        print(f"Warning: could not fetch tags for {title_slug}: {e}")
        return []


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def load_metadata(problem_dir: Path) -> dict:
    metadata_path = problem_dir / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path, "r") as f:
            return json.load(f)
    return {}


def save_metadata(problem_dir: Path, metadata: dict):
    with open(problem_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)


def load_synced_submissions() -> set:
    if not SYNCED_FILE.exists():
        return set()
    with open(SYNCED_FILE, "r") as f:
        return set(json.load(f))


def save_synced_submissions(submission_ids: set):
    with open(SYNCED_FILE, "w") as f:
        json.dump(sorted(list(submission_ids)), f, indent=2)


def save_recent_submissions(submissions: list):
    """Keep problems/recent_submissions.json in sync with the latest fetch."""
    RECENT_SUBMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RECENT_SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)


# ---------------------------------------------------------------------------
# Core save logic
# ---------------------------------------------------------------------------

def save_problem(submission_id: str, details: dict):
    question = details["question"]
    title_slug = question["titleSlug"]
    lang_name = details["lang"]["name"]
    timestamp = details["timestamp"]

    extension = LANGUAGE_EXTENSIONS.get(lang_name)
    if extension is None:
        print(f"Warning: unknown language '{lang_name}' for {title_slug} — saving as .txt")
        extension = "txt"

    problem_dir = Path("problems") / title_slug
    submissions_dir = problem_dir / "submissions"
    problem_dir.mkdir(parents=True, exist_ok=True)
    submissions_dir.mkdir(parents=True, exist_ok=True)

    # --- Save timestamped submission file ---
    timestamped_path = submissions_dir / f"{timestamp}.{extension}"
    with open(timestamped_path, "w") as f:
        f.write(details["code"])

    # --- Always overwrite solution.<ext> with the latest code ---
    latest_path = problem_dir / f"solution.{extension}"
    with open(latest_path, "w") as f:
        f.write(details["code"])

    # --- Build the submission record ---
    submission_record = {
        "submissionId": submission_id,
        "runtime": details["runtime"],
        "memory": details["memory"],
        "language": lang_name,
        "timestamp": timestamp,
    }

    # --- Load existing metadata and merge ---
    metadata = load_metadata(problem_dir)
    is_new_problem = not metadata

    if is_new_problem:
        # First time seeing this problem — fetch tags
        print(f"  Fetching tags for {title_slug}...")
        tags = get_problem_tags(title_slug)
        time.sleep(RATE_LIMIT_DELAY)

        metadata = {
            "title": question["title"],
            "titleSlug": title_slug,
            "difficulty": question["difficulty"],
            "tags": tags,
            "submissions": [submission_record],
        }
    else:
        # Problem already exists — append submission if not already present
        existing_ids = {s["submissionId"] for s in metadata.get("submissions", [])}
        if submission_id not in existing_ids:
            metadata["submissions"].append(submission_record)

        # Backfill tags if they were missing from an older sync
        if not metadata.get("tags"):
            print(f"  Backfilling tags for {title_slug}...")
            metadata["tags"] = get_problem_tags(title_slug)
            time.sleep(RATE_LIMIT_DELAY)

    save_metadata(problem_dir, metadata)
    print(f"Saved: {problem_dir} ({len(metadata['submissions'])} submission(s))")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate_environment():
    missing = []
    if not LEETCODE_SESSION:
        missing.append("LEETCODE_SESSION")
    if not CSRFTOKEN:
        missing.append("CSRFTOKEN")
    if not USERNAME:
        missing.append("LEETCODE_USERNAME")
    if missing:
        raise Exception(f"Missing environment variables: {', '.join(missing)}")


def main():
    validate_environment()

    synced_submissions = load_synced_submissions()

    submissions = get_recent_submissions()
    print(f"Found {len(submissions)} recent accepted submissions")

    save_recent_submissions(submissions)

    new_synced = set(synced_submissions)
    processed_count = 0

    for submission in submissions:
        submission_id = submission["id"]

        if submission_id in synced_submissions:
            print(f"Skipping already synced: {submission['title']}")
            continue

        print(f"Processing: {submission['title']}")

        details = get_submission_details(submission_id)
        save_problem(submission_id, details)

        # Flush after each save so a mid-run crash doesn't re-fetch
        new_synced.add(submission_id)
        save_synced_submissions(new_synced)

        processed_count += 1
        time.sleep(RATE_LIMIT_DELAY)

    print(f"Processed {processed_count} new submissions")


if __name__ == "__main__":
    main()