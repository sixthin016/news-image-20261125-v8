#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261125 competition.

The front page itself is drawn at build time by tools/generate.py
(Pillow + system fonts) and stored as assets/entry.png. This program
is deliberately tiny and uses only the standard library: it copies
that PNG into the output directory the grader provides.

Running it twice produces byte-identical output, because it copies a
fixed file and writes nothing else.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    if not os.path.isfile(src):
        print("missing assets/entry.png; run tools/generate.py first",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
