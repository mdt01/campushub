# Lab 13: seeded bugs for the review pipeline

`seeded-bugs.patch` adds a venue filter and a capacity-editing endpoint to CampusHub.
It also contains five deliberate bugs, listed in `seeded-bugs.json`. All existing tests
still pass with the patch applied - which is the point.

    git switch -c lab13-seeded
    git apply labs/ch13/seeded-bugs.patch
    python -m pytest -q                      # still green
    python -m minicode.review --base main --expect labs/ch13/seeded-bugs.json

On Windows, if `git apply` reports whitespace errors, use
`git apply --ignore-whitespace labs/ch13/seeded-bugs.patch`.

Each bug in `seeded-bugs.json` lists keywords. A finding counts as a catch only if it is in
the same file, within 10 lines, and mentions one of them: models often get line numbers
wrong by a few lines, and a line window alone credits the wrong bug (found in Lab 13).
Still triage the other findings by hand.

Do not read `seeded-bugs.json` before you have reviewed the diff yourself (Step 1).
Never merge this branch.
