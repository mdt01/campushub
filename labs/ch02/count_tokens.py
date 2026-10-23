"""Count tokens in a piece of text or a file.

Usage:
    python -m labs.ch02.count_tokens "Register student 21CE001 for the Hackathon"
    python -m labs.ch02.count_tokens --file app/routers/events.py
"""
import argparse
from pathlib import Path

import tiktoken


def count_tokens(text: str, encoding: str = "o200k_base") -> int:
    """Return the number of tokens in text for the given tokenizer."""
    return len(tiktoken.get_encoding(encoding).encode(text))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", help="text to measure")
    parser.add_argument("--file", help="measure a whole file instead")
    args = parser.parse_args()
    text = Path(args.file).read_text(encoding="utf-8") if args.file else (args.text or "")
    n = count_tokens(text)
    print(f"{n} tokens  |  {len(text)} characters  |  {len(text) / max(n, 1):.1f} characters per token")


if __name__ == "__main__":
    main()
