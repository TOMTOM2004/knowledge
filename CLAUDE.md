# Knowledge ナレッジベース

就職活動・ES執筆・企業調査・面接対策のマルチエージェント知識ベース。

**軽量モードが default。** セッション分割・brief 一次参照・reviewer 段階起動を守る。
詳細 → `docs/workflow/lightweight-mode.md`

---

## 出力スタイル

- 説明は最小限。変更は diff 中心
- 冗長な前置き・要約は省略
- 日本語で会話

---

## ファイル配置の要所

| 種類 | 場所 |
|---|---|
| エピソード / 部品 / 草稿 | `ES/{素材,部品,企業別/作成中}/` |
| 提出済 / 確定版 ES | `ES/企業別/提出済/`, `移行後ES/` |
| 企業調査 brief | `company-info/<企業名>/research_brief.md` |
| 面接調査 / 想定問答（新） | `company-info/<企業名>/interview_{research,qa}_<N>次_<日付>.md` |
| 面接OS設定・生成物 | `company-info/<企業名>/interview-os/{configs,generated,sessions,learning}/` |
| 面接振り返り / transcript | `company-info/<企業名>/{reflection,transcript}_<N>次_<日付>.md` |
| 直前チェックシート | `company-info/<企業名>/interview_direct_prep_<N>次_<日付>.md` |
| 横断ドキュメント | `docs/{interview_patterns,question_bank,am-comparison-framework,application_status,success_record}.md` |
| ペルソナ / スキーマ | `tools/interview_os/`, `docs/schemas/` |
| 運用ドキュメント | `docs/workflow/` |

旧 `interview_prep_*.md` は参照専用（上書き・削除禁止）。

---

## ワークフロー

### ES 作成
1. `company-info/<企業名>/research_brief.md` を読む（**一次参照はこれだけ**。軸7-A 必須）
2. `ES/素材/INDEX.md` でエピソード確認
3. `ES/部品/best_answers.md` でコア回答テンプレ確認
4. es-writer skill で生成
5. 機械チェック: `python tools/checks/es_checker.py`
6. Gate 2: question-fit + readability（草案後）
7. Gate 3: company-fit + role-fit（仕上げ前・別セッション推奨）

全 reviewer 一括禁止。詳細 → `docs/workflow/es-review-flow.md`

### 企業調査
1. `company-info/<企業名>/` 既存資料確認
2. company-researcher skill で生成（軸7-A 必須）
3. `python tools/checks/research_checker.py <企業名>`
4. research-gap-reviewer agent で不足論点確認

### 面接準備（新規企業の3段階＋模擬面接）

**前提**: `research_brief.md` が存在し軸7-A を含むこと。Stage 1-4 はすべて別セッション。

| Stage | skill / agent | 出力 |
|---|---|---|
| 1. 選考調査 | interview-research | `interview_research_<N>次_<日付>.md` |
| 2. 想定問答 | interview-qa | `interview_qa_<N>次_<日付>.md` |
| 3. 本番練習 | skeptical-interviewer (agent) | — |
| 4. 模擬面接OS | interview-session-preparer → interview-debate-orchestrator → interview-learning-updater | `interview-os/{configs,generated,sessions,learning}/` |

詳細 → `docs/workflow/interview-os-design.md`

### 面接後（transcript 活用）

| タイミング | アクション |
|---|---|
| 面接直後（スマホ可） | reflection 手作成・push（`result: pending`） |
| transcript 到着後 | interview-blindspot → 盲点追記 / question-bank-updater → question_bank.md 更新 |
| 次の選考確定後 | interview-next-prep → 引き継ぎ論点追加 / interview-reflect → patterns 更新 |
| 合否確認後 | reflection の `result` 更新、月1 で success-pattern-extractor |
| 面接30分前 | interview-direct-prep → 1枚チェックシート |

reflection テンプレ → `docs/schemas/reflection-template.md`

---

## スキル / エージェント / hook

| 種類 | 役割 | 場所 |
|---|---|---|
| **skill** | 作業手順 | `.claude/skills/<name>/SKILL.md`（description にトリガー語） |
| **agent** | レビュー視点 | `.claude/agents/<name>.md` |
| **hook/check** | 機械チェック | `tools/checks/` |

各 skill / agent の役割・発動条件は個別ファイルの description を正とする。
詳細 → `docs/workflow/agent-usage-guide.md`

---

## 禁止事項

- `company-researcher` を使わず自前 WebSearch で企業調査しない
- `ES/エピソード/` の docx 等の原本を削除・変更しない
- `research_brief.md` を直接書き換えない（skill 経由で更新）
- `interview_prep_*.md`（旧）を削除・変更しない（参照のみ）
- `interview-research` なしで `interview-qa` を起動しない
- `interview-blindspot` を transcript なしで実行しない
- `question-bank-updater` で質問文を要約・意訳しない（逐語記録）
- `reflection_*.md` の `result` を未設定のまま放置しない
- main ブランチに直接 commit・push しない（グローバル hook で物理的にブロック済み）
- `.env`・秘密情報を commit しない

---

## ポインタ

- 軽量モード → `docs/workflow/lightweight-mode.md`
- セッション分割 → `docs/workflow/session-splitting-guide.md`
- 品質ゲート → `docs/workflow/quality-gates.md`
- ES レビューフロー → `docs/workflow/es-review-flow.md`
- 面接スキル設計 → `docs/workflow/interview-skill-design.md`
- 面接OS設計 → `docs/workflow/interview-os-design.md`
- research_brief フロー → `docs/workflow/research-brief-flow.md`
- agent コスト階層 → `docs/workflow/agent-cost-tiering.md`
