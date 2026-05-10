#!/usr/bin/env python3
"""
自己分析タイムライン HTML 生成。

ES/素材/*.md の本文から「時期」と「テーマ軸」を自動推論し、
SVGの時系列レーン図 + エピソードカード一覧を1HTMLで出力。
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOZAI_DIR = ROOT / "ES" / "素材"
OUTPUT = Path(__file__).resolve().parent / "timeline.html"

# 出生年（学年→年齢のために）。2025年4月時点で大学3年と仮定 → 2003年生まれ。
# キーワードで期間（年）を推論する辞書。返り値: (start_year, end_year)
PERIOD_KEYWORDS: list[tuple[str, tuple[int, int]]] = [
    ("小学2年", (2010, 2010)),
    ("小学", (2009, 2014)),
    ("中学2年", (2016, 2016)),
    ("中学3年", (2017, 2017)),
    ("中学時代", (2015, 2017)),
    ("中学バスケ", (2015, 2017)),
    ("中学文化祭", (2016, 2016)),
    ("中学", (2015, 2017)),
    ("高校3年", (2020, 2020)),
    ("高校時代", (2018, 2020)),
    ("高校日本史", (2018, 2020)),
    ("高校", (2018, 2020)),
    ("大学1年", (2021, 2021)),
    ("大学2年", (2022, 2022)),
    ("大学3年", (2023, 2023)),
    ("大学4年", (2024, 2024)),
    ("卒論", (2024, 2025)),
    ("卒業論文", (2024, 2025)),
    ("ゼミ", (2023, 2025)),
    ("計量経済学", (2023, 2025)),
    ("長期インターン", (2024, 2026)),
    ("インターン", (2024, 2026)),
    ("塾講師", (2022, 2024)),
    ("塾バイト", (2022, 2024)),
    ("バイトリーダー", (2022, 2024)),
    ("OC", (2023, 2024)),
    ("オープンキャンパス", (2023, 2024)),
    ("バスケ部", (2015, 2017)),
    ("東海道", (2010, 2013)),
    ("Claude Code", (2025, 2026)),
    ("TODO管理", (2025, 2026)),
    ("生成AI", (2024, 2026)),
    ("Snowflake", (2024, 2026)),
    ("BigQuery", (2024, 2026)),
    ("OS 2.0", (2025, 2026)),
    ("DX", (2025, 2026)),
    ("ステーブルコイン", (2025, 2026)),
    ("AM", (2025, 2026)),
]

# テーマ軸（レーン）。category と本文キーワードから複数タグを付与。
THEME_KEYWORDS: dict[str, list[str]] = {
    "リーダーシップ": ["リーダー", "チーフ", "バイトリーダー", "マネジ", "権限委譲", "巻き込"],
    "型化・仕組み化": ["型化", "仕組み化", "標準化", "属人化", "再現性", "自動化", "フォーマット"],
    "データ・分析": ["データ", "分析", "因果", "計量", "POS", "Python", "SQL", "BigQuery", "Snowflake"],
    "技術・AI": ["AI", "API", "Claude", "Notebook", "クラウド", "OpenAI", "生成AI", "エンジニアリング"],
    "失敗・成長": ["失敗", "挫折", "反省", "苦労", "課題", "学び", "成長"],
    "リスク・守備": ["リスク", "守備", "ディフェンス", "受託者", "Failure", "綻び", "セキュリティ"],
    "思想・設計": ["設計", "思想", "哲学", "ビジョン", "OS", "Mission", "原理"],
    "対人・チーム": ["対人", "チーム", "コミュニケーション", "合意", "信頼", "関係"],
    "学業・専門性": ["学業", "ゼミ", "卒論", "資格", "統計", "10-K", "財務分析"],
    "リサーチ": ["リサーチ", "調査", "一次情報", "深掘り"],
}

CATEGORY_DEFAULT_THEMES: dict[str, list[str]] = {
    "自己分析": ["思想・設計"],
    "インターン": ["型化・仕組み化", "技術・AI"],
    "バイト": ["リーダーシップ", "対人・チーム"],
    "課外活動": ["リーダーシップ"],
    "学業": ["学業・専門性"],
    "GD記録": ["対人・チーム"],
    "参考": ["思想・設計"],
}

CATEGORY_COLOR: dict[str, str] = {
    "自己分析": "#a78bfa",
    "インターン": "#38bdf8",
    "バイト": "#34d399",
    "課外活動": "#fbbf24",
    "学業": "#f472b6",
    "GD記録": "#facc15",
    "参考": "#94a3b8",
}

THEME_ORDER = list(THEME_KEYWORDS.keys())


@dataclass
class Episode:
    num: str
    filename: str
    title: str
    category: str
    summary: str
    start_year: int = 0
    end_year: int = 0
    themes: list[str] = field(default_factory=list)
    inferred: bool = False  # 推論で year を埋めたか


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def extract_summary(text: str) -> str:
    """## 概要 直後の段落 (最大400字) を抽出。"""
    m = re.search(r"##\s*概要\s*\n+([^\n][^\n]*(?:\n[^\n#][^\n]*)*)", text)
    if m:
        return m.group(1).strip()[:400]
    # fallback: frontmatter後の最初のH1の次の段落
    m2 = re.search(r"\n#\s+[^\n]+\n+([^\n#][^\n]+)", text)
    return m2.group(1).strip()[:400] if m2 else ""


def infer_period(text: str, category: str, title: str = "") -> tuple[int, int, bool]:
    """タイトル優先・概要補助で期間推論。"""
    # 1. タイトルにキーワードが含まれていれば、その範囲を最優先
    title_matched: list[tuple[int, int]] = []
    for kw, span in PERIOD_KEYWORDS:
        if kw in title:
            title_matched.append(span)
    if title_matched:
        s = min(a for a, _ in title_matched)
        e = max(b for _, b in title_matched)
        return s, e, True
    # 2. 概要マッチ（過去エピソードへの参照を含むため範囲が広がるリスクあり）
    matched: list[tuple[int, int]] = []
    for kw, span in PERIOD_KEYWORDS:
        if kw in text:
            matched.append(span)
    if matched:
        s = min(a for a, _ in matched)
        e = max(b for _, b in matched)
        return s, e, True
    # 全くヒットしない場合のカテゴリ別フォールバック
    fallback = {
        "自己分析": (2025, 2026),
        "インターン": (2024, 2026),
        "バイト": (2022, 2024),
        "課外活動": (2018, 2024),
        "学業": (2023, 2025),
        "GD記録": (2025, 2026),
        "参考": (2025, 2026),
    }
    s, e = fallback.get(category, (2024, 2026))
    return s, e, True


def infer_themes(text: str, category: str) -> list[str]:
    found: list[str] = []
    for theme, kws in THEME_KEYWORDS.items():
        if any(k in text for k in kws):
            found.append(theme)
    # categoryデフォルトを補完
    for d in CATEGORY_DEFAULT_THEMES.get(category, []):
        if d not in found:
            found.append(d)
    return found or ["思想・設計"]


def load_episodes() -> list[Episode]:
    eps: list[Episode] = []
    for f in sorted(SOZAI_DIR.glob("*.md")):
        if f.name == "INDEX.md":
            continue
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        # frontmatter崩れに備えてファイル名からのフォールバック
        name_parts = f.stem.split("_", 2)  # ['04', 'インターン', '分析設計と...']
        fallback_cat = name_parts[1] if len(name_parts) >= 2 else "?"
        fallback_title = name_parts[2].replace("_", " ") if len(name_parts) >= 3 else f.stem
        title = fm.get("title", fallback_title)
        category = fm.get("category", fallback_cat)
        summary = extract_summary(text)
        m = re.match(r"(\d+)_", f.name)
        num = m.group(1) if m else ""
        # period 推論: タイトル優先 → 概要補助
        start, end, inferred = infer_period(summary, category, title)
        themes = infer_themes(text, category)
        eps.append(Episode(
            num=num, filename=f.name, title=title, category=category,
            summary=summary, start_year=start, end_year=end,
            themes=themes, inferred=inferred,
        ))
    return eps


# ---------- SVG レンダリング ----------

def render_svg(eps: list[Episode]) -> str:
    """X=年, Y=テーマレーン。エピソードを期間バーで描画。"""
    if not eps:
        return ""
    year_min = min(e.start_year for e in eps)
    year_max = max(e.end_year for e in eps)
    # 余白ある描画
    pad_left = 140
    pad_right = 30
    pad_top = 40
    row_h = 38
    n_rows = len(THEME_ORDER)
    bar_h = 16

    width = 1400
    height = pad_top + row_h * n_rows + 30

    plot_w = width - pad_left - pad_right

    def x_of(year: int, half: float = 0.0) -> float:
        # year+halfの位置 (half=0.5でその年の中央)
        span = max(year_max - year_min, 1)
        return pad_left + ((year + half - year_min) / span) * plot_w

    def y_of(theme: str, sub_offset: float = 0.0) -> float:
        idx = THEME_ORDER.index(theme) if theme in THEME_ORDER else 0
        return pad_top + idx * row_h + row_h / 2 + sub_offset

    parts: list[str] = []
    parts.append(f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" class="tl">')

    # X grid (年)
    for y in range(year_min, year_max + 2):
        x = x_of(y)
        parts.append(
            f'<line x1="{x:.1f}" y1="{pad_top - 8}" x2="{x:.1f}" y2="{height - 20}" '
            f'stroke="#242935" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{height - 6}" fill="#8a93a6" font-size="10" '
            f'text-anchor="middle">{y}</text>'
        )

    # Y lane labels + 帯
    for i, theme in enumerate(THEME_ORDER):
        y = pad_top + i * row_h
        parts.append(
            f'<rect x="0" y="{y:.1f}" width="{width}" height="{row_h}" '
            f'fill="{"#13171f" if i % 2 == 0 else "#161a22"}"/>'
        )
        parts.append(
            f'<text x="{pad_left - 10}" y="{y + row_h / 2 + 3:.1f}" fill="#e6e8eb" '
            f'font-size="11" text-anchor="end">{html.escape(theme)}</text>'
        )

    # 各エピソードを各テーマレーンにバー描画
    # 同一エピソードが複数レーンに登場する＝マルチタグ
    for ep in eps:
        color = CATEGORY_COLOR.get(ep.category, "#94a3b8")
        x1 = x_of(ep.start_year)
        x2 = x_of(ep.end_year, 1.0)
        bw = max(x2 - x1, 4)
        for theme in ep.themes:
            if theme not in THEME_ORDER:
                continue
            y = y_of(theme) - bar_h / 2
            tooltip = f"#{ep.num} {ep.title} ({ep.start_year}-{ep.end_year})"
            parts.append(
                f'<g class="ep" data-num="{ep.num}">'
                f'<rect x="{x1:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bar_h}" '
                f'rx="3" fill="{color}" fill-opacity="0.75" stroke="{color}" stroke-width="1">'
                f'<title>{html.escape(tooltip)}</title></rect>'
                f'<text x="{x1 + 4:.1f}" y="{y + 12:.1f}" fill="#0f1115" font-size="9" '
                f'font-weight="600">#{ep.num}</text>'
                f'</g>'
            )

    parts.append("</svg>")
    return "".join(parts)


def render_legend() -> str:
    items = "".join(
        f'<span class="lg-item"><span class="sw" style="background:{c}"></span>{html.escape(cat)}</span>'
        for cat, c in CATEGORY_COLOR.items()
    )
    return f'<div class="legend">{items}</div>'


def render_card(ep: Episode) -> str:
    themes_html = "".join(
        f'<span class="th">{html.escape(t)}</span>' for t in ep.themes
    )
    period = f"{ep.start_year}–{ep.end_year}" if ep.start_year != ep.end_year else f"{ep.start_year}"
    color = CATEGORY_COLOR.get(ep.category, "#94a3b8")
    summary = html.escape(ep.summary)
    rel = f"../../ES/素材/{ep.filename}"
    return f"""
<article class="card" data-num="{ep.num}" data-themes="{html.escape('|'.join(ep.themes))}" data-cat="{html.escape(ep.category)}">
  <header>
    <span class="cat" style="background:{color}">{html.escape(ep.category)}</span>
    <span class="num">#{ep.num}</span>
    <span class="period">{period}</span>
  </header>
  <h3>{html.escape(ep.title)}</h3>
  <div class="themes">{themes_html}</div>
  <div class="summary">{summary}</div>
  <a class="src" href="{html.escape(rel)}">→ 元ファイル</a>
</article>
""".strip()


def render(eps: list[Episode]) -> str:
    eps_sorted = sorted(eps, key=lambda e: (e.start_year, e.num))
    svg = render_svg(eps_sorted)
    cards = "\n".join(render_card(e) for e in eps_sorted)
    legend = render_legend()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    cat_counts: dict[str, int] = {}
    for e in eps_sorted:
        cat_counts[e.category] = cat_counts.get(e.category, 0) + 1
    summary_chips = " ".join(
        f'<span class="chip">{html.escape(c)} {n}</span>'
        for c, n in cat_counts.items()
    )

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>自己分析タイムライン</title>
<style>
:root {{
  --bg: #0f1115; --panel: #161a22; --border: #242935;
  --text: #e6e8eb; --muted: #8a93a6; --accent: #38bdf8;
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
.chips {{ margin-bottom: 14px; }}
.chip {{
  display: inline-block; background: var(--panel); border: 1px solid var(--border);
  padding: 3px 8px; border-radius: 10px; font-size: 11px; margin-right: 4px;
  color: var(--muted);
}}
.legend {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; font-size: 12px; }}
.lg-item {{ display: inline-flex; align-items: center; gap: 5px; color: var(--muted); }}
.sw {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
.tl-wrap {{
  background: var(--panel); border: 1px solid var(--border); border-radius: 8px;
  padding: 8px; margin-bottom: 18px; overflow-x: auto;
}}
.tl {{ display: block; min-width: 1000px; width: 100%; }}
.ep rect {{ cursor: pointer; transition: fill-opacity .15s; }}
.ep:hover rect {{ fill-opacity: 1; stroke-width: 2; }}
.controls {{ margin-bottom: 12px; display: flex; gap: 10px; flex-wrap: wrap; }}
.controls input {{
  background: var(--panel); border: 1px solid var(--border); color: var(--text);
  padding: 6px 10px; border-radius: 6px; min-width: 240px;
}}
.controls select {{
  background: var(--panel); border: 1px solid var(--border); color: var(--text);
  padding: 6px 10px; border-radius: 6px;
}}
.grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}}
.card {{
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 8px; padding: 12px; display: flex; flex-direction: column;
}}
.card.hl {{ outline: 2px solid var(--accent); }}
.card.hidden {{ display: none; }}
.card header {{
  display: flex; gap: 8px; align-items: center; margin-bottom: 8px;
  font-size: 11px;
}}
.cat {{ padding: 2px 6px; border-radius: 4px; color: #0f1115; font-weight: 600; }}
.num {{ color: var(--muted); }}
.period {{ margin-left: auto; color: var(--muted); }}
.card h3 {{ font-size: 14px; margin: 0 0 8px; line-height: 1.4; }}
.themes {{ display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 8px; }}
.th {{
  background: var(--border); color: var(--muted);
  padding: 1px 6px; border-radius: 3px; font-size: 10px;
}}
.summary {{ font-size: 12px; color: #cbd5e1; line-height: 1.65; flex: 1; }}
.src {{ font-size: 11px; color: var(--accent); margin-top: 8px; text-decoration: none; }}
.src:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<h1>自己分析タイムライン</h1>
<div class="meta">生成: {now} / 対象: ES/素材/ ({len(eps_sorted)}件) / 期間データは本文キーワードから自動推論</div>

<div class="chips">{summary_chips}</div>
{legend}

<div class="tl-wrap">{svg}</div>

<div class="controls">
  <input id="filter" type="text" placeholder="タイトル・本文・テーマで絞り込み">
  <select id="catfilter">
    <option value="">全カテゴリ</option>
    {"".join(f'<option value="{html.escape(c)}">{html.escape(c)}</option>' for c in CATEGORY_COLOR)}
  </select>
</div>

<div class="grid">{cards}</div>

<script>
const cards = document.querySelectorAll('.card');
const filter = document.getElementById('filter');
const catf = document.getElementById('catfilter');
function apply() {{
  const q = filter.value.trim().toLowerCase();
  const c = catf.value;
  cards.forEach(card => {{
    const text = card.textContent.toLowerCase();
    const cat = card.dataset.cat;
    const okQ = !q || text.includes(q);
    const okC = !c || cat === c;
    card.classList.toggle('hidden', !(okQ && okC));
  }});
}}
filter.addEventListener('input', apply);
catf.addEventListener('change', apply);

// SVG↔card hover連動
document.querySelectorAll('svg .ep').forEach(g => {{
  g.addEventListener('mouseenter', () => {{
    const num = g.dataset.num;
    document.querySelectorAll('.card').forEach(c =>
      c.classList.toggle('hl', c.dataset.num === num));
  }});
  g.addEventListener('mouseleave', () => {{
    document.querySelectorAll('.card.hl').forEach(c => c.classList.remove('hl'));
  }});
  g.addEventListener('click', () => {{
    const num = g.dataset.num;
    const card = document.querySelector(`.card[data-num="${{num}}"]`);
    if (card) card.scrollIntoView({{behavior: 'smooth', block: 'center'}});
  }});
}});
</script>
</body>
</html>
"""


def main() -> int:
    if not SOZAI_DIR.is_dir():
        print(f"ERROR: not found: {SOZAI_DIR}", file=sys.stderr)
        return 1
    eps = load_episodes()
    OUTPUT.write_text(render(eps), encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(eps)} episodes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
