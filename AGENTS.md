# AGENTS.md — Scout

Scout is public and currently under construction. It must not contain job-application operations.

## Boundary

The private `szmyty/career` repository is the sole source of truth for Alan’s application queue, documents, materials, submissions, follow-up, and outcomes. Do not link to it, fetch it, or expose its contents here.

Scout currently publishes only a static holding page. Do not add:

- employer or role targets;
- application statuses, dates, deadlines, scores, priorities, or next actions;
- private notes, correspondence, materials, contacts, or workspace paths;
- client-side authentication, tokens, a database, analytics, or a private-repository URL.

A future public Scout product must have an explicit scope, threat model, and reviewed public-only data contract before implementation.

## Technical rules

- Keep the site dependency-free and static.
- `scripts/validate.py` and `scripts/build.py` enforce the placeholder artifact allowlist.
- GitHub Pages deploys only after a merge to `master`.
- Use a focused branch and pull request. Never merge or publish new data without Alan’s explicit authorization.

## New-chat bootstrap

Read this file, then `README.md` and `docs/PRIVACY.md`. Treat `szmyty/career` as private and off-limits unless Alan explicitly asks to work there.
