---
name: interview-debate-orchestrator
description: >
  模擬面接の実行スキル。session_config と questions.json を入力に、
  進行役として質問を出し、ユーザー回答に対してペルソナ別評価・共通批評・次質問選択を行う。
  「<企業名>の<N>次面接を開始して」「/interview-debate-orchestrator」で起動。
  interview-session-preparer を先に実行していない場合は警告を出す。
allowed-tools: Read, Write, Glob
---

# interview-debate-orchestrator スキル

## 前提

knowledge リポジトリのルート: `/Users/ishidatomonori/Desktop/knowledge/`
ペルソナ定義: `tools/interview_os/personas/<persona_id>.yaml`

---

## 責務

**このスキルがやること**: 質問表示 → 回答受取 → ペルソナ別評価 → 差し込み判定 → 次質問選択 → FB生成 → ログ保存
**このスキルがやらないこと**: 質問候補の生成（→ interview-session-preparer が担当）

---

## Step 0: 入力確認

| 項目 | 必須 | 説明 |
|-----|------|------|
| session_config.yaml のパス | ✓ | 省略時はユーザーに企業名・日付を聞いて特定 |
| questions.json のパス | ✓ | 省略時は generated/ 配下の最新ファイルを使用 |
| 実行モード | — | `text`（デフォルト）/ `text+audio`（Phase 2） |

`questions.json` が存在しない場合:
```
【警告】質問ファイルが見つかりません。
interview-session-preparer を先に実行してください。続行しますか？
```

---

## Step 1: セッション開始宣言

以下の形式でセッション開始を宣言する:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模擬面接セッション開始
企業: <企業名> | コース: <コース> | 段階: <N>次面接
ペルソナ: <使用ペルソナ一覧>
重点テーマ: <テーマ一覧>
予定質問数: <N>問 / 目標時間: <M>分
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

準備ができたら「開始」と入力してください。
```

---

## Step 2: 質問ループ（1問ごとに繰り返す）

### 2-1. 質問表示

```
【Q<N>】<質問文>

（回答してください。終わったら「完了」と入力してください）
```

### 2-2. 回答受取

ユーザーが回答を入力する。「完了」を受け取ったら評価フェーズへ。

### 2-3. ペルソナ別評価

各ペルソナ（common_critic 以外）が回答を評価する。

評価観点（各ペルソナの `core_axes` に基づく）:
- 良い点（最大3つ）
- 問題点（最大3つ）
- 深掘り候補質問（1〜2問）

### 2-4. common_critic 評価

全ペルソナの評価を踏まえて、以下を判定する:

- 論理飛躍・矛盾の有無
- 差し込み質問の要否（priority ≥ 0.70 なら差し込み）
- 会社固有性の不足

差し込みが必要な場合:
```
【差し込み】<common_critic からの指摘質問>
```

### 2-5. 次質問の選択

以下の優先順で次の質問を選ぶ:

1. common_critic が差し込みを要求した場合 → その質問
2. 深掘り2段目が残っている場合（priority ≥ 0.70）→ 深掘り
3. それ以外 → 次の質問候補から最優先（priority 最大）のものを選ぶ

---

## Step 3: 回答ごとのフィードバック出力

`answer-reviewer` スキルのロジックに従い、コンパクト版 FB を生成する。

```
─── FB: Q<N> ───
[良] <良い点2〜3行>
[課] <改善点2〜3行>
[言] 人事向け: <言い換え案1文>
─────────────────
```

詳細版（完全4区分）はセッション終了後にまとめて出力する。

---

## Step 4: セッション終了

全質問完了またはユーザーが「終了」と入力した時点でセッションを終了する。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
セッション終了
回答済み: <N>問 / 全<M>問
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

その後、詳細FBをまとめて出力する（`answer-reviewer` スキルの4区分形式）。

---

## Step 5: ログ保存

以下のファイルを `sessions/session_<YYYYMMDD>_<HHMM>/` に保存する:

| ファイル | 内容 |
|---------|------|
| `metadata.yaml` | セッションメタ情報 |
| `questions_used.json` | 実際に使った質問と順序 |
| `answers/<question_id>_answer.md` | 各回答テキスト |
| `feedback/<question_id>_feedback.md` | 各回答の詳細FB（Markdown） |
| `feedback/<question_id>_feedback.json` | 各回答の詳細FB（JSON） |

保存後:
```
ログ保存完了: sessions/session_<YYYYMMDD>_<HHMM>/

次のステップ:
弱点記録 → 「今日の面接の学習ログを更新して」または /interview-learning-updater
```

---

## 品質ガードレール

- 質問表示は1問ずつ（先読みさせない）
- 回答評価はユーザー入力後にのみ実行する
- common_critic の差し込みは1セッションで最大3回まで
- セッション中に「スキップ」と入力された場合はその質問を記録してスキップする
- ランダム質問は必ず1問含める
