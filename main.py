#!/usr/bin/env python3
"""Write one line of honest, funny error copy to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only. Deterministic: the same line is written on every run.
"""

import os
import sys

LINE = (
    "Your disk is full, so your file has nowhere to go - "
    "delete something you love less, then save again."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    text = LINE
    if not text or not text.strip():
        raise SystemExit("error: line is empty")
    if len(text) > 200:
        raise SystemExit("error: line exceeds 200 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("error: line is not a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise SystemExit("error: line contains control characters")

    data = (text + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Post-write byte-level re-read verification.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("error: post-write verification failed")
    decoded = written.decode("utf-8")
    if decoded.count("\n") != 1 or not decoded.strip():
        raise SystemExit("error: output failed the single-line check")
    if len(decoded.rstrip("\n")) > 200:
        raise SystemExit("error: output exceeds 200 characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
