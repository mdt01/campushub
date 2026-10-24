"""Test the MCP server in-process, with a fake CampusHub API (no network needed)."""
import json
from datetime import datetime, timedelta

import pytest

pytest.importorskip("mcp")      # these tests run in the MCP environment, not CampusHub's

import anyio  # noqa: E402
import httpx  # noqa: E402
from mcp import Client  # noqa: E402

from mcp_server import server  # noqa: E402

SOON = (datetime.now() + timedelta(days=3)).replace(microsecond=0).isoformat()
LATER = (datetime.now() + timedelta(days=90)).replace(microsecond=0).isoformat()
EVENTS = [
    {"id": 1, "title": "Intro to Open Source", "venue": "Hall A", "starts_at": SOON,
     "capacity": 50, "seats_left": 3, "club_id": 1},
    {"id": 2, "title": "Robotics Expo", "venue": "Ground", "starts_at": LATER,
     "capacity": 200, "seats_left": 150, "club_id": 2},
]


def fake_api(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path == "/events":
        return httpx.Response(200, json=EVENTS)
    if path == "/events/search":
        q = request.url.params["q"].lower()
        return httpx.Response(200, json=[e for e in EVENTS if q in e["title"].lower()])
    if path == "/events/1/register":
        if json.loads(request.content)["student_id"] == 7:
            return httpx.Response(400, json={"detail": "Event is full"})
        return httpx.Response(201, json={"id": 99})
    if path == "/clubs":
        return httpx.Response(200, json=[{"id": 1, "name": "Coding Club", "description": "Code"}])
    return httpx.Response(404, json={"detail": "Not found"})


def run(coro_fn):
    server.http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(fake_api))
    return anyio.run(coro_fn)


def text(result) -> str:
    return result.content[0].text


def test_tools_are_discoverable():
    async def go():
        async with Client(server.mcp) as client:
            return sorted(t.name for t in (await client.list_tools()).tools)
    assert run(go) == ["campushub_register_student", "campushub_search_events",
                       "campushub_upcoming_events"]


def test_upcoming_events_respects_days():
    async def go():
        async with Client(server.mcp) as client:
            return await client.call_tool("campushub_upcoming_events", {"days": 30})
    result = run(go)
    assert "#1 Intro to Open Source" in text(result) and "Robotics" not in text(result)


def test_api_errors_reach_the_model_as_tool_errors():
    async def go():
        async with Client(server.mcp) as client:
            return await client.call_tool("campushub_register_student",
                                          {"event_id": 1, "student_id": 7})
    result = run(go)
    assert result.is_error and "Event is full" in text(result)


def test_resource_and_prompt():
    async def go():
        async with Client(server.mcp) as client:
            clubs = await client.read_resource("campushub://clubs")
            prompt = await client.get_prompt("weekly_digest", {"audience": "seniors"})
            return clubs, prompt
    clubs, prompt = run(go)
    assert "Coding Club" in clubs.contents[0].text
    assert "seniors" in prompt.messages[0].content.text
