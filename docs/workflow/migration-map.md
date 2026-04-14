# 移行マップ

ディレクトリ構成の変遷と今後の移行計画をまとめる。

---

## 完了済み移行

### 2026-04-14: ES フォルダ日本語化・企業別統合

| 旧パス | 新パス | 状態 |
|--------|--------|------|
| `ES/components/` | `ES/部品/` | 完了 |
| `ES/md/` | `ES/素材/` | 完了 |
| `ES/drafts/` | `ES/企業別/作成中/` | 完了 |
| `ES/submitted/` | `ES/企業別/提出済/` | 完了 |

- ファイル名は英語のまま据え置き
- 参照更新対象: `CLAUDE.md` / `AGENTS.md` / `.claude・.codex` スキル群 / `tools/interview_os/` / `docs/workflow/`
- 履歴ファイル（`company-info/` 配下・`ES/changelog.md`）は旧パス表記のまま保持

---

## 維持（変更なし）

| パス | 用途 |
|------|------|
| `ES/エピソード/` | docx 元資料（既に日本語） |
| `ES/changelog.md` | ES 作業履歴 |
| `移行後ES/` | 既存配置を維持 |
| `company-info/` | 企業研究資料 |
| `transcripts/others/` | transcript 保管 |

---

## 新設ディレクトリ

| 新設パス | 目的 | 状態 |
|---------|------|------|
| `.claude/agents/` | subagent定義 | **完了（9ファイル）** |
| `.claude/skills/es-review-protocol/` | ESレビュー手順 | **完了** |
| `.claude/skills/overlap-detection/` | 重複検出手順 | **完了** |
| `.claude/skills/readability-check/` | 可読性評価手順 | **完了** |
| `.claude/skills/company-fit-evaluation/` | 企業適合評価手順 | **完了** |
| `.claude/skills/role-fit-evaluation/` | 職種適合評価手順 | **完了** |
| `.claude/skills/es-rewrite-patterns/` | リライトパターン集 | **完了** |
| `.claude/skills/interview-probe-generation/` | 深掘り質問生成手順 | **完了** |
| `.claude/skills/company-research-audit/` | 企業調査監査手順 | **完了** |
| `.claude/skills/role-research-audit/` | 職種調査監査手順 | **完了** |
| `.claude/skills/research-gap-finding/` | 調査ギャップ発見手順 | **完了** |
| `.claude/skills/company-comparison-framework/` | 企業比較フレームワーク | **完了** |
| `.claude/hooks/` | hook README | **完了** |
| `tools/checks/` | 品質チェックスクリプト | **完了** |
| `docs/workflow/` | 運用ドキュメント | **完了** |
| `docs/schemas/` | ファイル形式定義 | 空（今後整備） |
| `docs/references/` | 長文背景知識 | 空（今後整備） |

---

## 将来の移行計画

### Phase A（緊急性低・任意）

1. `ES/自己分析マインドマップ.md` → `docs/references/self-analysis-mindmap.md`
   - 理由: ESの作業ファイルではなく参照資料のため

2. `ES/CLAUDE.md` の内容をルート `CLAUDE.md` または `docs/references/es-guidelines.md` に統合
   - 理由: CLAUDE.mdが2箇所に分散しているため

### Phase B（将来の大規模整理時）

ディレクトリを全面的に再編する場合の対応案:

| 現在 | 将来案 |
|---|---|
| `ES/企業別/作成中/` | `es/drafts/` |
| `ES/企業別/提出済/` | `es/submitted/` |
| `ES/部品/` | `es/components/` |
| `移行後ES/` | `es/final/` |
| `company-info/` | `data/companies/` |
| `ES/素材/` | `data/episodes/` |

> **注意**: Phase B は大規模な変更になるため、スキル内のパス参照をすべて更新する必要がある。
> 既存スキルの `es-writer`・`episode-formatter`・`es-refiner` などが特定パスを参照しているため、
> 移行前に全スキルのパス参照をチェックすること。
