# 🧭 Scout

A public, privacy-safe job-application queue and research-career scouting dashboard.

Scout turns a reviewed static snapshot into a calm operational view: what is submitted, what is being prepared, which deadlines are close, which listings need reverification, and what to do next.

## What it does

- Displays the public-safe research software opportunity queue.
- Searches and filters by status, priority, lane, and country.
- Sorts by recommendation, deadline, fit score, or employer.
- Highlights urgent deadlines without pretending stale postings are current.
- Keeps owner-confirmed submissions in a collapsed history section with date-level status only.
- Offers an optional owner mode that stores a private repository URL only in the owner's browser and opens the matching private workspace through the owner's existing GitHub session.
- Publishes no resumes, letters, references, contact details, private notes, or credentials.

## Architecture

Scout is a dependency-free static site. Routine status refreshes are a small, validated edit to `data/jobs.json`; see [the maintenance workflow](docs/WORKFLOW.md).


- "index.html" — accessible document shell.
- "assets/styles.css" — responsive visual system.
- "assets/app.js" — rendering, filters, sorting, copy actions, and owner mode.
- "data/jobs.json" — reviewed public snapshot.
- "scripts/validate.py" — data and privacy validation.
- "scripts/build.py" — deterministic allowlisted build into "dist/".
- ".github/workflows/" — pull-request validation and GitHub Pages deployment after merge.

Read [AGENTS.md](AGENTS.md) before changing data or behavior.

## Local use

Run:

    python3 scripts/validate.py
    python3 scripts/build.py
    python3 -m http.server --directory dist 8000

Then open "http://localhost:8000/scout/" only if serving the repository under a "scout" prefix, or "http://localhost:8000/" for the generated root directly.

## Publishing

The repository uses the "master" branch. After the setup PR is merged, enable GitHub Pages with "GitHub Actions" as the source in repository settings if it is not already enabled. The deployment workflow publishes the validated "dist/" artifact.

Expected project-site URL:

https://szmyty.github.io/scout/

## Privacy

The public site is intentionally lossy. Its source data is reviewed before it enters this repository. Owner mode stores configuration only in browser local storage; it publishes no private repository URL or token and never fetches private data.

## License

[MIT](LICENSE)

## Decision model

[PursuitEV](docs/PURSUIT-EV.md) documents the versioned decision aid used privately to prioritize sustainable applications. Scout never publishes the private inputs, estimates, or application materials behind a queue record.
