# 🧭 Scout

A privacy-preserving public career compass.

Scout communicates Alan Szmyt's broad engineering direction without publishing
the live application strategy behind it. The public site contains three reviewed
focus areas and a clear publication boundary. Employer and role targets,
application state, deadlines, scores, next actions, materials, correspondence,
and decision context stay private.

## Public surface

- Platform and developer experience as the primary lane.
- Research and AI-assisted systems as the secondary lane.
- Mobile and geospatial systems as a targeted differentiator.
- A deliberately aggregate, manually reviewed publication model.

Scout is not a job board, application queue, progress feed, or source of live
career operations.

## Architecture

Scout is a dependency-free static site:

- "index.html" contains the complete semantic experience.
- "assets/styles.css" owns the responsive visual system.
- "data/public-summary.json" is the only allowed public data file.
- "scripts/validate.py" enforces the aggregate-only contract.
- "scripts/test_public_boundary.py" proves live application fields are rejected.
- "scripts/build.py" copies a strict allowlist into "dist/".
- GitHub Actions validates pull requests and publishes after merge.

Read [AGENTS.md](AGENTS.md) before changing data or behavior.

## Local validation

```console
python3 scripts/validate.py
python3 scripts/test_public_boundary.py
python3 scripts/build.py
python3 -m http.server --directory dist 8000
```

Then open "http://localhost:8000/".

## Publishing

The repository uses the "master" branch. GitHub Pages deploys the allowlisted
"dist/" artifact after a reviewed merge.

Expected project-site URL: <https://szmyty.github.io/scout/>

## Privacy

The repository, history, workflow artifacts, and deployed site are public. Only
reviewed aggregate direction belongs here. See [docs/PRIVACY.md](docs/PRIVACY.md).

## License

[MIT](LICENSE)
