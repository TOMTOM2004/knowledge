# hooks README

このディレクトリは Claude Code の hook 設定を管理します。

## hook とは
Claude Code が特定のアクション（ファイル保存・ツール実行等）の前後に自動実行するスクリプトです。
機械的なチェックに限定し、深い意味判断は subagent に任せます。

## 現在のhook設定

hooks は `.claude/settings.json` または `.claude/settings.local.json` で設定します。
`update-config` スキルを使って追加・変更できます。

### 設定例（settings.jsonへの追記）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python /Users/ishidatomonori/Desktop/knowledge/tools/checks/es_checker.py \"$CLAUDE_TOOL_RESPONSE_FILE_PATH\"",
            "description": "ESファイル保存後の品質チェック"
          }
        ]
      }
    ]
  }
}
```

> 注意: hook の詳細設定は `update-config` スキルで行ってください。

## 利用可能なチェックスクリプト

| スクリプト | 対象 | 実行コマンド |
|-----------|------|------------|
| `tools/checks/es_checker.py` | ES Markdownファイル | `python tools/checks/es_checker.py <filepath>` |
| `tools/checks/research_checker.py` | 企業調査 research_brief.md | `python tools/checks/research_checker.py <企業名>` |

## 手動実行

```bash
# ES単体チェック
python tools/checks/es_checker.py 移行後ES/三菱UFJ銀行.md

# 全企業の調査品質チェック
python tools/checks/research_checker.py --all

# 特定企業の調査チェック
python tools/checks/research_checker.py 三菱UFJ銀行
```

## チェック項目

### ESチェック (es_checker.py)
1. 禁止表現チェック（御社・様々な・積極的に等）
2. 企業名・敬称の表記ゆれチェック（貴社/貴行/貴グループ混在）
3. 設問未回答警告（[TODO]・「記入予定」等の検出）
4. 同一ファイル内の重複表現検出
5. 技術用語過多警告
6. 抽象語過多警告
7. 数字不足警告

### 企業調査チェック (research_checker.py)
1. research_brief 9軸カバレッジチェック
2. 競合比較セクション有無チェック
3. 出典未記載警告
4. IR・中計・採用情報の主要論点欠落警告
5. 職種メモ未記入警告
6. 情報の鮮度チェック（古い年度の言及）

## 注意事項
- hook は機械的チェックに限定する
- 誤検知しうるものは WARNING として扱う（ERROR は確実な問題のみ）
- 深い意味判断（企業適合性・設問適合性等）は subagent に任せる
