"""
transcribe.py - 音声ファイルを文字起こしするスクリプト (Windows対応)

## セットアップ (Windows PowerShell)
    pip install faster-whisper

## 使い方
    # 単一ファイルの文字起こし
    python transcribe.py audio.mp3

    # 出力先ディレクトリを指定
    python transcribe.py audio.mp3 --output ../transcripts/interviews

    # モデルサイズ指定 (tiny/base/small/medium/large-v2)
    python transcribe.py audio.mp3 --model medium

## ファイル命名規則
    YYYYMMDD_企業名_種別.md
    例: 20260326_みずほFG_1次面接.md
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def transcribe(audio_path: Path, output_dir: Path, model_size: str) -> Path:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Error: faster-whisper がインストールされていません。")
        print("  pip install faster-whisper")
        sys.exit(1)

    print(f"モデル読み込み中: {model_size}")
    model = WhisperModel(model_size, device="auto", compute_type="auto")

    print(f"文字起こし開始: {audio_path.name}")
    segments, info = model.transcribe(str(audio_path), language="ja")

    print(f"検出言語: {info.language} (確度: {info.language_probability:.2f})")

    # Markdownに整形
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    out_file = output_dir / f"{stem}.md"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# 文字起こし: {stem}\n\n")
        f.write(f"- 元ファイル: `{audio_path.name}`\n")
        f.write(f"- 処理日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- モデル: {model_size}\n\n")
        f.write("---\n\n")

        for segment in segments:
            start = _fmt_time(segment.start)
            end = _fmt_time(segment.end)
            f.write(f"**[{start} → {end}]**\n{segment.text.strip()}\n\n")

    print(f"完了: {out_file}")
    return out_file


def _fmt_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="音声ファイルを文字起こし")
    parser.add_argument("audio", help="音声ファイルのパス")
    parser.add_argument(
        "--output", "-o",
        default="../transcripts/interviews",
        help="出力先ディレクトリ (デフォルト: ../transcripts/interviews)"
    )
    parser.add_argument(
        "--model", "-m",
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v2"],
        help="Whisperモデルサイズ (デフォルト: small)"
    )
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: ファイルが見つかりません: {audio_path}")
        sys.exit(1)

    output_dir = Path(args.output)
    transcribe(audio_path, output_dir, args.model)


if __name__ == "__main__":
    main()
