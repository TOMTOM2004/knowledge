---
name: es-refiner
description: >
  新規または提出済みESから改善要素を抽出し、企業固有の内容を除外した上で
  components/foundations/ の基盤回答をブラッシュアップするスキル。
  「ESから改善要素を抽出して」「このESをfoundationsに反映して」「基盤回答を更新して」
  「foundations を更新して」「/es-refiner」などの依頼で呼び出す。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ES Refiner

提出済み・作成済みESを読み込み、改善要素を抽出して `foundations/` の基盤回答を更新する。
es-writer（base → company ES）とは逆方向の責務。ユーザー承認なしにファイルを変更しな��。

## Step 概要

| Step | 内容 | 詳細 |
|------|------|------|
| 0 | 入力確認（対象ESファイル特定��� | `references/execution-protocol.md` |
| 1 | foundations/ の存在確認（未作成なら初期化） | 同上 |
| 2 | 対象ESの読み込みと設問種別分類 | 同上 |
| 3 | 改善要素の抽出（汎用化 vs 企業固有の分類） | ��上 |
| 4 | 改善抽出レポート提示（採用/保留/却下をユーザーに確認） | 同上 |
| 5 | ユーザー判断に基づくfoundations更新 | 同上 |
| 6 | update_log.md への記録 | 同上 |
| 7 | 完了報告 | 同上 |

## Core Rules (Guardrails)

| # | ルール |
|---|-------|
| G1 | **ユーザーの「採用/保留/却下」が揃うまでファイルを変��しない** |
| G2 | **企業名・敬称・企業固有ビジョンを含む表現は foundations に書かない** |
| G3 | **改善の最終判断はユーザーが行う。Claude は候補提示のみ** |
| G4 | **`submitted/` は読み取り専用** |
| G5 | **既存テキストを削除しない。旧版はコメントとして残す** |
| G6 | **保留・却下も update_log.md に必ず記録する** |
| G7 | **1セッションで更新するファイルは最大2件まで** |
| G8 | **foundations/ が初期化されていない場合は Step 1-B を完了してから進む** |

## Resources (load on demand)

| ファイル | 用途 | 読込タイミ��グ |
|---------|------|--------------|
| `references/execution-protocol.md` | Step 0-7 の詳細手順 | 各Step開始時 |
