"""Shared helpers for CampusHub's agent hooks."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def event() -> dict:
    """The event the agent harness sends on standard input."""
    return json.load(sys.stdin)


def project_python() -> str:
    """The Python that has CampusHub's dependencies (not necessarily the agent's own).

    Order: $CAMPUSHUB_PYTHON, then .venv in the project (only if it starts on this machine:
    a .venv made on another operating system exists but cannot run), then this interpreter.
    """
    if os.getenv("CAMPUSHUB_PYTHON"):
        return os.environ["CAMPUSHUB_PYTHON"]
    for candidate in (ROOT / ".venv" / "Scripts" / "python.exe", ROOT / ".venv" / "bin" / "python"):
        if candidate.is_file() and _runs(candidate):
            return str(candidate)
    return sys.executable


def _runs(python: Path) -> bool:
    try:
        return subprocess.run([str(python), "-c", "pass"], capture_output=True,
                              timeout=20).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def block(message: str) -> None:
    """Refuse the action; the message goes back to the model."""
    print(message, file=sys.stderr)
    sys.exit(2)
