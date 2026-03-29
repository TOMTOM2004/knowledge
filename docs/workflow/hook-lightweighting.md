# hook 軽量化ガイド

Claude を使わなくて済む判定は script に寄せる。agent hook の依存を最小化する。

---

## 判断基準

| 判定方法 | 担当 |
|---------|------|
| 文字列マッチ（禁止表現・表記ゆれ） | script |
| 数値比較（文字数・割合・密度） | script |
| 見出し存在確認（必須セクションの有無） | script |
| 意味の理解が必要な判定（設問適合・論旨整合） | agent |

---

## script に寄せた処理一覧

以下は `tools/checks/es_checker.py` または `tools/checks/research_checker.py` で対応:

### ES チェック（es_checker.py）

| チェック | 判定方法 | 閾値 |
|---------|---------|------|
| 文字数（超過・不足） | 設問ごとの文字数カウント | 設問別の上限・下限 |
| 禁止表現 | 正規表現マッチ | 「思います」「御社」等のリスト |
| 企業名表記ゆれ | 正規化後の一致確認 | company-info の名前と照合 |
| 設問未回答 | 見出し後の本文有無 | 空行のみ or 50字未満 |
| 重複表現検出 | 同一フレーズ（4字以上）の出現回数 | 3回以上で警告 |
| 技術用語過多 | 禁止語リストとのマッチ数 / 全体文字数 | 密度 5% 以上で警告 |
| 抽象語過多 | 抽象語リストとのマッチ数 | 10語以上で警告 |
| 数字不足 | 数値（金額・割合・期間等）の出現回数 | 設問あたり 0個で警告 |

### リサーチチェック（research_checker.py）

| チェック | 判定方法 |
|---------|---------|
| 必須セクション存在確認 | 見出し（## 企業固有性 等）の有無 |
| 企業固有性の件数 | 箇条書きアイテム数（3件未満で警告） |
| 志望動機論点の件数 | 箇条書きアイテム数（3件未満で警告） |
| 競合比較の存在確認 | 「vs」または「比較」を含む行の有無 |
| 面接深掘り論点の存在確認 | 該当セクションの空白確認 |
| 危険ポイントの存在確認 | 該当セクションの空白確認 |

---

## agent に残すべき判定

以下は意味理解が必要なので agent に任せる:

| 判定 | 担当 agent |
|-----|----------|
| 設問に正面から答えているか | question-fit-reviewer |
| 文系面接官に伝わるか | readability-reviewer |
| 企業固有性があるか | company-fit-reviewer |
| 職種適合しているか | role-fit-reviewer |
| 設問間の論旨重複 | consistency-overlap-reviewer |
| 面接で突っ込まれる弱点 | skeptical-interviewer |

---

## hook の現状と方針

### 現状
- `tools/checks/es_checker.py` — 実装済み、手動実行
- `tools/checks/research_checker.py` — 実装済み、手動実行
- `.claude/hooks/` — README のみ、active hook なし

### 方針
- 自動 hook よりも「コマンドとして実行しやすい形」を優先する
- ES保存後の自動 hook は将来対応（現状は手動が安全）
- hook を設定する場合は `docs/workflow/hook-setup.md` を参照

---

## 推奨コマンド（手動実行）

```bash
# ESファイルをチェック（提出前に必ず実行）
python tools/checks/es_checker.py 移行後ES/<企業名>.md

# 企業調査の品質確認
python tools/checks/research_checker.py <企業名>

# 全ES一括チェック
python tools/checks/es_checker.py --all
```

---

## script 追加時のルール

- `tools/checks/` に配置する
- 引数は `<ファイルパス>` または `<企業名>` に統一
- exit code: 0=OK、1=WARNING、2=ERROR
- JSON または人間可読テキストで出力する
- 閾値はファイル先頭の定数で管理する
