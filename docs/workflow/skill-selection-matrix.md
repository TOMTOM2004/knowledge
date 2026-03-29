# スキル選択マトリクス（軽量モード版）

**原則: 業種 skill は 1つだけ選ぶ。面接 skill と ES skill を同時に積まない。**

詳細: `docs/workflow/lightweight-mode.md`

---

## 使い方

1. 「何をしたいか」でセクションを選ぶ
2. 「業種」「職種」「設問タイプ」から該当するものだけ選ぶ
3. ◎=必須、○=推奨、△=任意、—=読まない

**finance-common と digital-common を同時に読まない。**
**asset-management / banking / securities / digital を同時に読まない。**

---

## ES作成（セッションC）

| skill | AM企業 | 銀行 | 証券 | 運用職 | リサーチ職 | DS職 |
|------|--------|------|------|--------|-----------|------|
| `domains/finance-common` | ◎ | ◎ | ◎ | ◎ | ◎ | △ |
| `domains/digital-common` | — | — | — | — | — | ◎ |
| `industries/asset-management-fit` | ◎ | — | — | ◎ | ◎ | — |
| `industries/banking-fit` | — | ◎ | — | — | — | — |
| `industries/securities-fit` | — | — | ◎ | — | — | — |
| `industries/digital-fit` | — | — | — | — | — | ◎ |
| `roles/fund-manager-fit` | ◎ | — | — | ◎ | — | — |
| `roles/investment-analyst-fit` | △ | — | ◎ | — | ◎ | — |
| `roles/data-science-fit` | — | — | — | — | — | ◎ |
| `roles/dx-consulting-fit` | — | — | — | — | — | △ |
| `audiences/junior-humanities-readable-style` | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ |
| `stages/es-screening-mode` | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ |

**ES 執筆時に interview 系 skill は読まない。**

---

## ES設問タイプ別追加 skill（設問タイプに合わせて 1〜2つ選ぶ）

| 設問タイプ | 対応 skill |
|----------|----------|
| 志望動機 | `question_types/motivation-question-patterns` |
| ガクチカ | `question_types/gakuchika-question-patterns` |
| 強み・弱み | `question_types/strengths-weaknesses-patterns` |
| キャリアビジョン | `question_types/future-vision-patterns` |

---

## 企業調査（セッションA）

| skill | 用途 |
|------|------|
| `company-researcher` ◎ | 必ず使う（自前 WebSearch 禁止） |
| `research/asset-management-research-lens` | AM企業のみ |
| `research/banking-research-lens` | 銀行のみ |
| `research/securities-research-lens` | 証券のみ |
| `research/digital-research-lens` | デジタル職のみ |
| `research/fund-manager-research-lens` | 運用職のみ |
| `research/data-science-research-lens` | DS職のみ |

**調査セッションで ES 系 skill は読まない。**

---

## ES レビュー（段階別）

| Gate | skill / agent | タイミング |
|------|-------------|----------|
| Gate 2 | `readability-check` + `question-fit-reviewer` | 草案後 |
| Gate 3 | `company-fit-evaluation` + `role-fit-evaluation` | 仕上げ前 |
| Gate 4 | `overlap-detection` + `consistency-overlap-reviewer` | 3設問以上 |
| Gate 5 | `skeptical-interviewer` | 面接前のみ |

**`es-review-protocol`（全 reviewer 一括）は第一志望最終提出前のみ。**

---

## 面接準備（セッションE）

| skill | 1次面接 | 2次面接 | 最終 |
|------|--------|--------|------|
| `interview-prep` | ◎ | ◎ | ◎ |
| `stages/first-interview-mode` | ◎ | — | — |
| `stages/final-interview-depth-mode` | — | — | ◎ |
| `interview/motivation-answer-patterns` | ◎ | ○ | △ |
| `interview/gakuchika-answer-patterns` | ◎ | △ | — |
| `interview/followup-defense-patterns` | △ | ◎ | ◎ |
| `interview/rebuttal-handling` | — | ○ | ◎ |
| `interview/role-why-us-answer-patterns` | ◎ | ◎ | ◎ |

**面接セッションで ES 系 skill は読まない。**

---

## 最小 skill セットの例

### アセットマネジメント企業・運用職の志望動機 ES

```
core（es-writer）
+ finance-common
+ asset-management-fit
+ fund-manager-fit
+ motivation-question-patterns
+ junior-humanities-readable-style
+ es-screening-mode
```

### 銀行のガクチカ ES

```
core（es-writer）
+ finance-common
+ banking-fit
+ gakuchika-question-patterns
+ junior-humanities-readable-style
+ es-screening-mode
```

### デジタル職の面接想定問答

```
core（interview-prep）
+ digital-common
+ digital-fit
+ data-science-fit（DS職の場合）
+ followup-defense-patterns
+ rebuttal-handling
+ first-interview-mode or final-interview-depth-mode
```

---

## クイックリファレンス（目的別最短経路）

### 「ESを最初から書く（AM企業・運用職）」
```
es-writer → finance-common + asset-management-fit + fund-manager-fit
          + motivation or gakuchika + junior-humanities + es-screening-mode
```

### 「ES 草案を素早く確認」
```
question-fit-reviewer + readability-reviewer のみ
```

### 「提出前の最終チェック（重要企業）」
```
company-fit-reviewer + role-fit-reviewer + consistency-overlap-reviewer
→ editor-refiner（修正）
```

### 「1次面接を翌日に控えた準備」
```
interview-prep → first-interview-mode
+ motivation-answer-patterns + gakuchika-answer-patterns
→ skeptical-interviewer
```

### 「最終面接（経営幹部）の前日準備」
```
final-interview-depth-mode + rebuttal-handling
+ role-why-us-answer-patterns → skeptical-interviewer
```
