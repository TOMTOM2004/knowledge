---
name: interview-blindspot
description: >
  reflection と transcript を照合し、自己反省で言及されていないが transcript 上で弱かった
  箇所を抽出して reflection に「## 盲点（AI検出）」セクションを追記するスキル。
  「盲点を検出して」「transcript と reflection を照合して」「/interview-blindspot」で起動。
  reflection 作成後・transcript 到着後に手動実行する。
allowed-tools: Read, Write, Edit, Glob
---

# interview-blindspot スキル

## 責務

**このスキルがやること**: reflection と transcript の差分分析・未言及の弱点抽出・reflection への盲点セクション追記  
**このスキルがやらないこと**: 全社横断集計（→ interview-reflect が担当）・次回質問の予測（→ interview-next-prep が担当）

**前提**: `reflection_<N>次_<YYYYMMDD>.md` と `transcript_<N>次_<YYYYMMDD>.md` の両方が存在すること

---

## Step 0: 入力確認

以下を確認する。不明な場合はユーザーに質問する。

| 項目 | 例 |
|-----|-----|
| 企業名 | 〇〇証券 |
| 選考ステップ | 1次 / 2次 / 最終 |

---

## Step 1: ファイルの確認と読み込み

以下を並列で確認する。

```
company-info/<企業名>/reflection_<N>次_*.md  ← 最新ファイルを使用
company-info/<企業名>/transcript_<N>次_*.md  ← 最新ファイルを使用
```

| 状態 | 対応 |
|-----|-----|
| 両方存在 | Step 2 へ進む |
| reflection のみ存在 | `【transcript が見つかりません】transcript_<N>次_<YYYYMMDD>.md が届いたら再実行してください。` と表示して終了 |
| transcript のみ存在 | `【reflection が見つかりません】まず reflection_<N>次_<YYYYMMDD>.md を作成してください。` と表示して終了 |
| 両方なし | 両方のファイルが必要な旨を表示して終了 |

reflection ファイルに `## 盲点（AI検出）` セクションが既に存在する場合:
`【既存の盲点セクションを上書きしますか？】（はい / キャンセル）`
と確認する。

---

## Step 2: reflection の自己評価の抽出

reflection ファイルから以下を抽出する:

- 自己評価した弱点・反省点のリスト（`## 反省点・弱点` セクション）
- 「うまくいった」と自己評価した点のリスト（`## よかった点` セクション）
- 言及された質問・トピックのリスト（`## 聞かれた質問` セクション）

---

## Step 3: transcript の弱点分析

transcript ファイルを分析し、以下の観点で弱かった箇所を特定する。

### 弱点判定の観点

| 観点 | 判定基準 |
|-----|---------|
| 回答の短さ | 1〜2文で終わっている質問がないか |
| 深掘りの受け方 | 同じテーマで複数回深掘りされた箇所がないか |
| 言い淀み | 「えー」「あの」「少し考えていいですか」が多い箇所 |
| 面接官の補足要求 | 「それは具体的には？」「もう少し教えてください」が続いた箇所 |
| 抽象度 | 具体例なく抽象論で終わった回答 |
| 数字・根拠の欠如 | 「いくつですか」「どれくらいですか」と補足を求められた箇所 |

---

## Step 4: 差分分析（盲点の特定）

Step 2（self-reflection）と Step 3（transcript 分析）を照合する。

| 分類 | 説明 |
|-----|-----|
| **盲点（新規）** | transcript で弱いが reflection で言及なし |
| **認識一致** | transcript で弱く、reflection でも認識あり |
| **自己過大評価** | reflection で「よかった」と書いたが transcript では弱かった箇所 |

「盲点（新規）」と「自己過大評価」の箇所を抽出してリストアップする。

---

## Step 5: プレビュー提示

追記する `## 盲点（AI検出）` セクションのプレビューを出力する。ファイルにはまだ保存しない。

```
## 盲点（AI検出）

検出日: YYYY-MM-DD
照合ファイル:
- reflection: reflection_<N>次_<YYYYMMDD>.md
- transcript: transcript_<N>次_<YYYYMMDD>.md

---

### 盲点（自己反省で未言及だが transcript 上で弱かった箇所）

| # | 質問・トピック | transcript 上の弱さ | 改善方針 |
|---|------------|------------------|---------|
| 1 | <質問> | <弱さの説明（観点を明記）> | <改善方針> |

### 自己過大評価（「よかった」と書いたが transcript では弱かった箇所）

| # | 質問・トピック | reflection の自己評価 | transcript の実態 |
|---|------------|-------------------|----------------|
| 1 | <質問> | <reflection での記述> | <transcriptの実態> |

### 認識一致（参考: reflection と transcript の評価が一致している弱点）

- <弱点1>
```

ユーザーに確認を求める。承認後 Step 6 へ進む。

---

## Step 6: reflection への追記

承認後、reflection ファイルの `## 盲点（AI検出）` セクションを更新する。

```
追記完了: company-info/<企業名>/reflection_<N>次_<YYYYMMDD>.md

次のステップ:
- 次回選考が決まったら → interview-next-prep を実行
- 全社パターンを更新したいなら → interview-reflect を実行
```

---

## 品質ガードレール

- transcript が存在しない場合は実行しない（reflection のみによる推測は禁止）
- `## 盲点（AI検出）` セクションの既存内容は、ユーザー確認なしに上書き・削除しない
- 弱点判定は transcript のテキスト根拠を必ず明示する（AI の主観による判断は禁止）
- 「自己過大評価」の指摘は事実ベースで行い、批判的トーンを避ける
