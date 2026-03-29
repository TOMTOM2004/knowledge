# セッション分割ガイド

「長い1会話ですべてやる」前提をやめ、セッション分割を標準運用にする。

---

## なぜ分割するか

- 1会話でやると 100〜200 KB のロードが発生
- 途中で skill や agent が混在してコンテキストが汚染される
- 前の話題の参照ファイルを引きずる
- 短い会話ほどトークンが少なく、品質も安定しやすい

---

## 標準 5セッション構成

### セッションA: 詳細調査

**目的**: 企業情報を収集して brief に圧縮する

**読むもの**:
- company-researcher SKILL
- WebSearch / WebFetch の結果（外部）

**書くもの**:
- `company-info/<企業名>/research_brief.md`

**書かないもの**: ES は書かない

**推奨依頼文**:
```
「[企業名]の企業調査をして research_brief.md に保存して。ESは書かない」
```

**次に渡す成果物**: `research_brief.md`

---

### セッションB: brief 整形・補強（任意）

**目的**: research_brief を ES/面接向けに確認・補強する

**読むもの**:
- `company-info/<企業名>/research_brief.md`

**書くもの**:
- `research_brief.md` の更新（必要な場合のみ）

**判断基準**:
- 志望動機の論点が 3点以上あるか
- 競合比較が入っているか
- ES を書き始める前に不安があるかどうか

**推奨依頼文**:
```
「company-info/[企業名]/research_brief.md を読んで
 志望動機と競合比較の論点が十分か確認して。不足があれば補充して」
```

**次に渡す成果物**: 確認済みの `research_brief.md`

---

### セッションC: ES草案

**目的**: brief と自己分析のみで ES を生成する

**読むもの**:
- `company-info/<企業名>/research_brief.md`
- `ES/md/INDEX.md`
- `ES/components/best_answers.md`（必要な設問タイプのみ）

**書くもの**:
- `ES/drafts/<企業名>.md` または `移行後ES/<企業名>.md`

**reviewer**: question-fit と readability のみ

**読まないもの**:
- 詳細調査ファイル（research.md等）
- interview 系 skill
- 他業種の domain skill

**推奨依頼文**:
```
「[企業名]のESを書いて。
 参照は research_brief.md と INDEX.md と best_answers.md だけでいい。
 レビューは question-fit と readability だけやって」
```

**次に渡す成果物**: ES草案 + question-fit/readability の指摘

---

### セッションD: ES仕上げ

**目的**: 草案をレビュー指摘と企業適合で最終確認する

**読むもの**:
- ES本文
- `company-info/<企業名>/research_brief.md`

**reviewer**: company-fit + role-fit + consistency-overlap

**書くもの**:
- ES最終版（editor-refiner による修正）

**推奨依頼文**:
```
「[企業名].md を読んで、company-fit と role-fit と consistency を確認して。
 指摘があれば editor-refiner で修正して」
```

**次に渡す成果物**: 提出可能な最終 ES

---

### セッションE: 面接想定問答

**目的**: ES をもとに面接深掘り耐性を確認する

**読むもの**:
- `company-info/<企業名>/interview_prep_*.md`（あれば）
- `company-info/<企業名>/research_brief.md`
- interview 系 skill（stage に応じた最小セット）

**reader**: skeptical-interviewer

**書くもの**:
- `company-info/<企業名>/interview_prep_<N>次_YYYYMMDD.md`

**読まないもの**:
- ES系 skill（es-writer等）
- research 系 skill

**推奨依頼文**:
```
「[企業名]の[N]次面接の準備をして。
 interview-prep を使って。ESレビューはしなくていい」
```

---

## セッション間の引継ぎ方法

各セッションの終わりに作成するファイルが「引継ぎ書」になる:

```
A → B: research_brief.md
B → C: （更新された）research_brief.md
C → D: ES草案ファイル
D → E: 最終 ES ファイル
```

新しいセッション開始時は:
```
「company-info/[企業名]/research_brief.md と 移行後ES/[企業名].md を読んで、[タスク]をして」
```

---

## 再開しやすいファイル命名

| ファイル | 命名規則 |
|---------|---------|
| ES草案 | `ES/drafts/<企業名>.md` |
| 提出前ES | `移行後ES/<企業名>.md` |
| 企業調査 | `company-info/<企業名>/research_brief.md` |
| 面接準備 | `company-info/<企業名>/interview_prep_<N>次_YYYYMMDD.md` |

---

## 会話を引きずらない運用

- 前の会話の内容は次の会話に持ち越さない
- 「前回話した内容と同じ」で参照させない（ファイルパスを明示する）
- セッション間は必ずファイルを経由する
- 口頭で引き継いだ情報は信頼しない（ファイルに書いてないものは存在しない）
