from datetime import datetime, timedelta
from types import SimpleNamespace

from app.utils import is_upcoming, reminder_due
from tests.conftest import make_student


def test_reminder_due_within_a_day():
    event = SimpleNamespace(starts_at=datetime.now() + timedelta(hours=5))
    assert reminder_due(event)


def test_no_reminder_for_next_week():
    event = SimpleNamespace(starts_at=datetime.now() + timedelta(days=7))
    assert not reminder_due(event)


def test_event_starting_now_is_still_upcoming(client):
    event = SimpleNamespace(starts_at=datetime.now() + timedelta(milliseconds=30))
    for i in range(3):
        make_student(client, f"22CE10{i}")
    assert is_upcoming(event)
