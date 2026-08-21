# Privacy boundary

Scout is fully public. The source repository, Git history, workflow artifacts,
and deployed files must all be treated as internet-visible.

## Allowed

- Broad, owner-approved career lanes.
- High-level engineering interests and evaluation principles.
- Deliberately delayed aggregate updates that cannot reveal individual targets.
- A public/private publication-boundary statement.

## Prohibited

- Employer or role targets and posting URLs.
- Application state, priority, fit scores, deadlines, verification dates, or
  next actions.
- Resumes, CVs, letters, supplements, screenshots, or submission evidence.
- Email addresses, phone numbers, home addresses, or private correspondence.
- Reference identities or contact details.
- Health, financial, benefits, family, legal, or transition context.
- Private notes, application answers, recruiter messages, or interview notes.
- Private repository URLs, paths, tokens, credentials, or signed links.

## Publication model

Private career operations are canonical. Scout receives only a manually
reviewed, broad projection. It never fetches private data, authenticates an
owner, stores device-local repository settings, or constructs private workspace
links.

## Publication checklist

1. Confirm the update is aggregate and intentionally public.
2. Run "python3 scripts/validate.py".
3. Run "python3 scripts/test_public_boundary.py".
4. Run "python3 scripts/build.py".
5. Inspect the complete source and generated diff.
6. Confirm "data/public-summary.json" is the only data file.
7. Confirm the built artifact contains no live-tracker assets or operational
   records.

Historical remediation, visibility changes, Pages changes, and cache purges
require a separate owner-approved operation.
