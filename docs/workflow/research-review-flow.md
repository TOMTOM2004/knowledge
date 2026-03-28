# 企業・職種調査レビューフロー

企業調査・職種調査の実施から品質確認までの標準フロー。

---

## フロー全体図

```
[調査依頼] → [research_brief生成] → [調査品質チェック] → [不足調査] → [ES/面接転用]
     ↓                ↓                    ↓                 ↓
company-researcher  research_brief.md  research-gap-      company-researcher
                                      reviewer           (追加調査)
```

---

## Step 1: 初期調査

```
「[企業名]の企業調査をして」
→ company-researcher スキルが起動
→ company-info/[企業名]/research_brief.md を生成
```

---

## Step 2: 調査品質の確認

### 機械チェック
```bash
python tools/checks/research_checker.py [企業名]
```

### 調査ギャップ発見
```
「[企業名]の企業調査の不足を確認して」
→ research-gap-reviewer エージェント
```

### 職種調査の確認
```
「[企業名]の[職種名]の職種調査に不足がないか確認して」
→ role-research-reviewer エージェント
```

---

## Step 3: 追加調査

research-gap-reviewer が提示した「次に調べるべきクエリ」を使って:
```
「[企業名]の[不足論点]を調査して」
→ company-researcher スキルで補完調査
```

---

## Step 4: 職種比較（必要な場合）

```
「[企業A]と[企業B]の[職種]を比較して」
→ company-comparison-framework スキル
```

---

## Step 5: ES・面接への転用

調査が揃ったら:
```
「[企業名]のESを書いて」→ es-writer（research_briefを自動参照）
「[企業名]の面接準備をして」→ interview-prep（research_briefを自動参照）
```

---

## 企業調査の品質基準

| 項目 | 基準 |
|-----|------|
| research_brief 9軸のカバレッジ | 7軸以上は記述あり |
| 競合比較 | 主要競合2〜3社との比較あり |
| 採用情報 | 求める人材像の記載あり |
| キャリアパス | 入社後3〜5年の具体的な流れあり |
| 直近ニュース | 1年以内の重要ニュース3件以上 |
| 面接差別化ポイント | 「なぜこの会社か」の論拠3点以上 |
