# Lab 14: find, triage, fix and harden

CampusHub still contains two planted security flaws (Chapters 12-13 pointed at them).
This folder holds what you need to find and fix them, and to harden your agent set-up.

| File | Use |
|---|---|
| `semgrep-rules.yml` | Two team rules: SQL built with f-strings, secret-looking literals |
| `security.yml` | A CI workflow to copy into `.github/workflows/` after you fix the findings |
| `Dockerfile.sandbox` | An image for running agent shell commands with no network |
| `reference-fix.patch` | One possible fix - compare with yours *after* you finish |

    pip install bandit semgrep pip-audit
    bandit -q -r app
    semgrep scan --metrics=off --config labs/ch14/semgrep-rules.yml app
    pip-audit -r requirements.txt

    # triage in read-only mode, then fix in a sandbox
    python -m minicode --workspace . --mode read-only
    docker build -t campushub-sandbox -f labs/ch14/Dockerfile.sandbox .
    python -m minicode --workspace . --sandbox docker --sandbox-image campushub-sandbox

Permission rules for agents are in `.agents/permissions.json`; every tool call is
logged to `.minicode/audit.jsonl`.
