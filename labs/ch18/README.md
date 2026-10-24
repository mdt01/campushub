# Lab 18: a mini software factory

    # 1. a spec goes in
    cat specs/registration-window.toml
    # 2. run the factory, pausing for a human to approve the plan
    python -m minicode.factory run specs/registration-window.toml --repo . \
        --python .venv/bin/python --pause-after plan          # Windows: .venv\Scripts\python.exe
    cat .minicode/factory/<run>-plan.md
    python -m minicode.factory approve <run> --repo . --python .venv/bin/python
    # 3. read the report, then review the branch factory/<run> like any pull request
    cat .minicode/factory/<run>-report.md

Stages: plan -> implement -> verify (tests, security scan of changed files, checker
agent) -> publish (commit; --open-pr for a draft PR) -> preview (the app on a free port
with a throw-away database, smoke checks over HTTP, log watcher).

Write your own spec from specs/TEMPLATE.toml. Never merge a factory branch without
reading it.
