---
name: episode-formatter
description: Use this skill when the user wants to add a new episode or self-analysis entry to the ES episode library. Triggered by phrases like "エピソードを追加", "自己分析を追加", "草案を整形", "episode-formatter", "/episode". Takes rough draft content from the user and formats it into the standard episode template, then saves it to /Users/ishidatomonori/Desktop/knowledge/ES/md/.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Episode Formatter

ユーザーが書いた草案を、ESエピソードライブラリの定型フォーマットに整形して保存するスキル。

---

## Step 0: 草案の受け取り

ユーザーが提供した草案テキストを受け取る。草案がない場合は「どんなエピソード・内容を追加しますか？箇条書きでも構いません」と促す。

---

## Step 1: カテゴリ判定

草案の内容から以下のいずれかに分類する。

| カテゴリ | 判定基準 |
|---------|---------|
| `インターン` | 長期インターンでの業務・プロジェクト経験 |
| `バイト` | アルバイト・塾講師・球場スタッフ等 |
| `課外活動` | サークル・文化祭・個人活動（東海道等） |
| `学業` | ゼミ・授業・卒論・資格 |
| `GD記録` | グループディスカッション・面談・面接の振り返り |
| `自己分析` | 価値観・強み・弱み・将来像・行動原理 |
| `参考` | ツール・型・フレームワーク（エピソードではない資料） |

---

## Step 2: 次のファイル番号を確認

```bash
ls /Users/ishidatomonori/Desktop/knowledge/ES/md/ | grep -E "^[0-9]+" | sort -n | tail -1
```

現在の最大番号 + 1 を次の番号とする。

---

## Step 3: ファイル名を決定

形式: `<連番2桁>_<カテゴリ>_<エピソード名略称（10文字以内）>.md`

例: `16_インターン_新規クライアント分析.md`

---

## Step 4: フォーマット変換

草案をSTAR形式に展開してファイルを生成する。

**エピソード系（インターン/バイト/課外活動/学業/GD記録）の場合:**

```markdown
---
title: <エピソード名>
category: <カテゴリ>
source_files:
  - 草案（ユーザー手書き）
last_updated: <今日の日付 YYYY-MM-DD>
---

# <エピソード名>

## 概要

<2〜3文でエピソードの要点。結果・数値があれば冒頭に>

## STAR形式

### Situation（状況）

<背景・課題・当時の環境>

### Task（役割・目標）

<自分の役割と達成すべき目標>

### Action（行動）

<具体的な行動・工夫・判断のプロセス>

### Result（結果・学び）

<定量的成果（数値化できるものは必ず入れる）と得た学び>

## 面接・ES活用メモ

- どの設問で使えるか（ガクチカ/強み/失敗談/チームワーク 等）
- 強調すべきポイント
- 注意点・補足

## 生の記録（草案原文）

<ユーザーが書いた草案をそのまま保存>
```

**自己分析系（自己分析/参考）の場合:**

```markdown
---
title: <タイトル>
category: 自己分析
source_files:
  - 草案（ユーザー手書き）
last_updated: <今日の日付 YYYY-MM-DD>
---

# <タイトル>

## 内容

<草案の内容を整理・構造化して記述。箇条書き・見出しを活用>

## 面接・ES活用メモ

- どの設問・文脈で参照するか
- 強調すべき軸・表現

## 生の記録（草案原文）

<ユーザーが書いた草案をそのまま保存>
```

---

## Step 5: INDEX.md を更新

`/Users/ishidatomonori/Desktop/knowledge/ES/md/INDEX.md` の「ファイル一覧」テーブルに新しい行を追加する。

追加する行の形式:
```
| <番号> | [<ファイル名>](<ファイル名>) | <カテゴリ> | <タイトル> | <主な設問> |
```

「カテゴリ別まとめ」セクションにも該当カテゴリの項目を追加する。

---

## Step 6: 完了報告

以下を報告する:
- 作成したファイルパス
- カテゴリ判定の根拠
- STAR変換で補完した箇所（草案に足りなかった情報）
- 面接・ES活用メモの要点

不明な点（数値・日付・固有名詞）は変換時に `【要確認】` タグを付けてプレースホルダーとして残し、ユーザーに確認を促す。
