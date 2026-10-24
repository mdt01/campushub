# CampusHub review rules

Read by human reviewers and by AI review agents (`python -m minicode.review`).
Each rule exists because we got it wrong once. Severity in brackets.

## Always flag
- [blocker] SQL built with f-strings, `%` or `+`. Use the ORM or `text()` with
  bound parameters (`:name`).
- [blocker] Secrets, tokens or passwords in code, tests or config defaults.
- [blocker] A change that lets registrations exceed capacity, or lets one student
  act on another student's registration.
- [major] Errors returned as a 200 response body. Raise `HTTPException`: 404 for
  missing rows, 400 or 409 for bad requests or conflicts.
- [major] New request fields without validation (e.g. counts must be positive:
  use `Field(gt=0)`).
- [major] New or changed behaviour without a test in `tests/`.
- [major] A test deleted, skipped or weakened in the same change as the code.
- [minor] Business rules in a router. Routers stay thin; rules live in `app/services/`.

## Do not flag
- Style that `ruff` checks or formats automatically.
- The naive datetimes used throughout `app/models.py` (a known, tracked decision).
- Missing docstrings on small private helpers.
- Suggestions to add new libraries or rewrite modules that the change did not touch.

## Context
- Owners: `app/services/` - registrations team; `app/routers/` - API team.
- A change that touches `app/services/registration_service.py` needs a human
  approval from the registrations team, whatever the AI review says.
