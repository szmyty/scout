# Public data contract

"data/jobs.json" is a reviewed snapshot, not a live API.

## Top level

| Field | Type | Meaning |
| --- | --- | --- |
| "schema_version" | string | Contract version |
| "generated_at" | ISO date | Snapshot date |
| "notice" | string | Freshness and interpretation warning |
| "jobs" | array | Approved public records |

## Job record

| Field | Type | Meaning |
| --- | --- | --- |
| "id" | slug | Stable record identity |
| "employer" | string | Public organization name |
| "title" | string | Public role title |
| "location" | string | Coarse public location |
| "country" | string | Country or public jurisdiction |
| "lane" | enum | Career lane used for filtering |
| "url" | URL or null | Public posting or source |
| "fit_score" | integer 0–100 | Internal prioritization score |
| "priority" | enum | A, B, C, skip, or hard_reject |
| "status" | enum | Public lifecycle state |
| "deadline" | ISO date or null | Captured application deadline |
| "verified_at" | ISO date or null | Last official-source check |
| "summary" | string | Public-safe role summary |
| "next_action" | string | Public-safe operational step |

Unknown facts remain null or explicit unknown text in the private source. Scout does not invent them.

Changes to this contract require synchronized validator, renderer, and documentation updates.
