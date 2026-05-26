# Handoff — みずほFG 2次面接 想定問答集 大幅改訂完了（卒論テーマ変更・コース確定を全面反映）
_Last updated: 2026-05-26 / session: みずほ2次QA 抜本改訂_

## 🎯 Next action（1つだけ、具体的に）
- What: みずほFG 2次面接の**模擬面接（声出し練習）**。skeptical-interviewer または interview-debate-orchestrator で実戦
- Where: `company-info/みずほフィナンシャルグループ/interview_qa_2次面接_20260515.md`（高1-10・中1-5・Step2.5/3/4）
- Done when: 高7(なぜみずほ)・高4(ガクチカ)・高10(挫折)・高8(キャリア)・高1(自己紹介) が30/60秒で自然に出る＋深掘り耐性
- 着手タイミング: 2次面接の日程が見えたら

## 🎉 本セッション成果（2026-05-26）※全て `claude/20260524-mizuho-2ji-qa-augment` に push 済
- **みずほ2次想定問答集を大幅改訂**:
  - 1次(5/12福崎面談)反省で補強／【高1】自己紹介PREP脱却・自然な流れ／【高2】幼少期を「仕組みへの好奇心」起点に抜本改訂／【高8】なぜRM起点(ヒアリング力→リサーチ)新設／【高7-B】グループオープン型・SC/RM横断スタンス／【高10】挫折を2エピソード格上げ／【中5】チーム経験追加／面接概要(40分/8-12問)
  - Step2.5/3(15観点)/4 を1次transcript・ES反映で見直し
- **1次面接(5/25)を文字起こし格納**（mlx-whisper）→ コース確定：**グループオープン型=BK/TB法人＋SC法人WM併願／志望順位 銀行信託>証券**。評価された軸＝「幅広く経験→専門性」(ES設問14)
- **卒論テーマ変更を全面反映**: 旧「手取り増×消費(POS/DID)」→現「輸入価格ショック→所得流出→家計消費の異質性→政策シミュ」。エピソード18全面改訂＋リネーム、01§9更新、【高1】【高5】波及修正
- **ES素材追加**: 33幼少期(仕組み好奇心)、34進め方失敗、35塾PoC(定性定量化の限界)。07東海道の事実訂正
- **transcript を transcript/ サブフォルダに集約**（スキル3つ両対応化・CLAUDE.md規約更新）

## 📍 State snapshot
- ✅ Done: 上記すべて push 済（ブランチ claude/20260524-mizuho-2ji-qa-augment）
- 🟡 In progress: なし
- 🔴 Blocked: なし

## 🧠 Context not in code
- **コース確定**: グループオープン型（BK/TB法人＝産業調査・AM／SC法人WM＝リサーチ・クオンツ）。軸足は銀行・信託。問答集 frontmatter・接続マップ反映済
- **ブレ防止の核**: ES設問14「幅広いキャリアフィールド×専門性が高い」＝1次で「素晴らしい」と評価された軸。全設問で貫く。"色々やりたい"に転落させず到達点(産業調査起点M&A)を必ず添える
- **卒論**: graduation-thesis で Phase1-3完了（交易損失34.6兆円/転嫁β=0.431/逆進性/政策シミュ）。**POS・傾向スコア・DID・IVは旧テーマ＝使わない**
- **塾PoC**: 長期インターン案件（小学校受験塾・面談記録定量化PoC）。定性は定量化しきれず「聞き方の標準化・人間の役割」が学び。塾講師バイト(05)とは別物
- **OSS化・マネタイズ構想**: personal-tasks/tasks/todo.md に起票（AM比較エンジン汎用化が第一弾候補）

## ❌ Don't do (this task)
- [feedback] 自己紹介にPREP法を強制しない（所属→学業→課外→意気込みの自然な流れ。PREPは志望理由・ガクチカ等の論点回答向け）
- [feedback] 自己分析で価値観を語る時、生得的特性か環境影響(親等)かを区別。出所が曖昧な特性を「幼少期から」と盛らない
- [trap] 長期インターンはチームワーク文脈で使わない（一人完遂が強み。チームは塾講師リーダー05・文化祭06）
- [trap] macOS TCC: bash経由プロセスはDesktop配下の新規DL/転送ファイル(quarantine付)を open 不可(EPERM)。dangerouslyDisableSandbox でも無効 → Finder複製でquarantine除去 or ホーム直下/tmpへ移動して回避

## ❓ Open questions for user
- [ ] research_brief.md（みずほ）の更新: 卒論1行＋一次情報(5/12,5/25,コース確定)を軸7/8に反映（company-researcher経由）。実益と鮮度向上のタイミング次第
- [ ] 模擬面接（声出し）をいつ実施するか
- [ ] みずほ2次のブランチを PR化して main マージするか

## 📂 Key files
- `company-info/みずほフィナンシャルグループ/interview_qa_2次面接_20260515.md`（本日の主成果）
- `company-info/みずほフィナンシャルグループ/transcript/transcript_1次面接_20260525.md`（コース確定の根拠）
- `ES/素材/{18卒論輸入価格,33幼少期,34進め方,35塾PoC}.md`
- `graduation-thesis/docs/`（卒論本体・新テーマ）

## ❌ Out of scope
- research_brief 更新は別途（company-researcher経由）
- 塾PoC・34進め方の細部（手法・数値）は記憶限定で【要確認】残し

- [ ] #travel-planner
予定通りで問題ないので価格や今予約をとってしまうものについてリストアップする。（Slack #todo より _2026-05-16_）
