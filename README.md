# DSA Solutions

[![Sync LeetCode](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/sync-leetcode.yml/badge.svg)](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/sync-leetcode.yml) [![Deploy Pages](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/shouvik-halder/DSA-Solutions/actions/workflows/deploy-pages.yml)

A self-updating repository that automatically syncs my LeetCode accepted submissions, enriches them with topic tags and AI-powered pattern analysis, and publishes a live dashboard to GitHub Pages.

**[View Dashboard →](https://shouvik-halder.github.io/DSA-Solutions/)**

---

## How it works

A GitHub Actions workflow runs every 30 minutes. If there are new accepted submissions on LeetCode, it:

1. Fetches submission details and topic tags via LeetCode's GraphQL API
2. Saves the solution code and builds a submission history over time
3. Calls GitHub Models (GPT-4o-mini) to analyse the algorithmic pattern, complexity, and potential improvements
4. Regenerates the dashboard and deploys it to GitHub Pages

If there are no new submissions, the workflow exits cleanly with no commits.

---

## Repository structure

```
problems/
  <problem-slug>/
    solution.cs          # latest accepted solution
    metadata.json        # difficulty, tags, full submission history
    analysis.json        # AI-generated pattern analysis
    submissions/
      <timestamp>.cs     # every accepted submission, timestamped

scripts/
  sync.py                # fetches from LeetCode + GitHub Models, saves problems
  generate_dashboard.py  # reads metadata and builds docs/index.html

docs/
  index.html             # generated dashboard (served via GitHub Pages)

.github/workflows/
  sync-leetcode.yml      # scheduled workflow
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

- Total solved with Easy / Medium / Hard breakdown
- Topic tag frequency
- 26-week submission calendar
- Filterable and searchable problems table with runtime, solve date, and attempt count

---

## Setup (for your own fork)

### 1. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | How to get it |
|--------|--------------|
| `LEETCODE_SESSION` | Browser DevTools → Application → Cookies → `LEETCODE_SESSION` on leetcode.com |
| `LEETCODE_CSRF_TOKEN` | Same cookies panel → `csrftoken` |
| `LEETCODE_USERNAME` | Your LeetCode username |

`GITHUB_TOKEN` is provided automatically by GitHub Actions — no setup needed.

### 2. Enable GitHub Pages

Go to **Settings → Pages → Source** → Deploy from a branch → `main` → `/docs`.

### 3. Trigger the first run

Go to **Actions → Sync LeetCode → Run workflow**.

The workflow will sync your last 20 accepted submissions, fetch tags, run AI analysis on each, generate the dashboard, and push everything in one commit.

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

- LeetCode's `recentAcSubmissionList` API returns a maximum of 20 submissions. History beyond the 20 most recent accepted submissions is not recoverable via the API.
- The workflow runs every 30 minutes, so there may be up to a 30-minute delay before a new submission appears in the dashboard.
- AI analysis is generated once per problem and not re-generated on subsequent submissions of the same problem.
