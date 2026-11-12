"""stop hook: the agent may not finish while CampusHub's tests fail.

Runs only if the agent changed files in this turn. Re-runs failures once, because one
test (tests/test_reminders.py) is known to be flaky. Exit 2 = not finished yet.

Exception, for the red step of test-driven development (Chapter 12): if the agent changed
only files in tests/ and every failing test is a NEW test (not in the last commit), the
agent may finish - new tests are supposed to fail before the feature exists. Existing
tests must always pass, and test_guard.py stops them from being weakened.
"""
import ast
import subprocess
from pathlib import Path

from _common import ROOT, block, event, project_python


def relative(path: str) -> str:
    p = Path(path.replace("\\", "/"))
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(ROOT)
        except ValueError:
            return path
    return p.as_posix().removeprefix("./")


def committed_tests(path: str) -> set[str]:
    """Names of the test functions in the last commit's version of a file."""
    done = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=ROOT,
                          capture_output=True, text=True)
    try:
        tree = ast.parse(done.stdout) if done.returncode == 0 else None
    except SyntaxError:
        tree = None
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)} if tree else set()


def only_new_tests_fail(output: str, changed: set[str]) -> bool:
    failed = [line.split()[1] for line in output.splitlines()
              if line.startswith(("FAILED ", "ERROR ")) and len(line.split()) > 1]
    if not failed or not all(c.startswith("tests/") for c in changed):
        return False
    for node in failed:
        path, _, name = node.partition("::")
        if path not in changed or not name or name.split("[")[0] in committed_tests(path):
            return False
    return True


e = event()
if not e.get("changed_files"):
    raise SystemExit(0)                       # nothing changed, nothing to check
changed = {relative(p) for p in e["changed_files"]}

python = project_python()
run = subprocess.run([python, "-m", "pytest", "-q", "--disable-warnings"],
                     cwd=ROOT, capture_output=True, text=True)
if run.returncode != 0:
    rerun = subprocess.run([python, "-m", "pytest", "-q", "--lf", "--disable-warnings"],
                           cwd=ROOT, capture_output=True, text=True)
    if rerun.returncode != 0:
        if only_new_tests_fail(rerun.stdout, changed):
            print("test gate: red step - only new tests fail, as expected before the feature "
                  "exists; existing tests pass")
            raise SystemExit(0)
        tail = "\n".join(rerun.stdout.strip().splitlines()[-15:])
        block(f"The test suite fails after your changes. Fix the code (not the tests) "
              f"and finish again.\n{tail}")
print("test gate: " + run.stdout.strip().splitlines()[-1] if run.stdout.strip() else "")
