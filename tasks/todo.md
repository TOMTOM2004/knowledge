# Handoff — 別PC同期 ＋ みずほ2次transcript重複解消 ＋ ブランチ大整理
_Last updated: 2026-05-30 / session: リポジトリ整理（3次transcript同期・重複解消・ブランチ23→2本）_

## 🎯 Next action（ユーザー側で実施）
- [ ] **PR #39 をマージ**（`https://github.com/TOMTOM2004/knowledge/pull/39`／2次transcript重複解消＋本todo更新）。マージ後 `claude/20260530-mizuho-transcript-cleanup` は削除可
- [ ] **別PC側の同期**: `git checkout main && git pull` ＋ `git fetch --prune`。削除済みローカルブランチが残れば `git branch -D <ブランチ名>` で1本ずつ削除

## 🎉 本セッション成果（2026-05-30）
- **みずほ3次面接transcript を同期確認**: 別PCが PR#38 で push 済（5/29 main マージ）。このPCの main を origin/main へ ff（39コミット遅れを解消）し取込。`transcript/transcript_3次面接_20260529.md` ＋ assets(.json/.srt/.txt)
- **2次transcript の重複解消（PR #39 作成・マージ待ち）**: 別PC=PR#35 の faster-whisper版（旧命名）と本PCの mlx正本が重複 → 旧命名版 `transcript_みずほフィナンシャルグループ 2次面接.md` を削除。正本 `transcript_2次面接_20260526.md`（補正表+Q&A整形+全文逐語①②）と生データ `-1/-2.md` を維持
- **ブランチ大整理（リモート 23→2本）**:
  - マージ済み17本 + PR#29 CLOSED 1本 を origin 削除
  - ローカルのみ・マージ済み 2本（SMBC-nikkousyoukenn / nissay-asset-management-es）削除
  - 未マージ3本を精査の上 全削除: playwright-mcp-integration（投信協会DSは4/23リファクタで main の references/ に取込済＝陳腐化）/ am-full-comparison（8社profile・比較表が main と0行差＝陳腐化）/ myam-uniqueness-audit（closed PR#29内包・MYAM 1次完了で用済み）
  - 現役 mizuho-2ji-qa-augment 削除（deliverable は PR#36/#37 で main に完備・0行差、残りは完了済みhandoffのみ）

## 📍 State snapshot
- ✅ Done: 3次transcript取込（main 反映済）、ブランチ整理（origin 2本＝main + PR#39ブランチ）
- 🟡 In progress: **PR #39 マージ待ち（ユーザー側）** / **別PC同期待ち（ユーザー側）**
- 🔴 Blocked: なし

## 🧠 Context not in code
- **みずほ最終面接（オファー面接）本番待ち**: 想定問答 `interview_qa_最終面接_20260527.md` ＋ 当日用チートシート `当日用/最終面接_要点+60秒版_20260529.md` は main に完備。日程出たら interview-direct-prep で直前シート生成
- **選考フロー**: 1次(4/6・計数あり)→2次(5/26・計数なし・3社兼用)→**オファー面接(=最終相当・1社に絞る)**。2次結果は **6/26まで連絡**
- **志望順位**: ①銀行 ②証券 ③信託。本命=銀行（軸直結・産業調査部ルート・マクロ志向）
- **かんぽ生命**: DX戦略部の内々定の約束あり。みずほ内定なら行く可能性高。差別化＝相手が社内 vs 顧客
- **コース確定**: グループオープン型（BK/TB法人＋SC法人WM）。"色々やりたい"NG・到達点(産業調査起点M&A)を必ず添える
- **transcript後続フロー（3次・未実施）**: interview-blindspot（reflection照合・盲点抽出）/ question-bank-updater（3次質問を question_bank.md 登録）

## ❌ Don't do（durable・継続）
- [feedback] 自己紹介にPREP法を強制しない（自然な流れ。PREPは論点回答向け）
- [feedback] 価値観の出所（生得 vs 環境）を区別、曖昧な特性を「幼少期から」と盛らない
- [feedback] 最終面接で「銀行でも証券でも同じ」はNG＝志望の濃淡が消える。**"同じ軸・別ルート・優先は銀行"**で一貫
- [trap] 長期インターンはチーム文脈で使わない（一人完遂が強み。チームは塾講師05・文化祭06）
- [trap] 面接transcriptの「何次」はファイル名/即答でなく**中身の物証**で確認（計数テスト有無/面接官冒頭発言/結果通知日の時系列）
- [process] skill のマージ可否判定は SKILL.md 本体だけでなく `references/` も含めて照合（リファクタで内容が references/ へ移動する。playwright判定で一度誤判定した）

## ❓ Open questions for user
- [ ] research_brief.md（みずほ）更新: 卒論1行＋一次情報(4/6,5/12,5/26,5/29)を軸7/8に反映（company-researcher経由）
- [ ] 模擬面接（声出し）をオファー面接前に実施するか（skeptical-interviewer）
- [ ] 3次面接の reflection 作成＋ interview-blindspot を回すか（transcript 到着済）

## 📂 Key files
- `company-info/みずほフィナンシャルグループ/interview_qa_最終面接_20260527.md`（最終面接想定問答・main完備）★本番起点
- `company-info/みずほフィナンシャルグループ/当日用/最終面接_要点+60秒版_20260529.md`（当日用チートシート）
- `company-info/みずほフィナンシャルグループ/transcript/transcript_3次面接_20260529.md`（3次transcript・同期取込）
- `company-info/みずほフィナンシャルグループ/transcript/transcript_2次面接_20260526.md`（2次正本）
- `company-info/みずほフィナンシャルグループ/reflection_2次_20260526.md`（盲点＝潰すべき弱点）

## 📂 Out of scope
- research_brief 更新は別途（company-researcher経由）
- PR #39 マージ・別PC同期はユーザー側で実施
