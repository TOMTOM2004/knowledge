# Handoff — みずほFG Career Lounge 調査＋MYAM Gate 2（2セッション並行）
_Last updated: 2026-04-18 01:00 / session: みずほFG Phase 1-2 完了、各社プロファイル再構成中_

## 🎯 Next actions（優先順）

### 1. みずほFG Phase 3: 志望動機「機能レベル固有性」抽出（別セッション）
- What: Phase 2（3本の競合深掘り）+ 各社プロファイルの成果を踏まえ、みずほの「機能レベル固有性」を3×3構造で抽出
- Where: `company-info/みずほフィナンシャルグループ/unique_value_synthesis_<日付>.md` を新規作成
- Steps:
  1. 「みずほにしかない機能」3つを抽出（候補: かなで統一人事/UPSIDER AI与信/産業調査部銀行本体内蔵）
  2. 「機能は同じだがみずほが数値で勝つ」3つを抽出（候補: DCM 12年連続首位/BLUE DREAM Fund 243億円/プラネットブース128拠点）
  3. 「機能は他社も持つがみずほの組み合わせが固有」3つを抽出
  4. 上記を `research_brief.md` の軸7-A（核心固有性）に反映 → company-researcher スキル経由
  5. `reverse_questions_career-lounge_20260416.md` の前提文言を `ir_primary_sources_v2_20260418.md` のIR引用ベースに差し替え
  6. `interview_qa` の回答骨格に競合比較ファクトを織り込み
- Done when: `unique_value_synthesis.md` が完成し、research_brief 軸7-A・逆質問・interview_qa が更新されている
- Input files:
  - `company-info/みずほフィナンシャルグループ/competitor_deepdive_corporate-banking_20260418.md`（法人営業6行×8軸）
  - `company-info/みずほフィナンシャルグループ/competitor_deepdive_securities-products_20260418.md`（証券5社×7軸）
  - `company-info/みずほフィナンシャルグループ/competitor_deepdive_bank-securities-integration_20260418.md`（銀証信託連携6FG×8軸）
  - `company-info/みずほフィナンシャルグループ/ir_primary_sources_v2_20260418.md`（IR PDF ページ番号付き逐語引用）
  - 各社プロファイル: `company-info/{MUFG,SMFG,りそな,コンコルディアFG,ふくおかFG,野村證券,大和証券}/competitor_profile_20260418.md`
- Key findings from Phase 2（引き継ぎ用サマリー）:
  - **みずほ固有3点**: (1)「かなで」統一人事+WITH（他メガに同規模なし） (2)UPSIDER AI与信内蔵（唯一のメガ） (3)産業調査部が銀行本体内（他はシンクタンク外出し）
  - **数値優位3点**: (1)DCM 12年以上連続首位・3.25兆円 (2)BLUE DREAM Fund 243億円（国内最大級ベンチャーデット） (3)プラネットブース128拠点
  - **競合構造的弱点**: MUFG→FW規制違反で役員21名処分 / SMFG→グループに信託なし / りそな→証券機能なし
  - **反論ロジック3本**: りそな（承継の先がない）/ 地銀（顧客成長時にグループ機能不足）/ MUFG（中堅中小海外はみずほ産業調査が上）
  - **志望動機の軸**: 証券寄り。ただし銀行面談でも第一志望マインド

### 2. MYAM Gate 2 レビュー（別セッション・従来通り）
- What: `移行後ES/明治安田アセットマネジメント.md` の Gate 2 レビュー（question-fit-reviewer + readability-reviewer）
- Where: 別セッションで実行推奨（軽量モード・段階起動）
- Done when: 2 reviewer の出力を受けて、4固有性の抽象表現（「貢献」「積極的に」等 WARNING 5件）を具体化した改訂案が生成されている

## 📍 State snapshot
- ✅ Done:
  - N-01 Playwright MCP 導入（PR #14 merged）
  - N-02 MYAM 403解消データ補強
  - N-03 面談会 transcript 抽出
  - N-04 / N-05 全8社横断比較（PR #16 merged）
  - N-06 `interview_qa_1次面接_20260417.md` 新規作成（4固有性ベース、504→626行 / +122行、commit `3c1b26a`）
  - **N-07 `移行後ES/明治安田アセットマネジメント.md` 更新**（2設問を4固有性ベース再構築・旧版は `_before_N07_20260329.md` に退避保存・実測798字/800字×2・es_checker ERROR 0件）
- 🟡 In progress:
  - 現ブランチ `claude/20260417-myam-interview-qa-update` に N-06 `3c1b26a` コミット済み（push / PR 状態は未確認）
  - N-07 コミット予定（本セッション）
  - `tools/transcribe.py` 未コミット変更あり（内容不明・N-06/N-07 と別起源・今回のコミットに含めない）
  - untracked: JCB `transcript_2次_20260416.md`、みずほFG 複数、大和AM 他（**別セッションのスコープ**、今回のコミットに含めない）
- 🔴 Blocked:
  - なし

## 🧠 Context not in code
- 決定:
  - MYAM 4固有性（2026-04-17 N-06 で採用・以降の ES / 面接準備の基礎）:
    1. 相互会社 × 調査集中 × 独立判断 × 小規模シニア（MYAM のみ PM 平均 15-19 年）
    2. ESG 格付を DCF 割引率に直接反映（他社はスコア化止まり）
    3. 営業と運用の完全分離（面談会 transcript「ファンドを売るからこの株を見といて、ということはない」）
    4. 純流出 ▲22 億円（8社中唯一の純流出 → 課題先進 → 若手貢献余地最大）
  - 旧 `interview_qa_1次面接_20260416.md` は差分比較のため**残す**（削除禁止）
- 試してダメだった:
  - （未把握）
- 落とし穴:
  - 新規ファイル名は `interview_qa_<ステップ>_<日付>.md`（CLAUDE.md 規則）。旧版と日付で区別する
  - `移行後ES/` 配下は日本語ファイル名。git log / status 出力ではエスケープ表記になる点に注意
  - 現ブランチ名は N-06 用。N-07 を同ブランチで継続すると1 PR に複数機能が混ざる可能性 → 別ブランチ `claude/20260417-myam-es-n07` を切る方が望ましい

## ❓ Open questions for user
- [ ] 現ブランチ `claude/20260417-myam-interview-qa-update` の N-06 `3c1b26a` + N-07 コミットは **push / PR 作成済み**か？ 未なら本セッションで push + PR を実行するか？
- [ ] `tools/transcribe.py` の未コミット変更は何の目的か？（今回の N-06/N-07 には含めていない）
- [ ] untracked の transcript / competitor_comparison 群（JCB 2次、みずほFG 複数、大和AM 他）は別セッションで扱う想定か？
- [ ] N-08（am-competitor-researcher eval）、N-09（面接本番準備）の実施時期は未定のままか？
- [ ] 旧 todo-running-log にある Interview OS 改善タスク **T-01〜T-09** は現在アクティブか、休眠か？
- [ ] Gate 2（question-fit + readability）はいつ・どのセッションで実施するか？

## 📂 Key files
- `company-info/明治安田アセットマネジメント/interview_qa_1次面接_20260417.md`（N-06 成果物）
- `company-info/明治安田アセットマネジメント/interview_qa_1次面接_20260416.md`（旧版・差分比較用）
- `docs/am_competitor_comparison_8companies_20260417.md`
- `company-info/明治安田アセットマネジメント/am_profile.md`
- `company-info/明治安田アセットマネジメント/transcript_findings_面談会1_20260416.md`
- `ES/素材/INDEX.md`
- `移行後ES/明治安田アセットマネジメント.md`（N-07 対象）
- `tasks/todo-running-log-20260417.md`（旧 todo.md をリネーム保全。N-01〜N-09 / T-01〜T-09 の詳細ログ）

## ❌ Out of scope
- 他企業（みずほFG、JCB、大和AM 等）の ES / 面接準備
- Interview OS 改善系タスク T-01〜T-09（別軸の system 改善）
- `tools/transcribe.py` の機能追加・変更（Open questions の回答後に判断）
