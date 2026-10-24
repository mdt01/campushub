"""Check for the keep-ci-green loop (Chapter 16): exit 0 only if the suite is reliably green.

Every test file is run LOOP_RUNS times (default 20), in one pytest process. A test that fails even once
is treated as failing: for an agent, a flaky test is a broken test. The output names the
failing test so the maker knows where to start.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents" / "hooks"))
from _common import project_python  # noqa: E402

runs = int(os.getenv("LOOP_RUNS", "20"))
files = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "tests").glob("test_*.py"))
# One pytest process; --keep-duplicates collects every file `runs` times.
done = subprocess.run([project_python(), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                       "--disable-warnings", "--keep-duplicates", *files * runs],
                      cwd=ROOT, capture_output=True, text=True)
lines = done.stdout.strip().splitlines()
if done.returncode != 0:
    failing = sorted({line for line in lines if line.startswith("FAILED")})
    print(f"NOT GREEN: {len(files)} test files x {runs} runs.")
    print("\n".join(failing))
    print("\nLast lines of output:")
    print("\n".join(lines[-25:]))
    sys.exit(1)
print(f"GREEN: {len(files)} test files x {runs} runs. {lines[-1] if lines else ''}")
