# DSA Solutions

[![Sync LeetCode](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/sync-leetcode.yml/badge.svg)](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/sync-leetcode.yml) [![Deploy Pages](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/deploy-pages.yml)

A self-updating repository that syncs my accepted LeetCode solutions, enriches them with topic tags and AI-powered pattern analysis, and publishes a live dashboard to GitHub Pages.

**[View Dashboard →](https://shouvik-halder.github.io/DSA-Solutions/)**

---

## How It Works

A GitHub Actions workflow runs once a day at **02:30 UTC** and can also be started manually. On each run it:

1. Authenticates against LeetCode with browser cookie secrets.
2. Paginates through `userProgressQuestionList` to find every solved problem on the account.
3. For each solved problem, requests accepted submissions with `questionSubmissionList`.
4. Checks only the latest accepted submission for that problem against `synced_submissions.json`.
5. Fetches full code, runtime, memory, percentiles, language, and tags through `submissionDetails` when the latest submission is new.
6. Saves the latest solution at the problem root and a timestamped copy under `submissions/`.
7. Runs GitHub Models (`gpt-4o-mini`) once per problem to generate pattern, complexity, hints, and improvement notes.
8. Regenerates `docs/index.html` and deploys the dashboard after a successful sync.

If there are no new latest accepted submissions, the workflow exits cleanly without committing changes.

---

## Repository structure

```
synced_submissions.json  # submission IDs already processed by the sync script

problems/
  <problem-slug>/
    solution.cs          # latest accepted solution
    metadata.json        # difficulty, tags, submission records, performance data
    analysis.json        # AI-generated pattern analysis
    submissions/
      <timestamp>.cs     # synced accepted submissions, timestamped

scripts/
  sync.py                # fetches LeetCode data, saves code, runs AI analysis
  generate_dashboard.py  # reads metadata and builds docs/index.html

docs/
  index.html             # generated dashboard (served via GitHub Pages)

.github/workflows/
  sync-leetcode.yml      # scheduled workflow
  deploy-pages.yml       # deploys docs/ to GitHub Pages after sync
```

### `metadata.json` format

```json
{
  "title": "Trapping Rain Water",
  "titleSlug": "trapping-rain-water",
  "difficulty": "Hard",
  "tags": ["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
  "submissions": [
    {
      "submissionId": "1970177491",
      "runtime": 0,
      "memory": 46856000,
      "runtimePercentile": 100.0,
      "memoryPercentile": 47.56,
      "language": "csharp",
      "timestamp": 1775448892
    }
  ]
}
```

### `analysis.json` format

```json
{
  "pattern": "Two Pointers",
  "timeComplexity": "O(n)",
  "spaceComplexity": "O(1)",
  "explanation": "Uses two pointers converging from both ends, tracking left and right max heights to calculate trapped water at each position without extra space.",
  "improvements": null,
  "relatedPatterns": ["Monotonic Stack", "Dynamic Programming"]
}
```

---

## Dashboard

The live dashboard at **[shouvik-halder.github.io/DSA-Solutions](https://shouvik-halder.github.io/DSA-Solutions/)** shows:

- Total solved count, total synced submissions, and Easy / Medium / Hard breakdown
- Topic tag frequency with clickable tag filters
- Algorithmic pattern frequency with clickable pattern filters
- 52-week submission activity calendar
- Searchable problem list filtered by title, tag, pattern, or difficulty
- Expandable problem cards with hidden hints, complexity notes, improvement suggestions, tags, and the saved solution code
- Direct links back to each LeetCode problem

---

## Setup (for your own fork)

### 1. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | How to get it |
|--------|--------------|
| `LEETCODE_SESSION` | Browser DevTools → Application → Cookies → `LEETCODE_SESSION` on leetcode.com |
| `LEETCODE_CSRF_TOKEN` | Same cookies panel → `csrftoken` |
| `UUUSERID` | Same cookies panel → `uuuserid` |
| `LEETCODE_USERNAME` | Your LeetCode username |

`GITHUB_TOKEN` is provided automatically by GitHub Actions — no setup needed.

### 2. Enable GitHub Pages

Go to **Settings → Pages → Source** and choose **GitHub Actions**. The `Deploy Pages` workflow uploads the generated `docs/` folder after each successful sync.

### 3. Trigger the first run

Go to **Actions → Sync LeetCode → Run workflow**.

The workflow will scan all solved problems, sync any latest accepted submissions that are not already recorded, fetch tags and performance data, run AI analysis for newly discovered problems, generate the dashboard, and push everything in one commit.

---

## Tech stack

| Component | Technology |
|-----------|-----------|
| Sync script | Python 3.13 |
| LeetCode data | GraphQL API |
| AI analysis | GitHub Models — GPT-4o-mini |
| Dashboard | Static HTML/JS, no framework |
| Hosting | GitHub Pages |
| Automation | GitHub Actions |

---

## Limitations

- The sync checks the latest accepted submission for each solved problem. Older accepted attempts are preserved if they were synced earlier, but the script does not backfill every historical accepted attempt for a problem.
- The workflow runs once per day, so there may be up to a day of delay before a new submission appears in the dashboard unless the workflow is triggered manually.
- AI analysis is generated once per problem and is not overwritten on later submissions of the same problem.
- The sync depends on LeetCode's private GraphQL responses and browser cookie authentication, so cookie expiry or API changes can require updating secrets or script logic.
