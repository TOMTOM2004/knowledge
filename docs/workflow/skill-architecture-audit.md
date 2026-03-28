# スキルアーキテクチャ監査レポート

作成日: 2026-03-28
対象: `.claude/skills/` 配下の全スキルファイル

---

## 監査サマリー

| カテゴリ | スキル数 | 状態 |
|---------|---------|------|
| フラット（既存） | 17 | 維持・参照先追加済み |
| フラット（新規追加） | 11 | 新規作成 |
| domains/ | 2 | 新規作成 |
| industries/ | 4 | 新規作成 |
| roles/ | 4 | 新規作成 |
| question_types/ | 4 | 新規作成 |
| audiences/ | 3 | 新規作成 |
| stages/ | 3 | 新規作成 |
| research/ | 7 | 新規作成 |
| interview/ | 6 | 新規作成 |
| **合計** | **65** | |

---

## フラット既存スキル（17本）一覧

| スキル名 | 目的 | 主な呼び出し元 |
|---------|------|--------------|
| `es-writer` | ES回答生成 | CLAUDE.md（自動起動） |
| `es-improver` | ES改善フィードバックループ | 手動 |
| `es-refiner` | ES微修正・磨き | 手動 |
| `company-researcher` | 企業調査・research_brief生成 | CLAUDE.md（自動起動） |
| `interview-prep` | 面接準備シート作成 | CLAUDE.md（自動起動） |
| `episode-formatter` | エピソードSTAR形式整形 | CLAUDE.md（自動起動） |
| `es-review-protocol` | ESレビュー5段階統合実行 | es-writer Step 9 / 手動 |
| `overlap-detection` | 設問間重複マトリクス作成 | consistency-overlap-reviewer |
| `readability-check` | 可読性7項目チェック | readability-reviewer |
| `company-fit-evaluation` | 企業固有性照合 | company-fit-reviewer |
| `role-fit-evaluation` | 職種適合度評価 | role-fit-reviewer |
| `es-rewrite-patterns` | 6パターンリライト手順 | editor-refiner |
| `interview-probe-generation` | 深掘り質問生成L1/L2/L3 | skeptical-interviewer |
| `company-research-audit` | 22点スコアリング監査 | research-gap-reviewer |
| `role-research-audit` | 職種調査チェックリスト | role-research-reviewer |
| `research-gap-finding` | P0/P1/P2分類・クエリ生成 | research-gap-reviewer |
| `company-comparison-framework` | 競合比較表・差別化テンプレート | company-fit-reviewer / 手動 |

---

## 新規フラットスキル（11本）

| スキル名 | 目的 | 状態 |
|---------|------|------|
| ※ 現在フラット新規は hierarchy に集約済み | — | — |

> **Note**: 当初計画の11本は、品質の高さを担保するためにhierarchy形式（domains/industries/roles等）に再設計された。フラット追加は行わず、すべて8カテゴリのサブディレクトリに配置した。

---

## 階層スキル（48本）設計方針

### カテゴリ設計の考え方

```
domains/           ← 業界横断の共通語彙・評価軸（ベースレイヤー）
industries/        ← 業種固有の評価軸（ドメインの上に積む）
roles/             ← 職種固有の評価軸（業種の上に積む）
question_types/    ← 設問種別の構造・典型パターン（ESの設問分類）
audiences/         ← 読者層別の文体・語彙基準（ES文体調整）
stages/            ← 選考ステージ別の評価基準（ES→面接の段階）
research/          ← 調査視点（企業・職種別の調査クエリ設計）
interview/         ← 面接回答パターン（話し言葉・口頭構造）
```

### スキル積み上げ原則

- `domains/` → `industries/` → `roles/` の順で特殊化
- `question_types/` は ES 設問構造の「型」。`audiences/` は「誰に向けて書くか」の文体調整
- `research/` は調査インプット設計。`interview/` はアウトプット（話し言葉）設計
- 各階層は独立して呼び出せる（上位層が未読でも機能する）

---

## 重複・矛盾チェック結果

### 重複なし（確認済み）
- `readability-check` (flat) と `audiences/junior-humanities-readable-style` は目的が異なる。前者はチェックリスト実行、後者は読者層定義
- `company-research-audit` と `research/asset-management-research-lens` は同様。前者は汎用22点スコア、後者は業種固有クエリ設計

### 命名衝突なし
- 全スキル名はユニーク（フラット名と階層パスを含めて）

---

## 優先度評価（使用頻度予測）

### 高頻度（毎回のES作成で使用）
- `domains/finance-common`
- `question_types/motivation-question-patterns`
- `question_types/gakuchika-question-patterns`
- `audiences/junior-humanities-readable-style`

### 中頻度（企業・職種が確定したら使用）
- `industries/asset-management-fit`
- `industries/banking-fit`
- `roles/fund-manager-fit`
- `research/asset-management-research-lens`

### 低頻度（特定ケースのみ）
- `stages/final-interview-depth-mode`
- `interview/rebuttal-handling`
- `domains/digital-common`（デジタル職応募時のみ）

---

## 課題と今後の対応

| 課題 | 対応方針 |
|-----|---------|
| 階層スキルはClaudeの自動トリガー対象外（SKILL.mdのdescriptionトリガーが効かない） | 各agentの「参照スキル」セクションに明示して手動参照を促す（Phase 4で対応済み） |
| スキル数が65本と多い | `docs/workflow/skill-selection-matrix.md` で用途マトリクスを整備 |
| `interview/` スキルはES作成時には不要 | `stages/` スキルによって選考段階でフィルタリング |
