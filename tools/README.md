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

# 企業名を指定 → company-info/みずほフィナンシャルグループ/ に保存
python transcribe.py C:\録音\20260326_みずほ_1次面接.mp3 --company みずほフィナンシャルグループ

# 企業名を省略 → 起動時に一覧から選択できる
python transcribe.py C:\録音\20260326_みずほ_1次面接.mp3

# 精度重視 (重要な面接に)
python transcribe.py audio.mp3 --company みずほフィナンシャルグループ --model medium

# 就活以外の用途 → transcripts/others/ に保存
python transcribe.py C:\録音\seminar.mp3 --output ../transcripts/others
```

## 出力先

| 用途 | 保存先 |
|------|--------|
| 面接（企業指定あり） | `company-info/企業名/transcript_音声ファイル名.md` |
| 面接（企業指定なし） | 起動時に一覧から選択 |
| その他 | `transcripts/others/` |

### 出力例

`company-info/みずほフィナンシャルグループ/transcript_20260326_みずほ_1次面接.md`

```markdown
# 文字起こし: 20260326_みずほ_1次面接

- 元ファイル: `20260326_みずほ_1次面接.mp3`
- 処理日時: 2026-03-26 14:30
- モデル: small

---

**[00:00 → 00:05]**
本日はよろしくお願いいたします。

**[00:05 → 00:12]**
...
```

## モデルの選び方

| モデル | 速度 | 精度 | 用途 |
|--------|------|------|------|
| tiny   | 最速 | 低   | テスト用 |
| small  | 速い | 中   | **日常利用推奨** |
| medium | 普通 | 高   | 重要な面接 |
| large-v2 | 遅い | 最高 | 最重要場面 |

## GitHubへのアップ

```powershell
git add company-info/
git commit -m "transcript: 20260326 みずほFG 1次面接"
git push
```
