#!/usr/bin/env python3
"""
企業調査品質チェッカー
対象: company-info/<企業名>/research_brief.md
実行: python tools/checks/research_checker.py <company_name>
       python tools/checks/research_checker.py --all  (全企業をチェック)
"""

import sys
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CheckResult:
    level: str  # ERROR / WARNING / INFO
    check_name: str
    message: str


RESEARCH_BRIEF_AXES = {
    '軸1': ['設立', '創業', '従業員', '事業規模', 'グループ'],
    '軸2': ['事業内容', '主力事業', '収益', 'セグメント', '売上'],
    '軸3': ['競合', '比較', '差別化', 'ポジション', '強み'],
    '軸4': ['中期経営計画', '中計', 'IR', '業績', '財務'],
    '軸5': ['採用', '求める人材', '選考', 'コース'],
    '軸6': ['キャリア', '研修', '異動', '昇進', '成長'],
    '軸7': ['戦略', 'DX', '注力', '社風', '文化', '働き方'],
    '軸8': ['ニュース', '提携', 'M&A', '最近', '直近'],
    '軸9': ['なぜ', '差別化', '志望理由', '他社との違い', '選んだ理由'],
}

REQUIRED_SECTIONS = [
    ('競合比較', r'(?:競合|比較|他社|ライバル)', "WARNING", "競合比較セクションが見つかりません。「なぜ競合ではないか」説明に必要です"),
    ('IR/中計情報', r'(?:中期経営計画|中計|IR|業績推移|財務)', "WARNING", "IR・中計情報が見つかりません。企業の将来方針理解に必要です"),
    ('採用情報', r'(?:採用|求める人材|求める力|欲しい人材)', "WARNING", "採用情報が見つかりません。自己PR・ガクチカとの対応付けに必要です"),
    ('キャリアパス', r'(?:キャリア|成長|昇進|異動|研修)', "WARNING", "キャリアパス情報が見つかりません。将来ビジョンの回答に必要です"),
]


def check_axis_coverage(content: str) -> List[CheckResult]:
    """research_briefの軸カバレッジチェック"""
    results = []

    for axis, keywords in RESEARCH_BRIEF_AXES.items():
        found = any(kw in content for kw in keywords)
        if not found:
            results.append(CheckResult(
                level="WARNING",
                check_name="axis_coverage",
                message=f"{axis} の情報が不足しています（キーワード: {', '.join(keywords[:3])}）"
            ))

    return results


def check_required_sections(content: str) -> List[CheckResult]:
    """必須セクションの有無チェック"""
    results = []

    for section_name, pattern, level, message in REQUIRED_SECTIONS:
        if not re.search(pattern, content):
            results.append(CheckResult(
                level=level,
                check_name="required_section",
                message=message
            ))

    return results


def check_source_citations(content: str) -> List[CheckResult]:
    """出典記載の有無チェック"""
    results = []

    # URLや「〇〇より」などの出典表記を確認
    has_url = bool(re.search(r'https?://', content))
    has_source = bool(re.search(r'(?:出典|参考|より|出所|Source)', content))

    if not has_url and not has_source:
        results.append(CheckResult(
            level="INFO",
            check_name="source_citation",
            message="出典・参考URLが記載されていません。情報の鮮度確認が難しくなります"
        ))

    return results


def check_company_name_consistency(content: str, company_name: str) -> List[CheckResult]:
    """企業名表記ゆれチェック"""
    results = []

    # 文中での企業名言及を確認
    if company_name and company_name not in content:
        # ファイルに企業名の言及が少ない場合
        results.append(CheckResult(
            level="INFO",
            check_name="company_name",
            message=f"企業名「{company_name}」の明示的な記載が少ない可能性があります"
        ))

    return results


def check_job_type_notes(content: str) -> List[CheckResult]:
    """職種メモの有無チェック"""
    results = []

    job_type_keywords = ['職種', 'コース', '総合職', '専門職', '部門', '配属']
    has_job_type = any(kw in content for kw in job_type_keywords)

    if not has_job_type:
        results.append(CheckResult(
            level="WARNING",
            check_name="job_type_notes",
            message="職種・コースに関する記載が見つかりません。志望職種への適合度確認に必要です"
        ))

    return results


def check_content_recency(content: str) -> List[CheckResult]:
    """情報の鮮度チェック（古い年度の言及）"""
    results = []

    # 2023年以前の中計・業績言及を検出
    old_year_pattern = re.compile(r'20(?:1[0-9]|2[0-2])年')
    old_mentions = old_year_pattern.findall(content)

    if len(old_mentions) > 2:
        results.append(CheckResult(
            level="WARNING",
            check_name="content_recency",
            message=f"古い年度への言及が多い({old_mentions[:3]})。最新情報への更新を確認してください"
        ))

    return results


def run_research_check(company_name: str, base_dir: str = "/Users/ishidatomonori/Desktop/knowledge") -> List[CheckResult]:
    """企業調査チェックを実行"""
    brief_path = Path(base_dir) / "company-info" / company_name / "research_brief.md"

    results = []

    if not brief_path.exists():
        return [CheckResult("ERROR", "file_not_found", f"research_brief.mdが見つかりません: {brief_path}")]

    content = brief_path.read_text(encoding='utf-8', errors='ignore')

    results.extend(check_axis_coverage(content))
    results.extend(check_required_sections(content))
    results.extend(check_source_citations(content))
    results.extend(check_company_name_consistency(content, company_name))
    results.extend(check_job_type_notes(content))
    results.extend(check_content_recency(content))

    return results


def format_output(results: List[CheckResult], company_name: str) -> str:
    """結果を整形"""
    if not results:
        return f"✅ {company_name}: 調査チェック問題なし"

    lines = [f"📊 企業調査チェック結果: {company_name}"]
    lines.append("=" * 60)

    errors = [r for r in results if r.level == "ERROR"]
    warnings = [r for r in results if r.level == "WARNING"]
    infos = [r for r in results if r.level == "INFO"]

    if errors:
        lines.append(f"\n❌ ERROR ({len(errors)}件):")
        for r in errors:
            lines.append(f"  [{r.check_name}] {r.message}")

    if warnings:
        lines.append(f"\n⚠️  WARNING ({len(warnings)}件):")
        for r in warnings:
            lines.append(f"  [{r.check_name}] {r.message}")

    if infos:
        lines.append(f"\nℹ️  INFO ({len(infos)}件):")
        for r in infos:
            lines.append(f"  [{r.check_name}] {r.message}")

    lines.append(f"\n合計: ERROR {len(errors)}件 / WARNING {len(warnings)}件")
    return '\n'.join(lines)


if __name__ == '__main__':
    base_dir = "/Users/ishidatomonori/Desktop/knowledge"

    if len(sys.argv) < 2:
        print("使用法:")
        print("  python tools/checks/research_checker.py <企業名>")
        print("  python tools/checks/research_checker.py --all")
        print("例: python tools/checks/research_checker.py 三菱UFJ銀行")
        sys.exit(1)

    if sys.argv[1] == '--all':
        company_dir = Path(base_dir) / "company-info"
        companies = [d.name for d in company_dir.iterdir() if d.is_dir()]

        total_errors = 0
        for company in sorted(companies):
            results = run_research_check(company, base_dir)
            print(format_output(results, company))
            print()
            total_errors += sum(1 for r in results if r.level == "ERROR")

        print(f"=== 全企業チェック完了: {len(companies)}社 ===")
        sys.exit(1 if total_errors > 0 else 0)
    else:
        company_name = sys.argv[1]
        results = run_research_check(company_name, base_dir)
        print(format_output(results, company_name))
        sys.exit(1 if any(r.level == "ERROR" for r in results) else 0)
