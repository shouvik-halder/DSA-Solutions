import json
import os
import time
import uuid
from pathlib import Path

import requests
from openai import OpenAI

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRFTOKEN = os.getenv("CSRFTOKEN")
USERNAME = os.getenv("LEETCODE_USERNAME")
UUUSERID = os.getenv("UUUSERID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GRAPHQL_URL = "https://leetcode.com/graphql/"

LANGUAGE_EXTENSIONS = {
    "Python3": "py", "python3": "py",
    "C++": "cpp", "cpp": "cpp",
    "Java": "java", "java": "java",
    "JavaScript": "js", "javascript": "js",
    "TypeScript": "ts", "typescript": "ts",
    "csharp": "cs", "C#": "cs",
    "golang": "go", "Go": "go",
    "Rust": "rs", "rust": "rs",
    "Ruby": "rb", "ruby": "rb",
    "Swift": "swift", "swift": "swift",
    "Kotlin": "kt", "kotlin": "kt",
}

SYNCED_FILE = Path("synced_submissions.json")
PROBLEMS_DIR = Path("problems")
RATE_LIMIT_DELAY = 2.0
PROGRESS_PAGE_LIMIT = 50

GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"
ANALYSIS_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Headers
# ---------------------------------------------------------------------------

def build_cookie() -> str:
    parts = [
        f"LEETCODE_SESSION={LEETCODE_SESSION}",
        f"csrftoken={CSRFTOKEN}",
    ]
    if UUUSERID:
        parts.append(f"uuuserid={UUUSERID}")
    return "; ".join(parts)


def make_headers(operation_name: str, referer: str) -> dict:
    return {
        "Cookie": build_cookie(),
        "x-csrftoken": CSRFTOKEN,
        "x-operation-name": operation_name,
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": referer,
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0"
        ),
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "random-uuid": str(uuid.uuid4()),
    }


# ---------------------------------------------------------------------------
# GraphQL
# ---------------------------------------------------------------------------

def graphql_request(query: str, variables: dict, operation_name: str, referer: str) -> dict:
    headers = make_headers(operation_name, referer)
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables, "operationName": operation_name},
        headers=headers,
        timeout=30,
    )
    print(f"  [{operation_name}] HTTP {response.status_code}")
    if not response.ok:
        print(f"  Body: {response.text[:400]}")
        response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    return data["data"]


def get_all_solved_problems() -> list[dict]:
    """
    Paginate through userProgressQuestionList and return all AC'd problems.
    Each entry includes: frontendId, title, titleSlug, difficulty, topicTags.
    """
    query = """
    query userProgressQuestionList($filters: UserProgressQuestionListInput) {
      userProgressQuestionList(filters: $filters) {
        totalNum
        questions {
          frontendId
          title
          titleSlug
          difficulty
          lastSubmittedAt
          lastResult
          topicTags {
            name
            slug
          }
        }
      }
    }
    """
    solved = []
    skip = 0

    while True:
        data = graphql_request(
            query,
            {"filters": {"skip": skip, "limit": PROGRESS_PAGE_LIMIT}},
            "userProgressQuestionList",
            referer="https://leetcode.com/progress/",
        )
        result = data.get("userProgressQuestionList", {})
        questions = result.get("questions", [])
        total = result.get("totalNum", 0)

        ac = [q for q in questions if q.get("lastResult") == "AC"]
        solved.extend(ac)
        print(
            f"  Page {skip // PROGRESS_PAGE_LIMIT + 1}: "
            f"{len(questions)} fetched, {len(ac)} AC'd "
            f"(running total: {len(solved)} / {total})"
        )

        skip += PROGRESS_PAGE_LIMIT
        if skip >= total or not questions:
            break
        time.sleep(RATE_LIMIT_DELAY)

    return solved


def get_accepted_submission_ids(title_slug: str) -> list[dict]:
    """
    Return accepted submissions for a problem (newest first, no code).
    Uses questionSubmissionList with status=10 (Accepted).
    """
    query = """
    query submissionList(
      $offset: Int!,
      $limit: Int!,
      $lastKey: String,
      $questionSlug: String!,
      $lang: Int,
      $status: Int
    ) {
      questionSubmissionList(
        offset: $offset
        limit: $limit
        lastKey: $lastKey
        questionSlug: $questionSlug
        lang: $lang
        status: $status
      ) {
        lastKey
        hasNext
        submissions {
          id
          statusDisplay
          lang
          langName
          runtime
          memory
          timestamp
        }
      }
    }
    """
    data = graphql_request(
        query,
        {
            "questionSlug": title_slug,
            "offset": 0,
            "limit": 20,
            "lastKey": None,
            "status": 10,
        },
        "submissionList",
        referer=f"https://leetcode.com/problems/{title_slug}/submissions/",
    )
    result = data.get("questionSubmissionList") or {}
    return result.get("submissions", [])


def get_submission_details(submission_id: str, title_slug: str) -> dict | None:
    """
    Fetch full submission details including code.
    Referer includes the submission ID as LeetCode expects.
    """
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        runtime
        runtimeDisplay
        runtimePercentile
        memory
        memoryDisplay
        memoryPercentile
        code
        timestamp
        statusCode
        lang {
          name
          verboseName
        }
        question {
          questionId
          titleSlug
        }
        topicTags {
          tagId
          slug
          name
        }
        runtimeError
        compileError
      }
    }
    """
    try:
        data = graphql_request(
            query,
            {"submissionId": int(submission_id)},
            "submissionDetails",
            referer=(
                f"https://leetcode.com/problems/{title_slug}"
                f"/submissions/{submission_id}/"
            ),
        )
        return data.get("submissionDetails")
    except Exception as e:
        print(f"  Warning: could not fetch details for submission {submission_id}: {e}")
        return None


# ---------------------------------------------------------------------------
# AI analysis
# ---------------------------------------------------------------------------

def get_ai_client() -> OpenAI | None:
    if not GITHUB_TOKEN:
        print("Warning: GITHUB_TOKEN not set — skipping AI analysis")
        return None
    return OpenAI(base_url=GITHUB_MODELS_ENDPOINT, api_key=GITHUB_TOKEN)


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

    prompt = f"""Analyze this LeetCode solution and respond ONLY with a JSON object.
No markdown fences, no explanation outside the JSON.

Problem: {title}
Difficulty: {difficulty}
Tags: {', '.join(tags)}
Language: {language}

Code:
{code}

Respond with exactly this structure:
{{
  "pattern": "primary algorithmic pattern (e.g. Monotonic Stack, Two Pointers, Binary Search)",
  "timeComplexity": "O(...)",
  "spaceComplexity": "O(...)",
  "explanation": "2-3 sentence explanation of the approach",
  "improvements": "one concrete improvement suggestion, or null if optimal",
  "relatedPatterns": ["pattern1", "pattern2"]
}}"""

    try:
        response = client.chat.completions.create(
            model=ANALYSIS_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a DSA expert. Respond only with valid JSON, no markdown.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if model ignores instructions
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"  Warning: AI analysis failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def load_synced_submissions() -> set:
    if not SYNCED_FILE.exists():
        return set()
    with open(SYNCED_FILE) as f:
        return set(json.load(f))


def save_synced_submissions(ids: set):
    with open(SYNCED_FILE, "w") as f:
        json.dump(sorted(list(ids)), f, indent=2)


def load_metadata(problem_dir: Path) -> dict:
    p = problem_dir / "metadata.json"
    return json.load(open(p)) if p.exists() else {}


def save_metadata(problem_dir: Path, metadata: dict):
    with open(problem_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)


def save_analysis(problem_dir: Path, analysis: dict):
    with open(problem_dir / "analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)


# ---------------------------------------------------------------------------
# Core save logic
# ---------------------------------------------------------------------------

def parse_runtime(raw: str) -> int:
    """Parse '10 ms' -> 10, '< 1 ms' -> 0, etc."""
    try:
        cleaned = raw.replace("< ", "").replace(" ms", "").strip()
        return int(float(cleaned))
    except Exception:
        return 0


def parse_memory(raw: str) -> int:
    """Parse '45.3 MB' -> 45300000 bytes."""
    try:
        mb = float(raw.replace(" MB", "").strip())
        return int(mb * 1_000_000)
    except Exception:
        return 0


def save_problem(problem: dict, submission: dict, details: dict, ai_client: OpenAI | None):
    title_slug = problem["titleSlug"]
    submission_id = submission["id"]
    lang_name = details["lang"]["name"]
    timestamp = int(details["timestamp"])
    code = details.get("code", "")

    runtime = parse_runtime(details.get("runtimeDisplay") or details.get("runtime") or "0 ms")
    memory = parse_memory(details.get("memoryDisplay") or details.get("memory") or "0 MB")
    extension = LANGUAGE_EXTENSIONS.get(lang_name, "txt")

    problem_dir = PROBLEMS_DIR / title_slug
    submissions_dir = problem_dir / "submissions"
    problem_dir.mkdir(parents=True, exist_ok=True)
    submissions_dir.mkdir(parents=True, exist_ok=True)

    # Write code files
    (submissions_dir / f"{timestamp}.{extension}").write_text(code)
    (problem_dir / f"solution.{extension}").write_text(code)

    submission_record = {
        "submissionId": submission_id,
        "runtime": runtime,
        "memory": memory,
        "runtimePercentile": details.get("runtimePercentile"),
        "memoryPercentile": details.get("memoryPercentile"),
        "language": lang_name,
        "timestamp": timestamp,
    }

    # Tags: prefer submissionDetails (authoritative) over progress list
    tags_from_details = [t["name"] for t in (details.get("topicTags") or [])]
    tags_from_progress = [t["name"] for t in (problem.get("topicTags") or [])]
    tags = tags_from_details or tags_from_progress

    metadata = load_metadata(problem_dir)
    if not metadata:
        metadata = {
            "title": problem["title"],
            "titleSlug": title_slug,
            "difficulty": problem.get("difficulty", "Unknown"),
            "tags": tags,
            "submissions": [submission_record],
        }
    else:
        existing_ids = {s["submissionId"] for s in metadata.get("submissions", [])}
        if submission_id not in existing_ids:
            metadata["submissions"].append(submission_record)
        # Backfill tags if missing
        if not metadata.get("tags") and tags:
            metadata["tags"] = tags

    save_metadata(problem_dir, metadata)

    # AI analysis — generated once per problem, never overwritten
    analysis_path = problem_dir / "analysis.json"
    if not analysis_path.exists() and code:
        print(f"  Running AI analysis...")
        analysis = analyze_solution(
            ai_client,
            problem["title"],
            metadata.get("difficulty", "Unknown"),
            metadata.get("tags", []),
            code,
            lang_name,
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
    missing = [
        v for v in ["LEETCODE_SESSION", "CSRFTOKEN", "LEETCODE_USERNAME"]
        if not os.getenv(v)
    ]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
    if not UUUSERID:
        print("Warning: LEETCODE_UUUSERID not set — submissionDetails may fail")


def main():
    validate_environment()

    ai_client = get_ai_client()
    synced_submissions = load_synced_submissions()
    new_synced = set(synced_submissions)
    processed_count = 0

    print("Fetching all solved problems...")
    solved_problems = get_all_solved_problems()
    print(f"\nFound {len(solved_problems)} AC'd problems total\n")

    for problem in solved_problems:
        title_slug = problem["titleSlug"]
        print(f"Processing: {problem['title']}")

        # Step 1: get accepted submission IDs for this problem
        try:
            submissions = get_accepted_submission_ids(title_slug)
            time.sleep(RATE_LIMIT_DELAY)
        except Exception as e:
            print(f"  Error fetching submission list: {e}\n")
            continue

        if not submissions:
            print(f"  No accepted submissions found\n")
            continue

        # Only process the latest accepted submission
        latest = submissions[0]
        submission_id = latest["id"]

        if submission_id in synced_submissions:
            print(f"  Already synced (submission {submission_id})\n")
            continue

        # Step 2: fetch full details including code
        print(f"  Fetching code for submission {submission_id}...")
        details = get_submission_details(submission_id, title_slug)
        time.sleep(RATE_LIMIT_DELAY)

        if not details or not details.get("code"):
            print(f"  No code returned — skipping\n")
            continue

        # Step 3: save everything
        save_problem(problem, latest, details, ai_client)

        new_synced.add(submission_id)
        save_synced_submissions(new_synced)
        processed_count += 1
        print()

    print(f"Done. Processed {processed_count} new submissions.")


if __name__ == "__main__":
    main()
