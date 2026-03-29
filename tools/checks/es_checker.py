#!/usr/bin/env python3
"""
ES (Entry Sheet) 品質チェッカー
対象: ES/ および 移行後ES/ 以下のMarkdownファイル
実行: python tools/checks/es_checker.py <filepath>
"""

import sys
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


@dataclass
class CheckResult:
    level: str  # ERROR / WARNING / INFO
    check_name: str
    message: str
    line_no: int = 0


def check_char_count(content: str, questions: List[dict]) -> List[CheckResult]:
    """文字数チェック: 設問ごとの字数上限・下限確認"""
    results = []
    # 設問パターン: 「Q:」「設問」「【】」などで始まる行
    q_pattern = re.compile(r'^(?:Q[:：]|設問|【.+?】|\d+[\.．）])\s*(.+)', re.MULTILINE)
    char_limit_pattern = re.compile(r'(\d+)字(?:以内|まで|程度)')

    for match in q_pattern.finditer(content):
        line = match.group(0)
        limit_match = char_limit_pattern.search(line)
        if limit_match:
            limit = int(limit_match.group(1))
            # 次の設問までのテキストを抽出（簡易版）
            start = match.end()
            # 実際のコンテンツ計測はファイル構造に依存するため警告のみ
            results.append(CheckResult(
                level="INFO",
                check_name="char_count",
                message=f"字数制限 {limit}字 を検出。実際の字数を確認してください。",
                line_no=content[:match.start()].count('\n') + 1
            ))
    return results


def check_forbidden_expressions(content: str) -> List[CheckResult]:
    """禁止表現チェック"""
    results = []

    forbidden = [
        (r'御社', "ERROR", "「御社」は口語。書き言葉では「貴社」「貴行」「貴グループ」を使うこと"),
        (r'思います(?:。|\s)', "WARNING", "「思います」は曖昧。「考えます」「確信しています」などに変更を検討"),
        (r'様々な', "WARNING", "「様々な」は曖昧。具体的に何種類・何件かを数字で示すこと"),
        (r'多くの', "WARNING", "「多くの」は曖昧。具体的な数を示すこと"),
        (r'積極的に', "WARNING", "「積極的に」は空語。具体的な行動（週次・月次・○回等）に変換すること"),
        (r'主体的に', "WARNING", "「主体的に」は空語。何を自分から始めたか具体的に書くこと"),
        (r'頑張り(?:ます|ました)', "WARNING", "「頑張る」は抽象的。具体的な行動・目標に変換すること"),
        (r'貢献(?:し|する|できる)', "WARNING", "「貢献する」は抽象的。具体的にどう貢献するか記述すること"),
        (r'(?:を通じて|を通して).{0,10}(?:を通じて|を通して)', "WARNING", "「〜を通じて」が短区間内に重複しています"),
    ]

    lines = content.split('\n')
    for line_no, line in enumerate(lines, 1):
        for pattern, level, message in forbidden:
            if re.search(pattern, line):
                results.append(CheckResult(
                    level=level,
                    check_name="forbidden_expression",
                    message=f"{message} (行 {line_no}: {line.strip()[:50]}...)" if len(line) > 50 else f"{message} (行 {line_no}: {line.strip()})",
                    line_no=line_no
                ))
    return results


def check_company_name_consistency(content: str, filepath: str) -> List[CheckResult]:
    """企業名表記ゆれチェック"""
    results = []

    # ファイル名から企業名を推定
    stem = Path(filepath).stem

    # 一般的な表記ゆれパターン
    variants_map = {
        '三菱UFJ': ['三菱ＵＦＪ', '三菱uFJ', 'MUFG', '三菱UFJ銀行', '三菱ＵＦＪ銀行'],
        'みずほ': ['Mizuho', 'みずほフィナンシャルグループ', 'みずほFG', 'みずほ銀行'],
        '三井住友': ['SMBC', '三井住友銀行', '三井住友フィナンシャルグループ', '三井住友FG'],
        '野村': ['野村証券', '野村HD', '野村ホールディングス'],
    }

    for base_name, variants in variants_map.items():
        found_variants = []
        for v in variants:
            if v in content and v != base_name:
                found_variants.append(v)
        if len(found_variants) > 1:
            results.append(CheckResult(
                level="WARNING",
                check_name="company_name_consistency",
                message=f"企業名の表記ゆれ検出: {found_variants} → 表記を統一してください"
            ))

    # 「貴行」「貴社」の混在チェック
    has_kisha = '貴社' in content
    has_kikou = '貴行' in content
    has_kigroup = '貴グループ' in content

    count = sum([has_kisha, has_kikou, has_kigroup])
    if count > 1:
        used = []
        if has_kisha: used.append('貴社')
        if has_kikou: used.append('貴行')
        if has_kigroup: used.append('貴グループ')
        results.append(CheckResult(
            level="ERROR",
            check_name="honorific_consistency",
            message=f"敬称の混在: {used} が混在しています。企業の業態に合わせて統一してください（銀行→貴行、証券/AM→貴社等）"
        ))

    return results


def check_unanswered_questions(content: str) -> List[CheckResult]:
    """設問未回答警告"""
    results = []

    # 設問後に内容が極端に少ない（100字未満）場合を検出
    # 簡易実装: [TODO]や「（記入予定）」「作成中」を検出
    todo_patterns = [
        r'\[TODO\]',
        r'（記入予定）',
        r'（作成中）',
        r'TBD',
        r'未記入',
        r'←.*書く',
    ]

    lines = content.split('\n')
    for line_no, line in enumerate(lines, 1):
        for pattern in todo_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                results.append(CheckResult(
                    level="ERROR",
                    check_name="unanswered_question",
                    message=f"未記入の設問が疑われます (行 {line_no}: {line.strip()})",
                    line_no=line_no
                ))

    return results


def check_duplicate_expressions(content: str) -> List[CheckResult]:
    """同一ファイル内の重複表現検出"""
    results = []

    # 4字以上の同一フレーズが3回以上出現する場合を検出
    # 日本語の連続4文字以上
    phrases = re.findall(r'[\u3040-\u9FFF]{4,}', content)
    phrase_count = {}
    for p in phrases:
        phrase_count[p] = phrase_count.get(p, 0) + 1

    threshold = 3
    for phrase, count in phrase_count.items():
        if count >= threshold and len(phrase) >= 6:  # 6字以上に絞る（短すぎる一般語を除外）
            results.append(CheckResult(
                level="WARNING",
                check_name="duplicate_expression",
                message=f"「{phrase}」が {count}回 出現しています。表現の多様化を検討してください"
            ))

    return results


def check_technical_terms(content: str) -> List[CheckResult]:
    """技術用語過多警告"""
    results = []

    tech_terms = [
        'アジャイル', 'スクラム', 'デプロイ', 'インフラ', 'クラウド', 'API',
        'KPI', 'OKR', 'SaaS', 'PaaS', 'DX推進', 'AI活用', 'データドリブン',
        'ピボット', 'アーキテクチャ', 'フレームワーク', 'スタック', 'バックログ',
        'バリューチェーン', 'エコシステム', 'プラットフォーム戦略',
        'AUM', 'NAV', 'ベンチマーク', 'アクティブ運用', 'パッシブ運用',
        'デュレーション', 'イールドカーブ', 'クレジットスプレッド',
    ]

    found_terms = []
    for term in tech_terms:
        if term in content:
            found_terms.append(term)

    if len(found_terms) >= 5:
        results.append(CheckResult(
            level="WARNING",
            check_name="technical_terms",
            message=f"技術用語が多い可能性があります ({len(found_terms)}語): {', '.join(found_terms[:5])}{'...' if len(found_terms) > 5 else ''}。文系面接官向けに言い換えを検討してください"
        ))

    return results


def check_abstract_words(content: str) -> List[CheckResult]:
    """抽象語過多警告"""
    results = []

    abstract_words = [
        '様々', '多様', '幅広い', '積極的', '主体的', '自発的',
        '柔軟に', '臨機応変', '課題解決', '貢献', '活躍', '成長',
        'チャレンジ', '挑戦', 'グローバル', 'イノベーション',
        '社会貢献', 'お客様のために', 'より良い',
    ]

    found = []
    for word in abstract_words:
        count = content.count(word)
        if count >= 2:
            found.append(f"{word}({count}回)")

    if len(found) >= 4:
        results.append(CheckResult(
            level="WARNING",
            check_name="abstract_words",
            message=f"抽象語が多い可能性があります: {', '.join(found[:4])}{'...' if len(found) > 4 else ''}。具体的な行動・数字・エピソードに変換してください"
        ))

    return results


def check_numbers(content: str) -> List[CheckResult]:
    """数字不足警告"""
    results = []

    # 数字（算用数字・漢数字）の出現数を確認
    num_pattern = re.compile(r'[0-9０-９]+|[一二三四五六七八九十百千万億]+(?:人|件|社|回|%|％|円|名|年|ヶ月|ヵ月)')
    numbers = num_pattern.findall(content)

    # ESの本文が500字以上あるのに数字が3個未満の場合
    # (ヘッダー・メタデータを除いた本文推定)
    body_length = len(re.sub(r'^#.*$', '', content, flags=re.MULTILINE))

    if body_length > 500 and len(numbers) < 3:
        results.append(CheckResult(
            level="WARNING",
            check_name="number_shortage",
            message=f"数字の使用が少ない可能性があります（検出: {len(numbers)}個）。人数・件数・達成率・期間など定量的表現を追加してください"
        ))

    return results


def run_all_checks(filepath: str) -> List[CheckResult]:
    """全チェックを実行"""
    path = Path(filepath)
    if not path.exists():
        return [CheckResult("ERROR", "file_not_found", f"ファイルが見つかりません: {filepath}")]

    if path.suffix.lower() not in ['.md', '.txt']:
        return [CheckResult("INFO", "skip", f"チェック対象外のファイル形式: {path.suffix}")]

    content = path.read_text(encoding='utf-8', errors='ignore')

    results = []
    results.extend(check_forbidden_expressions(content))
    results.extend(check_company_name_consistency(content, filepath))
    results.extend(check_unanswered_questions(content))
    results.extend(check_duplicate_expressions(content))
    results.extend(check_technical_terms(content))
    results.extend(check_abstract_words(content))
    results.extend(check_numbers(content))

    return results


def format_output(results: List[CheckResult], filepath: str) -> str:
    """結果を整形して出力"""
    if not results:
        return f"✅ {filepath}: チェック問題なし"

    lines = [f"📋 ESチェック結果: {filepath}"]
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
    if len(sys.argv) < 2:
        print("使用法: python tools/checks/es_checker.py <ESファイルパス>")
        print("例: python tools/checks/es_checker.py 移行後ES/三菱UFJ銀行.md")
        sys.exit(1)

    filepath = sys.argv[1]
    results = run_all_checks(filepath)
    print(format_output(results, filepath))

    # ERRORがあれば終了コード1
    if any(r.level == "ERROR" for r in results):
        sys.exit(1)
