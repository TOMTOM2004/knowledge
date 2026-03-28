# hook 設定ガイド

## hook とは

Claude Code が特定のアクション（ファイル書き込み等）の前後に自動実行するコマンドです。
機械的なチェックを自動化するために使います。

---

## 現在利用可能なチェックスクリプト

| スクリプト | 実行タイミング | 対象 |
|-----------|-------------|------|
| `tools/checks/es_checker.py` | ESファイル保存後 | `*.md` ファイル |
| `tools/checks/research_checker.py` | 企業調査ファイル保存後 | `research_brief.md` |

---

## 手動実行（すぐに使えます）

hook設定なしでも手動で実行できます:

```bash
# ESファイルをチェック
cd /Users/ishidatomonori/Desktop/knowledge
python tools/checks/es_checker.py 移行後ES/三菱UFJ銀行.md

# 全企業の調査をチェック
python tools/checks/research_checker.py --all

# 特定企業の調査をチェック
python tools/checks/research_checker.py かんぽ生命
```

---

## hook を自動設定する方法

### 方法1: update-config スキルを使う（推奨）

Claude Code に以下のように依頼します:

```
「ESファイルを保存したあとに自動でチェックが走るようhookを設定して」
```

または `/update-config` を実行して設定手順を確認してください。

### 方法2: 手動で settings.json に追記

`.claude/settings.local.json` に以下を追記:

```json
{
  "permissions": {
    "allow": ["Bash(python:*)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=\"${CLAUDE_TOOL_INPUT_FILE_PATH:-}\"; if [[ \"$FILE\" == *移行後ES*.md ]] || [[ \"$FILE\" == *ES/submitted*.md ]]; then python /Users/ishidatomonori/Desktop/knowledge/tools/checks/es_checker.py \"$FILE\"; fi",
            "description": "ES保存後の品質チェック"
          }
        ]
      }
    ]
  }
}
```

> **注意**: hook の環境変数名は Claude Code のバージョンによって異なる場合があります。
> `update-config` スキルで設定することを推奨します。

---

## チェック出力の見方

| マーク | 意味 | 対応 |
|-------|------|------|
| ERROR | 必ず修正が必要 | 提出前に修正する |
| WARNING | 修正を推奨 | 確認して判断する |
| INFO | 参考情報 | 必要に応じて対応 |

---

## 注意事項

- hook は機械的チェックに限定（深い内容評価はしない）
- 誤検知する場合はWARNINGとして扱う（ERRORにしない）
- チェックが遅すぎる場合はスクリプトを最適化する
