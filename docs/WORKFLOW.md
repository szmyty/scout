# Maintenance workflow

## Updating public direction

1. Complete career research and application work outside this repository.
2. Produce only a broad, deliberately aggregate public projection.
3. Review it against "docs/PRIVACY.md".
4. Replace "data/public-summary.json" without adding fields or files.
5. Synchronize visible static copy when positioning changes.
6. Run validation, boundary tests, and the deterministic build.
7. Review every changed line.
8. Open a focused draft pull request.
9. Merge only after Alan's review.

## Required checks

```console
python3 scripts/validate.py
python3 scripts/test_public_boundary.py
python3 scripts/build.py
```

Test the semantic shell at narrow and desktop widths, with keyboard navigation
and reduced motion.

## Publishing

Pull requests validate only. A merge to "master" validates, builds the strict
allowlisted artifact, and deploys it through GitHub Pages.

History rewrites, repository visibility changes, and Pages changes are separate
owner-approved operations.
