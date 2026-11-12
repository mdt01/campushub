# Lab 14: find, triage, fix and harden

CampusHub still contains two planted security flaws (Chapters 12-13 pointed at them).
This folder holds what you need to find and fix them, and to harden your agent set-up.

| File | Use |
|---|---|
| `semgrep-rules.yml` | Two team rules: SQL built with f-strings, secret-looking literals |
| `security.yml` | A CI workflow to copy into `.github/workflows/` after you fix the findings |
| `Dockerfile.sandbox` | An image for running agent shell commands with no network |
| `reference-fix.patch` | One possible fix - compare with yours *after* you finish |

    # scanners in their own venv: semgrep upgrades starlette and pydantic, which breaks CampusHub
    python -m venv .venv-sec && .venv-sec/bin/pip install bandit semgrep pip-audit detect-secrets
    .venv-sec/bin/bandit -q -r app                    # Windows: .venv-sec\Scripts\bandit
    .venv-sec/bin/semgrep scan --metrics=off --config labs/ch14/semgrep-rules.yml app
    .venv-sec/bin/pip-audit -r requirements.txt       # builds a temporary venv from PyPI
    .venv-sec/bin/pip-audit --path .venv/lib/python3.12/site-packages   # or: audit what is installed
    .venv-sec/bin/detect-secrets scan app scripts

    # triage in read-only mode, then fix in a sandbox
    python -m minicode --workspace . --mode read-only
    docker build -t campushub-sandbox -f labs/ch14/Dockerfile.sandbox .
    python -m minicode --workspace . --sandbox docker --sandbox-image campushub-sandbox

Permission rules for agents are in `.agents/permissions.json`; every tool call is
logged to `.minicode/audit.jsonl`.

After the fix, pip-audit still reports the dependency advisories (starlette, pytest) until you upgrade
FastAPI and pytest, so the SCA step in `security.yml` starts as advisory (`continue-on-error`). Make it
blocking once the dependencies are upgraded.
