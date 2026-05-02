---
name: reverse-question-generator
description: >
  面接の逆質問リストを生成するスキル。面接官のタイプ（人事・現場・役員等）に応じて
  質問内容を切り替え、research_brief の軸7-Aフックを使った企業固有の逆質問を優先度付きで生成する。
  「<企業名>の逆質問リストを作って」「/reverse-question-generator」で起動。
  interview-session-preparer の Step 5 からも呼び出し可能。
allowed-tools: Read, Write
---

# reverse-question-generator

**やること**: 面接官タイプ別の逆質問生成・優先度付け・NG逆質問チェック・保存
**やらないこと**: 面接全体の質問生成・回答骨格作成（→ interview-session-preparer / interview-qa）
**前提**: `company-info/<企業名>/research_brief.md` が存在すること

## Step 概要

| Step | 内容 | 詳細 |
|------|------|------|
| 0 | ��力確認（企業名・段階・面接官タイプ） | `references/execution-protocol.md` |
| 1 | ファイル読み込み（research_brief, interview_research, ペルソナ） | 同上 |
| 2 | 面接官タイプ × フォーカス決定 | 同�� |
| 3 | 逆質問生成（4カテゴリ × 面接官タイプ適合） | 同上 |
| 4 | 優先度判定（A/B/C）+ NG チェック | 同上 |
| 5 | ���レ��ュー提示 | 同上 |
| 6 | 保存 | 同上 |

## Core Rules

1. **優先度Aは必ず1問**を軸7-Aベースで生成する
2. **NG質問チェック**は毎回実行する（「御社の主力事業は？」等は除外）
3. 面接官が複数タイプ想定される場合は**タイプ別セクション**に分ける
4. 時間制約を冒頭に明示する
5. `research_brief.md` がない場合は軸7-Aフック生成不可の警告を出す

## Resources (load on demand)

| ファイル | 用途 | 読込タイミング |
|---------|------|--------------|
| `references/execution-protocol.md` | Step 0-6 の詳細手順 | 各Step開始時 |
