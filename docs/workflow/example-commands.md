# Claude Code 実行例（軽量モード版）

**軽量モードが default。** セッションを分割して使う。
詳細: `docs/workflow/lightweight-mode.md`

⚠️「全部まとめてやって」は非推奨（→ 下部に移動）

---

## セッションA: 企業調査 → research_brief を作る

```
「[企業名]の企業調査をして。
 research_brief.md に保存して。この会話では ES は書かない」
```

→ `company-info/<企業名>/research_brief.md` が生成される

---

## セッションB: brief の確認・補強（任意）

```
「company-info/[企業名]/research_brief.md を読んで、
 志望動機と競合比較の論点が十分か確認して。
 不足があれば補充して」
```

---

## セッションC: brief だけで ES 草案を作る

```
「[企業名]のESを書いて。
 参照は research_brief.md と INDEX.md と best_answers.md だけでいい。
 レビューは question-fit と readability だけやって」
```

→ `移行後ES/<企業名>.md` に草案が生成される
→ question-fit + readability が起動

---

## セッションD: ES 仕上げ（企業・職種・重複）

```
「[企業名].md を読んで、company-fit と role-fit を確認して。
 指摘があれば editor-refiner で修正して」
```

設問が 3つ以上の場合は追加:
```
「[企業名].md の設問間の重複も確認して」
```

---

## セッションE: 面接準備（interview skill に切り替える）

```
「[企業名]の[N]次面接の準備をして。
 interview-prep を使って。ESレビューはしなくていい」
```

---

## 草案確認だけ（question-fit + readability のみ）

```
「[企業名].md の設問適合と可読性だけ確認して。
 company-fit と role-fit はまだやらなくていい」
```

---

## 仕上げ確認（company-fit + role-fit + consistency）

```
「[企業名].md の企業適合・職種適合・設問間重複を確認して。
 readability はやらなくていい（前回確認済み）」
```

---

## 面接前の深掘り耐性確認（skeptical-interviewer のみ）

```
「[企業名].md で[N]次面接で突っ込まれそうな質問だけ出して。
 ES の修正はしなくていい」
```

---

## 文系若手面接官向けに表現をやさしくする

```
「[企業名].md を文系の新卒採用担当者（入社 2年目）目線で確認して。
 専門用語が多い部分があれば言い換え案も出して。
 readability-reviewer を使って」
```

---

## 最終面接前夜の深掘り対策

```
「[企業名]の最終面接（役員）の対策をして。
 特に競合比較の反論となぜここかの深掘りに備えたい。
 skeptical-interviewer と rebuttal-handling だけ使って」
```

---

## 不要な skill を読まずに進める

```
「[企業名]の志望動機 ES を書いて。
 banking-fit か digital-fit か finance-common だけ読んでいい。
 interview 系 skill は読まなくていい」
```

---

## research_brief 確認後すぐ ES を書く（2ステップ最短）

```
# Step 1（セッションA）
「[企業名]の企業調査をして research_brief.md を作って」

# Step 2（セッションC・別会話）
「[企業名]のESを書いて。参照は research_brief.md だけでいい」
```

---

## 品質チェック（手動実行）

```bash
# ES ファイルをチェック
python tools/checks/es_checker.py 移行後ES/<企業名>.md

# 企業調査の品質確認
python tools/checks/research_checker.py <企業名>
```

---

## スキル更新フロー

```
「今日の面接で[こういう指摘を受けた]。skill-update-log に記録して」
「[企業名].md の改善点を foundations に反映して」→ es-refiner
「es-writer スキルを今回の編集差分から改善して」→ es-improver
```

---

## ⚠️ 非推奨（高コスト・軽量モード違反）

以下の依頼は高コストになるため、特別な理由がない限り使わない:

```
# ❌ 全部まとめてやる（調査 + ES + レビュー）
「[企業名]の企業調査からESまで全部やって」

# ❌ 全 reviewer を一括起動
「[企業名].md を全体的にレビューして」
→ es-review-protocol が全エージェントを呼ぶ

# ❌ 草案段階で面接系 agent を呼ぶ
「ES草案に対してお突っ込み質問も出して」
```

**例外**: 第一志望の最終提出前等、重要な場面のみ一括を許可する
