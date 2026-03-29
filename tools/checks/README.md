# tools/checks/

ES・企業調査の品質チェックスクリプト群。

## スクリプト一覧

| ファイル | 目的 | 対象 |
|---------|------|------|
| `es_checker.py` | ESファイルの品質チェック | `移行後ES/*.md`, `ES/submitted/*.md` |
| `research_checker.py` | 企業調査の網羅性チェック | `company-info/<企業名>/research_brief.md` |

## 実行例

```bash
# ES単体チェック
cd /Users/ishidatomonori/Desktop/knowledge
python tools/checks/es_checker.py 移行後ES/三菱UFJ銀行.md

# 全企業調査チェック
python tools/checks/research_checker.py --all

# 特定企業の調査チェック
python tools/checks/research_checker.py かんぽ生命
```

## 出力フォーマット

- `❌ ERROR`: 提出前に必ず修正が必要
- `⚠️ WARNING`: 確認・修正を推奨
- `ℹ️ INFO`: 参考情報

## 注意事項
- Python 3.8以上が必要
- 外部ライブラリ不要（標準ライブラリのみ使用）
- 機械的チェックのみ実施。深い内容評価は subagent を使うこと
