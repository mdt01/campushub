# CampusHub endpoints and what "working" means

| Endpoint | Expected behaviour |
|---|---|
| GET /health | 200, {"status": "ok"} |
| GET /clubs | 200, list of clubs |
| GET /events | 200, events ordered by starts_at, each with seats_left |
| GET /events?upcoming_only=true | 200, only events in the future |
| GET /events/search?q=TEXT | 200, events whose title contains TEXT |
| POST /events | 201 with the event; 404 if club_id does not exist |
| POST /students | 201 with the student |
| POST /events/{id}/register | 201; 400 if full or already registered |
| DELETE /events/{id}/register/{student_id} | 204; 404 if not registered |
| GET /events/{id}/attendees | 200, list of registered students |

When a change touches one of these endpoints, add a check for it to scripts/smoke.py.
