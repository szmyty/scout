#!/usr/bin/env python3
"""Validate Scout's aggregate public contract and publication boundary."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-summary.json"
HTML_PATH = ROOT / "index.html"

TOP_LEVEL_FIELDS = {
    "schema_version",
    "generated_at",
    "notice",
    "focus_areas",
    "publication_model",
}
FOCUS_AREA_FIELDS = {"id", "label", "position", "summary"}
PUBLICATION_FIELDS = {"public", "private"}
POSITIONS = {"primary", "secondary", "targeted"}
FORBIDDEN_PUBLIC_KEYS = {
    "application_state",
    "deadline",
    "employer",
    "fit_score",
    "job_id",
    "jobs",
    "location",
    "next_action",
    "notes",
    "packet_path",
    "priority",
    "score",
    "status",
    "title",
    "url",
    "verified_at",
}
REQUIRED_SITE_FILES = {
    ".nojekyll",
    "assets/favicon.svg",
    "assets/styles.css",
    "data/public-summary.json",
    "index.html",
    "manifest.webmanifest",
    "robots.txt",
    "sitemap.xml",
}
FORBIDDEN_SITE_FILES = {"assets/app.js", "data/jobs.json"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?:\+\d[\d ()-]{7,}\d)")
URL_RE = re.compile(r"https?://", re.I)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: {exc}") from exc


def valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def find_forbidden_keys(value: object, path: str = "root") -> list[str]:
    """Return paths for fields that would expose live application operations."""

    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.lower() in FORBIDDEN_PUBLIC_KEYS:
                errors.append(f"{child_path}: forbidden public field")
            errors.extend(find_forbidden_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(find_forbidden_keys(child, f"{path}[{index}]"))
    return errors


def validate_data(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["data/public-summary.json: top level must be an object"]

    if set(payload) != TOP_LEVEL_FIELDS:
        errors.append(
            "data/public-summary.json: top-level fields differ from the public allowlist"
        )
    if payload.get("schema_version") != "2.0.0":
        errors.append("data/public-summary.json: schema_version must be 2.0.0")
    if not valid_date(payload.get("generated_at")):
        errors.append("data/public-summary.json: generated_at must be an ISO date")
    if not isinstance(payload.get("notice"), str) or not payload["notice"].strip():
        errors.append("data/public-summary.json: notice must be a non-empty string")

    focus_areas = payload.get("focus_areas")
    if not isinstance(focus_areas, list) or not focus_areas:
        errors.append("data/public-summary.json: focus_areas must be a non-empty array")
    else:
        seen: set[str] = set()
        for index, area in enumerate(focus_areas):
            prefix = f"data/public-summary.json focus_areas[{index}]"
            if not isinstance(area, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            if set(area) != FOCUS_AREA_FIELDS:
                errors.append(f"{prefix}: fields differ from the focus-area allowlist")

            area_id = area.get("id")
            if not isinstance(area_id, str) or not SLUG_RE.fullmatch(area_id):
                errors.append(f"{prefix}: id must be a lowercase slug")
            elif area_id in seen:
                errors.append(f"{prefix}: duplicate id {area_id}")
            else:
                seen.add(area_id)

            for field in ("label", "summary"):
                if not isinstance(area.get(field), str) or not area[field].strip():
                    errors.append(f"{prefix}: {field} must be a non-empty string")
            if area.get("position") not in POSITIONS:
                errors.append(f"{prefix}: unsupported position {area.get('position')!r}")

    publication_model = payload.get("publication_model")
    if not isinstance(publication_model, dict):
        errors.append("data/public-summary.json: publication_model must be an object")
    elif set(publication_model) != PUBLICATION_FIELDS:
        errors.append(
            "data/public-summary.json: publication_model fields differ from the allowlist"
        )
    else:
        for field in sorted(PUBLICATION_FIELDS):
            value = publication_model.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"data/public-summary.json: publication_model.{field} "
                    "must be a non-empty string"
                )

    errors.extend(find_forbidden_keys(payload))

    serialized = json.dumps(payload, ensure_ascii=False)
    forbidden_fragments = (
        "applications/",
        "archive/",
        "materials/",
        "references/",
        ".pdf",
        ".zip",
        "github.com/szmyty/career",
        "private_notes",
        "packet_path",
        "library_file",
    )
    for fragment in forbidden_fragments:
        if fragment.lower() in serialized.lower():
            errors.append(
                f"data/public-summary.json contains forbidden fragment: {fragment}"
            )
    if EMAIL_RE.search(serialized):
        errors.append("data/public-summary.json contains an email address")
    if PHONE_RE.search(serialized):
        errors.append("data/public-summary.json may contain a phone number")
    if URL_RE.search(serialized):
        errors.append("data/public-summary.json must not contain direct URLs")
    return errors


def validate_site_source() -> list[str]:
    errors: list[str] = []
    for relative in sorted(REQUIRED_SITE_FILES):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required site file: {relative}")
    for relative in sorted(FORBIDDEN_SITE_FILES):
        if (ROOT / relative).exists():
            errors.append(f"forbidden live-tracker file remains: {relative}")

    data_files = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "data").rglob("*")
        if path.is_file()
    }
    if data_files != {"data/public-summary.json"}:
        errors.append(
            "data directory differs from the single-file public allowlist: "
            f"{sorted(data_files)}"
        )

    try:
        html = HTML_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        return errors + [f"index.html: {exc}"]

    required_html = (
        "<title>Scout — Public Career Compass</title>",
        'id="direction"',
        'id="focus-title"',
        'id="boundary-title"',
        'href="assets/styles.css"',
        "A public map, not a live application tracker.",
        "Live application operations remain private.",
    )
    for fragment in required_html:
        if fragment not in html:
            errors.append(f"index.html missing required fragment: {fragment}")

    forbidden_html = (
        'id="job-card-template"',
        'id="owner-dialog"',
        'src="assets/app.js"',
        "Private repository URL",
    )
    for fragment in forbidden_html:
        if fragment in html:
            errors.append(f"index.html contains retired live-tracker fragment: {fragment}")

    if "http://" in html and "http://localhost" not in html:
        errors.append("index.html contains a non-local insecure HTTP URL")
    return errors


def main() -> int:
    try:
        payload = load_json(DATA_PATH)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors = validate_data(payload)
    errors.extend(validate_site_source())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    focus_count = len(payload["focus_areas"])
    print(f"Validated {focus_count} aggregate focus areas and the public boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
