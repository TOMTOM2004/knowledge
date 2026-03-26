# Knowledge ナレッジベース

就職活動・面接・企業調査・ES執筆のためのナレッジリポジトリ。

---

## スキル使用ルール（必ず遵守）

### company-researcher — 企業調査
**以下のいずれかに該当したら、必ずこのスキルを起動する。自前で調査を走らせてはならない。**

- 企業名が含まれるリサーチ・調査依頼（「〇〇を調べて」「〇〇の企業研究」「〇〇のリサーチブリーフ」）
- 面接前準備の依頼（「〇〇の面接対策」「〇〇の面接準備」）
- `company-info/<企業名>/` フォルダ内で作業しているとき

起動方法: `/company-researcher` を自分で呼び出すか、上記条件に合致したと判断したら自動で実行する。

---

### interview-prep — 面接準備
**面接準備・想定問答・逆質問の依頼があったら、このスキルを起動する。**

- 「〇〇の面接の想定問答を作って」「逆質問を考えて」「面接でどう答えるか」

起動方法: `/interview-prep`

---

### es-writer — ES執筆
**ESの設問に対して回答を書く依頼があったら、このスキルを起動する。**

起動方法: `/es-writer`

---

### es-improver / es-refiner — ES改善
**既存のES文章を改善・添削する依頼があったら起動する。**

起動方法: `/es-improver` または `/es-refiner`

---

### episode-formatter — エピソード整形
**エピソードをSTAR形式・PREP形式などで整形する依頼があったら起動する。**

起動方法: `/episode-formatter`

---

## ディレクトリ構成

```
knowledge/
├── company-info/<企業名>/   # 企業ごとの調査・面接記録
│   ├── research_brief.md    # 企業調査ブリーフ（company-researcherが生成）
│   ├── interview_prep_*.md  # 面接前準備
│   └── transcript_*.md      # 面接文字起こし（Windowsで生成後pushされる）
├── ES/                      # エントリーシート関連
├── 移行後ES/                 # 確定版ES
├── transcripts/others/      # 就活以外の文字起こし
└── tools/transcribe.py      # Windows向け文字起こしスクリプト
```
