---
name: interview-reflect
description: >
  全社の reflection ファイルを横断集計し、繰り返し出る弱点・成功パターンを抽出して
  docs/interview_patterns.md を更新するスキル。
  「振り返りを集計して」「面接パターンを更新して」「/interview-reflect」で起動。
  面接ごとに手動実行する。reflection が5件以上たまってから効果が出る。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# interview-reflect スキル

## 責務

**このスキルがやること**: 全社 reflection ファイルの横断集計・弱点/成功パターンの抽出・interview_patterns.md の更新  
**このスキルがやらないこと**: 個別面接の詳細分析（→ interview-blindspot が担当）・次回質問の予測（→ interview-next-prep が担当）

---

## Step 0: 入力確認

ユーザーから以下を確認する。不明な場合はデフォルト動作（全社・全ステップ）で進める。

| 項目 | デフォルト |
|-----|----------|
| 対象企業 | 全社 |
| 対象ステップ | 全ステップ |

---

## Step 1: reflection ファイルの収集

以下の glob パターンで全社の reflection ファイルを収集する。

```
company-info/*/reflection_*.md
```

収集結果を一覧表示する。ファイルが0件の場合は終了する。

---

## Step 2: 各 reflection ファイルの読み込みと抽出

発見した全 reflection ファイルを読み込む。各ファイルから以下を抽出する:

| 抽出項目 | 抽出場所 |
|---------|---------|
| 企業名・ステップ | ファイルパス |
| result | frontmatter の `result:` |
| 自己評価した弱点 | `## 反省点・弱点` セクション |
| うまくいった点 | `## よかった点` セクション |
| AI検出の盲点 | `## 盲点（AI検出）` セクション（存在する場合） |
| 深掘りされた質問 | `## 深掘りされた質問` セクション（存在する場合） |

frontmatter に `result:` がないファイルは `pending` 扱いとし、警告リストに追加する。

---

## Step 3: 横断集計

### 3-1. 弱点の集計（全ファイル対象）

弱点テーマを集計し出現回数でランキングする。出現回数2回以上を「繰り返し弱点」とする。

### 3-2. 成功パターンの集計（passed のみ）

`result: passed` のファイルのみを対象に、よかった点を集計する。出現回数2回以上を「再現性ある成功パターン」とする。

### 3-3. 深掘りテーマの集計（全ファイル対象）

深掘りされた質問・テーマを横断して集計する。

---

## Step 4: interview_patterns.md の現状読み込み

`docs/interview_patterns.md` を読み込む。既存の内容と差分のみを更新対象にする。
存在しない場合は新規作成する。

---

## Step 5: プレビュー提示

更新後の `docs/interview_patterns.md` の内容をプレビューする。ファイルにはまだ保存しない。

```
## interview_patterns.md 更新プレビュー

更新日: YYYY-MM-DD
集計対象 reflection: N件（passed: X件 / rejected: Y件 / pending: Z件）

### 追加・更新される内容
- 繰り返し弱点: N件
- 成功パターン: N件
- 深掘りテーマ: N件

### 警告（result 未設定ファイル）
- <ファイルパス>
```

ユーザーに確認を求める。承認後 Step 6 へ進む。

---

## Step 6: 保存

承認後、`docs/interview_patterns.md` を更新する。

```
保存完了: docs/interview_patterns.md

次のステップ:
- 直前チェックシート → interview-direct-prep を実行
- 通過実績の反映 → success-pattern-extractor を実行（定期）
```

---

## 品質ガードレール

- `result: passed` のファイルと `result: rejected` のファイルは別集計する（混在禁止）
- 出現回数1回のパターンは「繰り返し弱点」に含めない（「観察例」として別区分する）
- `docs/interview_patterns.md` の既存内容は削除しない（追記・更新のみ）
