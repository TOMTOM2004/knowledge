#!/usr/bin/env python3
"""
AM横断比較表 HTML 生成。

docs/am_competitor_comparison.md の Markdownテーブル群（A〜D群×28軸）を
sticky header/column・評価バッジ・出典折りたたみ・絞り込み付きの
単一HTMLに変換。
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "am_competitor_comparison.md"
OUTPUT = Path(__file__).resolve().parent / "am_comparison.html"

GROUP_RE = re.compile(r"^##\s+([A-D])群[:：]\s*(.+)$", re.MULTILINE)
TABLE_HEADER_RE = re.compile(r"^\|.+\|\s*$", re.MULTILINE)

EVAL_BADGE = {
    "◎": ("good", "◎"),
    "○": ("ok", "○"),
    "△": ("warn", "△"),
    "✗": ("bad", "✗"),
    "×": ("bad", "✗"),
}


@dataclass
class Row:
    axis_id: str           # "A-1"
    axis_name: str         # "顧客構成"
    cells: dict[str, str] = field(default_factory=dict)  # 会社名→内容
    eval: str = ""         # ◎ △ ✗
    source: str = ""


@dataclass
class Group:
    code: str  # "A"
    title: str
    rows: list[Row] = field(default_factory=list)


def parse_md_table(block: str) -> list[list[str]]:
    """Markdownテーブルブロック → 行ごとのセルリスト。"""
    rows: list[list[str]] = []
    for line in block.strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        # 区切り行 (|---|---|---|) はスキップ
        if re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def parse_axis(axis_cell: str) -> tuple[str, str]:
    """「A-1 顧客構成」→ ("A-1", "顧客構成")。"""
    m = re.match(r"^([A-D]-\d+[a-z]?)\s+(.+)$", axis_cell.strip())
    if m:
        return m.group(1), m.group(2)
    return "", axis_cell.strip()


def parse_groups(text: str) -> list[Group]:
    """## A群: ... の塊ごとに直後のテーブルを抽出。"""
    groups: list[Group] = []
    matches = list(GROUP_RE.finditer(text))
    for i, m in enumerate(matches):
        code = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        # テーブル行（|で始まる連続行）を抽出
        table_lines: list[str] = []
        in_table = False
        for line in block.splitlines():
            if line.strip().startswith("|"):
                table_lines.append(line)
                in_table = True
            elif in_table and not line.strip().startswith("|"):
                # 最初のテーブル終端でbreak（同セクションに複数テーブルがあれば最初のみ）
                break
        rows_raw = parse_md_table("\n".join(table_lines))
        if len(rows_raw) < 2:
            continue
        header = rows_raw[0]  # ['軸', 'MYAM', '評価', '出典']
        company_cols = header[1:-2]  # 中間列が会社名
        g = Group(code=code, title=title)
        for r in rows_raw[1:]:
            if len(r) < 4:
                continue
            axis_id, axis_name = parse_axis(r[0])
            row = Row(axis_id=axis_id, axis_name=axis_name)
            for col_name, val in zip(company_cols, r[1:-2]):
                row.cells[col_name] = val
            row.eval = strip_md_bold(r[-2]).strip()
            row.source = r[-1].strip()
            g.rows.append(row)
        groups.append(g)
    return groups


def strip_md_bold(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


def md_inline_to_html(text: str) -> str:
    """太字・改行のみ変換（escape済み入力前提）。"""
    # **bold** → <strong>
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # `code` → <code>
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    return text


def render_eval(e: str) -> str:
    e_clean = e.strip()
    if e_clean in EVAL_BADGE:
        cls, sym = EVAL_BADGE[e_clean]
        return f'<span class="ev {cls}">{sym}</span>'
    return f'<span class="ev unk">{html.escape(e_clean) or "?"}</span>'


def render_cell(content: str) -> str:
    escaped = html.escape(content)
    return md_inline_to_html(escaped)


def render_source(src: str) -> str:
    if not src:
        return '<span class="src-empty">—</span>'
    escaped = html.escape(src)
    return f'<details class="src"><summary>出典</summary><div>{md_inline_to_html(escaped)}</div></details>'


def render_groups(groups: list[Group]) -> tuple[str, list[str]]:
    """テーブル本体HTML + 全社名リスト。"""
    # 全グループから会社列を集める
    companies: list[str] = []
    for g in groups:
        for r in g.rows:
            for c in r.cells.keys():
                if c not in companies:
                    companies.append(c)

    parts: list[str] = []
    for g in groups:
        rows_html = []
        for r in g.rows:
            cell_cells = "".join(
                f'<td class="content">{render_cell(r.cells.get(c, ""))}</td>'
                for c in companies
            )
            rows_html.append(
                f'<tr data-group="{g.code}" data-eval="{html.escape(r.eval)}" data-axis="{html.escape(r.axis_id)}">'
                f'<td class="axis"><span class="aid">{html.escape(r.axis_id)}</span> {html.escape(r.axis_name)}</td>'
                f'{cell_cells}'
                f'<td class="eval">{render_eval(r.eval)}</td>'
                f'<td class="src-cell">{render_source(r.source)}</td>'
                f'</tr>'
            )
        co_headers = "".join(f'<th class="co">{html.escape(c)}</th>' for c in companies)
        parts.append(f"""
<section class="grp" data-group="{g.code}">
  <h2>{g.code}群: {html.escape(g.title)} <span class="cnt">({len(g.rows)}軸)</span></h2>
  <div class="tw">
    <table>
      <thead>
        <tr>
          <th class="axis">軸</th>
          {co_headers}
          <th class="eval">評価</th>
          <th class="src-cell">出典</th>
        </tr>
      </thead>
      <tbody>{"".join(rows_html)}</tbody>
    </table>
  </div>
</section>
""".strip())
    return "\n".join(parts), companies


def render_summary(groups: list[Group]) -> str:
    """各群×評価の集計バッジ。"""
    out: list[str] = []
    total_g = total_w = total_b = 0
    for g in groups:
        good = sum(1 for r in g.rows if "◎" in r.eval)
        warn = sum(1 for r in g.rows if "△" in r.eval)
        bad = sum(1 for r in g.rows if "✗" in r.eval or "×" in r.eval)
        total_g += good
        total_w += warn
        total_b += bad
        out.append(
            f'<div class="stat">'
            f'<div class="k">{g.code}群</div>'
            f'<div class="v"><span class="ev good">◎{good}</span> '
            f'<span class="ev warn">△{warn}</span> '
            f'<span class="ev bad">✗{bad}</span></div>'
            f'</div>'
        )
    out.append(
        f'<div class="stat total">'
        f'<div class="k">合計</div>'
        f'<div class="v"><span class="ev good">◎{total_g}</span> '
        f'<span class="ev warn">△{total_w}</span> '
        f'<span class="ev bad">✗{total_b}</span></div>'
        f'</div>'
    )
    return "".join(out)


def render(text: str, groups: list[Group]) -> str:
    body, companies = render_groups(groups)
    summary = render_summary(groups)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_axes = sum(len(g.rows) for g in groups)

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AM横断比較表</title>
<style>
:root {{
  --bg: #0f1115; --panel: #161a22; --panel2: #1c212d;
  --border: #242935; --text: #e6e8eb; --muted: #8a93a6; --accent: #38bdf8;
  --good: #4ade80; --warn: #fbbf24; --bad: #f87171; --good-bg: #0f2a18;
  --warn-bg: #2a1f00; --bad-bg: #2e0e0e;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: -apple-system, "Hiragino Sans", "Yu Gothic", system-ui, sans-serif;
  margin: 0; padding: 24px;
  background: var(--bg); color: var(--text);
  font-size: 13px; line-height: 1.6;
}}
h1 {{ font-size: 22px; margin: 0 0 4px; }}
.meta {{ color: var(--muted); font-size: 12px; margin-bottom: 16px; }}
.stats {{ display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }}
.stat {{
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 14px; min-width: 80px;
}}
.stat.total {{ border-color: var(--accent); }}
.stat .k {{ font-size: 11px; color: var(--muted); }}
.stat .v {{ font-size: 14px; font-weight: 600; margin-top: 2px; }}
.controls {{ display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; align-items: center; }}
.controls input {{
  background: var(--panel); border: 1px solid var(--border); color: var(--text);
  padding: 7px 11px; border-radius: 6px; min-width: 260px; font-size: 13px;
}}
.controls .btn {{
  background: var(--panel); border: 1px solid var(--border); color: var(--muted);
  padding: 7px 12px; border-radius: 6px; cursor: pointer; font-family: inherit;
  font-size: 12px;
}}
.controls .btn.active {{ background: var(--panel2); color: var(--text); border-color: var(--accent); }}
.controls .btn:hover {{ color: var(--text); }}
.controls .lab {{ color: var(--muted); font-size: 12px; }}
.grp {{ margin-bottom: 28px; }}
.grp h2 {{
  font-size: 15px; color: var(--accent); margin: 0 0 8px;
  padding: 6px 10px; background: var(--panel); border-radius: 6px;
  border-left: 3px solid var(--accent); position: sticky; top: 0; z-index: 5;
}}
.grp h2 .cnt {{ color: var(--muted); font-size: 12px; font-weight: 400; }}
.tw {{ overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; }}
table {{
  width: 100%; min-width: 800px; border-collapse: separate; border-spacing: 0;
  background: var(--panel);
}}
thead th {{
  background: var(--panel2); color: var(--muted); font-weight: 500;
  padding: 8px 10px; text-align: left; font-size: 11px;
  position: sticky; top: 38px; z-index: 4;
  border-bottom: 1px solid var(--border);
}}
thead th.axis {{ left: 0; z-index: 6; min-width: 180px; max-width: 220px; background: var(--panel2); }}
thead th.co {{ min-width: 380px; }}
thead th.eval {{ min-width: 60px; text-align: center; }}
thead th.src-cell {{ min-width: 90px; }}
tbody td {{
  padding: 10px; vertical-align: top; border-bottom: 1px solid var(--border);
  font-size: 12.5px;
}}
tbody td.axis {{
  position: sticky; left: 0; background: var(--panel);
  font-weight: 500; min-width: 180px; max-width: 220px; z-index: 2;
  border-right: 1px solid var(--border);
}}
tbody td.axis .aid {{
  display: inline-block; background: var(--border); color: var(--muted);
  padding: 1px 5px; border-radius: 3px; font-size: 10px;
  font-family: ui-monospace, monospace; margin-right: 4px;
}}
tbody td.content {{ line-height: 1.7; }}
tbody td.content strong {{ color: var(--accent); }}
tbody td.eval {{ text-align: center; }}
tbody td.src-cell {{ font-size: 11px; }}
tbody tr:hover td {{ background: #1a2030; }}
tbody tr:hover td.axis {{ background: #1d2434; }}
tbody tr.hidden {{ display: none; }}
.ev {{
  display: inline-block; min-width: 22px; padding: 2px 6px;
  border-radius: 4px; font-weight: 700; font-size: 12px; text-align: center;
}}
.ev.good {{ background: var(--good-bg); color: var(--good); }}
.ev.warn {{ background: var(--warn-bg); color: var(--warn); }}
.ev.bad {{ background: var(--bad-bg); color: var(--bad); }}
.ev.unk {{ background: var(--border); color: var(--muted); }}
details.src summary {{
  cursor: pointer; color: var(--accent); font-size: 11px; list-style: none;
}}
details.src summary::-webkit-details-marker {{ display: none; }}
details.src summary::before {{ content: "▶ "; font-size: 9px; }}
details.src[open] summary::before {{ content: "▼ "; }}
details.src div {{
  margin-top: 6px; color: var(--muted); font-size: 11px; line-height: 1.55;
  word-break: break-all;
}}
.src-empty {{ color: var(--border); }}
code {{
  background: var(--panel2); color: var(--text);
  padding: 1px 4px; border-radius: 3px; font-size: 11px;
  font-family: ui-monospace, monospace;
}}
</style>
</head>
<body>
<h1>AM横断比較表</h1>
<div class="meta">生成: {now} / 対象: {SOURCE.relative_to(ROOT)} / {total_axes}軸 / 比較対象: {", ".join(html.escape(c) for c in companies) if companies else "（なし）"}</div>

<div class="stats">{summary}</div>

<div class="controls">
  <input id="filter" type="text" placeholder="軸名・内容で絞り込み">
  <span class="lab">評価:</span>
  <button class="btn ev-btn active" data-ev="">全て</button>
  <button class="btn ev-btn" data-ev="◎">◎ のみ</button>
  <button class="btn ev-btn" data-ev="△">△ のみ</button>
  <button class="btn ev-btn" data-ev="✗">✗ のみ</button>
  <span class="lab">群:</span>
  <button class="btn gr-btn active" data-gr="">全群</button>
  <button class="btn gr-btn" data-gr="A">A</button>
  <button class="btn gr-btn" data-gr="B">B</button>
  <button class="btn gr-btn" data-gr="C">C</button>
  <button class="btn gr-btn" data-gr="D">D</button>
</div>

{body}

<script>
const filter = document.getElementById('filter');
const evBtns = document.querySelectorAll('.ev-btn');
const grBtns = document.querySelectorAll('.gr-btn');
let curEv = '';
let curGr = '';

function apply() {{
  const q = filter.value.trim().toLowerCase();
  document.querySelectorAll('tbody tr').forEach(tr => {{
    const text = tr.textContent.toLowerCase();
    const ev = tr.dataset.eval || '';
    const gr = tr.dataset.group || '';
    const okQ = !q || text.includes(q);
    const okE = !curEv || ev.includes(curEv);
    const okG = !curGr || gr === curGr;
    tr.classList.toggle('hidden', !(okQ && okE && okG));
  }});
  document.querySelectorAll('.grp').forEach(s => {{
    const visible = s.querySelectorAll('tbody tr:not(.hidden)').length;
    s.style.display = (curGr && s.dataset.group !== curGr) ? 'none' : (visible === 0 ? 'none' : '');
  }});
}}

filter.addEventListener('input', apply);
evBtns.forEach(b => b.addEventListener('click', () => {{
  evBtns.forEach(x => x.classList.remove('active'));
  b.classList.add('active');
  curEv = b.dataset.ev;
  apply();
}}));
grBtns.forEach(b => b.addEventListener('click', () => {{
  grBtns.forEach(x => x.classList.remove('active'));
  b.classList.add('active');
  curGr = b.dataset.gr;
  apply();
}}));
</script>
</body>
</html>
"""


def main() -> int:
    if not SOURCE.exists():
        print(f"ERROR: not found: {SOURCE}", file=sys.stderr)
        return 1
    text = SOURCE.read_text(encoding="utf-8")
    groups = parse_groups(text)
    OUTPUT.write_text(render(text, groups), encoding="utf-8")
    counts = ", ".join(f"{g.code}={len(g.rows)}" for g in groups)
    print(f"wrote {OUTPUT} ({counts})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
