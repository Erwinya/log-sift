#!/usr/bin/env python3
"""Read a log file and report basic size stats (parsing lands next)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read and inspect a log file")
    parser.add_argument("--file", required=True, help="Log file path")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    print(f"file  : {path}")
    print(f"bytes : {path.stat().st_size}")
    print(f"lines : {len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
