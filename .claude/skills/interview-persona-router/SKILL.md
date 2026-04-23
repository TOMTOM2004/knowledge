---
name: interview-persona-router
description: >
  業界・面接段階・重点テーマに応じてペルソナセットを選定するスキル。
  interview-session-preparer の内部で自動呼び出される。
  単独で「ペルソナ選定だけしてほしい」場合にも使用可能。
allowed-tools: Read
---

# interview-persona-router スキル

## 前提

ペルソナ定義ファイルの場所: `/Users/ishidatomonori/Desktop/knowledge/tools/interview_os/personas/<persona_id>.yaml`

---

## 責務

**このスキルがやること**: 入力条件からペルソナIDリストを決定する
**このスキルがやらないこと**: 質問生成・セッション実行

---

## ルーティングロジック

### 1. 業界 × 段階による基本セット

| industry | stage | デフォルトペルソナセット |
|----------|-------|----------------------|
| finance | 1st | `[hr_generalist, finance_front, common_critic]` |
| finance | 2nd | `[hr_generalist, finance_front, finance_manager, common_critic]` |
| finance | final | `[hr_generalist, finance_manager, final_interviewer, common_critic]` |
| tech | 1st | `[hr_generalist, tech_field, common_critic]` |
| tech | 2nd | `[hr_generalist, tech_field, tech_manager, common_critic]` |
| tech | final | `[hr_generalist, tech_manager, final_interviewer, common_critic]` |
| consulting | 1st | `[hr_generalist, common_critic]` |
| consulting | 2nd | `[hr_generalist, tech_manager, common_critic]` |
| consulting | final | `[hr_generalist, final_interviewer, common_critic]` |
| am | 1st | `[hr_generalist, am_business, common_critic]` |
| am | 2nd | `[hr_generalist, am_business, am_fund_manager, common_critic]` |
| am | final | `[hr_generalist, am_fund_manager, final_interviewer, common_critic]` |
| other | any | `[hr_generalist, common_critic]` |

### 2. focus_themes による調整

| テーマキーワード | 追加・調整 |
|----------------|----------|
| 「人事向け」「わかりやすく」 | `hr_generalist` のウェイトを上げる（複数回評価） |
| 「技術話を薄める」 | `tech_field` を除外 または `hr_generalist` で追加評価 |
| 「深掘り耐性」「詰められ対策」 | `common_critic` の `intervention_threshold` を下げる（0.5） |
| 「最終面接対策」 | `final_interview_mode: true` にする |

### 3. 出力形式

```yaml
selected_personas:
  - hr_generalist
  - finance_front
  - finance_manager
  - common_critic
routing_reason: "industry=finance, stage=2nd → デフォルトセット"
adjustments: []
```

---

## 品質ガードレール

- `common_critic` は常に含める（除外不可）
- 最終面接では `final_interviewer` を必ず含める
- ペルソナ数は最大4つまで推奨（5つ以上はセッションが重くなる）
