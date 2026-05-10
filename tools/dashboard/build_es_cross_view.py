#!/usr/bin/env python3
"""
ES横断ビュー HTML 生成。

ES/部品/{gakuchika,motivation,self_pr,other}.md から
頻出設問への複数回答を抽出し、4タブの単一HTMLに出力。
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTS_DIR = ROOT / "ES" / "部品"
OUTPUT = Path(__file__).resolve().parent / "es_cross_view.html"

TABS = [
    ("gakuchika", "ガクチカ", "gakuchika.md"),
    ("self_pr", "自己PR", "self_pr.md"),
    ("motivation", "志望動機", "motivation.md"),
    ("other", "その他頻出", "other.md"),
]


@dataclass
class Entry:
    """1つの回答エントリー。"""
    company: str
    question: str
    body: str
    length: str = ""           # "400字" などの表示用
    is_best: bool = False
    note: str = ""             # 出典補足 (submitted/draft 等)


@dataclass
class Section:
    """グループ/カテゴリ単位。"""
    title: str
    entries: list[Entry] = field(default_factory=list)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_h2_sections(text: str) -> list[tuple[str, str]]:
    """## 見出しでセクション分割。frontmatter は除去。"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    out: list[tuple[str, str]] = []
    for p in parts[1:]:
        nl = p.find("\n")
        title = p[:nl].strip() if nl != -1 else p.strip()
        body = p[nl + 1 :] if nl != -1 else ""
        out.append((title, body))
    return out


def split_entries(section_body: str) -> list[tuple[str, str, str]]:
    """
    セクション本体を ### / #### で区切り、(level, header, body) を返す。
    """
    pattern = re.compile(r"^(#{3,4})\s+(.+)$", re.MULTILINE)
    entries: list[tuple[str, str, str]] = []
    matches = list(pattern.finditer(section_body))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_body)
        level = "####" if m.group(1) == "####" else "###"
        header = m.group(2).strip()
        body = section_body[start:end].strip()
        entries.append((level, header, body))
    return entries


# ---------- gakuchika / self_pr / other 共通パーサ ----------

HEADER_BEST_RE = re.compile(r"⭐\s*ベスト(?:アンサー)?[^（(]*[（(]?\s*出典[:：]\s*([^/）)]+?)(?:\s*/\s*([^)）]+))?\s*[）)]")
# `#### [会社 / 設問]（字数）`
HEADER_OTHER_RE = re.compile(r"^\[([^/\]]+?)(?:\s*/\s*(.+?))?\](?:\s*[（(]\s*([^)）]+?)\s*[)）])?$")


def parse_grouped_file(text: str) -> list[Section]:
    sections: list[Section] = []
    for title, body in split_h2_sections(text):
        # 「Group 1: ...」「カテゴリ1: ...」両対応。タイトルはそのまま使う。
        sec = Section(title=title)
        for level, header, ebody in split_entries(body):
            if header.startswith("選定理由") or header.startswith("詳細") or header.startswith("他バージョン"):
                continue
            if level == "###":
                m = HEADER_BEST_RE.search(header)
                if m:
                    company = m.group(1).strip()
                    question = (m.group(2) or "").strip()
                    e = Entry(company=company, question=question, body=clean_body(ebody), is_best=True)
                    e.length = extract_length(ebody)
                    sec.entries.append(e)
                continue
            # level == "####"
            m = HEADER_OTHER_RE.match(header)
            if not m:
                continue
            company = m.group(1).strip()
            question = (m.group(2) or "").strip()
            length = (m.group(3) or "").strip()
            note = ""
            for tag in ("submitted", "draft"):
                if tag in company:
                    note = tag
                    company = company.replace(tag, "").strip()
            e = Entry(company=company, question=question, body=clean_body(ebody), length=length, note=note)
            if not e.length:
                e.length = extract_length(ebody)
            sec.entries.append(e)
        if sec.entries:
            sections.append(sec)
    return sections


# ---------- motivation 専用パーサ ----------

def parse_motivation(text: str) -> list[Section]:
    sections: list[Section] = []
    for title, body in split_h2_sections(text):
        sec = Section(title=title)
        for level, header, ebody in split_entries(body):
            if level != "###":
                continue
            company_part = header.replace("⭐", "").strip()
            is_best = "⭐" in header
            company = company_part
            question = ""
            length = ""
            note = ""
            # メタ行: **出典**: submitted / X.md / **設問**: ... / **字数**: ...
            for line in ebody.splitlines():
                line = line.strip()
                if line.startswith("**出典**"):
                    val = line.split(":", 1)[1].strip() if ":" in line else ""
                    for tag in ("submitted", "draft"):
                        if tag in val:
                            note = tag
                            break
                elif line.startswith("**設問**"):
                    question = line.split(":", 1)[1].strip()
                elif line.startswith("**字数**"):
                    length = line.split(":", 1)[1].strip()
            sec.entries.append(
                Entry(company=company, question=question, body=clean_body(ebody),
                      length=length, is_best=is_best, note=note)
            )
        if sec.entries:
            sections.append(sec)
    return sections


# ---------- 本文整形 ----------

LENGTH_RE = re.compile(r"字数[:：]?\s*(\d+字[^\n]*)")


def extract_length(body: str) -> str:
    m = LENGTH_RE.search(body)
    return m.group(1) if m else ""


def clean_body(body: str) -> str:
    """メタ行・selectionRationale行を取り除き、本文だけ残す。"""
    lines = []
    skip_meta = True
    for line in body.splitlines():
        s = line.strip()
        if skip_meta and (s.startswith("**") or s.startswith(">") or s.startswith("字数") or s == ""):
            continue
        skip_meta = False
        if s.startswith("---"):
            break
        lines.append(line)
    out = "\n".join(lines).strip()
    # 末尾の「→ ...参照」行除去
    out = re.sub(r"\n→\s+.+$", "", out, flags=re.MULTILINE)
    return out.strip()


# ---------- 統計 ----------

def summarize(secs_by_tab: dict[str, list[Section]]) -> dict[str, int]:
    out = {}
    for k, secs in secs_by_tab.items():
        n = sum(len(s.entries) for s in secs)
        out[k] = n
    return out


# ---------- レンダリング ----------

def render_card(e: Entry) -> str:
    badges = []
    if e.is_best:
        badges.append('<span class="b best">⭐ Best</span>')
    if e.note:
        badges.append(f'<span class="b note">{html.escape(e.note)}</span>')
    if e.length:
        badges.append(f'<span class="b len">{html.escape(e.length)}</span>')
    badges_html = "".join(badges)
    body_html = html.escape(e.body).replace("\n", "<br>")
    q = html.escape(e.question) if e.question else ""
    q_html = f'<div class="q">{q}</div>' if q else ""
    return f"""
<article class="card{' is-best' if e.is_best else ''}" data-company="{html.escape(e.company)}">
  <header>
    <div class="co">{html.escape(e.company)}</div>
    <div class="badges">{badges_html}</div>
  </header>
  {q_html}
  <div class="body">{body_html}</div>
</article>
""".strip()


def render_section(sec: Section) -> str:
    cards = "\n".join(render_card(e) for e in sec.entries)
    return f"""
<section class="group">
  <h2>{html.escape(sec.title)} <span class="count">({len(sec.entries)})</span></h2>
  <div class="grid">{cards}</div>
</section>
""".strip()


def render_tab(key: str, label: str, sections: list[Section]) -> str:
    body = "\n".join(render_section(s) for s in sections)
    return f'<div class="tab-panel" data-tab="{key}">{body}</div>'


def render(secs_by_tab: dict[str, list[Section]]) -> str:
    summary = summarize(secs_by_tab)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    nav = "".join(
        f'<button class="tab-btn{" active" if i==0 else ""}" data-target="{key}">'
        f'{label} <span class="ct">{summary.get(key,0)}</span></button>'
        for i, (key, label, _) in enumerate(TABS)
    )

    panels = []
    for i, (key, label, _) in enumerate(TABS):
        secs = secs_by_tab.get(key, [])
        cls = "tab-panel" + (" active" if i == 0 else "")
        body = "\n".join(render_section(s) for s in secs)
        panels.append(f'<div class="{cls}" data-tab="{key}">{body}</div>')
    panels_html = "\n".join(panels)

    total = sum(summary.values())

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ES横断ビュー</title>
<style>
:root {{
  --bg: #0f1115;
  --panel: #161a22;
  --panel2: #1c212d;
  --border: #242935;
  --text: #e6e8eb;
  --muted: #8a93a6;
  --accent: #38bdf8;
  --best: #fbbf24;
  --best-bg: #2a1f00;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: -apple-system, "Hiragino Sans", "Yu Gothic", system-ui, sans-serif;
  margin: 0; padding: 24px;
  background: var(--bg); color: var(--text);
  font-size: 14px; line-height: 1.7;
}}
h1 {{ font-size: 22px; margin: 0 0 4px; }}
.meta {{ color: var(--muted); font-size: 12px; margin-bottom: 18px; }}
.controls {{
  display: flex; gap: 12px; align-items: center; margin-bottom: 14px; flex-wrap: wrap;
}}
.controls input {{
  background: var(--panel); border: 1px solid var(--border); color: var(--text);
  padding: 8px 12px; border-radius: 6px; min-width: 280px; font-size: 14px;
}}
.controls label {{
  display: inline-flex; align-items: center; gap: 6px; color: var(--muted); font-size: 13px;
}}
.tabs {{ display: flex; gap: 4px; margin-bottom: 14px; flex-wrap: wrap; }}
.tab-btn {{
  background: var(--panel); border: 1px solid var(--border); color: var(--muted);
  padding: 8px 14px; border-radius: 6px 6px 0 0; cursor: pointer; font-size: 13px;
  font-family: inherit;
}}
.tab-btn:hover {{ color: var(--text); }}
.tab-btn.active {{ background: var(--panel2); color: var(--text); border-bottom-color: var(--panel2); }}
.tab-btn .ct {{
  display: inline-block; background: var(--border); color: var(--muted);
  padding: 1px 6px; border-radius: 10px; margin-left: 6px; font-size: 11px;
}}
.tab-panel {{ display: none; }}
.tab-panel.active {{ display: block; }}
.group {{ margin-bottom: 32px; }}
.group h2 {{
  font-size: 15px; color: var(--accent); margin: 0 0 12px;
  padding-bottom: 6px; border-bottom: 1px solid var(--border);
}}
.group h2 .count {{ color: var(--muted); font-size: 12px; font-weight: 400; }}
.grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 12px;
}}
.card {{
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 8px; padding: 14px;
  display: flex; flex-direction: column;
}}
.card.is-best {{ border-color: var(--best); background: linear-gradient(180deg, var(--best-bg) 0%, var(--panel) 60%); }}
.card header {{
  display: flex; justify-content: space-between; align-items: flex-start;
  gap: 8px; margin-bottom: 8px;
}}
.card .co {{ font-weight: 600; font-size: 13px; }}
.card .badges {{ display: flex; gap: 4px; flex-wrap: wrap; justify-content: flex-end; }}
.b {{
  display: inline-block; padding: 2px 6px; border-radius: 4px;
  font-size: 10px; font-weight: 600;
}}
.b.best {{ background: var(--best); color: #2a1f00; }}
.b.note {{ background: var(--border); color: var(--muted); }}
.b.len {{ background: var(--accent); color: #002030; }}
.q {{ color: var(--muted); font-size: 11px; margin-bottom: 8px; line-height: 1.5; }}
.body {{ font-size: 13px; line-height: 1.75; white-space: pre-wrap; word-break: break-word; }}
.card.collapsed .body {{
  max-height: 4.5em; overflow: hidden;
  -webkit-mask-image: linear-gradient(180deg, #000 60%, transparent);
}}
.card.hidden {{ display: none; }}
</style>
</head>
<body>
<h1>ES横断ビュー</h1>
<div class="meta">生成: {now} / 対象: ES/部品/ / 総回答数: {total}</div>

<div class="tabs">{nav}</div>

<div class="controls">
  <input id="filter" type="text" placeholder="本文・会社名で絞り込み">
  <label><input type="checkbox" id="bestonly"> ⭐ ベストのみ</label>
  <label><input type="checkbox" id="collapse" checked> 折りたたみ表示</label>
</div>

{panels_html}

<script>
const tabs = document.querySelectorAll('.tab-btn');
const panels = document.querySelectorAll('.tab-panel');
tabs.forEach(t => t.addEventListener('click', () => {{
  tabs.forEach(x => x.classList.remove('active'));
  panels.forEach(x => x.classList.remove('active'));
  t.classList.add('active');
  document.querySelector(`.tab-panel[data-tab="${{t.dataset.target}}"]`).classList.add('active');
}}));

const filter = document.getElementById('filter');
const bestonly = document.getElementById('bestonly');
const collapse = document.getElementById('collapse');
const cards = document.querySelectorAll('.card');

function applyFilter() {{
  const q = filter.value.trim().toLowerCase();
  const bo = bestonly.checked;
  cards.forEach(c => {{
    const text = c.textContent.toLowerCase();
    const matchQ = !q || text.includes(q);
    const matchB = !bo || c.classList.contains('is-best');
    c.classList.toggle('hidden', !(matchQ && matchB));
  }});
}}
function applyCollapse() {{
  cards.forEach(c => c.classList.toggle('collapsed', collapse.checked));
}}
filter.addEventListener('input', applyFilter);
bestonly.addEventListener('change', applyFilter);
collapse.addEventListener('change', applyCollapse);
cards.forEach(c => c.addEventListener('click', e => {{
  if (e.target.closest('.body, .q')) {{
    c.classList.toggle('collapsed');
  }}
}}));
applyCollapse();
</script>
</body>
</html>
"""


def main() -> int:
    if not PARTS_DIR.is_dir():
        print(f"ERROR: not found: {PARTS_DIR}", file=sys.stderr)
        return 1
    secs_by_tab: dict[str, list[Section]] = {}
    for key, label, fname in TABS:
        path = PARTS_DIR / fname
        if not path.exists():
            secs_by_tab[key] = []
            continue
        text = read(path)
        if key == "motivation":
            secs_by_tab[key] = parse_motivation(text)
        else:
            secs_by_tab[key] = parse_grouped_file(text)
    OUTPUT.write_text(render(secs_by_tab), encoding="utf-8")
    counts = ", ".join(f"{k}={sum(len(s.entries) for s in secs_by_tab[k])}" for k, _, _ in TABS)
    print(f"wrote {OUTPUT} ({counts})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
