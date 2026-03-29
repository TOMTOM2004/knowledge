# エージェント使用ガイド（軽量モード版）

各 subagent をいつ・どう使うかのガイド。**段階起動が default。**

コスト分類: `docs/workflow/agent-cost-tiering.md`
品質ゲート: `docs/workflow/quality-gates.md`

---

## 使い分けの原則

- **スキル（skill）**: 決まった手順で作業する（ES作成・調査・フォーマット変換等）
- **エージェント（agent）**: 特定の視点からレビュー・評価・質問生成を行う

スキルは「何を作るか」、エージェントは「どう評価するか」。

---

## 段階別の起動順序

```
Gate 2（草案後）: question-fit → readability
Gate 3（仕上げ）: company-fit → role-fit
Gate 4（横断）:  consistency-overlap
Gate 5（面接前）: skeptical-interviewer
Gate 6（修正）:  editor-refiner
```

**草案段階で Gate 3〜5 を呼ばない。**

---

## ES系エージェント — Tier 1（軽量）

### question-fit-reviewer
**使う場面**: 草案完成直後（Gate 2）

```
「[企業名].md の各設問に正面から答えているか確認して」
```

**特徴**: 内容の良し悪しは評価しない。「聞かれたことに答えているか」だけを評価。
**Tier**: 1（軽量モデルで十分）

---

### readability-reviewer
**使う場面**: 草案完成直後（Gate 2）

```
「[企業名].md の可読性をチェックして」
```

**特徴**: 内容ではなく「伝わりやすさ」だけを評価。技術用語・長文・結論の遅さを指摘。
**Tier**: 1（軽量モデルで十分）

---

## ES系エージェント — Tier 2（中程度）

### consistency-overlap-reviewer
**使う場面**: 設問が 3つ以上ある企業の ES仕上げ時（Gate 4）

```
「[企業名].md の設問間の重複を確認して」
```

**Tier**: 2（標準）

---

### editor-refiner
**使う場面**: 他の reviewer の指摘を受けて実際に文章を改善したいとき（Gate 6）

```
「question-fit-reviewer の指摘を踏まえて[企業名].md を改善して」
「可読性の問題を修正して字数 300字以内に収めて」
```

**Tier**: 2（標準）

---

### research-gap-reviewer
**使う場面**: ES作成・面接準備前に調査品質を確認したいとき

```
「[企業名]の企業調査の不足を確認して」
```

**使わない場面**: ES 執筆中（調査と執筆は別セッション）
**Tier**: 2（標準）

---

## ES系エージェント — Tier 3（重い推論）

### company-fit-reviewer
**使う場面**: ES仕上げ段階（Gate 3）。提出前の最終確認。

```
「[企業名].md が[企業名]向けになっているか確認して」
```

**前提**: `company-info/<企業名>/research_brief.md` が存在すること
**草案段階では使わない。**
**Tier**: 3（重い推論）

---

### role-fit-reviewer
**使う場面**: ES仕上げ段階（Gate 3）。職種系設問を書いたとき。

```
「[企業名].md が[職種名]向けになっているか確認して」
```

**草案段階では使わない。**
**Tier**: 3（重い推論）

---

### skeptical-interviewer
**使う場面**: ES完成後・面接準備時（Gate 5）。ES草案段階では使わない。

```
「[企業名].md で面接で突っ込まれそうな質問を出して」
「この志望動機で 2次面接で詰められる質問を生成して」
```

**書類選考段階では使わない。面接 1週間前以降に使う。**
**Tier**: 3（重い推論）

---

### role-research-reviewer
**使う場面**: 職種理解が浅いと感じるとき、職種系設問の回答前

```
「[企業名]の[職種名]の職種調査に不足がないか確認して」
```

**Tier**: 2〜3（内容次第）

---

## エージェント選択チートシート

| 状況 | Gate | 使う agent | Tier |
|-----|------|-----------|------|
| 草案完成直後 | Gate 2 | question-fit + readability | 1 |
| 仕上げ段階（企業・職種） | Gate 3 | company-fit + role-fit | 3 |
| 3設問以上の横断確認 | Gate 4 | consistency-overlap | 2 |
| 指摘後の文章修正 | Gate 6 | editor-refiner | 2 |
| 企業調査が薄い | — | research-gap-reviewer | 2 |
| 職種調査が薄い | — | role-research-reviewer | 2〜3 |
| 面接前の自己チェック | Gate 5 | skeptical-interviewer | 3 |

---

## ⚠️ やってはいけないこと

- `es-review-protocol` で全 reviewer を一括起動する（高コスト）
- 草案段階で Tier 3 の agent を使う
- 調査フェーズと執筆フェーズを同じ会話で混在させる
