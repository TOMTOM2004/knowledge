---
name: interview-session-preparer
description: >
  模擬面接セッションの準備スキル。企業名・面接段階・コースを入力に、
  session_config.yaml を作成し、質問候補セット・AI議論ログを生成・保存する。
  「<企業名>の<N>次面接セッションを準備して」「/interview-session-preparer」で起動。
allowed-tools: Read, Write, Glob, Grep, Bash
---

# interview-session-preparer

**やること**: session_config 作成 → 入力ファイル読み込み → 質問候補生成 → 議論ログ生成 → 保存
**���らないこと**: 実際の模擬面接実行（→ interview-debate-orchestrator）

**前提**:
- knowledge ルート: `/Users/ishidatomonori/Desktop/knowledge/`
- ペルソナ定義: `tools/interview_os/personas/<persona_id>.yaml`
- スキーマ: `tools/interview_os/session_config_schema.yaml`

## Step 概要

| Step | 内容 | 詳細 |
|------|------|------|
| 0 | ��力確認（企業名・段階・コース等） | `references/execution-protocol.md` |
| 1 | ペルソナセット選定（interview-persona-router ロジック） | 同上 |
| 2 | 入力ファイル読み込み（research_brief, interview_prep, ES, ペルソナ） | 同上 |
| 3 | 質問候補生成（基本7問 + 会社固有3-5問 + ペルソナ別深掘り + ランダム1問） | 同上 |
| 4 | AI議論ログ生成（JSONL形式） | 同上 |
| 5 | プレビュー提示（+ 逆質問生成の提案） | ��上 |
| 6 | 保存（configs/ + generated/） | 同上 |

## Core Rules

1. `research_brief.md` なしの場合は `【警告】` タグをつけて確認
2. 会社固有質問は最低3問生成する
3. 基本質問の深掘りは全ペルソナ分を網羅する
4. ランダム質問は毎回ランダムに選ぶ

## Resources (load on demand)

| フ���イル | 用途 | 読込タイミング |
|---------|------|--------------|
| `references/execution-protocol.md` | Step 0-6 の詳細手順 | 各Step開始時 |
