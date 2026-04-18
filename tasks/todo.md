# Handoff — みずほFG Career Lounge 調査＋MYAM Gate 2（2セッション並行）
_Last updated: 2026-04-18 16:45 / session: みずほFG Phase 3 完了、全変更コミット・push済_

## 🎯 Next actions（優先順）

### 1. MYAM Gate 2 レビュー（別セッション・従来通り）
- What: `移行後ES/明治安田アセットマネジメント.md` の Gate 2 レビュー（question-fit-reviewer + readability-reviewer）
- Where: 別セッションで実行推奨（軽量モード・段階起動）
- Done when: 2 reviewer の出力を受けて、4固有性の抽象表現（「貢献」「積極的に」等 WARNING 5件）を具体化した改訂案が生成されている

## 📍 State snapshot
- ✅ Done: → `tasks/done/2026-04.md` に移動済み
- 🟡 In progress:
  - なし
- 🔴 Blocked:
  - なし

### 未処理（前セッション残り・要対応）
- [ ] 現ブランチ `claude/20260417-myam-interview-qa-update` に N-06 `3c1b26a` コミット済み（push / PR 状態は未確認）
- [ ] N-07 コミット予定
- [ ] `tools/transcribe.py` 未コミット変更あり（内容不明・N-06/N-07 と別起源）
- [ ] untracked: JCB `transcript_2次_20260416.md`、みずほFG 複数、大和AM 他

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
