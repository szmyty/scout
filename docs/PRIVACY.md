# Privacy boundary

Scout is fully public. The source repository, Git history, workflow artifacts, and deployed files must all be treated as internet-visible.

## Allowed

- Public employer and role names.
- Public posting URLs.
- Coarse location and country.
- Reviewed fit score, priority, status, deadline, verification date, and owner-approved day-level submission date.
- Short public-safe summary and next action.

## Prohibited

- Resumes, CVs, letters, supplements, screenshots, or submission evidence.
- Email addresses, phone numbers, home addresses, or private correspondence.
- Reference identities or contact details.
- Health, financial, benefits, family, legal, or transition context.
- Private notes, application answers, recruiter messages, or interview notes.
- Private repository URLs, private paths, tokens, credentials, or signed links.

## Owner mode

Owner mode stores an optional repository URL and branch in the current browser's local storage. The repository URL is never committed, transmitted to Scout, or included in analytics because Scout has no analytics. No token is collected.

The resulting workspace link is a normal browser navigation. GitHub remains responsible for authentication and authorization.

## Publication checklist

1. Validate the snapshot.
2. Inspect the full diff.
3. Confirm every URL is intentionally public.
4. Search for contact information and document filenames.
5. Confirm status wording reveals no private correspondence; show submission dates only after the owner confirms them and never publish times or evidence.
6. Build from the allowlist and inspect the generated file inventory.
