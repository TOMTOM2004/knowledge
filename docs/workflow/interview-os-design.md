# 面接OS 設計仕様書

最終更新: 2026-04-13

---

## 0. 目的

1. 企業差し替え式で、面接前の想定問答を高精度に生成する
2. 複数ペルソナの視点で深掘り・批評し、回答ごとの改善点を出す
3. 模擬面接ログを蓄積して、次回以降の質問生成と弱点推定に再利用する

主戦場は **2次面接**。面接段階ごとに「聞かれている意図」が違う前提で動く。

---

## 1. 全体アーキテクチャ（5層）

```
Knowledge Layer  →  Config Layer  →  Generation Layer
                                          ↓
                              Simulation Layer  →  Learning Layer
```

| 層 | 役割 | 主なファイル |
|---|------|------------|
| Knowledge | 既存資産を読む（変更しない） | `company-info/`, `ES/`, `移行後ES/` |
| Config | 今回の模擬面接条件を決める | `session_config_YYYYMMDD.yaml` |
| Generation | 質問候補を生成する | スキル: `interview-session-preparer` |
| Simulation | 模擬面接を実行・評価する | スキル: `interview-debate-orchestrator`, `answer-reviewer` |
| Learning | 失敗・弱点を蓄積する | スキル: `interview-learning-updater` |

---

## 2. ディレクトリ構成（既存への追加分のみ）

```
knowledge/
├── company-info/<企業名>/
│   └── interview-os/
│       ├── configs/
│       │   ├── session_config_YYYYMMDD.yaml
│       │   └── persona_set_<industry>_<stage>.yaml  ← 参照のみ
│       ├── generated/
│       │   ├── questions_YYYYMMDD.md
│       │   ├── questions_YYYYMMDD.json
│       │   ├── debate_log_YYYYMMDD.md
│       │   └── debate_log_YYYYMMDD.jsonl
│       ├── sessions/
│       │   └── session_YYYYMMDD_HHMM/
│       │       ├── metadata.yaml
│       │       ├── questions_used.json
│       │       ├── answers/
│       │       ├── feedback/
│       │       └── transcripts/        ← Phase 2以降
│       └── learning/
│           ├── observed_questions.md
│           ├── weak_patterns.md
│           └── boundary_notes.md
│
├── tools/interview_os/
│   ├── session_config_schema.yaml      ← スキーマ定義
│   ├── session_config_template.yaml    ← 記入用テンプレート
│   └── personas/
│       ├── hr_generalist.yaml
│       ├── tech_field.yaml
│       ├── tech_manager.yaml
│       ├── finance_front.yaml
│       ├── finance_manager.yaml
│       ├── common_critic.yaml
│       └── final_interviewer.yaml
│
├── .codex/skills/
│   ├── interview-session-preparer/SKILL.md
│   ├── interview-persona-router/SKILL.md
│   ├── interview-debate-orchestrator/SKILL.md
│   ├── answer-reviewer/SKILL.md
│   └── interview-learning-updater/SKILL.md
│
├── transcripts/mock-interviews/
│   └── session_YYYYMMDD_HHMM/
│
└── logs/interview-os/
    └── session_YYYYMMDD_HHMM/
```

既存ファイルは **読むだけ**。追加のみで構造を壊さない。

---

## 3. 実行フロー

### 3-1. Step 1: prepare-session（セッション準備）

**スキル**: `interview-session-preparer`

| 入力 | 処理 | 出力 |
|-----|------|------|
| 企業名, 面接段階, コース, 使用ES, 重点テーマ, セッション時間, ペルソナセット | research_brief.md + interview_prep + ES群を読み込み → 質問候補生成 → ペルソナ別深掘り生成 → ランダム1問混入 → 議論ログ生成 | session_config.yaml, questions.md/json, debate_log.md/jsonl |

### 3-2. Step 2: run-session（模擬面接実行）

**スキル**: `interview-debate-orchestrator` + `answer-reviewer`

| 入力 | 処理 | 出力 |
|-----|------|------|
| session_config.yaml, questions.json, 使用ペルソナ, 実行モード | 進行役が質問表示 → ユーザー回答 → ペルソナ別評価 → 共通批評AI差し込み判定 → 次質問選択 → FB生成 → ログ保存 | feedback.md/json, 回答ログ |

---

## 4. ペルソナ設計

### 4-1. 原則

人格模倣ではなく **役割 + 業界差分 + 面接段階差分** で設計。固定するのは:
- 何を見ているか
- 何に違和感を持つか
- どう深掘りするか
- どの説明レベルを求めるか

### 4-2. ペルソナ一覧

| ID | 名称 | 重点軸 | technical_tolerance |
|----|------|--------|-------------------|
| `hr_generalist` | 人事（非技術）| 分かりやすさ・一貫性・人柄 | low |
| `tech_field` | テック現場 | 実務理解・再現性・思考の筋道 | high |
| `tech_manager` | テック中堅/管理寄り | 成長可能性・現場接続（成長7:実務3） | medium |
| `finance_front` | 金融営業現場 | 顧客理解・伝わるか・実務接続 | low |
| `finance_manager` | 金融中堅/管理寄り | 伸びしろ・会社理解・中長期視点（成長7:実務3） | low |
| `common_critic` | 共通批評AI | 論理飛躍・矛盾・差し込み要否判定 | — |
| `final_interviewer` | 最終面接 | 一貫性・価値観・判断力・斜め質問 | medium |

### 4-3. ペルソナ適用パターン

```yaml
金融2次:  [hr_generalist, finance_front, finance_manager, common_critic]
テック2次: [hr_generalist, tech_field, tech_manager, common_critic]
最終:     [hr_generalist, final_interviewer, common_critic]
```

---

## 5. 質問生成ロジック（4種類）

| 種類 | 生成元 | 深掘りレベル |
|-----|--------|------------|
| 基本質問 | 固定テンプレ | ペルソナ別2段 |
| 会社固有質問 | `research_brief.md` | ペルソナ別2段 |
| 深掘り質問 | 各回答に対して動的生成 | — |
| ランダム質問 | 毎回1問だけ混入 | — |

**深掘り型テンプレ**: 具体化要求 / 数字要求 / 役割切り分け / 再現性確認 / 他社比較 / 弱点露出 / 一貫性確認

**ランダム型テンプレ**: 趣味・特技 / 最近気になったこと / 強みが逆に弱みに出る場面 / 失敗時の説明 / 30秒で言うと何か

---

## 6. フィードバック仕様（4区分固定）

各回答ごとに以下を出力する:

```
## Q<N> <ペルソナ名>

### 良い点
### 悪い点
### 改善案
### より良い言い回し
  - hr_version（人事向け）
  - technical_version（技術者向け）
```

JSON構造は `tools/interview_os/session_config_schema.yaml` の feedback スキーマを参照。

---

## 7. ログ仕様

### 7-1. 回答ごとの記録項目（Phase 1）

- `question_id`, `persona_id`, `question_text`
- `answer_text`（テキスト入力）
- `evaluator_comments`, `suggested_better_phrasing`
- `logical_gaps`, `consistency_flags`, `jargon_flags`, `company_specificity_flags`

Phase 2 追加: `answer_audio_path`, `answer_raw_transcript`, `response_latency_sec`, `time_to_conclusion_sec`, `speech_rate`, `silence_segments`

### 7-2. AI議論ログ（JSONL 1行1件）

```json
{"turn": 1, "agent": "finance_manager", "candidate_question": "...", "reason": "...", "priority": 0.82}
```

### 7-3. セッションメタ情報（metadata.yaml）

企業名 / コース / 面接段階 / 使用ES / 重点テーマ / 日時 / ペルソナ構成 / 総質問数

---

## 8. Phase設計

### Phase 1（現在）
- テキストのみ
- 企業差し替え式の質問生成
- 多エージェント議論ログ
- 回答ごとの4区分フィードバック

### Phase 2（次）
- AI質問読み上げ
- 回答録音 + 逐語/整形 transcript（Whisper系 ASR）
- 話速 / 沈黙 / 結論到達時間の計測
- 人事向け/技術者向け言い換え強化

### Phase 3（理想）
- よりリアルタイムなターン制
- 音声読み上げの自然化
- 質問差し込みの即時性向上

---

## 9. 蓄積設計（Learning Layer）

優先順位:
1. 実際に聞かれた質問 → `observed_questions.md`
2. うまく答えられなかった質問 → `weak_patterns.md`
3. 詰まった時間・表現 → `weak_patterns.md`
4. 技術話が通じなかった境界 → `boundary_notes.md`

スキル: `interview-learning-updater` でセッション後に追記。

---

## 10. スキル設計方針

Claude Codeスキルとして `.codex/skills/<name>/SKILL.md` に実装。
Pythonスクリプトは Phase 2（transcript/timing処理）で必要になったタイミングで追加する。

| スキル | トリガー例 |
|-------|----------|
| `interview-session-preparer` | `/interview-session-preparer`, 「りそなの2次面接セッションを準備して」 |
| `interview-persona-router` | セッション準備内で自動呼び出し |
| `interview-debate-orchestrator` | `/interview-debate-orchestrator`, 「模擬面接を開始して」 |
| `answer-reviewer` | `/answer-reviewer`, 「この回答をレビューして」 |
| `interview-learning-updater` | `/interview-learning-updater`, 「今日の面接の弱点を記録して」 |
