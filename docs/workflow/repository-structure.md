# リポジトリ構成説明

## 設計思想

このリポジトリは「就活・ES・企業研究・面接対策のマルチエージェント知識ベース」として設計されています。

**責務の分離原則**:
- `subagent` = 視点（多角的レビュー・評価）
- `skill` = 手順（再現可能な作業手順）
- `hook` = 機械的チェック（自動的な品質確認）
- `CLAUDE.md` = 軽量ルール集

---

## ディレクトリ構成（現在）

```
knowledge/
├── CLAUDE.md                    # 軽量ルール集（スキル使い分け・参照順序）
├── .claude/
│   ├── agents/                  # subagent定義（9つのレビュー視点）
│   ├── skills/                  # スキル定義（17スキル）
│   ├── hooks/                   # hook設定README
│   └── settings.local.json      # WebSearch許可設定
│
├── ES/                          # ES関連ファイル（既存）
│   ├── md/                      # エピソードライブラリ（STAR形式、01〜27番）
│   ├── components/              # カテゴリ別最良回答テンプレート
│   │   ├── best_answers.md      # コア参照: 上位11回答
│   │   ├── gakuchika.md
│   │   ├── motivation.md
│   │   ├── self_pr.md
│   │   └── other.md
│   ├── drafts/                  # ES作成途中（42社）
│   ├── submitted/               # 提出済みES（33社）
│   └── エピソード/               # 原本docxファイル（24件）
│
├── 移行後ES/                     # 確定版ES（最終提出形式、6社）
│
├── company-info/                # 企業ごとの調査・面接記録（31社）
│   └── <企業名>/
│       ├── research_brief.md    # 企業調査ブリーフ（9軸）
│       ├── interview_prep_*.md  # 面接準備シート
│       └── notes.md             # その他メモ
│
├── docs/                        # 運用ドキュメント（新設）
│   ├── workflow/                # 作業フロー・運用手順
│   ├── schemas/                 # ファイル形式・テンプレート定義
│   └── references/              # 長文の背景知識（CLAUDE.mdから分離）
│
├── tools/
│   ├── checks/                  # 品質チェックスクリプト（新設）
│   │   ├── es_checker.py        # ESファイルチェック
│   │   └── research_checker.py  # 企業調査チェック
│   └── transcribe.py            # 文字起こしスクリプト（既存）
│
└── transcripts/others/          # 就活外の文字起こし（既存）
```

---

## 各ディレクトリの責務

### `.claude/agents/` — レビュー視点（9エージェント）

| エージェント | 役割 |
|------------|------|
| readability-reviewer | 文系読者目線の可読性チェック |
| company-fit-reviewer | 企業調査との適合確認 |
| role-fit-reviewer | 職種適合確認 |
| question-fit-reviewer | 設問への回答性確認 |
| consistency-overlap-reviewer | 設問間一貫性・重複確認 |
| editor-refiner | reviewerの指摘を改善文案に落とす |
| research-gap-reviewer | 企業調査の不足発見 |
| role-research-reviewer | 職種調査の不足発見 |
| skeptical-interviewer | 面接深掘り質問の事前生成 |

### `.claude/skills/` — 作業手順（17スキル）

既存6スキル（company-researcher, es-writer, es-improver, es-refiner, interview-prep, episode-formatter）に加えて、
新規11スキルを追加:

| スキル | 役割 |
|-------|------|
| es-review-protocol | ESレビュー全体の手順 |
| overlap-detection | 重複検出の手順 |
| readability-check | 可読性評価の手順 |
| company-fit-evaluation | 企業適合評価の手順 |
| role-fit-evaluation | 職種適合評価の手順 |
| es-rewrite-patterns | リライトパターン集 |
| interview-probe-generation | 深掘り質問生成の手順 |
| company-research-audit | 企業調査監査の手順 |
| role-research-audit | 職種調査監査の手順 |
| research-gap-finding | 調査ギャップ発見の手順 |
| company-comparison-framework | 企業比較フレームワーク |

---

## 命名規則

### ファイル名
- エージェント: `<役割>-<タイプ>.md`（例: `readability-reviewer.md`）
- スキル: `<機能名>/SKILL.md`（例: `es-review-protocol/SKILL.md`）
- 企業調査: `company-info/<企業名>/research_brief.md`
- 面接準備: `company-info/<企業名>/interview_prep_<ステップ>_<YYYYMMDD>.md`
- エピソード: `ES/md/<連番>_<カテゴリ>_<タイトル>.md`
- ESドラフト: `ES/drafts/<企業名>.md`
- 確定版ES: `移行後ES/<企業名>.md`

### ブランチ名
- 新機能: `claude/YYYYMMDD-<機能説明>`
- ES作成: `es/<企業名>`
