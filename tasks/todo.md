# Interview OS 改善タスク一覧

作成日: 2026-04-14  
ステータス: メモ（優先度・対応順は別途議論）

---

## 優先度 高

### [T-01] Debate log が一方通行モノローグになっている
- **問題**: 各ペルソナが「次の候補質問」を独立に提示するだけで、相互に反論・修正しない
- **影響**: 実際の面接委員会の議論を再現できていない。orchestrator が使える情報の質が低い
- **修正案**: Turn 構造を「提案 → 反論 → 合成」の3フェーズに変更。priority 数値を相互議論の結果として導出する

### [T-02] Q3・Q4 の重複（なぜMYAMか × 2問）
- **問題**: Q3「志望動機（なぜAMか・なぜMYAMか）」と Q4「なぜ競合AMではなくMYAMか」が15分面談で同一軸を重複消費
- **影響**: 1人あたり15分枠で貴重な2問を浪費
- **修正案**: Q4 を conditional（Q3 で MYAM 固有性に触れなかった場合のみ発動）に変更するか、Q4 を削除して common_critic の差し込みポイントに吸収する

### [T-03] 11問は15分枠では消化不能
- **問題**: 質問リストに11問あるが、1人あたり15分では現実的に5〜6問が上限
- **影響**: orchestrator がそのまま実行すると時間超過。練習として非現実的なシナリオになる
- **修正案**: 質問リストに「本番5問グループ（priority A）」と「時間があれば追加グループ（priority B）」の分類を追加

### [T-04] jargon_risk が common_critic の介入リストに入っていない
- **問題**: ESに「因果推論・傾向スコア・バイアス補正」等の専門用語が含まれており、1次面談（人事・AM業務系）では平易な言い換えが必要。しかし current の3介入スロットに jargon_risk が含まれていない
- **影響**: 最も発生頻度の高いリスクを見逃す可能性
- **修正案**: common_critic の detection_targets に jargon_risk を追加し、既存3スロットの優先度と比較して組み込む

---

## 優先度 中

### [T-05] Q2 深掘り2段目が1次面談にしては難易度が高すぎる
- **問題**: 「業務改善の型化・標準化という発想は、インベストメント・チェーンのどの機能に対応すると思いますか？」は3ステップの即時合成が必要
- **影響**: 1次で詰まると委縮し、後続の回答品質が下がる
- **修正案**: 1次向け設定では深掘り2段目を「連鎖への関心を確認する」レベルに緩める。深度設定を stage ごとに調整できるようにする

### [T-06] am_business.yaml に passing_criteria / excellent_criteria がない
- **問題**: dislikes と NG パターンは定義済みだが、「合格ライン」「高評価ライン」が未定義
- **影響**: orchestrator がフィードバックを生成する際の基準がなく、採点が恣意的になる
- **修正案**: 各 core_axes に対して passing（最低基準）・excellent（差別化ライン）を追記する

### [T-07] 深掘り2段目をスキップする条件ロジックがない
- **問題**: orchestrator は depth_level=2 なら機械的に2段目を実行する。1段目で十分な回答が出た場合も強制継続する
- **影響**: 自然な面談の流れを壊す。練習としてもリアリティが低下
- **修正案**: orchestrator に「1段目回答が passing_criteria を超えた場合は2段目をスキップ」の条件分岐を追加

---

## 優先度 低

### [T-08] common_critic の include_praise: false が固定されている
- **問題**: 練習モードでは肯定フィードバックがあるほうが学習効率が高い場面がある
- **影響**: 全セッションで称賛なし → 学習モチベーションに影響する可能性
- **修正案**: session_config に `practice_mode: true/false` を追加し、true の場合は include_praise を上書きする

### [T-09] ランダム質問がセッション時間に関係なく必ず1問選ばれる
- **問題**: 20分以下のセッション設定でもランダム質問が強制挿入される
- **影響**: 短時間セッションでは本質的な質問を圧迫する
- **修正案**: `session_time ≤ 20` かつ `question_policy.randomness = one_random_question` の場合は自動スキップ、または警告を出してユーザーに確認する

---

## 次のアクション（別途議論予定）

- [ ] フォルダ構成・保存方針の議論（ユーザー草案あり）
- [ ] Git管理の方針確認
- [ ] 上記タスクの修正順序と担当スキルの決定

---

# AM競合比較タスク（A-01起点）

作成日: 2026-04-16
起点: tasks/todo.md 旧A-00〜A-04 + 2026-04-16セッションの実行結果

---

## 完了済み

- [x] **A-01 スキル作成**: `am-competitor-researcher` スキル新規作成（PR #11 マージ済み）
  - SKILL.md（7ステップ）+ references/ 3ファイル（web-query-templates / comparison-template / quality-check-am）
  - research-lenses.md AMセクションをA-D群構造に再編
  - CLAUDE.md にスキル・ファイル場所を登録
- [x] **MYAM単社プロファイル**: `docs/am_competitor_comparison.md` を28軸で構築（PR #12）
  - C群: 全4軸◎（親会社PDF読み取りで議決権行使・対話実績・ISS非依存を確認）
  - A群: A-7◎、他8軸△
  - B群: 6軸△、2軸✗（B-1a/B-1b は情報非公開）
  - D群: D-3/D-5◎、他5軸△
- [x] **SKILL.md フォールバック方針追加**: Step 3-3 に403時の5段階チェーン記述

## 次セッションでやること

### [N-01] Playwright MCP導入（最優先・A-01補完）
- **目的**: myam.co.jp の403ブロックを解消し、MYAMプロファイルのA群・B群を◎に引き上げる
- **経緯**: 当初OpenClaw MCPを検討したが、OpenClawはチャットプラットフォーム統合AIであり、Webスクレイピング用途ではないことが判明。代替として実ブラウザ（Chromium）でページを取得するPlaywright MCPを採用
- **進捗**:
  - [x] Playwright MCPサーバーをuserスコープで追加（`claude mcp add` で `@playwright/mcp@latest` を登録済み・接続確認済み）
  - [x] myam.co.jp/about/voting/ にアクセスできることを検証（Playwright MCP経由で議決権行使ページの全内容取得に成功）
  - [x] SKILL.md の Step 3-3 のTODOを Playwright MCPの具体的手順（`browser_navigate` → `browser_snapshot` → `browser_click`）で記述
  - [x] SKILL.md の `allowed-tools` に `mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`, `mcp__playwright__browser_click` を追加
- **ブランチ**: `claude/YYYYMMDD-playwright-mcp-integration`

### [N-02] MYAM 403解消後のデータ補強（N-01完了後）
- **目的**: MYAMプロファイルの△軸を◎に引き上げる
- **進捗**: ◎ 7→10（+3軸）+ C群全4軸を最新データで大幅補強。HTMLページ6件+PDF1件を取得済み
- **完了分**:
  - [x] `www.myam.co.jp/about/voting/guideline.html` → C-2 補強（MYAM固有ガイドライン2種、2026年4月改定）
  - [x] `www.myam.co.jp/about/stewardship.html` → C-1/C-3 補強（責任投資部5名体制、サステナビリティ・レポート2025発見）
  - [x] `www.myam.co.jp/about/structure/` → B-2 ◎化（運用哲学3項目）
  - [x] `www.myam.co.jp/about/structure/inside.html` → B-2 ◎化（7部体制、PM49名、平均15-19年）+ B-3 ◎化
  - [x] `www.myam.co.jp/fund/price/` → A-6 ◎化（ダルトン524億円が旗艦、地域応援ファンド群）
  - [x] `www.myam.co.jp/about/voting/` → C-2 補強（議決権行使分科会→責任投資委員会の意思決定フロー）
- **PDF取得済み**:
  - [x] `stewardshipreview_2025.pdf` → C群全4軸を2024年度データで大幅補強（対話1,470件/会社提案反対率15.7%/PRI★5×4/みずほR&T 74機関中1位）
- **未実施（PDF取得が必要）**:
  - [ ] `sustainabilityreport_2025.pdf`（7.72MB）→ C-1/C-3 追加補強（**2024版より新しい2025版を発見**）
  - [ ] 目論見書PDF → B-4 Active Share・組入銘柄数・ターンオーバー
  - [ ] A-5 パッシブ/アクティブ比率（ディスクロージャー誌 or サステナビリティ・レポートで確認）
- **更新対象**: `docs/am_competitor_comparison.md` のMYAM列を更新済み
- **ブランチ**: `claude/20260416-playwright-mcp-integration`

### [N-03] A-00 面談会transcript固有性抽出（N-02と独立・並行可能）
- **目的**: `company-info/明治安田アセットマネジメント/transcript_明治安田アセットマネジメント第1回面談.md`（3,724行）から MYAM固有の情報を抽出し、比較表とdiscussion_topicsに反映
- **やること**:
  1. transcript全体を読み、責任投資部・リテール営業企画部の発言を整理
  2. MYAM固有の手がかり（エンゲージメントの具体例、販売戦略、グループ連携の実態等）を抽出
  3. `docs/am_competitor_comparison.md` のMYAM列に反映（特にB-1a Information edge、B-6 Risk management philosophy）
  4. `company-info/明治安田アセットマネジメント/discussion_topics.md` のテーマ1（志望動機の固有性再設計）を更新
- **ブランチ**: `claude/YYYYMMDD-myam-transcript-extraction`

### [N-04] A-02 Tier1競合の深掘り調査（N-01完了後・別セッション推奨）
- **目的**: ニッセイAM / AM-One を同じ28軸で調査し、`docs/am_competitor_comparison.md` に列を追加
- **前提**:
  - 両社の `research_brief.md` は既存（✅）
  - OpenClaw MCPが導入済みであること（各社サイトも403の可能性あり）
- **やること**:
  1. 各社research_briefから28軸マッピング（Step 1-2）
  2. ギャップ分析 → Web補完調査（Step 3）
  3. 比較表にニッセイAM・AM-One列を追加（Step 4）
- **ブランチ**: `claude/YYYYMMDD-am-tier1-comparison`

### [N-05] A-03 全8社横断比較表の構築（N-04完了後・別セッション推奨）
- **目的**: 全8社を28軸で比較し、Insight Layer（母体別パターン・MYAMにしか言えないこと）を生成
- **前提**: N-04完了。野村AM・三井住友DSAMはresearch_briefなし → company-researcherで先に作成が必要
- **ブランチ**: `claude/YYYYMMDD-am-full-comparison`

### [N-06] A-04 MYAM志望動機の固有性確定（N-05完了後）
- **目的**: 全社比較表から「MYAMにしか言えないこと」を抽出し、interview_qaの志望動機セクションを再構築
- **前提**: N-05の比較表とInsight Layerが完成していること

---

## 依存関係

```
N-01 (OpenClaw導入)
  └→ N-02 (MYAM 403解消データ補強)
  └→ N-04 (Tier1競合調査)
       └→ N-05 (全8社横断比較)
            └→ N-06 (志望動機固有性確定)

N-03 (transcript抽出) ← N-01/N-02と独立して実行可能
```
