#!/usr/bin/env python3
"""Validate Scout's static source, public data contract, and privacy boundary."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "jobs.json"
HTML_PATH = ROOT / "index.html"

TOP_LEVEL_FIELDS = {"schema_version", "generated_at", "notice", "jobs"}
JOB_FIELDS = {
    "id",
    "employer",
    "title",
    "location",
    "country",
    "lane",
    "url",
    "fit_score",
    "priority",
    "status",
    "submitted_at",
    "deadline",
    "verified_at",
    "summary",
    "next_action",
}
STATUSES = {
    "applying",
    "closed",
    "discovered",
    "ineligible",
    "interviewing",
    "needs_reverification",
    "offer",
    "preparing",
    "queued",
    "ready",
    "rejected",
    "submitted",
    "verified",
    "watch",
    "withdrawn",
}
PRIORITIES = {"A", "B", "C", "skip", "hard_reject"}
LANES = {
    "applied_ai",
    "developer_productivity",
    "platform",
    "research_data",
    "research_software",
    "scientific_software",
    "visualization_geospatial",
    "watch",
}
REQUIRED_SITE_FILES = {
    ".nojekyll",
    "assets/app.js",
    "assets/favicon.svg",
    "assets/styles.css",
    "data/jobs.json",
    "index.html",
    "manifest.webmanifest",
    "robots.txt",
    "sitemap.xml",
}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?:\+\d[\d ()-]{7,}\d)")


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: {exc}") from exc


def valid_date(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate_data(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["data/jobs.json: top level must be an object"]
    if set(payload) != TOP_LEVEL_FIELDS:
        errors.append(
            "data/jobs.json: top-level fields differ from the public allowlist"
        )
    if payload.get("schema_version") != "1.1.0":
        errors.append("data/jobs.json: schema_version must be 1.1.0")
    if not valid_date(payload.get("generated_at")):
        errors.append("data/jobs.json: generated_at must be an ISO date")
    if not isinstance(payload.get("notice"), str) or not payload["notice"].strip():
        errors.append("data/jobs.json: notice must be a non-empty string")

    jobs = payload.get("jobs")
    if not isinstance(jobs, list) or not jobs:
        return errors + ["data/jobs.json: jobs must be a non-empty array"]

    seen: set[str] = set()
    for index, job in enumerate(jobs):
        prefix = f"data/jobs.json jobs[{index}]"
        if not isinstance(job, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if set(job) != JOB_FIELDS:
            errors.append(
                f"{prefix}: fields differ from allowlist; "
                f"extra={sorted(set(job) - JOB_FIELDS)}, "
                f"missing={sorted(JOB_FIELDS - set(job))}"
            )

        job_id = job.get("id")
        if not isinstance(job_id, str) or not SLUG_RE.fullmatch(job_id):
            errors.append(f"{prefix}: id must be a lowercase slug")
        elif job_id in seen:
            errors.append(f"{prefix}: duplicate id {job_id}")
        else:
            seen.add(job_id)

        for field in (
            "employer",
            "title",
            "location",
            "country",
            "summary",
            "next_action",
        ):
            if not isinstance(job.get(field), str):
                errors.append(f"{prefix}: {field} must be a string")

        if job.get("status") not in STATUSES:
            errors.append(f"{prefix}: unsupported status {job.get('status')!r}")
        if job.get("status") == "submitted" and job.get("submitted_at") is None:
            errors.append(f"{prefix}: submitted jobs require submitted_at")
        if job.get("status") != "submitted" and job.get("submitted_at") is not None:
            errors.append(f"{prefix}: only submitted jobs may include submitted_at")
        if job.get("priority") not in PRIORITIES:
            errors.append(f"{prefix}: unsupported priority {job.get('priority')!r}")
        if job.get("lane") not in LANES:
            errors.append(f"{prefix}: unsupported lane {job.get('lane')!r}")

        score = job.get("fit_score")
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
            errors.append(f"{prefix}: fit_score must be an integer from 0 to 100")

        for field in ("submitted_at", "deadline", "verified_at"):
            if not valid_date(job.get(field)):
                errors.append(f"{prefix}: {field} must be an ISO date or null")

        url = job.get("url")
        if url is not None:
            if not isinstance(url, str) or urlparse(url).scheme not in {"http", "https"}:
                errors.append(f"{prefix}: url must be an http(s) URL or null")

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
            errors.append(f"data/jobs.json contains forbidden fragment: {fragment}")
    if EMAIL_RE.search(serialized):
        errors.append("data/jobs.json contains an email address")
    if PHONE_RE.search(serialized):
        errors.append("data/jobs.json may contain an international phone number")
    return errors


def validate_site_source() -> list[str]:
    errors: list[str] = []
    for relative in sorted(REQUIRED_SITE_FILES):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required site file: {relative}")

    try:
        html = HTML_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        return errors + [f"index.html: {exc}"]

    required_html = (
        "<title>Scout — Research Career Queue</title>",
        'id="job-grid"',
        'id="submitted-section"',
        'id="submitted-details"',
        'id="submitted-job-grid"',
        'id="filters"',
        'id="owner-dialog"',
        'id="job-card-template"',
        'href="assets/styles.css"',
        'src="assets/app.js"',
    )
    for fragment in required_html:
        if fragment not in html:
            errors.append(f"index.html missing required fragment: {fragment}")

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

    print(f"Validated {len(payload['jobs'])} public jobs and the static site boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
