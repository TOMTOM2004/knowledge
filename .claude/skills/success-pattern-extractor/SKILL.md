---
name: success-pattern-extractor
description: >
  result: passed がついた全 ES・reflection から通過パターンを抽出し、
  ES/部品/best_answers.md に「実績あり」タグ付きで反映、
  docs/interview_patterns.md と docs/success_record.md を更新するスキル。
  「通過パターンを抽出して」「成功実績を反映して」「/success-pattern-extractor」で起動。
  定期的（月1程度）に手動実行する。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# success-pattern-extractor スキル

## 責務

**このスキルがやること**: passed ES・reflection の横断分析・共通パターン抽出・best_answers.md への実績タグ付け・interview_patterns.md / success_record.md 更新  
**このスキルがやらないこと**: ES の新規生成（→ es-writer が担当）・個別面接の盲点検出（→ interview-blindspot が担当）

---

## Step 0: 入力確認

対象範囲を確認する。デフォルトは全社・全ステップ。

---

## Step 1: passed ファイルの収集

### 1-1. ES（passed）の収集

`移行後ES/<企業名>.md` のフロントマターを確認し、`result: passed` のファイルを収集する。
フロントマターが存在しないファイルは「`result` 未設定」として警告リストに追加する。

### 1-2. reflection（passed）の収集

`company-info/*/reflection_*.md` のフロントマターを確認し、`result: passed` のファイルを収集する。

---

## Step 2: 通過 ES のパターン分析

収集した passed ES を横断分析する。

- **使用エピソードの傾向**: 複数の passed ES で共通して使われたエピソードを抽出
- **志望動機の構造パターン**: 通過した志望動機の共通軸・導入パターンを分析
- **自己PR・強みの表現パターン**: 通過した自己PR で共通して使われた表現を分析

---

## Step 3: 通過 reflection のパターン分析

収集した passed reflection から面接通過に共通するパターンを分析する。

| 成功パターン | 出現回数 | 通過企業・ステップ |
|-----------|---------|---------------|
| <パターン> | N | ... |

---

## Step 4: best_answers.md への実績タグ付け

Step 2・3 の分析結果を踏まえ、`ES/部品/best_answers.md` の該当回答に実績タグを追加する。

**追加するタグの形式**:
```
✅ 実績あり（<企業名>通過 YYYY-MM-DD）
```

**タグ付け基準**:
- その回答（またはそのエピソード）を使って `result: passed` が確認された場合のみ付与
- 推測・間接的な関連での付与は禁止

---

## Step 5: プレビュー提示

更新内容のプレビューを出力する。ファイルにはまだ保存しない。

```
## success-pattern-extractor 更新プレビュー

実行日: YYYY-MM-DD
対象 passed ファイル:
- passed ES: N件
- passed reflection: M件
- result 未設定（警告）: K件

### best_answers.md への実績タグ追加（N件）

### interview_patterns.md への追記（成功パターン N件）

### success_record.md への追記（N件）
```

警告リスト（result 未設定ファイル）を合わせて表示し、ユーザーに設定を促す。
ユーザーに確認を求める。承認後 Step 6 へ進む。

---

## Step 6: 保存

承認後、以下の3ファイルを更新する:

1. `ES/部品/best_answers.md` — 実績タグの追記
2. `docs/interview_patterns.md` — 成功パターンの追記
3. `docs/success_record.md` — 通過実績と集計サマリーの更新

```
保存完了:
- ES/部品/best_answers.md（実績タグ N件追記）
- docs/interview_patterns.md（成功パターン N件追記）
- docs/success_record.md（通過実績 N件記録）
```

---

## 品質ガードレール

- `result: passed` が明示されていないファイルには実績タグを付与しない
- `result` 未設定ファイルは警告として列挙し、ユーザーに設定を促す
- best_answers.md の回答本文は変更しない（タグの追記のみ）
- interview_patterns.md・success_record.md の既存内容は削除しない（追記のみ）
