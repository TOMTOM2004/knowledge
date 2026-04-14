---
name: interview-learning-updater
description: >
  面接セッション後の学習ログ更新スキル。実際に聞かれた質問・うまく答えられなかった質問・
  詰まった表現・技術話の境界を learning/ 配下のファイルに追記する。
  「今日の面接の学習ログを更新して」「/interview-learning-updater」で起動。
---

# interview-learning-updater スキル

## 責務

**このスキルがやること**: セッションログを読み → 弱点パターンを抽出 → learning/ ファイルに追記  
**このスキルがやらないこと**: セッション実行・質問生成

---

## Step 0: 入力確認

| 項目 | 必須 | 説明 |
|-----|------|------|
| 企業名 | ✓ | |
| セッションパス | — | 省略時は最新セッションを自動検出 |
| 手動メモ | — | ユーザーが直接「今日はここで詰まった」と入力してもよい |

---

## Step 1: セッションログの読み込み

以下を読み込む（存在するものだけ）:

1. `sessions/session_<YYYYMMDD>_<HHMM>/metadata.yaml`
2. `sessions/session_<YYYYMMDD>_<HHMM>/feedback/<question_id>_feedback.json` — 全件
3. `sessions/session_<YYYYMMDD>_<HHMM>/answers/<question_id>_answer.md` — 全件

---

## Step 2: 弱点パターンの抽出

以下の基準で抽出する:

| 抽出対象 | 基準 |
|---------|------|
| うまく答えられなかった質問 | フラグ `logic_gap: true` または `company_specificity_low: true` かつ `missing_conclusion: true` |
| ジャーゴンリスクが高い表現 | フラグ `jargon_risk: true` の回答から具体的な語句を抽出 |
| 会社固有性が弱かった回答 | フラグ `company_specificity_low: true` の質問を記録 |
| 実際に聞かれた質問 | 全質問を `observed_questions.md` に追記 |

---

## Step 3: learning/ ファイルへの追記

### observed_questions.md

```markdown
## <企業名> <N>次面接 （<YYYY-MM-DD>）

- <実際に聞かれた質問1>
- <実際に聞かれた質問2>
...
```

### weak_patterns.md

フラグに基づき、以下のセクションに追記する:

```markdown
## <企業名> <N>次面接 （<YYYY-MM-DD>）

### うまく答えられなかった質問
- <質問> → 原因: <フラグから推定>

### ジャーゴンリスク表現
- 「<使ってしまった表現>」→ 人事向け言い換え: 「<hr_version から抜粋>」

### 会社固有性が弱かった回答
- <質問> → 対策: <具体的にどう接続すべきか1文>
```

### boundary_notes.md

技術話の通じ方に関する記録を追記する（手動メモからも生成可）:

```markdown
## <企業名> <N>次面接 （<YYYY-MM-DD>）

### 技術話の境界
- <ペルソナ名> には「<表現>」が通じなかった → 「<言い換え>」にすべきだった
```

---

## Step 4: プレビュー提示

追記内容をプレビューで示し、確認を求める。

```
以下の内容を learning/ に追記します:

[observed_questions.md]
...

[weak_patterns.md]
...

よろしいですか？
```

---

## Step 5: 保存

承認後、各ファイルに追記する。

保存先:
- `company-info/<企業名>/interview-os/learning/observed_questions.md`
- `company-info/<企業名>/interview-os/learning/weak_patterns.md`
- `company-info/<企業名>/interview-os/learning/boundary_notes.md`

保存後:
```
学習ログ更新完了:
  - learning/observed_questions.md
  - learning/weak_patterns.md
  - learning/boundary_notes.md

次回のセッション準備時に自動で参照されます。
```

---

## 品質ガードレール

- 既存の記録を上書きしない（append のみ）
- 手動メモがある場合はそれを優先して記録する
- フラグが全て `false` の質問は `observed_questions.md` にのみ記録し、weak_patterns には追加しない
- セッションログがない場合はユーザーの手動入力のみで記録を作成する
