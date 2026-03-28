# ESレビューフロー

ES作成から提出前チェックまでの標準フロー。

---

## フロー全体図

```
[エピソード収集] → [ES草稿作成] → [機械チェック] → [多角レビュー] → [改善] → [提出]
     ↓                ↓                ↓               ↓             ↓
episode-formatter   es-writer      tools/checks/   agents/       editor-refiner
                                   es_checker.py
```

---

## Step 1: 事前準備

### 1-1. エピソードライブラリの確認
```
「ES/md/INDEX.md を見て、使えるエピソードを教えて」
```

### 1-2. 企業調査の確認（未調査の場合）
```
「[企業名]の企業調査をして」→ company-researcher スキルが起動
```

### 1-3. 企業調査の品質チェック
```
python tools/checks/research_checker.py [企業名]
```
または
```
「[企業名]の企業調査の不足を確認して」→ research-gap-reviewer エージェントが参照
```

---

## Step 2: ES草稿作成

```
「[企業名]のESを書いて」→ es-writer スキルが起動
```

es-writerは以下を参照して自動生成:
- `ES/components/best_answers.md`（コア参照）
- `ES/md/INDEX.md`（エピソード一覧）
- `company-info/[企業名]/research_brief.md`（企業固有情報）

---

## Step 3: 機械チェック

```bash
python tools/checks/es_checker.py 移行後ES/[企業名].md
```

**確認項目**: 禁止表現・敬称混在・未回答・重複表現・技術語過多・抽象語過多・数字不足

ERRORがあれば先に修正してから次へ進む。

---

## Step 4: 多角レビュー

### 4-1. 設問適合チェック（最優先）
```
「[企業名].mdの各設問に正面から答えているか確認して」
→ question-fit-reviewer エージェント
```

### 4-2. 可読性チェック
```
「[企業名].mdの可読性をチェックして」
→ readability-reviewer エージェント
```

### 4-3. 企業適合チェック
```
「[企業名].mdが[企業名]向けになっているか確認して」
→ company-fit-reviewer エージェント
```

### 4-4. 職種適合チェック
```
「[企業名].mdが[職種名]向けになっているか確認して」
→ role-fit-reviewer エージェント
```

### 4-5. 重複チェック
```
「[企業名].mdの設問間の重複を確認して」
→ consistency-overlap-reviewer エージェント
```

### 一括レビュー（時間がない場合）
```
「[企業名].mdを全体的にレビューして」
→ es-review-protocol スキルが各エージェントを順番に呼び出す
```

---

## Step 5: 改善

```
「[reviewer名]の指摘を踏まえて[企業名].mdを改善して」
→ editor-refiner エージェント
```

または直接修正する。

---

## Step 6: 面接深掘り耐性チェック

```
「[企業名].mdで面接で突っ込まれそうな質問を出して」
→ skeptical-interviewer エージェント
```

---

## Step 7: 改善内容の知識ベースへの還元（任意）

### 提出後に実施
```
「[企業名].mdからfoundationsを更新して」→ es-refiner スキル
「ES改善点をskill-update-logに追加して」→ 手動記入
```

---

## レビュー判断基準

| 判定 | 基準 | アクション |
|-----|------|----------|
| 提出可 | 全reviewer評価 ○以上 | そのまま提出 |
| 修正後提出 | 1〜2項目 △あり | editor-refinerで修正後提出 |
| 大幅修正必要 | 複数項目 ✗あり | 草稿から見直し |
