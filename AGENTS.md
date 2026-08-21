# AGENTS.md — Scout Continuity Guide

Read this file completely before editing the repository. Scout is a public
GitHub Pages application, so every committed byte and built asset must be
treated as internet-visible.

## Mission

Scout is Alan Szmyt's privacy-preserving public career compass. It communicates
broad engineering direction without exposing the live application system.

The approved public positioning is:

1. Platform and developer experience — primary.
2. Research and AI-assisted systems — secondary.
3. Mobile and geospatial systems — targeted.

Do not turn Scout into a job board, live application queue, salary leaderboard,
hustle dashboard, social-performance feed, or public decision system.

## Source-of-truth boundary

Scout is not canonical. A separate private career system owns employer and role
targets, application state, deadlines, scores, next actions, source documents,
submission evidence, references, correspondence, and private decision context.

The only permitted flow is:

1. Career research and operations happen privately.
2. A broad, deliberately aggregate summary is reviewed.
3. The approved summary replaces "data/public-summary.json".
4. Scout validates and publishes the static projection.

Never fetch a private repository at build time or runtime. Never add a private
repository URL, raw-file URL, API token, OAuth secret, signed URL, contact
detail, packet path, correspondence, screenshot, resume, CV, cover letter,
reference identity, employer target, live status, deadline, score, or next
action to this repository.

## Public data contract

"data/public-summary.json" is the only file permitted beneath "data/". It has:

- "schema_version"
- "generated_at"
- "notice"
- "focus_areas"
- "publication_model"

Each focus area contains exactly:

- "id"
- "label"
- "position"
- "summary"

Allowed positions are "primary", "secondary", and "targeted". The publication
model contains only "public" and "private" boundary descriptions.

The validator rejects operational fields including employer, title, location,
URL, fit score, priority, status, deadline, verification date, and next action.
It also rejects direct URLs, contact details, document paths, additional data
files, and the retired live-tracker assets.

## Privacy rules

Run all three commands before every commit:

```console
python3 scripts/validate.py
python3 scripts/test_public_boundary.py
python3 scripts/build.py
```

Inspect the complete diff manually. Automated checks are guardrails, not
permission to publish.

Historical public data is a separate remediation concern. Do not rewrite
history, change repository visibility, disable Pages, or purge caches without
explicit owner authorization and a recovery plan.

## Experience and interaction design

The visual direction is a quiet nocturnal field notebook: deep ink, soft
indigo, mint and amber signals, restrained glow, precise typography, and
generous breathing room. It should feel focused rather than gamified.

The first viewport must answer:

- What is Scout?
- What career direction is public?
- What information intentionally stays private?
- Where can a visitor learn about Alan's work?

Accessibility requirements:

- Semantic landmarks and headings.
- Visible skip link and focus states.
- Native links and controls.
- Keyboard-complete interaction.
- Sufficient color contrast.
- Reduced-motion support.
- No color-only meaning.

Responsive behavior must work from narrow phones through wide desktops. Avoid
horizontal scrolling and undersized touch targets.

## Technical architecture

Scout deliberately has no production dependencies and no client framework.

- "index.html" contains the complete semantic shell.
- "assets/styles.css" owns the design and responsive behavior.
- "data/public-summary.json" is the aggregate public contract.
- "scripts/validate.py" checks source, data, and privacy invariants.
- "scripts/test_public_boundary.py" regression-tests prohibited fields.
- "scripts/build.py" copies a strict allowlist to "dist/".
- GitHub Actions validates pull requests and publishes "dist/" from "master".

Keep the GitHub Pages project path in mind. URLs must work under "/scout/" and
in a local "dist/" server.

Do not introduce npm, a bundler, analytics, trackers, cookies, external fonts,
remote images, runtime data fetching, or a framework without a concrete need
and explicit review.

## Content rules

Use direct, grounded language. Public content may describe career lanes,
engineering interests, evaluation principles, and a delayed aggregate update.

Do not imply a vacancy is active, an application is underway, a particular
employer is targeted, or a score predicts success. Do not publish counts small
enough to reconstruct live activity.

## Update workflow

1. Produce a deliberately aggregate summary outside this repository.
2. Review the summary against "docs/PRIVACY.md".
3. Replace "data/public-summary.json" without adding fields or files.
4. Synchronize visible static copy when the approved positioning changes.
5. Run validation, boundary tests, and the deterministic build.
6. Inspect every changed line for private material.
7. Open a focused feature branch and draft pull request.
8. Let Alan merge unless he explicitly authorizes otherwise.

## GitHub workflow

The default branch is "master".

- ".github/workflows/validate.yml" runs on pull requests and pushes.
- ".github/workflows/pages.yml" deploys only after a push to "master" or a
  manual dispatch.

Never merge a pull request, enable or disable Pages, change repository
visibility, rewrite history, or publish additional data without explicit
authorization.

## New-chat bootstrap

When a new chat takes over, the user can say: “Read AGENTS.md in szmyty/scout
and continue.”

The agent should:

1. Read this file completely.
2. Read "README.md", "docs/PRIVACY.md", "docs/DATA-CONTRACT.md",
   "docs/DESIGN.md", and "docs/WORKFLOW.md".
3. Inspect "data/public-summary.json".
4. Run validation, boundary tests, and build before editing.
5. Check the current branch, open pull requests, Pages workflow, and working
   tree.
6. Access private career data only when Alan explicitly supplies it for a
   private task; never copy it into Scout.
7. Keep one bounded pull request at a time and stop for review.

## Quality bar

A good change makes Scout clearer, safer, and more truthful. It preserves the
one-way aggregate publication boundary, works without hidden services, remains
accessible on keyboard and mobile, passes validation, and leaves the next agent
with less reconstruction work.
