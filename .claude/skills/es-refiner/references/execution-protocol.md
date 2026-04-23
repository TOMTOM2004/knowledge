# ES Refiner — 実行手順

SKILL.md から参照される詳細手順。

---

## Step 0: 入力の確認

ユーザーの依頼から以下を特定する。

- **対象ESファイル**: 企業名が指定されていれば以下を順に探す
  1. `/Users/ishidatomonori/Desktop/knowledge/ES/企業別/提出済/<企業名>.md`
  2. `/Users/ishidatomonori/Desktop/knowledge/移行後ES/<企業名>.md`
  3. `/Users/ishidatomonori/Desktop/knowledge/ES/企業別/作成中/<企業名>.md`

ファイルが見つからない場合は一覧を提示して終了。

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

## 核心テキスト（企業名なし・転用可能版）

## 補足エピソード素材

## 除外した企業固有要素（参考記録）
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

### [企業固有・隔離] <設問名>
- **内容**: 「〜〜〜」
- **除外理由**: <企業名/ビジョン/業界限定表現が含まれるため>

---

## アクション確認

昇格候補は全部で X 件です。
各候補について「採用」「保留」「却下」を教えてください。
```

---

## Step 5: ユーザー確認を受けて更新

### 採用の場合
対応する `foundations/<ファイル名>.md` を編集する:
- フロントマターの `last_updated` と `version` を更新
- 該当セクションのテキストを差し替える（既存テキストは `<!-- 旧版 YYYY-MM-DD: 〜 -->` としてコメントで残す）

### 保留・却下の場合
ファイルは変更しない。update_log.md への記録のみ行う。

---

## Step 6: update_log.md への記録

`/Users/ishidatomonori/Desktop/knowledge/ES/部品/update_log.md` に追記する。

追記フォーマット:

```markdown
## <YYYY-MM-DD> | ソース: <企業名>.md

| # | 対象ファイル | 改善種別 | 判断 | 内容要約 |
|---|------------|---------|------|---------|
| 1 | foundations/gakuchika.md | 論理展開の改善 | 採用 | 課題→原因→施策の流れを再構成 |
```

---

## Step 7: 完了報告

```
## 更新完了

- 採用: X 件（<ファイル名> を更新）
- 保留: Y 件（update_log.md に記録）
- 却下: Z 件（update_log.md に記録）
- 企業固有・除外: W 件
```
