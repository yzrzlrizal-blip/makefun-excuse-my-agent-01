#!/usr/bin/env python3
"""The Excuse My Agent Gave Me.

Writes one original excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Pure Python standard library, deterministic:
the same line on every run.
"""

import os
import sys
import tempfile

MAX_CHARS = 200
ENTRY_FILENAME = "entry.txt"

EXCUSE = (
    "I missed the deadline because I hallucinated a second, later "
    "deadline, met that one perfectly, and I would like some credit for it."
)


def main() -> int:
    line = EXCUSE
    if not line or not line.strip():
        print("error: entry is blank", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: entry is %d chars, over the %d limit" % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write can never leave a truncated
    # entry.txt behind, so the grader always reads the whole line or
    # nothing at all.
    target = os.path.join(out_dir, ENTRY_FILENAME)
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        os.replace(tmp_path, target)
    except OSError:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
