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
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://leetcode.com",
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
PENDING_FILE = Path("pending_submissions.json")
RECENT_SUBMISSIONS_FILE = Path("problems/recent_submissions.json")
RATE_LIMIT_DELAY = 1.5

GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"
ANALYSIS_MODEL = "gpt-4o-mini"

# Max pages to fetch via submissionList pagination (20 per page)
MAX_PAGES = 5


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


def analyze_solution(
    client: OpenAI,
    title: str,
    difficulty: str,
    tags: list[str],
    code: str,
    language: str,
) -> dict | None:
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
                    "content": "You are a DSA expert. Respond only with valid JSON, no markdown fences.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.2,
        )

        raw = response.choices[0].message.content.strip()
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

def graphql_request(query: str, variables: dict = None) -> dict:
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables or {}},
        headers=HEADERS,
        timeout=30,
    )
    print(f"  Status: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL Errors: {data['errors']}")
    return data["data"]


def get_all_accepted_submissions() -> list[dict]:
    """
    Fetch accepted submissions using submissionList with pagination.
    Returns submissions with code included — no second API call needed.
    Stops early when all submissions on a page are already synced.
    """
    query = """
    query submissionList($offset: Int!, $limit: Int!, $lastKey: String) {
      submissionList(offset: $offset, limit: $limit, lastKey: $lastKey) {
        lastKey
        hasNext
        submissions {
          id
          title
          titleSlug
          statusDisplay
          runtime
          memory
          timestamp
          lang
          code
        }
      }
    }
    """

    all_accepted = []
    offset = 0
    limit = 20
    last_key = None
    page = 0

    while page < MAX_PAGES:
        print(f"  Fetching page {page + 1} (offset={offset})...")
        try:
            data = graphql_request(query, {
                "offset": offset,
                "limit": limit,
                "lastKey": last_key,
            })
        except Exception as e:
            print(f"  Error fetching submissions page {page + 1}: {e}")
            break

        result = data.get("submissionList")
        if not result:
            print("  submissionList returned null — session may be expired")
            break

        submissions = result.get("submissions", [])
        has_next = result.get("hasNext", False)
        last_key = result.get("lastKey")

        accepted = [s for s in submissions if s.get("statusDisplay") == "Accepted"]
        all_accepted.extend(accepted)

        print(f"  Page {page + 1}: {len(submissions)} total, {len(accepted)} accepted")

        if not has_next:
            break

        offset += limit
        page += 1
        time.sleep(RATE_LIMIT_DELAY)

    return all_accepted


def get_problem_metadata(title_slug: str) -> dict:
    """Fetch difficulty and topic tags for a problem."""
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty
        topicTags {
          name
          slug
        }
      }
    }
    """
    try:
        data = graphql_request(query, {"titleSlug": title_slug})
        q = data.get("question", {})
        return {
            "difficulty": q.get("difficulty", "Unknown"),
            "tags": [tag["name"] for tag in q.get("topicTags", [])],
        }
    except Exception as e:
        print(f"  Warning: could not fetch metadata for {title_slug}: {e}")
        return {"difficulty": "Unknown", "tags": []}


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


def load_pending() -> dict:
    if not PENDING_FILE.exists():
        return {}
    with open(PENDING_FILE, "r") as f:
        return json.load(f)


def save_pending(pending: dict):
    with open(PENDING_FILE, "w") as f:
        json.dump(pending, f, indent=2)


def save_recent_submissions(submissions: list):
    RECENT_SUBMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Save a simplified version for reference (no code to keep file small)
    simplified = [
        {
            "id": s["id"],
            "title": s["title"],
            "titleSlug": s["titleSlug"],
            "timestamp": s["timestamp"],
            "lang": s["lang"],
        }
        for s in submissions
    ]
    with open(RECENT_SUBMISSIONS_FILE, "w") as f:
        json.dump(simplified, f, indent=2)


# ---------------------------------------------------------------------------
# Core save logic
# ---------------------------------------------------------------------------

def save_problem(submission: dict, ai_client: OpenAI | None):
    """
    Save a submission. submission dict comes directly from submissionList
    so it already contains code, runtime, memory, lang, timestamp.
    """
    submission_id = submission["id"]
    title_slug = submission["titleSlug"]
    lang_name = submission["lang"]
    timestamp = int(submission["timestamp"])
    code = submission.get("code", "")
    runtime_str = submission.get("runtime", "0 ms")
    memory_str = submission.get("memory", "0 MB")

    # Parse runtime (e.g. "10 ms" -> 10)
    try:
        runtime = int(runtime_str.replace(" ms", "").strip())
    except Exception:
        runtime = 0

    # Parse memory (e.g. "45.3 MB" -> 45300000 bytes)
    try:
        memory_mb = float(memory_str.replace(" MB", "").strip())
        memory = int(memory_mb * 1_000_000)
    except Exception:
        memory = 0

    extension = LANGUAGE_EXTENSIONS.get(lang_name)
    if extension is None:
        print(f"  Warning: unknown language '{lang_name}' — saving as .txt")
        extension = "txt"

    problem_dir = Path("problems") / title_slug
    submissions_dir = problem_dir / "submissions"
    problem_dir.mkdir(parents=True, exist_ok=True)
    submissions_dir.mkdir(parents=True, exist_ok=True)

    # Save timestamped submission
    with open(submissions_dir / f"{timestamp}.{extension}", "w") as f:
        f.write(code)

    # Always overwrite solution.<ext> with latest
    with open(problem_dir / f"solution.{extension}", "w") as f:
        f.write(code)

    submission_record = {
        "submissionId": submission_id,
        "runtime": runtime,
        "memory": memory,
        "language": lang_name,
        "timestamp": timestamp,
    }

    metadata = load_metadata(problem_dir)
    is_new_problem = not metadata

    if is_new_problem:
        print(f"  Fetching metadata for {title_slug}...")
        problem_meta = get_problem_metadata(title_slug)
        time.sleep(RATE_LIMIT_DELAY)

        metadata = {
            "title": submission["title"],
            "titleSlug": title_slug,
            "difficulty": problem_meta["difficulty"],
            "tags": problem_meta["tags"],
            "submissions": [submission_record],
        }
    else:
        existing_ids = {s["submissionId"] for s in metadata.get("submissions", [])}
        if submission_id not in existing_ids:
            metadata["submissions"].append(submission_record)

        # Backfill tags if missing
        if not metadata.get("tags"):
            print(f"  Backfilling tags for {title_slug}...")
            problem_meta = get_problem_metadata(title_slug)
            metadata["tags"] = problem_meta["tags"]
            if not metadata.get("difficulty") or metadata["difficulty"] == "Unknown":
                metadata["difficulty"] = problem_meta["difficulty"]
            time.sleep(RATE_LIMIT_DELAY)

    save_metadata(problem_dir, metadata)

    # AI analysis — only if missing
    analysis_path = problem_dir / "analysis.json"
    if not analysis_path.exists() and code:
        print(f"  Running AI analysis for {title_slug}...")
        analysis = analyze_solution(
            client=ai_client,
            title=submission["title"],
            difficulty=metadata.get("difficulty", "Unknown"),
            tags=metadata.get("tags", []),
            code=code,
            language=lang_name,
        )
        if analysis:
            save_analysis(problem_dir, analysis)
            print(f"  Pattern: {analysis.get('pattern', 'unknown')}")
        time.sleep(RATE_LIMIT_DELAY)

    print(f"  Saved: {problem_dir} ({len(metadata['submissions'])} submission(s))")


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
    pending = load_pending()

    print("Fetching accepted submissions from LeetCode...")
    submissions = get_all_accepted_submissions()
    print(f"Found {len(submissions)} accepted submissions total")

    # Save reference file (without code)
    save_recent_submissions(submissions)

    # Clear pending queue — submissionList includes code directly,
    # so the null-details problem no longer applies
    if pending:
        print(f"Clearing {len(pending)} stale pending entries (no longer needed)")
        save_pending({})

    new_synced = set(synced_submissions)
    processed_count = 0

    for submission in submissions:
        submission_id = submission["id"]

        if submission_id in synced_submissions:
            print(f"Skipping already synced: {submission['title']}")
            continue

        # Skip non-accepted (shouldn't happen since we filter above, but be safe)
        if submission.get("statusDisplay") != "Accepted":
            continue

        # Skip if no code returned
        if not submission.get("code"):
            print(f"  Warning: no code for {submission['title']} ({submission_id}) — skipping")
            continue

        print(f"Processing: {submission['title']}")
        save_problem(submission, ai_client)

        new_synced.add(submission_id)
        save_synced_submissions(new_synced)
        processed_count += 1
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\nProcessed {processed_count} new submissions")


if __name__ == "__main__":
    main()