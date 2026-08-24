#!/usr/bin/env python3
"""Validate Scout's temporary public placeholder boundary."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    ".nojekyll",
    "assets/favicon.svg",
    "assets/styles.css",
    "index.html",
    "manifest.webmanifest",
    "robots.txt",
    "sitemap.xml",
}
FORBIDDEN = {"assets/app.js", "data/jobs.json"}
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?:\+\d[\d ()-]{7,}\d)")

def main() -> int:
    errors: list[str] = []
    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required public file: {relative}")
    for relative in sorted(FORBIDDEN):
        if (ROOT / relative).exists():
            errors.append(f"forbidden operational file remains: {relative}")

    for relative in sorted(REQUIRED):
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if EMAIL_RE.search(text):
            errors.append(f"public file contains an email address: {relative}")
        if PHONE_RE.search(text):
            errors.append(f"public file may contain a phone number: {relative}")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for fragment in ("Under construction.", "noindex, nofollow, noarchive"):
        if fragment not in html:
            errors.append(f"index.html missing required text: {fragment}")
    if "application queue" in html.lower() and "former live application queue" not in html.lower():
        errors.append("index.html must not present an application queue")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Validated Scout's public under-construction boundary.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
