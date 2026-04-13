---
name: answer-reviewer
description: >
  回答レビュースキル。1つの回答に対して、複数ペルソナ視点での4区分フィードバック・
  人事向け/技術者向け言い換え・回答骨格を生成する。
  「この回答をレビューして」「/answer-reviewer」で起動。
  interview-debate-orchestrator から自動呼び出しされる場合もある。
---

# answer-reviewer スキル

## 責務

**このスキルがやること**: 4区分FB生成 + 言い換え案 + 回答骨格 + フラグ判定  
**このスキルがやらないこと**: 質問生成・セッション進行

---

## Step 0: 入力確認

| 項目 | 必須 | 説明 |
|-----|------|------|
| 質問文 | ✓ | レビュー対象の質問 |
| 回答テキスト | ✓ | レビュー対象の回答 |
| persona_ids | ✓ | 評価するペルソナIDのリスト |
| question_id | — | `Q1` のような識別子（省略時は `Q?`） |
| company | — | 企業名（会社固有性の評価に使用） |

---

## Step 1: ペルソナ別評価

各ペルソナ（`persona_ids` に指定されたもの）の `core_axes`, `dislikes`, `feedback_mode` を読み込み、
以下の観点で評価する:

| 観点 | 内容 |
|-----|------|
| 良い点 | そのペルソナが評価するポイント（最大3つ） |
| 悪い点 | そのペルソナが違和感を持つポイント（最大3つ） |
| 改善案 | 具体的な改善アクション（最大3つ） |
| 言い換え | そのペルソナにとって伝わりやすい表現への変換 |

---

## Step 2: フラグ判定

以下のフラグを `true/false` で判定する:

| フラグ | 判定基準 |
|-------|---------|
| `logic_gap` | 「なぜ」が抜けている・飛躍がある |
| `consistency_issue` | セッション内の他の回答と矛盾している |
| `jargon_risk` | 人事ペルソナには伝わりにくい専門用語が含まれる |
| `company_specificity_low` | 他社でも言えそうな内容になっている |
| `missing_conclusion` | 結論が後ろすぎる・ない |
| `role_ambiguity` | 自分の貢献・役割が曖昧 |

---

## Step 3: 言い換え案の生成

以下2パターンの言い換えを生成する:

**hr_version（人事向け）**:
- 専門用語をなくす
- 結論を先頭に置く
- 業務効果・顧客視点で言い換える

**technical_version（技術者向け）**:
- 具体的な手法・数字を入れる
- 何をなぜ選んだかを明示する

---

## Step 4: 回答骨格の生成

以下の構造で「次回このように答えるべき骨格」を生成する:

```
① 結論（1文）
② 背景（1〜2文）
③ 自分の工夫・行動（具体的に）
④ 成果（数字・事実）
⑤ この企業でどう活きるか（1文）
```

---

## Step 5: 出力

### Markdown形式

```markdown
## <question_id> <ペルソナ名>

### 良い点
- <良い点1>
- <良い点2>

### 悪い点
- <悪い点1>
- <悪い点2>

### 改善案
- <改善案1>
- <改善案2>

### より良い言い回し
**人事向け**: <hr_version>
**技術者向け**: <technical_version>

### 回答骨格
① 結論: ...
② 背景: ...
③ 工夫: ...
④ 成果: ...
⑤ 接続: ...

### フラグ
- logic_gap: true/false
- jargon_risk: true/false
- company_specificity_low: true/false
- missing_conclusion: true/false
```

### JSON形式（`save_json: true` の場合）

```json
{
  "question_id": "Q1",
  "persona_id": "hr_generalist",
  "good_points": ["..."],
  "bad_points": ["..."],
  "improvements": ["..."],
  "better_phrasing": {
    "hr_version": "...",
    "technical_version": "..."
  },
  "answer_skeleton": ["結論", "背景", "工夫", "成果", "接続"],
  "flags": {
    "logic_gap": false,
    "consistency_issue": false,
    "jargon_risk": true,
    "company_specificity_low": true,
    "missing_conclusion": false,
    "role_ambiguity": false
  }
}
```

---

## 品質ガードレール

- 良い点・悪い点は各ペルソナの `core_axes` と `dislikes` に基づいて生成する
- 改善案は「〇〇を△△に変える」という具体的アクション形式で書く
- 言い換えは文章で書く（箇条書き不可）
- 回答骨格は箇条書き・単語のみ（文章化しない。暗記防止のため）
- `company` が指定されている場合、言い換えに企業名を組み込む
