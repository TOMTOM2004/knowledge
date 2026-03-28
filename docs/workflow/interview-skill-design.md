# 面接スキル設計ガイド

面接準備・本番シミュレーションに使用するスキルの設計思想・使い分け・組み合わせを説明する。

---

## 面接スキルの全体像

```
面接準備プロセス
    │
    ├── [入力] 企業名・職種・面接ラウンド・ES草稿
    │
    ├── Stage A: 準備シート作成
    │   ├── interview-prep (SKILL.md)
    │   ├── stages/first-interview-mode     ← 1次面接対策
    │   └── stages/final-interview-depth-mode ← 最終面接対策
    │
    ├── Stage B: 深掘り質問生成
    │   ├── skeptical-interviewer (agent)
    │   ├── interview-probe-generation (SKILL.md)
    │   └── interview/followup-defense-patterns  ← 生成した質問への対処
    │
    ├── Stage C: 回答構造化（ES→話し言葉変換）
    │   ├── interview/motivation-answer-patterns
    │   ├── interview/gakuchika-answer-patterns
    │   ├── interview/strengths-weaknesses-answer-patterns
    │   └── interview/role-why-us-answer-patterns
    │
    └── Stage D: 反論・詰め対処
        └── interview/rebuttal-handling
```

---

## 面接スキルの分類

### `stages/` — 選考ステージ別評価軸

| スキル | ターゲット | 評価する側 | 主な使用タイミング |
|------|----------|----------|---------------|
| `stages/es-screening-mode` | 書類選考担当 | HR担当者 | ES提出直前 |
| `stages/first-interview-mode` | 1次面接 | 若手社員 / HR | 1次面接の前日 |
| `stages/final-interview-depth-mode` | 最終面接 | 役員・部長 | 最終前夜 |

**設計方針**: ステージが上がるほど「なぜここか」の深さが問われる。1次は基本的な志望動機・ガクチカの整理、最終は「なぜこの会社でなければならないか」の核心的説明力。

### `interview/` — 口頭回答パターン

| スキル | 担当するシーン | 特徴 |
|------|-------------|------|
| `motivation-answer-patterns` | 「志望動機を教えてください」 | 1〜2分の話し言葉構造。3層（業界/会社/職種）を自然に連結 |
| `gakuchika-answer-patterns` | 「学生時代に力を入れたことは？」 | 1分/3分/5分バージョン。「なぜ×5段」の準備 |
| `strengths-weaknesses-answer-patterns` | 「強み・弱みは？」 | 30秒〜1分。面接官タイプ別調整 |
| `role-why-us-answer-patterns` | 「なぜこの職種を？」「なぜ当社を？」 | 3階層の話し言葉組み立て。深掘り対処マトリクス付き |
| `followup-defense-patterns` | 深掘り質問への対処 | 5タイプ分類（事実確認/理由追求/代替案/批判/抽象化）|
| `rebuttal-handling` | 反論・詰め | 競合比較・第一志望確認・弱み指摘の3パターン |

---

## ESと面接の接続設計

ES（書き言葉）→面接（話し言葉）への変換が必要。以下のスキルがこの変換を担当する。

### 変換の方向性

```
ESの志望動機（400字）
    ↓ interview/motivation-answer-patterns
話し言葉1分バージョン（200〜300字相当）
    ↓ 深掘りが来たら
interview/rebuttal-handling → 競合比較への対処
```

```
ESのガクチカ（400字）
    ↓ interview/gakuchika-answer-patterns
1分バージョン → さらに深掘りが来たら3分バージョン
    ↓
interview/followup-defense-patterns → 事実確認質問への対処
```

### ES→話し言葉変換のルール（共通）

1. **主語を「私は」に戻す** — ESでは省略された主語を復活させる
2. **接続詞を口語化** — 「また」→「それと」、「しかし」→「ただ」
3. **結論を最初に** — ESより更に冒頭に「結論から言うと〜」を入れる
4. **数字を「感覚で言うと」に補足** — 「参加者50名のうち30名が」→「半数以上の方が」
5. **最後は「以上です」で終える** — 話し言葉特有の締め方

---

## ラウンド別の重点スキル

### 1次面接（若手社員、HR担当者）

**評価軸**: 基本マナー・ガクチカの具体性・志望動機の入口

```
使用スキル（優先順）:
1. stages/first-interview-mode        ← 1次の評価基準確認
2. interview/gakuchika-answer-patterns ← ガクチカ1分版を準備
3. interview/motivation-answer-patterns ← 志望動機1分版を準備
4. interview/followup-defense-patterns  ← 基本的な深掘りへの対処
```

### 2次面接（現場マネージャー、部長）

**評価軸**: 業務理解・職種へのフィット・チームで動けるか

```
使用スキル（優先順）:
1. skeptical-interviewer               ← 現場目線の深掘り質問を生成
2. interview/role-why-us-answer-patterns ← 「なぜこの職種か」の強化
3. interview/gakuchika-answer-patterns  ← 3分版を準備（具体性増）
4. interview/followup-defense-patterns  ← 現場業務への深掘り対処
```

### 最終面接（役員・経営幹部）

**評価軸**: 経営理念への共感・長期コミット・なぜここか

```
使用スキル（優先順）:
1. stages/final-interview-depth-mode   ← 最終面接の特有質問5問
2. interview/rebuttal-handling         ← 競合比較・第一志望確認対処
3. interview/motivation-answer-patterns ← 最長バージョン（2分）
4. interview/role-why-us-answer-patterns ← 3階層の最深部まで準備
```

---

## 面接スキルと企業調査の接続

面接回答の品質は企業調査の深さに依存する。以下のルートで接続する。

```
research_brief.md
    │
    ├── 軸7-4（志望動機の核）
    │       ↓
    │   interview/motivation-answer-patterns の「なぜここか」パートに使用
    │
    ├── 軸9-3（エピソード接続マップ）
    │       ↓
    │   interview/gakuchika-answer-patterns の「企業との接続一言フレーズ」に使用
    │
    ├── 軸7-5（反対尋問への一問一答）
    │       ↓
    │   interview/rebuttal-handling の「競合比較」パートに使用
    │
    └── 軸8（エピソード適合マッピング）
            ↓
        skeptical-interviewer の「ガクチカ深掘り」質問生成の根拠
```

---

## 面接スキル追加の基準

新しい職種・面接パターンが発生した場合:

1. **追加基準**: 3社以上の面接で同じパターンの質問が出た場合
2. **格納場所**: `interview/` または `stages/`
3. **作成手順**: `docs/workflow/skill-update-policy.md` → 「面接系スキル」セクション参照

面接フィードバック記録先: `company-info/<企業名>/transcript_*.md`
