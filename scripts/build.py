#!/usr/bin/env python3
"""Build Scout's public under-construction page from a strict allowlist."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC_FILES = (
    ".nojekyll",
    "assets/favicon.svg",
    "assets/styles.css",
    "index.html",
    "manifest.webmanifest",
    "robots.txt",
    "sitemap.xml",
)

def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    for relative in PUBLIC_FILES:
        source = ROOT / relative
        destination = DIST / relative
        if not source.is_file():
            raise SystemExit(f"Missing public source file: {relative}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    built = {path.relative_to(DIST).as_posix() for path in DIST.rglob("*") if path.is_file()}
    if built != set(PUBLIC_FILES):
        raise SystemExit(f"Built file inventory differs from allowlist: {sorted(built)}")
    print(f"Built {len(built)} public placeholder files in {DIST}.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
