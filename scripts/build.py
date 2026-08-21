#!/usr/bin/env python3
"""Build Scout by copying a strict public allowlist into dist."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC_FILES = (
    ".nojekyll",
    "assets/favicon.svg",
    "assets/styles.css",
    "data/public-summary.json",
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

    built = {
        path.relative_to(DIST).as_posix()
        for path in DIST.rglob("*")
        if path.is_file()
    }
    expected = set(PUBLIC_FILES)
    if built != expected:
        raise SystemExit(
            "Built file inventory differs from allowlist: "
            f"missing={sorted(expected - built)}, extra={sorted(built - expected)}"
        )

    if any(path.is_symlink() for path in DIST.rglob("*")):
        raise SystemExit("The public artifact must not contain symbolic links.")

    print(f"Built {len(built)} allowlisted public files in {DIST}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
