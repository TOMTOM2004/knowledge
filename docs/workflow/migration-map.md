# 移行マップ

旧ディレクトリ構成と目標構成の対応表。

> **現状**: 既存ファイルは移動していません。このマップは将来の移行計画です。
> 実際に移行する場合は、ファイルを移動した後にこの表を「完了」に更新してください。

---

## ファイル移行対応表

| 旧パス | 新パス（目標） | 優先度 | 状態 |
|--------|--------------|--------|------|
| `ES/素材/` | `ES/素材/`（変更なし）| - | 維持 |
| `ES/エピソード/` | `ES/エピソード/`（変更なし） | 低 | 維持 |
| `ES/部品/` | `ES/部品/`（変更なし） | - | 維持 |
| `ES/企業別/作成中/` | `ES/企業別/作成中/`（変更なし） | - | 維持 |
| `ES/企業別/提出済/` | `ES/企業別/提出済/`（変更なし） | - | 維持 |
| `ES/自己分析マインドマップ.md` | `docs/references/self-analysis-mindmap.md` | 中 | 未移行 |
| `ES/changelog.md` | `ES/changelog.md`（変更なし） | - | 維持 |
| `移行後ES/` | `移行後ES/`（変更なし） | - | 維持 |
| `company-info/` | `company-info/`（変更なし） | - | 維持 |
| `transcripts/others/` | `transcripts/others/`（変更なし） | - | 維持 |

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

## 将来の移行計画（優先度付き）

### Phase A（緊急性低・任意）
以下は将来的に整理したい項目ですが、既存の運用を壊さないために後回し:

1. `ES/自己分析マインドマップ.md` → `docs/references/self-analysis-mindmap.md`
   - 理由: ESの作業ファイルではなく参照資料のため

2. `ES/CLAUDE.md` の内容をルート `CLAUDE.md` または `docs/references/es-guidelines.md` に統合
   - 理由: CLAUDE.mdが2箇所に分散しているため

### Phase B（将来の大規模整理時）
ディレクトリを全面的に再編する場合の対応:

| 旧 | 新 |
|---|---|
| `ES/企業別/作成中/` | `es/drafts/` |
| `ES/企業別/提出済/` | `es/submitted/` |
| `ES/部品/` | `es/components/` |
| `移行後ES/` | `es/final/` |
| `company-info/` | `data/companies/` |
| `ES/素材/` | `data/episodes/` |

> **注意**: Phase Bは大規模な変更になるため、スキル内のパス参照をすべて更新する必要があります。
> 既存スキルの `es-writer`・`episode-formatter`・`es-refiner` などが特定パスを参照しているため、
> 移行前に全スキルのパス参照をチェックしてください。
