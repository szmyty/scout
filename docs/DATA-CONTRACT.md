# Aggregate public data contract

"data/public-summary.json" is a reviewed projection, not a live API or
application queue.

## Top level

| Field | Type | Meaning |
| --- | --- | --- |
| "schema_version" | string | Contract version; currently "2.0.0" |
| "generated_at" | ISO date | Date the public projection was reviewed |
| "notice" | string | Publication and freshness boundary |
| "focus_areas" | array | Broad owner-approved career lanes |
| "publication_model" | object | Explicit public/private split |

## Focus area

| Field | Type | Meaning |
| --- | --- | --- |
| "id" | slug | Stable public focus identifier |
| "label" | string | Human-readable career lane |
| "position" | enum | "primary", "secondary", or "targeted" |
| "summary" | string | Broad description with no live target data |

## Publication model

The object contains exactly "public" and "private" strings describing the
boundary. It contains no direct URLs or operational records.

## Rejected information

The validator rejects employer, role title, location, URL, fit score, priority,
status, deadline, verification date, next action, contact details, private paths,
and additional files beneath "data/".

Changes to this contract require synchronized validator, regression-test,
documentation, and static-copy updates.
