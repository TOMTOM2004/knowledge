---
name: es-refiner
description: >
  新規または提出済みESから改善要素を抽出し、企業固有の内容を除外した上で
  components/foundations/ の基盤回答をブラッシュアップするスキル。
  「ESから改善要素を抽出して」「このESをfoundationsに反映して」「基盤回答を更新して」
  「foundations を更新して」「/es-refiner」などの依頼で呼び出す。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ES Refiner スキル

提出済み・作成済みESを読み込み、改善要素を抽出して `foundations/` の基盤回答を更新する。
es-writer（base → company ES）とは逆方向の責務。ユーザー承認なしにファイルを変更しない。

---

## Step 0: 入力の確認

ユーザーの依頼から以下を特定する。

- **対象ESファイル**: 企業名が指定されていれば以下を順に探す
  1. `/Users/ishidatomonori/Desktop/knowledge/ES/企業別/提出済/<企業名>.md`
  2. `/Users/ishidatomonori/Desktop/knowledge/移行後ES/<企業名>.md`
  3. `/Users/ishidatomonori/Desktop/knowledge/ES/企業別/作成中/<企業名>.md`

ファイルが見つからない場合は一覧を提示して終了:
```bash
ls /Users/ishidatomonori/Desktop/knowledge/ES/企業別/提出済/
ls /Users/ishidatomonori/Desktop/knowledge/移行後ES/
```

---

## Step 1: foundations/ の存在確認と初期化

```bash
ls /Users/ishidatomonori/Desktop/knowledge/ES/部品/foundations/ 2>/dev/null
```

**foundations/ が存在しない、または5ファイルのいずれかが欠けている場合**: → Step 1-B へ
**全ファイルが揃っている場合**: → Step 2 へ

### Step 1-B: foundations/ を初期化する

`components/best_answers.md`、`components/gakuchika.md`、`components/motivation.md`、
`components/self_pr.md`、`components/other.md` を読み込み、
各ファイルのベストアンサー（⭐マーク）から企業名・敬称を除いた汎用核心部分のみを抽出して
以下の5ファイルを作成する。

```
components/foundations/
├── gakuchika.md        # ガクチカ基盤版（企業名なし）
├── tsuyomi.md          # 強み・自己PR基盤版
├── motivation_axis.md  # 志望動機の軸（業界共通部分のみ）
├── jikoshoukai.md      # 自己紹介基盤版
└── shukatu_jiku.md     # 就活軸基盤版
```

各ファイルのフォーマット:

```markdown
---
last_updated: YYYY-MM-DD
version: 1
source: <初期化元のファイル名・セクション名>
---

# <カテゴリ名> 基盤回答

## コアフレーズ
<!-- 強み・軸を1〜2文で表現したキャッチコピー -->

## 核心テキスト（企業名なし・転用可能版）
<!-- 敬称・企業名を除いた本文。「〇〇の会社で」などの企業固有表現は除く -->

## 補足エピソード素材
<!-- 使えるエピソード・数値のリスト（本文には入れない） -->

## 除外した企業固有要素（参考記録）
<!-- 初期化時に除外した企業名・ビジョン等のメモ -->
```

初期化完了後、ユーザーに以下を報告してから Step 2 に進む:
```
foundations/ を初期化しました（5ファイル作成）。
ソース: components/best_answers.md のベストアンサー（⭐）をベースに抽出。
引き続き改善抽出に進みます。
```

---

## Step 2: 対象ESの読み込みと分類

対象ESファイルを読み込み、各回答を以下の設問種別に分類する。

| 設問種別 | 対応 foundations ファイル |
|---------|--------------------------|
| ガクチカ・力を入れたこと・努力 | `foundations/gakuchika.md` |
| 自己PR・強み・長所 | `foundations/tsuyomi.md` |
| 志望動機・志望理由 | `foundations/motivation_axis.md` |
| 自己紹介・学生時代の概要 | `foundations/jikoshoukai.md` |
| 就活軸・企業選びの軸・キャリアビジョン | `foundations/shukatu_jiku.md` |
| チームワーク・挫折・弱み（単独設問） | 対象外（foundations 更新なし・記録のみ） |

対象外の設問は「スキップ（foundations 更新対象外）」として記録する。

---

## Step 3: 改善要素の抽出

対象 foundations ファイルを読み込み、ESの回答と比較して以下を抽出する。

### 抽出する改善単位

| 種別 | 判断基準 |
|------|---------|
| **部分表現の更新** | 既存より明確・鋭い言い回し。同じ意味でより説得力がある |
| **論理展開の改善** | 課題→原因→施策→成果の流れが現行 foundations より整理されている |
| **強みの言語化** | コアフレーズが現行より具体的・差別化されている |
| **構成の改善** | STAR構成の完成度、数値・具体行動・学びの3点の充足度が高い |
| **就活軸の深化** | 自分の why（動機の根）の言語化が現行より深い |

### 汎用化 vs 企業固有の分類ルール

**汎用化できる（昇格候補）**:
- 企業名・企業固有ビジョン・敬称を含まない
- 「〜業界で」「〜の分野で」など複数社に転用できる
- 強み・行動パターン・思考回路の言語化

**企業固有として隔離（foundations には混入しない）**:
- 企業名・「貴社」「貴行」などの敬称が埋め込まれた文
- 特定企業のビジョン・戦略・事業名・ブランドへの言及
- 「合併新会社」「〇〇との提携」など時限的文脈
- 業界限定の専門用語で他業界では通じないもの

---

## Step 4: 改善抽出レポートの提示

以下の形式でレポートを提示する。**この時点ではまだファイルを変更しない**。

```
## 改善抽出レポート: <企業名>（<ファイルパス>）

---

### [昇格候補 #1] <foundations ファイル名> — <改善種別>

- **現行**:
  > <foundations の該当テキスト（なければ「（未記載）」）>

- **提案**:
  > <新しいテキスト>

- **採用理由**: <なぜ改善と判断したか 1〜2文>

---

### [昇格候補 #2] ...（以下同形式）

---

### [企業固有・隔離] <設問名>

- **内容**: 「〜〜〜」
- **除外理由**: <企業名/ビジョン/業界限定表現が含まれるため>

---

### [スキップ] <設問名>
- **理由**: foundations 対象外の設問種別（チームワーク等）

---

## アクション確認

昇格候補は全部で X 件です。
各候補について「採用」「保留」「却下」を教えてください。
（例: 「#1採用 #2保留 #3却下」）

または「全採用」「全保留」でも構いません。
```

---

## Step 5: ユーザー確認を受けて更新

ユーザーから各候補への判断を受け取ったら以下を実行する。

### 採用の場合
対応する `foundations/<ファイル名>.md` を編集する:
- フロントマターの `last_updated` と `version` を更新
- 該当セクションのテキストを差し替える（既存テキストは削除せず `<!-- 旧版 YYYY-MM-DD: 〜 -->` としてコメントで残す）

### 保留・却下の場合
ファイルは変更しない。update_log.md への記録のみ行う。

---

## Step 6: update_log.md への記録

`/Users/ishidatomonori/Desktop/knowledge/ES/部品/update_log.md` に追記する。
ファイルが存在しない場合は以下のヘッダーで新規作成する:

```markdown
# ES Foundations 更新ログ

> 採用・保留・却下の全記録。保留は将来の再検討候補として残す。

---
```

追記フォーマット:

```markdown
## <YYYY-MM-DD> | ソース: <企業名>.md

| # | 対象ファイル | 改善種別 | 判断 | 内容要約 |
|---|------------|---------|------|---------|
| 1 | foundations/gakuchika.md | 論理展開の改善 | 採用 | 課題→原因→施策の流れを再構成 |
| 2 | foundations/motivation_axis.md | 部分表現の更新 | 保留 | 「リスクを未然に防ぐ」軸（他社で検証後に再判断） |
| 3 | — | 企業固有・除外 | — | 「〇〇のテーマパーク」は企業固有ビジョン |

---
```

---

## Step 7: 完了報告

以下を報告する:

```
## 更新完了

- 採用: X 件（<ファイル名> を更新）
- 保留: Y 件（update_log.md に記録）
- 却下: Z 件（update_log.md に記録）
- 企業固有・除外: W 件

update_log.md を更新しました。
次回 es-writer でESを作成する際、更新後の foundations/ が自動で参照されます。
```

---

## ガードレール（必ず守る）

| # | ルール |
|---|-------|
| G1 | **ユーザーの「採用/保留/却下」が揃うまでファイルを変更しない** |
| G2 | **企業名・敬称・企業固有ビジョンを含む表現は foundations に書かない** |
| G3 | **改善の最終判断はユーザーが行う。Claude は候補提示のみ** |
| G4 | **`submitted/` は読み取り専用。絶対に書き込まない** |
| G5 | **既存テキストを削除しない。旧版はコメントとして残す** |
| G6 | **保留・却下も update_log.md に必ず記録する（捨てない）** |
| G7 | **1セッションで更新するファイルは最大2件まで。それ以上は次回に分割** |
| G8 | **foundations/ が初期化されていない場合は Step 1-B を完了してから進む** |

---

## 注意事項

- `data/raw/` には絶対に触れない
- `ES/企業別/提出済/` のファイルは読み取り専用（参照のみ・書き込み禁止）
- `foundations/` の更新は es-writer の `components/best_answers.md` 参照には影響しない。
  foundations はes-writerとは独立した基盤資産。
- `motivation_axis.md` には「なぜ金融か」「なぜデータ分析か」など業界共通の軸のみを記録する。
  企業別の志望動機の全文は `components/motivation.md` に引き続き保持する。
