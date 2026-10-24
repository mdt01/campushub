"""Smoke test for CampusHub: python .agents/skills/verify-change/scripts/smoke.py

Runs the real app in-process against a fresh temporary SQLite database, seeds it, and
checks the main endpoints. Prints PASS/FAIL per check; exit code 1 if anything failed.
"""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]          # the campushub folder
sys.path.insert(0, str(ROOT))
db_file = Path(tempfile.mkdtemp()) / "smoke.db"
os.environ["CAMPUSHUB_DB"] = f"sqlite:///{db_file}"   # never touch the real database

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from scripts.seed import seed  # noqa: E402

seed()
client = TestClient(app)
results = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}{'  - ' + detail if detail and not ok else ''}")


r = client.get("/health")
check("GET /health", r.status_code == 200 and r.json() == {"status": "ok"}, r.text)
r = client.get("/clubs")
check("GET /clubs returns clubs", r.status_code == 200 and len(r.json()) > 0, r.text)
r = client.get("/events")
events = r.json() if r.status_code == 200 else []
check("GET /events returns events", r.status_code == 200 and len(events) > 0, r.text)
check("events have seats_left", all("seats_left" in e for e in events))
r = client.get("/events", params={"upcoming_only": True})
check("GET /events?upcoming_only=true", r.status_code == 200, r.text)
r = client.get("/events/search", params={"q": "Open"})
check("GET /events/search?q=Open", r.status_code == 200 and len(r.json()) > 0, r.text)
if events:
    eid = events[0]["id"]
    r = client.post(f"/events/{eid}/register", json={"student_id": 1})
    check("POST register student 1", r.status_code == 201, r.text)
    r = client.get(f"/events/{eid}/attendees")
    check("GET attendees includes student", r.status_code == 200 and len(r.json()) == 1, r.text)

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
