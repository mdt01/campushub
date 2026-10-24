---
name: verify-change
description: Verify that a change to CampusHub works before calling it done. Use after editing any code in app/ or tests/, when asked to "check", "verify" or "test" a change, or before writing a summary of finished work.
---
# Verify a CampusHub change

Never report a change as done until every step below has passed. Report the real output.

1. **Unit and integration tests.** Run `python -m pytest -q`.
   One test, `tests/test_reminders.py`, is known to be flaky. If it alone fails, run it
   again once; if it fails twice, report it.
2. **Smoke test the running app.** Run `python .agents/skills/verify-change/scripts/smoke.py`.
   It starts the app in-process on a temporary database, seeds it, calls the main
   endpoints and prints PASS or FAIL for each. It exits with a non-zero code on failure.
3. **Check the diff.** Run `git diff --stat` and confirm that only the files you meant
   to change are listed. Run `git diff` and look for debug prints and commented-out code.
4. **Report.** Write a short summary: what changed, the test result line
   (e.g. "17 passed"), the smoke result ("8/8 checks passed") and anything you could not verify.

For what each endpoint should return, read `references/endpoints.md` (only if you need it).

If a step fails, fix the cause and start again from step 1. Do not edit or delete a test
to make it pass unless the user asked you to change that behaviour.
