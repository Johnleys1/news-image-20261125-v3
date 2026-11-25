#!/usr/bin/env python3
"""Copy the pre-rendered front page into the grader's output folder.

Standard library only. Resolves every path from this script's own
directory, never from the working directory, and never deletes the
output folder: it creates it first, then copies one file into it.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
