"""
transcribe.py - 音声ファイルを文字起こしするスクリプト (Windows対応)

## セットアップ (Windows PowerShell)
    pip install faster-whisper

## 使い方
    # 企業名を指定 → company-info/企業名/ に保存
    python transcribe.py audio.mp3 --company みずほフィナンシャルグループ

    # 出力先を直接指定 (就活以外の用途など)
    python transcribe.py audio.mp3 --output ../transcripts/others

    # モデルサイズ指定 (tiny/base/small/medium/large-v2)
    python transcribe.py audio.mp3 --company みずほフィナンシャルグループ --model medium

## ファイル命名規則 (音声ファイル名に従う)
    YYYYMMDD_企業名_種別.mp3  →  transcript_YYYYMMDD_企業名_種別.md
    例: 20260326_みずほ_1次面接.mp3  →  transcript_20260326_みずほ_1次面接.md
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# tools/ からの相対パス
COMPANY_INFO_DIR = Path(__file__).parent.parent / "company-info"
TRANSCRIPTS_DIR = Path(__file__).parent.parent / "transcripts"


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

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"transcript_{audio_path.stem}.md"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# 文字起こし: {audio_path.stem}\n\n")
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


def resolve_output_dir(company: str | None, output: str | None) -> Path:
    if company:
        company_dir = COMPANY_INFO_DIR / company
        if not company_dir.exists():
            print(f"Warning: 企業フォルダが見つかりません: {company_dir}")
            print("  新規作成します。")
        return company_dir
    if output:
        return Path(output)
    # どちらも未指定の場合は一覧を表示して選択
    companies = sorted([d.name for d in COMPANY_INFO_DIR.iterdir() if d.is_dir()])
    print("\n企業フォルダ一覧:")
    for i, name in enumerate(companies, 1):
        print(f"  {i:2d}. {name}")
    print()
    choice = input("番号または企業名を入力 (Enterでスキップ → transcripts/others/): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(companies):
        return COMPANY_INFO_DIR / companies[int(choice) - 1]
    if choice:
        return COMPANY_INFO_DIR / choice
    return TRANSCRIPTS_DIR / "others"


def main():
    parser = argparse.ArgumentParser(description="音声ファイルを文字起こし")
    parser.add_argument("audio", help="音声ファイルのパス")
    parser.add_argument(
        "--company", "-c",
        help="企業名 (company-info/企業名/ に保存)"
    )
    parser.add_argument(
        "--output", "-o",
        help="出力先ディレクトリを直接指定 (--company より優先度低)"
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

    output_dir = resolve_output_dir(args.company, args.output)
    transcribe(audio_path, output_dir, args.model)


if __name__ == "__main__":
    main()
