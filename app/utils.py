# helper functions used across the app

from datetime import datetime, timedelta


def seats_left(event):
    return event.capacity - len(event.registrations)


def is_upcoming(event, now=None):
    now = now or datetime.now()
    return event.starts_at > now


def reminder_due(event, now=None):
    # send reminder 24 hours before the event
    now = now or datetime.now()
    diff = event.starts_at - now
    return timedelta(0) < diff <= timedelta(hours=24)


def format_event_line(e):
    return "%s | %s | %s" % (e.starts_at.strftime("%d %b %Y %H:%M"), e.title, e.venue)
