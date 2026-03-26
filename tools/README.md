# tools - 文字起こしツール

## 必要なもの (Windows)

- Python 3.9以上
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

```powershell
pip install faster-whisper
```

> GPU(CUDA)がある場合は自動的に使用されます。ない場合はCPUで動作します。

## 使い方

```powershell
cd tools

# 基本 (出力先: ../transcripts/interviews/)
python transcribe.py C:\録音\20260326_みずほ1次.mp3

# 出力先を others に変更
python transcribe.py C:\録音\seminar.mp3 --output ../transcripts/others

# 精度重視 (時間がかかる)
python transcribe.py audio.mp3 --model medium
```

## モデルの選び方

| モデル | 速度 | 精度 | 目安 |
|--------|------|------|------|
| tiny   | 最速 | 低   | テスト用 |
| small  | 速い | 中   | **日常利用推奨** |
| medium | 普通 | 高   | 重要な面接 |
| large-v2 | 遅い | 最高 | 最重要場面 |

## 出力ファイル

`transcripts/interviews/` または `transcripts/others/` に Markdown 形式で保存されます。

```markdown
# 文字起こし: 20260326_みずほ1次

- 元ファイル: `20260326_みずほ1次.mp3`
- 処理日時: 2026-03-26 14:30
- モデル: small

---

**[00:00 → 00:05]**
本日はよろしくお願いいたします。

**[00:05 → 00:12]**
...
```

## GitHubへのアップ

文字起こし完了後、このリポジトリにコミット・push すれば Mac側からも参照できます。

```powershell
git add transcripts/
git commit -m "transcript: 20260326 みずほFG 1次面接"
git push
```
