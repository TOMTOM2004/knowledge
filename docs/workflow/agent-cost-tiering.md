# エージェント コスト Tiering

agent を「全部同じ重さ」で使わない。目的に応じてコスト配分を変える。

---

## Tier 分類

### Tier 1 — 軽量モデルで十分

文体・形式・パターンマッチングで判断できる作業。推論深度は浅くてよい。

| agent | 主な判定 | 理由 |
|------|---------|------|
| `readability-reviewer` | 文体・長さ・語彙の難易度 | 表現評価は意味理解より形式判断 |
| `question-fit-reviewer` | 設問と回答の対応関係 | 「答えているか」はロジック確認 |

**使う条件**: 草案確認・早期フィードバック段階

---

### Tier 2 — 中程度（標準モデル）

内容の整合性・業界知識の照合が必要。ある程度の推論が要る。

| agent | 主な判定 | 理由 |
|------|---------|------|
| `editor-refiner` | 指摘に基づく文章の改善提案 | 指摘が明確な場合は生成精度で十分 |
| `consistency-overlap-reviewer` | 設問間のエピソード・強みの重複 | 複数文書の照合だが判断軸は明確 |
| `research-gap-reviewer` | 調査の不足論点を特定 | 構造化された評価軸に従う |

**使う条件**: ES仕上げ段階・調査品質確認

---

### Tier 3 — 重い推論が必要

深い意味理解・反論想定・複合的な論理評価が必要。

| agent | 主な判定 | 理由 |
|------|---------|------|
| `skeptical-interviewer` | 面接官の深掘り質問・反論の想定 | 相手の思考を模倣する必要がある |
| `company-fit-reviewer` | 企業固有性の有無・一般論の検出 | 業界知識と論旨評価の組み合わせ |
| `role-fit-reviewer` | 職種適合の深度・キャリアビジョンの整合 | 業界・職種の理解と個人の論旨を照合 |

**使う条件**: ES最終確認・面接前・重要企業のみ

---

## 起動コスト別フロー

### 最小コスト（草案確認）
```
Tier 1 のみ:
→ question-fit-reviewer
→ readability-reviewer
```

### 標準コスト（ES仕上げ）
```
Tier 1 完了後:
→ consistency-overlap-reviewer（Tier 2）
→ editor-refiner（Tier 2）
```

### 最大コスト（最終品質ゲート）
```
Tier 2 完了後:
→ company-fit-reviewer（Tier 3）
→ role-fit-reviewer（Tier 3）
→ skeptical-interviewer（Tier 3・面接前のみ）
```

---

## 重い agent を使う条件

`company-fit-reviewer`、`role-fit-reviewer` を使うのは以下の場合に限る:

- 提出前の最終確認
- 第一志望・重要企業の ES
- 一般論的な表現が多いと感じた場合
- 志望動機系の設問が含まれる ES

`skeptical-interviewer` を使うのは以下の場合に限る:

- ES 完成後（草案段階では使わない）
- 面接 1週間前以降
- 2次以降の面接前

---

## role-research-reviewer の位置づけ

- 職種調査の網羅性を確認する専用 agent
- 使うのは「職種理解が薄いと感じるとき」のみ
- Tier 2 相当（内容評価だが軸が明確）

---

## まとめ

| Tier | agent | 使う場面 |
|------|-------|---------|
| 1 | readability, question-fit | 草案確認（セッションC） |
| 2 | consistency, editor-refiner, research-gap | 仕上げ（セッションD） |
| 3 | company-fit, role-fit, skeptical | 最終ゲート（セッションD末・E） |
