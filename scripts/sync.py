import json
import os
import time
from pathlib import Path

import requests
from openai import OpenAI

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRFTOKEN = os.getenv("CSRFTOKEN")
USERNAME = os.getenv("LEETCODE_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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
RATE_LIMIT_DELAY = 1.0

# GitHub Models endpoint (OpenAI-compatible)
GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"
ANALYSIS_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# GitHub Models client
# ---------------------------------------------------------------------------

def get_ai_client() -> OpenAI | None:
    if not GITHUB_TOKEN:
        print("Warning: GITHUB_TOKEN not set — skipping AI analysis")
        return None
    return OpenAI(
        base_url=GITHUB_MODELS_ENDPOINT,
        api_key=GITHUB_TOKEN,
    )


def analyze_solution(client: OpenAI, title: str, difficulty: str, tags: list[str], code: str, language: str) -> dict | None:
    if client is None:
        return None

    prompt = f"""Analyze this LeetCode solution and respond ONLY with a JSON object, no markdown, no explanation outside the JSON.

Problem: {title}
Difficulty: {difficulty}
Tags: {', '.join(tags)}
Language: {language}

Code:
{code}

Respond with exactly this JSON structure:
{{
  "pattern": "primary algorithmic pattern used (e.g. Monotonic Stack, Two Pointers, Binary Search)",
  "timeComplexity": "O(...)",
  "spaceComplexity": "O(...)",
  "explanation": "2-3 sentence explanation of the approach",
  "improvements": "one concrete suggestion to improve the solution, or null if optimal",
  "relatedPatterns": ["pattern1", "pattern2"]
}}"""

    try:
        response = client.chat.completions.create(
            model=ANALYSIS_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a DSA expert. Respond only with valid JSON, no markdown fences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.2,
        )

        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if model adds them anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        return json.loads(raw)

    except Exception as e:
        print(f"  Warning: AI analysis failed: {e}")
        return None


# ---------------------------------------------------------------------------
# GraphQL helpers
# ---------------------------------------------------------------------------

def graphql_request(query: str, variables: dict = None):
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables or {}},
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

    details = data.get("submissionDetails")

    if details is None:
        print(f"Warning: submissionDetails returned null for {submission_id}")
        return None

    return details


def get_problem_tags(title_slug: str) -> list[str]:
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


def save_analysis(problem_dir: Path, analysis: dict):
    with open(problem_dir / "analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)


def load_synced_submissions() -> set:
    if not SYNCED_FILE.exists():
        return set()
    with open(SYNCED_FILE, "r") as f:
        return set(json.load(f))


def save_synced_submissions(submission_ids: set):
    with open(SYNCED_FILE, "w") as f:
        json.dump(sorted(list(submission_ids)), f, indent=2)


def save_recent_submissions(submissions: list):
    RECENT_SUBMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RECENT_SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)


# ---------------------------------------------------------------------------
# Core save logic
# ---------------------------------------------------------------------------

def save_problem(submission_id: str, details: dict, ai_client: OpenAI | None):
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

    # Save timestamped submission file
    with open(submissions_dir / f"{timestamp}.{extension}", "w") as f:
        f.write(details["code"])

    # Always overwrite solution.<ext> with latest
    with open(problem_dir / f"solution.{extension}", "w") as f:
        f.write(details["code"])

    submission_record = {
        "submissionId": submission_id,
        "runtime": details["runtime"],
        "memory": details["memory"],
        "language": lang_name,
        "timestamp": timestamp,
    }

    metadata = load_metadata(problem_dir)
    is_new_problem = not metadata

    if is_new_problem:
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
        existing_ids = {s["submissionId"] for s in metadata.get("submissions", [])}
        if submission_id not in existing_ids:
            metadata["submissions"].append(submission_record)

        if not metadata.get("tags"):
            print(f"  Backfilling tags for {title_slug}...")
            metadata["tags"] = get_problem_tags(title_slug)
            time.sleep(RATE_LIMIT_DELAY)

    save_metadata(problem_dir, metadata)

    # AI analysis — run for new problems or if analysis.json is missing
    analysis_path = problem_dir / "analysis.json"
    if not analysis_path.exists():
        print(f"  Running AI analysis for {title_slug}...")
        analysis = analyze_solution(
            client=ai_client,
            title=question["title"],
            difficulty=question["difficulty"],
            tags=metadata.get("tags", []),
            code=details["code"],
            language=lang_name,
        )
        if analysis:
            save_analysis(problem_dir, analysis)
            print(f"  Pattern: {analysis.get('pattern', 'unknown')}")
        time.sleep(RATE_LIMIT_DELAY)

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

    ai_client = get_ai_client()

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
        if details is None:
            print(f"Skipping submission {submission['title']} due to missing details")
            continue
        save_problem(submission_id, details, ai_client)

        new_synced.add(submission_id)
        save_synced_submissions(new_synced)

        processed_count += 1
        time.sleep(RATE_LIMIT_DELAY)

    print(f"Processed {processed_count} new submissions")


if __name__ == "__main__":
    main()