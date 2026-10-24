# CampusHub

CampusHub is a small campus **events and clubs** platform. Students can browse clubs,
see upcoming events and register for them.

It is the companion project for the book **_The Modern Software Developer_**: you will
explore it, extend it and improve it with AI coding agents chapter by chapter.

> **For learning only.** This code base is deliberately imperfect. Some of its problems
> are exercises in the book, so please do not deploy it or report them as bugs.

## Requirements

- Python 3.12
- Git

## Getting started

```bash
git clone https://github.com/mdt01/campushub.git
cd campushub
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m scripts.seed             # optional: load sample data
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API.

## Running the tests

```bash
pytest -q
```

## Project layout

```
app/
  main.py            FastAPI application
  config.py          settings
  database.py        SQLite engine and sessions
  models.py          Club, Event, Student, Registration
  schemas.py         request/response models
  utils.py           helper functions
  routers/           clubs, events, registrations endpoints
  services/          registration rules (capacity, duplicates)
scripts/seed.py      sample data
tests/               pytest test suite
frontend/            web interface (coming soon)
labs/                code for the book's chapter labs (see labs/README.md)
.agents/commands/    RePPIT workflow prompts (research, propose, design, implement, review) - Chapter 6
.agents/commands/readiness-audit.md  agent-readiness audit - Chapter 11
.agents/skills/      agent skills: verify-change, release-notes, grill-me - Chapter 9
.agents/hooks.json   hooks (guard, post-edit check, stop-time test gate) - Chapter 10
.agents/agents/      subagents: explorer, planner, reviewer - Chapter 10
mcp_server/          MCP server for agents (list, search, register) - Chapter 7
```

## API overview

| Method | Path | Purpose |
|---|---|---|
| GET | /clubs | List clubs |
| POST | /clubs | Create a club |
| GET | /events | List events (`?upcoming_only=true`) |
| GET | /events/search?q= | Search events by title |
| POST | /events | Create an event |
| POST | /students | Create a student |
| POST | /events/{id}/register | Register a student |
| DELETE | /events/{id}/register/{student_id} | Cancel a registration |
| GET | /events/{id}/attendees | List attendees |

## Licence

MIT — see [LICENSE](LICENSE).
