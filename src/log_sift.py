#!/usr/bin/env python3
"""Parse application / access logs for status codes, paths, levels, and errors."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

LINE_RE = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)?.*?"(?P<method>GET|POST|PUT|PATCH|DELETE)\s+(?P<path>\S+)[^"]*"\s+(?P<status>\d{3})'
    r"|(?P<status2>\d{3})\s+(?P<method2>GET|POST|PUT|PATCH|DELETE)\s+(?P<path2>\S+)"
    r"|(?P<level>ERROR|WARN|WARNING|INFO|DEBUG)\b.*?(?P<msg>.+)$",
    re.IGNORECASE,
)


def analyze(text: str) -> dict:
    statuses: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    levels: Counter[str] = Counter()
    errors: list[str] = []
    lines = 0

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        lines += 1
        m = LINE_RE.search(line)
        if not m:
            if re.search(r"\b(ERROR|Exception|Traceback)\b", line, re.I):
                levels["ERROR"] += 1
                errors.append(line[:200])
            continue
        status = m.group("status") or m.group("status2")
        method = m.group("method") or m.group("method2")
        path = m.group("path") or m.group("path2")
        level = m.group("level")
        if status:
            statuses[status] += 1
        if path:
            key = f"{(method or 'GET').upper()} {path}"
            paths[key] += 1
        if level:
            levels[level.upper().replace("WARNING", "WARN")] += 1
            if level.upper() in {"ERROR", "WARN", "WARNING"}:
                errors.append((m.group("msg") or line)[:200])

    return {
        "lines": lines,
        "status_counts": dict(statuses.most_common()),
        "top_paths": paths.most_common(10),
        "levels": dict(levels),
        "error_samples": errors[:10],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize status codes, paths, and errors in log files")
    parser.add_argument("--file", required=True, help="Log file path")
    parser.add_argument("--json", action="store_true", help="Emit report as JSON")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    report = analyze(path.read_text(encoding="utf-8", errors="replace"))
    if args.json:
        # top_paths as list of [path, count] for stable JSON
        payload = {
            "lines": report["lines"],
            "status_counts": report["status_counts"],
            "top_paths": [[p, n] for p, n in report["top_paths"]],
            "levels": report["levels"],
            "error_samples": report["error_samples"],
        }
        print(json.dumps(payload, indent=2))
        return 0

    print(f"file          : {path}")
    print(f"lines         : {report['lines']}")
    print(f"status_counts : {report['status_counts']}")
    print(f"levels        : {report['levels']}")
    print("top_paths:")
    if not report["top_paths"]:
        print("  (none matched)")
    else:
        for path_key, n in report["top_paths"]:
            print(f"  {n:5d}  {path_key}")
    if report["error_samples"]:
        print("error_samples:")
        for sample in report["error_samples"]:
            print(f"  - {sample}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
