---
name: es-review-protocol
description: ESレビューの共通手順。複数のreviewerエージェントを順番に呼び出し、総合レビューレポートを生成する。
---

# es-review-protocol

## 目的
ES全体のレビューを体系的に実施するための共通手順。
単発レビューではなく、複数視点から総合的に評価する際に使う。

## 使う場面
- ESが完成して提出前の最終チェックをしたいとき
- 「このESを全体的にレビューして」と依頼されたとき
- 複数設問を一括でレビューしたいとき

## 入力
- ESファイルパス（必須）
- 企業名（必須）
- 志望職種（必須）
- レビュー優先度（optional: 全体/可読性/企業適合/設問適合）

## 出力
- 総合レビューレポート（Markdown）
- 優先修正事項トップ5
- 各reviewer評価サマリー

## 手順

### Step 1: 前提確認
- 対象ESファイルを読み込む
- company-info/<企業名>/research_brief.md を読み込む（存在する場合）
- 設問数・各設問の字数制限を確認する

### Step 2: 個別レビュー実施（優先度順）
以下の順番でレビューを実施する:

1. **question-fit-reviewer**: 設問適合性（最優先）
2. **readability-reviewer**: 可読性
3. **company-fit-reviewer**: 企業適合性（research_briefが必要）
4. **role-fit-reviewer**: 職種適合性
5. **consistency-overlap-reviewer**: 一貫性・重複

### Step 3: 統合レポート生成
各reviewerの結果を統合し、以下の形式でレポートを作成する:

```
## ES総合レビューレポート
### 対象: [企業名] [職種名]
### 評価日: YYYY-MM-DD

#### 総合評価: [A/B/C/D]
- 提出判断: [提出可/修正後提出/大幅修正必要]

#### 優先修正事項（上位5件）
1. [最重要修正]
2. ...

#### reviewer別評価サマリー
| reviewer | 評価 | 主な指摘 |
|---|---|---|
| 設問適合 | ◎/○/△/✗ | ... |
| 可読性 | ◎/○/△/✗ | ... |
...
```

### Step 4: editor-refiner へ連携
修正が必要な場合、editor-refinerエージェントに統合レポートを渡す。

## 更新方針
面接後のフィードバックや通過/落選結果を `docs/workflow/skill-update-log.md` に記録し、
評価精度の改善に活用する。
