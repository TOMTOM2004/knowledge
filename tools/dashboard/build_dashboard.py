#!/usr/bin/env python3
"""
準備進捗マトリクス HTML ダッシュボード生成。

company-info/<企業名>/ 配下のファイル名から各企業の準備ステージ
(brief / interview_research / interview_qa / transcript / reflection)
を検出し、単一HTMLに出力。
"""

from __future__ import annotations

import html
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPANY_DIR = ROOT / "company-info"
OUTPUT = Path(__file__).resolve().parent / "index.html"

# 「1次」「2次」「3次」「最終」「面談」を捕捉。
STEP_RE = re.compile(r"(?P<step>1次|2次|3次|4次|5次|最終|面談|面談会)")
DATE_RE = re.compile(r"(20\d{6})")

KIND_PREFIXES = [
    ("research", "interview_research_"),
    ("qa", "interview_qa_"),
    ("transcript", "transcript_"),
    ("reflection", "reflection_"),
    ("prep_legacy", "interview_prep_"),
    ("direct_prep", "interview_direct_prep_"),
]

# ステージ表示順
STAGE_ORDER = ["brief", "1次", "面談", "2次", "3次", "4次", "5次", "最終"]
STAGE_LABEL = {
    "brief": "Brief",
    "1次": "1次",
    "面談": "面談",
    "2次": "2次",
    "3次": "3次",
    "4次": "4次",
    "5次": "5次",
    "最終": "最終",
}

KIND_LABEL = {
    "research": "調査",
    "qa": "想定問答",
    "transcript": "文字起こし",
    "reflection": "振り返り",
    "prep_legacy": "旧prep",
    "direct_prep": "直前準備",
}
KIND_ORDER_PER_STAGE = ["research", "qa", "transcript", "reflection"]
KIND_GLYPH = {
    "research": "R",
    "qa": "Q",
    "transcript": "T",
    "reflection": "F",
}


@dataclass
class Company:
    name: str
    has_brief: bool = False
    brief_updated: str | None = None
    course: str | None = None
    # stage("1次") -> kind("research") -> latest YYYYMMDD
    stages: dict[str, dict[str, str]] = field(default_factory=lambda: defaultdict(dict))
    file_count: int = 0


def parse_brief_frontmatter(path: Path) -> tuple[str | None, str | None]:
    """Return (course, updated_at|created_at) from YAML frontmatter."""
    course: str | None = None
    updated: str | None = None
    created: str | None = None
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None, None
    if not text.startswith("---"):
        return None, None
    end = text.find("\n---", 3)
    if end == -1:
        return None, None
    block = text[3:end]
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("course:"):
            course = line.split(":", 1)[1].strip()
        elif line.startswith("updated_at:"):
            updated = line.split(":", 1)[1].strip()
        elif line.startswith("created_at:"):
            created = line.split(":", 1)[1].strip()
    return course, updated or created


def detect_kind(filename: str) -> str | None:
    for kind, prefix in KIND_PREFIXES:
        if filename.startswith(prefix):
            return kind
    return None


def detect_stage(filename: str) -> str | None:
    m = STEP_RE.search(filename)
    if not m:
        return None
    s = m.group("step")
    if s in ("面談", "面談会"):
        return "面談"
    return s


def latest_date(filename: str) -> str | None:
    m = DATE_RE.search(filename)
    return m.group(1) if m else None


def scan() -> list[Company]:
    companies: list[Company] = []
    for sub in sorted(COMPANY_DIR.iterdir()):
        if not sub.is_dir():
            continue
        c = Company(name=sub.name)
        for f in sub.iterdir():
            if not f.is_file() or not f.name.endswith(".md"):
                continue
            c.file_count += 1
            if f.name == "research_brief.md":
                c.has_brief = True
                c.course, c.brief_updated = parse_brief_frontmatter(f)
                continue
            kind = detect_kind(f.name)
            stage = detect_stage(f.name)
            if not kind or not stage:
                continue
            date = latest_date(f.name) or ""
            cur = c.stages[stage].get(kind, "")
            if date >= cur:
                c.stages[stage][kind] = date
        companies.append(c)
    return companies


def progress_score(c: Company) -> int:
    """Sort key: 完了度高い順 (transcript有 > qa有 > research有 > brief有)。"""
    score = 0
    if c.has_brief:
        score += 1
    for stage, kinds in c.stages.items():
        for k in ("research", "qa", "transcript", "reflection"):
            if k in kinds:
                score += {"research": 2, "qa": 4, "transcript": 8, "reflection": 6}[k]
    return score


def render_stage_cell(kinds: dict[str, str]) -> str:
    """4種(R/Q/T/F)の有無を1セルにまとめる。"""
    if not kinds:
        return '<td class="cell empty">–</td>'
    badges = []
    for k in KIND_ORDER_PER_STAGE:
        if k in kinds:
            badges.append(
                f'<span class="badge {k}" title="{KIND_LABEL[k]} ({kinds[k]})">{KIND_GLYPH[k]}</span>'
            )
        else:
            badges.append(f'<span class="badge missing">{KIND_GLYPH[k]}</span>')
    return f'<td class="cell">{"".join(badges)}</td>'


def render_brief_cell(c: Company) -> str:
    if not c.has_brief:
        return '<td class="cell empty">–</td>'
    sub = []
    if c.course:
        sub.append(html.escape(c.course))
    if c.brief_updated:
        sub.append(html.escape(c.brief_updated))
    sub_html = (
        f'<div class="sub">{" / ".join(sub)}</div>' if sub else ""
    )
    return f'<td class="cell brief"><span class="badge brief-on">✓</span>{sub_html}</td>'


def render(companies: list[Company]) -> str:
    companies_sorted = sorted(companies, key=lambda c: (-progress_score(c), c.name))

    total = len(companies_sorted)
    with_brief = sum(1 for c in companies_sorted if c.has_brief)
    with_qa = sum(1 for c in companies_sorted if any("qa" in k for k in c.stages.values()))
    with_transcript = sum(
        1 for c in companies_sorted if any("transcript" in k for k in c.stages.values())
    )
    with_reflection = sum(
        1 for c in companies_sorted if any("reflection" in k for k in c.stages.values())
    )

    rows = []
    for c in companies_sorted:
        cells = [f'<td class="company">{html.escape(c.name)}</td>']
        cells.append(render_brief_cell(c))
        for stage in STAGE_ORDER[1:]:
            cells.append(render_stage_cell(c.stages.get(stage, {})))
        cells.append(f'<td class="num">{c.file_count}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")

    headers = (
        '<th class="company">企業</th>'
        + "".join(f'<th class="stage">{STAGE_LABEL[s]}</th>' for s in STAGE_ORDER)
        + '<th class="num">files</th>'
    )

    legend_items = "".join(
        f'<span class="legend-item"><span class="badge {k}">{KIND_GLYPH[k]}</span> {KIND_LABEL[k]}</span>'
        for k in KIND_ORDER_PER_STAGE
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>準備進捗ダッシュボード</title>
<style>
:root {{
  --bg: #0f1115;
  --panel: #161a22;
  --border: #242935;
  --text: #e6e8eb;
  --muted: #8a93a6;
  --on: #4ade80;
  --warn: #fbbf24;
  --off: #2a3142;
  --brief: #38bdf8;
  --research: #a78bfa;
  --qa: #f472b6;
  --transcript: #facc15;
  --reflection: #34d399;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: -apple-system, "Hiragino Sans", "Yu Gothic", system-ui, sans-serif;
  margin: 0; padding: 24px;
  background: var(--bg); color: var(--text);
  font-size: 14px;
}}
h1 {{ font-size: 20px; margin: 0 0 4px; }}
.meta {{ color: var(--muted); font-size: 12px; margin-bottom: 16px; }}
.summary {{
  display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;
}}
.stat {{
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 14px; min-width: 120px;
}}
.stat .v {{ font-size: 22px; font-weight: 600; }}
.stat .k {{ font-size: 11px; color: var(--muted); }}
.legend {{
  display: flex; gap: 14px; margin-bottom: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: 12px;
}}
.legend-item {{ display: inline-flex; align-items: center; gap: 4px; }}
.controls {{ margin-bottom: 12px; }}
.controls input {{
  background: var(--panel); border: 1px solid var(--border); color: var(--text);
  padding: 6px 10px; border-radius: 6px; min-width: 240px;
}}
table {{
  width: 100%; border-collapse: separate; border-spacing: 0;
  background: var(--panel); border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden;
}}
th, td {{ padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); }}
th {{
  background: #1c212d; color: var(--muted); font-weight: 500;
  font-size: 12px; position: sticky; top: 0; z-index: 1;
  cursor: pointer; user-select: none;
}}
th.stage, td.cell, th.num, td.num {{ text-align: center; }}
td.company {{ font-weight: 500; white-space: nowrap; }}
td.cell.empty {{ color: var(--off); }}
td.cell .sub {{ font-size: 10px; color: var(--muted); margin-top: 2px; }}
.badge {{
  display: inline-block; min-width: 18px; height: 18px; line-height: 18px;
  text-align: center; border-radius: 4px; font-size: 10px; font-weight: 700;
  margin: 0 1px; padding: 0 3px;
}}
.badge.research {{ background: var(--research); color: #1a0f2e; }}
.badge.qa {{ background: var(--qa); color: #2a0a1c; }}
.badge.transcript {{ background: var(--transcript); color: #2a1f00; }}
.badge.reflection {{ background: var(--reflection); color: #07261a; }}
.badge.brief-on {{ background: var(--brief); color: #002030; }}
.badge.missing {{ background: var(--off); color: #495069; }}
tr:hover td {{ background: #1a2030; }}
tr.hidden {{ display: none; }}
</style>
</head>
<body>
<h1>準備進捗ダッシュボード</h1>
<div class="meta">生成: {now} / 対象: {COMPANY_DIR.relative_to(ROOT)}</div>

<div class="summary">
  <div class="stat"><div class="v">{total}</div><div class="k">総企業数</div></div>
  <div class="stat"><div class="v">{with_brief}</div><div class="k">research_brief 済</div></div>
  <div class="stat"><div class="v">{with_qa}</div><div class="k">想定問答 着手</div></div>
  <div class="stat"><div class="v">{with_transcript}</div><div class="k">面接実施済</div></div>
  <div class="stat"><div class="v">{with_reflection}</div><div class="k">振り返り済</div></div>
</div>

<div class="legend">
  <span>各セル:</span> {legend_items}
  <span>（薄色 = 未実施）</span>
</div>

<div class="controls">
  <input id="filter" type="text" placeholder="企業名で絞り込み (例: みずほ, アセット)">
</div>

<table id="t">
  <thead><tr>{headers}</tr></thead>
  <tbody>
    {chr(10).join(rows)}
  </tbody>
</table>

<script>
const input = document.getElementById('filter');
const rows = document.querySelectorAll('#t tbody tr');
input.addEventListener('input', () => {{
  const q = input.value.trim().toLowerCase();
  rows.forEach(r => {{
    const name = r.querySelector('td.company').textContent.toLowerCase();
    r.classList.toggle('hidden', q && !name.includes(q));
  }});
}});
</script>
</body>
</html>
"""


def main() -> int:
    if not COMPANY_DIR.is_dir():
        print(f"ERROR: not found: {COMPANY_DIR}", file=sys.stderr)
        return 1
    companies = scan()
    OUTPUT.write_text(render(companies), encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(companies)} companies)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
