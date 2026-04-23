# interview-session-preparer — 実行手順

SKILL.md から参照される詳細手順。

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

- デフォルト:
  - 金融2次: `[hr_generalist, finance_front, finance_manager, common_critic]`
  - テック2次: `[hr_generalist, tech_field, tech_manager, common_critic]`
  - 最終: `[hr_generalist, final_interviewer, common_critic]`

---

## Step 2: 入力ファイルの読み込み（並列）

1. `company-info/<企業名>/research_brief.md` — 軸1・軸2・軸3・軸7-A を抽出
2. `company-info/<企業名>/interview_prep_*.md` — 最新ファイル（複数あれば全て）
3. 指定された `ES/md/<ファイル>.md` — エピソードを確認
4. `ES/components/best_answers.md` — コア回答テンプレを確認
5. `tools/interview_os/personas/<persona_id>.yaml` — 選定ペルソナ分を全て読む

ファイルが存在しない場合: `【警告】<ファイルパス> が見つかりません。スキップして続行しますか？`

---

## Step 3: 質問候補の生成

### 3-1. 基本質問（固定）

- 自己PR（1分で）
- 学生時代に最も力を入れたこと（ガクチカ）
- 志望動機
- なぜこの会社か（競合比較）
- なぜこのコース/職種か
- 強みと弱み
- 将来のキャリアイメージ

### 3-2. 会社固有質問

`research_brief.md` の軸1（最重要課題）・軸2（コース業務）・軸7-A（核心固有性）から3〜5問生成する。

### 3-3. ペルソナ別深掘り候補

各ペルソナの `probe_styles` に基づき、基本質問・会社固有質問それぞれに深掘り質問を生成する。
深掘りの段数は `session_config.question_policy.depth_level` に従う（デフォルト: 2）。

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

```
## セッション準備: <企業名> <コース> <N>次面接

作成日: YYYY-MM-DD
ペルソナ: <使用ペルソナ一覧>
セッション時間: <N>分
重点テーマ: <テーマ一覧>

---

### 質問リスト（全<N>問）
#### 基本質問 / 会社固有質問 / ランダム質問

### 深掘り展開（抜粋）

### AI議論ログ（上位5件）
```

**逆質問も生成しますか？**（推奨）
→ 「はい」→ `reverse-question-generator` を実行し追記。

---

## Step 6: 保存

**保存先**: `company-info/<企業名>/interview-os/`

| ファイル | 内容 |
|---------|------|
| `configs/session_config_<YYYYMMDD>.yaml` | session_config（記入済み） |
| `generated/questions_<YYYYMMDD>.md` | 質問リスト（Markdown） |
| `generated/questions_<YYYYMMDD>.json` | 質問リスト（JSON） |
| `generated/debate_log_<YYYYMMDD>.md` | AI議論ログ（Markdown） |
| `generated/debate_log_<YYYYMMDD>.jsonl` | AI議論ログ（JSONL） |

保存後:
```
次のステップ:
模擬面接開始 → 「<企業名>の<N>次面接を開始して」
```
