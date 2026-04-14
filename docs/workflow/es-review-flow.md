# ESレビューフロー（軽量モード）

**軽量モードが default。** 全 reviewer を毎回回さない。段階起動が標準。

詳細: `docs/workflow/quality-gates.md`

---

## フロー全体図

```
[ES草案] → [Gate1: script] → [Gate2: 設問+可読性] → [Gate3: 企業+職種適合] → [Gate4: 重複] → [提出]
                ↓                    ↓                        ↓                     ↓
          es_checker.py      question-fit            company-fit             consistency
                             readability             role-fit                -overlap
```

---

## Step 1: 事前準備

### 1-1. research_brief の確認
```
「company-info/[企業名]/research_brief.md を確認して。
 brief がなければ先に調査をして」
```

### 1-2. エピソード確認
```
「ES/素材/INDEX.md を見て、使えるエピソードを教えて」
```

---

## Step 2: ES草案作成（セッションC）

```
「[企業名]のESを書いて」→ es-writer が起動
```

参照するもの（最小限）:
- `company-info/<企業名>/research_brief.md`
- `ES/素材/INDEX.md`
- `ES/部品/best_answers.md`

---

## Step 3: Gate 1 — 機械チェック（必須）

```bash
python tools/checks/es_checker.py 移行後ES/[企業名].md
```

ERROR があれば先に修正してから次へ。

---

## Step 4: Gate 2 — 設問・可読性（必須、セッションC内）

```
「[企業名].md の設問適合と可読性を確認して」
→ question-fit-reviewer + readability-reviewer
```

草案段階ではここまで。

---

## Step 5: Gate 3 — 企業・職種適合（必須、セッションD）

**別セッションで実行することを推奨。**

```
「[企業名].md の企業適合と職種適合を確認して」
→ company-fit-reviewer + role-fit-reviewer
```

**前提**: `company-info/<企業名>/research_brief.md` が存在すること

---

## Step 6: Gate 4 — 重複・一貫性（設問 3つ以上の場合）

```
「[企業名].md の設問間の重複を確認して」
→ consistency-overlap-reviewer
```

---

## Step 7: 改善

```
「[reviewer名]の指摘を踏まえて[企業名].md を改善して」
→ editor-refiner（指摘が多い場合）または直接修正
```

---

## Step 8: Gate 5 — 面接深掘り（面接前のみ）

別セッション（セッションE）で実行:

```
「[企業名].md で面接で突っ込まれそうな質問を出して」
→ skeptical-interviewer
```

---

## 段階起動まとめ

| Gate | reviewer | セッション | スキップ可否 |
|------|---------|----------|-----------|
| Gate 1 | es_checker.py | C | スキップ不可 |
| Gate 2 | question-fit + readability | C | スキップ不可 |
| Gate 3 | company-fit + role-fit | D | スキップ不可 |
| Gate 4 | consistency-overlap | D | 設問 2つ以下ならスキップ可 |
| Gate 5 | skeptical-interviewer | E | 書類段階ならスキップ可 |
| Gate 6 | editor-refiner | D or E | 指摘なければスキップ可 |

---

## ⚠️ やってはいけないこと

- 草案段階で company-fit / role-fit / skeptical-interviewer を呼ばない
- `es-review-protocol` で全 reviewer を一括起動しない（重すぎる）
- 「全体的にレビューして」という依頼をそのまま通さない

### 一括レビューが必要な場合（例外）

第一志望の最終提出前など特別な場合のみ:
```
「[企業名].md を全体的にレビューして」
→ es-review-protocol（全エージェントを呼ぶ・高コスト）
```
