"""
generate_dashboard.py — builds docs/index.html from problems/ metadata + analysis
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
        if "submissions" not in data:
            continue

        analysis_path = metadata_path.parent / "analysis.json"
        if analysis_path.exists():
            with open(analysis_path, "r") as f:
                data["analysis"] = json.load(f)
        else:
            data["analysis"] = None

        for ext in ["cs", "py", "cpp", "java", "js", "ts", "go", "rs"]:
            sol_path = metadata_path.parent / f"solution.{ext}"
            if sol_path.exists():
                with open(sol_path, "r") as f:
                    data["solutionCode"] = f.read()
                data["solutionExt"] = ext
                break
        else:
            data["solutionCode"] = ""
            data["solutionExt"] = "txt"

        problems.append(data)
    return problems


def build_stats(problems: list[dict]) -> dict:
    difficulty_count = {"Easy": 0, "Medium": 0, "Hard": 0}
    tag_count = {}
    pattern_count = {}
    calendar = {}
    total_submissions = 0

    for p in problems:
        diff = p.get("difficulty", "Unknown")
        diff = diff.capitalize()
        if diff in difficulty_count:
            difficulty_count[diff] += 1

        for tag in p.get("tags", []):
            tag_count[tag] = tag_count.get(tag, 0) + 1

        if p.get("analysis") and p["analysis"].get("pattern"):
            pat = p["analysis"]["pattern"]
            pattern_count[pat] = pattern_count.get(pat, 0) + 1

        for s in p.get("submissions", []):
            total_submissions += 1
            ts = s.get("timestamp")
            if ts:
                date_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
                calendar[date_str] = calendar.get(date_str, 0) + 1

    return {
        "total": len(problems),
        "total_submissions": total_submissions,
        "difficulty": difficulty_count,
        "tags": sorted(tag_count.items(), key=lambda x: x[1], reverse=True),
        "patterns": sorted(pattern_count.items(), key=lambda x: x[1], reverse=True),
        "calendar": calendar,
    }


def build_problem_rows(problems: list[dict]) -> list[dict]:
    rows = []
    for p in problems:
        latest = max(p["submissions"], key=lambda s: s["timestamp"])
        analysis = p.get("analysis") or {}
        rows.append({
            "title": p["title"],
            "titleSlug": p["titleSlug"],
            "difficulty": p.get("difficulty", "").capitalize(),
            "tags": p.get("tags", []),
            "runtime": latest["runtime"],
            "memory": round(latest["memory"] / 1_000_000, 1),
            "timestamp": latest["timestamp"],
            "submissionCount": len(p["submissions"]),
            "pattern": analysis.get("pattern", ""),
            "timeComplexity": analysis.get("timeComplexity", ""),
            "spaceComplexity": analysis.get("spaceComplexity", ""),
            "explanation": analysis.get("explanation", ""),
            "improvements": analysis.get("improvements", ""),
            "relatedPatterns": analysis.get("relatedPatterns", []),
            "solutionCode": p.get("solutionCode", ""),
            "solutionExt": p.get("solutionExt", "txt"),
        })
    rows.sort(key=lambda r: r["timestamp"], reverse=True)
    return rows


def generate_html(stats: dict, rows: list[dict]) -> str:
    data_json = json.dumps({"stats": stats, "problems": rows}, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>dsa.solutions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #0a0a0f;
  --surface: #111118;
  --border: #1e1e2e;
  --border2: rgba(255,255,255,0.12);
  --accent: #7c6af7;
  --accent-glow: rgba(124,106,247,0.12);
  --accent2: #f97316;
  --easy: #22c55e;
  --medium: #f59e0b;
  --hard: #ef4444;
  --text: #e2e8f0;
  --muted: #4a4a6a;
  --card: #13131f;
  --font: 'Syne', sans-serif;
  --mono: 'JetBrains Mono', monospace;
}}

*,*::before,*::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--mono);
  min-height: 100vh;
  overflow-x: hidden;
}}

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

.wrap {{
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
  position: relative;
  z-index: 1;
}}

/* ── Header ── */
header {{
  padding: 56px 0 40px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 48px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}}

.logo {{
  font-family: var(--font);
  font-weight: 800;
  font-size: 2.4rem;
  letter-spacing: -0.03em;
  line-height: 1;
}}

.logo span {{ color: var(--accent); }}

.header-right {{
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}}

.gh-link {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--muted);
  text-decoration: none;
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  transition: all 0.2s;
  font-family: var(--mono);
}}

.gh-link:hover {{
  border-color: var(--accent);
  color: var(--text);
  background: var(--accent-glow);
}}

.updated {{
  font-size: 0.72rem;
  color: var(--muted);
}}

/* ── Stats ── */
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin-bottom: 48px;
}}

.stat {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 22px;
  transition: border-color 0.2s, transform 0.2s;
  position: relative;
  overflow: hidden;
}}

.stat:hover {{
  border-color: var(--accent);
  transform: translateY(-2px);
}}

.stat::after {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--accent);
  opacity: 0;
  transition: opacity 0.2s;
}}

.stat:hover::after {{ opacity: 1; }}

.stat-val {{
  font-family: var(--font);
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  margin-bottom: 8px;
}}

.stat-val.easy {{ color: var(--easy); }}
.stat-val.medium {{ color: var(--medium); }}
.stat-val.hard {{ color: var(--hard); }}
.stat-val.accent {{ color: var(--accent); }}

.stat-lbl {{
  font-size: 0.68rem;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
}}

/* ── Section heading ── */
.sec-head {{
  font-family: var(--font);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}}

.sec-head::after {{
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}}

/* ── Two col ── */
.two-col {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 48px;
}}

@media (max-width: 640px) {{
  .two-col {{ grid-template-columns: 1fr; }}
  .logo {{ font-size: 1.8rem; }}
  .stat-val {{ font-size: 1.8rem; }}
}}

/* ── Card shell ── */
.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px;
}}

/* ── Diff bars ── */
.diff-item {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}}

.diff-item:last-child {{ margin-bottom: 0; }}

.diff-name {{
  font-size: 0.72rem;
  font-weight: 500;
  width: 56px;
  letter-spacing: 0.04em;
}}

.diff-name.easy {{ color: var(--easy); }}
.diff-name.medium {{ color: var(--medium); }}
.diff-name.hard {{ color: var(--hard); }}

.diff-track {{
  flex: 1;
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  overflow: hidden;
}}

.diff-fill {{
  height: 100%;
  border-radius: 3px;
  transition: width 1s cubic-bezier(0.16,1,0.3,1);
}}

.diff-fill.easy {{ background: var(--easy); }}
.diff-fill.medium {{ background: var(--medium); }}
.diff-fill.hard {{ background: var(--hard); }}

.diff-n {{
  font-size: 0.78rem;
  font-weight: 500;
  width: 22px;
  text-align: right;
  color: var(--muted);
}}

/* ── Tags ── */
.tags-wrap {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}

.tag-chip {{
  font-size: 0.72rem;
  font-weight: 400;
  padding: 5px 11px;
  border-radius: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--muted);
  cursor: pointer;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--mono);
}}

.tag-chip:hover, .tag-chip.active {{
  border-color: var(--accent);
  color: var(--text);
  background: var(--accent-glow);
}}

.tag-chip .cnt {{
  font-size: 0.65rem;
  color: var(--accent);
  font-weight: 500;
}}

/* ── Patterns ── */
.patterns-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 10px;
  margin-bottom: 48px;
}}

.pat-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.15s;
}}

.pat-card:hover, .pat-card.active {{
  border-color: var(--accent);
  background: var(--accent-glow);
}}

.pat-name {{
  font-family: var(--font);
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 4px;
  color: var(--text);
}}

.pat-cnt {{
  font-size: 0.68rem;
  color: var(--muted);
  letter-spacing: 0.05em;
}}

/* ── Calendar ── */
.cal-wrap {{
  overflow-x: auto;
  padding-bottom: 4px;
}}

/* ── Controls ── */
.controls {{
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
}}

.search {{
  font-family: var(--mono);
  font-size: 0.78rem;
  padding: 9px 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--card);
  color: var(--text);
  outline: none;
  width: 260px;
  transition: border-color 0.2s;
}}

.search:focus {{ border-color: var(--accent); }}
.search::placeholder {{ color: var(--muted); }}

.fpill {{
  font-family: var(--mono);
  font-size: 0.72rem;
  padding: 7px 14px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.15s;
  letter-spacing: 0.04em;
}}

.fpill:hover, .fpill.on {{
  border-color: var(--accent);
  color: var(--text);
  background: var(--accent-glow);
}}

/* ── Problem cards ── */
#problem-list {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}

.pc {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  transition: border-color 0.2s;
}}

.pc:hover {{ border-color: var(--border2); }}
.pc.open {{ border-color: var(--accent); }}

.ph {{
  display: grid;
  grid-template-columns: 1fr auto auto auto auto;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  cursor: pointer;
  user-select: none;
}}

.pt {{
  font-family: var(--font);
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}}

.pt span {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

.pnum {{
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--muted);
  flex-shrink: 0;
}}

.badge {{
  font-size: 0.65rem;
  font-weight: 500;
  padding: 3px 9px;
  border-radius: 5px;
  letter-spacing: 0.04em;
  flex-shrink: 0;
  font-family: var(--mono);
}}

.badge.Easy {{ background: rgba(34,197,94,0.1); color: var(--easy); }}
.badge.Medium {{ background: rgba(245,158,11,0.1); color: var(--medium); }}
.badge.Hard {{ background: rgba(239,68,68,0.1); color: var(--hard); }}

.ppat {{
  font-size: 0.65rem;
  font-weight: 500;
  color: var(--accent);
  background: var(--accent-glow);
  padding: 3px 9px;
  border-radius: 5px;
  flex-shrink: 0;
  white-space: nowrap;
  font-family: var(--mono);
}}

.prt {{
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--muted);
  flex-shrink: 0;
}}

.pchev {{
  color: var(--muted);
  transition: transform 0.25s;
  flex-shrink: 0;
  font-size: 1rem;
}}

.pc.open .pchev {{ transform: rotate(180deg); }}

/* ── Detail panel ── */
.pd {{
  display: none;
  border-top: 1px solid var(--border);
}}

.pc.open .pd {{ display: block; }}

.pd-inner {{
  padding: 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}}

@media (max-width: 700px) {{
  .pd-inner {{ grid-template-columns: 1fr; }}
  .ph {{ grid-template-columns: 1fr auto auto; }}
  .ppat, .prt {{ display: none; }}
}}

.panel {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}}

.panel-head {{
  padding: 10px 14px;
  font-size: 0.65rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--mono);
}}

.panel-body {{ padding: 14px; }}

.rev-btn {{
  font-family: var(--mono);
  font-size: 0.65rem;
  font-weight: 500;
  padding: 4px 10px;
  border: 1px solid var(--accent);
  border-radius: 6px;
  background: var(--accent-glow);
  color: var(--accent);
  cursor: pointer;
  transition: all 0.15s;
  letter-spacing: 0.04em;
}}

.rev-btn:hover {{
  background: var(--accent);
  color: #fff;
}}

.locked {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px 12px;
  text-align: center;
}}

.locked p {{
  font-size: 0.72rem;
  color: var(--muted);
  line-height: 1.6;
}}

.lock-icon {{
  font-size: 1.4rem;
  color: var(--muted);
}}

.revealed {{ display: none; }}
.revealed.shown {{ display: block; }}

.hint-steps {{
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}}

.hint-steps li {{
  display: flex;
  gap: 10px;
  align-items: flex-start;
  font-size: 0.72rem;
  color: var(--text);
  line-height: 1.7;
}}

.snum {{
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent-glow);
  border: 1px solid var(--accent);
  color: var(--accent);
  font-size: 0.6rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;
  font-family: var(--mono);
}}

.cx-row {{
  display: flex;
  gap: 8px;
  margin-top: 12px;
}}

.cx {{
  font-family: var(--mono);
  font-size: 0.65rem;
  padding: 3px 8px;
  border-radius: 5px;
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 5px;
}}

.cx em {{
  color: var(--muted);
  font-size: 0.6rem;
  font-style: normal;
  opacity: 0.6;
}}

.improve {{
  margin-top: 12px;
  padding: 10px 12px;
  background: rgba(249,115,22,0.06);
  border: 1px solid rgba(249,115,22,0.2);
  border-radius: 8px;
  font-size: 0.68rem;
  color: var(--text);
  line-height: 1.6;
}}

.tag-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 12px;
}}

.t-chip {{
  font-size: 0.62rem;
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--card);
  color: var(--muted);
  border: 1px solid var(--border);
  font-family: var(--mono);
}}

.code-block {{
  background: var(--bg);
  border-radius: 7px;
  overflow: auto;
  max-height: 300px;
  font-family: var(--mono);
  font-size: 0.68rem;
  line-height: 1.65;
  color: var(--text);
  padding: 14px;
  white-space: pre;
  border: 1px solid var(--border);
}}

.p-links {{
  display: flex;
  gap: 10px;
  padding: 0 20px 16px;
}}

.lc-link {{
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--accent);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 14px;
  border: 1px solid var(--accent);
  border-radius: 8px;
  background: var(--accent-glow);
  transition: all 0.15s;
  font-family: var(--mono);
}}

.lc-link:hover {{
  background: var(--accent);
  color: #fff;
}}

.empty {{
  text-align: center;
  padding: 60px;
  color: var(--muted);
  font-size: 0.8rem;
}}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="logo">dsa<span>.</span>solutions</div>
    <div class="header-right">
      <a class="gh-link" href="https://github.com/shouvik-halder/DSA-Solutions" target="_blank">
        ↗ github
      </a>
      <div class="updated" id="ts"></div>
    </div>
  </header>

  <div class="stats-grid" id="stats-grid"></div>

  <div class="two-col">
    <div>
      <div class="sec-head">Difficulty</div>
      <div class="card" id="diff-card"></div>
    </div>
    <div>
      <div class="sec-head">Topics mastered</div>
      <div class="card">
        <div class="tags-wrap" id="tags-wrap"></div>
      </div>
    </div>
  </div>

  <div class="sec-head">Algorithmic patterns</div>
  <div class="patterns-grid" id="patterns-grid"></div>

  <div style="margin-bottom:48px">
    <div class="sec-head">Activity</div>
    <div class="card">
      <div class="cal-wrap"><svg id="cal-svg"></svg></div>
    </div>
  </div>

  <div style="margin-bottom:48px">
    <div class="sec-head">Problems</div>
    <div class="controls">
      <input class="search" id="srch" type="text" placeholder="Search by title, tag, or pattern…"/>
      <button class="fpill on" data-f="All">All</button>
      <button class="fpill" data-f="Easy">Easy</button>
      <button class="fpill" data-f="Medium">Medium</button>
      <button class="fpill" data-f="Hard">Hard</button>
    </div>
    <div id="problem-list"></div>
  </div>

</div>

<script>
const DATA = {data_json};
const {{ stats, problems }} = DATA;

document.getElementById('ts').textContent =
  'Updated ' + new Date().toLocaleDateString('en-GB', {{day:'numeric',month:'short',year:'numeric'}});

// Stats
const STATS = [
  {{ lbl:'Total Solved', val:stats.total, cls:'' }},
  {{ lbl:'Easy', val:stats.difficulty.Easy, cls:'easy' }},
  {{ lbl:'Medium', val:stats.difficulty.Medium, cls:'medium' }},
  {{ lbl:'Hard', val:stats.difficulty.Hard, cls:'hard' }},
  {{ lbl:'Submissions', val:stats.total_submissions, cls:'accent' }},
];
const sg = document.getElementById('stats-grid');
STATS.forEach(s => {{
  sg.innerHTML += `<div class="stat"><div class="stat-val ${{s.cls}}">${{s.val}}</div><div class="stat-lbl">${{s.lbl}}</div></div>`;
}});

// Diff bars
const dc = document.getElementById('diff-card');
const tot = stats.total || 1;
['Easy','Medium','Hard'].forEach(d => {{
  const n = stats.difficulty[d];
  const pct = Math.round(n/tot*100);
  dc.innerHTML += `<div class="diff-item">
    <span class="diff-name ${{d}}">${{d}}</span>
    <div class="diff-track"><div class="diff-fill ${{d.toLowerCase()}}" style="width:0%" data-w="${{pct}}%"></div></div>
    <span class="diff-n">${{n}}</span>
  </div>`;
}});
requestAnimationFrame(() => {{
  document.querySelectorAll('.diff-fill').forEach(el => el.style.width = el.dataset.w);
}});

// Tags
let activeTag = null;
const tw = document.getElementById('tags-wrap');
stats.tags.forEach(([tag, count]) => {{
  const el = document.createElement('button');
  el.className = 'tag-chip';
  el.dataset.tag = tag;
  el.innerHTML = `${{tag}} <span class="cnt">${{count}}</span>`;
  el.onclick = () => {{
    activeTag = activeTag === tag ? null : tag;
    document.querySelectorAll('.tag-chip').forEach(c => c.classList.toggle('active', c.dataset.tag === activeTag));
    render();
  }};
  tw.appendChild(el);
}});

// Patterns
let activePat = null;
const pg = document.getElementById('patterns-grid');
if (stats.patterns.length === 0) {{
  pg.innerHTML = '<div style="color:var(--muted);font-size:0.72rem;grid-column:1/-1">No pattern analysis yet — run sync to generate.</div>';
}} else {{
  stats.patterns.forEach(([pat, count]) => {{
    const el = document.createElement('div');
    el.className = 'pat-card';
    el.dataset.pat = pat;
    el.innerHTML = `<div class="pat-name">${{pat}}</div><div class="pat-cnt">${{count}} problem${{count>1?'s':''}}</div>`;
    el.onclick = () => {{
      activePat = activePat === pat ? null : pat;
      document.querySelectorAll('.pat-card').forEach(c => c.classList.toggle('active', c.dataset.pat === activePat));
      render();
    }};
    pg.appendChild(el);
  }});
}}

// Calendar
(function() {{
            const cal = stats.calendar;
            const WEEKS = 26,
                CELL = 14,
                GAP = 3,
                STEP = CELL + GAP,
                LP = 32,
                TP = 24;
            const W = LP + WEEKS * STEP + 4,
                H = TP + 7 * STEP + 24;
            const svg = document.getElementById('cal-svg');
            svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);
            svg.setAttribute('width', W);
            svg.setAttribute('height', H);
            const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            [1, 3, 5].forEach(d => {{
                    const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    t.setAttribute('x', LP - 6);
                    t.setAttribute('y', TP + d * STEP + CELL / 2);
                    t.setAttribute('text-anchor', 'end');
                    t.setAttribute('dominant-baseline', 'middle');
                    t.setAttribute('fill', '#4a4a6a');
                    t.setAttribute('font-size', '9');
                    t.setAttribute('font-family', 'JetBrains Mono,monospace');
                    t.textContent = days[d];
                    svg.appendChild(t);
                }});

            // Anchor to today in LOCAL time so day-of-week matches the grid
            const today = new Date();
            const todayStr = today.getFullYear() + '-' +
                String(today.getMonth() + 1).padStart(2, '0') + '-' +
                String(today.getDate()).padStart(2, '0');

            // Step back to the Sunday that starts the 26-week window
            const startDate = new Date(today);
            startDate.setDate(today.getDate() - (WEEKS * 7 - 1));
            // Align to Sunday
            startDate.setDate(startDate.getDate() - startDate.getDay());

            const months = {
                {}
            };
            let todayRect = null;

            for (let w = 0; w < WEEKS; w++) {{
                    for (let d = 0; d < 7; d++) {{
                            const date = new Date(startDate);
                            date.setDate(startDate.getDate() + w * 7 + d);

                            const ds = date.getFullYear() + '-' +
                                String(date.getMonth() + 1).padStart(2, '0') + '-' +
                                String(date.getDate()).padStart(2, '0');

                            const count = cal[ds] || 0;
                            const isToday = ds === todayStr;

                            let fill = '#1e1e2e';
                            if (count === 1) fill = '#312e81';
                            else if (count === 2) fill = '#4338ca';
                            else if (count >= 3) fill = '#7c6af7';

                            const x = LP + w * STEP;
                            const y = TP + d * STEP;

                            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                            rect.setAttribute('x', x);
                            rect.setAttribute('y', y);
                            rect.setAttribute('width', CELL);
                            rect.setAttribute('height', CELL);
                            rect.setAttribute('rx', 3);
                            rect.setAttribute('fill', fill);

                            const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
                            title.textContent = ds + (count ? ` — ${{count}} submission${{count>1?'s':''}}` : '');
                            rect.appendChild(title);
                            svg.appendChild(rect);

                            // Today: draw a border rect on top
                            if (isToday) {{
                                    todayRect = {
                                        {
                                            x,
                                            y
                                        }
                                    };
                                }}

                            // Month label on first day of each column
                            if (d === 0) {{
                                    const mo = date.toLocaleString('en', {
                                        {
                                            month: 'short'
                                        }
                                    });
                                    const key = date.getFullYear() + '-' + date.getMonth();
                                    if (!months[key]) {{
                                            months[key] = true;
                                            const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                                            t.setAttribute('x', LP + w * STEP);
                                            t.setAttribute('y', TP - 8);
                                            t.setAttribute('fill', '#4a4a6a');
                                            t.setAttribute('font-size', '9');
                                            t.setAttribute('font-family', 'JetBrains Mono,monospace');
                                            t.textContent = mo;
                                            svg.appendChild(t);
                                        }}
                                        
                                }}
                        }}
                }}

// Draw today highlight on top of everything else
 if (todayRect) {{
         const highlight = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
         highlight.setAttribute('x', todayRect.x);
         highlight.setAttribute('y', todayRect.y);
         highlight.setAttribute('width', CELL);
         highlight.setAttribute('height', CELL);
         highlight.setAttribute('rx', 3);
         highlight.setAttribute('fill', 'none');
         highlight.setAttribute('stroke', '#7c6af7');
         highlight.setAttribute('stroke-width', '1.5');
         svg.appendChild(highlight);

         // Dot below today's column
         const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
         dot.setAttribute('cx', todayRect.x + CELL / 2);
         dot.setAttribute('cy', TP + 7 * STEP + 6);
         dot.setAttribute('r', 2);
         dot.setAttribute('fill', '#7c6af7');
         svg.appendChild(dot);
     }}
 }})();

// Hints builder
function buildHints(p) {{
  const h = [];
  if(p.pattern) h.push(`Think about using the <strong>${{p.pattern}}</strong> technique.`);
  if(p.timeComplexity) h.push(`Aim for <strong>${{p.timeComplexity}}</strong> time complexity.`);
  if(p.explanation) h.push(p.explanation.split(' ').slice(0,14).join(' ')+'…');
  if(p.relatedPatterns&&p.relatedPatterns.length) h.push(`Related: ${{p.relatedPatterns.join(', ')}}.`);
  return h;
}}

function esc(s) {{
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

// Render
let currentFilter='All', searchQ='';

function render() {{
  let rows = problems.filter(p => {{
    const mf = currentFilter==='All'||p.difficulty===currentFilter;
    const q  = searchQ.toLowerCase();
    const ms = !q||p.title.toLowerCase().includes(q)
      ||p.tags.some(t=>t.toLowerCase().includes(q))
      ||(p.pattern||'').toLowerCase().includes(q);
    const mt = !activeTag||p.tags.includes(activeTag);
    const mp = !activePat||p.pattern===activePat;
    return mf&&ms&&mt&&mp;
  }});

  const list = document.getElementById('problem-list');

  if(!rows.length) {{
    list.innerHTML='<div class="empty">No problems match your filters.</div>';
    return;
  }}

  list.innerHTML = rows.map((p,i) => {{
    const id = `p${{i}}`;
    const hints = buildHints(p);
    const hItems = hints.map((h,j)=>`<li><span class="snum">${{j+1}}</span><span>${{h}}</span></li>`).join('');
    const code = esc(p.solutionCode||'// No solution file found');
    const rt = p.runtime===0?'< 1ms':p.runtime+'ms';
    const hasAnalysis = p.pattern||p.timeComplexity||p.explanation;

    return `<div class="pc" id="${{id}}">
      <div class="ph" onclick="tog('${{id}}')">
        <div class="pt"><span class="pnum">#${{i+1}}</span><span>${{esc(p.title)}}</span></div>
        ${{p.pattern?`<span class="ppat">${{esc(p.pattern)}}</span>`:''}}
        <span class="badge ${{p.difficulty}}">${{p.difficulty}}</span>
        <span class="prt">${{rt}}</span>
        <span class="pchev">⌄</span>
      </div>
      <div class="pd">
        <div class="pd-inner">

          <div class="panel">
            <div class="panel-head">
              💡 hint
              <button class="rev-btn" id="${{id}}-hbtn" onclick="revH('${{id}}')">Reveal</button>
            </div>
            <div class="panel-body">
              <div class="locked" id="${{id}}-hl">
                <span class="lock-icon">🔒</span>
                <p>Try solving this first.<br/>Click reveal when ready.</p>
              </div>
              <div class="revealed" id="${{id}}-hc">
                ${{hasAnalysis?`<ul class="hint-steps">${{hItems}}</ul>
                ${{p.improvements&&p.improvements!=='null'?`<div class="improve">💡 ${{esc(p.improvements)}}</div>`:''}}
                <div class="cx-row">
                  <span class="cx"><em>time</em>${{esc(p.timeComplexity||'—')}}</span>
                  <span class="cx"><em>space</em>${{esc(p.spaceComplexity||'—')}}</span>
                </div>
                <div class="tag-row">${{p.tags.map(t=>`<span class="t-chip">${{esc(t)}}</span>`).join('')}}</div>`
                :'<p style="font-size:0.72rem;color:var(--muted)">No analysis available yet.</p>'}}
              </div>
            </div>
          </div>

          <div class="panel">
            <div class="panel-head">
              ⌨ solution.${{p.solutionExt}}
              <button class="rev-btn" id="${{id}}-sbtn" onclick="revS('${{id}}')">Reveal</button>
            </div>
            <div class="panel-body">
              <div class="locked" id="${{id}}-sl">
                <span class="lock-icon">🔒</span>
                <p>Solution hidden.<br/>Attempt first.</p>
              </div>
              <div class="revealed" id="${{id}}-sc">
                <div class="code-block">${{code}}</div>
              </div>
            </div>
          </div>

        </div>
        <div class="p-links">
          <a class="lc-link" href="https://leetcode.com/problems/${{p.titleSlug}}/" target="_blank">Open on LeetCode ↗</a>
        </div>
      </div>
    </div>`;
  }}).join('');
}}

function tog(id) {{
  document.getElementById(id).classList.toggle('open');
}}

function revH(id) {{
  document.getElementById(id+'-hl').style.display='none';
  document.getElementById(id+'-hc').classList.add('shown');
  document.getElementById(id+'-hbtn').style.display='none';
}}

function revS(id) {{
  document.getElementById(id+'-sl').style.display='none';
  document.getElementById(id+'-sc').classList.add('shown');
  document.getElementById(id+'-sbtn').style.display='none';
}}

document.querySelectorAll('.fpill').forEach(b => {{
  b.addEventListener('click', () => {{
    currentFilter=b.dataset.f;
    document.querySelectorAll('.fpill').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    render();
  }});
}});

document.getElementById('srch').addEventListener('input', e => {{
  searchQ=e.target.value; render();
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
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()