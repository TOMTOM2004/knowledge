---
name: interview-session-preparer
description: >
  模擬面接セッションの準備スキル。企業名・面接段階・コースを入力に、
  session_config.yaml を作成し、質問候補セット・AI議論ログを生成・保存する。
  「<企業名>の<N>次面接セッションを準備して」「/interview-session-preparer」で起動。
---

# interview-session-preparer スキル

## 責務

**このスキルがやること**: session_config 作成 → 入力ファイル読み込み → 質問候補生成 → 議論ログ生成 → 保存  
**このスキルがやらないこと**: 実際の模擬面接実行（→ interview-debate-orchestrator が担当）

---

## Step 0: 入力確認

以下を確認する。不明な場合はユーザーに質問する。

| 項目 | 必須 | 例 |
|-----|------|-----|
| 企業名 | ✓ | りそなグループ |
| 面接段階 | ✓ | 1次 / 2次 / 最終 |
| コース・職種 | — | データサイエンス |
| 使用するESファイル | ✓ | （省略時は ES/md/INDEX.md から相談） |
| 重点テーマ | — | 例: 人事向けに分かりやすく話す |
| セッション時間（分） | — | 30（デフォルト） |
| ペルソナセット | — | 省略時は業界・段階から自動選択 |

---

## Step 1: ペルソナセット選定

`interview-persona-router` スキルのロジックに従い、ペルソナセットを決定する。

- 入力が省略された場合は以下のデフォルトを使用:
  - 金融2次: `[hr_generalist, finance_front, finance_manager, common_critic]`
  - テック2次: `[hr_generalist, tech_field, tech_manager, common_critic]`
  - 最終: `[hr_generalist, final_interviewer, common_critic]`

---

## Step 2: 入力ファイルの読み込み（並列）

以下を並列で読み込む。

1. `company-info/<企業名>/research_brief.md` — 軸1・軸2・軸3・軸7-A を抽出
2. `company-info/<企業名>/interview_prep_*.md` — 最新ファイル（複数あれば全て）
3. 指定された `ES/md/<ファイル>.md` — エピソードを確認
4. `ES/components/best_answers.md` — コア回答テンプレを確認
5. `tools/interview_os/personas/<persona_id>.yaml` — 選定ペルソナ分を全て読む

ファイルが存在しない場合: `【警告】<ファイルパス> が見つかりません。スキップして続行しますか？` と表示し確認する。

---

## Step 3: 質問候補の生成

### 3-1. 基本質問（固定）

以下を必ず含める:

- 自己PR（1分で）
- 学生時代に最も力を入れたこと（ガクチカ）
- 志望動機
- なぜこの会社か（競合比較）
- なぜこのコース/職種か
- 強みと弱み
- 将来のキャリアイメージ

### 3-2. 会社固有質問

`research_brief.md` の軸1（最重要課題）・軸2（コース業務）・軸7-A（核心固有性）から3〜5問生成する。

生成例:
- 「なぜ競合ではなく当社を選んだのか（軸7-A を使って）」
- 「当社の〇〇という課題に対して、あなたはどう関わりたいか」
- 「このコースの業務のどの部分で力を発揮できると思うか」

### 3-3. ペルソナ別深掘り候補

各ペルソナの `probe_styles` に基づき、基本質問・会社固有質問それぞれに深掘り質問を生成する。
深掘りの段数は `session_config.question_policy.depth_level` に従う（1=1段, 2=2段, 3=3段）。
`depth_level` が省略されている場合は 2 をデフォルトとして使用する。

形式:
```
Q: <基本・会社固有質問>
  └─ [<persona_id>] 1段目深掘り: <質問>
  └─ [<persona_id>] 2段目深掘り: <質問>
```

### 3-4. ランダム質問（1問）

`question_policy.randomness` が `one_random_question` の場合、以下からランダムで1問選ぶ:

- 最近気になったニュース・出来事は？
- 趣味・特技を教えてください
- あなたの強みが逆に弱みになった経験は？
- 学生時代に最も後悔していることは？
- 自分を動物に例えると何ですか？（理由も含めて）
- 30秒で自分を売り込んでください

---

## Step 4: AI議論ログの生成

各ペルソナの視点から「次に聞くべき質問」の候補を議論形式で生成する。

JSONL形式（1行1件）:
```json
{"turn": 1, "agent": "<persona_id>", "candidate_question": "<質問>", "reason": "<理由>", "priority": 0.85}
```

`common_critic` は最後に全体を評価し、差し込みが必要な問題点があれば追記する:
```json
{"turn": N, "agent": "common_critic", "detected_issues": ["..."], "intervention_required": true, "reason": "..."}
```

---

## Step 5: プレビュー提示

以下の形式でプレビューを出力する。ファイルにはまだ保存しない。

```
## セッション準備: <企業名> <コース> <N>次面接

作成日: YYYY-MM-DD
ペルソナ: <使用ペルソナ一覧>
セッション時間: <N>分
重点テーマ: <テーマ一覧>

---

### 質問リスト（全<N>問）

#### 基本質問
1. ...

#### 会社固有質問
N. ...

#### ランダム質問
N+1. ...

---

### 深掘り展開（抜粋）
...

---

### AI議論ログ（上位5件）
...
```

ユーザーに確認を求める。修正があれば反映してから Step 6 へ。

**逆質問も生成しますか？**（推奨）
→ 「はい」と答えると `reverse-question-generator` を実行し、質問リストの末尾に逆質問セクションを追記する。
→ 「いいえ」の場合はそのまま Step 6 へ。

---

## Step 6: 保存

承認後、以下のファイルを保存する。

**保存先ベースディレクトリ**: `company-info/<企業名>/interview-os/`

| ファイル | 内容 |
|---------|------|
| `configs/session_config_<YYYYMMDD>.yaml` | session_config（記入済み） |
| `generated/questions_<YYYYMMDD>.md` | 質問リスト（Markdown） |
| `generated/questions_<YYYYMMDD>.json` | 質問リスト（JSON） |
| `generated/debate_log_<YYYYMMDD>.md` | AI議論ログ（Markdown） |
| `generated/debate_log_<YYYYMMDD>.jsonl` | AI議論ログ（JSONL） |

保存後:
```
保存完了:
  - configs/session_config_<YYYYMMDD>.yaml
  - generated/questions_<YYYYMMDD>.md/.json
  - generated/debate_log_<YYYYMMDD>.md/.jsonl

次のステップ:
模擬面接開始 → 「<企業名>の<N>次面接を開始して」または /interview-debate-orchestrator
```

---

## 品質ガードレール

- `research_brief.md` なしで実行する場合は `【警告】` タグをつけて確認する
- 会社固有質問は最低3問生成する（research_brief がある場合）
- 基本質問の深掘りは全ペルソナ分を網羅する
- ランダム質問は毎回ランダムに選ぶ（前回と同じにならないよう配慮する）
