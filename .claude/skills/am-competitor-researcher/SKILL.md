---
name: am-competitor-researcher
description: >
  AM（アセットマネジメント）業界に特化した競合横断比較スキル。
  「AM各社を比較して」「AM競合調査をして」「AM横断比較表を作って」
  「〇〇と△△を比較して（AM文脈）」などの依頼で起動する。
  company-researcher が1社単位の調査であるのに対し、このスキルは
  複数AM企業を同一軸で横断比較し、差別化の構造を明らかにする。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_click
---

# AM Competitor Researcher

複数のAM企業を4群28軸で横断比較し、構造的な差別化ポイントを可視化する。
調査は◎/△/✗を追跡しながらループし、原理的限界まで情報を集め切ってから比較表を構築する。

## Phase 概要

| Phase | 内容 | 詳細 |
|-------|------|------|
| 1. 入力確認 + 初期収集 | 企業リスト確定、research_brief読込、ギャップマトリクスv0提示 | `references/execution-protocol.md#phase-1` |
| 2. Investigation Loop | ✗→◎ の調査ループ（Round 1: 一次ソース → Round 2: 二次+WebSearch → Round 3: クロス軸+フォールバック） | `references/execution-protocol.md#phase-2` |
| 3. 比較表構築 + Insight | 横断比較表生成、Insight Layer、品質チェック | `references/execution-protocol.md#phase-3` |
| 4. 保存 + 逆反映 | 承認後に保存、個別research_briefへの逆反映（任意） | `references/execution-protocol.md#phase-4` |

## セル評価基準（全Phase共通）

| 評価 | 定義 | 次のアクション |
|------|------|--------------|
| ◎ | 具体的な事実データ・数値がある（出典付き） | 不要 |
| △ | 言及はあるが具体性に欠ける | ◎化を試みる |
| ✗ | 記載なし | 調査で埋める |

### △/✗のサブタグ

| タグ | 意味 | 扱い |
|------|------|------|
| `✗[未調査]` | まだ調査していない | 次ラウンドで調査 |
| `✗[非公開]` | 業界慣行として非公開の情報 | **打ち切り** |
| `✗[資料未取得]` | 資料は存在するが技術的に取得不可 | 手動補完依頼 |
| `△[定性のみ]` | 定量データなし、定性は確認済 | 原理的に◎化不可なら確定 |
| `△[単一ソース]` | 1ソースのみで裏付け不足 | クロス軸再評価で◎化を試みる |

## Core Rules

1. **軸定義の正**: `docs/am-comparison-framework.md`（スキル側で複製しない）
2. **「立派に見える言葉」禁止**: 全社に当てはまる記述は差別化にならない
3. **3層モデル**: 説明層だけでなく、運用プロセス層・組織モデル層まで掘る
4. **出典必須**: 最優先軸の◎セルにはURL or 資料名を記載
5. **ユーザー確認ゲート**: Phase 1終了後（v0マトリクス）と Phase 4（最終保存）で承認を取る

## Resources (load on demand)

| ファイル | 用途 | 読込タイミング |
|---------|------|--------------|
| `references/execution-protocol.md` | Phase 1-4 の詳細手順 | 各Phase開始時に該当セクション |
| `references/web-query-templates.md` | 軸ごとのWeb調査クエリ・直接取得ソース一覧 | Phase 2 開始時 |
| `references/comparison-template.md` | 横断比較表のスケルトン | Phase 3 開始時 |
| `references/quality-check-am.md` | 品質チェックプロセス | Phase 3 開始時 |
| `docs/am-comparison-framework.md` | 4群28軸の定義・3層モデル・比較原則 | Phase 1 開始時（必須） |
