# 面接OS 設計 v1（ブレインストーム版）

> **このドキュメントは初期ブレインストーム版です。**
> 現行の正式仕様は `docs/workflow/interview-os-design.md` を参照してください。
> ここには構想段階の詳細・ペルソナ定義・Phase設計・ログ仕様の下書きが残っています。
>
> 由来: `面接OS/plan.md`（2026-04-14 に knowledge リポジトリへ統合）

---

面接OS 詳細設計 v1

0. 目的

このシステムの目的は次の3つです。
	1.	企業差し替え式で、面接前の想定問答を高精度に生成すること
	2.	複数ペルソナの視点で深掘り・批評し、回答ごとの改善点を出すこと
	3.	模擬面接ログを蓄積して、次回以降の質問生成と弱点推定に再利用すること

特に主戦場は 2次面接 とし、
面接段階ごとに「聞かれている意図」が違う前提で動きます。

⸻

1. 全体アーキテクチャ

構成は5層です。

1-1. Knowledge Layer

既存の knowledge リポジトリをそのまま活かします。

主な入力源は以下です。
	•	company-info/<企業名>/research_brief.md
	•	company-info/<企業名>/interview_prep_*.md
	•	company-info/<企業名>/notes.md
	•	ES/素材/*.md
	•	ES/部品/*.md
	•	ES/企業別/作成中, ES/企業別/提出済, 移行後ES
	•	将来的な面接反省ログ
	•	将来的な transcript

ここは既存資産を読むだけで、Phase 1ではリポジトリ構造を大きく壊しません。

⸻

1-2. Config Layer

ここで「今回の模擬面接の条件」を決めます。

決めるのは以下です。
	•	企業名
	•	業界区分（金融 / テック）
	•	面接段階（1次 / 2次 / 最終）
	•	コース / 職種
	•	使用するES群
	•	使用するエピソード群
	•	重点テーマ
	•	使用ペルソナ
	•	セッション時間
	•	ランダム性の強さ

この情報を 1つの設定ファイル にまとめます。

⸻

1-3. Generation Layer

ここが質問生成層です。

役割は4つです。
	•	企業差し替え式の質問生成
	•	回答候補に基づく深掘り生成
	•	面接段階に応じた質問重み付け
	•	斜め質問・未知質問の差し込み

ここでは「面接官の人格」ではなく、
質問を作るロジック を分けます。

⸻

1-4. Simulation Layer

ここが模擬面接実行層です。

Phase 1では主に以下です。
	•	質問表示
	•	回答入力
	•	回答ごとの評価
	•	議論ログ保存
	•	フィードバック出力

Phase 2以降で、
	•	質問読み上げ
	•	音声録音
	•	逐語 / 整形 transcript
	•	時間情報抽出

を加えます。

⸻

1-5. Learning Layer

ここが蓄積層です。

保存するのは以下です。
	•	実際に聞かれた質問
	•	うまく答えられなかった質問
	•	詰まった時間
	•	技術話が通じなかった境界
	•	人事に伝わらなかった表現
	•	弱点プロファイル
	•	面接官ごとの刺さる深掘り

これはモデル再学習ではなく、ナレッジ蓄積です。

⸻

2. ディレクトリ構成

既存構成に追加する想定です。

knowledge/
├─ company-info/
│  └─ <企業名>/
│     ├─ research_brief.md
│     ├─ interview_prep_*.md
│     ├─ interview-os/
│     │  ├─ configs/
│     │  │  ├─ session_config_YYYYMMDD.yaml
│     │  │  ├─ persona_set_finance_2nd.yaml
│     │  │  └─ persona_set_tech_2nd.yaml
│     │  ├─ generated/
│     │  │  ├─ questions_YYYYMMDD.md
│     │  │  ├─ questions_YYYYMMDD.json
│     │  │  ├─ debate_log_YYYYMMDD.md
│     │  │  ├─ debate_log_YYYYMMDD.jsonl
│     │  │  ├─ feedback_YYYYMMDD.md
│     │  │  └─ feedback_YYYYMMDD.json
│     │  ├─ sessions/
│     │  │  └─ session_YYYYMMDD_HHMM/
│     │  │     ├─ metadata.yaml
│     │  │     ├─ questions_used.json
│     │  │     ├─ answers/
│     │  │     ├─ transcripts/
│     │  │     ├─ analysis/
│     │  │     └─ audio/
│     │  └─ learning/
│     │     ├─ observed_questions.md
│     │     ├─ weak_patterns.md
│     │     └─ boundary_notes.md
│
├─ transcripts/
│  ├─ others/
│  └─ mock-interviews/
│     └─ session_YYYYMMDD_HHMM/
│
├─ logs/
│  └─ interview-os/
│     └─ session_YYYYMMDD_HHMM/
│
├─ tools/
│  └─ interview_os/
│     ├─ prepare_session.py
│     ├─ run_session.py
│     ├─ evaluate_answer.py
│     ├─ persona_router.py
│     ├─ debate_manager.py
│     ├─ transcript_cleaner.py
│     ├─ timing_analyzer.py
│     └─ config_loader.py
│
└─ docs/
   └─ workflow/
      └─ interview-os-design.md


⸻

3. 実行フロー

実行入口は 2段階 にします。

3-1. Step 1: prepare-session

目的は、模擬面接前に必要な材料を固めることです。

入力:
	•	企業名
	•	面接段階
	•	コース / 職種
	•	使用ES
	•	重点テーマ
	•	セッション時間
	•	ペルソナセット

処理:
	•	research_brief.md 読み込み
	•	interview_prep_*.md 読み込み
	•	ES群読み込み
	•	エピソード読み込み
	•	質問候補生成
	•	ペルソナ別の想定深掘り生成
	•	ランダムに1問だけ混ぜる
	•	議論ログ生成
	•	質問セット保存

出力:
	•	session_config.yaml
	•	questions.md/json
	•	debate_log.md/jsonl

⸻

3-2. Step 2: run-session

目的は、実際に模擬面接を回すことです。

入力:
	•	session_config.yaml
	•	questions.json
	•	使用ペルソナ
	•	実行モード（text / text+audio）

処理:
	•	進行役が質問を出す
	•	ユーザーが回答
	•	裏の評価AI群が評価
	•	共通批評AIが差し込み判定
	•	次質問を選ぶ
	•	回答ごとにFB生成
	•	ログ保存

出力:
	•	feedback.md/json
	•	回答ログ
	•	将来的には音声 / transcript / timing

⸻

4. ペルソナ設計

4-1. 原則

ペルソナは 人格模倣 ではなく、
役割 + 業界差分 + 面接段階差分 で設計します。

つまり、
	•	何を見ているか
	•	何に違和感を持つか
	•	どう深掘りするか
	•	どの説明レベルを求めるか

を固定します。

⸻

4-2. 初期ペルソナ一覧

A. 人事（非技術理解弱め）

役割:
	•	分かりやすさ
	•	一貫性
	•	人柄
	•	志望動機の自然さ

特徴:
	•	技術話は伝わりにくい前提
	•	専門用語に弱い
	•	話が長いと厳しい
	•	結論と印象を重視

見る点:
	•	結論先行か
	•	難しすぎないか
	•	自分の言葉か
	•	他社でも言えそうでないか

⸻

B. テック現場

役割:
	•	実務理解
	•	再現性
	•	思考の筋道
	•	将来どう活きるか

特徴:
	•	技術の筋が通っているかを見る
	•	表面的な理解を嫌う
	•	ただし誇張も嫌う

見る点:
	•	実際に何をやったか
	•	なぜその判断をしたか
	•	どこまで自分で理解していたか

⸻

C. テック中堅 / 管理寄り

役割:
	•	成長可能性
	•	現場との接続
	•	将来の伸びしろ
	•	入社後の方向性

特徴:
	•	現場理解はあるが、それだけでは足りない
	•	中長期のキャリア像を見る

比重:
	•	成長 7
	•	実務 3

⸻

D. 金融営業現場

役割:
	•	顧客理解
	•	分かりやすさ
	•	相手に応じた説明
	•	実務との接続

特徴:
	•	明るめ、柔らかめ
	•	だが伝わるかどうかは厳しく見る
	•	テック話が長いとマイナス

⸻

E. 金融中堅 / 管理寄り

役割:
	•	伸びしろ
	•	会社理解
	•	中長期視点
	•	任せられるか

特徴:
	•	成長 7
	•	実務 3
	•	入社後の見通しや納得感を見る

⸻

F. 共通批評AI

役割:
	•	各回答全体を見て、痛いところを突く
	•	差し込み質問の要否判定
	•	論理飛躍や矛盾検出

特徴:
	•	感情を出さない
	•	褒めない
	•	冷静に不足点だけ指摘

⸻

G. 最終面接ペルソナ

役割:
	•	一貫性
	•	伸びしろ
	•	会社理解の深さ
	•	価値観
	•	判断力

特徴:
	•	斜め質問あり
	•	価値観や判断基準を問う
	•	答えの正しさより、人として任せられるかを見る

⸻

4-3. ペルソナ適用方式

各回ごとに、オン / オフ可能にします。

例:
	•	金融2次: 人事 + 金融営業現場 + 金融中堅 + 共通批評
	•	テック2次: 人事 + テック現場 + テック中堅 + 共通批評
	•	最終: 人事 + 最終面接 + 共通批評

⸻

5. 設定ファイル仕様

5-1. session_config.yaml

例:

company: "りそなグループ"
industry: "finance"
stage: "2nd"
course: "データサイエンス"
duration_minutes: 30

focus_themes:
  - "人事向けに分かりやすく話す"
  - "結論を先に言う"
  - "技術話を薄める"

input_sources:
  research_brief: "company-info/りそなグループ/research_brief.md"
  interview_prep:
    - "company-info/りそなグループ/interview_prep_2次個人面談_20260328.md"
  es_files:
    - "ES/素材/03_インターン_財務資料自動化.md"
    - "ES/部品/best_answers.md"

personas:
  - "hr_generalist"
  - "finance_front"
  - "finance_manager"
  - "common_critic"

question_policy:
  randomness: "one_random_question"
  depth_level: 2
  company_specificity_priority: high
  final_interview_mode: false

output:
  base_dir: "company-info/りそなグループ/interview-os/sessions/session_20260412_1430"


⸻

5-2. persona_set.yaml

例:

persona_id: "hr_generalist"
industry: "common"
tone: "calm_sharp"
technical_tolerance: low
core_axes:
  - clarity
  - consistency
  - motivation_fit
  - human_readability

dislikes:
  - jargon
  - long_intro
  - missing_conclusion

probe_styles:
  - clarify
  - simplify
  - consistency_check

feedback_mode:
  produce_dual_explanation: true


⸻

6. 質問生成ロジック

質問は4種類に分けます。

6-1. 基本質問
	•	ガクチカ
	•	志望動機
	•	自己PR
	•	強み / 弱み
	•	なぜこの会社か
	•	なぜこの職種か

⸻

6-2. 会社固有質問

research_brief.md から生成します。

例:
	•	なぜ競合ではなく当社か
	•	当社のどの課題に関心があるか
	•	このコースのどの業務で力を発揮できるか

⸻

6-3. 深掘り質問

各回答に対して出します。

型:
	•	具体化要求
	•	数字要求
	•	役割切り分け
	•	再現性確認
	•	他社比較
	•	弱点露出
	•	一貫性確認

⸻

6-4. ランダム質問

毎回1問だけ混ぜます。

目的:
	•	本番感
	•	暗記対策
	•	斜め対応力

型:
	•	趣味 / 特技
	•	最近気になったこと
	•	その強みが逆に弱みに出る場面
	•	もし失敗していたらどう説明するか
	•	30秒で言うと何か

⸻

7. フィードバック仕様

各回答ごとに出す形式は固定4区分です。

7-1. Markdown整形版

## Q3 人事ペルソナ
### 良い点
- 結論を先に置けていた
- 専門用語を抑えられていた

### 悪い点
- 理由の説明が抽象的
- 会社固有性が弱い

### 改善案
- 「なぜその行動を取ったか」を1文追加する
- りそな固有の文脈に接続する

### より良い言い回し
- 冒頭は「私が学生時代に最も力を入れたのは〜です」で始める
- 人事向けなら「Pythonで自動化した」より「作業の流れを整理し、自動化した」と言う


⸻

7-2. JSON版

{
  "question_id": "Q3",
  "persona_id": "hr_generalist",
  "good_points": [
    "結論先行",
    "専門用語を抑制"
  ],
  "bad_points": [
    "理由が抽象的",
    "会社固有性が弱い"
  ],
  "improvements": [
    "行動理由を1文追加",
    "企業文脈へ接続"
  ],
  "better_phrasing": {
    "hr_version": "私が学生時代に最も力を入れたのは、...",
    "technical_version": "既存の作業フローを分解し、Pythonで..."
  },
  "answer_skeleton": [
    "結論",
    "背景",
    "自分の工夫",
    "成果",
    "その会社でどう活きるか"
  ],
  "flags": {
    "logic_gap": true,
    "consistency_issue": false,
    "jargon_risk": true,
    "company_specificity_low": true
  }
}


⸻

8. ログ仕様

8-1. 回答ごとの記録項目

採用します。
	•	question_id
	•	persona_id
	•	question_text
	•	question_audio_path
	•	answer_audio_path
	•	answer_raw_transcript
	•	answer_clean_transcript
	•	response_latency_sec
	•	time_to_conclusion_sec
	•	speech_rate
	•	silence_segments
	•	evaluator_comments
	•	suggested_better_phrasing
	•	logical_gaps
	•	consistency_flags
	•	jargon_flags
	•	company_specificity_flags

⸻

8-2. AI議論ログ

両方残します。

生ログ

AIがどう議論したかのMarkdown

構造化ログ

JSONL

1行1件例:

{
  "turn": 3,
  "agent": "finance_manager",
  "candidate_question": "その経験は入社後どの部署でどう活きると考えていますか？",
  "reason": "成長可能性と業務接続がまだ曖昧",
  "priority": 0.82
}


⸻

8-3. セッションメタ情報

残します。
	•	企業名
	•	コース
	•	面接段階
	•	使用ES
	•	重点練習テーマ
	•	日時
	•	ペルソナ構成
	•	総質問数

⸻

9. 音声設計

9-1. Phase 1

音声は必須にしません。
	•	質問はテキスト表示
	•	回答はテキストでも可
	•	ただし構造はPhase 2を見据えて切る

⸻

9-2. Phase 2

ここで音声を入れます。
	•	AI質問の読み上げ
	•	一問ごと回答音声保存
	•	セッション全体録音
	•	Whisper系で逐語 transcript
	•	整形 transcript 生成
	•	応答開始時間
	•	結論到達時間
	•	話速
	•	沈黙時間

Aqua Voice は使わず、模擬面接用途では
逐語寄り ASR に統一 の前提でよいです。

⸻

9-3. Phase 3

理想状態です。
	•	より自然な会話テンポ
	•	音声読み上げの自然化
	•	リアルタイム寄りのターン制
	•	質問差し込みの即時性向上

⸻

10. 学習 / 蓄積設計

優先蓄積対象はこの順です。
	1.	実際に聞かれた質問
	2.	うまく答えられなかった質問
	3.	詰まった時間や表現
	4.	技術の話が通じなかった境界

⸻

10-1. weak_patterns.md の例

## 人事向け弱点
- 技術用語が多くなりやすい
- 結論までの到達が遅い
- 背景説明が長い

## オンライン面接弱点
- 初動が硬い
- 質問後すぐに「そうですね」と入る
- 一呼吸置く余裕がない

## 境界条件
- 技術者相手なら具体語を増やしてよい
- 人事相手では抽象化しすぎず、業務効果まで言い換える


⸻

11. Phase設計

Phase 1

最優先3点を反映します。

目的
	•	企業差し替え式の質問生成
	•	多エージェント議論ログ
	•	回答ごとのフィードバック

できること
	•	設定ファイル作成
	•	質問生成
	•	ペルソナ別候補質問生成
	•	共通批評AIの差し込み
	•	回答ごとの4区分FB
	•	JSON/Markdown保存

まだやらない
	•	音声
	•	transcript
	•	timing解析

⸻

Phase 2

目的
	•	音声 / transcript 導入
	•	ペルソナ別深掘り強化
	•	言い換え案強化

追加するもの
	•	AI質問読み上げ
	•	回答録音
	•	逐語 / 整形 transcript
	•	話速 / 沈黙 / 結論時間
	•	人事向け / 技術者向け言い換え
	•	深掘り2段の精度向上

⸻

Phase 3

理想像

企業差し替え式・音声付き・多エージェント議論内蔵の模擬面接OS

これです。

⸻

12. 今の knowledge リポジトリへの差し込み方

ここはかなり重要です。
今の構造を壊さず、追加だけで済ませます。

12-1. 既存資産の再利用

そのまま使うもの:
	•	research_brief.md
	•	interview_prep_*.md
	•	ES/md/*.md
	•	AGENTS.md
	•	.codex/skills
	•	docs/workflow/*

⸻

12-2. 新規追加だけで足すもの
	•	company-info/<企業名>/interview-os/
	•	tools/interview_os/
	•	logs/interview-os/
	•	transcripts/mock-interviews/
	•	docs/workflow/interview-os-design.md

⸻

13. スキル分割方針

専用スキルを会社ごとに切る必要は薄いです。
自然なのは 共通スキル + 企業別設定ファイル です。

おすすめの新規スキルは5つです。

13-1. interview-session-preparer

役割:
	•	セッション設定読み込み
	•	参照ファイル特定
	•	質問候補生成

13-2. interview-persona-router

役割:
	•	業界 / 段階 / 重点テーマに応じてペルソナ選択

13-3. interview-debate-orchestrator

役割:
	•	各ペルソナの質問候補を集約
	•	共通批評AIを含めて1問を選ぶ

13-4. answer-reviewer

役割:
	•	回答ごとの4区分FB生成
	•	人事向け / 技術者向け言い換え
	•	回答骨格生成

13-5. interview-learning-updater

役割:
	•	実際の失敗・詰まり・境界表現を学習ログに追加

⸻

14. ここまでの判断

結論として、この設計はかなり成立します。
しかも、今のあなたの knowledge は単なるメモ集ではなく、すでに ES/企業研究/面接準備のOSの原型 になっています。
なので、面接OSはゼロから作るのではなく、既存リポジトリの上に薄く載せる のが正しいです。

⸻

15. 次にやること

次はもう設計議論ではなく、実装用の仕様書に変換する段階 です。

順番としてはこうです。
	1.	docs/workflow/interview-os-design.md の本文を書く
	2.	session_config.yaml の正式スキーマを決める
	3.	初期ペルソナ定義ファイルを7本切る
	4.	Phase 1 のCLI仕様を書く
	5.	出力フォーマットのサンプルを1社分作る
