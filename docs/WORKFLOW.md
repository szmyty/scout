# Maintenance workflow

## Refreshing jobs

1. Complete research and private review outside this repository.
2. Copy only the approved public snapshot into "data/jobs.json".
3. Run validation and the deterministic build.
4. Review every changed line.
5. Open a focused draft pull request.
6. Merge only after Alan's review.

## Recording a confirmed submission

1. Confirm the application was sent; do not infer it from a saved draft, opened portal, or recruiter conversation.
2. In `data/jobs.json`, set `status` to `submitted`, set `submitted_at` to the owner-approved `YYYY-MM-DD` date, and refresh `generated_at`.
3. Keep `submitted_at` as `null` for every non-submitted record. Do not add confirmation links, packet names, portal URLs, correspondence, times, or private notes.
4. Run validation and the deterministic build, review the exact diff, then open a focused draft PR.
5. After merge to `master`, GitHub Pages deploys the new static snapshot. The submitted card appears in the closed history section automatically.

## Changing the site

Keep behavior dependency-free unless a reviewed requirement justifies more infrastructure. Test:

- Empty and no-match states.
- Every filter and sort.
- Owner mode save and clear behavior.
- Keyboard navigation.
- Narrow viewport wrapping.
- Relative URLs under the "/scout/" GitHub Pages path.

## Publishing

Pull requests run validation only. A merge to "master" runs validation, creates the allowlisted static artifact, and deploys it through GitHub Pages.

If the deployment workflow reports that Pages is not configured, set repository Settings → Pages → Source to "GitHub Actions" and rerun the workflow. This is a one-time repository setting.
