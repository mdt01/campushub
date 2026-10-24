Audit how ready this repository is for coding agents. Focus: $ARGUMENTS

Part 1 - measure (deterministic):
1. Run `python -m minicode.readiness . --run-tests 5` if minicode is installed;
   otherwise check the same things by hand: README setup and test steps, an agent
   file, one test command, linter and formatter config, CI, type hints, a dev
   container, secrets in code, test speed and stability.
2. Time a clean setup: follow the README exactly, as a new student would. Note
   every step that was missing, wrong or needed a guess.

Part 2 - judge (what a script cannot see). For each item give PASS, PARTIAL or
FAIL with one line of evidence (file:line or command output):
- Docs agree with the code (commands, folder names, Python version).
- Module boundaries are clear: routers stay thin, rules live in services.
- One way to do each thing (one HTTP client, one date style, one error style).
- No dead code, commented-out blocks or unused files.
- Test failures are legible: names say what broke; assertions show values.
- An agent could find its next task: open TODOs, issues or a roadmap.

Part 3 - report. Write readiness/report.md with:
- The scorecard: level, checks passed, and one line per pillar.
- The top five gaps, ordered by (effect on agents) / (effort to fix). For each:
  the problem, the evidence, the fix, and an estimate (minutes or hours).
- A draft GitHub issue for each of the five gaps (title, body, done-when).
Do not fix anything in this command; only measure, judge and report.
