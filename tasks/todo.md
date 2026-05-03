# Handoff — 複数プロジェクト並行進行中（DX知見構造化完了 / みずほFG プロフィール待ち / MYAM Gate2 待ち）
_Last updated: 2026-05-03 / session: DX知見（ES/素材/31）構造化整理完了_

## 🎯 Next action（1つだけ、具体的に）
- What: みずほFG 大企業RM 面談相手プロフィール反映（届いてから Tier2 から該当質問を選択投入する流れ）
- Where: `company-info/みずほフィナンシャルグループ/reverse_questions_大企業RM_20260420.md` の「社員プロフィール反映後の調整候補」セクション
- Done when: 面談相手の年次・所属・経歴に応じて Tier2 (B1-B4, #6, #9) から投入する質問が選定済み + #X-B C「17年目で何が成熟・未成熟」の角度調整完了
- 着手タイミング: 面談（5/12）直前期、プロフィール届き次第

## 📍 State snapshot
- ✅ Done（本セッション 2026-05-03 後半）:
  - **DX 知見構造化整理完了**（`ES/素材/31_日本のDXに関する考察と改善.md`）
    - TL;DR 3行サマリー + 論点マップ（章立て一覧）追加
    - 12論点を見出し ID 付きで再構造化、引用集（面接・逆質問用 punch line）抽出
    - 業界別応用フック（銀行RM・AM・コンサル・損保生保）追加
    - 関連エピソード接続マップ（`03`/`19`/`20`/`26`/`29`/`30`等との対応）追加
    - `ES/素材/INDEX.md` に 31 を登録（ファイル一覧・参考資料カテゴリ・設問別クイックリファレンス）
- ✅ Done（本セッション 2026-05-03 前半）:
  - **みずほFG 大企業RM 逆質問ブラッシュアップ 7 commit 全 main マージ済**（PR #18, #19, #20）
    - `bd0e2f3` #5 数字判断を業界別ケース化（GX・半導体・海外M&A）
    - `32ee3bf` #X-B 邦銀唯一のみずほ証券兼職（リサーチ5ファクト引用、MUFG時事フック）
    - `aa81a4b` #X-A 長期テーマ伴走（粒度・KPI継承・引き継ぎ）
    - `d6a7c45` #1 #4 深掘り追加（意思決定権限・役割境界・リサーチャー実務）
    - `6c50da6` #7 v3 全面改訂（B/E/F: 稟議AI仮説・コミュニケーション中身・R&T翻訳機能）
    - `ce2f34f` 重複 #X-A 削除（merge artifact）
    - `bea7fd8` Tier2再構成・B4 ESG角度修正・当日優先順位ガイド改訂
- 🟡 In progress:
  - **MYAM 1次面接準備（stash@{0} に保留）**: `company-info/明治安田アセットマネジメント/interview_qa_1次面接_20260417.md` + `tasks/todo.md` の未コミット変更を `claude/20260428-myam-interview-format-update` ブランチで stash 退避中。再開時は stash pop
  - 旧 todo.md は MYAM N-06/N-07 進行中の状態で記載（本ファイルで上書き済、参照は git history）
- 🔴 Blocked:
  - なし

## 🧠 Context not in code
- 決定:
  - **DX 知見ファイル `ES/素材/31`** は方針A（元資料の構造化整理）で再構成完了。逆質問・志望動機・面接論点での再利用に最適化。引用集の punch line はそのまま発話可
  - **みずほFG 大企業RM 逆質問の最終構成**: 当日 45 分タイムラインで Tier1 = 必須6問（#1, #X-B, #4, #7, #X-A, #10）+ 時間次第4問（#2, #3, #5, #8）+ Tier2 = 6問（B1-B4, #6, #9 プロフィールトリガーで選択）
  - **B4 ESG**: 「ESG投資」（曖昧・運用会社文脈）から「サステナビリティリンクローン・グリーンボンド」（具体プロダクト）に角度修正。「ESGプレミアムは本物か」「達成しやすいKPIで金利優遇を取りに行く顧客を見抜けるか」というユーザー独自視点を質問に組込
  - **当日序盤の必須運用**: 面接官の経歴（年次・所属・前任部署・兼職対象か等）を必ず冒頭で聞き、Tier2 の選択投入の判断材料にする
- 参考情報:
  - みずほFG 関連リサーチ Agent 実行 2 回:
    1. みずほ証券兼職実態（2009年日本初・17年目・形式判明・GCF20人・MUFG処分）
    2. みずほR&T銀行統合（みずほデジタルコネクト・産調×R&T分業・統合効果）
  - claude-brain `claude/20260422-slack-todo-triage` の 4 commit 中、3 commit は B-1 PR #10 で main 取り込み済。`05ea50f` Slack TODO はスキップ判断（実体は `~/claude-memory-mcp/` と `~/.claude/`）
  - personal-tasks の DONE 3件処理済（音声集積update / アメリカ経済 / 財務情報分析論）

## ❌ Don't do (this task)
<!-- Hot層: このタスク限定の失敗・判断ミス -->
- [trap] merge --no-ff で同じセクションが重複挿入されることがある（今回 #X-A が2箇所に重複した。修正PR #19 で対応）
- [mistake] git heredoc で `$(cat <<'EOF' ... EOF)` が macOS bash で `bad substitution: no closing` エラーになる場合がある → 一時ファイル経由（`/tmp/commit-msg.txt`）+ `git commit -F` で回避

## ❓ Open questions for user
- [x] ~~DX 知見整理（`ES/素材/31` ベース）の別セッションはいつ実行するか？~~ → 本セッションで完了（方針A 構造化整理版）
- [ ] みずほFG 面談相手プロフィールが届いた時点で再度起動するか？それとも当日まで待つか？
- [ ] MYAM Gate2 レビューは別セッションで実施想定のままか？stash の扱いは？
- [ ] 旧 todo-running-log にある Interview OS 改善タスク T-01〜T-09 は現在アクティブか、休眠か？
- [ ] DX 知見の方針B（業界別逆質問テンプレ展開）・方針C（best_answers/motivation への DX 視点インジェクト）は実施するか？

## 📂 Key files
- `company-info/みずほフィナンシャルグループ/reverse_questions_大企業RM_20260420.md`（本セッションの主成果物）
- `company-info/みずほフィナンシャルグループ/transcript_CareerLounge-中堅中小RM_20260422.md`（中堅中小RM 実回答素材）
- `company-info/みずほフィナンシャルグループ/README.md`（みずほフォルダ index）
- `ES/素材/31_日本のDXに関する考察と改善.md`（DX 本質資料、別セッションで再整理予定）
- `company-info/明治安田アセットマネジメント/interview_qa_1次面接_20260417.md`（MYAM stash 中）
- `移行後ES/明治安田アセットマネジメント.md`（MYAM Gate2 待ち）

## ❌ Out of scope
- 本セッション内では MYAM N-08 / N-09 / Gate2 は実施しない（stash@{0} 退避継続）
- DX 知見の方針B（逆質問テンプレ展開）・方針C（foundations インジェクト）は次回以降
- Interview OS 改善系タスク T-01〜T-09
