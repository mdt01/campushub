"""A DELIBERATELY POOR MCP server for Lab 8. Do not copy its style!

It mirrors every CampusHub endpoint one-to-one, uses vague names, untyped dictionary
arguments, raw JSON output and unhelpful errors. Your job in Lab 8 is to measure how
badly agents do with it, then refactor it into a few outcome-oriented tools.
"""
import json
import os

import httpx
from mcp.server.mcpserver import MCPServer

http = httpx.Client(base_url=os.getenv("CAMPUSHUB_URL", "http://127.0.0.1:8000"), timeout=10)
mcp = MCPServer("campushub-naive")


def raw(method: str, path: str, **kwargs) -> str:
    response = http.request(method, path, **kwargs)
    if response.status_code >= 400:
        return "error"                                  # unhelpful on purpose
    return json.dumps(response.json()) if response.content else "ok"


@mcp.tool()
def get_clubs() -> str:
    """Get clubs."""
    return raw("GET", "/clubs")


@mcp.tool()
def get_club(id: int) -> str:
    """Get club."""
    return raw("GET", f"/clubs/{id}")


@mcp.tool()
def post_club(data: dict) -> str:
    """Create club."""
    return raw("POST", "/clubs", json=data)


@mcp.tool()
def get_events(params: dict) -> str:
    """Get events."""
    return raw("GET", "/events", params=params)


@mcp.tool()
def get_event(id: int) -> str:
    """Get event."""
    return raw("GET", f"/events/{id}")


@mcp.tool()
def search(q: str) -> str:
    """Search."""
    return raw("GET", "/events/search", params={"q": q})


@mcp.tool()
def post_event(data: dict) -> str:
    """Create event."""
    return raw("POST", "/events", json=data)


@mcp.tool()
def post_student(data: dict) -> str:
    """Create student."""
    return raw("POST", "/students", json=data)


@mcp.tool()
def post_registration(id: int, data: dict) -> str:
    """Register."""
    return raw("POST", f"/events/{id}/register", json=data)


@mcp.tool()
def delete_registration(id: int, sid: int) -> str:
    """Cancel."""
    return raw("DELETE", f"/events/{id}/register/{sid}")


@mcp.tool()
def get_attendees(id: int) -> str:
    """Attendees."""
    return raw("GET", f"/events/{id}/attendees")


@mcp.tool()
def get_seats(id: int) -> str:
    """Seats."""
    event = json.loads(raw("GET", f"/events/{id}"))
    return str(event["seats_left"])


@mcp.tool()
def get_capacity(id: int) -> str:
    """Capacity."""
    return str(json.loads(raw("GET", f"/events/{id}"))["capacity"])


@mcp.tool()
def check_event(id: int) -> str:
    """Check event."""
    return "yes" if raw("GET", f"/events/{id}") != "error" else "no"


@mcp.tool()
def get_health() -> str:
    """Health."""
    return raw("GET", "/health")


if __name__ == "__main__":
    mcp.run()
