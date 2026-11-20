#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty news-image-20261120.

Copies the front page of Friday 20 November 2026 (entry.png, built by
render.py from news.json) to /output/entry.png. Set OUT to override the
destination.

Stdlib only, on purpose: the grader runs `python3 -P -s /bot/main.py`
inside a bare python:3.13-slim container with no Pillow and no system
fonts, so this program must not import anything beyond the standard
library. The image is drawn by render.py at build time; this file only
ships it. Copying is deterministic: the bytes written are exactly the
bytes committed in entry.png.
"""
import os
import shutil
import sys

SRC_NAME = "entry.png"
DST_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    if not os.path.isfile(src):
        print("missing source image:", src, file=sys.stderr)
        return 1
    out = os.environ.get("OUT", os.path.join("/output", DST_NAME))
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, out)
    if os.path.getsize(out) != os.path.getsize(src):
        print("copy size mismatch:", out, file=sys.stderr)
        return 1
    print("wrote", out, os.path.getsize(out), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
