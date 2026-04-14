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
- `ES/素材/INDEX.md`
- `ES/部品/best_answers.md`（必要な設問タイプのみ）

**書くもの**:
- `ES/企業別/作成中/<企業名>.md` または `移行後ES/<企業名>.md`

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

### セッションE1: 面接調査

**目的**: 体験記・選考実態を収集し、質問を重要度別に分類する

**読むもの**:
- `company-info/<企業名>/research_brief.md`（軸3・軸7-A・軸9を確認）
- `company-info/<企業名>/interview_prep_*.md`（旧ファイルがあれば参考参照のみ）

**スキル**: interview-research

**書くもの**:
- `company-info/<企業名>/interview_research_<ステップ>_<YYYYMMDD>.md`

**読まないもの**:
- ES系 skill（es-writer等）
- interview-qa（次セッションで使う）

**推奨依頼文**:
```
「[企業名]の[N]次面接の選考調査をして。
 interview-research を使って。ESレビューはしなくていい」
```

**次に渡す成果物**: `interview_research_<ステップ>_<日付>.md`

---

### セッションE2: 想定問答生成

**目的**: 調査結果をもとに重要度別の回答骨格・詰め対策・逆質問を生成する

**読むもの**:
- `company-info/<企業名>/interview_research_<ステップ>_*.md`（E1の成果物）
- `company-info/<企業名>/research_brief.md`（軸3・軸7-A・軸8・軸9）
- `移行後ES/<企業名>.md`（提出済みES）
- `ES/素材/01_自己分析_コア価値観将来像行動原理.md`
- `ES/素材/02_自己分析_強み弱み伸びしろ.md`

**スキル**: interview-qa

**書くもの**:
- `company-info/<企業名>/interview_qa_<ステップ>_<YYYYMMDD>.md`

**読まないもの**:
- ES系 skill（es-writer等）
- research 系 skill

**推奨依頼文**:
```
「[企業名]の[N]次面接の想定問答を作って。
 interview-qa を使って。調査ファイルは interview_research_[ステップ]_*.md を読んで」
```

**次に渡す成果物**: `interview_qa_<ステップ>_<日付>.md`

---

## セッション間の引継ぎ方法

各セッションの終わりに作成するファイルが「引継ぎ書」になる:

```
A → B: research_brief.md
B → C: （更新された）research_brief.md
C → D: ES草案ファイル
D → E1: 最終 ES ファイル
E1 → E2: interview_research_<ステップ>_<日付>.md
```

新しいセッション開始時は:
```
「company-info/[企業名]/research_brief.md と 移行後ES/[企業名].md を読んで、[タスク]をして」
```

---

## 再開しやすいファイル命名

| ファイル | 命名規則 |
|---------|---------|
| ES草案 | `ES/企業別/作成中/<企業名>.md` |
| 提出前ES | `移行後ES/<企業名>.md` |
| 企業調査 | `company-info/<企業名>/research_brief.md` |
| 旧面接準備（参照のみ） | `company-info/<企業名>/interview_prep_<N>次_YYYYMMDD.md` |
| 面接調査（新） | `company-info/<企業名>/interview_research_<ステップ>_<YYYYMMDD>.md` |
| 面接想定問答（新） | `company-info/<企業名>/interview_qa_<ステップ>_<YYYYMMDD>.md` |

---

## 会話を引きずらない運用

- 前の会話の内容は次の会話に持ち越さない
- 「前回話した内容と同じ」で参照させない（ファイルパスを明示する）
- セッション間は必ずファイルを経由する
- 口頭で引き継いだ情報は信頼しない（ファイルに書いてないものは存在しない）
