"""
generate_dashboard.py — builds docs/index.html from problems/ metadata

Reads every problems/<slug>/metadata.json and generates a static
self-contained dashboard deployed via GitHub Pages.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

PROBLEMS_DIR = Path("problems")
OUTPUT_DIR = Path("docs")
OUTPUT_FILE = OUTPUT_DIR / "index.html"


def load_all_problems() -> list[dict]:
    problems = []
    for metadata_path in sorted(PROBLEMS_DIR.glob("*/metadata.json")):
        with open(metadata_path, "r") as f:
            data = json.load(f)
        if "submissions" in data:
            problems.append(data)
    return problems


def build_stats(problems: list[dict]) -> dict:
    difficulty_count = {"Easy": 0, "Medium": 0, "Hard": 0}
    tag_count = {}
    calendar = {}  # date string -> count
    total_submissions = 0

    for p in problems:
        diff = p.get("difficulty", "Unknown")
        if diff in difficulty_count:
            difficulty_count[diff] += 1

        for tag in p.get("tags", []):
            tag_count[tag] = tag_count.get(tag, 0) + 1

        for s in p.get("submissions", []):
            total_submissions += 1
            ts = s.get("timestamp")
            if ts:
                date_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
                calendar[date_str] = calendar.get(date_str, 0) + 1

    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "total": len(problems),
        "total_submissions": total_submissions,
        "difficulty": difficulty_count,
        "tags": sorted_tags,
        "calendar": calendar,
    }


def build_problem_rows(problems: list[dict]) -> list[dict]:
    rows = []
    for p in problems:
        latest = max(p["submissions"], key=lambda s: s["timestamp"])
        rows.append({
            "title": p["title"],
            "titleSlug": p["titleSlug"],
            "difficulty": p.get("difficulty", ""),
            "tags": p.get("tags", []),
            "runtime": latest["runtime"],
            "memory": round(latest["memory"] / 1_000_000, 1),
            "timestamp": latest["timestamp"],
            "submissionCount": len(p["submissions"]),
        })
    rows.sort(key=lambda r: r["timestamp"], reverse=True)
    return rows


def generate_html(stats: dict, rows: list[dict]) -> str:
    data_json = json.dumps({"stats": stats, "problems": rows})

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>DSA Solutions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #7c6af7;
    --accent2: #f97316;
    --easy: #22c55e;
    --medium: #f59e0b;
    --hard: #ef4444;
    --text: #e2e8f0;
    --muted: #4a4a6a;
    --card: #13131f;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* Background grid */
  body::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.4;
    pointer-events: none;
    z-index: 0;
  }}

  .container {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px;
    position: relative;
    z-index: 1;
  }}

  /* Header */
  header {{
    padding: 56px 0 40px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 48px;
  }}

  .header-inner {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 24px;
    flex-wrap: wrap;
  }}

  .logo {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.03em;
    line-height: 1;
  }}

  .logo span {{
    color: var(--accent);
  }}

  .updated {{
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.05em;
  }}

  /* Stats row */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 48px;
  }}

  .stat-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
  }}

  .stat-card:hover {{ border-color: var(--accent); }}

  .stat-card::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
    opacity: 0;
    transition: opacity 0.2s;
  }}

  .stat-card:hover::after {{ opacity: 1; }}

  .stat-label {{
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
  }}

  .stat-value {{
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    color: var(--text);
  }}

  .stat-value.easy {{ color: var(--easy); }}
  .stat-value.medium {{ color: var(--medium); }}
  .stat-value.hard {{ color: var(--hard); }}

  /* Section */
  .section {{
    margin-bottom: 48px;
  }}

  .section-title {{
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }}

  /* Calendar */
  .calendar-wrap {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    overflow-x: auto;
  }}

  #calendar-svg {{
    display: block;
    min-width: 680px;
  }}

  /* Tags */
  .tags-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }}

  .tag-pill {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: border-color 0.15s, background 0.15s;
    cursor: default;
  }}

  .tag-pill:hover {{
    border-color: var(--accent);
    background: rgba(124,106,247,0.08);
  }}

  .tag-count {{
    color: var(--accent);
    font-weight: 500;
  }}

  /* Table */
  .table-wrap {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
  }}

  .table-controls {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
  }}

  .search-input {{
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    padding: 8px 14px;
    border-radius: 6px;
    outline: none;
    width: 220px;
    transition: border-color 0.2s;
  }}

  .search-input:focus {{ border-color: var(--accent); }}
  .search-input::placeholder {{ color: var(--muted); }}

  .filter-btn {{
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s;
    letter-spacing: 0.05em;
  }}

  .filter-btn:hover, .filter-btn.active {{
    border-color: var(--accent);
    color: var(--text);
    background: rgba(124,106,247,0.1);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
  }}

  th {{
    text-align: left;
    padding: 12px 20px;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
  }}

  th:hover {{ color: var(--text); }}

  td {{
    padding: 14px 20px;
    border-bottom: 1px solid rgba(30,30,46,0.6);
    vertical-align: middle;
  }}

  tr:last-child td {{ border-bottom: none; }}

  tr:hover td {{ background: rgba(124,106,247,0.04); }}

  .problem-link {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.15s;
  }}

  .problem-link:hover {{ color: var(--accent); }}

  .badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.05em;
  }}

  .badge-Easy {{ background: rgba(34,197,94,0.12); color: var(--easy); }}
  .badge-Medium {{ background: rgba(245,158,11,0.12); color: var(--medium); }}
  .badge-Hard {{ background: rgba(239,68,68,0.12); color: var(--hard); }}

  .tag-inline {{
    display: inline-block;
    background: rgba(124,106,247,0.1);
    color: var(--accent);
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 0.65rem;
    margin: 2px 2px 2px 0;
  }}

  .submissions-count {{
    color: var(--muted);
    font-size: 0.72rem;
  }}

  .submissions-count.multi {{ color: var(--accent2); }}

  .no-results {{
    text-align: center;
    padding: 48px;
    color: var(--muted);
    font-size: 0.85rem;
  }}

  /* Difficulty bar */
  .diff-bars {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}

  .diff-row {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .diff-label {{
    width: 60px;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
  }}

  .diff-label.Easy {{ color: var(--easy); }}
  .diff-label.Medium {{ color: var(--medium); }}
  .diff-label.Hard {{ color: var(--hard); }}

  .diff-bar-track {{
    flex: 1;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
  }}

  .diff-bar-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s cubic-bezier(0.16,1,0.3,1);
  }}

  .diff-bar-fill.Easy {{ background: var(--easy); }}
  .diff-bar-fill.Medium {{ background: var(--medium); }}
  .diff-bar-fill.Hard {{ background: var(--hard); }}

  .diff-num {{
    width: 28px;
    text-align: right;
    font-size: 0.8rem;
    color: var(--muted);
  }}

  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}

  @media (max-width: 640px) {{
    .two-col {{ grid-template-columns: 1fr; }}
    .logo {{ font-size: 1.8rem; }}
    .stat-value {{ font-size: 1.8rem; }}
  }}
</style>
</head>
<body>
<div class="container">

  <header>
    <div class="header-inner">
      <div>
        <div class="logo">dsa<span>.</span>solutions</div>
      </div>
      <div class="updated" id="updated-label"></div>
    </div>
  </header>

  <div class="stats-grid" id="stats-grid"></div>

  <div class="two-col section">
    <div>
      <div class="section-title">Difficulty Breakdown</div>
      <div class="diff-bars" id="diff-bars"></div>
    </div>
    <div>
      <div class="section-title">Topics</div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;">
        <div class="tags-grid" id="tags-grid"></div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Submission Calendar</div>
    <div class="calendar-wrap">
      <svg id="calendar-svg"></svg>
    </div>
  </div>

  <div class="section">
    <div class="section-title">All Problems</div>
    <div class="table-wrap">
      <div class="table-controls">
        <input class="search-input" type="text" id="search" placeholder="Search problems..."/>
        <button class="filter-btn active" data-filter="All">All</button>
        <button class="filter-btn" data-filter="Easy">Easy</button>
        <button class="filter-btn" data-filter="Medium">Medium</button>
        <button class="filter-btn" data-filter="Hard">Hard</button>
      </div>
      <table>
        <thead>
          <tr>
            <th data-sort="title">Problem</th>
            <th data-sort="difficulty">Difficulty</th>
            <th data-sort="tags">Tags</th>
            <th data-sort="runtime">Runtime</th>
            <th data-sort="timestamp">Solved</th>
            <th data-sort="submissionCount">Attempts</th>
          </tr>
        </thead>
        <tbody id="problem-tbody"></tbody>
      </table>
    </div>
  </div>

</div>

<script>
const RAW = {data_json};
const {{ stats, problems }} = RAW;

// ── Updated label ──────────────────────────────────────────────────────────
document.getElementById('updated-label').textContent =
  'Updated ' + new Date().toLocaleDateString('en-GB', {{day:'numeric',month:'short',year:'numeric'}});

// ── Stat cards ─────────────────────────────────────────────────────────────
const statCards = [
  {{ label: 'Total Solved', value: stats.total, cls: '' }},
  {{ label: 'Easy', value: stats.difficulty.Easy, cls: 'easy' }},
  {{ label: 'Medium', value: stats.difficulty.Medium, cls: 'medium' }},
  {{ label: 'Hard', value: stats.difficulty.Hard, cls: 'hard' }},
  {{ label: 'Total Submissions', value: stats.total_submissions, cls: '' }},
];

const grid = document.getElementById('stats-grid');
statCards.forEach((c, i) => {{
  const el = document.createElement('div');
  el.className = 'stat-card';
  el.style.animationDelay = i * 60 + 'ms';
  el.innerHTML = `<div class="stat-label">${{c.label}}</div>
    <div class="stat-value ${{c.cls}}">${{c.value}}</div>`;
  grid.appendChild(el);
}});

// ── Difficulty bars ─────────────────────────────────────────────────────────
const diffWrap = document.getElementById('diff-bars');
const total = stats.total || 1;
['Easy','Medium','Hard'].forEach(d => {{
  const n = stats.difficulty[d];
  const pct = Math.round((n / total) * 100);
  diffWrap.innerHTML += `
    <div class="diff-row">
      <div class="diff-label ${{d}}">${{d}}</div>
      <div class="diff-bar-track">
        <div class="diff-bar-fill ${{d}}" style="width:0%" data-target="${{pct}}%"></div>
      </div>
      <div class="diff-num">${{n}}</div>
    </div>`;
}});
// Animate bars after paint
requestAnimationFrame(() => {{
  document.querySelectorAll('.diff-bar-fill').forEach(b => {{
    b.style.width = b.dataset.target;
  }});
}});

// ── Tags ────────────────────────────────────────────────────────────────────
const tagsWrap = document.getElementById('tags-grid');
const maxTagCount = stats.tags[0]?.[1] || 1;
stats.tags.forEach(([tag, count]) => {{
  const opacity = 0.4 + (count / maxTagCount) * 0.6;
  tagsWrap.innerHTML += `
    <div class="tag-pill" style="opacity:${{opacity.toFixed(2)}}">
      ${{tag}}<span class="tag-count">${{count}}</span>
    </div>`;
}});

// ── Calendar ────────────────────────────────────────────────────────────────
(function() {{
  const cal = stats.calendar;
  const today = new Date();
  const WEEKS = 26;
  const CELL = 14, GAP = 3, STEP = CELL + GAP;
  const LEFT_PAD = 32, TOP_PAD = 24;
  const W = LEFT_PAD + WEEKS * STEP + 4;
  const H = TOP_PAD + 7 * STEP + 24;

  const svg = document.getElementById('calendar-svg');
  svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);
  svg.setAttribute('width', W);
  svg.setAttribute('height', H);

  const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  [1,3,5].forEach(d => {{
    const y = TOP_PAD + d * STEP + CELL / 2;
    const t = document.createElementNS('http://www.w3.org/2000/svg','text');
    t.setAttribute('x', LEFT_PAD - 6);
    t.setAttribute('y', y);
    t.setAttribute('text-anchor','end');
    t.setAttribute('dominant-baseline','middle');
    t.setAttribute('fill','#4a4a6a');
    t.setAttribute('font-size','9');
    t.setAttribute('font-family','JetBrains Mono,monospace');
    t.textContent = days[d];
    svg.appendChild(t);
  }});

  // Walk back WEEKS*7 days
  const startDate = new Date(today);
  startDate.setDate(startDate.getDate() - (WEEKS * 7 - 1));

  const months = {{}};
  for (let w = 0; w < WEEKS; w++) {{
    for (let d = 0; d < 7; d++) {{
      const date = new Date(startDate);
      date.setDate(date.getDate() + w * 7 + d);
      const ds = date.toISOString().slice(0,10);
      const count = cal[ds] || 0;

      let fill = '#1e1e2e';
      if (count === 1) fill = '#312e81';
      else if (count === 2) fill = '#4338ca';
      else if (count >= 3) fill = '#7c6af7';

      const rect = document.createElementNS('http://www.w3.org/2000/svg','rect');
      rect.setAttribute('x', LEFT_PAD + w * STEP);
      rect.setAttribute('y', TOP_PAD + d * STEP);
      rect.setAttribute('width', CELL);
      rect.setAttribute('height', CELL);
      rect.setAttribute('rx', 3);
      rect.setAttribute('fill', fill);
      rect.setAttribute('data-date', ds);
      rect.setAttribute('data-count', count);
      rect.style.cursor = 'default';

      const title = document.createElementNS('http://www.w3.org/2000/svg','title');
      title.textContent = ds + (count ? ` — ${{count}} submission${{count>1?'s':''}}` : ' — none');
      rect.appendChild(title);
      svg.appendChild(rect);

      // Month label on first row (Sunday)
      if (d === 0) {{
        const mo = date.toLocaleString('en',{{month:'short'}});
        const key = date.getFullYear() + '-' + date.getMonth();
        if (!months[key]) {{
          months[key] = true;
          const t = document.createElementNS('http://www.w3.org/2000/svg','text');
          t.setAttribute('x', LEFT_PAD + w * STEP);
          t.setAttribute('y', TOP_PAD - 8);
          t.setAttribute('fill','#4a4a6a');
          t.setAttribute('font-size','9');
          t.setAttribute('font-family','JetBrains Mono,monospace');
          t.textContent = mo;
          svg.appendChild(t);
        }}
      }}
    }}
  }}
}})();

// ── Table ───────────────────────────────────────────────────────────────────
let currentFilter = 'All';
let currentSort = {{ key: 'timestamp', dir: -1 }};
let searchQuery = '';

function formatDate(ts) {{
  return new Date(ts * 1000).toLocaleDateString('en-GB',{{day:'numeric',month:'short',year:'numeric'}});
}}

function render() {{
  let rows = problems.filter(p => {{
    const matchFilter = currentFilter === 'All' || p.difficulty === currentFilter;
    const q = searchQuery.toLowerCase();
    const matchSearch = !q ||
      p.title.toLowerCase().includes(q) ||
      p.tags.some(t => t.toLowerCase().includes(q));
    return matchFilter && matchSearch;
  }});

  const {{ key, dir }} = currentSort;
  rows.sort((a, b) => {{
    let av = a[key], bv = b[key];
    if (typeof av === 'string') av = av.toLowerCase();
    if (typeof bv === 'string') bv = bv.toLowerCase();
    return av < bv ? -dir : av > bv ? dir : 0;
  }});

  const tbody = document.getElementById('problem-tbody');
  if (rows.length === 0) {{
    tbody.innerHTML = '<tr><td colspan="6" class="no-results">No problems found</td></tr>';
    return;
  }}

  tbody.innerHTML = rows.map(p => `
    <tr>
      <td>
        <a class="problem-link"
           href="https://leetcode.com/problems/${{p.titleSlug}}"
           target="_blank" rel="noopener">${{p.title}}</a>
      </td>
      <td><span class="badge badge-${{p.difficulty}}">${{p.difficulty}}</span></td>
      <td>${{p.tags.slice(0,3).map(t=>`<span class="tag-inline">${{t}}</span>`).join('')}}</td>
      <td>${{p.runtime === 0 ? '< 1ms' : p.runtime + 'ms'}}</td>
      <td style="color:var(--muted)">${{formatDate(p.timestamp)}}</td>
      <td><span class="submissions-count ${{p.submissionCount > 1 ? 'multi' : ''}}">${{p.submissionCount}}x</span></td>
    </tr>
  `).join('');
}}

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    currentFilter = btn.dataset.filter;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    render();
  }});
}});

// Search
document.getElementById('search').addEventListener('input', e => {{
  searchQuery = e.target.value;
  render();
}});

// Sort
document.querySelectorAll('th[data-sort]').forEach(th => {{
  th.addEventListener('click', () => {{
    const key = th.dataset.sort;
    if (currentSort.key === key) {{
      currentSort.dir *= -1;
    }} else {{
      currentSort = {{ key, dir: -1 }};
    }}
    render();
  }});
}});

render();
</script>
</body>
</html>"""


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    problems = load_all_problems()
    print(f"Found {len(problems)} problems")

    stats = build_stats(problems)
    rows = build_problem_rows(problems)

    html = generate_html(stats, rows)

    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"Dashboard written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()