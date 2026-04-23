---
name: interview-qa
description: >
  想定問答ファイル生成専門スキル。interview_research・ES・research_brief を入力に、
  重要度別の回答骨格・深掘り問答・詰められ対策・逆質問を生成する。
  「〇〇の想定問答を作って」「〇〇の<ステップ>の回答骨格を生成して」「/interview-qa」で起動。
  interview-research を先に実行していない場合は警告を出す。
allowed-tools: Read, Write
---

# interview-qa

**やること**: 重要度別の回答骨格生成・深掘り展開・詰められ対策・逆質問リスト作成
**やらないこと**: 体験記の収集・質問の重要度分類（→ interview-research）

**前提**: `interview-research` を先に実行し、`interview_research_<ステップ>_*.md` が存在すること

## Step 概要

| Step | 内容 | 詳細 |
|------|------|------|
| 0 | 入力確認（企業名・コース・ステップ） | `references/execution-protocol.md` |
| 1 | ファイル読み込み（interview_research, research_brief, ES, 自己分析） | 同上 |
| 1.5 | ES↔面接言い換え対照表（ES存在時のみ） | 同上 |
| 2 | 重要度別の回答骨格生成（高: フル / 中: 標準 / 低: 簡略） | 同上 |
| 2.5 | 志望動機接続マップ（4軸接続表 + 矛盾チェック） | 同上 |
| 3 | 詰められポイントと対策（11観点） | 同上 |
| 4 | 逆質問リスト（4カテゴリ×2問） | 同上 |
| 5 | プレビュー提示 | 同上 |
| 6 | 保存 | 同上 |

## Core Rules

1. **軸7-A（核心固有性）** を志望動機系回答に必ず組み込む。未抽出なら `【固有性未抽出】` 警告
2. **回答骨格は箇条書きのみ**（文章化しない）— 暗記防止
3. **高・中の質問には深掘り2段展開を必須**とする
4. **高の質問には地雷回避メモを必須**とする
5. **複数コース出願時**: 第一志望確定版回答 + 併願一貫ロジックを必ず生成
6. **自己評価型質問**（`【自己評価型】` タグ）には専用フレームを適用

## Resources (load on demand)

| ファイル | 用途 | 読込タイミング |
|---------|------|--------------|
| `references/execution-protocol.md` | Step 0-6 の詳細手順 | 各Step開始時 |
| `references/answer-patterns.md` | 面接回答パターン（話し言葉版） | Step 2で回答骨格生成時 |
| `references/stage-modes.md` | 選考段階別の評価基準・チェックリスト | Step 1で選考ステップ特定後 |
| `references/role-fit-criteria.md` | 職種別の評価観点・頻出質問 | Step 2でコース特定後 |
