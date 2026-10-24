"""CampusHub MCP server: lets any MCP-capable agent list, search and register for events.

It is a thin wrapper in front of the CampusHub REST API, so the API must be running:
    uvicorn app.main:app                      (in the campushub folder, terminal 1)

Run the server locally over stdio (the agent starts it as a subprocess):
    python mcp_server/server.py
or as a remote server over streamable HTTP:
    python mcp_server/server.py --http --port 8765      -> http://127.0.0.1:8765/mcp
"""
import argparse
import logging
import os
from datetime import datetime, timedelta

import httpx
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

API_URL = os.getenv("CAMPUSHUB_URL", "http://127.0.0.1:8000")
http = httpx.Client(base_url=API_URL, timeout=10)    # tests replace this client
logging.getLogger("httpx").setLevel(logging.WARNING)  # keep the agent's terminal quiet

mcp = MCPServer(
    "campushub",
    instructions="Tools for CampusHub, a college events platform. Use them to find "
                 "events and register students. Dates are local time.",
)


def call_api(method: str, path: str, **kwargs) -> list | dict:
    """Call the API; turn failures into errors the model can act on."""
    try:
        response = http.request(method, path, **kwargs)
    except httpx.ConnectError:
        raise ToolError(f"CampusHub API is not reachable at {API_URL}. "
                        "Ask the user to start it with: uvicorn app.main:app")
    if response.status_code >= 400:
        detail = response.json().get("detail", response.text)
        raise ToolError(f"CampusHub refused the request ({response.status_code}): {detail}")
    return response.json() if response.content else {}


def event_line(e: dict) -> str:
    when = datetime.fromisoformat(e["starts_at"]).strftime("%a %d %b %Y, %H:%M")
    return (f"#{e['id']} {e['title']} | {when} | {e['venue']} | "
            f"{e['seats_left']} of {e['capacity']} seats left")


@mcp.tool()
def campushub_upcoming_events(days: int = 30) -> str:
    """List CampusHub events starting in the next `days` days, soonest first.

    Each line shows the event id (needed for registration), title, start time,
    venue and seats left.
    """
    cutoff = datetime.now() + timedelta(days=days)
    upcoming = call_api("GET", "/events", params={"upcoming_only": True})
    events = [e for e in upcoming
              if datetime.fromisoformat(e["starts_at"]) <= cutoff]
    if not events:
        return f"No events in the next {days} days."
    return "\n".join(event_line(e) for e in events)


@mcp.tool()
def campushub_search_events(query: str) -> str:
    """Find CampusHub events whose title contains `query` (case-insensitive)."""
    events = call_api("GET", "/events/search", params={"q": query})
    return "\n".join(event_line(e) for e in events) or f"No events match '{query}'."


@mcp.tool()
def campushub_register_student(event_id: int, student_id: int) -> str:
    """Register a student for an event. Fails if the event is full or the student is
    already registered. Use campushub_search_events first to find the event id."""
    registration = call_api("POST", f"/events/{event_id}/register",
                            json={"student_id": student_id})
    return (f"Registered student {student_id} for event {event_id} "
            f"(registration #{registration['id']}).")


@mcp.resource("campushub://clubs", mime_type="text/plain")
def clubs() -> str:
    """All CampusHub clubs with their ids and descriptions."""
    return "\n".join(f"#{c['id']} {c['name']}: {c['description']}"
                     for c in call_api("GET", "/clubs"))


@mcp.prompt()
def weekly_digest(audience: str = "first-year students") -> str:
    """A ready-made request: summarize this week's events for an audience."""
    return (f"Use campushub_upcoming_events with days=7 and write a short, friendly "
            f"digest of this week's events for {audience}. Group by day and mention "
            f"events that are nearly full.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CampusHub MCP server")
    parser.add_argument("--http", action="store_true", help="serve over streamable HTTP")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.http:
        mcp.run("streamable-http", host="127.0.0.1", port=args.port)
    else:
        mcp.run()                                         # stdio
