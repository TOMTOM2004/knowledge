# 軽量モード運用ガイド

**軽量モードが default。** 全部を1セッションでやる運用はやめる。

---

## 軽量モードの5原則

1. **セッション分割** — 調査/執筆/レビュー/面接は別会話
2. **brief 一次参照** — 詳細調査ファイルを直接読まない
3. **skill 最小セット** — 必要な skill だけを呼ぶ
4. **段階起動** — reviewer を全部同時に回さない
5. **script 優先** — 機械的チェックは script に任せる

---

## セッション別ロード量の目安

| セッション | 読むもの | 目安サイズ |
|----------|---------|----------|
| A: 調査 | company-researcher SKILL + WebSearch | 10 KB + web |
| B: brief整形 | research_brief.md | 3〜7 KB |
| C: ES草案 | brief + INDEX.md + 必要 components 1本 | 20〜40 KB |
| D: ES仕上げ | ES本文 + brief | 15〜25 KB |
| E1: 面接調査 | interview-research SKILL + WebSearch | 5 KB + web |
| E2: 想定問答 | interview_research ファイル + brief + ES + 自己分析2本 | 25〜40 KB |

**参考: 全部1セッション（旧運用）の場合: 100〜200 KB**

---

## セッションごとの推奨依頼文

### セッションA: 企業調査

```
「[企業名]の企業調査をして。結果を research_brief.md に保存して。
 この会話ではESは書かない」
```

### セッションB: brief 確認・補強（必要時のみ）

```
「company-info/[企業名]/research_brief.md を読んで、
 志望動機と職種適合の論点が十分か確認して。
 不足があれば補充して」
```

### セッションC: ES草案

```
「[企業名]の[設問リスト]を書いて。
 参照するのは research_brief.md と ES/md/INDEX.md だけでいい。
 レビューはしなくていい」
```

### セッションD: ES仕上げ

```
「[企業名].md を読んで、question-fit と readability だけ確認して。
 company-fit と role-fit は最後にやる」
```

（続きは別コマンドで: 「company-fit と role-fit と consistency を確認して」）

### セッションE1: 面接調査

```
「[企業名]の[N]次面接の選考調査をして。
 interview-research を使って。ESレビューはしなくていい」
```

### セッションE2: 想定問答

```
「[企業名]の[N]次面接の想定問答を作って。
 interview-qa を使って。調査ファイルは interview_research_[ステップ]_*.md を読んで」
```

---

## やってはいけないこと（軽量モード違反）

| 違反パターン | 代替 |
|------------|------|
| 「全部まとめてやって」（調査+ES+レビュー） | セッション分割 |
| 「全体的にレビューして」（全 reviewer 一括） | 段階起動（C→D） |
| 詳細調査ファイルを直接 ES 執筆に使う | brief 経由 |
| finance-common と digital-common を同時に読む | 業種を1つ選ぶ |
| ES 執筆中に interview 系 skill を混入 | 面接セッションで使う |
| 草案段階で skeptical-interviewer を回す | ES 完成後に回す |
| E1・E2を同一セッションで実行する | 別セッションに分割する |
| interview-research なしで interview-qa を実行する | 必ず E1 を先に完了させる |

---

## 急ぎの場合（時間がない最小セット）

```
「[企業名].md を書いて。
 レビューは question-fit と readability だけ。
 company-fit は brief を自分で確認する」
```

---

## 通常モードに切り替える基準

以下の場合は全 reviewer を回してもよい:
- 第一志望企業の最終提出前
- 3ヶ月以上ぶりに ES を書く場合
- 大幅な文章変更後の総確認

それ以外は軽量モードを維持する。
