# 調査スキル設計ガイド

企業調査・職種調査に使用するスキルの設計思想・使い分け・組み合わせパターンを説明する。

---

## 調査スキルの全体像

```
調査プロセス
    │
    ├── [入力] 企業名・志望職種・コース
    │
    ├── Step 1: 調査レンズ選択
    │   ├── research/asset-management-research-lens  ← AM企業
    │   ├── research/banking-research-lens           ← 銀行
    │   ├── research/securities-research-lens        ← 証券
    │   ├── research/digital-research-lens           ← 金融デジタル
    │   ├── research/fund-manager-research-lens      ← 運用職
    │   ├── research/data-science-research-lens      ← DS職
    │   └── research/dx-consulting-research-lens     ← DXコンサル職
    │
    ├── Step 2: 調査実行
    │   └── company-researcher (SKILL.md) — 9軸 research_brief 生成
    │
    ├── Step 3: 品質確認
    │   ├── company-research-audit — 22点スコアリング
    │   ├── research-gap-finding   — P0/P1/P2 分類・クエリ生成
    │   └── role-research-audit    — 職種調査チェックリスト
    │
    └── Step 4: ギャップ補完
        ├── P0: 自動追加調査（company-researcher Step 7）
        ├── P1: 自動追加調査
        └── P2: リスト提示のみ
```

---

## 調査レンズスキルの設計

### なぜ「レンズ」という概念か

同じ企業でも「運用会社として調べる」のと「信託銀行の資産運用部門として調べる」では、
見るべき情報が大きく異なる。`research/` スキルは「どの観点で企業・職種を調べるか」の
**フレーム設計**を担当する。

- **調査クエリの設計**: 何を検索するかのキーワード・問いの立て方
- **評価軸の定義**: 何を見つければ「調査完了」か
- **ES/面接への接続**: 調査結果をどの設問・どの回答に使うか

### 業種レンズ vs 職種レンズ

| レンズ種別 | ファイル | 何を見るか |
|----------|---------|----------|
| **業種レンズ** | `research/asset-management-research-lens` | 会社全体の事業・競合・戦略 |
| | `research/banking-research-lens` | 会社全体の事業・競合・戦略 |
| | `research/securities-research-lens` | 会社全体の事業・競合・戦略 |
| | `research/digital-research-lens` | 会社全体のデジタル戦略・体制 |
| **職種レンズ** | `research/fund-manager-research-lens` | 運用職の業務・キャリア・若手関与 |
| | `research/data-science-research-lens` | DS職の組織・ツール・ビジネス協働 |
| | `research/dx-consulting-research-lens` | DX推進体制・変革実績・外部委託比率 |

**原則**: 業種レンズ + 職種レンズを組み合わせる。例:

- 「ニッセイAMの運用職」→ `asset-management-research-lens` + `fund-manager-research-lens`
- 「三菱UFJ銀行のDS職」→ `banking-research-lens` + `data-science-research-lens`

---

## research_brief.md の9軸とスキルの対応

| 軸 | 主な調査レンズ | 補完スキル |
|---|-------------|----------|
| 軸1: 基本情報 | 全業種レンズ共通 | `company-research-audit` |
| 軸2: 事業内容 | 業種別レンズ | `company-research-audit` |
| 軸3: 競合比較 | 業種別レンズ | `company-comparison-framework` |
| 軸4: IR/財務 | 業種別レンズ | `company-research-audit` |
| 軸5: 採用情報 | 職種別レンズ | `role-research-audit` |
| 軸6: キャリア | 職種別レンズ | `role-research-audit` |
| 軸7: 戦略/文化 | 業種別レンズ | `research-gap-finding` |
| 軸8: ニュース | 全業種レンズ共通 | `research-gap-finding` |
| 軸9: 面接差別化 | 競合比較レンズ | `company-comparison-framework` |

---

## ギャップ補完の優先度設計

### P0（自動追加調査トリガー）
**ES・面接の核心に直結する情報が不足している**

例:
- 志望動機の核（軸7-4）が空白
- 競合比較（軸3・軸9）が「同業他社と比較して」のみ
- キャリアパス（軸6）がウェブサイト情報の転記のみ

対応: company-researcher が自動追加調査を実行

### P1（自動追加調査トリガー）
**面接で突っ込まれる可能性が高い情報が不足**

例:
- 直近のニュース（軸8）が1年以上前
- 志望コース固有の業務内容が未調査
- AUM・運用残高などの定量情報が欠落

対応: company-researcher が自動追加調査を実行

### P2（リスト提示のみ）
**補足情報として有れば良いが必須ではない**

例:
- 社員インタビューの一次情報
- 創業の歴史・沿革の詳細
- 競合他社の詳細な財務データ

対応: ユーザーへの調査推奨リストとして提示のみ

---

## 調査品質チェックの自動化

### research_checker.py との連携

```bash
# 個別企業チェック
python tools/checks/research_checker.py company-info/<企業名>/research_brief.md

# 全企業一括チェック
python tools/checks/research_checker.py --all
```

チェック項目:
1. 必須軸（軸3・軸7・軸9）の記述量
2. 【要補完】タグの残存数
3. 情報の鮮度（1年以内か）
4. 定量情報（数字）の有無
5. 競合比較の具体性
6. 職種調査の分離度

---

## 調査スキル追加の基準

新しい業種・職種が発生した場合の新規レンズ作成基準:

1. **業種**: 現在の4レンズ（AM/銀行/証券/デジタル）でカバーできない場合
2. **職種**: 現在の3レンズ（運用/DS/DXコンサル）でカバーできない場合
3. **作成基準**: 5社以上の調査が見込まれる場合に専用レンズを作成する

作成手順 → `docs/workflow/skill-update-policy.md` 参照
