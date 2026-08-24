# AGENTS.md — Scout Continuity Guide

Read this file completely before editing the repository. Scout is a public GitHub Pages application, so every committed byte and every built asset must be treated as public.

## Mission

Scout is Alan Szmyt's calm, public-facing job-application queue for research-oriented software roles. It should reduce application friction and make the next useful action obvious without exposing private career materials or personal context.

The optimization order inherited from the private career process is:

1. Stability and a viable bridge into the next phase of life.
2. Sustainable work design and health.
3. Alignment with demonstrated research-software, systems, geospatial, visualization, developer-tooling, and applied-AI strengths.
4. Enough autonomy and energy for long-term independent work.
5. International mobility and durable optionality.

Do not turn the site into a salary leaderboard, hustle dashboard, social-performance feed, or generic job board.

## Source-of-truth boundary

Scout is not canonical. A separate private career vault owns detailed records, application packets, source documents, submission evidence, reference information, and private decision context.

The one-way flow is:

1. A job is researched and updated privately.
2. A deliberately reduced public record is reviewed.
3. The approved snapshot is copied to "data/jobs.json" here.
4. Scout validates and renders that static snapshot.

Never fetch the private repository at build time or runtime. Never add a private-repository URL, raw-file URL, API token, OAuth secret, signed URL, contact detail, packet path, correspondence, screenshot, resume, CV, cover letter, or reference identity to this repository.

## Owner mode

Owner mode is intentionally device-local:

- The owner manually enters a GitHub repository URL and branch.
- Values are stored only in browser local storage.
- No token is requested or stored.
- Scout constructs a normal GitHub directory link for the stable job ID.
- GitHub's existing signed-in session decides whether the visitor can open it.
- Clearing owner mode removes the local settings.

Do not hard-code Alan's private repository URL. Do not add direct packet downloads because the public snapshot intentionally contains no packet paths. A future authenticated backend would require a separate threat model and explicit user approval.

## Public data contract

"data/jobs.json" is a versioned snapshot with:

- "schema_version"
- "generated_at"
- "notice"
- "jobs"

Each public job must contain exactly:

- "id"
- "employer"
- "title"
- "location"
- "country"
- "lane"
- "url"
- "fit_score"
- "priority"
- "status"
- "submitted_at"
- "deadline"
- "verified_at"
- "summary"
- "next_action"

Allowed lifecycle states currently include "queued", "preparing", "needs_reverification", "submitted", and "watch". The UI must tolerate future states defined by the validator.

IDs are stable lowercase slugs. Submission, deadline, and verification dates use "YYYY-MM-DD". "submitted_at" is null until a submission is owner-confirmed; once public, it records only the date, never a time, confirmation artifact, or correspondence. A missing deadline is null, not a guessed rolling date.

The public export is intentionally limited to approved jobs. Do not infer that missing private jobs do not exist.

## Privacy rules

Run "python3 scripts/validate.py" before every commit.

The validator rejects:

- Unsupported fields.
- Email addresses and international phone-like values.
- PDF/ZIP/document paths.
- Private workspace paths or private-repository references.
- Duplicate IDs and malformed dates or URLs.
- Unknown statuses, priorities, or lanes.

Also inspect the complete diff manually. Automated checks are guardrails, not permission to publish.

## Experience and interaction design

The visual direction is a quiet nocturnal field notebook: deep ink, soft indigo, mint and amber signals, restrained glow, precise typography, and generous breathing room. It should feel focused rather than corporate or gamified.

The first viewport must answer:

- What is Scout?
- How current is this snapshot?
- What needs attention now?
- How many roles are active, submitted, or near deadline?

Core interactions:

- Free-text search.
- Status, priority, lane, and country filters.
- Recommendation, deadline, score, and employer sorting.
- Clear-all action.
- Copy job ID.
- Direct public posting link.
- Optional owner-mode private workspace link.

Accessibility requirements:

- Semantic landmarks and headings.
- Visible skip link and focus states.
- Native buttons, links, labels, select controls, and dialog behavior.
- Keyboard-complete interaction.
- Live result-count announcements.
- Sufficient color contrast.
- Reduced-motion support.
- No color-only status communication.

Responsive behavior must work from narrow phones through wide desktops. Avoid horizontal page scrolling and avoid shrinking controls below comfortable touch targets.

## Recommendation ordering

The default sort is operational, not purely numeric:

1. Work already being prepared or applied.
2. Queued roles with the nearest valid deadline.
3. Other queued roles.
4. Roles needing reverification.
5. Submitted roles.
6. Watch items.

Fit score breaks ties. Unknown deadlines sort after dated roles within a group.

Do not silently convert "needs_reverification" into "queued". Staleness is important information.

## Technical architecture

Scout deliberately has no production dependencies and no client framework.

- "index.html" contains the static semantic shell.
- "assets/app.js" fetches "data/jobs.json" relative to the document base and renders the queue.
- "assets/styles.css" owns the design system and responsive layout.
- "scripts/build.py" copies only a strict public allowlist to "dist/".
- "scripts/validate.py" checks source, data, and privacy invariants.
- GitHub Actions validates pull requests and publishes "dist/" from "master".

Keep the GitHub Pages project path in mind. All URLs must remain relative so the site works at "/scout/" and in a local "dist/" server.

Do not introduce npm, a bundler, analytics, trackers, cookies, external fonts, remote images, or a framework without a concrete need and explicit review.

## Content rules

Use direct, grounded language:

- "Fit score" is an internal prioritization aid, not an objective probability.
- "Submitted" means the application was owner-confirmed as sent. Submitted cards render in a collapsed history section and show only the approved submission date.
- "Reverify" means the posting state or another volatile fact must be checked.
- Deadline warnings must say that the employer page remains authoritative.

Do not claim sponsorship, compensation, vacancy status, or deadline freshness beyond the snapshot. Preserve "verified_at" and the site notice.

## Update workflow

For a routine data refresh:

1. Obtain the newly reviewed public snapshot from the private process.
2. Update only approved records in "data/jobs.json". For an owner-confirmed submission, set "status" to "submitted", set the date-only "submitted_at" value, and refresh "generated_at"; leave "submitted_at" null for every other lifecycle state.
3. Run "python3 scripts/validate.py".
4. Run "python3 scripts/build.py".
5. Inspect the diff for private material and stale copy.
6. Use a focused feature branch and draft pull request.
7. Let Alan merge unless he explicitly authorizes otherwise.

For interface changes, preserve the data contract and privacy boundary. Update documentation and tests when behavior changes.

## GitHub workflow

The default branch is "master".

- ".github/workflows/validate.yml" runs on pull requests and pushes.
- ".github/workflows/pages.yml" deploys only after a push to "master" or a manual dispatch.
- Deployment requires repository Settings → Pages → Source: GitHub Actions.

Never merge a pull request, enable Pages, change repository visibility, or publish additional data without explicit authorization.

## New-chat bootstrap

When a new chat takes over, the user can say: “Read AGENTS.md in szmyty/scout and continue.”

The agent should:

1. Read this file completely.
2. Read "README.md", "docs/PRIVACY.md", "docs/DATA-CONTRACT.md", "docs/DESIGN.md", and "docs/WORKFLOW.md".
3. Inspect "data/jobs.json".
4. Run validation and build before editing.
5. Check the current branch, open pull requests, Pages workflow, and working-tree state.
6. Access the private source-of-truth repository only if Alan explicitly includes it in the task.
7. Keep one bounded pull request at a time and stop for review.

## Quality bar

A good change makes the queue calmer, clearer, safer, and easier to act on. It preserves truth and privacy, works without hidden services, is accessible on keyboard and mobile, passes validation, and leaves the next agent with less reconstruction work.
