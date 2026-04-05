# Knowledge ナレッジベース — Codex設定

就職活動・ES執筆・企業調査・面接対策のマルチエージェント知識ベース。

**スキルは `.codex/skills/<name>/SKILL.md` の手順に従って実行する。**
**エージェントは `.codex/agents/<name>.md` の手順に従って実行する。**

---

## このリポジトリの目的

- ES品質の向上（多角レビュー・重複抑制・一貫性担保）
- 企業調査・職種調査の不足発見
- 面接深掘り耐性の向上
- 知識の継続的蓄積と改善

---

## ファイルの場所

| 種類 | 場所 |
|-----|------|
| エピソードライブラリ | `ES/md/` （INDEX.md で一覧確認） |
| ES最良回答テンプレ | `ES/components/best_answers.md` |
| ES草稿 | `ES/drafts/<企業名>.md` |
| 提出済みES | `ES/submitted/<企業名>.md` |
| 確定版ES | `移行後ES/<企業名>.md` |
| 企業調査 | `company-info/<企業名>/research_brief.md` |
| 面接準備 | `company-info/<企業名>/interview_prep_*.md` |
| 運用ドキュメント | `docs/workflow/` |
| チェックスクリプト | `tools/checks/` |
| スキル手順 | `.codex/skills/<name>/SKILL.md` |
| エージェント手順 | `.codex/agents/<name>.md` |

---

## ES作成時の参照順序

1. `company-info/<企業名>/research_brief.md` — 一次参照はこれだけ
2. `ES/md/INDEX.md` — 使えるエピソードを確認
3. `ES/components/best_answers.md` — コア回答テンプレを確認
4. `.codex/skills/es-writer/SKILL.md` の手順に従って生成
5. 機械チェック: `python tools/checks/es_checker.py`
6. Gate 2: question-fit + readability（草案後）→ `.codex/agents/` の手順に従う
7. Gate 3: company-fit + role-fit（仕上げ前）→ `.codex/agents/` の手順に従う

---

## 企業調査時の参照順序

1. `company-info/<企業名>/` フォルダを確認（既存資料があるか）
2. `.codex/skills/company-researcher/SKILL.md` の手順に従って調査・生成
3. チェック: `python tools/checks/research_checker.py <企業名>`
4. `.codex/agents/research-gap-reviewer.md` の手順に従って不足論点を確認

---

## スキル / エージェントの使い分け

| 種類 | 役割 | 使う場面 |
|-----|------|---------|
| **skill** | 手順（作業を実行する） | ES作成・企業調査・エピソード整形等 |
| **agent** | 視点（評価・レビューする） | ESレビュー・調査品質確認・深掘り質問生成 |

### 主なスキル（`.codex/skills/` 配下）
- `company-researcher` — 企業調査（必ずこのスキル経由。自前WebSearch禁止）
- `es-writer` — ES作成
- `interview-research` — 面接調査専門（体験記収集・重要度分類）← 新規
- `interview-qa` — 想定問答生成専門（重要度別回答骨格・詰められ・逆質問）← 新規
- `interview-prep` — 旧面接準備（既存ファイル参照専用。新規企業には使わない）
- `es-review-protocol` — ES全体レビュー（第一志望最終提出前のみ）
- `es-refiner` — 提出済みESからfoundations更新
- `es-improver` — 編集差分からes-writerを自動改善

### 主なエージェント（`.codex/agents/` 配下）
- `question-fit-reviewer` — 設問適合（最優先）
- `readability-reviewer` — 可読性
- `company-fit-reviewer` — 企業固有性
- `role-fit-reviewer` — 職種適合
- `consistency-overlap-reviewer` — 重複・一貫性
- `editor-refiner` — 改善文案生成
- `research-gap-reviewer` — 企業調査の不足発見
- `skeptical-interviewer` — 面接深掘り質問生成

---

## 禁止事項

- `company-researcher` スキルを使わず自前でWeb検索して企業調査しない
- `ES/エピソード/` の docx 等の原本ファイルを削除・変更しない
- `research_brief.md` を直接書き換えない（スキル経由で更新する）
- `interview_prep_*.md`（旧フォーマット）を削除・変更しない（参照のみ）
- `interview-research` なしで `interview-qa` を実行することを推奨しない
- main ブランチに直接コミット・push しない
- `.env` や秘密情報をコミットしない

---

## 出力スタイル

- 説明は最小限。変更はdiff中心で示す
- 冗長な前置き・要約は省略する
- 日本語で会話する

---

## 注記: Claude Code との差異

- Claude Code の hooks/settings.json は非対応。自動トリガーは手動実行に読み替える
- `mcp__memory__` ツールは使用不可。知識記録は `.codex/lessons.md` で管理する
- スキルは Skill ツールではなく、`.codex/skills/<name>/SKILL.md` を読んで手順に従う
