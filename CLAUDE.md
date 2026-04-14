# Knowledge ナレッジベース

就職活動・ES執筆・企業調査・面接対策のマルチエージェント知識ベース。

詳細な運用手順 → `docs/workflow/`

**軽量モードが default。** セッション分割・brief 一次参照・段階 reviewer 起動を守る。
→ `docs/workflow/lightweight-mode.md`

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
| エピソードライブラリ | `ES/素材/` （INDEX.md で一覧確認） |
| ES最良回答テンプレ | `ES/部品/best_answers.md` |
| ES草稿 | `ES/企業別/作成中/<企業名>.md` |
| 提出済みES | `ES/企業別/提出済/<企業名>.md` |
| 確定版ES | `移行後ES/<企業名>.md` |
| 企業調査 | `company-info/<企業名>/research_brief.md` |
| 面接調査（新） | `company-info/<企業名>/interview_research_<ステップ>_<日付>.md` |
| 面接想定問答（新） | `company-info/<企業名>/interview_qa_<ステップ>_<日付>.md` |
| 旧面接準備（参照のみ） | `company-info/<企業名>/interview_prep_*.md` |
| 面接OSセッション設定 | `company-info/<企業名>/interview-os/configs/` |
| 面接OS生成ファイル | `company-info/<企業名>/interview-os/generated/` |
| 面接OSセッションログ | `company-info/<企業名>/interview-os/sessions/` |
| 面接OS学習ログ | `company-info/<企業名>/interview-os/learning/` |
| 面接OSペルソナ・スキーマ | `tools/interview_os/` |
| 面接振り返り | `company-info/<企業名>/reflection_<N>次_<YYYYMMDD>.md` |
| 音声文字起こし | `company-info/<企業名>/transcript_<N>次_<YYYYMMDD>.md` |
| 直前チェックシート | `company-info/<企業名>/interview_direct_prep_<N>次_<YYYYMMDD>.md` |
| 面接傾向パターン（全社横断） | `docs/interview_patterns.md` |
| 質問バンク（全社横断） | `docs/question_bank.md` |
| 選考状況トラッカー | `docs/application_status.md` |
| 通過実績記録 | `docs/success_record.md` |
| reflection テンプレート | `docs/schemas/reflection-template.md` |
| 運用ドキュメント | `docs/workflow/` |
| チェックスクリプト | `tools/checks/` |

---

## ES作成時の参照順序（軽量モード）

1. `company-info/<企業名>/research_brief.md` — **一次参照はこれだけ**（詳細調査ファイルを直接読まない）
   - 軸7-A（核心固有性）が存在することを確認。未記載なら company-researcher を先に実行する
2. `ES/素材/INDEX.md` — 使えるエピソードを確認
3. `ES/部品/best_answers.md` — コア回答テンプレを確認
4. es-writer スキルで生成
5. 機械チェック: `python tools/checks/es_checker.py`
6. Gate 2: question-fit + readability（草案後）
7. Gate 3: company-fit + role-fit（仕上げ前・別セッション推奨）

reviewer は段階起動。全 reviewer 一括は禁止。詳細 → `docs/workflow/es-review-flow.md`

---

## 企業調査時の参照順序

1. `company-info/<企業名>/` フォルダを確認（既存資料があるか）
2. company-researcher スキルで調査・生成
   - 軸7-A（核心固有性）が生成されていることを確認する
3. チェック: `python tools/checks/research_checker.py <企業名>`
4. research-gap-reviewer エージェントで不足論点を確認

---

## 面接準備の3段階フロー（新規企業用）

**前提**: `company-info/<企業名>/research_brief.md` が存在すること（軸7-A含む）

### Stage 1: 選考調査（interview-research）
```
「<企業名>の<N>次面接の選考調査をして」
```
→ 出力: `company-info/<企業名>/interview_research_<ステップ>_<日付>.md`

### Stage 2: 想定問答生成（interview-qa）
```
「<企業名>の<N>次面接の想定問答を作って」
```
→ 出力: `company-info/<企業名>/interview_qa_<ステップ>_<日付>.md`

### Stage 3: 本番練習（skeptical-interviewer）
```
「<企業名>の<N>次面接で skeptical-interviewer を回して」
```
→ 別セッション推奨

### Stage 4: 模擬面接OS（interview-session-preparer → interview-debate-orchestrator）
```
「<企業名>の<N>次面接セッションを準備して」   → interview-session-preparer
「<企業名>の<N>次面接を開始して」            → interview-debate-orchestrator
「今日の面接の学習ログを更新して」            → interview-learning-updater
```
→ 企業差し替え式・多ペルソナ評価・フィードバック自動生成。別セッション推奨
→ 詳細: `docs/workflow/interview-os-design.md`

**軽量モード**: Stage 1・2・3・4は別セッションで実行する
**既存企業**: `interview_prep_*.md` は参照のみ（上書き・削除禁止）

---

## 面接後の処理フロー（transcript活用）

### 面接終了直後（スマホ / Claude Web）
```
① Gemini等で壁打ちしながら reflection を手作成・push
   → company-info/<企業名>/reflection_<N>次_<YYYYMMDD>.md
   → frontmatter は result: pending で作成
```
テンプレート → `docs/schemas/reflection-template.md`

### transcript 到着後（Windows PC 自動 PR マージ後）
```
② interview-blindspot  → reflection に盲点セクション追記
③ question-bank-updater → docs/question_bank.md 更新
```

### 次の選考が決まったら
```
④ interview-next-prep → 次回 interview_qa に引き継ぎ論点追加
⑤ interview-reflect   → docs/interview_patterns.md 更新
```

### 合否確認後
```
⑥ reflection の frontmatter を更新（result: passed/rejected・date_result 記入）
⑦ success-pattern-extractor → 定期実行（月1程度）
```

### 面接30分前
```
⑧ interview-direct-prep → 1枚チェックシートを生成
```

---

## スキル / エージェント / hook の使い分け

| 種類 | 役割 | 使う場面 |
|-----|------|---------|
| **skill** | 手順（作業を実行する） | ES作成・企業調査・エピソード整形等 |
| **agent** | 視点（評価・レビューする） | ESレビュー・調査品質確認・深掘り質問生成 |
| **hook/check** | 機械的チェック | ファイル保存後の自動検証 |

### 主なスキル
- `company-researcher` — 企業調査（**必ず**このスキル経由。自前WebSearch禁止）
- `es-writer` — ES作成（企業名+設問があれば自動起動）
- `interview-research` — 面接調査専門（体験記収集・重要度分類）← **新規**
- `interview-qa` — 想定問答生成専門（重要度別回答骨格・詰められ・逆質問）← **新規**
- `interview-prep` — 旧面接準備（**既存ファイル参照専用。新規企業には使わない**）
- `es-review-protocol` — ES全体レビュー（**第一志望最終提出前のみ使用**。通常は段階起動）
- `es-refiner` — 提出済みESからfoundations更新
- `es-improver` — 編集差分からes-writerを自動改善
- `interview-blindspot` — reflection × transcript の差分 → 盲点を reflection に追記 ← **新規**
- `question-bank-updater` — transcript から質問抽出 → question_bank.md にマージ ← **新規**
- `interview-direct-prep` — 面接30分前の1枚チェックシート生成 ← **新規**
- `interview-reflect` — 全 reflection 横断集計 → interview_patterns.md 更新 ← **新規**
- `interview-next-prep` — 前回深掘り → 次回 interview_qa に引き継ぎ論点追加 ← **新規**
- `success-pattern-extractor` — passed ES・reflection → 共通パターン抽出・実績タグ付け ← **新規**

#### 面接OS スキル（模擬面接実行用）
- `interview-session-preparer` — 模擬面接セッション準備（質問候補生成・議論ログ生成）
- `interview-persona-router` — 業界/段階/テーマからペルソナセット選定
- `interview-debate-orchestrator` — 模擬面接実行（質問表示・ペルソナ評価・差し込み判定）
- `answer-reviewer` — 回答の4区分FB・言い換え案・骨格生成
- `interview-learning-updater` — セッション後の弱点・境界表現を learning/ に記録
- `reverse-question-generator` — 逆質問生成専門（面接官タイプ別・軸7-Aフック付き・NG判定）

### 主なエージェント（`.claude/agents/`）
- `question-fit-reviewer` — 設問適合（最優先）
- `readability-reviewer` — 可読性
- `company-fit-reviewer` — 企業固有性
- `role-fit-reviewer` — 職種適合
- `consistency-overlap-reviewer` — 重複・一貫性
- `editor-refiner` — 改善文案生成
- `research-gap-reviewer` — 企業調査の不足発見
- `skeptical-interviewer` — 面接深掘り質問生成

詳細 → `docs/workflow/agent-usage-guide.md`

---

## 禁止事項

- `company-researcher` を使わず自前でWebSearchして企業調査しない
- `data/raw/` に相当する原本ファイル（`ES/エピソード/`の docx 等）を削除・変更しない
- `research_brief.md` を直接書き換えない（スキル経由で更新する）
- `interview_prep_*.md`（旧フォーマット）を削除・変更しない（参照のみ）
- `interview-research` なしで `interview-qa` を起動することを推奨しない
- `interview-blindspot` を transcript なしで実行しない（transcript 到着前の実行は禁止）
- `question-bank-updater` で質問文を要約・意訳しない（逐語記録を徹底する）
- `reflection_*.md` の frontmatter `result` を未設定のまま放置しない（合否確認後に必ず更新する）
- main ブランチに直接コミット・push しない
- `.env` や秘密情報をコミットしない

---

## 出力スタイル

- 説明は最小限。変更はdiff中心で示す
- 冗長な前置き・要約は省略する
- 日本語で会話する

---

## 長い背景知識の置き場

CLAUDE.md には入れない。以下に配置する:
- 評価基準・ルール詳細 → `docs/workflow/`
- ES生成の詳細ルール → `.claude/skills/es-writer/SKILL.md`
- スキル更新履歴 → `docs/workflow/skill-update-log.md`
- 軽量モード詳細 → `docs/workflow/lightweight-mode.md`
- セッション分割 → `docs/workflow/session-splitting-guide.md`
- 品質ゲート → `docs/workflow/quality-gates.md`
- エージェントコスト → `docs/workflow/agent-cost-tiering.md`
- research_brief フロー → `docs/workflow/research-brief-flow.md`
- 面接スキル設計思想 → `docs/workflow/interview-skill-design.md`
