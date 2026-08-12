#!/usr/bin/env python3
"""Reject invisible Unicode characters in tracked text files."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


HIDDEN_UNICODE = re.compile(
    "[\u00a0\u00ad\u1680\u2000-\u200c\u200e\u200f"
    "\u2028-\u202f\u205f\u3000\ufeff]"
)


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [Path(path) for path in result.stdout.decode().split("\0") if path]


def main() -> int:
    findings: list[str] = []

    for path in tracked_files():
        if not path.is_file():
            continue

        data = path.read_bytes()
        if b"\0" in data:
            continue

        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
            for match in HIDDEN_UNICODE.finditer(line):
                findings.append(
                    f"{path}:{line_number}:{match.start() + 1}: "
                    f"U+{ord(match.group()):04X}"
                )

    if findings:
        print("Hidden Unicode characters found:")
        print("\n".join(findings))
        return 1

    print("No hidden Unicode characters found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
