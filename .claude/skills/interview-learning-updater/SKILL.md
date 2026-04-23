---
name: interview-learning-updater
description: >
  面接セッション後の学習ログ更新スキル。実際に聞かれた質問・うまく答えられなかった質問・
  詰まった表現・技術話の境界を learning/ 配下のファイルに追記する。
  「今日の面接の学習ログを更新して」「/interview-learning-updater」で起動。
allowed-tools: Read, Write, Glob
---

# interview-learning-updater スキル

## 前提

knowledge リポジトリのルート: `/Users/ishidatomonori/Desktop/knowledge/`
learning/ の場所: `company-info/<企業名>/interview-os/learning/`

---

## 責務

**このスキルがやること**: セッションログを読み → 弱点パターンを抽出 → learning/ ファイルに追記
**このスキルがやらないこと**: セッション実行・質問生成

---

## Step 0: 入力確認

| 項目 | 必須 | 説明 |
|-----|------|------|
| 企業名 | ✓ | |
| セッションパス | — | 省略時は最新セッションを自動検出 |
| 手動メモ | — | 「今日はここで詰まった」と直接入力してもよい |

---

## Step 1: セッションログの読み込み

以下を読み込む（存在するものだけ）:

1. `sessions/session_<YYYYMMDD>_<HHMM>/metadata.yaml`
2. `sessions/session_<YYYYMMDD>_<HHMM>/feedback/<question_id>_feedback.json` — 全件
3. `sessions/session_<YYYYMMDD>_<HHMM>/answers/<question_id>_answer.md` — 全件

---

## Step 2: 弱点パターンの抽出

| 抽出対象 | 基準 |
|---------|------|
| うまく答えられなかった質問 | `logic_gap: true` または `company_specificity_low: true` かつ `missing_conclusion: true` |
| ジャーゴンリスク表現 | `jargon_risk: true` の回答から具体的な語句を抽出 |
| 会社固有性が弱かった回答 | `company_specificity_low: true` の質問を記録 |
| 実際に聞かれた質問 | 全質問を `observed_questions.md` に追記 |

---

## Step 3: learning/ ファイルへの追記

### observed_questions.md
```markdown
## <企業名> <N>次面接 （YYYY-MM-DD）
- <実際に聞かれた質問>
```

### weak_patterns.md
```markdown
## <企業名> <N>次面接 （YYYY-MM-DD）

### うまく答えられなかった質問
- <質問> → 原因: <フラグから推定>

### ジャーゴンリスク表現
- 「<使ってしまった表現>」→ 人事向け言い換え: 「<hr_version から抜粋>」

### 会社固有性が弱かった回答
- <質問> → 対策: <具体的にどう接続すべきか>
```

### boundary_notes.md
```markdown
## <企業名> <N>次面接 （YYYY-MM-DD）

### 技術話の境界
- <ペルソナ名> には「<表現>」が通じなかった → 「<言い換え>」にすべきだった
```

---

## Step 4: プレビュー提示

追記内容をプレビューで示し確認を求める。承認後に保存する。

---

## Step 5: 保存

- `company-info/<企業名>/interview-os/learning/observed_questions.md`（append）
- `company-info/<企業名>/interview-os/learning/weak_patterns.md`（append）
- `company-info/<企業名>/interview-os/learning/boundary_notes.md`（append）

```
学習ログ更新完了。次回セッション準備時に自動で参照されます。
```

---

## 品質ガードレール

- 既存の記録を上書きしない（append のみ）
- フラグが全て `false` の質問は `observed_questions.md` にのみ記録する
- セッションログがない場合はユーザーの手動入力のみで記録を作成する
