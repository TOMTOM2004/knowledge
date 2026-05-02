---
name: es-improver
description: >
  ESライター自動改善スキル。es-writer が main に保存した初稿と、ユーザーが編集した
  ブランチの差分を分析し、es-writer/SKILL.md のどのルールが不足していたかを洗い出して
  スキルを自動更新する。
  「〇〇のESフィードバックループを実行して」「ESライターを改善して」「差分からスキルを更新して」
  「/es-improver」などで呼び出す。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ES Improver

es-writer 初稿（main）とユーザー編集版（ブランチ）��差分を分析し、
es-writer/SKILL.md を自動更新してESライターの品質を継続的に向上させる。

## Step 概要

| Step | 内容 | 詳細 |
|------|------|------|
| 0 | 入力確認（企業名） | `references/execution-protocol.md` |
| 1 | ブランチ自動検出 | 同上 |
| 2 | 差分の対象ファイル特定 | 同上 |
| 3 | 差分取得（+行/-行の分類） | 同上 |
| 4 | 不足分析（変更カテゴリ分類 + 根本原因推定） | 同上 |
| 5 | 改善提案の生成（ユーザー承認待ち） | 同上 |
| 6 | ユーザー承認後に SKILL.md を更新 | 同上 |
| 7 | フィードバックループ記録（任意） | 同上 |

## Core Rules

1. **SKILL.md の更新は追記・修正のみ**。既存ルール削除はユーザー確認必須
2. **企業固有情報は SKILL.md に書かない**（汎用ルールのみ抽出���
3. **差分が100行超の場合**は汎用パターンのみ提案する
4. `ES/企業別/提出済/` は���み取り専用

## Resources (load on demand)

| ファイル | 用途 | 読込タイミング |
|---------|------|--------------|
| `references/execution-protocol.md` | Step 0-7 の詳��手順 | 各Step��始時 |
